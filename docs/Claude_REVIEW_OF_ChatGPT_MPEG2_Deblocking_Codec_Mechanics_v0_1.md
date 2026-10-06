# Claude - Review of ChatGPT MPEG-2 Deblocking Codec Mechanics v0.1

**Filename:** `Claude_REVIEW_OF_ChatGPT_MPEG2_Deblocking_Codec_Mechanics_v0_1.md`
**Version:** 0.1
**Date:** 2026-10-06
**Author:** Claude
**Reviewed document:** `ChatGPT_MPEG2_Deblocking_Codec_Mechanics_v0_1.md` (cited below as "CM", with
its section numbers, e.g. CM 20.2)
**Related:** `Claude_MPEG2_Deblocking_Prior_Art_v0_1.md` ("PA") and its addendum ("PA-add")
**Status:** REVIEW RECORD. Evidence input only. Not project authority. Nothing here is DECIDED or
VERIFIED.

---

## 0. Basis and limits of this review

- I have NOT read ISO/IEC 13818-2 / ITU-T H.262 myself. Where CM marks a claim RESEARCHED from
  the standard (CM S1), I assess it for internal consistency and plausibility only. Agreement
  below means "consistent with my understanding", not independent confirmation.
- My own technical statements are HYPOTHESIS unless they cite a PA source [Sxx].
- CM and PA were written in parallel. CM had not seen PA-add, so some points below connect the
  two rather than criticise CM for omissions.
- Disagreements are preserved for the three-way review, not resolved here.

---

## 1. Overall assessment

CM is a sound, well-disciplined pass. Labels are used consistently, reading depth is stated, and
the standard was read at the relevant sections rather than relied on from memory. Its
conclusions on chroma, quantiser semantics, skipped macroblocks and display order are consistent
with what I expected and with the project's earlier notes.

The two documents converge strongly on the main design question: both independently propose the
same Stage 2 ablation ladder (pixels only, then plus quantiser, then plus dct_type, then
optional extras). Compare CM 15.3 and CM 23.3 with PA 6.4.

I raise six substantive points (section 3). The most important are:

- R1: CM 20.2 should state plainly that a field-DCT macroblock has NO internal horizontal
  transform seam at all, not merely that the y = 8 seam must be filtered differently.
- R2: the inspector and index must not report a dct_type for macroblocks that carry none
  (skipped, and non-intra with no coded blocks). The current inspector may print a stale value.
- R3: propagated blocking in P and B pictures can lie off the current picture's grid, which no
  grid-based design (with or without metadata) can address. This bounds the achievable gain.

---

## 2. Points of agreement

| Topic | CM section | Agreement and connection to PA |
|---|---|---|
| 4:2:0 macroblock = 4 luma + 1 Cb + 1 Cr block | CM 4.1 | Agree. |
| No internal chroma seam inside a 4:2:0 macroblock | CM 4.2, 20.4 | Agree. Fills the chroma gap I listed (PA 8 item 4). |
| dct_type is per-macroblock, present only in frame pictures with frame_pred_frame_dct = 0 and coded blocks | CM 5.2 | Agree. Consistent with Dave's inspector printing FramePredFrameDCT=0. |
| A fixed-grid model is too simple for interlaced luma | CM 5.4 | Agree. Corrects the premise as v0.5 section 2 already does. |
| 4:2:0 chroma DCT is always frame-organised | CM 8.1, C3 | Agree; it matches my earlier stated belief. See R5 on Dave's chroma recollection. |
| Chroma prediction can still be field-based | CM 8.2 | Agree, and it matters (R5). |
| quantiser_scale_code needs q_scale_type; nonlinear table | CM 12.1-12.2 | Agree. The inspector's observed values (3, 4, 5, 6) cannot distinguish raw code from nonlinear scale, because codes 1-8 map to themselves. Only the source can settle this. |
| Skipped macroblock quantiser must be defined, not left ambiguous | CM 12.4 | Agree. Matches v0.5 section 5.2 item 2. |
| Weighting matrices matter; check real streams before indexing them | CM 13 | Agree. PA S05 (Nosratinia) found re-quantisation works best with the original matrix, which supports at least checking for custom matrices. |
| Skipped does not mean clean | CM 14.3 | Agree. PA S24 independently reports that motion compensation propagates reference blocking. |
| Motion vectors not justified for the first algorithm | CM 16.2, C9 | Agree, with the limitation noted in R3. |
| Picture type should not drive strength by default | CM 17.2 | Agree. PA found spp's B-frame QP option only, nothing stronger. |
| Display-order ordinal rather than temporal_reference for correspondence | CM 10.4, 28.2 | Agree. Consistent with D-02. |
| Decision principle: step large relative to local activity and plausible for the quantiser | CM 21 | Agree. Prior art supports this family: Chou et al. via PA S05; Annex F's QP range test, PA S02. It is also the "bounding" idea in PA-add 3.5. |
| Scalar oracle, then AVX2; avoid per-pixel branching | CM 24 | Agree. |
| Quantiser-aware MPEG-2 post-processing has precedent | CM 22 | Agree. CM's S6 (Forchhammer 2002) and S7 (US7574060B2) are good sources that my pass missed; I will add them to PA v0.2 as cross-references. |

