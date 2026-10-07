# Claude - Review of Stage 1 Evidence and Gate Report v0.2

**Filename:** `Claude_REVIEW_OF_Stage1_Evidence_and_Gate_Report_v0_2.md`
**Version:** 0.1
**Date:** 2026-10-07
**Author:** Claude
**Reviews:** `Stage1_Evidence_and_Gate_Report_v0_2.md` (cited as "GR", with its section numbers)
**Status:** Stage 1 working review. Not project authority.

---

## 1. Verdict

**Agree with the proposed disposition (GR 14): Stage 1 gate PASS.** No blocking issue.

Four corrections are needed before the report becomes the durable Stage 1 summary, because it
will replace the logs (section 3). Two are stale text carried over from v0.1; one is an
unexplained anomaly in the formal original sample; one is lost corroborating detail.

---

## 2. What I checked, and the limits

### 2.1 Checked

- **File identities (GR 2.3).** The SHA-256 of `getpic.c` and `mpeg2dec.c` in the
  `Mpeg2BlockInspector_src.zip` I reviewed earlier, and of `Stage1_Inspector_Analyzer_v0_2.py`,
  match the hashes in GR exactly. So the reviewed source is the source that produced the results.
- **Internal arithmetic of the formal pair (GR 8).** Every reconcilable number agrees:

| Check | Result |
|---|---|
| Transform states sum, original / blocky | 486,000 / 486,000 |
| Coding states sum, original / blocky | 486,000 / 486,000 |
| Per-picture-type transform sums = pictures x 1,620 (I, P, B, both samples) | all exact |
| Horizontal neighbour pairs = 44 x 36 x 300 | 475,200 (both samples) |
| Vertical neighbour pairs = 45 x 35 x 300 | 472,500 (both samples) |
| Original QP histogram total / mean / median | 486,000 / 14.455 / 14 |
| Q updates and dct bits read percentages | 36.11% / 87.88% |
| Formal index size; index/MPG ratios | 3,907,232; 69.7% / 220.8% |

- **Corroborating pair (GR 1.4, 6.3).** Against the `TEST_2A_A001` logs I have seen: VALID,
  300 records, 300 BestSource frames, 300 vspipe frames and 300/300 I/P/B matches, for both
  samples. Correct.

### 2.2 Not checked

I have not seen the `TEST_4A_A003` logs. The formal-pair figures are taken from GR; I can say
only that they are internally consistent, not that they were transcribed correctly from the
logs. If Dave wants that closed, the two summary blocks can be pasted here once before the logs
are deleted.

---

## 3. Corrections

### C1 - Section 4 is stale (TEST_2A figures under a TEST_4A heading)

GR 4 says "For both executed samples ... Both final indexes were 3,820,832 bytes ... For 300
frames at 704x576". Those are the `TEST_2A_A001` figures. GR 1.3 and 8.5 say the formal pair is
720x576 and 3,907,232 bytes. Section 4 should either use the formal-pair figures or state that it
describes the corroborating pair.

### C2 - Section 9.4 says 44x36

"per-picture macroblock counts are 44x36" is the `TEST_2A` grid. The formal pair is 45x36.

### C3 - One anomalous frame in `TEST_4A_A003` (original) is unexplained

Two facts in GR point to the same single frame:

- `q_scale_type` is 1 in 299 frames and 0 in 1 (GR 8.1);
- FRAME + FIELD = 428,727, but dct_type bits read = 427,107. The difference is **1,620 = exactly
  one frame's macroblocks** (the blocky sample has no difference).

Under the analyzer's own rules (FRAME/FIELD in a frame picture with `frame_pred_frame_dct = 0`
implies the bit was read), the only VALID explanation is one frame with
`frame_pred_frame_dct = 1`, every macroblock coded with an implicit frame DCT, and a linear
quantiser scale. The histogram supports this: values 26 and 30 occur (1 and 3 macroblocks); they
are not in the MPEG-2 non-linear table but are linear-scale values.

