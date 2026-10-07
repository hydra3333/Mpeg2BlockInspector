# Repository and GitHub Migration Proposal
## MPEG-2 Indexer + VapourSynth Deblocker Project

**Filename:** `Repository_and_GitHub_Migration_Proposal_v0_1.md`  
**Version:** 0.1  
**Date:** 2026-10-08  
**Drafted by:** ChatGPT  
**Status:** DISCUSSION / CLAUDE REVIEW INPUT ONLY. Not repository authority.  
**Scope:** Project/repository organisation and migration only. No Stage 2 coding is authorised by this document.

---

## 1. Purpose

The technical design is now sufficiently mature that the existing repository identity and Visual Studio layout no longer match the direction of the project.

The current GitHub/local repository began as a project for:

```text
Mpeg2BlockInspector
```

The ratified project is now broader:

```text
MPEG-2 indexer / inspector
+
Stage 2 experiment tooling
+
future VapourSynth MPEG-2 deblocking plugin
+
shared index-format / algorithm documentation
```

Dave and ChatGPT both currently favour **one umbrella repository** rather than splitting the indexer and filter into separate repositories.

Dave has selected the proposed umbrella name:

```text
VapourSynth-mpeg2Deblock
```

This proposal sets out:

- the current situation;
- why a repository migration is recommended;
- known migration risks;
- additional risks identified by ChatGPT;
- a proposed end-state tree;
- a safe staged migration;
- what may be reusable from Dave's existing `vapoursynth-cnr3` repository;
- what must be inspected rather than assumed;
- questions for Claude.

No repository rename, source move or Visual Studio project edit should occur until this proposal is reviewed and Dave decides the migration approach.

---

## 2. Current repository situation

### 2.1 Local repository

Current local repository:

```text
E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector
```

### 2.2 GitHub repository

Current GitHub repository:

```text
https://github.com/hydra3333/Mpeg2BlockInspector
```

Dave currently commits and pushes changes from Visual Studio 2026 Community from the local repository to that GitHub repository.

### 2.3 Current root tree reported by Dave

```text
Mpeg2BlockInspector\
    .gitignore
    .vs\
    docs\
    LICENSE
    Mpeg2BlockInspector.vcxproj
    README.md
    src\
    TESTING\
    VHSC_samples\
```

### 2.4 Current `src` tree characteristics

The current `src` contains several different categories mixed together:

1. MPEG-2 reference-decoder-derived C source used by the inspector.
2. Stage 1 inspector changes.
3. `Stage1_Inspector_Analyzer_v0_2.py`.
4. Visual Studio solution/project files:
   - `Mpeg2BlockInspector.sln`
   - `Mpeg2BlockInspector.vcxproj`
   - `Mpeg2BlockInspector.vcxproj.filters`
   - `Mpeg2BlockInspector.vcxproj.user`
5. generated/local-looking directories:
   - `Mpeg2Blo.F4B1A357`
   - `x64`
6. `patches`.

There is also a second:

```text
Mpeg2BlockInspector.vcxproj
```

at repository root.

At present it is not safe to assume which of the two project files is live, obsolete, auxiliary or differently configured without inspecting the actual solution/project contents.

### 2.5 Existing test layout

Dave reports that test `.vpy` and `.bat` files reside under:

```text
TESTING
```

The repository also contains:

```text
VHSC_samples
```

The exact tracked contents, size, provenance and GitHub suitability of the sample directory need to be audited before the migration.

---

## 3. Why change is recommended

The current repository name and source layout accurately describe the project's origin but not its future composition.

The expected project now contains at least these distinct work products:

```text
1. Mpeg2BlockInspector
   command-line MPEG-2 index / evidence tool

2. Stage 2 experimental implementation
   Python/reference research code

3. VapourSynth-mpeg2Deblock
   eventual production VapourSynth API4 plugin

4. Shared project knowledge
   decisions, algorithm concept, index-format specification,
   Stage 1/Stage 2 designs, tests and acceptance evidence
```

Keeping all future code directly under the existing flat `src` would create naming, build and ownership ambiguity.

Splitting the inspector and plugin into separate Git repositories now would create a different problem: the indexer, `.idx2` format, plugin and tests are expected to co-evolve and may require atomic changes.

Current ChatGPT recommendation:

> Keep **one umbrella Git repository**, rename the repository to `VapourSynth-mpeg2Deblock`, and make the inspector and plugin separate components/projects inside that repository.

