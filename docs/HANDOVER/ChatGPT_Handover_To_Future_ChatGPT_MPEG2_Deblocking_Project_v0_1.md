# ChatGPT Handover to Future ChatGPT Chat
## MPEG-2 Macroblock Index / VapourSynth Deblocking Project

**Filename:** `ChatGPT_Handover_To_Future_ChatGPT_MPEG2_Deblocking_Project_v0_1.md`  
**Version:** 0.1  
**Date:** 2026-10-07  
**Author:** ChatGPT  
**Status:** Handover / orientation for a future ChatGPT chat. Not repository authority.

---

## 1. Purpose of this handover

This document is intended to let a future ChatGPT chat resume the project safely if the present chat
reaches its length limit.

It summarises:

- project goals;
- participants and roles;
- workflow;
- authoritative and relevant documents;
- major findings and decisions already made;
- current status;
- immediate next steps;
- cautions / things not to lose.

This handover is **not** the primary source of truth where a newer or authoritative project document
exists. It is a roadmap to those documents and to the current state of play.

---

## 2. Project identity and goal

### 2.1 Project subject

This project is about building an **MPEG-2-specific VapourSynth API4 deblocker** supported by an
external **MPEG-2 macroblock index** derived from the MPEG-2 reference decoder.

### 2.2 Core product concept

The intended production architecture is now:

```text
Mpeg2BlockInspector (or final indexer)
    MPEG-2 elementary stream
        ->
    index file

MPEG-2 deblocker plugin
    VapourSynth clip
    + matching index
    + user strength parameter
        ->
    filtered clip
```

### 2.3 Current project objective

The current project objective is:

> Build and evaluate an MPEG-2-specific, **index-driven** deblocker that uses authoritative indexed
> luma geometry and effective QP, includes 4:2:0 chroma deblocking in scope, and spends Stage 2 on
> the real filtering problem (thresholds, edge protection, strength, NONE handling, chroma
> behaviour, no-harm, generalisation) rather than on reconstructing codec geometry from pixels.

---

## 3. People and roles

### 3.1 Dave / user

- final decision maker / ratifier;
- project manager;
- provides source materials, sample files and practical direction.

### 3.2 Claude

- independent reviewer / designer;
- performs cold reviews;
- checks ChatGPT draft text against repository documents, source and evidence;
- may perform pristine source cold reads;
- flags MUST / SHOULD / OPTIONAL changes.

### 3.3 ChatGPT

- drafter / coder-side analyst;
- drafts proposals, repository updates, design docs, reviews and handovers;
- does not become final authority by itself;
- proceeds only after Claude review and Dave ratification where required.

### 3.4 Current agreed workflow

```text
ChatGPT drafts
    ->
Claude reviews / cold-reviews
    ->
Dave amends / ratifies
    ->
ChatGPT proceeds
```

Use this as the default unless Dave or Claude explicitly change it.

---

## 4. Document authority model

### 4.1 Repository authority documents

These are the main project authority documents for this topic:

- `05_DECISIONS.md`
- `06_DEBLOCK_CONCEPT.md`
- `02_INDEX_FORMAT_SPEC.md`

These should be treated as authoritative once ratified.

### 4.2 Stage / evidence / review documents

These are important but subordinate:

- Stage 1 design / evidence docs;
- Stage 2 design docs;
- review documents by ChatGPT or Claude;
- handover / catch-up documents;
- provenance documents.

### 4.3 Project proposal

The project proposal series is helpful background and scope history, but subordinate to the current
repository documents once those exist and are ratified.

---

## 5. Important latest documents to know about

Below is the important known document set at the time of this handover.

### 5.1 Current repository baseline (current authority before proposed revision)

These were supplied by Dave in `REPOSITORY.zip` and are the current baseline repository files:

- `05_DECISIONS.md`  
  - Version: **1.0**
  - Status: **RATIFIED**

