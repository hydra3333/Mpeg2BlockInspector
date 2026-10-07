# Stage 2 Experimental Deblocking Design

**Filename:** `Stage2_Experiment_Design_v0_2.md`  
**Version:** 0.2  
**Date:** 2026-10-08  
**Drafted by:** ChatGPT  
**Status:** DRAFT FOR CLAUDE REVIEW AND DAVE RATIFICATION. No Stage 2 code is authorised by this draft.  
**Stage 1 prerequisite:** `Stage1_Evidence_and_Gate_Report_v0_3.md` ratified by Dave.  
**Repository authority:** `05_DECISIONS.md` v1.1 RATIFIED; `06_DEBLOCK_CONCEPT.md` v1.1 RATIFIED; `02_INDEX_FORMAT_SPEC.md` v0.4 current ratified-constraints baseline, still DRAFT / NOT FROZEN.  
**Scope:** Stage 2 Python/scalar prototype and experiment design only.

---

## 0. Purpose

Stage 1 established a credible, output-frame-correspondent metadata source for the tested MPEG-2
frame-picture material.

Stage 2 now addresses the ratified project question:

> **Given authoritative indexed MPEG-2 geometry and QP, what filtering rule produces useful luma
> and chroma deblocking without unacceptable damage, and which indexed metadata are actually needed
> by the final production filter?**

The production architecture is already decided to be **index-driven** (D-24).

Therefore Stage 2 does **not**:

- build a pixel seam-position detector;
- build Family B as a pixel-only architecture control;
- compare index-driven versus pixel-only production architectures;
- require the custom index to justify its existence by beating a pixel-only alternative;
- use an existing external filter as a planned yardstick.

Those older v0.1 experiments are superseded by the ratified repository direction.

Stage 2 may still conclude that:

- the chosen filtering kernel is ineffective;
- useful artifact reduction requires unacceptable detail loss;
- off-grid / prediction-propagated blocking bounds the achievable benefit too severely;
- chroma filtering causes unacceptable colour damage or field mixing;
- more filtering research is needed before production implementation;
- or the project should stop.

That is the feasibility gate that remains.

---

## 1. Authority and inherited constraints

This design is subordinate to:

- `05_DECISIONS.md` v1.1;
- `06_DEBLOCK_CONCEPT.md` v1.1;
- `02_INDEX_FORMAT_SPEC.md` v0.4 constraints;
- `Stage1_Evidence_and_Gate_Report_v0_3.md`.

The project proposal remains historical/workflow context only where later authority has not
superseded it.

### 1.1 Frame-owned processing

**DECIDED (D-09).**

The processing object is the decoded VapourSynth frame.

Do not split an interlaced frame into two independently deblocked field images.

Use field-parity-aware sample access where filtering across a seam would otherwise mix temporally
different fields.

### 1.2 Indexed geometry is authoritative

**DECIDED (D-24).**

For the supported luma frame-picture path, seam geometry / eligibility comes from MPEG-2 coding
structure and the index.

Pixels do not decide whether a macroblock is FRAME or FIELD.

Pixels remain essential for:

- blocking-versus-real-edge classification;
- local activity / flatness assessment;
- correction limiting;
- no-harm protection.

The production model is therefore:

```text
index metadata
    -> seam geometry / eligibility

decoded pixels
    -> block-like versus real-detail judgement
    -> local activity / edge protection

indexed QP + global strength
    -> threshold / correction scale
```

### 1.3 Transform-state semantics

The index states:

```text
FRAME
FIELD
NONE
```

`NONE` means:

> no current coded residual transform geometry is asserted for that macroblock.

It does **not** mean:

> no visible blocking can exist there.

Prediction may propagate prior blocking into skipped or no-residual areas.

### 1.4 Luma geometry in frame pictures

For a 16-line luma macroblock in a frame picture:

