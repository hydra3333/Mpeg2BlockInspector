# Migration / Visual Studio Design Record - D-C Intent, CNR3 Configuration Transfer and Developer Handback

**Filename:** `Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_11.md`  
**Version:** 0.11  
**Date:** 2026-10-09  
**Drafted by:** migration ChatGPT chat  
**Cold-review status:** prior design stages/reviews were cold-reviewed by migration Claude; this v0.11 candidate still requires Claude cold review  
**Ratification status:** Dave has ratified the policy decisions carried here; this v0.11 document is not final until the current review cycle closes  
**Status:** Current migration-design candidate after Dave ratification of the AVX2 minimum-target, security-hardening, project-file source-of-truth and documentation-handback policies; requires Claude cold review before the superseding A3 candidate is applied.  
**Supersedes:** `Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_10.md`  
**Scope:** Repository migration, Visual Studio 2026 solution/project normalization, standalone Release artifact configuration, build harness, release workflow, wheel/PyPI packaging scaffold, validation, and handback to the technical-development chats.  
**Does not authorize:** Stage 2 algorithm implementation or MPEG-2 deblocking implementation.

---

## 1. Purpose

This document records the current migration end-state and method after:

- repository rename and restructure;
- first post-restructure validation;
- Dave's decision to remove Win32/x86 completely;
- Dave's decision that the `Mpeg2BlockInspector` project configuration is in scope for improvement while its source remains frozen;
- the decision to use CNR3's command-line/self-test project as the primary proven reference for the inspector;
- the decision to create a buildable VapourSynth MPEG-2 deblocker DLL placeholder before returning to technical development;
- adoption of a subtractive / exclusion-first CNR3 settings audit, cross-checked by an independent target-requirements audit;
- Claude's reviews of the Stage A/B plan and the v0.5 design record / v0.1 common handback;
- confirmation of Dave's installed Windows SDKs;
- confirmation that no per-user x64 MSBuild property sheet exists;
- recovery of proven Visual Studio 2026 environment and MSBuild-discovery patterns;
- Dave's decision not to pin a Windows SDK version;
- Dave's clarification that Deblock4 is historical/reference material only and may be recycled where appropriate, but is not an active project or required current migration input;
- adoption of one common Developer Handback for both technical-development chats;
- Dave's requirement that the Release `Mpeg2BlockInspector.exe` and Release `mpeg2Deblock.dll` be standalone distribution artifacts that do not require a separately installed Microsoft Visual C++ Redistributable;
- Dave's requirement that the Visual Studio project files themselves carry the standalone linkage settings: CI/build scripts may invoke the projects but must not repair or override their runtime-linkage policy;
- Dave's ratified D4 decision to accept attribution risk and consolidate the inspector Release `/MT` standalone-runtime change into A3; there is no A4 stage;
- Dave's stated eventual PyPI installation/distribution objective;
- Claude's finding that the current CNR3 release workflow uses a duplicate hand-written `cl` flag map and already constructs a Windows wheel;
- the resulting one-build-route policy: the final GitHub release workflow must invoke the same Stage C MSBuild/`.slnx` harness used by the local gates, with project XML as the source of build settings;
- Dave's ratified D5 decision that the future plugin DLL also uses `/MT`, with the hybrid static-VC-runtime/Windows-UCRT model documented only as a fallback;
- Dave's ratified D6 decision that Release artifacts embed only the PDB file name using `/PDBALTPATH:%_PDB%`.
- Dave's product policy that x64 + AVX2 is the minimum supported CPU target for both `Mpeg2BlockInspector` and `mpeg2Deblock`; supporting pre-AVX2 CPUs is not a project objective.
- Dave's policy that performance must not be obtained by globally disabling security mitigations: CFG, CET shadow-stack compatibility, Spectre mitigation and `/GS` are enabled in the accepted project settings, subject to toolchain/component availability being made an explicit build prerequisite rather than silently disabling protection.
- Dave's inspector-specific `/sdl` exception: `/sdl` remains OFF for the frozen MPEG-2 reference-decoder-derived inspector source, while new `mpeg2Deblock` code uses `/sdl` ON.
- Dave's requirement that the same AVX2/security/runtime policy be encoded in the Visual Studio project files and verified by the canonical build harness and final GitHub release workflow; CI may not inject a divergent flag set.
- Dave's direction that the migration close-out handback and future-ChatGPT handover explicitly reference the updated repository `README.md` and `NOTICE.md`, with `NOTICE.md` remaining the legal/attribution boundary and the README remaining the public product/build summary.
- the documentation-consistency rule that README claims about AVX2, standalone Release artifacts and Spectre-enabled builds must be verified against accepted project/build evidence before final handback; documentation is not a substitute for the A3/Stage B gates.

---

## 2. Current published repository checkpoint

GitHub repository:

```text
https://github.com/hydra3333/VapourSynth-mpeg2Deblock
```

Active local repository:

```text
E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock
```

Retained rollback/reference repository:

```text
E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector
```

Published post-restructure HEAD:

```text
a9c782acb525943881e65b2b3f8f0484521a01c5
```

Published lightweight tag:

```text
vapoursynth-mpeg2deblock-post-restructure
```

The old tree is retained as rollback/reference material. It is not the active build/test tree.

---

## 3. What the earlier restructure established

Current repository layout includes:

```text
src\Mpeg2BlockInspector\
tools\
TESTING\
VHSC_samples\
docs\
vs\VapourSynth-mpeg2Deblock\
```

The inspector remains named:

```text
Mpeg2BlockInspector
```

The umbrella repository/product identity is:

```text
VapourSynth-mpeg2Deblock
```

The first post-move Visual Studio Release x64 rebuild passed:

```text
1 succeeded
0 failed
```

and reproduced the known 17 warning instances.

Two representative functional migration runs produced byte-identical indexes and demonstrated that tools, VPY files, source media and the rebuilt executable were being used from the new repository tree.

Dave waived the remaining planned runs for that earlier path/restructure gate.

