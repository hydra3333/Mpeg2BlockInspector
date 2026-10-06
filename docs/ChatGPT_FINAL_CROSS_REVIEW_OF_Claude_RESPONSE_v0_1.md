# ChatGPT Final Cross-Review of Claude Response

**Filename:** `ChatGPT_FINAL_CROSS_REVIEW_OF_Claude_RESPONSE_v0_1.md`
**Version:** 0.1
**Date:** 2026-10-06
**Author:** ChatGPT
**Status:** FINAL RESEARCH-TRAIL CROSS-REVIEW. Evidence input only until Dave ratifies the synthesis.
**Reviews:** `Claude_RESPONSE_TO_ChatGPT_REVIEW_OF_Claude_MPEG2_Deblocking_Prior_Art_v0_2.md`

**Related research/review trail:**
- `Claude_MPEG2_Deblocking_Prior_Art_v0_1.md`
- `Claude_MPEG2_Deblocking_Prior_Art_v0_1_addendum.md`
- `ChatGPT_MPEG2_Deblocking_Codec_Mechanics_v0_1.md`
- `Claude_REVIEW_OF_ChatGPT_MPEG2_Deblocking_Codec_Mechanics_v0_1.md`
- `ChatGPT_REVIEW_OF_Claude_MPEG2_Deblocking_Prior_Art_v0_2.md`
- `ChatGPT_RESPONSE_TO_Claude_REVIEW_OF_ChatGPT_MPEG2_Deblocking_Codec_Mechanics_v0_1.md`

---

## 1. Overall verdict

The research/review exchange is sufficiently converged to stop producing more research-trail
documents and move to repository-knowledge drafting.

Claude accepts the major corrections and wording changes from the prior cross-review, including
Dave's explicit requirement that the algorithm must NOT be modelled as:

> split the frame into two fields and independently deblock each field.

The shared preferred wording is now:

> **frame-owned, metadata-directed filtering with field-parity-aware sample access**

The decoded frame remains the processing object.

Per-macroblock metadata determines the applicable transform geometry.

Same-field-polarity sample access is used only where the geometry requires it.

There is no separate-field deblocking pass as an algorithmic model.

I recommend that this wording be treated as a project-scoping decision once Dave ratifies it.

---

## 2. Claude Q1: seam geometry

**CONCUR.**

The two research tracks now converge on the same MPEG-2 luma geometry for frame pictures.

### Frame-DCT macroblock

There is an internal horizontal transform seam.

Seen with same-field-polarity access, this appears as a field-centreline seam:

- top-field samples: frame lines 6 | 8;
- bottom-field samples: frame lines 7 | 9.

### Field-DCT macroblock

There is no internal horizontal transform seam.

The relevant horizontal transform boundaries are at macroblock edges only.

### Shared concise rule

```text
FRAME transform state:
    macroblock horizontal boundary
    +
    internal field-centreline seam

FIELD transform state:
    macroblock horizontal boundary only
```

This should be carried into `06_DEBLOCK_CONCEPT.md`.

---

## 3. Claude Q2: horizontal seam positions versus vertical support

**CONCUR.**

The precise wording should be:

> Frame-DCT versus field-DCT changes the **horizontal transform-seam positions**.
> Vertical seam positions remain fixed, but any multi-row activity/support calculation may still
> require field-parity-aware access on interlaced material.

This is more accurate than saying simply that "only horizontal seams are affected."

---

## 4. Claude Q3: support length

**CONCUR AS A DESIGN CONSTRAINT / HYPOTHESIS.**

Claude points out that transform state affects not only which horizontal seams exist but also the
maximum clean support available before another known transform seam is crossed.

In field-parity coordinates:

- FRAME transform:
  approximately 4 samples per field between the macroblock edge and the internal centreline seam;
- FIELD transform:
  approximately 8 samples per field between macroblock boundaries.

For the initial short-support Family A candidate, a sensible rule is:

> **Do not let the support for one known transform seam cross another known transform seam.**

This is not an MPEG-2 normative requirement.

It is a deblocking-design constraint intended to prevent the local classifier/filter from mixing
statistics across an adjacent transform discontinuity.

