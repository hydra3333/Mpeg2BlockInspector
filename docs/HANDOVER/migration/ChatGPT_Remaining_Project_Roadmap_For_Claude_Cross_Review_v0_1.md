# Remaining Project Roadmap - ChatGPT Understanding for Claude Cross-Review

**Filename:** `ChatGPT_Remaining_Project_Roadmap_For_Claude_Cross_Review_v0_1.md`
**Version:** 0.1
**Date:** 2026-10-10 (Adelaide)
**Author:** ChatGPT, migration chat
**Status:** CROSS-REVIEW PROPOSAL; not independently ratified project authority
**Subject:** `hydra3333/VapourSynth-mpeg2Deblock` after acceptance of Stage A A3 v0.10
**Purpose:** Describe my understanding of the remaining BUILD/REPOSITORY MIGRATION and the subsequent MPEG-2 FILTER DEVELOPMENT, identify exact sequencing and gates, and ask Claude to challenge any discrepancy against the ratified source documents.

---

## 0. Essential distinction: two stage-numbering systems

This project has TWO DIFFERENT plans. They must not be conflated.

1. **Repository/build/distribution migration**, from `Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_19.md` (DR): Stage A (accepted, close-out under way), Stage B (VapourSynth DLL placeholder), Stage C (canonical local MSBuild harness), Stage D (GitHub release workflow), Stage E (Windows wheel/PyPI scaffold), followed by final migration handback. There is also one small post-Stage-A compiler-selection candidate; it is not a new algorithm stage.
2. **MPEG-2 deblocking technical development**, governed by `05_DECISIONS.md`, `06_DEBLOCK_CONCEPT.md`, `02_INDEX_FORMAT_SPEC.md`, and `Stage2_Experiment_Design_v0_3.md`: Stages 0-9, with a feasibility decision after Stage 2. Its Stage 2 means Python reference experiments, NOT migration Stage B or migration Stage C.

**Proposed execution dependency:**

```
Migration Stage A acceptance / close-out
    -> establish final pushed/tagged baseline (tag optional)
    -> small reviewed post-Stage-A compiler/toolset candidate
    -> Migration Stage B: loadable, entry-point-only DLL placeholder
    -> Migration Stage C: canonical, guarded, version-discovering build harness
    -> Migration Stage D: GitHub release workflow using that harness
    -> Migration Stage E: local Windows wheel / PyPI packaging scaffold
    -> final migration handback, Claude review, Dave ratification, push
    -> return to technical-development chats when Dave authorises
    -> technical Stage 2 S2-I1 ... S2-I10 and feasibility gate
    -> ONLY IF FEASIBLE: technical Stages 3-9
```

The order above reflects the DR's migration stages and the development handover's explicit instruction to defer S2-I1 until migration is closed. The exact placement of the small compiler-selection candidate immediately before Stage B is my understanding from recent discussion and should be cross-verified by Claude. No implementation is authorised merely by writing this roadmap.

## 1. Authorities and snapshots used

**Migration authorities** - latest available reviewed document set:

- `Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_19.md` (DR), especially sections 17-38 and the 2026-10-10 policy/close-out addenda.
- `StageA_Visual_Studio_Normalization_Execution_Plan_v0_14.md` (Plan), especially sections 30-34 and the one-off waiver.
- `MPEG2_Deblocking_Developer_Handback_v0_13.md` (Handback), especially sections 9-16 and H2/H3c.
- `StageA_VS2026_MSBuild_Hard_Earned_Knowledge_v0_5.md`.
- `ChatGPT_Migration_Chat_Handover_v0_12.md` (migration continuity only).
- `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_10_Final_Gate_v0_1.md` and `Claude_REVIEW_OF_ChatGPT_StageA_Closeout_DocSet_v0_1.md`.

**Technical-development authorities** - from the available repository snapshot:

- `docs/REPOSITORY/05_DECISIONS.md` v1.1 RATIFIED (D-01, D-09, D-20, D-24-D-26 in particular).
- `docs/REPOSITORY/06_DEBLOCK_CONCEPT.md` v1.1 RATIFIED.
- `docs/REPOSITORY/02_INDEX_FORMAT_SPEC.md` v0.4: ratified constraints; final index layout NOT FROZEN.
- `docs/REPOSITORY/Stage1_Evidence_and_Gate_Report_v0_3.md`: Stage 1 accepted evidence.
- `docs/REPOSITORY/Stage2_Experiment_Design_v0_3.md`: experiment ladder and implementation increments S2-I1 to S2-I10.
- `docs/MPEG2_Macroblock_Index_VapourSynth_Deblocking_Project_Proposal_v0_5.md` section 3: original agreed technical-stage ordering, subordinate to later ratified repository decisions.
- The separate ChatGPT and Claude technical-development handovers, v0.4 in the available snapshot, for continuity (not authority).

**Source limitation:** The available GitHub repository ZIP may precede Dave's most recent push. Dave reports having pushed. I have not independently verified the live remote HEAD, the exact new commit, or the presence of all seven close-out files in that commit. This roadmap does not claim that an unverified Git action is complete. It also does not override later ratified files on Dave's machine.

## 2. Present status - Stage A is accepted, not to be repeated

**DECIDED / ACCEPTED:** Dave chose option (b), ratified A3 v0.10, and directed Stage A close-out. Claude's final gate review independently reproduced W1 and other evidence. Claude's later close-out document review was ACCEPTED with no MUST/SHOULD findings.

Accepted A3 evidence:

- Debug and Release clean rebuilds: successful, 17 warnings and zero errors each.
- W1 effective CL/LINK command-line check: PASS, 113 tokens total; `/LTCGOUT` removed; native `HostX64\x64` compiler/linker invocations established.
- Warning comparison to v0.9: matching 17-warning signatures in both configurations.
- Release W2: PE32+/x64, AVX2 build policy evidence, LAA, HEVA, ASLR, NX, CFG with 37 functions, CET, `/GS`, nonzero cookie, KERNEL32-only imports, basename-only PDB, embedded asInvoker/SegmentHeap.
- Ratified `.vcxproj` working-copy SHA-256: `73e9019cda7d1061ecdb06526c60f4ee84baa4c385b7ca0dde4269544e4fdb46`.
- Frozen-file hashes and Git comparison PASS; working tree clean when last reported; no `.iobj` / `.ipdb` files.
- **Six-index rerun for A3 v0.10: WAIVED, NEVER PASS.** Dave ratified a one-time deviation from Plan section 30. v0.9 passed the six tests; v0.10 retained identical CL token sets and differed in LINK only by deleting `/LTCGOUT` while plain `/LTCG` remained. Claude compared normalized Release dumpbin `/headers`, `/loadconfig` and `/imports` and found no differences. This is **strong evidence of identical code generation, not byte-for-byte proof**. The deviation has NO continuing authority for subsequent compiler/toolset/code-generation changes.

**No more repetitive frozen-source audits or extra A3 builds** without a specific newly discovered cause. Dave explicitly stopped those redundant checks.

**Close-out verification still to confirm, not assume:** The final local Git state, whether all five close-out docs and the two required Claude reviews were committed and pushed to `docs/HANDOVER/migration/`, and any chosen tag. Claude checked the pushed-snapshot README against the build and prescribed the live README/HEAD comparison; Dave subsequently said "pushed", but has not provided the final commit ID here.

Suggested smallest final baseline record (not a new build gate): `git status -sb`, `git log -1 --format="%H %s"`, and confirm the expected close-out files and the README are part of that commit. Tagging `post-stageA-vs-normalization` is optional and requires Dave's choice. Do not infer a successful push solely from a clean local status.

## 3. Small post-Stage-A toolset-selection candidate - FIRST proposed technical change

**Ratified POLICY, not yet installed in project:**

> Use the newest installed MSVC toolset (minimum v145) and the MSVC build Visual Studio designates as current for that toolset (normally the newest installed, in-support build), with 64-bit host tools. The toolset name and exact compiler version are recorded on every build. If either differs from the last accepted build, the switch check, warning comparison and six-index regression must all pass again before that build is accepted.

