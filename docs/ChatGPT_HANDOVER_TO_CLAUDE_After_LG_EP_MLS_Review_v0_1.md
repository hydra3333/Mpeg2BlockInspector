# ChatGPT Handover to Claude After `Claude_REVIEW_OF_LG_EP_MLS_Stage1_Runs_v0_1.md`

**Filename:** `ChatGPT_HANDOVER_TO_CLAUDE_After_LG_EP_MLS_Review_v0_1.md`  
**Version:** 0.1  
**Date:** 2026-10-07  
**From:** ChatGPT, for Dave to provide to the correct Claude project chat  
**Status:** CATCH-UP / PROVENANCE / REVIEW INPUT ONLY. Not repository authority.  
**Handover boundary:** immediately after Claude produced `Claude_REVIEW_OF_LG_EP_MLS_Stage1_Runs_v0_1.md` and Dave supplied it to ChatGPT.

---

## 0. Important provenance note

The exact file `Claude_REVIEW_OF_LG_EP_MLS_Stage1_Runs_v0_1.md` is not currently available to
ChatGPT in retrievable file context.

Therefore this document does **not** attempt to reconstruct or paraphrase that file as though it
were present.

Claude should treat his own `Claude_REVIEW_OF_LG_EP_MLS_Stage1_Runs_v0_1.md` as the starting
review input and use this handover only for what happened **after that point**.

Where this handover needs earlier context to explain a later decision, it relies on named files
that are available and is explicit about their status.

No repository file, Stage 1 source file, analyzer, or Stage 2 implementation was changed during the
events described below.

---

## 1. State at the handover boundary

At the point immediately after Claude's EP/MLS Stage 1 review:

- Stage 1 had passed and `Stage1_Evidence_and_Gate_Report_v0_3.md` had been ratified by Dave.
- The Stage 1 inspector/analyzer were considered frozen unless new evidence exposed a defect.
- `Stage2_Experiment_Design_v0_1.md` existed as a **draft only**:
  - drafted by ChatGPT;
  - intended for Claude review and Dave ratification;
  - no Stage 2 code authorised.
- The existing repository authority remained:
  - `05_DECISIONS.md`
  - `06_DEBLOCK_CONCEPT.md`
  - `02_INDEX_FORMAT_SPEC.md`
- Claude had already produced the separate chroma/index review:
  - `Claude_REVIEW_OF_ChatGPT_Discussion_Brief_Index_Value_and_Chroma_Deblocking_v0_2.md`
- That review contained Claude's reference-decoder cold reads V1/V2/V3 and recorded Dave's ruling
  R-A that chroma is in scope on mechanism.
- EP and MLS had been run through the Stage 1 toolchain and had passed their structural /
  frame-correspondence gates.
- The software `_blocky` transcodes had already become less attractive as the main real-world
  evidence because their transform-state distributions differed materially from the LG recorder
  originals.

The later events below materially alter the intended Stage 2 experiment, but they do **not**
invalidate the Stage 1 evidence.

---

## 2. New evidence after the handover boundary: LG LP recording

Dave next ran another real LG recorder sample through the same frozen Stage 1 toolchain:

```text
LG_576i_3_LP.mpg
```

Evidence source:

```text
LG_576i_3_LP.log
```

### 2.1 Structural / correspondence result

The LP sample passed cleanly:

```text
Inspector exit code       = 0
Analyzer                  = VALID
Sequences                 = 1
Index records             = 204
BestSource frames         = 204
Picture-type comparison   = MATCH 204/204
Full vspipe output        = 204 frames
Format                    = YUV420P8
```

Dimensions / picture structure:

```text
720x576
MB grid                   = 45x36
25 fps
picture_structure         = FRAME for 204/204
progressive_frame         = 0 for 204/204
top_field_first           = 1 for 204/204
repeat_first_field        = 0 for 204/204
q_scale_type              = 1 for 204/204
```

So LP is full-resolution 576-line interlaced LG material and is fully supported by the current
Stage 1 path.

### 2.2 Transform-state distribution

