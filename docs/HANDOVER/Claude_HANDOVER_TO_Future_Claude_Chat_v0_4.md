# Claude Handover to a Future Claude Chat - MPEG-2 Index-Driven Deblocker

**Filename:** `Claude_HANDOVER_TO_Future_Claude_Chat_v0_4.md`
**Version:** 0.4 (supersedes v0.3)
**Date:** 2026-10-08 (Adelaide)
**From:** the original Claude chat on this project (reviewer/researcher role)
**To:** a fresh Claude chat taking over the same role
**Status:** Handover / orientation only. NOT project authority. Where this document and a named
authority file differ, the authority file wins. This document points to the authorities; it does
not replace them.

---

## 0. First actions for the new chat

Where Dave keeps things (his Windows machine):

- Active repository root:
  `E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock`
- Handovers:
  `E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock\docs\HANDOVER`
- Repository authority files:
  `E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock\docs\REPOSITORY`
- Test clips, indexes and logs: `...\VapourSynth-mpeg2Deblock\VHSC_samples`
- Inspector source: `...\VapourSynth-mpeg2Deblock\src\Mpeg2BlockInspector`
- Stage-1 analyzer: `...\VapourSynth-mpeg2Deblock\tools\Stage1_Inspector_Analyzer_v0_2.py`
- Visual Studio solution/project: `...\VapourSynth-mpeg2Deblock\vs\VapourSynth-mpeg2Deblock`
- Test scripts: `...\VapourSynth-mpeg2Deblock\TESTING`

The previous local tree under
`E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector`
is rollback/reference material only until restructure Gate C passes.

The new chat cannot see these folders; Dave uploads files from them.

1. Read this whole document.
2. Ask Dave to upload, as actual files (not summaries):
   - the **current repository set** (`REPOSITORY_RATIFIED_2026-10-08.zip` or later):
     `05_DECISIONS.md` v1.1, `06_DEBLOCK_CONCEPT.md` v1.1, `02_INDEX_FORMAT_SPEC.md` v0.4;
   - `Stage1_Evidence_and_Gate_Report_v0_3.md`;
   - `Stage2_Experiment_Design_v0_3.md` (ratified 2026-10-08) or any later version;
   - any Stage 2 code and run output produced so far (S2-I1 onwards);
   - `REFERENCE-mpeg2dec-src.zip` (pristine reference decoder) - needed for any source check;
   - `Mpeg2BlockInspector_src.zip` (frozen Stage 1 instrumented source + analyzer);
   - the latest Claude and ChatGPT review/handover documents listed in section 7;
   - ChatGPT's own latest handover document for its future chat, if Dave has it;
   - if the repository restructure is still incomplete, the latest migration runbook/review evidence.
3. Before doing any task, state which version of each authority file you are working from and
   ask Dave to confirm it is current. Do not assume.
4. Then pick up the **pending task** in section 9.

---

## 1. The project in one paragraph

Dave (developer, Adelaide; sole committer) is building an **MPEG-2-specific, index-driven
deblocking filter for VapourSynth (API4, C++ later, AVX2 target)** for his own LG DVD-recorder
captures of VHS-C home video (MPEG-2, 4:2:0, mostly interlaced PAL). A separate tool,
**Mpeg2BlockInspector** (the pristine MPEG-2 reference decoder plus minimal instrumentation),
parses the elementary stream and writes a per-frame, per-macroblock index. The deblocker reads
decoded frames from BestSource plus that index, so it knows authoritatively, per macroblock,
the quantiser and the luma transform organisation (FRAME/FIELD/NONE), instead of guessing
codec structure from pixels. This is a **new project**; it is NOT Deblock4 (abandoned by Dave
2026-08-26 - never propose resuming it).

---

## 2. Who does what