This remains a proposal until reviewed by Claude and decided by Dave.

---

## 4. Proposed identity

### 4.1 Umbrella repository name

Proposed:

```text
VapourSynth-mpeg2Deblock
```

Not:

```text
VapourSynthMpeg2Deblock
```

### 4.2 Proposed GitHub repository

```text
https://github.com/hydra3333/VapourSynth-mpeg2Deblock
```

subject to the actual GitHub rename operation Dave chooses.

### 4.3 Proposed new local clone location

Following Dave's normal repository layout:

```text
E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\
    VapourSynth-mpeg2Deblock\
```

The old working tree should initially be left untouched as a recovery/reference copy.

### 4.4 Component naming

The repository rename does **not** require the existing command-line component to lose its useful name.

The following may remain valid:

```text
Mpeg2BlockInspector.exe
Mpeg2BlockInspector.vcxproj
```

The future plugin can have its own project/binary naming.

Repository name, Visual Studio project name, DLL filename, VapourSynth plugin identifier and C/C++ symbol names do not all need to be identical.

In particular, a hyphenated repository/project filename is possible, while C/C++ identifiers and VapourSynth registration names may require or benefit from different identifier-safe spelling.

Those naming details should be decided explicitly rather than inferred from the GitHub repository name.

---

## 5. Known migration issues raised by Dave

### 5.1 Hard-coded paths / names in Visual Studio files

Likely or known candidates include:

```text
.sln
.slnx
.vcxproj
.vcxproj.filters
.vcxproj.user
```

Possible embedded dependencies include:

```text
relative source paths
absolute paths
project paths
output directories
intermediate directories
include directories
library directories
post-build commands
debugger working directories
test executable paths
```

A repository or source move must therefore be preceded by file-content inspection.

### 5.2 Duplicate / multiple project files

There is:

```text
Mpeg2BlockInspector.vcxproj
```

at repository root and another under:

```text
src\
```

The active relationship between:

```text
Mpeg2BlockInspector.sln
Mpeg2BlockInspector.vcxproj
root Mpeg2BlockInspector.vcxproj
```

must be established before deleting, moving or renaming anything.

### 5.3 Existing `src` is not suitable for the future multi-component project

Current flat layout:

```text
src\
    MPEG-2 C source
    inspector project files
    Python analyzer
    generated folders
```

does not provide clean ownership for:

```text
Mpeg2BlockInspector
VapourSynth-mpeg2Deblock
Stage 2 experiments
shared tools
```

### 5.4 Generated Visual Studio/build directories

Current examples:

```text
.vs\
src\x64\
src\Mpeg2Blo.F4B1A357\
src\*.vcxproj.user
```

These appear likely to contain local/generated state, but that must be confirmed by:

```text
git ls-files
.gitignore inspection
Visual Studio project inspection
```

They should not simply be moved because they exist.

### 5.5 Test scripts may encode old paths

Potentially affected:

```text
TESTING\*.bat
TESTING\*.vpy
Python scripts
README examples
documentation commands
```

A successful Visual Studio build alone would therefore not prove a migration is complete.

---

## 6. Additional risks identified by ChatGPT

### 6.1 Licensing / provenance

The inspector contains MPEG-2 reference-decoder-derived source.

The future plugin will contain newly developed project code.

Before adopting a single repository-wide licensing presentation, verify:

- source provenance;
- licence obligations of the reference-decoder-derived code;
- whether the existing repository `LICENSE` accurately applies to all future components;
- whether component-level notices are required.

This is not a claim that there is a licence conflict.

It is a migration item that should be checked explicitly rather than implied by directory layout.

### 6.2 Git history preservation

The migration should preserve the existing history.

Avoid creating a completely unrelated new Git repository unless there is a strong reason.

A repository rename plus fresh clone can preserve continuity while changing the working path.

### 6.3 Test-media policy

Audit:

```text
VHSC_samples
```

and any other media before treating the new public GitHub repository as the permanent umbrella.

Questions:

- Is the material tracked by Git?
- How large is it?
- Is redistribution permitted?
- Is it user-created / freely redistributable / copyrighted broadcast material?
- Would hashes, logs, indexes or metadata be sufficient in Git while media remains local?

Default recommendation:

> Do not commit large or redistribution-sensitive video merely because it is needed for local acceptance testing.

### 6.4 Build-output policy

