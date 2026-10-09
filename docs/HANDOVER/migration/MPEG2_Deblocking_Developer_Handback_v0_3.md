# MPEG-2 Index-Driven Deblocking Project - Common Developer Handback After Repository Migration

**Filename:** `MPEG2_Deblocking_Developer_Handback_v0_3.md`
**Version:** 0.3
**Date:** 2026-10-09
**Drafted by:** migration ChatGPT chat
**Cold-review status:** migration Claude has reviewed the handback/design approach and the current migration policy; final evidence-based handback review remains required after Stage A/B completion
**Ratification status:** Dave has ratified the migration policy decisions explicitly recorded below; this v0.3 remains PROVISIONAL until final migration close-out
**Intended recipients:** both the main ChatGPT and Claude technical-development chats
**Repository location when final:** `docs\HANDOVER\`
**Status:** PROVISIONAL - migration remains in progress
**Do not treat this version as authority or as authorization to resume Stage 2.**

---

## 1. Purpose

This is the single common migration handback for both technical-development chats.

It exists to prevent ChatGPT and Claude from receiving divergent accounts of the repository migration.

It records:

- what migration work has been completed;
- the active repository identity;
- where source, projects, tests and authority documents live;
- the state of the inspector;
- the Visual Studio end-state being established;
- the future plugin-project placeholder being created;
- migration validation evidence;
- migration/build decisions;
- decisions deliberately left to technical development;
- what the developer chats must read and verify before resuming work.

The individual ChatGPT and Claude handovers should point to this document for migration facts rather than repeat them.

This v0.2 is an interim draft. It must be updated against the final repository state, cold-reviewed by migration Claude, and ratified by Dave before handback.

---

## 2. Repository identity

GitHub:

```text
https://github.com/hydra3333/VapourSynth-mpeg2Deblock
```

Active local repository:

```text
E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock
```

Retained old rollback/reference tree:

```text
E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector
```

The old tree is not the active development tree.

---

## 3. Published migration checkpoint

Published post-restructure HEAD:

```text
a9c782acb525943881e65b2b3f8f0484521a01c5
```

Published lightweight tag:

```text
vapoursynth-mpeg2deblock-post-restructure
```

That tag marks the successful repository rename/restructure checkpoint before Visual Studio configuration normalization.

A later final migration checkpoint/tag may supersede it as the normal technical-development handback point.

---

## 4. Current repository layout

Current important locations:

```text
src\Mpeg2BlockInspector\
    frozen Stage 1 inspector C/H source

tools\
    Stage1_Inspector_Analyzer_v0_2.py

TESTING\
    inspector BAT/VPY regression/test scripts

VHSC_samples\
    tracked recordings, indexes and test evidence

docs\REPOSITORY\
    repository-authoritative technical documents

docs\HANDOVER\
    AI orientation/handover documents

vs\VapourSynth-mpeg2Deblock\
    Visual Studio solution/project area
```

Stage 2 experimental Python, when the proper development workflow resumes it, belongs under:

```text
experiments\stage2\
```

It was deliberately not created as an empty directory during migration.

---

## 5. Technical project authority remains separate from migration

Migration work has not replaced or rewritten the ratified MPEG-2 technical design.

The proper development chats must continue to use the current ratified repository/design documents as authority.

Important repository authority locations include:

```text
docs\REPOSITORY\02_INDEX_FORMAT_SPEC.md
docs\REPOSITORY\05_DECISIONS.md
docs\REPOSITORY\06_DEBLOCK_CONCEPT.md
```

Important Stage documents include the current ratified:

```text
Stage1_Evidence_and_Gate_Report
Stage2_Experiment_Design
```

Use the versions current at final handback.

The frozen analyzer's exact identity remains:

```text
tools\Stage1_Inspector_Analyzer_v0_2.py
```

Migration documents and this handback are orientation/build-state records, not substitutes for technical authority.

---

## 6. Stage 1 inspector status

Stage 1 was already:

```text
COMPLETE
PASS
FROZEN
```

before repository migration.

Important distinction established during migration:

```text
INSPECTOR SOURCE:
    frozen

INSPECTOR VISUAL STUDIO PROJECT CONFIGURATION:
    in scope for migration normalization
```

The source is not to be changed merely to accommodate build-setting preferences.

---

## 7. Frozen source identities

Migration baseline hashes include:

```text
src\Mpeg2BlockInspector\getpic.c
e80239cfe73a0c04490a9bf131714861254ed1d7d095b052aac616a887ef0eca

src\Mpeg2BlockInspector\mpeg2dec.c
8e6053ccb3a40be8c0d985f2e35124bf728d1f61df9b6d0c01b71e13e13b0947

