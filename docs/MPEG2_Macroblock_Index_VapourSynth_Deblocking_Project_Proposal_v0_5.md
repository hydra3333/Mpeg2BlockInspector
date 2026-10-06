# MPEG-2 Macroblock Index + VapourSynth Deblocking - Project Proposal v0.5

**Status:** Discussion proposal. No coding approved. Supersedes v0.4 (move v0.4 to `superseded/`).
**Date:** 2026-10-06
**Scope:** MPEG-2 post-processing/deblocking for legally recorded MPEG-2 captures, using an externally generated macroblock metadata index and a VapourSynth API4 C++/AVX2 filter, if and only if the feasibility gate (section 3) is passed.

---

## 0. How to read this document

Every substantive statement carries one of these labels, stated or implied by its section heading:

- **DECIDED** - Dave has ratified it.
- **CARRIED** - taken from v0.2 as "currently favoured"; not yet re-ratified by Dave in this version.
- **PROPOSAL** - a suggested course of action, not a fact.
- **HYPOTHESIS** - a technical belief from general knowledge, NOT verified. May be wrong. Must be checked against ISO/IEC 13818-2, the reference decoder source, or experiment before it is relied on.
- **RESEARCHED** - found in a cited source (citation required).
- **VERIFIED** - demonstrated by test or by reading the source cold (file:line).

Nothing in this document is DECIDED unless Dave says so. Section 11 records his rulings; anything not recorded there is not DECIDED.

This document is a proposal, not an authority. Where it conflicts with a ratified specification, the specification wins.

---

## 1. Project intent

**PROPOSAL.** Investigate and, only if technically justified, build a VapourSynth MPEG-2 deblocking filter that combines:

1. decoded frames from BestSource/VapourSynth; and
2. an externally generated binary macroblock index (`.idx2`) produced by an instrumented MPEG-2 reference decoder.

**CARRIED.** This is a fresh project, not a continuation of Deblock4. Nothing from Deblock4 is inherited by default.

**CARRIED.** C++ (not Zig), VapourSynth API4, Windows, AVX2 as the SIMD target, one global user-selected strength, external index generation (not a VapourSynth graph filter), scalar/reference implementation before AVX2.

---

## 2. Corrected premise: what the index can and cannot add

**HYPOTHESIS (corrects v0.2 section 3).**

For uncropped, unscaled MPEG-2, the 8x8 and 16x16 grid positions are fixed by the pixel grid, so the index does not "reveal where the boundaries are". The value of the index is the information the pixels cannot supply:

- per-macroblock quantiser (a scale for how strong blocking is likely to be);
- intra / inter / skipped status;
- frame DCT versus field DCT, per macroblock;
- picture type and picture structure;
- possibly coded-block pattern and coefficient activity (to be established by research, not assumed).

**HYPOTHESIS arising from Dave's prior recollection; accepted as a research question, not as established MPEG-2 fact.** Dave's starting recollection was that MPEG-2 blocking is complex and can sometimes mix field- and frame-related blocking within the same displayed frame, so saying that all relevant boundary positions are simply fixed by the pixel grid is incomplete. A likely mechanism is per-macroblock frame-DCT versus field-DCT selection in frame pictures, but the exact transform geometry, seam locations, neighbouring mixed-DCT behaviour, and significance to visible blocking must be verified against ISO/IEC 13818-2, the reference decoder, and experiment before the algorithm relies on it. If verified, this may be one of the strongest justifications for carrying codec metadata in the index.

**HYPOTHESIS, to verify against the standard:** for 4:2:0, field/frame DCT reordering applies to luma only and chroma blocks keep a fixed arrangement. Dave thinks there may be chroma blocking based on hazy recall of historical posts online so the issue needs to be researched to confirm or otherwise.

---

## 3. Order of work (single authoritative order)

**DECIDED (D-01).** This replaces the conflicting orderings in v0.2 (its revised strategy versus its sections 5, 19, 20 and 21). Each stage ends in a stop/continue point for Dave.

