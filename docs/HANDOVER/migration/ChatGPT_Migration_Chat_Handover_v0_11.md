# ChatGPT Handover to a Future Migration Chat

## VapourSynth-mpeg2Deblock Repository / Visual Studio / Release Migration


**Filename:** `ChatGPT_Migration_Chat_Handover_v0_11.md`
**Version:** 0.11
**Date:** 2026-10-10 (updated after successful A3 v0.10 W1 and HostX64 gates)
**From:** migration ChatGPT chat, incorporating Claude migration handover v0.10 and subsequent Dave evidence/decisions (Claude did not author this v0.11 revision).
**To:** a fresh ChatGPT chat continuing migration/build-system work
**Status:** MIGRATION-ONLY continuity handover; not MPEG-2 technical authority
**Supersedes:** `ChatGPT_Migration_Chat_Handover_v0_10.md`.

**Rule for the new chat:** do not reconstruct anything from memory. Where this handover says "verify", run the command and look. Facts marked **(unverified)** were not seen first-hand by the author.

---

## 2026-10-10 addendum: 64-bit, discovery and compiler policy

## New binding decisions and staged implementation (2026-10-10)

Decision authority: Dave. Review basis: `Claude_REVIEW_OF_ChatGPT_StageC_MSBuild_Discovery_Proposal_v0_3.md` (M1-M5), cold-reviewed by ChatGPT on 2026-10-10. This is a documentation update only: no production project modification and no interruption to the A3 v0.10 gate. The technical implementation mechanisms identified below as UNVERIFIED remain pending local tests and a separately reviewed candidate.

### Binding policy: 64-bit everywhere

- Target: x64 only, unchanged from the historical baseline.
- All production projects shall explicitly set `PreferredToolArchitecture=x64` in each appropriate `Label="Configuration"` group; compiler/linker evidence must show `HostX64\x64\CL.exe` and `HostX64\x64\link.exe`.
- Permanent harness and CI select `MSBuild\Current\Bin\amd64\MSBuild.exe` beneath the discovered installation; verify the MSBuild *process* is 64-bit at runtime (not merely by path or PE header). MSBuild engine bitness and compiler/linker host bitness are separate requirements.
- Interactive tool setup: `VsDevCmd.bat -arch=amd64 -host_arch=amd64`; use the `HostX64\x64` dumpbin/toolchain from that same installation. Python and helper binaries must be 64-bit. Stage D uses x64 Windows runners.
- No silent x86 fallback. The x86 host is permitted solely as the last D4 diagnostic step, after ISA, `/MD`, and `/GL`+`/LTCG` diagnostic experiments; local, uncommitted, never shipped.

### Binding policy: installation discovery and version handling

- Stage C performs one `vswhere` installation search, with no VS version range, no `-prerelease`, and no hard-coded VS installation path: `-latest -products * -requires Microsoft.Component.MSBuild Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath`. Build Tools products are explicitly eligible; record selected product and installation identity. The VC component identifier remains UNVERIFIED on Dave's machine.
- From the single discovered root derive MSBuild, the project-owned toolset resolution, interactive VsDevCmd and 64-bit dumpbin. No independent search/fallback to another VS installation. `vswhere` use and the exact runtime lookup chain require Stage C validation.
- Current A3 v0.10 gate **keeps** the established fixed `C:\Program Files\Microsoft Visual Studio\18\Community\MSBuild\Current\Bin\MSBuild.exe` checkpoint path; that path is not a template for the permanent harness. The v0.10 project stays at `PlatformToolset=v145` until Stage A is closed.
- Permanent compiler policy (Dave): **Use the newest installed MSVC toolset (minimum v145) and the MSVC build Visual Studio designates as current for that toolset (normally the newest installed, in-support build), with 64-bit host tools. The toolset name and exact compiler version are recorded on every build. If either differs from the last accepted build, the switch check, warning comparison and six-index regression must all pass again before that build is accepted.**
- Record this policy now, but implement toolset selection only *after* Stage A closes, as a small independently reviewed and ratified project candidate. Claude M5 proposes (UNVERIFIED) `PlatformToolset=$(DefaultPlatformToolset)` with a minimum-v145 project guard; BOTH its availability at the configuration import point and its selection semantics remain UNVERIFIED, and must not be asserted as a working implementation. The meaning of "newest installed" versus "latest in-support default" must be reconciled and demonstrated. Minimum-version comparison must be numeric/semantic, not lexicographic. No new project flags supplied by harness/CI.
- Do not silently rely on Microsoft defaults: **discover, verify, record**. Log installation/product, VS version, selected MSBuild path/version/runtime bitness, `PlatformToolset`, exact MSVC compiler version/host paths, and SDK version on every build.

### Permanent acceptance gates and environment isolation

- Every harness/CI build must mechanically verify CL and LINK command-switch sets against a reviewed expected set, require `HostX64\x64` for compiler/linker, and verify Release imports are exactly `KERNEL32.dll`. Toolset/compiler change triggers additional warning-by-code/file/line comparison and byte-identical six-index regression before acceptance. Do not weaken required security flags to obtain a pass. The maintained switch baseline must be consciously updated and reviewed if toolchain semantics evolve; unknown switches are failures, not silently accepted.
- Harness builds launch from a plain CMD environment, NOT after executing VsDevCmd; explicitly pass configuration and x64 platform without injecting compiler/linker settings. Refuse or sanitize `CL`, `_CL_`, `LINK`, `_LINK_`, `Platform`, and any environment property overriding project-owned configuration, including `PreferredToolArchitecture` and relevant MSBuild override entry points. Which properties MSBuild treats as global, and the precise environment guard, require tested design. VsDevCmd is permitted for separate interactive tools such as dumpbin.
- Prove locally before accepting Stage C: vswhere component/product selection, actual engine process bitness, default-toolset property/import ordering, minimum-version guard, default compiler-build selection, and the exact installed `dumpbin.exe` lookup. Keep UNVERIFIED findings labeled until directly evidenced; do not import unverified claims as fact.

### Current A3 state and documentation boundary

