# Stage A Visual Studio 2026 / MSBuild Hard-Earned Knowledge

**Filename:** `StageA_VS2026_MSBuild_Hard_Earned_Knowledge_v0_2.md`
**Version:** 0.2
**Date:** 2026-10-10
**Status:** Durable migration knowledge through Claude acceptance and Dave ratification of A3 v0.9; post-A3 gate evidence remains outstanding.
**Scope:** Reusable lessons from normalizing the legacy Mpeg2BlockInspector project under Visual Studio 2026 / MSBuild v180. This is not MPEG-2/deblocking algorithm knowledge.

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

v0.9 still requires Claude's short cold review and Dave's ratification before application.

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
