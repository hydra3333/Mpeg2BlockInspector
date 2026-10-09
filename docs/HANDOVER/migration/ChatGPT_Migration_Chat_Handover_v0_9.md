# ChatGPT Handover to a Future Migration Chat
## VapourSynth-mpeg2Deblock Repository / Visual Studio / Release Migration

**Filename:** `ChatGPT_Migration_Chat_Handover_v0_9.md`
**Version:** 0.9
**Date:** 2026-10-10
**From:** current migration ChatGPT chat
**To:** a fresh ChatGPT chat continuing migration/build-system work
**Status:** MIGRATION-ONLY continuity handover; not MPEG-2 technical authority
**Supersedes:** `ChatGPT_Migration_Chat_Handover_v0_8.md`

---


# 0A. CURRENT STATE - A3 v0.9 RATIFIED, NOT YET GATED

Latest Claude review:

```text
Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_9_Candidate_v0_1.md
```

Claude verdict:

```text
Ratifiable.
U1 and U2 fixed.
No new MUST or SHOULD.
```

Exact candidate:

```text
Mpeg2BlockInspector_A3_APPLYABLE_CANDIDATE_v0_9.vcxproj
SHA-256 ebfcde82405fd2dc25aa7a14a160f89375465d545927b3e4583e7a40fd1af668
```

Dave ratified this exact SHA on 2026-10-10.

READY package:

```text
StageA_A3_v0_9_READY_FOR_CLAUDE.zip
SHA-256 4feea4ecbdc82448ab8480a3c28350b917bb5a8101aa87ff1cde5b89e130a921
```

Current published Git baseline before A3 application:

```text
34e8a46 Add vapoursynth include files ready for use with DLL building
```

The vendored VapourSynth include files are already pushed. The five `.h` files currently show `i/lf w/lf attr/`; do not interrupt A3 to change that policy.

**Immediate next action:** apply the exact ratified candidate byte-for-byte to:

```text
vs\VapourSynth-mpeg2Deblock\Mpeg2BlockInspector.vcxproj
```

verify the production project hashes to `ebfcde82405fd2dc25aa7a14a160f89375465d545927b3e4583e7a40fd1af668`, then execute the full A3 gate. Do not redesign the candidate unless that gate fails and the agreed diagnostic sequence produces evidence requiring a reviewed change.

Claude also noted the current Claude migration continuity document is:

```text
Claude_HANDOVER_TO_Future_Claude_Migration_Chat_v0_3.md
```

Use v0.3, not the v0.2 copy carried in the older package.



# 0. READ THIS FIRST - HARD-EARNED KNOWLEDGE BEFORE EXECUTION

The first document a future migration chat should read after this handover is:

```text
StageA_VS2026_MSBuild_Hard_Earned_Knowledge_v0_2.md
```

That document exists because the Stage A A3 normalization process consumed substantial effort proving how Visual Studio 2026 / MSBuild v180 actually recognizes, persists and emits settings.

Do **not** repeat that research casually.

Its key durable lessons include:

- installed v180 rule XML is the property-recognition authority;
- property placement/DataSource is part of the setting, not incidental XML layout;
- `Label="Configuration"` properties must be in the correct pre-`Microsoft.Cpp.props` group;
- compiler and linker error-reporting properties are different;
- `/Zc:inline` is not `/Ob2`;
- there is no recognized v180 `HighEntropyVA` property used here;
- native `.command.1.tlog` files do not necessarily contain `cl.exe`/`link.exe`;
- native tlogs omitted four error-reporting switches that were present in detailed MSBuild logs;
- `/IMPLIB:<path>.lib` must not be mistaken for a bare default library;
- explicit pinning can cause formerly implicit switches to appear without changing semantics;
- **single-owner rule:** do not add a second project property just because a downstream command-line switch is measured if an existing higher-level setting already generates that switch;
- `Manifest/EnableSegmentHeap=true` is the single owner of the segment-heap input for this project; gate the resulting one `/manifestinput:` rather than adding `Link/ManifestInput`.

That knowledge document should be treated as durable migration knowledge and retained in the repository when Dave approves the next documentation commit.

---

# 1. Document taxonomy - keep roles separate

There are four distinct documentation roles.

