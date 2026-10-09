# Stage A Visual Studio Normalization Execution Plan

**Filename:** `StageA_Visual_Studio_Normalization_Execution_Plan_v0_2.md`
**Version:** 0.2
**Date:** 2026-10-09
**Drafted by:** migration ChatGPT chat
**Reviewed against:** `Claude_REVIEW_OF_ChatGPT_StageA_Audit_Proposal_v0_2.md`
**Controlling migration design:** `Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_7.md`
**Execution status:** READY FOR A1 + A2 when Dave gives GO
**Scope:** Stage A only - inspector project normalization and umbrella `.slnx`.
**Does not authorize:** Stage B DLL placeholder work or Stage 2 technical implementation.

---

## 1. Purpose

This document is the operational runbook for Stage A.

It converts the migration design and Claude's accepted/revised Stage A review into a bounded execution sequence:

```text
A1
    ->
A2
    ->
mandatory pre-A3 checkpoint
    ->
A3 v0.2 drafting
    ->
Claude cold review
    ->
Dave ratification
    ->
A3 application
    ->
full Stage A gate
```

No step may silently collapse into the next.

---

## 2. Current execution boundary

Current state:

```text
A1: ACCEPTED AS PACKAGED - NOT YET APPLIED
A2: ACCEPTED AS PACKAGED - NOT YET APPLIED

A3 v0.1: REVIEW HISTORY ONLY - DO NOT APPLY
A3 v0.2: NOT YET CREATED

Pre-A3 checkpoint: NOT YET RUN
```

Claude's Stage A review v0.2 is the controlling review input for this execution plan.

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
- use exact pasted command output as evidence rather than assumptions.

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

# A3 v0.2 GENERATION

## 20. A3 v0.1 is superseded for application

Do not apply:

```text
Mpeg2BlockInspector_A3_PROPOSED_SETTINGS_v0_1.vcxproj
```

It remains review/history material only.

A3 v0.2 is a fresh proposal based on:

```text
accepted A1 project
+
checkpoint effective command lines
+
full CNR3 reconciliation
+
ratified D1/D2/D3
```

---

## 21. Full CNR3 reconciliation requirement

A3 v0.2 must mechanically account for:

```text
56 CNR3 self-test setting rows
57 CNR3 DLL setting rows
113 total rows
```

The spreadsheet must include, keyed by project + source line:

```text
setting
condition/context
value
disposition
reason
```

Use only Design Record v0.7 section 9 disposition vocabulary.

A validation script must exit non-zero if any required:

```text
disposition
reason
```

is blank.

No hand-written summary table is an acceptable substitute.

---

## 22. Explicit no-defaults policy

For every output-affecting compiler/linker/manifest/ABI setting measured at the checkpoint:

- write the currently effective value explicitly in A3 v0.2;
- unless the setting is one of the deliberately changed settings below.

The objective is:

```text
explicit XML
=
checkpoint effective behavior
```

except for reviewed deliberate changes.

The Windows SDK version remains deliberately unpinned.

---

## 23. Ratified A3 deliberate changes

### D1 - Release code generation

Explicitly adopt:

```text
/O2
/Ot
/Ob2
/Oi
/Gy
/GL
/LTCG
```

with the corresponding MSBuild XML elements.

### D2 - Windows SDK

Do not write a specific `WindowsTargetPlatformVersion`.

Record the actual SDK selected by each gate.

### D3 - Debug optimizer-related settings

Explicitly use CNR3's values:

```text
FavorSizeOrSpeed = Speed
InlineFunctionExpansion = AnySuitable
IntrinsicFunctions = true
```

### Inspector AVX2

Keep AVX2 off and explicitly pin the current non-AVX2 state as represented by MSBuild.

### SDL / CRT

Explicitly retain:

```text
SDLCheck = false
_CRT_SECURE_NO_WARNINGS
```

### COMDAT / OPT:REF

Retain inspector's reviewed behavior:

```text
EnableCOMDATFolding = true
OptimizeReferences = true
```

---

## 24. A3 v0.2 review package

Before application, create a new review package containing at minimum:

```text
A3 v0.2 candidate .vcxproj
A1 -> A3 v0.2 exact diff
full 113-row reconciliation spreadsheet
reconciliation validation script + PASS output
checkpoint Debug detailed log
checkpoint Release detailed log
extracted pre-A3 cl.exe/link.exe commands
proposed A3 cl.exe/link.exe commands or predicted XML mapping
command-line delta analysis
six-index checkpoint results
warning baseline
actual SDK/toolchain evidence
```

