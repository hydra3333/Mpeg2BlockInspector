# Claude review of ChatGPT migration plan update (standalone Release, PyPI, release workflow)

**Filename:** Claude_REVIEW_OF_ChatGPT_Migration_Plan_Update_Standalone_PyPI_v0_1.md
**Version:** 0.1
**Date:** 2026-10-09
**Reviewer:** Claude (migration chat), cold review
**Subject:** "Migration plan update following A3 v0.2 review", pasted by Dave on 2026-10-09
**Evidence also read:** the CNR3 main zip, specifically `.github/workflows/build-windows-x64-release.yml` (281 lines) and `1.BUILD.bat`

---

## 1. Verdict

The direction is sound. Release `/MT` for the inspector EXE is the right answer to Dave's standalone requirement, and Debug `/MDd` is acceptable.

Reading CNR3's actual workflow changes two things in the plan:

- CNR3's CI does **not** build its Visual Studio project. It runs a hand-maintained `cl` command.
- CNR3's CI **already builds a pip wheel**.

There are three MUST corrections and three decisions for Dave. None of them blocks ChatGPT from drafting the next A3 candidate.

---

## 2. Answers to the five questions

### Q1. Is Release /MT right for the EXE and the DLL?

- **EXE: yes.**
  - `/MT` links both the VC runtime and the UCRT statically. Only Windows system DLLs should remain in the imports. The gate proves this (see Q2).
  - Side effect: the static UCRT now comes from whichever Windows SDK the build selected. The unpinned SDK (D2) is therefore inside the shipped exe, not just a header choice. Recording the SDK at every gate (already agreed) becomes provenance for the artefact itself.
- **DLL: yes, with known trade-offs, to be confirmed at Stage B (D5).**
  - It meets the requirement and is a common build choice for VapourSynth plugins.
  - **Separate runtime instance.** A `/MT` DLL carries its own runtime and heap. ChatGPT's rule, that no runtime-owned object or memory crosses the DLL boundary, is the right constraint. The API4 model already works this way: frames, nodes and maps go through `vsapi` functions, and the filter frees its own instance data.
  - **FLS slots (unverified for this case).** Each statically linked runtime instance uses process-wide FLS slots. Processes that load very many statically linked DLLs have been reported to exhaust them. One more plugin is unlikely to matter.
  - **Alternative: "hybrid" linking**, with the VC runtime static and the UCRT taken from Windows. It also needs no redistributable on Windows 10 and later, but its behaviour then follows the OS UCRT version, and it needs non-obvious linker overrides in the project.
  - **Recommendation: `/MT` for both**, with hybrid kept as a documented fallback.

### Q2. Should M3 change because of /MT?

Yes, but only the import part. **M3a and M3b below are a MUST.**

- **M3a. The rest of M3 is unchanged.** These stay unchanged before and after:
  - the PE characteristics: Large Address Aware, High Entropy VA, Dynamic Base, NX, no CET flag, no full CFG, x64 PE32+;
  - the Debug linker /OPT behaviour;
  - manifest generation;
  - the debug-information mode.

  Apart from `/MT` and the changes already ratified, the command lines must also match exactly.
- **M3b. Replace "imports identical" with a two-part rule for Release:**
  1. Forbidden DLL names: `VCRUNTIME*`, `MSVCP*`, `api-ms-win-crt-*`, `ucrtbase*`, `CONCRT*`, `VCOMP*`.
  2. Allowed DLL names: those in the measured checkpoint import list once the C runtime DLLs are removed, which I expect to be `KERNEL32.dll` only (unverified). Any other DLL name stops the gate.

  Expect the functions imported from KERNEL32 to grow, because the static runtime calls more of them; that is not a failure. Debug is compared at the DLL-name level and must be unchanged (ucrtbased, vcruntime140d, kernel32). The function lists may shrink slightly where D3 /Oi makes calls such as strcat intrinsic.
- **Standalone test.** The forbidden and allowed lists above are the standalone test. Put the same check in the Stage C harness and the Stage D workflow, so it is enforced everywhere the artefacts are built.

### Q3. Debug /MDd, standalone for Release only?

Acceptable. Debug is not distributed. The debug runtime DLLs cannot be redistributed in any case, and the functional gate runs the Release exe that will ship. Pin `MultiThreadedDebugDLL` explicitly, as v0.2 already does.

### Q4. Is the ordering A3, B, C, D, E sound?

Yes, with one structural MUST and one reuse note:

- **MUST M5. One build route.** The CNR3 workflow builds with a hand-written `cl` command and "flag map" (workflow lines 88-128). It does not use MSBuild on the project, even though CNR3's local `1.BUILD.bat` does.
  - That is a second, hand-maintained copy of the settings. It can drift from the `.vcxproj`, and it is a different route from the one the gates qualify.
  - Here, Stage D must invoke the **same** Stage C harness (vswhere, MSBuild, the `.slnx`, Release x64), so the ratified XML is the single source of build settings.
  - Do not adopt CNR3's flag map, and never override the toolset on the command line (for example `/p:PlatformToolset=...`) to suit a runner. If a runner lacks v145, the job should fail hard.
  - The workflow comment that "windows-latest = Windows Server 2025 + Visual Studio 2026 (v145) since the June 2026 image migration" (lines 17-18) is a dated claim and must be re-verified at Stage D.
- **Reuse note.** CNR3's workflow already builds and checks a wheel (lines 165-257):
  - layout `vapoursynth/plugins/cnr3/cnr3.dll`, which VapourSynth's recursive autoload scans;
  - tag `py3-none-win_amd64`;
  - the version taken from the release tag;
  - RECORD hashes computed by hand.

  So Stage E is largely "adapt the CNR3 wheel step", and in practice D and E fold into one workflow. Keep them as separate review stages anyway.

### Q5. Should anything be pulled earlier?

Yes, three items. One of them affects A3.

- **Package identity, before the Stage B names are ratified.** The wheel name (CNR3 uses `vapoursynth-cnr3`), the plugin folder `vapoursynth/plugins/<name>/` and the DLL name belong together. Decide them as one set with the other Stage B naming decisions. Checking whether the PyPI name is free is a lookup to do then.
- **MUST M6. Licence metadata.** CNR3's wheel metadata says `License: MIT` (workflow line 198). This project is AGPL v3 "or any later version", with the LGPL VapourSynth headers and the MSSG decoder notices carried by NOTICE. Stage E must not copy CNR3's licence line, and the wheel must carry LICENSE and NOTICE. Recording this now is cheap; doing it wrong at release is not.
- **D6, a Release link setting, decided in A3 if wanted.** Release builds embed the full absolute PDB path (for example your `E:\SOFTWARE-Win11\...` path, or the CI runner's path) in the shipped exe and dll. `/PDBALTPATH:%_PDB%` embeds the file name only. This is OPTIONAL hygiene; if you want it, it belongs in the A3 Release link settings now. I know of no dedicated MSBuild property for it, so it would go through AdditionalOptions, which ChatGPT's own rule allows only with a stated justification.
- **Nothing else from PyPI or the workflow changes the inspector's compile settings.** A version resource (VERSIONINFO) in the exe and dll is a Stage B or C choice, not A3.

---

## 3. Recommended attribution: put /MT in its own commit (D4)

A3 currently would combine three changes that each move generated code or linkage:

- the x64 host;
- `/GL` with `/LTCG`;
- `/MT`.

If an index then differs, there would be no way to tell which caused it. Recommendation:

- **A3: normalisation only.** All the pins, plus the host, D1, D3 and `/Zi`. Release stays `/MD`, so M3 is applied strictly: imports identical.
- **A4: Release `/MT` only.** Its own small diff, with its own gate: M3b's import rule plus the six indexes.

The cost is one more six-index run. In return, each change can be attributed and reverted on its own, and the standalone change is recorded as a distribution decision, separate from normalisation.

---

## 4. Decisions for Dave

| # | Question | Options | Recommendation |
|---|---|---|---|
| D4 | Apply Release /MT in A3 or in a separate A4? | (a) separate A4 commit with its own gate; (b) fold into A3 | **(a)**, for attribution (section 3). |
| D5 | DLL runtime model (confirmed at Stage B) | (a) /MT; (b) hybrid: static VC runtime plus Windows UCRT | **(a)**, with hybrid as the documented fallback. |
| D6 | Strip the absolute PDB path from Release artefacts? | (a) yes, `/PDBALTPATH:%_PDB%` in Release; (b) no, keep the default | **(a)**, mildly. It is distribution hygiene, not correctness. |

---

## 5. MUST summary

- **M3a / M3b.** Keep the PE characteristics strict, and replace "imports identical" with the forbidden and allowed import lists for Release. Use the same rule in the harness and the workflow.
- **M5.** CI builds through the Stage C harness (MSBuild on the `.slnx`), not a duplicated `cl` flag map, and never overrides the toolset.
- **M6.** The wheel licence metadata is AGPL-3.0-or-later, with LICENSE and NOTICE included. Do not copy CNR3's MIT line.

The scope boundary is unchanged: none of this authorises Stage 2 deblocking work.
