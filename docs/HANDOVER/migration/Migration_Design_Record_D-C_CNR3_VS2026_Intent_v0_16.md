# Migration / Visual Studio Design Record - D-C Intent, CNR3 Configuration Transfer and Developer Handback

**Filename:** `Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_16.md`
**Version:** 0.16
**Date:** 2026-10-10
**Drafted by:** migration ChatGPT chat
**Cold-review status:** Claude reviews through `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_8_Candidate_v0_1.md` are carried. Q1/R1/R4 are closed. Claude found A3 v0.8 not yet ratifiable because of U1 duplicate segment-heap ownership; U2 required predicted-delta additions. Corrective v0.9 is prepared but not yet cold-reviewed.
**Ratification status:** Dave has ratified x64+AVX2, Release `/MT`, `/GS`, CFG, CET, inspector `/sdl` OFF, plugin `/sdl` ON, Spectre mitigation explicitly Disabled, and O7=`YES` (`/favor:blend` in Debug and Release). O8 remains a Stage B decision.
**Status:** Current migration-design candidate with Q1/R1/R4 closed. A3 v0.8 was cold-reviewed and not ratifiable due U1. A3 v0.9 SHA-256 `ebfcde82405fd2dc25aa7a14a160f89375465d545927b3e4583e7a40fd1af668` removes only the two explicit `Link/ManifestInput` owners and carries U2 predicted-delta corrections; it is not yet Claude-reviewed, ratified or applied.
**Supersedes:** `Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_15.md`
**Scope:** Repository migration, Visual Studio 2026 solution/project normalization, standalone Release artifact configuration, build harness, release workflow, wheel/PyPI packaging scaffold, validation, and handback to the technical-development chats.
**Does not authorize:** Stage 2 algorithm implementation or MPEG-2 deblocking implementation.

---

## 0A. Current A3 boundary after Claude v0.8 review

Claude's `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_8_Candidate_v0_1.md` independently verified the v0.8 package, candidate recognition, T1 import position, T2 dual `WholeProgramOptimization` representation, frozen project membership, local evidence identity and validators.

One MUST remained:

```text
U1: duplicate segment-heap manifest ownership
```

The v0.8 candidate both retained:

```text
Manifest/EnableSegmentHeap=true
```

and added:

```text
Link/ManifestInput=$(VCToolsInstallDir)Include\Manifest\segmentheap.manifest
```

The measured checkpoint proved the existing `EnableSegmentHeap=true` setting already generated the linker `/manifestinput:`. The corrective design therefore keeps `EnableSegmentHeap=true` as the sole project owner and removes both explicit `Link/ManifestInput` elements.

Claude's U2 also requires the predicted delta to list the newly explicit spellings:

```text
Debug CL: /Gy- /GF-
Debug LINK: /OPT:NOREF /OPT:NOICF /LARGEADDRESSAWARE /TSAWARE
Release LINK: /LARGEADDRESSAWARE /TSAWARE
```

and to state expected non-emission for explicitly pinned default enum values.

Current corrective candidate:

```text
Mpeg2BlockInspector_A3_APPLYABLE_CANDIDATE_v0_9.vcxproj
SHA-256 ebfcde82405fd2dc25aa7a14a160f89375465d545927b3e4583e7a40fd1af668
```

It has not yet been cold-reviewed, ratified or applied.

The reusable reasoning behind U1 and the preceding Q1/R1/R4 work is preserved in:

```text
StageA_VS2026_MSBuild_Hard_Earned_Knowledge_v0_1.md
```

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
- Dave's policy that performance must not be obtained by disabling the conventional memory/control-flow protections retained for this project: `/GS`, CFG and CET compatibility remain enabled. Spectre mitigation is deliberately not used for this local video-processing threat model and is not a build prerequisite.
- Dave's inspector-specific `/sdl` exception: `/sdl` remains OFF for the frozen MPEG-2 reference-decoder-derived inspector source, while new `mpeg2Deblock` code uses `/sdl` ON.
- Dave's requirement that the same AVX2/security/runtime policy be encoded in the Visual Studio project files and verified by the canonical build harness and final GitHub release workflow; CI may not inject a divergent flag set.
- Dave's direction that the migration close-out handback and future-ChatGPT handover explicitly reference the updated repository `README.md` and `NOTICE.md`, with `NOTICE.md` remaining the legal/attribution boundary and the README remaining the public product/build summary.
- the documentation-consistency rule that README claims about AVX2, standalone Release artifacts and retained security hardening must be verified against accepted project/build evidence before final handback; documentation is not a substitute for the A3/Stage B gates.
- receipt of the previously missing Claude review `Claude_REVIEW_OF_ChatGPT_DR_v0_10_and_StageA_Plan_v0_5_v0_1.md`, including MUST M7 and SHOULD S12-S15;
- Dave's later explicit decision that Spectre mitigation is not required supersedes M7. There is therefore no Spectre library component, `MSB8040`, `/Qspectre`, or Spectre-runtime provenance requirement in the accepted design;
- the S13 rule that newly introduced Visual Studio property XML names are learned empirically from VS2026 property pages on a scratch project rather than guessed;
- the S14 rule that inspector builds retain `/fp:precise` and prove `/fp:contract` absent;
- the S15 information-only LP timing comparison before and after A3;
- Claude's handover-taxonomy correction: migration-only Claude continuity is `Claude_HANDOVER_TO_Future_Claude_Migration_Chat_v0_*.md`; development-chat continuity remains separate.
- receipt of `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_4_PreCandidate_and_DR_v0_12_v0_1.md`, restoring P1 and P3-P6;
- receipt of `Claude_REVIEW_OF_ChatGPT_NoSpectre_DR_v0_13_A3_v0_5_v0_1.md`, requiring N1, N3 and N5;
- Dave's O7=`YES`: `/favor:blend` is explicit in both Debug and Release and Stage B follows the same rule;
- Dave's N4 option (a): commit the corrected README now; it may state ratified target build policy before A3 binary evidence catches up.

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

Published `main` observed after the interim migration checkpoint and subsequent archival commit:

```text
ab145f56fd22cf4812d1e5b3e9fbbffc1f974095
```

**README timing (N4): option (a).** Commit the corrected no-Spectre README now. Its AVX2 and standalone-runtime statements remain ratified target policy until A3 supplies matching binary evidence.

The migration documentation checkpoint itself is:

```text
b4dace033e2d6f6d0c4b505875aeae6879077324
Checkpoint Stage A migration design and review state
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
    /favor:blend explicitly recorded in Debug and Release for broad AMD/Intel tuning
    retained conventional hardening is not disabled merely for performance

Security hardening
    /GS ON
    Control Flow Guard ON at compile and link
    CET shadow-stack compatibility ON
    SpectreMitigation explicitly Disabled in Debug and Release; /Qspectre absent

SDL
    Mpeg2BlockInspector: OFF only as a documented frozen/reference-decoder exception
    mpeg2Deblock: ON for new code
```

The accepted project policy deliberately keeps `/GS`, CFG and CET while not using Spectre mitigation. Spectre-specific libraries and discovery checks are therefore not build prerequisites.

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

Debug and Release both explicitly use `/favor:blend` as the broad AMD/Intel microarchitecture tuning policy. Dave ratified O7=`YES`; the setting is written explicitly in each configuration so the intended performance target does not depend on a mutable compiler default.

### Security hardening

The project does not trade security protections away merely for speed. The intended accepted project settings apply to **both Debug and Release** unless an explicit exception says otherwise:

```text
BufferSecurityCheck = true            -> /GS
Control Flow Guard = enabled          -> /guard:cf at compile and link
CET shadow-stack compatible = enabled -> /CETCOMPAT
SpectreMitigation = Disabled          -> /Qspectre absent
```

The Stage A inspector and Stage B plugin gates must verify the effective command lines and PE/load-config state. The inspector keeps `/sdl` OFF in both configurations only as the frozen-reference-decoder exception; new plugin code uses `/sdl` ON.

**Spectre policy decision - supersedes M7, with N1 explicit OFF pin.** Claude's M7 review was valid for the earlier policy that required `/Qspectre`. Dave subsequently decided that Spectre mitigation is outside the required threat model. Under the no-defaults rule this is not omission/default: Debug and Release explicitly write the VS2026 `SpectreMitigation = Disabled` setting captured by S13, and the effective compiler commands contain no `/Qspectre`. No Spectre runtime component, `MSB8040` gate or Spectre-library provenance check is required.