Do not mix the architectural migration with an unnecessary redesign of all output paths.

For example, moving from current `x64` behaviour to a new central:

```text
build\
```

tree may be desirable later, but it changes `OutDir`, `IntDir` and possibly test scripts.

Recommendation:

> first preserve behaviour; then clean build-output layout in a separate verified change.

### 6.5 Toolchain settings

The new plugin project will require build details distinct from the inspector:

```text
C++ rather than C
DynamicLibrary configuration
VapourSynth API4 include paths
plugin entry point / export settings
x64-only configurations
runtime library settings
language standard
warning settings
preprocessor definitions
possibly self-test project configuration
```

Do not derive these settings from memory if the working `vapoursynth-cnr3` repository can provide a proven local example.

### 6.6 Third-party header versioning

If VapourSynth API4 headers are copied into:

```text
third_party\vapoursynth\include
```

as in `vapoursynth-cnr3`, record their source/version.

The current CNR3 example includes:

```text
VapourSynth4.h
VERSION.txt
VSConstants4.h
VSHelper4.h
VSScript4.h
```

A future plugin should pin or otherwise document the header baseline used to build it.

### 6.7 Documentation authority

The repository will contain:

```text
ratified authority
research
reviews
handover documents
superseded material
```

Git tracking alone must not make all of these equally authoritative.

The existing explicit authority model must survive the reorganisation.

---

## 7. Existing `vapoursynth-cnr3` repository as a proven build reference

Dave has an existing working VapourSynth API4 DLL project at:

```text
E:\SOFTWARE-Win11\MULTIMEDIA\vapoursynth-cnr3\github
```

Reported root layout:

```text
.github
.gitignore
.vs
CHANGELOG.md
LICENSE
README.md
src
third_party
vs
```

This project can be used as a **local proven example**, especially for obscure Visual Studio and VapourSynth settings.

Important constraint:

> The file **contents have not yet been supplied to or inspected by ChatGPT in this repository discussion**.

Therefore the descriptions below distinguish known filenames from inferred likely roles.

Do not mechanically copy settings until the relevant files are inspected.

---

## 8. Candidate CNR3 files/material to inspect and possibly reuse

### 8.1 `vs\cnr3\cnr3.vcxproj`

**Known:** existing Visual Studio C++ project file for the successful CNR3 plugin.

**Likely useful for inspection/reuse:**

- x64 configuration;
- `DynamicLibrary` configuration;
- Visual Studio platform toolset;
- C++ language-standard setting;
- output DLL naming;
- `OutDir` / `IntDir`;
- warning / optimisation settings;
- runtime library;
- preprocessor definitions;
- VapourSynth include directory setup;
- any export or linker settings;
- references to `src`;
- Debug/Release differences.

**Reuse method proposed:**

Do not copy it wholesale.

Extract only the settings that are actually relevant to a new:

```text
VapourSynth-mpeg2Deblock.vcxproj
```

and then change:

```text
project GUID
project name
source files
output name
paths
preprocessor definitions
```

as required.

### 8.2 `vs\cnr3\cnr3.vcxproj.filters`

**Known:** Visual Studio Solution Explorer filter/group metadata.

**Likely useful for:**

- showing the file-grouping convention used in Dave's Visual Studio projects.

**Reuse value:** low to moderate.

It can be patterned after, but source filenames will necessarily differ.

### 8.3 `vs\cnr3\cnr3.vcxproj.user`

**Known:** Visual Studio per-user project settings file.

**Likely nature:** machine/user-specific debugger or environment state.

**Recommendation:**

Inspect, but normally do **not** use this as a project template unless it contains a deliberate local run/debug setting Dave wants reproduced.

Also determine whether `.vcxproj.user` is intentionally tracked in CNR3 or merely present locally.

### 8.4 `vs\cnr3\cnr3.slnx`

**Known:** solution file used by the CNR3 Visual Studio setup.

**Likely useful for:**

- current Visual Studio solution format;
- how one or more projects are referenced;
- relative project paths.

**Potential reuse:**

Use as a structural example for the new umbrella solution if Dave prefers `.slnx`.

Do not assume the MPEG-2 repository should use `.slnx` rather than `.sln` until the current VS2026 workflow and migration cost are considered.

### 8.5 `vs\cnr3\cnr3_cache_core_selftest.vcxproj`

**Known:** separate CNR3 self-test Visual Studio project.

