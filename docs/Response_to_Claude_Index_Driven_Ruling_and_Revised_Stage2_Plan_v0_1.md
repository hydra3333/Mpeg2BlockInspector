# Response to Claude: Index-Driven Ruling and Revised Stage 2 Plan

**Filename:** `Response_to_Claude_Index_Driven_Ruling_and_Revised_Stage2_Plan_v0_1.md`  
**Version:** 0.1  
**Date:** 2026-10-07  
**From:** Dave / ChatGPT  
**Status:** Decision-and-review input for Claude. Not itself repository authority.

---

## 1. Dave's ruling

After revisiting the original project intent and the later Stage 0 expansion, Dave has decided:

> **The production MPEG-2 deblocker is index-driven by definition. It does not operate without its
> Stage 1/final `.idx2` index, and Stage 2 will not implement or evaluate a pixel-only seam-position
> detector or a pixel-only Family B deblocker.**

This is a scope decision, not an experimental finding that pixel-only deblocking is bad.

The reason is that the project is specifically intended to exploit authoritative MPEG-2 bitstream
information supplied by the indexer. The reference-decoder work has now established the relevant
geometry exactly enough that spending substantial Stage 2 effort throwing that information away and
trying to infer it again from reconstructed pixels is not justified for the product Dave wants to
build.

Dave accepts the resulting reduction in falsification breadth in exchange for a substantially
simpler and more directly relevant Stage 2.

---

## 2. Historical clarification

There are two distinct facts that should not be conflated.

### 2.1 Original/product architecture

The original project architecture was index-driven:

```text
Mpeg2BlockInspector
    MPEG-2 elementary stream
        ->
    .idx2

MPEG2Deblock
    VapourSynth clip
    + .idx2
    + strength
        ->
    filtered clip
```

The founding premise was that the deblocker should consume codec structure obtained authoritatively
while parsing the MPEG-2 stream rather than infer MPEG-2 coding structure from reconstructed
pixels.

That remains Dave's intended product.

### 2.2 Later Stage 0 experimental expansion

During Stage 0 research the project deliberately broadened into a more general falsification
exercise:

- Family B was made a mandatory strong pixel-only control;
- pixel-detected geometry was introduced;
- Step 2b was added;
- the custom-index architecture was made provisional on demonstrating advantage over a simpler
  decoder-side-data / pixel-inference path.

That was a legitimate research direction, and it became part of the ratified Stage 0 experimental
design.

Dave now regards that expansion as an unintended broadening of the project and explicitly
supersedes it.

Therefore it would be historically inaccurate to say that pixel-only experimentation was never in
scope. It *was* added later. The new ruling removes it from scope again.

---

## 3. Why Dave is comfortable removing the pixel detector

The decision rests on the combined findings from Stage 0/1 and Claude's recent reference-decoder
cold read.

### 3.1 Geometry is authoritative, not estimated

For the supported MPEG-2 frame-picture path, the index provides authoritative per-macroblock
transform state:

```text
FRAME
FIELD
NONE
```

The important luma consequence is the mid-height horizontal seam:

```text
FRAME:
    the mid-height transform seam exists

FIELD:
    that seam does not exist

NONE:
    no current coded residual transform seam is asserted
```

The fixed vertical seams and macroblock-edge seams come from the known MPEG-2 grid.

Thus the index supplies the difficult per-macroblock decision directly.

### 3.2 The index also prevents false geometry

The value is not merely finding seams that exist.

For FIELD macroblocks, the index authoritatively states that the FRAME-style mid-height seam is
absent. That prevents a deblocker from smoothing genuine image detail at a location that is not a
current transform seam.

The transform state also constrains safe filter support between known seams.

### 3.3 Stage 1 showed this is not a rare path

Real LG material contains extensive mixed FRAME/FIELD organisation.

Examples already measured include:

```text
LG LP:
    FIELD 52.74%
    FRAME 22.97%
    NONE 24.29%
    mixed FRAME/FIELD frames 97.06%

LG EP:
    FIELD 76.22%
    FRAME 9.69%
    NONE 14.09%
    mixed FRAME/FIELD frames 99.54%

TEST_2A_A001 original:
    FRAME-dominant, materially different again
```

So the authoritative index paths are heavily exercised in the actual target material.

### 3.4 What still requires pixel analysis

Removing a pixel seam-position detector does **not** make the filter purely metadata-driven in the
sense of blindly smoothing every known seam.

The index answers:

```text
WHERE is a legitimate transform seam?
WHAT transform geometry applies?
WHAT is the effective per-MB QP?
```

The decoded pixels still have to answer questions such as:

```text
Does this known seam actually look objectionably block-like?
Is it instead a genuine high-contrast image edge?
How much correction is safe?
How should local activity/detail limit the correction?
```

So the filter remains edge-preserving and pixel-aware at the known indexed seams.

What is removed is only the attempt to infer **seam position / FRAME-vs-FIELD geometry** from
pixels.

---

## 4. Consequence for the LP/EP discussion

LP remains the preferred first real-recorder luma development sample, but the rationale changes.

The correct LP rationale is now:

- genuine LG recorder output;
- full 720x576;
- substantial real quantisation: QP median 18, mean 21.285, max 112;
- substantial FRAME and FIELD populations;
- 97.06% mixed FRAME/FIELD frames;
- therefore heavy exercise of both authoritative index-directed geometry paths under realistic
  recorder compression.

It is **not** preferred because it gives a pixel detector many opportunities to guess FRAME/FIELD
correctly.

EP remains a strong complementary FIELD-heavy sample.

MLS remains useful as a progressive/fixed-geometry and chroma/no-harm control, but not as evidence
about the FRAME/FIELD index paths.

The software `_blocky` re-encodes remain optional stress/reference material; they are no longer
needed to justify the index architecture.

---

## 5. Chroma remains in scope

Dave's separate ruling that 4:2:0 chroma is in scope remains unchanged.

Claude's V2/V3 cold-read findings are especially useful:

- 4:2:0 chroma transform placement does not follow luma `dct_type`;
- chroma uses the macroblock's same effective quantiser;
- in the inspected reference-decoder 4:2:0 path, the luma quantisation matrices apply rather than
  separate chroma matrices.

Therefore the first chroma path should remain simple:

```text
native Cb/Cr planes
+
fixed 8x8 chroma transform grid
+
effective indexed per-MB QP
+
pixel edge/activity protection
```

Luma FRAME/FIELD/NONE must not be copied into chroma transform geometry.

Chroma does not independently justify the custom index, but that question is now moot as an
architecture gate because Dave has fixed the overall product architecture as indexed.

The open chroma questions remain:

- threshold;
- strength;
- horizontal/vertical treatment;
- interlaced same-field sample access where appropriate;
- colour-smearing/no-harm behaviour.

---

## 6. Proposed Stage 2 objective after this ruling

The Stage 2 question should change from:

> Does authoritative MPEG-2 metadata beat a pixel-only alternative strongly enough to justify the
> index architecture?

to:

> **Given authoritative indexed MPEG-2 geometry and QP, what filtering rule produces useful luma
> and chroma deblocking without unacceptable damage, and which indexed metadata are actually needed
> in the final format?**

This is closer to the original project purpose and removes a large branch of non-production work.

The feasibility gate still matters.

Dave is **not** pre-deciding that the deblocking filter will be good enough to ship.

Stage 2 may still conclude:

- the chosen kernel is ineffective;
- useful strength is too small;
- artifact reduction is not worth damage to detail;
- off-grid propagated blocking limits benefit too much;
- chroma filtering causes unacceptable colour damage;
- another candidate algorithm is required;
- or the project should stop.

What is no longer being tested is whether the index itself should be replaced by pixel inference.

---

## 7. Proposed revised Stage 2 experiment

### Step 1 - Unfiltered baseline