| Stage | Work | Exit criterion |
|---|---|---|
| 0 | Conceptual algorithm design (no code). Section 4. | Dave ratifies a written concept document |
| 1 | Evidence tooling: ground-truth test material; throwaway inspector writing a DRAFT binary .idx2 (display order, versioned); throwaway Python analyzer reading it and printing readable summaries; baseline comparison where research shows it is meaningful. Sections 6.5, 7. | Test set, readable analyzer summaries and baseline results exist |
| 2 | Python reference prototype of the concept; experiments on test set and real clips | Measured result, positive or negative |
| **Gate** | Feasibility gate (below) | Dave decides: continue, revise, or stop |
| 3 | Freeze `.idx2` specification, including mandatory validity fields | Spec ratified |
| 4 | Inspector rebuilt as a minimal diff against the pristine reference decoder. Section 6. | Diff reviewed; output matches spec |
| 5 | Prove `.idx2` record N = VapourSynth frame N on representative material | Test report, including failure cases |
| 6 | C++ scalar implementation, validated against the Python prototype | Matches the oracle |
| 7 | VapourSynth API4 wrapper | Loads, validates index, filters |
| 8 | AVX2, scalar kept as reference | Bit-identical or documented tolerance |
| 9 | Acceptance on real captures | Criteria from section 7 met |

The throwaway inspector in Stage 1 is explicitly NOT authoritative. Its output is used only to find out what metadata is useful; the real inspector is rebuilt at Stage 4.

### Feasibility gate (carried from v0.2, unchanged in substance)

Do not commit to Stage 3 onward until a credible candidate algorithm is shown to be: technically plausible; materially useful on target material; edge-preserving; computationally practical; compatible with one global strength; scalar-first and AVX2-suitable; compatible with VapourSynth frame-request semantics; and supportable by metadata the reference decoder can provide reliably. A negative result is an acceptable outcome. Stopping at the gate is a success of the process, not a failure.

---

## 4. Stage 0: conceptual algorithm design (no code)

**PROPOSAL.** The first deliverable is a short concept document (`06_DEBLOCK_CONCEPT.md`), written and reviewed before any code. The items below are HYPOTHESES for discussion, not conclusions. None has been researched or tested.

### 4.1 Geometry the algorithm must handle

- Progressive or frame-DCT macroblocks: seams on a regular 8x8 / 16x16 grid.
- Field-DCT macroblocks within frame pictures: different vertical seam structure (section 2).
- Field pictures: each field has its own grid.
- Boundaries between macroblocks of different DCT type, and between coded and skipped macroblocks.
- Chroma 4:2:0, with its own block size and sampling.
- Open question: are blocking artefacts concentrated at 8x8 internal seams, at 16x16 macroblock seams, or both, on the real target material?

### 4.2 Deciding whether a step across a seam is blocking or a real edge

Ideas to evaluate (hypotheses):

- Compare the size of the step across the seam with the activity on each side. A small step beside flat areas is likely blocking; a large step is likely a real edge.
- Use the macroblock quantiser as a scale for the largest step that quantisation alone would plausibly create.
- Use intra / inter / skipped to adjust confidence (for example, skipped regions usually inherit their appearance from the previous picture).
- Ask whether coefficient or coded-block information is needed at all, or whether quantiser plus pixels is enough. This decides whether `.idx2` must grow.

### 4.3 Applying one global strength

- The current design exposes one global user-selected strength. Metadata and pixel tests may determine whether a seam is eligible for filtering and how that requested strength maps into a safe correction; the initial design must not silently turn this into an independent adaptive strength selector for every seam.
- The strength range and units stay undefined until behaviour is understood.
- Strength evolution (a possible later `auto` or limited adaptive mode): see D-07. The present design must not preclude it.

### 4.4 Shape of the correction

- Small support (a few pixels each side of a seam), clamped so the correction cannot exceed what the step could plausibly be.
- Deterministic and simple enough for a scalar reference and later AVX2.
- Explicit ringing and detail-loss limits.

### 4.5 Questions the concept document must answer

