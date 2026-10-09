# Claude review of the migration documents against the handover taxonomy

**Filename:** Claude_REVIEW_OF_ChatGPT_Migration_Docs_and_Handover_Taxonomy_v0_1.md
**Version:** 0.1
**Date:** 2026-10-09
**Reviewer:** Claude (migration chat), cold review
**Request:** ChatGPT's taxonomy note (pasted by Dave on 2026-10-09) and `migration.zip` (Dave's `docs\HANDOVER\migration` folder).

**Documents reviewed:**
- `Migration_Design_Record_D-C_CNR3_VS2026_Intent_v0_11.md`;
- `StageA_Visual_Studio_Normalization_Execution_Plan_v0_6.md`;
- `MPEG2_Deblocking_Developer_Handback_v0_5.md`;
- `ChatGPT_Migration_Chat_Handover_v0_2.md`.

All four are US-ASCII with CRLF line endings, no BOM and no bare LF (checked by script). DR v0.11 and plan v0.6 are byte-identical to the copies I diffed earlier today; against v0.10 and v0.5 they add only the README/NOTICE documentation policy.

---

## 1. The taxonomy: agreed, with one correction about Claude's documents

I agree with ChatGPT's three document roles:

1. migration-only continuity handovers;
2. the common migration-to-development handback;
3. each development chat's own continuity handover.

**Correction (MUST, for every document that names it).** ChatGPT's note says "Your `Claude_HANDOVER_TO_Future_Claude_Chat_...` serves the analogous migration-only purpose". It does not. The two Claude handovers are:

| Role | File | Owner |
|---|---|---|
| 1. Migration continuity (Claude) | `Claude_HANDOVER_TO_Future_Claude_Migration_Chat_v0_*.md` (v0.1 issued today; v0.2 accompanies this review) | this migration chat |
| 3. Development continuity (Claude) | `Claude_HANDOVER_TO_Future_Claude_Chat_v0_*.md` | the Claude technical-development chat (Stage 2 reviewer) |

**My own boundary error, which I withdraw.** Earlier today, at Dave's request, I issued `Claude_HANDOVER_TO_Future_Claude_Chat_v0_5.md`. That is the development chat's handover, so editing it crossed the boundary in exactly the way the taxonomy forbids.