```text
FRAME:
    fixed macroblock-edge seams
    +
    internal horizontal transform seam between frame lines 7 | 8

FIELD:
    fixed macroblock-edge seams
    no FRAME-style mid-height horizontal seam

NONE:
    no current residual transform seam asserted internally
```

For interlaced frame material, D-09 requires field-parity-aware access where ordinary adjacent-line
filtering would mix fields.

For the FRAME internal horizontal seam this gives, relative to the 16-line macroblock:

```text
top-field pair around the seam:       6 | 8
bottom-field pair around the seam:    7 | 9
```

Vertical transform-grid seam positions do not depend on FRAME versus FIELD state.

### 1.5 4:2:0 chroma

**DECIDED in scope (D-25); mechanics accepted as K-04, K-10 and K-11.**

For the inspected MPEG-2 4:2:0 frame-picture path:

- one 8x8 Cb block and one 8x8 Cr block correspond to each 16x16 luma macroblock;
- chroma transform placement does not follow luma `dct_type`;
- chroma uses the macroblock's same effective `quantizer_scale`;
- the inspected reference decoder selects the luma quantisation-matrix path for 4:2:0;
- in field prediction, chroma-line parity alternates top/bottom by line.

The first chroma experiment therefore uses:

```text
native Cb / Cr planes
+
fixed 8x8 chroma transform grid
+
indexed effective per-MB QP
```

Do not import luma FRAME/FIELD/NONE transform geometry into chroma placement.

Whether interlaced horizontal chroma filtering should use same-field-polarity access remains a
Stage 2 design question (O-06/O-14), with V4 providing a verified parity premise.

### 1.6 Support constraint

For the initial short-support candidate:

> **Support for one known transform seam must not cross another known transform seam.**

This is a filter-design constraint, not an MPEG-2 normative rule.

### 1.7 Initial metadata scope

The first Stage 2 filtering work uses:

- authoritative luma FRAME/FIELD/NONE state;
- effective per-macroblock QP;
- per-picture `progressive_frame`;
- picture type for I/P/B reporting and leading-B quality exclusion;
- frame/dimension correspondence needed for index validation.

Do not initially consume:

- coded-block pattern as a filtering input;
- coefficient activity;
- prediction mode as a filtering input;
- motion vectors;
- quantisation-matrix coefficient values.

Availability in the Stage 1 temporary index does not imply production retention.

---

## 2. Stage 2 questions

### Q2-01 - Does the candidate index-directed filtering family help?

Can a short-support, edge-preserving filter reduce visible MPEG-2 blocking on real LG material
without unacceptable detail damage?

### Q2-02 - Does the real per-MB QP map help?

With indexed geometry, pixels, kernel and parameters held constant, does replacing one fixed
clip-wide representative QP with the real effective per-macroblock QP improve behaviour?

### Q2-03 - What kernel / thresholds / strength are useful?

Once the fixed-versus-real QP comparison is interpretable, what bounded correction and gating
behaviour works best on the development material?

### Q2-04 - How should `NONE` be treated?

What conservative index-consistent policy best handles visible blocking in macroblocks with no
current coded residual transform geometry?

### Q2-05 - What is the practical limit from I/P/B prediction?

Does useful benefit differ materially among I, P and B pictures, consistent with the known
off-grid / propagated-blocking limitation?

### Q2-06 - How should chroma be filtered safely?

For native MPEG-2 4:2:0 chroma:

- what thresholds and strength are useful?
- does real per-MB QP improve behaviour?
- what horizontal/vertical treatment is appropriate?
- what interlaced sample-access rule is safe?
- can colour smearing and field mixing be avoided?

### Q2-07 - Which indexed metadata survive into the final production design?

Stage 2 does not freeze the final `.idx2`.

It should identify which currently available metadata the eventual production filter actually
consumes.

---

## 3. Experimental material and evidence hierarchy

### 3.1 Primary product evidence

**DECIDED (D-26).**

Real LG recorder material is primary.

Use:

```text
DEVELOPMENT / TUNING
    LG_576i_3_LP

LOCKED INTERLACED HOLD-OUTS
    LG_576i_4_EP
    TEST_4A_A003 original
    TEST_2A_A001 original

SEPARATE PROGRESSIVE / CONTROL MATERIAL
    LG_576i_5_MLS
```

The real-recorder decision is based primarily on:

- Dave's visual assessment;
- seam-local diagnostics;
- collateral-change / no-harm diagnostics;
- consistency across materially different recorder modes.

### 3.2 Why LP is the development clip

Known Stage 1 properties include:

```text
720x576
204 frames
45x36 MBs
interlaced / top-field-first
FRAME 22.97%
FIELD 52.74%
NONE  24.29%
mixed FRAME/FIELD frames 97.06%
QP median 18
QP mean   21.285
QP max    112
```

This gives one real LG sample with:

- full spatial resolution;
- materially stronger real quantisation;
- substantial FRAME and FIELD populations;
- substantial NONE population;
- I/P/B coverage.

It is therefore a good first development source for both authoritative luma geometry paths.

### 3.3 Locked hold-outs

After a candidate parameter set is fixed on LP, evaluate unchanged on:

```text
LG_576i_4_EP
TEST_4A_A003 original
TEST_2A_A001 original
```

Do not retune on a hold-out and continue calling it hold-out validation.

If a hold-out exposes a real design flaw:

1. report the failure;
2. reopen development explicitly;
3. label the next parameter search as a new tuning round;
4. do not treat already viewed hold-outs as pristine independent validation thereafter.

The fact that metadata distributions for these clips are already known does not invalidate them as
filter hold-outs; no filtered-output tuning has yet been performed on them.

### 3.4 MLS role

`LG_576i_5_MLS` is progressive 352x288 material:

```text
progressive_frame = 1 throughout
FIELD = 0
FRAME = 85.44%
NONE  = 14.56%
QP median = 10
```

It is not a FRAME-versus-FIELD exercise source.

Use it for:

- progressive frame-domain access;
- general low-resolution no-harm behaviour;
- progressive chroma behaviour;
- a check that the filter does not depend accidentally on interlaced special cases.

### 3.5 Secondary paired-reference material

Retain:

```text
TEST_4A_A003_blocky
TEST_2A_A001_blocky
```

with the corresponding higher-quality originals as secondary practical references.

They are deliberately degraded re-encodes and are **not** pristine ground truth.

Paired-reference numerical metrics mean only:

> movement toward or away from the decoded higher-quality source.

They do not dominate the product decision.

### 3.6 No existing-filter yardstick

Per Dave's explicit 2026-10-08 ruling:

> No existing external deblocker is part of the planned Stage 2 comparison.

Revisit only if later evidence creates a specific need.

---

## 4. Excluded leading B pictures

Some extracted real LG clips begin with B pictures whose normal prediction context extends before
the clip.

For quality evidence, use the observable index rule:

> **Exclude B pictures output before the first I picture of the clip.**

Exclude those pictures from:

- parameter tuning;
- quality metric aggregates;
- visual A/B selections;
- feasibility conclusions.

Still process and validate them for:

- record/frame correspondence;
- parser / index robustness;
- bounds safety;
- diagnostic completeness.

Record the number of excluded leading B pictures for each clip.

---

## 5. Prototype architecture

Stage 2 is a research prototype, not the production VapourSynth plugin.

### 5.1 Language and execution model

Preferred first implementation:

- Python 3;
- VapourSynth / BestSource for decoded frames;
- NumPy for scalar/reference operations where convenient;
- Stage 1 temporary-index reader;
- deterministic per-frame processing;
- serial runs acceptable.

No C++, API4 production plugin or AVX2 optimisation belongs in Stage 2.

### 5.2 Inputs

For each clip:

```text
BestSource decoded frame
+
matching Stage 1 index record
```

Reject:

- wrong magic/version;
- incomplete index;
- dimension mismatch;
- frame-count mismatch;
- record ordinal mismatch;
- unsupported field-picture structure for this experiment.