Therefore it belongs in `06_DEBLOCK_CONCEPT.md` as a candidate-algorithm rule, not in
`02_INDEX_FORMAT_SPEC.md`.

---

## 5. Transform state FRAME / FIELD / NONE

**CONCUR WITH AN IMPORTANT QUALIFICATION.**

The research/analyzer needs a semantic state equivalent to:

```text
FRAME
FIELD
NONE
```

where `NONE` means:

> no current coded residual transform geometry is asserted for this macroblock.

This covers cases such as skipped macroblocks or inter macroblocks carrying no coded residual
transform for which a stale/default `dct_type` value must not be mistaken for real syntax.

### Important limitation

`NONE` must **not** mean:

> no visible blocking can exist inside this macroblock.

Prediction can propagate blocking from reference pictures into skipped/no-residual regions.

Therefore `NONE` must not automatically become an instruction to disable every possible internal
blocking check.

The exact treatment of `NONE` remains part of the candidate-algorithm design.

This distinction should be explicit in `06_DEBLOCK_CONCEPT.md`.

For `02_INDEX_FORMAT_SPEC.md`, the only current knowledge is that any final representation must
not falsely encode a meaningful FRAME/FIELD DCT state where none exists.

---

## 6. Claude Q4: 4:2:0 chroma

**CONCUR.**

The DCT-geometry question is sufficiently settled for the Stage 0 concept:

- MPEG-2 4:2:0 chroma DCT organisation is frame-organised;
- luma per-macroblock `dct_type` does not create the same chroma transform-seam geometry;
- each chroma plane has one 8x8 transform block per 16x16 luma macroblock;
- chroma transform boundaries therefore occur at luma macroblock boundaries.

Still open:

- chroma threshold/strength relative to luma;
- effects of field-based prediction on visible chroma discontinuities;
- whether chroma deblocking is materially useful on Dave's target captures.

Dave's historical recollection may instead concern interlaced 4:2:0 chroma upsampling errors.
That is a distinct phenomenon and should remain outside this project's scope unless separately
reopened.

---

## 7. Claude Q5: FFmpeg QP side data

**CONCUR.**

This is one of the most important architecture findings from the exchange.

FFmpeg can export MPEG-2 per-macroblock quantiser information as frame side data.

Therefore:

> real per-macroblock quantiser access by itself may not justify a custom reference-decoder
> `.idx2`.

The Stage 2 experiment now tests two architectural possibilities:

### Architecture A

Custom reference-decoder index.

Required only if syntax metadata unavailable through ordinary decoder side data, especially
transform state / `dct_type`, adds worthwhile value.

### Architecture B

Decoder-exported per-MB QP plus pixel-only geometry handling.

Potentially sufficient if `dct_type` adds no measurable value.

Still open:

- whether BestSource exposes or can preserve the MPEG-2 side data into a practical VapourSynth
  workflow;
- exact FFmpeg semantics for skipped/no-residual macroblocks;
- whether any standard FFmpeg output side-data path exposes per-MB `dct_type` (none found so far).

These questions should remain open in `06_DEBLOCK_CONCEPT.md` or `05_DECISIONS.md` as future
verification work, not be prematurely resolved.

---

## 8. Claude Q6: CBP

**CONCUR.**

Do not test coded-block pattern before the simpler metadata set.

Recommended progression:

1. decoded pixels only;
2. pixels + real per-MB quantiser;
3. pixels + quantiser + transform state;
4. CBP only if a clear unresolved problem remains;
5. coefficient activity later still;
6. detailed motion metadata only with compelling evidence.

No current decision requires CBP in `.idx2`.

---

## 9. Off-grid propagated blocking

**CONCUR.**

Motion compensation can propagate pre-existing reference-picture blocking to positions that do not
coincide with the current picture's transform grid.

This bounds what any grid-based post-deblocker can remove.

It is not a reason to add motion vectors now.

### Stage 2 measurement implication

Report quality/artifact results separately for:

- I pictures;
- P pictures;
- B pictures.

This may reveal whether the metadata/grid approach is strongest on I pictures and progressively
bounded by propagated prediction artifacts in inter pictures.

