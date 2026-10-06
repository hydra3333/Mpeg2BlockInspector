# 06 - MPEG-2 Deblocking Concept

**Document:** `06_DEBLOCK_CONCEPT.md`
**Version:** 1.0 (RATIFIED)
**Date:** 2026-10-06
**Drafted by:** Claude (first synthesis, per D-23)
**Status:** RATIFIED. Ratified by Dave on 2026-10-06 as the agreed Stage 0 concept and a normal project authority.
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

It introduces no new technical conclusions. Every item traces to the research and review trail
listed in section 13. Where this document and a research file differ, the difference must be
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
Dave's tests or a cold read of authoritative source). Nothing in this document is VERIFIED.

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
! SC | `ChatGPT_REFERENCE_vs_INTERIM_Source_Comparison_v0_2.md` |

---

## 1. Purpose and scope

The concept is a VapourSynth post-decode deblocking filter for MPEG-2 4:2:0 material (Dave's LG
captures), using decoded frames from BestSource plus per-macroblock MPEG-2 coding metadata, with
one global user-selected strength (D-07).

The central question this concept sets up for Stage 2:

> Can authoritative per-macroblock MPEG-2 metadata (real quantiser and transform state) give a
> simpler and/or better field-safe deblocking decision than pixel-only detection?

A negative answer is acceptable and stops or redirects the project at the feasibility gate
(proposal v0.5 section 3).

---

## 2. Processing model

**DECIDED (D-09).**

The deblocking model is **frame-owned, metadata-directed filtering with field-parity-aware sample
access**:

- the decoded VapourSynth frame is the processing object;
- per-macroblock metadata determines which transform seams exist and where;
- same-field-polarity samples are used only where the known geometry requires it, to avoid
  mixing temporally different fields;
- there is NO separate-field deblocking pass: the frame is never split into two fields that are
  deblocked independently on a fixed field grid.

Origin: Dave's explicit requirement (recorded in CR section 6 and FCR section 1). Any future
proposal that says "process each field separately" is rejected unless it means only
parity-aware sample access inside this model.

---

## 3. MPEG-2 knowledge this concept relies on

All items are **ACCEPTED** at the evidence level shown for each item (D-21; Ratified by Dave on 2026-10-06). None
is VERIFIED. Numbering follows FCR section 13.

| ID | Knowledge | Evidence level | Source |
|---|---|---|---|
| K-01 | An MPEG-2 4:2:0 macroblock contains four 8x8 luma transform blocks and one 8x8 transform block in each chroma plane. | RESEARCHED | CM 4.1 |
| K-02 | In suitable frame pictures (frame_pred_frame_dct = 0), luma transform organisation can vary per macroblock between frame DCT and field DCT. | RESEARCHED | CM 5.2, 5.3 |
| K-03 | Horizontal luma transform seams in frame pictures: frame-DCT macroblock has an internal seam plus macroblock-edge seams; field-DCT macroblock has macroblock-edge seams only. | RESEARCHED (H.262); implementation handling not yet VERIFIED | CM 6; CRV R1; GRSP 2; FCR 2 |
| K-04 | In MPEG-2 4:2:0 frame pictures, chroma blocks are organised in frame structure for DCT coding and do not follow the per-macroblock luma dct_type reorganisation. Field pictures: see section 4.6. | RESEARCHED | CM 8.1 |
| K-05 | quantiser_scale_code must be mapped through q_scale_type to the actual quantiser scale; weighting matrices also affect quantisation. | RESEARCHED | CM 12, 13 |
| K-06 | Coded order and display order differ when B pictures are present; index correspondence must follow the output (display) frame sequence that maps to VapourSynth frames. | RESEARCHED | CM 10 |
| K-07 | FRAME/FIELD/NONE describes applicable coded residual transform geometry, not merely the presence or value of dct_type. NONE applies where no coded residual transform geometry exists, including skipped macroblocks and non-intra macroblocks with effective coded_block_pattern == 0; a dct_type bit may nevertheless have been read in the latter case. A stale/default decoder dct_type must not create a FRAME/FIELD state. Field pictures are identified separately by picture_structure. | RESEARCHED syntax/decoder semantics + PROPOSED implementation constraint | CM 5.2; CRV R2; GRSP 4; SC v0.2 9.3 |
| K-08 | Motion compensation can copy blocking from reference pictures into the current picture (researched). Such blocking can lie off the current picture's transform grid and so bound what a current-grid post-filter can target (inference). | HYPOTHESIS supported by RESEARCHED evidence | PA S24, S03; CRV R3; GRSP 5 |
| K-09 | FFmpeg's MPEG-2 decoder can export per-macroblock quantiser information as frame side data associated with output frames. | RESEARCHED | PA S18; CR section 7; GRSP 9 |

