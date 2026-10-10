# Stage 1 proving-workflow candidate v0.2 for Claude (2026-10-10)

**Decision disposition:** ACCEPT the migration plan G1-G11/P1-P6 and O1-O7 as recorded in Claude's 2026-10-10 response. This package does NOT rewrite that agreed plan.

**Dave's branch correction (supersedes test-branch references in the original agreed plan):** main is the sole ongoing development branch. After Claude's candidate review, Dave commits the proof workflow to main and manually dispatches it on main. There is no test branch, source_ref input, push trigger or release trigger at this proving step. Git commits/snapshots and release attachments provide historical recovery. See https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_dispatch .

**Package files (flat):** `Migration_Status.md` (P1 living status), `prove-project-build-windows-x64.yml` (manual-only G6 candidate), `expected_a3_v0_10_switches.csv` (byte-identical accepted A3 v0.10 post-tokens, 113 tokens), Claude's original response unchanged, this README, and SHA-256 manifest.

**Target repository paths once approved:**
- `docs/HANDOVER/migration/Migration_Status.md`
- `.github/workflows/prove-project-build-windows-x64.yml`
- `.github/workflows/expected_a3_v0_10_switches.csv`

**Review focus:**
1. First GitHub `workflow_dispatch` registration directly on main, preserving manual-only semantics; checkout is pinned to the triggering commit SHA.
2. Empirical 64-bit MSBuild probe, vswhere version-independence and `windows-latest` image capabilities. Do not assume the hosted runner is identical to Dave's installation.
3. Windows `CommandLineToArgvW` token extraction, tlog normalisation and exact comparison against 113 reviewed tokens; report any false mismatch (including incidental path/SDK differences) before altering the baseline.
4. Actual executable HostX64 invocation matching, never incidental `HostX86` property-reassignment lines.
5. `-noAutoResponse`, auto-import and environment guards. K4 scratch negative test is not yet executed.
6. Dumpbin Release PE/CFG/CET/PDB/import verification, actual MSVC tool-folder/file versions and evidence uploads.
7. Check that proposed inline code is runnable in GitHub Actions. It has passed local static structure checks only; Windows/runner execution is NOT claimed. No release/push trigger; no CI-controlled compiler/linker flag map.

**Scope:** Only a proving candidate for the accepted inspector project. The Stage B+ project/toolset changes are NOT part of this candidate; no DLL, final Release workflow or wheel is built. All subsequent approved candidates will also be committed to main, without creating a test branch.

**Other standing open items:** Claude document O1-O7 all remain for Dave, without implicit decisions. No production changes or commits/pushes made by ChatGPT.
