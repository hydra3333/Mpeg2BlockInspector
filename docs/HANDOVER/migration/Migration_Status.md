# Migration_Status: VapourSynth-mpeg2Deblock

**Filename:** Migration_Status.md
**Version:** 0.5 (living file; filename unchanged)
**Date:** 2026-10-10
**Owner:** ChatGPT migration chat; Dave ratifies; Claude independently reviews
**Source:** Claude_RESPONSE_TO_ChatGPT_Agreed_Remaining_Plan_v0_1.md; Claude_REVIEW_OF_ChatGPT_Step1_Proving_Workflow_v0_1.md; Claude_REVIEW_OF_ChatGPT_Step1_GitHub_Proving_Run_v0_1.md; GitHub run 38034308907; Claude's Step 0 structure-validator confirmation; Dave's 2026-10-10 Step 1, floating-point, D-SDK and O1-O7 decisions
**Status:** Living migration status; NOT the Design Record or an amended roadmap

## Agreed boundary

- Stage A A3 v0.10: ACCEPTED by Dave, Claude's close-out documents accepted.
- Six-index v0.10 status: WAIVED, NEVER PASS. Dave-ratified exception limited to A3 v0.10, not a future policy waiver.
- Step 0 COMPLETE / PASS: Claude confirmed the **live inspector project structure-validator PASS with 140 pin applications** and independently examined the accepted content; Dave verified Windows working-copy SHA-256 identities of `.vcxproj` and `.slnx`. Stage A close-out commit `b5eb1b9f0ef2cac6fa4cb0fc7b7aef1fdf6b6bb7` identified. The structure-validation result is the substantive live-project content evidence; matching hashes are the identity check.
- Branch policy confirmed by Dave: main is the sole ongoing development branch; no test branch will be created. Existing Git commits/snapshots and release attachments are the recovery references.
- Migration sequence: Step 0 baseline confirmation CLOSED / PASS; Step 1 proving CI workflow CLOSED / ACCEPTED; **all O1-O7 decisions CLOSED** on 2026-10-10; next Step 2 Stage B+ DLL plus toolset-selection change (**candidate scope for Dave to inspect, not yet implemented or gate-accepted**); Step 3 final release workflow; Step 4 handback and migration closure.
- Wheel/PyPI (former migration Stage E) belongs to technical development Stages 7-9. Do not make a placeholder wheel.
- Separate Stage C harness and local build script are cancelled. Developer builds use the VS2026 GUI; development-chat commands are documented in the handback; CI logic is inline in one workflow plus reviewed expected-switch data.
- **DAVE-RATIFIED 2026-10-10 - plugin floating point:** the C++ plugin shall use `/fp:precise` with **no automatic contraction**, matching the inspector. In both Debug and Release the effective CL switches shall show `/fp:precise` and no `/fp:contract`. This closes the plugin floating-point policy item added in provisional Developer Handback v0.16 section R.6 item 7; it is **not** an open decision. Explicit FMA intrinsics, if proposed later for performance, remain subject to separate technical review and numerical-oracle comparison. Record this ratification in the **final common developer handback**; do not issue another provisional Handback version solely for this decision. This is a decision, not evidence that the not-yet-created plugin project already implements it.
- **DAVE-RATIFIED 2026-10-10 - D-SDK option (c):** the selected Windows SDK version remains **unpinned and recorded on every build**. An SDK version change **alone does not trigger additional switch/warning/six-index reruns**. Ordinary per-build mechanical switch/security checks still apply; changes to the MSVC toolset/compiler or inspector project retain their own regression triggers. Dave chose (c) despite the `/MT` static UCRT being a code-changing SDK input; this is an explicit decision, not proof that SDK changes are behaviourally irrelevant.

## Process simplification (P1-P6)

- P1: update THIS status file per step. Update Design Record and Hard-Earned Knowledge only at stage close. Stage A Plan is frozen history. Write the common handback once at the end.
- P2: ChatGPT script-checks ASCII/CRLF, current header and stale versions. Claude need not re-review document housekeeping.
- P3: two Claude reviews per stage: candidate and gate evidence.
- P4: one flat review ZIP with SHA-256 inventory; no nested ZIPs or transmittal essays.
- P5: always run recognition and mechanical CL/LINK switch checks. The binding inspector rule requires all six indexes for any inspector `.vcxproj` edit or MSVC toolset/exact compiler change; `.filters`-only changes are exempt, and infrastructure-only changes with both inspector files byte-identical use one LP smoke run. D-SDK (c) expressly does not add a regression rerun solely because the SDK version changes.
- P6: derive new project settings by comparing accepted projects and CNR3, not rediscovering from scratch.