The absence of a per-macroblock dct_type export is a negative search result, not knowledge; it
is recorded as O-13.

Note on K-03: K-03 is RESEARCHED from H.262. Before inspector output is relied on, the reference
decoder source must be cold-read to verify how it represents, derives and exposes the
corresponding frame/field-DCT state.

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
the frame-picture logic (CR 4.7). Whether they occur in Dave's captures is to be measured in
Stage 1.

### 4.7 Chroma (4:2:0)

**AGREED (K-04; CM 4.2, 20.4; FCR 6).**

- One 8x8 chroma transform block per plane per macroblock; chroma transform seams coincide with
  luma macroblock boundaries. There is no internal chroma seam.
- Chroma does not inherit luma dct_type geometry.
- Chroma prediction can still be field-based, so interlace-related chroma effects are not
  excluded (CM 8.2; CRV R5).
- Chroma strength or threshold relative to luma is OPEN (O-06).
- Interlaced 4:2:0 chroma upsampling errors (colour combing) are a distinct phenomenon and are out
  of scope unless separately reopened (CRV R5; FCR 6).

---

## 5. Decision vocabulary: three kinds of "detection"

**AGREED (PA-add 3.5; CR section 6; FCR 1).**

1. **Seam geometry - where the transform seams are.** In the metadata-directed Family A path, seam
   positions are supplied by MPEG-2 geometry and metadata; pixel detection of seam positions is not
   required. (Family B detects seam positions from pixels deliberately, as the control.)
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
- Whether custom weighting matrices occur, and matter, is OPEN (O-07).
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

### 8.1 Family A - leading hypothesis

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

### 8.2 Family B - mandatory control

**DECIDED (D-11).**

Pixel-only, interlace-aware deblocking with no codec metadata, in the manner of the MERL
interlaced post-filter (PA S10), which checks for horizontal blocking at both candidate seam
positions. Its role is to falsify the claim that authoritative metadata is worth its cost. It is
not a candidate for adoption.

### 8.3 Family C - optional quality reference

**DECIDED (D-12).**

Shifted-DCT re-quantisation using the per-macroblock quantiser (PA S04, S05). Heavier; may solve a
broader restoration problem than intended. Must not delay testing A and B.

---

## 9. Stage 2 experiment (feasibility-gate evidence)

**DECIDED (D-15, D-16, D-18).**

### 9.1 Ladder

| Step | Configuration | Seam geometry | Quantiser |
|---|---|---|---|
| 1 | Unfiltered decode | - | - |
| 2 | Family B control | pixel-detected | none |
| 2b | Family A kernel | pixel-detected (both candidate positions) | emulated / fixed |
| 3 | Family A kernel | pixel-detected (both candidate positions) | real per-macroblock |
| 4 | Family A kernel | transform state (FRAME/FIELD/NONE) | real per-macroblock |
| 5 (optional) | Family A kernel | transform state | emulated / fixed |
| 6 (optional) | Family C | as designed | real per-macroblock |

"Pixel-detected (both candidate positions)" means horizontal seams are sought at both the
macroblock-edge and field-centreline positions, in the manner of PA S10, without dct_type (D-18).

### 9.2 Comparisons

```text
2  vs 2b : Family B control versus Family A under metadata-blind / fixed-QP conditions
2b vs 3  : value of the real per-macroblock quantiser, Family A otherwise held constant
3  vs 4  : value of authoritative transform geometry, Family A + real QP held constant
5  vs 4  : value of the real quantiser with authoritative geometry held constant
2  vs 4  : complete metadata-assisted Family A versus the strong Family B control
I vs P vs B (all steps) : effect of propagated / off-grid blocking (K-08)
```