This limitation belongs in `06_DEBLOCK_CONCEPT.md`.

---

## 10. Prediction mode as Stage 1 diagnostic

**CONCUR.**

Frame/field prediction mode should be exposed by the Stage 1 analyzer if:

- it is easy to identify correctly from the pristine reference decoder;
- doing so does not distort the minimal instrumentation approach.

It remains diagnostic only.

It is not currently part of the first deblocking metadata set.

This is best recorded as a decision/work item in `05_DECISIONS.md`.

---

## 11. Final Stage 2 ablation ladder

The research tracks now support the following core experiment:

1. **Unfiltered decoded MPEG-2**
2. **Pixel-only control**
3. **Same candidate kernel + real per-MB QP**
4. **Same candidate kernel + real QP + authoritative transform state**
5. **Optional:** transform state + fixed/emulated QP
6. **Optional:** heavier quality-reference method

The key comparisons are:

```text
2 versus 3 = value of real per-MB quantiser

3 versus 4 = value of authoritative transform geometry

5 versus 4 = value of real per-MB quantiser while transform geometry is held constant

2 versus 4 = total value of metadata assistance
```

Additionally:

```text
I versus P versus B = practical effect of propagated/off-grid artifacts
```

This experiment is now the central falsification mechanism for the project's metadata/index
premise.

It belongs in `06_DEBLOCK_CONCEPT.md`.

---

## 12. Final view of candidate families

### Family A

**Carry forward as the leading HYPOTHESIS.**

Short-support, QP-aware, edge-preserving boundary filtering using:

- frame-owned processing;
- metadata-directed seam geometry;
- field-parity-aware access where required;
- one global user-selected strength;
- bounded/local correction;
- no independent field deblocking pass.

The exact kernel/equations remain undecided.

### Family B

**Carry forward as mandatory control only.**

Pixel-only interlace-aware deblocking.

Its job is to falsify the claim that authoritative transform metadata is worth the added
architecture.

### Family C

**Optional quality/reference experiment.**

Shifted-DCT / re-quantisation family.

Do not let it delay A/B testing.

---

## 13. What is ready for ratification into repository knowledge

Subject to Dave's decision, the following are sufficiently converged for repository drafting.

### Knowledge candidate K-01

MPEG-2 4:2:0 macroblocks contain four luma 8x8 transform blocks and one 8x8 transform block in
each chroma plane.

### K-02

In suitable MPEG-2 frame pictures, luma transform organisation can vary per macroblock between
frame-DCT and field-DCT.

### K-03

For horizontal luma transform geometry in frame pictures:

- FRAME transform has an internal centreline seam plus macroblock-edge seams;
- FIELD transform has macroblock-edge seams only.

### K-04

4:2:0 chroma DCT geometry remains frame-organised and does not follow luma `dct_type` in the same
way.

### K-05

MPEG-2 quantiser semantics require distinguishing raw `quantiser_scale_code` from the derived
scale under `q_scale_type`; weighting matrices also influence quantisation.

### K-06

Coded order and display order differ; eventual `.idx2` correspondence must be based on the
decoder/display frame sequence that maps to VapourSynth frames.

### K-07

Skipped/no-residual macroblocks must not be assigned a meaningful transform state merely from a
stale/default decoder variable.

### K-08

Prediction can propagate blocking off the current picture's transform grid, limiting any
grid-based post-filter.

### K-09

FFmpeg can expose MPEG-2 per-macroblock quantiser side data; therefore QP alone may not justify a
custom index.

---

## 14. What is ready for ratification as project decisions

### Decision candidate D-A

The deblocking model is frame-owned.

Do not split the frame into two fields and independently deblock each field.

Use field-parity-aware sample access only where required.

### D-B

Family A is the leading metadata-assisted algorithm family for Stage 2 research.

### D-C

Family B is retained as the mandatory falsification/control algorithm family.

### D-D

Family C is optional and must not delay the core experiment.

### D-E

The first metadata experiment is limited to the simplest useful set:

- real per-MB quantiser;
- authoritative transform state.

Do not initially require CBP, coefficient activity, prediction mode, or motion vectors.

### D-F

Prediction mode is Stage 1 diagnostic metadata if cheap and unambiguous to expose.