## Step 0 - accepted baseline confirmation (CLOSED / PASS)

- Claude independently checked the pushed GitHub snapshot: `.slnx` contains the accepted x64-only inspector solution; `.vcxproj` contains the required A3 v0.10 settings, including explicitly required and deliberately absent switches/settings. Claude subsequently confirmed that the **structure validator was run against the live inspector project and PASSED with 140 pin applications**. This substantive structure/pin result belongs to Step 0, not merely the hash checks.
- Dave's Windows `certutil` SHA-256 checks matched the accepted local project `73e9019cda7d1061ecdb06526c60f4ee84baa4c385b7ca0dde4269544e4fdb46` and solution `fa24efcd73401a38604e2f4228b07d8b960abcbfb66da22c02908e9d1cdb0754`.
- Stage A close-out commit was `b5eb1b9f0ef2cac6fa4cb0fc7b7aef1fdf6b6bb7`; Step 1 workflow and migration records were committed and pushed to `main` as `bf2412593e0dd3a93f7b1f0d958e596f9b9abdf5` (clean local working tree confirmed after push).
- The A3 v0.10 six-index rerun remains **WAIVED, NOT PASS**. Step 0 did not add a new six-index result.

## Step 1 - proving GitHub Actions workflow (CLOSED / ACCEPTED)

- Dave committed the reviewed manual-only workflow `.github/workflows/prove-project-build-windows-x64.yml` and its reviewed 113-switch reference `.github/workflows/expected_a3_v0_10_switches.csv` to `main` in `bf2412593e0dd3a93f7b1f0d958e596f9b9abdf5`. Candidate corrections S1 (HostX64 PowerShell regex) and S2 (`detailed` log verbosity) were applied before commit.
- **GitHub Actions run 38034308907 on commit `bf24125`: all proving checks PASS.** Claude's independent gate review `Claude_REVIEW_OF_ChatGPT_Step1_GitHub_Proving_Run_v0_1.md` **ACCEPTED** Step 1; **Dave ACCEPTED** the gate on 2026-10-10. Step 1 is CLOSED; no change to the expected-switch CSV is needed.
- Selected released Visual Studio 2026 Enterprise (`18.10.12217.157`), x64 MSBuild (`18.10.1.42706`, runtime `MSBUILD_IS64=True`), MSVC tools directory `14.51.36231`, and actual CL/LINK `19.51.36260.0`. Actual compiler/linker invocations use `HostX64\x64`; the project files, not a workflow-owned compiler/linker flag map, supply the build settings.
- Debug x64 and Release x64 rebuilds: **PASS**. Actual CL/LINK switch lists match the accepted **113 tokens**, partitioned as Debug CL 33, Debug LINK 23, Release CL 32, Release LINK 25. The only spelling discrepancy is LINK `/manifestinput:` versus `/MANIFESTINPUT:`, equivalent under the agreed case-insensitive LINK comparison.
- Warnings: **17 Debug and 17 Release**, with exactly the same `(source file, line, warning code)` signatures as the accepted local A3 v0.10 logs. Release imports remain `KERNEL32.dll` only, with imported names in the same order; CFG function count 37, expected security features and embedded manifest match. The proof artifact and log were reviewed. Import-name counts reported by the two reviewers differ because of parsing (77 versus 81), **not** because the imported names differ.
- **Release EXE differs from the accepted local EXE.** Claude traced the differences to the static UCRT linked under Release `/MT`: the runner selected Windows SDK `10.0.26100.0` (`Windows Kits\10\lib\10.0.26100.0\ucrt\x64` library directory), while Dave's local accepted A3 build selected SDK `10.0.28000.0`. Differences include code/data section sizes and UCRT-internal symbols; the program's inspected CF targets, imports, entry-point RVA and guard settings match. This is a **strongly supported inference, not byte-for-byte proof** of the cause or of identity of program-authored code; the runner's EXE was not in the Step 1 proof artifact. Do not claim identical binaries.
- **D-SDK CLOSED: Dave selected option (c), record SDK version on every build; an SDK-only change does not trigger extra reruns.** SDK version remains unpinned. Existing per-build checks, project-edit rules and compiler/toolset-change regression gates remain intact.
- **No new six-index regression was performed.** A3 v0.10 remains **WAIVED (NOT PASS)**. The mandatory six-index gate for forthcoming Stage B+ inspector toolset-mechanism changes is unchanged.
- Successful proof verifies that CI can build through project-owned settings without a second flag map. The workflow remains manual-only until the reviewed Step 3 workflow changes its triggers.

