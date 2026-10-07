# Claude - Reconciliation Review After Handover v0.1

**Filename:** `Claude_REVIEW_Reconciliation_After_Handover_v0_1.md`
**Version:** 0.1
**Date:** 2026-10-07
**Author:** Claude (the correct project chat)
**Reviews:**
- `ChatGPT_HANDOVER_TO_CLAUDE_After_LG_EP_MLS_Review_v0_1.md` ("HO")
- `ChatGPT_RESPONSE_TO_Claude_QUESTIONS_After_Handover_v0_1.md` ("QR")
- `Stage2_Experiment_Design_v0_1.md` ("S2")
- `Response_to_Claude_Index_Driven_Ruling_and_Revised_Stage2_Plan_v0_1.md` (provenance only)
**Against:** repository `05_DECISIONS.md` v1.0, `06_DEBLOCK_CONCEPT.md` v1.0,
`02_INDEX_FORMAT_SPEC.md` v0.3 (the ratified versions this chat produced; **Dave to confirm these
are the current repository copies**); `Claude_REVIEW_OF_LG_EP_MLS_Stage1_Runs_v0_1.md`;
`LG_576i_3_LP.log`; reference decoder V1-V4.
**Status:** Review input only. Not project authority.

Classification used: **MUST CHANGE**, **SHOULD CHANGE**, **OPTIONAL**, **NO OBJECTION**.

---

## 1. Summary

- HO's chronology is accurate. QR's answers are accepted with two precision corrections (section 4).
- **No technical objection to Dave's index-driven ruling.** Once the product is defined as
  index-driven, a pixel seam-position detector and Family B answer a question the product no longer
  asks.
- Removing Family B loses **one thing that is still needed** and one that is useful:
  - needed: a check that the index is **spatially** registered to the pixels (Stage 1 proved only
    temporal correspondence) - section 5, MUST;
  - useful: an existing-filter **yardstick** for the "is it worth it" judgement - OPTIONAL, Dave's
    call, because it brushes against the ruling.
- Repository changes are identified by exact ID and section (sections 2 and 3). They include two
  conflicts the handover did not list: **D-08** (mandatory ground-truth baseline) and **D-23**
  (drafting workflow).

---

## 2. `05_DECISIONS.md` - exact effects (HO Q4)

| ID | Effect | Class | Note |
|---|---|---|---|
| D-11 Family B mandatory control | SUPERSEDED by new D-24 | MUST | |
| D-17 Custom `.idx2` provisional | SUPERSEDED by D-24 | MUST | Contents/packing remain unfrozen under D-22 and `02` C-5; that part survives elsewhere |
| D-18 Ablation step 2b | SUPERSEDED by D-24 | MUST | Its fixed-QP idea survives as the new Step 2, but with indexed geometry |
| D-15 Measure metadata values independently | AMEND (supersede and restate) | MUST | Keep "measure the value of real per-MB QP" (fixed vs real); drop transform-state value measurement and the rationale "the index must justify itself" |
| D-08 Existing-filter baseline | AMEND | MUST | It says "the unfiltered decode **and ground-truth source** remain mandatory baselines". Real LG material has no ground truth (QR Q2). Restate: unfiltered decode mandatory everywhere; paired reference only where one exists (transcode pairs) |
| D-23 Drafting conventions | CLARIFY | SHOULD | Its workflow line says Claude drafts, ChatGPT reviews. QR Q1 reverses this for the current round. Record the current workflow, or scope D-23 to the initial repository drafting |
| D-10 Family A | NO CHANGE | - | "Metadata-directed geometry" already matches the ruling. Title "leading hypothesis" may become "design family" (OPTIONAL) |
| D-09, D-12, D-13, D-14, D-16 | NO CHANGE | - | Frame-owned model, Family C optional, first metadata QP + transform state, prediction diagnostic only, I/P/B reporting all still hold |
| D-01 to D-07, D-19 to D-22 | NO CHANGE | - | |

New decisions (numbering continues per D-19):

- **D-24 Index-driven production architecture** (MUST). Substance as HO 14.1 Decision A. State it is
  a scope decision, not an experimental finding. Supersedes D-11, D-17, D-18; amends D-15.
