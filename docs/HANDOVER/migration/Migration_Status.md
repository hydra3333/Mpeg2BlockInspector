# Migration_Status: VapourSynth-mpeg2Deblock

**Filename:** Migration_Status.md
**Version:** 0.4 (living file; filename unchanged)
**Date:** 2026-10-10
**Owner:** ChatGPT migration chat; Dave ratifies; Claude independently reviews
**Source:** Claude_RESPONSE_TO_ChatGPT_Agreed_Remaining_Plan_v0_1.md; Claude_REVIEW_OF_ChatGPT_Step1_Proving_Workflow_v0_1.md; Claude_REVIEW_OF_ChatGPT_Step1_GitHub_Proving_Run_v0_1.md; GitHub run 38034308907; Dave's 2026-10-10 Step 1 acceptance, floating-point ratification and D-SDK decision
**Status:** Living migration status; NOT the Design Record or an amended roadmap

## Agreed boundary

- Stage A A3 v0.10: ACCEPTED by Dave, Claude's close-out documents accepted.
- Six-index v0.10 status: WAIVED, NEVER PASS. Dave-ratified exception limited to A3 v0.10, not a future policy waiver.
- Step 0 COMPLETE / PASS: Dave verified the current Windows working-copy SHA-256 identities of the accepted `.vcxproj` and `.slnx`; Stage A close-out commit `b5eb1b9f0ef2cac6fa4cb0fc7b7aef1fdf6b6bb7` identified. The accepted content was previously independently checked by Claude.
- Branch policy confirmed by Dave: main is the sole ongoing development branch; no test branch will be created. Existing Git commits/snapshots and release attachments are the recovery references.
- Migration sequence: Step 0 baseline confirmation CLOSED / PASS; Step 1 proving CI workflow CLOSED / ACCEPTED; next Step 2 Stage B+ DLL plus toolset-selection change (awaiting Dave's O1-O7 decisions); Step 3 final release workflow; Step 4 handback and migration closure.
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

- Claude independently checked the pushed GitHub snapshot: `.slnx` contains the accepted x64-only inspector solution; `.vcxproj` contains the required A3 v0.10 settings, including explicitly required and deliberately absent switches/settings.
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

## Step 2 - Stage B+ (NEXT; NOT STARTED)

- Stage B+ awaits Dave's O1-O7 decisions (or explicit dispositions of items deferred to later stages). Do not silently settle open items.
- Dave decides coupled naming: project/folder, DLL, VapourSynth namespace/plugin ID, future PyPI name/autoload folder.
- One reviewed production candidate: replace inspector's fixed `PlatformToolset=v145` with tested `$(DefaultPlatformToolset)` plus numeric minimum-v145 guard (NO `VCToolsVersion` override); new DLL `.vcxproj` / `.filters`, solution registration, minimal CNR3-derived `VapourSynthPluginInit2` and a trivial callable filter.
- DLL settings follow inspector pins except reviewed DLL-only differences: dynamic library, C++20/permissive policy proven from CNR3 project, `/sdl` ON, no inspector `_CRT_SECURE_NO_WARNINGS`, no exe-specific subsystem/UAC/segmentHeap settings.
- The DLL additionally implements Dave's ratified `/fp:precise` policy with `/fp:contract` absent in Debug and Release. Confirm effective CL switches at the Stage B+ gate.
- Use existing 113-row reconciliation, with 57 DLL rows. Both projects build in GUI, output switches checked, DLL export verified, local VapourSynth load/call verified, and all SIX INSPECTOR indexes rerun because toolset-selection mechanism changes. Run the manual proof workflow again on main after the B+ candidate is committed.

## Step 3 - final workflow (NOT STARTED)

- One self-contained `.github/workflows/*.yml` with `release` (published) and `workflow_dispatch`; build both projects via `.slnx` and verify both against reviewed expected-switch files.
- Fail loudly on unexpected/missing compiler or linker switches, print exact differences, no runner/toolset pinning; reviewed legitimate changes update expected CSV and non-executing G7 reference comments in the same commit.
- Actual HostX64 invocations, security, imports/exports, logs and release assets required. Wheel/PyPI excluded.
- **S4 (Step 3):** include the generated **Release EXE and PDB** in the uploaded proof artifact to enable future byte comparisons and CI executable testing.
- **S5 (Step 3):** correct the stale workflow line-1 header saying `CANDIDATE v0.2` / `not run on GitHub yet`; use an accurate production header.
- **S6 (Step 3):** address Node 20 deprecation notices for `actions/checkout@v4` and `actions/upload-artifact@v4`: check then-current supported major versions and their Node 24 runtimes before changing these actions; the exact replacements were unverified in Claude's review.
- O7 (six indexes in CI or local) remains for Dave to decide. A local six-index run on an applicable inspector project or compiler/toolset change is required if CI does not run it. SDK-only change is excluded by D-SDK (c).

## Step 4 - final common handback and migration close (NOT STARTED)

- Human VS2026 GUI build, proven plain-CMD 64-bit MSBuild discovery/build, separate VsDevCmd/dumpbin example, prohibited environment/flag overrides, actual successful output, gate instructions and CI failure handling.
- Preserve CNR3-derived wheel details for technical Stages 7-9: `py3-none-win_amd64`, `vapoursynth/plugins/<name>/<name>.dll`, AGPL-3.0-or-later, NOT MIT.
- The final common handback must record Dave's 2026-10-10 ratification of the plugin `/fp:precise`, no-automatic-contraction policy and remove the floating-point item from its open-decision list. Record D-SDK (c) and the observed SDK/UCRT inference without overstating byte equivalence. Retain the separate caveat about explicit FMA and Python-oracle bit equality. No intermediate Handback version is required.
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
- D-SDK: **CLOSED** by Dave on 2026-10-10, option (c), SDK version recorded each build without SDK-only regression rerun.

## Stage C-derived safeguards carried into the single workflow

- 64-bit everywhere; x86 host only last D4 local uncommitted diagnostic.
- Latest means latest INSTALLED RELEASED VS, with no `-prerelease`; no hard-coded version/install root. Build Tools eligible.
- Use VS-designated current MSVC build for its toolset, recorded not pinned; file version and toolset directory version both logged.
- N1 Windows command-line splitting only, or fail on non-Windows.
- N2 check actual HostX64 invocation lines, not any `HostX86` text.
- N3 record MSVC directory version AND actual executable file version.
- N4 rely only on established Guard CF table/flag evidence, not speculative bit-field interpretations.
- D-SDK (c): capture exact Windows SDK version on every build; distinguish SDK-derived UCRT changes under `/MT` from toolset/compiler-change regression triggers. SDK changes alone do not add a rerun requirement.
- Guard ambient build environment and ancestor `Directory.Build.*` files; `-noAutoResponse`; prove K4 scratch case before final workflow acceptance.

## Next review checkpoint

- Claude independently reviews this **single updated living `Migration_Status.md`** for an accurate Step 1 closure and D-SDK disposition. No other document revisions or Stage A source/project changes are part of this update.
- Next implementation is **Stage B+**, after Dave dispositions O1-O7. Use the agreed candidate -> Claude review -> Dave ratification -> implementation/gates workflow; commit to `main` directly, retaining the inspector regression and switch-check rules. At Step 3 incorporate S4-S6. The final common handback is written at migration close, not versioned again now.
