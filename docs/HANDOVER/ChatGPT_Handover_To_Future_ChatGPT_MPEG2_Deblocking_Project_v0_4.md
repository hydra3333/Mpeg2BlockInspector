# ChatGPT Handover to Future ChatGPT Chat
## MPEG-2 Macroblock Index / VapourSynth Deblocking Project

**Filename:** `ChatGPT_Handover_To_Future_ChatGPT_MPEG2_Deblocking_Project_v0_4.md`  
**Version:** 0.4  
**Date:** 2026-10-09  
**Author:** ChatGPT  
**Status:** Current role-specific handover / orientation for a future ChatGPT chat. Not repository authority. Migration facts are delegated to the common Developer Handback where possible.  
**Supersedes:** `ChatGPT_Handover_To_Future_ChatGPT_MPEG2_Deblocking_Project_v0_3.md`

---

## 1. Purpose

This document exists so that a future ChatGPT chat can resume the project safely if the current
chat reaches its conversation limit.

It records:

- the project objective;
- roles and workflow;
- current repository authority;
- the latest ratified design state;
- important technical findings;
- current sample roles;
- Stage 1 status;
- Stage 2 status;
- the immediate next activity;
- future implementation order;
- known cautions and non-goals;
- which documents a future chat should read first.

Where this handover conflicts with a later ratified repository document or ratified design
document, the later ratified document prevails.

---

## 2. Project identity

### 2.1 Local project root

Current production repository root:

```text
E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock
```

The previous local tree under:

```text
E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector
```

is retained as rollback/reference material. Do not use it as the active build/test tree.

### 2.2 Handover storage

Current AI handover documents are stored under:

```text
E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock\docs\HANDOVER
```

Do not confuse this with `docs\REPOSITORY`.

### 2.3 Repository / product identity

GitHub repository:

```text
https://github.com/hydra3333/VapourSynth-mpeg2Deblock
```

Repository / umbrella project direction:

```text
VapourSynth-mpeg2Deblock
```

The existing command-line inspector remains named:

```text
Mpeg2BlockInspector
```

Current Phase-2 layout:

```text
src\Mpeg2BlockInspector\              inspector C/H source
tools\Stage1_Inspector_Analyzer_v0_2.py
vs\VapourSynth-mpeg2Deblock\          Visual Studio solution/project
TESTING\                              test BAT/VPY scripts
VHSC_samples\                         tracked sample media/index/log evidence
docs\                                 project documentation
```

Future Stage-2 Python belongs under `experiments\stage2\` when S2-I1 starts. Migration now deliberately creates the VapourSynth plugin project/build skeleton before returning to technical development; that placeholder does not implement the Stage-2/deblocking algorithm.

### 2.4 Product goal

Build an MPEG-2-specific VapourSynth API4 deblocker supported by a matching external MPEG-2
macroblock index.

Conceptually:

```text
MPEG-2 stream
    ->
Mpeg2BlockInspector / final indexer
    ->
matching index

VapourSynth decoded clip
    +
matching index
    +
user strength
    ->
MPEG-2-specific deblocked output
```

The production filter is now **index-driven by definition**.

---

## 3. People and roles

### Dave

- project owner;
- final authority;
- ratifies specifications, decisions and acceptance;
- controls the local repository and sample material;
- judges visual quality.

### ChatGPT

- primary drafter / implementation partner;
- technical mechanics analysis;
- specification drafting;
- code and test design when authorised;
- reviews Claude proposals;
- must not silently promote drafts to authority.

### Claude

- independent reviewer / designer;
- cold-review role;
- checks ChatGPT drafts against pristine source, evidence and ratified repository knowledge;
- may perform source cold reads;
- identifies blocking versus optional issues.

### Current default workflow

```text
ChatGPT drafts
    ->
Claude cold-reviews
    ->
Dave amends / ratifies
    ->