**Likely useful for:**

- pattern for a non-DLL test executable living beside a DLL project;
- shared source/include references;
- x64 Release/Debug test configuration;
- independent test target.

This may become relevant later if the MPEG-2 plugin acquires C++ unit/self-test targets.

It is probably **not required for the initial repository migration or Stage 2 Python work**.

### 8.6 `third_party\vapoursynth\include\*`

Known files:

```text
VapourSynth4.h
VERSION.txt
VSConstants4.h
VSHelper4.h
VSScript4.h
```

**Likely useful for:**

- establishing the API4 header set used by a known-working plugin;
- providing a reproducible local include baseline.

Before reuse, inspect:

```text
VERSION.txt
header provenance
licence/notices
current plugin include usage
```

### 8.7 `src\vapoursynth-Cnr3.cpp`

**Known by filename:** likely the primary plugin-facing translation unit.

**Possible useful things to inspect:**

- VapourSynth plugin initialization/registration pattern;
- API4 function signatures;
- include order;
- namespace / exported entry point pattern;
- how instance creation and callbacks are wired.

Do not copy algorithm content.

Reuse only the generic API4/plugin-registration pattern if it is current and appropriate.

### 8.8 `src\cnr3_arInitial.cpp` and `src\cnr3_arAllFramesReady.cpp`

**Known by filename:** callback-specific source units.

**Likely useful for:**

- project organisation;
- API4 callback function declaration style;
- separation of `arInitial` and `arAllFramesReady`;
- source-request / output-frame lifecycle pattern.

The MPEG-2 filter's actual scheduling/state model must still follow its own design.

### 8.9 `src\cnr3_build_config.h`

**Known by filename:** build configuration header.

**Potential reuse:**

- pattern for compile-time feature/configuration definitions;
- version/build identifiers;
- diagnostic feature gates.

Do not assume its macros apply to the MPEG-2 project.

### 8.10 `src\cnr3_common.h` and `src\cnr3_plugin_internal.h`

**Known by filename:** shared/internal headers.

**Potential reuse:**

- source organisation convention;
- central internal plugin declarations;
- API include conventions;
- portability/compiler macros if present.

Exact value requires content inspection.

### 8.11 CNR3 diagnostics and self-test files

Examples reported:

```text
cnr3_diagnostics.*
cnr3_memory_diagnostics.*
cnr3_cache_diagnostics.*
cnr3_cache_core_selftest.*
```

**Potential reuse:** not algorithmically.

They may be useful as examples of:

- diagnostic compile gates;
- self-test target organisation;
- logging/assertion conventions;
- keeping test code out of the production DLL path.

These should be considered only later if the new project needs comparable infrastructure.

### 8.12 `.github`

**Known:** directory exists.

**Unknown:** exact contents.

Inspect later for:

- workflows;
- issue/release metadata;
- build automation;
- other repository-specific GitHub configuration.

Do not copy workflows without checking paths/toolchain assumptions.

### 8.13 `.gitignore`

The CNR3 `.gitignore` is particularly valuable to compare with the current inspector `.gitignore`.

Audit whether it successfully excludes:

```text
.vs
x64
intermediate files
generated databases
*.user
other Visual Studio local state
```

while retaining intended project metadata.

Do not blindly replace the inspector `.gitignore`; merge deliberately.

---

## 9. Proposed end-state tree

ChatGPT proposes refining the earlier tree using the successful CNR3 separation between source and Visual Studio build metadata.

Candidate:

```text
VapourSynth-mpeg2Deblock\
|
+-- .github\
+-- .gitignore
+-- LICENSE
+-- README.md
|
+-- docs\
|   +-- REPOSITORY\
|   +-- HANDOVER\
|   +-- REVIEW\
|   +-- RESEARCH\
|   +-- SUPERSEDED\
|
+-- src\
|   +-- Mpeg2BlockInspector\
|   |   +-- *.c
|   |   +-- *.h
|   |   +-- patches\
|   |
|   +-- VapourSynth-mpeg2Deblock\
|       +-- *.cpp
|       +-- *.h
|
+-- tools\
|   +-- Stage1_Inspector_Analyzer_v0_2.py
|
+-- experiments\
|   +-- stage2\
|       +-- ... Stage 2 Python/reference implementation ...
|
+-- TESTING\
|   +-- inspector\
|   +-- stage2\
|   +-- plugin\
|
+-- third_party\
|   +-- vapoursynth\
|       +-- include\
|           +-- VapourSynth4.h
|           +-- VSConstants4.h
|           +-- VSHelper4.h
|           +-- VSScript4.h
|           +-- VERSION.txt
|
+-- vs\
    +-- VapourSynth-mpeg2Deblock\
        +-- VapourSynth-mpeg2Deblock.slnx   [or .sln; decide]
        +-- Mpeg2BlockInspector.vcxproj
        +-- Mpeg2BlockInspector.vcxproj.filters
        +-- VapourSynth-mpeg2Deblock.vcxproj
        +-- VapourSynth-mpeg2Deblock.vcxproj.filters
```

