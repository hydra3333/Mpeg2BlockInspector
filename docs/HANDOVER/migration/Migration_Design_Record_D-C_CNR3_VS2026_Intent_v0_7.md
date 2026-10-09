# Migration / Visual Studio Design Record - D-C Intent, CNR3 Configuration Transfer and Developer Handback

**Filename:** `Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_7.md`
**Version:** 0.7
**Date:** 2026-10-09
**Drafted by:** migration ChatGPT chat
**Cold-reviewed by:** migration Claude chat
**Ratified by:** Dave
**Status:** Current ratified migration-design baseline for Stage A audit/proposal work; to be updated again at migration close-out.
**Supersedes:** `Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_6.md`
**Scope:** Repository migration, Visual Studio 2026 solution/project normalization, build-system scaffolding, validation, and handback to the technical-development chats.
**Does not authorize:** Stage 2 algorithm implementation or MPEG-2 deblocking implementation.

---

## 1. Purpose

This document records the current migration end-state and method after:

- repository rename and restructure;
- first post-restructure validation;
- Dave's decision to remove Win32/x86 completely;
- Dave's decision that the `Mpeg2BlockInspector` project configuration is in scope for improvement while its source remains frozen;
- the decision to use CNR3's command-line/self-test project as the primary proven reference for the inspector;
- the decision to create a buildable VapourSynth MPEG-2 deblocker DLL placeholder before returning to technical development;
- adoption of a subtractive / exclusion-first CNR3 settings audit, cross-checked by an independent target-requirements audit;
- Claude's reviews of the Stage A/B plan and the v0.5 design record / v0.1 common handback;
- confirmation of Dave's installed Windows SDKs;
- confirmation that no per-user x64 MSBuild property sheet exists;
- recovery of proven Visual Studio 2026 environment and MSBuild-discovery patterns;
- Dave's decision not to pin a Windows SDK version;
- Dave's clarification that Deblock4 is historical/reference material only and may be recycled where appropriate, but is not an active project or required current migration input;
- adoption of one common Developer Handback for both technical-development chats.

---

## 2. Current published repository checkpoint

GitHub repository:

```text
https://github.com/hydra3333/VapourSynth-mpeg2Deblock
```

Active local repository:

```text
E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock
```

Retained rollback/reference repository:

```text
E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector
```

Published post-restructure HEAD:

```text
a9c782acb525943881e65b2b3f8f0484521a01c5
```

Published lightweight tag:

```text
vapoursynth-mpeg2deblock-post-restructure
```

The old tree is retained as rollback/reference material. It is not the active build/test tree.

---

## 3. What the earlier restructure established

Current repository layout includes:

```text
src\Mpeg2BlockInspector\
tools\
TESTING\
VHSC_samples\
docs\
vs\VapourSynth-mpeg2Deblock\
```

The inspector remains named:

```text
Mpeg2BlockInspector
```

The umbrella repository/product identity is:

```text
VapourSynth-mpeg2Deblock
```

The first post-move Visual Studio Release x64 rebuild passed:

```text
1 succeeded
0 failed
```

and reproduced the known 17 warning instances.

Two representative functional migration runs produced byte-identical indexes and demonstrated that tools, VPY files, source media and the rebuilt executable were being used from the new repository tree.

Dave waived the remaining planned runs for that earlier path/restructure gate.

That waiver does not apply to the forthcoming build-definition changes.

---

## 4. Revised Visual Studio end-state

The intended end-state is:

```text
Solution:
    VapourSynth-mpeg2Deblock.slnx

Platform:
    x64 only

Configurations:
    Debug
    Release

Projects:

    Mpeg2BlockInspector
        command-line Application / EXE
        C
        existing frozen inspector source

    mpeg2Deblock
        VapourSynth API4 Dynamic Library / DLL
        C++
        placeholder/build skeleton only at migration completion
```

Exact plugin/project capitalization and public plugin identity remain subject to the Stage B naming decision.

Both projects are to appear in one Visual Studio 2026 solution and remain independently selectable for Build, Rebuild, Clean and Properties.

---

## 5. Important frozen/non-frozen distinction

The `Mpeg2BlockInspector` source is frozen.

