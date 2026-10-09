# Stage A Visual Studio Normalization Execution Plan

**Filename:** `StageA_Visual_Studio_Normalization_Execution_Plan_v0_3.md`  
**Version:** 0.3  
**Date:** 2026-10-09  
**Drafted by:** migration ChatGPT chat  
**Reviewed against:** `Claude_REVIEW_OF_ChatGPT_StageA_Audit_Proposal_v0_2.md`, `Claude_REVIEW_OF_ChatGPT_StageA_Checkpoint_Status_v0_1.md`, `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_2_Package_v0_1.md`, and `Claude_REVIEW_OF_ChatGPT_Migration_Plan_Update_Standalone_PyPI_v0_1.md`  
**Controlling migration design:** `Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_8.md` candidate, superseding v0.7 after Dave ratification  
**Execution status:** A1 + A2 + pre-A3 checkpoint COMPLETE; revised A3 proposal pending; A4 standalone split recommended as D4  
**Scope:** Stage A only - inspector project normalization, PE/default pinning, standalone Release EXE linkage, and umbrella `.slnx`.  
**Does not authorize:** Stage B DLL placeholder work or Stage 2 technical implementation.

---

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
revised A3 normalization proposal
    ->
Claude cold review
    ->
Dave ratification
    ->
A3 application + A3 gate
    ->
A4 Release /MD -> /MT proposal (if D4 ratified)
    ->
Claude review + Dave ratification
    ->
A4 application + standalone/six-index gate
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
Revised A3: NOT YET CREATED

A4 standalone Release runtime change: RECOMMENDED AS D4; not yet ratified/applied
```

The current review inputs are Claude's Stage A audit review, checkpoint closure, A3 v0.2 package review, and migration-plan update review.

---

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
- neither the Stage C harness nor the final GitHub workflow may inject `/MT`, override `PlatformToolset`, or maintain a second compile/link flag map;
- if standalone Release linkage is accepted, it must be encoded in `Mpeg2BlockInspector.vcxproj` itself.

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
ratified D1/D2/D3
+
Claude M3/S7/S8/S9 corrections
```

Under Claude's recommended D4 attribution model, revised A3 deliberately keeps Release `/MD`; standalone `/MT` becomes A4.

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

Use only Design Record v0.8 section 9 disposition vocabulary.

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

Release runtime is not an A3 exception under D4: it remains explicitly pinned to the checkpoint `/MD` value in A3 and changes separately in A4.

---

## 23. Revised A3 required settings

### D1 - Release optimization

Current Microsoft `/O2` behaviour already supplies the relevant optimization components. Revised A3 must explicitly represent/pin the already-effective Release behaviour, including:

```text
/O2
/Ot
/Ob2
/Oi
/GF
/Gy
```

The genuine D1 Release code-generation additions are:

```text
/GL
/LTCG
```

### D2 - Windows SDK

Do not write a specific `WindowsTargetPlatformVersion`.

Record the actual selected SDK at every gate. The pre-A3 checkpoint used:

```text
10.0.28000.0
```

### D3 - Debug optimizer-related settings

Explicitly use the ratified values:

```text
FavorSizeOrSpeed = Speed
InlineFunctionExpansion = AnySuitable
IntrinsicFunctions = true
```

### Compiler host

Set:

```text
PreferredToolArchitecture = x64
```

Post-A3 evidence must show both CL and LINK tool paths using:

```text
HostX64\x64
```

### Debug information

Normalize Debug compiler debug information from `/ZI` to `/Zi` as reviewed. The existing LNK4075 warning caused by `/EDITANDCONTINUE` with `/INCREMENTAL:NO` should therefore disappear; any different result requires explanation.

### Runtime library in A3

If D4 is ratified, keep the measured runtime explicitly during A3:

```text
Debug   MultiThreadedDebugDLL  /MDd
Release MultiThreadedDLL       /MD
```

