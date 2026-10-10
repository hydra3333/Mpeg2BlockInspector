# Claude handover to future Claude - migration chat

**Filename:** Claude_HANDOVER_TO_Future_Claude_Migration_Chat_v0_5.md
**Version:** 0.5 (supersedes v0.4; new section 2.0 and updates to sections 5 and 6)
**Date:** 2026-10-10
**Role:** Claude = independent cold reviewer in the **migration chat only** (role 1 of the document taxonomy).
**Why now:** the migration ChatGPT chat reached its length limit on 2026-10-10 (about 12:20). Claude wrote ChatGPT's replacement handover, `ChatGPT_Migration_Chat_Handover_v0_10.md`, at Dave's request. This chat is long too. Knowledge comes first; status, history and the reading list come after.

---

## 1. Knowledge first: what a future Claude must know

### 1.1 The job

- Move GitHub `hydra3333/Mpeg2BlockInspector` to `hydra3333/VapourSynth-mpeg2Deblock`.
- Active local repository: `E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock`.
- Old tree `E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector`: rollback and reference only. Do not touch it until the migrated tree passes its checks.
- **Workflow:** ChatGPT drafts and maintains the Stage documents. Claude cold-reviews. Dave decides, runs everything on Windows and commits.
- **Review style:** findings are classed MUST / SHOULD / OPTIONAL / NO OBJECTION, each with file:line and a scripted check. Decisions go to Dave as question / why / recommendation / options, in plain English.

### 1.2 Dave's standing rules (all still in force)

1. Verify against the files and cite file and line. Label anything not verified as unverified. Disagree with ChatGPT, or with my own earlier review, where the evidence supports it.
2. Nothing destructive without Dave's explicit go: no GitHub rename, no deletes, no history rewrite, no force push. Stop at each decision and each check.
3. The inspector **source is frozen**: files may move, their content may not change. The inspector **project configuration** is in scope.
4. **No defaults:** "we should not rely on default behaviours for settings since microsoft are well known for fiddling with things in their releases." Every setting is written explicitly in the project XML.
5. Every document Claude produces is US-ASCII with CRLF line endings, checked by script, and named `Claude_<TOPIC>_vX_Y.md`. Repository files such as `README.md` keep their names.
6. Keep chat replies short and put the detail in the file.
7. Licence wording: AGPL, "version 3 or any later version".
8. At the end, Dave needs a short summary of the final layout and every path that changed.
9. **Policy:** target performance where possible, but never at the expense of security. Target AVX2 PCs, which have been around for a decade or more. This applies to both the VS2026 settings and GitHub Actions.

### 1.3 The document taxonomy: never cross it

| Role | Documents | Who edits |
|---|---|---|
| 1. Migration continuity | `ChatGPT_Migration_Chat_Handover_v0_*`, `Claude_HANDOVER_TO_Future_Claude_Migration_Chat_v0_*` | the migration chat |
| 2. Common handback | `MPEG2_Deblocking_Developer_Handback_v0_*` | ChatGPT drafts, Claude reviews |
| 3. Development-chat handovers | `ChatGPT_Handover_To_Future_ChatGPT_MPEG2_Deblocking_Project_v0_*`, `Claude_HANDOVER_TO_Future_Claude_Chat_v0_*` | **only the development chats. The migration chat never edits these.** |

Lesson already learned: I once wrote a role-3 `Claude_HANDOVER_TO_Future_Claude_Chat_v0_5`, withdrew it and Dave deleted it. Do not repeat that.

### 1.4 Stage plan

| Stage | What it covers | Status |
|---|---|---|
| A | Inspector normalisation plus the `.slnx` | A1 and A2 done; A3 in candidate review |
| B | VapourSynth API4 DLL placeholder: entry point only, no algorithm | not started |
| C | Canonical build harness: vswhere + MSBuild on the `.slnx` | not started |
| D | Release workflow that calls the same harness; no `cl` flag map | not started |
| E | Wheel/PyPI scaffold | not started |
| End | Common handback, then the final summary | not started |

### 1.5 Ratified build decisions