The `Mpeg2BlockInspector` Visual Studio project configuration is not frozen.

The inspector `.vcxproj` is therefore a working starting point, not an untouchable authority.

Dave explicitly requires the command-line project configuration to be checked and corrected using the proven CNR3 command-line/self-test project as an important reference.

Any resulting build-definition change must pass the full regression gate defined below.

No frozen C source is to be changed merely to make a Visual Studio setting easier to enable.

---

# STAGE A - INSPECTOR AND UMBRELLA SOLUTION

## 6. Stage A goals

Stage A will:

1. remove Win32/x86 from the inspector project;
2. remove x86 from the solution;
3. retain Debug x64 and Release x64;
4. replace the old `.sln` with `VapourSynth-mpeg2Deblock.slnx`;
5. keep the actual command-line project named `Mpeg2BlockInspector`;
6. compare and normalize the command-line project configuration against the proven CNR3 console/self-test project;
7. preserve inspector functional output exactly.

---

## 7. Stage A comparison references

Primary CNR3 executable reference:

```text
cnr3_cache_core_selftest.vcxproj
```

Secondary comparison:

```text
cnr3.vcxproj
```

Solution reference:

```text
cnr3.slnx
```

Also inspect:

```text
*.vcxproj.filters
*.vcxproj.user
```

The CNR3 DLL project is included as a second settings column because settings common to both CNR3 projects may indicate deliberate Visual Studio conventions.

DLL-specific settings must not be transferred to the inspector merely because the CNR3 DLL uses them.

---

## 8. Dual-pass / subtractive audit method

The settings audit deliberately attacks the problem from both directions.

### Pass A - CNR3 retention/exclusion

For the relevant CNR3 project, presume every explicit setting may embody useful prior work.

A setting is removed or changed only when there is a stated reason such as:

```text
NOT APPLICABLE
CNR3-SPECIFIC
WRONG FOR THIS TARGET
SOURCE-CONSTRAINED
USER/MACHINE-LOCAL
SUPERSEDED
DELIBERATELY DIFFERENT
```

For Stage B this becomes stronger: start from a byte copy of the CNR3 DLL project and account for every changed/deleted line.

### Pass B - target requirements

Independently ask what the target project should contain.

This checks for:

- settings CNR3 leaves at Visual Studio defaults;
- settings embodied in workflow/build scripts instead of `.vcxproj`;
- source-level build dependencies;
- hidden environment/property-sheet dependencies;
- requirements specific to the MPEG-2 projects.

### Reconciliation

Any difference between Pass A and Pass B becomes an explicit review item.

The aim is that no CNR3 setting can disappear merely because nobody remembered to ask about it.

---

## 9. Required classification

Every relevant setting is to receive one of:

```text
REUSE UNCHANGED
REUSE WITH NAME/PATH ADJUSTMENT
NOT APPLICABLE TO THIS PROJECT
DELIBERATELY DIFFERENT
DEFAULT IN CNR3 - LEAVE AT DEFAULT
USER/MACHINE-LOCAL - RECORD BUT DO NOT COPY
PROVISIONAL - TECHNICAL DEVELOPMENT DECISION NOT YET FINAL
```

Every `DELIBERATELY DIFFERENT` entry requires a reason.

Every `PROVISIONAL` entry must be carried into the final Developer Handback so it is not mistaken for a ratified algorithm/design decision.

A script-generated inventory is REQUIRED for the explicit CNR3 project elements so every meaningful project line/property is accounted for. The audit table must account for every relevant item emitted by that inventory. This is the mechanical check that prevents an explicit CNR3 setting from being silently lost.

---

## 10. Known inspector-specific deviations

### SDL

Inspector:

```text
SDLCheck = false
```

This remains appropriate because enabling SDL checks turns classic calls in the frozen decoder-derived C source into build errors.

The source will not be edited merely to enable SDL.

### CRT deprecation suppression

Retain:

```text
_CRT_SECURE_NO_WARNINGS
```

for the frozen classic C source.

### C++ settings

CNR3 C++ language-standard and C++-specific conformance choices are not automatically meaningful for the C inspector.

### VapourSynth dependencies