LP reports:

```text
FIELD = 174,291 = 52.74%
FRAME =  75,903 = 22.97%
NONE  =  80,286 = 24.29%

mixed FRAME/FIELD frames = 198/204 = 97.06%
```

This is an unusually useful real-recorder mixture because both authoritative luma transform paths
occur in substantial numbers.

Picture-type breakdown:

```text
I:
    FIELD = 56.54%
    FRAME = 43.46%

P:
    FIELD = 56.22%
    FRAME = 30.97%
    NONE  = 12.81%

B:
    FIELD = 50.96%
    FRAME = 17.41%
    NONE  = 31.64%
```

Thus both FRAME and FIELD geometry occur meaningfully across I/P/B pictures.

### 2.3 Quantiser regime

LP reports:

```text
QP min    = 1
QP max    = 112
QP mean   = 21.285
QP median = 18
```

This is materially harsher than EP's median 14 / mean 17.760 while retaining genuine LG
FRAME/FIELD mixture.

LP also has:

```text
custom intra matrix       = no
custom non-intra matrix   = yes, all 204 frames
chroma matrix differences = none reported
```

### 2.4 Initial ChatGPT interpretation

ChatGPT initially called LP arguably the strongest first real-recorder luma Stage 2 sample because
it combined:

- real LG encoder output;
- 720x576;
- materially heavier quantisation;
- substantial FRAME;
- substantial FIELD;
- 97.06% mixed frames.

At that moment the Stage 2 design still contained the pixel-only control / pixel-detected geometry
experiment, so part of the initial rationale was that LP would give a pixel detector many examples
of both sides of the FRAME/FIELD decision.

That particular rationale is now superseded by Dave's later architecture ruling described below.

The LP sample itself remains highly valuable.

---

## 3. The scope issue that was exposed

A separate, accidental discussion occurred in the wrong Claude chat.

That wrong-chat exchange is **not** technical authority and should not be used as project evidence.

Its only lasting value is that it exposed a mismatch between:

1. Dave's original understanding of the intended product; and
2. the broader falsification experiment that had grown into the Stage 0 / Stage 2 design.

Dave's recollection was:

> The deliverable is an MPEG-2-specific VapourSynth deblocker that consumes the index. Producing and
> using the index is central to the project. The production filter was never intended to operate
> index-free.

The wrong-chat Claude asserted that this meant a pixel-only detector should not exist at all.

ChatGPT then audited the actual project documents rather than accepting that assertion.

---

## 4. What the document audit showed

The audit established an important historical distinction.

### 4.1 Original production architecture

The original project proposal was indeed index-driven.

Conceptually:

```text
Mpeg2BlockInspector
    MPEG-2 elementary stream
        ->
    .idx2

MPEG2Deblock
    VapourSynth clip
    + matching .idx2
    + strength
        ->
    filtered clip
```

The original project idea was specifically that codec structure would be obtained authoritatively
while parsing MPEG-2 rather than reconstructed from pixels.

### 4.2 Later Stage 0 expansion

During Stage 0 research, the experiment was deliberately broadened.

The repository/design trail added:

- Family B as a mandatory strong pixel-only falsification/control;
- pixel-detected geometry;
- a metadata-blind/fixed-QP Family A step;
- a real-QP/pixel-geometry step;
- an authoritative-geometry step;
- a requirement to compare the metadata-assisted design against the pixel-only control;
- a provisional position that the custom index should justify its production role experimentally.

`Stage2_Experiment_Design_v0_1.md` reflects that expanded experiment.

Its core ladder is:

```text
1    unfiltered
2    Family B strong pixel-only control
2b   Family A fixed/emulated QP + pixel-detected geometry
3    Family A real QP + pixel-detected geometry
4    Family A real QP + authoritative FRAME/FIELD/NONE geometry
5    optional fixed-QP + authoritative geometry
6    optional Family C
```

So the historically correct statement is:

> The production concept began index-driven, but pixel-only processing was later added deliberately
> as an **experimental control**.

It would be wrong to claim that pixel-only experimentation was never in scope.

