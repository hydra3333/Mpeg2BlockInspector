# Stage 2 Experimental Deblocking Design

**Filename:** `Stage2_Experiment_Design_v0_1.md`  
**Version:** 0.1  
**Date:** 2026-10-07  
**Drafted by:** ChatGPT  
**Status:** DRAFT FOR CLAUDE REVIEW AND DAVE RATIFICATION. No Stage 2 code is authorised by this draft.  
**Stage 1 prerequisite:** `Stage1_Evidence_and_Gate_Report_v0_3.md` ratified by Dave.  
**Scope:** Stage 2 Python/scalar prototype and experiment design only.

---

## 0. Purpose

Stage 1 has established a credible, frame-correspondent metadata source for the tested MPEG-2
frame-picture material. Stage 2 now tests the project's central feasibility question:

> **Does MPEG-2 metadata materially improve post-deblocking enough to justify the added
> architecture, especially authoritative per-macroblock transform geometry?**

This is a falsification experiment, not an implementation commitment.

The Stage 2 result is allowed to conclude that:

- real per-macroblock QP is useful;
- authoritative transform state is useful;
- pixel-only filtering is sufficient;
- the custom index is not justified;
- or the entire filter concept does not produce enough benefit to continue.

No outcome is preselected.

---

## 1. Authority and inherited constraints

This draft is subordinate to the ratified repository knowledge:

- `05_DECISIONS.md`
- `06_DEBLOCK_CONCEPT.md`
- `02_INDEX_FORMAT_SPEC.md`

and to the ratified Stage 1 evidence summary:

- `Stage1_Evidence_and_Gate_Report_v0_3.md`

The project proposal remains useful workflow/context, but does not override later ratified
repository knowledge.

The following inherited constraints are treated as fixed for this Stage 2 draft unless Dave
explicitly changes them.

### 1.1 Frame-owned processing

The algorithm is frame-owned.

Do **not** split an interlaced frame into two independent field-processing passes.

Use field-parity-aware sample access only where the applicable geometry requires it.

### 1.2 Transform-state semantics

The Stage 1 semantic states are:

```text
FRAME
FIELD
NONE
```

`NONE` means:

> no current coded residual transform geometry is asserted for that macroblock.

It does **not** mean:

> no visible blocking can exist there.

Prediction may propagate blocking into skipped/no-residual areas.

### 1.3 Luma geometry in frame pictures

For horizontal luma transform geometry:

```text
FRAME:
    macroblock horizontal boundary
    +
    internal field-centreline seam

FIELD:
    macroblock horizontal boundary only

NONE:
    no current residual transform seam is asserted
```

The FRAME internal seam is observed through same-field-polarity access:

```text
top-field samples:    frame lines 6 | 8
bottom-field samples: frame lines 7 | 9
```

relative to the 16-line macroblock.

Frame-DCT versus field-DCT changes horizontal seam positions. Vertical grid positions remain fixed,
although multi-row support/activity calculations on interlaced material may still require
field-parity-aware access.

### 1.4 4:2:0 chroma

For MPEG-2 4:2:0 frame pictures, chroma transform geometry remains frame-organised and does not
follow luma `dct_type` in the same way.

Chroma threshold/strength remains an open question.

### 1.5 Support constraint

For the initial short-support Family A candidate:

> **Support for one known transform seam must not cross another known transform seam.**

This is a deblocking-design constraint, not an MPEG-2 normative rule.

### 1.6 Initial metadata scope

The first metadata experiment is limited to:

- real effective per-macroblock quantiser scale;
- authoritative transform state.

Do not initially require:

- coded-block pattern as a filtering input;
- coefficient activity;
- prediction mode;
- motion vectors.

Stage 1 may contain more diagnostic information, but availability does not imply Stage 2 use.

### 1.7 Algorithm families

**Family A** remains the leading metadata-assisted hypothesis:

- short-support;
- QP-aware;
- edge-preserving;
- frame-owned;
- field-parity-aware where needed;
- metadata-directed seam geometry;
- bounded/local correction;
- one eventual global user strength;
- scalar-friendly and later AVX2-friendly.

**Family B** is mandatory as the strong pixel-only falsification/control.

**Family C** is optional quality/reference work and must not delay the A/B experiment.