- `06_DEBLOCK_CONCEPT.md`  
  - Version: **1.0**
  - Status: **RATIFIED**

- `02_INDEX_FORMAT_SPEC.md`  
  - Version: **0.3**
  - Status: **DRAFT / constraints ratified**

These exact files were the baseline used for the current revision round.

### 5.2 Proposed revised repository drafts (not yet authority unless ratified)

These were just drafted by ChatGPT from the repository baseline:

- `repo_revised_drafts/05_DECISIONS.md`
  - proposed next version: **1.1 draft**

- `repo_revised_drafts/06_DEBLOCK_CONCEPT.md`
  - proposed next version: **1.1 draft**

- `repo_revised_drafts/02_INDEX_FORMAT_SPEC.md`
  - proposed next version: **0.4 draft**

Packaged in:

- `REPOSITORY_PROPOSED_UPDATE_2026-10-07.zip`

These **must be cold-reviewed by Claude and then ratified by Dave** before being treated as
authority.

### 5.3 Stage 1 design / code / evidence documents

Important Stage 1 artifacts include:

- `Stage1_Inspector_Instrumentation_Design_v0_3.md`
- `Stage1_Inspector_Analyzer_v0_2.py`
- `Stage1_Evidence_and_Gate_Report_v0_3.md`
  - Status: **RATIFIED**

Stage 1 is currently considered **frozen** unless later evidence exposes a real defect.

### 5.4 Stage 2 design document

- `Stage2_Experiment_Design_v0_1.md`

Important:

- This exists.
- It is **not** yet superseded.
- It still reflects the older broader experiment that included a pixel-only Family B / pixel
  detector branch.
- It is now expected to be superseded by a future:
  - `Stage2_Experiment_Design_v0_2.md`
- v0.2 must only be drafted **after** the repository revisions are reviewed and ratified.

### 5.5 Important review / provenance / handover documents

Important recent support documents include:

- `ChatGPT_HANDOVER_TO_CLAUDE_After_LG_EP_MLS_Review_v0_1.md`
- `ChatGPT_RESPONSE_TO_Claude_QUESTIONS_After_Handover_v0_1.md`
- `Response_to_Claude_Index_Driven_Ruling_and_Revised_Stage2_Plan_v0_1.md`
- `Claude_REVIEW_Reconciliation_After_Handover_v0_1.md`
- `Claude_REVIEW_OF_ChatGPT_Discussion_Brief_Index_Value_and_Chroma_Deblocking_v0_2.md`
- `ChatGPT_REVIEW_OF_Claude_Chroma_Index_Review_and_EP_MLS_Logs_v0_1.md`

These are not repository authority, but they capture the reasoning trail and exact review outcomes.

### 5.6 Earlier proposal / history documents

Relevant background series:

- `MPEG2_Macroblock_Index_VapourSynth_Deblocking_Project_Proposal_v0_5.md`
- earlier proposal versions exist, but use the latest version only if needed.

---

## 6. Current major decisions / direction

### 6.1 Index-driven ruling

Dave has ruled that the production deblocker is **index-driven by definition**.

Practical consequence:

- the production deblocker requires its matching index;
- Stage 2 will **not** build or evaluate a pixel seam-position detector;
- Stage 2 will **not** build Family B as a pixel-only control path.

Important nuance:

- this is a **scope / architecture decision**;
- it is **not** a proof that pixel-only deblocking is technically inferior.

### 6.2 Chroma ruling

Dave has separately ruled that **4:2:0 chroma deblocking is in scope on mechanism**.

Practical consequence:

- Stage 2 does **not** need a preliminary experiment whose purpose is merely to prove chroma
  blocking exists;
- instead Stage 2 must determine safe/effective chroma deblocking behaviour.

Important nuance:

- chroma remains experimental regarding threshold, strength, sample access, no-harm and benefit;
- chroma being "in scope" is a separate decision from the index-driven ruling.

### 6.3 Existing-filter yardstick