1. What does existing MPEG-2 post-processing prior art do, and what is genuinely a post-decode filter versus codec-internal?
2. Which of the metadata items in section 2 measurably improve decisions?
3. What per-seam and per-pixel computation is required?
4. Does field/frame mixing within a frame require different filtering geometry per macroblock, and how are mixed neighbours handled?
5. What does chroma need?
6. How is success measured (section 7)?

Prior art search can be done by Claude with web search (section 8), with every claim labelled RESEARCHED and cited.

---

## 5. `.idx2` format

### 5.1 Status

**CARRIED, DRAFT ONLY.** The v0.2 layout (16-byte header "MBX2"; 4-byte frame header; 2 bytes per macroblock: flags + quantiser) is a starting point and must not be frozen before the gate.

**VERIFIED (arithmetic):** PAL 720x576 gives 45 x 36 = 1620 macroblocks, 3244 bytes per frame, about 584 MB for two hours at 25 fps.

### 5.2 Defects in the v0.2 draft to resolve at spec time

1. One frame header holds one coding type and one structure. A frame assembled from two field pictures may have two different types and quantisers.
2. The quantiser byte for skipped macroblocks is undefined in the draft. State what it holds.
3. State whether the stored value is the raw quantiser code or the actual scale after the linear/non-linear mapping (q_scale_type), and how custom quantiser matrices are treated.
4. Display order versus decode order, repeat-first-field / pulldown, open-GOP leading B-pictures, and mid-stream sequence changes (the header fixes dimensions once).
5. "Total display frames" is "filled at sequence end"; define behaviour for truncated or damaged streams.

### 5.3 Validity and correspondence (DECIDED IN PRINCIPLE; keep simple)

The user is responsible for selecting the `.idx2` that belongs with the input video. The project should not build a complex source-identity or anti-user-error system unless testing demonstrates a real need.

Version 1 should nevertheless contain enough simple structural information to detect obvious index corruption or loss of frame correspondence. At minimum:

- an index format version;
- a frame/display record number (or equivalent simple ordinal) sufficient to detect missing/extra/out-of-sequence records;
- structural sanity checks: the plugin compares the index's dimensions and record count with the input clip and hard-aborts on any mismatch.

These checks do not detect a wrong index of identical shape; per D-02 that remains the user's responsibility.

A full elementary-stream hash, partial-content hash, or elaborate source-identity scheme is **not currently required**. It may be reconsidered only if Stage 5 demonstrates that simple correspondence checks are inadequate.

The central correspondence question is expected to be whether the index record representing displayed frame N maps to VapourSynth frame N. The exact MPEG-2 picture/field-to-BestSource/VapourSynth display-order mapping must be researched and tested rather than assumed.

### 5.4 The invariant

> `.idx2` record N must correspond exactly to VapourSynth frame N.

This is tested (Stage 5), not assumed, over progressive, interlaced, frame-picture, field-picture, and the actual capture material, including damaged streams.

---

## 6. Inspector (index generator)

### 6.1 Approach (DECIDED (D-06), replaces v0.2 section 5)

Do not "repair" the AI-converted inspector. Instead:

1. Dave supplies both the pristine reference decoder source and the current working inspector C source. The current working inspector is the practical starting point; the pristine reference decoder is the authority against which it is compared.
2. Produce a mechanical diff of the two. Dave recalls that the working inspector differs by only a few lines (principally a print); this is to be VERIFIED by the diff, not assumed.
3. Treat the instrumentation as a minimal patch against the pristine source. The patch is the reviewable authority.
4. No reformatting, renaming, comment rewriting or restructuring. Any change beyond the instrumentation is a separate proposal with a before/after block and a change ID.

### 6.2 Work list for Stage 4

- The current inspector's command line and input handling require significant verification and change.
- Clean binary input either from a named MPEG-2 elementary-stream file or from stdin piped from ffmpeg; no text-mode translation on Windows. (The reference decoder does not read the .mpg container; see 6.3.)
- Explicit output filename; unambiguous option parsing; clear errors and exit codes; hard abort on failure.
- No CSV or other text index. Debug/diagnostic output only if and as required, flushed, to stderr only, never mixed with index output.
- Deterministic output.
- Validate against the pristine decoder on known elementary streams.