tools\Stage1_Inspector_Analyzer_v0_2.py
8e0d58305ee4fe518c25b67bdbe74acc4fb392486f23e6137862d916e5e02cda
```

These remain protected through Visual Studio project normalization.

---

## 8. Repository migration already achieved

Completed work includes:

- GitHub repository renamed to `VapourSynth-mpeg2Deblock`;
- fresh production clone established at the new root;
- inspector source moved under `src\Mpeg2BlockInspector\`;
- Visual Studio material moved under `vs\VapourSynth-mpeg2Deblock\`;
- analyzer retained under `tools\`;
- test scripts repaired for the new tree;
- Python cache ignore rules added;
- repository notice/test-recording restrictions added;
- migration-era ChatGPT/Claude handovers updated;
- representative post-move regression evidence refreshed;
- migration commits pushed;
- post-restructure tag pushed.

---

## 9. Earlier restructure Gate C result

The restructured inspector was rebuilt in Visual Studio 2026 as:

```text
Release | x64
```

Result:

```text
1 succeeded
0 failed
```

The rebuilt executable appeared at the expected new-tree path.

The build produced the same known 17 warning instances as the pre-migration baseline.

Two representative tests were executed:

```text
TEST_2A_A001
TEST_2A_A001_blocky
```

Both:

- used the new-tree executable/tools/media;
- returned inspector exit code 0;
- validated successfully;
- regenerated indexes byte-identical to their tracked baselines.

Dave explicitly waived the remaining planned test runs for that earlier path/restructure gate.

Do not report that earlier gate as six-of-six.

---

## 10. Why migration remains open

After the repository restructure, Dave decided that the Visual Studio configuration should also be put into its intended final shape before technical development resumes.

Migration therefore additionally includes:

### Stage A

Final inspector/umbrella-solution normalization.

### Stage B

Creation of the future VapourSynth MPEG-2 deblocker DLL project as a buildable placeholder.

No deblocking implementation is included.

---

## 11. Intended final Visual Studio structure

Target:

```text
VapourSynth-mpeg2Deblock.slnx

    Mpeg2BlockInspector
        Application / EXE
        C
        Debug x64
        Release x64

    mpeg2Deblock
        Dynamic Library / DLL
        C++
        Debug x64
        Release x64
        placeholder/build-system project only
```

Win32/x86 is being removed completely from the inspector project and solution.

---

## 12. CNR3 as proven build reference

The working `vapoursynth-cnr3` Visual Studio project is the primary source of proven Visual Studio 2026 / VapourSynth build knowledge.

Its current comparison material includes:

```text
cnr3.slnx

cnr3.vcxproj
cnr3.vcxproj.filters
cnr3.vcxproj.user