```text
A. ChatGPT_Migration_Chat_Handover_v0_*.md
   migration ChatGPT -> future migration ChatGPT

B. Claude_HANDOVER_TO_Future_Claude_Migration_Chat_v0_*.md
   migration Claude -> future migration Claude

C. MPEG2_Deblocking_Developer_Handback_v0_*.md
   migration -> BOTH technical-development chats

D. developer-chat continuity handovers
   ChatGPT_Handover_To_Future_ChatGPT_MPEG2_Deblocking_Project_v0_*.md
   Claude_HANDOVER_TO_Future_Claude_Chat_v0_*.md
```

Migration must not rewrite the development-chat handovers unless Dave explicitly asks.

The accidental ChatGPT development handover v0.4 is archival history only.

---

# 2. FIRST READING ORDER FOR A FUTURE MIGRATION CHAT

Read these before changing anything:

1. `ChatGPT_Migration_Chat_Handover_v0_9.md`
2. `StageA_VS2026_MSBuild_Hard_Earned_Knowledge_v0_2.md`
3. `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_8_Candidate_v0_1.md`
4. `Claude_REVIEW_OF_ChatGPT_StageA_A3_Q1_R1_R4_Local_Evidence_Closure_v0_1.md`
5. `Claude_REVIEW_OF_StageA_A3_S13_Q1_Local_Evidence_v0_1.md`
6. `Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_16.md`
7. `StageA_Visual_Studio_Normalization_Execution_Plan_v0_11.md`
8. `MPEG2_Deblocking_Developer_Handback_v0_10.md`
9. `StageA_A3_Q1_R1_R4_Local_Evidence_Closure_v0_1.md`
10. final current A3 pin table / rule CSV / token CSV / reconciliation CSV / validators.

Also retain and consult all earlier Claude migration reviews listed in v0.7 when a historical decision is questioned.

Do not substitute this handover for live Git/filesystem inspection.

---

# 3. USER / WORKFLOW / BOUNDARIES

Dave is final authority.

Workflow:

```text
ChatGPT drafts/mechanics
    -> Claude cold review
    -> Dave resolves/ratifies
    -> ChatGPT proceeds
```

Rules:

- no guessing;
- one bounded action/check at a time where practical;
- no `git add -A`;
- named staging only;
- ordinary interactive CMD one-line commands;
- no literal `<placeholder>` commands;
- keep old rollback tree until no longer needed;
- do not modify frozen inspector C/H source for build normalization;
- migration chat does not redesign Stage 2 deblocking;
- do not apply an unreviewed A3 candidate.

Current user intent after the next accepted documentation/candidate state:

```text
update the hard-earned knowledge/control documents
-> inspect
-> named stage
-> commit
-> push
```

Dave explicitly wants the long Q1/R1/R4/U1 process preserved before the chat fails.

---

# 4. REPOSITORY / PROJECT IDENTITY

GitHub:

```text
https://github.com/hydra3333/VapourSynth-mpeg2Deblock
```

Production tree:

```text
E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock
```

Old rollback/reference tree:

```text
E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector
```

CLI remains:

```text
Mpeg2BlockInspector
```

Exact path case:

```text
VapourSynth-mpeg2Deblock
```

Tags:

```text
pre-vapoursynth-mpeg2deblock-restructure
vapoursynth-mpeg2deblock-post-restructure
pre-stageA-vs-normalization
```

`pre-stageA-vs-normalization`:

```text
b38fde11d64935db933707704b45581d5dddcde7
```

Known Stage A commits:

```text
A1 d38d56d697107e7409f4baa7753bfb31b8d94747
A2 837df123ebfe0fa083fec9d6de8969bd180f9ac0
```

Later migration/document checkpoint commits known from this chat:

```text
b4dace033e2d6f6d0c4b505875aeae6879077324
ab145f56fd22cf4812d1e5b3e9fbbffc1f974095
```

Always run live `git status`, `git log`, and `git rev-parse` before staging.

---

# 5. FROZEN / AUTHORITATIVE TECHNICAL INPUTS

This migration does not redesign MPEG-2 semantics.

Controlling development docs:

```text
docs/REPOSITORY/02_INDEX_FORMAT_SPEC.md
docs/REPOSITORY/05_DECISIONS.md
docs/REPOSITORY/06_DEBLOCK_CONCEPT.md
Stage 1 report
Stage 2 experiment design v0.3
Proposal v0.5
```