Do not weaken Stage 1 validity checks because Stage 2 is experimental.

### 5.3 Outputs

The prototype should be able to produce:

- filtered lossless comparison output;
- difference frames / maps;
- seam / eligibility maps;
- per-seam diagnostic records;
- CSV or other machine-readable metrics;
- per-frame summaries;
- I/P/B aggregate summaries;
- QP-band aggregate summaries.

### 5.4 Reproducibility

Every run must record:

- input filename;
- index filename;
- frame range;
- variant ID;
- parameter set;
- fixed-QP rule/value where applicable;
- global strength;
- code/script version;
- excluded leading-B count;
- aggregate results.

No result should depend on an unrecorded interactive setting.

---

## 6. Mandatory pre-filter validation

### 6.1 Temporal / structural validation

Stage 1 already established the intended output-record correspondence model.

Stage 2 repeats cheap checks:

```text
index records == BestSource frames
dimensions match
record ordinals match
picture structure supported
```

### 6.2 Spatial index-to-pixel registration

**MUST complete before filtering-quality conclusions.**

Stage 1 proved temporal correspondence but did not independently prove that macroblock `(x,y)` in
the index is spatially registered to decoded pixels at the intended 16x16 luma location.

On LP, produce a detector-free registration diagnostic.

At indexed mid-height positions:

- measure the same-field-polarity luma step separately for indexed FRAME and FIELD macroblocks;
- also report the fixed macroblock-edge step for both populations.

Expected working hypothesis:

```text
FRAME mid-height step distribution / mean
    should be stronger than FIELD at that same candidate position

fixed macroblock-edge behaviour
    should not show the same FRAME/FIELD disappearance pattern
```

This is a **registration validation**, not a production seam detector.

If the result is weak, inverted or otherwise inconsistent:

- stop before quality conclusions;
- inspect seam maps / coordinates;
- check for crop, row offset, parity swap or other registration error.

Do not automatically reinterpret pixels to override indexed geometry.

---

## 7. Initial luma boundary abstraction

A boundary operation receives conceptually:

```text
samples on side P
samples on side Q
boundary orientation
sample stride / parity-aware stride
boundary class
effective QP or fixed clip QP
global strength
pixel activity / edge state
```

For a vertical boundary:

```text
... p2 p1 p0 | q0 q1 q2 ...
```

uses neighbouring horizontal samples.

For horizontal boundaries in interlaced material, use parity-aware row access where ordinary
adjacent-line access would mix fields.

The implementation must make the access rule explicit.

---

## 8. Initial candidate luma kernel

The production kernel is not yet decided.

Stage 2 begins with a deliberately parameterised, short-support candidate.

### 8.1 Required properties

The candidate must:

- operate only at index-eligible / fixed coding-grid seams;
- reject strong genuine edges;
- use short support;
- clamp correction magnitude;
- allow thresholds / limits to scale monotonically with QP and strength;
- avoid crossing another known transform seam;
- be suitable for later integer scalar and AVX2 implementation.

### 8.2 Candidate pixel tests

The first candidate may combine:

1. boundary step magnitude;
2. same-side local activity;
3. bounded local range / flatness;
4. QP-scaled thresholds.

Conceptual quantities:

```text
D  = abs(q0 - p0)
LP = local activity on P side
LQ = local activity on Q side
R  = local max - local min
Q  = selected boundary quantiser
S  = global experimental strength
```

The candidate should prefer corrections where the boundary step looks block-like relative to local
same-side activity and reject obviously strong natural edges.

No MPEG-4/H.264 threshold table is adopted blindly.

### 8.3 Candidate correction

Start with a bounded local correction primarily modifying `p0` and `q0`, optionally with smaller
`p1` / `q1` participation in sufficiently flat regions.

Requirements:

- clipping to valid sample range;
- bounded correction magnitude;
- near-zero-sum local correction where practical;
- no support across another known transform seam.

