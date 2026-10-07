# Stage 1 Evidence and Gate Report

**Filename:** `Stage1_Evidence_and_Gate_Report_v0_1.md`  
**Version:** 0.1  
**Date:** 2026-10-07  
**Drafted by:** ChatGPT  
**Status:** DRAFT FOR CLAUDE REVIEW AND DAVE RATIFICATION. Not project authority.  
**Scope:** Evidence consolidation and Stage 1 gate assessment only. No Stage 2 design is started or authorised by this document.

---

## 0. Purpose and authority

This document consolidates the evidence produced by the Stage 1 MPEG-2 inspector implementation and the Windows acceptance runs, and assesses that evidence against the accepted Stage 1 instrumentation design.

The normal repository authority remains:

- `05_DECISIONS.md`
- `06_DEBLOCK_CONCEPT.md`
- `02_INDEX_FORMAT_SPEC.md`

The implementation design used for this work is:

- `Stage1_Inspector_Instrumentation_Design_v0_3.md`

That design is a Stage 1 task/design document, not repository authority. This report is likewise an evidence/gate report, not repository authority.

This report deliberately does **not**:

- alter any repository decision;
- alter the frozen Stage 1 inspector;
- design Stage 2;
- freeze any final `.idx2` representation;
- claim the full Stage 5 frame-identity proof.

Dave has requested that further design work pause until an explicit go after Claude reviews this report.

---

## 1. Executive result

### 1.1 Implemented toolchain

The Stage 1 inspector implementation is credible and should remain frozen unless later evidence exposes a defect.

The accepted implementation characteristics are:

- pristine reference decoder used as the patch base;
- substantive C changes limited to `getpic.c` and `mpeg2dec.c`;
- no third source/header file required;
- Stage 1 metadata emitted in display/output order at the decoder's `Write_Frame()` events;
- safe temporary-file publication through `<index>.s1tmp`, renamed to the requested index only after successful finalisation;
- ffmpeg elementary-video stdin supported through `-b -`;
- Windows stdin forced to binary mode;
- Stage 1 output selected with `-m <file>`;
- analyzer performs structural, coverage and semantic validation before reporting statistics.

Claude's independent review of the patch concluded:

> The patch is correct and the run is credible. No blocking issues.

Claude also independently confirmed the two-file source footprint, hook placement, temporary binary layouts and the first sample's arithmetic consistency.

### 1.2 Analyzer baseline

`Stage1_Inspector_Analyzer_v0_2.py` is the current Stage 1 analyzer baseline.

v0.2 retains the v0.1 format/CLI handling and adds Claude's requested low-cost checks:

1. `INTRA -> transform != NONE`;
2. `INTRA -> effective CBP == 63`;
3. `INTER with effective CBP > 0 -> transform != NONE`;
4. in a frame picture with `frame_pred_frame_dct == 0`, `transform != NONE -> dct_type_bit_read`;
5. file summaries for `progressive_frame`, `q_scale_type`, `top_field_first`, and `repeat_first_field`.

The added checks were locally exercised against deliberately valid/invalid synthetic records before the Windows runs. Both real Windows sample indexes pass analyzer v0.2.

### 1.3 Executed Windows acceptance pair

The actual Windows acceptance evidence consolidated here is:

```text
TEST_2A_A001.mpg
TEST_2A_A001_blocky.mpg
```

For both samples:

- inspector exit code = 0;
- final Stage 1 index published;
- no `.s1tmp` remained after successful completion;
- analyzer v0.2 reports `VALID`;
- exactly 300 index records;
- BestSource reports exactly 300 frames;
- full `vspipe --container y4m ... NUL` run outputs exactly 300 frames;
- all 300 per-frame I/P/B picture types match between BestSource `_PictType` and Stage 1 index record order.

Accordingly, **the executed `TEST_2A_A001` pair passes the Stage 1 structural, semantic, count-correspondence and strengthened I/P/B-order correspondence checks.**

### 1.4 Important ratification item: sample-name substitution

`Stage1_Inspector_Instrumentation_Design_v0_3.md` explicitly names this acceptance pair:

```text
TEST_4A_A003.mpg
TEST_4A_A003_blocky.mpg
```

The Windows acceptance work actually used:

```text
TEST_2A_A001.mpg
TEST_2A_A001_blocky.mpg
```

This report does **not** silently assume those pairs are equivalent.

Therefore the most precise gate statement is:

> **PASS for the executed `TEST_2A_A001` pair. Formal closure of the v0.3 design's specifically named sample requirement is pending Dave's ratification that the `TEST_2A_A001` pair is an acceptable substitution, or a decision to run the named `TEST_4A_A003` pair as well.**

This is a test-evidence scope question, not an identified inspector defect.

---

## 2. Evidence set

The principal evidence used by this report is:

### 2.1 Design and implementation evidence

- `Stage1_Inspector_Instrumentation_Design_v0_3.md`
- `Stage1_Inspector_Source_Patch_v0_1.diff`
- `Stage1_Mpeg2BlockInspector_src_v0_1.zip`
- `Stage1_Inspector_Patch_Review_v0_1.md`
- `Claude_REVIEW_OF_Stage1_Patch_and_First_Run_v0_1.md`
- `Stage1_Inspector_Analyzer_v0_2.py`

### 2.2 Latest Windows run evidence

- `LATEST_RESULTS_2.zip`
  - `TEST_2A_A001.log`
  - `TEST_2A_A001_blocky.log`
  - `show_source_clip_info_2.vpy`
  - `show_source_clip_info_blocky_2.vpy`
  - `TEST_Mpeg2BlockInspector_2.BAT`
  - `TEST_Mpeg2BlockInspector_blocky_2.BAT`

The `.log` files are working evidence only. Dave has stated they need not be retained after analysis. The durable findings extracted from them are therefore recorded in this report.

### 2.3 File identities

The known SHA-256 identities for the current Stage 1 implementation/analyzer evidence are:

```text
getpic.c
e80239cfe73a0c04490a9bf131714861254ed1d7d095b052aac616a887ef0eca

mpeg2dec.c
8e6053ccb3a40be8c0d985f2e35124bf728d1f61df9b6d0c01b71e13e13b0947

Stage1_Inspector_Analyzer_v0_2.py
8e0d58305ee4fe518c25b67bdbe74acc4fb392486f23e6137862d916e5e02cda

LATEST_RESULTS_2.zip
4930d07418dcc298eba3b268856b9aab88135274768321e9d043d2fff151edda
```

These hashes identify the artifacts reviewed for this report; they do not create project authority.

---

## 3. Implementation review status

### 3.1 Mechanical source discipline

Claude's independent review against pristine source found:

- only `getpic.c` and `mpeg2dec.c` differ from pristine;
- the other 18 source/header files are identical after line-ending normalisation;
- line endings of the changed files match pristine;
- `getpic.c` instrumentation is additive;
- no third source/header file was required.

The reviewed hook placements include:

- Stage 1 picture metadata begin after reference-buffer rotation;
- picture coverage validation before output reordering;
- recovery marking at the decoder recovery path;
- per-macroblock recording after motion compensation and before MBA advance;
- effective-CBP capture only on successful macroblock decode;
- output-record emission at the three relevant `Write_Frame()` call sites.

This matches the approved metadata-slot/output-event design.

### 3.2 Optional diff reduction rejected as unnecessary churn

Claude noted one non-blocking opportunity to make the `mpeg2dec.c` stdin patch mechanically smaller by relying more directly on existing pristine `base.Infile != 0` guards.

The behaviour would be equivalent.

Because:

- the Windows build succeeds;
- stdin piping works;
- binary stdin handling is present;
- both accepted runs complete;
- indexes validate;
- no functional defect has been found;

there is no evidence-based reason to modify the inspector merely to reduce the diff.

**Recommendation: keep the current inspector frozen.**

### 3.3 Windows build

Dave rebuilt `Mpeg2BlockInspector`, Release x64, successfully:

```text
Rebuild All: 1 succeeded, 0 failed, 0 skipped
```

The build emitted legacy-reference-decoder warnings for old POSIX names/missing declarations and one linker warning that incremental linking was disabled because Release optimisation `/OPT:ICF` was active.

No warning identified a Stage 1 instrumentation failure, and the resulting executable successfully completed the acceptance runs.

