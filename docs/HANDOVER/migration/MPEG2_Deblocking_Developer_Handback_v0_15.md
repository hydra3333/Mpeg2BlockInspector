# MPEG-2 Index-Driven Deblocking Project - Common Developer Handback from Migration



**Filename:** `MPEG2_Deblocking_Developer_Handback_v0_15.md`
**Version:** 0.15
**Date:** 2026-10-10 (Stage A closed and pushed; remaining migration plan agreed with Dave)
**Drafted by:** migration ChatGPT chat (v0.1-v0.13); section R and supersession markers written by migration Claude at Dave's request (v0.14). This v0.15 adds narrowly scoped ChatGPT review corrections; see the v0.15 change log.
**Supersedes:** `MPEG2_Deblocking_Developer_Handback_v0_14.md`
**Intended recipients:** the main ChatGPT and Claude technical-development chats
**Repository location when final:** `docs\HANDOVER\`
**Status:** PROVISIONAL. Stage A is CLOSED (A3 v0.10 accepted; six-index rerun for v0.10 WAIVED, not PASS; close-out committed and pushed by Dave). The migration is NOT finished: Stage B+, the CI workflow and the final handback remain (section R.5).
**Authority:** migration/build-state orientation only; not MPEG-2 technical-design authority
**Read first:** section R. Where sections 0A-17 below conflict with section R, **section R governs**. The older sections are kept as history until the final handback rewrite.
**Review status of v0.15:** ChatGPT correction draft for Dave/Claude cross-review; not yet ratified and not the final migration handback.

---

## R. READ FIRST: what migration has done, what changes for you, and why

This section is written for the two technical-development chats. It tells you what the migration did while you were paused, what you will inherit, what is still coming, and what you will have to deal with yourselves later, each with the reason. Details and history are in the sections below and in the migration documents named in R.9.

### R.1 The short version

1. The repository is now `hydra3333/VapourSynth-mpeg2Deblock`, with a VS2026 x64-only solution (`vs\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock.slnx`).
2. The Stage 1 inspector (`Mpeg2BlockInspector.exe`) builds with its reviewed, product-defining build settings explicitly pinned in its project file and validated against Visual Studio's rule files and actual compiler/linker output. This is not a claim that every possible MSBuild property is explicitly specified.
   - Its accepted Release binary is AVX2, standalone (imports `KERNEL32.dll` only, so no Visual C++ Redistributable is needed), and hardened: `/GS`, CFG, CET, ASLR with high-entropy VA, NX.
   - Its six reference indexes are byte-identical to the Stage 1 baseline. (They were verified on v0.9; the v0.10 rerun was waived with evidence, see R.2.)
3. **The inspector's C source is still frozen.** Migration changed only build settings, never code.
4. Still to come before you get the repository back:
   - a placeholder VapourSynth DLL project (no filter algorithm);
   - one GitHub Actions workflow that builds both programs;
   - the final version of this handback.
5. **Wheel/PyPI packaging is now yours** (it moved out of the migration). See R.6.

### R.2 What migration did (Stage A), and why it matters to you

| What | Value now | Why it matters to you |
|---|---|---|
| Platform | x64 only (Win32 removed) | Everything you build is 64-bit. |
| CPU baseline | `/arch:AVX2` in Debug and Release | Users need an AVX2 CPU (Haswell 2013+ / Excavator 2015+ / Zen); the README says so. Your later SIMD code can assume AVX2 for the build. A runtime CPU check is still to be decided (R.6). |
| Host tools | 64-bit compiler and linker (`HostX64\x64`, via `PreferredToolArchitecture=x64`) | **Dave's standing rule: 64-bit everywhere** (tools, MSBuild, Python, CI). x86 tools appear only as a last-resort diagnostic. |
| Release runtime | Static CRT (`/MT`); Debug `/MDd` | A standalone binary with no redistributable. **For the plugin DLL this creates a rule (R.4).** |
| Optimisation | Release `/O2` (components pinned), `/GL` + `/LTCG` (plain, not incremental), `/favor:blend` | Fast Release builds. The empty `LinkTimeCodeGenerationObjectFile` pin stops an unwanted `/LTCGOUT` switch (see the Knowledge record). |
| Floating point (accepted inspector only) | `/fp:precise`, **no `/fp:contract`** | The accepted MSVC configuration does not enable automatic FMA contraction under `/fp:precise`. The later plugin/Stage 6 floating-point and FMA policy has NOT been ratified merely by inheriting the inspector setting; see R.6. |
| Security | `/GS`, CFG, CET, ASLR + high-entropy VA, NX; `/sdl` **OFF for the inspector only** (its legacy C triggers incompatible diagnostics); **`/sdl` ON for the plugin** | Plugin code must pass `/sdl`. The compiler promotes specified security warnings (including C4996 and detected uninitialised-variable warnings) to errors; it does not guarantee detection of every unsafe call or defect. |
| Spectre mitigation | Deliberately OFF (`SpectreMitigation=false`); `/Qspectre` absent | Dave's threat-model decision for a local video tool. Do not switch it on without a decision. |
| Debug info | Full PDB; Release PDB path is the file name only (`/PDBALTPATH:%_PDB%`) | No build-machine paths in shipped binaries. |
| Toolset | Currently `v145` (VS2026). Policy: newest installed toolset, minimum v145, with the change made in Stage B+ (R.5) | The build selects from the **installed, maintained** Visual Studio toolchain; discovery does not install updates. Record the exact selection and apply the change gates (R.4). |
| Settings source | **Project files own the executed compiler/linker settings.** GUI, command line and CI build those project files. CI separately keeps an **expected-switch CSV** and a commented, non-executed reference of accepted CL/LINK command lines (G5/G7). | Those comparison/reference records are verification evidence, **not** alternative build flag maps. A setting change belongs in the reviewed `.vcxproj`; CI must not pass a competing flag set. |
| Waiver on record | The A3 v0.10 six-index rerun was **WAIVED (not PASS)** by Dave | The evidence: identical compiler lines, only `/LTCGOUT` removed, identical binary structure. It is not a precedent. Any future toolset, compiler or code-generation change needs all six indexes. |

### R.3 How to build: humans and chats

**Dave builds in the VS2026 GUI:** open the `.slnx`, choose **Release | x64** (or Debug | x64), and Build. Nothing else is needed.

**Chats and scripted builds (command line).** These are examples to be re-run on Dave's machine and pasted from real output in the final handback. Use a **plain `cmd` prompt, not a Developer Command Prompt**:

```text
for /f "usebackq delims=" %i in (`"%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" -latest -products * -requires Microsoft.Component.MSBuild Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath`) do set "VS_INSTALL=%i"
"%VS_INSTALL%\MSBuild\Current\Bin\amd64\MSBuild.exe" "vs\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock.slnx" -noAutoResponse /m /t:Rebuild /p:Configuration=Release /p:Platform=x64
```

- In a `.bat` file, write `%%i` instead of `%i`.
- `-latest` means the newest **released** Visual Studio installed and updated on that machine. Previews are never used. Build Tools installations are accepted.

**Interactive tools (dumpbin and others): a separate prompt, never the build prompt:**

```text
call "%VS_INSTALL%\Common7\Tools\VsDevCmd.bat" -arch=amd64 -host_arch=amd64
dumpbin /dependents vs\VapourSynth-mpeg2Deblock\x64\Release\Mpeg2BlockInspector.exe
dumpbin /headers vs\VapourSynth-mpeg2Deblock\x64\Release\Mpeg2BlockInspector.exe
```

What a good inspector Release build shows:
- the dependencies are only `KERNEL32.dll`;
- the DLL characteristics include "High Entropy Virtual Addresses", "Dynamic base", "NX compatible", "Control Flow Guard" and "Terminal Server Aware";
- "CET compatible" appears under the extended DLL characteristics;
- the CodeView entry names `Mpeg2BlockInspector.pdb` with no path.

**Never do these (and why):**
- **Pass compiler or linker flags on the MSBuild command line.** It creates a second, unreviewed source of settings.
- **Set the `CL`, `_CL_`, `LINK` or `_LINK_` environment variables.** `cl.exe` and `link.exe` silently add their contents to every invocation, bypassing the project.
- **Build inside a VsDevCmd prompt.** It sets variables such as `Platform` that MSBuild reads as build properties.
- **Add a `Directory.Build.props`, `.targets` or `.rsp` file** anywhere above or inside the repository. MSBuild imports them automatically and silently.
- **Copy CNR3's GitHub `cl` flag map.** It is a hand-maintained copy of settings that drifts (it uses `/MD`, for example).
- **Search build logs for the text "HostX86" to check the tools.** It appears harmlessly in Microsoft's property messages. Check the actual `...\HostX64\x64\CL.exe` and `link.exe` invocation lines.

### R.4 Rules you inherit, and the reasons

1. **Build-setting and solution-configuration change control.** Changes to `.vcxproj` compiler/linker/manifest/toolchain settings or `.slnx` build configuration follow candidate -> review -> Dave ratifies -> apply. Routine source-file membership changes remain normal technical development, but they still receive the tests appropriate to their behavioural effect.
   - **Why:** MSBuild can silently ignore a misspelt or misplaced setting.
   - Changed build settings must be proven against Visual Studio's rule files (see the Knowledge record), and the effective compiler/linker command lines compared before and after.
2. **The switch check.** The actual CL and LINK switches are extracted from the build's tlog files and compared with a reviewed expected set.
   - Missing or extra switches fail.
   - **Why:** this is the only check that caught `/LTCGOUT`; reading the project file did not.
   - Tools exist: `extract_StageA_A3_checkpoint_tlog_tokens_v0_4.py` and `Claude_check_A3_post_tokens_v0_1.py`. The CI workflow will run the equivalent on every build.
   - If you run the extractor off Windows, it must use Windows command-line splitting rules. Its old non-Windows fallback mis-splits quoted arguments.
3. **The six-index regression.** All six inspector reference indexes must stay byte-identical whenever the MSVC toolset, exact compiler version or a change capable of affecting the inspector's generated code changes. If it is uncertain whether a project edit can affect generation, run all six.
   - **Why:** a new compiler can generate different code from identical switches. Only the functional output catches that.
   - **Reconciliation of older H2/H3c with Dave's later G11/P5:** the historical sections 16/H2 and 16/H3c require six indexes merely because `.vcxproj`/`.filters` bytes changed. For current migration purposes, G11/P5 controls: a proven *non-code-generating* metadata or `.filters`-only change does not by itself require the six-index rerun. Source compilation/membership, toolset and code-generation-relevant edits still require appropriate regression; no broad waiver is implied. Claude should verify this interpretation of the later ratification before final handback.
4. **Toolchain updates.** Every build records the toolset name and exact compiler version.
   - If either differs from the last accepted build, the switch check, warning comparison and all six indexes must pass again **before that build is accepted**. A successful CI compile or matching switch list alone does not discharge the six-index gate. Whether CI or Dave's local machine executes the indexes remains open (O7).
   - The folder version (for example 14.51.36231) and a tool's file version (for example dumpbin 14.51.36260.0) are different numbers. Record both, and do not confuse them.
5. **The plugin runtime-ownership rule.** The DLL uses the static CRT (`/MT`), so it has its **own** heap and CRT state, separate from VapourSynth's.
   - **No CRT-owned memory or objects may cross the DLL boundary.** Do not `free()` what the host allocated, or vice versa, and do not pass `FILE*` across.
   - All VapourSynth resources (frames, nodes, maps) go through the `vsapi` functions.
   - **Why:** mixing heaps across a `/MT` boundary corrupts memory, often silently.
6. **AGPL-3.0-or-later**, with `NOTICE.md` as the legal and test-media boundary.
   - The test recordings in `VHSC_samples/` are **not** AGPL. They are for testing only.

### R.5 What is still coming before migration hands back (agreed with Dave on 2026-10-10)

| Step | What | Notes for you |
|---|---|---|
| 0 | Confirm the accepted settings are in the repository | Done by Claude on the pushed snapshot; Dave confirms the local hashes. |
| 1 | **Proving workflow.** A `workflow_dispatch`-only GitHub Actions run builds the current project on `main` and performs the agreed checks | **`main` is the sole development branch; there is no test branch.** The reviewed manual-only workflow is committed to `main`, invoked manually, and has no release/push trigger at this proving step. It tests project-file-only builds before release automation is enabled. |
| 2 | **Stage B+.** The toolset change (`PlatformToolset=$(DefaultPlatformToolset)` plus a numeric minimum-v145 guard) **and** the placeholder DLL project | The DLL is a cut-down CNR3 entry point (`VapourSynthPluginInit2`, `configPlugin`) plus **one trivial function** (for example, returning its input clip). It is loaded once in VapourSynth locally. Its settings copy the inspector's, with the C++ DLL differences: DynamicLibrary, C++ (`/std:c++20 /permissive-` as CNR3, to be confirmed), `/sdl` ON, no `_CRT_SECURE_NO_WARNINGS`, and no exe-only settings (console subsystem, UAC manifest, segment heap). **This placeholder is what you will grow into the real filter in technical Stage 7.** |
| 3 | **The final GitHub Actions workflow**, one self-contained file | Triggers: **published GitHub Release** and manual `workflow_dispatch`. It builds both programs through the `.slnx`, runs all checks inline, uploads the files, and attaches them to the Release. It carries a dated, commented **reference block** of known-good command lines, for diagnosis only. **If a runner's Visual Studio emits different switches, the run fails and prints the difference.** A legitimate change is accepted by updating the expected-switch file and the reference block in one reviewed commit. No runner pinning. |
| 4 | **The final handback** (this document, rewritten) | It will contain the R.3 examples pasted from real runs, the final names, hashes and commits, and the CI instructions. |

### R.6 What you will have to deal with yourselves, and why

1. **Wheel/PyPI packaging (moved to you).**
   - **Why:** a wheel of a DLL with no real filter proves little; packaging belongs with the working filter (technical Stages 7-9).
   - The facts carried over from CNR3:
     - a `py3-none-win_amd64` wheel, placing the DLL at `vapoursynth/plugins/<name>/<name>.dll` (VapourSynth's autoload path);
     - metadata must say **AGPL-3.0-or-later**, never CNR3's `License: MIT`;
     - include `LICENSE` and `NOTICE`;
     - package the CI-built Release binaries, do not rebuild;
     - publishing to PyPI needs Dave's explicit decision.
   - The CNR3 workflow (lines 165-257) shows a working wheel-assembly pattern; reuse its *structure*, not its metadata.
2. **A runtime AVX2 CPU check.** It is deferred until AVX2 code exists (technical Stage 7 or 8).
   - **Why:** on a non-AVX2 CPU, executing AVX2 instructions can cause an illegal-instruction error. A correctly positioned, baseline-safe plugin-load check could give a friendlier failure, but is not yet designed or authorised.
3. **`/sdl` in real plugin code.** Specified diagnostics, including C4996 for deprecated/unsafe CRT functions and certain uninitialised-variable warnings, become errors when emitted. Use suitable safer functions or C++ alternatives; this is not a comprehensive static analyser.
4. **Bit-exactness in the Stage 6 port.** The inspector's `/fp:precise` is proven; the real plugin's floating-point/FMA policy remains to be ratified. Even with `/fp:precise` and contraction disabled, Python/NumPy-to-C++ bit equality is **not automatic**: verify types, operation order, intermediate rounding, library routines and any explicit FMA against the numerical oracle.
5. **CI switch-check failures after Visual Studio updates.** They are expected occasionally and are not a bug. Read the printed difference, decide whether it is legitimate, and update the expected file and reference block in one commit (with review). Run the six indexes if the compiler changed.
6. **The DLL and package names** (decided by Dave at Stage B+ and recorded in the final handback). Use them consistently in the namespace, the DLL, the wheel and the autoload folder.
7. **Open items Dave may still decide at Stage B+:**
   - `/guard:ehcont` on the DLL;
   - a version resource;
   - dropping Large Address Aware on the DLL;
   - whether CI also runs the six indexes;
   - whether Python Stage 2 may start in parallel with the remaining migration.

### R.7 What did NOT change

- Technical authority is unchanged: `02_INDEX_FORMAT_SPEC.md`, `05_DECISIONS.md`, `06_DEBLOCK_CONCEPT.md`, the Stage 1 report, the Stage 2 experiment design v0.3 (ratified by Dave on 2026-10-08; its file header still says DRAFT, which is for you to correct) and Proposal v0.5.
- K-07 (FRAME/FIELD/NONE semantics) is unchanged.
- The Stage 1 inspector code and the analyzer are frozen and hash-verified.
- No technical Stage 2 work has started.

### R.8 How you restart

Wait for Dave's go after the final handback (unless Dave separately authorises Python Stage 2 in parallel under open decision O6). Then:
1. read this section;
2. read the final handback's build section;
3. read the Knowledge record;
4. update your **own** handovers. Migration never edits them.

### R.9 Where the detail is

| Topic | Document |
|---|---|
| Decisions and history | `Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_19.md` |
| How Stage A was executed | `StageA_Visual_Studio_Normalization_Execution_Plan_v0_14.md` (frozen) |
| Hard-won MSBuild lessons (setting placement, rule-file proof, tlog format, `/LTCGOUT`, the single-owner rule) | `StageA_VS2026_MSBuild_Hard_Earned_Knowledge_v0_5.md` |
| The agreed remaining plan | `Claude_RESPONSE_TO_ChatGPT_Agreed_Remaining_Plan_v0_1.md` |
| The A3 gate evidence and waiver | `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_10_Final_Gate_v0_1.md` |
| CI and toolchain discovery policy | `Claude_REVIEW_OF_ChatGPT_StageC_MSBuild_Discovery_Proposal_v0_3.md` (M1-M5), as adapted to one self-contained workflow (plan G3-G8) |

---

## Stage A close-out acceptance and explicit Plan section 30 deviation (2026-10-10)

**Decision authority:** Dave. **Gate:** A3 v0.10 ACCEPTED; Stage A proceeds to
close-out. This does not mean repository documentation has been committed or
pushed. This close-out update supersedes earlier *in-progress* gate status in
the historical sections below. The production `.vcxproj` remains unchanged.

**Ratified and applied A3 v0.10 identity:** `Mpeg2BlockInspector.vcxproj` SHA-256
`73e9019cda7d1061ecdb06526c60f4ee84baa4c385b7ca0dde4269544e4fdb46`.
Windows working-copy `.slnx` SHA-256:
`fa24efcd73401a38604e2f4228b07d8b960abcbfb66da22c02908e9d1cdb0754`.
Debug EXE SHA-256:
`df92319fc0d39d9b09d8de82dd059324adca0eedae8f5e404aa6460d8cd1a0cc`.
Release EXE SHA-256:
`fc168013f74074e3921dc781f6b2db69a9e67f7df80396dd2ab1fcc146c1ad48`.
These are reported from Dave's machine; the executable hashes were not
independently recomputed from the evidence ZIP.

**Completed gate results:** Both Debug and Release clean rebuild RC=0;
W1 content-checker RC=0 with Debug CL 33, Release CL 32, Debug LINK 23,
Release LINK 25; native logs prove HostX64\x64 CL and LINK. v0.9-to-v0.10
warning signatures matched: 17 Debug and 17 Release, with no new warnings.
W2 Release PE/security/import/manifest PASS: x64 PE32+, LAA, HEVA, ASLR,
NX, CFG with 37 function-table entries, CET, nonzero security cookie,
Terminal Server Aware, basename-only PDB path, KERNEL32.dll-only imports,
embedded asInvoker/SegmentHeap manifest. Production project and solution
hashes matched expected identities. Three frozen-file SHA-256 values and the
Git comparison passed; no more source audits are authorised absent a new
specific cause. Last reported Git status was clean, with eight expected
ignored paths and no `.iobj`/`.ipdb`. External evidence ZIP captured.

**Dave-ratified deviation from Execution Plan section 30:** Section 30
says "No representative subset or waiver is allowed." Dave specifically
ratified option (b) on 2026-10-10, making one bounded exception for the
A3 v0.10 six-index rerun. Its status is **WAIVED**, explicitly **NOT PASS**.
The v0.9 six-index regression previously PASSED; it was NOT rerun for v0.10.
The rationale, attributed by Dave to
`Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_10_Final_Gate_v0_1.md`, section 3:

1. v0.10 and v0.9 CL command lines are identical (W1 token sets and
   same-size CL tlogs); the v0.9 executable passed all six index cases.
2. The sole LINK difference is removal of `/LTCGOUT`, applicable to
   incremental LTCG, while ordinary `/LTCG` remains enabled.
3. Comparing the v0.9 and v0.10 Release `dumpbin /headers`, `/loadconfig`
   and `/imports` after masking timestamps, PDB GUID and dump path produces
   zero differences. This covers code size, entry point, section layout,
   Guard CF function count (37), Guard Flags and imports.

Together these constitute **strong evidence of identical code generation,
not byte-for-byte proof**. Do not relabel the waiver PASS or weaken the
future rule: whenever the MSVC toolset, exact compiler version or any
code-generation-relevant setting changes, the six-index regression is
mandatory before acceptance. Permanent CL/LINK switches, HostX64 and
Release-only KERNEL32 import checks also remain required for every harness
or CI build. The waiver does not authorise a general exception to section 30.

**Stage C/D carry-forward from Claude final-gate review v0.1, section 4
(N1-N4; OPTIONAL review notes, not additional A3 gate conditions):**

- **N1 - command-line tokenisation:** On non-Windows, the existing
  `extract_StageA_A3_checkpoint_tlog_tokens_v0_4.py` fallback
  `shlex.split(posix=False)` incorrectly splits quoted Windows command lines,
  including `/MANIFESTUAC:"level='asInvoker' uiAccess='false'"` and
  paths containing spaces. Claude initially obtained 117 tokens and a
  false FAIL; Windows-rules tokenisation obtained the correct 113-token CSV.
  Dave's Windows runs used `CommandLineToArgvW` and are valid. For Stage C/D,
  implement correct Windows command-line splitting on every supported
  platform or fail closed on non-Windows; do not accept a false failure or
  silently rewrite the expected token set.
- **N2 - actual tool invocations:** `HostX86` appears 34 times in each
  detailed log as `Microsoft.Cpp.Common.props` property-reassignment
  messages. A global text search for that string falsely rejects a valid
  HostX64 build. Verify actual `...\bin\HostX64\x64\CL.exe` and
  `...\bin\HostX64\x64\link.exe` *invocation* lines in both
  configurations; distinguish them from informational property lines.
- **N3 - two version identities:** The MSVC tools installation folder
  contains `14.51.36231`, while the selected x64 `dumpbin` reports its
  executable file version as `14.51.36260.0`. Record the actual toolset
  directory version and the relevant tool executable's file version,
  with executable path and provenance, on every Stage C/D build. These
  numbers are not interchangeable. Claude's suggestion that folder/file
  versions commonly differ, and that the two come from one installation,
  remains unverified on Dave's machine until Stage C establishes it.
- **N4 - Guard Flags interpretation:** Withdraw unsupported bit-by-bit
  decoding of hex Guard Flags `10017500` from Claude's earlier v0.9 review.
  The evidence directly identifies only `CF instrumented` and
  `FID table present`; `dumpbin` reports zero long-jump targets. The
  accepted CFG criteria are presence of the Guard CF function table and
  a nonzero function count (37), which PASS. Do not infer additional
  protection states solely by reading undecoded bits in this value.

**Provenance:** `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_10_Final_Gate_v0_1.md`,
section 4, now included byte-for-byte in this review package. N1-N4 are
future Stage C/D engineering constraints and corrections, not evidence of
work already implemented or tested there. Anything explicitly marked
unverified remains unverified until proven on Dave's machine.


**Close-out boundary:** README consistency comparison against the accepted
build is documented in `README_CONSISTENCY_ASSESSMENT_v0_1.md`. The available
README is an attached repository ZIP snapshot; confirm the live Windows
working-copy README before final commit. This document set is for Claude's
review. After review, re-run `git status`, stage only intended files, inspect
`git diff --cached`, commit, push, verify the remote commit, and ask Dave
whether an optional tag is wanted. None of these repository mutations has
been performed by ChatGPT. Stage B/C/D implementation is not authorised by
accepting this documentation alone.

---

### Developer-facing contract

A3 v0.10 has been accepted and the Stage A close-out is underway. The
published inspector remains x64-only with AVX2, `/GS`, CFG/CET and static
Release runtime; the six-index rerun was WAIVED for the narrow v0.10
`/LTCGOUT` correction, not passed. Developers should not infer a new
algorithm/bitstream change or a new test result from this acceptance.
The VS2026 project currently pins `PlatformToolset=v145`; floating to the
newest installed MSVC toolset is subsequent, separately reviewed work.
Ordinary local builds are made in Visual Studio; CI must use the reviewed
Stage C harness without duplicating project-owned switches.


## 2026-10-10 addendum: 64-bit, discovery and compiler policy

## New binding decisions and staged implementation (2026-10-10)

Decision authority: Dave. Review basis: `Claude_REVIEW_OF_ChatGPT_StageC_MSBuild_Discovery_Proposal_v0_3.md` (M1-M5), cold-reviewed by ChatGPT on 2026-10-10. This is a documentation update only: no production project modification and no interruption to the A3 v0.10 gate. The technical implementation mechanisms identified below as UNVERIFIED remain pending local tests and a separately reviewed candidate.

### Binding policy: 64-bit everywhere

- Target: x64 only, unchanged from the historical baseline.
- All production projects shall explicitly set `PreferredToolArchitecture=x64` in each appropriate `Label="Configuration"` group; compiler/linker evidence must show `HostX64\x64\CL.exe` and `HostX64\x64\link.exe`.
- Permanent harness and CI select `MSBuild\Current\Bin\amd64\MSBuild.exe` beneath the discovered installation; verify the MSBuild *process* is 64-bit at runtime (not merely by path or PE header). MSBuild engine bitness and compiler/linker host bitness are separate requirements.
- Interactive tool setup: `VsDevCmd.bat -arch=amd64 -host_arch=amd64`; use the `HostX64\x64` dumpbin/toolchain from that same installation. Python and helper binaries must be 64-bit. Stage D uses x64 Windows runners.
- No silent x86 fallback. The x86 host is permitted solely as the last D4 diagnostic step, after ISA, `/MD`, and `/GL`+`/LTCG` diagnostic experiments; local, uncommitted, never shipped.

### Binding policy: installation discovery and version handling

- Stage C performs one `vswhere` installation search, with no VS version range, no `-prerelease`, and no hard-coded VS installation path: `-latest -products * -requires Microsoft.Component.MSBuild Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath`. Build Tools products are explicitly eligible; record selected product and installation identity. The VC component identifier remains UNVERIFIED on Dave's machine.
- From the single discovered root derive MSBuild, the project-owned toolset resolution, interactive VsDevCmd and 64-bit dumpbin. No independent search/fallback to another VS installation. `vswhere` use and the exact runtime lookup chain require Stage C validation.
- Current A3 v0.10 gate **keeps** the established fixed `C:\Program Files\Microsoft Visual Studio\18\Community\MSBuild\Current\Bin\MSBuild.exe` checkpoint path; that path is not a template for the permanent harness. The v0.10 project stays at `PlatformToolset=v145` until Stage A is closed.
- Permanent compiler policy (Dave): **Use the newest installed MSVC toolset (minimum v145) and the MSVC build Visual Studio designates as current for that toolset (normally the newest installed, in-support build), with 64-bit host tools. The toolset name and exact compiler version are recorded on every build. If either differs from the last accepted build, the switch check, warning comparison and six-index regression must all pass again before that build is accepted.**
- Record this policy now, but implement toolset selection only *after* Stage A closes, as a small independently reviewed and ratified project candidate. Claude M5 proposes (UNVERIFIED) `PlatformToolset=$(DefaultPlatformToolset)` with a minimum-v145 project guard; BOTH its availability at the configuration import point and its selection semantics remain UNVERIFIED, and must not be asserted as a working implementation. The meaning of "newest installed" versus "latest in-support default" must be reconciled and demonstrated. Minimum-version comparison must be numeric/semantic, not lexicographic. No new project flags supplied by harness/CI.
- Do not silently rely on Microsoft defaults: **discover, verify, record**. Log installation/product, VS version, selected MSBuild path/version/runtime bitness, `PlatformToolset`, exact MSVC compiler version/host paths, and SDK version on every build.

### Permanent acceptance gates and environment isolation

- Every harness/CI build must mechanically verify CL and LINK command-switch sets against a reviewed expected set, require `HostX64\x64` for compiler/linker, and verify Release imports are exactly `KERNEL32.dll`. Toolset/compiler change triggers additional warning-by-code/file/line comparison and byte-identical six-index regression before acceptance. Do not weaken required security flags to obtain a pass. The maintained switch baseline must be consciously updated and reviewed if toolchain semantics evolve; unknown switches are failures, not silently accepted.
- Harness builds launch from a plain CMD environment, NOT after executing VsDevCmd; explicitly pass configuration and x64 platform without injecting compiler/linker settings. Refuse or sanitize `CL`, `_CL_`, `LINK`, `_LINK_`, `Platform`, and any environment property overriding project-owned configuration, including `PreferredToolArchitecture` and relevant MSBuild override entry points. Which properties MSBuild treats as global, and the precise environment guard, require tested design. VsDevCmd is permitted for separate interactive tools such as dumpbin.
- Prove locally before accepting Stage C: vswhere component/product selection, actual engine process bitness, default-toolset property/import ordering, minimum-version guard, default compiler-build selection, and the exact installed `dumpbin.exe` lookup. Keep UNVERIFIED findings labeled until directly evidenced; do not import unverified claims as fact.

### Current A3 state and documentation boundary

- A3 candidate v0.10 (`Mpeg2BlockInspector_A3_APPLYABLE_CANDIDATE_v0_10.vcxproj`, SHA-256 `73e9019cda7d1061ecdb06526c60f4ee84baa4c385b7ca0dde4269544e4fdb46`) was ratified/applied; Debug and Release clean rebuilds had RC=0.
- W1 post-application evidence preserved four tlogs, byte-compared them, extracted 33/32 CL and 23/25 LINK tokens, and Claude's unchanged checker reported four PASS outcomes (`W1_CHECKER_RC=0`). Build logs also confirmed HostX64 x64 CL and LINK in both configurations. Evidence is on Dave's Windows machine outside the repository; not in the GitHub ZIP.
- HISTORICAL 2026-10-10 pre-final-gate status (superseded by the accepted A3 close-out section above): warning/W2/hash/waiver review had not yet completed. These checks are now resolved as recorded in the first section; do not rerun them as a result of this historical text.
- On this user's Windows working copy, agreed `.vcxproj`/`.slnx` SHA-256 hashes are for the CRLF file representation. GitHub ZIP LF representations can legitimately differ. Confirm paths and bytes locally; the ZIP is reference/layout only.

### Developer-facing implications (not an algorithm change)

This handback communicates the final build/runtime contract, not authority to edit technical MPEG-2 semantics, the frozen inspector decoder, or development-chat handovers. For the future VapourSynth API4 plugin, use x64 target, x64 MSBuild/host/tools/Python, explicit `PreferredToolArchitecture=x64` per configuration, AVX2 and established security settings; plugin Release `/MT`, `/sdl` ON. No CRT objects across the DLL API boundary. A separate later-reviewed project candidate will implement the floating-toolset decision. Until that review, keep existing `v145` settings. On compiler/toolset change, compare switches, warnings and six-index regression. Stage A remains open and this handback is preliminary until its accepted closure.

### K4: automatic imports and response files (binding for Stage C/D)

- Fail closed if any `Directory.Build.props`, `Directory.Build.targets`, or `Directory.Build.rsp` exists in a repository ancestor directory, from the repository parent through filesystem root; also reject unreviewed occurrences within the repository that may affect a build. Log the checked paths and results.
- Launch MSBuild with `-noAutoResponse` so implicit MSBuild response files do not silently inject switches (including applicable `MSBuild.rsp` and `Directory.Build.rsp`). Validate the precise MSBuild 18.x response-file behavior locally; any uncertainty is an unverified Stage C gate item.
- Prove the guard experimentally once using a disposable scratch project and a scratch `Directory.Build.props` in its ancestor directory. Confirm the harness refuses to build, then remove the scratch file. Never create this probe in or above the production repository. Record command, output, and return code.
- The guard is additive to environment-property checks, including `PreferredToolArchitecture`, `CL`, `_CL_`, `LINK`, `_LINK_`, `Platform`, and relevant MSBuild/global-property override mechanisms. No build-policy injection through environment, response files or auto-imports is permitted.

### K3: compiler build designated by Visual Studio

- No project-level `VCToolsVersion` override: the designated current build is **recorded, not pinned**. Any change relative to last accepted compiler/toolset triggers command-switch, warning, and six-index rerun before acceptance. The exact selection rules and `DefaultPlatformToolset` implementation remain UNVERIFIED until local Stage C/post-A testing.
- `-latest`, without `-prerelease`, selects the newest **released** qualifying installed Visual Studio. Keeping the build machine updated is an operator responsibility; discovery does not install updates. Build Tools are eligible via `-products *`, and the selected product must be logged.

---

## 0A. Current Stage A caution for developer chats

The migration has **not** handed control back to technical development yet.

Latest accepted review state:

- Q1/R1/R4 evidence: closed;
- A3 v0.8: cold-reviewed, not ratifiable because of U1;
- A3 v0.9: corrective candidate prepared, not yet Claude-accepted or Dave-ratified;
- production project: A3 not yet applied;
- Stage A binary/security/dependency/six-index gate: not yet run.

The migration-specific reasoning is preserved in:

```text
StageA_VS2026_MSBuild_Hard_Earned_Knowledge_v0_2.md
```

Developer chats should not reproduce that build-system research or treat the v0.9 target state as installed until the final handback says Stage A passed.

---


## 0B. Ratified-but-not-yet-installed distinction

Technical-development chats must distinguish these two states:

```text
A3 v0.9 design: accepted and ratified
A3 v0.9 production state: not yet proven installed/passed
```

Exact ratified SHA:

```text
ebfcde82405fd2dc25aa7a14a160f89375465d545927b3e4583e7a40fd1af668
```

Do not assume the new project settings are live until migration handback records a successful post-A3 gate and final Git commit/tag.


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

This document is also **not** the migration-chat continuity handover. Migration-only continuity is recorded in `ChatGPT_Migration_Chat_Handover_v0_*.md` and `Claude_HANDOVER_TO_Future_Claude_Migration_Chat_v0_*.md`. Claude's `Claude_HANDOVER_TO_Future_Claude_Chat_v0_*.md` is instead a development-chat handover and is not owned by migration.

The individual developer-chat handovers should reference this common handback for migration facts instead of copying or reinterpreting those facts.

Because migration remains open, this v0.10 is a current-state handback snapshot. The final handback must be refreshed against completed Stage A-E evidence and Dave's migration-close decision before it is treated as the final return-to-development record.

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

Current published `main` observed by migration:

```text
ab145f56fd22cf4812d1e5b3e9fbbffc1f974095
```

The substantive interim migration checkpoint is `b4dace033e2d6f6d0c4b505875aeae6879077324`.

Published tag:

```text
vapoursynth-mpeg2deblock-post-restructure
```

A later final migration commit/tag is expected to become the normal development restart point.

---

## 3. Repository layout inherited by development

Current important locations are shown using the case reported by the A2/test evidence. Before final handback, confirm the committed case with `git ls-files vs` and preserve it exactly everywhere:

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

vs\VapourSynth-mpeg2Deblock\
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

The supplied updated README already describes target AVX2/standalone/security policy. Its live Git commit status is not established by this handback snapshot. Until the corresponding A3/Stage B gates pass, those build statements are target policy rather than proof that every current checked-out artifact already has those properties. Claude recommends committing the README with A3 or after the A3 gate if it is not already committed.

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
- Visual Studio material moved under `vs\VapourSynth-mpeg2Deblock\`;
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
Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_15.md
StageA_Visual_Studio_Normalization_Execution_Plan_v0_10.md
```