---

## 2. Stage 2 questions

The experiment must answer these questions separately.

### Q2-01 - Does the candidate filtering family help at all?

Can a short-support edge-preserving filter reduce visible MPEG-2 blocking without unacceptable
detail loss or edge damage?

### Q2-02 - Does real per-macroblock QP help Family A?

When Family A's geometry/detector/kernel are otherwise held constant, does replacing a fixed or
emulated QP with the real effective per-macroblock quantiser improve the result?

### Q2-03 - Does authoritative transform state help Family A?

With the same Family A kernel and real QP, does authoritative FRAME/FIELD/NONE geometry outperform
pixel-detected candidate geometry?

### Q2-04 - Does the complete metadata-assisted Family A beat the strong pixel-only Family B?

This is the practical architecture comparison.

### Q2-05 - Is the benefit different for I, P and B pictures?

This tests the expected practical limitation from prediction-propagated/off-grid blocking.

### Q2-06 - Is the custom-index architecture justified?

QP alone is not enough justification if a simpler decoder-side-data path can supply it.

The custom index earns a production role only if metadata unavailable through the simpler path,
especially authoritative transform state, provides worthwhile benefit.

### Q2-07 - How should `NONE` be treated?

Does metadata-assisted Family A perform best when `NONE`:

- suppresses internal transform-seam filtering;
- falls back to pixel detection;
- or uses another bounded rule?

This must be measured rather than assumed.

---

## 3. Experimental material

### 3.1 Formal development/reference pair

Use:

```text
TEST_4A_A003.mpg
TEST_4A_A003_blocky.mpg
```

Known Stage 1 properties include:

- 720x576;
- 300 frames;
- 45x36 macroblocks;
- all frame pictures;
- no repeat-first-field;
- strong per-macroblock FRAME/FIELD mixture;
- formal-original effective QP approximately 2..36, predominantly non-linear scaling;
- formal-blocky QP = 62 for every macroblock;
- formal-original custom non-intra matrix present;
- formal-blocky custom non-intra matrix absent.

The blocky file is deliberately much more compressed and is the primary practical stress input.

### 3.2 Corroborating/hold-out pair

Use:

```text
TEST_2A_A001.mpg
TEST_2A_A001_blocky.mpg
```

Known differences make this useful as more than duplicate evidence:

- 704x576;
- 300 frames;
- 44x36 macroblocks;
- different original GOP/picture-type pattern;
- no custom matrices;
- original QP spans the full MPEG-2 non-linear effective scale through 80;
- blocky QP = 62 throughout.

### 3.3 Development-versus-holdout discipline

To reduce overfitting:

- use the `TEST_4A_A003` pair for first-pass parameter development;
- lock a candidate parameter set;
- then evaluate unchanged on the `TEST_2A_A001` pair.

If the holdout result fails badly, do not silently retune and still call it validation.

A second tuning round may be performed, but it must be labelled as such and followed by a new
independent validation source if available.

### 3.4 Reference-quality qualification

The non-blocky MPG is **not pristine ground truth**.

It is a higher-quality practical reference for the deliberately degraded/blocky encode.

Therefore reference-based numerical metrics mean:

> movement toward or away from the decoded higher-quality source,

not:

> absolute restoration quality.

Dave's visual judgement on real target material remains essential.

---

## 4. Pre-experiment correspondence check between each original/blocky pair

Stage 1 proved:

```text
index record N == BestSource frame N
```

for each file independently.

Before using the non-blocky source as a paired numerical reference for its blocky transcode,
Stage 2 must also verify:

```text
original decoded frame N corresponds to blocky decoded frame N
```

for each pair.

### 4.1 Cheap cross-pair check

For each frame, compare the blocky frame against original frames in a small temporal window,
for example:

```text
N-2 .. N+2
```

using luma mean absolute error or mean squared error.

Expected condition:

```text
best match occurs at original frame N
```

for all or effectively all non-ambiguous frames.

Ambiguous very-static frames may tie and should be reported, not treated as failures.

This check is not a unique-content cryptographic proof. It is sufficient to prevent an accidental
one-frame temporal displacement from corrupting the Stage 2 paired metrics.

---

## 5. Prototype architecture

