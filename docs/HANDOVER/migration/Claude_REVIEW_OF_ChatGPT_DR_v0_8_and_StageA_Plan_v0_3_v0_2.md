# Claude review of Design Record v0.8 and Stage A Execution Plan v0.3

**Filename:** Claude_REVIEW_OF_ChatGPT_DR_v0_8_and_StageA_Plan_v0_3_v0_2.md
**Version:** 0.2
**Date:** 2026-10-09
**Reviewer:** Claude (migration chat), cold review
**Subject:** Migration_Plan_Update_v0_8_and_StageA_v0_3.zip, containing:
- Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_8.md (39,414 bytes);
- StageA_Visual_Studio_Normalization_Execution_Plan_v0_3.md (32,683 bytes).

**Method:** v0.8 was diffed line by line against v0.7, and plan v0.3 was read in full. Both files are US-ASCII with CRLF line endings, no BOM and no bare LF (checked by script).

---

## 1. Verdict

Both documents faithfully carry the four Claude reviews of today and Dave's new requirements:
- the A3/A4 split;
- the M3 PE and import gate;
- S7-S9;
- the one-build-route rule;
- the forbidden runtime DLL list;
- SDK provenance;
- Stages C, D and E;
- AGPL-3.0-or-later and NOTICE.

There are no MUST corrections. Two SHOULD items and three OPTIONAL items follow. Dave needs to decide D4, D5 and D6 before the revised A3 is drafted.

---

## 2. SHOULD

**S10. Restore the authorisation guard in DR section 39.**

v0.7 ended with "No Stage A project-setting change or Stage B project creation is authorized merely by this document." v0.8 replaces it with "No Stage 2 algorithm implementation is authorized by this document." That drops the guard on project changes.

Keep both sentences, for example: "No project or solution change, and no Stage B project creation, is authorised by this document; each step requires Claude review and Dave ratification. No Stage 2 algorithm implementation is authorised."

**S11. Plan section 23, linker/manifest pins: name the remaining mitigation settings.**

The list is introduced with "including", but it omits the items from my A3 v0.2 review M3:
- Link `CETCompat`;
- ClCompile `ControlFlowGuard`;
- Configuration `SpectreMitigation`.

Under the no-defaults ruling, the revised A3 should either pin each at its measured value, or say in one line why not, for example if current Microsoft documentation shows no supported property.

All three are in fact also caught by the gate. /Qspectre and /guard:cf would appear in the cl.exe command line, and /CETCOMPAT in the link.exe command line or in the dumpbin flags. So this is belt and braces, not a hole.

---

## 3. OPTIONAL

- **O4.** Add `MSVCR1*` (older Visual C++ runtimes such as MSVCR120.dll) to the forbidden list (DR "PE / load-config / import gate" section; plan section 35). It cannot normally appear, but the list is the standalone test and should be complete. Do not use a bare `MSVCR*` pattern, which would also match the Windows system `msvcrt.dll`.
- **O5.** Plan section 23 pins `GenerateDebugInformation = true`, which emits a bare `/DEBUG`. Whether that means FULL or FASTLINK is itself a linker default. If current documentation confirms the measured meaning, pin `DebugFull`. This affects only the PDB, so it is low impact.
- **O6.** Plan section 34 rebuilds only Release for A4. A Debug rebuild with an unchanged command line costs little and proves A4 touched only Release. Optional.

---

## 4. Verified as carried correctly (NO OBJECTION)

