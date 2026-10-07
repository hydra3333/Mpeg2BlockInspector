# Claude Handover to a Future Claude Chat - MPEG-2 Index-Driven Deblocker

**Filename:** `Claude_HANDOVER_TO_Future_Claude_Chat_v0_1.md`
**Version:** 0.1
**Date:** 2026-10-07 (Adelaide)
**From:** the original Claude chat on this project (reviewer/researcher role)
**To:** a fresh Claude chat taking over the same role
**Status:** Handover / orientation only. NOT project authority. Where this document and a named
authority file differ, the authority file wins. This document points to the authorities; it does
not replace them.

---

## 0. First actions for the new chat

1. Read this whole document.
2. Ask Dave to upload, as actual files (not summaries):
   - the **current repository set**: `05_DECISIONS.md`, `06_DEBLOCK_CONCEPT.md`,
     `02_INDEX_FORMAT_SPEC.md` - both the ratified versions and any pending drafts;
   - `Stage1_Evidence_and_Gate_Report_v0_3.md`;
   - the latest Stage 2 design (`Stage2_Experiment_Design_v0_1.md`, or v0.2 if it now exists);
   - `REFERENCE-mpeg2dec-src.zip` (pristine reference decoder) - needed for any source check;
   - `Mpeg2BlockInspector_src.zip` (frozen Stage 1 instrumented source + analyzer);
   - the latest Claude and ChatGPT review/handover documents listed in section 7;
   - ChatGPT's own handover document for its future chat, if Dave has it.
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
amends/ratifies -> ChatGPT proceeds. (Note: `05` D-23 recorded the opposite for the very first
repository drafting round; that conflict is flagged for fixing - section 8.)

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

## 4. Dave's rulings that shape everything (as of 2026-10-07)

| Ruling | Substance | Recorded where |
|---|---|---|
| Index-driven product (proposed **D-24**) | The production deblocker requires its matching index and takes luma seam geometry from it. Stage 2 will **not** build or evaluate a pixel-only seam-position detector or a pixel-only "Family B" deblocker. Pixels are still used to judge blocking vs genuine edge and to limit correction at known seams. A **scope decision, not an experimental finding**. | Pending draft `05` v1.1 |
| Chroma in scope (**R-A**, proposed **D-25**) | 4:2:0 chroma deblocking is in scope on mechanism (V2, V3 below). No need to prove chroma blocking exists first; Stage 2 must find threshold, strength, H/V treatment, interlaced access, no-harm. Kept separate from D-24. | Pending draft `05` v1.1 |
| Real recorder material primary (**R-B**) | Real LG recordings are primary evidence; the software `_blocky` transcodes are secondary/optional (paired-reference numerics only). | Claude review v0.2 (chroma brief); pending D-26 |
| Pause discipline (**R-C**) | Work pauses at review points until Dave gives an explicit go. No Stage 2 code before Stage 2 v0.2 is ratified. | Standing practice |
| Inspector frozen | Stage 1 inspector and analyzer v0.2 frozen unless evidence shows a defect. `mpeg2dec.c` deliberately not re-touched to shrink the diff. | Stage 1 gate report v0.3 |

