# Stage A Visual Studio Normalization Execution Plan



**Filename:** `StageA_Visual_Studio_Normalization_Execution_Plan_v0_14.md`
**Version:** 0.14
**Date:** 2026-10-10 (Stage A A3 v0.10 accepted by Dave; close-out documentation review)
**Drafted by:** migration ChatGPT chat
**Reviewed against:** `Claude_REVIEW_OF_ChatGPT_StageA_Audit_Proposal_v0_2.md`, `Claude_REVIEW_OF_ChatGPT_StageA_Checkpoint_Status_v0_1.md`, `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_2_Package_v0_1.md`, `Claude_REVIEW_OF_ChatGPT_Migration_Plan_Update_Standalone_PyPI_v0_1.md`, `Claude_REVIEW_OF_ChatGPT_DR_v0_8_and_StageA_Plan_v0_3_v0_2.md`, `Claude_REVIEW_OF_ChatGPT_DR_v0_10_and_StageA_Plan_v0_5_v0_1.md`, `Claude_REVIEW_OF_ChatGPT_Migration_Docs_and_Handover_Taxonomy_v0_1.md`, `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_4_PreCandidate_and_DR_v0_12_v0_1.md`, and `Claude_REVIEW_OF_ChatGPT_NoSpectre_DR_v0_13_A3_v0_5_v0_1.md`
**Controlling migration design:** `Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_19.md` (Stage A close-out review version)
**Execution status:** A3 v0.10 accepted by Dave; rebuild/W1/HostX64/warnings/W2/hashes/frozen checks/hygiene PASS. Section-30 six-index regression WAIVED for v0.10 only, not PASS. Stage A close-out pending README live check, Claude document review, Git commit/push.
**Scope:** Stage A only - inspector project normalization, PE/default pinning, standalone Release EXE linkage, and umbrella `.slnx`.
**Does not authorize:** Stage B DLL placeholder work or Stage 2 technical implementation.

---

## Stage A close-out acceptance and explicit Plan section 30 deviation (2026-10-10)

**Decision authority:** Dave. **Gate:** A3 v0.10 ACCEPTED; Stage A proceeds to
close-out. This does not mean repository documentation has been committed or
pushed. This close-out update supersedes earlier *in-progress* gate status in
the historical sections below. The production `.vcxproj` remains unchanged.

**Ratified and applied A3 v0.10 identity:** `Mpeg2BlockInspector.vcxproj` SHA-256
`73e9019cda7d1061ecdb06526c60f4ee84baa4c385b7ca0dde4269544e4fdb46`.
Windows working-copy `.slnx` SHA-256:
`fa24efcd73401a38604e2f4228b07d8b960abcbfb66da22c02908e9d1cdb0754`.
Debug EXE SHA-256:
`df92319fc0d39d9b09d8de82dd059324adca0eedae8f5e404aa6460d8cd1a0cc`.
Release EXE SHA-256:
`fc168013f74074e3921dc781f6b2db69a9e67f7df80396dd2ab1fcc146c1ad48`.
These are reported from Dave's machine; the executable hashes were not
independently recomputed from the evidence ZIP.

**Completed gate results:** Both Debug and Release clean rebuild RC=0;
W1 content-checker RC=0 with Debug CL 33, Release CL 32, Debug LINK 23,
Release LINK 25; native logs prove HostX64\x64 CL and LINK. v0.9-to-v0.10
warning signatures matched: 17 Debug and 17 Release, with no new warnings.
W2 Release PE/security/import/manifest PASS: x64 PE32+, LAA, HEVA, ASLR,
NX, CFG with 37 function-table entries, CET, nonzero security cookie,
Terminal Server Aware, basename-only PDB path, KERNEL32.dll-only imports,
embedded asInvoker/SegmentHeap manifest. Production project and solution
hashes matched expected identities. Three frozen-file SHA-256 values and the
Git comparison passed; no more source audits are authorised absent a new
specific cause. Last reported Git status was clean, with eight expected
ignored paths and no `.iobj`/`.ipdb`. External evidence ZIP captured.

**Dave-ratified deviation from Execution Plan section 30:** Section 30
says "No representative subset or waiver is allowed." Dave specifically
ratified option (b) on 2026-10-10, making one bounded exception for the
A3 v0.10 six-index rerun. Its status is **WAIVED**, explicitly **NOT PASS**.
The v0.9 six-index regression previously PASSED; it was NOT rerun for v0.10.
The rationale, attributed by Dave to
`Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_10_Final_Gate_v0_1.md`, section 3:

1. v0.10 and v0.9 CL command lines are identical (W1 token sets and
   same-size CL tlogs); the v0.9 executable passed all six index cases.
2. The sole LINK difference is removal of `/LTCGOUT`, applicable to
   incremental LTCG, while ordinary `/LTCG` remains enabled.
3. Comparing the v0.9 and v0.10 Release `dumpbin /headers`, `/loadconfig`
   and `/imports` after masking timestamps, PDB GUID and dump path produces
   zero differences. This covers code size, entry point, section layout,
   Guard CF function count (37), Guard Flags and imports.

Together these constitute **strong evidence of identical code generation,
not byte-for-byte proof**. Do not relabel the waiver PASS or weaken the
future rule: whenever the MSVC toolset, exact compiler version or any
code-generation-relevant setting changes, the six-index regression is
mandatory before acceptance. Permanent CL/LINK switches, HostX64 and
Release-only KERNEL32 import checks also remain required for every harness
or CI build. The waiver does not authorise a general exception to section 30.

**Stage C/D carry-forward from Claude final-gate review v0.1, section 4
(N1-N4; OPTIONAL review notes, not additional A3 gate conditions):**

- **N1 - command-line tokenisation:** On non-Windows, the existing
  `extract_StageA_A3_checkpoint_tlog_tokens_v0_4.py` fallback
  `shlex.split(posix=False)` incorrectly splits quoted Windows command lines,
  including `/MANIFESTUAC:"level='asInvoker' uiAccess='false'"` and
  paths containing spaces. Claude initially obtained 117 tokens and a
  false FAIL; Windows-rules tokenisation obtained the correct 113-token CSV.
  Dave's Windows runs used `CommandLineToArgvW` and are valid. For Stage C/D,
  implement correct Windows command-line splitting on every supported
  platform or fail closed on non-Windows; do not accept a false failure or
  silently rewrite the expected token set.
- **N2 - actual tool invocations:** `HostX86` appears 34 times in each
  detailed log as `Microsoft.Cpp.Common.props` property-reassignment
  messages. A global text search for that string falsely rejects a valid
  HostX64 build. Verify actual `...\bin\HostX64\x64\CL.exe` and
  `...\bin\HostX64\x64\link.exe` *invocation* lines in both
  configurations; distinguish them from informational property lines.
- **N3 - two version identities:** The MSVC tools installation folder
  contains `14.51.36231`, while the selected x64 `dumpbin` reports its
  executable file version as `14.51.36260.0`. Record the actual toolset
  directory version and the relevant tool executable's file version,
  with executable path and provenance, on every Stage C/D build. These
  numbers are not interchangeable. Claude's suggestion that folder/file
  versions commonly differ, and that the two come from one installation,
  remains unverified on Dave's machine until Stage C establishes it.