- A3 candidate v0.10 (`Mpeg2BlockInspector_A3_APPLYABLE_CANDIDATE_v0_10.vcxproj`, SHA-256 `73e9019cda7d1061ecdb06526c60f4ee84baa4c385b7ca0dde4269544e4fdb46`) was ratified/applied; Debug and Release clean rebuilds had RC=0.
- W1 post-application evidence preserved four tlogs, byte-compared them, extracted 33/32 CL and 23/25 LINK tokens, and Claude's unchanged checker reported four PASS outcomes (`W1_CHECKER_RC=0`). Build logs also confirmed HostX64 x64 CL and LINK in both configurations. Evidence is on Dave's Windows machine outside the repository; not in the GitHub ZIP.
- Stage A remains OPEN. Warning comparison, W2 binary/security/import checks, hashes, frozen sources, six-index regression, status evidence, packaging and Claude gate review remain outstanding. Next action: compare Debug/Release warnings against v0.9 by code, file and line. Do not claim A3/Stage A closure yet.
- On this user's Windows working copy, agreed `.vcxproj`/`.slnx` SHA-256 hashes are for the CRLF file representation. GitHub ZIP LF representations can legitimately differ. Confirm paths and bytes locally; the ZIP is reference/layout only.

### Immediate operational continuation for a new migration chat

The previous v0.10 handover section 0.3 ordering remains controlling except that steps 1 (copy tlogs), 2 (W1 extractor/checker) and 3 (HostX64 check) are now DONE/PASS based on Dave's 2026-10-10 console evidence. Step 4 is NEXT: capture v0.10 Debug and Release warning lines and compare with v0.9 by code/file/line; expected counts are 17 each. Then proceed sequentially through W2 binary checks, hashes/frozen checks, six-index regressions, hygiene and Claude gate review. No project edits, rebuilds, or cleanup without Dave's approval.

The attached `Claude_REVIEW_OF_ChatGPT_StageC_MSBuild_Discovery_Proposal_v0_3.md` is the controlling Stage C review (v0.1/v0.2 superseded). This v0.11 document is written for Claude's review, NOT a declaration that Stage A has closed. Keep developer handovers `ChatGPT_Handover_To_Future_ChatGPT_MPEG2_Deblocking_Project_*` and `Claude_HANDOVER_TO_Future_Claude_Chat_*` untouched. The A3 evidence remains out of repository.

### K4: automatic imports and response files (binding for Stage C/D)

- Fail closed if any `Directory.Build.props`, `Directory.Build.targets`, or `Directory.Build.rsp` exists in a repository ancestor directory, from the repository parent through filesystem root; also reject unreviewed occurrences within the repository that may affect a build. Log the checked paths and results.
- Launch MSBuild with `-noAutoResponse` so implicit MSBuild response files do not silently inject switches (including applicable `MSBuild.rsp` and `Directory.Build.rsp`). Validate the precise MSBuild 18.x response-file behavior locally; any uncertainty is an unverified Stage C gate item.
- Prove the guard experimentally once using a disposable scratch project and a scratch `Directory.Build.props` in its ancestor directory. Confirm the harness refuses to build, then remove the scratch file. Never create this probe in or above the production repository. Record command, output, and return code.
- The guard is additive to environment-property checks, including `PreferredToolArchitecture`, `CL`, `_CL_`, `LINK`, `_LINK_`, `Platform`, and relevant MSBuild/global-property override mechanisms. No build-policy injection through environment, response files or auto-imports is permitted.

### K3: compiler build designated by Visual Studio

- No project-level `VCToolsVersion` override: the designated current build is **recorded, not pinned**. Any change relative to last accepted compiler/toolset triggers command-switch, warning, and six-index rerun before acceptance. The exact selection rules and `DefaultPlatformToolset` implementation remain UNVERIFIED until local Stage C/post-A testing.
- `-latest`, without `-prerelease`, selects the newest **released** qualifying installed Visual Studio. Keeping the build machine updated is an operator responsibility; discovery does not install updates. Build Tools are eligible via `-products *`, and the selected product must be logged.

---

# 0. WHERE WE ARE RIGHT NOW (read this first)

## 0.1 Current authoritative state (updated 2026-10-10)

- A3 v0.10 SHA-256 `73e9019cda7d1061ecdb06526c60f4ee84baa4c385b7ca0dde4269544e4fdb46` was ratified and applied byte-for-byte.
- Debug and Release clean `/t:Rebuild` returned RC=0. The four native tlogs were copied to the external evidence directory and passed `fc /b`.
- W1 extraction: Debug CL 33, Release CL 32, Debug LINK 23, Release LINK 25; unchanged Claude checker PASS, RC=0.
- Debug and Release `CL.exe` and `link.exe` from `HostX64\x64` confirmed in detailed logs.
- Stage A remains OPEN; NEXT is warning comparison, then W2 and remaining gates. This supersedes the stale uncompleted-step phrasing preserved in the historical section 0.3 below.

## 0.2 Exact current facts (from Dave's command log, 2026-10-10)

```text
Candidate applied:  Mpeg2BlockInspector_A3_APPLYABLE_CANDIDATE_v0_10.vcxproj
Candidate SHA-256:  73e9019cda7d1061ecdb06526c60f4ee84baa4c385b7ca0dde4269544e4fdb46
Source copy:        E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\A3_v0_7_PRE_CANDIDATE\StageA_A3_v0_10_APPLYABLE_CANDIDATE_REVIEW_PACKAGE\Mpeg2BlockInspector_A3_APPLYABLE_CANDIDATE_v0_10.vcxproj
Production path:    vs\VapourSynth-mpeg2Deblock\Mpeg2BlockInspector.vcxproj
Production SHA:     73e9019cda7d1061ecdb06526c60f4ee84baa4c385b7ca0dde4269544e4fdb46  (certutil, after copy /b)
```

`git diff` of the production project against HEAD shows **exactly the two added lines**:
- `<LinkTimeCodeGenerationObjectFile />` after `<LinkTimeCodeGeneration>Default</LinkTimeCodeGeneration>` (Debug, around line 110);
- the same element after `<LinkTimeCodeGeneration>UseLinkTimeCodeGeneration</LinkTimeCodeGeneration>` (Release, around line 178).