Stage 2 is a research prototype, not the production VapourSynth plugin.

### 5.1 Language and execution model

Preferred first implementation:

- Python 3;
- VapourSynth/BestSource for decoded frames;
- NumPy arrays for scalar/reference experiment operations where convenient;
- Stage 1 `.idx` reader for per-frame/per-MB metadata;
- deterministic single-frame operations;
- serial experimental runs acceptable.

No AVX2 work belongs in Stage 2.

### 5.2 Inputs

For each test source:

```text
BestSource decoded frame
+
matching Stage 1 index record
```

The Stage 1 reader must reject:

- wrong magic/version;
- incomplete index;
- dimension mismatch;
- frame-count mismatch;
- record ordinal mismatch;
- unsupported picture structure for this experiment.

Do not weaken Stage 1 validity simply because Stage 2 is experimental.

### 5.3 Outputs

The prototype should be able to produce, per variant:

- filtered lossless frames or a lossless comparison clip;
- difference frames/maps;
- seam masks/eligibility maps;
- CSV or machine-readable metric results;
- per-frame summary;
- aggregate I/P/B summary.

Optional diagnostic image output should support inspecting selected frames and boundaries.

### 5.4 Reproducibility

Every run should record:

- input filename;
- index filename;
- variant ID;
- all numeric parameters;
- strength setting;
- frame range;
- script/tool version;
- aggregate metrics.

No result should depend on an unrecorded interactive setting.

---

## 6. Initial plane scope

### 6.1 Luma first

**PROPOSAL FOR REVIEW:** The core feasibility experiment should start on luma only.

Reasons:

- the central transform-state hypothesis concerns luma geometry;
- chroma does not follow luma `dct_type` in the same way;
- chroma strength remains an open question;
- keeping chroma unchanged makes QP/geometry comparisons cleaner.

The prototype should preserve U/V unchanged during the first ablation.

### 6.2 Chroma follow-up

Chroma experimentation is permitted only after the core luma comparisons are interpretable.

A later chroma test may use:

- macroblock-grid boundaries only;
- independent chroma strength;
- no luma `dct_type` internal-seam mapping.

Chroma must not delay the central metadata feasibility result.

---

## 7. Common boundary-processing abstraction

Family A and, where practical, Family B should share a common one-dimensional boundary interface so
that experiments compare geometry/metadata rather than unrelated plumbing.

Conceptually, a boundary operation receives:

```text
samples on side P
samples on side Q
boundary orientation
sample stride / field-parity stride
effective QP or emulated QP
global experimental strength
eligibility/detector state
```

For a vertical boundary:

```text
... p2 p1 p0 | q0 q1 q2 ...
```

uses adjacent horizontal samples.

For a horizontal boundary on interlaced frame material, the same abstract sequence may use frame
row stride 2 when same-field-polarity access is required.

The prototype must make the access pattern explicit; it must not hide field parity inside ad hoc
index arithmetic.

---

## 8. Candidate Family A detector/kernel

The exact production kernel is not yet ratified. Stage 2 therefore uses a deliberately parameterised
short-support candidate whose purpose is to test the metadata hypothesis.

### 8.1 Required properties

The candidate must:

- operate only across selected grid/seam positions;
- preserve strong genuine edges by local-activity/step gating;
- use short support;
- clamp correction magnitude;
- allow thresholds/correction limits to scale with effective QP;
- permit identical kernel mathematics under pixel-detected and authoritative geometry;
- be implementable later with integer scalar code and AVX2.

### 8.2 Starting detection model

The first candidate should combine the prior-art ideas already accepted for experiment:

1. boundary step magnitude;
2. local same-side activity;
3. bounded local range/flatness;
4. QP-scaled thresholds when real/emulated QP is enabled.

No one borrowed codec's threshold table should be copied blindly because MPEG-2 effective quantiser
semantics differ from MPEG-4/H.264 QP.

Use a small number of dimensionless tuning coefficients multiplying the MPEG-2 effective QP.

Example conceptual quantities:

```text
D  = abs(q0 - p0)                  boundary step
LP = local activity on P side
LQ = local activity on Q side
R  = local max - local min
Q  = selected boundary effective quantiser
S  = experimental global strength
```

Candidate gating form:

```text
D must look block-like relative to LP/LQ
and
D/R must remain below a strong-edge rejection condition
and, when QP is enabled,
relevant limits scale monotonically with Q * S
```

This document intentionally does not freeze the coefficients.

### 8.3 Starting correction model

Use a bounded local correction that primarily moves `p0` and `q0` toward each other, optionally
with smaller `p1`/`q1` participation in flat mode.

Requirements:

- zero-sum or near-zero-sum local correction where practical;
- clipping to valid sample range;
- correction magnitude clamped by a QP/strength-derived limit;
- no support crossing another known seam.

Two modes are permitted:

- **detail mode:** minimal `p0/q0` correction;
- **flat mode:** slightly wider short support.

This is intentionally Annex-F/libpostproc-like in experimental spirit, not a claim that any
existing normative filter is being reproduced.

### 8.4 Parameter search discipline

Use a small, declared parameter grid.

Do not search hundreds of unconstrained combinations against the same 300 frames.

Recommended first-pass variables:

```text
step/activity coefficient
strong-edge rejection coefficient
correction clip coefficient
global strength
```

After a reasonable candidate is selected on the development pair, lock it for holdout evaluation.

---

## 9. Geometry modes used by the ablation

### 9.1 Pixel-detected geometry

For Family A without authoritative transform state:

- vertical candidate seams remain on the known luma coding grid;
- horizontal candidate positions include the plausible macroblock-edge and internal positions;
- local pixel tests decide whether a candidate behaves like a block boundary.

This is deliberately allowed to test positions that authoritative metadata can rule in or rule out.

It is the geometry used by Stage 2 steps 2b and 3.

### 9.2 Authoritative geometry

For Family A with transform state:

- FRAME MBs expose their applicable internal horizontal field-centreline seam;
- FIELD MBs do not expose that internal horizontal seam;
- macroblock edges remain eligible coding-grid locations;
- `NONE` does not invent a current residual transform seam.

This is the geometry used by steps 4 and 5.

### 9.3 Mixed-neighbour boundaries

A macroblock boundary can have different state/QP on each side.

**Initial QP proposal for review:**

```text
Q_boundary = rounded mean(Q_left, Q_right)
```

for a shared macroblock boundary.

An internal seam uses the containing macroblock's QP.

This mean rule is a neutral first hypothesis, not project knowledge.

If Claude identifies a stronger MPEG-2/post-filter precedent for min/max/other treatment, review it
before implementation.

### 9.4 `NONE` policy as an explicit experiment

For internal horizontal positions in a `NONE` macroblock, compare at least:

**N0 - authoritative conservative**

```text
do not assert/filter an internal transform seam
```

**N1 - pixel fallback**

```text
allow pixel detector to test the candidate internal position
```

Macroblock edges remain eligible pixel discontinuity locations even where one or both macroblocks
are `NONE`.

The better rule should be chosen from evidence, not semantics alone.

---

## 10. Stage 2 ablation ladder

The corrected ladder is:

### Step 1 - unfiltered

```text
decoded blocky source
```

Purpose: baseline.

### Step 2 - Family B strong pixel-only control

No Stage 1 QP or transform state used for decisions.

Purpose: serious falsification baseline, not a straw man.

### Step 2b - Family A, metadata-blind/fixed-QP, pixel-detected geometry

Use:

- Family A detector/kernel;
- fixed/emulated QP;
- pixel-detected geometry;
- no authoritative transform state.

Purpose:

- establish Family A behaviour without real metadata;
- create a clean base for isolating real-QP value in 2b vs 3.

Do **not** describe 2 vs 2b as a pure kernel comparison unless all other detector/eligibility/support
logic is genuinely identical.

### Step 3 - Family A + real per-MB QP + pixel-detected geometry

Same Family A machinery as step 2b.

Change:

```text
fixed/emulated QP -> real effective per-MB QP
```

Primary comparison:

```text
2b vs 3 = value of real per-MB QP within Family A
```

### Step 4 - Family A + real QP + authoritative transform geometry

Same Family A kernel and real QP as step 3.

Change:

```text
pixel-detected candidate geometry -> authoritative FRAME/FIELD/NONE geometry
```

Primary comparison:

```text
3 vs 4 = value of authoritative transform-state geometry within Family A
```