Current state:

```text
Repository restructure: COMPLETE
Stage A1: APPLIED / COMMITTED
Stage A2: APPLIED / COMMITTED
Pre-A3 checkpoint: COMPLETE / PASS / Claude closed
A3 v0.2: superseded
A3 v0.3: superseded for application because it targeted SSE2/security-off
Superseding A3: PRE-CANDIDATE v0.6 requirements/pin-table package prepared; final applyable `.vcxproj` still waits on S13 and is NOT YET APPLIED
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
Debug+Release /favor:blend
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

**Runtime ownership rule (H1):** no CRT-owned memory or object may cross the plugin DLL boundary when using the static runtime. Memory allocated by the plugin is freed by the plugin; VapourSynth-owned frames/nodes/maps and other cross-boundary resources are acquired/released through the `vsapi` functions. Do not design an API where one static-CRT instance allocates and another module frees/manages that allocation.

### 9.3 Release PDB path hygiene

Release artifacts use:

```text
/PDBALTPATH:%_PDB%
```

so shipped artifacts embed the PDB file name rather than Dave's/CI's absolute build path.

### 9.4 Security policy

Performance work must not gain speed merely by globally disabling security mitigations.

Accepted target settings in **both Debug and Release** are:

```text
/GS ON
Control Flow Guard ON at compile/link
CET compatibility ON
SpectreMitigation explicitly Disabled in Debug and Release; `/Qspectre` absent
```

Spectre mitigation is deliberately not used for this project's threat model, but no-defaults still applies: both project configurations explicitly set the captured VS2026 `SpectreMitigation=Disabled` element and compiler commands contain no `/Qspectre`. Harness/CI must not add Spectre flags or runtime prerequisites. This does not authorize disabling `/GS`, CFG or CET for performance.

### 9.5 Build-setting traceability inherited by development

Final migration infrastructure carries a mechanical pin table linking effective compiler/linker/PE behaviour to explicit project XML or a documented exception, with recognition evidence proving that each XML property/value is accepted by the selected VS/MSBuild rule set or by VS2026 Property Pages evidence. After handback, any build-setting change must preserve that traceability and rerun the applicable command-line/dumpbin gates. Source-file membership changes remain normal development work; settings changes are reviewed infrastructure changes.

### 9.6 SDL exception

Inspector:

```text
/sdl OFF
```

This is a deliberate exception because the inspector source is frozen and derived from the MPEG-2 reference decoder; migration will not edit legacy/reference-decoder source merely to satisfy `/sdl` diagnostics.

New `mpeg2Deblock` code:

```text
/sdl ON
```

### 9.7 Floating-point policy inherited by the inspector

The accepted inspector build pins:

```text
/fp:precise
/fp:contract absent
```

in Debug and Release. AVX2 therefore does not silently authorize FMA contraction in the frozen inspector. The plugin's eventual floating-point/FMA policy remains an explicit Stage B/technical-development choice until ratified.

### 9.8 Project files are the build-settings source of truth

The `.vcxproj` files own the accepted CPU/runtime/security/optimization settings.

The local harness and GitHub release workflow must build those project files through MSBuild and verify the effective result. They must not maintain a second hand-written `cl` flag map or inject `/MT`, `/arch:AVX2`, CFG, CET, `/sdl`, optimization or toolset overrides to repair divergent project settings. They must also not inject `/Qspectre`; Spectre is deliberately outside the accepted policy.

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

> **Superseded (v0.14):** Stage A is CLOSED. See section R.1/R.2. Kept as history.

The superseding A3 must be cold-reviewed/ratified before application and must then prove, at minimum:

- Debug and Release x64 build PASS;
- exact effective compiler/linker deltas explained;
- `/arch:AVX2` effective in Debug and Release;
- Release `/MT` effective and no prohibited VC/UCRT runtime DLL dependencies remain;
- `/GS`, CFG and CET actually effective in Debug and Release;
- Spectre-OFF policy proved: `/Qspectre` absent and no project/harness/CI injection;
- `/fp:precise` effective and `/fp:contract` absent;
- information-only LP timing recorded before/after A3;
- inspector `/sdl` exception remains OFF;
- frozen source/analyzer unchanged;
- all six tracked indexes byte-identical;
- warnings explained;
- README build-policy claims match accepted evidence;
- project settings, not harness overrides, are responsible for the result.

If AVX2/security changes unexpectedly alter an index, migration must diagnose by temporary local variants. It must not silently abandon the ratified product/security policy.

---

## 13. Stage B result the developer chats should expect

> **Partly superseded (v0.14):** Stage B is now "Stage B+" (the toolset change plus the DLL placeholder with one trivial function). See R.5 step 2.

Stage B is migration/build-system scaffolding only. It does **not** implement the deblocking algorithm.

Expected end-state:

```text
VapourSynth-mpeg2Deblock.slnx
    Mpeg2BlockInspector    C EXE
    mpeg2Deblock           C++ VapourSynth API4 DLL placeholder (working name until Stage B naming ratification)