**S13 - property XML is empirical.** Before the superseding A3 `.vcxproj` candidate is finalized, use a scratch copy in VS2026 Property Pages to set each newly introduced/uncertain security/debug-information property and inspect the exact XML VS writes. At minimum capture CFG enabled, CET compatible enabled, Spectre mitigation explicitly Disabled, and Full-PDB/debug-information behaviour. Use that exact representation when available. Use `AdditionalOptions` only where VS2026 writes no dedicated stable project element, and record that fact.

**S14 - floating-point contraction guard.** The inspector keeps `FloatingPointModel=Precise`; the exact Debug and Release compiler commands must prove `/fp:contract` is absent. This protects the AVX2/FMA transition from silently changing floating-point contraction policy.

**S15 - information-only performance measurement.** Time the LP regression case three times using the preserved pre-A3 Release executable and three times using the accepted post-A3 Release executable on the same machine. Record all six timings and simple summary statistics. This is informational only and cannot justify disabling `/GS`, CFG or CET.

**P1 - mechanical pin table.** The final A3 candidate package carries a CSV pin table with one row for every switch from the four checkpoint CL/LINK command lines and every M3 dumpbin property. Each row records checkpoint value, A3 value, configuration, exact XML element or justified `AdditionalOptions`/tool-semantic/deliberate exception, and evidence source. N1 and O7 are rows. The final validator fails on a missing/duplicate row, blank coverage, unknown coverage kind or any remaining `S13_PENDING`.


**Q1 - prove every XML name/value and derive command coverage from measured evidence.** Before the final A3 candidate reaches review:

1. Every `XML` pin-table target must have recognition evidence that the property name and, for enumerations, the value are accepted by the installed VS2026/MSBuild rule set or were written by VS2026 in the S13 scratch-project capture. Merely naming plausible XML is insufficient because unknown item metadata can be ignored silently.
2. The preferred mechanical evidence is a scan of the installed Visual C++ property-page rule XML files under the selected `VSINSTALL`; unresolved items are added to S13. The scan must not assume a fixed version/locale path.
3. The CL/LINK expected evidence set must be generated from the four byte-copied checkpoint command tlogs, not from a hand-written key list. The default Windows library list (`kernel32.lib` through `odbccp32.lib`) is part of that evidence and must be represented either as an explicit pin or a deliberate exception whose command-line/import gates still prove the accepted outcome.
4. The final pin-table validator fails if any XML target lacks recognition evidence, any measured checkpoint token lacks exactly one coverage row, any extra coverage row claims checkpoint evidence that is absent, or any `S13_PENDING` remains.

The A3 v0.7 pre-candidate provided the local scripts/checklists. The evidence has now passed; A3 v0.8 contains the first applyable candidate, still gated by Claude cold review and Dave ratification.

**P3 - exact post-A3 dumpbin criteria.** Require the Control Flow Guard DLL characteristic, a present/non-zero Guard CF function table/count, CET-compatible extended DLL characteristics, and Release CodeView/RSDS PDB data containing only the PDB file name while Debug retains its ordinary development path. Record the exact wording from the first accepted post-A3 capture and use that wording thereafter.

**P4 - reconciliation validator regression.** Reject duplicate keys, enforce 56 self-test + 57 DLL rows, cross-check key/setting/value against `StageA_CNR3_113_row_source_reference_v0_1.csv`, and reject blank/unknown dispositions or reasons.

**N5 - one Visual Studio installation.** `VSINSTALL` comes from `vswhere`; `MSBuild.exe` is derived or positively verified underneath that same root. Mismatch is a hard failure.

**O7 ratified; O8 remains open.** O7=`YES`: `/favor:blend` is explicit in Debug and Release and Stage B follows the same policy. O8 `/guard:ehcont` remains a Stage B decision.

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

A3 is the single reviewed Stage A project-settings change after A1/A2. There is no A4.

Before a final candidate is generated, S13 must be completed on a scratch copy in Dave's VS2026 installation so the package uses the XML VS2026 actually writes for the relevant property-page choices rather than guessed names.

The accepted A3 direction includes:

```text
explicit pins derived from the pre-A3 checkpoint
Claude M3/S7-S15 corrections; M7 is recorded as superseded by Dave's later Spectre-policy decision
ratified D1-D3
PreferredToolArchitecture=x64
Release RuntimeLibrary=/MT   (D4 = NO: consolidated into A3)
Release /PDBALTPATH:%_PDB%   (D6 = YES)
/arch:AVX2 Debug+Release
/favor:blend Debug+Release
/fp:precise Debug+Release with /fp:contract absent
/GS enabled Debug+Release
CFG enabled at compile+link Debug+Release
/CETCOMPAT enabled Debug+Release
SpectreMitigation explicitly Disabled in Debug+Release; /Qspectre absent
inspector /sdl remains OFF Debug+Release only as the frozen-reference-decoder exception
```