### 8.4 Initial-kernel freeze for the QP ablation

Steps 2 and 3 of the experiment require one initial candidate kernel and parameter set.

Development sequence:

1. use LP with fixed clip-wide QP;
2. select a bounded initial candidate parameter set;
3. freeze it as **K0**;
4. compare fixed QP versus real per-MB QP using exactly K0.

Do not retune K0 separately for the real-QP variant.

After that clean comparison is complete, further kernel / threshold / strength development may
continue using real QP.

---

## 9. QP handling

### 9.1 Fixed-QP control

For the fixed-versus-real QP comparison:

```text
Q_fixed(clip) = median effective per-MB QP for that clip
```

Use that one scalar for every macroblock in that clip.

Known examples:

```text
LP  -> 18
EP  -> 14
MLS -> 10
```

Apply the same median rule to other clips.

This control preserves an approximate clip-level compression severity while removing spatial QP
variation.

### 9.2 Real-QP variant

Use the effective per-macroblock QP from the validated Stage 1 index.

### 9.3 Shared macroblock boundaries

For a boundary shared by two macroblocks, the first implementation hypothesis is:

```text
Q_boundary = rounded mean(Q_left, Q_right)
```

An internal seam uses the containing macroblock's QP.

This is a Stage 2 hypothesis, not repository knowledge.

If results show sensitivity to this choice, compare a small bounded set such as min / mean / max
rather than silently changing the rule.

### 9.4 QP saturation reporting

LP and EP contain macroblocks at effective QP 112.

Report QP-112 behaviour separately where practical so saturation does not disappear inside whole-
clip averages.

---

## 10. Revised Stage 2 experiment ladder

### Step 1 - unfiltered baseline

No filtering.

Purpose:

- mandatory visual baseline;
- diagnostic baseline;
- paired-reference baseline where a practical reference exists.

### Step 2 - indexed geometry + fixed clip-wide QP

Use:

- authoritative indexed luma geometry;
- fixed clip-wide median QP;
- initial candidate kernel K0;
- pixel edge/activity protection.

Purpose:

- establish K0 under the actual index-driven architecture;
- provide the control for spatial real-QP value.

### Step 3 - indexed geometry + real per-MB QP

Hold constant:

- authoritative geometry;
- K0;
- pixel tests;
- strength;
- all other parameters.

Change only:

```text
fixed clip-wide median QP
    ->
real indexed per-MB effective QP
```

Primary comparison:

```text
Step 2 vs Step 3
    =
value of the real spatial QP map inside the production architecture
```

### Step 4 - luma kernel / threshold / strength development

Using indexed geometry and real QP:

- refine edge/activity rejection;
- refine correction magnitude;
- refine flat/detail behaviour;
- define a small strength sweep;
- require OFF to be bit-exact;
- preserve the no-cross-seam support rule.

Development remains on LP.

Do not expose locked hold-outs during parameter tuning.

### Step 5 - `NONE` policy

Start with:

**N0 - conservative**

```text
do not invent an internal transform seam in NONE
```

Macroblock-edge locations remain fixed coding-grid locations and may still be tested by the
pixel-domain blocking/detail logic.

Only if N0 leaves a demonstrated problem should a bounded alternative be designed.

Any alternative must remain index-consistent and must not recreate a general FRAME/FIELD pixel
detector by another name.

### Step 6 - bounded chroma experiment

Use native Cb/Cr planes and fixed 8x8 chroma geometry.

Initial QP comparison:

```text
C0  unfiltered chroma
C1  chroma candidate + fixed clip-wide median QP
C2  same candidate + real indexed per-MB QP
```

For interlaced material, explicitly investigate the horizontal sample-access rule required by
O-06/O-14.

Leading candidate:

```text
same-field-polarity horizontal access
```

because V4 verifies the chroma parity premise and D-09 requires avoiding field mixing where
applicable.

