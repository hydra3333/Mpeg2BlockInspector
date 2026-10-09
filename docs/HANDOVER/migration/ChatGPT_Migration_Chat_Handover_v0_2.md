# ChatGPT Handover to a Future Migration Chat
## VapourSynth-mpeg2Deblock Repository / Visual Studio / Release Migration

**Filename:** `ChatGPT_Migration_Chat_Handover_v0_2.md`  
**Version:** 0.2  
**Date:** 2026-10-09  
**From:** current migration ChatGPT chat  
**To:** a fresh ChatGPT chat continuing migration/build-system work  
**Status:** MIGRATION-ONLY continuity handover; not MPEG-2 technical authority  
**Supersedes:** `ChatGPT_Migration_Chat_Handover_v0_1.md`  

---

## 0. Document taxonomy - do not mix these roles

This handover exists **only** to continue the migration/build-system chat if the current ChatGPT conversation must be replaced.

Keep these three document roles distinct:

```text
A. ChatGPT_Migration_Chat_Handover_v0_*.md
   -> migration ChatGPT -> future migration ChatGPT
   -> contains migration execution state/details

B. MPEG2_Deblocking_Developer_Handback_v0_*.md
   -> migration -> BOTH technical-development chats
   -> contains the repository/layout/build/settings state they inherit

C. developer-chat internal handovers
   -> one technical-development chat -> its future replacement chat
   -> owned by that developer chat; migration does not rewrite them unless Dave explicitly asks
```

Claude has an analogous migration-only continuity handover. It must not be confused with Claude's technical-development handovers either.

The common developer handback should be the single shared source for migration facts consumed by both developer chats. Their own handovers should point to it instead of independently reconstructing migration history.

---

## 1. First actions for a future migration ChatGPT

Before changing anything:

1. Read this whole handover.
2. Read the current controlling migration documents:
   - `Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_11.md`
   - `StageA_Visual_Studio_Normalization_Execution_Plan_v0_6.md`
   - `MPEG2_Deblocking_Developer_Handback_v0_5.md`
3. Read the current migration Claude reviews, especially:
   - `Claude_REVIEW_OF_ChatGPT_DR_v0_8_and_StageA_Plan_v0_3_v0_2.md`
   - `Claude_REVIEW_OF_ChatGPT_Migration_Plan_Update_Standalone_PyPI_v0_1.md`
   - `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_2_Package_v0_1.md`
   - `Claude_REVIEW_OF_ChatGPT_StageA_Checkpoint_Status_v0_1.md`
   - `Claude_RESPONSE_TO_ChatGPT_AVX2_Acceptance_and_README_v0_1.md`
4. Read the repository `README.md`, `NOTICE.md` and `LICENSE` for public/build/legal context.
5. Inspect the actual repository state before assuming Git status from this handover; this document records the last known migration evidence, not a live filesystem query.
6. Do not use the technical project's future-ChatGPT handover as a migration execution document.
7. Do not redesign or implement Stage 2 deblocking in the migration chat.
8. Do not modify frozen inspector C/H source.
9. Do not apply any superseded A3 candidate.

Current high-level state:

```text
Repository restructure: COMPLETE
A1: APPLIED / COMMITTED
A2: APPLIED / COMMITTED
Pre-A3 checkpoint: COMPLETE / PASS / Claude closed
A3 v0.2: superseded
A3 v0.3: superseded for application (SSE2/security-off conflict)
Superseding A3: must be generated/reviewed before application
Stage B: not started
Stage C: not started
Stage D: not started
Stage E: not started
Migration: OPEN
```

---

## 2. Scope of this migration chat

This migration owns:

- repository migration/restructure mechanics;
- Visual Studio solution/project normalization;
- x64-only configuration;
- `.sln` -> `.slnx`;
- explicit build-setting audit/normalization;
- inspector standalone Release configuration;
- creation of a minimal/buildable VapourSynth API4 DLL placeholder project;
- canonical local VS2026/MSBuild build harness;
- release-triggered GitHub workflow using that same build route;
- Windows wheel/PyPI packaging scaffold;
- validation/evidence;
- migration documentation and common handback to development.

This migration does **not** own:

- Stage 2 experiment implementation;
- deblocking algorithm design/implementation;
- scalar or AVX2 kernel implementation details;
- index-consumption algorithm details beyond existing authority;
- final VapourSynth processing/scheduling/filter architecture;
- visual-quality decisions.

Deblock4 is abandoned technical history. It may be consulted only to recycle useful proven build/script patterns where appropriate.

---

## 3. Roles and workflow

```text
Dave
    owner/final authority; runs local Windows builds/tests; ratifies decisions

Migration ChatGPT
    drafts migration mechanics, project candidates, scripts, audits, exact commands/docs

Migration Claude
    independent cold reviewer
```