Then send to Claude for cold review.

Do not apply A3 v0.2 before that review and Dave's ratification.

---

# A3 APPLICATION AND FINAL STAGE A GATE

## 25. Apply accepted A3

After Claude approval and Dave ratification:

- apply by accepted candidate byte copy;
- verify candidate SHA-256;
- named staging;
- inspect exact diff;
- commit A3.

If the reviewed package specifically authorizes another application mechanism, follow that later ruling instead.

---

## 26. Detailed post-A3 build

Rebuild:

```text
Debug | x64
Release | x64
```

with detailed logging equivalent to the checkpoint.

Capture effective:

```text
cl.exe command
link.exe command
toolchain
SDK
warnings
```

---

## 27. Command-line delta proof

Compare pre-A3 checkpoint command lines with post-A3 command lines.

Required result:

- explicitly pinned settings that preserve previous effective behavior produce no unintended semantic change;
- deliberate command-line changes correspond exactly to D1/D3 and other specifically reviewed differences;
- no unexplained switch appears/disappears.

If an unexplained change exists, Stage A fails pending diagnosis.

---

## 28. Warning comparison

Compare pre-A3 checkpoint to post-A3 by:

```text
code
file
line
stage
```

With `/GL` and `/LTCG`, some warnings may move from compile to link/LTCG phase.

A location/stage shift is not automatically a new defect, but must be explained.

No unexplained warning difference is accepted.

---

## 29. Frozen source gate

Recompute SHA-256 for:

```text
src\Mpeg2BlockInspector\getpic.c
src\Mpeg2BlockInspector\mpeg2dec.c
tools\Stage1_Inspector_Analyzer_v0_2.py
```

Required:

```text
getpic.c
e80239cfe73a0c04490a9bf131714861254ed1d7d095b052aac616a887ef0eca

mpeg2dec.c
8e6053ccb3a40be8c0d985f2e35124bf728d1f61df9b6d0c01b71e13e13b0947

Stage1_Inspector_Analyzer_v0_2.py
8e0d58305ee4fe518c25b67bdbe74acc4fb392486f23e6137862d916e5e02cda
```

Any mismatch is a hard stop.

---

## 30. Final six-index gate

Run all six cases again.

Every regenerated `.idx` must be byte-identical to section 18 baselines.

Mandatory LP SHA-256:

```text
849b6a9c411a7db837268af3ac54501a06f5f1158e68d5245ce2b3ec40a0d011
```

No waiver/representative subset for the final Stage A gate.

---

## 31. Record new accepted binary/project identities

After Stage A passes, record:

```text
Release Mpeg2BlockInspector.exe SHA-256
Debug Mpeg2BlockInspector.exe SHA-256 if useful
Mpeg2BlockInspector.vcxproj SHA-256
Mpeg2BlockInspector.vcxproj.filters SHA-256
VapourSynth-mpeg2Deblock.slnx SHA-256
```

The accepted `.vcxproj` and `.filters` hashes become the Stage B inspector-protection baseline.

---

## 32. Final Git/Visual Studio state

Run:

```bat
git status --short
git status --short --ignored
```

Required:

```text
no unexpected tracked files
only expected ignored VS/build state
```

Record the output.

---

## 33. Stage A close-out decision

Stage A is PASS only when all of these are true:

```text
A1 accepted/applied/committed
A2 accepted/applied/committed
pre-A3 checkpoint PASS
A3 v0.2 reviewed/ratified
A3 applied/committed
Debug build PASS
Release build PASS
warning delta explained
compiler/linker delta explained
frozen source hashes PASS
six indexes PASS
Git/VS state PASS
accepted hashes recorded
```

Only then may Stage B begin.

Do not push/finalize/tag outside the already agreed migration push policy.

---

## 34. Evidence to preserve

Preserve at least:

```text
A1 SHA proof
A2 SHA proof
A1/A2 commit hashes
checkpoint Debug detailed log
checkpoint Release detailed log
pre-A3 effective compiler/linker commands
checkpoint warning list
checkpoint SDK/toolchain data
checkpoint Release EXE SHA
checkpoint six-index results
A3 v0.2 reconciliation spreadsheet
reconciliation validator output
Claude A3 v0.2 review
A3 commit hash
post-A3 detailed logs
post-A3 compiler/linker commands
command-line delta report
post-A3 warning report
frozen source hash report
final six-index results
final project/solution hashes
final Git status outputs
```

These feed the migration close-out and common developer handback.

---

## 35. Change log

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