A3 must not contain `/MT`; A4 owns that change.

### AVX2 / ISA floor

Inspector AVX2 remains OFF. Explicitly pin the current x64 non-AVX ISA state as:

```text
EnableEnhancedInstructionSet = StreamingSIMDExtensions2
/arch:SSE2
```

### SDL / CRT suppression

Explicitly retain:

```text
SDLCheck = false
_CRT_SECURE_NO_WARNINGS
```

Do not add `_DEBUG`, `NDEBUG` or `_CONSOLE` merely because CNR3 carries them; preserve the measured inspector define set.

### Warning-gate output settings (S7)

Explicitly pin the measured values on which the warning comparison depends:

```text
DiagnosticsFormat = Column            -> /diagnostics:column
UseFullPaths = true                   -> /FC
ExternalWarningLevel = Level3         -> /external:W3
WarningLevel = Level3                 -> /W3
TreatWarningAsError = false           -> /WX-
```

### Other compiler pins

Pin the measured effective values for at least:

```text
RuntimeLibrary
BufferSecurityCheck
BasicRuntimeChecks (Debug)
SupportJustMyCode (Debug)
CharacterSet = NotSet
CompileAs = CompileAsC
Optimization
FavorSizeOrSpeed
InlineFunctionExpansion
IntrinsicFunctions
DebugInformationFormat
FloatingPointModel = Precise
PrecompiledHeader = NotUsing
FunctionLevelLinking
WholeProgramOptimization
```

No C++ language-standard/conformance setting is to be forced into the C inspector without an independent reason.

### Linker / manifest pins and M3

Pin or explicitly encode the measured behaviour where MSBuild provides a supported property, including:

```text
SubSystem = Console
GenerateDebugInformation = true
GenerateManifest = true
EnableUAC / UACExecutionLevel at measured behaviour
RandomizedBaseAddress = true          -> /DYNAMICBASE
DataExecutionPrevention = true        -> /NXCOMPAT
TargetMachine = MachineX64
LargeAddressAware = true
OptimizeReferences / EnableCOMDATFolding at measured per-config values
LinkIncremental = false
```

For PE/load-config behaviours that do not map cleanly to a supported MSBuild property, do not invent XML properties. Use a documented `AdditionalOptions` pin only when technically justified and reviewed; otherwise make the pre/post `dumpbin` comparison the gate.

The checkpoint M3 baseline to preserve through A3 is:

```text
x64 PE32+
Large Address Aware
High Entropy Virtual Addresses
Dynamic Base
NX Compatible
no CET-compatible image flag
no fully enabled CFG image state
manifest generation present
Debug /OPT behaviour equivalent to NOREF/NOICF
```

Debug and Release dependency DLL-name sets must remain unchanged through A3 because A3 does not alter the runtime model.

### D6 - Release PDB path hygiene

Claude recommends `/PDBALTPATH:%_PDB%` so shipped Release artifacts contain only the PDB filename rather than an absolute local/CI path.

This is OPTIONAL distribution hygiene and remains a Dave-ratification item. If accepted, it belongs in a separately identified reviewed Release linker delta; do not slip it into A3 without recording D6.

---

## 24. Revised A3 review package

Before application, the package must contain at minimum:

```text
revised A3 candidate .vcxproj
A1 -> revised A3 exact diff
candidate SHA-256
full 113-row reconciliation CSV
validator + PASS output
checkpoint Debug detailed MSBuild log
checkpoint Release detailed MSBuild log
byte copies of four UTF-16 CL/LINK tlogs
verbatim full pre-A3 CL and LINK command lines
predicted/reviewed post-A3 CL and LINK mappings
command-line delta analysis
Debug and Release M3 dumpbin captures
PE/load-config/import comparison plan
normalized 20-Debug / 17-Release warning baselines
six-index checkpoint results + tracked-file baseline provenance
A1/A2 commit evidence
`git show --name-status 837df123` proving A2 delete/add only
vswhere Visual Studio/MSBuild discovery evidence
actual SDK/toolchain evidence
git status --short and --short --ignored evidence
```

