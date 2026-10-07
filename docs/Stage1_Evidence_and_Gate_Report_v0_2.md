# Stage 1 Evidence and Gate Report

**Filename:** `Stage1_Evidence_and_Gate_Report_v0_2.md`  
**Version:** 0.2  
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

### 1.3 Formal Windows acceptance pair

The formal Windows acceptance evidence now uses the exact pair named by `Stage1_Inspector_Instrumentation_Design_v0_3.md`:

```text
TEST_4A_A003.mpg
TEST_4A_A003_blocky.mpg
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

Accordingly, **the design-specified `TEST_4A_A003` pair passes the Stage 1 structural, semantic, count-correspondence and strengthened I/P/B-order correspondence checks.**

### 1.4 Additional corroborating pair

Before the formal pair was rerun, the same harness was exercised successfully on:

```text
TEST_2A_A001.mpg
TEST_2A_A001_blocky.mpg
```

That pair also produced:

- inspector exit code 0;
- analyzer v0.2 `VALID`;
- 300 Stage 1 records;
- 300 BestSource frames;
- 300 full-vspipe output frames;
- 300/300 per-frame I/P/B matches.

The `TEST_2A_A001` pair is therefore retained as useful corroborating evidence, but it is no longer needed to substitute for the design-specified acceptance pair.

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

### 2.2 Windows run evidence

Formal design-specified acceptance evidence:

- `TEST_4A_A003.log`
- `TEST_4A_A003_blocky.log`

These runs use the exact sample pair named by `Stage1_Inspector_Instrumentation_Design_v0_3.md`.

Additional corroborating evidence was previously produced for:

- `TEST_2A_A001.log`
- `TEST_2A_A001_blocky.log`

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

### 6.1 Formal count gate: design-specified pair

For `TEST_4A_A003.mpg`:

```text
Stage 1 index records        = 300
BestSource clip.num_frames   = 300
vspipe full output frames    = 300
```

For `TEST_4A_A003_blocky.mpg`:

```text
Stage 1 index records        = 300
BestSource clip.num_frames   = 300
vspipe full output frames    = 300
```

Thus the v0.3 correspondence-count gate passes for the exact design-specified pair.

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

For `TEST_4A_A003.mpg`:

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

For `TEST_4A_A003_blocky.mpg`:

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

The formal original/blocky pair therefore matches BestSource picture type at every tested output ordinal.

### 6.3 Additional corroborating pair

The earlier `TEST_2A_A001` / `_blocky` pair independently passed the same:

- 300-record index count;
- 300-frame BestSource count;
- 300-frame full-vspipe output count;
- 300/300 I/P/B equality.

This is supplementary evidence only; the formal gate is now satisfied by `TEST_4A_A003`.

### 6.4 What this correspondence result supports

The combined evidence now establishes substantially more than equal totals:

- no missing/extra output record is observed;
- no obvious I/P/B reorder displacement is observed;
- inspector output record ordinal and BestSource frame ordinal agree in picture type for all 600 positions of the formal pair;
- the same result was independently reproduced on the corroborating `TEST_2A_A001` pair.

This is strong Stage 1 evidence that:

> **For the tested frame-picture MPEG-2 samples, Stage 1 index record N corresponds to BestSource output frame N closely enough to support Stage 1 evidence interpretation and, once separately authorised, later-stage experimentation.**

### 6.5 What it does not prove

The I/P/B sequence is not a unique frame fingerprint.

A hypothetical displacement that happened to preserve the same picture-type pattern could evade this test.

Therefore this strengthened check:

- is stronger than count equality;
- is appropriate as a cheap Stage 1 gate;
- does **not** replace the deliberately deferred full Stage 5 frame-identity proof.

No Stage 5 requirement is silently closed by this result.

---

## 7. Common picture-level properties of the formal pair

Both `TEST_4A_A003` samples report:

```text
dimensions            = 720x576
macroblock grid        = 45x36
records/frames         = 300
picture_structure      = FRAME for 300/300 pictures
progressive_frame      = 0 for 300/300 pictures
top_field_first        = 1 for 300/300 pictures
repeat_first_field     = 0 for 300/300 pictures
custom intra matrices  = 0 frames
chroma matrix diff     = 0 frames
```

BestSource reports:

```text
Frames                 = 300
FPS                    = 25/1
Format                  = YUV420P8
```

The original sample reports a custom non-intra matrix in all 300 frames; the blocky sample reports no custom non-intra matrix.

Important terminology:

- `picture_structure = FRAME` means these are frame pictures;
- `progressive_frame = 0` means the coded pictures are not signalled as progressive frames;
- per-macroblock transform state `FIELD` is **not** a field picture.

The absence of field pictures means the first-pass design's deferred field-pair merge path was not required for the formal acceptance pair.

`repeat_first_field = 0` throughout also removes repeat-first-field cadence as a possible explanation for correspondence-count behaviour in these samples.

---

## 8. Formal original-versus-blocky evidence

The following is evidence gathering about the coded material, not a deblocking-quality conclusion.

### 8.1 Side-by-side summary

| Measure | `TEST_4A_A003` | `TEST_4A_A003_blocky` |
|---|---:|---:|
| Records | 300 | 300 |
| Dimensions | 720x576 | 720x576 |
| MB grid | 45x36 | 45x36 |
| I pictures | 26 (8.67%) | 26 (8.67%) |
| P pictures | 76 (25.33%) | 75 (25.00%) |
| B pictures | 198 (66.00%) | 199 (66.33%) |
| FRAME transform MBs | 94,741 (19.49%) | 56,235 (11.57%) |
| FIELD transform MBs | 333,986 (68.72%) | 35,243 (7.25%) |
| NONE transform MBs | 57,273 (11.78%) | 394,522 (81.18%) |
| INTER MBs | 426,204 (87.70%) | 316,290 (65.08%) |
| INTRA MBs | 42,224 (8.69%) | 46,078 (9.48%) |
| SKIPPED MBs | 17,572 (3.62%) | 123,632 (25.44%) |
| Mixed FRAME/FIELD frames | 299 (99.67%) | 300 (100.00%) |
| q_scale_type | 1 in 299 frames, 0 in 1 | 0 in all 300 |
| Effective QP | min 2, max 36, mean 14.455, median 14 | 62 for every MB |
| Macroblock Q updates | 175,480 (36.11%) | 0 (0.00%) |
| dct_type bits read | 427,107 (87.88%) | 91,478 (18.82%) |
| INTER CBP=0 with dct bit read | 0 | 0 |
| Custom intra matrices | none | none |
| Custom non-intra matrices | 300 frames | none |
| Field pictures | none | none |

Each sample contains:

```text
300 * 45 * 36 = 486,000 macroblocks
```

and the coding-state and transform-state totals each reconcile to that total.

### 8.2 Transform state by picture type

#### Original

```text
I:
  FIELD = 22,212 (52.74%)
  FRAME = 19,908 (47.26%)