Decoded MPEG-2, no filtering.

Purpose:

- visual baseline;
- numerical baseline where a paired reference exists.

### Step 2 - Indexed geometry + fixed/emulated QP

Use authoritative:

```text
FRAME/FIELD/NONE geometry
```

from the index for every luma decision.

Use a fixed/emulated quantiser value for the candidate filter.

Purpose:

- establish the behaviour of the candidate kernel and edge/activity logic;
- provide a clean comparison for real-QP value.

No pixel seam-position detector exists.

### Step 3 - Indexed geometry + real effective per-MB QP

Same geometry, detector-at-known-seam logic, support and kernel as Step 2.

Only change:

```text
fixed/emulated QP
    ->
real effective indexed per-MB QP
```

Primary comparison:

```text
Step 2 vs Step 3
    =
value of real QP within the actual index-driven design
```

### Step 4 - Kernel / threshold / strength development

Using indexed geometry and real QP:

- tune the bounded short-support correction;
- tune edge/detail rejection;
- establish useful global strength behaviour;
- verify OFF is bit-exact;
- verify filter support never crosses another known transform seam;
- report I/P/B behaviour separately where useful.

This is where the real filtering research belongs.

### Step 5 - NONE policy

`NONE` remains a genuine design question because:

```text
NONE != no visible blocking
```

Prediction can carry old blocking through skipped/no-residual regions.

The experiment should compare only index-consistent policies.

Possible first alternatives:

**N0 - conservative**

```text
do not invent an internal transform seam in NONE
```

**N1 - bounded non-transform fallback at fixed grid boundaries only**

Only if a specific evidence-backed need remains after N0; do not resurrect a general pixel
FRAME/FIELD detector through this route.

The exact N1 wording should be reviewed carefully by Claude before implementation.

### Step 6 - bounded chroma experiment

Use fixed 4:2:0 chroma geometry.

Compare:

```text
C0  unfiltered chroma

C1  chroma filter + fixed/emulated QP

C2  same chroma filter + real indexed per-MB QP
```

Questions:

- does chroma filtering visibly/numerically help?
- does real QP improve it?
- what chroma strength/threshold is safe?
- does it avoid colour smearing and field mixing?

### Step 7 - generalisation / no-harm testing

Primary real-recorder set:

```text
LG_576i_3_LP
LG_576i_4_EP
TEST_4A_A003 original
TEST_2A_A001 original
```

Control/additional material:

```text
LG_576i_5_MLS
```

Optional severe/reference stress material:

```text
TEST_4A_A003_blocky
TEST_2A_A001_blocky
```

The real-recorder set should dominate the product decision.

The software re-encodes may still be useful where paired-reference metrics are desirable, but they
are no longer the principal evidence for architecture.

### Optional later experiments only if a demonstrated problem remains

- custom-matrix-aware thresholding;
- CBP;
- coefficient activity;
- heavier Family C/reference method.

Do not add these automatically.

---

## 8. What should be deleted from the current Stage 2 design

`Stage2_Experiment_Design_v0_1.md` should be superseded by v0.2 rather than patched informally.

Remove the following concepts from the core design:

- Family B as mandatory pixel-only control;
- pixel-detected seam geometry;
- Step 2b metadata-blind/pixel-geometry path;
- current Step 3 pixel-detected geometry path;
- current Step 3-vs-4 transform-state justification experiment;
- 2-vs-4 Family B architecture comparison;
- detector-versus-index FRAME/FIELD/NONE confusion matrix;
- any requirement to prove the custom index better than a pixel-only detector;
- any statement that the production index architecture remains contingent on beating a simpler
  pixel-only geometry path.

Retain:

- unfiltered baseline;
- indexed FRAME/FIELD/NONE geometry;
- real-QP versus fixed-QP ablation;
- edge/detail pixel tests at known seams;
- support-length constraints;
- I/P/B reporting;
- off-grid propagated-blocking limitation;
- chroma experiment;
- final no-harm/feasibility gate.