Practical architecture comparison:

```text
2 vs 4 = complete metadata-assisted Family A vs strong pixel-only Family B
```

### Step 5 - optional Family A + fixed/emulated QP + authoritative geometry

Change from step 4:

```text
real QP -> fixed/emulated QP
```

Comparison:

```text
5 vs 4 = value of real QP while authoritative geometry is held constant
```

This is optional if 2b vs 3 already answers the QP question convincingly.

### Step 6 - optional Family C

Heavier shifted-DCT/re-quantisation quality/reference experiment.

Do not begin Step 6 until Steps 1-4 are interpretable.

---

## 11. Family B requirements

Family B must be strong enough to falsify the metadata premise.

It must not be intentionally simplistic.

### 11.1 Required characteristics

Family B should:

- operate on decoded pixels only;
- know the regular MPEG-2 grid from frame coordinates, not from the index;
- be interlace-aware;
- use field-parity-aware tests for horizontal boundaries where appropriate;
- detect block-like steps from local pixel activity;
- reject obvious genuine edges;
- use short bounded correction.

### 11.2 No hidden metadata

Family B must not use:

- per-MB QP;
- FRAME/FIELD/NONE;
- coding state;
- picture type as a filtering decision.

Picture type may still be used later for reporting metrics.

---

## 12. Strength handling

The eventual filter is intended to expose one global user strength.

Stage 2 needs a sweep rather than a prematurely frozen UI scale.

Use a small ordered set such as:

```text
OFF
LOW
NOMINAL
HIGH
```

or equivalent numeric values.

Requirements:

- OFF must be bit-exact input;
- increasing strength must monotonically increase or relax the permitted correction/threshold scale;
- the same strength definition must be used across compared Family A variants;
- do not tune separate strengths independently for each variant merely to make one win.

For fair Family A versus Family B comparison, report both:

- same nominal strength position;
- best visually/metric-reasonable setting for each family, clearly labelled.

---

## 13. Metrics

No single metric decides the project.

Use several layers.

### 13.1 Whole-frame paired-reference metrics

For the blocky input and its higher-quality reference:

- luma MSE;
- luma PSNR;
- luma MAE.

SSIM may be added if a reliable implementation is already available, but Stage 2 should not acquire
a large dependency merely for SSIM.

### 13.2 Boundary-local reference metrics

Because whole-frame PSNR can hide a small but useful boundary improvement, calculate error in
windows around candidate grid seams separately.

Suggested reporting:

```text
vertical seam neighbourhood error
horizontal macroblock-seam neighbourhood error
horizontal internal-seam neighbourhood error
non-seam region error
```

For authoritative variants, additionally separate:

```text
FRAME MB internal seams
FIELD MB candidate internal positions
NONE MB candidate internal positions
```

### 13.3 Change/blur penalty

Measure how much the filter changes pixels away from eligible boundaries.

Useful simple measures:

- mean absolute output-input change;
- percentage of changed pixels;
- change energy outside seam neighbourhoods.

A filter that improves seam metrics by blurring large non-seam areas should not pass.

### 13.4 Boundary discontinuity metrics

For each tested seam, measure quantities such as:

```text
abs(q0 - p0)
local same-side gradients
boundary step / local activity ratio
```

Report before and after.

This is diagnostic evidence, not a standalone quality score.

### 13.5 I/P/B breakdown

All practical metrics should be aggregated separately for:

- I pictures;
- P pictures;
- B pictures;
- all pictures.

This directly tests whether propagated prediction artifacts reduce the benefit of current-grid
metadata in P/B frames.

### 13.6 Visual evidence

Produce matched crops or lossless clips for Dave to inspect.

At minimum include examples of:

- flat/blocky areas;
- strong legitimate edges;
- texture/detail;
- FRAME-heavy regions;
- FIELD-heavy regions;
- NONE-heavy regions;
- I/P/B pictures.

Blind or shuffled A/B presentation is preferred where practical.

---

## 14. Frame/region selection

Do not rely only on hand-picked favourable examples.

### 14.1 Full-clip metrics

Run numerical metrics over all 300 frames.

### 14.2 Deterministic diagnostic subset

Also choose a deterministic subset based on metadata/statistics, for example:

- highest mean QP frames;
- lowest mean QP frames;
- highest FRAME proportion;
- highest FIELD proportion;
- highest NONE proportion;
- representative I, P and B frames;
- formal-original exceptional frame 298 as a metadata-path regression case.

Selection rules must be defined before viewing filtered results where possible.

### 14.3 Visual-interest additions

Dave may add visually troublesome frames manually.

Those are useful, but they must be labelled manually selected rather than statistical samples.

---

## 15. Treatment of custom quantisation matrices

Stage 1 found:

- formal original: custom non-intra matrix present throughout;
- formal blocky: no custom non-intra matrix;
- corroborating pair: no custom matrices.

The first Family A experiment should **not** immediately consume matrix coefficients.

Reason:

- the ratified first metadata set is QP + transform state;
- adding matrices now would confound the test of whether those simpler metadata are sufficient.

However, matrix presence must be recorded with the result because the formal original/blocky pair
differs in this respect.

If QP-based thresholding behaves inconsistently across sources, matrix influence becomes a
candidate follow-up before adding more exotic metadata.

---

## 16. FFmpeg/BestSource QP side-data architecture question

This remains an architecture investigation, not a blocker for the core Stage 2 algorithm test.

### 16.1 Core experiment source

For Steps 3-5, use the already validated Stage 1 index QP.

This guarantees that:

- the effective QP semantics are known;
- skipped/inherited values follow the inspected decoder semantics;
- QP and transform state are frame-correspondent in one source.

### 16.2 Parallel architecture check

Separately determine whether the intended BestSource/VapourSynth workflow can expose or preserve
FFmpeg's MPEG-2 per-MB QP side data cleanly.

If yes, later compare that QP map against Stage 1 effective QP.

Do not make Stage 2 algorithm progress depend on this connector/path investigation.

---

## 17. Feasibility gate

Stage 2 must end with an explicit decision, not an indefinite prototype.

### 17.1 Evidence needed

The gate report should show:

- full ablation results;
- development and holdout behaviour;
- I/P/B breakdown;
- visual examples;
- artifact/detail trade-offs;
- effect of real QP;
- effect of authoritative transform state;
- Family A versus Family B;
- any dependence on custom matrices;
- known failure modes.

### 17.2 Custom-index justification test

The custom index remains justified for continuation only if metadata that is not readily available
through the simpler decoder path provides worthwhile benefit.

The strongest current candidate is authoritative transform state.

Therefore:

```text
If Step 4 is not meaningfully better than Step 3,
the case for indexing transform state is weakened substantially.

If Step 4 is not meaningfully better than Step 2,
the case for the metadata-assisted architecture as a whole is weakened.

If real QP helps but transform state does not,
investigate the simpler decoder-side QP architecture before committing to final .idx2.
```

### 17.3 No arbitrary numerical pass threshold in advance

Do not invent a PSNR threshold merely to make the decision mechanical.

"Meaningful" should combine:

- repeatable numerical improvement;
- localisation of the improvement to actual artifacts;
- absence of unacceptable detail damage;
- Dave's visual judgement;
- consistency across the formal and corroborating material.

Dave makes the final feasibility decision.

---

## 18. Suggested Stage 2 implementation sequence after this design is ratified

No coding should start until this design has been reviewed and ratified.

After ratification:

### S2-I1 - read-only experiment harness

Implement:

- BestSource frame input;
- Stage 1 index reader;
- frame/index validation;
- cross-pair temporal alignment check;
- deterministic metric framework;
- no filtering yet.

Acceptance:

- exact frame/index correspondence maintained;
- original/blocky frame pairing validated;
- metrics reproducible.

### S2-I2 - seam-map diagnostics

Implement:

- coding-grid masks;
- authoritative FRAME/FIELD/NONE seam maps;
- pixel-detected candidate maps;
- diagnostic render/export.

Acceptance:

- hand-check representative frames against Stage 1 metadata;
- frame 298 regression confirms `frame_pred_frame_dct=1` behaviour does not invent per-MB dct bits.

### S2-I3 - Family A scalar candidate

Implement one parameterised short-support detector/kernel.

First run Step 2b only.

Acceptance:

- OFF bit-exact;
- no support crosses forbidden known seam;
- deterministic;
- diagnostic correction maps available.

