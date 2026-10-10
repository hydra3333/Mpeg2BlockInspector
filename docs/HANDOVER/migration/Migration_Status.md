# Migration_Status: VapourSynth-mpeg2Deblock

**Filename:** Migration_Status.md
**Version:** 0.3
**Date:** 2026-10-10
**Owner:** ChatGPT migration chat; Dave ratifies; Claude independently reviews
**Source:** Claude_RESPONSE_TO_ChatGPT_Agreed_Remaining_Plan_v0_1.md (2026-10-10), Claude_REVIEW_OF_ChatGPT_Step1_Proving_Workflow_v0_1.md, and Dave's 2026-10-10 floating-point decision
**Status:** Living migration status; NOT the Design Record or an amended roadmap

## Agreed boundary

- Stage A A3 v0.10: ACCEPTED by Dave, Claude's close-out documents accepted.
- Six-index v0.10 status: WAIVED, NEVER PASS. Dave-ratified exception limited to A3 v0.10, not a future policy waiver.
- Dave reports the Stage A documentation was pushed. Final working-copy SHA256 / Git commit ID have NOT been independently rechecked in this turn.
- Branch policy confirmed by Dave: main is the sole ongoing development branch; no test branch will be created. Existing Git commits/snapshots and release attachments are the recovery references.
- Migration is now: Step 0 baseline confirmation; Step 1 proving CI workflow; Step 2 Stage B+ DLL plus toolset-selection change; Step 3 final release workflow; Step 4 handback and migration closure.
- Wheel/PyPI (former migration Stage E) belongs to technical development Stages 7-9. Do not make a placeholder wheel.
- Separate Stage C harness and local build script are cancelled. Developer builds use the VS2026 GUI; development-chat commands are documented in the handback; CI logic is inline in one workflow plus reviewed expected-switch data.
- **DAVE-RATIFIED 2026-10-10 - plugin floating point:** the C++ plugin shall use `/fp:precise` with **no automatic contraction**, matching the inspector. In both Debug and Release the effective CL switches shall show `/fp:precise` and no `/fp:contract`. This closes the plugin floating-point policy item added in provisional Developer Handback v0.16 section R.6 item 7; it is **not** an open decision. Explicit FMA intrinsics, if proposed later for performance, remain subject to separate technical review and numerical-oracle comparison. Record this ratification in the **final common developer handback**; do not issue another provisional Handback version solely for this decision. This is a decision, not evidence that the not-yet-created plugin project already implements it.

## Process simplification (P1-P6)

- P1: update THIS status file per step. Update Design Record and Hard-Earned Knowledge only at stage close. Stage A Plan is frozen history. Write the common handback once at the end.
- P2: ChatGPT script-checks ASCII/CRLF, current header and stale versions. Claude need not re-review document housekeeping.
- P3: two Claude reviews per stage: candidate and gate evidence.
- P4: one flat review ZIP with SHA-256 inventory; no nested ZIPs or transmittal essays.
- P5: always run recognition and mechanical CL/LINK switch checks; run six indexes when compiler/toolset/code generation can change.
- P6: derive new project settings by comparing accepted projects and CNR3, not rediscovering from scratch.

## Step 0 - accepted baseline confirmation

- Claude checked the GitHub snapshot: `.slnx` x64 and one inspector project; `.vcxproj` contains the ratified A3 v0.10 settings.
- Remaining Dave command evidence (not provided in this turn): hash the local project and solution, run `git status --short` and identify the Stage A close-out commit.
- Expected working-copy SHA256: `.vcxproj` = `73e9019cda7d1061ecdb06526c60f4ee84baa4c385b7ca0dde4269544e4fdb46`; `.slnx` = `fa24efcd73401a38604e2f4228b07d8b960abcbfb66da22c02908e9d1cdb0754`.

## Step 1 - proving GitHub Actions workflow (CURRENT)

- Review candidate `.github/workflows/prove-project-build-windows-x64.yml`, manual trigger ONLY, plus `.github/workflows/expected_a3_v0_10_switches.csv` generated unchanged from accepted A3 evidence (113 tokens).
- Runner is `windows-latest`, x64. Discover one newest released Visual Studio (Build Tools permitted), require C++ and MSBuild; derive x64 MSBuild, verify actual 64-bit MSBuild execution, and enforce K4/`-noAutoResponse`.
- Build accepted `.slnx` Debug and Release x64 through project files. Do not copy compiler/linker switches into the workflow.
- Extract Windows command-line tokens from native tlogs; compare mechanically against reviewed baseline; fail with exact missing/extra tokens. Check actual HostX64 compiler/linker INVOCATION lines, not property-reassignment text. Validate Release binary security, KERNEL32-only imports, upload diagnostic evidence even on failure.
- Collect actual VS, MSBuild, MSVC directory/file and SDK versions and evidence; record differences against A3 rather than claiming a toolchain-independent pass.
- Claude reviews the candidate. Dave commits the approved manual-only proof workflow directly to main, dispatches it against main, and returns CI evidence for Claude's gate review.
- Candidate review: Claude's review v0.1 accepted the workflow after mandatory S1 (PowerShell HostX64 regex) and recommended S2 (file log verbosity `detailed`, not `diagnostic`). Both corrections were made in the reviewed candidate without other workflow edits; Claude waived re-review for these two exact changes. Step 1 has **not** been executed on GitHub.
- **GitHub trigger prerequisite:** `workflow_dispatch` requires registration on the default branch. This is satisfied naturally: main is the default and sole ongoing development branch. No bootstrap/test branch, source_ref input, or branch selection is required. DO NOT add an unratified push/release trigger.
- **Unverified until run:** runner software inventory, MSBuild runtime probe property expression, PowerShell/YAML scripting and executable command-line extraction; the workflow is a candidate, not PASS evidence.