### 9.1 Why put Visual Studio metadata under `vs`

This is a proposed refinement based on the successful CNR3 repository layout.

Advantages:

- source remains source;
- Visual Studio project/solution metadata is grouped separately;
- one umbrella solution can reference both projects;
- avoids putting `.vcxproj` files inside component source directories;
- closely resembles a Dave-maintained project known to work with a VapourSynth API4 DLL.

This is not yet decided.

Claude should specifically compare this to the earlier proposal where each `.vcxproj` sits inside its component's `src` directory and recommend which is simpler/safer for this repository.

### 9.2 `VHSC_samples`

Not shown in the proposed tree deliberately.

Its final location depends on the media audit.

Possible outcomes:

```text
local only / gitignored
small redistributable fixtures under TESTING\fixtures
hash/manifests only in Git
```

---

## 10. Proposed migration strategy

The migration should be **checkpointed**.

Do not perform repository rename, local move, source re-layout and project recreation as one opaque operation.

### M0 - freeze current known-good state

Before changing structure:

1. Ensure all current ratified repository/design documents are committed and pushed.
2. Ensure `git status` is clean.
3. Build current `Mpeg2BlockInspector` x64 Release successfully.
4. Run the current known-good inspector/analyzer acceptance path.
5. Record current commit hash.
6. Create a pre-migration Git tag.

Suggested semantic tag concept:

```text
pre-vapoursynth-mpeg2deblock-restructure
```

Exact tag name remains Dave's decision.

### M1 - audit the existing repository before rename

Inspect:

```text
.gitignore
root Mpeg2BlockInspector.vcxproj
src\Mpeg2BlockInspector.sln
src\Mpeg2BlockInspector.vcxproj
src\Mpeg2BlockInspector.vcxproj.filters
src\Mpeg2BlockInspector.vcxproj.user
tracked-file list
TESTING scripts
VHSC_samples
```

Search tracked text for:

```text
Mpeg2BlockInspector
E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector
$(SolutionDir)
$(ProjectDir)
OutDir
IntDir
x64
hard-coded EXE paths
relative source paths
```

Output of M1:

> a migration inventory identifying every path/name dependency that must change.

### M2 - audit the CNR3 build reference

Inspect only the files needed to establish a proven plugin/project template:

```text
vs\cnr3\cnr3.vcxproj
vs\cnr3\cnr3.vcxproj.filters
vs\cnr3\cnr3.slnx
vs\cnr3\cnr3_cache_core_selftest.vcxproj    [reference only]
third_party\vapoursynth\include\VERSION.txt
src\vapoursynth-Cnr3.cpp
src\cnr3_build_config.h
src\cnr3_common.h
src\cnr3_plugin_internal.h
.gitignore
.github\...                                  [if later relevant]
```

Produce:

- settings to reuse;
- settings to change;
- settings not applicable.

Do not copy application logic.

### M3 - rename GitHub repository

If M0-M2 reveal no blocker:

```text
Mpeg2BlockInspector
    ->
VapourSynth-mpeg2Deblock
```

Preserve existing Git history.

Do not immediately delete the old local working tree.

### M4 - fresh clone into the new local hierarchy

Proposed:

```text
E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\
    VapourSynth-mpeg2Deblock\
```

Validate:

```text
same expected commit
clean status
origin points to renamed repository
current inspector builds unchanged
current acceptance still passes
```

This separates:

```text
repository rename/path relocation
```

from:

```text
source/project restructure
```

### M5 - create a bounded restructure branch

Keep `main` at the verified post-clone state.

Create one short-lived branch solely for repository layout migration.

No Stage 2 algorithm code belongs in this branch.

### M6 - move existing inspector source as a component