---

## 5. Why the pixel-only control had been added

The pixel-only path existed for a defensible research reason.

It asked:

> Does authoritative MPEG-2 metadata improve post-deblocking enough to justify the additional index
> architecture, or could a sufficiently good pixel-only method achieve essentially the same result?

Under that broader research framing:

```text
Step 2b vs Step 3
    isolated the value of real per-MB QP within Family A

Step 3 vs Step 4
    isolated pixel-detected vs authoritative transform geometry within Family A

Step 2 vs Step 4
    compared complete metadata-assisted Family A against strong pixel-only Family B
```

The proposed detector/index confusion matrix was also intended to measure:

```text
FRAME:
    detector says seam / no seam

FIELD:
    detector says seam / no seam

NONE:
    detector says seam / no seam
```

That was a legitimate falsification experiment.

The new decision below is therefore a **scope/architecture decision**, not a discovery that the
earlier reasoning was invalid.

---

## 6. Dave's new explicit ruling: no pixel geometry detector / no Family B

After the audit, Dave asked directly whether the pixel-only control was actually necessary.

ChatGPT's answer was:

- it is useful only if the project intends to test whether the index architecture should exist;
- it is **not required** to build the index-driven product Dave originally intended;
- building a serious blind detector would consume significant Stage 2 effort deliberately throwing
  away exact transform-state information and trying to reconstruct it from decoded pixels.

Dave then made the explicit ruling:

> **The production MPEG-2 deblocker is index-driven by definition. It requires its matching index.
> Stage 2 will not implement or evaluate a pixel-only seam-position detector or a pixel-only
> Family B deblocker.**

Important qualification:

> This is a scope decision. It is **not** an experimental finding that pixel-only deblocking is
> inferior.

This ruling restores the original production premise and supersedes the later expansion that made
the index architecture contingent on beating a pixel-only alternative.

---

## 7. What "no pixel detector" does and does not mean

The ruling concerns **geometry inference**.

The index answers authoritatively, for the supported luma frame-picture path:

```text
FRAME:
    current coded residual geometry includes the mid-height horizontal seam

FIELD:
    that FRAME-style mid-height seam is absent

NONE:
    no current coded residual transform geometry is asserted
```

The regular MPEG-2 grid supplies the fixed vertical / macroblock-edge locations.

Therefore Stage 2 no longer needs to ask reconstructed pixels:

```text
"Is this macroblock FRAME or FIELD?"
"Does the codec's mid-height seam exist here?"
```

However pixels remain essential.

At every known eligible seam the filter must still determine:

```text
Does the local discontinuity actually look like objectionable blocking?
Is it a genuine picture edge/detail?
How much correction is safe?
How should local activity limit correction?
```

So the intended model becomes:

```text
SEAM GEOMETRY / ELIGIBILITY
    authoritative from MPEG-2/index

BLOCK-VERSUS-DETAIL CLASSIFICATION
    from decoded pixels at the known seam

CORRECTION LIMIT / STRENGTH
    from pixels + indexed QP + global user strength
```

This distinction is important and must survive the repository rewrite.

---

## 8. Consequence for the LP sample

LP remains an excellent candidate, but its rationale changes.

The correct current rationale is:

- genuine LG recorder output;
- full 720x576;
- QP median 18 / mean 21.285 / max 112;
- FIELD 52.74%;
- FRAME 22.97%;
- NONE 24.29%;
- 97.06% mixed FRAME/FIELD frames;
- therefore substantial exercise of both **authoritative index-directed** luma geometry paths under
  realistically heavier compression.

The obsolete rationale is:

> LP is useful because a pixel detector must guess both FRAME and FIELD frequently.

There will be no such detector.

### Current proposed sample roles

These roles are recommendations pending normal Claude/Dave review, not yet new repository authority.

**LP**

```text
preferred first luma development material
full 720x576
heavier real LG quantisation
substantial FRAME and FIELD
```

**EP**