---

## 3. Substantive review points

### R1 - Field-DCT luma has no internal horizontal seam (CM 6.3, 20.2)

CM 6.2 states (RESEARCHED) that each field-DCT luma block holds 8 lines of one field spanning
the macroblock's full 16 frame lines. If that is right, then within a field-DCT macroblock:

- in the frame domain there is no transform seam at y = 8 (CM 6.3 says filtering there would be
  wrong, which is correct);
- in the field domain each field's 8 lines are ONE block vertically, so there is no internal
  horizontal seam in either field either;
- the only horizontal seams of a field-DCT macroblock are at its top and bottom macroblock
  edges, seen in each field between field lines 7 and 8 of adjacent macroblocks (frame lines
  14|16 for the top field and 15|17 for the bottom field, consistent with CM 6.5).

CM 20.2 presents same-parity sample patterns around an unspecified "y" and says exact indexing
depends on where the boundary falls. HYPOTHESIS: the answer is simply "at macroblock edges
only", and CM 20.2 should say so explicitly. Otherwise an implementer may filter a non-existent
internal seam inside field-DCT macroblocks.

The converse case completes the picture (PA-add 3.3, HYPOTHESIS): a frame-DCT macroblock's y = 8
seam, seen within each field, falls between field lines 3 and 4. So a single field-domain
filter can serve both types, with dct_type choosing the seam set:

```text
                         horizontal seams, seen in each field
frame-DCT macroblock :   macroblock edge  +  field centreline (field lines 3|4)
field-DCT macroblock :   macroblock edge only
```

Request for ChatGPT: confirm or correct this against Figures 6-13 and 6-14, which CM has seen
and I have not.

### R2 - Do not report dct_type where none exists (CM 5.2, 26)

CM 5.2 notes that dct_type is absent for skipped macroblocks and, by its stated presence rule,
for non-intra macroblocks with no coded block pattern. Two consequences:

1. **Inspector verification.** Dave's current inspector prints FRAME or FIELD for every
   macroblock. In I-pictures every macroblock is intra, so this is fine. In P and B pictures, the
   printed value for skipped or no-CBP macroblocks may be a stale variable left over from an
   earlier macroblock, or a default. HYPOTHESIS; this must be checked in the source.
