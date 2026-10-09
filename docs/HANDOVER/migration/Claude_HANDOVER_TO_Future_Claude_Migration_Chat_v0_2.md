# Claude Handover to a Future Claude Migration Chat - VapourSynth-mpeg2Deblock

**Filename:** Claude_HANDOVER_TO_Future_Claude_Migration_Chat_v0_2.md
**Version:** 0.2
**Date:** 2026-10-09 (Adelaide)
**From:** the Claude migration-review chat
**To:** a fresh Claude chat continuing the same migration-review role
**Status:** Orientation only; NOT authority. Where this document and an authority file differ, the authority file wins. Always ask Dave for the actual files.

**Document taxonomy (agreed with ChatGPT and Dave on 2026-10-09; keep these apart):**

| Role | ChatGPT | Claude |
|---|---|---|
| 1. Migration continuity (chat to successor chat) | `ChatGPT_Migration_Chat_Handover_v0_*.md` | **this document**, `Claude_HANDOVER_TO_Future_Claude_Migration_Chat_v0_*.md` |
| 2. Migration-to-development handback (shared) | `MPEG2_Deblocking_Developer_Handback_v0_*.md` | same file |
| 3. Development continuity (owned by the development chats) | `ChatGPT_Handover_To_Future_ChatGPT_MPEG2_Deblocking_Project_v0_*.md` | `Claude_HANDOVER_TO_Future_Claude_Chat_v0_*.md` |

The migration chats do not edit role-3 documents unless Dave explicitly asks.

The Claude role-3 handover v0.4 was edited by migration ChatGPT. A v0.5 that I issued at Dave's request was **WITHDRAWN** the same day as a boundary crossing. Do not use it or commit it.

---

## 0. First actions for the new chat