Dave explicitly decided to **avoid even the distraction** of using an optional existing external
filter as a yardstick.

Practical consequence:

- do **not** include an optional existing-filter comparison in the current plan;
- only revisit later if some very specific fallback need arises.

### 6.4 Stage 1 freeze

Stage 1 tooling is frozen for now:

- no Stage 1 code change is planned;
- do not reopen Stage 1 merely to add matrix values or extra metadata;
- only reopen if Stage 2 evidence later shows a concrete need.

---

## 7. Key technical findings already established

### 7.1 Luma transform-state geometry matters

For supported MPEG-2 frame pictures, indexed luma transform state is important.

Key states:

```text
FRAME
FIELD
NONE
```

Conceptually:

- `FRAME` means the mid-height luma seam exists;
- `FIELD` means that FRAME-style mid-height seam does not exist;
- `NONE` means no current coded residual transform seam is asserted.

The index therefore gives authoritative luma seam geometry.

### 7.2 Pixels still matter

Even though seam geometry is index-driven, the filter still must use decoded pixels to decide:

- whether a known seam actually looks like blocking;
- whether it is real picture detail instead;
- how much correction is safe.

So the production model is:

```text
index -> seam geometry / eligibility
pixels -> blocking-vs-detail / correction limiting
QP + strength -> correction control
```

### 7.3 Chroma findings (from Claude cold read / review trail)

Claude performed important reference-decoder cold reads.

Important verified findings include:

#### V1
Luma placement behaviour in the reference decoder for frame pictures.

#### V2
For MPEG-2 4:2:0, chroma transform placement does **not** follow luma `dct_type`.

#### V3
For MPEG-2 4:2:0 in the inspected reference decoder:

- chroma uses the same macroblock `quantizer_scale`;
- the decoder's 4:2:0 path uses the luma matrix-selection path.

Important evidence-level caution:

- this is VERIFIED for the inspected reference decoder implementation;
- do **not** silently upgrade it to a stronger normative claim unless separately verified.

#### V4
Claude later verified that, in the inspected reference decoder, for MPEG-2 4:2:0 field prediction
in frame pictures, chroma lines alternate field parity by line.

Important consequence:

- this supports the **premise** for same-field chroma access in interlaced cases;
- but whether the filter **uses** same-field chroma access remains a **design choice**, not an
  automatically ratified rule.

### 7.4 Chroma practical implication

Current intended first chroma model:

- native Cb/Cr planes;
- fixed 8x8 chroma transform geometry;
- effective indexed per-MB QP;
- no copying of luma FRAME/FIELD/NONE geometry into chroma placement.

### 7.5 Matrix handling

Observed:

- most real LG samples use a custom non-intra matrix;
- `TEST_2A_A001` is notable as a no-custom-matrix sample.

Current decision:

- record matrix presence as provenance;
- do **not** reopen Stage 1 to capture matrix coefficient values yet;
- only revisit if Stage 2 evidence shows matrix information is actually needed.

---

## 8. Stage 1 current status

Stage 1 is complete and accepted for current purposes.

### 8.1 Current Stage 1 capability

Stage 1 provides:

- index generation from MPEG-2 elementary stream;
- analyzer support;
- structural validation;
- frame-count correspondence;
- picture-type correspondence with BestSource;
- useful transform-state / QP / structure summaries.

### 8.2 Important Stage 1 evidence documents

Most important current Stage 1 evidence file:

- `Stage1_Evidence_and_Gate_Report_v0_3.md`
  - ratified

### 8.3 Stage 1 no-change note

Do not modify Stage 1 unless a future concrete problem requires it.

---

## 9. Samples and current sample roles

### 9.1 Main known samples

The following sample names have been important:

- `LG_576i_3_LP`
- `LG_576i_4_EP`
- `LG_576i_5_MLS`
- `TEST_4A_A003`
- `TEST_4A_A003_blocky`
- `TEST_2A_A001`
- `TEST_2A_A001_blocky`

