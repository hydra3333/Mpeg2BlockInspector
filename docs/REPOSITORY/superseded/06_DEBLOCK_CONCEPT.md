# 06 - MPEG-2 Deblocking Concept

**Document:** `06_DEBLOCK_CONCEPT.md`
**Version:** 1.1 (DRAFT - PROPOSED UPDATE)
**Date:** 2026-10-08
**Drafted by:** ChatGPT for Claude cold review
**Status:** DRAFT FOR CLAUDE REVIEW AND DAVE RATIFICATION. Version 1.0 remains the current ratified Stage 0 concept until this revision is ratified.
Items labelled HYPOTHESIS remain hypotheses and items labelled OPEN remain unresolved; ratification
does not change their evidence status. The Stage 0 research and review files are provenance only.
**Controlling proposal:** `MPEG2_Macroblock_Index_VapourSynth_Deblocking_Project_Proposal_v0_5.md`
**Decision authority:** `05_DECISIONS.md` (D-20)

---

## 0. How to read this document

### 0.1 Role

This is the Stage 0 concept document (proposal v0.5 section 4). It states the processing model,
the MPEG-2 knowledge the concept rests on, the candidate algorithm families, the Stage 2
experiment, and the open questions. It does NOT define filter equations, thresholds or the
strength scale; those remain undecided (section 12).

Version 1.0 introduced no new technical conclusions beyond the then-completed research trail.
This proposed v1.1 update adds only post-v1.0 findings and Dave rulings that are explicitly traced
to the newer provenance in section 0.3. Nothing new in v1.1 becomes project authority until Dave
ratifies this revision. Where this document and a provenance file differ, the difference must be
raised, not silently resolved.

### 0.2 Labels

- **DECIDED** - ratified by Dave; recorded in `05_DECISIONS.md`.
- **AGREED** - part of the Stage 0 concept accepted by Dave on 2026-10-06. Not a decision record;
  does not change the evidence status of anything it contains.
- **PROPOSED** - drafted for ratification; not yet project knowledge.
- **ACCEPTED (evidence level)** - knowledge item ratified by Dave, with its evidence level kept
  visible (D-21). Before ratification these are shown as **PROPOSED -> ACCEPTED (evidence level)**.
- **HYPOTHESIS** - design inference or proposal, not established by evidence.
- **OPEN** - unresolved; listed in section 11.