ChatGPT proceeds
```

Dave remains final authority.

---

## 4. Repository authority model

The principal project authority documents are:

```text
05_DECISIONS.md
06_DEBLOCK_CONCEPT.md
02_INDEX_FORMAT_SPEC.md
```

Research, review, handover and evidence documents are subordinate unless a ratified authority
document explicitly incorporates their result.

Important management rule:

> Review documents explain why. Repository authority says what the project currently believes or
> has decided.

Do not allow large review trails to become competing authority.

---

## 5. Current ratified repository state

The previous repository revision round is complete.

### 5.1 `05_DECISIONS.md`

```text
Version: 1.1
Status: RATIFIED
Date: 2026-10-08
SHA-256:
8db00dd4930542f56fc81e774cd3a569babc4a0650b5677ddf053480091ac004
```

Important v1.1 state includes:

```text
D-11  SUPERSEDED by D-24
D-17  SUPERSEDED by D-24
D-18  SUPERSEDED by D-24

D-08  AMENDED by D-26
D-15  AMENDED by D-24
D-23  CLARIFIED

D-24  DECIDED
D-25  DECIDED
D-26  DECIDED
```

### 5.2 `06_DEBLOCK_CONCEPT.md`

```text
Version: 1.1
Status: RATIFIED
Date: 2026-10-08
SHA-256:
f5b5f587dc5a15c3343b3368709c0d75ba7ab9de718efe86624752f765e0a5e1
```

Important v1.1 state includes:

```text
K-07  revised and ACCEPTED
K-10  ACCEPTED
K-11  ACCEPTED
```

### 5.3 `02_INDEX_FORMAT_SPEC.md`

```text
Version: 0.4
Status:
    DRAFT / NOT FROZEN
    current constraints and architecture ratified
Date: 2026-10-08
SHA-256:
6f8f076526336829ce8df1719f23d8dc9755d59acaaaaa4539ad336edc45596e
```

Critical distinction:

```text
INDEX-DRIVEN ARCHITECTURE:
    decided

FINAL INDEX CONTENTS / PACKING:
    not frozen
```

### 5.4 Ratified repository package

```text
REPOSITORY_RATIFIED_2026-10-08.zip
SHA-256:
cbf67b81136b33848012b28017612b5d2e226923c1fc62d820c5e8f07bdc5e2e
```

Claude checked the package after ratification and reported:

- US-ASCII;
- CRLF;
- zero bare LF;
- only the expected status / ratification changes;
- no objection.

---

## 6. Major current decisions

### 6.1 D-24 - index-driven production architecture

The production MPEG-2 deblocker requires its matching index.

Stage 2 does **not**:

- implement a pixel-only seam-position detector;
- implement Family B;
- compare index-driven versus pixel-only production architectures;
- require the custom index to justify itself by beating a pixel-only alternative.

This is a **scope / architecture decision**, not an experimental finding that pixel-only filtering
is technically inferior.

Pixels are still required at known seams for:

- block-versus-real-edge judgement;
- activity/detail protection;
- correction limiting.

Current model:

```text
INDEX
    -> authoritative seam geometry / eligibility

PIXELS
    -> blocking-versus-detail classification
    -> local protection / correction limiting

INDEXED QP + USER STRENGTH
    -> correction scale
```

### 6.2 D-25 - chroma is in scope

MPEG-2 4:2:0 chroma deblocking is in production scope on mechanism.

Stage 2 does not need to prove merely that chroma blocking can exist.

Stage 2 must instead establish:

- safe threshold;
- useful strength;
- horizontal / vertical treatment;
- interlaced access;
- no field mixing;
- no colour smearing;
- useful product benefit.

### 6.3 D-26 - evidence hierarchy

Primary product evidence:

```text
real LG recorder material
```

Secondary evidence:

```text
software blocky transcode pairs
```

No single numerical metric decides the project.

Dave's visual judgement on target material remains essential.

### 6.4 Existing-filter yardstick

Dave explicitly ruled:

> Do not include an existing external deblocker as a planned Stage 2 yardstick.

It may be revisited only if later evidence creates a specific fallback need.

---

## 7. Technical knowledge that must not be lost

### 7.1 FRAME / FIELD / NONE semantics

The transform state describes applicable **coded residual transform geometry**.

It is not simply the value or presence of `dct_type`.

```text
FRAME
FIELD
NONE
```

`NONE` applies where no coded residual transform geometry exists, including:

- skipped macroblocks;
- effective-CBP-zero non-intra macroblocks.

A `dct_type` bit may nevertheless have been read in some no-residual cases.

### 7.2 Critical NONE geometry clarification

This was discovered during Claude's Stage 2 v0.2 review and is incorporated into ratified Stage 2
v0.3:

> A NONE macroblock has **no internal transform seam in either orientation**.

Therefore:

```text
NONE:
    no internal vertical x=8 seam
    no internal horizontal mid-height seam
    outer macroblock-edge locations only
