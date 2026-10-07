# Claude - Review of Stage 2 Experiment Design v0.2

**Filename:** `Claude_REVIEW_OF_ChatGPT_Stage2_Experiment_Design_v0_2.md`
**Version:** 0.1
**Date:** 2026-10-08
**Author:** Claude
**Reviews:** `Stage2_Experiment_Design_v0_2.md` ("S2"), against the ratified repository
(`05` v1.1, `06` v1.1, `02` v0.4 in `REPOSITORY_RATIFIED_2026-10-08.zip`) and V1-V4.
**Status:** Review input only. Not project authority.

---

## 0. Ratified repository check

`REPOSITORY_RATIFIED_2026-10-08.zip` was checked against the reviewed drafts: US-ASCII, CRLF, zero
bare LF; the only changes are the expected status flips (D-11, D-17, D-18 SUPERSEDED; D-08, D-15
AMENDED; D-23 CLARIFIED; D-24..D-26 DECIDED; K-07, K-10, K-11 ACCEPTED; headers RATIFIED). No
objection.

---

## 1. Verdict

**Approve with two MUST changes** (sections 2.1 and 2.2), both small and both about geometry or
validation that a later result would otherwise silently depend on. The rest is sound and faithful to
D-24/D-25/D-26.

---

## 2. MUST CHANGE

### 2.1 N0 must cover the internal vertical seam too (S2 1.4, 10 Step 5)

S2 1.4 says "vertical transform-grid seam positions do not depend on FRAME versus FIELD state", and
N0 says "do not invent an internal transform seam in NONE". Read together, a NONE macroblock would
still be filtered at its internal vertical seam (x = 8 within the macroblock).

But a NONE macroblock has no coded blocks at all, so it has **no internal seams in either
orientation**: no x = 8 vertical seam and no mid-height horizontal seam. Only its macroblock edges
remain, where prediction steps can occur. (For FRAME and FIELD macroblocks the x = 8 vertical seam
does exist: V1, blocks 0/1 and 2/3 are left/right in both organisations.)

Fix: state in 1.4 and N0 that internal seams, vertical and horizontal, exist only for FRAME/FIELD
macroblocks; NONE keeps macroblock-edge locations only. A one-line note should also go into the next
`06` revision (4.1 implicitly assumes a coded macroblock); not blocking for S2.

### 2.2 The registration check needs a horizontal test and a shifted-label control (S2 6.2)

As written, 6.2 compares the mid-height step for FRAME versus FIELD macroblocks. That tests vertical
registration only, and gives an absolute result that is hard to judge if it comes out "weakly
stronger".

- **Horizontal offsets are not caught.** A shift of a few pixels, or of a whole macroblock, leaves the
  mid-height rows where they are; FRAME/FIELD labels are spatially correlated (most neighbours share a
  state), so the contrast would only weaken, not vanish.
- **Fix (still detector-free):** compute the same FRAME-minus-FIELD contrast with the index labels
  shifted by -1, 0 and +1 macroblock in x and in y. Correct registration means the contrast **peaks at
  zero shift**. Add a grid-phase check: mean luma step across columns at x mod 8 = 0 versus the other
  seven phases; the step should peak at phase 0.

Neither step infers geometry; both only ask whether the index and pixels line up.

---

## 3. SHOULD CHANGE

1. **QP value cannot be measured on the transcode pairs.** The `_blocky` clips have QP 62 in every
   macroblock, so Step 2 (fixed median) and Step 3 (real map) are identical there. State this in 13.3 /
   18.2 so identical transcode results are not read as "the QP map does not matter". The QP-map
   question rests on real LG diagnostics and Dave's viewing.
2. **K0 selection bias (8.4).** K0 is chosen on LP *with fixed QP*, then fixed and real QP are compared
   on the same LP frames. That favours the fixed-QP variant. Cheap mitigation: select K0 on half the LP
   GOPs (e.g. even-numbered) and run the 2-vs-3 comparison on the other half, or keep K0 selection to a
   small declared grid chosen before viewing.
3. **Reader cross-check (S2-I1).** The new Stage 2 index reader should reproduce analyzer v0.2's
   summary totals for each clip (records, FRAME/FIELD/NONE, QP histogram). Cheap, and it ties the new
   code to already-verified numbers.
4. **Shared-boundary QP (9.3).** Rounded mean is a reasonable start (as far as I know, without
   checking, H.264's in-loop filter averages the two sides' QP). Note that LP has QP 112 macroblocks
   next to QP 14 ones; mean gives 63. If min/mean/max are compared later, report that population
   separately.

---

## 4. Answers to S2 section 21

| Q | Answer |
|---|---|
| 1 Authority fidelity | Yes. D-24/D-25/D-26 implemented; no discarded experiment reintroduced |
| 2 Registration | Not sufficient as written: add 2.2 |
| 3 K0 freeze | Clean in principle; add 3.2 mitigation |
| 4 Fixed QP | Yes, per-clip median |
| 5 Shared-boundary QP | Reasonable first hypothesis; 3.4 |
| 6 NONE | Conservative once 2.1 is fixed; index-consistent |
| 7 Chroma | Yes. V2/V3/V4 distinctions preserved; same-field chroma kept experimental. Note the support limit: 4 same-field chroma samples per block, so corrections should modify at most 2 per side (1.6 covers it) |
| 8 Progressive access | Correct |
| 9 Evidence hierarchy | Clear; add 3.1 |
| 10 Hold-out discipline | Appropriate. LP is one 8-second clip (17 GOPs), so the hold-outs carry the generalisation weight, as designed |
| 11 Leading B | Correct and sufficient; zero exclusions for clips starting with I is the expected case |
| 12 Implementation order | Keep; add 3.3 to S2-I1 and 2.2 to S2-I2 |
| 13 Stage 1 unfreeze | Nothing in S2 requires it |

---

## 5. Change log

### v0.1 - 2026-10-08

- Review of Stage 2 design v0.2 and check of the ratified repository zip: two MUST (NONE vertical
  seam; registration check), four SHOULD.
