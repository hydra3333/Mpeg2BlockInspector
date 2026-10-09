# Stage A - Mpeg2BlockInspector / CNR3 Visual Studio Audit and Proposed Edits

**Filename:** `StageA_Inspector_CNR3_Audit_and_Proposed_Edits_v0_1.md`
**Version:** 0.1
**Date:** 2026-10-09
**Author:** migration ChatGPT chat
**Status:** PROPOSAL FOR CLAUDE COLD REVIEW - NO REPOSITORY FILES HAVE BEEN MODIFIED
**Controlling migration record:** `Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_7.md`

---

## 1. Scope

This is the Stage A implementation proposal for:

1. removing Win32/x86 from `Mpeg2BlockInspector.vcxproj`;
2. replacing `Mpeg2BlockInspector.sln` with an x64-only `VapourSynth-mpeg2Deblock.slnx`;
3. normalizing the inspector's Visual Studio build settings using the actual CNR3 console/self-test project as the primary reference and the CNR3 DLL project/workflow as cross-checks.

The inspector **source is frozen**. Its **project configuration is in scope**.

Nothing in this package changes the repository. All `.vcxproj` / `.slnx` files here are review candidates only.

---

## 2. Actual files audited

Inspector:

```text
Mpeg2BlockInspector.sln
Mpeg2BlockInspector.vcxproj
Mpeg2BlockInspector.vcxproj.filters
Mpeg2BlockInspector.vcxproj.user
```

CNR3 supplied seven-file bundle:

```text
cnr3.slnx
cnr3.vcxproj
cnr3.vcxproj.filters
cnr3.vcxproj.user
cnr3_cache_core_selftest.vcxproj
cnr3_cache_core_selftest.vcxproj.filters
cnr3_cache_core_selftest.vcxproj.user
```

CNR3 `main` cross-checks:

```text
1.BUILD.bat
.github\workflows\build-windows-x64-release.yml
selected FINAL_DOCS build-history material
```

---

## 3. Mandatory script-generated project-element inventory

The required XML inventory was generated mechanically with `lxml`, preserving source line numbers.

Counts:

```text
Inspector .vcxproj:        120 element records
CNR3 self-test .vcxproj:  107 element records
CNR3 DLL .vcxproj:        116 element records
TOTAL:                     343 element records
```

Generated evidence:

```text
StageA_vcxproj_element_inventory_v0_1.md
StageA_vcxproj_element_inventory_v0_1.csv
StageA_vcxproj_relevant_inventory_v0_1.csv
StageA_explicit_setting_matrix_v0_1.csv
```

This is the accounting mechanism required by the migration design record: explicit CNR3 elements are not allowed to disappear merely because they were omitted from a hand checklist.

---

## 4. Mechanical Stage A proposal

### A1 - remove Win32 configurations only

Candidate:

```text
Mpeg2BlockInspector_A1_x64only_DELETIONS_ONLY.vcxproj
```

SHA-256:

```text
87acd9ad1c94e5545f84fe57857c076781ca499523d2a80545919ae571dc7a57
```

Method:

- exact byte-line deletion from the supplied current project;
- 58 lines removed;
- no retained x64 line rewritten;
- no line added;
- current `ProjectGuid` retained;
- `<Keyword>Win32Proj</Keyword>` retained.

Removed blocks are exactly:

```text
ProjectConfiguration Debug|Win32
ProjectConfiguration Release|Win32
Debug|Win32 Configuration PropertyGroup
Release|Win32 Configuration PropertyGroup
Debug|Win32 PropertySheets ImportGroup
Release|Win32 PropertySheets ImportGroup
Debug|Win32 LinkIncremental PropertyGroup
Release|Win32 LinkIncremental PropertyGroup
Debug|Win32 ItemDefinitionGroup
Release|Win32 ItemDefinitionGroup
```

Review diff:

```text
A1_Win32_removal.diff
```

### A2 - replace old `.sln` with x64-only `.slnx`

Candidate:

```text
VapourSynth-mpeg2Deblock_A2_PROPOSED.slnx
```

SHA-256:

```text
fa24efcd73401a38604e2f4228b07d8b960abcbfb66da22c02908e9d1cdb0754
```

Candidate content:

```xml
<Solution>
  <Configurations>
    <Platform Name="x64" />
  </Configurations>
  <Project Path="Mpeg2BlockInspector.vcxproj" Id="f4b1a357-b93c-7aab-3946-9c7a95523c9b" />
</Solution>
```