```

For coded FRAME and FIELD macroblocks:

```text
internal vertical x=8 seam exists
```

For FRAME only:

```text
internal horizontal mid-height transform seam exists
```

This clarification should also be carried into the **next revision of `06_DEBLOCK_CONCEPT.md`**.
It is not blocking current Stage 2 work because Stage 2 v0.3 already states it correctly.

### 7.3 Frame-owned interlaced processing

Processing remains frame-owned.

Do not split the decoded image into independently filtered field images.

Use field-parity-aware sample access where ordinary filtering across a seam would otherwise mix
temporally different fields.

### 7.4 Luma FRAME internal horizontal seam

For an interlaced 16-line luma macroblock:

```text
top-field pair around FRAME seam:
    6 | 8

bottom-field pair around FRAME seam:
    7 | 9
```

relative to the macroblock.

### 7.5 Chroma V1-V4 findings

Claude performed reference-decoder cold reads.

#### V1

Luma frame-picture block placement confirms the relevant FRAME/FIELD geometry.

#### V2

For MPEG-2 4:2:0, chroma transform placement does **not** follow luma `dct_type`.

#### V3

In the inspected reference decoder's MPEG-2 4:2:0 path:

- chroma uses the macroblock's same `quantizer_scale`;
- the luma matrix-selection path applies to 4:2:0 chroma.

Evidence precision:

> VERIFIED reference-decoder implementation finding.

Do not silently promote this to a stronger normative H.262 claim without separate verification.

#### V4

For 4:2:0 field prediction in frame pictures, the inspected decoder reconstructs chroma with
alternating field parity by chroma line:

```text
even chroma line -> top field
odd chroma line  -> bottom field
```

This verifies the **premise** for same-field chroma access.

Whether the post-filter should use same-field chroma access remains a Stage 2 design choice.

---

## 8. Stage 1 status

Stage 1 is **complete / PASS / frozen** for current purposes.

Important documents:

```text
Stage1_Inspector_Instrumentation_Design_v0_3.md
Stage1_Inspector_Analyzer_v0_2.py
Stage1_Evidence_and_Gate_Report_v0_3.md
```

`Stage1_Evidence_and_Gate_Report_v0_3.md` is ratified.

Do not reopen Stage 1 unless later evidence exposes a concrete need.

In particular:

- do not reopen simply to capture quantisation-matrix coefficient values;
- do not add metadata merely because the temporary format can hold it.

---

## 9. Important sample set and roles

### Development

```text
LG_576i_3_LP
```

Known important properties:

```text
720x576
204 frames
45x36 MB
interlaced / TFF
FRAME 22.97%
FIELD 52.74%
NONE  24.29%
mixed FRAME/FIELD frames 97.06%
QP median 18
QP mean 21.285
QP max 112
```

### Locked interlaced hold-outs

```text
LG_576i_4_EP
TEST_4A_A003 original
TEST_2A_A001 original
```

### Progressive / control

```text
LG_576i_5_MLS
```

Important MLS characteristics:

```text
progressive_frame = 1 throughout
FIELD = 0
FRAME = 85.44%
NONE = 14.56%
QP median = 10
```

### Secondary paired-reference / stress material

```text
TEST_4A_A003_blocky
TEST_2A_A001_blocky
```

Important limitation:

> The `_blocky` transcodes use effective QP 62 everywhere.

Therefore their fixed-median-QP and real-per-MB-QP variants are identical with respect to QP.

They **cannot** answer whether a spatial QP map is useful.

They remain useful only as secondary paired-reference / severe-blocking evidence.

---

## 10. Stage 2 design status

### 10.1 Current design

Current Stage 2 design:

```text
Stage2_Experiment_Design_v0_3.md
```

Dave ratified v0.3 on 2026-10-08 after Claude reviewed the revised v0.2 and gave:

```text
NO OBJECTION to ratification
```

Known generated v0.3 SHA-256:

```text
b02749dba6d50e8ad0c532a159bb0df42761c86b23571576209d6fbbb868af24
```

Important practical note:

- the generated file was created immediately before Dave's explicit ratification message;
- if its header still says "ready for Dave ratification", Dave's subsequent ratification in chat is
  controlling;
- when next maintaining the stored file, its status metadata may be updated to RATIFIED without
  changing technical content.

No Stage 2 code has been written. S2-I1 remains the next technical code increment only after the migration close-out handback is ratified and Dave explicitly authorises technical coding.

### 10.2 Superseded Stage 2 designs

Earlier versions are design history:

```text
Stage2_Experiment_Design_v0_1.md
Stage2_Experiment_Design_v0_2.md
Stage2_Experiment_Design_v0_2_REVISED_AFTER_CLAUDE_REVIEW.md
```

Do not use them instead of v0.3.

---

## 11. Ratified Stage 2 v0.3 - key experiment structure

### Step 1

Unfiltered baseline.

### Step 2

Authoritative indexed geometry + fixed clip-wide QP.

Fixed-QP rule:

```text
Q_fixed(clip) = median effective per-MB QP of that clip
```

### Step 3

Same geometry / same kernel / same pixels / same strength, but:

```text
fixed median QP
    ->