The inspector does not use VapourSynth and therefore does not inherit:

```text
VapourSynth include paths
CNR3_SELFTEST_CONSOLE
CNR3 plugin definitions
NOMINMAX solely because CNR3 uses it
```

unless another independent reason is identified.

### AVX2

Ratified migration policy for the inspector:

```text
AVX2 OFF
```

Reason:

- inspector correctness/output is the primary requirement;
- speed is not a demonstrated bottleneck;
- enabling AVX2 would unnecessarily add a CPU requirement and alter generated code;
- no evidence presently justifies that change.

---

## 11. Win32/x86 removal

Dave has explicitly decided to remove Win32/x86.

This is to be a separate, reviewable change.

For `Mpeg2BlockInspector.vcxproj`, remove only the Win32 configuration material.

Do not remove:

```xml
<Keyword>Win32Proj</Keyword>
```

because `Win32Proj` is the Visual Studio native C/C++ project keyword, not a declaration that the target platform must be Win32.

Retain the current `ProjectGuid`.

The Win32-removal edit should be mechanically deletions-only, with x64 material byte-identical before and after.

---

## 12. `.sln` to `.slnx`

The old:

```text
Mpeg2BlockInspector.sln
```

will be removed when the new:

```text
VapourSynth-mpeg2Deblock.slnx
```

is added.

The solution will initially contain the inspector during Stage A and will gain the plugin placeholder in Stage B.

The solution exposes x64 only.

No duplicate old/new solution files should remain in the final tree.

---

## 13. Machine-state findings established

Dave checked for:

```text
%LOCALAPPDATA%\Microsoft\MSBuild\v4.0\Microsoft.Cpp.x64.user.props
```

Result:

```text
NO x64 user property sheet found
```

Therefore no such per-user x64 property sheet is presently supplying hidden settings to the inspector.

Installed Windows SDK include versions are:

```text
10.0.22621.0
10.0.26100.0
10.0.28000.0
```

CNR3 currently pins `10.0.28000.0`, but Dave has now ratified a different policy for this project:

```text
DO NOT PIN A SPECIFIC WINDOWS SDK VERSION
```

The build should use the appropriate currently installed SDK selected by the Visual Studio/MSBuild environment, and the build log must record the actual SDK/toolchain used.

This is an explicit, documented deviation from the current CNR3 project configuration.

---

## 14. Toolset and version policy

### Platform toolset

Keep the explicit Visual Studio 2026 platform toolset:

```text
v145
```

Changing the major toolset is a deliberate compiler upgrade and therefore remains an explicit project decision.

### Windows SDK

Do not pin a specific SDK version.

Every controlled build log should record which Windows SDK was actually used.

### VapourSynth headers

The plugin project will keep the vendored VapourSynth header release identity in one file:

```text
third_party\vapoursynth\include\VERSION.txt
```

Other documents should refer to that file rather than repeatedly hard-coding a release number that will eventually age.

### Documentation versions

Stable authority-document names/locations should be used where possible.

The final common handback may record versions as "current at handback", but should avoid unnecessary version duplication throughout the prose.

Frozen/version-bearing tool identities such as `Stage1_Inspector_Analyzer_v0_2.py` remain exact.

---

## 15. Stage A commit sequence

Preferred sequence:

### A-1 - remove Win32 configurations

Remove Win32 project configurations only.

Expected character:

```text
deletions only
```

Retain `Win32Proj` and the existing project GUID.

### A-2 - replace `.sln` with `.slnx`

Remove:

```text
Mpeg2BlockInspector.sln
```

and add:

```text
VapourSynth-mpeg2Deblock.slnx
```

### A-3 - apply reviewed settings normalization

Apply separately reviewed settings changes.

Do not combine unrelated project-setting changes into the Win32-removal step.

Named Git staging is required. Do not use `git add -A`.

---

## 16. Stage A validation gate

If compiler/linker/build settings change, Stage A must pass all of the following.

### Build

Rebuild:

```text
Debug | x64
Release | x64
```

### Warnings

Compare warnings by:

```text
warning code
file
line
```

Do not merely compare the warning count.

Any new warning must be examined and explained.