This is HYPOTHESIS, but cheap to confirm and worth recording because:

- it is a genuine property of the recorder's stream that the report does not mention;
- it means the analyzer's `frame_pred_frame_dct = 1` path was actually exercised on real data;
- `frame_pred_frame_dct` is not in the analyzer's file-level summary at all, so the next sample
  could hide the same thing.

Suggested action: use the analyzer's frame dump to identify the frame (number, picture type,
`frame_pred_frame_dct`, `q_scale_type`) and record it in GR 7/8. No inspector change.

### C4 - Corroborating pair detail is lost when the logs go

v0.1 preserved the `TEST_2A_A001` statistics; v0.2 replaced them with the formal pair. Once the
logs are deleted, the only record of the second pair is "it passed". It differs usefully from the
formal pair (704x576 not 720x576; no custom matrices; original QP 1..80 spanning the full
non-linear table; IBPBP GOP in the original against IBBP in the formal pair; its blocky sample a
constant-QP 62 linear re-encode). Suggest a short appendix holding the two analyzer summary
blocks verbatim (about 50 lines), or point to `Stage1_Evidence_and_Gate_Report_v0_1.md` and
retain that file.

### C5 - Minor

- GR 12 retain list names `Stage1_Evidence_and_Gate_Report_v0_1.md`; it should name v0.2 (and v0.1
  too if C4 is resolved by pointing to it).
- GR 7 "Common picture-level properties" omits `q_scale_type` and `frame_pred_frame_dct`; with C3
  these are not common to both samples, so list them per sample.

---

## 4. Answers to GR section 13

**Q1 - Gate assessment.** Yes. Source discipline and hook placement were checked against
pristine; the hashes tie the reviewed source to the runs; both formal indexes are VALID with the
v0.2 checks; the numbers reconcile.

**Q2 - Correspondence wording.** Fair. One addition worth stating in GR 6.5: with a strictly
periodic GOP (the formal pair repeats every 12 frames), a picture-type comparison cannot detect a
displacement that is a multiple of the GOP length. Count equality makes such a displacement
unlikely, because it would also need compensating errors at both ends, but it is the specific
case the test is blind to. The irregular GOP of the `TEST_2A_A001` original is useful here.

**Q3 - Sample coverage.** No reason not to close Stage 1. GR 11 already lists what is untested:
field pictures, damaged streams, multiple sequences / sequence_end mid-stream. All four executed
samples are single-sequence, frame-picture, undamaged clips; that should stay explicit in the
scope of the PASS.

**Q4 - Inspector freeze.** Agree. Nothing in the evidence calls for an inspector change. C3 is a
reporting matter; if anything changes it is the analyzer summary (adding `frame_pred_frame_dct`),
and even that can wait for Stage 2 tooling.

**Q5 - Evidence preservation.** C3 and C4 are the omissions.

**Q6 - Overreach.** Sections 10-11 are appropriately limited. One wording point: GR 10.5 says the
quantiser capture is "strong evidence" because two regimes are distinguished. Stronger supporting
evidence is already in hand: the stored values in both `TEST_2A_A001` and `TEST_4A_A003` originals
are exactly the members of the MPEG-2 non-linear table (apart from the C3 frame), which confirms
the derived scale is stored, not the raw code. Suggest citing that.

---

## 5. Recommended disposition

Stage 1 gate PASS as proposed in GR 14, after:

1. C1 and C2 corrected;
2. C3 identified (one analyzer frame dump) and recorded;
3. C4 resolved by appendix or by retaining v0.1;
4. C5 and the Q2/Q6 wording points applied at the drafter's discretion.

None needs an inspector rebuild or a rerun of the gate.

---

## 6. Change log

### v0.1 - 2026-10-07

- Review of `Stage1_Evidence_and_Gate_Report_v0_2.md`: hash and arithmetic verification, five
  corrections, answers to the six questions, recommended disposition.