real indexed per-MB QP
```

Purpose:

> isolate the value of the spatial QP map inside the already-decided index-driven architecture.

### Step 4

Luma kernel / threshold / strength development.

### Step 5

Conservative NONE policy.

Initial N0:

```text
NONE:
    outer macroblock edges only
    no internal vertical seam
    no internal horizontal seam
```

### Step 6

Bounded native 4:2:0 chroma experiment.

Conceptual comparison:

```text
C0 unfiltered
C1 fixed clip-wide QP
C2 real indexed per-MB QP
```

### Step 7

Locked generalisation / no-harm evaluation.

---

## 12. Stage 2 v0.3 - important methodological details

### 12.1 Mandatory spatial index-to-pixel registration check

Stage 1 proved temporal correspondence.

Before filtering-quality conclusions, Stage 2 must also validate spatial registration.

Detector-free checks include:

#### FRAME-versus-FIELD shifted-label contrast

Compute a FRAME-minus-FIELD seam statistic using index labels shifted by:

```text
x: -1, 0, +1 macroblock
y: -1, 0, +1 macroblock
```

Correct registration should produce the contrast maximum at zero shift.

#### 8-pixel column grid-phase check

Measure vertical-boundary step by:

```text
x mod 8
```

Expected coding-grid signal should peak at phase 0.

Important caveat:

- an 8-pixel horizontal offset is itself on the 8-pixel phase;
- therefore the shifted-label contrast must also be interpreted;
- absence of a clear zero-shift maximum is a stop condition.

These diagnostics validate alignment.

They do **not** infer production seam geometry from pixels.

### 12.2 Stage 2 reader cross-check

The new Stage 2 index reader must reproduce analyzer v0.2 summaries for formal clips, including at
least:

```text
record count
FRAME / FIELD / NONE totals
QP histogram / totals
```

A mismatch must be resolved before filter experiments.

### 12.3 K0 selection versus QP-map comparison

Avoid selecting K0 on the same LP frames used to compare fixed versus real QP.

For this experiment, define a GOP as:

> the display-order run from one I picture up to, but not including, the next I picture.

Number GOPs from:

```text
0 at the first I picture
```

Use:

```text
even usable GOPs:
    K0 tuning / selection

odd usable GOPs:
    fixed-QP versus real-QP comparison
