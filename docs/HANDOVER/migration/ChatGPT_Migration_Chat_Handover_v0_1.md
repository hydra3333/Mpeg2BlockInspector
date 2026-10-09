# ChatGPT Handover to a New Migration Chat
## VapourSynth-mpeg2Deblock Repository / Visual Studio Migration

**Filename:** `ChatGPT_Migration_Chat_Handover_v0_1.md`
**Version:** 0.1
**Date:** 2026-10-09
**From:** current migration ChatGPT chat
**To:** a fresh ChatGPT chat continuing migration/build-system work
**Status:** Migration-chat orientation and execution-state handover. NOT project technical authority.
**Purpose:** Risk-management handover because the current migration chat is long.
**Important:** This is distinct from the common technical-development handback `MPEG2_Deblocking_Developer_Handback_v0_3.md`.

---

## 0. First actions for the new migration chat

Before changing anything:

1. Read this whole handover.
2. Read:
   - `Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_7.md`
   - `MPEG2_Deblocking_Developer_Handback_v0_3.md`
   - `Claude_REVIEW_OF_ChatGPT_StageA_Audit_Proposal_v0_2.md`
   - `StageA_Inspector_CNR3_Audit_and_Proposed_Edits_v0_1.md`
3. Inspect the contents of:
   - `StageA_Inspector_VS2026_Audit_Proposal_v0_1.zip`
4. Treat the Claude review v0.2 as the controlling review input for the current Stage A execution boundary.
5. Do not redesign Stage 2 or the MPEG-2 deblocking algorithm in this migration chat.
6. Do not apply A3 v0.1. It has been superseded as a proposal by Claude's review requirements; A3 v0.2 must be generated only after the A1+A2 checkpoint.
7. Do not modify frozen inspector C/H source.

The immediate migration state is:

```text
A1: reviewed and accepted, NOT YET APPLIED
A2: reviewed and accepted, NOT YET APPLIED
A3 v0.1: review-only, DO NOT APPLY
A3 v0.2: NOT YET CREATED; requires A1+A2 checkpoint evidence first
```

---

## 1. Scope of this migration chat

This chat is responsible for:

- repository-migration mechanics;
- Visual Studio solution/project normalization;
- x64-only conversion;
- `.sln` to `.slnx`;
- CNR3-derived Visual Studio build-setting audit;
- reproducible VS2026 build harness;
- creation of a minimal/buildable future VapourSynth DLL placeholder project;
- migration validation;
- migration close-out documentation and handback.

This chat is NOT responsible for:

- Stage 2 experiment implementation;
- MPEG-2 deblocking algorithm design/implementation;
- scalar deblocking kernel;
- AVX2 deblocking kernel;
- index-consumption behavior;
- final filter processing/scheduling architecture.

Those return to the proper technical-development chats only after migration close-out.

Deblock4 is abandoned development history. It may be consulted only to recycle a useful proven build/script pattern if appropriate.

---

## 2. Roles and workflow

- **Dave**: owner, final authority, runs Windows builds/tests, ratifies decisions and commits.
- **Migration ChatGPT**: drafts migration mechanics, candidate files, scripts, audits and exact commands.
- **Migration Claude**: independent cold reviewer.
- Workflow:
  ```text
  ChatGPT draft/proposal
      ->
  Claude cold review
      ->
  Dave resolves/ratifies
      ->
  ChatGPT proceeds
  ```

Do not bypass the review boundary on substantive changes.

Use named Git staging only. Do not use `git add -A`.

Do not push until the agreed gate for the relevant migration stage passes.

---

## 3. Repository identity

GitHub:

```text
https://github.com/hydra3333/VapourSynth-mpeg2Deblock
```

Active local repository:

```text
E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock
```

Old rollback/reference tree:

```text
E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector
```

The old tree is not the active development/build tree.

Published post-restructure HEAD before the current VS-normalization work:

```text
a9c782acb525943881e65b2b3f8f0484521a01c5
```

Published lightweight tag:

```text
vapoursynth-mpeg2deblock-post-restructure
```

Pre-restructure lightweight tag:

```text
pre-vapoursynth-mpeg2deblock-restructure
```

---

## 4. Current repository layout

Important locations:

```text
src\Mpeg2BlockInspector\
    frozen Stage 1 C/H source

tools\Stage1_Inspector_Analyzer_v0_2.py

TESTING\
    inspector BAT/VPY regression scripts

VHSC_samples\
    tracked recordings, indexes and logs

docs\REPOSITORY\
    technical authority documents

docs\HANDOVER\
    handovers / common developer handback

vs\VapourSynth-mpeg2Deblock\
    current VS solution/project area
```

Do not create `experiments\stage2\` merely for migration. It belongs to later Stage 2 implementation.

---

## 5. Frozen source / mutable build distinction

Frozen:

```text
src\Mpeg2BlockInspector\*.c
src\Mpeg2BlockInspector\*.h
```

The inspector source must not be changed merely to satisfy a compiler-setting preference.

Not frozen:

```text
vs\VapourSynth-mpeg2Deblock\Mpeg2BlockInspector.vcxproj
vs\VapourSynth-mpeg2Deblock\Mpeg2BlockInspector.vcxproj.filters
solution/build-system files
```

Dave explicitly ruled that the command-line project configuration is in scope for correction/normalization.

---

## 6. Frozen identities

Important SHA-256 baselines:

```text
src\Mpeg2BlockInspector\getpic.c
e80239cfe73a0c04490a9bf131714861254ed1d7d095b052aac616a887ef0eca

src\Mpeg2BlockInspector\mpeg2dec.c
8e6053ccb3a40be8c0d985f2e35124bf728d1f61df9b6d0c01b71e13e13b0947

tools\Stage1_Inspector_Analyzer_v0_2.py
8e0d58305ee4fe518c25b67bdbe74acc4fb392486f23e6137862d916e5e02cda
```

Old reference EXE:

```text
3edb7147001341f669b8d49be7446d79fe2d688fcff66a16f3227f80290aa5de
```

The EXE hash is expected to change after the ratified A3 Release code-generation changes.

---

## 7. Six tracked index baselines

```text
TEST_2A_A001.idx
AFE51F251B2861D5C62E1629D95645C47B06F69D86F03B5FC531CF9FE3EA9273
size 3,820,832

TEST_2A_A001_blocky.idx
CBF6E8720E47E1F097E6310540D8CBD20862E3A427AD53C61D9A235ACDBA9288
size 3,820,832

TEST_4A_A003.idx
5B989CED016ADFE5CC4546F196DD63CB2DB9B431798A99203C830A98165B9A65
size 3,907,232

LG_576i_3_LP.idx
849b6a9c411a7db837268af3ac54501a06f5f1158e68d5245ce2b3ec40a0d011
size 2,656,928

LG_576i_4_EP.idx
11B42AADF9F46B72DEC20A8F3FDD754D07CDCE78F0460A14EDA08838336FFA87
size 1,382,432

LG_576i_5_MLS.idx
378980EA462122A02D75F412FAF9CFAF79962D503C68A8F6EE41C32B24D98D7F
size 1,357,472
```

The forthcoming checkpoint and final Stage A gate require all six indexes, not the earlier reduced two-test migration gate.

---

## 8. Current Visual Studio direction

Final Stage A end-state:

```text
VapourSynth-mpeg2Deblock.slnx

    Mpeg2BlockInspector
        Application / EXE
        C
        Debug x64
        Release x64