The exact command-line transcriptions must be checked against the copied tlogs; elided material may contain only source/object lists, paths or default library lists.

Then send the package to Claude for cold review. Do not apply revised A3 before Claude approval and Dave ratification.

---

# A3 APPLICATION AND A3 GATE

## 25. Apply accepted A3

After Claude approval and Dave ratification:

- apply the accepted candidate byte-for-byte;
- verify candidate SHA-256;
- use named staging only;
- inspect exact diff and `git diff --cached --check`;
- commit A3 with no unrelated file.

No `/MT` change belongs in this commit if D4 is accepted.

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

Compare pre-A3 checkpoint and post-A3 command lines.

Required character:

- explicit pins of previously effective behaviour do not create unintended semantic changes;
- deliberate deltas correspond only to reviewed A3 changes such as D1, D3, `/ZI -> /Zi`, PreferredToolArchitecture and any explicitly ratified D6;
- Release remains `/MD` if D4 is accepted;
- no unexplained switch appears/disappears.

Any unexplained delta fails A3 pending diagnosis.

---

## 28. A3 PE/load-config/import proof

Run the same:

```text
dumpbin /headers /loadconfig /imports /dependents
```

against post-A3 Debug and Release executables.

Require unchanged semantic state for the M3 baseline:

```text
PE32+ x64
Large Address Aware
High Entropy VA
Dynamic Base
NX Compatible
no CET-compatible flag
no fully enabled CFG image
manifest behaviour
Debug /OPT behaviour
```

Because A3 retains `/MDd` and `/MD`, the dependency DLL-name sets must match the checkpoint sets at the DLL-name level. Function-level imports may change where D3 makes calls intrinsic, but any DLL-name change stops the gate.

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

If A3 passes, it becomes the normalization baseline for A4.

---

# A4 - STANDALONE RELEASE RUNTIME LINKAGE

## 32. D4 decision and A4 scope

Claude recommends D4 option (a): separate A4 for attribution.

If Dave ratifies D4, A4 changes exactly one semantic build setting in the inspector project:

```text
Release RuntimeLibrary
MultiThreadedDLL (/MD)
    ->
MultiThreaded (/MT)
```

This is a distribution decision, separate from Visual Studio normalization.

The change MUST be present in `Mpeg2BlockInspector.vcxproj`. A harness or GitHub action that obtains a standalone EXE only by injecting `/MT` fails the design.

If Dave rejects the split and instead folds `/MT` into A3, this runbook must be revised before application; do not improvise.

---

## 33. A4 proposal/review/application

Create a tiny A4 review package containing:

```text
accepted A3 project SHA
A4 candidate .vcxproj
A3 -> A4 exact diff
A4 candidate SHA
predicted command delta (/MD -> /MT only)
A3 Release dumpbin dependency baseline
standalone forbidden/allowed DLL rules
six-index A3 baseline identities
```

Claude reviews; Dave ratifies; then apply by byte copy, verify SHA, named-stage and commit A4 alone.

---

## 34. A4 build and command-line gate

Clean+Build Release | x64 using the same MSBuild route.

Required compiler delta from accepted A3:

```text
/MD disappears
/MT appears
```

No other unexplained compiler/linker switch change is permitted.

The project file must still carry all accepted A3 pins and `PreferredToolArchitecture=x64`; CL and LINK must still come from `HostX64\x64`.

Record the actual SDK used because with `/MT` the selected SDK's static UCRT implementation becomes part of the shipped EXE provenance.

---

## 35. A4 standalone dependency and PE gate

Run:

```text
dumpbin /headers /loadconfig /imports /dependents
```

The PE/load-config state that A4 is not intended to change must remain equivalent to A3:

```text
x64 PE32+
Large Address Aware
High Entropy VA
Dynamic Base
NX Compatible
no CET-compatible flag
no fully enabled CFG image
```

Release dependency DLL names must contain none of:

```text
VCRUNTIME*
MSVCP*
api-ms-win-crt-*
ucrtbase*
CONCRT*
VCOMP*
```

Allowed dependency names are the measured pre-A4 Release set after removing the dynamic C-runtime dependencies. From the current checkpoint evidence that expected allowed set is:

```text
KERNEL32.dll
```

If any additional DLL name appears, stop and review rather than silently widening the allow-list.

Function-level KERNEL32 imports may grow because the statically linked runtime itself uses Windows APIs; that is not by itself failure.

---

## 36. A4 warning, frozen-source and six-index gate

Compare Release warnings with accepted A3. Explain every difference.

Frozen source/analyzer identities must remain unchanged.

Run all six gated index cases again. Every `.idx` must remain byte-identical to the section 18 baseline.

This second six-index run is intentional: it isolates the standalone-runtime linkage change from A3 normalization.

Record the final standalone Release EXE SHA-256 and final accepted project SHA-256.

---

# STAGE A CLOSE-OUT

## 37. Final Git/Visual Studio state

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

## 38. Stage A PASS criteria

Stage A is PASS only when all applicable items are true:

```text
A1 applied/committed
A2 applied/committed
pre-A3 checkpoint PASS
revised A3 reviewed/ratified
A3 applied/committed
A3 Debug build PASS
A3 Release build PASS
A3 command-line delta explained
A3 M3 PE/import gate PASS
A3 warning delta explained
A3 frozen-source gate PASS
A3 six-index gate PASS

if D4 ratified:
    A4 reviewed/ratified
    A4 applied/committed
    A4 /MD -> /MT-only delta PASS
    A4 standalone dependency gate PASS
    A4 PE gate PASS
    A4 six-index gate PASS

final Git/VS state PASS
accepted project/binary hashes recorded
```

Only then may Stage B begin.

Do not push/finalize/tag outside the already agreed migration push policy.

---

## 39. Evidence to preserve

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
full 113-row reconciliation + validator PASS
Claude A3 v0.2 review
revised A3 package + review + ratification
A3 commit hash
post-A3 detailed logs/tlogs
post-A3 command-line delta report
post-A3 M3 dumpbin report
post-A3 warning report
A3 six-index results

if D4 ratified:
    A4 candidate/review/ratification
    A4 commit hash
    A4 Release detailed log/tlog
    A4 /MD -> /MT delta proof
    A4 standalone dependency/PE report
    A4 six-index results

frozen source hash reports
final project/solution hashes
final Git status outputs
```

These feed Design Record v0.8, Stage B protection baselines, migration close-out and the common Developer Handback.

---

## 40. Change log

### v0.3 - 2026-10-09

- Updated execution state: A1/A2 and the mandatory pre-A3 checkpoint are complete.
- Incorporated Claude's A3 v0.2 review M3 and S7-S9 findings.
- Recorded completed Debug/Release dumpbin M3 baseline measurement.
- Superseded the A3 v0.2 DRAFT candidate for application.
- Corrected D1 interpretation: `/O2` components including `/GF` are pins; `/GL` + `/LTCG` are the genuine D1 Release additions.
- Added explicit warning-output pins and HostX64 proof.
- Added PE/load-config/import gate.
- Added Dave's standalone Release requirement as a project-file requirement, not a CI override.
- Added Claude's recommended D4 A3/A4 split for clean attribution, pending Dave ratification.
- Added A4 `/MD -> /MT`-only proposal/application/gate with a second six-index regression.
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
- Added explicit AVX2-off pin requirement.
- Added command-line delta proof.
- Added `git status --short --ignored` to checkpoint/final gate.
- Added Stage A accepted-hash recording for the later Stage B protection trigger.