```text
strong complementary interlaced sample
very FIELD-heavy
FIELD 76.22%
FRAME 9.69%
NONE 14.09%
mixed 99.54%
QP median 14 / mean 17.760 / max 112
```

**TEST_2A_A001 original**

```text
useful FRAME-dominant counter-regime
approximately FRAME 59% / FIELD 6%
```

**TEST_4A_A003 original**

```text
useful FIELD-dominant full-resolution real-recorder sample
approximately FIELD 69% / FRAME 19%
```

**MLS**

```text
352x288 progressive
FIELD 0%
useful as progressive/fixed-geometry control
useful for chroma and no-harm work
not a FRAME/FIELD exercise sample
```

**software `_blocky` transcodes**

```text
retain as optional severe-compression / paired-reference stress material
do not treat as primary evidence about real LG encoder transform-state behaviour
```

---

## 9. Chroma: provenance and current shared position

Before drafting new documents, Dave asked ChatGPT to re-establish exactly where the recent chroma
findings came from and what their evidence level was.

The relevant provenance document is:

```text
Claude_REVIEW_OF_ChatGPT_Discussion_Brief_Index_Value_and_Chroma_Deblocking_v0_2.md
```

Author: Claude.

Status in that file:

```text
Review input only. Not project authority.
```

Claude defined `VERIFIED` there as a cold read of the pristine reference decoder source.

### 9.1 Claude V1

**Luma placement by `dct_type`.**

From `Add_Block()` in `getpic.c`, Claude verified the reference decoder's frame-picture luma
placement:

```text
field DCT:
    blocks are arranged by field
    no FRAME-style internal horizontal seam

frame DCT:
    blocks begin at rows 0 and 8
    internal horizontal seam between frame lines 7 and 8
```

This is the source verification supporting K-03.

### 9.2 Claude V2

**MPEG-2 4:2:0 chroma ignores luma `dct_type` for transform placement.**

Claude's cold read of `Add_Block()`, `getpic.c` 467-482, found that the field-DCT placement branch is
taken only when:

```text
dct_type && chroma_format != CHROMA420
```

Therefore for 4:2:0 the chroma block takes the frame-organised placement path:

```text
8 consecutive chroma lines
row step 1
```

This verifies the reference-decoder implementation behind K-04.

### 9.3 Claude V3

**4:2:0 chroma uses the macroblock's same quantiser and the luma matrix path in the inspected
reference decoder.**

Claude's cold read identified:

```text
getblk.c 274-276 and 443-445:
    matrix selection uses the luma matrix when
    comp < 4 OR chroma_format == CHROMA420

getblk.c 411 and 563:
    luma and chroma blocks use the same quantizer_scale
```

Consequences for our current design:

- the effective per-MB QP already captured by Stage 1 applies to Cb/Cr for 4:2:0;
- no separate chroma QP semantics are needed;
- the inspected decoder's 4:2:0 path uses the luma quantisation-matrix selection rather than
  separate chroma matrices.

### 9.4 Evidence-level precision

The matrix statement should be recorded as:

> **VERIFIED for the inspected pristine reference decoder implementation.**

It should **not** silently be promoted to:

> "H.262 normatively requires this"

unless separately verified against the MPEG-2 standard.

The source cold read is sufficient for the current decoder/index design, but the evidence label
must remain exact.

### 9.5 Chroma sample-access qualification

Claude's proposed same-field access for horizontal chroma boundaries in interlaced material was
still a design inference / hypothesis in the available review trail.

It should **not** be promoted to V2/V3-level VERIFIED merely because V2 verifies 4:2:0 block
placement.

This remains a Stage 2 design item to review/verify.

---

## 10. Dave's separate chroma ruling remains in force

This is distinct from the newer index-driven/no-pixel-detector ruling.

Claude's chroma review recorded Dave's ruling R-A:

> **Chroma is in scope on mechanism.**

The verified mechanism is sufficient reason to include 4:2:0 chroma deblocking in the intended
product.

Stage 2 does **not** need a preliminary go/no-go experiment whose purpose is merely:

```text
"Does chroma blocking exist?"
"Should chroma be deblocked at all?"
```