The existing warnings are not a reason to broaden the source diff during Stage 1.

---

## 4. Safe index publication evidence

The Stage 1 writer first writes:

```text
<requested-index>.s1tmp
```

and only publishes the requested final index after successful completion.

For both executed samples:

- the old final index and old `.s1tmp` were removed before the run;
- the inspector returned exit code 0;
- the final `.idx` existed after completion;
- no `.s1tmp` remained.

Both final indexes were:

```text
3,820,832 bytes
```

For 300 frames at 704x576, the index arithmetic is:

```text
macroblocks/frame = 44 * 36 = 1,584

file size =
    32-byte file header
  + 300 * (64-byte record header + 1,584 * 8-byte MB payload)

= 3,820,832 bytes
```

The observed size therefore agrees exactly with the format and record count.

An orphan `.s1tmp` after a crash/forced termination remains deliberately invalid working state and is not accepted as an index.

---

## 5. Structural and semantic validation

Analyzer v0.2 reports `VALID` for both Windows indexes.

A `VALID` result means the analyzer accepted the file/header/record structure and the implemented Stage 1 cross-field invariants rather than merely printing plausible statistics.

The tested rules include the original v0.3 contract and the additional v0.2 rules requested by Claude.

No accepted sample produced:

- missing or duplicate macroblock coverage;
- non-contiguous output ordinal;
- unsupported field-picture publication;
- invalid stream/format flag;
- stale skipped-macroblock flag interpretation;
- quantiser-inheritance inconsistency;
- motion-source inconsistency;
- invalid dct-type-bit relationship;
- FRAME/FIELD/NONE contradiction;
- intra/CBP contradiction added in analyzer v0.2.

This is significant because the instrumented decoder is being trusted as an evidence producer only after these redundant checks agree.

---

## 6. BestSource correspondence evidence

### 6.1 Count gate

For `TEST_2A_A001.mpg`:

```text
Stage 1 index records        = 300
BestSource clip.num_frames   = 300
vspipe full output frames    = 300
```

For `TEST_2A_A001_blocky.mpg`:

```text
Stage 1 index records        = 300
BestSource clip.num_frames   = 300
vspipe full output frames    = 300
```

Thus the original v0.3 cheap correspondence gate passes for both executed samples.

### 6.2 Strengthened per-frame I/P/B check

At Claude's suggestion, the count check was extended without modifying the inspector.

The VapourSynth test script:

1. opens the Stage 1 index;
2. validates the 32-byte file header;
3. requires the file complete flag;
4. walks each 64-byte record header in ordinal order;
5. validates record magic, ordinal and record size;
6. extracts MPEG-2 `picture_coding_type`;
7. maps `1/2/3` to `I/P/B`;
8. reads BestSource `_PictType` for the corresponding VapourSynth output frame;
9. compares the sequences frame-by-frame.

For `TEST_2A_A001.mpg`:

```text
frames compared = 300
RESULT: MATCH - all 300 frames have the same picture type
```

Representative first 100-frame sequence:

```text
BestSource:
IBPBPBPBPIBPBPBPBPIBPBPBPBPIBPBPBPBPIBPBPBPBPIBPBPBPBPIBPBPBPBPIBPBPBPBPIBPBPBPBPIBPBPBPBPIBPBPBPBPI

Index:
IBPBPBPBPIBPBPBPBPIBPBPBPBPIBPBPBPBPIBPBPBPBPIBPBPBPBPIBPBPBPBPIBPBPBPBPIBPBPBPBPIBPBPBPBPIBPBPBPBPI
```

For `TEST_2A_A001_blocky.mpg`:

```text
frames compared = 300
RESULT: MATCH - all 300 frames have the same picture type
```

Representative first 100-frame sequence:

```text
BestSource:
IBBPBBPBBPBBIBBPBBPBBPBBIBBPBBPBBPBBIBBPBBPBBPBBIBBPBBPBBPBBIBBPBBPBBPBBIBBPBBPBBPBBIBBPBBPBBPBBIBBP

Index:
IBBPBBPBBPBBIBBPBBPBBPBBIBBPBBPBBPBBIBBPBBPBBPBBIBBPBBPBBPBBIBBPBBPBBPBBIBBPBBPBBPBBIBBPBBPBBPBBIBBP
```

