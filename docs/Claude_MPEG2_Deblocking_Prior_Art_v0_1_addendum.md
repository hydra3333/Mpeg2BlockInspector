# Claude - MPEG-2 Deblocking Prior Art - Research v0.1 - Addendum

**Filename:** `Claude_MPEG2_Deblocking_Prior_Art_v0_1_addendum.md`
**Date:** 2026-10-06
**Author:** Claude
**Status:** EVIDENCE INPUT ONLY. Not project authority. Nothing here is DECIDED or VERIFIED.
**Supplements:** `Claude_MPEG2_Deblocking_Prior_Art_v0_1.md` (does not replace it)
**Brief:** `research_proposal_01_v1.0.md`

All technical content below is **HYPOTHESIS** (Claude's reasoning) unless marked otherwise.
The field/frame seam geometry in section 3 belongs to ChatGPT's mechanics track and must be
confirmed against ISO/IEC 13818-2 (ITU-T H.262) before anything relies on it.

---

## 1. Context: Dave's comment (verbatim)

> Thanks. I am wondering if it is ok to consider separated-field processing as "dangerous"
> since we know a frame for interlaced material can/will contain both field based and frame
> based blocks. I am currently inclined to treat such models with very great caution, as with
> models which rely on detection (which we are trying to avoid as our approach may ne
> new/novel) ...

Background for the reviewer: Dave's own inspector output (picture 0, an I-picture, rows 0-3)
shows frame DCT and field DCT macroblocks mixed within single macroblock rows. The inspector is
not yet verified against the pristine reference decoder.

---

## 2. Summary

Caution is justified, but "field-separated processing is dangerous" is not quite the right
line. Neither pure frame processing nor pure field processing is geometrically correct for a
frame that mixes frame-DCT and field-DCT macroblocks; each is wrong in a different way. The
per-macroblock dct_type in the index can remove the need to guess, which may be the most
defensible novel element of the project.

---

## 3. Points

### 3.1 Only horizontal seams are affected

Vertical seams (filtered horizontally along a row) lie every 8 pixels regardless of DCT type,
and each row belongs to a single field. The frame/field question concerns only horizontal
seams (filtered vertically).

### 3.2 Each pure approach fails differently

- **Frame-based vertical filtering** blends lines from both fields. Where there is motion
  between fields, this smears temporal detail (the classic interlace hazard).
- **Field-separated filtering** never mixes fields, but if it assumes one fixed seam grid it
  places seams wrongly for some macroblocks.

### 3.3 Seam positions as seen within a field (to be verified)

For one 16-line luma macroblock in a frame picture:

```text
Frame DCT macroblock: 8x8 blocks are frame lines 0-7 and 8-15.
  Internal seam between frame lines 7 and 8.
  Top field sees frame lines 6 | 8  -> field lines 3 | 4  (field centreline)
  Bottom field sees frame lines 7 | 9 -> field lines 3 | 4 (field centreline)
  => In each field: seams at the macroblock edge AND at the field centreline.

Field DCT macroblock: each 8x8 luma block is 8 lines of ONE field.
  => In each field: seams at the macroblock edge only (every 8 field lines).
```

If correct, this explains the 2005 MERL observation that horizontal blocking appears at both
the block boundary and the block centreline within a field, and why MERL needed detection to
choose between them ([S10] in v0.1, RESEARCHED for the observation itself).

### 3.4 Candidate refinement of Family A: field-domain filtering, metadata-selected seams

Filter horizontal seams always in the field domain, so fields are never mixed, but take each
macroblock's seam positions from dct_type, so no geometric detection is needed:

- frame-DCT macroblock: filter at the macroblock edge and at the field centreline;
- field-DCT macroblock: filter at the macroblock edge only.

This combines the safety of field-separated processing with the geometric certainty that only
the index can provide. It refines Family A (v0.1 section 6.1); it is not a new family. Open
questions: the rule at boundaries between vertically adjacent macroblocks of different DCT
type; field pictures; and chroma (4:2:0 chroma geometry under field DCT is unresolved).

### 3.5 Three kinds of "detection"

1. **Where the seams are** (geometry). The index eliminates this entirely. This is what
   pixel-only interlace-aware filters such as MERL's must guess.
2. **Whether a seam is visibly blocky.** It can largely be replaced by bounding: never change a
   pixel by more than quantisation at that macroblock's quantiser could plausibly have caused.
3. **Blocking versus a genuine edge lying on a seam.** It cannot be eliminated entirely by any
   filter that avoids blurring real edges. A quantiser-bounded correction makes it implicit and
   calibrated rather than a tuned detector, which is consistent with Dave's aim.

### 3.6 Family B is retained as a control, not a candidate

Treating pixel-only, detection-based models with caution as candidates is reasonable. Family B
(v0.1 section 6.2) should still stay in the Stage 2 ablation, because the feasibility gate
needs to show that the metadata-driven approach beats it. Without the control, the value of
dct_type cannot be measured.

---

## 4. Proposed points for three-way review

1. Confirm or correct the seam geometry in 3.3 (ChatGPT mechanics track; standard).
2. Consider the field-domain, dct_type-selected seam rule (3.4) as the leading Family A variant.
3. Adopt the three-way distinction of "detection" in 3.5 as vocabulary for the concept document.
4. Retain Family B as the ablation control only (3.6).

---

## 5. Change log

### Addendum to v0.1 - 2026-10-06

- Recorded Dave's comment on field-separated processing and detection, with Claude's analysis,
  so that it can be cited in the ChatGPT review.