However, same-field chroma filtering remains an experimental design choice until Stage 2 evidence
is reviewed.

For progressive MLS:

```text
progressive_frame = 1
    -> normal frame-domain access
```

Do not use luma FRAME/FIELD/NONE state to place chroma seams.

### Step 7 - locked generalisation / no-harm

After luma/chroma parameters are fixed on development material:

Run unchanged on:

```text
LG_576i_4_EP
TEST_4A_A003 original
TEST_2A_A001 original
```

Use MLS as the separate progressive/control case.

Then report the software-transcode pairs as secondary paired-reference evidence.

No retuning on hold-outs is allowed without explicitly reopening development.

---

## 11. Progressive versus interlaced access

Take `progressive_frame` per picture from the index.

### `progressive_frame = 1`

Use ordinary frame-domain sample access.

### `progressive_frame = 0`

Use parity-aware sample access where filtering across the selected seam would otherwise mix fields.

Do not infer progressive/interlaced handling from:

- filename;
- vertical resolution;
- container metadata alone.

Field pictures remain outside the current Stage 2 filtering path.

---

## 12. Strength handling

The intended eventual user interface exposes one global strength.

Stage 2 uses a small declared sweep such as:

```text
OFF
LOW
NOMINAL
HIGH
```

or equivalent numeric values.

Requirements:

- OFF is bit-exact input;
- stronger settings must monotonically permit more correction / looser thresholds;
- compared variants use the same strength definition;
- do not independently retune strength merely to make one variant win.

The exact production scale remains open.

---

## 13. Measurements and evidence

No single metric decides the project.

### 13.1 Real-LG seam diagnostics

At known eligible seams, report before/after quantities such as:

```text
boundary step magnitude
same-side local activity
step / activity relationship
applied correction magnitude
percentage of eligible seams changed
```

Break down where useful by:

```text
seam class
FRAME / FIELD / NONE
I / P / B
QP band
strength
```

These are diagnostics, not absolute perceptual-quality scores.

### 13.2 No-harm / collateral-change measures

Report:

```text
mean absolute output-input change
percentage of changed pixels
change energy away from eligible seam neighbourhoods
changes around strong natural edges
```

A filter that improves seam statistics by broadly blurring non-seam content should fail.

### 13.3 Paired-reference metrics

For the software-transcode pairs only:

- luma MAE;
- luma MSE;
- luma PSNR;
- seam-local reference error;
- non-seam reference error.

Interpretation:

> movement toward or away from the decoded higher-quality source.

Not:

> absolute restoration truth.

### 13.4 I/P/B reporting

Report practical results separately for:

- I pictures;
- P pictures;
- B pictures;
- all included pictures.

This tests the practical limit from prediction-propagated / off-grid blocking.

### 13.5 QP-band reporting

Use declared QP bands sufficient to reveal whether behaviour changes materially with quantisation.

At minimum identify the QP-112 saturation population separately where present.

### 13.6 Visual evidence

Produce matched crops or lossless clips for Dave.

Include:

- flat/blocky regions;
- strong genuine edges;
- texture/detail;
- FRAME-heavy regions;
- FIELD-heavy regions;
- NONE-heavy regions;
- I/P/B examples;
- representative low/mid/high QP regions;
- chroma-rich areas for chroma testing.

Blind or shuffled A/B presentation is preferred where practical.

---

## 14. Frame / region selection

Do not rely only on favourable hand-picked examples.

### 14.1 Full included-frame reporting

Run aggregate diagnostics across all quality-eligible frames after applying the leading-B exclusion.

### 14.2 Deterministic diagnostic subset

Before viewing filtered results where practical, select a reproducible subset based on metadata,
for example:

- highest mean-QP frames;
- lower-QP comparison frames;
- highest FRAME proportion;
- highest FIELD proportion;
- highest NONE proportion;
- representative I/P/B frames.

### 14.3 Manual additions

Dave may add visually troublesome frames.

Label them as manually selected rather than statistical samples.