- **D-25 Chroma in scope on mechanism** (MUST, separate from D-24, HO Q7 agreed). Substance as HO
  14.1 Decision B (Dave's R-A).
- **D-26 Stage 2 evidence hierarchy and material** (SHOULD). Records Dave's R-B (real recorder
  material primary, transcodes secondary) and the QR Q2 weighting, declared before results. This
  is what makes the amended D-08 workable. The finer rules (QR Q3, Q4, Q7) belong in Stage 2
  v0.2, not in `05`.

---

## 3. `06_DEBLOCK_CONCEPT.md` - exact effects (HO Q5)

| Section / item | Change | Class |
|---|---|---|
| 1 central question | Replace "...than pixel-only detection?" with the QR/HO objective: given authoritative indexed geometry and QP, what filtering produces useful luma and chroma deblocking without unacceptable damage, and which indexed metadata the final filter needs | MUST |
| 3 K-03 | Evidence becomes "RESEARCHED (H.262) + VERIFIED (reference decoder V1)"; delete the "must still be cold-read" note, now done | MUST |
| 3 K-04 | Add "VERIFIED (reference decoder V2)" | MUST |
| 3 new K-10 | V3: 4:2:0 chroma blocks use the macroblock's `quantizer_scale`; the reference decoder selects the luma matrices for 4:2:0 chroma. VERIFIED reference-decoder implementation, not a normative H.262 claim | MUST |
| 3 new K-11 | V4: in 4:2:0 frame pictures with field prediction the decoder treats even chroma lines as top field, odd as bottom. VERIFIED reference-decoder implementation | MUST |
| 3 K-09 | Keep; reword its role to "cross-check source", not a competing architecture | SHOULD |
| 4.7 chroma | Add K-10/K-11; state same-field chroma access remains a **design choice** (OPEN), premise verified | MUST |
| 5 item 1 | Delete the Family B parenthesis; state "no pixel detection of seam positions" as a design rule (D-24) | MUST |
| 6 quantiser | Add K-10 consequence: per-MB QP applies to chroma unchanged | SHOULD |
| 8.2 Family B | Mark SUPERSEDED by D-24; keep text as history or remove per D-23 conventions | MUST |
| 9.1 / 9.2 ladder and comparisons | Replace with the indexed-only ladder (Stage 2 v0.2 holds the detail) | MUST |
| 9.3 material and measures | Replace the "ground-truth encodes" reference with the D-26 evidence hierarchy | MUST |
| 9.4 architectural meaning | Delete Architectures A/B; replace with a one-line pointer to D-24 | MUST |
| 10 bound | No change | - |
| O-01, O-02, O-13 | Re-label: no longer architecture questions; FFmpeg QP side data is an optional cross-check | MUST |
| O-03 | Close: answered by the Stage 1 design (gated NONE) and VALID runs | SHOULD |
| O-06 | **Amend by meaning, not number.** Remove "whether chroma deblocking is useful" (D-25); keep chroma threshold, strength, H/V treatment, interlaced access, no-harm | MUST |
| O-07 | Partly answered: custom non-intra matrices occur in 4 of 5 LG recordings (4A, LP, EP, MLS); "do they matter" deferred per QR Q5 | SHOULD |
| O-08 | Partly answered: no field pictures in any of the 7 clips run; archive-wide still open | SHOULD |
| O-10a, O-10b | Withdraw (not answered; out of scope by D-24) | MUST |
| new O-14 | Progressive pictures: frame-domain access when progressive_frame = 1 (MLS) | SHOULD |

---

## 4. `02_INDEX_FORMAT_SPEC.md` (HO Q6)

| Item | Change | Class |
|---|---|---|
| 0 scope, "Why the custom index is provisional ... see 06 9.4" | Replace: architecture fixed by D-24; contents and packing still unfrozen until Stage 3 | MUST |
| Candidate contents (not a freeze) | Name **progressive_frame per picture** explicitly; the filter's access mode depends on it (QR Q6). Picture type is needed for I/P/B reporting and the leading-B rule | SHOULD |
| C-1 to C-5 | No change | - |

---

## 5. Experiments lost by removing Family B (HO Q9)

### 5.1 Needed: spatial registration of index to pixels (MUST, in Stage 2 v0.2)