P:
  FIELD = 88,494 (71.88%)
  FRAME = 27,084 (22.00%)
  NONE  = 7,542 (6.13%)

B:
  FIELD = 223,280 (69.61%)
  FRAME = 47,749 (14.89%)
  NONE  = 49,731 (15.50%)
```

#### Blocky

```text
I:
  FIELD = 9,422 (22.37%)
  FRAME = 32,698 (77.63%)

P:
  FIELD = 10,640 (8.76%)
  FRAME = 11,740 (9.66%)
  NONE  = 99,120 (81.58%)

B:
  FIELD = 15,181 (4.71%)
  FRAME = 11,797 (3.66%)
  NONE  = 295,402 (91.63%)
```

### 8.3 Neighbour-state counts

#### Original

```text
horizontal:
  FIELD-FIELD = 247,484
  FIELD-FRAME = 89,166
  FIELD-NONE  = 65,384
  FRAME-FRAME = 42,130
  FRAME-NONE  = 14,609
  NONE-NONE   = 16,427

vertical:
  FIELD-FIELD = 247,888
  FIELD-FRAME = 90,947
  FIELD-NONE  = 62,793
  FRAME-FRAME = 37,303
  FRAME-NONE  = 16,193
  NONE-NONE   = 17,376
```

#### Blocky

```text
horizontal:
  FIELD-FIELD = 13,042
  FIELD-FRAME = 12,717
  FIELD-NONE  = 29,362
  FRAME-FRAME = 34,998
  FRAME-NONE  = 28,259
  NONE-NONE   = 356,822

vertical:
  FIELD-FIELD = 13,718
  FIELD-FRAME = 9,949
  FIELD-NONE  = 27,437
  FRAME-FRAME = 32,798
  FRAME-NONE  = 29,295
  NONE-NONE   = 359,303
