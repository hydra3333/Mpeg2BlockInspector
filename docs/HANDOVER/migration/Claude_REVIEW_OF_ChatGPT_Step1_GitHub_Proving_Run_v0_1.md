# Claude review - Step 1 GitHub Actions proving run

File: Claude_REVIEW_OF_ChatGPT_Step1_GitHub_Proving_Run_v0_1.md
Version / date: v0.1 / 2026-10-10
Author: Claude (migration chat, independent reviewer)
Reviewed: Step1_GitHub_Proof_Claude_Gate_Review_v0_1.zip (18 files, all SHA-256 in
PACKAGE_SHA256.txt verified), including ChatGPT_Step1_GitHub_Proving_Run_Gate_Review_v0_1.md.
Compared against: accepted local A3 v0.10 evidence (A3_v0_10_POST_APPLY_GATE).

## 1. Verdict

ACCEPT the Step 1 gate. The "project files own every setting, CI only drives MSBuild"
approach is proven on GitHub's windows runner. I agree with ChatGPT's assessment, with one
addition (section 4): the cause of the binary difference can be identified from the
evidence, and it has a policy consequence for Dave to decide (D-SDK, section 5).

## 2. What I checked independently

| Check | Result | Evidence |
|---|---|---|
| Package integrity | PASS, 18/18 SHA-256 | PACKAGE_SHA256.txt |
| Switches vs A3 (113 tokens, per key, same order) | PASS 33/23/32/25; only `/manifestinput:` vs `/MANIFESTINPUT:` case differs (LINK compare is case-insensitive) | actual_switches.csv vs A3 CSV |
| MSBuild is 64-bit at run time | PASS, MSBUILD_IS64=True | msbuild-bitness.txt |
| Compiler/linker host | HostX64\x64 only | job-logs.txt lines ~400-406 |
| Toolset | MSVC 14.51.36231, CL 19.51.36260.0, LINK/DUMPBIN 14.51.36260.0 = Dave's | tool_versions.txt |
| Warnings | Debug 17, Release 17; the set of (file, line, code) is identical to Dave's for both | runner MSBuild_*_diagnostic.log vs StageA_A3_v0_10_*_x64.log |
| Imports | KERNEL32.dll only; imported names identical and in the same order | Release_imports.txt |
| Guard CF | Function count 37, Guard Flags 10017500, CF function table identical by name (addresses masked) | Release_loadconfig.txt lines 67-126 |
| Manifest | identical | Release_embedded_manifest.xml |

## 3. Differences found (all from the same cause)

- Code size 28C00 -> 28800, initialised data 16E00 -> 16A00, exception directory
  1BD8 -> 1BC0, .text/.rdata sizes, and shifted addresses in the load-config tables.
- The Volatile Access RVA Table is much longer locally (load-config lines 137-322 local vs
  137-172 runner).
- Some UCRT-internal symbols appear only in Dave's build, e.g. `__acrt_FlsGetValue2`,
  `__acrt_app_verifier_enabled`, `_set_fpcsr`.

## 4. Cause (my addition)

Under `/MT` the static C runtime is linked into the EXE. The UCRT part of it (libucrt.lib)
ships with the Windows SDK, not with MSVC:

- runner link LIB path: `Windows Kits\10\lib\10.0.26100.0\ucrt\x64`
  (MSBuild_Release_x64_diagnostic.log)
- Dave's link LIB path: `Windows Kits\10\lib\10.0.28000.0\ucrt\x64`
  (StageA_A3_v0_10_Release_x64.log)

Every symbol-level difference I found is in UCRT code (`__acrt_*`), and the program's own
CF targets, imports, entry point RVA (EDE0) and guard settings match. So the different SDK
contributed different static UCRT code to the EXE.

Label: strongly supported inference, NOT proven byte-for-byte. The EXE is not in the
artifact, so I cannot show that the program's own code is identical.

## 5. Consequence and decision for Dave (D-SDK)

The Windows SDK is not just headers for us: with `/MT` it puts code into the binary. That
applies to the plugin DLL as well. Today the SDK is "unpinned and recorded" (D2), but a
change of SDK does not trigger the six-index regression; only a toolset or compiler change
does.

Options:
- (a) Recommended: treat the SDK like the compiler (same shape as K3 (a)). Use the newest
  installed released SDK, record its version on every build, and if it differs from the
  last accepted build, the switch check, warning comparison and six-index regression must
  all pass again before that build is accepted.
- (b) Pin `WindowsTargetPlatformVersion` in the project files. Not recommended: it breaks
  version independence, and the runner image may not have Dave's SDK installed.
- (c) Record only, as today. Not recommended: a code-changing input would then go
  unchecked.

## 6. Small items for Step 3 (not blocking)

- S4: also upload the Release EXE and PDB in the proof artifact. This allows byte
  comparison and lets the six-index check run on the CI binary later. Cheap.
- S5: workflow line 1 still says "CANDIDATE v0.2 ... not run on GitHub yet". Fix it in the
  final workflow.
- S6: Node 20 deprecation notices for actions/checkout@v4 and actions/upload-artifact@v4.
  Move to the current major versions in Step 3. Unverified: I have not checked which
  versions use Node 24; confirm on the actions' release pages.
- The log names `*_diagnostic.log` hold detailed verbosity, as ChatGPT notes. Cosmetic.

## 7. Agreements with ChatGPT's review

- The binaries are not identical. No claim of identical code is made.
- There is no new six-index result. A3 stays WAIVED, not PASS.
- No change to the expected-switch reference is needed.
- Stage B+ waits for Dave's acceptance of Step 1.
- Update only Migration_Status.md (P1). There is no document cascade.

One count to check: I matched the import names one by one and they are identical in the
same order. My parser counted 77 names; ChatGPT says 81. The difference is a parsing
matter, not a difference between the builds.
