# ChatGPT Review of Claude MPEG-2 Deblocking Prior Art Research

**Filename:** `ChatGPT_REVIEW_OF_Claude_MPEG2_Deblocking_Prior_Art_v0_2.md`
**Version:** 0.2
**Date:** 2026-10-06
**Author:** ChatGPT
**Status:** CROSS-REVIEW EVIDENCE INPUT ONLY. Not project authority.
**Reviews:**
- `Claude_MPEG2_Deblocking_Prior_Art_v0_1.md`
- `Claude_MPEG2_Deblocking_Prior_Art_v0_1_addendum.md`
**Related ChatGPT research:**
- `ChatGPT_MPEG2_Deblocking_Codec_Mechanics_v0_1.md`
**Controlling proposal:**
- `MPEG2_Macroblock_Index_VapourSynth_Deblocking_Project_Proposal_v0_5.md`
**Research brief:**
- `research_proposal_01_v1.0.md`

---

## 1. Executive assessment

I concur with the majority of Claude's v0.1 prior-art findings and with the central
direction of the addendum.

The main research document is disciplined about evidence quality and does a particularly
good job of attempting to falsify the metadata-assisted premise rather than merely
collecting supporting literature.

The addendum is technically important.

Its central refinement:

> process horizontal luma seams in the field domain, but select which horizontal seams
> actually exist from per-macroblock `dct_type`

is consistent with the MPEG-2 frame-DCT / field-DCT organisation found independently in
my mechanics research.

This is a better formulation than either:

- treating the whole interlaced frame as one ordinary raster for vertical-direction
  filtering; or
- blindly splitting the frame into two fields and assuming one universal 8-line seam
  grid.

I recommend carrying this refined Family A into the three-way Stage 0 concept discussion
as the current leading HYPOTHESIS.

I also strongly support retaining Claude's Family B as a control, not as the preferred
project algorithm. Without that control, the project cannot measure whether `dct_type`
metadata has useful value.

No material finding in Claude's document causes me to recommend stopping the project.

The most significant challenge Claude found is real:

> FFmpeg can already export per-macroblock MPEG-2 quantiser information.

That means the custom index must justify itself through metadata or correspondence that
ordinary decoder side data does not provide, especially `dct_type`, rather than merely
through quantiser access.

---

## 2. Review labels

**AGREE**
Claude's statement is consistent with my mechanics research and/or direct cross-check.

**AGREE WITH QUALIFICATION**
The direction is sound but wording/evidence should be narrowed.

**CORRECTION**
I believe the statement should be changed.

**OPEN**
Evidence is insufficient for project truth.

**HYPOTHESIS**
Design inference rather than researched fact.

Nothing in this review is VERIFIED project truth merely because ChatGPT agrees with it.

---

## 3. Review of Claude's main summary

### 3.1 Practical prior art mostly uses 8x8 boundary filtering with quantiser guidance

**AGREE WITH QUALIFICATION.**

Claude's sampled practical implementations strongly support this statement.

However, the word "mostly" should be read as:

> mostly among the practical implementations found in this research pass

rather than as an exhaustive statement about all MPEG-2 post-processing ever published.

The source-depth limitations in Claude section 8 justify this narrower wording.

---

### 3.2 Real stream quantiser is the most established practical metadata input

**AGREE.**

This aligns strongly with both the historical tools Claude found and my mechanics track.

Quantiser metadata is the only codec-side input with broad practical precedent in the
sampled post-processing implementations.

The important caveat remains:

MPEG-2 `quantiser_scale_code`, derived `quantiser_scale`, q_scale_type, and weighting
matrices must not be conflated with MPEG-4 or H.264 QP units.

Any threshold equation borrowed from Annex F/libpostproc must be re-derived or
experimentally calibrated for MPEG-2 semantics.

---

### 3.3 No prior-art MPEG-2 post-filter found using per-MB dct_type

**AGREE as a gap statement.**

Claude correctly labels this as an absence in the sources found, not proof that no such
work exists.

This absence is actually useful for the project:

- it prevents us pretending the idea is established;
- it leaves `dct_type` as a clearly testable project hypothesis;
- it strengthens the need for the Stage 2 ablation.

---

### 3.4 Pixel-only interlace-aware filtering challenges the custom-index premise

**AGREE.**