```

### 8.4 Original QP histogram

```text
2=124
3=1322
4=5631
5=13452
6=14483
7=8168
8=11965
10=24156
12=76430
14=121348
16=93593
18=51052
20=29408
22=16952
24=12004
26=1
28=5310
30=3
32=562
36=36
```

The blocky sample is:

```text
62=486000
```

### 8.5 Index-size observation

Both formal Stage 1 indexes are exactly:

```text
3,907,232 bytes
```

because the temporary format stores a fixed 8-byte payload for every macroblock:

```text
45 * 36 = 1,620 MB/frame
1,620 * 8 = 12,960 payload bytes/frame
12,960 + 64-byte record header = 13,024 bytes/frame
300 * 13,024 + 32-byte file header = 3,907,232 bytes
```

The source program-stream file sizes differ substantially:

```text
TEST_4A_A003.mpg         = 5,605,376 bytes
TEST_4A_A003_blocky.mpg  = 1,769,472 bytes
```

Thus the current Stage 1 index is about 69.7% of the original MPG size and about 221% of the blocky MPG size.

This is not treated as a defect. The Stage 1 binary format is deliberately fixed-width, redundant and disposable, optimised for evidence quality and validation rather than production storage efficiency. Final `.idx2` packing/compression remains outside Stage 1.

### 8.6 Evidence-level observations

Without turning these observations into Stage 2 design decisions:

1. Per-macroblock FRAME/FIELD mixture is common in the formal pair:
   - 99.67% of original frames contain both;
   - 100% of blocky frames contain both.

2. The original and blocky coding structures differ substantially:
   - skipped MB prevalence rises from 3.62% to 25.44%;
   - NONE rises from 11.78% to 81.18%;
   - FIELD falls from 68.72% to 7.25%;
   - FRAME falls from 19.49% to 11.57%.

3. The quantiser regimes differ strongly:
   - original is almost entirely `q_scale_type=1`, with effective QP 2..36;
   - blocky is entirely `q_scale_type=0`, with effective QP 62 for every macroblock;
   - blocky reports no macroblock quantiser updates.

4. The original uses a custom non-intra matrix throughout; the blocky sample does not.

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

**Result: PASS for the formal design-specified sample pair**

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

**Result: PASS**

For each design-specified `TEST_4A_A003` sample:

```text
index records = 300
BestSource frames = 300
full vspipe output frames = 300
```

The additional I/P/B comparison also matches all 300 positions per sample.

The earlier `TEST_2A_A001` pair independently corroborates the same result.

### 9.6 Section 34.6 - Semantic invariants

**Result: PASS**

Analyzer v0.2 reports `VALID` for both samples after the original invariants and Claude's additional checks.

No structural/semantic mismatch was downgraded to a mere statistic.

### 9.7 Section 34.7 - Evidence output

**Result: PASS for the formal design-specified pair**

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


---

## 10. What Stage 1 evidence now supports

The formal design-specified acceptance evidence supports the following working conclusions.

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

Because the substantive values and gate results have been captured in this report, the formal and corroborating run logs need not become repository knowledge artifacts.

The Stage 1 `.idx` files are also explicitly temporary-format artifacts. Whether to retain them through Claude's review is a convenience choice; they are reproducible from the source clips and frozen inspector.

---

## 13. Questions for Claude review

Claude is asked to review this report primarily for correctness and overclaiming.

Please address:

1. **Gate assessment:**  
   Do you agree that the current inspector/analyzer implementation has passed the structural and semantic gates for the design-specified `TEST_4A_A003` pair?

2. **Correspondence wording:**  
   Is the statement that 300/300 I/P/B equality provides strong Stage 1 output-order evidence, while not replacing Stage 5 identity proof, technically fair?

3. **Formal sample coverage:**  
   The exact `TEST_4A_A003` / `_blocky` pair named by v0.3 has now been run and passes all current gates. The earlier `TEST_2A_A001` pair is retained only as corroborating evidence. Do you see any remaining sample-coverage reason not to close Stage 1?

4. **Inspector freeze:**  
   Do you agree that no further inspector modification is justified by the current evidence?

5. **Evidence preservation:**  
   Have any material results from the disposable logs been omitted from this report?

6. **Overreach check:**  
   Does any conclusion in sections 10-11 claim more than the evidence supports?

No Stage 2 design review is requested in this cycle.

---

## 14. Proposed gate disposition for Dave after Claude review

If Claude finds no new blocking issue, proposed disposition:

> **Stage 1 implementation/evidence gate: PASS.**  
> The exact sample pair named by `Stage1_Inspector_Instrumentation_Design_v0_3.md` has passed the Windows build/run, structural validation, semantic validation, BestSource count correspondence and 300/300 I/P/B correspondence checks.  
> Freeze the current inspector and analyzer v0.2 as the Stage 1 evidence baseline.  
> Preserve this report as the durable Stage 1 evidence summary.  
> Treat the earlier `TEST_2A_A001` pair as supplementary corroborating evidence.  
> Full Stage 5 frame-identity proof remains deferred.  
> No Stage 2 work begins until Dave gives an explicit go.

---

## 15. Change log

### v0.2 - 2026-10-07

- Replaced the former sample-substitution qualification with formal acceptance evidence from the exact v0.3-design pair: `TEST_4A_A003.mpg` and `TEST_4A_A003_blocky.mpg`.
- Recorded both formal indexes as `VALID`, 300 records each, 720x576, 45x36 MB.
- Recorded BestSource 300-frame count equality and full-vspipe 300-frame output equality for both formal samples.
- Recorded 300/300 per-frame I/P/B correspondence matches for both formal samples.
- Updated original-versus-blocky transform, coding, QP, matrix and neighbour statistics to the formal pair.
- Recorded the fixed-width Stage 1 index-size observation: 3,907,232 bytes for each formal index, including why this can exceed the compressed MPG size.
- Reclassified the earlier `TEST_2A_A001` pair as additional corroborating evidence.
- Removed the obsolete need for Dave to ratify a sample substitution.
- Kept Stage 5 identity proof, field-picture support, final `.idx2`, and all Stage 2 design outside scope.

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
