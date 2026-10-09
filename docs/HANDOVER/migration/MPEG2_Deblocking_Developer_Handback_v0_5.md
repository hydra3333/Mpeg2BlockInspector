# MPEG-2 Index-Driven Deblocking Project - Common Developer Handback from Migration

**Filename:** `MPEG2_Deblocking_Developer_Handback_v0_5.md`  
**Version:** 0.5  
**Date:** 2026-10-09  
**Drafted by:** migration ChatGPT chat  
**Intended recipients:** the main ChatGPT and Claude technical-development chats  
**Repository location when final:** `docs\HANDOVER\`  
**Status:** PROVISIONAL CURRENT-STATE HANDBACK - migration remains open  
**Authority:** migration/build-state orientation only; not MPEG-2 technical-design authority  

---

## 1. Purpose and document boundary

This is the single common handback from the repository/build-system migration work to the technical-development chats.

Its job is to tell both developer chats, consistently:

- which repository and layout they inherit;
- what migration work has completed and what remains open;
- which source is frozen and which build/project files are intentionally mutable;
- the intended Visual Studio, CPU, runtime, security and release-build policies;
- what the build harness and GitHub release workflow must do;
- what README, NOTICE and licence boundaries now apply;
- what evidence/gates must have passed before the developer chats resume implementation;
- which decisions remain technical-development decisions rather than migration decisions.

This document is **not** a handover from one developer ChatGPT/Claude chat to its successor. Any within-development-chat handover is separate and remains owned by that development chat.

This document is also **not** the migration-chat continuity handover. Migration-only continuity is recorded in `ChatGPT_Migration_Chat_Handover_v0_*.md` (and Claude's corresponding migration-only handover).

The individual developer-chat handovers should reference this common handback for migration facts instead of copying or reinterpreting those facts.

Because migration remains open, this v0.5 is a current-state handback snapshot. The final handback must be refreshed against completed Stage A-E evidence and Dave's migration-close decision before it is treated as the final return-to-development record.

---

## 2. Repository identity

GitHub repository:

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

The old tree is reference/rollback material only. It is not the active development or build tree.

Published post-restructure checkpoint known to migration:

```text
a9c782acb525943881e65b2b3f8f0484521a01c5
```

Published tag:

```text
vapoursynth-mpeg2deblock-post-restructure
```

A later final migration commit/tag is expected to become the normal development restart point.

---

## 3. Repository layout inherited by development

Current important locations are:

```text
src\Mpeg2BlockInspector\
    frozen Stage 1 inspector C/H source

tools\
    Stage1_Inspector_Analyzer_v0_2.py

TESTING\
    inspector BAT/VPY regression/test scripts

VHSC_samples\
    tracked sample media, reference indexes and related test evidence

docs\REPOSITORY\
    repository-authoritative MPEG-2/project technical documents

docs\HANDOVER\
    AI handovers plus this common migration handback

docs\HANDOVER\migration\
    migration-specific design/review/execution records

vs\VapourSynth-mpeg2deblock\
    Visual Studio solution/project area
```

When Stage 2 technical work resumes, its experimental Python belongs under:

```text
experiments\stage2\
```

Migration deliberately does not create empty technical-development directories merely to anticipate later work.

Stage B migration work will add the buildable `mpeg2Deblock` VapourSynth DLL project to the same solution. Exact public plugin naming/source-directory details remain subject to the accepted Stage B naming decision; this handback does not invent them.

---

## 4. Technical authority remains separate from migration

Migration has not replaced or redesigned the MPEG-2 algorithm/specification work.

Technical-development chats must continue to use the repository-authoritative documents, especially the current versions of:

```text
docs\REPOSITORY\02_INDEX_FORMAT_SPEC.md
docs\REPOSITORY\05_DECISIONS.md
docs\REPOSITORY\06_DEBLOCK_CONCEPT.md
```

and the ratified Stage documents including the current:

```text
Stage1_Evidence_and_Gate_Report
Stage2_Experiment_Design
```

At the current migration checkpoint, Stage 2 experiment design v0.3 is the ratified technical restart design known to migration.

Migration records build/repository state. It does not authorize or redefine deblocking algorithm work.

---

## 5. Documentation/licence files the developer chats must read

The developer chats should read the repository's current:

```text
README.md
NOTICE.md
LICENSE
```

The intended division is:

- `README.md` - public product/build summary, including the intended AVX2 minimum CPU, standalone Release build and build prerequisites;
- `NOTICE.md` - legal/attribution boundary, including MPEG reference-decoder-derived source, restricted test recordings and third-party material;
- `LICENSE` - licence for project-developed material, currently AGPL-3.0-or-later.

Do not replace the exact legal/attribution language from `NOTICE.md` with paraphrases from an AI handover.

The currently updated README already describes target AVX2/standalone/security policy. Until the corresponding A3/Stage B gates pass, those build statements are target policy rather than proof that every current checked-out artifact already has those properties.

---

## 6. Stage 1 inspector status and frozen boundary

Stage 1 was already:

```text
COMPLETE
PASS
FROZEN
```

before this migration.

The critical boundary is:

```text
Mpeg2BlockInspector C/H SOURCE:
    frozen