- **N4 - Guard Flags interpretation:** Withdraw unsupported bit-by-bit
  decoding of hex Guard Flags `10017500` from Claude's earlier v0.9 review.
  The evidence directly identifies only `CF instrumented` and
  `FID table present`; `dumpbin` reports zero long-jump targets. The
  accepted CFG criteria are presence of the Guard CF function table and
  a nonzero function count (37), which PASS. Do not infer additional
  protection states solely by reading undecoded bits in this value.

**Provenance:** `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_10_Final_Gate_v0_1.md`,
section 4, now included byte-for-byte in this review package. N1-N4 are
future Stage C/D engineering constraints and corrections, not evidence of
work already implemented or tested there. Anything explicitly marked
unverified remains unverified until proven on Dave's machine.


**Close-out boundary:** README consistency comparison against the accepted
build is documented in `README_CONSISTENCY_ASSESSMENT_v0_1.md`. The available
README is an attached repository ZIP snapshot; confirm the live Windows
working-copy README before final commit. This document set is for Claude's
review. After review, re-run `git status`, stage only intended files, inspect
`git diff --cached`, commit, push, verify the remote commit, and ask Dave
whether an optional tag is wanted. None of these repository mutations has
been performed by ChatGPT. Stage B/C/D implementation is not authorised by
accepting this documentation alone.

---

### Execution disposition

For A3 v0.10, interpret the six-index entry in this Plan's older Stage A
PASS checklist as **WAIVED by Dave**, not PASS, and not an omission. This
specific waiver takes precedence over section 30's general prohibition for
one candidate only; the rest of section 30 continues unchanged. The next
actions are README verification, documentation review, final Git inspection,
commit, push and optional-tag question. There is no A4.


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
- HISTORICAL 2026-10-10 pre-final-gate status (superseded by the accepted A3 close-out section above): warning/W2/hash/waiver review had not yet completed. These checks are now resolved as recorded in the first section; do not rerun them as a result of this historical text.
- On this user's Windows working copy, agreed `.vcxproj`/`.slnx` SHA-256 hashes are for the CRLF file representation. GitHub ZIP LF representations can legitimately differ. Confirm paths and bytes locally; the ZIP is reference/layout only.

### Execution sequencing and gates

HISTORICAL pre-final-gate sequence (superseded): all specified checks were subsequently completed except the v0.10 six-index rerun, specifically WAIVED by Dave (not PASS); do not repeat them. Current work is README live verification, review, and Git close-out.

AFTER Claude approves A3 and Stage A closes: README consistency, versioned records and handback, Git close-out, then a distinct reviewed proposal for floating toolset and newest build selection.

STAGE B: begin x64-only DLL placeholder with `PreferredToolArchitecture=x64`, Release `/MT`, `/sdl` ON and established security/AVX2 policy.

STAGE C: one vswhere discovery, x64 MSBuild runtime proof, clean environment, project settings as sole flag source, permanent CL/LINK token, HostX64 and import gate; separately record toolset/build/SDK/product. Collect on-machine evidence for all UNVERIFIED items before acceptance.

STAGE D: invoke exactly Stage C's verified harness on x64 runners; no independent discovery or flag map. On any toolset or compiler-build change, rerun warning and six-index gates before accepting build artifacts.

### K4: automatic imports and response files (binding for Stage C/D)

- Fail closed if any `Directory.Build.props`, `Directory.Build.targets`, or `Directory.Build.rsp` exists in a repository ancestor directory, from the repository parent through filesystem root; also reject unreviewed occurrences within the repository that may affect a build. Log the checked paths and results.
- Launch MSBuild with `-noAutoResponse` so implicit MSBuild response files do not silently inject switches (including applicable `MSBuild.rsp` and `Directory.Build.rsp`). Validate the precise MSBuild 18.x response-file behavior locally; any uncertainty is an unverified Stage C gate item.
- Prove the guard experimentally once using a disposable scratch project and a scratch `Directory.Build.props` in its ancestor directory. Confirm the harness refuses to build, then remove the scratch file. Never create this probe in or above the production repository. Record command, output, and return code.
- The guard is additive to environment-property checks, including `PreferredToolArchitecture`, `CL`, `_CL_`, `LINK`, `_LINK_`, `Platform`, and relevant MSBuild/global-property override mechanisms. No build-policy injection through environment, response files or auto-imports is permitted.

### K3: compiler build designated by Visual Studio

- No project-level `VCToolsVersion` override: the designated current build is **recorded, not pinned**. Any change relative to last accepted compiler/toolset triggers command-switch, warning, and six-index rerun before acceptance. The exact selection rules and `DefaultPlatformToolset` implementation remain UNVERIFIED until local Stage C/post-A testing.
- `-latest`, without `-prerelease`, selects the newest **released** qualifying installed Visual Studio. Keeping the build machine updated is an operator responsibility; discovery does not install updates. Build Tools are eligible via `-products *`, and the selected product must be logged.

---

## 0A. Immediate execution boundary

Current sequence is now:

```text
A3 v0.8 cold review COMPLETE
    ->
U1/U2 corrective v0.9 PREPARED
    ->
Dave-local v0.9 assembler + all LOCAL validators
    ->
Claude short v0.9 diff/SHA cold review
    ->
Dave ratifies exact v0.9 SHA
    ->
apply exact candidate
    ->
full A3 build / tlog / dumpbin / imports / six-index gate
```

v0.9 project-file delta from v0.8 is intentionally only:

```text
remove Debug Link/ManifestInput
remove Release Link/ManifestInput
```

`Manifest/EnableSegmentHeap=true` remains in both configurations as the single owner.

The post-A3 linker tlog must contain exactly one effective `/manifestinput:` resolving to `segmentheap.manifest`.

Claude U2 is carried in `StageA_A3_v0_9_Predicted_Command_Line_Delta.md`.

Do not apply v0.9 until Claude accepts it and Dave ratifies SHA-256:

```text
ebfcde82405fd2dc25aa7a14a160f89375465d545927b3e4583e7a40fd1af668
```

---


## 0B. Ratified application boundary

Accepted candidate:

```text
Mpeg2BlockInspector_A3_APPLYABLE_CANDIDATE_v0_9.vcxproj
SHA-256 ebfcde82405fd2dc25aa7a14a160f89375465d545927b3e4583e7a40fd1af668
```

Claude verdict:

```text
Ratifiable; U1 and U2 fixed; no new MUST or SHOULD.
```

Dave ratified this exact SHA on 2026-10-10.

Current published repository baseline before application:

```text
34e8a46 Add vapoursynth include files ready for use with DLL building
```

Application must be byte-for-byte. The production project must hash to the exact ratified SHA before any A3 build is accepted.

Post-A3 command-line proof must include exactly one segment-heap `/manifestinput:` resolving to `segmentheap.manifest`. This will also confirm the previously inferred `EnableSegmentHeap` ownership mechanism.


## 1. Purpose

This document is the operational runbook for Stage A.

It converts the migration design and Claude's accepted/revised Stage A review into a bounded execution sequence:

```text
A1 COMPLETE
    ->
A2 COMPLETE
    ->
mandatory pre-A3 checkpoint COMPLETE
    ->
revised consolidated A3 proposal
    ->
Claude cold review
    ->
Dave ratification
    ->
A3 application + complete normalization/standalone/six-index gate
    ->
Stage A close-out
```

No step may silently collapse into the next.

---

## 2. Current execution boundary

Current state:

```text
A1: APPLIED/COMMITTED - d38d56d697107e7409f4baa7753bfb31b8d94747
A2: APPLIED/COMMITTED - 837df123ebfe0fa083fec9d6de8969bd180f9ac0
.slnx Visual Studio load: PASS
Pre-A3 Debug/Release checkpoint: PASS
Pre-A3 six-index regression: PASS
M3 dumpbin measurement: COMPLETE

A3 v0.1: REVIEW HISTORY ONLY - DO NOT APPLY
A3 v0.2 DRAFT candidate a59788b4...108a: REVIEW HISTORY ONLY - DO NOT APPLY
A3 v0.3 DRAFT candidate `d7c6085f462927daa5e8f5128dac0b3e1f0d202f116b0ca9c8c4ca315bf51567`: REVIEW HISTORY ONLY - DO NOT APPLY
Superseding A3 candidate: NOT YET GENERATED; must carry AVX2/security policy

D4 = NO: Release /MT is part of A3; no A4
D5 = YES: future plugin DLL Release /MT
D6 = YES: Release /PDBALTPATH:%_PDB%
CPU policy: x64 + AVX2 minimum for both projects, Debug + Release
Security policy: /GS + CFG + CET enabled in Debug and Release; Spectre mitigation deliberately not used
SDL policy: inspector OFF as frozen reference-decoder exception; plugin ON
```

The current review inputs are Claude's Stage A audit review, checkpoint closure, A3 v0.2 package review, and migration-plan update review.

---

### Documentation consistency guard

`README.md` was committed in the interim migration checkpoint while the then-current policy still required Spectre-mitigated libraries. Dave subsequently removed Spectre mitigation from the required build policy. The README must therefore be corrected to retain Windows x64 + AVX2, standalone Release runtime and project-file-owned settings while removing the Spectre-library prerequisite.

The README was included in commit `b4dace033e2d6f6d0c4b505875aeae6879077324`. N4 option (a) is now chosen: commit the corrected no-Spectre README now. Until A3 passes, its AVX2 and standalone-runtime statements remain ratified target policy rather than gate evidence.

At Stage A close-out, compare README claims against the accepted `.vcxproj`, exact CL/LINK evidence and `dumpbin`/dependency results. Any mismatch stops documentation close-out.

`NOTICE.md` is not rewritten merely because build settings change. It remains the repository notice/attribution/restricted-test-media reference.

## 3. General execution rules

Throughout Stage A:

- work only in the active repository:
  ```text
  E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock
  ```
- do not modify frozen C/H source;
- do not use `git add -A`;
- use named Git staging only;
- do not apply LF review `.diff` files to CRLF project files;
- apply accepted project/solution candidates by byte copy and verify SHA-256;
- do not open the old `.sln` between A1 and A2;
- do not push until the agreed Stage A gate passes unless Dave explicitly changes that rule;
- stop on unexplained build, warning, index, SHA or tracked-file changes;
- use exact pasted command output as evidence rather than assumptions;
- the `.vcxproj` / `.slnx` files are the source of compile/link/runtime settings;
- neither the Stage C harness nor the final GitHub workflow may inject `/MT`, `/arch:AVX2`, `/favor:blend`, CFG/CET/`/GS`/SDL settings, override `PlatformToolset`, or maintain a second compile/link flag map;
- standalone Release linkage, AVX2 minimum target and security hardening must be encoded in the project file itself and merely verified by harness/CI.

---

# A1 - REMOVE WIN32 CONFIGURATIONS

## 4. A1 accepted candidate

Candidate:

```text
Mpeg2BlockInspector_A1_x64only_DELETIONS_ONLY.vcxproj
```

Accepted SHA-256:

```text
87acd9ad1c94e5545f84fe57857c076781ca499523d2a80545919ae571dc7a57
```

Pre-A1 tracked project SHA-256:

```text
e383cbce4eaae1ab5953aa6334d433ea1af4d977c8eae9a2db8699c6c658375f
```

Claude independently verified:

```text
58 deletions
0 insertions
0 retained-line rewrites
```

and verified that:

```text
<Keyword>Win32Proj</Keyword>
```

and the existing `ProjectGuid` remain.

---

## 5. A1 pre-check

From repository root:

```bat
git status -sb
git status --short
```

Expected:

```text
clean working tree
main aligned with the intended pre-A1 migration checkpoint
```

If not clean, stop and identify the difference before continuing.

Verify current tracked project:

```bat
certutil -hashfile "vs\VapourSynth-mpeg2Deblock\Mpeg2BlockInspector.vcxproj" SHA256
```

Expected:

```text
e383cbce4eaae1ab5953aa6334d433ea1af4d977c8eae9a2db8699c6c658375f
```

If it differs, stop.

---

## 6. Apply A1

Copy the accepted candidate byte-for-byte over:

```text
vs\VapourSynth-mpeg2Deblock\Mpeg2BlockInspector.vcxproj
```

Do not use the review `.diff`.

Immediately verify:

```bat
certutil -hashfile "vs\VapourSynth-mpeg2Deblock\Mpeg2BlockInspector.vcxproj" SHA256
```

Required result:

```text
87acd9ad1c94e5545f84fe57857c076781ca499523d2a80545919ae571dc7a57
```

Then inspect:

```bat
git diff -- "vs\VapourSynth-mpeg2Deblock\Mpeg2BlockInspector.vcxproj"
git diff --numstat -- "vs\VapourSynth-mpeg2Deblock\Mpeg2BlockInspector.vcxproj"
```

Required numstat character:

```text
0 insertions
58 deletions
```

No retained x64 line should be rewritten.

---

## 7. Commit A1

Named staging only:

```bat
git add "vs\VapourSynth-mpeg2Deblock\Mpeg2BlockInspector.vcxproj"
git diff --cached --check
git diff --cached --stat
git diff --cached -- "vs\VapourSynth-mpeg2Deblock\Mpeg2BlockInspector.vcxproj"
```

Commit message recommendation:

```bat
git commit -m "Remove Win32 inspector configurations"
```

Then:

```bat
git status --short
git log -1 --oneline
```

Do NOT open Visual Studio.

Proceed directly to A2.

---

# A2 - REPLACE .SLN WITH X64-ONLY .SLNX

## 8. A2 accepted candidate

Candidate:

```text
VapourSynth-mpeg2Deblock_A2_PROPOSED.slnx
```

Accepted SHA-256:

```text
fa24efcd73401a38604e2f4228b07d8b960abcbfb66da22c02908e9d1cdb0754
```

Accepted content:

```xml
<Solution>
  <Configurations>
    <Platform Name="x64" />
  </Configurations>
  <Project Path="Mpeg2BlockInspector.vcxproj" Id="f4b1a357-b93c-7aab-3946-9c7a95523c9b" />
</Solution>
```

---

## 9. A2 pre-checks

Before changing the solution:

```bat
git grep -n "Mpeg2BlockInspector.sln"
```

Review every occurrence.

Distinguish:

```text
current executable/build scripts that require change
historical documentation/evidence that should retain old names
```

Do not blindly replace historical references.

Check `.gitignore` for `.slnx` handling:

```bat
git check-ignore -v "vs\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock.slnx"
```

Expected:

```text
no output
```

If the proposed `.slnx` is ignored, stop and fix the ignore-policy issue before A2.

---

## 10. Apply A2

