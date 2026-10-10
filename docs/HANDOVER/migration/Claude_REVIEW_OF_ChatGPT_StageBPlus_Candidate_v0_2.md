# Claude review - Stage B+ candidate v0.2 (diff check)

File: Claude_REVIEW_OF_ChatGPT_StageBPlus_Candidate_v0_2.md
Version / date: v0.1 / 2026-10-10
Author: Claude (migration chat, independent reviewer)
Reviewed: StageBPlus_CANDIDATE_FOR_CLAUDE_v0_2.zip (10 files plus PACKAGE_SHA256.txt), diffed against v0.1 and against the accepted A3 v0.10 inspector (73e9019c...db46).
Scope: diff check only, as agreed. Q1 and Q2 are closed by Migration_Status v0.5 (O2 is ON for both projects; O4 keeps Large Address Aware on both).

## 1. Verdict

READY FOR DAVE TO RATIFY AND APPLY, then run gates A to F locally. Nothing here is built or proven yet.

## 2. Checks

- SHA-256: 10/10 OK. All files are ASCII with CRLF line endings, no bare LF, no BOM.
- Unchanged from v0.1, byte for byte: `.slnx`, `.filters`, `plugin.cpp`, `plugin_version.h`, `mpeg2Deblock.rc`.
- The changes are only the project files, the README and the diffs.

| Item | Fixed? | Where (v0.2) |
|---|---|---|
| B1 native EHCONT, both projects | Yes. `GuardEHContMetadata=true` is inside ClCompile; `LinkGuardEHContMetadata=true` is in the conditioned PropertyGroup next to `LinkControlFlowGuard`, not inside `<Link>`. `/guard:ehcont` is removed from all eight `AdditionalOptions`. | inspector lines 53, 59, 75, 144; DLL lines 54, 60, 74, 144 |
| B2 DLL preprocessor definitions | Yes. Debug `NOMINMAX;_DEBUG;_WINDOWS;_USRDLL`, Release `NOMINMAX;NDEBUG;_WINDOWS;_USRDLL` | DLL lines 64, 134 |
| B3 `SubSystem=Windows` | Yes, both configurations | DLL lines 116, 186 |
| B4 `EnableUAC=false` | Yes, both configurations | DLL lines 122, 192 |
| B5 resource compiler pins | Yes. A ResourceCompile block in each configuration's ItemDefinitionGroup (`_DEBUG` or `NDEBUG`, `0x0409`, nologo); the README's gate C adds `rc.command.1.tlog` | DLL lines 105-109, 175-179 |
| B6 RTTI, plus the C++ token audit | Yes. `RuntimeTypeInfo=true` in both configurations; the README's gate C audits every CL, LINK and RC token | DLL lines 92, 162 |
| N1-N3 | Recorded in the README (lines 57-59) | - |

- The inspector against A3 v0.10 now differs only in:
  - the two `PlatformToolset` lines;
  - two `LinkGuardEHContMetadata` lines;
  - two `GuardEHContMetadata` lines;
  - the guard target.
  Nothing else changed. The inspector `.filters` file is untouched.

## 3. Reminders for the local gate (already in the README)

- A: probe the toolset guard in a scratch copy with `v145` (pass), `v143` (fail), `v150` (pass), `vX` (fail) and empty (fail).
- B: `/guard:ehcont` must appear on the actual CL **and** LINK lines. Record any LNK4291 warnings. Show the EH Continuation table and its count for both binaries; the count may be 0. The Guard Flags will change from 10017500.
- C: compare the inspector with A3, so only the toolset and EHCONT tokens change. Capture the DLL's CL, LINK and RC switches and reconcile every token.
- D: dumpbin checks on both binaries, the DLL export `VapourSynthPluginInit2`, the DLL's embedded manifest (no UAC), and VERSIONINFO.
- E: `core.mpeg2deblock.Identity(core.std.BlankClip())` returns a frame.
- F: all six inspector indexes, locally (O7).