What remains experimental is:

- threshold;
- strength;
- horizontal/vertical treatment;
- exact interlaced sample access where not yet verified;
- no colour smearing;
- no field mixing;
- visible / numerical benefit;
- appropriate relation, if any, between luma and chroma strength.

This ruling should eventually receive its **own decision entry**.

It should not be smuggled into the repository merely as a side-effect of the index-driven ruling.

---

## 11. Revised Stage 2 objective

The old Stage 2 v0.1 central question was approximately:

> Does MPEG-2 metadata materially improve deblocking enough to justify the index architecture,
> especially authoritative transform geometry?

That question no longer matches Dave's product ruling.

The proposed replacement objective is:

> **Given authoritative indexed MPEG-2 geometry and QP, what filtering rule produces useful luma
> and chroma deblocking without unacceptable damage, and which indexed metadata are actually needed
> by the final production filter?**

The feasibility gate remains real.

Dave has **not** pre-decided that the deblocker is good enough to ship.

Stage 2 may still conclude:

- the candidate filter does too little;
- useful correction causes unacceptable detail loss;
- off-grid prediction-propagated blocking limits benefit too much;
- chroma filtering causes unacceptable colour damage;
- another kernel family is required;
- or the project should stop.

What Stage 2 no longer has to decide is whether the index should be replaced by pixel inference.

---

## 12. Proposed revised Stage 2 experiment

This is a proposed replacement direction for v0.1, not yet repository authority.

### Step 1 - unfiltered baseline

Decoded MPEG-2 with no filtering.

Purpose:

- visual baseline;
- numerical baseline where meaningful paired-reference material exists.

### Step 2 - indexed geometry + fixed/emulated QP

Luma geometry is always authoritative from the index:

```text
FRAME / FIELD / NONE
```

Use a fixed/emulated QP in the first candidate kernel.

Purpose:

- develop and understand the filtering kernel / pixel edge-activity logic;
- provide a clean base for measuring the value of real QP.

There is no pixel seam-position detector.

### Step 3 - indexed geometry + real effective per-MB QP

Hold geometry, pixel classification logic, support and kernel constant.

Change only:

```text
fixed/emulated QP
    ->
real effective indexed per-MB QP
```

Primary comparison:

```text
Step 2 vs Step 3
    =
value of real QP inside the actual index-driven design
```

### Step 4 - kernel / threshold / strength development

With indexed geometry and real QP:

- tune short-support correction;
- tune local step/activity/edge rejection;
- establish useful global strength behaviour;
- require OFF to be bit-exact;
- keep support from crossing another known transform seam;
- report I/P/B behaviour where useful.

This is now the centre of the Stage 2 filtering work.

### Step 5 - NONE policy

`NONE` remains a genuine problem:

```text
NONE != no visible blocking
```

Prediction may carry old blocking into skipped/no-residual regions.

First policy:

```text
N0:
    do not invent an internal current transform seam in NONE
```

Any more permissive policy should remain index-consistent and must not recreate a general
FRAME/FIELD pixel detector by another name.

The exact follow-up policy should be designed/reviewed after N0 evidence.

### Step 6 - bounded chroma experiment

Use native Cb/Cr.

Geometry:

```text
fixed 8x8 4:2:0 chroma transform grid
```

Metadata:

```text
effective indexed per-MB QP
```

Do not copy luma FRAME/FIELD/NONE transform geometry into chroma placement.

Suggested bounded comparison:

```text
C0:
    unfiltered chroma

C1:
    same chroma filter + fixed/emulated QP

C2:
    same chroma filter + real indexed per-MB QP
```

Questions:

- what threshold is safe?
- what strength is useful?
- does real QP improve behaviour?
- is colour detail preserved?
- is field mixing avoided?
- is there useful benefit on real LG material?

### Step 7 - generalisation / no-harm

Use real recorder material as the primary product evidence.

Proposed main set:

```text
LG_576i_3_LP
LG_576i_4_EP
TEST_4A_A003 original
TEST_2A_A001 original
```