1. Read this whole document.
2. Ask Dave to upload, as files:
   - the latest `Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_*.md` (v0.11 or later);
   - the latest `StageA_Visual_Studio_Normalization_Execution_Plan_v0_*.md` (v0.6 or later);
   - the latest `MPEG2_Deblocking_Developer_Handback_v0_*.md` (v0.5 or later; the common handback);
   - the latest `ChatGPT_Migration_Chat_Handover_v0_*.md` (v0.2 or later; ChatGPT's migration continuity handover);
   - the repository `README.md`, `NOTICE.md` and `LICENSE`;
   - any A3 review package (DRAFT or READY zip) issued after 2026-10-09 14:00;
   - the Claude documents in section 8 that the next task touches.
3. State which version of each file you are working from and ask Dave to confirm it is current.
4. Pick up the pending work in section 6.

---

## 1. Scope of this chat (Dave's original brief, verbatim intent)

- **The job:** a bounded migration chat. It plans and carries out moving the repository from GitHub `hydra3333/Mpeg2BlockInspector` (local `E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector`) to `hydra3333/VapourSynth-mpeg2Deblock` (local `E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock`). No Stage 2 deblocking design or code happens here.
- **Evidence:** "Verify against the files; cite file and line. Label anything you have not verified as unverified. Disagree with the proposal or the review where the evidence supports it."
- **Nothing destructive without Dave's explicit go:** no GitHub rename, no deletes, no history rewrite, no force push. Stop at each decision and each check.
- **The old local tree stays untouched** until the migrated one passes its checks.
- **Inspector source is frozen:** moving files is allowed, editing their content is not. Dave later amended this so that the inspector *project configuration* is in scope while the source stays frozen.
- **Scope has grown (all ratified by Dave):**
  - the umbrella `.slnx`;
  - the inspector project normalisation (Stage A);
  - a buildable VapourSynth DLL placeholder (Stage B, entry-point-only stub, no algorithm);
  - the canonical local build harness (Stage C);
  - the release-triggered GitHub workflow (Stage D);
  - the wheel/PyPI packaging scaffold (Stage E);
  - the common Developer Handback.
- **Documents:** any document Claude produces is US-ASCII with CRLF line endings, checked by script after every write, and named `Claude_<TOPIC>_vX_Y.md`. Repository files such as `README.md` keep their required names. Keep chat replies short and put the detail in the file.
- **Close-out:** when the migration finishes, Dave needs a short summary of the final layout and every path that changed, to take back to the development chats.
- **Licence wording:** at the end use "version 3 or any later version" (AGPL).

---

## 2. Workflow and how Dave wants things

- **Roles.** ChatGPT (separate chat) drafts the migration mechanics, documents and candidates. Claude cold-reviews each substantive step. Dave decides, ratifies, runs everything on Windows and commits.
- **Review findings** are classed MUST / SHOULD / OPTIONAL / NO OBJECTION, with file:line evidence and scripted checks.
- **Decisions** are put to Dave in plain English as question / why / recommendation / options, usually as a small table, with Claude's recommendation first.
- **Dave's standing cautions:**
  - "careful of version numbers, they change all the time": discover tools with vswhere, never hard-code `18\Community`, and do not pin the SDK;
  - he fears "losing good hard-earned settings" from CNR3, hence the subtractive, dual-pass audit;
  - **no-defaults ruling (2026-10-09):** "we should not rely on default behaviours for settings since microsoft are well known for fiddling with things in their releases".
- **Delivery.** When Dave asks for a response for ChatGPT, give a paste-ready note or a `Claude_RESPONSE_TO_ChatGPT_...` file.

---

## 3. Repository and paths (current)

- Active repository: `E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock` (GitHub `hydra3333/VapourSynth-mpeg2Deblock`).
- Inspector source (frozen): `src\Mpeg2BlockInspector\` (16 `.c`, 4 `.h`).
- Analyzer (frozen): `tools\Stage1_Inspector_Analyzer_v0_2.py`.
- Solution and project: `vs\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock.slnx` and `Mpeg2BlockInspector.vcxproj` (with `.filters`; `.vcxproj.user` is ignored).
- Test scripts: `TESTING\` (7 BATs and 7 VPYs; all 7 BATs are tracked). The BATs call `...\vs\VapourSynth-mpeg2Deblock\x64\Release\Mpeg2BlockInspector.exe` (line 6 of each) with `-b - -m <index>`.
- Test media and indexes: `VHSC_samples\` (restricted use; see NOTICE).
- Handovers: `docs\HANDOVER\` (migration documents under `docs\HANDOVER\migration\`). Repository authorities: `docs\REPOSITORY\`.
- Recovery tag: `pre-stageA-vs-normalization`.

---

## 4. State at handover (2026-10-09, about 14:10 Adelaide)

### 4.1 Done

- **Phase 1/2 restructure and path migration:** complete. See `Claude_Migration_Final_Summary_v0_1.md` (layout and paths at that time).
- **A1** (Win32 removal, deletions only): commit `d38d56d697107e7409f4baa7753bfb31b8d94747`. Project SHA-256 `87acd9ad...7a57`; numstat 0 insertions, 58 deletions.
- **A2** (`.sln` replaced by an x64-only `.slnx`): commit `837df123ebfe0fa083fec9d6de8969bd180f9ac0`. `.slnx` SHA-256 `fa24efcd...0754`. It loads in VS2026 without a rewrite.
- **Pre-A3 checkpoint:** PASS. Details:
  - toolchain (records, not pins): MSBuild 18.10.1.42706, v145, VC tools 14.51.36231, host HostX86\x64, SDK 10.0.28000.0 (unpinned);
  - Debug: 20 warnings (the 17 Release warnings, plus C4013 `strcat` at spatscal.c line 91 and store.c line 217, plus LNK4075 from /ZI with /INCREMENTAL:NO). Release: 17, matching the baseline;
  - exe SHA-256: Debug `66be0a77...8bb9`, Release `d31fbad8...c6f8`;
  - all six indexes byte-identical. Proved twice: by SHA-256, and by a clean `git status` after cleanup that restored only `.log` files;
  - frozen source unchanged against the tag;
  - `dumpbin` M3 baseline: PE32+, Large Address Aware, High Entropy VA, Dynamic Base, NX; no CET flag; CFG not fully enabled; Release imports VCRUNTIME140, the UCRT api-set DLLs and KERNEL32.

### 4.2 Ratified decisions (Dave, 2026-10-09)

- **D1:** Release adopts /GL and /LTCG. The /O2 components (/Oi /Ot /Ob2 /GF /Gy) are pins, not changes.
- **D2:** the Windows SDK stays unpinned; every gate records the SDK used. With /MT this is shipped-artefact provenance.
- **D3:** Debug uses CNR3's Speed, AnySuitable and Intrinsics settings.
- **D4 = NO:** Release /MT is consolidated into A3; there is no A4. Dave accepted the attribution risk. If an index fails, follow the documented uncommitted bisect order.
- **D5 = YES:** the plugin DLL uses /MT, with "hybrid" as a documented fallback only.
- **D6 = YES:** Release uses `/PDBALTPATH:%_PDB%`.
- **CPU/security policy:**
  - x64 + **AVX2 minimum** for both projects, Debug and Release; pre-AVX2 CPUs are unsupported. Dave accepts that budget non-AVX2 CPUs are irrelevant for VapourSynth.
  - **/GS, CFG, CET and Spectre are ON.** Do not trade security for speed.
  - Release uses `/favor:blend`.
  - **/sdl:** OFF for the inspector only, as the frozen reference-decoder exception; ON for the plugin.
- **One build route.** The `.vcxproj` and `.slnx` are the source of all settings. The Stage C harness (vswhere + MSBuild on the `.slnx`) is used locally, and Stage D CI calls that same harness. CI never injects flags or overrides the toolset; it fails if v145 or the Spectre libraries are missing.
- **Standalone Release artefacts.** Their imports must contain none of `VCRUNTIME*`, `MSVCP*`, `api-ms-win-crt-*`, `ucrtbase*`, `CONCRT*`, `VCOMP*`, `MSVCR1*`. Do not use a bare `MSVCR*`, which would also match the system `msvcrt.dll`. The allowed set is currently `KERNEL32.dll`.
- **Licence:** AGPL-3.0-or-later; NOTICE stays the legal and test-media boundary. The wheel must not copy CNR3's `License: MIT`.

### 4.3 Superseded candidates (history only; never apply)

- A3 v0.1 (`a86ec5b5...`).
- A3 v0.2 DRAFT (`a59788b4...108a`).
- A3 v0.3 DRAFT (`d7c6085f...1567`, which carried SSE2 and security OFF). I never saw its contents, only its hash in plan v0.5.

---

## 5. Latest documents at handover

| Document | Version | Claude review state |
|---|---|---|
| Design Record (DR) | v0.11 | **Reviewed** (taxonomy review). M7 and S12-S15 still not carried; boundary wording B1 and B2. |
| Stage A Execution Plan | v0.6 | **Reviewed** (taxonomy review). Only the README guard was added; M7 and S12-S15 are still missing. |
| Common Developer Handback | v0.5 | **Reviewed** in the taxonomy review: MUST H1 (runtime ownership rule) and H2 (project-file change control); SHOULD H3-H9. |
| ChatGPT migration handover | v0.2 | **Reviewed** in the taxonomy review: add the missing DR v0.10 review; fix the naming of Claude's handovers. |
| ChatGPT development handover | v0.4 | Role 3; not migration's to review or edit. |
| README.md | Claude draft of 2026-10-09 | Written by Claude at Dave's request. |
| NOTICE.md | unchanged | Checked. No change needed. |

---

## 6. Pending work and open items (pick up here)

0. **Taxonomy review outcomes** (`Claude_REVIEW_OF_ChatGPT_Migration_Docs_and_Handover_Taxonomy_v0_1.md`, section 7):
   - **Root cause of the missing M7:** `Claude_REVIEW_OF_ChatGPT_DR_v0_10_and_StageA_Plan_v0_5_v0_1.md` was missing from Dave's migration folder, so ChatGPT never saw it.
   - **Check that the following were taken up:**
     - the handback MUSTs H1 and H2, and SHOULDs H3-H9;
     - the DR boundary wording B1 and B2;
     - the naming of Claude's handovers;
     - the withdrawal of the role-3 v0.5.
1. **M7 and S12-S15 are not yet carried.** A grep of DR v0.11 and plan v0.6 finds no MSB8040, /fp:contract, per-configuration security statement or timing item:
   - **M7:** treat MSB8040 (missing Spectre libraries) as a hard failure; prove the Spectre libraries were used (LibraryPath, or `link /VERBOSE:LIB`); add the Spectre component to vswhere `-requires`. The component ID needs verifying; I believe it is `Microsoft.VisualStudio.Component.VC.Runtimes.x86.x64.Spectre`.
   - **S12:** state the security settings per configuration (recommended: both Debug and Release).
   - **S13:** find the XML property names by setting them in a scratch project and reading the `.vcxproj`.
   - **S14:** the gate confirms /fp:contract is absent.
   - **S15:** time the LP clip before and after A3, for information only.
   - **O7** (/favor:blend in Debug too) and **O8** (/guard:ehcont for the plugin) are also open.

   Check these in the next DR/plan or A3 package.
2. **README commit timing.** DR v0.11 and plan v0.6 say the README "has already been updated" and treat its claims as target policy until A3 passes. Claude's advice was to commit it **with or after A3**, never before. Confirm with Dave or ChatGPT whether it was committed. If it was, the published README currently overstates the build (AVX2, standalone runtime, Spectre).
3. **Superseding A3 package.** Expect a DRAFT, then a READY zip with logs, tlogs, dumpbin output and the regenerated 113-row reconciliation. Check:
   - insertions-only against A1, plus the deliberate changes;
   - every pin against the checkpoint tlogs;
   - the CNR3 EnableEnhancedInstructionSet rows (self-test lines 83 and 112, DLL lines 92 and 121) are now REUSE UNCHANGED;
   - the post-A3 gate: HostX64 paths, the command-line delta, dumpbin with CET and CFG now ON, the standalone import rule, warnings by code/file/line, frozen-source proof, all six indexes, README consistency.
4. **Reviews owed:** DR v0.11, plan v0.6 and Handback v0.4, when Dave asks.
5. **Stage B decisions to put to Dave**, as one coupled set:
   - the names: folder, project, DLL, plugin identifier, namespace, VapourSynth autoload folder `vapoursynth/plugins/<name>/`, and the PyPI/package name;
   - the stub type (recommended: entry-point only);
   - the C++ standard;
   - the vendored header release and API minor;
   - an optional CPU check in the plugin;
   - /guard:ehcont.

   The method: start from a byte copy of `cnr3.vcxproj`, so the diff is the audit record, then apply the subtractive dual pass. Release /MT, /PDBALTPATH, AVX2, /sdl ON and the security set apply from the start. COMDAT is to be compared, not inherited; its provenance in CNR3 is disputed.
6. **Stages C, D and E**, then close-out:
   - update `Claude_Migration_Final_Summary_v0_1.md` (layout and every changed path);
   - review the final common handback;
   - make sure every Claude review document is committed by name or deliberately removed.

---

## 7. Key technical facts (all verified unless marked otherwise)

### Inspector

- **Frozen-source constraints.** SDL OFF and `_CRT_SECURE_NO_WARNINGS` are needed: there are 34 classic CRT calls (for example getpic.c lines 179-181). No source file tests `_DEBUG`, `NDEBUG` or `_CONSOLE`; only `_WIN32` is used (mpeg2dec.c lines 36 and 102). There is no TCHAR or windows.h use, and no setjmp, longjmp or asm.
- **The index:**
  - `-m <file>` selects index output (mpeg2dec.c lines 455-466) and suppresses picture output;
  - the index is written to `<index>.s1tmp` and renamed only on success (getpic.c lines 179-183 and 238-239);
  - exit code 0 means success, 1 means failure (mpeg2dec.c lines 178-192);
  - the index is deterministic: no time, path or environment data;
  - the reference IDCT (double precision) is used only with `-r` (mpeg2dec.c line 497, getpic.c line 1421). The tests do not pass `-r`, so the index path is integer.
- **Baselines (SHA-256):**
  - getpic.c `e80239cf...0eca`;
  - mpeg2dec.c `8e6053cc...0947`;
  - analyzer `8e0d5830...2cda`;
  - original exe `3edb7147...` (historic; expected to change).
- **Six gated indexes** (authority: the tracked `.idx` files in git):

  | Index | SHA-256 |
  |---|---|
  | TEST_2A_A001 | `AFE51F25...9273` |
  | TEST_2A_A001_blocky | `CBF6E872...9288` |
  | TEST_4A_A003 | `5B989CED...9A65` |
  | LG_576i_4_EP | `11B42AAD...FA87` |
  | LG_576i_3_LP | `849b6a9c411a7db837268af3ac54501a06f5f1158e68d5245ce2b3ec40a0d011` (2,656,928 bytes) |
  | LG_576i_5_MLS | `378980EA...D7F` |

  The seventh script, `_blocky_2`, gives a path-only check; its index is untracked and not gated.

### MSVC (labelled as in the reviews)

- /O2 equals `/Og /Oi /Ot /Oy /Ob2 /GF /Gy`. ChatGPT confirmed this against current Microsoft documentation.
- Release C4013 is absent because of /Oi (Claude's inference).
- MSB8040 is a warning, not an error (Claude, unverified on v145).
- /fp:precise does not contract to FMA without /fp:contract in VS2022 and later (unverified for v145).
- CETCOMPAT may have no stable XML property (ChatGPT); settle it empirically (S13).
- The library search path reaches link.exe through the LIB environment variable, not the command line.

### CNR3 facts (from vapoursynth-cnr3-main)

- The CI workflow `.github/workflows/build-windows-x64-release.yml` compiles through a hand-written `cl` flag map (lines 88-128) with /MD and /arch:AVX2, not MSBuild. It builds a `py3-none-win_amd64` wheel with layout `vapoursynth/plugins/cnr3/cnr3.dll` (lines 165-257), and its metadata says `License: MIT` (line 198).
- The local `1.BUILD.bat` uses vswhere and MSBuild on `cnr3.slnx`.
- The CI comment claims the "windows-latest = WS2025 + VS2026 (v145)" runner image (lines 17-18). That is a dated claim; re-verify it at Stage D.

### The script

- `phase2_byte_path_edit.py` (SHA-256 `334aca05...c926`) was used for the Phase 2 path edits. It edits bytes exactly, counts its edits, is all-or-nothing, and is a dry run unless `--apply` is given.

---

## 8. Claude document map (this chat; all US-ASCII/CRLF verified)

**Audit and summaries:**
- `Claude_Pre_Migration_Audit_Findings_v0_1` to `v0_4`
- `Claude_Migration_Phase1_Summary_v0_1`
- `Claude_Migration_Final_Summary_v0_1` (needs updating at close-out)
- `Claude_Inspector_vs_CNR3_Settings_Comparison_v0_1`

**Reviews:**
- `Claude_REVIEW_OF_ChatGPT_D-B_VS2026_Clone_Refinement_v0_1`
- `Claude_REVIEW_OF_ChatGPT_Runbook_v0_3_and_D-C_Design_Record_v0_1`, `v0_2`
- `Claude_REVIEW_OF_ChatGPT_Phase2_Restructure_Next_Steps_v0_1`
- `Claude_REVIEW_OF_ChatGPT_Phase2_Execution_Runbook_v0_1`
- `Claude_REVIEW_OF_ChatGPT_Stage_A_B_VS_Plan_v0_1` to `v0_4`
- `Claude_REVIEW_OF_ChatGPT_Handback_v0_1_and_Design_Record_v0_5_v0_1`
- `Claude_REVIEW_OF_ChatGPT_StageA_Audit_Proposal_v0_1`, `v0_2` (v0.2 records D1-D3)
- `Claude_REVIEW_OF_ChatGPT_StageA_Checkpoint_Status_v0_1`
- `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_2_Package_v0_1` (M3, S7-S9)
- `Claude_REVIEW_OF_ChatGPT_Migration_Plan_Update_Standalone_PyPI_v0_1` (M3a/b, M5, M6, D4-D6)
- `Claude_REVIEW_OF_ChatGPT_DR_v0_8_and_StageA_Plan_v0_3_v0_1`, `v0_2` (S10, S11; v0.2 records D4-D6)
- `Claude_REVIEW_OF_ChatGPT_DR_v0_10_and_StageA_Plan_v0_5_v0_1` (M7, S12-S15, O7, O8)

**Responses and repository files:**
- `Claude_RESPONSE_TO_ChatGPT_AVX2_Acceptance_and_README_v0_1`
- `Claude_REVIEW_OF_ChatGPT_Migration_Docs_and_Handover_Taxonomy_v0_1` (DR v0.11, plan v0.6, Handback v0.5, ChatGPT migration handover v0.2)
- `Claude_HANDOVER_TO_Future_Claude_Migration_Chat_v0_1`, `v0_2` (this document)
- `Claude_HANDOVER_TO_Future_Claude_Chat_v0_5`: **WITHDRAWN** (role-3 boundary crossing)
- `README.md` (repository file)
- `phase2_byte_path_edit.py`

These files live in Dave's download area and repository, not in the new chat. Ask for any that are needed.

---

## 9. Pitfalls and lessons from this chat

- **Do not claim something is unverifiable before checking the uploads.** I once said the inspector's write behaviour was "not verifiable" when Dave had already supplied the source.
- **Measure before stating figures.** I once quoted encoding counts before measuring them.
- **Re-check line citations after writing.** I once cited the wrong mpeg2dec.c lines for the exit codes, and fixed it before sending.
- **Read the real CI file, not its description.** CNR3's workflow turned out to bypass the project entirely.
- **Do not assume a default stays a default.** Dave's no-defaults ruling exists for this reason. Pin what is measured; prove anything that is invisible on the command line with dumpbin and the logs.
- **Avoid hidden scope narrowing.** I wrongly treated the inspector project configuration as frozen; it is in scope, and only the source is frozen.
- **Respect the document taxonomy.** Never edit a development chat's handover from the migration chat. If Dave asks, point out the boundary first.
- **Check that every review actually reached the other chat.** M7 was lost because the review file never got into Dave's folder. When a MUST stays unaddressed, check delivery before repeating it.
- **Each review gets a new version.** When Dave ratifies decisions after a review, issue a v0.(n+1) of that review recording them, with a change log.

---

## 10. Change log

- **v0.2 (2026-10-09):** adopted the three-role document taxonomy; recorded the withdrawal of the role-3 Claude handover v0.5; added Handback v0.5, the ChatGPT migration handover v0.2 and the taxonomy review; recorded that the DR v0.10 review was missing from Dave's folder (root cause of the missing M7); two new lessons.
- **v0.1 (2026-10-09):** first handover for the migration-review role. Records state up to DR v0.11 / plan v0.6 / Handback v0.4 / ChatGPT handover v0.4, and that M7 and S12-S15 are not yet carried.