The two samples have materially different GOP/picture-type patterns, yet each sample matches BestSource at every tested output ordinal.

### 6.3 What this correspondence result supports

The combined evidence now establishes substantially more than equal totals:

- no missing/extra output record is observed;
- no obvious I/P/B reorder displacement is observed;
- inspector output record ordinal and BestSource frame ordinal agree in picture type for all 600 tested frame positions across the two samples.

This is strong Stage 1 evidence that:

> **For the two executed 300-frame samples, Stage 1 index record N corresponds to BestSource output frame N closely enough to support Stage 1 evidence interpretation and, once separately authorised, later-stage experimentation.**

### 6.4 What it does not prove

The I/P/B sequence is not a unique frame fingerprint.

A hypothetical displacement that happened to preserve the same picture-type pattern could evade this test.

Therefore this strengthened check:

- is stronger than count equality;
- is appropriate as a cheap Stage 1 gate;
- does **not** replace the deliberately deferred full Stage 5 frame-identity proof.

No Stage 5 requirement is silently closed by this result.

---

## 7. Common picture-level properties of the executed pair

Both samples report:

```text
dimensions            = 704x576
macroblock grid        = 44x36
records/frames         = 300
picture_structure      = FRAME for 300/300 pictures
progressive_frame      = 0 for 300/300 pictures
top_field_first        = 1 for 300/300 pictures
repeat_first_field     = 0 for 300/300 pictures
custom intra matrices  = 0 frames
custom non-intra       = 0 frames
chroma matrix diff     = 0 frames
```

BestSource reports:

```text
Frames                 = 300
FPS                    = 25/1
Format                  = YUV420P8
```

Important terminology:

- `picture_structure = FRAME` means these are frame pictures;
- `progressive_frame = 0` means the coded pictures are not signalled as progressive frames;
- per-macroblock transform state `FIELD` is **not** a field picture.

The absence of field pictures means the first-pass design's deferred field-pair merge path was not required for these executed samples.

`repeat_first_field = 0` throughout also removes repeat-first-field cadence as a possible explanation for correspondence-count behaviour in these samples.

---

## 8. Original-versus-blocky evidence

The following is evidence gathering about the coded material, not a deblocking-quality conclusion.

### 8.1 Side-by-side summary

| Measure | `TEST_2A_A001` | `TEST_2A_A001_blocky` |
|---|---:|---:|
| Records | 300 | 300 |
| I pictures | 34 (11.33%) | 26 (8.67%) |
| P pictures | 133 (44.33%) | 75 (25.00%) |
| B pictures | 133 (44.33%) | 199 (66.33%) |
| FRAME transform MBs | 281,112 (59.16%) | 63,019 (13.26%) |
| FIELD transform MBs | 29,330 (6.17%) | 108,611 (22.86%) |
| NONE transform MBs | 164,758 (34.67%) | 303,570 (63.88%) |
| INTER MBs | 371,425 (78.16%) | 315,892 (66.48%) |
| INTRA MBs | 91,514 (19.26%) | 68,410 (14.40%) |
| SKIPPED MBs | 12,261 (2.58%) | 90,898 (19.13%) |
| Mixed FRAME/FIELD frames | 263 (87.67%) | 300 (100.00%) |
| q_scale_type | 1 for all frames | 0 for all frames |
| Effective QP | min 1, max 80, mean 16.534, median 12 | 62 for every MB |
| Macroblock Q updates | 106,447 (22.40%) | 0 (0.00%) |
| dct_type bits read | 310,442 (65.33%) | 171,630 (36.12%) |
| INTER CBP=0 with dct bit read | 0 | 0 |
| Custom matrices | none | none |
| Field pictures | none | none |

Each sample contains:

```text
300 * 44 * 36 = 475,200 macroblocks
```

and the coding-state and transform-state totals each reconcile to that total.

### 8.2 Transform state by picture type

#### Original

```text
I:
  FIELD = 13,077 (24.28%)
  FRAME = 40,779 (75.72%)

P:
  FIELD = 15,684 (7.44%)
  FRAME = 172,598 (81.93%)
  NONE  = 22,390 (10.63%)

B:
  FIELD = 569 (0.27%)
  FRAME = 67,735 (32.15%)
  NONE  = 142,368 (67.58%)
```