2 vs 2b is not a single-variable kernel isolation unless the detector, eligibility logic and all
other non-kernel behaviour are explicitly held identical. The purpose of step 2b is to make 2b vs 3
and 3 vs 4 clean comparisons (D-18).

### 9.3 Material and measures

As proposal v0.5 section 7: ground-truth encodes (objective measures plus detail-loss and ringing
checks) and Dave's real captures (visual judgement). Results are reported separately for I, P and
B pictures where practical (D-16).

### 9.4 Architectural meaning

The ladder decides between two architectures (FCR 7):

- **Architecture A:** custom reference-decoder index. Justified only if metadata unavailable from
  ordinary decoder side data, chiefly transform state, adds worthwhile value (step 3 vs 4).
- **Architecture B:** decoder-exported per-macroblock quantiser (K-09) plus pixel-only geometry
  handling. Potentially sufficient if transform state adds little.

The custom `.idx2` remains provisional until this is settled (D-17).

---

## 10. Achievable-benefit bound

**AGREED (K-08, HYPOTHESIS supported by RESEARCHED evidence; CRV R3; FCR 9).**

A post-filter restricted to the current picture's known grid seams, pixel-only or
metadata-assisted, cannot systematically target blocking that motion compensation has propagated
to off-grid locations. This can bound the achievable improvement in P and B pictures. It is not, by itself, a reason to add motion vectors. A filter must not be judged
"wrong" for failing to remove artefacts no current-grid filter can reach.

---

## 11. Open questions

From FCR section 15 (O-01 to O-10, with O-10 split into O-10a/O-10b), plus O-11 and O-12 from the
trail and O-13 from the cold review.

| ID | Question | Where it gets answered |
|---|---|---|
| O-01 | Can BestSource expose or preserve FFmpeg's MPEG-2 per-macroblock QP side data in the intended workflow? | Early architecture investigation; need not block Stage 1 throwaway inspector/analyzer tooling; settle before committing to the final index path |
| O-02 | Exact FFmpeg QP semantics for skipped / no-residual macroblocks. | With O-01 |
| O-03 | Does the current inspector print stale or default DCT state for skipped / no-CBP macroblocks? | Stage 1 source check |
| O-04 | How should NONE affect filtering eligibility, including NONE / NONE macroblock edges? | Stage 2 design and experiment |
| O-05 | Strength range, units and equations. | After Stage 2 behaviour is understood |
| O-06 | Chroma strength / threshold relative to luma; whether chroma deblocking is useful on the target captures. | Stage 2 |
| O-07 | Do custom quantisation matrices occur in the target captures, and do they matter? | Stage 1 analyzer |
| O-08 | Do field pictures occur in the target captures, and how often? | Stage 1 analyzer |
| O-09 | How much visible blocking is on-grid versus propagated / off-grid? | Stage 2 (I/P/B breakdown) |
| O-10a | Does authoritative transform-state geometry improve Family A over pixel-detected geometry? | Stage 2 (step 3 vs 4) |
| O-10b | Does metadata-assisted Family A beat the strong pixel-only Family B control? | Stage 2 (step 2 vs 4) |
| O-11 | Do macroblock edges need treatment distinct from internal 8x8 seams? | Stage 2 |
| O-12 | Is frame/field prediction type relevant to visible macroblock-edge steps? | Stage 1 diagnostic (D-14) |
| O-13 | Is per-macroblock dct_type available from any standard FFmpeg or BestSource interface? None has been identified in the research so far (negative search result, not established absence). | With O-01 |

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
- chroma strength (O-06);
- field-picture geometry path (O-08);
- index field content and packing (`02_INDEX_FORMAT_SPEC.md`).

---

## 13. Evidence trail

The research and review files listed in section 0.3 are the evidence. They remain unchanged in
the project's research folder and are not superseded by this document. This document records the
ratifiable synthesis and points to them; it does not restate them.

---

## 14. Change log

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