K-07 remains:

```text
FRAME/FIELD/NONE describes applicable coded residual transform geometry.
NONE applies to skipped macroblocks and non-intra macroblocks with effective CBP=0.
Absence of a dct_type bit does not itself imply NONE.
```

Do not edit these because of Visual Studio migration work.

Frozen hashes:

```text
src\Mpeg2BlockInspector\getpic.c
e80239cfe73a0c04490a9bf131714861254ed1d7d095b052aac616a887ef0eca

src\Mpeg2BlockInspector\mpeg2dec.c
8e6053ccb3a40be8c0d985f2e35124bf728d1f61df9b6d0c01b71e13e13b0947

tools\Stage1_Inspector_Analyzer_v0_2.py
8e0d58305ee4fe518c25b67bdbe74acc4fb392486f23e6137862d916e5e02cda
```

Historic EXE:

```text
3edb7147001341f669b8d49be7446d79fe2d688fcff66a16f3227f80290aa5de
```

LP baseline:

```text
VHSC_samples\LG_576i_3_LP.idx
849b6a9c411a7db837268af3ac54501a06f5f1158e68d5245ce2b3ec40a0d011
size 2,656,928
```

---

# 6. STAGE A COMPLETED BASELINE

Repository restructure complete.

A1:
- Win32 removed;
- project SHA after A1:

```text
87acd9ad1c94e5545f84fe57857c076781ca499523d2a80545919ae571dc7a57
```

A2:
- `.sln` replaced by x64 `.slnx`;
- `.slnx` SHA:

```text
fa24efcd73401a38604e2f4228b07d8b960abcbfb66da22c02908e9d1cdb0754
```

VS2026 load PASS.

Pre-A3 environment:

```text
VS: C:\Program Files\Microsoft Visual Studio\18\Community
MSBuild: 18.10.1.42706
toolset: v145
VC tools: 14.51.36231
Windows SDK: 10.0.28000.0 observed, deliberately unpinned
checkpoint PreferredToolArchitecture: x86
checkpoint CL/LINK host: HostX86\x64
target: x64
```

Pre-A3 build:

```text
Debug RC0, 20 warnings
Debug EXE SHA:
66be0a77e21b34c9a92330c1752604b3be98d91deb6f133d37a1578361ea8bb9

Release RC0, 17 warnings
Release EXE SHA:
d31fbad88f7cade245234c3fb81832e17ec9d2024e6c638ed8a033e3cc5bc6f8
```

Pre-A3 six-index regression PASS.

Six required hashes:

```text
TEST_2A_A001          AFE51F...9273
TEST_2A_A001_blocky   CBF6E8...9288
TEST_4A_A003          5B989C...9A65
LG_576i_3_LP          849b6a...D011
LG_576i_4_EP          11B42A...FA87
LG_576i_5_MLS         378980...8D98D7F
```

The exact full values exist in earlier migration evidence; do not infer missing hex from this abbreviated handover line.

---

# 7. RATIFIED BUILD / PRODUCT POLICY

x64 only.

Both inspector and future plugin:

```text
/arch:AVX2 minimum
/GS ON
CFG ON
CET ON
ASLR / Dynamic Base ON
High Entropy VA ON
DEP / NX ON
/favor:blend explicit
Spectre mitigation explicitly Disabled
/Qspectre absent
```

Inspector:

```text
/sdl OFF documented exception
/fp:precise
/fp:contract absent
Debug /MDd
Release /MT
```

Future plugin:

```text
/sdl ON
Release /MT
```

Release inspector:

```text
/O2
/GL
/LTCG
/PDBALTPATH:%_PDB%
```

Release must not require separately installed VC/UCRT redistributable DLLs.

Forbidden Release imports:

```text
VCRUNTIME*
MSVCP*
api-ms-win-crt-*
ucrtbase*
CONCRT*
VCOMP*
MSVCR1*
```

Expected current allowed dependency:

```text
KERNEL32.dll
```

SDK deliberately unpinned but recorded/gated.

Toolset v145.

PreferredToolArchitecture target policy: x64 host tools.

Project files are authoritative for build policy. Harness/CI may invoke, not repair/override.

---

# 8. Q1 / R1 / R4 HARD-EARNED EVIDENCE - CLOSED

Claude's closure verdict:

```text
Q1, R1 and R4 closed by the evidence.
```

Strict rule scan:

```text
1512 recognized definitions
v160=16
v170=743
v180=753
```

Strict XML recognition eventually passed with zero tolerated pending rows.

Native preserved tlogs:

```text
%TEMP%\mpeg2deblock_stageA_checkpoint\evidence\Debug_CL.command.1.tlog
%TEMP%\mpeg2deblock_stageA_checkpoint\evidence\Release_CL.command.1.tlog
%TEMP%\mpeg2deblock_stageA_checkpoint\evidence\Debug_link.command.1.tlog
%TEMP%\mpeg2deblock_stageA_checkpoint\evidence\Release_link.command.1.tlog
```

Measured token counts:

```text
Debug CL     25
Release CL   23
Debug LINK   16
Release LINK 18
TOTAL        82
```

Final accounting:

```text
82 native-tlog tokens
+4 detailed-MSBuild-log-only error-reporting pins
=86 checkpoint CL/LINK rows
```

Final reconciliation PASS:

```text
82 native-tlog tokens map exactly once to 82 pin rows.
4 additional checkpoint pins explicitly classified detailed-MSBuild-log-only.
All 86 checkpoint CL/LINK rows accounted for exactly once.
```

Important property findings:

```text
Link/LinkErrorReporting=QueueForNextLogin

Configuration/LinkIncremental=false
Configuration/GenerateManifest=true
Configuration/LinkControlFlowGuard=true

ClCompile/RemoveUnreferencedCodeData=true      -> /Zc:inline
ClCompile/ProgramDataBaseFileName=$(IntDir)vc$(PlatformToolsetVersion).pdb

Link/GenerateDebugInformation=DebugFull

no recognized HighEntropyVA property
-> Link/AdditionalOptions /HIGHENTROPYVA %(AdditionalOptions)
```

Native tlog parser lessons are in the hard-earned knowledge doc.

---

# 9. CLAUDE v0.8 CANDIDATE REVIEW - CURRENT AUTHORITY

Latest review:

```text
Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_8_Candidate_v0_1.md
```

Claude verdict:

```text
Not yet ratifiable, but close.
```

Everything requested in the v0.8 package was present and Claude independently verified:

- package hashes;
- local evidence identity;
- CRLF / ASCII;
- all local validators;
- candidate property recognition against v180;
- T1 import position;
- T2 dual WholeProgramOptimization pins;
- frozen ItemGroup membership;
- only intended A1 value changes/additions.

One MUST:

```text
U1 - segment-heap manifest had two owners.
```

v0.8 incorrectly retained:

```text
Manifest/EnableSegmentHeap=true
```

and added:

```text
Link/ManifestInput=$(VCToolsInstallDir)Include\Manifest\segmentheap.manifest
```

Claude established the existing `EnableSegmentHeap=true` already caused the measured checkpoint `/manifestinput:`.

Required correction:

```text
keep Manifest/EnableSegmentHeap=true
remove both Link/ManifestInput elements
re-point LD_maninput / LR_maninput pins to Manifest/EnableSegmentHeap=true
post-A3 tlog must show exactly one /manifestinput: resolving to segmentheap.manifest
```

One SHOULD:

```text
U2 - predicted delta must include switches made explicit by pins:
Debug CL: /Gy- /GF-
Debug LINK: /OPT:NOREF /OPT:NOICF /LARGEADDRESSAWARE /TSAWARE
Release LINK: /LARGEADDRESSAWARE /TSAWARE
```

Also document expected non-emission for explicitly pinned default enum values such as:

```text
Debug LinkTimeCodeGeneration=Default
Release BasicRuntimeChecks=Default
```

---

# 10. CURRENT A3 v0.9 STATE - VERY IMPORTANT

A v0.9 candidate has been prepared locally in the working artifact tree.

Candidate:

```text
Mpeg2BlockInspector_A3_APPLYABLE_CANDIDATE_v0_9.vcxproj
```

SHA-256:

```text
ebfcde82405fd2dc25aa7a14a160f89375465d545927b3e4583e7a40fd1af668
```

The v0.8 -> v0.9 project diff is intentionally only:

```text
remove Debug Link/ManifestInput
remove Release Link/ManifestInput
```

No other project-file change.

The v0.9 pin table:

```text
StageA_A3_pin_table_v0_8.csv
```

re-points:

```text
LD_maninput
LR_maninput
```

to:

```text
Manifest/EnableSegmentHeap=true
```

with single-owner notes.

The v0.9 predicted delta includes Claude U2:

```text
Debug CL: /Gy- /GF-
Debug LINK: /OPT:NOREF /OPT:NOICF /LARGEADDRESSAWARE /TSAWARE
Release LINK: /LARGEADDRESSAWARE /TSAWARE
```

and expected default-enum non-emission notes.

Offline current PASS outputs:

```text
PASS: candidate structure, T1 import position, T2 dual WPO pins,
      frozen membership and 138 pin applications verified.

PASS: 141 structural pin rows; no duplicate keys/blanks;
      no pending coverage kinds.

PASS: 113 CNR3 rows; 56 self-test + 57 DLL;
      source-reference reconciliation complete.
```

IMPORTANT CURRENT INTERRUPTION STATE:

The current chat became slow while packaging v0.9.

The candidate, diffs, pin table, predicted delta, knowledge doc, updated control docs and validators exist in the working artifact directory, but the final v0.9 READY package has **not yet been proven complete on Dave's machine** and Claude has **not reviewed v0.9**.

Do not treat v0.9 as ratified or applied.

The safest next action in a fresh chat is:

1. inspect the v0.9 working package;
2. finish/regenerate the base ZIP cleanly;
3. Dave extracts it beside the existing A3 evidence directories;
4. run `ASSEMBLE_AND_VALIDATE_A3_v0_9_FOR_CLAUDE.bat`;
5. obtain all LOCAL PASS outputs and `StageA_A3_v0_9_READY_FOR_CLAUDE.zip`;
6. send that exact READY ZIP to Claude;
7. Claude performs the requested short v0.9-vs-v0.8 check;
8. Dave ratifies the exact v0.9 SHA only after Claude accepts it.

Do not apply before that.

---

# 11. HARD-EARNED KNOWLEDGE DOCUMENT - CURRENT DRAFT

Current durable knowledge draft:

```text
StageA_VS2026_MSBuild_Hard_Earned_Knowledge_v0_2.md
```

It should be retained and updated after Claude's v0.9 response if needed.

It covers:

- recognition authority;
- placement;
- Configuration group import ordering;
- Link error reporting;
- `/Zc:inline`;
- HighEntropyVA;
- Full PDB;
- single-owner rule / segment heap;
- native tlog format;
- 82+4=86 evidence;
- `/IMPLIB` parsing trap;
- default-library deliberate exception;
- newly explicit switch prediction;
- evidence hierarchy;
- provenance retention.

This is the principal answer to Dave's requirement not to lose the long, hard-earned process.

---

# 12. CONTROL DOCUMENT UPDATES PREPARED / INTENDED

The following current versions are intended for the next controlled documentation checkpoint:

```text
StageA_VS2026_MSBuild_Hard_Earned_Knowledge_v0_2.md
Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_16.md
StageA_Visual_Studio_Normalization_Execution_Plan_v0_11.md
MPEG2_Deblocking_Developer_Handback_v0_10.md
ChatGPT_Migration_Chat_Handover_v0_9.md
```

Also retain the exact Claude reviews:

```text
Claude_REVIEW_OF_StageA_A3_Q1_R1_R4_Local_Evidence_Closure_v0_1.md
Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_8_Candidate_v0_1.md
```

Do not update:

```text
02_INDEX_FORMAT_SPEC.md
05_DECISIONS.md
06_DEBLOCK_CONCEPT.md
developer-chat internal handovers
```

because no MPEG-2/deblocking semantic decision changed.

---

# 13. COMMIT / PUSH INTENT

Dave wants to commit and push after the knowledge/control-document update is agreed.

Do not commit blindly.

Before staging:

```text
git status --short
git diff --check
```

Use named `git add` only.

Before commit inspect:

```text
git diff --cached --check
git diff --cached --name-status
git status --short
```

The intended checkpoint should preserve:

- latest accepted/reviewed migration knowledge/control docs;
- final relevant Claude reviews;
- final evidence/validators intended to be durable;
- accepted candidate only if Dave decides it belongs in that checkpoint.

Because v0.9 is not yet Claude-accepted, a future chat must distinguish:

```text
documentation/evidence checkpoint
```

from:

```text
application of A3 project candidate
```

Do not accidentally commit an unratified project change into the production project path.

---

# 14. A3 POST-APPLICATION GATE - STILL FUTURE

After Claude accepts v0.9 and Dave ratifies it:

1. byte-copy/apply exact candidate to the production project path;
2. Debug + Release clean builds;
3. prove HostX64\x64 CL/LINK;
4. inspect post-A3 tlogs against predicted deltas;
5. require exactly one segment-heap `/manifestinput:`;
6. require `/Qspectre` absent;
7. require `/fp:contract` absent;
8. Release `/MT`, `/GL`, `/LTCG`;
9. CFG/CET/High Entropy/ASLR/NX/security-cookie dumpbin gates;
10. Release PDB CodeView path filename-only under D6;
11. standalone Release imports: expected KERNEL32 only, forbidden patterns absent;
12. warning comparison;
13. S15 timing / Release EXE evidence;
14. frozen source hashes unchanged;
15. run all six tracked index regressions;
16. all six exact byte-identical;
17. only after full PASS close Stage A / commit/tag as agreed.

Diagnosis sequence if index regression changes:

```text
1. ISA / AVX2 first
2. old ISA behavior
3. Release /MD vs /MT
4. remove GL/LTCG
5. Host x86 vs x64
```

Do not weaken security settings as an accepted fix. Spectre remains deliberately disabled by policy.

---

# 15. LATER MIGRATION STAGES

Stage B:
- buildable provisional VapourSynth API4 DLL placeholder;
- C++;
- x64 / AVX2;
- Release `/MT`;
- plugin `/sdl` ON;
- same security policy;
- vendor VS headers as decided;
- no Stage 2 algorithm implementation.

Stage C:
- canonical reproducible VS2026 build harness;
- `vswhere`;
- same-install MSBuild;
- umbrella `.slnx`;
- no build-policy overrides.

Stage D:
- GitHub release workflow invokes same harness/project route;
- re-verify hosted runner capability at implementation time.

Stage E:
- wheel/PyPI scaffold;
- likely VapourSynth plugin DLL layout;
- AGPL-3.0-or-later project metadata;
- LICENSE/NOTICE;
- actual PyPI publication requires explicit authorization.

---

# 16. CRITICAL PROCESS LESSONS

- Do not infer project XML from compiler/linker switches.
- Do not infer effective command lines from project XML alone.
- Do not treat a recognized property as sufficient; placement matters.
- Do not duplicate ownership of a generated downstream switch.
- Preserve raw generated evidence and exact Claude reviews.
- Native command tlogs can omit switches visible in detailed MSBuild logs.
- Do not make a hand-maintained expected-key list when mechanical reconciliation is possible.
- `findstr` output is contextless; do not overinterpret it.
- Interactive CMD uses `%i`; BAT uses `%%i`.
- Test BATs pause; run individually.
- Do not use `git add -A`.
- Do not let CI/harness become a second configuration source.
- Do not claim Stage A complete until post-application binary and six-index gates pass.

---

# 17. IMMEDIATE NEXT ACTION IN A FRESH CHAT

Priority order:

```text
1. Preserve/inspect this v0.8 handover and the hard-earned knowledge v0.1.
2. Finish the v0.9 candidate review package cleanly.
3. Run Dave-local v0.9 assembler/validators.
4. Send READY package to Claude.
5. Carry Claude v0.9 response into knowledge/control docs.
6. Dave reviews documentation checkpoint.
7. Named-stage, inspect, commit and push documentation/evidence checkpoint.
8. If/when Dave ratifies v0.9, apply A3 and run full Stage A gate.
```

If the old chat is unavailable, do not reconstruct this sequence from memory; use the documents above.

# 18. Ratification update

A3 v0.9 candidate review is complete. Candidate design is no longer pending.

Claude independently confirmed the exact two-line v0.8 -> v0.9 diff, single-owner segment-heap fix, two pin-row changes, U2 delta coverage, six validator PASS state, and 132-property v180 recognition.

Dave ratified SHA-256:

```text
ebfcde82405fd2dc25aa7a14a160f89375465d545927b3e4583e7a40fd1af668
```

The next migration chat must proceed to application/gating, not reopen candidate design without new evidence.