---

## 15. Cross-pair temporal correspondence for secondary reference metrics

Stage 1 proves index-record correspondence inside each file.

Before using an original/blocky pair for paired-reference metrics, also verify that decoded frame
`N` in one corresponds to decoded frame `N` in the other.

For each frame, compare against a small temporal window, e.g.:

```text
N-2 .. N+2
```

using luma MAE or MSE.

Expected:

```text
best match at N
```

for all or effectively all non-ambiguous frames.

Very static ties may be reported rather than treated as failures.

This check applies only to the software-transcode pairs.

---

## 16. Quantisation matrices

Current evidence shows custom non-intra matrices in four of the five real LG recordings examined.

The first Stage 2 filter does **not** consume matrix coefficients.

Record matrix-presence provenance with results.

Reopen Stage 1 for matrix values only if there is a concrete unresolved pattern such as:

```text
QP-normalised threshold behaviour differs consistently
between custom-matrix and no-custom-matrix LG material
```

and simpler explanations have been excluded.

Do not unfreeze Stage 1 pre-emptively.

---

## 17. FFmpeg / BestSource QP side data

FFmpeg per-macroblock QP side data remains an optional implementation cross-check, not an
architecture decision.

Core Stage 2 filtering uses the validated Stage 1 index.

If the BestSource/VapourSynth path later exposes FFmpeg QP side data cleanly, it may be compared
against Stage 1 QP as a cross-check.

This must not block Stage 2.

---

## 18. Feasibility gate

Stage 2 ends with an explicit gate report.

### 18.1 Primary evidence

Primary product evidence is:

```text
real LG visual quality
+
real LG seam-local behaviour
+
real LG no-harm / collateral-change behaviour
+
consistency across locked hold-outs
```

### 18.2 Secondary evidence

Secondary evidence is:

```text
paired-reference movement on the software-transcode pairs
+
supporting I/P/B and QP-band diagnostics
```

### 18.3 Pass / fail interpretation

Do not invent one arbitrary PSNR or seam-step threshold in advance.

A positive result requires:

- visible blocking reduction on target material;
- corrections localised appropriately;
- acceptable preservation of real edges and texture;
- acceptable chroma behaviour;
- no unacceptable field mixing or colour smearing;
- reasonable consistency across hold-outs.

The project may fail the gate even if some numerical seam measures improve.

### 18.4 Final metadata-retention output

The gate report should explicitly list:

```text
metadata definitely consumed by the successful filter
metadata used only for diagnostics
metadata shown unnecessary
metadata still unresolved
```

That evidence feeds Stage 3 and the final index specification.

---

## 19. Implementation increments

No code begins until this v0.2 design is reviewed by Claude and ratified by Dave.

Proposed incremental implementation:

```text
S2-I1
    read-only Stage 1 index reader / validation
    progressive_frame and picture-type handling
    leading-B quality exclusion accounting

S2-I2
    seam-map diagnostics
    mandatory spatial index-to-pixel registration check

S2-I3
    initial luma candidate kernel on LP with fixed median QP
    choose and freeze K0

S2-I4
    K0 fixed-QP versus real-QP comparison
    no retuning between variants

S2-I5
    real-QP luma kernel / threshold / strength development on LP

S2-I6
    NONE N0 policy and only evidence-driven alternatives

S2-I7
    bounded native 4:2:0 chroma experiment
    progressive/interlaced access investigation

S2-I8
    locked hold-out generalisation / no-harm
    EP + 4A original + 2A original
    MLS progressive/control

S2-I9
    secondary software-transcode paired-reference reporting

S2-I10
    Stage 2 feasibility / metadata-retention gate report
```

Review each bounded increment before advancing where a result could change the next design step.

---

## 20. Explicit non-goals

Stage 2 does not:

- freeze final `.idx2` packing;
- optimise index size;
- build the final production indexer;
- build the production C++ VapourSynth API4 plugin;
- implement AVX2;
- solve field-picture filtering;
- solve damaged-stream production support;
- add motion vectors;
- add CBP or coefficient activity unless evidence later demands them;
- capture quantisation-matrix coefficient values without evidence;
- build a pixel seam-position detector;
- build Family B;
- run an existing-filter yardstick as part of the planned experiment;
- reopen the production architecture question decided by D-24.

Family C remains optional later research under D-12, but is not part of the core v0.2 experiment and
must not delay the feasibility gate.

---

## 21. Questions for Claude review

Please identify **blocking issues separately from optional refinements**.

1. **Authority fidelity:** Does v0.2 correctly implement ratified D-24, D-25 and D-26 without
   reopening the discarded architecture experiment?
2. **Registration check:** Is section 6.2 sufficient to validate spatial index-to-pixel alignment
   without becoming a pixel seam detector?
3. **Kernel freeze:** Is the K0 sequence a clean way to isolate fixed versus real per-MB QP before
   later kernel development?
4. **Fixed QP:** Is per-clip median effective QP still the preferred control?
5. **Shared-boundary QP:** Is rounded mean a reasonable first Stage 2 hypothesis, or should another
   initial rule be preferred before coding?
6. **NONE:** Is N0 sufficiently conservative and index-consistent for the first pass?
7. **Chroma:** Does the bounded chroma experiment preserve the V2/V3/V4 evidence distinctions,
   especially keeping same-field chroma filtering as an experimental design choice?
8. **Progressive access:** Is the `progressive_frame`-driven split stated correctly?
9. **Evidence hierarchy:** Are the real-LG and secondary paired-reference roles sufficiently clear?
10. **Hold-out discipline:** Is LP development with EP/4A/2A locked hold-out appropriate?
11. **Leading B pictures:** Is the observable exclusion rule correct and sufficient?
12. **Implementation order:** Would you change S2-I1 through S2-I10 before any coding begins?
13. **Scope:** Does anything in this draft accidentally require Stage 1 to be unfrozen without
    evidence?

---

## 22. Proposed disposition after review

If Claude approves or requests only bounded corrections:

1. ChatGPT revises this document;
2. Dave ratifies `Stage2_Experiment_Design_v0_2.md`;
3. implement **S2-I1 only**;
4. review S2-I1 output before S2-I2;
5. continue incrementally;
6. produce the Stage 2 feasibility / metadata-retention gate report before Stage 3.

---

## 23. Change log

### v0.2 - 2026-10-08

- Supersedes the experimental premise of v0.1 after ratified D-24.
- Removes Family B, pixel seam-position detection, Step 2b, transform-state-value architecture
  comparisons and custom-index justification testing.
- Incorporates D-25: chroma deblocking is in scope on mechanism; Stage 2 tests how to do it safely,
  not whether chroma is eligible for scope.
- Incorporates D-26: real LG recorder material is primary evidence; software-transcode pairs are
  secondary paired-reference evidence.
- Uses LP for development; EP, 4A original and 2A original as locked interlaced hold-outs; MLS as
  progressive/control material.
- Uses per-clip median effective QP as the fixed-QP control.
- Adds mandatory detector-free spatial index-to-pixel registration validation.
- Adds leading-B quality-evidence exclusion before the first I picture.
- Uses `progressive_frame` per picture to select progressive frame-domain versus interlaced
  parity-aware access.
- Carries Claude V1-V4 evidence distinctions into luma/chroma geometry and access design.
- Keeps same-field chroma filtering experimental rather than promoting it to VERIFIED.
- Defers quantisation-matrix coefficient capture unless Stage 2 evidence requires it.
- Explicitly excludes an existing-filter yardstick from the planned experiment.
- Defines S2-I1 through S2-I10 incremental implementation order.
- No Stage 2 code is authorised by this draft.

### v0.1 - 2026-10-07

- Original pre-D-24 Stage 2 draft.
- Retained here only as superseded design history after v0.2 is ratified.