---

## 9. Proposed repository-document updates

These are proposed edits for Claude to draft, then ChatGPT to cold-review, then Dave to ratify.

### 9.1 `05_DECISIONS.md`

Add a new DECIDED entry recording Dave's ruling:

> **Index-driven production architecture / no pixel seam-position detector.**  
> The MPEG-2 deblocker requires its matching index and consumes authoritative transform geometry
> from it. Stage 2 will not implement or evaluate a pixel-only seam-position detector or Family B
> pixel-only deblocker. Pixels remain used for block-vs-real-edge discrimination and correction
> limiting at known indexed seams.

The new entry should explicitly supersede whichever existing decisions currently establish:

- Family B as mandatory control;
- Step 2b / pixel-detected geometry as required Stage 2 work;
- the custom index architecture as provisional on outperforming a pixel-only geometry path.

From the review trail, **D-18** is the decision that added Step 2b and should be marked
`SUPERSEDED` by the new ruling.

Any other affected decision IDs should be identified from the current pristine
`05_DECISIONS.md` rather than guessed from review-document labels.

Preserve, not supersede:

- frame-owned processing;
- Family A as leading algorithm family;
- minimal first metadata set;
- I/P/B reporting;
- one global manual strength;
- Python Stage 2 reference/oracle;
- final index format remaining unfrozen until the useful metadata set is understood.

### 9.2 `06_DEBLOCK_CONCEPT.md`

Revise the conceptual architecture so that:

```text
seam geometry:
    authoritative from MPEG-2/index

pixel analysis:
    classifies/limits correction at those known seams
```

Remove Family B as a required algorithm family.

Remove pixel-detected geometry as a Stage 2 path.

Remove or supersede the open question asking whether authoritative transform state beats a strong
pixel-only control.

Replace the Stage 2 ablation ladder with the indexed-only ladder in section 7 above.

Clarify that "no pixel detection of seam positions" is now a production/design rule, while
pixel-domain edge/activity analysis remains required.

Incorporate Claude's V1-V3 knowledge updates, subject to Dave ratification:

- K-03 reference-decoder representation/placement verified;
- K-04 4:2:0 chroma placement verified;
- 4:2:0 chroma same effective per-MB quantiser and matrix-path finding recorded at the appropriate
  evidence level.

Keep:

- NONE limitation;
- field-picture path still separate/open;
- off-grid propagated blocking;
- exact filtering equations/thresholds open.

### 9.3 `02_INDEX_FORMAT_SPEC.md`

Do **not** freeze the final binary packing merely because the architecture is now fixed.

Change the architecture wording so that:

> the production deblocker requires a matching index.

Remove any implication that the entire index architecture may be abandoned if QP is available from
FFmpeg side data or if a pixel-only detector performs well.

However, retain the useful distinction:

- the **index architecture is decided**;
- the **index contents and packing remain not frozen** until Stage 2 shows which metadata the
  production filter actually consumes.

The final index should carry, directly or derivably, whatever Stage 2 confirms the filter requires.
Current leading requirements are:

- output/display frame correspondence;
- authoritative FRAME/FIELD/NONE transform state for luma;
- sufficient quantiser information to obtain the effective MPEG-2 scale used by the algorithm;
- required picture/frame structural information.

Do not yet add CBP, coefficient activity, motion data or extra diagnostics merely because the Stage
1 temporary index has them.

FFmpeg per-MB QP side-data knowledge remains useful background/validation information, but no
longer represents an alternate production architecture.

### 9.4 `MPEG2_Macroblock_Index_VapourSynth_Deblocking_Project_Proposal_v0_5.md`

This proposal is subordinate to repository authority, so updating it is optional if the team no
longer uses it routinely.

If retained as an active roadmap, issue a new version stating:

- index-driven architecture is DECIDED;
- pixel-only Family B architecture testing is removed;
- feasibility gate now concerns deblocking quality/no-harm and useful metadata, not whether to keep
  the index at all;