| Item | Where |
|---|---|
| A3 keeps /MDd and /MD pinned; /MT only in A4; harness/workflow may not inject /MT | DR "Release runtime / standalone distribution policy"; plan sections 3, 23, 32 |
| The DLL-name sets must be unchanged through A3, while function-level imports may change under D3 | plan section 28 |
| A4 runs a second six-index regression | plan sections 36, 38 |
| /O2 components (including /GF) are pins; /GL and /LTCG are the D1 additions | plan section 23 |
| HostX64\x64 is proved for both CL and LINK | plan sections 23, 26, 34 |
| S7 warning-output pins (DiagnosticsFormat, UseFullPaths, ExternalWarningLevel) | plan section 23 |
| S9 source/header ItemGroups are NOT APPLICABLE | plan section 21 |
| Deliberate default exceptions: SDK (D2) and LanguageStandard_C | plan section 22 |
| D6 kept separate and explicit | plan section 23 |
| One build route; no toolset override; dated runner claims re-verified | DR sections 29, Stage C |
| Do not copy CNR3's MIT metadata; LICENSE and NOTICE in the wheel | DR section 33 |
| Package identity reviewed as one coupled set before Stage B names | DR section 32 |
| Review documents committed by name or removed before close-out | plan section 37 |
| Six baselines are the tracked `.idx` files in git, with the SHA list as a convenience copy | plan section 18 |

---

## 5. Decisions - RATIFIED by Dave 2026-10-09

- **D4 = NO.** Dave accepts the attribution risk to speed the migration up: Release `/MT` is consolidated into A3, and there is no separate A4.
- **D5 = YES.** The plugin DLL uses `/MT`, with the "hybrid" model kept only as a documented fallback.
- **D6 = YES.** Release artefacts embed the PDB file name only (`/PDBALTPATH:%_PDB%`, through `AdditionalOptions` unless current documentation shows a supported property). It is part of the A3 Release linker delta.

### 5.1 Consequences ChatGPT must carry into DR v0.9 / plan v0.4 and the revised A3

1. **Delete the A4 stage.** Remove plan sections 32-36 and the A4 branch of section 38, and remove the A3/A4 split text from the DR. A3 now owns three things:
   - Release `RuntimeLibrary=MultiThreaded` (/MT), with Debug staying /MDd, pinned;
   - D6 `/PDBALTPATH:%_PDB%` in Release;
   - everything already listed for A3.
2. **Rewrite the A3 import gate.** Plan section 28's "DLL-name sets unchanged" now applies to Debug only. Release uses the standalone rule:
   - none of `VCRUNTIME*`, `MSVCP*`, `api-ms-win-crt-*`, `ucrtbase*`, `CONCRT*`, `VCOMP*` (plus `MSVCR1*`, O4);
   - allowed DLL names are the checkpoint Release set minus the runtime DLLs, currently `KERNEL32.dll`;
   - any other DLL name stops the gate.

   The rest of the M3 PE/load-config baseline must still be identical.
3. **Rewrite the command-line delta.** For the Release compiler, the expected change becomes `/MD` -> `/MT` in addition to the other ratified A3 changes, and the Release linker gains `/PDBALTPATH:%_PDB%`. Nothing else may be unexplained.
4. **Update the expected Debug warnings.** No change from D4: Debug is still /MDd. Release may gain or lose runtime-related link warnings; explain each.
5. **Add a diagnosis plan for failure.** This is the price of D4 = NO. If any of the six indexes differs after A3, do not loosen the gate. Bisect by building local, uncommitted variants, in this order:
   1. A3 with Release /MD restored;
   2. then also without /GL and /LTCG;
   3. then also with PreferredToolArchitecture x86.

   That isolates the cause. Then return to Claude and Dave with the evidence.
6. **SDK provenance (from v0.8) applies at A3.** The selected SDK's static UCRT is now inside the A3 Release exe.
7. **Stage B.** `mpeg2Deblock.vcxproj` carries Release `/MT` and `/PDBALTPATH:%_PDB%` from the start, and runs the same standalone import gate.

| # | Question | Recommendation |
|---|---|---|
| D4 | Separate A4 commit for Release /MT (its own gate) instead of folding it into A3? | Yes, separate. |
| D5 | Plugin DLL runtime model: /MT, with "hybrid" as the documented fallback? (DR v0.8 already records /MT as the "current required direction") | Yes, /MT. |
| D6 | Embed only the PDB file name (`/PDBALTPATH:%_PDB%`) in Release artefacts? | Yes, mildly. If accepted, it goes into the reviewed Release linker delta. |

---

## 6. Change log

- v0.2: recorded Dave's ratification (D4 = NO, D5 = YES, D6 = YES) and the consequences in section 5.1. Sections 1-4 are unchanged.
- v0.1: initial review.