This is the most valuable falsification result in Claude's pass.

The MERL approach demonstrates that a filter can attempt to accommodate mixed
frame/field-coded artifact positions using pixel-domain detection rather than syntax
metadata.

That does not disprove the index approach.

It creates the correct experimental question:

> Does authoritative `dct_type` geometry outperform or simplify a good pixel-domain
> geometry detector enough to justify the index?

This should become an explicit feasibility-gate result.

---

## 4. Interlaced addendum: detailed mechanics review

This section addresses Dave's concern directly.

### 4.1 Dave's caution is justified

**AGREE.**

Dave's concern was that treating an interlaced frame globally as either frame-based or
field-based can be dangerous because MPEG-2 may mix frame-DCT and field-DCT macroblocks
within the same frame picture.

My independent mechanics research agrees that `dct_type` is macroblock-level syntax
under the relevant MPEG-2 conditions.

Therefore neither one whole-frame geometry nor one whole-field geometry should be
accepted blindly as universally correct.

---

### 4.2 Claude addendum 3.1: vertical seams versus horizontal seams

**AGREE.**

Claude says the frame/field DCT distinction primarily changes the geometry relevant to
horizontal image seams, i.e. boundaries filtered in the vertical direction.

This is consistent with MPEG-2 transform organisation.

The left/right 8x8 division remains at the same x location.

The vertical organisation of samples inside each transform block changes.

One qualification:

even when the x seam location is fixed, a multi-row vertical-edge filter should avoid
unnecessary cross-field vertical support in interlaced material.

So "only horizontal seams are affected" is correct regarding **seam location**, but not
necessarily every aspect of filter support.

Recommended wording:

> Only the horizontal transform-seam positions change with frame-DCT versus field-DCT;
> vertical seam positions remain fixed, although field-aware support may still matter.

---

### 4.3 Claude addendum 3.3 seam geometry

**AGREE.**

For a 16-frame-line luma macroblock in a frame picture:

#### Frame-DCT

The two luma block rows occupy ordinary frame lines:

- upper block row: frame lines 0-7;
- lower block row: frame lines 8-15.

If those samples are considered separately by field:

top field:
- frame lines 0,2,4,6 | 8,10,12,14

bottom field:
- frame lines 1,3,5,7 | 9,11,13,15

Thus the frame-DCT internal 7/8 transform seam becomes a **centreline seam inside each
field**:

- top field: frame-line transition 6 | 8;
- bottom field: frame-line transition 7 | 9.

#### Field-DCT

Each 8x8 luma transform block contains eight lines of one field across the entire
16-frame-line macroblock height.

Therefore, inside one field, there is no halfway horizontal transform boundary inside
that macroblock.

The next horizontal transform boundary is at the macroblock boundary.

Claude's proposed geometry is therefore consistent with my mechanics findings.

---

### 4.4 Relationship to MERL's centreline observation

**AGREE WITH QUALIFICATION.**

Claude's explanation is highly plausible:

MERL's need to check both a field-domain block boundary and a field-domain centreline is
consistent with the coexistence of frame-DCT and field-DCT macroblocks.

However, I would not yet label MERL's observation as proof that this was specifically
caused by MPEG-2 `dct_type`, because Claude correctly notes that the codec in that paper
was not conclusively identified in the text read.

Recommended status:

**HYPOTHESIS strongly consistent with MPEG-2 mechanics.**

---

### 4.5 Claude addendum 3.4: field-domain filtering with metadata-selected seams

**AGREE and recommend as leading Family A hypothesis.**

This is currently the cleanest conceptual answer to Dave's concern.

For horizontal luma filtering in frame pictures:

- never mix opposite field polarity merely to apply the deblocker;
- operate in field-domain sample order;
- use per-macroblock `dct_type` to decide whether the internal field-centreline seam
  exists.

Provisional rule:

- frame-DCT macroblock:
  - macroblock-boundary horizontal seam;
  - field-centreline horizontal seam;
- field-DCT macroblock:
  - macroblock-boundary horizontal seam only.

This removes the need to **detect seam geometry from pixels**.

It does not remove the need to protect real edges.

That distinction is important.

---

### 4.6 Mixed DCT types at vertically adjacent macroblock boundaries

Claude lists this as open.

I think the geometry is less problematic than the addendum implies.

**HYPOTHESIS.**