## Dave decisions O1-O7 - ALL CLOSED / RATIFIED (2026-10-10)

These are implementation policy decisions, **not** claims that unbuilt DLL code, settings or tests already exist. Rationale and retained acceptance boundaries follow.

- **O1 - coupled naming: CLOSED.** Visual Studio project `mpeg2Deblock`, source directory `src\mpeg2Deblock`, DLL `mpeg2Deblock.dll`, VapourSynth callable namespace `mpeg2deblock`, plugin ID `com.hydra3333.mpeg2deblock`, future PyPI distribution `vapoursynth-mpeg2deblock`, and intended future autoload directory `mpeg2Deblock`. **Rationale:** keep project, runtime identity and future distribution names consistent. Naming is agreed now, but wheel generation and PyPI publication are **not** migration tasks or authorised by O1.
- **O2 - `/guard:ehcont`: CLOSED, explicitly ON for BOTH inspector EXE and plugin DLL**, Debug and Release; configure the effective compiler/linker settings in their `.vcxproj` files and verify the result through the applicable existing build/switch/binary gates. **Rationale:** improved security consistency, rather than excluding the frozen inspector solely because it is frozen. Dave was happy to add the option **without a separate O2-specific experimental test**; that is **not** a waiver of the already-required Stage B+ builds, effective-switch/security checks or the **local six-index regression** triggered by the inspector `.vcxproj` edit/toolset change. Do not label an unperformed test PASS. Inspector C/H source remains frozen.
- **O3 - embedded DLL version resource: CLOSED, YES.** Compile a minimal `VERSIONINFO` resource **into the DLL**; no extra distributed resource file. Maintain **one authoritative version definition** shared by the `.rc` and C++ headers/source; clearly comment where and how the version is changed and distinguish plugin version from VapourSynth API version. **Rationale:** identify installed DLL versions without creating multiple independently maintained version literals or extra distribution files. Initial version value/convention is part of the Stage B+ candidate, not already ratified.
- **O4 - `/LARGEADDRESSAWARE`: CLOSED, explicitly ON for BOTH** x64 inspector and plugin, Debug and Release. The inspector already has it; apply the same explicit setting to the DLL and confirm via actual LINK switches and PE headers. **Rationale:** x64 build consistency and the project's no-silent-defaults principle; this **overrides Claude's earlier recommendation to omit it from the DLL**. A DLL does not independently determine the host process's address-space policy.
- **O5 - x64 + AVX2 everywhere: CLOSED.** Both projects use project-owned `/arch:AVX2` in Debug and Release; no separate AVX2 linker switch is required. Keep the accepted `/favor:blend` setting. **No hand-coded runtime AVX2 CPU detection, mixed-ISA modules, or baseline-safe bootstrap** in Stage B+ or later under the current policy. README declares the AVX2 minimum. **Rationale:** avoid a complicated, fragile multi-ISA/runtime-detection design; Dave accepts unsupported CPUs potentially failing with illegal instruction. This closes O5 rather than merely deferring a guard to Stage 7.
- **O6 - parallel technical development: CLOSED, NO.** All technical implementation and **all experiments, including Python Stage 2**, stay paused until the **entire migration** is finished and Dave explicitly authorises resumption. **Rationale:** maintain one controlled workstream. Retain the previously identified future `experiments\stage2\` location, but do not create speculative experimental directories during migration.
- **O7 - six-index test location: CLOSED, LOCAL ONLY.** Dave runs the mandatory six inspector index regressions in his local Windows repository/development environment whenever the accepted change-control triggers apply. **Do not run them in GitHub Actions.** GitHub is the offsite source repository and builds release assets; CI still verifies toolchain provenance, CL/LINK switches, PE/security, imports/exports and other agreed gates. **Rationale:** keep functional/regression testing in the established local environment without adding an ffmpeg/VapourSynth CI test harness. Dave **explicitly accepts the residual risk** that an Actions-built Release EXE can differ from the locally tested EXE due to compiler/toolset/SDK/environment differences and that the distinct CI binary may not have had the six-index functional regression. Do not equate local regression with a test of the CI-built binary or label an unperformed CI regression PASS. D-SDK option (c) continues to apply.

## Step 2 - Stage B+ (NEXT; SCOPE AGREED IN PRINCIPLE, IMPLEMENTATION NOT STARTED)

- **Review sequence:** ChatGPT shows Dave the bounded candidate scope, then prepares an actual applyable candidate for **Claude's independent candidate review** and Dave's ratification **before** applying production project/source changes. Stage B+ gate evidence receives a second Claude review. No test branch; `main` only.
- **Inspector project change:** test the `PlatformToolset=$(DefaultPlatformToolset)` import-order/selection mechanism locally and use a **numeric minimum-v145 guard**, with no explicit `VCToolsVersion` override. Add Dave's O2 `/guard:ehcont` compiler/linker settings in both configurations. Do not edit frozen inspector C/H source.
- **New DLL project and source:** create `mpeg2Deblock.vcxproj`/`.filters` and `src\mpeg2Deblock` using the O1 name set, register the project in the `.slnx`, and create a minimal VapourSynth API4 DLL scaffold based on CNR3's verified entry-point pattern: `VapourSynthPluginInit2`, `configPlugin`, and one trivial callable function for local load/call proof. **No deblocking filter algorithm or technical Stage 2 experiments.**
- **Settings and verification:** copy the accepted inspector x64/AVX2 `/favor:blend`, floating-point (`/fp:precise`, no `/fp:contract`), CRT (`/MT` Release), optimisation, debug-symbol and security pins; apply O2 `/guard:ehcont` and O4 explicit `/LARGEADDRESSAWARE` to both projects. Retain necessary DLL-only differences: C++20 and `/permissive-` after CNR3 verification, `DynamicLibrary`, `/sdl` ON, no `_CRT_SECURE_NO_WARNINGS`, and no EXE-only Console/UAC/SegmentHeap settings. No CI flag injection or second build-settings map.
- **Version resource (O3):** include a small `.rc` and single canonical version header shared with C++ source, with clear maintenance comments; version resource is embedded in `mpeg2Deblock.dll`, not distributed separately. Choose initial version/convention within the reviewed candidate.
- **Stage B+ local acceptance:** build both projects in the Visual Studio GUI (Debug/Release x64), check rule recognition and effective CL/LINK switch sets (inspector baseline updated solely for reviewed O2 changes), host x64, binary/import/export/security properties including EHCONT as applicable, and local VapourSynth loading/calling the trivial function. Reconcile the new DLL's pins against inspector/CNR3 evidence (existing 113-row / 57-DLL-row comparison). **Run all SIX inspector indexes locally** because the inspector `.vcxproj` and toolset mechanism change; no separate O2-only index run. Report actual PASS/FAIL, never assume success beforehand.
- **CI after candidate acceptance:** commit reviewed changes to `main` and run the existing manual-only Step 1 proving workflow again. Its present switch expectations will require a deliberately reviewed update for O2, not a silent acceptance. Final dual-project CI switch/security/export/release handling is completed in Step 3. **No six-index tests in Actions**, per O7.

## Step 3 - final workflow (NOT STARTED)

- One self-contained `.github/workflows/*.yml` with `release` (published) and `workflow_dispatch`; build both projects via `.slnx` and verify both against reviewed expected-switch files.
- Fail loudly on unexpected/missing compiler or linker switches, print exact differences, no runner/toolset pinning; reviewed legitimate changes update expected CSV and non-executing G7 reference comments in the same commit.
- Actual HostX64 invocations, security (including O2 EHCONT where supported), O4 Large Address Aware, imports/exports, logs and release assets required. Explicitly verify x64/AVX2 compiler settings for both projects. Build switches stay owned by `.vcxproj`, never injected by workflow. Wheel/PyPI excluded.
- **S4 (Step 3):** include the generated **Release EXE and PDB** in the uploaded proof artifact to enable future byte comparisons and CI executable testing.
- **S5 (Step 3):** correct the stale workflow line-1 header saying `CANDIDATE v0.2` / `not run on GitHub yet`; use an accurate production header.
- **S6 (Step 3):** address Node 20 deprecation notices for `actions/checkout@v4` and `actions/upload-artifact@v4`: check then-current supported major versions and their Node 24 runtimes before changing these actions; the exact replacements were unverified in Claude's review.
- **O7 CLOSED:** six-index regression runs on Dave's local Windows environment only when triggered by accepted rules; **no six-index regression in GitHub Actions**. Dave accepts the difference/risk between locally tested and CI-built Release binaries. SDK-only change is excluded by D-SDK (c).

## Step 4 - final common handback and migration close (NOT STARTED)

- Human VS2026 GUI build, proven plain-CMD 64-bit MSBuild discovery/build, separate VsDevCmd/dumpbin example, prohibited environment/flag overrides, actual successful output, gate instructions and CI failure handling.
- Preserve CNR3-derived wheel details for technical Stages 7-9: `py3-none-win_amd64`, `vapoursynth/plugins/<name>/<name>.dll`, AGPL-3.0-or-later, NOT MIT.
- The final common handback must record Dave's 2026-10-10 ratification of the plugin `/fp:precise`, no-automatic-contraction policy, **all O1-O7 dispositions and rationales**, and his O7 acceptance of untested-CI-binary divergence risk. Remove these from its open-decision list. Record D-SDK (c) and the observed SDK/UCRT inference without overstating byte equivalence. Retain the separate caveat about explicit FMA and Python-oracle bit equality. No intermediate Handback version is required.
- Claude reviews; Dave ratifies, commits/pushes; migration ends; **all technical development and experiments remain paused until then and Dave explicitly authorises resumption** (O6).

## Open decisions / agreed dispositions

- **O1-O7 all CLOSED / RATIFIED by Dave (2026-10-10).** Details and rationale are in the O1-O7 section above. There is no open O-item blocking the **drafting** of Stage B+.
- Plugin floating-point policy: **CLOSED** by Dave on 2026-10-10 (`/fp:precise`, no automatic contraction); already recorded above. Explicit FMA later would require separate technical review.
- D-SDK: **CLOSED** by Dave on 2026-10-10, option (c), SDK version recorded every build without an SDK-only regression rerun.
- **Stage B+ candidate details still require normal review and ratification** (not new O1-O7 policy decisions), especially the empirically proven toolset-selection implementation, minimal plugin API code, canonical version definition and exact effective switch sets.

## Stage C-derived safeguards carried into the single workflow

- 64-bit everywhere; x86 host only last D4 local uncommitted diagnostic.
- Latest means latest INSTALLED RELEASED VS, with no `-prerelease`; no hard-coded version/install root. Build Tools eligible.
- Use VS-designated current MSVC build for its toolset, recorded not pinned; file version and toolset directory version both logged.
- N1 Windows command-line splitting only, or fail on non-Windows.
- N2 check actual HostX64 invocation lines, not any `HostX86` text.
- N3 record MSVC directory version AND actual executable file version.
- N4 rely only on established Guard CF table/flag evidence, not speculative bit-field interpretations.
- D-SDK (c): capture exact Windows SDK version on every build; distinguish SDK-derived UCRT changes under `/MT` from toolset/compiler-change regression triggers. SDK changes alone do not add a rerun requirement.
- Guard ambient build environment and ancestor `Directory.Build.*` files; `-noAutoResponse`; prove K4 scratch case before final workflow acceptance. No six-index tests are added to CI (O7).

## Next review checkpoint

- Claude may review this **single living `Migration_Status.md` v0.5 update** for O1-O7 decision fidelity, rationale, risk acceptance and Step 0 validator evidence. No other document revisions or production project/source changes are part of this status update.
- **Next:** Dave first examines ChatGPT's Stage B+ candidate outline. ChatGPT then drafts the bounded applyable candidate for Claude's independent candidate review; Dave ratifies before implementation, followed by local gate evidence and Claude's gate review. Commit reviewed steps directly to `main`, retaining mandatory **local** inspector regression and per-build switch/security checks. At Step 3 incorporate S4-S6. The final common handback is written at migration close, not versioned again now.