Stage 1 proved **temporal** correspondence (record N = frame N; picture types match). It did not
prove that macroblock (x, y) in the index sits on the pixel block BestSource delivers at
(16x, 16y): no crop, offset, or field-parity swap between the two paths. The old detector/index
confusion matrix would have exposed a misregistration incidentally. Nothing in the indexed-only
ladder does.

Cheap, detector-free check (part of S2's seam-map diagnostics, S2-I2): on LP, measure the mean
same-field step at the mid-height position split by indexed state. Expected (HYPOTHESIS): FRAME
macroblocks show a larger step there than FIELD macroblocks, and the macroblock-edge step is similar
for both. A one-row or one-field offset would flatten or invert that pattern. This is a validation
of index alignment, not a seam detector, and does not conflict with D-24.

### 5.2 Useful: an existing-filter yardstick (OPTIONAL, Dave's call)

The gate's "is it worth it" judgement is easier with a reference point. An existing deblocker
already in Dave's toolset, run at default settings on the same frames, gives one at almost no cost.
This is not Family B (no designed control, no geometry comparison, no architecture question), but
it is a pixel-only filter, so Dave should say whether it fits his ruling.

### 5.3 Not lost

The fixed-vs-real QP comparison (QR Q4) keeps the one clean metadata ablation that still bears on
the final index contents.

---

## 6. Answers to the remaining HO questions

- **Q1 chronology:** accurate. Nothing material missing between my EP/MLS review and HO.
- **Q2 LP as first luma material:** agree, on the re-grounded rationale. Two notes: LP is a single
  8-second clip, so hold-outs (QR Q3) carry the generalisation weight; 3.8% of LP macroblocks sit at
  QP 112, the top of the table, so behaviour at saturation should be reported separately.
- **Q3 pixel detector still needed?** No, for geometry. Section 5.1 is a registration check, not a
  detector.
- **Q7 chroma R-A separate:** agree (D-25).
- **Q8 evidence levels:** confirmed exactly as HO states. V2 and V3 (same `quantizer_scale`) VERIFIED
  reference-decoder implementation; V3 luma-matrix path VERIFIED implementation, not a normative
  claim; same-field chroma *filtering* a design choice, its parity premise now VERIFIED (V4).
- **Q10 unfreeze Stage 1?** No. LP/EP/MLS all VALID; nothing points to a defect.

### 6.1 Precision corrections to QR

1. **QR Q6 (MUST, wording):** "luma horizontal FRAME-DCT seam: same-field access is *required by
   the established geometry*". The geometry (V1) places the seam between frame lines 7 and 8; it
   does not require same-field access. Same-field access is the D-09 design rule (avoid mixing
   fields). Keep the two labels separate, as QR rightly does for chroma.
2. **QR Q7 (SHOULD, wording):** make the exclusion rule observable from what the index records:
   "B pictures output before the first I picture of the clip". "First in-sample reference picture
   that can anchor normal prediction" needs GOP-header information (closed_gop, broken_link) the
   index does not store.

QR Q2, Q3, Q4 and Q5: NO OBJECTION. The per-clip median for the fixed QP is the right control.

---

## 7. Stage 2 v0.2 - what to carry (for ChatGPT's draft)

MUST: indexed-only ladder; D-26 evidence hierarchy with weighting declared in advance; LP
development and EP/4A/2A locked hold-outs, MLS separate; per-clip median fixed QP; leading-B
exclusion; progressive_frame-driven access mode; spatial registration check (5.1); remove S2 Q2-03,
Q2-04, Q2-06, sections 9.1, 11, 16.2 as architecture question, 17.2, S2-I5, S2-I6.

SHOULD: report QP-112 macroblocks separately; keep S2 section 4 cross-pair check for the transcode
pairs only; keep S2 section 15 matrix rule as QR Q5.

OPTIONAL: existing-filter yardstick (5.2), if Dave agrees it fits his ruling.

---

## 8. Change log

### v0.1 - 2026-10-07

- Reconciliation review after the handover: exact `05`/`06`/`02` effects, experiments lost and kept,
  answers to HO questions, two precision corrections to QR, carry-list for Stage 2 v0.2.