At the horizontal boundary between two vertically adjacent macroblocks, there is a
transform boundary for each field regardless of whether either macroblock is frame-DCT
or field-DCT.

The ambiguous geometry mainly concerns the **internal horizontal seam inside a
macroblock**, not the 16-line macroblock boundary itself.

However, the appropriate filter strength/eligibility at the shared boundary may still
depend on metadata from both macroblocks.

This should be checked carefully before coding, but it does not currently look like a
fundamental geometry blocker.

---

### 4.7 Field pictures

**OPEN.**

Claude correctly leaves field pictures unresolved.

My mechanics research found that a field picture is already composed of one field's
successive lines and does not have the frame-DCT/field-DCT distinction used for frame
pictures.

The eventual algorithm should therefore have a distinct geometry path for field
pictures rather than trying to reuse the frame-picture mixed-DCT logic blindly.

Whether the user's LG captures actually contain field pictures should be measured early.

---

### 4.8 4:2:0 chroma

**CORRECTION / RESOLUTION OF ONE OPEN POINT.**

Claude's prior-art research found no answer.

My mechanics research found a normative MPEG-2 answer:

for 4:2:0 MPEG-2, chroma blocks remain organised in **frame structure for DCT coding**;
the luma frame-DCT/field-DCT reorganisation is not applied to the 4:2:0 chroma blocks in
the same way.

Therefore:

- do not apply luma `dct_type` seam geometry directly to 4:2:0 chroma;
- chroma still can block;
- in 4:2:0 there is one 8x8 Cb and one 8x8 Cr block per 16x16 luma macroblock;
- therefore chroma transform boundaries coincide with luma macroblock boundaries rather
  than the luma internal 8x8 boundaries.

This is a significant point for `06_DEBLOCK_CONCEPT.md`.

---


## 6. Dave's explicit requirement: do not adopt independent field processing as the model

### 5.1 Requirement

**DECISION REQUEST / USER REQUIREMENT TO PRESERVE.**

Dave explicitly does **not** want the project to adopt this conceptual model:

> split an interlaced frame into two fields and process the two fields independently as the
> deblocking approach.

The concern is that a frame picture may contain a mixture of frame-DCT and field-DCT
macroblocks. A blanket "field-based processing" model can therefore hide the fact that the
existence and position of an internal horizontal transform seam varies on a
macroblock-by-macroblock basis.

This requirement is not an objection to using same-field-polarity samples where MPEG-2
geometry requires them. It is an objection to making "separate the frame into two fields
and independently process each field" the algorithmic model.

### 5.2 Agreed clarification

**AGREE.**

The preferred conceptual model should instead be:

> **Frame-owned, metadata-directed filtering, with field-parity-aware sample access only
> where required by the MPEG-2 transform geometry.**

The decoded VapourSynth frame remains the object being filtered.

The `.idx2` metadata tells the filter, macroblock by macroblock, which transform geometry
applies.

For luma in a frame picture:

- if the macroblock is frame-DCT coded, the index tells us that the internal horizontal
  transform seam exists;
- if the macroblock is field-DCT coded, the index tells us that the corresponding
  ordinary internal frame-centre seam does not exist in the same way;
- at macroblock boundaries, the geometry is likewise known from the raster and the
  neighbouring macroblock metadata.

Therefore **seam geometry is not detected from pixels** where the index provides the
necessary coding state.

### 5.3 Field-parity-aware access is not the same as independent field processing

Where horizontal filtering would otherwise mix opposite temporal fields, the filter may
use same-parity samples.

Conceptually, for a known frame-DCT internal seam:

```text
top-field samples:     ... 4, 6 | 8, 10 ...
bottom-field samples:  ... 5, 7 | 9, 11 ...
```

That is a sampling rule inside one frame-owned filtering operation.

It is **not**:

```text
split frame into field A
split frame into field B
run an independent deblocker on each field
recombine fields
```

The distinction is important because the metadata, not a generic field grid, determines
which transform seam exists for each macroblock.

### 5.4 What still requires pixel analysis

Knowing the exact transform geometry does not eliminate all content decisions.

A genuine image edge can lie on a known transform boundary.

The project may therefore still need local pixel analysis to decide whether, or how
safely, the known seam should be corrected.

This is **edge-preservation / correction eligibility**, not seam-location detection.