This follows the supplied working CNR3 `.slnx` structure.

The inspector project GUID is retained as the `.slnx` project Id, lower-cased in the same form used by CNR3.

The old `.sln` solution GUID is not carried into `.slnx`; the supplied working CNR3 `.slnx` likewise contains project IDs but no separate solution GUID.

### A3 - proposed x64 settings normalization

Candidate:

```text
Mpeg2BlockInspector_A3_PROPOSED_SETTINGS_v0_1.vcxproj
```

SHA-256:

```text
a86ec5b561abd278bd8dd305f0305c6d54bf0e6736f6c592075899683f2e8921
```

This candidate is based on A1, not on the original Win32-bearing project.

Review diff:

```text
A3_Settings_from_A1.diff
```

---

## 5. Explicit CNR3 self-test settings classification

The primary reference is `cnr3_cache_core_selftest.vcxproj`; `cnr3.vcxproj` is the second comparison column.

| Setting / area | CNR3 self-test | Inspector proposal | Classification / reason |
|---|---|---|---|
| Debug/Release x64 only | x64 only | x64 only | REUSE UNCHANGED - Dave ratified |
| `VCProjectVersion` | `18.0` | keep `18.0` | REUSE UNCHANGED |
| `ProjectGuid` | CNR3 identity | keep inspector GUID | REUSE WITH IDENTITY ADJUSTMENT |
| `Keyword` | `Win32Proj` | keep `Win32Proj` | REUSE UNCHANGED - native C/C++ project keyword, not target platform |
| `RootNamespace` | self-test name | leave absent | NOT APPLICABLE / no demonstrated inspector need |
| `WindowsTargetPlatformVersion` | `10.0.28000.0` | leave absent | DELIBERATELY DIFFERENT - Dave ratified no SDK pin |
| `ConfigurationType` | Application | Application | REUSE UNCHANGED |
| `UseDebugLibraries` | true/false | true/false | REUSE UNCHANGED |
| `PlatformToolset` | `v145` | `v145` | REUSE UNCHANGED |
| `CharacterSet` | Unicode | leave absent | NOT APPLICABLE - inspector is legacy C/narrow-character code |
| `PreferredToolArchitecture` | x64 | **add x64** | REUSE UNCHANGED - selects 64-bit build tools, not target architecture |
| Release `WholeProgramOptimization` | true | **add true** | REUSE UNCHANGED - proper optimized Release candidate |
| Property-sheet imports | standard platform user props | retain x64 imports | REUSE UNCHANGED; no x64 user props exists on Dave's machine |
| `LinkIncremental` | not explicit | retain inspector `false` | DELIBERATELY DIFFERENT - preserve current known build setting |
| Warning level | Level3 | Level3 | REUSE UNCHANGED |
| SDL checks | true | **keep false** | DELIBERATELY DIFFERENT - frozen classic C source requires it |
| `_CRT_SECURE_NO_WARNINGS` | absent | **keep** | DELIBERATELY DIFFERENT - frozen classic CRT calls |
| `_DEBUG` / `NDEBUG` | explicit | **add appropriate symbol** | REUSE WITH INSPECTOR DEFINES; source review found no `assert`, so `NDEBUG` is not expected to alter inspector logic |
| `_CONSOLE` | explicit | **add** | REUSE WITH INSPECTOR DEFINES - standard console configuration marker |
| `NOMINMAX` | explicit | leave absent | NOT APPLICABLE - no CNR3/Windows min/max collision rationale in inspector |
| `CNR3_SELFTEST_CONSOLE` | explicit | leave absent | CNR3-SPECIFIC |
| C++20 / conformance | explicit | leave absent | NOT APPLICABLE - inspector compiles C files |
| VapourSynth includes | explicit | leave absent | NOT APPLICABLE |
| Precompiled header | `NotUsing` | **add `NotUsing`** | REUSE UNCHANGED - makes current no-PCH intent explicit |
| Debug Optimization | Disabled | **add Disabled** | REUSE UNCHANGED / explicit intent |
| Release Optimization | MaxSpeed | **add MaxSpeed** | REUSE UNCHANGED - code-generation change; requires six-index gate |
| Release FavorSizeOrSpeed | Speed | **add Speed** | REUSE UNCHANGED - code-generation change; requires gate |
| AVX2 | on | **leave off / absent** | DELIBERATELY DIFFERENT - Dave ratified inspector AVX2 OFF |
| Release inline expansion | AnySuitable | **add AnySuitable** | REUSE UNCHANGED - code-generation change; requires gate |
| Release intrinsics | true | **add true** | REUSE UNCHANGED - code-generation change; requires gate |
| Debug intrinsics | true | leave default | DELIBERATELY DIFFERENT - unnecessary for debug inspector |
| Debug WPO | false | **add false** | REUSE UNCHANGED / explicit intent |
| Release WPO | true | **add true** | REUSE UNCHANGED - code-generation change; requires gate |
| PDB compiler debug format | ProgramDatabase | **add both configs** | REUSE UNCHANGED - retains useful symbols, including optimized Release |
| Link subsystem | Console | Console | REUSE UNCHANGED |
| Generate linker debug info | true | true | REUSE UNCHANGED |
| UAC | false | leave current default | DEFAULT / no inspector-specific reason to alter manifest behavior |
| Explicit OutputFile | self-test exe | leave default project output | NOT NEEDED - project name already yields correct EXE name |
| Debug LTCG | Default | **add Default** | REUSE UNCHANGED / explicit intent |
| Release LTCG | UseLTCG | **add UseLTCG** | REUSE UNCHANGED - pairs with `/GL`; code-generation change; requires gate |
| Segment heap | true | true | REUSE UNCHANGED |
| Release COMDAT folding | self-test not explicit; DLL currently false | **keep inspector true** | DELIBERATELY DIFFERENT - inspector already true; CNR3 DLL provenance is conflicted/profiling-specific |
| Release optimize references | self-test not explicit | **keep inspector true** | KEEP CURRENT - already `/OPT:REF` equivalent |
| Source/header membership | CNR3-specific | keep inspector list | PROJECT-SPECIFIC |
| `.filters` | CNR3-specific organization | keep inspector file byte-unchanged | KEEP CURRENT |
| `.vcxproj.user` | empty | keep inspector empty | REUSE UNCHANGED |