Mpeg2BlockInspector Visual Studio project/build configuration:
    migration-owned and intentionally mutable
```

The inspector source must not be edited merely to satisfy build-setting preferences.

Known protected identities include:

```text
src\Mpeg2BlockInspector\getpic.c
e80239cfe73a0c04490a9bf131714861254ed1d7d095b052aac616a887ef0eca

src\Mpeg2BlockInspector\mpeg2dec.c
8e6053ccb3a40be8c0d985f2e35124bf728d1f61df9b6d0c01b71e13e13b0947

tools\Stage1_Inspector_Analyzer_v0_2.py
8e0d58305ee4fe518c25b67bdbe74acc4fb392486f23e6137862d916e5e02cda
```

---

## 7. Migration work already completed

Repository/restructure work already completed includes:

- GitHub repository renamed to `VapourSynth-mpeg2Deblock`;
- production clone established at the new root;
- inspector source moved under `src\Mpeg2BlockInspector\`;
- Visual Studio material moved under `vs\VapourSynth-mpeg2deblock\`;
- analyzer retained under `tools\`;
- test scripts repaired for the new tree;
- Python cache ignore rules added;
- repository licence/notice/test-media boundary documented;
- post-restructure build/test evidence produced and published;
- x86/Win32 project configurations removed in Stage A1;
- legacy `.sln` replaced by x64 `.slnx` in Stage A2;
- mandatory pre-A3 Debug/Release checkpoint completed;
- all six tracked index baselines reproduced byte-identically at the pre-A3 checkpoint;
- frozen inspector source/analyzer protected through that checkpoint.

Known Stage A commits:

```text
A1 d38d56d697107e7409f4baa7753bfb31b8d94747
    Remove Win32 inspector configurations

A2 837df123ebfe0fa083fec9d6de8969bd180f9ac0
    Replace inspector solution with x64 slnx