That waiver does not apply to the forthcoming build-definition changes.

---

## 4. Revised Visual Studio end-state

The intended end-state is:

```text
Solution:
    VapourSynth-mpeg2Deblock.slnx

Platform:
    x64 only

Configurations:
    Debug
    Release

Projects:

    Mpeg2BlockInspector
        command-line Application / EXE
        C
        existing frozen inspector source

    mpeg2Deblock
        VapourSynth API4 Dynamic Library / DLL
        C++
        placeholder/build skeleton only at migration completion
```

Exact plugin/project capitalization and public plugin identity remain subject to the Stage B naming decision.

Both projects are to appear in one Visual Studio 2026 solution and remain independently selectable for Build, Rebuild, Clean and Properties.

For Release x64, the Visual Studio projects themselves are the source of truth for standalone distribution linkage. The intended distribution state is:

```text
Mpeg2BlockInspector.exe Release
    standalone with respect to the Microsoft VC/UCRT redistributable
    RuntimeLibrary = static release runtime (/MT)

mpeg2Deblock.dll Release
    standalone with respect to the Microsoft VC/UCRT redistributable
    static release runtime (/MT) is the current required direction
    no CRT-owned memory/object may cross the VapourSynth module boundary
```

The final build harness and GitHub release workflow must build these project definitions; they must not add `/MT` or otherwise maintain a second copy of compile/link settings.

The project-wide minimum CPU and security policy is:

```text
CPU target
    x64 only
    AVX2 minimum in Debug and Release for both projects
    pre-AVX2 CPUs are intentionally unsupported

Performance tuning
    Release optimized for speed
    /favor:blend explicitly recorded for broad AMD/Intel tuning
    security mitigations are not disabled merely for performance

Security hardening
    /GS ON
    Control Flow Guard ON at compile and link
    CET shadow-stack compatibility ON
    Spectre mitigation ON using the MSBuild Spectre setting and mitigated libraries

SDL
    Mpeg2BlockInspector: OFF only as a documented frozen/reference-decoder exception
    mpeg2Deblock: ON for new code
```

Microsoft documents `/arch:AVX2` as the minimum-CPU code-generation choice for AVX2, CFG as a compiler+linker mitigation, `/CETCOMPAT` as the x64 CET marker, and Spectre mitigation as requiring the corresponding mitigated runtime libraries. Those dependencies are build prerequisites; their absence must fail the gate rather than cause the projects or CI to disable the protection.

---

## 5. Important frozen/non-frozen distinction

The `Mpeg2BlockInspector` source is frozen.

The `Mpeg2BlockInspector` Visual Studio project configuration is not frozen.

The inspector `.vcxproj` is therefore a working starting point, not an untouchable authority.

Dave explicitly requires the command-line project configuration to be checked and corrected using the proven CNR3 command-line/self-test project as an important reference.

Any resulting build-definition change must pass the full regression gate defined below.

No frozen C source is to be changed merely to make a Visual Studio setting easier to enable.

---

# STAGE A - INSPECTOR AND UMBRELLA SOLUTION

## 6. Stage A goals

Stage A will:

1. remove Win32/x86 from the inspector project;
2. remove x86 from the solution;
3. retain Debug x64 and Release x64;
4. replace the old `.sln` with `VapourSynth-mpeg2Deblock.slnx`;
5. keep the actual command-line project named `Mpeg2BlockInspector`;
6. compare and normalize the command-line project configuration against the proven CNR3 console/self-test project;
7. preserve inspector functional output exactly through normalization;
8. measure and pin/compare non-command-line PE/load-config behaviour required by the no-defaults policy;
9. encode the ratified standalone Release linkage, AVX2 minimum target and security-hardening policy directly in the inspector project rather than hiding or repairing any of them in CI or packaging;
10. preserve the inspector's sole `/sdl` exception because the frozen source is derived from the MPEG-2 reference decoder.

---

## 7. Stage A comparison references

Primary CNR3 executable reference:

```text
cnr3_cache_core_selftest.vcxproj
```

Secondary comparison:

```text
cnr3.vcxproj
```

Solution reference:

```text
cnr3.slnx
```

Also inspect:

```text
*.vcxproj.filters
*.vcxproj.user
```

The CNR3 DLL project is included as a second settings column because settings common to both CNR3 projects may indicate deliberate Visual Studio conventions.

DLL-specific settings must not be transferred to the inspector merely because the CNR3 DLL uses them.

---

## 8. Dual-pass / subtractive audit method

The settings audit deliberately attacks the problem from both directions.

### Pass A - CNR3 retention/exclusion

For the relevant CNR3 project, presume every explicit setting may embody useful prior work.

A setting is removed or changed only when there is a stated reason such as:

```text
NOT APPLICABLE
CNR3-SPECIFIC
WRONG FOR THIS TARGET
SOURCE-CONSTRAINED
USER/MACHINE-LOCAL
SUPERSEDED
DELIBERATELY DIFFERENT
```

For Stage B this becomes stronger: start from a byte copy of the CNR3 DLL project and account for every changed/deleted line.

### Pass B - target requirements

Independently ask what the target project should contain.

This checks for:

- settings CNR3 leaves at Visual Studio defaults;
- settings embodied in workflow/build scripts instead of `.vcxproj`;
- source-level build dependencies;
- hidden environment/property-sheet dependencies;
- requirements specific to the MPEG-2 projects.

### Reconciliation

Any difference between Pass A and Pass B becomes an explicit review item.

The aim is that no CNR3 setting can disappear merely because nobody remembered to ask about it.

---

## 9. Required classification

Every relevant setting is to receive one of:

```text
REUSE UNCHANGED
REUSE WITH NAME/PATH ADJUSTMENT
NOT APPLICABLE TO THIS PROJECT
DELIBERATELY DIFFERENT
DEFAULT IN CNR3 - LEAVE AT DEFAULT
USER/MACHINE-LOCAL - RECORD BUT DO NOT COPY
PROVISIONAL - TECHNICAL DEVELOPMENT DECISION NOT YET FINAL
```

