# Stage A Visual Studio 2026 / MSBuild Hard-Earned Knowledge



**Filename:** `StageA_VS2026_MSBuild_Hard_Earned_Knowledge_v0_5.md`
**Version:** 0.5
**Date:** 2026-10-10 (Stage A A3 v0.10 accepted by Dave; close-out documentation review)
**Status:** Stage A A3 v0.10 accepted by Dave; W1/HostX64/warnings/W2/hashes/hygiene PASS, six-index v0.10 WAIVED (not PASS); close-out docs/repository push pending. Reusable Stage C findings remain unverified until local demonstration.
**Scope:** Reusable lessons from normalizing the legacy Mpeg2BlockInspector project under Visual Studio 2026 / MSBuild v180. This is not MPEG-2/deblocking algorithm knowledge.

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

### Durable rule: evidence proportional to the change

The v0.10 waiver was exceptional and reasoned; it was not permission to
replace behavioural evidence with binary hashes generally. Bytewise EXE
hash differences do not prove behavioural changes or equivalence. Equality
of relevant CL/LINK configurations and normalized PE output strongly
corroborates unchanged code generation for this narrow linker-output
property correction but is **not byte-for-byte code proof**. Preserve
normal six-index tests on code-generation/compiler/toolset changes. Avoid
repeated source-file audits when frozen-file SHA and Git-baseline checks
have already passed and no new risk has emerged.


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

### Newly learned distinctions and verification trail

- The A3 host change was only `HostX86\x64` -> `HostX64\x64`; the target stayed x64 throughout. The MSBuild *engine* can be independent of the native host selection. A3's fixed `Bin\MSBuild.exe` bitness has NOT been measured; do not describe it as 32-bit fact.
- Evidence on 2026-10-10: W1 extractor returned four token totals 33/32/23/25 and checker validated content, `W1_CHECKER_RC=0`; logs contain compiler and linker from `HostX64\x64` in Debug and Release. The old v0.9 extra LINK `/LTCGOUT` was removed in v0.10.
- Microsoft docs distinguish the C++ `PlatformToolset` from the host-tool `PreferredToolArchitecture`. A configured x64 MSBuild path does not prove x64 CL/LINK; independently test each. `Bin\amd64\MSBuild.exe` needs independent runtime-bitness proof (managed AnyCPU PE headers may be misleading).
- `vswhere -products *` explicitly includes standalone Build Tools per Microsoft's vswhere guidance. `Microsoft.VCToolsVersion.default.txt` documents the latest *in-support* MSVC tools build; this does not by itself prove "newest folder installed".
- Beware unreviewed defaults and environment overrides: process-level CL/_CL_/LINK/_LINK_ switches bypass `.vcxproj`; MSBuild imports properties from its environment. A Stage C guard must be evidence-based, including `Platform` and `PreferredToolArchitecture`; VsDevCmd is for interactive diagnostics, not the harness environment.
- Warning: DO NOT hash the repository GitHub ZIP's LF `.vcxproj`/`.slnx` representation as though it were the Windows working copy's CRLF representation.

### K4: automatic imports and response files (binding for Stage C/D)

- Fail closed if any `Directory.Build.props`, `Directory.Build.targets`, or `Directory.Build.rsp` exists in a repository ancestor directory, from the repository parent through filesystem root; also reject unreviewed occurrences within the repository that may affect a build. Log the checked paths and results.
- Launch MSBuild with `-noAutoResponse` so implicit MSBuild response files do not silently inject switches (including applicable `MSBuild.rsp` and `Directory.Build.rsp`). Validate the precise MSBuild 18.x response-file behavior locally; any uncertainty is an unverified Stage C gate item.
- Prove the guard experimentally once using a disposable scratch project and a scratch `Directory.Build.props` in its ancestor directory. Confirm the harness refuses to build, then remove the scratch file. Never create this probe in or above the production repository. Record command, output, and return code.
- The guard is additive to environment-property checks, including `PreferredToolArchitecture`, `CL`, `_CL_`, `LINK`, `_LINK_`, `Platform`, and relevant MSBuild/global-property override mechanisms. No build-policy injection through environment, response files or auto-imports is permitted.

### K3: compiler build designated by Visual Studio

- No project-level `VCToolsVersion` override: the designated current build is **recorded, not pinned**. Any change relative to last accepted compiler/toolset triggers command-switch, warning, and six-index rerun before acceptance. The exact selection rules and `DefaultPlatformToolset` implementation remain UNVERIFIED until local Stage C/post-A testing.
- `-latest`, without `-prerelease`, selects the newest **released** qualifying installed Visual Studio. Keeping the build machine updated is an operator responsibility; discovery does not install updates. Build Tools are eligible via `-products *`, and the selected product must be logged.