```

Win32/x86 is to be removed from both the inspector project and solution.

Keep:

```xml
<Keyword>Win32Proj</Keyword>
```

because that is the native C/C++ project keyword, not the target architecture.

Keep the inspector ProjectGuid.

Later Stage B will add the future DLL placeholder project to the same `.slnx`.

---

## 9. Ratified build-setting policy

Important Dave rulings:

### 9.1 No reliance on mutable Microsoft defaults

Dave ruled:

```text
we should not rely on default behaviours for settings since microsoft are well known for fiddling with things in their releases
```

Therefore every output-affecting compiler/linker/manifest/ABI setting must be explicitly represented in the project file at its currently effective value unless the setting is a deliberate reviewed change.

The effective pre-A3 values must come from the A1+A2 checkpoint build log, not from memory of Visual Studio defaults.

### 9.2 Windows SDK

Ratified:

```text
DO NOT PIN A SPECIFIC WINDOWS SDK VERSION
```

This is the deliberate exception to the no-default policy.

Each controlled build/gate must record the actual SDK selected.

Installed SDK include versions observed:

```text
10.0.22621.0
10.0.26100.0
10.0.28000.0
```

### 9.3 Platform toolset

Keep explicitly:

```text
v145
```

### 9.4 Inspector AVX2

Ratified:

```text
AVX2 OFF
```

A3 v0.2 must pin the effective non-AVX2 value explicitly rather than merely omit the setting.

### 9.5 SDL / CRT

Keep:

```text
SDLCheck = false
_CRT_SECURE_NO_WARNINGS
```

### 9.6 CNR3 transfer method

Use the dual-pass / subtractive audit:

- presume explicit CNR3 settings may be useful;
- every relevant CNR3 explicit setting gets a disposition;
- independently inspect target requirements;
- reconcile differences;
- no CNR3 setting disappears silently.

---

## 10. Mandatory CNR3 inventory

A mechanical XML inventory was produced for:

```text
Mpeg2BlockInspector.vcxproj
cnr3_cache_core_selftest.vcxproj
cnr3.vcxproj
```

Counts:

```text
Inspector:        120 XML element records
CNR3 self-test:  107 XML element records
CNR3 DLL:        116 XML element records
TOTAL:           343
```

CNR3 settings requiring explicit reconciliation:

```text
56 self-test setting rows
57 DLL setting rows
113 total CNR3 setting rows
```

A3 v0.2 MUST:

- provide `disposition` and `reason` for all 113 CNR3 rows;
- use only the classification vocabulary from Design Record v0.7 section 9;
- include a script check that fails if any disposition/reason required by the schema is blank.

Do not substitute another hand-written summary table for this mechanical accounting.

---

## 11. Current Stage A review package

Primary package:

```text
StageA_Inspector_VS2026_Audit_Proposal_v0_1.zip
```

Primary audit:

```text
StageA_Inspector_CNR3_Audit_and_Proposed_Edits_v0_1.md
```

Claude review:

```text
Claude_REVIEW_OF_ChatGPT_StageA_Audit_Proposal_v0_2.md
```

The review verdict is:

```text
A1 accepted
A2 accepted
A3 v0.1 not acceptable yet
A3 v0.2 must be generated after the A1+A2 checkpoint
```

---

## 12. A1 candidate - ACCEPTED, NOT YET APPLIED

Candidate filename:

```text
Mpeg2BlockInspector_A1_x64only_DELETIONS_ONLY.vcxproj
```

SHA-256:

```text
87acd9ad1c94e5545f84fe57857c076781ca499523d2a80545919ae571dc7a57
```

Current pre-A1 inspector project SHA-256:

```text
e383cbce4eaae1ab5953aa6334d433ea1af4d977c8eae9a2db8699c6c658375f
```

Claude independently verified A1:

- 58 lines deleted;
- zero insertions;
- no retained line rewritten;
- no Win32 configuration remains;
- `<Keyword>Win32Proj</Keyword>` remains;
- ProjectGuid remains;
- CRLF/no-BOM form preserved.

### Application rule

Do NOT apply the LF review `.diff`.

Copy the accepted candidate file byte-for-byte over:

```text
vs\VapourSynth-mpeg2Deblock\Mpeg2BlockInspector.vcxproj
```

Then verify the SHA-256 is exactly:

```text
87acd9ad1c94e5545f84fe57857c076781ca499523d2a80545919ae571dc7a57
```

Then inspect Git diff/numstat and make the A1 commit with named staging.

---

## 13. A2 candidate - ACCEPTED, NOT YET APPLIED

Candidate filename:

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

Claude verified:

- same structural style as CNR3 `.slnx`;
- lower-case project ID is the inspector's retained ProjectGuid;
- no separate SolutionGuid is needed;
- solution folder remains unchanged, so `$(SolutionDir)` remains unchanged.

### Before A2 commit

Run:

```text
git grep -n "Mpeg2BlockInspector.sln"
```

across the repository.

Confirm `.gitignore` does not accidentally ignore `*.slnx`.

### Application rule

Do NOT open the old `.sln` in Visual Studio after A1.

Perform A1 and A2 command-line commits back-to-back.

For A2:

- remove the tracked old:
  ```text
  vs\VapourSynth-mpeg2Deblock\Mpeg2BlockInspector.sln
  ```
- copy the accepted `.slnx` candidate to:
  ```text
  vs\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock.slnx
  ```
- verify its SHA-256 is exactly:
  ```text
  fa24efcd73401a38604e2f4228b07d8b960abcbfb66da22c02908e9d1cdb0754
  ```
- named staging only;
- commit A2.

The first Visual Studio open after these changes must be the new `.slnx`.

---

## 14. Critical checkpoint AFTER A1+A2 and BEFORE A3

This checkpoint is now mandatory.

A1/A2 should not change x64 build behavior, so this checkpoint establishes the exact pre-A3 effective build state.

### 14.1 Build

Rebuild both:

```text
Debug | x64
Release | x64
```

Use MSBuild found through `vswhere`.

Use a detailed MSBuild log:

```text
-v:detailed
```

or an equivalent binary log where the exact effective compiler/linker invocations can be extracted.

### 14.2 Record exact effective commands

For both Debug and Release capture:

```text
cl.exe effective command line
link.exe effective command line
```

The log, not remembered defaults, is the authority for A3 pinning.

### 14.3 Record warnings

Record warnings by:

```text
warning code
file
line
```

Do not rely only on warning count.

Known prior Release warning set is 17 warning instances, but the checkpoint must record the actual current detailed list.

Be aware that `/GL`/`/LTCG` later may move some diagnostics to the link/code-generation stage; attribution changes must be examined rather than assumed to be new defects.

### 14.4 Record build identities

Record:

```text
actual Visual Studio installation used
MSBuild path/version
v145 toolset evidence
actual Windows SDK used
cl.exe path/version if available
link.exe path/version if available
Debug EXE identity
Release EXE SHA-256
```

### 14.5 Run all six index regressions

Regenerate all six tracked indexes and require byte identity to their baselines in section 7.

### 14.6 Git/Visual Studio state

After opening/building the new `.slnx`, run:

```text
git status --short
git status --short --ignored
```

Explain any unexpected tracked rewrite.

---

## 15. A3 v0.1 - DO NOT APPLY

Existing review candidate:

```text
Mpeg2BlockInspector_A3_PROPOSED_SETTINGS_v0_1.vcxproj
```

SHA-256:

```text
a86ec5b561abd278bd8dd305f0305c6d54bf0e6736f6c592075899683f2e8921
```

This file is review history only.

Do not apply it.

Claude found two blocking issues:

1. incomplete 113-row CNR3 reconciliation;
2. it still relied on several Visual Studio/MSBuild defaults, contrary to Dave's later ruling.

---

## 16. A3 v0.2 - requirements

A3 v0.2 must be generated from the accepted A1 project after the A1+A2 checkpoint evidence exists.

### 16.1 Explicit pinning

For each output-affecting setting:

- derive the effective current value from the checkpoint compiler/linker/build evidence;
- write that value explicitly into the project;
- unless it is one of the deliberate ratified A3 changes.

Candidate areas include, but are not limited to:

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
EnableUAC
UACExecutionLevel
RandomizedBaseAddress
DataExecutionPrevention
TargetMachine
LinkIncremental
FloatingPointModel
FunctionLevelLinking
WholeProgramOptimization
LinkTimeCodeGeneration
warning level
SDL
PCH policy
preprocessor definitions
```