### 6.3 Pipeline (CARRIED)

```text
.MPG -> ffmpeg (-c:v copy -an -f mpeg2video) -> MPEG-2 elementary stream
     -> instrumented reference decoder -> capture.idx2
```

### 6.4 Known trade-off (PROPOSAL, for discussion)

The reference decoder and BestSource need not decode identically for metadata purposes, but they can disagree on frame count and order, error handling, and start-of-stream behaviour. An alternative that avoids this is extracting the metadata from the same decoder BestSource uses. That is harder and is NOT proposed now; it is the fallback if Stage 5 shows unfixable disagreements.

### 6.5 Stage 1-2 tooling: draft binary index and analyzer (PROPOSAL)

- From Stage 1 the inspector writes the index in the binary, fixed-format, memory-mappable form, one record per display frame in display order. No text index format is used.
- The Stage 1-2 layout is a DRAFT with a format version number. It may change as research shows which fields are needed. It is frozen only at Stage 3.
- The input and command-line items in 6.2 are needed from Stage 1, because the throwaway inspector must already read clean input.
- The inspector is to be extended (picture type I/P/B, field and display-order information, skipped macroblocks, and whatever research shows is needed). Field meanings are VERIFIED from the source, not inferred from output.
- Writing in display order means emitting records where the reference decoder outputs a frame, not where it parses a picture. Where that happens in the source is to be verified first.
- A throwaway Python analyzer reads the binary index and produces summaries Dave can read directly, for example: picture-type sequence; per-frame counts of field/frame DCT; quantiser distribution; intra/inter/skipped counts; where field/frame DCT changes between neighbours.
- The analyzer also has a raw dump mode (one frame's records, decoded to readable values), so binary output can be checked by eye against the source and the standard.
- Analyzer results describe the inspector's output only. They are no more trustworthy than the inspector until it is verified against the pristine decoder (Section 6.1).
- The analyzer is AI-generated code and is reviewed like the inspector before its summaries are used for decisions.

---

## 7. Test material and acceptance

**PROPOSAL.**

- **Ground truth:** encode clean progressive and interlaced material at low bitrates to MPEG-2 so the original is known. Measure improvement against the original (for example PSNR/SSIM, plus detail-loss and ringing checks) in addition to viewing. HYPOTHESIS: these encodes will probably come from a software encoder such as ffmpeg, whose blocking character and field/frame DCT choices may differ from the LG recorder's hardware encoder. Ground truth therefore validates mechanics and measurement; real captures still need visual judgement.
- **Real material:** actual LG captures, including visibly blocky ones and different recording modes.
- **Baseline/context:** first establish what genuinely relevant post-decode deblocking implementations or algorithms actually exist. No existing MPEG-2-specific VapourSynth deblocking filter is currently assumed. Where technically meaningful, generic or historical post-processing/deblocking implementations may be used as comparison/context, but only after research establishes that the comparison is valid. The unfiltered MPEG-2 decode is always a baseline.
- **Acceptance criteria:** defined with Dave before Stage 2, including a maximum acceptable detail loss.

---

## 8. Roles

### 8.1 Dave - project owner

Final authority over specifications, decisions, acceptance, and what counts as established knowledge.

### 8.2 ChatGPT - primary analyst / implementation partner (CARRIED)

Specification drafting, code, test/edge-case review, as proposed in v0.2.

### 8.3 Claude - independent designer, reviewer, and researcher (DECIDED (D-04))

Claude may be used for:

- review of proposed designs, including the Stage 0 concept document;
- review of the minimal-diff inspector and later C++/API4/AVX2 code;
- adversarial review of ChatGPT proposals;
- MPEG-2 deblocking prior-art research, using web search where available;
- alternative algorithm proposals.

Working rules for Claude:

- Reviews cite file:line or document section, not impressions.
- Research claims are labelled RESEARCHED only with a citation; otherwise HYPOTHESIS. Claude's research is never VERIFIED. Only Dave's tests or a cold read of the source make something VERIFIED.
- Code edits are proposals shown as before/after blocks with change IDs, applied only when Dave says so. No reformatting.
- Claude cannot run Dave's clips, build on his machine, or judge visual quality; those remain Dave's.
- Both AIs are language models and share blind spots. The real independent checks are the reference decoder, the ground-truth test material, and Dave's eyes.
- Claude's usefulness depends on being given the actual files, not summaries of them.

### 8.4 Workflow

```text
Dave requirement -> ChatGPT analysis / Claude analysis -> compare and challenge
                 -> Dave decision -> ratified specification
```

---

## 9. Knowledge management

**PROPOSAL, deliberately light.** v0.2 suggested eleven documents. Start with three and add others only when a real need appears:

```text
02_INDEX_FORMAT_SPEC.md      (draft until the gate is passed)
05_DECISIONS.md              (decision ID, date, issue, alternatives, decision, rationale, superseded-by)
06_DEBLOCK_CONCEPT.md        (Stage 0 deliverable)
```

Carried rules: proposals are not facts; no silent supersession (old versions go to `superseded/`); converted or AI-generated code is compared against the trusted reference before acceptance; important material lives in files, not chat history; exchange source as named zip snapshots.

---

## 10. Effort and cost

**PROPOSAL.** Rough relative size only, Claude's estimate, not measured:

| Stage | Relative size |
|---|---|
| 0 Concept | small |
| 1 Evidence tooling | small to medium |
| 2 Python prototype and experiments | medium |
| 3-5 Spec, inspector, correspondence | medium |
| 6-7 C++ scalar and API4 | medium to large |
| 8 AVX2 | medium |
| 9 Acceptance | small to medium |

The bounded first commitment is Stages 0 to 2 and the gate. Later stages are only paid for if the gate is passed.

---

## 11. Decisions and rulings

These rulings preserve the scoping agreements reached during review of v0.3. They remain subordinate to later explicit decisions by Dave.

### D-01. Order of work - DECIDED

Accept the single order of work in section 3: conceptual algorithm design, evidence/test tooling, Python experimental prototype, feasibility gate, then index specification/inspector/C++/API4/AVX2.

Technical hypotheses inside those stages are not thereby ratified as facts.

### D-02. `.idx2` validity/correspondence - DECIDED WITH SIMPLIFICATION

Include simple versioning and record/frame correspondence checks from version 1. Avoid a complex source-identity mechanism by default: the user bears responsibility for choosing the index belonging to the input file.

The intended simple correspondence model is expected to centre on displayed frame number / VapourSynth frame number, but the exact picture/field/display-order mapping must be established by research and Stage 5 testing before the format is frozen.

### D-03. Python reference prototype - DECIDED

Use Python for Stage 2 if practical. Its purpose is an experimental algorithmic oracle/reference, not production speed. Short test clips and deliberately slow execution are acceptable.

If the selected algorithm proves genuinely impractical to express/test faithfully in Python, that is grounds to revisit the implementation language rather than force Python.

### D-04. Claude research and review - DECIDED

Claude may perform both independent research and review. ChatGPT and Claude may deliberately investigate different research questions, then exchange and contrast findings. Duplication is used selectively where independent confirmation is valuable.

Citations/evidence and Dave's ratification remain required before research becomes project truth.

### D-05. Starter knowledge documents - DECIDED

Begin with the three-document set in section 9. Add documents only when a demonstrated project-management or technical need exists.

Research division between ChatGPT and Claude does not itself require extra permanent documents; durable findings should be incorporated into the appropriate project document.

### D-06. Reference decoder / inspector sources - DECIDED

Dave can provide both the pristine reference decoder source and the current working inspector C source.

The working inspector is the practical starting point. The pristine source is the comparison authority. A mechanical diff will establish the actual changes before further instrumentation work.

### D-07. Strength evolution - DECIDED FOR CURRENT SCOPE

Initial work uses one manually selected global strength. A future `auto` mode or adaptive strength with explicit limiting may be considered later if evidence supports it. It is not part of the initial feasibility requirement.

### D-08. Existing-filter baseline - CLARIFIED

Do not assume that an existing MPEG-2-specific deblocking filter is available. Research first establishes what relevant historical/generic post-processing algorithms or implementations exist and whether comparison is meaningful. The unfiltered decode and ground-truth source remain mandatory baselines.


## 12. Change log

### v0.5 - tooling, input handling and housekeeping

- C5-01: Stage 1 row now specifies a draft binary .idx2 written by the throwaway inspector and a throwaway Python analyzer (section 3).
- C5-02: Added section 6.5: draft binary index in display order from Stage 1, no text index, analyzer with summaries and raw dump mode, trust limits.
- C5-03: Section 6.2: inspector command line/input require significant verification and change; clean input from a named elementary-stream file or ffmpeg stdin; debug output only to stderr, flushed, as required; no CSV.
- C5-04: Section 5.3: plugin checks index dimensions and record count against the clip and hard-aborts on mismatch; same-shape wrong index stays the user's responsibility (D-02).
- C5-05: Section 7: noted that software-encoded ground truth may not match the LG recorder's encoder (HYPOTHESIS).
- C5-06: Housekeeping: section 0 wording; labels of sections 3, 6.1 and 8.3 aligned with D-01, D-06 and D-04; section 4.3 points to D-07 instead of repeating it; non-ASCII dashes replaced.

### v0.4 - review decisions preserved and scope clarified

- C4-01: Preserved Dave's original limited recollection about mixed field/frame MPEG-2 blocking as a research hypothesis rather than promoting the proposed mechanism to established fact.
- C4-02: Ratified the v0.3 Stage 0 -> Stage 2 -> feasibility-gate work order.
- C4-03: Clarified current strength semantics: one global manual strength; future `auto` or adaptively limited strength remains a possible later enhancement, not current scope.
- C4-04: Simplified `.idx2` validity requirements. The user is responsible for matching index to input; version 1 needs simple structural/frame correspondence checks, not a complex source-identity/hash scheme unless evidence later requires one.
- C4-05: Made displayed-frame/VapourSynth-frame correspondence the expected simple model while retaining exact MPEG-2 picture/field/display-order mapping as a research/test obligation.
- C4-06: Corrected baseline wording: no existing MPEG-2-specific VapourSynth deblocking filter is assumed. Relevant generic/historical implementations are comparisons only if research establishes their relevance.
- C4-07: Confirmed that Dave can supply both pristine reference decoder source and current working inspector C source; working inspector is the starting point and pristine source the comparison authority.
- C4-08: Ratified Python as the Stage 2 experimental oracle/reference if practical, not as a production-performance implementation.
- C4-09: Ratified Claude for independent research and review, with ChatGPT and Claude allowed to divide research topics and cross-compare results.
- C4-10: Ratified the three-document starter knowledge set.
- C4-11: Converted section 11 from open questions into recorded decisions/rulings so agreed scope is not lost.

### v0.3 - corrections and restructure

- C3-01: Replaced the conflicting orderings in v0.2 with one authoritative order (section 3). Added Stage 0, conceptual design first, per Dave.
- C3-02: Corrected the v0.2 section 3 premise that the index reveals boundary positions; restated its value, including Dave's point that field and frame blocking can be mixed within one frame (section 2).
- C3-03: Added a Stage 0 concept section with hypotheses and questions, all labelled unverified (section 4).
- C3-04: Added index defects to resolve (section 5.2) and mandatory validity fields (section 5.3).
- C3-05: Replaced "repair the inspector" with a minimal diff against the pristine decoder (section 6.1); noted the same-decoder fallback (section 6.4).
- C3-06: Moved ground-truth test material, baseline comparison and acceptance criteria up front (section 7).
- C3-07: Added a Python reference prototype before C++ (sections 3, D-03).
- C3-08: Extended Claude's role to design review, code review and optional research, with evidence and no-reformatting rules (section 8.3).
- C3-09: Reduced the suggested document set from eleven to three (section 9).
- C3-10: Added effort sizing and a bounded first commitment (section 10).
- C3-11: Added the label scheme (section 0) and a decisions list in plain English (section 11).
- C3-12: Removed v0.2 statements that the indexer is the first deliverable (sections 5, 20, 21) as superseded.
