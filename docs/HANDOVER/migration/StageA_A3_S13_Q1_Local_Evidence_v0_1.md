# Stage A A3 S13 / Q1 Local Evidence

**Filename:** `StageA_A3_S13_Q1_Local_Evidence_v0_1.md`  
**Version:** 0.1  
**Date:** 2026-10-09  
**Purpose:** Record Dave's local Visual Studio 2026 / MSBuild evidence gathered for Stage A A3 S13 and Claude Q1 before generation of an applyable A3 `.vcxproj` candidate.

---

## 1. Scope and status

This document records only evidence actually observed during the local A3 v0.7 pre-candidate work.

It does **not** authorize application of an A3 project file.

Current state:

- A3 v0.7 remains **PRE-CANDIDATE / NOT APPLYABLE**.
- The prerequisite check passed.
- The installed Visual Studio 2026 rule metadata was scanned successfully.
- The structural A3 pin table passed in pre-candidate mode.
- XML recognition is resolved for all currently tested items except `HighEntropyVA`, for which the installed VS2026 linker rule metadata contains no such property.
- Several former `S13_PENDING` names have now been resolved mechanically.
- Post-A3 binary checks for CFG, CET and High Entropy VA remain impossible until an A3 candidate is built.
- Claude Q1's tlog-derived expected-key work remains outstanding.

---

## 2. Local environment evidence

The A3 v0.7 prerequisite checker was run from:

`E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\A3_v0_7_PRE_CANDIDATE`

Observed output:

```text
Stage A A3 v0.7 prerequisite check
VSINSTALL=C:\Program Files\Microsoft Visual Studio\18\Community
MSBUILD=C:\Program Files\Microsoft Visual Studio\18\Community\MSBuild\Current\Bin\MSBuild.exe
PASS: same-installation MSBuild derivation.
Spectre policy: project setting explicitly Disabled; /Qspectre absent.
Required retained hardening: /GS, CFG, CET.
Required CPU target: /arch:AVX2.
/favor:blend: explicit in Debug and Release.
```

Consequences:

- Visual Studio installation selected:
  `C:\Program Files\Microsoft Visual Studio\18\Community`
- MSBuild is taken from the same Visual Studio installation:
  `C:\Program Files\Microsoft Visual Studio\18\Community\MSBuild\Current\Bin\MSBuild.exe`
- No Spectre-libraries component is required by current policy.

---

## 3. Installed VS2026 rule scan

Command:

```text
python scan_VS2026_rule_properties_v0_1.py --vs-install "C:\Program Files\Microsoft Visual Studio\18\Community"
```

Observed result:

```text
PASS: wrote 1704 recognized property definitions from C:\Program Files\Microsoft Visual Studio\18\Community\MSBuild\Microsoft\VC to StageA_A3_VS_rule_properties_generated.csv
```

Generated evidence file:

`StageA_A3_VS_rule_properties_generated.csv`

This file is machine-generated from Dave's installed VS2026 rule XML and must accompany this evidence document when supplied to Claude.

---

## 4. Structural pin-table validation

Command:

```text
python validate_StageA_A3_pin_table_v0_2.py --allow-s13-pending
```

Observed result:

```text
PASS: 138 structural pin rows; no duplicate keys/blanks; S13_PENDING allowed for pre-candidate.
```

Note:

- The current structural row count is **138**.
- Earlier references to 136 rows are superseded by the current v0.2 table after Q1/default-library coverage was added.

---

## 5. XML-recognition validation

Command:

```text
python validate_StageA_A3_xml_recognition_v0_1.py --allow-local-evidence-pending
```

Observed result:

```text
UNRESOLVED: | M3D_hev | Link/HighEntropyVA=true | property not found in installed rule XML; resolve by S13
UNRESOLVED: | M3R_hev | Link/HighEntropyVA=true | property not found in installed rule XML; resolve by S13
PASS-PRE-CANDIDATE: 2 XML items require S13/local resolution.
```

Interpretation:

- The installed rule metadata recognized all other XML items tested by the validator.
- `Link/HighEntropyVA=true` is **not** a recognized installed VS2026 rule property and must not be invented in the final project.

---

## 6. S13 scratch-project baseline

Scratch directory:

`E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\A3_v0_7_PRE_CANDIDATE\S13_SCRATCH`

Files:

- `Mpeg2BlockInspector_BASE.vcxproj`
- `Mpeg2BlockInspector_WORK.vcxproj`

Both were copied from the current repository inspector project before S13 changes.

Observed SHA-256 for both:

```text
87acd9ad1c94e5545f84fe57857c076781ca499523d2a80545919ae571dc7a57
```

Therefore BASE and WORK started byte-identical.

Visual Studio also created:

`Mpeg2BlockInspector_WORK.slnx`

when the scratch project was opened directly. This is scratch-only and is not repository evidence.

---

## 7. Spectre mitigation = explicitly Disabled

### 7.1 Property Pages observation

In VS2026:

- Configuration: All Configurations
- Platform: x64
- C/C++ -> Code Generation -> Spectre Mitigation

The UI already displayed **Disabled**.

Dave temporarily selected Enabled without saving, then re-selected Disabled and saved so that the project was dirty and Visual Studio had an opportunity to serialize the setting.

Comparison:

```text
fc /n "S13_SCRATCH\Mpeg2BlockInspector_BASE.vcxproj" "S13_SCRATCH\Mpeg2BlockInspector_WORK.vcxproj"
```

Observed:

```text
FC: no differences encountered
```

Conclusion:

- VS2026 Property Pages did **not** serialize Disabled because it is the existing/default UI state.
- Property-page non-serialization is not sufficient evidence for the no-defaults rule.

### 7.2 Installed rule-file evidence

Search result from `StageA_A3_VS_rule_properties_generated.csv`:

```text
...\v180\1033\cl.xml,CL,EnumProperty,SpectreMitigation,Spectre;SpectreLoad;SpectreLoadCF;false
```

The installed VS2026 rule metadata therefore recognizes:

```xml
<SpectreMitigation>false</SpectreMitigation>
```

Final A3 intent:

- write `<SpectreMitigation>false</SpectreMitigation>` explicitly in Debug and Release;
- gate `/Qspectre` as absent from both compiler command lines.

This satisfies N1 without relying on the current default.

---

## 8. Control Flow Guard - compiler

Using the scratch WORK project, Dave set:

- Configuration: All Configurations
- Platform: x64
- C/C++ -> Code Generation -> Control Flow Guard = Guard

Visual Studio wrote the following into both Debug and Release `ClCompile` sections:

```xml
<ControlFlowGuard>Guard</ControlFlowGuard>
```

Observed diff excerpts:

```text
<SDLCheck>false</SDLCheck>
<ControlFlowGuard>Guard</ControlFlowGuard>
```

for both configuration sections.

This is direct empirical S13 evidence.

---

## 9. Control Flow Guard - linker

The expected Linker -> Advanced Property Pages entry was not present in Dave's VS2026 UI.

Installed rule scan showed:

```text
...\v180\1033\link.xml,Link,BoolProperty,LinkControlFlowGuard,
```

Therefore the installed VS2026 linker rules recognize:

```xml
<LinkControlFlowGuard>true</LinkControlFlowGuard>
```

Final A3 intent:

- compiler side:
  `<ControlFlowGuard>Guard</ControlFlowGuard>`
- linker side:
  `<LinkControlFlowGuard>true</LinkControlFlowGuard>`

Post-A3 gate must additionally prove the effective linker/binary CFG state, including the expected `/GUARD:CF` behavior and non-zero CF function table/count in `dumpbin`.

---

## 10. CET compatibility

Search of installed rule definitions found:

```text
...\v180\1033\link.xml,Link,BoolProperty,CETCompat,
```

Therefore the installed VS2026 linker rules recognize:

```xml
<CETCompat>true</CETCompat>
```

No invented property is required.

Post-A3 `dumpbin` evidence remains required to prove the resulting binary is CET compatible.

---

## 11. Program database / debug-information properties