Every `DELIBERATELY DIFFERENT` entry requires a reason.

Every `PROVISIONAL` entry must be carried into the final Developer Handback so it is not mistaken for a ratified algorithm/design decision.

A script-generated inventory is REQUIRED for the explicit CNR3 project elements so every meaningful project line/property is accounted for. The audit table must account for every relevant item emitted by that inventory. This is the mechanical check that prevents an explicit CNR3 setting from being silently lost.

---

## 10. Known inspector-specific deviations

### SDL

Inspector:

```text
SDLCheck = false
```

This is a deliberate inspector-only exception. The frozen source is derived from the MPEG-2 reference decoder, and enabling `/sdl` turns legacy/reference-decoder diagnostics into build failures. The source will not be edited merely to enable SDL.

This exception must not propagate to new code: the future `mpeg2Deblock` project uses `/sdl` ON.

### CRT deprecation suppression

Retain:

```text
_CRT_SECURE_NO_WARNINGS
```

for the frozen classic C source.

### C++ settings

CNR3 C++ language-standard and C++-specific conformance choices are not automatically meaningful for the C inspector.

### VapourSynth dependencies

The inspector does not use VapourSynth and therefore does not inherit:

```text
VapourSynth include paths
CNR3_SELFTEST_CONSOLE
CNR3 plugin definitions
NOMINMAX solely because CNR3 uses it
```

unless another independent reason is identified.

### AVX2 / minimum CPU target

Ratified project-wide CPU policy:

```text
x64 + AVX2 minimum
/arch:AVX2
```

This applies to Debug and Release for both `Mpeg2BlockInspector` and the future `mpeg2Deblock` project. Supporting pre-AVX2 CPUs is intentionally out of scope. The earlier inspector-only AVX2-OFF policy is superseded.

Release builds also explicitly retain `/favor:blend` as the broad AMD/Intel microarchitecture tuning policy. Microsoft documents `/favor:blend` as the cross-vendor tuning default; it is recorded explicitly so the intended performance target does not depend on a mutable compiler default.

### Security hardening

The project does not trade security protections away merely for speed. The intended accepted project settings are:

```text
BufferSecurityCheck = true            -> /GS
Control Flow Guard = enabled          -> /guard:cf at compile and link
CET shadow-stack compatible = enabled -> /CETCOMPAT
Spectre mitigation = enabled          -> /Qspectre plus mitigated runtime libraries
```

The Stage A inspector and Stage B plugin gates must verify the effective command lines and PE/load-config state. Missing Spectre-mitigated libraries are an environment/toolchain prerequisite failure, not grounds to silently disable Spectre mitigation.

The only security-related compiler-policy exception currently ratified is inspector `/sdl` OFF for the frozen reference-decoder-derived source. New plugin code uses `/sdl` ON.

---

## 11. Win32/x86 removal

Dave has explicitly decided to remove Win32/x86.

This is to be a separate, reviewable change.

For `Mpeg2BlockInspector.vcxproj`, remove only the Win32 configuration material.

Do not remove:

```xml
<Keyword>Win32Proj</Keyword>
```

because `Win32Proj` is the Visual Studio native C/C++ project keyword, not a declaration that the target platform must be Win32.

Retain the current `ProjectGuid`.

The Win32-removal edit should be mechanically deletions-only, with x64 material byte-identical before and after.

---

## 12. `.sln` to `.slnx`

The old:

```text
Mpeg2BlockInspector.sln
```

will be removed when the new:

```text
VapourSynth-mpeg2Deblock.slnx
```

is added.

The solution will initially contain the inspector during Stage A and will gain the plugin placeholder in Stage B.

The solution exposes x64 only.

No duplicate old/new solution files should remain in the final tree.

---

## 13. Machine-state findings established

Dave checked for:

```text
%LOCALAPPDATA%\Microsoft\MSBuild\v4.0\Microsoft.Cpp.x64.user.props
```

Result:

```text
NO x64 user property sheet found
```

Therefore no such per-user x64 property sheet is presently supplying hidden settings to the inspector.

Installed Windows SDK include versions are:

```text
10.0.22621.0
10.0.26100.0
10.0.28000.0
```

CNR3 currently pins `10.0.28000.0`, but Dave has now ratified a different policy for this project:

```text
DO NOT PIN A SPECIFIC WINDOWS SDK VERSION
```

The build should use the appropriate currently installed SDK selected by the Visual Studio/MSBuild environment, and the build log must record the actual SDK/toolchain used.

This is an explicit, documented deviation from the current CNR3 project configuration.

---

## 14. Toolset and version policy

### Platform toolset

Keep the explicit Visual Studio 2026 platform toolset:

```text
v145
```

Changing the major toolset is a deliberate compiler upgrade and therefore remains an explicit project decision.

### Windows SDK

Do not pin a specific SDK version.

Every controlled build log should record which Windows SDK was actually used.

### Release runtime / standalone distribution policy

The Release x64 project files, not CI command-line overrides, define the runtime linkage used by shipped artifacts.

Dave ratified D4 = NO: there is no separate A4. The inspector A3 project-file change itself must set:

```text
Release RuntimeLibrary = MultiThreaded (/MT)
Debug RuntimeLibrary   = MultiThreadedDebugDLL (/MDd)
```

The resulting Release `Mpeg2BlockInspector.exe` must not require a separately installed Microsoft Visual C++ Redistributable. The Stage A gate enforces this by inspecting the built PE/imports rather than trusting the project setting alone.

The future `mpeg2Deblock.vcxproj` must likewise carry Release `/MT` from its first accepted Stage B build. Dave ratified D5 = YES; the hybrid static-VC-runtime/Windows-UCRT model is retained only as a documented fallback if Stage B uncovers a concrete technical problem.

Because `/MT` statically incorporates the selected SDK's UCRT implementation, the deliberately unpinned Windows SDK becomes shipped-artifact provenance. Every controlled Release build must record the actual SDK used.