The checkpoint log decides the complete list.

### 16.2 Full CNR3 reconciliation

All:

```text
56 CNR3 self-test rows
57 CNR3 DLL rows
113 total
```

must have:

```text
disposition
reason
```

using only the Design Record v0.7 section 9 classification labels.

A validation script must fail on incomplete accounting.

### 16.3 Ratified D1 / D2 / D3 decisions

Dave ratified Claude review v0.2 section 7:

#### D1 = (a)

Adopt Release code-generation settings explicitly:

```text
/O2
/Ot
/Ob2
/Oi
/Gy
/GL
/LTCG
```

subject to the strict six-index gate.

#### D2 = (a)

Keep no Windows SDK pin.

Record the actual SDK used in every gate.

#### D3 = (a)

Debug x64 gets the CNR3 explicit values:

```text
FavorSizeOrSpeed = Speed
InlineFunctionExpansion = AnySuitable
IntrinsicFunctions = true
```

### 16.4 Explicit AVX2-off state

Do not merely omit AVX2.

A3 v0.2 must pin the effective non-AVX2 instruction-set state explicitly, based on the checkpoint/effective MSBuild semantics.

### 16.5 Command-line delta proof

After generating/applying A3 v0.2 for test:

- rebuild detailed logs;
- compare pre-A3 checkpoint `cl.exe` / `link.exe` command lines to A3;
- the delta must contain exactly:
  - explicit pins that preserve the checkpoint's effective behavior; and
  - the deliberate D1/D3 changes;