2. **Index and analyzer semantics.** The effective-DCT field needs a third state ("no transform
   coded") alongside frame and field, or a rule tying it to the skipped/CBP flags. CM 26 asks for
   "effective dct_type where meaningful", which is the right intent; it should be made explicit.

This matters for R1: a macroblock with no coded transform has no transform seams of its own.

### R3 - Off-grid propagated blocking bounds every grid-based design (CM 14.3, 16)

CM 14.3 rightly says skipped does not mean clean. The further consequence (HYPOTHESIS):

- Blocking copied from a reference picture by motion compensation appears displaced by the
  motion vector. In P and B pictures, much visible block structure may therefore sit off the
  current picture's 8x8 grid.
- No grid-based filter can address that, with or without the index. libpostproc's own source
  comment says one of its filters can only smooth blocks at the expected locations, not moved
  ones (PA S03, RESEARCHED).
- Separately, adjacent inter macroblocks with different motion vectors can produce steps at
  macroblock edges even with no residual (PA S24, RESEARCHED). Those are on-grid and filterable.

Implication: the achievable gain in P and B pictures is bounded by how much blocking is on-grid.
This is a reason to measure gains per picture type in Stage 2, not a reason to add motion
vectors now.

### R4 - Field prediction may matter for macroblock-edge geometry (CM 16, 18 Tier C)

CM places motion and prediction type in Tier C. One narrow exception may deserve Tier B
(HYPOTHESIS): in frame pictures, a macroblock using field-based prediction has separate
predictions for its top-field and bottom-field lines. The step at its macroblock edges can then
differ between the two fields. A field-domain filter (R1) handles this naturally, but whether a
frame-domain filter is acceptable at such edges may depend on knowing the prediction type, not
just dct_type. Suggest the Stage 1 analyzer report frame/field prediction type per macroblock
(CM 26 already allows "if easy to expose"), so its frequency is known before deciding.

### R5 - Chroma: DCT is frame-organised, but interlace still reaches chroma (CM 8)

CM's chroma findings appear correct for transform geometry. Three nuances (HYPOTHESIS):

1. Chroma prediction can be field-based (CM 8.2), so motion-related chroma steps can still
   differ by field even though chroma DCT blocks are frame-organised.
2. In interlaced 4:2:0, a frame-organised 8x8 chroma block necessarily contains chroma lines
   associated with both fields. A frame-domain chroma filter is consistent with the transform,
   but on moving content it blends temporally different chroma.
3. Dave's hazy recollection of "chroma" issues in historical posts may refer to a different,
   well-known interlaced 4:2:0 problem: chroma upsampling handled progressively when it should be
   handled per field. That causes streaky or combed colour edges, not DCT blocking. If so, it is
   outside the deblocker's scope but worth naming so the two are not confused. Not researched;
   to be checked if Dave thinks it fits.

### R6 - Sources and evidence notes

- CM S1's accessible copy (burgerlib.readthedocs.io) is a third-party host of the 1995 text.
  Later editions and corrigenda exist (HYPOTHESIS that they do not change these mechanics).
  The ITU link in CM S1 suggests H.262 is obtainable from ITU directly; that would be the
  better citation for the repository.
- CM 22.1's description of US7574060B2 and Forchhammer (2002) are claims I cannot check without
  reading them. I note them as CM-RESEARCHED and will treat them as such.
- CM 4.2 and 20.4 (chroma seams only at macroblock edges) rest on CM 4.1 and 8.1; agreed.
- CM's tiering (CM 18) places CBP in Tier B. PA found no post-filter prior art using CBP. This
  is a difference of emphasis, not a contradiction: CM's case for CBP is mechanical (it maps to
  individual blocks), mine is empirical (no precedent). Both point to testing it as an optional
  step, as CM 15.3 already proposes.

---

## 4. Status of the questions in PA section 5

| PA 5 question | Answered by CM? | Status |
|---|---|---|
| 1. MERL centreline vs MPEG-2 field-DCT geometry | Partly (CM 6.2-6.5) | Consistent with R1; explicit confirmation requested. |
| 2. Mapping borrowed QP thresholds to MPEG-2 quantiser | Yes for semantics (CM 12-13) | Threshold re-derivation remains design work. |
| 3. What libavcodec's MPEG-2 QP export contains | No | OPEN. CM read mpeg12dec.c but does not mention the video_enc_params export (PA S18). |
| 4. Does libavcodec expose dct_type per macroblock? | No | OPEN. CM 5.3 shows FFmpeg parses it internally; export not addressed. |
| 5. Interlaced 4:2:0 chroma geometry under dct_type | Yes (CM 8, C3) | Resolved for DCT geometry; see R5 for prediction nuance. |
| 6. 16x16 inter-macroblock edges vs 8x8 | Partly (CM 14.3) | See R3; experiment needed. |

Questions 3 and 4 matter for the "same decoder as BestSource" fallback in v0.5 section 6.4.
I suggest one of us answers them before Stage 1 tooling is committed.

---

## 5. Proposed synthesis points for the three-way review

1. Adopt the shared ablation ladder (CM 15.3 = PA 6.4) as the core Stage 2 experiment.
2. Horizontal seams: field-domain filtering with dct_type selecting the seam set (R1 and PA-add
   3.4), subject to ChatGPT confirming the geometry.
3. Effective DCT state has three values: frame, field, none (R2). Verify the inspector's
   behaviour for skipped and no-CBP macroblocks before relying on its output.
4. Chroma: filter at macroblock-edge positions only, frame-organised geometry, with a separate
   strength or threshold left open (CM 20.4, CM 31 item 4, R5).
5. Stage 1 analyzer: CM 26 field list, plus frame/field prediction type per macroblock (R4) and
   the per-picture-type breakdown needed to measure R3.
6. Before Stage 1 tooling: answer PA 5 questions 3 and 4 (libavcodec export of QP and dct_type).

---

## 6. Change log

### v0.1 - 2026-10-06

- First cross-review of `ChatGPT_MPEG2_Deblocking_Codec_Mechanics_v0_1.md`.
- Agreements tabulated (section 2); six substantive points R1-R6 (section 3); status of PA
  section 5 questions (section 4); synthesis points for three-way review (section 5).
