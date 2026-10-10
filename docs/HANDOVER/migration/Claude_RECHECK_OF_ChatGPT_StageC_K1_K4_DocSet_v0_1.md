# Claude re-check of K1-K4 (Stage C disposition and document set)

**Filename:** Claude_RECHECK_OF_ChatGPT_StageC_K1_K4_DocSet_v0_1.md
**Version:** 0.1
**Date:** 2026-10-10
**Reviewer:** Claude (migration chat)
**Subject:** `StageA_StageC_20261010_K1_K4_Claude_Recheck.zip`: DR v0.18, Plan v0.13, Handback v0.12, Knowledge v0.4 and Handover v0.11, as revised.

**Checked by script:**
- all 9 `PACKAGE_SHA256.txt` entries verify;
- every file is US-ASCII with CRLF line endings and no BOM;
- my two reviews are byte-identical to what I issued, and ChatGPT's cold review is unchanged.

---

## 1. Verdict

**K1-K4 are done in DR v0.18, Plan v0.13, Handback v0.12 and Knowledge v0.4. Accepted.**

**Handover v0.11 is fixed at the top, but three sections further down still point at the old document versions (H1).** That is a small edit. It matters because the reading order is how a new chat starts.

---

## 2. Checks

| Item | Result |
|---|---|
| **K1: headers** | All four documents now state the current position in their header: A3 v0.10 (`73e9019c...db46`) ratified and applied, rebuilds RC=0, W1 PASS (33 / 32 / 23 / 25), HostX64 PASS, warning comparison next, Stage A open. The DR's Supersedes line now names v0_17. The handover header now says it is from ChatGPT ("Claude did not author this v0.11 revision") and supersedes v0_10, and its section 0.1 and 0.3 mark steps 1-3 DONE/PASS with step 4 NEXT. |
| **K2: placement and label** | In all five, the addendum now follows the metadata header. The phrase "review draft" appears nowhere (count 0 in each file). |
| **K3: compiler policy** | DR line 37 (and the same line in the other four) carries Dave's option (a) sentence exactly. "No project-level `VCToolsVersion` override: the designated current build is recorded, not pinned" is stated, and the selection mechanics remain marked unverified. |
| **K4: auto-imports** | All five carry the rules:
- fail closed on `Directory.Build.props`, `.targets` or `.rsp` in any ancestor folder, from the repository's parent up to the drive root;
- refuse unreviewed in-tree ones;
- run MSBuild with `-noAutoResponse`;
- prove it once with a scratch ancestor `Directory.Build.props`. |
| **Boundaries** | No production project change. The compiler-policy project change is deferred until after Stage A. The fixed MSBuild path is for the A3 gate only. |

---

## 3. H1: Handover v0.11, three stale sections (SHOULD; fix before the handover is next used)

1. **Section 2, reading order.**
   - Item 2 names `StageA_VS2026_MSBuild_Hard_Earned_Knowledge_v0_3.md`; it should be **v0_4**.
   - Item 9 names DR **v0_17**, Plan **v0_12** and Handback **v0_11**, and says "All three still describe v0.9"; it should be **v0_18 / v0_13 / v0_12**, now current.
   - Add items for `Claude_REVIEW_OF_ChatGPT_StageC_MSBuild_Discovery_Proposal_v0_3.md`, `Claude_REVIEW_OF_ChatGPT_StageC_Disposition_and_DocSet_DR_v0_18_v0_1.md` and `ChatGPT_COLD_REVIEW_OF_Claude_StageC_MSBuild_v0_3_v0_1.md`.
2. **Section 10, review status.**
   - Add the Stage C review v0.3 (M1-M5, accepted with ChatGPT's Q1-Q6 qualifications).
   - Add the document-set review v0.1 (K1-K4, closed by this re-check).
   - Add this re-check.
3. **Section 11, documents.**
   - The table still lists DR v0.17, Plan v0.12, Handback v0.11 and Knowledge v0.3 as current.
   - It still says "`ChatGPT_Migration_Chat_Handover_v0_11.md` (this file) -> v0.11 at close-out".
   - Update it to the current versions, with "-> next at close-out" (v0.19 / v0.14 / v0.13 / v0.5 / v0.12).

No re-review is needed for H1 if the change is limited to those three sections. I will see the result in the next package anyway.

---

## 4. Note

The A3 v0.10 gate continues as planned: warning comparison next, then W2 (dumpbin), hashes, frozen sources, six indexes, `git status` and the evidence package for Claude. None of these document edits affect it.