## Step 2 - Stage B+ (NOT STARTED)

- Dave decides coupled naming: project/folder, DLL, VapourSynth namespace/plugin ID, future PyPI name/autoload folder.
- One reviewed production candidate: replace inspector's fixed `PlatformToolset=v145` with tested `$(DefaultPlatformToolset)` plus numeric minimum-v145 guard (NO `VCToolsVersion` override); new DLL `.vcxproj` / `.filters`, solution registration, minimal CNR3-derived `VapourSynthPluginInit2` and a trivial callable filter.
- DLL settings follow inspector pins except reviewed DLL-only differences: dynamic library, C++20/permissive policy proven from CNR3 project, `/sdl` ON, no inspector `_CRT_SECURE_NO_WARNINGS`, no exe-specific subsystem/UAC/segmentHeap settings.
- The DLL additionally implements Dave's ratified `/fp:precise` policy with `/fp:contract` absent in Debug and Release. Confirm effective CL switches at the Stage B+ gate.
- Use existing 113-row reconciliation, with 57 DLL rows. Both projects build in GUI, output switches checked, DLL export verified, local VapourSynth load/call verified, and all SIX INSPECTOR indexes rerun because toolset-selection mechanism changes. Run the manual proof workflow again on main after the B+ candidate is committed.

## Step 3 - final workflow (NOT STARTED)

- One self-contained `.github/workflows/*.yml` with `release` (published) and `workflow_dispatch`; build both projects via `.slnx` and verify both against reviewed expected-switch files.
- Fail loudly on unexpected/missing compiler or linker switches, print exact differences, no runner/toolset pinning; reviewed legitimate changes update expected CSV and non-executing G7 reference comments in the same commit.
- Actual HostX64 invocations, security, imports/exports, logs and release assets required. Wheel/PyPI excluded.
- O7 (six indexes in CI or local) remains for Dave to decide. A local six-index run on compiler/toolset/code-generation change is required if CI does not run it.

## Step 4 - final common handback and migration close (NOT STARTED)

- Human VS2026 GUI build, proven plain-CMD 64-bit MSBuild discovery/build, separate VsDevCmd/dumpbin example, prohibited environment/flag overrides, actual successful output, gate instructions and CI failure handling.
- Preserve CNR3-derived wheel details for technical Stages 7-9: `py3-none-win_amd64`, `vapoursynth/plugins/<name>/<name>.dll`, AGPL-3.0-or-later, NOT MIT.
- The final common handback must record Dave's 2026-10-10 ratification of the plugin `/fp:precise`, no-automatic-contraction policy and remove the floating-point item from its open-decision list. Retain the separate caveat about explicit FMA and Python-oracle bit equality. No intermediate Handback version is required.
- Claude reviews; Dave ratifies, commits/pushes; migration ends; technical development resumes only when Dave authorises.

## Open Dave decisions (do not pre-decide)

- O1: coupled DLL/project/plugin/wheel names, at beginning of Stage B+.
- O2: `/guard:ehcont` on DLL; Claude recommends ON.
- O3: minimal DLL version resource; Claude recommends YES.
- O4: drop ineffective DLL Large Address Aware property or retain; Claude recommends DROP.
- O5: runtime AVX2 guard; Claude recommends defer until technical Stage 7.
- O6: Python technical Stage 2 in parallel with migration, Dave's call.
- O7: six indexes in CI or locally at Step 3.
- Plugin floating-point policy: **CLOSED** by Dave on 2026-10-10 (`/fp:precise`, no automatic contraction); no longer an O-item.

## Stage C-derived safeguards carried into the single workflow

- 64-bit everywhere; x86 host only last D4 local uncommitted diagnostic.
- Latest means latest INSTALLED RELEASED VS, with no `-prerelease`; no hard-coded version/install root. Build Tools eligible.
- Use VS-designated current MSVC build for its toolset, recorded not pinned; file version and toolset directory version both logged.
- N1 Windows command-line splitting only, or fail on non-Windows.
- N2 check actual HostX64 invocation lines, not any `HostX86` text.
- N3 record MSVC directory version AND actual executable file version.
- N4 rely only on established Guard CF table/flag evidence, not speculative bit-field interpretations.
- Guard ambient build environment and ancestor `Directory.Build.*` files; `-noAutoResponse`; prove K4 scratch case before final workflow acceptance.

## Next review checkpoint

- Claude cold-review of THIS status file, the unchanged expected-switch CSV and the self-contained main-only proof workflow. No production `.vcxproj` or source changes in this step.
- Stage B+ and final workflow will likewise be reviewed as candidate packages and, after Dave approves, committed to main directly. Execute manual proof on main; existing commits/snapshots and release attachments provide historical retrieval. The original Claude plan mentions a test/B+ branch; Dave has explicitly superseded that implementation detail.