---

## 1. Why this document exists

The A3 normalization work required repeated empirical checks of Visual Studio 2026 rule XML, MSBuild persistence placement, native command tlogs and generated binary behavior. The expensive part was not choosing flags; it was proving which project element actually owns each behavior and how Visual Studio/MSBuild serializes and emits it.

Future project work should consult this document before attempting another Visual Studio project normalization.

## 2. Installed rule XML is the recognition authority

For VS2026/v180 project-property recognition, do not infer XML property names from command-line switches, old project examples, UI labels or previous toolsets.

Scan the installed v180 rule XML and validate:

- exact property name;
- owning rule/tool;
- enum/bool value;
- DataSource placement;
- configuration conditioning;
- where relevant, placement before `Microsoft.Cpp.props`.

A property name being plausible is not evidence that MSBuild recognizes it.

## 3. Property placement is part of the setting

A setting is not fully identified by `PropertyName=Value`. Its persistence location matters.

Observed important cases:

- `SpectreMitigation` -> `Label="Configuration"` PropertyGroup.
- `WholeProgramOptimization` has both Configuration and ClCompile representations; for this project both are explicit.
- `LinkIncremental`, `GenerateManifest`, `LinkControlFlowGuard` -> conditioned PropertyGroup, despite being Link-related behavior.
- `ControlFlowGuard`, `RemoveUnreferencedCodeData`, compiler `ProgramDataBaseFileName`, compiler `ErrorReporting` -> `ItemDefinitionGroup/ClCompile`.
- `LinkErrorReporting`, `CETCompat`, `ManifestEmbed`, `GenerateDebugInformation` -> `ItemDefinitionGroup/Link`.
- `EnableSegmentHeap` -> `ItemDefinitionGroup/Manifest` via v180 `mt.xml`.

Configuration-labelled properties should be in their Configuration PropertyGroup before the `Microsoft.Cpp.props` import when that is how Visual Studio persists them.

## 4. Specific recognition traps

### 4.1 Link error reporting

Compiler and linker error-reporting properties are different.

Correct linker mapping:

```text
Link/LinkErrorReporting=QueueForNextLogin
```

Do not use `Link/ErrorReporting=Queue`.

### 4.2 `/Zc:inline` is not `/Ob2`

`/Zc:inline` maps to:

```text
ClCompile/RemoveUnreferencedCodeData=true
```

It is distinct from function inlining policy:

```text
ClCompile/InlineFunctionExpansion=AnySuitable
```

### 4.3 High Entropy VA

No `HighEntropyVA` property exists in the installed v180 rules used for this work.

The accepted explicit representation is:

```text
Link/AdditionalOptions includes /HIGHENTROPYVA %(AdditionalOptions)
```

Binary `dumpbin` evidence remains authoritative.

### 4.4 Full PDB

The explicit linker representation adopted is:

```text
Link/GenerateDebugInformation=DebugFull
```

The post-build linker line and PE/PDB evidence still decide whether the intended output was produced.

## 5. Single-owner rule for derived switches

A major lesson from Claude's v0.8 cold review:

> Do not add a second explicit project property merely because the measured command line contains a switch.

The existing A1 project already had:

```text
Manifest/EnableSegmentHeap=true
```

The checkpoint linker tlog contained `/manifestinput:...segmentheap.manifest` even though A1 had no `Link/ManifestInput`.

Therefore the working conclusion is that the Visual Studio toolset derives the linker manifest-input switch from `EnableSegmentHeap=true` (inferred from A1 + checkpoint tlog; to be confirmed by the post-A3 tlog).

Adding an explicit:

```text
Link/ManifestInput=...
```

created two project-level owners for the same effective manifest input. Both properties were individually recognized, but their coexistence was semantically wrong.

The v0.9 correction is:

```text
keep Manifest/EnableSegmentHeap=true
remove Link/ManifestInput
gate exactly one /manifestinput:...segmentheap.manifest after build
```

General rule:

**When an existing higher-level property already generates a measured downstream switch, pin the higher-level owner and gate the emitted switch. Do not duplicate ownership at a lower layer unless independent evidence proves both are required.**

## 6. Native `.command.1.tlog` format

Do not assume native MSBuild command tlogs contain `cl.exe` or `link.exe`.

Observed CL format is alternating records:

```text
^<tracker key/source path>
<raw argument payload>
```

The payload begins directly with switches such as `/c /ZI ...`.

The corrected extractor therefore:

- decodes UTF-16;
- ignores `^` tracker-key records;
- parses all payload records;
- normalizes only path/source/object noise;
- requires all per-source CL records within a configuration to normalize identically.

## 7. Native tlogs are not complete copies of detailed MSBuild logs

The preserved checkpoint produced 82 native-tlog tokens:

```text
Debug CL      25
Release CL    23
Debug LINK    16
Release LINK  18
```

The checkpoint pin table had 86 CL/LINK rows.

The four missing native-tlog items were exactly:

```text
CLD_er  /errorReport:queue
CLR_er  /errorReport:queue
LD_err  /ERRORREPORT:QUEUE
LR_err  /ERRORREPORT:QUEUE
```

Those four were present in the detailed MSBuild logs.

Correct accounting was therefore:

```text
82 native-tlog-derived tokens
+4 detailed-MSBuild-log-only error-reporting pins
=86 checkpoint CL/LINK rows
```

Never manufacture the missing four into tlog evidence.

## 8. `/IMPLIB:` parser trap

A token classifier that checks only whether a LINK token ends with `.lib` will incorrectly absorb:

```text
/IMPLIB:<path>.lib
```

into the default library list.

Path-valued switches must be recognized before classifying bare `.lib` operands.

Correct outputs are separate:

```text
LIBS=kernel32.lib;...;odbccp32.lib
/IMPLIB:<PATH>
```

## 9. Default libraries are a deliberate exception

The measured default linker library list is not explicitly rewritten as `AdditionalDependencies`.

Reason:

- an unreferenced library cannot reach the final image;
- the Release import/dependency gate proves the distributed result;
- current accepted Release expectation is `KERNEL32.dll` only.

This is a deliberate exception, not an unnoticed default.

## 10. Predict explicit spellings introduced by pinning

Pinning an existing default/implicit behavior can make a command-line switch appear even though product behavior has not changed.

Claude v0.8 identified these expected spellings:

```text
Debug CL:   /Gy- /GF-
Debug LINK: /OPT:NOREF /OPT:NOICF /LARGEADDRESSAWARE /TSAWARE
Release LINK: /LARGEADDRESSAWARE /TSAWARE
```

The delta document must include such spellings because the gate treats any unexplained delta as a stop condition.

Likewise, explicitly pinned enum values whose chosen value emits no switch should be documented as expected non-emission.

## 11. Evidence hierarchy used successfully

For this normalization, use this order:

1. pristine/A1 project;
2. preserved checkpoint tlogs and detailed MSBuild logs;
3. installed VS2026 v180 rule XML;
4. Visual Studio Property Pages where needed;
5. strict generated reconciliation/validators;
6. post-application tlogs;
7. `dumpbin`/imports/PDB binary evidence;
8. six-index functional regression.

No single layer substitutes for the later behavioral/binary gates.

## 12. Preserve provenance, not just conclusions

Durable evidence set should retain:

- final pin table;
- final rule-property CSV;
- final checkpoint-token CSV;
- final tlog-to-pin reconciliation CSV;
- scanners/validators;
- Claude cold-review files;
- A1->candidate and candidate-to-candidate diffs;
- final candidate SHA-256;
- PASS outputs from Dave's local machine.

Failed intermediate tools may remain in archival packages but should not be treated as active authority.

## 13. Current candidate state

A3 v0.8 SHA-256:

```text
30999ef34b9a38c4dbc2ad7b9ce7b1dcba0fe5f727c1963c9ba0dc2a4f5d52f3
```

was **not ratifiable** because of duplicate segment-heap ownership.

A3 v0.9 candidate SHA-256:

```text
ebfcde82405fd2dc25aa7a14a160f89375465d545927b3e4583e7a40fd1af668
```

removes only the two explicit `Link/ManifestInput` owners from the project file and carries the U2 predicted-delta corrections.

That was the candidate-preparation state. v0.9 was subsequently cold-reviewed, ratified and applied; sections 14-16 record the later state and the W1 `/LTCGOUT` finding.

## 14. A3 v0.9 final review and ratification

Claude's short cold review of the READY package independently verified:

- the v0.8 -> v0.9 project diff is exactly two removed `Link/ManifestInput` lines;
- v0.9 contains zero `ManifestInput` elements and retains `Manifest/EnableSegmentHeap=true` in both configurations;
- only `LD_maninput` and `LR_maninput` changed in the pin table;
- all U2 predicted-delta spellings are present;
- all six validators pass;
- all 132 v0.9 property elements independently match v180 rule/tool/name/value/placement expectations.

Claude's verdict:

```text
Ratifiable.
```

Dave ratified exact candidate SHA-256:

```text
ebfcde82405fd2dc25aa7a14a160f89375465d545927b3e4583e7a40fd1af668
```

on 2026-10-10.

This closes candidate-design review, but it does **not** close Stage A. The post-application gate remains authoritative.

## 15. Current published repository baseline before A3 application

The repository was additionally advanced after the knowledge checkpoint by vendoring the VapourSynth API4 headers:

```text
34e8a46 Add vapoursynth include files ready for use with DLL building
```

Five `.h` files are stored and checked out as LF (`i/lf w/lf`) with no explicit `.gitattributes` rule yet. That line-ending policy should be normalized during Stage B/tooling cleanup, not by interrupting A3.


## 16. W1 found a cross-property emission side effect: `/LTCGOUT`

Applied v0.9 passed the intended CL deltas, but mechanical W1 reconciliation found one extra LINK token in each configuration:

```text
/LTCGOUT:<...Mpeg2BlockInspector.iobj>
```

This token was absent from both preserved checkpoint LINK tlogs. W1 therefore stopped exactly as designed. The checker was not relaxed.

Installed VS2026 v180 evidence established (exact installed-file lines):

- `Microsoft.Cpp.Common.props:259` imports `Microsoft.Link.Common.props`.
- `Microsoft.Link.Common.props:63` supplies `$(IntDir)$(TargetName).iobj` when `%(Link.LinkTimeCodeGenerationObjectFile)` is empty; that condition itself does **not** test `LinkTimeCodeGeneration`.
- `v180\1033\link.xml:914-919` defines `LinkTimeCodeGenerationObjectFile` as a Link `StringProperty` and maps it to `LTCGOUT:`.
- `Microsoft.CppCommon.targets:1253-1254` passes both `LinkTimeCodeGeneration` and `LinkTimeCodeGenerationObjectFile` to the Link task (with corresponding handoffs also present later in that targets file).
- other visible `LinkTimeCodeGeneration` conditions/setters include `Microsoft.Cpp.WholeProgramOptimization.props:24-26` and `Microsoft.CppCommon.targets:1140`; none of the searched props/targets provided a visible condition tying the line-63 `.iobj` default itself to `LinkTimeCodeGeneration`.

Controlled scratch experiments established the behavioral boundary:

1. checkpoint/A1: `LinkTimeCodeGeneration` not explicitly written; no `/LTCGOUT`.
2. v0.9 Debug: `LinkTimeCodeGeneration=Default`; `/LTCGOUT` appeared.
3. removing only the Debug `Default` pin removed `/LTCGOUT`.
4. restoring the explicit LinkTimeCodeGeneration pins and adding `<LinkTimeCodeGenerationObjectFile />` in both configurations removed `/LTCGOUT` in both; Release still emitted plain `/LTCG`.

The exact cross-property emission rule is therefore in Link task command-line generation, not in the visible `Microsoft.Link.Common.props` condition. Do not invent an unobserved MSBuild condition.

General lesson:

**An explicitly written property can alter emission of another tool property even when the chosen value emits no switch of its own. "This value emits nothing" must be judged against the complete measured command line, not only the property's direct Switch/ReverseSwitch mapping.**

The v0.10 correction keeps explicit `LinkTimeCodeGeneration` ownership and pins `LinkTimeCodeGenerationObjectFile` explicitly empty in Debug and Release. W1 remains unchanged and must see no `/LTCGOUT:`.

If incremental LTCG (`/LTCG:INCREMENTAL`) is ever adopted, revisit this empty pin because `.iobj` output is then relevant.

## 17. Stage B and Stage C/D carry-forward from the LTCGOUT finding

- Any Stage B plugin project that explicitly sets `LinkTimeCodeGeneration` should also explicitly pin `LinkTimeCodeGenerationObjectFile` empty unless incremental LTCG is deliberately adopted.
- The Stage C build harness and Stage D CI command-line verification should reject unexpected `/LTCGOUT:` for the current plain-LTCG policy.
- Project files remain the policy owner; harness/CI verify rather than inject the setting.

---

## Close-out v0.5 change log (2026-10-10)

- Promoted header to accepted A3 v0.10 and pending Stage A repository close-out.
- Recorded Dave-ratified Plan section 30 deviation: six-index v0.10 status WAIVED, never PASS.
- Preserved the three explicitly supplied Claude section-3 corroboration points and the no-bytewise-proof limitation.
- Maintained permanent future compiler/toolset/codegen six-index requirement.
- Incorporated Claude final-gate review N1-N4 from section 4, with unverified Stage C/D mechanics explicitly deferred.
- Recorded README snapshot consistency assessment and live Git/repository action boundary.