Dave also ratified D6 = YES: shipped Release artifacts embed only the PDB file name, using:

```text
/PDBALTPATH:%_PDB%
```

through project-file linker settings/AdditionalOptions unless a current supported dedicated property is established. CI may not inject this separately.

### VapourSynth headers

The plugin project will keep the vendored VapourSynth header release identity in one file:

```text
third_party\vapoursynth\include\VERSION.txt
```

Other documents should refer to that file rather than repeatedly hard-coding a release number that will eventually age.

### Documentation versions

Stable authority-document names/locations should be used where possible.

The final common handback may record versions as "current at handback", but should avoid unnecessary version duplication throughout the prose.

Frozen/version-bearing tool identities such as `Stage1_Inspector_Analyzer_v0_2.py` remain exact.

---

## 15. Stage A commit sequence

Preferred sequence:

### A-1 - remove Win32 configurations

Remove Win32 project configurations only.

Expected character:

```text
deletions only
```

Retain `Win32Proj` and the existing project GUID.

### A-2 - replace `.sln` with `.slnx`

Remove:

```text
Mpeg2BlockInspector.sln
```

and add:

```text
VapourSynth-mpeg2Deblock.slnx
```

### A-3 - apply reviewed settings normalization and standalone Release linkage

A3 is the single reviewed Stage A project-settings change after A1/A2.

It includes:

```text
explicit pins derived from the pre-A3 checkpoint
Claude M3/S7-S11 corrections
ratified D1-D3
PreferredToolArchitecture=x64
Release RuntimeLibrary=/MT   (D4 = NO: consolidated into A3)
Release /PDBALTPATH:%_PDB%   (D6 = YES)
/arch:AVX2 Debug+Release
/favor:blend Release
/GS enabled
CFG enabled at compile+link
/CETCOMPAT enabled
Spectre mitigation enabled with mitigated libraries
inspector /sdl remains OFF only as the frozen-reference-decoder exception
```

There is no A4.

The `/MT` and PDB-path choices MUST be present in `Mpeg2BlockInspector.vcxproj`. The local harness and final GitHub workflow are forbidden from injecting them as corrective overrides.

If the post-A3 six-index gate fails, do not loosen the gate and do not silently abandon the AVX2/security policy. Diagnose with local, uncommitted variants to isolate causation, beginning with the settings most capable of altering generated code/output:

1. temporarily restore the pre-A3 ISA floor (`/arch:SSE2`) while leaving the ratified AVX2 policy unchanged on paper;
2. if required, restore Release `/MD`;
3. then remove `/GL` and `/LTCG`;
4. then restore `PreferredToolArchitecture=x86`;
5. security switches may be toggled only as diagnostic experiments if the earlier variants do not isolate the failure; they are not to be accepted OFF merely to make the gate pass.

Return the attribution evidence to Claude and Dave before changing the accepted design.

Do not combine unrelated project-setting changes into A1 or A2.

Named Git staging is required. Do not use `git add -A`.

---

## 16. Stage A validation gate

If compiler/linker/build settings change, Stage A must pass all of the following.

### Build

Rebuild:

```text
Debug | x64
Release | x64
```

### Warnings

Compare warnings by:

```text
warning code
file
line
```

Do not merely compare the warning count.

Any new warning must be examined and explained.

### Frozen source hashes

Frozen inspector-source hashes must remain unchanged.

### Functional regression

Run all six tracked index cases after the consolidated A3.

All six regenerated `.idx` files must be byte-identical to their established baselines.

Mandatory LP SHA-256:

```text
849b6a9c411a7db837268af3ac54501a06f5f1158e68d5245ce2b3ec40a0d011
```

This also closes the previously deferred requirement to run the LP `_2` test before Stage 2 depends on that clip.

### PE / load-config / import gate

The checkpoint Debug and Release executables establish the M3 baseline. For behaviour not fully visible in CL/LINK command lines, use `dumpbin /headers /loadconfig /imports /dependents`.

A3 must preserve the baseline PE/load-config properties below unless a ratified change says otherwise:

```text
x64 PE32+
Large Address Aware
High Entropy VA
Dynamic Base
NX Compatible
manifest generation
Debug linker /OPT behaviour
debug-information mode
```

A3 deliberately changes the security state from the checkpoint baseline:

```text
CET-compatible image flag: OFF -> ON
full CFG image state: OFF -> ON
Spectre mitigation: OFF -> ON in the project/compiler policy
/GS: explicitly ON
```

The post-A3 dumpbin gate must therefore require CET compatibility and a fully CFG-enabled image (including the expected Guard/FID-table evidence), while the exact CL/LINK logs must show the Spectre and `/GS` settings. The corresponding Spectre-mitigated libraries are required build components.

The post-A3 CL and LINK executable paths must show `HostX64\x64`, proving `PreferredToolArchitecture=x64` took effect.

Because consolidated A3 changes Release `/MD -> /MT`, the Release import gate intentionally changes. The post-A3 Release artifact must contain no dependency whose DLL name matches:

```text
VCRUNTIME*
MSVCP*
api-ms-win-crt-*
ucrtbase*
CONCRT*
VCOMP*
MSVCR1*
```

Do not use a broad `MSVCR*` prohibition because that would also match the Windows system `msvcrt.dll`.

The allowed Release dependency-DLL list is the measured checkpoint Release list after removing dynamic C-runtime dependencies. On the current checkpoint that leaves:

```text
KERNEL32.dll
```

Any additional DLL name stops the gate for review. Function-level KERNEL32 imports may grow because the statically linked runtime itself uses Windows APIs.

Debug remains `/MDd`; its dependency DLL-name set is compared against the Debug checkpoint at the DLL-name level, allowing only explained function-level changes.

### Visual Studio rewrite check

After opening/building the `.slnx`:

```text
git status --short
```

must show no unexpected Visual Studio rewrite of tracked project/solution files.

Also inspect:

```text
git status --short --ignored
```

to confirm generated Visual Studio state remains under already ignored output/cache areas.