So **HEAD already contains the v0.9 project**: Dave committed the applied v0.9 as a snapshot earlier.

`git status --short` at that moment:

```text
 M vs/VapourSynth-mpeg2Deblock/Mpeg2BlockInspector.vcxproj
?? docs/HANDOVER/migration/Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_10_Candidate_v0_1.md
?? docs/HANDOVER/migration/StageA_A3_v0_10_APPLYABLE_CANDIDATE_REVIEW_PACKAGE.zip
```

The v0.10 gate evidence folders have been created:

```text
E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\A3_v0_7_PRE_CANDIDATE\A3_v0_10_POST_APPLY_GATE\
    Debug\StageA_A3_v0_10_Debug_x64.log      (detailed MSBuild log, /t:Rebuild)
    Release\StageA_A3_v0_10_Release_x64.log  (detailed MSBuild log, /t:Rebuild)
```

The build commands used (cwd = production tree):

```text
set "MSBUILD=C:\Program Files\Microsoft Visual Studio\18\Community\MSBuild\Current\Bin\MSBuild.exe"
"%MSBUILD%" "vs\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock.slnx" /m /t:Rebuild /p:Configuration=Debug /p:Platform=x64 /v:detailed > "...\A3_v0_10_POST_APPLY_GATE\Debug\StageA_A3_v0_10_Debug_x64.log" 2>&1
   -> DEBUG_REBUILD_RC=0
"%MSBUILD%" "vs\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock.slnx" /m /t:Rebuild /p:Configuration=Release /p:Platform=x64 /v:detailed > "...\A3_v0_10_POST_APPLY_GATE\Release\StageA_A3_v0_10_Release_x64.log" 2>&1
   -> RELEASE_REBUILD_RC=0
findstr /i /c:" /LTCGOUT:" <Debug log>    -> RC=1 (not found)
findstr /i /c:" /LTCGOUT:" <Release log>  -> RC=1 (not found)
```

The `findstr` result is encouraging but **not** the gate. W1 on the native tlogs is the gate.

## 0.3 Gate checklist (steps 1-3 completed; step 4 next)

Do these one bounded step at a time, with ordinary one-line CMD commands and no placeholders. Run every command from the production tree unless stated.