- no unexplained command-line change is acceptable.

### 16.6 A3 commit strategy

Claude recommendation:

- keep A3 as one reviewed settings commit;
- split into A3a explicit pins and A3b code-generation changes only if the combined A3 fails the gate and attribution requires separation.

---

## 17. Stage A final gate after A3

Required:

1. Debug x64 rebuild.
2. Release x64 rebuild.
3. Detailed warning comparison by code/file/line.
4. Frozen source hashes unchanged.
5. All six indexes byte-identical.
6. LP exact SHA:
   ```text
   849b6a9c411a7db837268af3ac54501a06f5f1158e68d5245ce2b3ec40a0d011
   ```
7. Record new Release EXE SHA-256 as the post-A3 baseline.
8. `git status --short`.
9. `git status --short --ignored`.
10. No unexplained VS rewrite.
11. Record accepted Stage A project and `.filters` SHA-256 for the later Stage B protection trigger.

Do not weaken this gate to accommodate a setting change.

---

## 18. CNR3 settings/reference facts

Primary Stage A reference:

```text
cnr3_cache_core_selftest.vcxproj
```

Secondary:

```text
cnr3.vcxproj
```

Solution reference:

```text
cnr3.slnx
```

The supplied CNR3 project files match current CNR3 main copies apart from line endings.

Known inspector-specific differences that remain intentional:

```text
SDL off
_CRT_SECURE_NO_WARNINGS retained
AVX2 off
no C++20/conformance setting for C project
no VapourSynth include/dependencies
no CNR3-specific preprocessor symbols
no SDK pin
COMDAT remains true
OPT:REF remains true
```

Claude verified source contains no `_DEBUG`, `NDEBUG` or `_CONSOLE` tests; only `_WIN32` appears among those relevant symbols.

---

## 19. Visual Studio / build-harness direction

Final harness policy:

- discover Visual Studio with `vswhere`;
- discover MSBuild with `vswhere`;
- use consistent `-products *` and component criteria so both resolve to the same installation;
- support Build Tools as well as full VS editions;
- do not hard-code `18\Community`;
- invoke `VsDevCmd.bat` from the discovered installation only when direct Microsoft command-line tools such as `dumpbin` require that environment;
- restore project directory after `VsDevCmd`;
- verify `dumpbin`;
- build umbrella `.slnx` for Debug/Release x64;
- fail immediately on non-zero return;
- log selected tool paths/versions and SDK.