The `/MT`, AVX2, security and PDB-path choices MUST be present in `Mpeg2BlockInspector.vcxproj`. The local harness and final GitHub workflow are forbidden from injecting them as corrective overrides.

Spectre-specific discovery, `MSB8040` handling and Spectre-library provenance are not A3 requirements because Spectre mitigation is deliberately not used.

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

### Build and discovery

Rebuild:

```text
Debug | x64
Release | x64
```

The same Visual Studio discovery used by the controlled build must require MSBuild and x64 C++ tools. At minimum the `vswhere -requires` set includes:

```text
Microsoft.Component.MSBuild
Microsoft.VisualStudio.Component.VC.Tools.x86.x64
```

No Spectre component or `MSB8040` handling is required because `/Qspectre` is deliberately not used.

### S13 property representation proof

Before the candidate is applied, preserve the scratch-project Property Pages experiment showing what VS2026 writes for the newly introduced/uncertain properties (at least CFG, CET and full-PDB/debug-information settings). The accepted project uses those exact elements where VS supplies them. No guessed XML property is accepted.

### Warnings

Compare warnings by:

```text
warning code
file
line
stage
```

Do not merely compare the warning count. Any new warning must be examined and explained.

### Effective compiler/linker policy

Both Debug and Release compiler/linker evidence must prove the configuration-specific security/CPU policy:

```text
/arch:AVX2
/GS
CFG compile+link enabled
/CETCOMPAT enabled
SpectreMitigation explicitly Disabled; `/Qspectre` absent
/fp:precise
/fp:contract absent
```

Debug remains `/MDd`; Release is `/MT`. Debug and Release both explicitly carry `/favor:blend` (O7=`YES`).

### Spectre policy evidence

The A3 evidence must show `SpectreMitigation=Disabled` explicitly in Debug and Release, `/Qspectre` absent from both effective compiler commands, and no Spectre-specific library requirement or CI override.

### Frozen source hashes

Frozen inspector-source hashes and the analyzer hash must remain unchanged.

### Functional regression

Run all six tracked index cases after consolidated A3. All six regenerated `.idx` files must be byte-identical to their established baselines. Mandatory LP SHA-256:

```text
849b6a9c411a7db837268af3ac54501a06f5f1158e68d5245ce2b3ec40a0d011
```

### S15 LP timing (information only)

Preserve the pre-A3 Release executable before A3 overwrites the build output. Run the LP case three times with the pre-A3 Release executable and three times with the accepted post-A3 Release executable on the same machine under comparable conditions. Record individual elapsed times plus a simple mean/median. Timing is not a PASS/FAIL criterion and cannot justify weakening CFG/CET/GS.

### PE / load-config / import gate

Use `dumpbin /headers /loadconfig /imports /dependents`. Preserve baseline semantic state except for ratified changes. Require:

```text
x64 PE32+
Large Address Aware
High Entropy VA
Dynamic Base
NX Compatible
manifest generation
Debug linker /OPT behaviour
debug-information mode
CET-compatible image flag PRESENT
fully enabled CFG image PRESENT
```

The post-A3 CL/LINK executable paths must show `HostX64\x64`.

Because Release changes `/MD -> /MT`, Release must contain no dependency whose DLL name matches:

```text
VCRUNTIME*
MSVCP*
api-ms-win-crt-*
ucrtbase*
CONCRT*
VCOMP*
MSVCR1*
```

Do not use broad `MSVCR*`, which would also match Windows system `msvcrt.dll`. The current expected allowed Release DLL-name set after static-runtime conversion is `KERNEL32.dll`; any additional DLL name stops the gate for review. Debug remains `/MDd` and its dependency DLL-name set is compared with the checkpoint at DLL-name level.

### Visual Studio rewrite / Git state

After opening/building the `.slnx`, `git status --short` must show no unexpected rewrite of tracked project/solution files. Preserve `git status --short --ignored` as well.

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