```

The split is fixed before viewing results.

### 12.4 Leading B pictures

For quality evidence:

> Exclude B pictures output before the first I picture of the clip.

Still include them for:

- structural validation;
- robustness;
- bounds safety;
- diagnostic completeness.

### 12.5 QP semantics for NONE

For a NONE macroblock:

> the indexed QP is the quantiser scale in force at that point in the slice, but it quantised no
> residual in that macroblock.

The pixels come from prediction and inherit prior reference-picture quantisation history.

Consequences:

- a shared boundary touching NONE may include a QP that does not directly describe that side's
  pixels;
- Step 2 versus Step 3 must report boundaries touching NONE separately;
- a different NONE-boundary QP rule, if needed, is an evidence question under Step 5.

### 12.6 Shared-boundary QP

Initial controlled hypothesis:

```text
Q_boundary = rounded mean(Q_left, Q_right)
```

Internal seam:

```text
Q = containing macroblock QP
```

Large disparities must be reported separately.

Known illustrative case:

```text
112 next to 14
    ->
rounded mean 63
```

Do not let the mean hide severe asymmetry.

---

## 13. Stage 2 implementation increments

No implementation has started.

Ratified order:

```text
S2-I1
    read-only Stage 1 index reader / validation
    reproduce analyzer v0.2 summary totals
    progressive_frame and picture-type handling
    leading-B quality exclusion accounting

S2-I2
    seam-map diagnostics
    two-dimensional spatial registration validation
    shifted-label controls
    8-pixel grid-phase check

S2-I3
    initial luma candidate kernel
    even usable LP GOPs
    fixed median QP
    select / freeze K0

S2-I4
    K0 fixed-QP versus real-QP comparison
    odd usable LP GOPs
    no retuning
    report NONE-touching boundaries separately

S2-I5
    real-QP luma kernel / threshold / strength development

S2-I6
    NONE N0 policy and evidence-driven alternatives only

S2-I7
    bounded native 4:2:0 chroma experiment

S2-I8
    locked hold-out / no-harm evaluation

S2-I9
    secondary paired-reference transcode reporting

S2-I10
    Stage 2 feasibility / metadata-retention gate report
```

---

## 14. Immediate current project state

This is the most important section for a future ChatGPT chat.

### Current technical state

```text
Repository technical authority:
    ratified

Stage 1:
    complete / PASS / frozen

Stage 2 design:
    v0.3 ratified

Stage 2 code:
    NOT STARTED

Next technical code increment after migration close-out + Dave authorization:
    S2-I1
```

### Current migration/build-system state

The repository rename/restructure is complete and published. The migration has since advanced into Visual Studio/build/release normalization.

Current accepted state:

```text
A1 remove Win32/x86 configurations:
    COMPLETE / committed

A2 replace old .sln with x64-only VapourSynth-mpeg2deblock.slnx:
    COMPLETE / committed

interactive .slnx load:
    PASS

mandatory pre-A3 Debug/Release checkpoint:
    COMPLETE

pre-A3 six tracked index regressions:
    PASS / byte-identical

M3 dumpbin baseline:
    COMPLETE