```

The placeholder DLL should be minimally buildable/loadable and expose the API4 plugin entry point, but contain no Stage 2 deblocking implementation. `mpeg2Deblock` is a **working name**, not a final public identity, until the coupled Stage B naming decision is ratified.

No CRT-owned memory/object may cross the DLL boundary under `/MT`; cross-boundary VapourSynth resources use `vsapi` ownership functions.

Its project must already carry the accepted project policy:

```text
x64 only
AVX2 minimum
/favor:blend explicit in Debug and Release
Release /MT
Release /PDBALTPATH:%_PDB%
/GS ON
CFG ON
CET ON
SpectreMitigation explicitly Disabled; /Qspectre absent
/sdl ON
```

The vendored VapourSynth headers live under `third_party\vapoursynth\include\`. `third_party\vapoursynth\include\VERSION.txt` is the single header-release identity record; other documents should point to it rather than duplicate a version number.

Stage B must prove exports, dependencies/loadability and inspector non-regression.

---

## 14. Stage C/D/E result the developer chats should expect

> **Superseded (v0.14):** there is no separate local build harness. CI is one self-contained GitHub Actions workflow (R.5 step 3). **Stage E (wheel/PyPI) has moved to the development chats** (R.6 item 1).

### Stage C - canonical local build harness

One reproducible route discovers the installed Visual Studio/MSBuild using `vswhere`, including required x64 C++ tools, builds the `.slnx`, records toolchain/SDK provenance and verifies project outputs/settings. It verifies that the project-defined AVX2/runtime/security settings are effective and that `/Qspectre` is absent.

### Stage D - release-triggered GitHub workflow

The workflow must call the same Stage C/MSBuild route. It must not reproduce CNR3's old hand-written `cl` flag map or override ratified project settings.

Runner/toolset claims must be verified when the workflow is built. If required v145 or other accepted build prerequisites are absent, CI fails rather than substitutes or weakens the build.

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

The final handback must label each of these **RATIFIED** or **PROVISIONAL** rather than silently inheriting CNR3 values:

```text
final plugin/project/DLL/package/namespace naming set
C++ language standard
VapourSynth header/API profile (identity recorded in VERSION.txt)
plugin floating-point/FMA policy
COMDAT-folding policy
version resource / version source
optional clean AVX2-capability check in plugin entry point
/guard:ehcont policy for the C++ plugin
EXE exposure/access strategy from the wheel/package
```

On a non-AVX2 CPU, code compiled globally with `/arch:AVX2` can fail with illegal-instruction exception `0xC000001D`; the README must state the requirement. A clean CPU-capability check in the plugin entry path is an optional Stage B/technical-development decision and must itself be safe to execute before AVX2-only code.

---

## 16. How the developer chats should restart after final migration close-out

When Dave explicitly authorizes return to development, both developer chats should:

1. start from the final migration commit/tag and active repository only;
2. read the final version of this common handback;
3. read `README.md`, `NOTICE.md`, `LICENSE`;
4. re-read the repository-authoritative technical documents (`02`, `05`, `06`) and Stage 2 experiment design;
5. confirm the frozen inspector/analyzer identities and current build harness work on their machine/session as appropriate;
6. follow the project-file change-control rule below rather than treating accepted build settings as casual implementation detail;
7. resume the established technical workflow:

```text
ChatGPT drafts/designs
    -> Claude independent review
    -> Dave resolves/ratifies
    -> implementation proceeds