| Party | Role |
|---|---|
| **Dave** | Owner, final authority, ratifies everything, runs all builds/tests on Windows (Visual Studio 2026, ffmpeg, VapourSynth R81, BestSource), commits |
| **ChatGPT** (separate chat) | Primary drafter: designs, repository drafts, code, analyzer, reports |
| **Claude** (this role) | Independent reviewer and researcher: cold reviews against source (file:line) and evidence, prior-art research, reference-decoder verification, occasional small helper scripts (e.g. the `.vpy` checker) when Dave asks |

**Current workflow (confirmed 2026-10-07):** ChatGPT drafts -> Claude cold-reviews -> Dave
amends/ratifies -> ChatGPT proceeds. (`05` v1.1 D-23 is clarified to record this.)

Claude does not write production code unless Dave explicitly asks.

---

## 3. How Dave works (important - follow it)

- Values **independent, honest assessment over validation**. Disagree when warranted.
- **Distrusts assertion; wants verification cold against source with file:line.**
- **Strong aversion to summaries displacing the authorities they summarise.** Always ask for the
  real files; never treat a summary (including this one) as authority.
- **Every project document: US-ASCII, CRLF, mechanically verified after every emit.** Check with a
  script (all bytes < 128; zero bare LF) and report the result.
- **Versioning:** research/review files `AUTHOR_TOPIC_vX_Y.md` and
  `AUTHOR_REVIEW_OF_OTHER_TOPIC_vX_Y.md`; repository files carry no version suffix (version in
  header + change log); superseded copies go to `superseded/`.
- **Labels:** DECIDED / PROPOSED / AGREED / HYPOTHESIS / RESEARCHED / VERIFIED / OPEN.
  VERIFIED = Dave's test or a cold read of authoritative source. Never promote a design inference
  to VERIFIED.
- **Decisions presented as plain English: question / why / recommendation / options**, document
  references on a trailing line only. Plain English, not acronym-dense, when addressing Dave.
- Propose before transforming; before/after blocks with change IDs for edits.
- Prefers **hard abort over silent continuation** in code.
- No git staging in the build-test loop; he applies deliveries, tests, decides.
- Classify review findings as **MUST CHANGE / SHOULD CHANGE / OPTIONAL / NO OBJECTION**.
- Keep chat replies concise; put substance in the file.

---

## 4. Dave's rulings that shape everything (as of 2026-10-08)

| Ruling | Substance | Recorded where |
|---|---|---|
| Index-driven product (**D-24**, DECIDED) | The production deblocker requires its matching index and takes luma seam geometry from it. Stage 2 does **not** build or evaluate a pixel-only seam-position detector or a pixel-only "Family B" deblocker. Pixels are still used to judge blocking vs genuine edge and to limit correction at known seams. A **scope decision, not an experimental finding**. Supersedes D-11, D-17, D-18; amends D-15. | `05` v1.1 |
| Chroma in scope (**D-25**, DECIDED) | 4:2:0 chroma deblocking is in scope on mechanism (V2, V3 below). Stage 2 finds threshold, strength, H/V treatment, interlaced access, no-harm. Same-field chroma filtering stays an experimental design choice. | `05` v1.1 |
| Evidence hierarchy (**D-26**, DECIDED) | Real LG recordings are primary evidence; the software `_blocky` transcodes are secondary (paired-reference numerics only). | `05` v1.1 |
| No existing-filter yardstick | No external deblocker is part of the planned Stage 2 comparison (Dave, confirmed 2026-10-08). Revisit only on a specific need. | `05` v1.1 D-08 note; Stage 2 v0.3 section 3.6 |
| Pause discipline | Work pauses at review points until Dave gives an explicit go. Stage 2 code proceeds one increment at a time (S2-I1 first), each reviewed. | Standing practice; Stage 2 v0.3 section 22 |
| Inspector frozen | Stage 1 inspector and analyzer v0.2 frozen unless evidence shows a defect. | Stage 1 gate report v0.3 |