Remove old tracked solution:

```bat
git rm "vs\VapourSynth-mpeg2Deblock\Mpeg2BlockInspector.sln"
```

Copy the accepted candidate to:

```text
vs\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock.slnx
```

Verify:

```bat
certutil -hashfile "vs\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock.slnx" SHA256
```

Required:

```text
fa24efcd73401a38604e2f4228b07d8b960abcbfb66da22c02908e9d1cdb0754
```

Stage by name:

```bat
git add "vs\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock.slnx"
```

Inspect:

```bat
git status --short
git diff --cached --check
git diff --cached --stat
git diff --cached
```

Expected A2 staged change:

```text
delete old Mpeg2BlockInspector.sln
add VapourSynth-mpeg2Deblock.slnx
```

No project-file setting change belongs in A2.

---

## 11. Commit A2

Recommended:

```bat
git commit -m "Replace inspector solution with x64 slnx"
```

Then:

```bat
git status --short
git log --oneline -2
```

The working tree should be clean.

Only now may Visual Studio be opened.

The first Visual Studio solution opened after A1/A2 must be:

```text
vs\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock.slnx
```

---

# PRE-A3 CHECKPOINT

## 12. Purpose of the checkpoint

A1 and A2 are intended not to alter x64 build behavior.

The checkpoint therefore becomes the authoritative measurement of:

```text
effective pre-A3 compiler behavior
effective pre-A3 linker behavior
effective defaults currently supplied by VS2026/MSBuild
warning baseline
actual SDK/toolchain
functional six-index baseline after A1/A2
```

A3 v0.2 will be derived from this evidence.

Do not construct A3 v0.2 from memory of Microsoft's defaults.

---

## 13. Discover MSBuild

Use `vswhere`.

The exact final discovery form must use the same product/component selection criteria as later Visual Studio discovery.

Candidate:

```bat
set "VSWHERE=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"

for /f "usebackq tokens=*" %%i in (`"%VSWHERE%" -latest -products * -requires Microsoft.Component.MSBuild Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -find MSBuild\**\Bin\MSBuild.exe`) do set "MSBUILD=%%i"

if not defined MSBUILD (
    echo ERROR: MSBuild not found.
    exit /b 1
)

echo MSBUILD=%MSBUILD%
```

Record the actual resolved path.

If this exact command fails on Dave's machine, diagnose the discovery syntax before substituting a hard-coded MSBuild path.

---

### N5 / P6 prerequisite-script requirements

The A3 prerequisite BAT uses CRLF. It selects one `VSINSTALL` with accepted `vswhere` criteria and derives or positively verifies `MSBuild.exe` underneath the same installation root. Mismatch is fatal. Spectre components are not required.

## 14. Checkpoint build logs

From:

```text
vs\VapourSynth-mpeg2Deblock
```

build the new umbrella solution.

Debug:

```bat
"%MSBUILD%" "VapourSynth-mpeg2Deblock.slnx" /m /t:Clean;Build /p:Configuration=Debug /p:Platform=x64 /v:detailed > "StageA_checkpoint_Debug_x64.log" 2>&1
```

Release:

```bat
"%MSBUILD%" "VapourSynth-mpeg2Deblock.slnx" /m /t:Clean;Build /p:Configuration=Release /p:Platform=x64 /v:detailed > "StageA_checkpoint_Release_x64.log" 2>&1
```

Capture each `%ERRORLEVEL%` immediately in the actual execution harness/commands.

Both must succeed.

If desired, also create MSBuild binary logs:

```text
/bl:StageA_checkpoint_Debug_x64.binlog
/bl:StageA_checkpoint_Release_x64.binlog
```

The text/detailed log remains required for direct review unless another extraction method is agreed.

---

## 15. Extract effective compiler/linker state

For both Debug and Release record:

```text
exact cl.exe command line
exact link.exe command line
cl.exe path/version if available
link.exe path/version if available
MSBuild path/version
platform toolset evidence
actual Windows SDK version
```

This measurement is the authority for A3 explicit pinning.

Output-affecting switches that appear only because of toolchain defaults must be identified.

Candidate categories include:

```text
RuntimeLibrary
BufferSecurityCheck
BasicRuntimeChecks
SupportJustMyCode
CharacterSet
CompileAs
LanguageStandard_C
EnableEnhancedInstructionSet
Optimization
FavorSizeOrSpeed
InlineFunctionExpansion
IntrinsicFunctions
DebugInformationFormat
FloatingPointModel
FunctionLevelLinking
WholeProgramOptimization
LinkTimeCodeGeneration
EnableUAC
UACExecutionLevel
RandomizedBaseAddress
DataExecutionPrevention
TargetMachine
LinkIncremental
warning level
SDL
PCH policy
preprocessor definitions
```

The log may reveal additional output-affecting settings; include them.

---

## 16. Checkpoint warnings

For Debug and Release record every warning as:

```text
warning code
source/object
line, where supplied
build stage
```

Do not compare only counts.

Known previous Release baseline contained 17 warning instances.

The checkpoint establishes the new exact pre-A3 warning evidence after A1/A2.

---

## 17. Checkpoint executable identities

Record Debug EXE identity and Release EXE SHA-256.

For Release:

```bat
certutil -hashfile "vs\VapourSynth-mpeg2Deblock\x64\Release\Mpeg2BlockInspector.exe" SHA256
```

The checkpoint Release EXE becomes the immediate pre-A3 binary comparison point.

---

## 18. Run all six index regressions

The checkpoint requires all six tracked cases.

Expected baseline SHA-256 values:

```text
TEST_2A_A001.idx
AFE51F251B2861D5C62E1629D95645C47B06F69D86F03B5FC531CF9FE3EA9273

TEST_2A_A001_blocky.idx
CBF6E8720E47E1F097E6310540D8CBD20862E3A427AD53C61D9A235ACDBA9288

TEST_4A_A003.idx
5B989CED016ADFE5CC4546F196DD63CB2DB9B431798A99203C830A98165B9A65

LG_576i_3_LP.idx
849b6a9c411a7db837268af3ac54501a06f5f1158e68d5245ce2b3ec40a0d011

LG_576i_4_EP.idx
11B42AADF9F46B72DEC20A8F3FDD754D07CDCE78F0460A14EDA08838336FFA87

LG_576i_5_MLS.idx
378980EA462122A02D75F412FAF9CFAF79962D503C68A8F6EE41C32B24D98D7F
```

Each regenerated index must be byte-identical.

Baseline provenance for Stage A: the authoritative bytes are the six tracked `.idx` files in Git, unchanged from the pre-Stage-A recovery point. The SHA list above is a recorded convenience copy of those tracked-file identities; Claude independently holds matching baselines for `TEST_2A_A001`, `TEST_2A_A001_blocky`, and `LG_576i_3_LP`.

Also retain analyzer validity evidence as applicable to the existing test scripts.

If any case differs, stop before A3.

---

## 19. Visual Studio/Git checkpoint state

After opening/building the new `.slnx`:

```bat
git status --short
git status --short --ignored
```

Required:

- no unexplained tracked rewrite;
- `.vs` and other generated state only where expected/ignored.

Record the output.

---

# REVISED A3 - NORMALIZATION / EXPLICIT PINNING

## 20. Superseded A3 proposals

Do not apply either earlier candidate:

```text
Mpeg2BlockInspector_A3_PROPOSED_SETTINGS_v0_1.vcxproj
A3 v0.2 DRAFT candidate SHA-256:
a59788b492534334b86befdf440b5cae5a7687829e84f57377637f759044108a
```

They remain review/history material only.

The revised A3 proposal is based on:

```text
accepted A1 project
+
completed pre-A3 detailed Debug/Release checkpoint
+
byte-copied CL/LINK tlogs
+
M3 dumpbin /headers /loadconfig /imports /dependents measurements
+
full 113-row CNR3 reconciliation
+
ratified D1/D2/D3/D4/D5/D6
+
Claude M3/S7/S8/S9/S10/S11 corrections
```

Dave ratified D4 = NO: revised A3 itself changes Release `/MD -> /MT`; there is no A4.

---

## 21. Full CNR3 reconciliation requirement

The revised A3 package must retain the mechanically complete reconciliation:

```text
56 CNR3 self-test setting rows
57 CNR3 DLL setting rows
113 total rows
```

Each row is keyed by project + source line and contains:

```text
setting
condition/context
value
disposition
reason
```

Use only Design Record v0.14 section 9 disposition vocabulary.

The validator must fail non-zero for:

```text
wrong row count
missing/duplicate key
blank disposition
blank reason
invalid disposition vocabulary
```

S9 must also be stated explicitly: CNR3 source/header ItemGroups are project-specific membership and are `NOT APPLICABLE TO THIS PROJECT`; the inspector keeps its own source/header list.

---

## 22. Explicit no-defaults policy and deliberate exceptions

For every output-affecting compiler/linker/manifest/ABI setting measured at the checkpoint:

- write the currently effective value explicitly in revised A3;
- unless it is a reviewed deliberate change;
- or a documented deliberate exception below.

The objective remains:

```text
explicit project XML
=
checkpoint effective behaviour
```

except for reviewed deliberate changes.

Deliberate default exceptions:

```text
Windows SDK version
    unpinned by D2; every gate records the selected SDK

LanguageStandard_C = Default
    do not replace with /std:c11 or /std:c17 because that would change C compiler behaviour rather than pin it
```

Release runtime is a ratified deliberate A3 change under D4 = NO: Debug remains pinned `/MDd`, while Release changes `/MD -> /MT` in the project file itself.

---

## 23. Revised A3 required settings

### D1 - Release optimization

Pin the already-effective `/O2` components (`/O2 /Ot /Ob2 /Oi /GF /Gy`). The genuine D1 additions remain `/GL` and `/LTCG`.

### D2 - Windows SDK

Do not write a specific `WindowsTargetPlatformVersion`. Record the actual selected SDK at every gate. The pre-A3 checkpoint used `10.0.28000.0`.

### D3 - Debug optimizer-related settings

Explicitly use:

```text
FavorSizeOrSpeed = Speed
InlineFunctionExpansion = AnySuitable
IntrinsicFunctions = true
```

### Compiler host

Set `PreferredToolArchitecture=x64`; post-A3 CL and LINK paths must both use `HostX64\x64`.

### Debug information

Normalize Debug `/ZI -> /Zi`. Do not guess the XML for a Full-PDB choice: S13 below determines what VS2026 itself writes.

### Runtime library

```text
Debug   /MDd
Release /MT
```

Release `/MT` is part of A3 (D4=NO). The project file owns it; harness/CI may not inject it.

### AVX2 / minimum CPU target

Debug and Release explicitly use:

```text
EnableEnhancedInstructionSet = AdvancedVectorExtensions2
/arch:AVX2
```

Debug and Release both explicitly use `/favor:blend`. Dave ratified O7=`YES`; Stage B follows the same policy.

### Floating point (S14)

Pin `FloatingPointModel=Precise` for Debug and Release. The exact compiler commands must prove `/fp:contract` is absent in both configurations. No FMA-contraction policy change is accepted merely because AVX2 is enabled.

### SDL / CRT suppression

Inspector retains `SDLCheck=false` and `_CRT_SECURE_NO_WARNINGS` in both configurations. This is the frozen reference-decoder exception only. Do not add `_DEBUG`, `NDEBUG` or `_CONSOLE` merely because CNR3 carries them.

### Warning-gate output settings (S7)

Pin:

```text
DiagnosticsFormat = Column
UseFullPaths = true
ExternalWarningLevel = Level3
WarningLevel = Level3
TreatWarningAsError = false
```

### S12 - security settings are per-configuration

The superseding candidate must set the following in **both Debug and Release**:

```text
/GS ON
CFG ON at compile and link
CET compatibility ON
SpectreMitigation = Disabled (explicit project setting); `/Qspectre` absent
```

This is a deliberate product-policy decision and N1 pin. It is not represented by omission/default: S13 must capture the exact VS2026 `SpectreMitigation=Disabled` element for Debug and Release, and `/Qspectre` must be absent from both effective compiler commands.

Inspector `/sdl` remains OFF in both configurations as the sole frozen-source exception.

### S13 - learn XML names from VS2026, do not guess

Before generating the final superseding candidate:

1. make a scratch copy of the current A1/A2 `Mpeg2BlockInspector.vcxproj`;
2. open that scratch project in Dave's VS2026;
3. set the intended values through Property Pages for each newly introduced/uncertain property, at minimum CFG enabled, CET compatible enabled, Spectre mitigation explicitly Disabled, and Full-PDB/debug-information behaviour, for Debug|x64 and Release|x64 as applicable;
4. save and close VS;
5. diff the scratch project against its untouched copy;
6. preserve the exact XML VS2026 wrote in the A3 review package;
7. use those exact elements in the real candidate where they exist; use `AdditionalOptions` only when VS2026 itself supplies no dedicated stable element, with the reason recorded.

Do not generate the final candidate before this evidence exists.

### Spectre decision - M7 superseded

Claude M7 was a valid MUST under the earlier `/Qspectre` policy. Dave has now deliberately chosen not to use Spectre mitigation for this project. Therefore:

- do not require `Microsoft.VisualStudio.Component.VC.Runtimes.x86.x64.Spectre`;
- do not add `-warnAsError:MSB8040`;
- do not scan for `MSB8040` as a project-specific gate;
- do not perform `/VERBOSE:LIB` Spectre-runtime provenance;
- explicitly set the captured VS2026 `SpectreMitigation=Disabled` element in Debug and Release;
- prove `/Qspectre` is absent from both effective compiler commands and that CI/harness does not inject it.

### P1 - mandatory mechanical pin table

The final A3 candidate package contains a versioned pin-table CSV with one row for every switch on the four checkpoint CL/LINK command lines, every M3 dumpbin semantic property, N1 explicit Spectre Disabled and O7 Debug+Release `/favor:blend`. Each row records checkpoint value, A3 value, configuration, exact XML target or justified `AdditionalOptions` / tool-semantic / deliberate exception, and evidence source. The final validator fails on missing/duplicate rows, blanks, unknown coverage kinds and any remaining `S13_PENDING`. A PRE-CANDIDATE may use `--allow-s13-pending` only to prove the checklist is complete before local capture.

### Q1 - mandatory XML-recognition and tlog-derived evidence

Before generating the final A3 `.vcxproj` candidate:

- scan the selected VS2026 installation's Visual C++ rule XML files recursively and record which pin-table property names and enum values are recognized;
- resolve anything not proven by the rule scan through S13 Property Pages evidence;
- generate the checkpoint CL/LINK evidence set from the four byte-copied command tlogs, not from a hand-written expected-key file;
- cover the default Windows link-library list explicitly or as a documented deliberate exception while still requiring the measured link-line/import outcome;
- run the final pin validator with no local-evidence waiver and no `S13_PENDING`.

A final A3 candidate does not exist until all of the above pass.

### P4 - reconciliation validator

Ship the validator. It rejects duplicate keys, requires 113 rows (56 `CNR3_selftest`, 57 `CNR3_DLL`), cross-checks key/setting/CNR3 value against the source-reference CSV, and rejects blank target/reason/disposition or unknown vocabulary.

### Other compiler/linker/manifest pins

Continue to pin the measured effective values required by M2/M3/S7-S11: runtime, `/GS`, basic runtime checks, JMC, character set, C compilation, optimization/inlining/intrinsics, debug information, precompiled-header state, function-level linking, whole-program optimization, manifest, LAA, ASLR/DEP, target x64, Debug/Release REF/ICF behaviour and High Entropy VA.

### D6 - Release PDB path hygiene

Release adds `/PDBALTPATH:%_PDB%` in the project file. Determine whether VS2026 writes a dedicated property during S13; otherwise use Link `AdditionalOptions` with that justification.

### O8 - future plugin only

`/guard:ehcont` is not an A3 inspector requirement. Record it as an explicit Stage B plugin decision.

## 24. Revised A3 review package

The next package is a **superseding A3 package**. Because S13 requires local VS2026 evidence, it is acceptable first to issue a PRE-CANDIDATE package that contains requirements and capture tools but **no applyable `.vcxproj`**. The applyable candidate package is generated only after S13 evidence is returned.

The final candidate package must contain at minimum:

```text
revised A3 candidate .vcxproj
A1 -> revised A3 exact diff
candidate SHA-256
full 113-row reconciliation CSV + source-reference CSV + strict validator PASS
P1 pin table + expected-key list + strict final validator PASS
S13 VS2026 property-page XML capture/diff
checkpoint Debug/Release detailed MSBuild logs
byte copies of four UTF-16 CL/LINK tlogs
verbatim full pre-A3 CL/LINK command lines
predicted/reviewed post-A3 CL/LINK mappings
Spectre-policy evidence: `/Qspectre` absent and no Spectre-specific dependency/discovery override
S14 /fp:contract-absence check
S15 pre-A3 LP three-run timing evidence
Debug and Release M3 dumpbin captures
PE/load-config/import comparison plan
normalized warning baselines
six-index checkpoint results + tracked-file provenance
A1/A2 commit evidence
`git show --name-status 837df123`
actual SDK/toolchain evidence
README live Git-status/last-commit evidence
exact Visual Studio path case from `git ls-files vs`
git status --short and --short --ignored evidence
```

The 113-row reconciliation must change the four CNR3 `EnableEnhancedInstructionSet=AdvancedVectorExtensions2` rows from `DELIBERATELY DIFFERENT` to `REUSE UNCHANGED`. SDL rows remain deliberately different for the frozen-decoder reason.

Send the completed candidate package to Claude for cold review. Do not apply A3 before Claude approval and Dave ratification.

# A3 APPLICATION AND A3 GATE

## 25. Apply accepted A3

After Claude approval and Dave ratification:

- apply the accepted candidate byte-for-byte;
- verify candidate SHA-256;
- use named staging only;
- inspect exact diff and `git diff --cached --check`;
- commit A3 with no unrelated file.

Release `/MD -> /MT` belongs in this A3 commit because Dave ratified D4 = NO; there is no A4.

---

## 26. Detailed post-A3 builds

Clean+Build:

```text
Debug | x64
Release | x64
```


Capture:

```text
exact cl.exe command
exact link.exe command
CL/LINK executable paths
MSBuild path/version
VCTools/toolset
actual selected Windows SDK
warnings
```

Both CL and LINK paths must contain `HostX64\x64`.

---

## 27. A3 command-line delta proof

Compare the exact post-A3 CL/LINK tlogs with the checkpoint originals.

Required deliberate deltas include:

```text
tool host HostX86\\x64 -> HostX64\\x64
Debug /ZI -> /Zi
Debug D3 optimizer/intrinsic settings
Release /MD -> /MT
Release /GL
Release /LTCG
Release /PDBALTPATH:%_PDB%
Debug+Release /arch:AVX2
Debug+Release /favor:blend
/GS explicitly enabled
CFG enabled at compile+link
/CETCOMPAT enabled
SpectreMitigation explicitly Disabled in Debug+Release; /Qspectre absent
/fp:precise present and /fp:contract absent in Debug+Release
explicit warning-output pins
```

Release `/O2` components such as `/Oi`, `/Ot`, `/Ob2`, `/GF` and `/Gy` are pins of already-effective `/O2` behaviour, not additional D1 behaviour.

Apart from reviewed pins and the deliberate changes above, no unexplained compiler/linker switch may appear or disappear.

If an unexplained delta exists, A3 fails pending diagnosis.

---

## 28. A3 PE/load-config/import proof

### P3 exact post-A3 dumpbin criteria

The gate proves using `dumpbin /headers /loadconfig /imports /dependents` and the first accepted capture's exact wording:

- PE DLL characteristics include Control Flow Guard;
- Guard Flags show a Guard CF function table is present and Guard CF function count is greater than zero;
- extended DLL characteristics report CET compatibility;
- `/GS` remains evidenced by security-cookie/feature data;
- Release CodeView/RSDS contains only `Mpeg2BlockInspector.pdb`, no absolute directory;
- Debug CodeView/RSDS may retain its development path;
- standalone Release forbidden-DLL rule still passes.

If installed `dumpbin` wording differs, record the exact accepted wording and match that thereafter.


Run:

```text
dumpbin /headers /loadconfig /imports /dependents
```

against post-A3 Debug and Release executables.

Require unchanged semantic state for the M3 baseline except for the intentionally changed Release runtime imports:

```text
PE32+ x64
Large Address Aware
High Entropy VA
Dynamic Base
NX Compatible
CET-compatible flag PRESENT
fully enabled CFG image PRESENT (including the expected Guard/FID-table evidence)
manifest behaviour
Debug /OPT behaviour
full-PDB/debug-information mode as explicitly pinned
```

The effective Debug and Release compiler commands must also show `/arch:AVX2` and `/GS`. The effective compile/link settings must show CFG enabled, and `/Qspectre` must be absent by deliberate policy. These are intentional changes from the checkpoint baseline, not discrepancies to normalize away.

Debug remains `/MDd`; its dependency DLL-name set must match the checkpoint Debug set at the DLL-name level. Function-level imports may change only where explained by D3/intrinsics.

Release uses the standalone rule. It must contain no dependency whose DLL name matches:

```text
VCRUNTIME*
MSVCP*
api-ms-win-crt-*
ucrtbase*
CONCRT*
VCOMP*
MSVCR1*
```

Do not use broad `MSVCR*`, because the Windows system `msvcrt.dll` must not be accidentally prohibited.

The allowed Release dependency-DLL set is the checkpoint Release set after removing dynamic C-runtime DLLs. Current measured expected set:

```text
KERNEL32.dll
```

Any other Release dependency DLL stops the gate for review. Function-level KERNEL32 imports may grow because the static runtime uses Windows APIs.