The intended distinction is:

1. **Where is the coded transform seam?**
   - determined from MPEG-2 geometry and `.idx2` metadata;
   - no pixel detection required where metadata is authoritative.

2. **Is the visible discontinuity at that known seam actually blocking rather than a
   genuine picture edge?**
   - may require local pixel evidence;
   - correction should be bounded by the selected global strength and relevant codec
     information.

### 5.5 Consequence for Family A wording

The phrase:

> "field-domain filtering"

is potentially misleading if read as "split the frame and process the fields
independently."

For future project documents, the preferred wording should be:

> **frame-owned, metadata-directed filtering with field-parity-aware sample access**

or equivalent wording that preserves the same meaning.

Family A should therefore be understood as:

- one decoded frame remains the processing object;
- seam existence/geometry comes from per-macroblock MPEG-2 metadata;
- same-field-polarity samples are used where required to avoid temporal-field mixing;
- there is no separate-field deblocking pass as an algorithmic model.

### 5.6 Three-way review implication

This clarification should be treated as a project-scoping requirement during the
three-way review.

Any future concept proposal that says "process each field separately" must be examined
carefully and rejected unless it is merely shorthand for parity-aware sampling inside the
frame-owned, metadata-directed model described above.


## 6. Claude's three kinds of "detection"

### 5.1 Geometry detection

**AGREE strongly.**

This vocabulary is useful.

The custom index can potentially eliminate the need to infer:

> where the relevant transform seam is

for luma frame pictures.

That is qualitatively different from deciding whether visible pixels should be modified.

---

### 5.2 Artifact eligibility / magnitude

**AGREE WITH QUALIFICATION.**

Quantiser-bounded correction is attractive because it constrains damage.

However, "quantisation at that macroblock's quantiser could plausibly have caused" is not
yet a defined bound.

MPEG-2 inverse quantisation also depends on:

- intra versus non-intra formulae;
- weighting matrices;
- coefficient values;
- clipping/mismatch behaviour.

So a safe correction bound based only on macroblock quantiser must initially be treated
as an empirical or derived threshold, not a rigorous mathematical maximum.

---

### 5.3 Genuine edge versus blocking edge

**AGREE.**

Metadata cannot eliminate this problem completely.

A genuine image edge can lie exactly on a transform boundary.

Therefore the project cannot avoid all pixel-content decisions.

The useful distinction is:

- **geometry** can potentially come from syntax metadata;
- **edge preservation** still requires local reconstructed-pixel evidence.

This distinction should be preserved in the concept document.

---

## 7. FFmpeg MPEG-2 quantiser export

Claude's S18/Q11 finding is important enough to cross-check directly.

### 6.1 Export exists

**RESEARCHED / CROSS-CHECKED.**

Current FFmpeg has `AV_VIDEO_ENC_PARAMS_MPEG2`.

Its documentation says the final block quantiser is represented through the
frame-level value plus per-block delta.

FFmpeg's QP-table helper describes extraction of:

> one 8-bit QP value per 16x16 macroblock in raster order

from this side data.

Relevant current documentation:

- https://ffmpeg.org/doxygen/trunk/video__enc__params_8h.html
- https://ffmpeg.org/doxygen/trunk/qp__table_8h.html

### 6.2 MPEG-2 decoder attaches the QP table to output frames

**RESEARCHED / CROSS-CHECKED.**

FFmpeg's MPEG-1/2 decoder calls its QP export function on the frame being output.

For B pictures / low-delay it exports the current picture.

For reordered I/P pictures it exports the delayed previous picture when that picture is
actually returned.

Therefore this side data is associated with decoder output frames rather than merely raw
bitstream parse order.

This is favourable if such side data can be obtained through the eventual decoding path.

### 6.3 What this changes

It does **not** currently invalidate the custom `.idx2` concept.

It does mean:

- QP alone is not sufficient justification for a custom reference-decoder indexer;
- Stage 2 should measure QP's value independently from `dct_type`;
- if `dct_type` and other syntax metadata add no measurable benefit, a simpler decoder
  side-data route should be reconsidered.

### 6.4 What remains open

I have not established that BestSource exposes this FFmpeg side data through VapourSynth.

I also found no standard FFmpeg frame-side-data field exposing per-macroblock MPEG-2
`dct_type`.

