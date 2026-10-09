# Stage A A3 Q1 / R1 / R4 Local Evidence Closure

**Filename:** `StageA_A3_Q1_R1_R4_Local_Evidence_Closure_v0_1.md`
**Version:** 0.1
**Date:** 2026-10-09
**Purpose:** Record closure of the local Visual Studio 2026 recognition/placement evidence (R1/S13) and checkpoint tlog-derived coverage evidence (R4) required by Claude Q1 before generation of an applyable A3 candidate.

---

## 1. Status

The following local evidence requirements are now complete:

- strict VS2026 rule recognition;
- strict MSBuild placement recognition;
- all prior `S13_PENDING` rows resolved;
- native checkpoint `.command.1.tlog` parsing;
- measured default linker-library coverage;
- exact tlog-token-to-pin-table reconciliation;
- explicit accounting for checkpoint error-reporting switches that are present in detailed MSBuild logs but omitted from native `.command.1.tlog` payloads.

Current result:

```text
R1 / S13 recognition: PASS
R4 tlog evidence: PASS
R4 tlog-to-pin reconciliation: PASS
S13_PENDING rows: 0
```

This evidence does **not** itself authorize application of A3.

The next process step is Claude cold review of the completed Q1 evidence and the superseding A3 candidate package generated from it.

---

## 2. Strict VS2026 recognition closure

The corrected rule scanner read the installed Visual Studio 2026 rule XML from:

```text
C:\Program Files\Microsoft Visual Studio\18\Community\MSBuild\Microsoft\VC
```

Observed scan result:

```text
PASS: wrote 1512 recognized property/DataSource definitions from C:\Program Files\Microsoft Visual Studio\18\Community\MSBuild\Microsoft\VC to StageA_A3_VS_rule_properties_generated_v0_3.csv
Toolset-folder counts: v160=16, v170=743, v180=753
UNSPECIFIED placement counts: v170=13, v180=13
```

Only `v180` definitions are permitted to satisfy Stage A A3 recognition.

The strict final recognition validator was run **without** `--allow-s13-pending`.

Observed result:

```text
PASS: 129 XML pin targets recognized in v180 with correct rule/tool, exact property name, enum/bool value and DataSource placement.
```

Consequences:

- no unresolved XML recognition rows remain;
- no `S13_PENDING` allowance remains;
- all recognized XML pins use the installed VS2026 `v180` rules;
- tool/rule confusion is rejected;
- enum/bool values are validated;
- MSBuild persistence/placement is validated.

---

## 3. Important R1 corrections carried

### 3.1 Link error reporting

The earlier incorrect candidate:

```text
Link/ErrorReporting=Queue
```

was rejected.

Installed v180 `link.xml` proves the correct linker property/value is:

```text
Link/LinkErrorReporting=QueueForNextLogin
```

for Debug and Release.

Compiler error reporting remains the separate CL property/value:

```text
ClCompile/ErrorReporting=Queue
```

### 3.2 Configuration-conditioned Link properties

Installed v180 `link.xml` showed all three properties below with:

```text
Persistence=ProjectFile
ItemType=<blank>
Label=<blank>
HasConfigurationCondition=true
```

Therefore these are configuration-conditioned `PropertyGroup` values rather than `Link` ItemDefinitionGroup metadata:

```text
Configuration/LinkIncremental=false
Configuration/GenerateManifest=true
Configuration/LinkControlFlowGuard=true
```

### 3.3 Spectre placement/value

Spectre mitigation is explicitly pinned Disabled.

Installed v180 rule evidence establishes the recognized value:

```text
SpectreMitigation=false
```

The strict recognition/placement validator now accepts its actual VS2026 persistence location.

Post-build gate still requires `/Qspectre` absent.

### 3.4 Full PDB

The final intended explicit linker setting is:

```text
Link/GenerateDebugInformation=DebugFull
```

to emit explicit full-debug information rather than relying on the bare `/DEBUG` default semantics.

### 3.5 High Entropy VA

No recognized `HighEntropyVA` XML property exists in installed v180 `link.xml`.

Therefore A3 must not invent:

```xml
<HighEntropyVA>true</HighEntropyVA>
```

Instead, the pin is:

```text
Link/AdditionalOptions includes /HIGHENTROPYVA %(AdditionalOptions)
```

with post-A3 `dumpbin` proof that High Entropy VA remains present.

---

## 4. Final compiler PDB S13 evidence

Dave observed in Visual Studio 2026 Property Pages:

Debug | x64:

```text
$(IntDir)vc$(PlatformToolsetVersion).pdb
```

Release | x64:

```text
$(IntDir)vc$(PlatformToolsetVersion).pdb
```

Therefore the final explicit compiler PDB pin for both configurations is:

```text
ClCompile/ProgramDataBaseFileName=$(IntDir)vc$(PlatformToolsetVersion).pdb
```

After this evidence was incorporated:

```text
S13_PENDING rows: 0
```

---

## 5. Preserved checkpoint tlogs

The four preserved checkpoint native command tlogs are:

```text
%TEMP%\mpeg2deblock_stageA_checkpoint\evidence\Debug_CL.command.1.tlog
%TEMP%\mpeg2deblock_stageA_checkpoint\evidence\Debug_link.command.1.tlog
%TEMP%\mpeg2deblock_stageA_checkpoint\evidence\Release_CL.command.1.tlog
%TEMP%\mpeg2deblock_stageA_checkpoint\evidence\Release_link.command.1.tlog
```

The native `.command.1.tlog` format was empirically established.

For CL, records alternate between:

```text
^<tracker key/source path>
<raw compiler argument payload>
```

The argument payload does not contain a literal `cl.exe` executable token.

The corrected extractor therefore treats non-`^` payload records as authoritative command payloads and verifies per-file consistency.

---

## 6. Native tlog extraction result

The corrected extractor was run against all four preserved checkpoint tlogs.

Observed result:

```text
EVIDENCE: CL C:\Users\u\AppData\Local\Temp\mpeg2deblock_stageA_checkpoint\evidence\Debug_CL.command.1.tlog: 16 payload record(s), 25 normalized token(s)
EVIDENCE: CL C:\Users\u\AppData\Local\Temp\mpeg2deblock_stageA_checkpoint\evidence\Release_CL.command.1.tlog: 16 payload record(s), 23 normalized token(s)
EVIDENCE: LINK C:\Users\u\AppData\Local\Temp\mpeg2deblock_stageA_checkpoint\evidence\Debug_link.command.1.tlog: 1 payload record(s), 16 normalized token(s)
EVIDENCE: LINK C:\Users\u\AppData\Local\Temp\mpeg2deblock_stageA_checkpoint\evidence\Release_link.command.1.tlog: 1 payload record(s), 18 normalized token(s)
PASS: wrote 82 measured checkpoint command tokens to StageA_A3_checkpoint_tokens_generated_v0_4.csv
```

Thus the preserved native tlogs mechanically yield:

```text
Debug CL     25
Release CL   23
Debug LINK   16
Release LINK 18
----------------
TOTAL         82
```

---

## 7. Default linker-library evidence

The tlog evidence validator was run on the generated 82-token CSV.

Observed result:

```text
PASS: measured token evidence present (82 tokens), including default library lists.
NOTE: final candidate generator must map every measured token exactly once to pin-table coverage.
```

The measured Debug and Release default linker library token is:

```text
LIBS=kernel32.lib;user32.lib;gdi32.lib;winspool.lib;comdlg32.lib;advapi32.lib;shell32.lib;ole32.lib;oleaut32.lib;uuid.lib;odbc32.lib;odbccp32.lib
```

The extractor separately emits:

```text
/IMPLIB:<PATH>
```

rather than incorrectly absorbing `/IMPLIB:<path>.lib` into the library list.

---

## 8. Why native tlogs yield 82 tokens while the pin table has 86 checkpoint rows

The pin table contains:

```text
Debug CL     26 checkpoint rows
Release CL   24 checkpoint rows
Debug LINK   17 checkpoint rows
Release LINK 19 checkpoint rows
--------------------------------
TOTAL         86 checkpoint CL/LINK rows
```