Progressive/control:

```text
LG_576i_5_MLS
```

Optional severe / paired-reference stress:

```text
TEST_4A_A003_blocky
TEST_2A_A001_blocky
```

---

## 13. `Stage2_Experiment_Design_v0_1.md` status

There is **no later Stage 2 design version** at present.

The latest actual Stage 2 design artifact is:

```text
Stage2_Experiment_Design_v0_1.md
```

It remains:

```text
DRAFT FOR CLAUDE REVIEW AND DAVE RATIFICATION
```

and no Stage 2 code has been authorised from it.

Because Dave's new ruling removes a central branch of its experiment, v0.1 should not be casually
patched.

The proposal is to supersede it with:

```text
Stage2_Experiment_Design_v0_2.md
```

but only **after** the repository authority has been brought into alignment and reviewed.

---

## 14. Repository changes now indicated

No repository files have yet been changed as a result of the new ruling.

The following are proposed changes for normal review/ratification.

### 14.1 `05_DECISIONS.md`

Two distinct Dave decisions need durable treatment.

#### Decision A - index-driven production architecture

Proposed substance:

> The MPEG-2 deblocker requires its matching index and consumes authoritative transform geometry
> from it. Stage 2 will not implement or evaluate a pixel-only seam-position detector or Family B
> pixel-only deblocker. Pixels remain used for blocking-vs-real-edge discrimination and correction
> limiting at known indexed seams.

This should supersede the current decisions that require:

- Family B as mandatory control;
- pixel-detected geometry;
- Step 2b as required architecture work;
- the custom index architecture to justify itself by beating a pixel-only geometry path.

From the existing review trail, **D-18** is known to be the decision that added Step 2b.

Claude should identify the exact other affected decision IDs from the current repository files
rather than rely on ChatGPT guessing from review-document labels.

#### Decision B - chroma is in scope

R-A should become a separate durable decision.

Proposed substance:

> MPEG-2 4:2:0 chroma deblocking is in production scope on the verified coding mechanism and
> supporting practice. Stage 2 does not need a preliminary experiment merely to prove chroma
> blocking exists; it must determine safe/effective strength, threshold and no-harm behaviour.

Do **not** conflate this with Decision A.

### 14.2 `06_DEBLOCK_CONCEPT.md`

Proposed changes:

- retain frame-owned processing;
- retain FRAME/FIELD/NONE semantics;
- retain authoritative luma seam geometry;
- remove Family B as a required Stage 2 family;
- remove pixel-detected transform geometry as a Stage 2 path;
- remove the detector-vs-index architecture comparison;
- state explicitly:
  - seam geometry from the index;
  - pixel-domain tests classify/limit correction at known seams;
- update the Stage 2 ladder to the indexed-only design;
- incorporate Claude V1/V2/V3 at their correct evidence levels;
- close any open question whose substance is only:
  - "should chroma be in scope?"
  - "does chroma first need to prove it has blocking?"
- **retain** open chroma questions about:
  - threshold;
  - strength;
  - orientation;
  - interlaced access;
  - no-harm.

Important numbering caution:

> Do not automatically delete "O-06" merely by number.

In parts of the review trail O-06 referred to **chroma strength/threshold relative to luma**, which
is still open.

Claude should inspect the current `06_DEBLOCK_CONCEPT.md` and update by meaning, not by guessed
number.

### 14.3 `02_INDEX_FORMAT_SPEC.md`

The new distinction should be:

```text
INDEX ARCHITECTURE:
    decided - production filter requires matching index

FINAL INDEX CONTENTS/PACKING:
    still not frozen
```

The final format should contain only what Stage 2 shows the production algorithm actually needs.

Current leading semantics include:

- frame/output correspondence;
- authoritative luma FRAME/FIELD/NONE state;
- sufficient quantiser information to obtain the effective MPEG-2 scale;
- required picture/frame structural information.

Do not add CBP, coefficient activity, motion vectors or diagnostic fields merely because the Stage
1 temporary index currently has them.