- **Withdraw v0.5.** Remove it from `docs\HANDOVER\migration\`; it is in Dave's migration folder now. Do not commit it.
- **v0.4 stands until the development chat replaces it.** Note its provenance problem: v0.4 was itself edited by migration ChatGPT, so it is not purely the development chat's own text either.
- When development resumes, the development Claude chat should issue its own next version, pointing to the final common handback for migration facts.

---

## 2. Root cause of the missing M7: my latest review never reached ChatGPT

`Claude_REVIEW_OF_ChatGPT_DR_v0_10_and_StageA_Plan_v0_5_v0_1.md` is **not in Dave's migration folder**. It holds:
- MUST M7 (missing Spectre libraries must fail the build);
- S12-S15 and O7-O8.

ChatGPT's migration handover v0.2 (section 1) also does not list it, and DR v0.11 / plan v0.6 contain none of its items (a grep finds no MSB8040, /fp:contract, per-configuration security statement or timing item). That explains why M7 is still open.

**Action (MUST):**
1. Dave adds that review to the folder and gives it to ChatGPT.
2. ChatGPT adds it to its migration handover reading list (section 1) and to the A3 requirements (section 12).
3. M7 and S12-S15 are carried into the next DR and plan, or into the superseding A3 package.

Also missing from the folder: `Claude_HANDOVER_TO_Future_Claude_Migration_Chat_v0_1.md` and its v0.2 (my migration handover), plus several earlier Claude reviews (see the map in my handover v0.2, section 8). Keep the current review files in the folder so neither chat works from a partial set.

---

## 3. Developer Handback v0.5, read as a receiving development chat

The question I asked of it: could the development chats start analysis and coding safely from this alone, plus the repository authorities?

It gives them the repository identity, layout, frozen-source boundary, build policy, SDK/toolset policy, the six baselines, the README/NOTICE/LICENSE roles, what stays theirs, and the restart steps. Its document boundary (section 1) is right.

What it lacks is what a chat that is about to *write code* needs. Several of these items were in v0.4 and were lost in the v0.5 rewrite.

### MUST

- **H1. The runtime ownership rule for the plugin was dropped.**
  - v0.4 section 19 said: "No CRT-owned memory/object may cross the plugin boundary when using the static runtime."
  - v0.5 section 9.2 states Release /MT for the DLL but not the consequence.
  - The development chats write the plugin code, so they are the ones who must obey it: memory allocated by the plugin is freed by the plugin, and everything crossing the boundary goes through the `vsapi` functions.
  - Restore it in sections 9.2 and 13.
- **H2. No change-control rule for project files after handback.**
  - Section 16 point 6 says only "treat the accepted Visual Studio project files ... as infrastructure, not as an invitation to redesign". A development chat needs to know what it *may* do. Proposed rule:
    1. Adding or removing source files in a project is normal development work.
    2. Any compiler, linker or manifest **setting** change is written explicitly in the `.vcxproj`, under Dave's no-defaults ruling, and goes through review. The effective-command-line delta and the dumpbin / standalone-import checks must be run.
    3. Any change to `Mpeg2BlockInspector.vcxproj` or `.filters` re-runs all six indexes.
    4. Settings are never changed in the harness or CI, only in the project files.
    5. A security setting is never turned off for speed. A specific hotspot is profiled and reviewed instead.
  - Without this the development chats are either blocked or unconstrained.

### SHOULD

- **H3. Restore three other v0.4 items that development needs:**
  - **(a) Header identity.** The vendored VapourSynth headers live in `third_party\vapoursynth\include\`, and `VERSION.txt` is the single place that names the release (v0.4 section 20).
  - **(b) Ratified versus provisional build choices** (v0.4 section 21). These include the C++ standard, the header/API profile, the floating-point mode, COMDAT, the version resource and the naming set. The final handback must mark each RATIFIED or PROVISIONAL, because the development chats inherit them.
  - **(c) The inspector-protection trigger** (v0.4 section 22).
- **H4. Floating point and per-configuration security.** When decided, state:
  - /fp:precise without /fp:contract (no FMA contraction under AVX2; my S14);
  - which configurations carry /GS, CFG, CET and Spectre (my S12).

  Kernel authors need both.
- **H5. Exact path case.** The handback (sections 3 and 13) and ChatGPT's migration handover write `vs\VapourSynth-mpeg2deblock\` and `VapourSynth-mpeg2deblock.slnx`. The A2 runbook and the TESTING BATs use `VapourSynth-mpeg2Deblock`. Windows ignores the difference, but Git paths, CI on other filesystems and humans do not. Confirm the committed case with `git ls-files vs` and use it everywhere.
- **H6. Plugin name.** `mpeg2Deblock` is used as if final (sections 9.1, 9.2 and 13), while section 3 says naming is undecided. Label it "working name" until the Stage B naming decision.
- **H7. How to run the regression.** Add the practical facts a development chat needs to reproduce baselines:
  - the TESTING BATs pipe ffmpeg into the inspector with `-b - -m`, then run the analyzer and vspipe;
  - they contain machine-specific tool paths (ffmpeg, the VapourSynth R81 vspipe) and a `pause`;
  - after a run, restore only the `.log` files; a clean tracked status then proves the `.idx` bytes matched;
  - LP is the mandatory hash case.
- **H8. AVX2 failure mode.** On a non-AVX2 CPU the programs crash with an illegal-instruction error; the README says so. An optional CPU check in the plugin's entry point is a development decision, so list it in section 15.
- **H9.** Name Claude's migration handover correctly in section 1 (see this review's section 1).

### OPTIONAL

- **H10.** At finalisation, drop migration candidate history from section 8 (A3 v0.2 / v0.3 superseded). That is migration-only detail; development needs only the final state and gate results.

---

## 4. Boundary crossings in DR v0.11 and plan v0.6

- **SHOULD B1.** DR v0.11 lines 1230-1231 tell migration to "update the ChatGPT role-specific handover" and "update the Claude role-specific handover" so they point to the common handback. Under the taxonomy, migration does not edit the development chats' handovers. Reword to: "Dave gives the final common handback to both development chats; each development chat updates its own handover to reference it."
- **SHOULD B2.** DR v0.11 lines 46 and 1329 say the "future-ChatGPT handover" must reference README and NOTICE. Make clear which document is meant. The migration handover may; the development handover is the development chat's business.
- **No crossing found in plan v0.6.** It does not mention handovers at all.
- **Open question, carried from earlier.** DR v0.11, plan v0.6, handback v0.5 and ChatGPT's handover all say the README "has already been updated". **Has it been committed?** If so, the published README already claims AVX2, standalone runtime and Spectre for a build that does not yet have them. My advice stands: commit it with A3 or after the A3 gate.

---

## 5. ChatGPT_Migration_Chat_Handover_v0_2

A good migration-only document. The taxonomy section, the state table, the "do not apply superseded A3" rule and the lessons (section 20) are all correct and useful.

- **MUST.** Add the missing review (section 2 above) to the reading list in section 1 and carry M7 and S12-S15 into section 12.
- **SHOULD.**
  - Fix the Claude handover naming in section 0 and the note (this review's section 1).
  - Fix the path case (H5).
- **NO OBJECTION.** The new detail is fine: the pre-Stage-A tag at `b38fde11...` and the A1/A2 commits being local and ahead of origin. It belongs in a migration handover and should not go into the common handback except as the final pushed state.

---

## 6. What in my migration handover should stay migration-only, and what should reach the handback

**Stays migration-only** (in `Claude_HANDOVER_TO_Future_Claude_Migration_Chat_v0_*`):
- candidate history and hashes;
- my review map;
- the pending-review list;
- the pitfalls of this chat;
- the unverified MSVC notes (MSB8040, CETCOMPAT property, FASTLINK);
- the CNR3 workflow line references;
- the Phase 2 path-edit script.

**Should reach the common handback** (once settled), because development needs it:
- the runtime ownership rule (H1);
- project-file change control and the no-defaults rule (H2);
- the header-identity rule (H3a);
- ratified versus provisional build choices (H3b);
- the inspector-protection trigger (H3c);
- the floating-point / FMA outcome and per-configuration security (H4);
- the regression procedure (H7);
- the harness's hard failure on missing Spectre libraries. That is a fact about the infrastructure development inherits, so it belongs in Stage C/D once implemented.

---

## 7. Summary of actions

| # | Who | Action | Class |
|---|---|---|---|
| 1 | Dave | Withdraw `Claude_HANDOVER_TO_Future_Claude_Chat_v0_5.md` from the migration folder; do not commit it | MUST |
| 2 | Dave -> ChatGPT | Supply `Claude_REVIEW_OF_ChatGPT_DR_v0_10_and_StageA_Plan_v0_5_v0_1.md`; carry M7 and S12-S15 | MUST |
| 3 | ChatGPT | Correct the Claude handover naming in the note, the handback and the migration handover | MUST |
| 4 | ChatGPT | Handback: restore the runtime ownership rule (H1); add project-file change control (H2) | MUST |
| 5 | ChatGPT | Handback: H3-H9 | SHOULD |
| 6 | ChatGPT | DR: reword the boundary lines (B1, B2) | SHOULD |
| 7 | Dave | Answer: has README.md been committed yet? | question |
| 8 | Dave | Add `Claude_HANDOVER_TO_Future_Claude_Migration_Chat_v0_2.md` to the migration folder | housekeeping |

No Stage 2 or deblocking work is implied by this review.