### Frozen source hashes

Frozen inspector-source hashes must remain unchanged.

### Functional regression

Run all six tracked index cases.

All six regenerated `.idx` files must be byte-identical to their established baselines.

Mandatory LP SHA-256:

```text
849b6a9c411a7db837268af3ac54501a06f5f1158e68d5245ce2b3ec40a0d011
```

This also closes the previously deferred requirement to run the LP `_2` test before Stage 2 depends on that clip.

### Visual Studio rewrite check

After opening/building the `.slnx`:

```text
git status --short
```

must show no unexpected Visual Studio rewrite of tracked project/solution files.

Also inspect:

```text
git status --short --ignored
```

to confirm generated Visual Studio state remains under already ignored output/cache areas.

---

# STAGE B - VAPOURSYNTH DLL PLACEHOLDER

## 17. Stage B purpose

Stage B creates the final project/build-system position for the future MPEG-2 deblocker.

It does not implement the deblocking algorithm.

Expected conceptual layout:

```text
src\
    Mpeg2BlockInspector\
    mpeg2Deblock\

vs\
    VapourSynth-mpeg2Deblock\
        VapourSynth-mpeg2Deblock.slnx
        Mpeg2BlockInspector.vcxproj
        Mpeg2BlockInspector.vcxproj.filters
        mpeg2Deblock.vcxproj
        mpeg2Deblock.vcxproj.filters
```

Names remain subject to the naming decision.

---

## 18. Stage B primary method

Start from the latest current CNR3 DLL `.vcxproj` and `.filters` as the proven baseline.

The default for an explicit CNR3 setting is:

```text
KEEP
```

unless there is a documented reason to change it.

The final diff from CNR3 to the new MPEG-2 DLL project is itself part of the audit evidence.

Every changed/deleted line should be attributable to:

```text
identity/name change
source-list change
path adjustment
known CNR3-specific item
Dave-ratified technical difference
```

The independent settings checklist remains a cross-check.

---

## 19. Stage B decisions that must not happen accidentally

Before the DLL project files are finalized, explicitly review:

```text
project name
DLL filename
source-folder name
VapourSynth identifier
VapourSynth namespace
display name
C++ language standard
VapourSynth header release
API minor/profile selection
AVX2
floating-point mode
COMDAT folding
```

Windows SDK policy is already ratified:

```text
do not pin a specific SDK version
```

Where Dave does not yet want to settle a technical-development decision, the project configuration and handback must mark it:

```text
PROVISIONAL
```

rather than presenting it as a considered algorithm/design choice.

---

## 20. Placeholder source policy

Preferred placeholder form:

```text
entry point only
```

That means:

- include the relevant VapourSynth API4 header;
- export `VapourSynthPluginInit2`;
- call `configPlugin`;
- register no filter functions.

This proves:

- include-path correctness;
- API header use;
- export configuration;
- DLL linking;
- basic VapourSynth loadability.

It does not implement:

```text
Deblock
frame processing
index reading
filter registration
algorithm behaviour
```

and therefore does not pre-empt Stage 2 technical development.

This preferred form still requires Dave to ratify plugin identity/namespace before finalization.

---

## 21. CNR3 evidence beyond the seven Visual Studio files

The Stage B audit must also inspect the latest current forms of relevant:

```text
CNR3 build scripts
CNR3 GitHub workflow
CNR3 handover/build-history documents
plugin source/header dependencies
third_party\vapoursynth\include\VERSION.txt
VapourSynth API headers
```

The purpose is to capture not just what CNR3 sets, but why settings were introduced.

Deblock4 may be consulted only as historical/reference material when it contains a useful proven implementation pattern. It is not an active project, it is not authoritative for this project, and its old scripts are not assumed current or superior to CNR3.

---

# BUILD HARNESS / VS2026 ENVIRONMENT

## 22. Visual Studio discovery policy

Historical CNR3/Deblock4 work proved that the x64 Visual Studio environment can be established through `VsDevCmd.bat`, but the final harness must not hard-code:

```text
Visual Studio major-version directory
Visual Studio edition
```

Discover the current Visual Studio installation with `vswhere.exe`.