The DLL project must also carry the project-wide CPU/security policy directly in its own settings: `/arch:AVX2`, `/GS`, CFG and CET enabled, Spectre mitigation deliberately not used, and `/sdl` ON for the new C++ source. These are not CI-only switches.

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
plugin `/guard:ehcont` policy (Claude O8; explicit Stage B decision)
plugin floating-point/FMA contraction policy
optional clean AVX2-capability failure path in the plugin entry point
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

The exact command is to be verified on Dave's machine before the build harness is accepted. No Spectre component is required because `/Qspectre` is deliberately outside the accepted build policy.

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


**Q3 - MSBuild same-installation method.** The canonical local prerequisite method is intentionally `vswhere` -> `VSINSTALL` -> `%VSINSTALL%\MSBuild\Current\Bin\MSBuild.exe`. This replaces an independent `vswhere -find` lookup for Stage A so the selected MSBuild is guaranteed to belong to the same installation. Stage C may wrap the same rule but may not select a different installation.

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

Do not adopt CNR3's duplicated CI `cl` flag map. Do not override `PlatformToolset`, `/MT`, `/GL`, `/LTCG`, `/arch:AVX2`, `/favor:blend`, `/GS`, CFG, CET, SDL policy or other ratified project settings from the harness/workflow. The harness/workflow must also not inject `/Qspectre`. If the runner lacks required `v145` or another accepted prerequisite, it must fail rather than silently substitute another toolset or weaken the build.

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

For the Release DLL, also run `dumpbin /dependents` plus the corresponding header/load-config checks and require the standalone-runtime and security policy. The accepted evidence must show AVX2 in the effective compiler command, `/GS`, CFG at compile+link, CET compatibility, `/Qspectre` absent by policy, and `/sdl` ON for the new plugin project. The DLL project itself must be configured to produce that result; passing only because a harness or workflow injects different flags is a failure.

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

The workflow must fail if the required `v145` toolset or another accepted prerequisite is unavailable; it must not override `PlatformToolset` or weaken the CPU/security policy to suit the runner.

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
Spectre mitigation deliberately absent (`/Qspectre` not present)
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

There will be one shared migration-to-development handback:

```text
docs\HANDOVER\MPEG2_Deblocking_Developer_Handback_<version>.md
```

It is common to both the ChatGPT and Claude technical-development chats and carries the final repository/layout/build/settings/gate state they inherit.

Migration continuity documents are separate:

```text
ChatGPT_Migration_Chat_Handover_v0_*.md
Claude_HANDOVER_TO_Future_Claude_Migration_Chat_v0_*.md
```

Each technical-development chat owns its own role-3 successor-chat handover. Migration does **not** edit those development handovers. Dave gives the final common handback to both development chats; each development chat may then update its own handover to reference the common handback.

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

At migration completion, repository-facing documentation and **migration-owned** handover documentation must agree with the accepted build evidence.

Required close-out work:

- update/finalize the common Developer Handback;
- update `ChatGPT_Migration_Chat_Handover_v0_*.md`;
- ensure migration Claude's continuity file is correctly named `Claude_HANDOVER_TO_Future_Claude_Migration_Chat_v0_*.md`;
- give the final common handback to both technical-development chats; each development chat updates its own internal future-chat handover if/when that chat chooses to do so;
- do **not** edit `ChatGPT_Handover_To_Future_ChatGPT_MPEG2_Deblocking_Project_v0_*.md` or `Claude_HANDOVER_TO_Future_Claude_Chat_v0_*.md` from migration unless Dave explicitly asks for a boundary-crossing update;
- explicitly correct stale Gate C / pre-Stage-A language in migration-owned documents;
- produce/finalize the migration summary;
- record final solution/project identities and exact path case;
- record every final build-setting decision and which settings remain PROVISIONAL;
- record build/test/hash results;
- verify the repository `README.md` against accepted project files and gated binaries;
- retain `NOTICE.md` as the authoritative notice/attribution/restricted-test-media boundary and reference it from the common handback and migration continuity docs rather than paraphrasing away its distinctions;
- if a NOTICE clarification is still desirable for decoder-derived source location or Stage 1 modifications, review it explicitly without altering frozen source files.

The current updated `README.md` describes the intended post-A3 product/build policy. Its Git commit status has not been established by the supplied review documents. Before A3 documentation close-out, verify that status from the live repository. Claude recommends committing the README with A3 or after the A3 gate, not as an earlier independent claim of build state.

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