```

The checkpoint used VS/MSBuild 18.10.1.42706, toolset v145 and selected Windows SDK 10.0.28000.0. The SDK version is recorded as build provenance but is deliberately not pinned in the project.

---

## 8. Current migration state at this handback snapshot

Current controlling migration documents are:

```text
Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_11.md
StageA_Visual_Studio_Normalization_Execution_Plan_v0_6.md
```

Current state:

```text
Repository restructure: COMPLETE
Stage A1: APPLIED / COMMITTED
Stage A2: APPLIED / COMMITTED
Pre-A3 checkpoint: COMPLETE / PASS / Claude closed
A3 v0.2: superseded
A3 v0.3: superseded for application because it targeted SSE2/security-off
Superseding A3: NOT YET GENERATED/APPLIED at this snapshot
Stage B: NOT YET STARTED
Stage C: NOT YET STARTED
Stage D: NOT YET STARTED
Stage E: NOT YET STARTED
Migration close-out: NOT YET COMPLETE
```

Therefore this document does not yet authorize Stage 2 implementation. Dave will explicitly decide when migration is closed and development may resume.

---

## 9. Final Visual Studio/product build policy inherited by development

The intended project-level policy is now explicit and project-wide unless a project-specific exception is stated.

### 9.1 Platform / CPU

```text
Windows x64 only
Debug x64
Release x64
Minimum CPU: x64 + AVX2
/arch:AVX2 in both Debug and Release
pre-AVX2 CPUs intentionally unsupported
Release /favor:blend
```

This applies to both `Mpeg2BlockInspector` and the future `mpeg2Deblock` DLL project.

### 9.2 Release runtime / standalone distribution

Release artifacts are intended to require no separately installed Microsoft Visual C++ Redistributable:

```text
Release RuntimeLibrary = /MT
Debug RuntimeLibrary   = /MDd
```

The project files themselves must produce this result.

The future plugin DLL follows the same Release `/MT` policy. A hybrid runtime model is only a documented fallback if Stage B finds a concrete technical problem.

### 9.3 Release PDB path hygiene

Release artifacts use:

```text
/PDBALTPATH:%_PDB%
```

so shipped artifacts embed the PDB file name rather than Dave's/CI's absolute build path.

### 9.4 Security policy

Performance work must not gain speed merely by globally disabling security mitigations.

Accepted target settings are:

```text
/GS ON
Control Flow Guard ON at compile/link
CET compatibility ON
Spectre mitigation ON with the corresponding mitigated libraries
```

Missing Spectre-mitigated libraries are a toolchain/build-prerequisite failure, not permission to silently weaken the build.

### 9.5 SDL exception

Inspector:

```text
/sdl OFF
```

This is a deliberate exception because the inspector source is frozen and derived from the MPEG-2 reference decoder; migration will not edit legacy/reference-decoder source merely to satisfy `/sdl` diagnostics.

New `mpeg2Deblock` code:

```text
/sdl ON
```

### 9.6 Project files are the build-settings source of truth

The `.vcxproj` files own the accepted CPU/runtime/security/optimization settings.

The local harness and GitHub release workflow must build those project files through MSBuild and verify the effective result. They must not maintain a second hand-written `cl` flag map or inject `/MT`, `/arch:AVX2`, CFG, CET, Spectre, `/sdl`, optimization or toolset overrides to repair divergent project settings.

---

## 10. Windows SDK/toolset policy

Platform toolset remains explicitly:

```text
v145
```

A specific Windows SDK version is deliberately **not** pinned.

Controlled builds must record the actual SDK selected by Visual Studio/MSBuild as artifact provenance. This matters more after `/MT`, because the selected SDK's static UCRT contributes to the shipped Release binary.

---

## 11. Six Stage A functional baselines

The six tracked `.idx` files in Git are authoritative baseline bytes for Stage A regression. Recorded SHA-256 values are:

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

The superseding A3 gate must reproduce all six exactly. Do not weaken that gate to accommodate a build-setting change.

---

## 12. What Stage A must still prove before handback

The superseding A3 must be cold-reviewed/ratified before application and must then prove, at minimum:

- Debug and Release x64 build PASS;
- exact effective compiler/linker deltas explained;
- `/arch:AVX2` effective in Debug and Release;
- Release `/MT` effective and no prohibited VC/UCRT runtime DLL dependencies remain;
- `/GS`, CFG, CET and Spectre policies actually effective;
- inspector `/sdl` exception remains OFF;
- frozen source/analyzer unchanged;
- all six tracked indexes byte-identical;
- warnings explained;
- README build-policy claims match accepted evidence;
- project settings, not harness overrides, are responsible for the result.

If AVX2/security changes unexpectedly alter an index, migration must diagnose by temporary local variants. It must not silently abandon the ratified product/security policy.

---

## 13. Stage B result the developer chats should expect

Stage B is migration/build-system scaffolding only. It does **not** implement the deblocking algorithm.

Expected end-state:

```text
VapourSynth-mpeg2deblock.slnx
    Mpeg2BlockInspector    C EXE
    mpeg2Deblock           C++ VapourSynth API4 DLL placeholder