1. **DONE/PASS: Preserve the four native tlogs from this rebuild into the evidence folder.**
   - Locate them; do not guess the intermediate path: `dir /s /b vs\VapourSynth-mpeg2Deblock\*.command.1.tlog`
   - Copy the Debug and Release `CL.command.1.tlog` and `link.command.1.tlog` into `A3_v0_10_POST_APPLY_GATE\Debug\` and `\Release\`, named `Debug_CL.command.1.tlog`, `Debug_link.command.1.tlog`, `Release_CL.command.1.tlog` and `Release_link.command.1.tlog`. These are the names used for v0.9.
   - Confirm the timestamps are from this rebuild.
2. **DONE/PASS: W1, the mechanical command-line gate.** The extractor, the checker and `StageA_A3_checkpoint_tokens_generated_v0_4.csv` are all in the v0.10 package folder, `...\A3_v0_7_PRE_CANDIDATE\StageA_A3_v0_10_APPLYABLE_CANDIDATE_REVIEW_PACKAGE\` (verify). The checker is also in `docs\HANDOVER\migration\`. Run the existing extractor, unchanged, on the four tlogs:
   ```text
   python extract_StageA_A3_checkpoint_tlog_tokens_v0_4.py --debug-cl <Debug_CL tlog> --release-cl <Release_CL tlog> --debug-link <Debug_link tlog> --release-link <Release_link tlog> --out StageA_A3_v0_10_post_tokens_v0_1.csv
   ```
   (Write the real paths, not the `<...>` names.) Then run Claude's checker, **unchanged**:
   ```text
   python Claude_check_A3_post_tokens_v0_1.py --checkpoint StageA_A3_checkpoint_tokens_generated_v0_4.csv --post StageA_A3_v0_10_post_tokens_v0_1.csv
   ```
   - Required: `PASS` for all four. Debug CL 33, Release CL 32, Debug LINK 23, Release LINK 25.
   - If it FAILs: **stop**. Do not edit the checker. Reconcile each listed token and return to Claude and Dave.
3. **DONE/PASS: HostX64 check.** The detailed logs must show `HostX64\x64` `CL.exe` and `link.exe` for both configurations.
4. **NEXT: Warnings.**
   - Expected: Debug 17 and Release 17, the same as applied v0.9.
   - The Debug drop from 20 to 17 is already explained: 2 x C4013 `strcat` gone with `/Oi`, and LNK4075 gone with `/ZI` -> `/Zi`.
   - Compare by code, file and line against the v0.9 lists. Any new or unexplained warning stops the gate.
5. **W2: the PE/security gate on the v0.10 Release exe** (`vs\VapourSynth-mpeg2Deblock\x64\Release\Mpeg2BlockInspector.exe`; verify the path). Save each capture as a text file in `A3_v0_10_POST_APPLY_GATE\Release\`:
   ```text
   dumpbin /headers <exe>      -> StageA_A3_v0_10_Release_headers.txt
   dumpbin /loadconfig <exe>   -> StageA_A3_v0_10_Release_loadconfig.txt
   dumpbin /imports <exe>      -> StageA_A3_v0_10_Release_imports.txt
   dumpbin /dependents <exe>   -> StageA_A3_v0_10_Release_dependents.txt
   ```
   Run `dumpbin` from a VS Developer Command Prompt, or by full path under `VC\Tools\MSVC\14.51.36231\bin\HostX64\x64\`. The headers output also contains the debug directories.

   Required:
   - x64 (`8664`), PE32+;
   - "Application can handle large (>2GB) addresses";
   - High Entropy Virtual Addresses;
   - Dynamic base;
   - NX compatible;
   - Terminal Server Aware;
   - Control Flow Guard in the DLL characteristics;
   - CET compatible in the extended DLL characteristics;
   - a non-zero security cookie;
   - a Guard CF function table present, with a count above 0. Applied v0.9 had a count of 37 and Guard Flags `10017500`;
   - imports exactly `KERNEL32.dll`, with none of `VCRUNTIME*`, `MSVCP*`, `api-ms-win-crt-*`, `ucrtbase*`, `CONCRT*`, `VCOMP*` or `MSVCR1*`;
   - the Release CodeView/RSDS entry holds the file name `Mpeg2BlockInspector.pdb` only (D6);
   - an embedded manifest present. A `.rsrc` section is the minimum evidence. Stronger: `mt.exe -inputresource:<exe>;#1 -out:extracted.manifest`, and confirm the segment-heap and `asInvoker` content.

   Optionally capture the Debug exe the same way (Claude's W5).
6. **Record SHA-256** of:
   - the Debug exe;
   - the Release exe (applied v0.9 Release was `de564acf54aaa657dbbb98f8d06132292f7fd8ea372601fa682f77958985288f`; v0.10 may differ, and that is informational only);
   - the production `.vcxproj`, which must be `73e9019c...db46`;
   - `Mpeg2BlockInspector.vcxproj.filters`;
   - `VapourSynth-mpeg2Deblock.slnx`, whose A2 value was `fa24efcd73401a38604e2f4228b07d8b960abcbfb66da22c02908e9d1cdb0754`.
7. **Frozen-source gate.**
   - `certutil -hashfile` the three frozen files (section 5). They must be unchanged.
   - `git diff --name-status pre-stageA-vs-normalization -- src/Mpeg2BlockInspector tools/Stage1_Inspector_Analyzer_v0_2.py` must print nothing.
8. **Six-index regression with the new Release exe.**
   - The cases are `TEST_2A_A001`, `TEST_2A_A001_blocky`, `TEST_4A_A003`, `LG_576i_3_LP`, `LG_576i_4_EP` and `LG_576i_5_MLS`.
   - Each is demuxed with ffmpeg to an MPEG-2 elementary stream and fed to the inspector. **Use exactly the same commands as the v0.9 gate run** (the repository's existing test scripts or Dave's CMD history). The exact command lines are **(unverified)** here, so do not invent them.
   - Capture each return code correctly with `echo RC=%ERRORLEVEL%`. In the v0.9 run, four were lost to a `cho` typo.
   - Compare each new `.idx` with the tracked baseline using `fc /b`. All six must be byte-identical (hashes in section 6).
   - Keep the byte stream inside `cmd.exe`. **Never pipe binary MPEG-2 through PowerShell**: it altered the stream during the S15 attempt.
9. **Build-output hygiene.**
   - `dir /s /b vs\*.iobj vs\*.ipdb`: report any stray `.iobj` or `.ipdb` files (there may be one left over from the v0.9 build). Do not delete without Dave's go.
   - Also run `git status --short` and `git status --short --ignored`.
10. **Package the evidence for Claude** (US-ASCII/CRLF for any text you write). Include:
    - the W1 console output;
    - `StageA_A3_v0_10_post_tokens_v0_1.csv`;
    - the four tlogs;
    - the dumpbin text files;
    - the warning comparison;
    - the SHA list;
    - frozen-hash output;
    - six-index `fc` output with return codes;
    - the `git status` outputs.

    Include **all** Claude reviews the package answers. Do **not** include stale document versions: the v0.10 package wrongly carried DR v0.10 and Plan v0.5, probably because a `*v0_10*` filename pattern matched them.
11. **Claude reviews the gate.** If it is clean, A3 v0.10 is accepted and Stage A goes to close-out (section 13).

S15 timing is **not** repeated for v0.10.

---

# 1. Document taxonomy - keep roles separate

```text
A. ChatGPT_Migration_Chat_Handover_v0_*.md            migration ChatGPT -> future migration ChatGPT (this file)
B. Claude_HANDOVER_TO_Future_Claude_Migration_Chat_v0_*.md   migration Claude -> future migration Claude
C. MPEG2_Deblocking_Developer_Handback_v0_*.md        migration -> BOTH technical-development chats
D. development-chat continuity handovers (DO NOT EDIT from migration):
   ChatGPT_Handover_To_Future_ChatGPT_MPEG2_Deblocking_Project_v0_*.md
   Claude_HANDOVER_TO_Future_Claude_Chat_v0_*.md
```

- Migration must not rewrite role-D documents unless Dave explicitly asks.
- The accidental ChatGPT development handover v0.4 is archival history only.
- Claude's own migration handover is currently `Claude_HANDOVER_TO_Future_Claude_Migration_Chat_v0_4.md`; a v0.5 may follow.

---

# 2. READING ORDER FOR THE NEW CHAT

1. this file, `ChatGPT_Migration_Chat_Handover_v0_11.md`;
2. `StageA_VS2026_MSBuild_Hard_Earned_Knowledge_v0_4.md` (durable MSBuild lessons and the reviewed 2026-10-10 policy addendum);
3. `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_10_Candidate_v0_1.md`: v0.10 is RATIFIABLE, with OPTIONAL Y1 and Y2;
4. `Claude_REVIEW_OF_ChatGPT_StageA_A3_W1_LTCGOUT_and_v0_10_Proposal_v0_1.md`: X1-X5;
5. `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_9_Post_Apply_Gate_v0_1.md`: W1-W7, and why W1 is required;
6. `Claude_check_A3_post_tokens_v0_1.py` (the W1 checker; never edit it to make it pass);
7. `StageA_A3_v0_10_Predicted_Command_Line_Delta.md`, `StageA_A3_v0_10_LTCGOUT_Correction_Record_v0_1.md` and `StageA_A3_v0_10_LTCGOUT_Toolset_Evidence_v0_1.md`;
8. `StageA_A3_pin_table_v0_9.csv`: 143 rows, including `LD_ltcgout` and `LR_ltcgout`;
9. `Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_18.md`, `StageA_Visual_Studio_Normalization_Execution_Plan_v0_13.md` (A3 gate detail in sections 27-32) and `MPEG2_Deblocking_Developer_Handback_v0_12.md`. These contain the 2026-10-10 policy and A3 v0.10 application/gate status; refresh again with final gate results at close-out (section 13);
10. Stage C decision/review record, read before future Stage C implementation:
    - `Claude_REVIEW_OF_ChatGPT_StageC_MSBuild_Discovery_Proposal_v0_3.md` (M1-M5);
    - `ChatGPT_COLD_REVIEW_OF_Claude_StageC_MSBuild_v0_3_v0_1.md` (Q1-Q6 qualifications);
    - `Claude_REVIEW_OF_ChatGPT_StageC_Disposition_and_DocSet_DR_v0_18_v0_1.md` (K1-K4);
    - `Claude_RECHECK_OF_ChatGPT_StageC_K1_K4_DocSet_v0_1.md` (K1-K4 accepted; H1 continuity fix).
11. earlier Claude reviews, consulted when a historical decision is questioned:
    - `..._v0_9_Candidate_v0_1`;
    - `..._v0_8_Candidate_v0_1`;
    - `Claude_REVIEW_OF_StageA_A3_Q1_R1_R4_Local_Evidence_Closure_v0_1`;
    - `Claude_REVIEW_OF_StageA_A3_S13_Q1_Local_Evidence_v0_1`;
    - and the earlier ones listed in handover v0.7.

Do not substitute this handover for live Git and filesystem inspection.

---

# 3. USER / WORKFLOW / BOUNDARIES

**Dave is the final authority.** The workflow:

```text
ChatGPT drafts / mechanics
    -> Claude cold review (MUST / SHOULD / OPTIONAL / NO OBJECTION, file:line, scripted checks)
    -> Dave resolves / ratifies (exact SHA-256)
    -> ChatGPT proceeds
```

**Dave's standing rules:**
- **Evidence and honesty**
  - Verify against files and cite file and line. Label anything unverified. No guessing.
  - **No defaults:** "we should not rely on default behaviours for settings since microsoft are well known for fiddling with things in their releases." Every setting is written explicitly in the project XML.
- **Safety**
  - Nothing destructive without Dave's explicit go: no GitHub rename, no deletes, no history rewrite, no force push.
  - Stop at each decision and each check.
  - Do not apply an unreviewed or unratified candidate.
- **Scope**
  - The inspector source (C/H) is **frozen**: files may move, but content may not change.
  - The inspector project configuration is in scope.
  - Migration does not redesign Stage 2 deblocking or MPEG-2 semantics.
  - Keep the old rollback tree until it is no longer needed.
- **Format**
  - Documents are US-ASCII with CRLF line endings, checked by script. BAT files are CRLF too.
  - Use ordinary interactive one-line CMD commands, with no literal `<placeholder>` text in commands Dave will paste. Interactive CMD uses `%i`; a BAT uses `%%i`.
  - Licence wording: AGPL, "version 3 or any later version" (AGPL-3.0-or-later).
- **Policy:** target performance where possible, but never at the expense of security. Target AVX2 PCs, a decade-plus installed base. This applies to both the VS2026 settings and GitHub Actions.
- **End of migration:** Dave needs a short summary of the final layout and every path that changed.

**Git practice (UPDATED, superseding v0.9's "no git add -A"):**
- Dave now uses `git add -A` for **snapshot** commits, after previewing with `git add -A --dry-run`. He commits interim "Snapshot: ..." commits routinely and pushes them as offsite backup. Follow that.
- Before any push, check that nothing personal, secret or unintended is staged. Use `git diff --cached --stat`.
- Fix unwanted files through `.gitignore`, not by hand-picking.
- Dave has added ignore entries for the two scratch folders `vs/A3_LTCGOUT_SCRATCH/` and `vs/A3_LTCG_SUPPRESS_SCRATCH/`, and for build logs in `vs/VapourSynth-mpeg2Deblock/` (`*.log`). Verify the exact lines in `.gitignore`.
  - Detailed MSBuild logs matched `C:\Users` / `USERNAME` style strings, so they are kept out of the public repository. The A3 evidence folder is **outside** the repository.
  - Previously tracked logs are unaffected by `.gitignore`. Untracking them (`git rm --cached`) is later cleanup and needs Dave's go.
- For final or Stage-close commits, still inspect: `git status --short`, `git diff --check`, `git diff --cached --name-status`.

---

# 4. REPOSITORY / PROJECT IDENTITY

```text
GitHub:            https://github.com/hydra3333/VapourSynth-mpeg2Deblock
Production tree:   E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock
Rollback tree:     E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector   (reference only; untouched)
A3 evidence root:  E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\A3_v0_7_PRE_CANDIDATE\   (outside the repo; folder name is historical)
CLI name:          Mpeg2BlockInspector
Path case:         VapourSynth-mpeg2Deblock
Solution:          vs\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock.slnx   (x64 only)
Project:           vs\VapourSynth-mpeg2Deblock\Mpeg2BlockInspector.vcxproj
```

**Tags:**
- `pre-vapoursynth-mpeg2deblock-restructure`;
- `vapoursynth-mpeg2deblock-post-restructure`;
- `pre-stageA-vs-normalization` = `b38fde11d64935db933707704b45581d5dddcde7`.

**Commits** (verify with `git log --oneline -15`):

```text
A1   d38d56d697107e7409f4baa7753bfb31b8d94747   Win32 removed (project SHA after A1: 87acd9ad1c94e5545f84fe57857c076781ca499523d2a80545919ae571dc7a57)
A2   837df123ebfe0fa083fec9d6de8969bd180f9ac0   .sln -> x64 .slnx
     b4dace033e2d6f6d0c4b505875aeae6879077324   interim docs checkpoint (README committed here)
     ab145f56fd22cf4812d1e5b3e9fbbffc1f974095   docs checkpoint
     34e8a46   Add vapoursynth include files ready for use with DLL building
     365222b   Record A3 v0.9 ratification and migration state
     <hash?>   Snapshot: A3 v0.9 applied; W1 found /LTCGOUT; v0.10 pending   (Dave's snapshot; HEAD project = v0.9, proven by today's two-line git diff)
```

**Pending policy item, not part of A3:** the five vendored VapourSynth `.h` files show `i/lf w/lf attr/` (LF endings). Decide their line-ending and `.gitattributes` policy at Stage B; do not interrupt A3 for it.

---

# 5. FROZEN / AUTHORITATIVE TECHNICAL INPUTS

Migration does not redesign MPEG-2 semantics. The controlling development documents, which must not be edited for migration:
- `docs/REPOSITORY/02_INDEX_FORMAT_SPEC.md`;
- `docs/REPOSITORY/05_DECISIONS.md`;
- `docs/REPOSITORY/06_DEBLOCK_CONCEPT.md`;
- the Stage 1 report, Stage 2 experiment design v0.3 and Proposal v0.5.

K-07 remains:
- FRAME/FIELD/NONE describes the applicable coded residual transform geometry.
- NONE applies to skipped macroblocks and to non-intra macroblocks with effective CBP=0.
- The absence of a `dct_type` bit does not by itself imply NONE.

Frozen hashes, which must stay unchanged:

```text
src\Mpeg2BlockInspector\getpic.c                 e80239cfe73a0c04490a9bf131714861254ed1d7d095b052aac616a887ef0eca
src\Mpeg2BlockInspector\mpeg2dec.c               8e6053ccb3a40be8c0d985f2e35124bf728d1f61df9b6d0c01b71e13e13b0947
tools\Stage1_Inspector_Analyzer_v0_2.py          8e0d58305ee4fe518c25b67bdbe74acc4fb392486f23e6137862d916e5e02cda
```

The project's frozen membership is 16 `.c` and 4 `.h` ClCompile/ClInclude items, unchanged since A1. Historic exe: `3edb7147001341f669b8d49be7446d79fe2d688fcff66a16f3227f80290aa5de`.

---

# 6. STAGE A BASELINE (pre-A3 checkpoint) AND SIX-INDEX HASHES

```text
VS:        C:\Program Files\Microsoft Visual Studio\18\Community
MSBuild:   18.10.1.42706       toolset v145      VC tools 14.51.36231
SDK:       10.0.28000.0 observed (deliberately unpinned; record what is used)
Checkpoint host: HostX86\x64 (PreferredToolArchitecture x86)  -> A3 policy: x64 host
Pre-A3 Debug   RC0, 20 warnings, EXE 66be0a77e21b34c9a92330c1752604b3be98d91deb6f133d37a1578361ea8bb9
Pre-A3 Release RC0, 17 warnings, EXE d31fbad88f7cade245234c3fb81832e17ec9d2024e6c638ed8a033e3cc5bc6f8
```

The authoritative index baselines are the tracked `.idx` files in Git. Their recorded SHA-256 values (Plan v0.12 section 18):

```text
TEST_2A_A001.idx         AFE51F251B2861D5C62E1629D95645C47B06F69D86F03B5FC531CF9FE3EA9273
TEST_2A_A001_blocky.idx  CBF6E8720E47E1F097E6310540D8CBD20862E3A427AD53C61D9A235ACDBA9288
TEST_4A_A003.idx         5B989CED016ADFE5CC4546F196DD63CB2DB9B431798A99203C830A98165B9A65
LG_576i_3_LP.idx         849b6a9c411a7db837268af3ac54501a06f5f1158e68d5245ce2b3ec40a0d011  (VHSC_samples\, 2,656,928 bytes)
LG_576i_4_EP.idx         11B42AADF9F46B72DEC20A8F3FDD754D07CDCE78F0460A14EDA08838336FFA87
LG_576i_5_MLS.idx        378980EA462122A02D75F412FAF9CFAF79962D503C68A8F6EE41C32B24D98D7F
```

Checkpoint command lines, which are the W1 reference in `StageA_A3_checkpoint_tokens_generated_v0_4.csv`, as 82 native-tlog tokens. The four `/errorReport` switches appear only in the detailed log, giving 86 pin rows.

```text
Debug CL:   /c /ZI /JMC /nologo /W3 /WX- /diagnostics:column /sdl- /Od /D _CRT_SECURE_NO_WARNINGS /Gm- /EHsc /RTC1 /MDd /GS /fp:precise /Zc:wchar_t /Zc:forScope /Zc:inline /Fo /Fd /external:W3 /Gd /TC /FC
Release CL: same but /Zi /O2 /MD, no /JMC, no /RTC1
LINK:       /OUT /INCREMENTAL:NO /NOLOGO <default libs> /MANIFEST /MANIFESTUAC:level='asInvoker' uiAccess='false' /manifest:embed /MANIFESTINPUT:<segmentheap> /DEBUG /PDB /SUBSYSTEM:CONSOLE [Release: /OPT:REF /OPT:ICF] /TLBID:1 /DYNAMICBASE /NXCOMPAT /IMPLIB /MACHINE:X64
```

---

# 7. RATIFIED BUILD / PRODUCT POLICY

**Both the inspector and the future plugin:**
- x64 only, `/arch:AVX2` minimum. Non-AVX2 CPUs are unsupported; the README says so.
- Security: `/GS` ON, CFG ON (compile + link), CET ON, ASLR/Dynamic Base ON, High Entropy VA ON (`/HIGHENTROPYVA` via Link `AdditionalOptions`), DEP/NX ON.
- `/favor:blend` explicit in Debug and Release (O7).
- Spectre mitigation **explicitly disabled**: `SpectreMitigation=false` in `Label="Configuration"`, and `/Qspectre` must be absent (Dave's threat-model decision).
- `/fp:precise`, with `/fp:contract` absent.

**Inspector specifics:**
- `/sdl` OFF (frozen reference-decoder exception);
- Debug `/MDd`; Release `/MT`;
- Release `/O2`, with its components `/Oi /Ot /Ob2 /GF /Gy` pinned (D1);
- Release `/GL` + `/LTCG` (plain, **not** incremental);
- Release `/PDBALTPATH:%_PDB%` (D6);
- Debug D3 (a): FavorSizeOrSpeed=Speed, InlineFunctionExpansion=AnySuitable, IntrinsicFunctions=true;
- full PDB (`GenerateDebugInformation=DebugFull`).

**Future plugin:** `/sdl` ON; Release `/MT` (D5; "hybrid" only as a fallback); the same security policy.

**Release standalone:**
- No separately installed VC/UCRT redistributable.
- Forbidden imports: `VCRUNTIME*`, `MSVCP*`, `api-ms-win-crt-*`, `ucrtbase*`, `CONCRT*`, `VCOMP*`, `MSVCR1*`. Never use a bare `MSVCR*` pattern, because it would match the system `msvcrt.dll`.
- Allowed: `KERNEL32.dll`.
- Runtime ownership: no CRT-owned memory or objects cross the `/MT` DLL boundary. VapourSynth resources go through `vsapi`.

**Toolchain and build route:**
- Toolset v145; the SDK is unpinned but recorded.
- Project files are the only source of build policy. The harness and CI invoke the build; they never inject or override flags.

**D4 = NO:** there is no A4. If an index fails, bisect with uncommitted diagnostic variants:
1. ISA (SSE2);
2. then `/MD`;
3. then remove `/GL` + `/LTCG`;
4. then the x86 host;
5. security toggles only as diagnostic evidence, never as an accepted fix.

---

# 8. HOW A3 GOT HERE (history, condensed)

1. **Q1 / R1 / R4 (closed).**
   - Every XML pin is proven against the installed v180 rule XML on rule/tool, exact name, value and placement, with the toolset folder v180 only.
   - The rule scan found 1512 definitions (v160=16, v170=743, v180=753).
   - R1 corrected `Link/ErrorReporting` to `Link/LinkErrorReporting=QueueForNextLogin`.
   - R4: expected keys are derived from the tlogs (82 + 4 = 86).
   - Properties: `LinkIncremental`, `GenerateManifest` and `LinkControlFlowGuard` go in a conditioned PropertyGroup; `/Zc:inline` = `RemoveUnreferencedCodeData`; `/Fd` = `ProgramDataBaseFileName=$(IntDir)vc$(PlatformToolsetVersion).pdb`.
   - T1: `Label="Configuration"` properties go before the `Microsoft.Cpp.props` import.
   - T2: `WholeProgramOptimization` is set in both Configuration and ClCompile.
   - T3: the default-library list is a `DELIBERATE_EXCEPTION`, proven by the import gate.
2. **v0.8** (`30999ef3...52f3`) was not ratifiable.
   - U1: the segment-heap manifest had two owners (`EnableSegmentHeap` and `Link/ManifestInput`).
   - U2: the prediction missed `/Gy- /GF- /OPT:NOREF /OPT:NOICF /LARGEADDRESSAWARE /TSAWARE`.
3. **v0.9** (`ebfcde82...f668`): two `ManifestInput` lines removed; `EnableSegmentHeap` is the single owner. Ratifiable; Dave ratified and applied it.
4. **Applied v0.9 gate**, as reported:
   - HostX64; warnings Debug 17 and Release 17;
   - `KERNEL32.dll` only; CFG (count 37, Guard Flags `10017500`), CET, HEVA, NX, ASLR, cookie; D6 file name only;
   - frozen hashes OK; six indexes byte-identical;
   - S15 one run each: 0.6527 s pre-A3 and 0.6130 s post-A3 (informational; PowerShell piping rejected).
5. **W1 on applied v0.9:** CL passed exactly, but each LINK line had one extra token, `/LTCGOUT:...\Mpeg2BlockInspector.iobj`.
   - Cause: once `LinkTimeCodeGeneration` is written explicitly, the Link task emits the `.iobj` default from `Microsoft.Link.Common.props:63`, which is conditioned only on the object-file metadata being empty.
   - The coupling is not visible in props or targets; it was recorded empirically.
   - Scratch experiment A: remove Debug `Default` and `/LTCGOUT` disappears.
   - Scratch experiment B: add the explicit empty element and `/LTCGOUT` is gone from both, with `/LTCG` kept.
6. **v0.10** (`73e9019c...db46`): v0.9 plus the two empty `LinkTimeCodeGenerationObjectFile` elements.
   - Pin rows `LD_ltcgout` / `LR_ltcgout`; 140 pin applications, 143 rows, 134 v180 targets.
   - Validators enforce both the presence and the emptiness of the value.
   - Claude found it RATIFIABLE; Dave ratified and applied it, and it is now being gated (section 0).

---

# 9. HARD-EARNED LESSONS (do not relearn)

- Do not infer project XML from switches, or effective command lines from XML. The installed v180 rule XML is the recognition authority, and placement (DataSource) is part of the setting.
- MSBuild silently ignores unknown metadata, so a wrong pin is invisible. Prove every pin.
- **Single owner:** do not add a lower-level property for a switch a higher-level setting already emits (`EnableSegmentHeap` -> `/manifestinput`).
- **Cross-property side effects exist:** setting `LinkTimeCodeGeneration`, even to `Default`, made `/LTCGOUT` appear. Judge "emits nothing" on the whole command line, mechanically (W1). Revisit the empty pin only if `/LTCG:INCREMENTAL` is ever adopted.
- **Tlogs:**
  - Native `.command.1.tlog` records are UTF-16, alternating `^` tracker keys and raw argument payloads, without `cl.exe`/`link.exe`.
  - They omit `/errorReport`.
  - Treat `/IMPLIB:<path>.lib` as a path-valued switch, not as a library.
- Pinning implicit behaviour makes switches appear (for example `/LARGEADDRESSAWARE`). Predict them.
- Never hand-maintain expected-key lists when a mechanical derivation is possible.
- **Packages:**
  - Each package must carry every Claude review it answers. Two reviews were once lost in transit.
  - Do not let filename globs pull in stale documents (Y1).
- `findstr` output is contextless, and `/m` only names files.
- The harness and CI must not become a second configuration source.
- Do not claim Stage A complete until the post-application binary and six-index gates pass and Claude has reviewed them.

---

# 10. CLAUDE REVIEW STATUS (latest first)

| Review | Verdict / open items |
|---|---|
| `Claude_RECHECK_OF_ChatGPT_StageC_K1_K4_DocSet_v0_1.md` | K1-K4 accepted in DR v0.18, Plan v0.13, Handback v0.12, Knowledge v0.4; H1 handover sections 2/10/11 repaired in this revision without changing other sections. |
| `Claude_REVIEW_OF_ChatGPT_StageC_Disposition_and_DocSet_DR_v0_18_v0_1.md` | K1 header currency, K2 addendum placement, K3 compiler wording, K4 build-environment/auto-import isolation; completed and accepted at re-check. |
| `Claude_REVIEW_OF_ChatGPT_StageC_MSBuild_Discovery_Proposal_v0_3.md` | M1-M5 policy/design accepted with ChatGPT Q1-Q6 qualifications and Dave's K3 option (a). Implementation marked UNVERIFIED pending local proof; production remains unchanged during A3. |
| `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_10_Candidate_v0_1.md` | RATIFIABLE. OPTIONAL Y1 (stale DR v0.10 and Plan v0.5 in the package) and Y2 (record that S15 was run once each, not three times). |
| `Claude_REVIEW_OF_ChatGPT_StageA_A3_W1_LTCGOUT_and_v0_10_Proposal_v0_1.md` | Agrees with the empty pins. X1 and X2 MUST (both done in the v0.10 package; X2 = the full gate, now in progress). X3-X5 SHOULD (carried). |
| `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_9_Post_Apply_Gate_v0_1.md` | W1 MUST (mechanical token check before Stage A closes). W2 SHOULD (raw PE evidence: LAA, TS Aware, PE32+, manifest). W3-W7 OPTIONAL: re-run lost RCs, S15 run count, Debug PE capture, warning-text diff, evidence folder name. |
| `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_9_Candidate_v0_1.md` | RATIFIABLE. V1: in the knowledge document, mark the segment-heap derivation as inferred until confirmed by the tlog. V2: carry Claude's current handover. |
| `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_8_Candidate_v0_1.md` | U1 MUST and U2 SHOULD, both fixed in v0.9. |

---

# 11. DOCUMENTS CURRENTLY AT THE CHATGPT END (all need a close-out refresh)

```text
Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_18.md     (current; A3 v0.10 applied, W1/HostX64 PASS) -> next v0.19 at close-out
StageA_Visual_Studio_Normalization_Execution_Plan_v0_13.md  (current; same)                    -> next v0.14 at close-out
MPEG2_Deblocking_Developer_Handback_v0_12.md                (current; same)                    -> next v0.13 at close-out
StageA_VS2026_MSBuild_Hard_Earned_Knowledge_v0_4.md         (current; same)                    -> next v0.5 at close-out
ChatGPT_Migration_Chat_Handover_v0_11.md                    (this file; H1 reconciled)        -> next v0.12 at close-out
StageA_A3_v0_9_Ratification_Record_v0_1.md, StageA_A3_v0_10_LTCGOUT_Correction_Record_v0_1.md, StageA_A3_v0_10_LTCGOUT_Toolset_Evidence_v0_1.md
```

A v0.10 ratification/application record (for example `StageA_A3_v0_10_Ratification_Record_v0_1.md`) should be written. Dave ratified `73e9019c...db46` by applying it after Claude's verdict.

---

# 12. IF THE v0.10 GATE FAILS

- **W1 token mismatch:** stop. List each token, find its owner in the v180 rules and props, propose a reviewed correction (v0.11), and send it to Claude. Never relax the checker.
- **Index difference:** use the D4 bisect order (section 7), with uncommitted variants only, then go to Claude and Dave.
- **PE or import failure:** stop. Capture the evidence and send it to Claude.
- Do not weaken security settings, AVX2 or `/MT` as an accepted fix.

---

# 13. STAGE A CLOSE-OUT (after Claude accepts the v0.10 gate)

1. **README consistency.** Compare the README claims against the accepted `.vcxproj`, the CL/LINK evidence and the dumpbin results: AVX2 required, no redistributable, `/GS` + CFG + CET, Spectre deliberately not used, AGPL, the NOTICE link. Any mismatch stops close-out.
2. **Refresh the documents** in section 11, and carry Claude's v0.10 candidate review and gate review.
3. **Git hygiene.** `git status --short` and `--short --ignored`; no unexpected tracked changes.
4. **Commit and push.** Use Dave's snapshot practice or a named close-out commit. Ask Dave whether to tag; a candidate tag name such as `post-stageA-vs-normalization` is a **suggestion only**.
5. **Later cleanup (Dave's call, may be a separate commit):**
   - previously tracked `.log` files;
   - stale review zips;
   - the scratch folders;
   - the evidence folder naming (`A3_v0_7_PRE_CANDIDATE`);
   - the vendored `.h` line-ending policy;
   - eventually the old rollback tree.

---

# 14. LATER MIGRATION STAGES (not authorized yet)

**Stage B: a VapourSynth API4 DLL placeholder** (entry point only, no algorithm). C++, x64/AVX2, Release `/MT`, `/sdl` ON, the same security policy. Also carry forward:
- `SpectreMitigation=false`;
- the empty `LinkTimeCodeGenerationObjectFile` pin whenever `LinkTimeCodeGeneration` is set;
- `EnableSegmentHeap` as the single manifest owner, if used;
- the runtime-ownership rule.

Open decisions:
- the coupled naming and package-identity set;
- the C++ standard;
- the header/API profile and vendored headers;
- FP/FMA;
- COMDAT;
- the version resource;
- O8 `/guard:ehcont` (`GuardEHContMetadata` exists in v180 `cl.xml`);
- an optional runtime CPU check.

**Stage C:** a canonical VS2026 build harness: vswhere plus same-install MSBuild on the umbrella `.slnx`, with no flag injection. It verifies command lines, including "no `/LTCGOUT`".

**Stage D:** a GitHub release workflow calling the same harness, with no `cl` flag map. Re-verify the hosted runner's capability at implementation time.

**Stage E:** the wheel/PyPI scaffold (`py3-none-win_amd64`, layout like CNR3's `vapoursynth/plugins/<name>/<name>.dll`).
- Metadata must say AGPL-3.0-or-later; never copy CNR3's MIT metadata.
- Include LICENSE and NOTICE.
- Publication needs Dave's explicit authorization.

**Then:** the final handback review and the migration final summary for Dave.