Therefore the proposed custom index still has a plausible unique purpose.

---

## 8. Coded-block pattern and coefficient activity

Claude found no MPEG-2 post-filter evidence establishing value for these.

**AGREE.**

My mechanics research nevertheless ranks CBP above motion vectors as the next metadata
worth testing if QP + dct_type is insufficient, because CBP directly identifies which
of the six 4:2:0 transform blocks carry coded residual information.

But Claude's lack of prior-art support is a reason **not** to put CBP into the initial
algorithm automatically.

Recommended sequence:

1. pixels only;
2. pixels + QP;
3. pixels + QP + dct_type;
4. only then test CBP if results leave a clear problem;
5. coefficient activity only after that.

This keeps the index minimal.

---

## 9. Motion compensation and 16x16 boundaries

Claude raises the possibility that macroblock edges can carry prediction discontinuities
not reducible to residual 8x8 quantisation boundaries.

**AGREE as a research question.**

However, I would avoid creating a second special "16x16 strength" path before experiments.

Every 16x16 macroblock boundary is already also an 8x8 transform-grid boundary in luma.

The initial filter can therefore process it through the same boundary framework and let
the Stage 2 evidence show whether macroblock boundaries require distinct treatment.

Motion vectors themselves remain low priority.

---

## 10. Review of candidate families

### 9.1 Family A - QP-scaled boundary filter with dct_type geometry

**SUPPORT as leading candidate.**

This family currently best matches the project constraints:

- deterministic;
- short support;
- scalar-friendly;
- AVX2-friendly;
- one user strength;
- MPEG-2 metadata used only where it has a plausible purpose.

Refinement from the addendum should replace the less precise original description:

> for horizontal luma seams in frame pictures, process in field-domain sample order and
> use `dct_type` to select the internal seam geometry.

Do not yet freeze the mathematical filter itself.

Claude's Annex-F/two-mode family is prior art to study, not automatically the final
kernel.

---

### 9.2 Family B - pixel-only field-aware control

**SUPPORT as mandatory control, not preferred design.**

This is essential for falsification.

It answers:

> Does dct_type actually buy us anything?

If Family A with dct_type cannot materially outperform or simplify Family B, the
custom-index premise is weakened.

---

### 9.3 Family C - shifted-DCT re-quantisation

**SUPPORT only as optional quality/reference family.**

It is intellectually useful because it uses quantisation information more directly.

But it is substantially heavier and may solve a broader restoration problem than the
user actually wants.

It should not delay testing Families A and B.

---

## 11. Recommended Stage 2 ablation

I endorse Claude's structure with one refinement.

Run:

1. unfiltered decode;
2. Family B, pixel-only geometry detection;
3. Family A kernel using QP but no dct_type;
4. same Family A kernel using QP + dct_type geometry;
5. optionally Family A with dct_type but fixed/emulated QP;
6. optionally Family C.

This separates three questions:

- value of the filtering kernel itself;
- value of real QP;
- value of dct_type.

The particularly useful comparisons are:

- 3 versus 4 = value of dct_type;
- 5 versus 4 = value of real per-MB QP;
- 2 versus 4 = total value of metadata-driven geometry/strength relative to pixel-only
  handling.

---

## 12. Points where I would narrow Claude's wording

### 11.1 "The quantiser can be had without a custom indexer"

**NARROW.**

Better:

> FFmpeg's MPEG-2 decoder can export per-macroblock quantiser side data, so QP alone may
> not require the project's custom reference-decoder index.

Whether this can be obtained cleanly in the actual BestSource/VapourSynth architecture
is still open.

---

### 11.2 "Practical tools switch the whole frame"

**NARROW.**

DGDecode's documented field/progressive post-processing mode is relevant evidence, but
without reading its implementation source we should avoid over-specifying exactly how
every internal boundary is handled.

The documented behaviour is enough to show it does not expose or advertise a
per-macroblock dct_type-driven geometry.

---

### 11.3 "Motion compensation is a second source of blocking"

**ACCEPT CONCEPTUALLY, BUT KEEP DISTINCT.**

Prediction can introduce or propagate block-boundary discontinuities.

But for this project, the visually relevant target is the final reconstructed
discontinuity, not necessarily attribution of the artifact to residual quantisation
versus prediction.

Do not let this finding pull the first design toward motion-vector metadata.