```

A developer chat's own future-chat handover remains separate from this common migration handback.


### Project-file change control after handback (H2)

Normal development may add/remove source files from a project. Compiler, linker or manifest **setting** changes are different:

1. write every setting explicitly in the `.vcxproj` under Dave's no-defaults rule;
2. review the setting change and preserve the effective CL/LINK delta plus relevant `dumpbin`/standalone-import checks;
3. any change to `Mpeg2BlockInspector.vcxproj` or its `.filters` re-runs all six inspector index regressions;
4. the Stage C harness and Stage D CI never change/repair project settings;
5. `/GS`, CFG and CET are never turned off merely for speed - profile a specific hotspot and review any proposed exception instead. Spectre is already deliberately outside the required policy.

### Inspector regression procedure (H7)

The tracked `TESTING` BATs pipe `ffmpeg` into the inspector with `-b - -m`, then run the analyzer and `vspipe`. They contain machine-specific tool paths (including ffmpeg and the installed VapourSynth `vspipe`) and contain `pause`, so run them one at a time. After the six gated runs, restore only tracked `.log` files and remove only known untracked path-only output. A clean tracked Git status then independently proves regenerated tracked `.idx` files match. The LP case is mandatory and its SHA-256 is:

```text
849b6a9c411a7db837268af3ac54501a06f5f1158e68d5245ce2b3ec40a0d011
```

### Inspector-protection trigger (H3c)

After Stage A acceptance record SHA-256 for `Mpeg2BlockInspector.vcxproj` and `.filters`. After Stage B or later infrastructure work:

- if both remain byte-identical to the accepted Stage A versions, one LP inspector smoke run is sufficient for an infrastructure-only change;
- if either differs, run all six inspector regressions.

This trigger never overrides the stricter H2 rule above when the inspector project itself is intentionally changed.

---

## 17. Final migration close-out data still to insert

> **Historical v0.13 checklist - partly superseded.** The standalone Stage C harness and migration Stage E wheel were removed by G1/G3. The final handback instead records the proving workflow on `main`, Stage B+, the final one-file CI workflow, and migration close-out evidence. Items below referring to the old Stage C harness or Stage E wheel are **not** current migration deliverables.

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

### v0.10 - 2026-10-10

- Recorded Q1/R1/R4 evidence closure.
- Recorded A3 v0.8 candidate-under-review state without implying application or Stage A completion.


### v0.8 - 2026-10-09

- Updated controlling references to DR v0.14 / Stage A plan v0.9.
- O7=`YES`: `/favor:blend` explicit in Debug and Release and inherited by Stage B.
- Added N1 explicit `SpectreMitigation=Disabled` in both configurations while retaining `/Qspectre` absence.
- Added final build-setting pin-table/traceability expectation inherited by development.
- Corrected duplicated repository-layout introduction and stale controlling-document reference.
- Kept runtime-ownership and project-file change-control rules intact.


### v0.7 - 2026-10-09

- Recorded Dave's deliberate decision not to use Spectre mitigation.
- Kept `/GS`, CFG and CET enabled; inspector `/sdl` OFF and plugin `/sdl` ON remain unchanged.
- Removed inherited Spectre-component/MSB8040/library-provenance expectations.
- Clarified that project/harness/CI must keep `/Qspectre` absent rather than silently falling back.
- Recorded current published `main` and the interim migration checkpoint.
- Noted that the committed README needs its superseded Spectre prerequisite corrected.

### v0.6 - 2026-10-09

- Carried Claude H1/H2 MUSTs: restored static-CRT runtime ownership boundary and added explicit project-file change control after handback.
- Carried H3-H9: VERSION.txt header identity, provisional-vs-ratified choices, inspector-protection trigger, `/fp:precise` with `/fp:contract` absent, per-configuration security, exact path-case check, working plugin name, practical regression procedure, AVX2 illegal-instruction behavior and correct Claude migration-handover naming.
- The earlier inherited M7 Spectre infrastructure requirement is superseded by Dave's later decision not to use Spectre mitigation.
- Kept developer-chat successor handovers separate from migration-owned documents.

### v0.5 - 2026-10-09

- Clarified document taxonomy: this is migration-to-development handback, not migration-chat continuity and not an internal developer-chat handover.
- Updated execution state to A1/A2 applied and pre-A3 checkpoint complete, with A3 v0.3 superseded and a new AVX2/security-on A3 still required.
- Added current AVX2 minimum, `/favor:blend`, `/MT`, PDB-path, `/GS`, CFG, CET and SDL-exception policies; Spectre is deliberately not used.
- Added the project-files-as-source-of-truth and one-build-route rule for local harness/GitHub Actions.
- Added explicit README/NOTICE/LICENSE roles and the target-policy-versus-build-evidence distinction.
- Expanded the handback into a practical restart record for both development chats after migration close-out.
- Kept technical-development authority and within-dev-chat handovers explicitly separate.

### v0.4 - 2026-10-09

- Interim current-state refresh during Stage A migration work.


## Change log

### v0.9 - 2026-10-09

- Updated controlling migration documents to DR v0.15 / Stage A plan v0.10.
- Added the Q1 rule that accepted project-setting XML must carry MSBuild/VS recognition evidence, not merely syntactically plausible element names.
- Recorded tlog-derived command coverage as part of the inherited build-setting traceability.

---

## Close-out v0.13 change log (2026-10-10)

- Promoted header to accepted A3 v0.10 and pending Stage A repository close-out.
- Recorded Dave-ratified Plan section 30 deviation: six-index v0.10 status WAIVED, never PASS.
- Preserved the three explicitly supplied Claude section-3 corroboration points and the no-bytewise-proof limitation.
- Maintained permanent future compiler/toolset/codegen six-index requirement.
- Incorporated Claude final-gate review N1-N4 from section 4, with unverified Stage C/D mechanics explicitly deferred.
- Recorded README snapshot consistency assessment and live Git/repository action boundary.

## Change log v0.14 (2026-10-10, written by migration Claude at Dave's request)

- Added section R (read first): what migration did and why it matters; how to build (GUI and command line); the inherited rules with their reasons; the remaining agreed migration steps; what the development chats must handle themselves (wheel/PyPI moved to them, CPU check, `/sdl`, FP bit-exactness, CI switch failures, names, open items); what did not change; how to restart; and where the detail is.
- Marked sections 12-14 as superseded or partly superseded.
- Updated the header (Stage A closed and pushed).
- No other content changed from v0.13.

## Change log v0.15 (2026-10-10, ChatGPT verification draft for Claude)

- Preserved Claude's v0.14 section R and the historical sections. Tightened wording where it contradicted G5/G7 (expected-switch CSV and non-executed reference are allowed), G11/P5 (regression based on code-generation impact), and Dave's `main`-only workflow decision.
- Clarified installed/toolset updates, exact compiler-change acceptance, scoped build-setting change control, inspector-versus-plugin floating-point policy, and what `/sdl` actually promotes to errors.
- Explicitly superseded the old Section 17 standalone-harness/wheel close-out checklist. Preserved all Stage A hashes and the v0.10 six-index WAIVED status.
- Identified the H2/H3c versus G11/P5 interpretation as a point for Claude's cross-verification, not a unilateral new policy decision.
- No production repository/build/algorithm files changed.