The FFmpeg per-MB QP side-data finding remains useful background / cross-check information.

It no longer represents a competing production architecture under Dave's new ruling.

### 14.4 Project Proposal v0.5

This file is subordinate to repository authority.

Updating it is optional unless it is still being used as an active roadmap.

If retained actively, a new proposal version should reflect:

- index-driven architecture now explicit;
- pixel-only Family B removed from the planned experiment;
- chroma in scope;
- real LG LP/EP evidence;
- feasibility gate focused on filtering quality/no-harm and required metadata rather than
  "keep index versus abandon index."

### 14.5 Stage 1 artifacts

No change indicated.

Keep frozen unless a real defect is found:

```text
Mpeg2BlockInspector Stage 1 implementation
Stage1_Inspector_Analyzer_v0_2.py
Stage1_Evidence_and_Gate_Report_v0_3.md
```

LP/EP/MLS evidence gives no reason to reopen the Stage 1 implementation.

---

## 15. What has NOT happened

To avoid accidental history drift:

- no `Stage2_Experiment_Design_v0_2.md` exists yet;
- no Stage 2 filtering code has been written;
- no repository authority file has yet been updated for the new index-driven ruling;
- no final `.idx2` layout has been frozen;
- no pixel detector has been implemented;
- no Family B implementation has been started;
- no Stage 1 source/analyzer change has been made because of LP;
- the wrong-Claude chat created no authoritative technical result.

---

## 16. Current knowledge/status classification

### Dave DECIDED / ruled

1. Production deblocker is index-driven and requires its matching index.
2. Stage 2 will not build/evaluate a pixel seam-position detector or Family B.
3. Chroma deblocking is in scope on mechanism (earlier R-A).
4. Chroma does not need a preliminary "prove blocking exists" gate.
5. Normal review/ratification remains required before Stage 2 coding.

### VERIFIED in Claude's pristine-reference-decoder cold read, pending repository promotion where
needed

1. V1: luma FRAME/FIELD placement behaviour in the inspected decoder.
2. V2: 4:2:0 chroma placement ignores luma `dct_type` in the inspected decoder.
3. V3:
   - 4:2:0 chroma blocks use the same macroblock `quantizer_scale`;
   - the inspected decoder's 4:2:0 path uses the luma quantisation-matrix selection.

### Strong empirical Stage 1 evidence

1. EP:
   - valid;
   - interlaced;
   - very FIELD-heavy;
   - mixed FRAME/FIELD in 99.54% of frames.
2. MLS:
   - valid;
   - 352x288 progressive;
   - no FIELD transform state;
   - useful control/chroma/no-harm material.
3. LP:
   - valid;
   - 720x576 interlaced;
   - FIELD 52.74%, FRAME 22.97%, NONE 24.29%;
   - mixed 97.06%;
   - QP median 18 / mean 21.285 / max 112;
   - especially attractive as first luma development material.

### PROPOSED, not yet ratified

1. LP as first luma development sample.
2. Revised indexed-only Stage 2 ladder in section 12.
3. Exact repository edits in section 14.
4. Fixed-QP versus real-QP luma ablation as the first clean metadata experiment.
5. C0/C1/C2 bounded chroma experiment.
6. Main real-recorder generalisation set LP + EP + 4A original + 2A original.

### OPEN

1. Exact luma kernel mathematics.
2. Threshold equations.
3. Strength mapping.
4. Boundary QP combination at shared MB edges.
5. Exact NONE policy beyond conservative N0.
6. Chroma threshold and strength.
7. Exact interlaced chroma sample access where not source-verified.
8. Chroma horizontal/vertical treatment.
9. No-harm criteria / colour smearing / field mixing.
10. Whether matrix information ever needs to influence filtering.
11. Whether CBP/coefficient activity are later useful.
12. Final `.idx2` packing and minimum production metadata set.
13. Deferred field-picture support.
14. Damaged-stream/final production robustness work.

---

## 17. Revised next step

Because this document is being supplied to the **correct** Claude project chat, the clean next step
is now:

```text
1. Claude reads:
   - his own `Claude_REVIEW_OF_LG_EP_MLS_Stage1_Runs_v0_1.md`
   - this handover
   - `Stage2_Experiment_Design_v0_1.md`
   - current repository `05_DECISIONS.md`
   - current repository `06_DEBLOCK_CONCEPT.md`
   - current repository `02_INDEX_FORMAT_SPEC.md`
   - his prior chroma/index v0.2 review as needed

2. Claude responds with a bounded reconciliation review:
   - confirm/correct this post-handover chronology;
   - identify any technical objection to Dave's no-pixel-detector ruling;
   - identify exact current decision IDs / sections superseded;
   - confirm chroma R-A remains separate;
   - confirm V1/V2/V3 evidence levels;
   - identify any useful Stage 2 experiment accidentally lost by removing Family B;
   - advise on the revised indexed-only Stage 2 ladder;
   - flag MUST / SHOULD / OPTIONAL changes separately.

3. ChatGPT drafts minimal repository updates:
   - `05_DECISIONS.md`
   - `06_DEBLOCK_CONCEPT.md`
   - `02_INDEX_FORMAT_SPEC.md`

4. Claude cold-reviews those proposed repository updates.

5. Dave amends/ratifies them.

6. ChatGPT drafts:
   - `Stage2_Experiment_Design_v0_2.md`

7. Claude reviews Stage 2 v0.2.

8. Dave ratifies Stage 2 v0.2.

9. Only then begin Stage 2 implementation, one bounded step at a time.
```

This restores the normal working pattern:

```text
ChatGPT drafts
    ->
Claude reviews
    ->
Dave decides / ratifies
    ->
ChatGPT proceeds
```

No Stage 2 code should be started before the revised design is ratified.

---

## 18. Specific questions for Claude

Please answer these against your own `Claude_REVIEW_OF_LG_EP_MLS_Stage1_Runs_v0_1.md`, the
repository files, and the pristine-reference-decoder findings already in your chat.

1. Does this document correctly capture everything material that happened **after** your LG EP/MLS
   Stage 1 review?
2. Do you agree LP is unusually strong first luma development material for the **index-driven**
   design on the re-grounded rationale: full resolution, heavier QP, and substantial authoritative
   FRAME/FIELD populations?
3. Do you see any technical reason Dave's production design still needs a pixel seam-position
   detector or Family B control once index-driven operation is a fixed product premise?
4. What exact `05_DECISIONS.md` decision IDs are superseded or need amendment by that ruling?
5. What exact `06_DEBLOCK_CONCEPT.md` sections/open items need amendment?
6. Does `02_INDEX_FORMAT_SPEC.md` require anything beyond the distinction:
   - index architecture fixed;
   - contents/packing still unfrozen?
7. Do you agree chroma R-A must be recorded as its own decision, separate from the index ruling?
8. Confirm the evidence levels:
   - V2 = VERIFIED reference-decoder implementation;
   - V3 same `quantizer_scale` = VERIFIED reference-decoder implementation;
   - V3 luma-matrix path for CHROMA420 = VERIFIED reference-decoder implementation, not yet a
     normative H.262 claim;
   - proposed interlaced same-field chroma access remains HYPOTHESIS/design inference unless you
     have since verified it.
9. Does the revised indexed-only Stage 2 sequence lose any experiment that is still necessary to
   answer the product's actual feasibility question?
10. Do you see any reason to unfreeze the Stage 1 inspector/analyzer from the LP/EP/MLS evidence?

Please classify your findings:

```text
MUST CHANGE
SHOULD CHANGE
OPTIONAL
NO OBJECTION
```

---

## 19. One-sentence current direction

> **Build and evaluate an MPEG-2-specific, index-driven deblocker that uses authoritative indexed
> luma geometry and effective QP, includes 4:2:0 chroma deblocking in scope, and spends Stage 2 on
> the actual filtering problem - edge protection, correction strength, NONE handling, chroma
> behaviour and no-harm/generalisation - rather than on reconstructing codec geometry from pixels.**