The accepted build has no Spectre-library provenance requirement because `/Qspectre` is deliberately not used.

Do not compare PE timestamps, PDB GUIDs or section sizes as identity requirements.

---

## 29. A3 warning comparison

Compare checkpoint to post-A3 by:

```text
code
file
line
stage
```

Expected directional changes include:

```text
Debug LNK4075 disappears after /ZI -> /Zi
Debug strcat C4013 instances may disappear under D3 /Oi
Release /GL + /LTCG may move warning attribution from compile to LTCG/link stage
security/AVX2 changes must not create unexplained diagnostics
```

Every difference must be explained. No unexplained new warning is accepted.

---

## 30. A3 frozen-source and six-index gate

Recompute the frozen hashes:

```text
getpic.c
    e80239cfe73a0c04490a9bf131714861254ed1d7d095b052aac616a887ef0eca
mpeg2dec.c
    8e6053ccb3a40be8c0d985f2e35124bf728d1f61df9b6d0c01b71e13e13b0947
Stage1_Inspector_Analyzer_v0_2.py
    8e0d58305ee4fe518c25b67bdbe74acc4fb392486f23e6137862d916e5e02cda
```

Also require no name-status difference from the pre-Stage-A tag across the full frozen source/analyzer set.

Run all six gated index cases. Every regenerated `.idx` must be byte-identical to the section 18 tracked-file baseline.

No representative subset or waiver is allowed.

**Dave-ratified deviation for A3 v0.10 ONLY (2026-10-10):** The
v0.10 six-index rerun is **WAIVED, not PASS**, despite the preceding rule.
This exceptional decision is supported by the three technical comparisons
recorded in Claude's final A3 gate review v0.1, section 3, and the first
close-out section above: v0.9 six-index PASS and identical CL invocation
sets; only `/LTCGOUT` removed from LINK while plain `/LTCG` remains;
and zero normalized differences in Release `/headers`, `/loadconfig` and
`/imports`. The measurements are strong evidence of identical code
generation, **not byte-for-byte proof**. This deviation has no continuing
authority: any later toolset, exact compiler or code-generation change
still requires the six-index regression.

If any index differs, do not weaken the gate and do not silently weaken the ratified AVX2 and retained security policy. Build local, uncommitted diagnostic variants to isolate the cause in this order:

1. temporarily restore the pre-A3 ISA floor (`/arch:SSE2`) while keeping the ratified policy unchanged on paper;
2. restore Release `/MD`;
3. then also remove `/GL` and `/LTCG`;
4. then also restore `PreferredToolArchitecture=x86`;
5. security settings may be toggled only as diagnostic experiments if the earlier variants fail to isolate the cause; an OFF diagnostic result is evidence, not an accepted final configuration.

Use the resulting evidence to isolate the cause, then return to Claude and Dave before revising the accepted design.


### S15 LP timing evidence (information only)

Before A3 application overwrites the Release output, preserve the checkpoint Release EXE. Time the LP case three times with that executable. After the accepted A3 Release build, time the same LP case three times on the same machine under comparable conditions. Record all six elapsed times and mean/median. This is informational only and cannot weaken a security setting or functional gate.

---

## 31. A3 Git/project evidence

Record:

```text
post-A3 Debug EXE SHA-256
post-A3 Release EXE SHA-256
post-A3 Mpeg2BlockInspector.vcxproj SHA-256
Mpeg2BlockInspector.vcxproj.filters SHA-256
VapourSynth-mpeg2Deblock.slnx SHA-256
git status --short
git status --short --ignored
```

Restore generated tracked test logs and remove only known untracked test outputs before final status evidence.

If A3 passes, Stage A proceeds directly to close-out; there is no A4.

---

# STAGE A CLOSE-OUT

## 32. Final Git/Visual Studio state

Run:

```bat
git status --short
git status --short --ignored
```

Required:

```text
no unexpected tracked files
only expected ignored Visual Studio/build state
```

Before migration close-out, every Claude review document created during Stage A must either be committed by exact name or deliberately removed; do not leave unexplained review files untracked.

---

## 33. Stage A PASS criteria

Stage A is PASS only when all applicable items are true:

```text
A1 applied/committed
A2 applied/committed
pre-A3 checkpoint PASS
revised consolidated A3 reviewed/ratified
A3 applied/committed
A3 Debug build PASS
A3 Release build PASS
A3 command-line delta explained
A3 M3 PE/load-config/import gate PASS
A3 standalone Release dependency gate PASS
A3 AVX2 minimum-target proof PASS
A3 CFG/CET/GS security-hardening proof PASS in Debug+Release
A3 explicit Spectre-OFF pin PASS (`SpectreMitigation=Disabled` in both configurations; `/Qspectre` absent; no CI/harness override)
A3 /fp:contract absence proof PASS
A3 S15 LP timing recorded (information only; not a gate)
A3 warning delta explained
A3 frozen-source gate PASS
A3 six-index v0.10 rerun WAIVED by Dave (NOT PASS; see section 30 exception)
README target build/distribution claims verified against accepted A3 evidence
final Git/VS state PASS
accepted project/binary hashes recorded
```

Only then may Stage B begin.

Do not push/finalize/tag outside the already agreed migration push policy.

---

## 34. Evidence to preserve

Preserve at least:

```text
A1/A2 candidate SHA proof and commit hashes
A2 git show --name-status proof
pre-A3 Debug/Release detailed logs
pre-A3 exact CL/LINK tlogs and transcriptions
pre-A3 normalized warning lists
pre-A3 toolchain/SDK/vswhere evidence
pre-A3 Debug/Release EXE hashes
pre-A3 M3 dumpbin captures
pre-A3 six-index results and baseline provenance
full 113-row reconciliation + source-reference cross-check + validator PASS
Claude A3 v0.2 review
Claude DR v0.8 / Stage A plan v0.3 review
DR v0.14 + Stage A plan v0.9
README.md target-policy snapshot + live Git commit/status evidence used for close-out consistency check
S13 property-page XML capture
Spectre-policy absence evidence
S14 /fp:contract-absence evidence
S15 pre/post LP timing record
NOTICE.md identity/current repository copy for handback reference
superseding A3 package (post-v0.3) + review + Dave ratification
A3 commit hash
post-A3 Debug/Release detailed logs/tlogs
post-A3 command-line delta report
post-A3 M3 dumpbin report
post-A3 standalone Release dependency report
post-A3 warning report
post-A3 six-index results
frozen source hash reports
final project/solution hashes
final Git status outputs
```

These feed Design Record v0.14, Stage B protection baselines, migration close-out and the common Developer Handback.

---

## 35. Change log

### v0.11 - 2026-10-10

- Recorded Q1/R1/R4 local evidence closure and Claude review.
- Advanced the boundary from v0.7 pre-candidate evidence gathering to v0.8 applyable-candidate cold review.
- Added T1/T2/T3 candidate requirements from Claude's closure review.


### v0.10 - 2026-10-09

- Carried Claude review of A3 v0.6 / DR v0.14.
- Added Q1 recognition evidence for every XML property/enumeration used by the pin table.
- Replaced the hand-maintained expected-key authority with CL/LINK evidence generated from the four checkpoint command tlogs.
- Added the default Windows library list to mandatory checkpoint coverage.
- Clarified that Stage A deliberately derives MSBuild beneath the selected `VSINSTALL`.