- chroma is in scope;
- real LG LP/EP material has superseded the software `_blocky` material as primary development
  evidence.

### 9.5 `Stage2_Experiment_Design_v0_1.md`

Supersede with:

```text
Stage2_Experiment_Design_v0_2.md
```

Do not merely annotate v0.1 because the experimental premise has materially changed.

### 9.6 Stage 1 documents

No Stage 1 inspector/analyzer change follows from this ruling.

Stage 1 has already produced the authoritative metadata the new Stage 2 design intends to use.

`Stage1_Evidence_and_Gate_Report_v0_3.md` remains valid.

---

## 10. Revised forward plan

Proposed workflow from here:

```text
1. Claude reviews this ruling/response.
   - identify any technical objection;
   - identify exact current 05/06/02 sections/decision IDs affected;
   - check that no useful experiment is accidentally lost.

2. Claude drafts repository updates:
   - 05_DECISIONS.md
   - 06_DEBLOCK_CONCEPT.md
   - minimal 02_INDEX_FORMAT_SPEC.md change

3. ChatGPT cold-reviews those drafts against:
   - original project intent;
   - Stage 0 research;
   - Stage 1 evidence;
   - Claude V1-V3 source verification;
   - Dave's new ruling.

4. Dave ratifies/amends the repository updates.

5. ChatGPT drafts `Stage2_Experiment_Design_v0_2.md`
   from the updated repository authority.

6. Claude reviews Stage 2 v0.2.

7. Dave ratifies Stage 2 v0.2.

8. Implement Stage 2 incrementally:
   S2-I1  read-only indexed harness / validation
   S2-I2  authoritative seam-map diagnostics
   S2-I3  indexed Family A + fixed/emulated QP
   S2-I4  real indexed QP
   S2-I5  kernel/threshold/strength work
   S2-I6  NONE policy
   S2-I7  bounded chroma experiment
   S2-I8  generalisation/no-harm gate

9. Produce a Stage 2 feasibility report.

10. Only after Stage 2 PASS:
    freeze useful final index semantics/contents,
    then proceed toward final indexer/specification and C++/API4/scalar/AVX2 work.
```

This keeps the evidence-first workflow while removing the substantial experimental branch that no
longer serves the product definition.

---

## 11. Questions for Claude

Please review the following specifically.

1. Do you agree that removing the pixel-only Family B / pixel seam-position detector is technically
   coherent once Dave fixes the product architecture as index-driven?
2. Is any important filtering question lost by accepting authoritative FRAME/FIELD/NONE geometry as
   an input premise rather than experimentally re-inferring it?
3. Do you agree that pixels should still be used for edge/detail/blocking classification and
   correction limiting at known indexed seams?
4. Do you agree with the simplified fixed-QP versus real-indexed-QP ablation?
5. How should the first NONE experiment be phrased so that it does not accidentally recreate a
   general pixel seam detector?
6. Do you agree with the proposed chroma path: fixed chroma geometry + effective indexed QP, with
   no luma `dct_type` geometry?
7. Please identify the exact current `05_DECISIONS.md` entries that the new ruling should supersede,
   especially D-18 and the decision making Family B mandatory.
8. Please identify the exact `06_DEBLOCK_CONCEPT.md` sections/open items that should be removed or
   rewritten.
9. Please advise whether `02_INDEX_FORMAT_SPEC.md` needs any change beyond distinguishing
   "architecture fixed" from "contents/packing still unfrozen."
10. Do you agree that LP should remain primary luma development material for the re-grounded reasons
    in section 4?
11. Do you agree with the revised forward plan in section 10?

Please separate:

- MUST change;
- SHOULD change;
- optional refinements.

---

## 12. Dave's decision in one sentence

> **We are building an MPEG-2-specific, index-driven deblocker; Stage 2 will use the exact geometry
> supplied by the index and will experiment with how best to filter those known seams, not spend
> effort building a blind pixel detector to rediscover geometry the decoder has already told us.**