Installed VS2026 rules reported:

```text
CL EnumProperty   DebugInformationFormat     None;OldStyle;ProgramDatabase;EditAndContinue
CL StringProperty ProgramDataBaseFileName
Link EnumProperty GenerateDebugInformation  false;true;DebugFastLink;DebugFull
Link StringProperty ProgramDatabaseFile
Link BoolProperty FullProgramDatabaseFile
```

Current VS2026 Property Pages observed by Dave under Linker -> Debugging:

- **Generate Debug Info** = `Generate Debug Information (/DEBUG)`
- **Generate Program Database File** = `$(OutDir)$(TargetName).pdb`
- no separate visible `Generate Full Program Database File` row was present.

Recognized mappings:

```xml
<DebugInformationFormat>ProgramDatabase</DebugInformationFormat>
```

is the compiler debug-information format corresponding to `/Zi`.

```xml
<ProgramDataBaseFileName>...</ProgramDataBaseFileName>
```

is the compiler PDB-output property corresponding to `/Fd...`.

```xml
<ProgramDatabaseFile>$(OutDir)$(TargetName).pdb</ProgramDatabaseFile>
```

is the linker PDB output path.

`GenerateDebugInformation` remains the recognized linker debug-information property.

### Still to close

The exact final representation of the intended "Full PDB" policy must be stated carefully in the final pin table/gate. Current VS2026 UI evidence shows plain `/DEBUG`; the final A3 package must avoid relying on stale VS2022/older UI assumptions and must validate the actual post-build PDB/debug-directory result.

D6 remains:

- Release uses `/PDBALTPATH:%_PDB%`;
- post-A3 Release `dumpbin` `cv` entry must show the PDB **file name only**;
- Debug may retain its path.

---

## 12. High Entropy VA

### 12.1 Recognition result

No `HighEntropyVA` property exists in Dave's installed VS2026 `v180\1033\link.xml`.

Search returned no output for:

```text
HIGHENTROPY
HighEntropy
```

The pin-table recognition validator independently flagged exactly:

```text
Link/HighEntropyVA=true
```

for Debug and Release as unresolved.

### 12.2 Required resolution

Do **not** emit:

```xml
<HighEntropyVA>true</HighEntropyVA>
```

because the installed VS2026 rule metadata does not recognize it.

Final A3 intent:

- preserve high-entropy ASLR explicitly with linker switch `/HIGHENTROPYVA`, carried via `AdditionalOptions` unless a later current-toolchain evidence source establishes a dedicated recognized property;
- keep `RandomizedBaseAddress=true` / `/DYNAMICBASE`;
- prove post-A3 with `dumpbin` that **High Entropy VA** remains present.

The earlier checkpoint already established High Entropy VA in the PE characteristics; the A3 gate must preserve it.

---

## 13. `/Zc:inline` is not optimizer function inlining

Installed `cl.xml` search returned:

```text
Name="RemoveUnreferencedCodeData"
Switch="Zc:inline"
F1Keyword="VC.Project.VCCLCompilerTool.RemoveUnreferencedCodeData">
```

Therefore the exact recognized XML mapping is:

```xml
<RemoveUnreferencedCodeData>true</RemoveUnreferencedCodeData>
```

for checkpoint `/Zc:inline`.

Important distinction:

- `/Zc:inline` / `RemoveUnreferencedCodeData` is **not** the main optimizer setting that decides whether suitable small functions are expanded inline.
- performance-oriented inline expansion is represented separately by `InlineFunctionExpansion`, with Dave's ratified Debug policy using `AnySuitable` (`/Ob2`).

The final A3 pin table must keep these two concepts distinct.

---

## 14. Manifest settings

Installed VS2026 rule metadata establishes:

### `/MANIFEST`

Recognized linker property:

```xml
<GenerateManifest>true</GenerateManifest>
```

### `/manifestinput:...`

Recognized linker property:

```xml
<ManifestInput>...</ManifestInput>
```

The checkpoint value is the Visual C++ segment-heap manifest path used in the measured linker command.