---

# STAGE B - VAPOURSYNTH DLL PLACEHOLDER

## 17. Stage B purpose

Stage B creates the final project/build-system position for the future MPEG-2 deblocker.

It does not implement the deblocking algorithm.

The Stage B project must itself encode the standalone Release distribution policy. The Release DLL may not rely on a CI-only runtime-linkage override. Package identity decisions that couple the DLL name, VapourSynth autoload folder and eventual wheel name must be reviewed together before Stage B names are ratified.

Expected conceptual layout:

```text
src\
    Mpeg2BlockInspector\
    mpeg2Deblock\

vs\
    VapourSynth-mpeg2Deblock\
        VapourSynth-mpeg2Deblock.slnx
        Mpeg2BlockInspector.vcxproj
        Mpeg2BlockInspector.vcxproj.filters
        mpeg2Deblock.vcxproj
        mpeg2Deblock.vcxproj.filters
```

Names remain subject to the naming decision.

---

## 18. Stage B primary method

Start from the latest current CNR3 DLL `.vcxproj` and `.filters` as the proven baseline.

The default for an explicit CNR3 setting is:

```text
KEEP
```

unless there is a documented reason to change it.

The final diff from CNR3 to the new MPEG-2 DLL project is itself part of the audit evidence.

Every changed/deleted line should be attributable to:

```text
identity/name change
source-list change
path adjustment
known CNR3-specific item
Dave-ratified technical difference
```

The independent settings checklist remains a cross-check.

The CNR3 DLL project remains a settings reference, not an authority that can override this project's distribution requirement. In particular, the new `mpeg2Deblock.vcxproj` must carry its Release standalone-runtime choice explicitly; the final workflow must not substitute a different runtime model on the command line.

The DLL project must also carry the project-wide CPU/security policy directly in its own settings: `/arch:AVX2`, `/GS`, CFG, CET and Spectre mitigation enabled, with `/sdl` ON for the new C++ source. These are not CI-only switches.

---

## 19. Stage B decisions that must not happen accidentally

Before the DLL project files are finalized, explicitly review:

```text
project name
DLL filename
source-folder name
VapourSynth identifier
VapourSynth namespace
display name
C++ language standard
VapourSynth header release
API minor/profile selection
AVX2 implementation details beyond the already-ratified `/arch:AVX2` minimum target
floating-point mode
COMDAT folding
Release runtime model / standalone linkage
Release PDB alternate-path policy (`/PDBALTPATH:%_PDB%`)
wheel/package name
VapourSynth wheel plugin-folder name
DLL distribution filename
licence/NOTICE packaging obligations
```

Windows SDK policy is already ratified:

```text
do not pin a specific SDK version
```

Where Dave does not yet want to settle a technical-development decision, the project configuration and handback must mark it:

```text
PROVISIONAL
```

rather than presenting it as a considered algorithm/design choice.

---

## 20. Placeholder source policy

Preferred placeholder form:

```text
entry point only
```

That means:

- include the relevant VapourSynth API4 header;
- export `VapourSynthPluginInit2`;
- call `configPlugin`;
- register no filter functions.

This proves:

- include-path correctness;
- API header use;
- export configuration;
- DLL linking;
- basic VapourSynth loadability.

It does not implement:

```text
Deblock
frame processing
index reading
filter registration
algorithm behaviour
```

and therefore does not pre-empt Stage 2 technical development.

This preferred form still requires Dave to ratify plugin identity/namespace before finalization.

---

## 21. CNR3 evidence beyond the seven Visual Studio files

The Stage B audit must also inspect the latest current forms of relevant:

```text
CNR3 build scripts
CNR3 GitHub workflow
CNR3 handover/build-history documents
plugin source/header dependencies
third_party\vapoursynth\include\VERSION.txt
VapourSynth API headers
```

The purpose is to capture not just what CNR3 sets, but why settings were introduced.

Claude's 2026-10-09 review established two important current CNR3 workflow facts that must shape, but not be copied blindly into, this project:

```text
CNR3 GitHub CI compiles through a hand-written cl/link flag map rather than the Visual Studio project.
CNR3 GitHub CI already assembles and validates a Windows wheel.
```

For this project the first pattern is rejected: maintaining a second command-line copy of project settings creates drift. The second pattern is useful evidence for the later wheel stage, subject to this project's identity and AGPL-3.0-or-later/LGPL/NOTICE obligations.

Deblock4 may be consulted only as historical/reference material when it contains a useful proven implementation pattern. It is not an active project, it is not authoritative for this project, and its old scripts are not assumed current or superior to CNR3.

---

# STAGE C - CANONICAL BUILD HARNESS / VS2026 ENVIRONMENT

## 22. Visual Studio discovery policy

Historical CNR3/Deblock4 work proved that the x64 Visual Studio environment can be established through `VsDevCmd.bat`, but the final harness must not hard-code:

```text
Visual Studio major-version directory
Visual Studio edition
```

Discover the current Visual Studio installation with `vswhere.exe`.

The Visual Studio and MSBuild discoveries MUST use the same selection criteria so they select the same current installation and remain compatible with Community, Professional, Enterprise or Build Tools installations.

Current candidate pattern:

```bat
set "VSWHERE=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"

for /f "usebackq tokens=*" %%i in (`"%VSWHERE%" -latest -products * -requires Microsoft.Component.MSBuild Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath`) do set "VSINSTALL=%%i"

if not defined VSINSTALL goto :fail

set "VSDEVCMD=%VSINSTALL%\Common7\Tools\VsDevCmd.bat"

if not exist "%VSDEVCMD%" goto :fail

echo Using Visual Studio at: %VSINSTALL%
```

The exact command is to be verified on Dave's machine before the build harness is accepted.

---

## 23. When `VsDevCmd.bat` is required

MSBuild does not require the calling batch to manually configure the compiler environment when MSBuild itself is discovered and invoked correctly.

`VsDevCmd.bat` remains useful when Microsoft command-line tools such as:

```text
dumpbin
```

are used directly by the migration gate/build harness.

When `VsDevCmd.bat` is called:

1. capture its exit code immediately;
2. fail on non-zero;
3. restore the intended project directory afterwards;
4. verify required direct tools such as `dumpbin` with `where`.

A structured `:run` helper is preferred if the final current CNR3 build harness supports that style.

---

## 24. MSBuild discovery

Do not hard-code the MSBuild executable.

Use the same `vswhere.exe` product/component selection criteria used for the Visual Studio installation discovery:

```bat
for /f "usebackq tokens=*" %%i in (`"%VSWHERE%" -latest -products * -requires Microsoft.Component.MSBuild Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -find MSBuild\**\Bin\MSBuild.exe`) do set "MSBUILD=%%i"
```

The final harness must fail clearly if no MSBuild path is returned.

The selected `VSINSTALL` and `MSBUILD` paths must be printed in the log and checked during harness validation to confirm that both discoveries resolved to the same Visual Studio installation.

This candidate command is to be verified on Dave's machine before the build harness is accepted.

---

## 25. Solution-level build routine

A reusable solution-build routine is preferred.

It should accept at least:

```text
configuration
solution directory
solution filename
```

and build the complete umbrella solution with the x64 platform, for example:

```bat
"%MSBUILD%" <solution> /m /t:Clean;Build /p:Configuration=<Debug-or-Release> /p:Platform=x64
```

The harness must capture the exit code immediately and fail on any non-zero result.

This becomes particularly useful after Stage B, when the `.slnx` contains both projects.

---

## 26. Build-harness source policy

The primary current reference is the latest available proven CNR3 build plumbing.

Historical Deblock4 batch material may be reused only where it contains a useful safeguard or implementation pattern.

Rule:

```text
CURRENT CNR3 BUILD MATERIAL IS THE PRIMARY REFERENCE.

DEBLOCK4 IS HISTORY/REFERENCE ONLY.

OLDER SCRIPT VERSIONS ARE EVIDENCE ONLY UNLESS THEY CONTAIN
A USEFUL SAFEGUARD MISSING FROM THE CURRENT REFERENCE.
```

The final build harness should not be reconstructed solely from remembered or quoted historical fragments.

There must be exactly one authoritative build route for project settings:

```text
.vcxproj / .slnx = source of compile/link/runtime settings
Stage C harness = discovers tools and invokes MSBuild on the .slnx
Stage D GitHub workflow = invokes the same Stage C harness
```

Do not adopt CNR3's duplicated CI `cl` flag map. Do not override `PlatformToolset`, `/MT`, `/GL`, `/LTCG`, `/arch:AVX2`, `/favor:blend`, `/GS`, CFG, CET, Spectre, SDL policy or other ratified project settings from the harness/workflow. If the runner lacks required `v145` or the required Spectre-mitigated libraries, it must fail rather than silently substitute another toolset or disable security.

Each significant build step should:

- display what it is doing;
- capture the exit code immediately;
- stop on failure;
- log the actual tools/environment used.

---

## 27. Stage B build gate

The placeholder DLL must build under the agreed x64 configurations.

For the entry-point-only placeholder, validate at least:

```text
dumpbin /exports
```

and require:

```text
VapourSynthPluginInit2
```

to be exported.

A simple VapourSynth load smoke test may additionally verify that the plugin namespace exists while exposing no filter functions.

For the Release DLL, also run `dumpbin /dependents` plus the corresponding header/load-config checks and require the standalone-runtime and security policy. The accepted evidence must show AVX2 in the effective compiler command, `/GS`, CFG at compile+link, CET compatibility, Spectre mitigation using the mitigated libraries, and `/sdl` ON for the new plugin project. The DLL project itself must be configured to produce that result; passing only because a harness or workflow injects different flags is a failure.

---

## 28. Protecting the inspector during Stage B

Record SHA-256 hashes of the Stage A accepted:

```text
Mpeg2BlockInspector.vcxproj
Mpeg2BlockInspector.vcxproj.filters
```

After Stage B:

- if both remain byte-identical, one LP inspector smoke run is sufficient;
- if either differs, repeat all six inspector index regressions.

This replaces subjective judgement with a mechanical trigger.

---

# STAGE D - RELEASE-TRIGGERED GITHUB WORKFLOW

## 29. Stage D purpose and one-build-route rule

After Stage A, Stage B and the Stage C harness are stable, inspect and adapt the current CNR3 release-triggered workflow.

The adapted workflow must not compile through a second hand-maintained `cl` flag map. It must invoke the same Stage C harness, which discovers Visual Studio/MSBuild and builds `VapourSynth-mpeg2Deblock.slnx` Release x64.

The workflow must fail if the required `v145` toolset or Spectre-mitigated libraries are unavailable; it must not override `PlatformToolset` or weaken the CPU/security policy to suit the runner.

Any dated assumption about the GitHub-hosted Windows image or installed Visual Studio version must be re-verified at Stage D implementation time.

## 30. Stage D artifact checks

The release workflow must verify at least:

```text
Mpeg2BlockInspector.exe exists at the expected Release path
mpeg2Deblock.dll exists at the expected Release path
Release EXE standalone dependency policy PASS
Release DLL standalone dependency policy PASS
VapourSynthPluginInit2 exported
actual Visual Studio/MSBuild/toolset/SDK recorded
project-file runtime/PDB-path settings were not overridden by CI
Mpeg2BlockInspector effective compile uses /arch:AVX2
mpeg2Deblock effective compile uses /arch:AVX2
/GS present as required
CFG compile+link settings present and output verifies CFG
CET compatibility present in output
Spectre mitigation present and Spectre-mitigated libraries selected
inspector /sdl exception remains OFF
plugin /sdl remains ON
```

The standalone forbidden-DLL rule and CPU/security verification used locally must be the same rules used in CI. The workflow verifies these properties after invoking the Stage C harness; it does not create them by injecting replacement compiler/linker flags.

---