Workflow:

```text
ChatGPT draft/proposal
    -> Claude cold review
    -> Dave resolves/ratifies
    -> ChatGPT proceeds
```

Use named Git staging only. Do not use `git add -A`.

Do not push before the agreed gate for the relevant stage unless Dave explicitly changes that rule.

---

## 4. Repository identity and known checkpoints

GitHub:

```text
https://github.com/hydra3333/VapourSynth-mpeg2Deblock
```

Active repository:

```text
E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock
```

Old rollback/reference tree:

```text
E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector
```

Published post-restructure HEAD:

```text
a9c782acb525943881e65b2b3f8f0484521a01c5
```

Published tag:

```text
vapoursynth-mpeg2deblock-post-restructure
```

Pre-Stage-A tag:

```text
pre-stageA-vs-normalization
```

at:

```text
b38fde11d64935db933707704b45581d5dddcde7
```

Known local Stage A commits:

```text
A1 d38d56d697107e7409f4baa7753bfb31b8d94747
    Remove Win32 inspector configurations

A2 837df123ebfe0fa083fec9d6de8969bd180f9ac0
    Replace inspector solution with x64 slnx
```

At the last explicit migration Git-state check before the later documentation refresh, A1/A2 were local commits ahead of origin and no A3 settings had been applied. Always re-check the live repository before acting.

---

## 5. Current repository layout

```text
src\Mpeg2BlockInspector\
    frozen Stage 1 inspector C/H source

tools\Stage1_Inspector_Analyzer_v0_2.py

TESTING\
    inspector BAT/VPY regression scripts

VHSC_samples\
    tracked media/index evidence

docs\REPOSITORY\
    technical authority documents

docs\HANDOVER\
    project/developer handovers

docs\HANDOVER\migration\
    migration records/reviews/plans

vs\VapourSynth-mpeg2deblock\
    current solution/project area
```

Do not create `experiments\stage2\` merely for migration. It belongs to later technical work.

---

## 6. Frozen source / mutable build distinction

Frozen:

```text
src\Mpeg2BlockInspector\*.c
src\Mpeg2BlockInspector\*.h
```

Not frozen:

```text
vs\VapourSynth-mpeg2deblock\Mpeg2BlockInspector.vcxproj
vs\VapourSynth-mpeg2deblock\Mpeg2BlockInspector.vcxproj.filters
solution/build-system/harness/workflow files
```

Dave explicitly ruled that inspector project/build settings are migration scope. Source remains frozen.

Protected hashes:

```text
getpic.c
 e80239cfe73a0c04490a9bf131714861254ed1d7d095b052aac616a887ef0eca

mpeg2dec.c
 8e6053ccb3a40be8c0d985f2e35124bf728d1f61df9b6d0c01b71e13e13b0947

Stage1_Inspector_Analyzer_v0_2.py
 8e0d58305ee4fe518c25b67bdbe74acc4fb392486f23e6137862d916e5e02cda