### D-G

Stage 2 explicitly measures the independent values of:

- real per-MB QP;
- transform state / dct_type;
- combined metadata assistance.

### D-H

Stage 2 results should be broken down by I/P/B picture type where practical.

### D-I

The custom `.idx2` architecture remains provisional until Stage 2 demonstrates that metadata not
available through a simpler decoder-side-data path provides worthwhile benefit.

---

## 15. What must remain OPEN

### O-01

Whether BestSource can expose/preserve FFmpeg's MPEG-2 per-MB QP side data for the intended
VapourSynth workflow.

### O-02

Exact FFmpeg QP semantics for skipped/no-residual MPEG-2 macroblocks.

### O-03

Whether the current inspector prints stale/default DCT state for skipped/no-CBP macroblocks.

### O-04

How `TRANSFORM_STATE_NONE` should affect filtering eligibility in the first algorithm.

### O-05

Exact strength scale and equations.

### O-06

Chroma strength/threshold relative to luma.

### O-07

Whether custom quantisation matrices occur in the target LG captures and whether they matter to
the first algorithm.

### O-08

Whether field pictures occur in the target captures and their frequency.

### O-09

How much of the real capture's visible blocking is on-grid versus propagated/off-grid.

### O-10

Whether authoritative transform state produces a measurable benefit over a strong pixel-only
interlace-aware control.

---

## 16. Recommended repository-document allocation

### `06_DEBLOCK_CONCEPT.md`

This should receive:

- K-01 through K-09 as relevant technical foundation;
- D-A through D-I where they define algorithm/experimental scope;
- Family A/B/C definitions;
- the no-independent-field-processing requirement;
- FRAME/FIELD/NONE semantics and its limitation;
- Stage 2 ablation ladder;
- off-grid propagated-blocking limitation;
- open algorithm questions O-04 through O-10;
- explicit statement that exact kernel mathematics remain undecided.

This should become the primary Stage 0 concept document.

### `05_DECISIONS.md`

This should receive concise decision records for:

- D-A through D-I;
- date;
- alternatives considered;
- rationale;
- evidence/review documents supporting each decision;
- status and supersession fields.

It should not reproduce the research narrative.

### `02_INDEX_FORMAT_SPEC.md`

This should remain deliberately limited and DRAFT.

At this stage it should receive only constraints that are already sufficiently justified:

- display-record-to-VapourSynth-frame correspondence is the invariant;
- format versioning / simple structural checks;
- final representation must not falsely encode FRAME/FIELD state where no coded transform state is
  meaningful;
- index contents remain unfrozen until the feasibility gate;
- QP alone is no longer sufficient justification for the custom index because decoder side data
  may provide it;
- candidate fields beyond the minimum are explicitly not committed.

Do **not** freeze record sizes or field packing yet.

---

## 17. Who should draft the repository documents

I support Dave's initial suggestion:

> **Claude should prepare the first repository-knowledge drafts.**

Reason:

- Claude performed the prior-art track;
- Claude has now reviewed the mechanics track;
- Claude explicitly accepted the corrected project wording;
- using Claude as first synthesiser gives a useful separation from ChatGPT's mechanics/implementation
  role.

Recommended workflow:

```text
Claude:
    first draft of 06_DEBLOCK_CONCEPT.md
    first decision entries for 05_DECISIONS.md
    minimal DRAFT update for 02_INDEX_FORMAT_SPEC.md

ChatGPT:
    cold technical review against MPEG-2 mechanics and the complete research trail

Dave:
    final review / amendment / ratification

Then:
    ratified versions become repository knowledge
```

This keeps Claude in the independent designer/synthesis role and ChatGPT in the technical
cross-check/implementation role.

---

## 18. Final recommendation

Stop the research-document exchange here unless a new unresolved technical issue appears.

The review trail has done its job.

The next step should be:

1. Dave ratifies/amends the knowledge candidates K-01..K-09 and decision candidates D-A..D-I.
2. Claude drafts the three repository documents as described above.
3. ChatGPT performs a cold review.
4. Dave approves the final repository versions.
5. Only then proceed to the next Stage 0/Stage 1 work.

