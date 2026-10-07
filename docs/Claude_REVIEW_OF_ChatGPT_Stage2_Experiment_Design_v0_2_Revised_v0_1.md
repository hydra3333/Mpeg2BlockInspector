# Claude - Review of Stage 2 Experiment Design v0.2 (revised after Claude review)

**Filename:** `Claude_REVIEW_OF_ChatGPT_Stage2_Experiment_Design_v0_2_Revised_v0_1.md`
**Version:** 0.1
**Date:** 2026-10-08
**Author:** Claude
**Reviews:** `Stage2_Experiment_Design_v0_2_REVISED_AFTER_CLAUDE_REVIEW.md` ("S2r"), against
`Claude_REVIEW_OF_ChatGPT_Stage2_Experiment_Design_v0_2.md` ("R1").
**Status:** Review input only. Not project authority.

---

## 1. Verdict

**NO OBJECTION to ratification.** Both MUST items and all four SHOULD items from R1 are carried
correctly. Nothing ratified is altered. Format: US-ASCII, 1388 CRLF, zero bare LF or CR (checked).

Three small points follow. None blocks ratification; 3.1 and 3.2 are one-line clarifications that
can be made now or at S2-I1 / S2-I3.

---

## 2. R1 items - disposition

| R1 item | Where in S2r | Result |
|---|---|---|
| MUST 2.1 NONE has no internal seam in either orientation | 1.4 (NONE block and paragraph), Step 5 N0, S2-I6 | Done, correctly worded |
| MUST 2.2 shifted-label control and grid-phase check | 6.2.1, 6.2.2, 6.2.3, S2-I2 | Done. Labels shifted, not pixels; stays detector-free |
| SHOULD 1 QP-62 transcodes cannot test the QP map | 13.3, 18.2 | Done |
| SHOULD 2 K0 selection bias | 8.4, S2-I3, S2-I4 | Done (even/odd GOP split, declared in advance) |
| SHOULD 3 reader reproduces analyzer v0.2 totals | 6.1, S2-I1 | Done |
| SHOULD 4 high-disparity shared-boundary QP | 9.3 | Done |

---

## 3. SHOULD CHANGE (non-blocking)

### 3.1 Define "GOP" and the numbering base for the 8.4 split

"Even-numbered usable LP GOPs" is ambiguous in two ways:

- **Base:** is the first GOP number 0 or 1? The parity assignment is meant to be fixed before
  results are seen, so the base must be stated.
- **Boundary:** the index is in display order. In display order the B pictures of an open GOP are
  output before that GOP's I picture, so "GOP" needs an observable definition.

Suggested wording: "a GOP, for this split, is the display-order run of pictures from one I picture
up to but not including the next I picture; GOPs are numbered from 0 at the first I picture of the
clip". This uses only what the index records, like the leading-B rule.

### 3.2 State what the indexed QP means for a NONE macroblock

This is a late observation of mine, not a fault in the revision; R1 should have raised it.

A NONE macroblock has no coded residual, so the QP recorded for it is only the quantiser in force
at that point in the slice. It quantised nothing in that macroblock. The pixels there come from
prediction, with whatever quantisation the reference pictures had. NONE is 24.29% of LP.

Consequences:

- at a boundary touching a NONE macroblock, the 9.3 rounded mean includes a QP that does not
  describe that side's pixels;
- the Step 2 versus Step 3 comparison (value of the real QP map) may behave differently at such
  boundaries.

No design change is needed yet. Suggested: one sentence in 9.2 or 9.3 stating the above, and the
S2-I4 comparison reported separately for boundaries that touch a NONE macroblock (13.1 already
breaks down by FRAME / FIELD / NONE, so this is a reporting split, not new machinery). Whether a
different QP rule is wanted for NONE then becomes an evidence question under Step 5.

---

## 4. OPTIONAL

1. **Two texts carry "v0.2".** The reviewed draft and this revision share filename and version;
   the change log merges both under v0.2. At ratification, the earlier v0.2 text should go to
   `superseded/` under a distinguishing name so the two cannot be confused.
2. **6.2.1 residual case.** An 8-pixel horizontal offset passes the grid-phase check (it is
   a multiple of 8) and would show as zero-shift and one-macroblock-shift contrasts being about
   equal, not as a clear wrong peak. The stop rule in 6.2.3 ("does not give the expected contrast
   peak") already covers this; no change needed, only awareness when reading the S2-I2 output.

---

## 5. Answers to S2r section 21

| Q | Answer |
|---|---|
| 1 Authority fidelity | Yes |
| 2 Registration | Yes; see 4.2 for reading the result |
| 3 K0 freeze | Yes; add 3.1 definition |
| 4 Fixed QP | Yes, per-clip median |
| 5 Shared-boundary QP | Reasonable first hypothesis; see 3.2 |
| 6 NONE | Yes, correct |
| 7 Chroma | Yes |
| 8 Progressive access | Yes |
| 9 Evidence hierarchy | Yes |
| 10 Hold-out discipline | Yes |
| 11 Leading B | Yes |
| 12 Implementation order | No change |
| 13 Stage 1 unfreeze | Nothing requires it |

---

## 6. Change log

### v0.1 - 2026-10-08

- Check of the revised Stage 2 design v0.2: all R1 items carried; no objection to ratification;
  two non-blocking SHOULD (GOP definition, QP meaning for NONE), two OPTIONAL.