```

Dave has additionally ratified the build-policy direction:

```text
x64 + AVX2 is the minimum supported CPU target for inspector and plugin
pre-AVX2 CPUs are intentionally unsupported
Release EXE and DLL use /MT so no separate VC++ Redistributable is required
Release artifacts embed only the PDB filename
/GS ON
CFG ON
CET compatibility ON
Spectre mitigation ON with mitigated libraries required
inspector /sdl OFF only as the frozen reference-decoder-derived exception
new mpeg2Deblock code /sdl ON
project files are the source of build settings
GitHub Actions/harness verify those settings and do not inject replacements
```

The existing A3 v0.3 package that used SSE2/security-off settings is superseded and must not be applied.

### Immediate next activity

```text
FINISH STAGE-A A3 REVIEW/APPLICATION/GATE
```

Use the common handback and current migration design/plan rather than this role-specific document for exact migration mechanics:

```text
docs\HANDOVER\MPEG2_Deblocking_Developer_Handback_v0_4.md
Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_11.md
StageA_Visual_Studio_Normalization_Execution_Plan_v0_6.md
```

The immediate sequence is:

1. cold-review Design Record v0.11 and Stage A plan v0.6;
2. generate/review/ratify a superseding A3 candidate with AVX2, standalone runtime and security policy in the inspector `.vcxproj` itself;
3. apply A3 and run the complete Stage A gate;
4. Stage B creates the buildable dummy VapourSynth API4 DLL project with the same project-owned target/runtime/security policy;
5. Stage C creates the canonical local build harness;
6. Stage D adapts the CNR3 release-triggered GitHub workflow to invoke that same harness;
7. Stage E adapts the wheel/PyPI packaging scaffold and runs local install/smoke validation;
8. finalize/cold-review/ratify the common handback before technical development resumes.

Do not begin S2-I1 until migration is formally closed and Dave explicitly authorises coding.

---

## 15. Repository / GitHub decisions now settled

The following repository/build decisions are settled for the migration unless Dave explicitly reopens them:

- one umbrella Git repository, `VapourSynth-mpeg2Deblock`;
- active GitHub remote: `https://github.com/hydra3333/VapourSynth-mpeg2Deblock`;
- active local root: `E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock`;
- command-line inspector remains named `Mpeg2BlockInspector`;
- `TESTING\` and `VHSC_samples\` remain at repository root;
- inspector source is under `src\Mpeg2BlockInspector\`;
- analyzer is under `tools\`;
- Visual Studio files are under `vs\VapourSynth-mpeg2deblock\`;
- current umbrella solution is `.slnx`, x64 only, Debug + Release;
- future Stage-2 Python goes under `experiments\stage2\` when needed;
- migration creates the plugin build skeleton before technical Stage 2 resumes, but does not implement deblocking;
- project-developed material is AGPL-3.0-or-later; `NOTICE.md` preserves the distinct treatment of reference-decoder-derived source, restricted-use test recordings and other third-party material;
- updated `README.md` is the public product/build summary and points to `NOTICE.md`;
- x64 + AVX2 is the minimum supported CPU target for both native projects;
- Release EXE/DLL are configured in their `.vcxproj` files for static runtime `/MT` standalone distribution;
- `/GS`, CFG, CET and Spectre mitigation are enabled rather than traded away for performance;
- inspector `/sdl` remains OFF only as the frozen reference-decoder-derived exception; new plugin code uses `/sdl` ON;
- Windows SDK version is not pinned, but actual SDK/toolchain provenance is recorded;
- explicit platform toolset remains `v145`;
- build harness and GitHub Actions use one MSBuild/`.slnx` route and do not maintain a second flag map;
- actual PyPI publication is not authorized merely because a wheel scaffold is created.

### Still deliberate rather than accidental

Stage B/close-out must explicitly settle or record provisional status for coupled public/package identities, VapourSynth header/API profile, C++ language standard, floating-point policy, version-resource/version-source policy and other items called out by the current migration design.

Do not reinterpret those unresolved items as reopening the repository name/layout, AVX2, runtime-linkage or security-hardening policies above.

---

## 16. Visual Studio / CNR3 configuration rule for later work

The current migration no longer treats CNR3 as a bag of settings to copy later. The settings audit is active and evidence-driven.

Key rule:

> The accepted Visual Studio project files are the source of truth. The Stage C harness and Stage D GitHub workflow invoke those projects and verify effective settings; they do not inject a second compiler/linker policy.

For the inspector, CNR3's command-line/self-test project is the primary proven reference, reconciled against inspector requirements. For the plugin placeholder, CNR3's DLL project is the primary build reference, again with every difference classified and justified.

The current product-level target policy is already settled:

```text
x64 only
Debug + Release
/arch:AVX2 minimum
Release /MT
/GS ON
CFG ON
CET compatibility ON
Spectre mitigation ON
inspector /sdl OFF legacy exception
new plugin /sdl ON
```

Do not disable these security settings merely for performance. If performance later shows a concrete hotspot, profile and review that specific case rather than weakening the global security policy.

Use the actual current migration documents and CNR3 files at the time of work, not memory.

---

## 17. Important documents for a future ChatGPT chat

A future chat should ask for / read the **latest version of** the following.

### Highest priority

```text
ChatGPT_Handover_To_Future_ChatGPT_MPEG2_Deblocking_Project_v0_4.md
MPEG2_Deblocking_Developer_Handback_v0_4.md
Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_11.md
StageA_Visual_Studio_Normalization_Execution_Plan_v0_6.md
README.md
NOTICE.md
Claude_HANDOVER_TO_Future_Claude_Chat latest version
05_DECISIONS.md latest ratified version
06_DEBLOCK_CONCEPT.md latest ratified version
02_INDEX_FORMAT_SPEC.md latest version / ratified constraints
Stage2_Experiment_Design_v0_3.md
Stage1_Evidence_and_Gate_Report_v0_3.md
```

### Important recent Claude reviews

```text
Claude_REVIEW_Reconciliation_After_Handover_v0_1.md
Claude_REVIEW_OF_ChatGPT_Repository_Drafts_v1_1_v0_1.md
Claude_REVIEW_OF_ChatGPT_Stage2_Experiment_Design_v0_2.md
Claude_REVIEW_OF_ChatGPT_Stage2_Experiment_Design_v0_2_Revised_v0_1.md
Claude_REVIEW_OF_ChatGPT_Discussion_Brief_Index_Value_and_Chroma_Deblocking_v0_2.md
```

### Important Stage 1 design/evidence

```text
Stage1_Inspector_Instrumentation_Design_v0_3.md
Stage1_Inspector_Analyzer_v0_2.py
Stage1_Evidence_and_Gate_Report_v0_3.md
```

### Historical / provenance only where needed

```text
Stage2_Experiment_Design_v0_1.md
Stage2_Experiment_Design_v0_2.md
Stage2_Experiment_Design_v0_2_REVISED_AFTER_CLAUDE_REVIEW.md
MPEG2_Macroblock_Index_VapourSynth_Deblocking_Project_Proposal_v0_5.md
Response_to_Claude_Index_Driven_Ruling_and_Revised_Stage2_Plan_v0_1.md
ChatGPT_HANDOVER_TO_CLAUDE_After_LG_EP_MLS_Review_v0_1.md
ChatGPT_RESPONSE_TO_Claude_QUESTIONS_After_Handover_v0_1.md
```

Always prefer the latest ratified repository/design document over earlier provenance.

---

## 18. Things a future ChatGPT must not do

1. Do not revive Family B.
2. Do not build a pixel seam-position detector.
3. Do not add an existing-filter yardstick unless Dave explicitly reopens it.
4. Do not treat `_blocky` QP-62 transcodes as evidence for spatial QP-map value.
5. Do not give NONE an internal vertical or horizontal transform seam.
6. Do not treat a NONE macroblock's current indexed QP as having quantised residual pixels there.
7. Do not reopen Stage 1 without concrete evidence.
8. Do not capture quantisation-matrix values pre-emptively.
9. Do not start S2-I1 before the migration close-out/common handback is ratified and Dave explicitly authorises technical coding.
10. Do not treat handover/review docs as repository authority.
11. Do not reopen settled repository name/layout decisions merely because later plugin/CI/release details are deferred.
12. Do not use superseded Stage 2 v0.1/v0.2 designs in place of v0.3.

---

## 19. Suggested opening prompt for the next ChatGPT chat

Dave can start a future ChatGPT chat with approximately:

> We are continuing the MPEG-2 macroblock index / VapourSynth deblocking project. First read
> `ChatGPT_Handover_To_Future_ChatGPT_MPEG2_Deblocking_Project_v0_4.md` and the common
> `MPEG2_Deblocking_Developer_Handback_v0_4.md`, then the latest ratified
> `05_DECISIONS.md`, `06_DEBLOCK_CONCEPT.md`, `02_INDEX_FORMAT_SPEC.md`,
> `Stage2_Experiment_Design_v0_3.md`, and `Stage1_Evidence_and_Gate_Report_v0_3.md`.
> Also read the current repository `README.md` and `NOTICE.md`.
>
> Stage 2 v0.3 is ratified but no Stage 2 coding has started. Repository restructure is complete;
> the remaining work is migration/build-system close-out. Resume from the exact migration state in
> the common handback and current migration design/Stage A plan. Do not begin S2-I1 until migration
> is formally closed and I explicitly authorise technical coding.

---

## 20. Final current-state summary

The technical design remains aligned and Stage 2 remains untouched while migration/build-system close-out continues.

Current state:

```text
INDEX-DRIVEN ARCHITECTURE:
    ratified