### S2-I4 - real-QP ablation

Add Step 3.

Run:

```text
2b vs 3
```

on development then holdout.

### S2-I5 - authoritative geometry ablation

Add Step 4 plus N0/N1 `NONE` treatment.

Run:

```text
3 vs 4
2 vs 4
```

### S2-I6 - Family B control

Family B may be implemented before I3 if Claude/Dave prefer, but it must exist before the final gate.

### S2-I7 - optional experiments

Only if needed:

- Step 5 fixed-QP authoritative geometry;
- chroma;
- matrix-aware QP interpretation;
- CBP;
- Family C.

Do not add them automatically.

---

## 19. Explicit non-goals for Stage 2

Stage 2 does not:

- freeze final `.idx2`;
- optimise index size;
- build a production indexer;
- build the C++ VapourSynth plugin;
- use AVX2;
- define production UI/parameter syntax;
- solve field-picture processing;
- solve damaged-stream support;
- prove Stage 5 unique frame identity;
- use motion vectors;
- add CBP unless evidence demands it;
- declare Family A successful before the ablation.

---

## 20. Review questions for Claude

Claude is asked to review this draft against the ratified repository knowledge and prior-art work.

Please address:

1. **Ablation correctness:** Is the 1 / 2 / 2b / 3 / 4 / optional 5 / optional 6 ladder faithful to the final ratified intent?
2. **Family A prototype:** Is the proposed parameterised short-support step/activity/flatness/QP-gated kernel a fair first test, or is there a better minimal candidate supported by the prior-art evidence?
3. **Family B strength:** Is the specification sufficient to prevent Family B becoming a straw man?
4. **Luma-first scope:** Is luma-only appropriate for the core feasibility gate, with chroma deferred?
5. **QP at shared boundaries:** Is rounded mean of the two neighbouring effective QPs a defensible neutral first hypothesis, or should another rule be tested first?
6. **NONE experiment:** Are N0 conservative versus N1 pixel fallback the right first alternatives?
7. **Metrics:** Are the proposed whole-frame, seam-local, non-seam-change and I/P/B metrics sufficient for the first gate?
8. **Paired-reference discipline:** Is using the higher-quality MPEG as a practical reference, explicitly not pristine ground truth, methodologically sound for these experiments?
9. **Overfitting:** Is development on `TEST_4A_A003` with `TEST_2A_A001` as holdout adequate for this bounded prototype?
10. **Scope/overreach:** Does this draft accidentally decide any open repository issue that should remain experimental?
11. **Implementation order:** Would you reorder S2-I1 through S2-I7 before coding begins?

Please identify blocking issues separately from optional refinements.

---

## 21. Proposed disposition after review

If Claude and Dave accept this design:

1. ratify a corrected Stage 2 design version;
2. implement **S2-I1 only** first;
3. review its output before implementing filtering;
4. continue incrementally through the ablation;
5. produce a Stage 2 feasibility/gate report before any Stage 3/final-index commitment.

This preserves the project's evidence-first workflow.

---

## 22. Change log

### v0.1 - 2026-10-07

- First Stage 2 experiment-design draft after ratified Stage 1 PASS.
- Carries forward frame-owned processing, FRAME/FIELD/NONE semantics, luma geometry, support constraint and minimal metadata scope.
- Uses corrected ablation ladder with Step 2b to isolate real-QP value within Family A.
- Defines Family B as a mandatory strong falsification control.
- Proposes luma-first bounded Python/scalar experimentation.
- Defines development/holdout discipline using `TEST_4A_A003` and `TEST_2A_A001` pairs.
- Adds cross-pair original/blocky temporal correspondence precheck before paired-reference metrics.
- Proposes a parameterised short-support edge-preserving Family A test kernel without freezing production mathematics.
- Makes `NONE` handling an explicit N0/N1 experiment.
- Defines whole-frame, seam-local, change/blur and I/P/B metric layers.
- Keeps FFmpeg/BestSource QP side-data investigation parallel rather than blocking.
- Defines an explicit feasibility gate for real QP, transform-state value and custom-index justification.
- Keeps final `.idx2`, C++/API4, AVX2, CBP, motion vectors and Stage 5 proof outside scope.