---

## 6. CNR3 workflow-only settings cross-check

The current CNR3 GitHub workflow deliberately spells out additional effective Release compiler/linker switches that are not all explicit XML entries in `cnr3.vcxproj`.

| CNR3 workflow switch | Inspector proposal | Reason |
|---|---|---|
| `/MD` | no explicit XML addition yet | DEFAULT/INHERITED in CNR3 `.vcxproj`; retain MSBuild normal runtime selection and verify effective command line at gate |
| `/EHsc` | not applicable | C++ exception handling; inspector sources are C |
| `/MP` | no explicit XML addition | build-throughput setting only; CNR3 `.vcxproj` does not explicitly carry it |
| `/fp:precise` | **add `FloatingPointModel=Precise` Debug+Release** | CNR3 records precise FP as deliberate; MSVC documents `/fp:precise` as default. Making it explicit protects intent without choosing `/fp:fast` |
| `/Gy` | **add `FunctionLevelLinking=true` in Release** | CNR3 workflow deliberately uses it; appropriate with optimized Release and `/OPT:REF` |
| `/Zc:inline` | no explicit XML addition | C++-oriented / supplied by MSBuild policy; no need to force it into the legacy C project |
| `/GS` | no explicit XML addition | leave compiler/MSBuild security default; no CNR3 `.vcxproj` explicit element to copy |
| `/OPT:REF` | already explicit as `OptimizeReferences=true` | KEEP CURRENT |
| `/OPT:NOICF` | do not adopt | CNR3 DLL-specific/conflicted provenance; inspector keeps `EnableCOMDATFolding=true` |
| `/DEBUG` | already explicit via `GenerateDebugInformation=true` | KEEP CURRENT |

Microsoft documentation cross-check used for the proposal:

- `PreferredToolArchitecture=x64` selects 64-bit compiler/tools and does not change output platform.
- `/fp:precise` is the MSVC default floating-point behavior.
- `FunctionLevelLinking=true` maps to `/Gy`.
- `WholeProgramOptimization=true` maps to `/GL`.
- linker LTCG is the matching link-time code generation control.

---

## 7. Why A3 is intentionally a substantive build change

This is not merely formatting.

The proposed Release configuration makes optimization intent explicit and aligns the inspector's Release project with the proven CNR3 console-project pattern where applicable:

```text
/O2      MaxSpeed
/Ot      Favor Speed
/Ob2     AnySuitable inline expansion
/Oi      intrinsics
/Gy      function-level linking
/GL      whole-program optimization
/LTCG    link-time code generation
/Zi      ProgramDatabase symbols
/fp:precise explicit
```