1. Dave/ChatGPT verify the live repository status of `README.md` and exact committed Visual Studio path case (`git ls-files vs`).
2. Complete S13 on a scratch copy in VS2026: set the new/uncertain properties in Property Pages and preserve the exact XML VS writes.
3. Generate the superseding A3 candidate/package from the untouched current A1/A2 project state using DR v0.13 / Plan v0.8 and the S13 evidence.
4. Cold-review and ratify A3; only then apply it.
5. Run the full A3 gate including S12-S15, six indexes and PE/import/security checks; prove `/Qspectre` absent by policy.
6. Close Stage A, then proceed Stage B -> C -> D -> E.
7. Finalize the common Developer Handback and migration-only continuity handovers; development chats update their own successor-chat handovers separately.

No project/solution change and no Stage B project creation is authorized merely by this document; each application step still requires the established Claude review and Dave ratification. No Stage 2 algorithm implementation is authorized.

## 40. Change log

### v0.16 - 2026-10-10

- Recorded Claude closure of Q1/R1/R4 local evidence.
- Recorded A3 v0.8 applyable candidate generation for cold review; candidate remains unapplied and unratified.
- Carried T1 pre-`Microsoft.Cpp.props` Configuration placement, T2 dual WholeProgramOptimization representation, and T3 exact default-library exception rationale.


### v0.15 - 2026-10-09

- Carried `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_6_PreCandidate_and_DR_v0_14_v0_1.md`.
- Added Q1: every XML pin name/value requires rule-file or S13 recognition evidence; silently ignored MSBuild metadata is not acceptable.
- Replaced hand-maintained expected-key authority with checkpoint-tlog-derived CL/LINK evidence, including the default Windows library list.
- Required final pin validation to cross-check XML recognition, measured command tokens and zero remaining `S13_PENDING` rows.
- Recorded the same-installation MSBuild derivation as the deliberate Stage A discovery method.

### v0.14 - 2026-10-09

- Carried the missing A3 v0.4 pre-candidate review and the no-Spectre v0.13/v0.5 review.
- O7=`YES`: `/favor:blend` explicit in Debug and Release; Stage B follows.
- N1: `SpectreMitigation=Disabled` explicit in both configurations; `/Qspectre` absence still gated.
- Restored P1 mechanical pin table and final fail-on-uncovered validation.
- Added P3 exact CFG/CET/PDB dumpbin criteria and P4 strict reconciliation validation.
- Fixed P5 headings, required P6 CRLF BAT, N3 stale references and N5 same-installation MSBuild proof.
- N4 option (a): commit corrected README now.


### v0.13 - 2026-10-09

- Recorded Dave's deliberate decision not to use Spectre mitigation for this project's threat model.
- Retained `/GS`, CFG, CET, ASLR/High-Entropy VA and DEP/NX; security is not traded away for speed.
- Superseded Claude M7's Spectre-library/MSB8040 requirements because `/Qspectre` is no longer part of the accepted build policy.
- Updated S12 so Debug and Release both carry `/GS`, CFG and CET while Spectre remains deliberately unused.
- Kept S13 property-page XML capture for CFG, CET and full-PDB/debug-information settings; S14 and S15 remain required.
- Kept O7 open and deferred O8 `/guard:ehcont` to Stage B.
- Recorded the published interim migration checkpoint `b4dace0` and subsequent `main` state `ab145f5`.
- Required README correction because the committed README still carried the superseded Spectre-library prerequisite.

### v0.12 - 2026-10-09

- Carried the previously missing Claude DR v0.10 / Plan v0.5 review: M7, S12-S15, and recorded optional O7/O8.
- Added hard Spectre prerequisite enforcement: `vswhere` component requirement, `MSB8040` fatal handling, and positive Spectre-library resolution evidence.
- Made CFG/CET/GS policy explicit for both Debug and Release.
- Added S13 empirical VS2026 Property Pages XML capture before the final A3 candidate is generated.
- Added S14 `/fp:precise` with `/fp:contract` absent and S15 three-run LP timing before/after A3 for information only.
- Corrected the three-role handover taxonomy and exact Claude migration-handover name; migration no longer instructs itself to edit development-chat continuity handovers.
- Clarified README commit timing/status as a live-repository check; recommended commit timing remains with A3 or after its gate.

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