| ID | Decision |
|---|---|
| D1 | Release `/GL` + `/LTCG`. The `/O2` components (`/Oi /Ot /Ob2 /GF /Gy`) are written explicitly as pins, not changes. |
| D2 | Windows SDK unpinned; record the SDK actually used. |
| D3 (a) | Debug `FavorSizeOrSpeed=Speed`, `InlineFunctionExpansion=AnySuitable`, `IntrinsicFunctions=true`. |
| D4 = NO | `/MT` is consolidated into A3; there is no A4. If an index fails, bisect with uncommitted variants in this order: ISA, then `/MD`, then `/GL`+`/LTCG`, then host. |
| D5 | The plugin DLL uses `/MT`; "hybrid" only as a fallback. |
| D6 | Release `/PDBALTPATH:%_PDB%`. |
| O7 = YES | `/favor:blend` in Debug and Release. |
| AVX2 | x64 + AVX2 minimum for both projects, Debug and Release. Non-AVX2 budget CPUs are unsupported, and the README says so. |
| Security | `/GS`, CFG and CET ON in both configurations. `/sdl` is OFF for the inspector only (frozen reference-decoder exception) and ON for the plugin. `/fp:precise`, with `/fp:contract` absent. |
| Spectre | **Removed by Dave** on threat-model grounds; I agreed. It is pinned explicitly as `SpectreMitigation=false` in the `Label="Configuration"` group. M7 and MSB8040 are superseded. |
| S15 | LP timing: three runs before A3 and three after, for information only. |
| O8 | `/guard:ehcont` (`GuardEHContMetadata` exists in v180 `cl.xml`). Open, for Stage B. |

### 1.6 Distribution and licensing

- **Standalone Release:** the imports must contain none of `VCRUNTIME*`, `MSVCP*`, `api-ms-win-crt-*`, `ucrtbase*`, `CONCRT*`, `VCOMP*` or `MSVCR1*`. The inspector's allowed set is `KERNEL32.dll`. Do not use a bare `MSVCR*` pattern: it would match the system `msvcrt.dll`.
- **Runtime ownership:** no CRT-owned memory or objects cross the `/MT` DLL boundary. VapourSynth resources go through `vsapi`.
- **One build route:** the project XML is the only source of settings. The harness and CI never inject flags.
- **Licence:** AGPL-3.0-or-later. `NOTICE.md` is the legal and test-media boundary. The wheel must not copy CNR3's MIT metadata (CNR3 workflow line 198 says `License: MIT`).
- **CNR3 reference points:**
  - its workflow (lines 88-128) uses a hand-written `cl` flag map with `/MD` and `/arch:AVX2`, which we do not copy;
  - its wheel is `py3-none-win_amd64` with layout `vapoursynth/plugins/cnr3/cnr3.dll` (lines 165-257);
  - its local `1.BUILD.bat` uses vswhere + MSBuild.

### 1.7 MSBuild lessons (hard-won, keep applying)

- **MSBuild silently ignores unknown item metadata.** Every XML pin must be proven against Dave's installed VS2026 **v180** rule XML (`...\MSBuild\Microsoft\VC\v180\1033\*.xml`) on all of:
  - rule/tool;
  - the exact element name;
  - the enum or bool value;
  - placement (DataSource);
  - the toolset folder (v170 and v160 rows in the CSV do not count).
- **Placement facts from the v180 scan:**
  - `SpectreMitigation`, `WholeProgramOptimization`, `CharacterSet` and `PreferredToolArchitecture` go in `PropertyGroup Label="Configuration"`, **before** the `Microsoft.Cpp.props` import.
  - `WholeProgramOptimization` also exists in CL (`/GL`). Set it in both places, as CNR3 does.
  - `LinkIncremental`, `GenerateManifest` and `LinkControlFlowGuard` go in an unlabelled conditioned `PropertyGroup`.
  - The linker's error-reporting property is `LinkErrorReporting=QueueForNextLogin`. CL's `ErrorReporting=Queue` is a different property. `Link/ErrorReporting` does **not** exist (finding R1).
  - `GenerateDebugInformation` takes `false;true;DebugFastLink;DebugFull`. The pin is `DebugFull`.
  - There is no HighEntropyVA property, so use `/HIGHENTROPYVA` in Link `AdditionalOptions`.
  - `CETCompat`, `ManifestEmbed` and `ManifestInput` are Link metadata. `EnableSegmentHeap` is Manifest (`mt.xml`) metadata. `RemoveUnreferencedCodeData` gives `/Zc:inline`; `ProgramDataBaseFileName` gives `/Fd`.
  - A `false` BoolProperty with a `ReverseSwitch` **emits** that reverse switch (for example `/Gy-` or `/OPT:NOREF`). The predicted delta must list these.