```

---

## 7. Six tracked Stage A index baselines

The authoritative baseline bytes are the tracked `.idx` files in Git. Recorded SHA-256 copies:

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

All six reproduced exactly at the mandatory pre-A3 checkpoint.

---

## 8. A1/A2 and pre-A3 checkpoint - completed

### A1

Removed Win32 inspector configurations only.

Accepted project SHA after A1:

```text
87acd9ad1c94e5545f84fe57857c076781ca499523d2a80545919ae571dc7a57
```

Commit:

```text
d38d56d697107e7409f4baa7753bfb31b8d94747
```

### A2

Replaced legacy `.sln` with x64 `.slnx`.

Candidate `.slnx` SHA:

```text
fa24efcd73401a38604e2f4228b07d8b960abcbfb66da22c02908e9d1cdb0754
```

Commit:

```text
837df123ebfe0fa083fec9d6de8969bd180f9ac0
```

Interactive VS2026 load passed: one inspector project, x64 only, Debug/Release, no conversion/rewrite.

### Pre-A3 checkpoint

Toolchain evidence:

```text
VSINSTALL = C:\Program Files\Microsoft Visual Studio\18\Community
MSBuild   = 18.10.1.42706
Toolset   = v145
VCTools   = 14.51.36231
Host      = pre-A3 HostX86\x64 compiler/linker
SDK       = 10.0.28000.0 (selected, not pinned)
```

Debug: build PASS; 20 normalized warnings.  
Release: build PASS; exact known 17-warning baseline.  
All six tracked indexes: exact SHA baseline PASS.  
Frozen source/analyzer diff: none.

Claude closed the checkpoint with no evidence defect and authorized moving to a revised A3 proposal.

---

## 9. Ratified product/build policy - current, superseding old AVX2-off assumptions

### 9.1 CPU/platform

```text
x64 only
minimum supported CPU = x64 + AVX2
/arch:AVX2 Debug + Release
pre-AVX2 CPUs intentionally unsupported
Release /favor:blend
```

This applies to both inspector and future plugin project.

### 9.2 Runtime / standalone Release

```text
Debug   /MDd
Release /MT
```

Release EXE and DLL must not require a separately installed Microsoft Visual C++ Redistributable.

The `.vcxproj` files themselves are the source of truth for this. Harness/CI may verify but not inject it.

### 9.3 Release PDB path

```text
/PDBALTPATH:%_PDB%
```

### 9.4 Security

```text
/GS ON
CFG ON compile+link
CET compatibility ON
Spectre mitigation ON + matching mitigated libraries
```

Performance must not be gained merely by globally disabling these mitigations.

Missing Spectre-mitigated libraries fail the build/readiness check.

### 9.5 SDL

Inspector:

```text
/sdl OFF
```

because frozen source derives from the MPEG-2 reference decoder.

New plugin:

```text
/sdl ON
```

### 9.6 Windows SDK/toolset

```text
PlatformToolset = v145
Windows SDK version = deliberately unpinned
```

Record the actual selected SDK at every controlled gate/release build.

---

## 10. Project files are authoritative; one build route

Hard rule:

- accepted `.vcxproj` settings define AVX2/runtime/security/optimization/toolset behavior;
- Stage C harness invokes MSBuild on the `.slnx`;
- Stage D GitHub Actions invokes that same harness/build route;
- no duplicated hand-written CNR3-style `cl` flag map;
- no CI-only `/MT`, `/arch:AVX2`, CFG/CET/Spectre/SDL/toolset/optimization overrides;
- if the runner lacks required v145 or Spectre libraries, fail hard.

This is both a reproducibility and configuration-drift control.

---

## 11. Current A3 state - superseded candidates; do not apply them

Historical/review candidates:

```text
A3 v0.1: DO NOT APPLY
A3 v0.2 DRAFT: SUPERSEDED
A3 v0.3 DRAFT: SUPERSEDED FOR APPLICATION
```

A3 v0.3 became invalid when Dave changed the product policy from an inspector SSE2 floor/security-off preservation to:

```text
/arch:AVX2
/favor:blend Release
/GS ON
CFG ON
CET ON
Spectre ON
/MT Release
/PDBALTPATH:%_PDB%
```

with inspector `/sdl` OFF as the sole deliberate security-compiler-policy exception.

The next A3 package must be newly generated from the current A1/A2/pre-A3 state and current DR/Plan. Do not patch/apply v0.3 in place.

---

## 12. Superseding A3 requirements

The next A3 proposal/review package must include:

- complete 113-row CNR3 reconciliation with dispositions/reasons;
- exact project candidate and diff;
- explicit pins required by DR v0.11 / Plan v0.6;
- `/arch:AVX2` Debug+Release;
- Release `/favor:blend`;
- Debug `/MDd`, Release `/MT`;
- Release `/PDBALTPATH:%_PDB%`;
- `/GS`, CFG, CET, Spectre ON;
- inspector `/sdl` OFF;
- required Spectre-library readiness check;
- predicted exact compiler/linker command deltas;
- M3 PE/load-config/import gate;
- standalone forbidden-runtime-DLL gate;
- six-index gate;
- frozen-source gate;
- README policy consistency check;
- evidence assembly.

It must be cold-reviewed by Claude and ratified by Dave before application.

If the post-A3 index gate fails, do not weaken the gate or silently revert policy. Diagnose with uncommitted variants, beginning with settings capable of altering generated code (ISA floor, `/GL`/`/LTCG`, host architecture, etc.), then return evidence to Claude/Dave.

---

## 13. Stage B - after Stage A closes

Create a minimal/buildable VapourSynth API4 DLL placeholder in the same `.slnx`.

No deblocking algorithm.

The DLL project must itself encode:

```text
x64 only
/arch:AVX2 Debug+Release
Release /favor:blend
Debug /MDd
Release /MT
Release /PDBALTPATH:%_PDB%
/GS ON
CFG ON
CET ON
Spectre ON
/sdl ON
```

Use project-relative VapourSynth headers. The minimal source should expose `VapourSynthPluginInit2` and be sufficient for export/dependency/load smoke testing.

Protect the inspector during Stage B with rebuild/regression evidence.

---

## 14. Stage C - canonical local build harness

Requirements:

- discover Visual Studio using `vswhere -products *` plus required C++ component criteria;
- derive MSBuild from that same installation;
- build `VapourSynth-mpeg2deblock.slnx` Debug/Release x64 as requested;
- record toolchain/SDK paths/versions;
- verify expected output artifacts;
- verify project settings took effect;
- no hard-coded Community-only path assumption;
- no toolset/runtime/security/ISA command-line repair overrides.

---

## 15. Stage D - release-triggered GitHub workflow

CNR3's actual workflow was inspected. Important finding:

- CNR3 CI does not build through its Visual Studio project; it has a separate hand-written `cl` flag map;
- CNR3 CI already builds a Windows wheel.

For this project, do **not** copy the duplicate flag map.

Stage D must invoke the same Stage C harness/MSBuild/`.slnx` route qualified locally.

It must verify toolchain/SDK, EXE/DLL outputs, exports/dependencies/security/standalone state, and fail if the runner cannot satisfy the accepted project requirements.

Any claim about the current `windows-latest` image/toolset must be re-verified when Stage D is implemented.

---

## 16. Stage E - wheel/PyPI packaging scaffold

Adapt the proven CNR3 wheel pattern rather than inventing a second packaging approach.

Decide the package identity, plugin folder and DLL name as one coupled Stage B/E naming set.

Wheel metadata must reflect this project's licences/notices:

```text
AGPL-3.0-or-later for project-developed material
LICENSE included
NOTICE included
```

Do not copy CNR3's MIT metadata.

Actual publication to PyPI is not automatically authorized.

---

## 17. README / NOTICE documentation rule

The updated repository README already states target product/build requirements including AVX2, standalone Release artifacts and Spectre-mitigated build prerequisites.

Treat those as ratified target policy but not as substitute evidence. Stage A/Stage B gates must prove the corresponding binaries/projects.

`NOTICE.md` is the legal/attribution boundary. Migration handovers should point to it rather than duplicate/rewrite its exact legal language.

At migration close-out, handback must confirm README claims and accepted build evidence agree.

---

## 18. Common developer handback - role and timing

Current common handback:

```text
MPEG2_Deblocking_Developer_Handback_v0_5.md
```

Its role:

```text
migration -> both technical-development chats
```

It is intentionally separate from this migration-only handover and from each technical chat's own future-chat handover.

It may be kept current provisionally during migration, but it becomes the final development restart record only after Stage A-E close-out, final repository/tag/build evidence and Dave authorization.

---

## 19. Immediate next action

At this handover snapshot, the next controlled sequence is:

1. send current migration documents and boundary clarification to migration Claude for cold review:
   - DR v0.11;
   - Stage A Plan v0.6;
   - common Developer Handback v0.5;
   - this migration ChatGPT handover v0.2;
2. resolve any Claude/Dave corrections;
3. generate the superseding A3 review package from the untouched current repository project state;
4. cold-review and ratify A3;
5. apply A3 only after approval;
6. run full Stage A gate;
7. continue Stage B -> C -> D -> E;
8. finalize common developer handback and migration-specific handovers;
9. Dave explicitly closes migration and authorizes return to Stage 2 technical development.

---

## 20. Cautions / lessons

- Do not confuse migration handovers with technical-development handovers.
- Do not use a development-chat handover as migration authority.
- Do not claim the earlier restructure Gate C was six-of-six; Dave waived four cases there. The later pre-A3 checkpoint *was* six-of-six.
- Do not modify frozen C/H source to accommodate build settings.
- Do not use `git add -A`.
- Do not assume ignored/intermediate files imply tracked changes; inspect `git status --short --ignored` when needed.
- Do not restore tracked `.idx` files after a regression run merely to make Git clean; exact clean tracked status after regeneration is evidence that the bytes matched.
- Batch test scripts contain `pause`; run them one at a time.
- In interactive CMD use `%i`; in BAT files use `%%i`.
- Prefer exact binary copies for tlogs (`copy /b /y`).
- Do not rely on mutable Microsoft defaults for output-affecting settings except the deliberate unpinned-SDK policy.
- Do not let CI become a second configuration source.

---

## 21. Change log

### v0.2 - 2026-10-09

- Replaced the obsolete pre-A1/A2 state in v0.1 with the current post-A1/A2/pre-A3-checkpoint state.
- Added explicit document taxonomy separating migration continuity, common migration-to-development handback, and within-development-chat handovers.
- Added current AVX2 minimum, standalone `/MT`, PDB-path, security-hardening and SDL-exception policies.
- Marked A3 v0.3 superseded for application and specified requirements for its replacement.
- Added Stage C/D/E current direction including one-build-route GitHub and wheel scaffold.
- Added README/NOTICE consistency rules.
- Updated exact next action to Claude review -> superseding A3 -> Stage A gate -> B/C/D/E -> final handback.

### v0.1 - 2026-10-09

- Initial migration-chat continuity handover, written before A1/A2 were applied and before the AVX2/security/standalone policy was finalized.