cnr3_cache_core_selftest.vcxproj
cnr3_cache_core_selftest.vcxproj.filters
cnr3_cache_core_selftest.vcxproj.user
```

Migration uses:

```text
cnr3_cache_core_selftest.vcxproj
```

as the primary command-line/EXE reference for `Mpeg2BlockInspector`.

The CNR3 DLL project:

```text
cnr3.vcxproj
```

is the primary reference for the future `mpeg2deblock` DLL placeholder.

The purpose is to preserve hard-earned build/configuration knowledge rather than rediscover prior problems.

Deblock4 is not an active project and is not authority for this project. It may be consulted only as historical/reference material when an old implementation pattern is useful.

---

## 13. Settings-transfer discipline

Migration uses a dual-pass audit.

### CNR3-first / subtractive pass

Assume explicit CNR3 settings may be valuable and require a reason to discard or change them.

### Target-requirements pass

Independently check what the inspector or plugin project requires.

### Reconciliation

Any difference becomes explicit review material.

For Stage B, the intended method is especially conservative:

```text
start from CNR3 DLL project
change only what has a stated reason
use the diff as part of the audit record
```

This prevents useful CNR3 settings from disappearing silently.

A script-generated inventory of the relevant explicit CNR3 project elements is REQUIRED. The settings audit must account for every relevant item emitted by that inventory.

---

## 14. Visual Studio 2026 environment policy

Historical working paths demonstrated how VS2026 could be initialized, but the final build harness will not hard-code a Visual Studio major-version directory or edition.

The current Visual Studio installation is to be discovered with `vswhere.exe`.

`MSBuild.exe` is also to be discovered with `vswhere.exe`.

Both discoveries must use the same `-products *` and component-selection criteria so they select the same current Visual Studio installation, including where the installed product is Build Tools rather than a full IDE edition. The build log must print both resolved paths, and harness validation must confirm they belong to the same installation.

When Microsoft tools such as `dumpbin` are invoked directly, the harness may call the discovered Visual Studio installation's:

```text
Common7\Tools\VsDevCmd.bat
```

with:

```text
-arch=amd64 -host_arch=amd64
```

and must:

- capture the return code immediately;
- fail on non-zero;
- restore the project directory afterwards;
- verify required tools with `where`.

The final build log should identify the actual Visual Studio/MSBuild/toolchain environment used.

---

## 15. Windows SDK and toolset policy

Installed Windows SDK include versions observed during migration:

```text
10.0.22621.0
10.0.26100.0
10.0.28000.0
```

CNR3 currently pins `10.0.28000.0`.

Dave has explicitly chosen a different policy for this project:

```text
DO NOT PIN A SPECIFIC WINDOWS SDK VERSION
```

The current Visual Studio/MSBuild environment may select the appropriate installed SDK.

Every controlled build log must record the actual SDK/toolchain used.

The explicit Visual Studio 2026 platform toolset remains:

```text
v145
```

because changing the major compiler/toolset is a deliberate upgrade.

---

## 16. Per-user MSBuild property sheet

Checked:

```text
%LOCALAPPDATA%\Microsoft\MSBuild\v4.0\Microsoft.Cpp.x64.user.props
```

Result:

```text
not present
```

Therefore migration found no hidden x64 per-user property sheet supplying additional project settings.

---

## 17. Inspector-specific migration policy

Known inspector decisions include:

```text
source remains frozen
project configuration is in scope
SDLCheck remains OFF
_CRT_SECURE_NO_WARNINGS remains
AVX2 remains OFF
x64 only
Debug and Release remain
```

C++ language settings and VapourSynth-specific settings from CNR3 are not automatically applicable to the C inspector.

---

## 18. Stage A regression requirement

Because the inspector project file itself is being changed, the final Stage A gate is stronger than the earlier path-only migration gate.

Required:

```text
Debug x64 rebuild
Release x64 rebuild
warning comparison by code/file/line
frozen source hashes unchanged
all six tracked indexes reproduced byte-identically
```

Mandatory LP baseline:

```text
849b6a9c411a7db837268af3ac54501a06f5f1158e68d5245ce2b3ec40a0d011
```

The final handback must record actual results.

---

## 19. Stage B placeholder policy

The future DLL project is migration/build scaffolding only.

Preferred placeholder source:

```text
VapourSynthPluginInit2 entry point only
```

Expected behaviour:

- include the selected vendored VapourSynth API4 header;
- export `VapourSynthPluginInit2`;
- call `configPlugin`;
- register no filter functions.

It therefore proves plugin-specific build/load configuration without implementing the MPEG-2 filter.

No development chat should mistake the placeholder for an implemented deblocker.

---

## 20. VapourSynth header identity

The vendored VapourSynth header release is to be identified once in:

```text
third_party\vapoursynth\include\VERSION.txt
```

Other build and handback documents should refer to that file rather than duplicating a release number that will age.

The actual header/API choice remains a Stage B decision until finalized.

---

## 21. Stage B decisions still to be carried explicitly

Migration must not silently settle technical choices merely because CNR3 has values for them.

Items requiring explicit decision or provisional status include:

```text
plugin source-folder name
project name
DLL name
VapourSynth identifier
VapourSynth namespace
display name
C++ language standard
VapourSynth header/API profile
AVX2
floating-point mode
COMDAT folding
```

Windows SDK policy is already decided: no specific SDK pin.

The final common handback must distinguish:

```text
RATIFIED MIGRATION/BUILD CHOICE
```

from:

```text
PROVISIONAL TECHNICAL-DEVELOPMENT CHOICE
```

---

## 22. Stage B inspector-protection rule

After Stage A acceptance, record SHA-256 hashes of:

```text
Mpeg2BlockInspector.vcxproj
Mpeg2BlockInspector.vcxproj.filters
```

After Stage B:

- if both remain byte-identical to the Stage A accepted versions, one LP inspector smoke run is sufficient;
- if either differs, repeat all six inspector regression runs.

This is an objective mechanical trigger.

---

## 23. Build-harness direction

The final repository build harness should be based primarily on the latest current proven CNR3 build plumbing.

It should:

- discover Visual Studio with `vswhere`;
- discover MSBuild with `vswhere`;
- avoid hard-coded Visual Studio version/edition paths;
- build the umbrella `.slnx` for x64;
- support Debug and Release;
- fail immediately on errors;
- echo/log significant commands;
- record actual selected toolchain/SDK information;
- establish `VsDevCmd` only where direct Microsoft command-line tools require it;
- verify `dumpbin` before the Stage B export gate.

Historical Deblock4 build plumbing may be recycled where useful, but Deblock4 is not an active project or current configuration authority.

---

## 24. Things migration must not decide

Migration does not implement or settle:

```text
Stage 2 experiment algorithms
index-reading behaviour
frame-processing behaviour
deblocking strength calculations
pixel kernels
scalar deblocking implementation
AVX2 deblocking implementation
filter scheduling architecture
final filter function/API contract beyond placeholder identity/configuration
```

Those belong to the proper technical-development workflow and its authority documents.

---

## 25. Normal development workflow after handback

The agreed development workflow remains:

```text
ChatGPT drafts / implements
    ->