The Visual Studio and MSBuild discoveries MUST use the same selection criteria so they select the same current installation and remain compatible with Community, Professional, Enterprise or Build Tools installations.

Current candidate pattern:

```bat
set "VSWHERE=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"

for /f "usebackq tokens=*" %%i in (`"%VSWHERE%" -latest -products * -requires Microsoft.Component.MSBuild Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath`) do set "VSINSTALL=%%i"

if not defined VSINSTALL goto :fail

set "VSDEVCMD=%VSINSTALL%\Common7\Tools\VsDevCmd.bat"

if not exist "%VSDEVCMD%" goto :fail

echo Using Visual Studio at: %VSINSTALL%
```

The exact command is to be verified on Dave's machine before the build harness is accepted.

---

## 23. When `VsDevCmd.bat` is required

MSBuild does not require the calling batch to manually configure the compiler environment when MSBuild itself is discovered and invoked correctly.

`VsDevCmd.bat` remains useful when Microsoft command-line tools such as:

```text
dumpbin
```

are used directly by the migration gate/build harness.

When `VsDevCmd.bat` is called:

1. capture its exit code immediately;
2. fail on non-zero;
3. restore the intended project directory afterwards;
4. verify required direct tools such as `dumpbin` with `where`.

A structured `:run` helper is preferred if the final current CNR3 build harness supports that style.

---

## 24. MSBuild discovery

Do not hard-code the MSBuild executable.

Use the same `vswhere.exe` product/component selection criteria used for the Visual Studio installation discovery:

```bat
for /f "usebackq tokens=*" %%i in (`"%VSWHERE%" -latest -products * -requires Microsoft.Component.MSBuild Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -find MSBuild\**\Bin\MSBuild.exe`) do set "MSBUILD=%%i"
```

The final harness must fail clearly if no MSBuild path is returned.

The selected `VSINSTALL` and `MSBUILD` paths must be printed in the log and checked during harness validation to confirm that both discoveries resolved to the same Visual Studio installation.

This candidate command is to be verified on Dave's machine before the build harness is accepted.

---

## 25. Solution-level build routine

A reusable solution-build routine is preferred.

It should accept at least:

```text
configuration
solution directory
solution filename
```

and build the complete umbrella solution with the x64 platform, for example:

```bat
"%MSBUILD%" <solution> /m /t:Clean;Build /p:Configuration=<Debug-or-Release> /p:Platform=x64
```

The harness must capture the exit code immediately and fail on any non-zero result.

This becomes particularly useful after Stage B, when the `.slnx` contains both projects.

---

## 26. Build-harness source policy

The primary current reference is the latest available proven CNR3 build plumbing.

Historical Deblock4 batch material may be reused only where it contains a useful safeguard or implementation pattern.

Rule:

```text
CURRENT CNR3 BUILD MATERIAL IS THE PRIMARY REFERENCE.

DEBLOCK4 IS HISTORY/REFERENCE ONLY.

OLDER SCRIPT VERSIONS ARE EVIDENCE ONLY UNLESS THEY CONTAIN
A USEFUL SAFEGUARD MISSING FROM THE CURRENT REFERENCE.
```

The final build harness should not be reconstructed solely from remembered or quoted historical fragments.

Each significant build step should:

- display what it is doing;
- capture the exit code immediately;
- stop on failure;
- log the actual tools/environment used.

---

## 27. Stage B build gate

The placeholder DLL must build under the agreed x64 configurations.

For the entry-point-only placeholder, validate at least:

```text
dumpbin /exports
```

and require:

```text
VapourSynthPluginInit2
```

to be exported.

A simple VapourSynth load smoke test may additionally verify that the plugin namespace exists while exposing no filter functions.

---

## 28. Protecting the inspector during Stage B

Record SHA-256 hashes of the Stage A accepted:

```text
Mpeg2BlockInspector.vcxproj
Mpeg2BlockInspector.vcxproj.filters
```

After Stage B:

- if both remain byte-identical, one LP inspector smoke run is sufficient;
- if either differs, repeat all six inspector index regressions.

This replaces subjective judgement with a mechanical trigger.

---

# FINAL MIGRATION CLOSE-OUT