The difference is exactly four error-reporting switches:

```text
CLD_er  /errorReport:queue
CLR_er  /errorReport:queue
LD_err   /ERRORREPORT:QUEUE
LR_err   /ERRORREPORT:QUEUE
```

These four switches are present in the preserved detailed MSBuild checkpoint logs but are omitted from the native `.command.1.tlog` payload records.

The pin table therefore retains all four settings but records their evidence provenance as:

```text
checkpoint detailed MSBuild log;
native .command.1.tlog omits error-reporting switch
```

They are not removed and the gate is not weakened.

---

## 9. Final tlog-to-pin reconciliation

The mechanical reconciliation validator was run using:

- `StageA_A3_checkpoint_tokens_generated_v0_4.csv`
- `StageA_A3_pin_table_v0_6.csv`

Observed result:

```text
PASS: 82 native-tlog tokens map exactly once to 82 pin rows.
PASS: 4 additional checkpoint pins are explicitly classified as detailed-MSBuild-log-only error-reporting evidence.
PASS: all 86 checkpoint CL/LINK pin rows are accounted for exactly once.
PASS: wrote reconciliation evidence to StageA_A3_tlog_pin_reconciliation_generated_v0_1.csv
```

This closes the hand-maintained-expected-key problem.

The final accounting is:

```text
82 native-tlog-derived measured tokens
+4 detailed-MSBuild-log-only error-reporting pins
------------------------------------------------
86 checkpoint CL/LINK pin rows
```

Every checkpoint CL/LINK row is accounted for exactly once.

---

## 10. Q1 closure status

Claude Q1 required:

1. recognition of every XML element/value;
2. correct tool/rule matching;
3. correct VS2026 toolset generation;
4. correct placement;
5. tlog-derived expected-key coverage;
6. default linker-library coverage.

Local evidence now establishes:

```text
1. PASS
2. PASS
3. PASS - v180 only
4. PASS
5. PASS
6. PASS
```

There are no `S13_PENDING` rows and no unresolved recognition rows.

---

## 11. Files that must accompany Claude's next cold review

Provide Claude with the following evidence artifacts from Dave's local run:

1. `StageA_A3_Q1_R1_R4_Local_Evidence_Closure_v0_1.md`
2. `StageA_A3_VS_rule_properties_generated_v0_3.csv`
3. `StageA_A3_checkpoint_tokens_generated_v0_4.csv`
4. `StageA_A3_tlog_pin_reconciliation_generated_v0_1.csv`
5. `StageA_A3_pin_table_v0_6.csv`
6. `scan_VS2026_rule_properties_v0_3.py`
7. `validate_StageA_A3_xml_recognition_v0_5.py` or its superseding strict equivalent
8. `extract_StageA_A3_checkpoint_tlog_tokens_v0_4.py`
9. `validate_StageA_A3_tlog_evidence_v0_4.py`
10. `validate_StageA_A3_tlog_pin_reconciliation_v0_1.py`
11. `Claude_REVIEW_OF_StageA_A3_S13_Q1_Local_Evidence_v0_1.md`
12. the current A3 requirements / migration design / execution plan / handback / migration handover files.

The three generated CSV evidence files are primary local evidence and should not be replaced by prose summaries.

---

## 12. Next process step

Do not apply an A3 project file yet.

Next:

1. generate the superseding applyable A3 candidate from the now-closed pin/evidence set;
2. package it together with the complete Q1 evidence above;
3. Claude performs a cold review;
4. Dave ratifies the exact reviewed candidate;
5. only then apply A3 and run the full A3 gate:
   - Debug + Release builds;
   - expected command-line deltas;
   - HostX64\x64 tool-host proof;
   - CFG/CET/High Entropy VA dumpbin checks;
   - Release standalone dependency gate;
   - D6 PDB filename-only Release evidence;
   - `/fp:contract` absent;
   - warning expectations;
   - S15 timing;
   - all six index regressions;
   - frozen source hashes unchanged.

---

## 13. Repository mutation

The Q1/R1/R4 evidence work described here was performed outside the production repository.

No repository project/source mutation is authorized by this evidence note alone.