The exact final harness is a later migration deliverable. Do not create it before Stage A settings/solution state is accepted.

---

## 20. Stage B preview - do not start yet

After Stage A passes:

- add a buildable future VapourSynth DLL placeholder project to the same `.slnx`;
- use the CNR3 DLL project as the primary subtractive template;
- same no-defaults ruling applies to Stage B;
- explicitly pin output-affecting settings rather than relying on CNR3 XML defaults;
- placeholder preference is entry-point only:
  - include `VapourSynth4.h`;
  - export `VapourSynthPluginInit2`;
  - call `configPlugin`;
  - register no filter functions;
- no deblocking algorithm.

After Stage A acceptance, record hashes of:

```text
Mpeg2BlockInspector.vcxproj
Mpeg2BlockInspector.vcxproj.filters
```

After Stage B:

- if both are byte-identical, only one LP smoke run is required;
- if either changed, repeat all six inspector regressions.

---

## 21. Common developer handback architecture

There is one shared technical-development handback:

```text
MPEG2_Deblocking_Developer_Handback_v0_3.md
```

It is currently provisional.

At migration close-out:

- update it with actual final evidence;
- migration Claude cold-reviews it against the repository;
- Dave ratifies it;
- store under `docs\HANDOVER\`;
- both technical-development chats consume the same handback.

Role-specific ChatGPT/Claude technical handovers should point to the common handback rather than duplicate migration facts.

This migration-chat handover is separate and exists only to safely continue migration work if this chat ends.

---

## 22. Current migration documentation

Current baseline documents:

```text
Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_7.md
MPEG2_Deblocking_Developer_Handback_v0_3.md
StageA_Inspector_CNR3_Audit_and_Proposed_Edits_v0_1.md
Claude_REVIEW_OF_ChatGPT_StageA_Audit_Proposal_v0_2.md
ChatGPT_Migration_Chat_Handover_v0_1.md
```

Review/evidence package:

```text
StageA_Inspector_VS2026_Audit_Proposal_v0_1.zip
```

The final migration docs will receive further versions after Stage A and Stage B.

---

## 23. Exact next action

Do NOT regenerate A3 yet.

The next execution boundary is:

```text
Dave explicitly authorizes A1+A2 execution
    ->
apply accepted A1 by byte copy + verify SHA
    ->
commit A1
    ->
without opening old .sln, perform A2 repository-reference checks
    ->
replace old .sln with accepted .slnx + verify SHA
    ->
commit A2
    ->
first VS open is new .slnx
    ->
run mandatory pre-A3 checkpoint
    ->
produce checkpoint evidence
    ->
draft A3 v0.2
    ->
Claude reviews A3 v0.2
    ->
Dave ratifies
    ->
apply A3 and run full Stage A gate
```

If inheriting this handover in a new chat, do not ask Dave to repeat decisions already recorded here. Ask only for the actual current repository outputs needed at the next execution step.

---

## 24. Important cautions

- No `git add -A`.
- No force push/reset history rewriting.
- No source edits.
- Do not apply review `.diff` files; A1/A2 are applied by byte-copying accepted candidate files and verifying SHA-256.
- Do not open old `.sln` between A1 and A2.
- Do not treat A3 v0.1 as accepted.
- Do not infer current effective compiler settings from documented defaults; capture them from the checkpoint.
- No Windows SDK pin.
- Do not resurrect Deblock4 as a project.
- Do not advance Stage 2 from this migration chat.
- Partial/representative regressions are no longer sufficient for Stage A; all six index baselines are required.

---

## 25. Change log

### v0.1 - 2026-10-09

- First migration-chat risk-management handover.
- Captures repository state after Claude Stage A review v0.2.
- Records A1/A2 accepted-but-not-applied boundary.
- Records exact candidate SHA-256 values.
- Records mandatory A1+A2 pre-A3 checkpoint.
- Records Dave's no-defaults ruling and ratified D1/D2/D3 decisions.
- Records all-six-index gate and A3 v0.2 requirements.