## 29. One common Developer Handback

There will be one shared migration handback:

```text
docs\HANDOVER\MPEG2_Deblocking_Developer_Handback_<version>.md
```

It is common to both the ChatGPT and Claude technical-development chats.

The individual ChatGPT and Claude handover documents should point to the common handback rather than duplicate migration facts such as:

```text
repository paths
solution/project setup
migration gate results
hashes
build-harness state
final migration checkpoint
```

This avoids divergence between two independent accounts of the same migration.

---

## 30. Common handback provenance

The final common handback header must state:

```text
drafted by migration ChatGPT
cold-reviewed by migration Claude
ratified by Dave
date
```

It must not use a ChatGPT- or Claude-specific filename prefix.

It is to be stored under:

```text
docs\HANDOVER\
```

and committed with the final migration material.

---

## 31. Documentation to update at close-out

At migration completion:

- update the common Developer Handback;
- update the ChatGPT role-specific handover to point to it;
- update the Claude role-specific handover to point to it;
- explicitly correct stale Gate C language;
- explicitly record provenance of earlier handover edits;
- produce/finalize the migration summary;
- record final solution/project identities and paths;
- record every final build-setting decision;
- record which settings remain PROVISIONAL;
- record build/test/hash results;
- optionally clarify `NOTICE.md` regarding decoder-derived source location and Stage 1 modifications without altering frozen source files.

---

## 32. Handback gate

The migration is not considered ready for return to technical development merely because both projects build.

Before handback:

1. ChatGPT updates the common Developer Handback to its final candidate version.
2. Claude cold-reviews the final migration state and common handback against actual repository evidence.
3. Dave resolves any review findings and ratifies the handback.
4. Final migration commits are pushed.
5. Final repository status/tag/checkpoint is recorded.
6. Only then does Dave return to the main ChatGPT and Claude technical-development chats.

---

## 33. What remains outside this migration

This migration does not authorize:

```text
Stage 2 experiment implementation
MPEG-2 deblocking algorithm implementation
index-consumption algorithm implementation
pixel filtering
AVX2 filter implementation
final VapourSynth filter-function/API contract beyond the placeholder identity
```

Those remain work for the proper technical-development workflow after handback.

---

## 34. Immediate next work

The migration is now in position to begin Stage A audit/proposal work.

Next steps:

1. produce the REQUIRED script-generated complete Stage A project-element inventory;
2. perform the dual-pass/reconciliation comparison;
3. produce the settings-transfer/deviation table;
4. prepare exact proposed Stage A edits without applying them;
5. Claude cold-reviews those proposed edits;
6. Dave resolves/ratifies;
7. only then apply Stage A project/solution changes;
8. execute the Stage A build/regression gate.

No Stage A project-setting change or Stage B project creation is authorized merely by this document.

---

## 35. Change log

### v0.7 - 2026-10-09

- Finalized the current Stage A migration-design baseline after Claude's follow-up review.
- Made the script-generated CNR3 project-element inventory mandatory rather than preferred.
- Required Visual Studio and MSBuild `vswhere` discovery to use the same `-products *` and component-selection criteria.
- Required the selected Visual Studio and MSBuild paths to be logged and checked as resolving to the same installation.
- Kept the exact discovery commands subject to one machine verification before the build harness is accepted.

### v0.6 - 2026-10-09

- Incorporated Claude's review of v0.5 and the common handback v0.1.
- Recorded Dave's decision not to pin a Windows SDK version.
- Kept explicit Visual Studio 2026 toolset `v145`.
- Changed Visual Studio bootstrap policy from hard-coded version/edition path to `vswhere` discovery.
- Required build logs to identify actual toolchain/SDK used.
- Made `third_party\vapoursynth\include\VERSION.txt` the single header-release identity source.
- Clarified stable authority-document naming/version policy.
- Recorded inspector AVX2 OFF as the migration policy.
- Clarified Deblock4 as historical/reference material only.
- Formalized one common Developer Handback for both technical-development chats.
- Required final handback provenance: drafted by migration ChatGPT, cold-reviewed by migration Claude, ratified by Dave.
- Retained US-ASCII-compatible punctuation.