CHROMA IN SCOPE:
    ratified

STAGE 1:
    complete / PASS / frozen

REPOSITORY AUTHORITY:
    ratified

STAGE 2 DESIGN:
    v0.3 ratified

STAGE 2 CODE:
    not started

REPOSITORY MODEL:
    one umbrella repo, VapourSynth-mpeg2Deblock

RESTRUCTURE:
    complete / published

STAGE A:
    A1 complete
    A2 complete
    pre-A3 checkpoint complete
    superseding AVX2/security-on A3 candidate still required

BUILD POLICY:
    x64 + AVX2 minimum
    Release /MT standalone artifacts
    /GS + CFG + CET + Spectre ON
    inspector /sdl OFF legacy exception
    new plugin /sdl ON
    project files are source of truth

LATER MIGRATION STAGES:
    Stage B placeholder DLL
    Stage C canonical harness
    Stage D release-triggered GitHub workflow using same harness
    Stage E wheel/PyPI scaffold

DOCUMENTATION:
    updated README describes intended public build/product policy
    NOTICE remains legal/attribution/restricted-test-media reference
    common Developer Handback v0.4 carries migration facts

IMMEDIATE NEXT TOPIC:
    finish current Stage A plan/A3 review and gate

NEXT TECHNICAL CODE ITEM AFTER MIGRATION CLOSE-OUT + DAVE AUTHORISATION:
    S2-I1 only