---

## 13. Points from Claude that strengthen the project

1. Real QP has strong historical precedent as post-processing metadata.
2. There is a real pixel-only competitor capable of handling interlaced geometry.
3. No evidence was found that detailed MPEG-2 motion metadata is needed.
4. `dct_type` remains an unproven but technically coherent differentiator.
5. The proposed experiment can measure its value directly.
6. The addendum provides a cleaner way to exploit dct_type without mixing fields.
7. A small, deterministic Annex-F-like family remains a credible production direction.

---

## 14. Points from Claude that weaken or challenge the project

1. A custom index is not justified by QP alone if FFmpeg side data is practical.
2. Pixel-only field-aware filtering may be good enough.
3. Prior art does not establish that per-MB dct_type improves MPEG-2 post-deblocking.
4. Real captures may have analogue/VHS noise that hides or confounds block artifacts.
5. Current-picture metadata cannot fully describe blocking propagated from reference
   pictures.
6. Existing practical post-processing already has decades of tuned heuristics, so a
   simple new filter is not guaranteed to win.

These are appropriate feasibility-gate risks, not reasons to stop before testing.

---

## 15. Recommended three-way review conclusions

I recommend that Dave, Claude and ChatGPT provisionally agree on the following, subject
to Dave's ratification.

### R1

Carry Family A forward as the leading metadata-assisted hypothesis:

> short-support QP-aware deblocking, with horizontal luma filtering performed in the
> field domain and seam geometry selected per macroblock from dct_type.

### R2

Carry Family B forward only as the mandatory pixel-only falsification control.

### R3

Keep Family C optional as a quality/reference experiment.

### R4

Do not add CBP, coefficient activity, motion mode or motion vectors to the initial
`.idx2` research requirements.

### R5

Treat 4:2:0 chroma independently from luma dct_type geometry.

### R6

Design Stage 2 specifically to measure:

- value of the kernel;
- value of real per-MB QP;
- value of dct_type.

### R7

Investigate the FFmpeg MPEG-2 QP side-data path before claiming that QP itself requires
the custom indexer.

### R8

Retain the custom reference-decoder index approach provisionally because dct_type and
other MPEG-2 syntax metadata do not appear to be available through the standard FFmpeg
frame-side-data interface found so far.

---

## 16. Questions for Claude's response

1. Does Claude agree that addendum 3.3 is now supported by the mechanics track rather
   than remaining merely speculative geometry?

2. Does Claude agree that "only horizontal seams are affected" should be narrowed to
   "only horizontal seam POSITIONS change", because vertical-edge filtering support may
   still need field-aware handling?

3. Does Claude agree that the mixed-DCT-neighbour problem is mainly an eligibility/
   threshold issue at macroblock boundaries rather than an unresolved seam-position
   problem?

4. Does Claude agree that 4:2:0 chroma can now be removed from the unresolved
   dct_type-geometry list, while chroma filtering strength remains open?

5. Does Claude agree that the QP side-data finding makes the Stage 2 ablation more
   important rather than making the project index automatically unnecessary?

6. Does Claude see evidence in its sources that would justify testing CBP before the
   simpler QP + dct_type experiment?

---

## 17. Cross-review verdict

**PROVISIONAL VERDICT: CONTINUE.**

Claude's research materially improves the project.

The strongest result is not that metadata assistance has been proven.

It is that the project now has a clean falsifiable hypothesis:

> Authoritative MPEG-2 `dct_type` plus real per-macroblock quantiser information can
> permit a simpler and/or better field-safe deblocking decision than pixel-only
> detection.

The appropriate next action is not to enlarge `.idx2`.

It is to complete the three-way review, settle the conceptual geometry and experiment
design, then test the smallest metadata set capable of answering that hypothesis.

## 18. Change log

### v0.2 - 2026-10-06

- Added Dave's explicit requirement that the project must not adopt "split into two
  fields and independently process each field" as the deblocking model.
- Recorded the agreed alternative: frame-owned, metadata-directed filtering with
  field-parity-aware sample access only where MPEG-2 geometry requires it.
- Clarified that metadata determines seam geometry, while local pixel analysis may still
  be required for genuine-edge preservation.
- Clarified future Family A wording to avoid the ambiguous phrase "field-domain
  filtering" when it could be interpreted as independent field processing.