Answers to Claude's questions, accepted by both reviewers (from
`ChatGPT_RESPONSE_TO_Claude_QUESTIONS_After_Handover_v0_1.md`; to be carried into Stage 2 v0.2):
LP = development clip; EP, 4A original, 2A original = locked hold-outs; MLS = separate progressive
path; fixed-QP control = **per-clip median effective QP**; custom matrix coefficients **deferred**
(unfreeze Stage 1 only on evidence); `progressive_frame = 1` -> frame-domain access; leading open-GOP
B pictures excluded from quality metrics (Claude suggested wording: "B pictures output before the
first I picture").

---

## 5. Authority files and their state

| File | Ratified version | Pending draft | Notes |
|---|---|---|---|
| `05_DECISIONS.md` | v1.0 (D-01..D-23) | **v1.1** in `REPOSITORY_updated.zip` (ChatGPT draft) | Decision authority (D-20) |
| `06_DEBLOCK_CONCEPT.md` | v1.0 | **v1.1** in `REPOSITORY_updated.zip` | Concept; K-01..K-09 ACCEPTED |
| `02_INDEX_FORMAT_SPEC.md` | v0.3 (constraints C-1..C-5 ratified; spec DRAFT/not frozen) | **v0.4** in `REPOSITORY_updated.zip` | Contents/packing frozen only at Stage 3 |
| `Stage1_Evidence_and_Gate_Report_v0_3.md` | RATIFIED (Stage 1 PASS) | - | Durable Stage 1 evidence summary; Appendix A keeps 2A summaries |
| `Stage2_Experiment_Design_v0_1.md` | draft, never ratified | v0.2 to be drafted by ChatGPT after repo update | v0.1 is built around the now-removed Family B ladder; supersede, do not patch |
| `MPEG2_Macroblock_Index_VapourSynth_Deblocking_Project_Proposal_v0_5.md` | controlling proposal for stage order (D-01) | optional update | Subordinate to repository files |

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
- Per luma macroblock (frame picture): 4 seam lines - 2 vertical and the macroblock top edge are
  fixed by the grid; only the **mid-height** horizontal seam depends on FRAME/FIELD. Same-field view
  of a FRAME seam: top field 6|8, bottom 7|9 (field centreline).
- **NONE** = no current coded residual transform geometry asserted; it does NOT mean no visible
  blocking (prediction propagates it).
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
| `Claude_REVIEW_Reconciliation_After_Handover_v0_1.md` | **latest substantive review**: exact `05`/`06`/`02` effects, carry-list for Stage 2 v0.2 |
| `show_source_clip_info.vpy` | test helper (Dave holds `_2`, `_EP_2`, `_MLS_2` variants) |

### 7.2 ChatGPT documents to request

`ChatGPT_HANDOVER_TO_CLAUDE_After_LG_EP_MLS_Review_v0_1.md`;
`ChatGPT_RESPONSE_TO_Claude_QUESTIONS_After_Handover_v0_1.md`;
`Stage1_Inspector_Instrumentation_Design_v0_3.md`; `Stage2_Experiment_Design_v0_1.md`;
ChatGPT's own future-chat handover (being drafted 2026-10-07).

### 7.3 Provenance only - not evidence

`Response_to_Claude_Index_Driven_Ruling_and_Revised_Stage2_Plan_v0_1.md` (written for a wrong
Claude chat). Anything produced by the **wrong Claude chat** on 2026-10-07 has no authority.

---

## 8. Open points Claude has raised that are not yet resolved

From `Claude_REVIEW_Reconciliation_After_Handover_v0_1.md` - check whether the pending drafts
(`05` v1.1, `06` v1.1, `02` v0.4) took them up:

1. D-11, D-17, D-18 superseded; D-15 amended; new D-24 (index), D-25 (chroma), D-26 (evidence
   hierarchy).
2. **D-08** still names a mandatory ground-truth baseline - real LG clips have none; restate.
3. **D-23** workflow line conflicts with the current ChatGPT-drafts workflow.
4. `06`: rewrite section 1 question; remove Family B (5, 8.2, 9.1-9.4); K-03/K-04 gain VERIFIED;
   add K-10 (V3) and K-11 (V4); O-06 amended **by meaning** (keep chroma strength/threshold/no-harm);
   O-10a/b withdrawn; O-01/O-02/O-13 become cross-check only; O-03 closed; O-07/O-08 partly answered;
   new O-14 progressive path.
5. `02`: replace the "index is provisional, see 06 9.4" pointer; name `progressive_frame` per picture
   among candidate contents.
6. **Spatial registration check (MUST, Stage 2):** Stage 1 proved temporal correspondence only. Verify
   index macroblock (x, y) sits on BestSource pixels at (16x, 16y): on LP, mean same-field step at the
   mid-height position should be larger for FRAME than FIELD macroblocks. Not a detector.
7. Optional existing-filter yardstick - Dave's call whether it fits his ruling.
8. Wording corrections to ChatGPT: same-field luma access is the D-09 design rule, not required by
   geometry; leading-B rule should use index-observable terms.

---

## 9. Pending task at the moment of handover

Dave uploaded **`REPOSITORY_updated.zip`** (2026-10-07 23:59): ChatGPT's drafts `05_DECISIONS.md`
v1.1, `06_DEBLOCK_CONCEPT.md` v1.1, `02_INDEX_FORMAT_SPEC.md` v0.4 (all PROPOSED), plus the ratified
Stage 1 gate report v0.3. Dave asked Claude to review and comment, but **not to respond until he
says so**. If this chat has ended, the new chat should:

1. confirm with Dave that the review is still wanted;
2. cold-review the three drafts against the ratified v1.0/v1.0/v0.3, the reconciliation review
   (section 8 list), V1-V4 and Dave's rulings;
3. verify `05` D-01..D-23 text is unchanged except where intentionally superseded/amended, and that
   superseded decisions are marked, not deleted (D-20);
4. check every repository file is US-ASCII + CRLF;
5. deliver `Claude_REVIEW_OF_ChatGPT_Repository_Drafts_v1_1_v0_1.md` (or similar) classified
   MUST / SHOULD / OPTIONAL / NO OBJECTION.

---

## 10. Probable next steps after that

1. Dave ratifies `05`/`06`/`02` (possibly after one amendment round).
2. ChatGPT drafts `Stage2_Experiment_Design_v0_2.md` (indexed-only ladder: unfiltered; indexed
   geometry + per-clip median QP; indexed geometry + real per-MB QP; kernel/threshold/strength
   development; NONE policy starting with N0; bounded chroma C0/C1/C2; generalisation/no-harm on
   hold-outs; spatial registration check; I/P/B and QP-112 reporting; evidence hierarchy declared in
   advance; leading-B exclusion; progressive path).
3. Claude reviews Stage 2 v0.2; Dave ratifies.
4. Stage 2 implementation in Python (D-03), one bounded step at a time, reviewed each step:
   read-only harness and seam-map diagnostics first.
5. Feasibility gate (Dave decides; no pre-set numeric pass threshold). Then Stage 3 (freeze `.idx2`),
   Stage 4 (inspector as minimal diff - largely done), Stage 5 (frame-identity proof), C++ scalar,
   API4 wrapper, AVX2 (proposal v0.5 section 3).

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
  represents the archive. Dave has not yet said which modes his VHS-C archive mainly uses - worth
  asking when Stage 2 weighting is set.
- When reviewing, check arithmetic (index size = 32 + N x (64 + MBs x 8); totals = N x MBs; pair
  counts) - it has caught real errors.
- Dave's memory profile may be available to the new chat; it records his working style and that
  Deblock4 is abandoned.

---

## 12. Change log

### v0.1 - 2026-10-07

- First handover from the original Claude chat, written at Dave's request as risk management
  against chat length limits.