### `/manifest:embed`

Direct context from installed `v180\1033\link.xml`:

```text
Name="ManifestEmbed"
DisplayName="Embed Manifest"
...
Switch="manifest:embed"
Visible="false"
F1Keyword="VC.Project.VCLinkerTool.ManifestEmbed">
```

Therefore the exact linker property is:

```xml
<ManifestEmbed>true</ManifestEmbed>
```

The installed `mt.xml` also contains an `EmbedManifest` property for the manifest tool. That is distinct from the linker property's `ManifestEmbed` mapping above and must not be substituted for it in the Link section.

---

## 15. Current `S13_PENDING` set and resolution status

The pre-candidate table currently contains 22 `S13_PENDING` rows.

They group as follows.

### Resolved pre-build names/values

- Debug + Release `/Zc:inline`
  - `ClCompile/RemoveUnreferencedCodeData=true`
- Debug + Release compiler `/Fd...`
  - `ClCompile/ProgramDataBaseFileName=...`
- Debug + Release CFG compile
  - `ClCompile/ControlFlowGuard=Guard`
- Debug + Release Spectre Disabled
  - `ClCompile/SpectreMitigation=false`
- Debug + Release `/manifest:embed`
  - `Link/ManifestEmbed=true`
- Debug + Release `/manifestinput:...`
  - `Link/ManifestInput=...`
- Debug + Release CFG link
  - `Link/LinkControlFlowGuard=true`
- Debug + Release CET
  - `Link/CETCompat=true`

### Partly resolved / final interpretation still required

- Debug + Release full-PDB rows
  - recognized debug/PDB properties are known;
  - final VS2026-specific representation/gate still needs to be settled without relying on obsolete UI assumptions.

### Post-build only

- Debug + Release full CFG state
  - must be proved through post-A3 `dumpbin`, including function table/count.
- Debug + Release CET-compatible state
  - must be proved through post-A3 `dumpbin`.

### Additional Q1 item

- High Entropy VA
  - no recognized `HighEntropyVA` rule property;
  - intended explicit resolution is `/HIGHENTROPYVA` in `AdditionalOptions` plus `dumpbin` proof.

---

## 16. Claude Q1: remaining work before final A3 candidate

The following remain outstanding:

1. **Tlog-derived expected keys**
   - derive CL/LINK expected-key coverage mechanically from the four preserved checkpoint tlogs;
   - do not rely on a hand-written expected-key list;
   - include the checkpoint default library list in coverage or a deliberate exception.

2. **Update pin-table rows**
   - replace the now-resolved `S13_PENDING` mappings with the recognized XML element/value or deliberate `AdditionalOptions` resolution;
   - update High Entropy VA rows to the non-invented resolution;
   - settle the final Full-PDB rows.

3. **Final validator**
   - must pass without `--allow-s13-pending`;
   - must include XML/rule recognition evidence;
   - must include tlog-derived expected-key coverage.

4. **Post-build binary gate**
   - CFG full binary state;
   - CET compatible;
   - High Entropy VA present;
   - D6 PDB filename-only behavior in Release;
   - standalone Release dependency rule;
   - `/fp:contract` absent;
   - all intended command-line deltas only.

5. **Six-index regression gate**
   - all six tracked indexes remain byte-identical.

No applyable A3 project file should be reviewed or applied before items 1-3 are complete.

---

## 17. Evidence files to give Claude

When this evidence is sent to Claude, include at minimum:

1. `StageA_A3_S13_Q1_Local_Evidence_v0_1.md`
2. `StageA_A3_VS_rule_properties_generated.csv`
3. current `StageA_A3_pin_table_v0_2.csv`
4. current pin-table and recognition validators
5. when generated, the tlog-derived expected-key artifact(s)
6. the latest A3 pre-candidate requirements and migration design/plan documents

The machine-generated VS rule-property CSV is primary recognition evidence and should not be replaced by a prose summary alone.

---

## 18. No repository mutation

All S13 work described above was performed in the external scratch/pre-candidate tree.

The production repository project was not modified by these S13 experiments.