AVX2 is **not** adopted.

SDL remains **off**.

`_CRT_SECURE_NO_WARNINGS` remains.

COMDAT folding remains **on**.

Because A3 changes code generation, it is acceptable only if the agreed Stage A gate passes.

---

## 8. Settings deliberately not copied

The proposal deliberately does **not** add:

```text
WindowsTargetPlatformVersion
CharacterSet=Unicode
RootNamespace
ConformanceMode
LanguageStandard=stdcpp20
NOMINMAX
CNR3_SELFTEST_CONSOLE
VapourSynth include directories
EnableEnhancedInstructionSet=AVX2
CNR3 OutputFile name
CNR3 UAC policy
CNR3 DLL COMDAT=false
C++ exception-handling settings
```

These are either project-specific, C++/VapourSynth-specific, expressly rejected for the inspector, or governed by an already-ratified different policy.

---

## 9. Files deliberately unchanged

Stage A proposes no changes to:

```text
Mpeg2BlockInspector.vcxproj.filters
Mpeg2BlockInspector.vcxproj.user
any inspector C/H source
Stage1_Inspector_Analyzer_v0_2.py
```

The `.filters` source/header paths are already correct for the restructured repository.

All three supplied `.vcxproj.user` files are effectively empty.

---

## 10. Stage A commit/application sequence after review

If Claude and Dave approve:

### Commit A1

Apply only the deletion-only Win32 removal.

No setting additions.

### Commit A2

`git rm` old:

```text
Mpeg2BlockInspector.sln
```

and add:

```text
VapourSynth-mpeg2Deblock.slnx
```

### Commit A3

Apply the reviewed settings delta from:

```text
A3_Settings_from_A1.diff
```

Named staging only; no `git add -A`.

---

## 11. Stage A validation gate after A3

Required:

1. open the new `.slnx` in VS2026;
2. confirm Debug/Release, x64 only;
3. rebuild Debug x64;
4. rebuild Release x64;
5. compare warning code/file/line to the known baseline and explain any new warning;
6. verify frozen source hashes unchanged;
7. run all six tracked inspector/index reproductions;
8. require all six `.idx` outputs byte-identical;
9. specifically require LP SHA-256:

```text
849b6a9c411a7db837268af3ac54501a06f5f1158e68d5245ce2b3ec40a0d011
```

10. check tracked file status after Visual Studio opens/builds;
11. record final A3 project SHA-256.

If the substantive Release optimization settings fail the regression, stop and diagnose; do not weaken the gate.

---

## 12. Requested Claude review

Please cold-review:

1. whether the mandatory inventory accounts for the actual supplied project files;
2. A1 as deletions-only Win32 removal;
3. A2 `.slnx` structure and reuse of the inspector project GUID;
4. every A3 addition, especially the Release optimization/LTCG settings;
5. the decision to make `/fp:precise` and `/Gy` explicit based on the CNR3 workflow cross-check;
6. every CNR3 setting deliberately rejected/not copied;
7. whether A3 should remain one reviewed settings change or be split further for attribution.

No repository edit should occur until Claude review and Dave ratification.

---

## 13. Generated candidate/evidence files

```text
StageA_vcxproj_element_inventory_v0_1.md
StageA_vcxproj_element_inventory_v0_1.csv
StageA_vcxproj_relevant_inventory_v0_1.csv
StageA_explicit_setting_matrix_v0_1.csv

Mpeg2BlockInspector_A1_x64only_DELETIONS_ONLY.vcxproj
A1_Win32_removal.diff

VapourSynth-mpeg2Deblock_A2_PROPOSED.slnx

Mpeg2BlockInspector_A3_PROPOSED_SETTINGS_v0_1.vcxproj
A3_Settings_from_A1.diff
A1_to_A3_full.diff
```

All three candidate XML files parse successfully.

---

## 14. Key SHA-256 identities

Supplied current inspector project:

```text
Mpeg2BlockInspector.vcxproj
e383cbce4eaae1ab5953aa6334d433ea1af4d977c8eae9a2db8699c6c658375f
```

A1 candidate:

```text
87acd9ad1c94e5545f84fe57857c076781ca499523d2a80545919ae571dc7a57
```

A2 candidate `.slnx`:

```text
fa24efcd73401a38604e2f4228b07d8b960abcbfb66da22c02908e9d1cdb0754
```

A3 candidate:

```text
a86ec5b561abd278bd8dd305f0305c6d54bf0e6736f6c592075899683f2e8921
```