### 9.2 Current proposed roles

These roles are the current intended direction, but should be finalised in the future Stage 2 v0.2.

#### Development / tuning

- `LG_576i_3_LP`

Reason:

- 720x576;
- real LG recorder sample;
- heavier real quantisation;
- substantial FRAME and FIELD populations.

#### Locked interlaced hold-outs

- `LG_576i_4_EP`
- `TEST_4A_A003` original
- `TEST_2A_A001` original

#### Progressive / control

- `LG_576i_5_MLS`

#### Secondary paired-reference / stress material

- `TEST_4A_A003_blocky`
- `TEST_2A_A001_blocky`

Important note:

- software `_blocky` transcodes are now secondary evidence, not primary architecture evidence.

### 9.3 Leading B-picture exclusion

Important Stage 2 review outcome:

- leading B pictures before the first I picture of a clip should be excluded from **quality
  evidence / tuning / visual assessment**;
- but they remain included for structural validation and robustness.

This should go into Stage 2 v0.2, not necessarily into repository `05_DECISIONS.md`.

---

## 10. Current Stage 2 intended shape

### 10.1 Current status

- `Stage2_Experiment_Design_v0_1.md` exists but reflects the older broader experiment.
- It is expected to be superseded by:
  - `Stage2_Experiment_Design_v0_2.md`
- v0.2 should be drafted **after** repository review and ratification.

### 10.2 Current intended v0.2 experiment direction

Expected broad shape:

#### Step 1
Unfiltered baseline.

#### Step 2
Indexed geometry + fixed/emulated QP.

Important current preference:

- use **per-clip median effective QP** as the fixed clip-wide QP control.

#### Step 3
Indexed geometry + real effective per-MB QP.

Purpose:

- isolate the value of real per-MB QP versus a fixed clip-wide QP.

#### Step 4
Kernel / threshold / strength development using indexed geometry and real QP.

#### Step 5
NONE policy experiment.

#### Step 6
Bounded chroma experiment.

Likely comparison shape:

```text
C0  unfiltered chroma
C1  chroma filter + fixed/emulated QP
C2  chroma filter + real indexed per-MB QP
```

#### Step 7
Generalisation / no-harm.

### 10.3 Important Stage 2 must-have from Claude reconciliation

A detector-free but important check still needed:

- a **spatial registration check** between index macroblock coordinates and the decoded BestSource
  pixel grid.

Reason:

- Stage 1 established temporal correspondence;
- Stage 2 still needs to cheaply verify index MB coordinates map correctly to the decoded image
  pixels.

This should be included early in Stage 2 as seam-map diagnostics.

---

## 11. Current evidence hierarchy for Stage 2

This was an important recent clarification.

### 11.1 Primary evidence

Real LG recorder material is primary product evidence.

That means:

- real LG visual judgement;
- seam-local diagnostics;
- no-harm / collateral-change diagnostics;
- consistency across recorder modes.

### 11.2 Secondary evidence

Software transcode pairs are secondary evidence.

Use them for:

- paired-reference numerical movement;
- support / corroboration.

Do **not** let them dominate the product decision.

### 11.3 No single magic metric

Do not assume one metric alone decides success.

---

## 12. Immediate current state at the time of handover

At the moment of this handover:

1. The current repository baseline has been confirmed from `REPOSITORY.zip`.
2. ChatGPT has drafted revised repository files:
   - `05_DECISIONS.md` draft 1.1
   - `06_DEBLOCK_CONCEPT.md` draft 1.1
   - `02_INDEX_FORMAT_SPEC.md` draft 0.4
3. These are packaged in:
   - `REPOSITORY_PROPOSED_UPDATE_2026-10-07.zip`
4. Those repository revisions **still need Claude cold review and then Dave ratification**.
5. `Stage2_Experiment_Design_v0_2.md` has **not** yet been drafted.
6. No Stage 2 code has been authorised.
7. No later repository versions than those drafts are known.