```

That is the state a future ChatGPT chat must preserve.

---

## 21. Change log

### v0.4 - 2026-10-09

- Replaced obsolete Phase-2/Gate-C migration state with the completed restructure plus current Stage A A1/A2/pre-A3 checkpoint state.
- Points migration facts to the common Developer Handback v0.4 and current migration design/Stage A plan.
- Records the ratified x64 + AVX2 minimum, Release `/MT`, PDB filename-only, `/GS`, CFG, CET, Spectre and SDL policies.
- Records the one-build-route rule for local harness and GitHub Actions.
- Records that the Stage B plugin build skeleton now occurs during migration before technical Stage 2 resumes, while still implementing no deblocking algorithm.
- Adds the updated `README.md` and `NOTICE.md` to the future-chat reading set and distinguishes README target-policy statements from actual gate evidence until migration acceptance.
- Updates the opening prompt and coding guard so S2-I1 remains blocked until formal migration close-out and Dave authorization.

### v0.3 - 2026-10-08

- Supersedes handover v0.2.
- Updates active repository/GitHub identity to `VapourSynth-mpeg2Deblock`.
- Records the new production local root and Phase-2 source/tools/vs/TESTING/VHSC layout.
- Records that the one-repository/name/layout discussion is settled for the current migration.
- Records Phase 1 / Gate B PASS and the Phase-2 restructure state through the NOTICE/handover step.
- Replaces the obsolete repository-design discussion as the immediate task with Phase-2 Gate C.
- Records that S2-I1 remains blocked only until Gate C passes and Dave explicitly authorises coding.
- Records the later CNR3-based Visual Studio configuration-normalisation requirement without
  transferring CNR3 compiler/linker settings into the frozen inspector.
- Records AGPLv3-or-later project-development licensing and the restricted test-recording treatment
  stated in `NOTICE.md`.

### v0.2 - 2026-10-08

- Supersedes handover v0.1.
- Updates repository documents from pending drafts to the ratified 05 v1.1 / 06 v1.1 / 02 v0.4
  baseline.
- Records D-24/D-25/D-26 ratification state.
- Records Stage 2 v0.3 as ratified.
- Adds final NONE geometry clarification.
- Adds detector-free two-dimensional registration design.
- Adds analyzer-summary cross-check requirement for the Stage 2 reader.
- Adds GOP definition / 0-based even-odd LP split.
- Adds NONE-QP semantic caveat and NONE-touching-boundary reporting.
- Records that QP-62 blocky transcodes cannot test spatial QP-map value.
- Records the current implementation sequence S2-I1 through S2-I10.
- Records that Stage 2 coding has not started.
- Changes the immediate next task to the project/local-Git/GitHub repository discussion.
- Corrects the handover storage path to `docs\HANDOVER`.

### v0.1 - 2026-10-07

- Initial future-ChatGPT handover.