Move genuine inspector source to:

```text
src\Mpeg2BlockInspector\
```

using Git-aware moves.

Move:

```text
.c
.h
patches
```

Do **not** carry generated/intermediate directories merely to preserve old shape.

Update the live inspector `.vcxproj` references accordingly.

Build and test before further restructuring.

### M7 - establish umbrella Visual Studio structure

Candidate:

```text
vs\VapourSynth-mpeg2Deblock\
```

Create/update the umbrella solution and point it at:

```text
Mpeg2BlockInspector
future VapourSynth-mpeg2Deblock
```

At first, only the inspector needs to exist and build.

This allows the Visual Studio structure itself to be verified before a new DLL project is added.

### M8 - separate tool / experiment material

Move:

```text
Stage1_Inspector_Analyzer_v0_2.py
```

from mixed inspector C source into the chosen `tools` location, updating tests/documentation.

Create:

```text
experiments\stage2\
```

for future S2-I1+ Python/reference work.

No Stage 2 code is written merely to perform this move.

### M9 - add VapourSynth API4 build skeleton later

Only after the repository restructure is stable:

- create the new plugin project;
- derive proven Visual Studio/VapourSynth settings from inspected CNR3 files;
- add pinned/documented API4 headers if that remains the chosen pattern.

This is not S2-I1 and need not occur before Stage 2 Python work unless there is a separate reason.

### M10 - merge after migration acceptance

Before merging the restructure branch:

```text
inspector builds x64
known inspector acceptance passes
analyzer works from new location
testing scripts work
documentation paths updated
no unintended generated files tracked
no sample-media policy violation introduced
```

Then merge and tag the new structural baseline.

---

## 11. Why a fresh clone is preferred over moving the old working directory

Dave proposed:

1. rename GitHub repository;
2. create the new parent folder;
3. clone the renamed repository into the new location.

ChatGPT supports this approach.

Advantages:

- the old local repository remains untouched during migration;
- proves that a clean clone contains everything actually needed;
- exposes accidentally untracked local dependencies;
- generates fresh `.vs` local state;
- separates remote/path changes from later source-tree changes;
- provides an immediate comparison source if something behaves differently.

If the clean clone does **not** build before restructuring, that is valuable evidence that the current repository depends on untracked/local state.

Fix that first.

---

## 12. Things not to combine into the first migration

Avoid simultaneously changing:

```text
source layout
output-directory architecture
compiler warning policy
runtime library policy
C/C++ language level
plugin project
Stage 2 algorithm code
test framework
GitHub Actions
release packaging
```

The migration should answer one question at a time.

First:

> can the existing inspector survive the umbrella-repository rename and clean component layout?

Then add new capability.

---

## 13. Suggested acceptance gates

### Gate A - pre-migration baseline

PASS if:

```text
clean Git state
pushed commit
tagged checkpoint
current x64 Release build passes
known inspector/analyzer test passes
```

### Gate B - renamed GitHub + fresh clone

PASS if:

```text
fresh clone
correct origin
same expected history
no required local file missing
existing inspector builds/tests without source restructure
```

### Gate C - inspector component move

PASS if:

```text
all source/project references repaired
x64 build passes
acceptance passes
TESTING paths work
```

### Gate D - umbrella solution

PASS if:

```text
solution opens cleanly in VS2026
inspector project builds from solution
no obsolete duplicate project is accidentally used
```

### Gate E - final restructure baseline

PASS if:

```text
clean repository tree
generated files ignored as intended
documentation paths consistent
sample policy decided
migration committed
migration tag created
```

Only after Gate E should normal development resume from the new structure.

---

## 14. Questions for Claude review

Please review this proposal as an independent designer and identify:

```text
MUST CHANGE
SHOULD CHANGE
OPTIONAL
NO OBJECTION
```

### Q1 - one repository

Do you agree that the indexer, Stage 2 experiment, eventual `.idx2` specification and production VapourSynth plugin should remain in one Git repository for now?

If not, what concrete coupling or release problem makes separate repositories safer?

### Q2 - umbrella name

Any objection to:

```text
VapourSynth-mpeg2Deblock
```

as the umbrella repository name while retaining:

```text
Mpeg2BlockInspector
```

as the existing command-line component/project name?

### Q3 - migration method

Is:

```text
current clean/tagged repository
    ->
rename GitHub repository
    ->
fresh clone to new local path
    ->
verify old build unchanged
    ->
restructure on a branch
```