---

## 13. Immediate next recommended steps for a future ChatGPT chat

If a new ChatGPT chat is started, the safest next sequence is:

### Step A - orient on latest materials

Ask Dave for / use the latest versions of:

- `REPOSITORY_PROPOSED_UPDATE_2026-10-07.zip`
- `REPOSITORY.zip`
- `Claude_REVIEW_Reconciliation_After_Handover_v0_1.md`
- `Claude_REVIEW_OF_ChatGPT_Discussion_Brief_Index_Value_and_Chroma_Deblocking_v0_2.md`
- `Stage2_Experiment_Design_v0_1.md`
- `Stage1_Evidence_and_Gate_Report_v0_3.md`

If later versions exist by then, use the **latest versions only**.

### Step B - determine whether repository revisions were already reviewed/ratified

There are two possibilities.

#### Case 1: Claude has not yet reviewed the revised repository drafts

Then the next move is:

```text
Claude cold-reviews the revised repository drafts
    ->
Dave ratifies / amends
```

#### Case 2: repository revisions have already been reviewed and ratified

Then use the ratified updated repository documents as authority and proceed directly to:

```text
draft Stage2_Experiment_Design_v0_2.md
```

### Step C - if drafting Stage 2 v0.2

Ensure it reflects:

- index-driven architecture only;
- no pixel seam-position detector;
- no Family B;
- no external-filter yardstick;
- chroma in scope;
- LP as development material;
- EP / 4A / 2A as locked interlaced hold-outs;
- MLS as progressive/control;
- per-clip median fixed-QP control;
- leading B-picture exclusion from quality evidence;
- spatial registration check;
- V4-aware chroma discussion;
- staged luma/chroma/no-harm approach.

### Step D - review cycle

Then:

```text
ChatGPT drafts Stage2_Experiment_Design_v0_2.md
    ->
Claude reviews
    ->
Dave ratifies
```

Only after that should any Stage 2 implementation proceed.

---

## 14. Things a future ChatGPT chat must avoid

1. **Do not revive Family B / pixel detector** unless Dave explicitly reopens that decision.
2. **Do not add an external-filter yardstick** unless Dave explicitly asks for reconsideration.
3. **Do not treat review or handover docs as repository authority** if later ratified repository docs
   exist.
4. **Do not reopen Stage 1 casually** just to add more fields.
5. **Do not assume V3 is a stronger normative claim than it is**. It is reference-decoder verified.
6. **Do not copy luma FRAME/FIELD/NONE geometry into chroma placement**.
7. **Do not use outdated earlier proposal/review versions** when a later version exists.
8. **Do not start coding Stage 2** before the revised design is ratified.

---

## 15. Suggested starting prompt for a future ChatGPT chat

A future chat could be started with something like:

> We are continuing the MPEG-2 macroblock index / VapourSynth deblocking project.  
> Please first read:
> - `ChatGPT_Handover_To_Future_ChatGPT_MPEG2_Deblocking_Project_v0_1.md`
> - the latest repository zip / repository authority docs
> - the latest Claude review of the repository revision round
> - `Stage1_Evidence_and_Gate_Report_v0_3.md`
> - `Stage2_Experiment_Design_v0_1.md`
> Then confirm the current state, identify the next required action, and do not assume authority for
> any draft that has not yet been ratified.

---

## 16. Final summary

The project is now in a much clearer state than earlier.

The essential current direction is:

- the production deblocker is **index-driven**;
- Stage 2 will focus on **using authoritative index geometry**, not rediscovering it from pixels;
- **chroma deblocking is in scope**;
- Stage 1 is complete and frozen;
- repository revisions have been drafted but still need review / ratification;
- the next major document after repository ratification is:
  - `Stage2_Experiment_Design_v0_2.md`

That is the main handover message a future ChatGPT chat must preserve.