#### Blocky

```text
I:
  FIELD = 19,893 (48.30%)
  FRAME = 21,291 (51.70%)

P:
  FIELD = 40,308 (33.93%)
  FRAME = 22,626 (19.05%)
  NONE  = 55,866 (47.03%)

B:
  FIELD = 48,410 (15.36%)
  FRAME = 19,102 (6.06%)
  NONE  = 247,704 (78.58%)
```

### 8.3 Neighbour-state counts

These counts are preserved because the working logs are disposable and the neighbour statistics may be useful later.

#### Original

```text
horizontal:
  FIELD-FIELD = 15,175
  FIELD-FRAME = 25,437
  FIELD-NONE  = 1,511
  FRAME-FRAME = 226,401
  FRAME-NONE  = 69,177
  NONE-NONE   = 126,699

vertical:
  FIELD-FIELD = 16,903
  FIELD-FRAME = 23,620
  FIELD-NONE  = 1,233
  FRAME-FRAME = 228,283
  FRAME-NONE  = 66,355
  NONE-NONE   = 125,606
```

#### Blocky

```text
horizontal:
  FIELD-FIELD = 61,434
  FIELD-FRAME = 27,152
  FIELD-NONE  = 61,796
  FRAME-FRAME = 33,397
  FRAME-NONE  = 29,101
  NONE-NONE   = 251,520

vertical:
  FIELD-FIELD = 67,796
  FIELD-FRAME = 24,335
  FIELD-NONE  = 54,718
  FRAME-FRAME = 32,061
  FRAME-NONE  = 31,750
  NONE-NONE   = 251,340
```

### 8.4 Original QP histogram

The original sample's effective-QP histogram is preserved here:

```text
1=19
2=124
3=1169
4=6504
5=14586
6=26354
7=27959
8=63336
10=63927
12=45530
14=29046
16=17867
18=16570
20=17208
22=19915
24=38012
28=33295
32=22186
36=11479
40=6276
44=4622
48=3148
52=2155
56=1679
64=1061
72=750
80=423
```

The blocky sample is:

```text
62=475200
```

### 8.5 Evidence-level observations

Without turning these observations into Stage 2 design decisions:

1. Per-macroblock FRAME/FIELD mixture is common, not exceptional, in the executed material:
   - 87.67% of original frames contain both;
   - 100% of blocky frames contain both.

2. The blocky transcode's coding statistics are substantially different from the original:
   - skipped MB prevalence rises from 2.58% to 19.13%;
   - NONE rises from 34.67% to 63.88%;
   - FRAME falls from 59.16% to 13.26%;
   - FIELD rises from 6.17% to 22.86%.

3. The quantiser behaviour is also materially different:
   - original uses `q_scale_type=1` throughout with a broad derived-QP distribution;
   - blocky uses `q_scale_type=0` throughout and effective QP 62 for every macroblock;
   - blocky reports no macroblock quantiser updates.

4. No custom quantisation matrices occur in either executed sample.

These are Stage 1 codec-metadata observations only. They do not by themselves establish which deblocking rule or strength is best.

---

## 9. Assessment against `Stage1_Inspector_Instrumentation_Design_v0_3.md` section 34

### 9.1 Section 34.1 - Source-diff discipline

**Result: PASS**

Evidence:

- pristine base used;
- substantive C changes limited to `getpic.c` and `mpeg2dec.c`;
- no `global.h` or `store.c` change;
- no third source/header file;
- Claude independently checked the mechanical diff and hook placement.

### 9.2 Section 34.2 - Build/run

**Result: PASS for the executed Windows tests**

Evidence:

- Release x64 Windows rebuild succeeded;
- `-b -` successfully consumed ffmpeg elementary-video stdin;
- Windows stdin binary mode is present;
- `-m` produced final indexes;
- inspector returned 0 for both runs;
- Stage 1 data did not contaminate the binary input/output pipeline;
- successful runs published final indexes through the safe temporary-file path.

### 9.3 Section 34.3 - Supported-stream gate

**Result: PASS for the executed sample pair**

Evidence:

- both final indexes were published;
- analyzer reports both valid;
- 4:2:0 output is independently reported by BestSource as YUV420P8;
- all 300 picture structures in each sample are FRAME;
- no unsupported-stream/error flag is reported by the analyzer.

No field-picture implementation was needed for these samples.

### 9.4 Section 34.4 - File and coverage validation

**Result: PASS**

Evidence:

- final files close and publish cleanly;
- file sizes reconcile exactly;
- analyzer structural validation passes;
- per-picture macroblock counts are 44x36;
- totals reconcile for all 300 records;
- no coverage, unsupported-format or semantic validity failure was reported.

### 9.5 Section 34.5 - Early correspondence

**Result: PASS for the executed `TEST_2A_A001` pair; design sample-name substitution requires ratification**

For each executed sample:

```text
index records = 300
BestSource frames = 300
full vspipe output frames = 300
```

The additional I/P/B comparison also matches all 300 positions per sample.

The only unresolved point is that v0.3 names the `TEST_4A_A003` pair while the Windows evidence uses `TEST_2A_A001`.

### 9.6 Section 34.6 - Semantic invariants

**Result: PASS**

Analyzer v0.2 reports `VALID` for both samples after the original invariants and Claude's additional checks.

No structural/semantic mismatch was downgraded to a mere statistic.

### 9.7 Section 34.7 - Evidence output

**Result: PASS for the executed pair**

This report records the original-versus-blocky comparison required by the design, including:

- record/frame counts;
- I/P/B counts;
- FRAME/FIELD/NONE proportions;
- effective QP;
- coding-state proportions;
- mixed FRAME/FIELD prevalence;
- matrix occurrence;
- field-picture occurrence;
- neighbour-state counts.

Again, the literal v0.3 sample-name substitution remains a review/ratification point.

---

## 10. What Stage 1 evidence now supports

Subject to resolution of the sample-name substitution, the executed evidence supports the following working conclusions.

### 10.1 Inspector implementation

The current Stage 1 inspector is suitable to remain the frozen evidence-producing baseline for the tested frame-picture MPEG-2 4:2:0 scope.

No further inspector change is currently justified.

### 10.2 Temporary index validity

For the executed samples, the temporary Stage 1 index:

- is structurally self-consistent;
- has exactly-once macroblock coverage;
- obeys the implemented cross-field semantic invariants;
- publishes only after successful completion;
- records 300 output events corresponding in count to BestSource's 300 frames.

### 10.3 Output-order correspondence

For the executed samples, output ordinal correspondence is supported by two independent levels of evidence:

1. exact record-count equality;
2. exact 300/300 frame-by-frame I/P/B equality against BestSource `_PictType`.

This is sufficient Stage 1 evidence to interpret the metadata in output-record order for these samples.

### 10.4 Transform-state evidence

The instrumentation is producing plausible and internally consistent FRAME/FIELD/NONE distributions, and mixed transform geometry occurs extensively in both executed samples.

This supports preserving per-macroblock transform-state information as meaningful evidence.

It does not by itself decide later filtering behaviour.

### 10.5 Quantiser evidence

The instrumentation clearly distinguishes two very different real encoded quantiser regimes:

- nonlinear scale with varied effective QP in the original;
- linear scale with fixed effective QP 62 in the blocky sample.

This is strong evidence that the effective derived quantiser metadata is being captured in a form capable of distinguishing the intended stress sample from the original.

---

## 11. What Stage 1 has not proved

The following remain outside the conclusions of this report:

1. **Full Stage 5 frame identity.**  
   Matching I/P/B at every position is strong but not unique-picture identity.

2. **Field-picture handling.**  
   Both executed samples contain frame pictures only. Field-pair merge semantics remain deferred.

3. **Damaged-stream completeness beyond implemented guards.**  
   The accepted samples did not exercise every possible damaged-stream recovery path.

4. **All MPEG-2 profiles/levels/chroma/scalable modes.**  
   The temporary v1 scope is intentionally narrow.

5. **Final `.idx2` design.**  
   The Stage 1 8-byte-per-MB representation remains disposable research format.

6. **Production index size/compression.**  
   Not addressed.

7. **Final plugin/index-reader architecture.**  
   Not addressed.