Evidence levels: **RESEARCHED** (supported by a cited source) and **VERIFIED** (demonstrated by
Dave's tests or a cold read of authoritative source). Items explicitly labelled VERIFIED below
retain that implementation/test evidence level; VERIFIED does not imply a normative H.262 claim
unless stated separately.

### 0.3 Source abbreviations

| Abbrev. | File |
|---|---|
| PA | `Claude_MPEG2_Deblocking_Prior_Art_v0_1.md` |
| PA-add | `Claude_MPEG2_Deblocking_Prior_Art_v0_1_addendum.md` |
| CM | `ChatGPT_MPEG2_Deblocking_Codec_Mechanics_v0_1.md` |
| CRV | `Claude_REVIEW_OF_ChatGPT_MPEG2_Deblocking_Codec_Mechanics_v0_1.md` |
| CR | `ChatGPT_REVIEW_OF_Claude_MPEG2_Deblocking_Prior_Art_v0_2.md` |
| CRSP | `Claude_RESPONSE_TO_ChatGPT_REVIEW_OF_Claude_MPEG2_Deblocking_Prior_Art_v0_2.md` |
| GRSP | `ChatGPT_RESPONSE_TO_Claude_REVIEW_OF_ChatGPT_MPEG2_Deblocking_Codec_Mechanics_v0_1.md` |
| FCR | `ChatGPT_FINAL_CROSS_REVIEW_OF_Claude_RESPONSE_v0_1.md` |
| SC | `ChatGPT_REFERENCE_vs_INTERIM_Source_Comparison_v0_2.md` |
| CDR | `Claude_REVIEW_OF_ChatGPT_Discussion_Brief_Index_Value_and_Chroma_Deblocking_v0_2.md` |
| RR | `Claude_REVIEW_Reconciliation_After_Handover_v0_1.md` |

---

## 1. Purpose and scope

The concept is a VapourSynth post-decode deblocking filter for MPEG-2 4:2:0 material (Dave's LG
captures), using decoded frames from BestSource plus per-macroblock MPEG-2 coding metadata, with
one global user-selected strength (D-07).

The central question this concept sets up for Stage 2:

> Given authoritative indexed MPEG-2 geometry and QP, what filtering rule produces useful luma
> and chroma deblocking without unacceptable damage, and which indexed metadata are actually
> needed by the final production filter?

A negative answer about the filter's practical value is acceptable and stops or redirects the
project at the feasibility gate. Whether the production architecture should use an index is no
longer part of that gate (proposed D-24).

---

## 2. Processing model

**DECIDED (D-09).**

The deblocking model is **frame-owned, metadata-directed filtering with field-parity-aware sample
access**:

- the decoded VapourSynth frame is the processing object;
- per-macroblock metadata determines which transform seams exist and where;
- same-field-polarity samples are used where filtering across a seam would otherwise mix
  temporally different fields;
- there is NO separate-field deblocking pass: the frame is never split into two fields that are
  deblocked independently on a fixed field grid.

Origin: Dave's explicit requirement (recorded in CR section 6 and FCR section 1). Any future
proposal that says "process each field separately" is rejected unless it means only
parity-aware sample access inside this model.

---

## 3. MPEG-2 knowledge this concept relies on

K-01 to K-06, K-08 and K-09 remain **ACCEPTED** at the evidence level shown (D-21; ratified
by Dave on 2026-10-06). K-07 is revised in v1.1 and is **PROPOSED -> ACCEPTED** in this draft;
its expanded decoder-semantics wording is supported by a reference-decoder cold read. K-10 and
K-11 are likewise **PROPOSED -> ACCEPTED** and require Dave's ratification. Numbering continues
the K-nn sequence.

| ID | Knowledge | Evidence level | Source |
|---|---|---|---|
| K-01 | An MPEG-2 4:2:0 macroblock contains four 8x8 luma transform blocks and one 8x8 transform block in each chroma plane. | RESEARCHED | CM 4.1 |
| K-02 | In suitable frame pictures (frame_pred_frame_dct = 0), luma transform organisation can vary per macroblock between frame DCT and field DCT. | RESEARCHED | CM 5.2, 5.3 |
| K-03 | Horizontal luma transform seams in frame pictures: frame-DCT macroblock has an internal seam plus macroblock-edge seams; field-DCT macroblock has macroblock-edge seams only. | RESEARCHED (H.262) + VERIFIED (reference-decoder implementation, V1) | CM 6; CRV R1; GRSP 2; FCR 2; CDR V1 |
| K-04 | In MPEG-2 4:2:0 frame pictures, chroma blocks are organised in frame structure for DCT coding and do not follow the per-macroblock luma dct_type reorganisation. Field pictures: see section 4.6. | RESEARCHED + VERIFIED (reference-decoder implementation, V2) | CM 8.1; CDR V2 |
| K-05 | quantiser_scale_code must be mapped through q_scale_type to the actual quantiser scale; weighting matrices also affect quantisation. | RESEARCHED | CM 12, 13 |
| K-06 | Coded order and display order differ when B pictures are present; index correspondence must follow the output (display) frame sequence that maps to VapourSynth frames. | RESEARCHED | CM 10 |
| K-07 | FRAME/FIELD/NONE describes applicable coded residual transform geometry, not merely the presence or value of dct_type. NONE applies where no coded residual transform geometry exists, including skipped macroblocks and non-intra macroblocks with effective coded_block_pattern == 0; a dct_type bit may nevertheless have been read in the latter case. A stale/default decoder dct_type must not create a FRAME/FIELD state. Field pictures are identified separately by picture_structure. | RESEARCHED syntax + VERIFIED reference-decoder semantics; revised derivation/implementation rule PROPOSED -> ACCEPTED | CM 5.2; CRV R2; GRSP 4; SC v0.2 9.3; Claude repository-draft review M1 |
| K-08 | Motion compensation can copy blocking from reference pictures into the current picture (researched). Such blocking can lie off the current picture's transform grid and so bound what a current-grid post-filter can target (inference). | HYPOTHESIS supported by RESEARCHED evidence | PA S24, S03; CRV R3; GRSP 5 |
| K-09 | FFmpeg's MPEG-2 decoder can export per-macroblock quantiser information as frame side data associated with output frames. This is retained as a cross-check source, not a competing production architecture. | RESEARCHED | PA S18; CR section 7; GRSP 9 |
| K-10 | In the inspected reference decoder's MPEG-2 4:2:0 path, chroma blocks use the macroblock's same `quantizer_scale`; for 4:2:0 the decoder selects the luma quantisation matrices rather than separate chroma matrices. This is VERIFIED implementation knowledge, not a normative H.262 claim. | VERIFIED (reference-decoder implementation, V3) - PROPOSED -> ACCEPTED | CDR V3 |
| K-11 | In the inspected reference decoder, MPEG-2 4:2:0 field prediction in frame pictures reconstructs chroma with alternating field parity by line: even chroma lines top field, odd chroma lines bottom field. This verifies the parity premise; same-field access in the post-filter remains a design choice. | VERIFIED (reference-decoder implementation, V4) - PROPOSED -> ACCEPTED | RR section 1, V4 |

The absence of a per-macroblock dct_type export is a negative search result, not knowledge; it
is recorded as O-13.

Note on K-03: the required reference-decoder cold read has now been completed (CDR V1). The
normative geometry remains RESEARCHED from H.262; the inspected implementation handling is
separately VERIFIED.

---

## 4. Geometry

### 4.1 Luma vertical seams

**AGREED (from CR 4.2, CRSP Q2, FCR 3).**

Vertical seam positions (every 8 luma samples horizontally) do not depend on frame versus field
DCT. The correction across a vertical seam runs along one row. Any decision or activity measure
that spans several rows must still use field-parity-aware access on interlaced material.

### 4.2 Luma horizontal seams by transform state (frame pictures)

**AGREED (K-03).**

Frame lines within one 16-line macroblock are numbered 0-15.

```text
Transform state FRAME (frame-DCT macroblock):
    seam at the macroblock top/bottom edges
    + internal seam between frame lines 7 | 8,
      seen with same-field-polarity access as:
        top-field samples    6 | 8   (field centreline)
        bottom-field samples 7 | 9   (field centreline)

Transform state FIELD (field-DCT macroblock):
    seam at the macroblock top/bottom edges only
    (no internal horizontal seam in either field)

Transform state NONE:
    no coded transform seam belonging to this macroblock (see 4.3)
```

At a macroblock edge, seen with same-field-polarity access, the seam lies between frame lines
14 | 16 (top field) and 15 | 17 (bottom field) of the adjacent macroblocks (CM 6.5).

### 4.3 Transform state semantics, including NONE

**AGREED (K-07; FCR 5).**

Three semantic states: FRAME, FIELD, NONE. NONE means only:

> no current coded residual transform geometry is asserted for this macroblock.

NONE does **not** mean "no visible blocking can exist here". Prediction can carry blocking from
reference pictures into skipped and no-residual macroblocks (K-08). How NONE affects filtering
eligibility is OPEN (O-04).

These are semantic states for research and design; they do not imply a particular bit encoding
in the index (see `02_INDEX_FORMAT_SPEC.md`).

### 4.4 Support-length rule

**AGREED design constraint; HYPOTHESIS (CRSP Q3; FCR 4).**

> The support used to classify or correct one known transform seam must not cross another known
> transform seam.

Consequence with same-field-polarity access:

- a FRAME macroblock offers about 4 samples per field between its macroblock edge and its internal
  centreline seam;
- a FIELD macroblock offers about 8 samples per field between its macroblock edges.

This is a deblocking-design constraint, not an MPEG-2 normative requirement. It belongs to the
algorithm, not to the index.

### 4.5 Macroblock edges between different transform states

**AGREED (CR 4.6; CRSP Q3).**

The macroblock-edge seam exists in both fields at the same position whatever the transform states
on either side. The open matter is eligibility and threshold, which may depend on metadata from
both macroblocks, plus support length on each side (4.4). Whether a NONE | NONE edge (no coded
transform on either side, but possible motion-compensation steps) should be filtered is OPEN
(O-04).

Every 16x16 macroblock edge lies on the regular 8x8 luma coding grid. Where coded transforms are
present it is also a transform-block boundary. For any FRAME/FIELD/NONE combination the edge remains
a macroblock boundary that may show a reconstructed-pixel discontinuity, even when one or both sides
have no current coded transform. The first design processes macroblock edges in the same boundary
framework; whether they need distinct treatment is OPEN (O-11).

### 4.6 Field pictures

**OPEN (O-08).** A field picture contains one field's lines, and there is no frame/field DCT
distinction within it (CM 9.1). Field pictures need their own geometry path rather than reuse of
the frame-picture logic (CR 4.7). No field pictures occurred in the seven clips examined so far; archive-wide occurrence remains OPEN (O-08).

### 4.7 Chroma (4:2:0)

**AGREED / PROPOSED UPDATE (K-04, K-10, K-11; proposed D-25).**

- One 8x8 chroma transform block per plane per macroblock; chroma transform seams coincide with
  luma macroblock boundaries. There is no internal chroma transform seam.
- Chroma does not inherit luma `dct_type` geometry (K-04, V2).
- In the inspected reference decoder, 4:2:0 chroma uses the macroblock's same effective
  `quantizer_scale`, and the 4:2:0 path selects the luma quantisation matrices (K-10, V3).
- V4 verifies the implementation premise that field-predicted 4:2:0 chroma alternates field parity
  by line: even chroma lines top field, odd chroma lines bottom field (K-11).
- Whether horizontal chroma deblocking on interlaced frame pictures should use same-field sample
  access remains an OPEN Stage 2 design choice; V4 verifies the parity premise, not the filter rule.
- Chroma deblocking is proposed to be in production scope on mechanism (D-25). Stage 2 therefore
  tests safe/effective threshold, strength, H/V treatment and no-harm behaviour rather than first
  asking whether chroma blocking exists at all.
- Interlaced 4:2:0 chroma upsampling errors (colour combing) are a distinct phenomenon and are out
  of scope unless separately reopened (CRV R5; FCR 6).

---

## 5. Decision vocabulary: three kinds of "detection"

**AGREED (PA-add 3.5; CR section 6; FCR 1).**

1. **Seam geometry - where the transform seams are.** In the production index-driven path, seam
   positions are supplied by MPEG-2 geometry and metadata. Pixel detection of seam positions is
   not part of the design (proposed D-24).
2. **Eligibility and magnitude - whether, and how far, to correct a known seam.** Bounded by the
   global strength and codec information. A quantiser-based bound is an empirical or derived
   threshold, not a rigorous maximum, because weighting matrices, intra/non-intra rules,
   coefficient values and mismatch control all intervene (CR section 6; CRSP 3 item 2).
3. **Edge preservation - blocking versus a genuine edge lying on a seam.** Cannot be eliminated
   by metadata. Requires local reconstructed-pixel evidence.

Guiding principle (HYPOTHESIS, CM 21; prior-art support PA Q4): a step at a known seam that is
large relative to nearby within-block variation, and plausible for the local quantiser, is likely
blocking; otherwise preserve it.

---

## 6. Quantiser use

**AGREED (K-05).**

- The algorithm should reason in terms of the derived MPEG-2 quantiser scale, not the raw 5-bit
  code (CM 12.3). Whether `.idx2` stores the derived value directly or stores enough syntax to
  derive it remains an index format decision (`02_INDEX_FORMAT_SPEC.md` C-4).
- Thresholds borrowed from MPEG-4 Annex F, libpostproc or H.264 are in different units and must be
  re-derived or calibrated for MPEG-2 (CR 3.2).
- K-10 verifies that the effective per-macroblock QP applies to MPEG-2 4:2:0 chroma unchanged in the inspected reference-decoder path.
- Custom non-intra matrices occur in four of the five real LG recordings examined (4A, LP, EP, MLS); whether matrix values materially affect the filter remains OPEN (O-07).
- The quantiser value for skipped macroblocks must be defined, not left ambiguous (CM 12.4); this
  is an index-specification matter (`02_INDEX_FORMAT_SPEC.md`).

---

## 7. Strength

**DECIDED (D-07).** One manually selected global strength. Metadata and pixel tests decide where
and how much of it is applied; they do not create a per-seam user setting. Range, units and
mapping are OPEN (O-05).

---

## 8. Candidate algorithm families

All families are **HYPOTHESIS**. Exact kernels are undecided (section 12).

### 8.1 Family A - design family

**DECIDED (D-10).**

Short-support, quantiser-aware, edge-preserving boundary filtering:

- frame-owned processing (section 2);
- metadata-directed seam geometry (4.2);
- field-parity-aware sample access where required;
- support-length rule (4.4);
- one global strength (D-07);
- bounded, local correction.

Prior art studied (not adopted): MPEG-4 Annex F / Kim et al. two-mode filter and libpostproc
(PA S01-S03). These inform but do not define the kernel (CR section 10).

### 8.2 Family B - historical control, proposed superseded

**DECIDED historically (D-11); PROPOSED SUPERSEDED by D-24.**

Family B was the pixel-only, interlace-aware falsification control in the Stage 0 architecture
experiment. Under proposed D-24 the production architecture is index-driven by definition, so
Stage 2 no longer implements or evaluates Family B. This is a scope change, not an experimental
finding that Family B is inferior.

### 8.3 Family C - optional quality reference

**DECIDED (D-12).**

Shifted-DCT re-quantisation using the per-macroblock quantiser (PA S04, S05). Heavier; may solve a
broader restoration problem than intended. Must not delay testing Family A.

---

## 9. Stage 2 experiment (feasibility-gate evidence)

**PROPOSED UPDATE (D-15, D-16, proposed D-24/D-25/D-26).**

The detailed experiment belongs in `Stage2_Experiment_Design_v0_2.md`; this section fixes only
the concept-level structure.

### 9.1 Indexed-only ladder

| Step | Configuration | Geometry / metadata purpose |
|---|---|---|
| 1 | Unfiltered decode | mandatory baseline |
| 2 | Family A + authoritative indexed geometry + fixed/emulated QP | kernel/edge-activity behaviour with spatial QP variation removed |
| 3 | Same Family A + authoritative indexed geometry + real per-macroblock QP | value of the real spatial QP map |
| 4 | Kernel / threshold / strength development | filtering-quality development with indexed geometry and real QP |
| 5 | NONE-policy experiment | resolve filtering behaviour where no current coded residual transform geometry is asserted |
| 6 | Bounded 4:2:0 chroma experiment | fixed chroma geometry; fixed-QP versus real-QP behaviour; no-harm |
| 7 | Generalisation / no-harm | locked real-recorder hold-outs plus progressive/control material |

Steps 2 and 3 use the same initial candidate kernel, frozen for that fixed-QP versus real-QP
comparison. Step 4 then develops the kernel, thresholds and strength further.

Before filtering-quality conclusions, Stage 2 must validate that index macroblock coordinates are
spatially registered to the BestSource pixels. This is a detector-free registration check, not a
pixel seam-position detector.

### 9.2 Comparisons

```text
Step 2 vs Step 3 : value of the real per-macroblock QP map while authoritative geometry is fixed
I vs P vs B       : practical effect of propagated / off-grid blocking (K-08; D-16)
QP bands          : behaviour across quantiser severity, including QP 112 saturation where present
```

There is no Stage 2 comparison of pixel-detected geometry versus indexed geometry, and no Family B
architecture comparison (proposed D-24).

### 9.3 Material and evidence hierarchy

**PROPOSED (D-26).**

Primary product evidence is real LG recorder material. The unfiltered decode is the mandatory
baseline for every clip. On real LG material, use seam-local diagnostics, collateral-change/no-harm
measures and Dave's visual assessment.

Software-transcode pairs remain secondary paired-reference evidence. Their numerical measures are
interpreted only as movement toward or away from the decoded higher-quality source, not as pristine
ground truth. Results remain broken down by I/P/B where practical (D-16).

The planned experiment does not include an existing-filter yardstick. Such a comparison may be
revisited only if later evidence creates a specific need.

### 9.4 Architectural meaning

The production deblocker is index-driven by definition under proposed D-24. Stage 2 tests whether
the deblocking filter is worthwhile and which indexed metadata the final filter actually needs; it
does not decide between index-driven and pixel-only production architectures. Final index contents
and packing remain unfrozen (`02_INDEX_FORMAT_SPEC.md`; D-22).

---

## 10. Achievable-benefit bound

**AGREED (K-08, HYPOTHESIS supported by RESEARCHED evidence; CRV R3; FCR 9).**

A post-filter restricted to the current picture's known grid seams cannot systematically target blocking that motion compensation has propagated
to off-grid locations. This can bound the achievable improvement in P and B pictures. It is not, by itself, a reason to add motion vectors. A filter must not be judged
"wrong" for failing to remove artefacts no current-grid filter can reach.

---

## 11. Open questions

O-10a and O-10b from v1.0 are withdrawn by proposed D-24; they are not answered experimentally,
but become out of scope. O-03 is closed by the Stage 1 gated-NONE design/source review and VALID
runs. Remaining/open items are:

| ID | Question | Where it gets answered |
|---|---|---|
| O-01 | Can BestSource expose or preserve FFmpeg's MPEG-2 per-macroblock QP side data in the intended workflow? | Optional implementation cross-check; not an architecture gate |
| O-02 | Exact FFmpeg QP semantics for skipped / no-residual macroblocks. | Optional cross-check with O-01 |
| O-04 | How should NONE affect filtering eligibility, including NONE / NONE macroblock edges? | Stage 2 design and experiment |
| O-05 | Strength range, units and equations. | Stage 2 behaviour / later design |
| O-06 | Chroma threshold, strength, H/V treatment, interlaced access and no-harm behaviour. | Stage 2 |
| O-07 | Custom non-intra matrices occur in 4 of 5 real LG recordings examined; do matrix values materially affect filtering? | Deferred; reopen inspector only if Stage 2 evidence requires matrix values |
| O-08 | No field pictures occurred in the seven clips examined; do they occur elsewhere in Dave's archive, and how often? | Archive-wide evidence / later support decision |
| O-09 | How much visible blocking is on-grid versus propagated / off-grid? | Stage 2 (I/P/B breakdown) |
| O-11 | Do macroblock edges need treatment distinct from internal 8x8 seams? | Stage 2 |
| O-12 | Is frame/field prediction type relevant to visible macroblock-edge steps? | Stage 1 diagnostic / Stage 2 evidence if needed |
| O-13 | What exact FFmpeg/BestSource metadata interfaces are useful as cross-checks? No per-macroblock `dct_type` export has been identified in the research so far (negative search result, not established absence). | Optional implementation cross-check |
| O-14 | Progressive pictures use frame-domain sample access; for interlaced pictures, exactly which plane/orientation operations should use parity-aware access? | Stage 2 design; chroma same-field use remains a design choice |

Stage 1 diagnostics wanted (AGREED, from GRSP 12; prediction type per D-14): per output frame -
display ordinal, picture type, picture_structure, frame_pred_frame_dct, q_scale_type,
progressive_frame, top_field_first / repeat_first_field, dimensions; per macroblock - position,
transform state FRAME/FIELD/NONE, intra/inter/skipped, derived quantiser scale, explicit quantiser
change if easy, CBP and prediction type as optional diagnostics; per-frame summaries - state counts,
neighbour transitions, quantiser distribution, coding-mode counts, picture-type statistics.

---

## 12. Explicitly undecided

- filter kernels and equations;
- thresholds and their mapping from the quantiser;
- strength range, units and per-level behaviour (O-05);
- treatment of NONE (O-04);
- chroma threshold/strength, H/V treatment and interlaced access (O-06, O-14);
- field-picture geometry path (O-08);
- index field content and packing (`02_INDEX_FORMAT_SPEC.md`).

---

## 13. Evidence trail

The research and review files listed in section 0.3 are the evidence. The newer CDR and RR files carry the V1-V4 reference-decoder cold-read provenance used by this proposed update. They remain unchanged in the project's research folder and are not superseded by this document. This document records the
ratifiable synthesis and points to them; it does not restate them.

---

## 14. Change log

### v1.1 - 2026-10-08 (DRAFT - CORRECTED AFTER CLAUDE REVIEW)

- Drafted by ChatGPT for Claude cold review; v1.0 remains ratified authority until Dave ratifies
  this revision.
- Re-grounded Stage 2 around the proposed index-driven production architecture (D-24); Family B and
  pixel-detected seam geometry removed from the planned experiment.
- Added proposed D-25 chroma-in-scope consequence and revised the Stage 2 evidence hierarchy per
  proposed D-26. Existing-filter yardstick explicitly excluded from the planned experiment.
- K-03/K-04 evidence upgraded with Claude V1/V2 reference-decoder verification; proposed K-10
  (V3 chroma QP/matrix path) and K-11 (V4 chroma field parity) added at VERIFIED implementation
  level.
- K-07 explicitly marked as revised in v1.1 and PROPOSED -> ACCEPTED; its expanded decoder
  semantics are identified as VERIFIED reference-decoder implementation evidence rather than
  silently inheriting the v1.0 acceptance of the older wording.
- Clarified that D-09, not transform geometry itself, is the reason for same-field-polarity access;
  renamed Family A's section heading from "leading hypothesis" to "design family".
- Clarified that Steps 2 and 3 use one frozen initial candidate kernel for the fixed-QP versus
  real-QP comparison, with further kernel/threshold/strength development beginning at Step 4.
- Added detector-free spatial index-to-pixel registration check as a Stage 2 requirement.
- Open questions updated by meaning: O-03 closed, O-10a/O-10b withdrawn, chroma and FFmpeg items
  reframed, O-14 added for progressive/interlaced access.

### v1.0 - 2026-10-06 (RATIFIED)

- Ratified by Dave on 2026-10-06. Statuses updated only; no technical content changed.
- K-01 to K-09 ACCEPTED at exactly the evidence levels shown in section 3.
- References to D-09 to D-17 now DECIDED.
- Concept content previously marked PROPOSED is now AGREED (label added to section 0.2).
  HYPOTHESIS and OPEN items unchanged.
- This document, `05_DECISIONS.md` and `02_INDEX_FORMAT_SPEC.md` are now the normal project
  authority; the Stage 0 research and review files (section 0.3) are provenance only.

### v0.2 - 2026-10-06 (DRAFT, PROPOSED)

Corrections from `ChatGPT_COLD_REVIEW_OF_Repository_Drafts_v0_1.md` (all MUST FIX and SHOULD FIX
items):

- Section 3: evidence level per K item; K-04 narrowed to frame pictures; K-07 split into syntax
  fact and implementation constraint; K-08 relabelled HYPOTHESIS supported by RESEARCHED
  evidence; K-09 limited to the positive QP-export finding; K-03 note separates H.262 knowledge
  from implementation verification.
- Section 4.5: macroblock edges described as coding-grid boundaries, transform boundaries only
  where coded transforms exist (consistent with NONE).
- Section 5: "no pixel detection of seam positions" scoped to Family A.
- Section 6: algorithm reasons in derived quantiser scale; storage left to the index spec.
- Section 9.2: comparisons reworded; 2 vs 2b no longer claimed as a kernel isolation.
- Section 10: off-grid bound softened.
- Section 11: O-01 no longer blocks Stage 1 throwaway tooling; O-10 split into O-10a/O-10b;
  O-13 added for dct_type export (negative search result).

### v0.1 - 2026-10-06 (DRAFT, PROPOSED)

- First synthesis by Claude from the completed Stage 0 research and review trail, following FCR
  section 16 allocation and Dave's rulings I-1 to I-6 (D-18 to D-23).
- No new technical conclusions introduced.