At A3 v0.10, `PlatformToolset=v145` is still fixed in the inspector project; that is a historical accepted baseline, not yet the final floating selection implementation. No project-level `VCToolsVersion` override is authorised; Visual Studio's designated current build is to be recorded, not pinned.

**Proposed bounded procedure:**

1. Preserve the Stage A accepted project, executable/toolchain identities and W1 expectations; work on an independent candidate, not an unreviewed live edit.
2. Empirically prove on Dave's installed released VS2026 that `$(DefaultPlatformToolset)` is defined at the point where `PlatformToolset` is evaluated in a C++ project, and prove which MSVC generation it selects. Do not assume that an implementation proposed in Claude M5 works, or that "VS default" always means the numerically newest installed qualifying toolset.
3. Prove a project-owned **numeric/semantic** minimum-v145 guard. An ordinary lexicographic string comparison is unacceptable. Confirm the exact XML/import order and diagnostic on an intentionally below-minimum scratch case.
4. If the evidence supports it, propose minimal `.vcxproj` change: `PlatformToolset=$(DefaultPlatformToolset)` plus the validated minimum guard. Keep `PreferredToolArchitecture=x64` explicit, no `VCToolsVersion` override, and all current explicit CPU/runtime/security settings.
5. ChatGPT drafts the exact candidate and its test evidence; Claude cold-reviews; Dave ratifies; only then apply and build. Record actual selected toolset name, exact compiler file/tool version, SDK, and emitted CL/LINK switches.
6. Run the required switch checks, warning comparison and **all six** inspector index regressions when toolset/compiler changes (or other governing inspector-project change invokes the stricter project-change rule). A3 v0.10's waiver does not transfer.
7. Review outcome, commit/push accepted candidate separately, retain rollback identity, and update the expected-switch baseline only through explicit review.

**Clarification for Claude:** Is this a distinct preliminary candidate before Stage B, as agreed conversationally, or should the formal migration sequence assign it within Stage B/C? Either way, it must be completed before the final Stage C/D automatic-toolchain policy can be claimed implemented.

## 4. Migration Stage B - second, loadable VapourSynth project only

**Goal (DR 17-21; Handback 13):** Add an API4 C++ VapourSynth DLL project to the x64-only `.slnx` without implementing the deblocking algorithm, index reading, frame processing, or any registered filter functions.

**Proposed work in bounded reviewed steps:**

1. Reacquire/read the **current** CNR3 DLL project and filter files, relevant scripts/workflow, header/vendor `VERSION.txt`, and build-history rationale. CNR3 is a settings reference; make a line-attributable **subtractive** project diff. Do not use abandoned Deblock4 as an active implementation source.
2. Review/ratify the coupled name/identity set BEFORE finalizing project identity: project/source folder, DLL filename, `VapourSynthPluginInit2` plugin identifier/namespace/display name, PyPI/distribution/package name, autoload folder, EXE exposure strategy. Do not settle independently incompatible names.
3. Review decisions not automatically inherited from CNR3: C++ standard; VapourSynth API4 header release/profile; floating-point/FMA contraction; COMDAT folding; `/guard:ehcont` (O8); version resource; optional CPU-capability check before AVX2-only code. Mark unresolved items PROVISIONAL, not silently settled.
4. Add `src/mpeg2Deblock/` and `vs/VapourSynth-mpeg2Deblock/mpeg2Deblock.vcxproj` + `.filters`, and register the project in `VapourSynth-mpeg2Deblock.slnx`. Exact spelling/case subject to the identity decision.
5. New DLL placeholder contains only API4 entry point, `configPlugin`, and NO filter registrations. It proves linkage/loading, NOT filtering. No source-code port from CNR3's filter algorithm.
6. Project itself must own Release standalone runtime (`/MT`), x64/AVX2, `/favor:blend`, `/GS`, CFG, CET, Spectre mitigation explicitly disabled, `/sdl` ON for new C++ plugin, and `/PDBALTPATH:%_PDB%`; preserve explicit configurations and correct manifest owner, including the established `/LTCGOUT` suppression where necessary. Debug policy remains separately explicit. No CI-only substitute switches.
7. Build Debug/Release x64; check actual CL/LINK invocations and binary properties, `/exports` containing `VapourSynthPluginInit2`, Release imports/dependencies and security, and a simple VapourSynth plugin-load smoke test (namespace but no filters).
8. Protect existing inspector: compare its accepted `.vcxproj` and `.filters` identities. If unchanged, one LP smoke test suffices for Stage B infrastructure changes per H3c; if changed, six inspector index regressions. Do not let this relaxed infrastructure rule override the stricter H2 rule for intentional inspector-project changes.
9. Deliver reviewed DLL candidate, exact CNR3-to-new-project diff, test evidence, decisions/provisional list, and Dave-ratified commit.