- **Setting one property can switch on a toolset default for another.** Setting `LinkTimeCodeGeneration` (even `Default`) caused `/LTCGOUT`. Pin `LinkTimeCodeGenerationObjectFile` empty. "Emits nothing" must be judged on the whole command line, which is exactly what the mechanical W1 token diff does.
- **One owner per emitted switch** (U1). Do not add a lower-level property for a switch a higher-level one already produces (`EnableSegmentHeap` -> `/manifestinput`).
- **Expected keys come from evidence, not by hand.** The 82 native-tlog tokens break down as Debug CL 25, Release CL 23, Debug LINK 16 and Release LINK 18. Add the four `/errorReport` switches, which appear only in the detailed MSBuild log, to get 86. The default library list is a `DELIBERATE_EXCEPTION`, proven by the Release import gate.

### 1.8 Checkpoint baseline (after A1 `d38d56d6` and A2 `837df123`)

- **Toolchain:** MSBuild 18.10.1.42706, v145, VCTools 14.51.36231, HostX86\x64, SDK 10.0.28000.0.
- **Warnings:**
  - Release: 17.
  - Debug: 20 (the Release 17, plus C4013 strcat at `spatscal.c:91` and `store.c:217`, plus LNK4075).
- **Exe hashes:** Debug `66be0a77...8bb9`; Release `d31fbad8...c6f8`.
- **Indexes:** all six byte-identical. Cleanup restored only `.log` files.
- **Checkpoint command lines** (from the token CSV):
  - Debug CL: `/c /ZI /JMC /nologo /W3 /WX- /diagnostics:column /sdl- /Od /D _CRT_SECURE_NO_WARNINGS /Gm- /EHsc /RTC1 /MDd /GS /fp:precise /Zc:wchar_t /Zc:forScope /Zc:inline /Fo /Fd /external:W3 /Gd /TC /FC`
  - Release CL: the same, but `/Zi`, `/O2` and `/MD`, with no `/JMC` and no `/RTC1`.
  - LINK: `/OUT /INCREMENTAL:NO /NOLOGO <default libs> /MANIFEST /MANIFESTUAC:level='asInvoker' uiAccess='false' /manifest:embed /MANIFESTINPUT:<segmentheap> /DEBUG /PDB /SUBSYSTEM:CONSOLE [Release: /OPT:REF /OPT:ICF] /TLBID:1 /DYNAMICBASE /NXCOMPAT /IMPLIB /MACHINE:X64`
- **Dumpbin:**
  - DLL characteristics `8160` (HEVA, Dynamic base, NX, TS Aware), with no Guard flag;
  - Guard Flags `0x100`, function count 0;
  - Release imports `VCRUNTIME140`, 8 `api-ms-win-crt` DLLs and `KERNEL32`;
  - Debug imports `VCRUNTIME140D`, `ucrtbased` and `KERNEL32`;
  - the `cv` entry holds the full PDB path.
- **A1 project:** `Mpeg2BlockInspector.vcxproj`, SHA-256 `87acd9ad...7a57`. It already has `Manifest/EnableSegmentHeap=true` (lines 49 and 63) and **no** `ManifestInput`. EnableSegmentHeap is what produced the checkpoint `/MANIFESTINPUT`.

### 1.9 Published state

- `main` = `ab145f5`; interim checkpoint `b4dace0` (the README was committed there with the old Spectre wording, since corrected).
- Tags: pre-Stage-A `b38fde11`; post-restructure `a9c782ac`.
- Dave pushes as an offsite backup after review-driven updates.

---

## 2.0 LATEST STATE (2026-10-10 12:50): read this before the rest of section 2

**v0.10 is RATIFIED and APPLIED, and its gate is in progress.**

**v0.10 candidate:** v0.9 plus `<LinkTimeCodeGenerationObjectFile />` in the Debug and Release Link sections.
- SHA-256 `73e9019cda7d1061ecdb06526c60f4ee84baa4c385b7ca0dde4269544e4fdb46`.
- My review: `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_10_Candidate_v0_1.md` = RATIFIABLE.
  - I verified independently: the two-line diff; pin rows `LD_ltcgout` / `LR_ltcgout`; counts of 140 applications, 143 rows and 134 v180 targets; all six validators PASS.
  - Negative tests: removing an element or giving it a non-empty value both FAIL.
  - `LinkTimeCodeGenerationObjectFile` = `link.xml` StringProperty, `Switch=LTCGOUT:`.
  - X3 is answered honestly. `Microsoft.Link.Common.props:63` sets the `.iobj` default with the condition `'%(Link.LinkTimeCodeGenerationObjectFile)' == ''` only, so the coupling to `LinkTimeCodeGeneration` sits inside the Link task and is recorded empirically.
  - OPTIONAL Y1: the package wrongly carried the stale DR v0_10 and Plan v0_5, probably through a `*v0_10*` filename pattern. Y2: note that S15 was run once each.