# STAGE E - WHEEL / PYPI PACKAGING SCAFFOLD

## 31. Stage E purpose

Dave has stated the eventual objective that the native artifacts be installable/distributable through PyPI. Migration does not authorize a production PyPI upload, but it must leave a credible, locally testable Windows x64 wheel route.

CNR3 already builds a `py3-none-win_amd64` wheel and is therefore a useful packaging reference. Reuse is subtractive: adapt the proven wheel mechanics while replacing CNR3 identity/licence/build-route assumptions.

## 32. Package identity and layout

Before Stage B names are finalized, review as one coupled identity set:

```text
PyPI/distribution name
Python package name
VapourSynth autoload folder vapoursynth/plugins/<name>/
DLL filename
plugin identifier / namespace / display name
EXE exposure/access strategy
```

Check PyPI name availability only when that identity decision is ready to be made.

## 33. Packaging/licence requirements

Do not copy CNR3's MIT metadata.

The wheel/package metadata must represent this project's actual licensing and notices, including:

```text
AGPL-3.0-or-later for project-developed material
LGPL obligations/notice for vendored VapourSynth headers as applicable
MSSG decoder notices retained through NOTICE
LICENSE and NOTICE included in the distribution
```

The wheel route must use the Release artifacts built by the ratified project files/harness; it must not rebuild them with a separate flag set.

Before any real PyPI upload is considered, build a local wheel and smoke-test installation/use in a clean or suitably isolated environment.

---

# FINAL MIGRATION CLOSE-OUT

## 34. One common Developer Handback

There will be one shared migration handback:

```text
docs\HANDOVER\MPEG2_Deblocking_Developer_Handback_<version>.md
```

It is common to both the ChatGPT and Claude technical-development chats.

The individual ChatGPT and Claude handover documents should point to the common handback rather than duplicate migration facts such as:

```text
repository paths
solution/project setup
migration gate results
hashes
build-harness state
final migration checkpoint
```

This avoids divergence between two independent accounts of the same migration.

---

## 35. Common handback provenance

The final common handback header must state:

```text
drafted by migration ChatGPT
cold-reviewed by migration Claude
ratified by Dave
date
```

It must not use a ChatGPT- or Claude-specific filename prefix.

It is to be stored under:

```text
docs\HANDOVER\
```

and committed with the final migration material.

---

## 36. Documentation to update at close-out

At migration completion, the repository-facing and AI-handover documentation must agree with the accepted build evidence.

Required close-out work:

- update the common Developer Handback;
- update the ChatGPT role-specific handover to point to it;
- update the Claude role-specific handover to point to it;
- explicitly correct stale Gate C / pre-Stage-A language;
- explicitly record provenance of earlier handover edits;
- produce/finalize the migration summary;
- record final solution/project identities and paths;
- record every final build-setting decision;
- record which settings remain PROVISIONAL;
- record build/test/hash results;
- verify the repository `README.md` against the accepted project files and gated binaries;
- retain `NOTICE.md` as the authoritative notice/attribution/restricted-test-media boundary and reference it from the handback/role handovers rather than paraphrasing away its distinctions;
- if a NOTICE clarification is still desirable for decoder-derived source location or Stage 1 modifications, review it explicitly without altering frozen source files.

The current updated `README.md` already states the intended public-facing target policy, including:

```text
Windows x64
AVX2-capable CPU required
Release artifacts do not require a separately installed Visual C++ Redistributable
Spectre-mitigated libraries are a build prerequisite
project files own the build settings; command-line overrides are not the build policy
```

Until the superseding A3 and later Stage B gates have actually passed, those README build/distribution statements describe the intended accepted end-state; they are not evidence that the presently checked-out pre-A3 Release EXE/DLL already has those properties.

The README's licence/notices summary must continue to point readers to `NOTICE.md`, including the distinction between AGPL-3.0-or-later project-developed material, MPEG reference-decoder-derived source retaining its original notices, restricted-use `VHSC_samples` recordings, and other third-party material under its own terms.

---

## 37. Handback gate

The migration is not considered ready for return to technical development merely because both projects build. Stage C harness, Stage D release workflow, standalone-artifact enforcement and the Stage E wheel/PyPI packaging scaffold are also part of migration close-out.

Before handback:

1. ChatGPT updates the common Developer Handback to its final candidate version.
2. Claude cold-reviews the final migration state and common handback against actual repository evidence.
3. Dave resolves any review findings and ratifies the handback.
4. Final migration commits are pushed.
5. Final repository status/tag/checkpoint is recorded.
6. Only then does Dave return to the main ChatGPT and Claude technical-development chats.

---

## 38. What remains outside this migration

This migration does not authorize:

```text
Stage 2 experiment implementation
MPEG-2 deblocking algorithm implementation
index-consumption algorithm implementation
pixel filtering
AVX2 filter implementation
final VapourSynth filter-function/API contract beyond the placeholder identity
```

Those remain work for the proper technical-development workflow after handback.

---

## 39. Immediate next work

Current position:

```text
A1 complete
A2 complete
pre-A3 checkpoint complete
A3 v0.2 draft cold-reviewed
M3 dumpbin measurement complete
DR v0.8 / Stage A plan v0.3 cold-reviewed with no MUST corrections
D4 = NO ratified: /MT consolidated into A3; no A4
D5 = YES ratified: future plugin DLL /MT
D6 = YES ratified: Release /PDBALTPATH:%_PDB%
README.md updated to the intended AVX2/standalone/security public build policy
NOTICE.md remains the legal/attribution/restricted-test-media reference to be carried into handback
```

Next work:

1. cold-review DR v0.10 and Stage A execution plan v0.5 carrying the ratified AVX2/security/SDL policy;
2. issue a superseding A3 candidate/review package with M3/S7-S11, Release `/MT`, Release `/PDBALTPATH:%_PDB%`, `/arch:AVX2`, `/favor:blend`, `/GS`, CFG, CET and Spectre enabled, with inspector `/sdl` remaining OFF;
3. Claude cold-reviews the revised A3 package and READY evidence;
4. Dave ratifies that exact A3 candidate;
5. apply and gate A3 once, including standalone dependency checks and all six index regressions;
6. if the gate fails, use the ratified uncommitted diagnosis sequence rather than weakening the gate;
7. after Stage A closes, create the Stage B dummy DLL project with `/MT` and `/PDBALTPATH:%_PDB%` encoded in `mpeg2Deblock.vcxproj`;
8. then create Stage C harness, Stage D release workflow and Stage E wheel scaffold.

No project or solution change, and no Stage B project creation, is authorised merely by this design record; each implementation step requires Claude review and Dave ratification. No Stage 2 algorithm implementation is authorised.

---

## 40. Change log

### v0.11 - 2026-10-09

- Added the documentation-handback policy requested by Dave after the AVX2/security decisions.
- Required the common Developer Handback and future-ChatGPT handover to reference the updated `README.md` and `NOTICE.md` explicitly.
- Recorded that `NOTICE.md` remains the notice/attribution/restricted-test-media boundary rather than having those distinctions rephrased independently in handovers.
- Added a documentation-consistency guard: README claims about AVX2, standalone Release artifacts and security-hardened builds must be confirmed by the accepted Stage A/Stage B evidence before final migration handback.
- Recorded the current README's intended public build requirements without treating the README itself as gate evidence.
- Kept all v0.10 AVX2, `/MT`, CFG, CET, Spectre, `/GS`, SDL and one-build-route policies unchanged.

### v0.10 - 2026-10-09

- Superseded the earlier inspector AVX2-OFF/SSE2 policy: x64 + AVX2 is now the minimum supported CPU target for both projects in Debug and Release.
- Added explicit Release `/favor:blend` cross-vendor tuning intent.
- Ratified security-over-speed policy: `/GS`, CFG, CET compatibility and Spectre mitigation remain enabled; performance work may not obtain speed merely by globally disabling them.
- Recorded the inspector-only `/sdl` OFF exception for frozen MPEG-2 reference-decoder-derived source and `/sdl` ON for new `mpeg2Deblock` code.
- Changed the Stage A M3 gate so CFG and CET are deliberate OFF->ON changes rather than baseline states to preserve.
- Required Spectre-mitigated libraries as a build prerequisite; missing components cause gate/CI failure rather than silent mitigation disablement.
- Expanded the one-build-route rule so project files, Stage C and GitHub CI agree on AVX2/security/runtime settings; CI verifies but does not inject them.
- Marked the existing A3 v0.3 SSE2/security-off proposal as superseded for application; a new A3 candidate is required.

### v0.9 - 2026-10-09

- Incorporated Claude review of DR v0.8 / Stage A plan v0.3.
- Restored the explicit project/solution authorisation guard (S10).
- Recorded Dave-ratified D4 = NO: removed A4 and consolidated Release `/MT` into A3.
- Recorded Dave-ratified D5 = YES: future `mpeg2Deblock.dll` uses `/MT`, hybrid only as fallback.
- Recorded Dave-ratified D6 = YES: Release `/PDBALTPATH:%_PDB%`.
- Added the consolidated A3 standalone Release import gate and `MSVCR1*` forbidden pattern.
- Added the required diagnosis sequence if consolidated A3 changes an index.
- Kept project XML as the single source of standalone/PDB-path settings; harness/CI overrides remain prohibited.
- Carried S11 mitigation/default pinning requirement into the revised A3 direction.

### v0.8 - 2026-10-09

- Incorporated the completed pre-A3 checkpoint and Claude A3 v0.2 cold-review findings.
- Added Dave's hard requirement that Release EXE and DLL be standalone with respect to separately installed MSVC/UCRT redistributables.
- Made the Visual Studio project files the source of truth for Release runtime linkage; CI/harness overrides are prohibited.
- Recorded the proposed D4 A3/A4 split so `/MT` can be attributed and gated independently.
- Added M3 PE/load-config/import measurement and standalone forbidden-DLL gate.
- Added S7 warning-output pins and S8 HostX64 tool-host proof.
- Expanded Stage B to require standalone DLL output from `mpeg2Deblock.vcxproj` itself.
- Recast the build harness as Stage C and adopted the one-build-route rule.
- Added Stage D for adapting CNR3's release-triggered GitHub workflow through the Stage C MSBuild/`.slnx` route rather than CNR3's duplicate `cl` flag map.
- Added Stage E for adapting CNR3's existing wheel mechanics to this project's identity, AGPL-3.0-or-later licensing and eventual PyPI objective.
- Expanded migration close-out so local builds alone are insufficient.

### v0.7 - 2026-10-09

- Finalized the current Stage A migration-design baseline after Claude's follow-up review.
- Made the script-generated CNR3 project-element inventory mandatory rather than preferred.
- Required Visual Studio and MSBuild `vswhere` discovery to use the same `-products *` and component-selection criteria.
- Required the selected Visual Studio and MSBuild paths to be logged and checked as resolving to the same installation.
- Kept the exact discovery commands subject to one machine verification before the build harness is accepted.

### v0.6 - 2026-10-09

- Incorporated Claude's review of v0.5 and the common handback v0.1.
- Recorded Dave's decision not to pin a Windows SDK version.
- Kept explicit Visual Studio 2026 toolset `v145`.
- Changed Visual Studio bootstrap policy from hard-coded version/edition path to `vswhere` discovery.
- Required build logs to identify actual toolchain/SDK used.
- Made `third_party\vapoursynth\include\VERSION.txt` the single header-release identity source.
- Clarified stable authority-document naming/version policy.
- Recorded the then-current inspector AVX2-OFF policy (superseded by v0.10).
- Clarified Deblock4 as historical/reference material only.
- Formalized one common Developer Handback for both technical-development chats.
- Required final handback provenance: drafted by migration ChatGPT, cold-reviewed by migration Claude, ratified by Dave.
- Retained US-ASCII-compatible punctuation.