**Exit:** Two correctly configured x64 projects in one umbrella solution, with a loadable **nonfunctional** DLL skeleton. Stage B does not implement a deblocking filter. Build skeleton and final API4 Stage 7 wrapper are distinct milestones.

## 5. Migration Stage C - canonical local build harness

**Goal (DR 22-28 plus 2026-10-10 addendum):** A single, documented build route that discovers tools, invokes MSBuild on the `.slnx`, and verifies the *project-owned* effective settings. This route also becomes the Stage D route. Dave should be able to use Visual Studio normally, not run a special manual flag command each day.

1. **One installation selection:** invoke `vswhere.exe` with `-latest -products * -requires Microsoft.Component.MSBuild Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath`; no `-prerelease`, version range, Visual Studio edition or fixed install directory. "Latest" means the newest installed, **released** qualifying installation on an updated build machine. Build Tools editions are eligible. Fail if none qualifies; log the selected product/version/root. Prove the VC component ID and query behaviour locally.
2. **Same root for everything:** derive `%VS_INSTALL%\MSBuild\Current\Bin\amd64\MSBuild.exe`, VsDevCmd and x64 dumpbin from THAT installation. No second VS search or fallback. Confirm MSBuild *runtime* process is 64-bit; the Bin/amd64 path alone is not proof. Independently confirm actual CL/link invocations are `HostX64\x64` (MSBuild engine bitness and compiler/linker host bitness are separate requirements). Use 64-bit Python/helpers.
3. **Current compiler selection:** honor the post-Stage-A project-owned toolset policy (minimum v145; Visual Studio-designated current in-support compiler build; no `VCToolsVersion` override). Record PlatformToolset, MSVC folder version, actual CL/link/dumpbin file versions and paths, and SDK version. N3: folder `14.51.36231` versus dumpbin's reported `14.51.36260.0` are different version identities, not automatically an error.
4. **Build isolation:** start from plain CMD, not a VsDevCmd-mutated build environment. Avoid environment and global-property flag injection; guard `CL`, `_CL_`, `LINK`, `_LINK_`, `Platform`, `PreferredToolArchitecture` and other meaningful overrides. Fail on unexpected ancestor `Directory.Build.props`, `Directory.Build.targets` or `Directory.Build.rsp`; reject unreviewed in-repository equivalents. Pass `-noAutoResponse` and demonstrate the failure path once on a disposable scratch project with a scratch ancestor props file, NEVER above the production repo. Record the scan. Keep VsDevCmd `-arch=amd64 -host_arch=amd64` only in a separate command context for interactive inspection tools.
5. **Build both configurations:** one harness accepts solution/configuration and runs MSBuild with explicit `/p:Configuration=... /p:Platform=x64`, capturing return codes immediately, building from the reviewed `.slnx`. It does not reproduce CNR3's independent, hand-maintained `cl`/`link` switch table or override `/GL`, `/LTCG`, `/MT`, AVX2, CFG/CET etc.
6. **Permanent gates every build:** mechanical token extraction of actual CL and LINK invocation tlogs against a reviewed expected switch set (missing/extra switches fail); verify real HostX64 invocation lines, not arbitrary occurrences of `HostX86` (N2: the latter appears in harmless props reassignment text); Release standalone/import checks (inspector's accepted direct imports are KERNEL32 only), output/export/security checks for the DLL, and sufficient evidence of required security flags. Don't assume `10017500` Guard Flags means more than dumpbin actually names (N4: `CF instrumented`, `FID table present`; nonzero CF table count is gate).
7. **Tokenisation N1:** extractor must use Windows command-line splitting rules on every supported execution platform, or fail closed on non-Windows. The historical non-Windows `shlex.split(posix=False)` path produced a false 117-token report; Windows interpretation produced the correct 113 tokens.
8. **Change-triggered additional gates:** if MSVC toolset name, exact compiler version, or code-generation-relevant setting differs from last accepted build, perform reviewed switch-delta check, warning comparison and the full six-index regression BEFORE accepting that build. The A3 one-off waiver cannot be reused.
9. **Independent test and review:** demonstrate discovery, build, isolation/negative tests, reproducible logs and failures on Dave's actual machine (S13-style evidence discipline), including every item explicitly UNVERIFIED in DR M1-M5/K4. Claude reviews; Dave ratifies the working harness.

**Exit:** One approved, version-discovering, x64-only local/MSBuild route, with deterministic refusal on missing tools or injected configuration, and clear evidence of exactly what ran. Project configuration remains the single compiler/linker authority.

## 6. Migration Stage D - release-triggered GitHub Actions

**Goal (DR 29-30):** Adapt current CNR3 release workflow to run the SAME Stage C harness on Windows x64 GitHub-hosted runners. Do not copy CNR3's hand-maintained alternate `cl`/`link` flag map.

1. Reacquire current workflow and the actual runner image/tool installations when this stage starts; historical runner/version statements are not accepted evidence. Runner must be x64 and its required released Visual Studio/MSVC capability must be proved or fail closed.
2. Call the Stage C harness to select one VS installation, use 64-bit MSBuild/CL/LINK and build Release x64 umbrella `.slnx`; don't override project-owned build settings.
3. Record VS/product/installation, MSBuild bitness/version, MSVC toolset/compiler file versions, SDK, and the exact CL/LINK switches. Apply Stage C isolation, auto-import/response-file rules, Windows-tokenisation rules and real-invocation HostX64 detection.
4. Verify expected artifacts (`Mpeg2BlockInspector.exe`, placeholder `mpeg2Deblock.dll`), DLL export `VapourSynthPluginInit2`, Release runtime/forbidden-import checks, CPU/security/CET/CFG/PDB policies and intentional `/Qspectre` absence; inspect outputs, not simply project XML.
5. Define how the CI run determines whether its toolset/compiler is a changed build identity relative to the last accepted baseline. If changed, require the warning and SIX-index revalidation before accepting release artifacts. If test media/resources are unavailable on a hosted runner, the workflow must fail/block acceptance or rely on a separately reviewed, proven evidence gate; it must not silently waive the regression. The exact CI implementation is a review item, not yet decided.
6. Test success and explicit failure paths, retain logs/artifacts, review workflow permissions/triggers and no-surprise publication behaviour. ChatGPT candidate -> Claude review -> Dave ratifies -> commit.

**Exit:** Release workflow consumes the very same project/harness settings; no divergent GitHub-only compilation policy. Triggering release automation is not authorization to publish to PyPI.

## 7. Migration Stage E - Windows wheel/PyPI packaging scaffold

**Goal (DR 31-33):** Adapt the current CNR3 Windows wheel construction into a reproducible LOCAL wheel for this project; no PyPI upload without Dave's explicit authorization.

1. Resolve the coupled distribution identity decided at Stage B: public distribution name, Python package, VapourSynth autoload path `vapoursynth/plugins/<name>/`, DLL file, namespace and how users access the inspector EXE. Check external name availability at the decision point, not earlier.
2. Package the Release artifacts made by the accepted Stage C/D route, not separately recompiled binaries. Expected CNR3-derived Windows wheel form is `py3-none-win_amd64`; verify applicability with actual wheel metadata and installed paths rather than blindly copying CNR3.
3. Include correct AGPL-3.0-or-later metadata for project-developed material; preserve LGPL-related obligations for vendored VapourSynth headers as applicable, MPEG Software Simulation Group notices and `LICENSE`/`NOTICE`. DO NOT copy CNR3's MIT metadata.
4. Test local wheel build, integrity, install and uninstall in a clean/isolated Windows environment; verify DLL placement, import/export and VapourSynth load behaviour, with the explicit understanding that the plugin still registers NO deblocking filters.
5. Document the later functional packaging/test obligations when the actual algorithm exists. Public PyPI upload, tagging/releases and use of real user clips need their own Dave decision. Do not make migration success depend on a working deblocking algorithm that this migration expressly does not implement.

**Exit:** A locally validated, correctly identified/licensed Windows x64 wheel packaging scaffold with explicit publication boundary.

## 8. FINAL migration close-out and handback to development

The *whole migration* finishes only after Stages B-E, NOT after Stage A. DR sections 34-37 require:

1. Collect project files, naming decisions, exact selected build configuration/toolchain, source/project hashes and Stage B-E test evidence; record any PROVISIONAL settings rather than pretend they were decided.
2. Refresh README/NOTICE/licence and migration-owned documents to reflect actual accepted outputs and names. Preserve documentation provenance and distinction between current authority and history; do not casually edit frozen source.
3. Produce ONE neutral common Developer Handback under `docs/HANDOVER/`, credited as drafted by migration ChatGPT, cold-reviewed by migration Claude, ratified by Dave, with date. This is different from the role-specific ChatGPT/Claude development handovers and the migration chat continuity files.
4. Claude independently reviews the FINAL repository/evidence/handback; Dave resolves findings and ratifies the handback. Commit/push, record final Git revision and optional tag.
5. Give the common handback to BOTH technical-development chats. Migration does not edit their own `ChatGPT_Handover_To_Future_ChatGPT_MPEG2_Deblocking_Project_*` or `Claude_HANDOVER_TO_Future_Claude_Chat_*` files; each chat may update its own handover after reading the common one.
6. Dave expressly authorises return to technical development. No inferred authorization from the availability of the DLL skeleton or CI workflow.

**Gate:** A final build and packaging handback suitable for development and future releases, but still no MPEG-2 deblocking implementation.

## 9. Technical-development stages after migration

**Authoritative distinction:** D-01 (in `05_DECISIONS.md`) ratifies the technical order in Project Proposal v0.5 section 3, with later D-24-D-26 refinements. Project authority is the current ratified `05_DECISIONS.md`, `06_DEBLOCK_CONCEPT.md`, and `02_INDEX_FORMAT_SPEC.md`; later Stage 2 experiment design controls the experiment specifics.

### Technical Stage 0 - concept (already ratified)

`06_DEBLOCK_CONCEPT.md` v1.1 ratifies a frame-owned, index-directed, field-parity-aware research concept. FRAME/FIELD/NONE describes **actual coded residual transform geometry**; skipped and effective-CBP-zero non-intra macroblocks have NONE even if the syntax does not expose a `dct_type` bit. Luma seam existence is authoritative from index/coding structure. Pixels judge blocking versus real image detail, not the codec's transform selection. One global strength, and chroma in scope subject to evidence. Equations, threshold policy and actual kernels are NOT already approved.

### Technical Stage 1 - provisional inspector/test evidence (already accepted)

The minimally instrumented MPEG-2 reference decoder and `Stage1_Inspector_Analyzer_v0_2.py` produced verified display/output-order draft records on the formal tested material; Stage 1 evidence report v0.3 is ratified. This is a TEMPORARY Stage 1/2 index layout, NOT the final `.idx2` and NOT an unrestricted proof across all streams/field structures. Keep the accepted Stage 1 inspector frozen unless an actual defect is demonstrated.

### Technical Stage 2 - Python reference experiment and feasibility gate (NEXT technical work, NOT yet implementation)

**Status distinction:** The `Stage2_Experiment_Design_v0_3.md` file's header still says DRAFT awaiting Dave ratification, but later ChatGPT and Claude development handovers independently record Dave's ratification on 2026-10-08. The latter seems to be the latest recorded decision. Claude should confirm this record and flag the stale header for the owning development chat rather than silently amending authority. Both handovers report that **NO S2-I1 coding has started**.

Ratified architectural direction D-24 is INDEX-DRIVEN. Stage 2 does not reopen a pixel-only-versus-index architecture contest, and there is no planned external-deblocker yardstick. The remaining feasibility question is whether the index-directed kernel yields useful quality at acceptable cost and with acceptable no-harm behaviour.

**Planned research execution, using the Stage 2 v0.3 increments:**

- **S2-I1:** read-only Python index reader and validation. Reproduce analyzer totals on formal samples; frame count/ordinals/dimensions, picture type, `progressive_frame`, and leading B-picture exclusions. Refuse mismatches.
- **S2-I2:** luma indexed seam-map diagnostics; verify spatial index-to-pixel alignment in both dimensions, controls shifted by -1/0/+1 MB, and 8-pixel column grid phase; no filtering yet.
- **S2-I3:** initial luma K0 candidate with indexed geometry and FIXED clip-wide median quantiser on selected even-numbered usable LP GOPs; freeze K0 before testing its QP benefit.
- **S2-I4:** hold K0/geometry/pixel gating/strength constant and compare fixed median QP versus real per-macroblock effective QP on odd-numbered LP GOPs. Report NONE-neighbour cases separately; do not retune between variants.
- **S2-I5:** develop luma edge rejection, thresholds, correction and a small global-strength sweep using real-QP map on development LP; OFF must be bit-exact and collateral detail preservation assessed.
- **S2-I6:** begin with conservative NONE policy N0 (no internal coded transform seam; outer macroblock edges may remain eligible). Consider a bounded alternative only if N0 leaves evidenced problems; do not invent a pixel transform-type detector.
- **S2-I7:** bounded native 4:2:0 chroma experiments (unfiltered, fixed-QP and real-QP variants); ensure safe progressive/interlaced field-parity handling and avoid colour smearing. Chroma geometry is not inferred from luma FRAME/FIELD/NONE.
- **S2-I8:** lock tuned settings and run no-retuning hold-out assessment: LG_576i_4_EP, original TEST_4A_A003 and TEST_2A_A001, plus MLS progressive control.
- **S2-I9:** secondary paired-reference reporting on software transcodes, with metrics appropriately qualified (both blocky transcodes use constant QP 62 and cannot establish the value of a variable spatial QP map).
- **S2-I10:** feasibility gate report: real LG visual/seam-local/no-harm evidence is primary, paired-reference and I/P/B/QP diagnostics secondary; list metadata consumed versus diagnostic/unnecessary/unresolved. Dave decides continue, revise/research, or stop. A negative result is a valid project outcome.

Prototype: Python 3 / VapourSynth / BestSource / NumPy as convenient, deterministic, scalar/research code, not C++ production/AVX2. Review increment by increment; use the accepted temporary index. No independent field-processing passes; frame-owned processing with parity-aware access. Stage 2 does not freeze the final index schema.

### Technical Stage 3 - freeze production `.idx2` specification (conditional)

Only after Stage 2 feasibility succeeds and Dave approves: choose final fields and format based on metadata actually used. Ratify binary header/record layout, versioning, effective quantiser semantics, FRAME/FIELD/NONE validity, dimensions/count/display ordinal, failure behaviour, and correspondence contract. `02_INDEX_FORMAT_SPEC.md` v0.4 currently holds constraints, not final packing. Do not copy the illustrative proposal layout as though already approved.

### Technical Stage 4 - production inspector minimal patch (conditional)

Rebuild the final index-writing inspector from the pristine reference decoder with the smallest reviewable instrumentation diff. Supported binary input through file or ffmpeg-piped ES, clear errors/exit codes and deterministic output; no text index. Verify output against the frozen final spec. Stage 1's temporary indexer does not become final merely because it worked on Stage 1 samples.

### Technical Stage 5 - rigorous index/frame correspondence (conditional)

Demonstrate **index record N == VapourSynth output frame N** on representative progressive/interlaced streams, including tricky display-order/leading-B, picture/field, repeated-field and error paths as applicable. Fail closed on missing/extra/mismatched records. The source-identity policy remains Dave's simple responsibility model, not an unratified complex hash system. Do not treat limited Stage 1 correspondence as proof of Stage 5.

### Technical Stage 6 - production C++ scalar kernel (conditional)

Port the *successful* Stage 2 Python oracle to a C++ scalar reference; compare outputs bitwise where exactness is required or within an explicitly ratified tolerance. Preserve frame-owned/parity semantics, strength/no-harm rules, and strict index validation. Review before optimisation.

### Technical Stage 7 - functional VapourSynth API4 wrapper (conditional)

Extend the Stage B loadable placeholder into an actual API4 filter with index input, parameter validation, correct frame requests, deterministic errors, and output frame processing. Correct scheduling/memory/frame ownership must be proven. The Stage B DLL placeholder's successful load is NOT a Stage 7 functional-filter pass.

### Technical Stage 8 - AVX2 optimisation (conditional)

Implement AVX2 for the accepted scalar algorithm, retaining scalar as oracle/test reference. Establish bit identity or explicitly ratified numerical tolerance; verify CPU policy and performance on realistic captures. No premature SIMD assumptions during Stage 2. Preserve /GS, CFG, CET and build hardening.

### Technical Stage 9 - real-capture product acceptance (conditional)

Run final acceptance on actual LG VHS-C captures and controls: visually meaningful blocking reduction, acceptable detail preservation and chroma handling, no temporal/field artefacts, predictable strength, robust index mismatch rejection and satisfactory speed. Dave judges subjective quality and ratifies acceptance. Only then consider a functional production wheel/PyPI publication under a separately approved release decision.

## 10. Open issues / cross-review questions for Claude

**Please return ACCEPT / CORRECTIONS with source section references, not just a general impression.** Particular questions:

1. **Sequence:** Is the small compiler/toolset-selection candidate formally FIRST after Stage A (and before Stage B), or should it be recorded inside Stage B/C? Does it require its own baseline/commit/tag?
2. **Stage A close-out:** Dave says "pushed". Which exact HEAD/README/document verification remains necessary to call the repository baseline closed, versus already being established in Claude's reviewed pushed snapshot? Optional tag only at Dave's direction.
3. **Stage B identity and proof:** Are the coupled naming decisions and open technical settings exhaustive? Are any listed Stage B settings already ratified differently? Is the proposed minimal load test/LP smoke trigger accurately derived from DR 17-21, 27-28 and Handback H2/H3c?
4. **Stages C/D:** Does the roadmap accurately carry Dave's discover/verify/record, current compiler-build choice, 64-bit-everywhere rule, environment/auto-import/response isolation, N1-N4, permanent output gates and toolchain-change-triggered six-index requirement? Identify any requirement that has been mislabeled as tested rather than UNVERIFIED.
5. **Stage E:** Is a locally installable placeholder wheel in scope before functional deblocking, as DR 31-33 suggests? What exactly must be verified for wheel naming and inspector EXE exposure?
6. **Development handback:** Does DR 34-37 really make all migration Stages B-E and the shared handback prerequisites to resuming technical Stage 2 S2-I1? Is any overlap explicitly authorised, or only possible on a separate Dave decision?
7. **Technical Stage 2 status:** Please reconcile the v0.3 design file's draft header against both later development handovers saying Dave ratified it on 2026-10-08. No S2-I1 implementation should be inferred.
8. **Stage 3/5 mapping:** Is the D-01 sequence of index freeze at Stage 3 followed by stringent correspondence proof at Stage 5 faithful to the ratified index constraints, without prematurely claiming universal correspondence?
9. **Any omissions:** List missing critical review gates, open decisions, prerequisites, or provenance documents, especially where a historical clause in DR conflicts with a dated addendum.

## 11. Method and limits

- **Agreed decisions** are distinguished above from **my inferred scheduling** and **unverified implementation mechanisms**. This document is deliberately NOT a new master plan or an amendment to a ratified decision.
- The currently accepted source of compiler/linker policy is the project file; neither harness nor CI invents a second switch map. User intends routine Visual Studio builds, not manual batch builds.
- No source-code work, algorithm edits, project settings, Git commit/push, or tagging is performed by this roadmap.
- This is specifically intended for Claude to cold-compare against the ratified DR, Plan, Handback, repository authority and development stage design, and for Dave to ratify any reconciliation before work begins.