Claude independently cold-reviews
    ->
Dave resolves and ratifies
    ->
next implementation step
```

Migration does not alter that workflow.

---

## 26. Expected technical restart point

Unless later project authority changes it, the technical project remains at:

```text
Stage 1 complete / PASS / frozen
Stage 2 experiment design ratified
Stage 2 implementation not started
```

Migration work does not advance Stage 2.

The expected next technical-development activity remains the first authorized increment of the ratified Stage 2 experiment design.

This handback does not authorize that restart.

Dave will explicitly state when migration has closed and technical development may resume.

---

## 27. Final common handback architecture

This document is the shared migration-state handback for both developer chats.

The ChatGPT-specific and Claude-specific handovers should retain only:

```text
role-specific orientation
workflow/interaction guidance
references to technical authority
reference to this common migration handback
```

They should not repeat migration facts such as:

```text
paths
solution/project setup
migration gate results
hashes
build harness state
final migration checkpoint
```

Those facts belong here so there is one place to correct them.

---

## 28. What the final handback must add

Before this document becomes final, update it with:

- final migration commit(s);
- final HEAD;
- final tag/checkpoint;
- final `.slnx` path and project membership;
- final inspector project hash/settings;
- final DLL project path/name/settings;
- final placeholder-source identity;
- actual vendored VapourSynth header version from `VERSION.txt`;
- final API-profile choice;
- AVX2 decision/status for the plugin;
- floating-point decision/status;
- COMDAT decision;
- final build-harness filename/path;
- actual Visual Studio/MSBuild/toolset/SDK evidence;
- Debug and Release build results;
- six-index Stage A results;
- LP hash confirmation;
- Stage B export/load smoke-test result;
- post-Stage-B inspector smoke/regression result;
- final Git status;
- any NOTICE change;
- updated role-specific handover versions;
- Claude's final migration/handback review outcome;
- Dave's final ratification date.

---

## 29. Required final review

Before this handback is ready:

1. migration ChatGPT updates it against actual final repository evidence;
2. migration Claude cold-reviews it against that evidence;
3. Dave resolves discrepancies and ratifies the result;
4. the final reviewed version is stored under `docs\HANDOVER\`;
5. it is committed with the final migration material;
6. the role-specific ChatGPT and Claude handovers point to it;
7. Dave then provides the resulting repository/handback state to the proper technical-development chats.

Until then:

```text
THIS v0.2 IS ORIENTATION ONLY.
DO NOT RESUME PROJECT IMPLEMENTATION FROM IT.
```

---

## 30. Immediate migration status

The migration is now ready to begin the Stage A audit/proposal work.

The next sequence is:

1. complete the REQUIRED script-generated project-element inventory;
2. perform CNR3 subtractive/reference audit plus target-requirements audit;
3. reconcile them;
4. produce exact proposed Stage A edits;
5. Claude cold-reviews;
6. Dave ratifies;
7. apply edits;
8. execute Stage A build/regression gate;
9. proceed to separately reviewed Stage B.

---

## 31. Change log

### v0.3 - 2026-10-09

- Finalized the current common-handback baseline before Stage A execution.
- Made the script-generated CNR3 project-element inventory mandatory.
- Required Visual Studio and MSBuild `vswhere` discovery to use the same product/component selection and resolve to the same installation.
- Kept this handback explicitly provisional until final Stage A/B evidence is available and Claude performs the final cold review.

### v0.2 - 2026-10-09

- Converted to the single common handback architecture for both development chats.
- Added explicit draft/review/ratification provenance model.
- Incorporated Claude's review of v0.1 and design record v0.5.
- Recorded Dave's no-Windows-SDK-pin decision.
- Recorded explicit `v145` toolset policy.
- Replaced hard-coded Visual Studio path policy with `vswhere` discovery.
- Required actual toolchain/SDK evidence in build logs.
- Made `third_party\vapoursynth\include\VERSION.txt` the single header-release identity source.
- Recorded inspector AVX2 OFF.
- Clarified Deblock4 as historical/reference material only.
- Reduced duplicated version-number references.
- Kept US-ASCII-compatible punctuation.