**Dave's command log, as applied:**
- The production `vs\VapourSynth-mpeg2Deblock\Mpeg2BlockInspector.vcxproj` hashes to `73e9019c...db46`.
- `git diff` shows only the two added lines, so HEAD holds v0.9 (Dave's earlier snapshot commit).
- Clean `/t:Rebuild` of Debug and Release through the `.slnx`, `/v:detailed`: both RC=0.
- Logs are in `E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\A3_v0_7_PRE_CANDIDATE\A3_v0_10_POST_APPLY_GATE\{Debug,Release}\StageA_A3_v0_10_{Debug,Release}_x64.log`.
- `findstr " /LTCGOUT:"` on both logs: RC=1 (absent). That is encouraging, but it is not the gate.

**The ChatGPT migration chat died** at its length limit. I wrote `ChatGPT_Migration_Chat_Handover_v0_10.md` (US-ASCII, CRLF).
- Section 0.3 holds the full remaining gate sequence:
  1. preserve the four tlogs;
  2. W1 with the extractor and my checker, both unchanged (expect 33 / 32 / 23 / 25);
  3. HostX64;
  4. warnings 17 / 17;
  5. W2 dumpbin;
  6. SHAs;
  7. frozen hashes;
  8. six indexes with return codes;
  9. `.iobj` / `.ipdb` and `git status`;
  10. package the evidence for Claude.
- Dave was given the exact list of 16 files to attach to the new ChatGPT chat.

**Git at 12:49:**
- Dave's `got add -A` typo meant nothing was staged, the commit did nothing and the push was a no-op. He was told to repeat it correctly.
- The working tree showed two tracked files deleted: `docs/HANDOVER/migration/A3_v0_8_to_v0_9.diff` and `CANDIDATE_STRUCTURE_VALIDATOR_PASS.txt`. They may have been moved into a new `docs/HANDOVER/migration/chatgpt_new_chat_stuff_2026.10.10/` folder; unverified.
- Also untracked: `ChatGPT_Migration_Chat_Handover_v0_10.md`, my v0.10 review, the v0.10 package zip, and `chatgpt_new_chat_stuff_2026.10.10.zip` plus its folder.

**Git practice now:**
- Dave uses `git add -A --dry-run`, then `git add -A`, then a "Snapshot: ..." commit and a push as backup. That is fine.
- `.gitignore` now excludes the two scratch folders `vs/A3_LTCGOUT_SCRATCH/` and `vs/A3_LTCG_SUPPRESS_SCRATCH/`, and `vs/VapourSynth-mpeg2Deblock/*.log`, because the detailed MSBuild logs matched `C:\Users` / `USERNAME` style strings.
- Before the snapshot push I checked that no zip contains `.log` or `.tlog` files. Nothing was found.

**My next job:** review the v0.10 gate evidence package from the new ChatGPT chat.
- W1 must PASS unchanged.
- W2 must show PE32+, LAA, HEVA, Dynamic base, NX, TS Aware, CFG with a non-zero function count, CET, the cookie, `KERNEL32.dll` only, D6 file name only, and the manifest present.
- The six indexes must be byte-identical with return codes recorded.
- Frozen hashes unchanged; warnings explained.

If all of that holds, A3 is accepted and Stage A goes to close-out: README consistency, refreshed DR v0.18 / Plan v0.13 / Handback v0.12 / knowledge v0.4, commit, push, and an optional tag that is Dave's call.

## 2. Current position (where to pick up), as of 2026-10-10 11:46 (superseded in part by 2.0)

**A3 history in this round:**
1. **v0.8** (`30999ef3...52f3`): not ratifiable. U1 was the double owner of the segment-heap manifest; U2 was six switches missing from the prediction.
2. **v0.9** (`ebfcde82405fd2dc25aa7a14a160f89375465d545927b3e4583e7a40fd1af668`): reviewed RATIFIABLE (`Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_9_Candidate_v0_1.md`).
   - The diff against v0.8 removed exactly the two `Link/ManifestInput` lines; `EnableSegmentHeap` is the single owner.
   - Pin rows 81 and 100 were re-pointed, and U2 was added to the prediction.
3. **Dave ratified v0.9 and applied it to the production working tree. It is NOT committed.** The last published commit is `365222b` ("Record A3 v0.9 ratification and migration state"), which still holds the pre-A3 project.

**Post-apply gate status note (ChatGPT), as reported** (raw evidence not yet seen by Claude):
- Debug and Release built on HostX64; the applied project's SHA equals the v0.9 SHA.
- Warnings: Debug 20 -> 17 (2 x C4013 strcat gone with `/Oi`; LNK4075 gone with `/Zi`); Release 17.
- `/Qspectre` and `/fp:contract` absent.
- Release:
  - imports `KERNEL32.dll` only;
  - HEVA, Dynamic base, NX, CFG and CET present;
  - Guard Flags `0x10017500`, CF function count 37;
  - CodeView entry holds the file name only (D6);
  - exe SHA `de564acf...288f`.
- Frozen hashes unchanged (getpic.c `e80239cf...`, mpeg2dec.c `8e6053cc...`, `tools\Stage1_Inspector_Analyzer_v0_2.py` `8e0d5830...`), and `git diff` against the `pre-stageA-vs-normalization` tag is empty.
- All six indexes byte-identical. Four return codes were lost to a typo (W3, optional).
- S15: one run each, 0.653 s pre-A3 and 0.613 s post-A3. PowerShell pipe timing was rejected.
- Evidence root: `E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\A3_v0_7_PRE_CANDIDATE\A3_v0_9_POST_APPLY_GATE`.

**My gate review** (`Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_9_Post_Apply_Gate_v0_1.md`):
- **W1 (MUST before Stage A closure, not before an interim commit):** a mechanical token check using `Claude_check_A3_post_tokens_v0_1.py`. It compares the checkpoint tokens plus exactly the v0.9 predicted delta against the post-A3 tokens. Expected counts: Debug CL 33, Release CL 32, Debug LINK 23, Release LINK 25.
- **W2 (SHOULD):** the four raw Release dumpbin files, covering LAA, TS Aware, PE32+ and the manifest.
- **W3-W7 (OPTIONAL).**

**W1 result:** both CL lines passed exactly. Each LINK line had exactly one extra token, `/LTCGOUT:...\<cfg>\Mpeg2BlockInspector.iobj`.
- **Cause:** setting `LinkTimeCodeGeneration` explicitly (Debug `Default`, Release `UseLinkTimeCodeGeneration`) makes `Microsoft.Link.Common.props` default `LinkTimeCodeGenerationObjectFile` to `$(IntDir)$(TargetName).iobj`. A1 had neither property, and the checkpoint had no `/LTCGOUT`.
- **Scratch experiment A:** removing Debug `Default` removes `/LTCGOUT` from Debug.
- **Scratch experiment B:** adding `<LinkTimeCodeGenerationObjectFile />` (empty) after each `LinkTimeCodeGeneration` removes `/LTCGOUT` from both; `/LTCG` is kept in Release; both builds RC=0.
- Production is still exactly v0.9.

**Proposed v0.10:** v0.9 plus those two empty elements. My review is `Claude_REVIEW_OF_ChatGPT_StageA_A3_W1_LTCGOUT_and_v0_10_Proposal_v0_1.md`. The checker stays **unchanged**.
- Q1 = yes, use the empty pins.
- Q2 = no, do not remove Debug `Default` instead: it breaks no-defaults and cannot fix Release.
- Q3 = yes, after the MUST items.
- MUST X1: pin rows `LD_ltcgout` / `LR_ltcgout`; the validators must accept an empty value; counts 140 applications and 143 rows.
- MUST X2: the full A3 gate on v0.10, with a clean rebuild, `git status` free of stray `.iobj`/`.ipdb`, W1 unchanged, W2, imports, D6, the six indexes, the frozen hashes and the warnings.
- SHOULD X3: quote the exact props condition with file:line. ChatGPT's "when otherwise empty" does not explain why A1 got no `/LTCGOUT`; the trigger is `LinkTimeCodeGeneration` being set.
- SHOULD X4: knowledge record and predicted delta.
- SHOULD X5: the Stage B plugin gets the same empty pin, and the Stage C/D harness checks for "no /LTCGOUT".

**Next:**
1. ChatGPT, in the same chat if it recovers, otherwise a new chat bootstrapped from its handover, produces the v0.10 package.
2. Claude does a short check: the diff against v0.9 is exactly two added lines, plus the pin table and validators.
3. Dave ratifies, applies, cleanly rebuilds and runs the full gate, including W1 unchanged.
4. Claude reviews the gate, including W2.
5. Stage A close-out.

**ChatGPT's documents at last sight:**
- DR v0.16, Plan v0.11, Handback v0.10;
- ChatGPT migration handover **v0.8**;
- `StageA_VS2026_MSBuild_Hard_Earned_Knowledge_v0_1.md`, which is new: a durable MSBuild lessons record, accurate apart from the inference noted in V1 of my v0.9 review.

## 3. Still to do after A3

1. **Stage B decisions:**
   - the coupled naming and package-identity set;
   - the C++ standard;
   - the header/API profile;
   - FP/FMA;
   - COMDAT;
   - the version resource;
   - O8 `/guard:ehcont`;
   - an optional runtime CPU check;
   - the plugin's `SpectreMitigation=false`, `/sdl` ON and `/MT`.
2. Stage C (harness), Stage D (release workflow, using the same harness), Stage E (wheel: AGPL metadata, not MIT).
3. Review the final handback.
4. Update `Claude_Migration_Final_Summary_v0_1.md`.
5. Make sure each review document is either committed by name or removed.

---

## 4. Process notes

- Every package must carry all the Claude reviews it answers. Twice a review never reached ChatGPT; that was caught and fixed.
- Run `python3 -I` on extracted packages, keep each package in its own directory, and verify the SHA files first.
- ChatGPT sandbox PASS files can contain "Spreadsheet runtime warmup failed" tracebacks. They are noise; trust the LOCAL_PASS files and your own re-runs.
- Errors I have made, so watch for them:
  - a wrong line citation (`mpeg2dec.c` exit codes are lines 178-192);
  - assuming MSB8040 was a warning;
  - the role-3 boundary crossing.
- ChatGPT defects caught so far:
  - the `Link/ErrorReporting` pin;
  - a dropped pin checklist;
  - a loosely matching validator;
  - duplicated headings;
  - a LF-only BAT;
  - the double manifest owner (v0.8);
  - the `/LTCGOUT` side effect, caught by W1 and not by prediction.

---

## 5. Claude reviews issued in this chat (all in Dave's folder)

1. `Claude_REVIEW_OF_ChatGPT_StageA_Audit_Proposal_v0_1.md`, `v0_2.md`
2. `Claude_REVIEW_OF_ChatGPT_StageA_Checkpoint_Status_v0_1.md`
3. `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_2_Package_v0_1.md`
4. `Claude_REVIEW_OF_ChatGPT_Migration_Plan_Update_Standalone_PyPI_v0_1.md`
5. `Claude_REVIEW_OF_ChatGPT_DR_v0_8_and_StageA_Plan_v0_3_v0_1.md`, `v0_2.md`
6. `Claude_REVIEW_OF_ChatGPT_DR_v0_10_and_StageA_Plan_v0_5_v0_1.md`
7. `Claude_RESPONSE_TO_ChatGPT_AVX2_Acceptance_and_README_v0_1.md` (plus the user-facing `README.md`)
8. `Claude_REVIEW_OF_ChatGPT_Migration_Docs_and_Handover_Taxonomy_v0_1.md`
9. `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_4_PreCandidate_and_DR_v0_12_v0_1.md`
10. `Claude_REVIEW_OF_ChatGPT_NoSpectre_DR_v0_13_A3_v0_5_v0_1.md`
11. `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_6_PreCandidate_and_DR_v0_14_v0_1.md`
12. `Claude_REVIEW_OF_StageA_A3_S13_Q1_Local_Evidence_v0_1.md`
13. `Claude_REVIEW_OF_StageA_A3_Q1_R1_R4_Local_Evidence_Closure_v0_1.md`
14. `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_8_Candidate_v0_1.md`
15. `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_9_Candidate_v0_1.md`
16. `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_9_Post_Apply_Gate_v0_1.md`, plus the tool `Claude_check_A3_post_tokens_v0_1.py`
17. `Claude_REVIEW_OF_ChatGPT_StageA_A3_W1_LTCGOUT_and_v0_10_Proposal_v0_1.md`
18. `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_10_Candidate_v0_1.md` (latest review)
19. `ChatGPT_Migration_Chat_Handover_v0_10.md` (a role-1 document, written by Claude for ChatGPT at Dave's request)

---

## 6. First actions for a new Claude migration chat

1. Read this file, then the latest ChatGPT migration handover, DR, Plan and Handback that Dave attaches.
2. Ask Dave for the v0.10 A3 gate evidence package from the new ChatGPT chat, or later material.
3. Re-run the validators locally against the package's CSVs before trusting any PASS.