Stage 2 choices now fixed in the ratified design: LP = development clip; EP, 4A original, 2A
original = locked hold-outs; MLS = separate progressive/control; fixed-QP control = per-clip median
effective QP; matrix coefficients deferred; `progressive_frame` per picture selects the access mode;
B pictures output before the first I picture are excluded from quality evidence.

### 4.1 Repository / migration decisions now in force

These are migration/project-management decisions from Dave, not replacements for the technical
repository authorities above:

- one umbrella Git repository;
- GitHub repository renamed to `hydra3333/VapourSynth-mpeg2Deblock`;
- active local root:
  `E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock`;
- command-line tool remains named `Mpeg2BlockInspector`;
- `TESTING\` and `VHSC_samples\` remain at repository root;
- inspector source moved to `src\Mpeg2BlockInspector\`;
- analyzer moved to `tools\`;
- Visual Studio solution/project moved to `vs\VapourSynth-mpeg2Deblock\`;
- future Stage-2 Python will use `experiments\stage2\` when S2-I1 starts;
- eventual VapourSynth plugin creation is deferred until after the Stage-2 gate;
- Phase 2 does not retune the frozen inspector to copy CNR3 compiler/linker settings;
- later plugin / umbrella `.slnx` work requires a deliberate CNR3-based configuration audit;
- sample media remains tracked;
- new project development is AGPL version 3 or later;
- `VHSC_samples` recordings/media are excluded from that AGPL grant and are restricted by
  `NOTICE.md` to project-testing use;
- no Phase-2 push before Gate C unless Dave explicitly changes the decision.

Phase 1 / Gate B has passed. Phase 2 structural commits are complete through source/layout moves,
test-path repair, selective Python-cache ignores and `NOTICE.md`. Gate C has not yet passed at the
time of this handover.

---

## 5. Authority files and their state

| File | State | Notes |
|---|---|---|
| `05_DECISIONS.md` | **v1.1 RATIFIED 2026-10-08** (D-01..D-26) | Decision authority (D-20). D-11, D-17, D-18 SUPERSEDED; D-08, D-15 AMENDED; D-23 CLARIFIED |
| `06_DEBLOCK_CONCEPT.md` | **v1.1 RATIFIED 2026-10-08** | K-03, K-04 gain VERIFIED; K-07 revised; K-10 (V3), K-11 (V4) ACCEPTED; O-03 closed; O-10a/b withdrawn; O-14 added |
| `02_INDEX_FORMAT_SPEC.md` | **v0.4** (constraints C-1..C-5 ratified; spec DRAFT / not frozen) | Contents/packing frozen only at Stage 3. Candidates include `progressive_frame` and picture type |
| `Stage1_Evidence_and_Gate_Report_v0_3.md` | RATIFIED (Stage 1 PASS) | Durable Stage 1 evidence summary |
| `Stage2_Experiment_Design_v0_3.md` | **RATIFIED by Dave 2026-10-08** | Controls Stage 2. v0.1 and both v0.2 texts are superseded |
| `MPEG2_Macroblock_Index_VapourSynth_Deblocking_Project_Proposal_v0_5.md` | controlling proposal for stage order (D-01) | Subordinate to repository files |

Stage 1 file identities (SHA-256, verified by Claude against the reviewed source):
`getpic.c` e80239cf...0eca, `mpeg2dec.c` 8e6053cc...0b947, `Stage1_Inspector_Analyzer_v0_2.py`
8e0d5830...e02cda (full hashes in the gate report section 2.3).

---

## 6. Key technical knowledge (pointers, with evidence level)

### 6.1 Reference-decoder verifications by Claude (cold reads of `REFERENCE-mpeg2dec-src.zip`)

| ID | Finding | Source | Level |
|---|---|---|---|
| V1 | Luma frame-picture placement: field DCT = blocks by field, no mid-height seam; frame DCT = blocks at rows 0 and 8, seam between frame lines 7 and 8 | getpic.c 436-449 (`Add_Block`) | VERIFIED (implementation) |
| V2 | 4:2:0 chroma ignores `dct_type`: field path only if `dct_type && chroma_format != CHROMA420` | getpic.c 467-482 | VERIFIED (implementation) |
| V3 | All blocks of a macroblock, luma and chroma, use the same `quantizer_scale`; for 4:2:0 chroma the luma matrices are selected | getblk.c 274-276, 443-445 (matrix); 411, 563 (scale) | VERIFIED (implementation; not a normative H.262 claim) |
| V4 | 4:2:0 chroma lines alternate field parity in field prediction: even = top field, odd = bottom | recon.c 267-286, calls at 83-91 | VERIFIED (implementation). Same-field chroma *filtering* remains a design choice |

Other source facts used in Stage 1 design/review: output only via `Write_Frame()` at getpic.c 749
(end of sequence), 765 (B), 771 (delayed I/P); `progressive_frame` is swapped around the I/P
output (getpic.c 768-773) so record fields must come from the metadata slot; skipped macroblocks
carry stale `macroblock_type` (only INTRA cleared, getpic.c 896); dct_type read condition at
getpic.c 388-392; `coded_block_pattern` value 0 decodable (getvlc.h 250). Line numbers may drift
by one or two.

### 6.2 Geometry and semantics (in `06`)

- Processing model: **frame-owned, metadata-directed filtering with field-parity-aware sample
  access** (D-09). No separate-field deblocking pass.
- Per coded luma macroblock (frame picture): the macroblock edges and the internal vertical seam at
  x = 8 are the same for FRAME and FIELD; only the **mid-height** horizontal seam depends on the
  state (FRAME has it, FIELD does not). Same-field view of a FRAME seam: top field 6|8, bottom 7|9.
- **NONE** = no current coded residual transform geometry asserted; it does NOT mean no visible
  blocking (prediction propagates it). A NONE macroblock has **no internal seam in either
  orientation**; only its outer macroblock edges remain eligible (Stage 2 v0.3 section 1.4, N0).
  `06` v1.1 section 4.1 implicitly assumes a coded macroblock; a one-line note is owed there.
- The QP indexed for a NONE macroblock is the quantiser in force at that point, but it quantised
  nothing in that macroblock (Stage 2 v0.3 section 9.2). Boundaries touching NONE are reported
  separately.
- Support rule: a correction for one seam must not cross another known seam (FRAME MB: about 4
  same-field samples between edge and centreline; FIELD MB: 8; chroma block: 4 per field).
- Off-grid propagated blocking bounds any grid-based post-filter (report I/P/B separately, D-16).
- Effective QP stored by the index is the **derived** scale (proven: values match the non-linear
  table; linear values 26/30 only in the one `q_scale_type = 0` frame).

### 6.3 Sample material (all passed Stage 1 gates: VALID, frame counts = BestSource, I/P/B MATCH)

| Clip | Size | Scan | FIELD / FRAME / NONE | QP median (max) | Role |
|---|---|---|---|---|---|
| `LG_576i_3_LP` | 720x576 | interlaced | 52.7 / 23.0 / 24.3 % | 18 (112; 3.8% at 112) | Stage 2 development |
| `LG_576i_4_EP` | 352x576 | interlaced | 76.2 / 9.7 / 14.1 % | 14 (112) | hold-out (FIELD-heavy) |
| `TEST_4A_A003` | 720x576 | interlaced | 68.7 / 19.5 / 11.8 % | 14 (36); frame 298 is fpfd=1, linear QP | hold-out; formal Stage 1 pair |
| `TEST_2A_A001` | 704x576 | interlaced | 6.2 / 59.2 / 34.7 % | 12 (80); no custom matrices | hold-out (FRAME-heavy) |
| `LG_576i_5_MLS` | 352x288 | **progressive** | 0 / 85.4 / 14.6 % | 10 (62, linear) | progressive path, chroma, no-harm |
| `*_blocky` | as source | interlaced | mostly NONE | 62 constant | optional paired-reference stress only |

Custom non-intra matrices in 4A, LP, EP, MLS (not 2A). No field pictures in any clip. LP, EP, MLS
start with two leading B pictures (open GOP). Only single-sequence, undamaged clips tested.

### 6.4 Test harness Dave uses

`TEST_Mpeg2BlockInspector*.BAT`: ffmpeg `-c:v copy -an -f mpeg2video -` piped to
`Mpeg2BlockInspector.exe -b - -m <idx>`; then analyzer `summary`; then `vspipe` with
`show_source_clip_info_*.vpy` (written by Claude), which reads the index record headers and compares
picture types with BestSource `_PictType` frame by frame (`--arg "src=..." --arg "idx=..."`;
`SHOW_FIRST`, `MAX_DIFFS_SHOWN` constants). Lesson learned: a hardcoded source path once made a
"count check" silently test the wrong file - always have scripts print what they actually read.

---

## 7. Document map (latest versions)

### 7.1 Claude documents (this role)

| File | Status |
|---|---|
| `Claude_MPEG2_Deblocking_Prior_Art_v0_1.md` + `_addendum` | Stage 0 research, provenance |
| `Claude_REVIEW_OF_ChatGPT_MPEG2_Deblocking_Codec_Mechanics_v0_1.md` | provenance |
| `Claude_RESPONSE_TO_ChatGPT_REVIEW_OF_Claude_MPEG2_Deblocking_Prior_Art_v0_2.md` | provenance |
| `Claude_REVIEW_OF_ChatGPT_REFERENCE_vs_INTERIM_Source_Comparison_v0_1.md` | Stage 1 input |
| `Claude_REVIEW_OF_ChatGPT_Stage1_Inspector_Instrumentation_Design_v0_1.md` | Stage 1 input |
| `Claude_REVIEW_OF_Stage1_Patch_and_First_Run_v0_1.md` | Stage 1 evidence |
| `Claude_REVIEW_OF_Stage1_Evidence_and_Gate_Report_v0_2.md` | Stage 1 evidence |
| `Claude_REVIEW_OF_ChatGPT_Discussion_Brief_Index_Value_and_Chroma_Deblocking_v0_2.md` | **V1-V3, R-A, R-B** (v0.1 superseded) |
| `Claude_REVIEW_OF_LG_EP_MLS_Stage1_Runs_v0_1.md` | EP/MLS evidence and roles |
| `Claude_QUESTIONS_FOR_ChatGPT_After_Handover_v0_1.md` | **V4**, LP log verification, Q1-Q7 |
| `Claude_REVIEW_Reconciliation_After_Handover_v0_1.md` | exact `05`/`06`/`02` effects, carry-list for Stage 2 v0.2 |
| `Claude_REVIEW_OF_ChatGPT_Repository_Drafts_v1_1_v0_1.md` | review of 05 v1.1 / 06 v1.1 / 02 v0.4 drafts; all taken up before ratification |
| `Claude_REVIEW_OF_ChatGPT_Stage2_Experiment_Design_v0_2.md` | two MUST (NONE internal seams; registration check), four SHOULD; all taken up |
| `Claude_REVIEW_OF_ChatGPT_Stage2_Experiment_Design_v0_2_Revised_v0_1.md` | **latest review**: no objection; two SHOULD (GOP definition, QP meaning for NONE), both taken up in v0.3 |
| `show_source_clip_info.vpy` | test helper (Dave holds `_2`, `_EP_2`, `_MLS_2` variants) |

### 7.2 ChatGPT documents to request

`ChatGPT_HANDOVER_TO_CLAUDE_After_LG_EP_MLS_Review_v0_1.md`;
`ChatGPT_RESPONSE_TO_Claude_QUESTIONS_After_Handover_v0_1.md`;
`Stage1_Inspector_Instrumentation_Design_v0_3.md`;
`ChatGPT_Handover_To_Future_ChatGPT_MPEG2_Deblocking_Project_v0_3.md` or later.

### 7.3 Provenance only - not evidence

`Response_to_Claude_Index_Driven_Ruling_and_Revised_Stage2_Plan_v0_1.md` (written for a wrong
Claude chat). Anything produced by the **wrong Claude chat** on 2026-10-07 has no authority.

---

## 8. Open points

All points Claude raised up to 2026-10-08 on the repository files and the Stage 2 design were taken
up before ratification. What remains:

1. **`06` section 4.1 note (SHOULD, next `06` revision):** state that internal seams exist only for
   FRAME/FIELD macroblocks; NONE keeps macroblock-edge locations only.
2. **Stage 2 v0.3 tidy-up (OPTIONAL):** the copy Dave ratified still carries the header status
   "DRAFT READY FOR DAVE RATIFICATION", and sections 20, 21 and 22 still say "v0.2" in places. No
   effect on content; the repository copy should read RATIFIED.
3. **`05` D-09 wording (OPTIONAL):** it still says same-field access is used where the geometry
   "requires" it. Same-field access is the design rule against mixing fields, not a geometric
   requirement; `06` v1.1 section 2 already says this correctly.
4. Dave has not yet said which recorder modes his VHS-C archive mainly uses; worth asking when the
   Stage 2 gate weighs the hold-outs.

---

## 9. State at the moment of handover

**Done (2026-10-08):**

- Repository set ratified: `05` v1.1, `06` v1.1, `02` v0.4 (`REPOSITORY_RATIFIED_2026-10-08.zip`
  checked by Claude: only the expected status changes; US-ASCII, CRLF).
- `Stage2_Experiment_Design_v0_3.md` ratified by Dave after two Claude review rounds.
- Repository/GitHub migration decisions made: one umbrella repo, renamed
  `VapourSynth-mpeg2Deblock`, final active local root established.
- Phase 1 / Gate B passed: fresh VS2026 clone, frozen EOL/hash checks, Release x64 rebuild, warning
  comparison and LP baseline-index byte identity all passed.
- Phase 2 structural work completed through the separate commits for dead-project removal,
  source/analyzer/Visual-Studio relocation, TESTING path repair, Python-cache ignores and
  `NOTICE.md`.
- Current handover/path housekeeping is being completed before Gate C.

**No Stage 2 code exists yet.**

**Immediate next task:** finish Phase-2 restructure verification / **Gate C**. In particular, the
moved solution must be reopened in Visual Studio 2026 and rebuilt `Release | x64`; warning behaviour
must match baseline; all six tracked acceptance indexes must regenerate byte-identically; the
seventh blocky-2 case is path-only; regenerated logs must prove the new tree/VPY paths; and the old
local tree must remain untouched.

**After Gate C passes and Dave explicitly authorises coding:** ChatGPT implements **S2-I1 only**
(read-only Stage 1 index reader and validation; reproduce analyzer v0.2 summary totals for each
formal clip; `progressive_frame` and picture-type handling; leading-B exclusion accounting).
Dave runs it. Claude reviews the code and output before S2-I2.

---

## 10. Probable next steps after Gate C

Per Stage 2 v0.3 section 19, each increment is reviewed before the next:

1. **S2-I1** index reader and validation (above).
2. **S2-I2** seam-map diagnostics and the mandatory spatial registration check on LP: FRAME-minus-FIELD
   contrast with index labels shifted -1/0/+1 macroblock in x and y (must peak at zero shift), and
   the 8-pixel column grid-phase check (must peak at phase 0). A missing clear zero-shift peak is a
   stop condition. An 8-pixel horizontal offset would pass the phase check and show as an ambiguous
   contrast, not a clean wrong peak.
3. **S2-I3** initial luma kernel, fixed median QP, on even-numbered LP GOPs; freeze as K0. A GOP here
   is the display-order run from one I picture up to the next, numbered from 0 at the first I.
4. **S2-I4** K0 with fixed QP versus real per-macroblock QP on odd-numbered LP GOPs; no retuning;
   boundaries touching NONE and high-disparity QP boundaries (e.g. 112 next to 14) reported
   separately. The `_blocky` transcodes cannot inform this (QP 62 everywhere).
5. **S2-I5** kernel/threshold/strength development on LP with real QP. **S2-I6** NONE policy N0.
   **S2-I7** bounded chroma experiment. **S2-I8** locked hold-outs (EP, 4A, 2A originals; MLS
   control), no retuning. **S2-I9** transcode paired-reference reporting. **S2-I10** gate report,
   including which metadata the filter actually consumed.
6. Feasibility gate (Dave decides; no pre-set numeric pass threshold). Then Stage 3 (freeze `.idx2`),
   Stage 4 (inspector as minimal diff - largely done), Stage 5 (frame-identity proof), C++ scalar,
   API4 wrapper, AVX2 (proposal v0.5 section 3).

Things to watch when reviewing Stage 2 code: scripts must print the files they actually read; OFF
strength must be bit-exact; the support rule (no correction crossing another known seam) must hold
for FRAME (4 same-field samples), FIELD (8) and chroma (4 per field); hold-outs must not be viewed
during tuning.

Deferred/known gaps: field pictures (inspector refuses to publish, fail-safe); damaged streams;
multi-sequence clips; matrix-aware thresholds; final index packing; Stage 5 unique-frame identity.

---

## 11. Pitfalls and lessons

- **Wrong-chat incident (2026-10-07):** Dave once posted into the wrong Claude chat; its output
  conflicted with project history. If anything seems to contradict the authority files, stop and
  ask which chat/file it came from.
- Do not reconstruct files from memory or summaries; ask Dave to upload them. ChatGPT's handover
  explicitly declined to paraphrase a file it could not see - do the same.
- Updates to `06` open questions: change **by meaning, not by number** (O-06 has carried different
  meanings in different documents).
- A fixed-QP or "blocky" test sample can mislead: the ffmpeg `_blocky` transcodes have constant QP 62
  and are mostly NONE - useless for QP or geometry questions.
- Recorder modes differ sharply (EP half-width; MLS progressive SIF). Never assume one clip
  represents the archive.
- When reviewing, check arithmetic (index size = 32 + N x (64 + MBs x 8); totals = N x MBs; pair
  counts) - it has caught real errors.
- Dave's memory profile may be available to the new chat; it records his working style and that
  Deblock4 is abandoned.

---

## 12. Change log

### v0.4 - 2026-10-08

- Supersedes v0.3.
- Updates all operational paths to the active `VapourSynth-mpeg2Deblock` production repository.
- Separates inspector source, analyzer, Visual Studio, TESTING and VHSC sample locations explicitly.
- Records the settled one-repository/name/layout migration decisions.
- Records Phase 1 / Gate B PASS and current Phase-2 restructure state.
- Changes the pending task from immediate S2-I1 to Phase-2 Gate C.
- Records that S2-I1 follows only after Gate C passes and Dave explicitly authorises coding.
- Records later CNR3-based Visual Studio configuration-normalisation as deferred deliberate work.
- Records AGPLv3-or-later project-development licensing and the restricted `VHSC_samples` treatment
  stated in `NOTICE.md`.

### v0.3 - 2026-10-08

- Updated for the ratified repository set (`05` v1.1, `06` v1.1, `02` v0.4) and the ratified
  `Stage2_Experiment_Design_v0_3.md`: sections 0, 2, 4, 5, 6.2, 7, 8, 9 and 10 rewritten to the new
  state; next task is review of S2-I1.

### v0.2 - 2026-10-08

- Added Dave's folder locations; recorded the completed repository-draft review and its findings;
  updated section 9 (state) and section 10 step 1.

### v0.1 - 2026-10-07

- First handover from the original Claude chat, written at Dave's request as risk management
  against chat length limits.
