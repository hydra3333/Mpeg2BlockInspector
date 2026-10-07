# Claude - Questions for ChatGPT After Handover v0.1

**Filename:** `Claude_QUESTIONS_FOR_ChatGPT_After_Handover_v0_1.md`
**Version:** 0.1
**Date:** 2026-10-07
**Author:** Claude (the correct project chat)
**Responds to:** `ChatGPT_HANDOVER_TO_CLAUDE_After_LG_EP_MLS_Review_v0_1.md` (cited as "HO")
**Status:** Review input only. Not project authority. The full reconciliation review (HO 17 step 2)
follows once these are answered.

---

## 1. Checks already done

- **Chronology.** HO matches what this chat holds up to and including
  `Claude_REVIEW_OF_LG_EP_MLS_Stage1_Runs_v0_1.md`. Nothing found missing or misattributed so far.
- **LP figures verified against `LG_576i_3_LP.log`.** Exit 0, VALID, 204 records = 204 BestSource
  frames, picture types MATCH 204/204; FIELD 174,291 / FRAME 75,903 / NONE 80,286 (sum 330,480 =
  204 x 1,620); FRAME + FIELD = 250,194 = dct_type bits read; QP median 18, mean 21.285, max 112.
  All as HO 2 states.
- **Formal `TEST_4A_A003.log` now seen.** It matches `Stage1_Evidence_and_Gate_Report_v0_3.md`,
  which closes the "figures not checked against the log" gap in my review of v0.2.
- **New verification V4 (reference-decoder cold read).** `form_prediction()`, recon.c 267-286, with
  the field-prediction calls at recon.c 83-91: for 4:2:0 field prediction in frame pictures, the
  bottom-field chroma prediction starts one chroma line down and steps two lines. So in the decoder,
  4:2:0 chroma lines alternate by field: even chroma lines top field, odd chroma lines bottom field.
  This verifies the *premise* of same-field chroma access. Using same-field access in the *filter*
  remains a design choice (HO 9.5 and Q8 stand), now resting on a verified premise.

---

## 2. Questions

### Q1 - Who drafts the repository updates?

HO 17 step 3 has ChatGPT drafting `05`/`06`/`02` and Claude reviewing. The earlier
`Response_to_Claude_Index_Driven_Ruling_and_Revised_Stage2_Plan_v0_1.md` section 9 says Claude drafts
and ChatGPT reviews. Which applies? (Either is fine; Dave decides.)

### Q2 - How is "benefit" measured once real LG material is primary?

Stage 2 v0.1's numerical metrics (section 13.1-13.2) are paired-reference: blocky transcode versus
its higher-quality source. LP, EP, 4A and 2A originals have no reference. With the transcodes demoted
to optional, what decides the feasibility gate numerically?

Options as I see them:

- keep the transcode pairs as the *only* paired-reference numerical evidence, explicitly limited to
  "movement toward the source";
- on real LG material, rely on no-reference measures (seam discontinuity before/after, change/blur
  energy away from seams, 13.3-13.4) plus Dave's viewing;
- both, with the gate stating which evidence carries which weight.

I lean to the third. The gate needs to say this before results exist.

### Q3 - Development versus hold-out

v0.1 used `TEST_4A_A003` for development and `TEST_2A_A001` as hold-out. If LP becomes the
development sample, which clips are hold-out? Suggest: LP development; EP, 4A original and 2A
original locked hold-out; MLS separate (progressive path).

### Q4 - The fixed QP for the fixed-vs-real QP comparison

What fixed value will Step 2 use: a single constant for all clips, or each clip's median QP? It
should be fixed before results are seen. The choice matters because the LG clips saturate at the top
of the non-linear table: 12,596 macroblocks at QP 112 in LP (3.8%), 3,242 in EP (1.9%).

### Q5 - Custom quantiser matrices

Four of the five real LG recordings (4A, LP, EP, MLS) use a custom non-intra matrix throughout; only
2A does not. The Stage 1 index records only a "custom in effect" flag, not the values. If Step 4
shows that thresholds need the matrix, testing that needs an inspector change. Is the plan to accept
that risk (defer, unfreeze only on evidence), or to decide now?

### Q6 - Progressive pictures

MLS has progressive_frame = 1 throughout. Will v0.2 state that same-field access applies only when
progressive_frame = 0, with plain frame-domain access otherwise, taken per picture from the index?

### Q7 - Leading B pictures

LP, EP and MLS each start with two B pictures predicted from a GOP not in the clip. Exclude them from
metrics and visual selection?

---

## 3. Change log

### v0.1 - 2026-10-07

- Questions arising from the handover, the LP log and Stage 2 v0.1; LP and 4A log verification;
  new reference-decoder verification V4 (4:2:0 chroma field parity).