8. **Any deblocking filter algorithm, kernel, strength or eligibility rule.**  
   Not addressed in this report.

9. **Stage 2 design.**  
   Explicitly paused pending a later go from Dave.

---

## 12. Artifact-retention recommendation

### Retain

At minimum, retain the durable Stage 1 implementation/review artifacts:

```text
Stage1_Inspector_Instrumentation_Design_v0_3.md
Stage1_Mpeg2BlockInspector_src_v0_1.zip
Stage1_Inspector_Source_Patch_v0_1.diff
Stage1_Inspector_Patch_Review_v0_1.md
Claude_REVIEW_OF_Stage1_Patch_and_First_Run_v0_1.md
Stage1_Inspector_Analyzer_v0_2.py
Stage1_Evidence_and_Gate_Report_v0_1.md
```

Retain the source test media needed to reproduce the evidence.

### Working evidence may be discarded after review

Dave has stated that the `.log` files need not be retained after analysis.

Because the substantive values and gate results have been captured in this report, the two run logs in `LATEST_RESULTS_2.zip` need not become repository knowledge artifacts.

The Stage 1 `.idx` files are also explicitly temporary-format artifacts. Whether to retain them through Claude's review is a convenience choice; they are reproducible from the source clips and frozen inspector.

---

## 13. Questions for Claude review

Claude is asked to review this report primarily for correctness and overclaiming.

Please address:

1. **Gate assessment:**  
   Do you agree that the current inspector/analyzer implementation has passed the structural and semantic gates for the executed `TEST_2A_A001` pair?

2. **Correspondence wording:**  
   Is the statement that 300/300 I/P/B equality provides strong Stage 1 output-order evidence, while not replacing Stage 5 identity proof, technically fair?

3. **Sample substitution:**  
   `Stage1_Inspector_Instrumentation_Design_v0_3.md` names `TEST_4A_A003` and `_blocky`, but Windows acceptance used `TEST_2A_A001` and `_blocky`.  
   - Is the `TEST_2A_A001` pair an adequate substitute for Stage 1 closure based on the evidence available?
   - Or should the named `TEST_4A_A003` pair also be run before Stage 1 is formally closed?

4. **Inspector freeze:**  
   Do you agree that no further inspector modification is justified by the current evidence?

5. **Evidence preservation:**  
   Have any material results from the disposable logs been omitted from this report?

6. **Overreach check:**  
   Does any conclusion in sections 10-11 claim more than the evidence supports?

No Stage 2 design review is requested in this cycle.

---

## 14. Proposed gate disposition for Dave after Claude review

### If Claude agrees the sample substitution is acceptable

Proposed disposition:

> **Stage 1 implementation/evidence gate: PASS.**  
> Freeze the current inspector and analyzer v0.2 as the Stage 1 evidence baseline.  
> Preserve this report as the durable Stage 1 evidence summary.  
> Full Stage 5 frame-identity proof remains deferred.  
> No Stage 2 work begins until Dave gives an explicit go.

### If Claude requires the named `TEST_4A_A003` pair

Proposed disposition:

> Keep the current inspector/analyzer frozen.  
> Run the same already-proven acceptance harness against `TEST_4A_A003.mpg` and `TEST_4A_A003_blocky.mpg`.  
> Update only this evidence report with those results.  
> Do not redesign the inspector unless the new run exposes an actual defect.

---

## 15. Change log

### v0.1 - 2026-10-07

- First consolidated Stage 1 evidence/gate report.
- Recorded the frozen two-file inspector implementation and analyzer v0.2 baseline.
- Consolidated both `TEST_2A_A001` Windows analyzer summaries.
- Recorded BestSource 300-frame count equality for both samples.
- Recorded full-vspipe 300-frame output equality for both samples.
- Recorded strengthened 300/300 per-frame I/P/B matches for both samples.
- Preserved side-by-side transform, coding, QP, matrix and neighbour-state statistics so disposable logs need not be retained.
- Explicitly identified the v0.3 `TEST_4A_A003` versus executed `TEST_2A_A001` sample-name divergence for Claude/Dave review rather than silently treating them as equivalent.
- Kept Stage 5 identity proof, field-picture support, final `.idx2`, and all Stage 2 design outside scope.
