# Claude review of the Stage A close-out document package (v0.2)

**Filename:** Claude_REVIEW_OF_ChatGPT_StageA_Closeout_DocSet_v0_1.md
**Version:** 0.1
**Date:** 2026-10-10
**Reviewer:** Claude (migration chat)
**Subject:** `StageA_Closeout_20261010_Claude_Review_v0_2.zip`: DR v0.19, Plan v0.14, Handback v0.13, Knowledge v0.5, Handover v0.12, the README consistency assessment, the corrections note and the reviews.

**Checked by script:**
- all 15 `PACKAGE_SHA256.txt` entries verify;
- every text file is US-ASCII with CRLF line endings and no BOM;
- all four of my reviews in the package are byte-identical to what I issued, including the final gate review, which the v0.1 package lacked.

---

## 1. Verdict

**Accepted. No MUST or SHOULD findings.** Stage A can be closed once Dave has done the three local steps in section 3.

---

## 2. What I checked

| Item | Result |
|---|---|
| **Headers** | All five are current: A3 v0.10 accepted; W1, HostX64, warnings, W2, hashes, frozen files and hygiene PASS; six indexes **WAIVED (not PASS)**; README live check and Git close-out pending. The DR supersedes v0.18 and the handover supersedes v0.11. |
| **Waiver** | Recorded as a Dave-ratified deviation, with the three-point evidence from my final gate review section 3, and labelled "strong evidence ... not byte-for-byte proof".
- Plan v0.14 keeps section 30's "No representative subset or waiver is allowed." verbatim (line 1345). The A3 v0.10-only exception is placed directly after it and explicitly labelled (lines 1347-1357), with "no continuing authority".
- No document labels the six indexes PASS for v0.10. |
| **N1-N4** | Transcribed accurately from my final gate review section 4 into all five documents (DR lines 74-112, and the same block in the other four). They are labelled as Stage C/D notes, **not** A3 gate conditions, and my unverified items stay marked unverified. |
| **Earlier decisions** | The 64-bit policy, discovery, K1-K4, K3 option (a) and the deferred toolset change are all still present. The production `.vcxproj` is untouched. |
| **No premature closure** | Every document says that the commit, push and tag have not happened. |

---

## 3. README: I can close most of the live check from the pushed snapshot

The `README.md` in Dave's GitHub snapshot (pushed `main`, downloaded today) is consistent with the accepted build:
- x64 only (line 26);
- AVX2 required, with CPU generations (line 27);
- "No Visual C++ Redistributable is needed" (line 28), which matches the imports: `KERNEL32.dll` only;
- `/GS`, CFG and CET hardening, and "Spectre mitigation is deliberately not required" (line 32);
- build through `VapourSynth-mpeg2Deblock.slnx`, Release or Debug x64 (line 33);
- "The build settings live in the project files" (line 34);
- the AGPL "version 3 or any later version" wording and the NOTICE section at the top.

It makes no claim about automatic toolset selection. (The "gcc / clang" remark at line 69 is in the original background notes, which describe the reference decoder's history, not this build. No change is needed.)

**What remains is to prove the working copy's README is that same file.** Dave runs, in the repository:

```text
git diff --stat HEAD -- README.md
git log -1 --format="%H %s" -- README.md
git status --short
```

An empty first output means the live README equals the committed and pushed one I checked. The `git status` should show only the five new or updated documents once they have been copied into `docs\HANDOVER\migration\`.

---

## 4. Stage A close-out, in order (Dave)

1. Copy the five documents, plus this review and `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_10_Final_Gate_v0_1.md`, into `docs\HANDOVER\migration\`.
2. Run the three README commands above. The first must print nothing.
3. Run `git add -A --dry-run`, then `git add -A`, then `git diff --cached --stat`. Commit (suggested message: `Stage A closed: A3 v0.10 accepted (six-index WAIVED for v0.10), close-out docs`) and push.
4. Optionally tag the commit, for example `post-stageA-vs-normalization`. That is Dave's call, and a tag can be added later.

Then: the post-Stage-A toolset candidate (`DefaultPlatformToolset` plus a numeric minimum-v145 guard, proven locally first), followed by Stage B.