the safest method?

Is there a materially easier method that preserves rollback and history equally well?

### Q4 - Visual Studio organisation

Which is preferable:

**A. CNR3-like build metadata separation**

```text
src\Mpeg2BlockInspector\
src\VapourSynth-mpeg2Deblock\
vs\VapourSynth-mpeg2Deblock\*.vcxproj / solution
```

or:

**B. project files colocated with each component**

```text
src\Mpeg2BlockInspector\Mpeg2BlockInspector.vcxproj
src\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock.vcxproj
root solution
```

Please assess specifically for Visual Studio 2026 path maintenance and future multi-project use.

### Q5 - existing project files

Do you agree that the two existing `Mpeg2BlockInspector.vcxproj` files and the `.sln` must be inspected before deciding which is authoritative and what can be removed?

### Q6 - generated/local state

Any objection to treating:

```text
.vs
x64
Mpeg2Blo.F4B1A357
*.vcxproj.user
```

as candidates for generated/per-user state pending actual Git/project inspection, rather than preserving them automatically?

### Q7 - CNR3 reuse

Does the proposed CNR3 inspection set capture the useful reusable build/API4 knowledge without dragging CNR3 algorithm architecture into this project?

What other CNR3 files/settings should be inspected?

### Q8 - third-party VapourSynth headers

Would you reuse the successful CNR3 pattern:

```text
third_party\vapoursynth\include
```

with a recorded version, or recommend another dependency arrangement?

### Q9 - licence/provenance

Do you agree that the repository migration should include an explicit check of the reference-decoder source licence/provenance before presenting one umbrella repository-level licence?

### Q10 - samples

What repository policy would you recommend for:

```text
VHSC_samples
real LG recordings
derived indexes
logs
small synthetic fixtures
```

given a public GitHub repository?

### Q11 - build-output migration

Do you agree that reorganising `OutDir` / `IntDir` / `x64` should be deferred until after the source and solution migration is stable?

### Q12 - migration gates

Are Gates A-E sufficient to avoid a large undiagnosable migration failure?

### Q13 - easier alternative

Most importantly:

> Is there a simpler way to reach the same clean umbrella repository without risking the working inspector or losing useful Git/Visual Studio history?

If yes, please propose the simpler sequence explicitly.

---

## 15. Decisions requested from Dave only after review

No immediate decision is required beyond authorising discussion/review.

After Claude's review, Dave will need to decide:

1. one repository or more than one;
2. final umbrella repository name;
3. source/VS directory model;
4. GitHub rename/fresh-clone method;
5. CNR3-derived dependency/build conventions;
6. sample-media policy;
7. licence/provenance presentation;
8. migration start.

No structural repository changes should be performed before those decisions are settled.

---

## 16. Immediate next step

Give this proposal to Claude together with, ideally:

```text
current .gitignore
root Mpeg2BlockInspector.vcxproj
src\Mpeg2BlockInspector.sln
src\Mpeg2BlockInspector.vcxproj
src\Mpeg2BlockInspector.vcxproj.filters
```

For the CNR3 reference, provide or make available:

```text
vapoursynth-cnr3\.gitignore
vapoursynth-cnr3\vs\cnr3\cnr3.vcxproj
vapoursynth-cnr3\vs\cnr3\cnr3.vcxproj.filters
vapoursynth-cnr3\vs\cnr3\cnr3.slnx
vapoursynth-cnr3\third_party\vapoursynth\include\VERSION.txt
vapoursynth-cnr3\src\vapoursynth-Cnr3.cpp
```

Those contents would allow the next review to move from directory-name inference to exact migration advice.

---

## 17. Change log

### v0.1 - 2026-10-08

- Initial repository/GitHub migration proposal.
- Records Dave's selected umbrella name `VapourSynth-mpeg2Deblock`.
- Records current local/GitHub repository state.
- Identifies Visual Studio/path/layout risks raised by Dave.
- Adds licensing, sample-media, Git-history, third-party-header and build-output risks.
- Proposes a multi-component source tree and CNR3-like `vs` build-metadata layout for review.
- Identifies candidate CNR3 files/settings to inspect and possible reuse, with explicit distinction between known filenames and uninspected content.
- Defines migration stages M0-M10 and acceptance Gates A-E.
- Requests Claude review, including whether a materially simpler approach exists.