### v0.9 - 2026-10-09

- Carried P1/P3-P6 and N1/N3/N5 from the two newly received Claude reviews.
- O7=`YES`: `/favor:blend` explicit in Debug and Release; Stage B follows.
- N1: Spectre mitigation explicitly Disabled in both project configurations; `/Qspectre` absence also proved.
- Restored mandatory mechanical pin table and strict final validator.
- Restored strict 113-row reconciliation validation with duplicate, 56/57 count and source-reference checks.
- Added exact CFG/CET/PDB dumpbin pass criteria.
- Corrected stale references and duplicated headings; BAT must be CRLF and prove MSBuild is under selected VS root.
- N4 option (a): commit corrected README now.


### v0.8 - 2026-10-09

- Recorded Dave's deliberate decision not to use Spectre mitigation.
- Superseded M7's Spectre component, `MSB8040` and `/VERBOSE:LIB` provenance requirements.
- Kept `/GS`, CFG and CET enabled in both Debug and Release; Spectre remains deliberately unused in both configurations.
- Kept S13 for empirical VS2026 XML capture of CFG, CET and full-PDB/debug-information settings.
- Kept S14 `/fp:contract` absence and S15 LP timing.
- Kept O7 open and O8 `/guard:ehcont` deferred to Stage B.
- Recorded that README was committed in `b4dace0` with now-superseded Spectre wording and must be corrected.

### v0.7 - 2026-10-09

- Carried the previously missing Claude review M7 and S12-S15; recorded optional O7/O8.
- M7: added Spectre component to `vswhere -requires`, `-warnAsError:MSB8040` plus literal log scan, and positive `/VERBOSE:LIB` Spectre-runtime provenance.
- S12: made /GS, CFG, CET and Spectre explicit in both Debug and Release.
- S13: final A3 project candidate is blocked until VS2026 Property Pages reveal the exact XML written for new/uncertain settings.
- S14: required `/fp:precise` and absence of `/fp:contract` in both compiler command lines.
- S15: added three-run LP timing before/after A3 for information only.
- Added live README commit-status check and retained Claude's recommendation to commit it with A3 or after the gate if not already committed.
- Corrected the handover-review input set and aligned with DR v0.12.

### v0.6 - 2026-10-09

- Updated the controlling migration design reference to v0.11.
- Added a documentation-consistency guard for the already-updated `README.md`: its AVX2/standalone/security claims are target policy until A3 passes and must be verified against accepted build evidence at Stage A close-out.
- Added `NOTICE.md` as preserved handback/reference evidence without making Stage A a licence-document rewrite.
- Added README consistency to Stage A PASS criteria and README/NOTICE snapshots to evidence preservation.
- Kept the v0.5 AVX2, CFG, CET, Spectre, `/GS`, `/MT`, SDL-exception and one-build-route requirements unchanged.

### v0.5 - 2026-10-09

- Superseded A3 v0.3 for application because its `/arch:SSE2` and security-off settings conflict with Dave's ratified target policy.
- Changed the inspector CPU floor to x64 + `/arch:AVX2` for both Debug and Release; pre-AVX2 CPUs are intentionally unsupported.
- Added explicit Release `/favor:blend` through project `AdditionalOptions` for broad AMD/Intel performance tuning.
- Changed `/GS`, CFG, CET and Spectre from baseline-preservation OFF states to deliberate security-hardening ON states.
- Required the Spectre-mitigated v145 x64 libraries as a build prerequisite; missing components fail the build/readiness check rather than weakening security.
- Kept inspector `/sdl` OFF solely as the frozen MPEG-2 reference-decoder-derived exception and recorded `/sdl` ON for the future plugin project.
- Expanded the A3 command-line and dumpbin gates to prove AVX2, CFG, CET and `/GS` are actually effective.
- Expanded the later harness/GitHub rule: project settings are authoritative and CI verifies rather than injects AVX2/security/runtime settings.
- Updated the diagnostic sequence so AVX2/security may be toggled only in local attribution experiments, not silently accepted OFF.

### v0.4 - 2026-10-09

- Incorporated Claude review of DR v0.8 / plan v0.3.
- Recorded Dave-ratified D4 = NO, D5 = YES and D6 = YES.
- Deleted the A4 stage; consolidated Release `/MT` into A3.
- Rewrote the A3 Release import gate for standalone `/MT`, including `MSVCR1*`.
- Added Release `/PDBALTPATH:%_PDB%`.
- Added S11 mitigation/default pinning details.
- Added explicit `SpectreMitigation=false`, Control Flow Guard off, CET off, High Entropy VA on, manifest and Debug `/OPT` pinning requirements.
- Added consolidated-A3 failure diagnosis order.
- Kept project XML as the single source of runtime and PDB-path settings.

### v0.3 - 2026-10-09

- Updated execution state: A1/A2 and the mandatory pre-A3 checkpoint are complete.
- Incorporated Claude's A3 v0.2 review M3 and S7-S9 findings.
- Recorded completed Debug/Release dumpbin M3 baseline measurement.
- Superseded the A3 v0.2 DRAFT candidate for application.
- Corrected D1 interpretation: `/O2` components including `/GF` are pins; `/GL` + `/LTCG` are the genuine D1 Release additions.
- Added explicit warning-output pins and HostX64 proof.
- Added PE/load-config/import gate.
- Added Dave's standalone Release requirement as a project-file requirement, not a CI override.
- Recorded Claude's then-recommended D4 A3/A4 split as review history; v0.4 supersedes it after Dave's D4 = NO decision.
- Added the standalone forbidden-DLL rule and SDK artifact-provenance requirement.
- Added one-build-route constraint: later harness/workflow may invoke the projects but may not duplicate or override project settings.
- Added explicit review-document cleanup requirement before close-out.

### v0.2 - 2026-10-09

- Reissued Stage A sequence after Claude review v0.2.
- Marked A1/A2 accepted as packaged and A3 v0.1 not for application.
- Added byte-copy + SHA application rule.
- Added no-Visual-Studio-open rule between A1 and A2.
- Added mandatory pre-A3 Debug/Release checkpoint.
- Added detailed MSBuild log and exact cl.exe/link.exe capture.
- Added actual SDK/toolchain evidence requirement.
- Added six-index checkpoint before A3.
- Added Dave's no-defaults ruling as an explicit A3 requirement.
- Added mandatory 113-row CNR3 reconciliation and fail-on-blank validation.
- Added ratified D1, D2 and D3.
- Added the then-current AVX2-off pin requirement (superseded by v0.5).
- Added command-line delta proof.
- Added `git status --short --ignored` to checkpoint/final gate.
- Added Stage A accepted-hash recording for the later Stage B protection trigger.

---

## Close-out v0.14 change log (2026-10-10)

- Promoted header to accepted A3 v0.10 and pending Stage A repository close-out.
- Recorded Dave-ratified Plan section 30 deviation: six-index v0.10 status WAIVED, never PASS.
- Preserved the three explicitly supplied Claude section-3 corroboration points and the no-bytewise-proof limitation.
- Maintained permanent future compiler/toolset/codegen six-index requirement.
- Incorporated Claude final-gate review N1-N4 from section 4, with unverified Stage C/D mechanics explicitly deferred.
- Recorded README snapshot consistency assessment and live Git/repository action boundary.