```

The placeholder DLL should be minimally buildable/loadable and expose the API4 plugin entry point, but contain no Stage 2 deblocking implementation.

Its project must already carry the accepted project policy:

```text
x64 only
AVX2 minimum
Release /MT
Release /PDBALTPATH:%_PDB%
/GS ON
CFG ON
CET ON
Spectre ON
/sdl ON
```

Stage B must prove exports, dependencies/loadability and inspector non-regression.

---

## 14. Stage C/D/E result the developer chats should expect

### Stage C - canonical local build harness

One reproducible route discovers the installed Visual Studio/MSBuild using `vswhere`, builds the `.slnx`, records toolchain/SDK provenance and verifies project outputs/settings.

### Stage D - release-triggered GitHub workflow

The workflow must call the same Stage C/MSBuild route. It must not reproduce CNR3's old hand-written `cl` flag map or override ratified project settings.

Runner/toolset claims must be verified when the workflow is built. If required v145 or Spectre-mitigated libraries are absent, CI fails rather than substitutes/weakens the build.

### Stage E - Windows wheel/PyPI packaging scaffold

The migration scope includes adapting the proven CNR3 wheel pattern for this project, with project-specific package identity and correct AGPL/NOTICE metadata. Actual publication to PyPI is not implicitly authorized by migration.

---

## 15. What migration deliberately does not decide

The following remain technical-development responsibilities unless separately ratified:

- Stage 2 experiment implementation/results;
- actual deblocking algorithm;
- scalar/AVX2 kernel design and optimization details;
- index-consumption semantics beyond existing repository authority;
- VapourSynth processing/scheduling/filter architecture;
- visual-quality decisions;
- final public plugin behavior/API beyond build/package identity decisions required for migration scaffolding.

AVX2 as the minimum supported CPU is already a product/build policy. How the deblocking implementation best uses AVX2 remains technical-development work.

---

## 16. How the developer chats should restart after final migration close-out

When Dave explicitly authorizes return to development, both developer chats should:

1. start from the final migration commit/tag and active repository only;
2. read the final version of this common handback;
3. read `README.md`, `NOTICE.md`, `LICENSE`;
4. re-read the repository-authoritative technical documents (`02`, `05`, `06`) and Stage 2 experiment design;
5. confirm the frozen inspector/analyzer identities and current build harness work on their machine/session as appropriate;
6. treat the accepted Visual Studio project files and build harness as infrastructure, not as an invitation to redesign migration settings;
7. resume the established technical workflow:

```text
ChatGPT drafts/designs
    -> Claude independent review
    -> Dave resolves/ratifies
    -> implementation proceeds
```

A developer chat's own future-chat handover remains separate from this common migration handback.

---

## 17. Final migration close-out data still to insert

Before this document becomes the final handback, migration should replace provisional/current-state statements with exact final evidence including:

- final migration HEAD/commit/tag and push status;
- final accepted A3 project hash/commit and Stage A gate result;
- final Stage B project/solution paths and hashes;
- final Stage C harness path/version and gate result;
- final Stage D workflow path and release-build evidence;
- final Stage E package/wheel layout and local install/load smoke evidence;
- final selected package/plugin naming;
- final toolchain/SDK provenance for accepted release artifacts;
- final standalone dependency/export/security checks;
- final README/NOTICE consistency check;
- clean Git status and any old-tree retirement/retention decision.

---

## 18. Change log

### v0.5 - 2026-10-09

- Clarified document taxonomy: this is migration-to-development handback, not migration-chat continuity and not an internal developer-chat handover.
- Updated execution state to A1/A2 applied and pre-A3 checkpoint complete, with A3 v0.3 superseded and a new AVX2/security-on A3 still required.
- Added current AVX2 minimum, `/favor:blend`, `/MT`, PDB-path, `/GS`, CFG, CET, Spectre and SDL-exception policies.
- Added the project-files-as-source-of-truth and one-build-route rule for local harness/GitHub Actions.
- Added explicit README/NOTICE/LICENSE roles and the target-policy-versus-build-evidence distinction.
- Expanded the handback into a practical restart record for both development chats after migration close-out.
- Kept technical-development authority and within-dev-chat handovers explicitly separate.

### v0.4 - 2026-10-09

- Interim current-state refresh during Stage A migration work.
