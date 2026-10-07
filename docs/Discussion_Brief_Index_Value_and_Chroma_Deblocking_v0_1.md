# Discussion Brief: Index Value and Chroma Deblocking

**Filename:** `Discussion_Brief_Index_Value_and_Chroma_Deblocking_v0_1.md`  
**Version:** 0.1  
**Date:** 2026-10-07  
**Author:** ChatGPT, recording Dave's questions/assumptions and ChatGPT's responses  
**Status:** Discussion brief for Claude review. Not project authority.  
**Purpose:** Clarify two foundational assumptions before Stage 2 design is ratified:
1. why the custom index may be necessary; and
2. whether 4:2:0 chroma should also be deblocked.

---

## 1. Dave's original assumptions

Dave's working premise has been approximately:

### Assumption A - why the index matters

The exact block structure inside a decoded MPEG-2 frame can vary because macroblocks may use
frame-DCT or field-DCT organisation, potentially in mixtures within the same displayed frame.

Therefore the custom index was expected to be valuable because it would tell the deblocker exactly
where the relevant block/transform boundaries are, rather than forcing the filter to guess them
from reconstructed pixels.

### Assumption B - chroma probably also needs deblocking

Dave also had an intuitive but explicitly unverified assumption that chroma could exhibit visible
blocking and should probably be deblocked as well as luma.

The question raised after Stage 1 was:

> If MPEG-2 4:2:0 chroma does not follow luma `dct_type`, does that mean chroma does not need
> deblocking, or merely that chroma needs a different deblocking geometry?

These assumptions are reasonable starting hypotheses, but they need to be separated into what the
research established and what remains experimental.

---

## 2. ChatGPT response on the value of the index

### 2.1 The important correction

The index does **not** reveal the ordinary luma coding grid itself.

For uncropped, unscaled MPEG-2, the regular 8x8 / 16x16 grid positions are already derivable from
frame coordinates.

The unique potential value of the index is more precise:

> **It supplies authoritative per-macroblock coding/transform state that tells the deblocker which
> candidate transform geometry actually applies at that macroblock.**

For suitable MPEG-2 frame pictures, luma macroblocks can use different transform organisations.

The project semantic states are:

```text
FRAME
FIELD
NONE
```

where:

```text
FRAME
    current coded residual uses frame-DCT organisation

FIELD
    current coded residual uses field-DCT organisation

NONE
    no current coded residual transform geometry is asserted
```

`NONE` does not imply that reconstructed-pixel blocking cannot be visible; prediction can propagate
blocking into skipped/no-residual regions.

### 2.2 Why this matters geometrically

For horizontal luma transform geometry in frame pictures:

```text
FRAME:
    macroblock horizontal boundary
    +
    internal field-centreline seam

FIELD:
    macroblock horizontal boundary only

NONE:
    no current internal residual-transform seam is asserted
```

The FRAME internal seam is observed using same-field-polarity samples.

Therefore a pixel-only filter knows the possible grid locations but does not know the encoder's
actual per-macroblock transform organisation.

It can only infer:

```text
"Does this candidate location look block-like?"
```

from reconstructed pixels.

The index can instead state:

```text
"This macroblock was actually coded with FRAME transform organisation."
```

or:

```text
"This macroblock was actually coded with FIELD transform organisation."
```

That distinction is especially important because Stage 1 found extensive mixed transform
organisation within individual frames.

### 2.3 Stage 1 evidence strengthened the premise

The formal `TEST_4A_A003` material showed:

```text
mixed FRAME/FIELD frames:
    original = 299/300
    blocky   = 300/300
```

The corroborating `TEST_2A_A001` pair also showed widespread mixed transform organisation.

So the issue is not merely permitted by MPEG-2 syntax; it occurs heavily in the tested material.

### 2.4 The refined index premise

The project premise should therefore be stated as:

> **The custom index may be worthwhile because it supplies authoritative per-macroblock transform
> geometry -- particularly FRAME/FIELD/NONE -- which determines which horizontal luma transform
> seams actually apply within mixed-coded frame pictures. Without that metadata, a deblocker knows
> the candidate coding grid but must infer applicable transform geometry from the decoded pixels.**

This is narrower and more accurate than saying:

> "The index tells us where all the block boundaries are."

### 2.5 Why Stage 2 still has to test it

Semantic correctness alone does not prove practical value.

A sufficiently good pixel-only detector may infer the relevant boundaries accurately enough that
authoritative transform state gives little visible benefit.

Therefore the key Stage 2 comparison remains:

```text
Family A + real QP + pixel-detected geometry

versus

Family A + real QP + authoritative FRAME/FIELD/NONE geometry
```

If authoritative geometry materially improves artifact removal/detail preservation, the custom
index has demonstrated a unique value.

If it does not, the extra architecture may not be justified even though its metadata is more
semantically exact.

---

## 3. What the mechanics research established about 4:2:0 chroma

### 3.1 Chroma transform organisation is different from luma

The MPEG-2 mechanics research found:

**RESEARCHED:**

For MPEG-2 4:2:0, chrominance blocks are always organised in frame structure for DCT coding.

This differs from 4:2:2 and 4:4:4, where chroma may follow frame/field DCT treatment similarly to
luma.

Thus luma per-macroblock `dct_type` does **not** create the same transform-seam geometry in
4:2:0 chroma.

### 3.2 Chroma can still have blocking

This is the crucial distinction.

The fact that chroma remains frame-organised does **not** mean:

```text
chroma has no transform blocks
```

or:

```text
chroma cannot show quantisation blocking
```

For each 16x16 luma macroblock in 4:2:0 there is:

```text
one 8x8 Cb transform block
one 8x8 Cr transform block
```

Therefore the chroma planes still have regular 8x8 DCT blocks, quantisation, and block boundaries.

The mechanics research concluded:

> **HYPOTHESIS strongly supported by transform structure: chroma can still exhibit blocking.**

Its principal transform boundaries correspond to luma macroblock boundaries.

### 3.3 Field-based prediction remains possible

The MPEG-2 standard also permits field-based prediction for 4:2:0 chroma even though its DCT
organisation remains frame-structured.

Therefore:

```text
DCT geometry
```

and:

```text
prediction geometry
```

are separate issues.

This means that visible chroma discontinuities on interlaced MPEG-2 may still have complications
that are not explained by chroma DCT geometry alone.

---

## 4. What Claude's prior-art research found about chroma deblocking

Claude's Stage 0 prior-art research found positive evidence that chroma deblocking is a real,
established operation.

### 4.1 Practical MPEG post-processing

**RESEARCHED:**

DGDecode and libpostproc-derived tools provide separate controls for chroma horizontal and vertical
deblocking.

That is direct evidence that practical MPEG-era post-processing considered chroma blocking worth
addressing.

### 4.2 Other codec/filter evidence

Claude also found:

- the MPEG-4 informative deblocking filter is applied to both luminance and chrominance;
- H.264's in-loop deblocker filters luma and chroma, with different treatment.

These are not direct proof of the correct MPEG-2 chroma algorithm, but they reinforce the general
point that chroma blocking is a legitimate artifact class rather than something that can be
dismissed because chroma is subsampled.

### 4.3 Important research gap

Claude found **no useful prior-art answer specifically for interlaced MPEG-2 4:2:0 chroma**
addressing questions such as:

- should chroma filtering use field-domain access?
- should field-based prediction change the filtering rule?
- what threshold should chroma use relative to luma?
- how much visible benefit is obtained on real interlaced MPEG-2 captures?

So the research supports:

```text
chroma deblocking can be useful / historically used
```

but does **not** establish:

```text
the correct chroma filter for Dave's interlaced 4:2:0 material
```

---

## 5. What follows for the custom index

### 5.1 Luma

For luma, the potential unique index value is strong and clear:

```text
authoritative per-MB FRAME/FIELD/NONE transform geometry
```

This is metadata that final pixels do not directly expose.

### 5.2 Chroma

For 4:2:0 chroma, luma `dct_type` is **not** needed to locate the chroma transform grid.

The chroma transform grid is regular:

```text
one 8x8 chroma block per luma macroblock, per chroma plane
```

Therefore the index's unique FRAME/FIELD transform-state advantage is principally a **luma**
advantage.

However, the index can still provide other potentially useful chroma-related information,
especially:

- effective per-MB quantiser;
- picture/frame correspondence;
- perhaps later coding-state information if experiment justifies it.

QP itself may eventually be obtainable through a simpler decoder-side-data architecture, so this
does not by itself prove that the custom index is needed for chroma.

### 5.3 Current architectural interpretation

The likely architecture is therefore:

```text
LUMA:
    fixed candidate grid
    +
    index-provided authoritative per-MB transform geometry
    +
    per-MB QP
    +
    pixel edge/activity tests

CHROMA:
    fixed chroma transform grid at macroblock boundaries
    +
    probably QP-aware filtering
    +
    chroma-specific edge/activity thresholds
    +
    no blind inheritance of luma FRAME/FIELD geometry
```

This is a Stage 2 hypothesis, not yet a ratified algorithm.

---

## 6. Does chroma need to be in the first Stage 2 experiment?

ChatGPT's Stage 2 v0.1 draft proposed starting with luma only.

The reason was methodological, not a conclusion that chroma is unimportant:

- the custom-index hypothesis is most directly testable on luma;
- transform-state geometry is a luma issue in 4:2:0;
- chroma threshold/strength is still open;
- changing luma and chroma simultaneously would make the first ablation harder to interpret.

However, Dave's question exposes an important issue:

> If the intended final deblocker is expected to remove visible MPEG-2 blocking in both luma and
> chroma, should chroma really be deferred beyond the feasibility gate, or should Stage 2 include a
> bounded chroma experiment before the gate closes?

ChatGPT's current view is:

> **Chroma should not be dismissed or treated as optional merely because luma `dct_type` does not
> control its geometry.**

A reasonable experimental order is:

1. establish the unique value (or lack of value) of index geometry on luma;
2. then, before the overall deblocking concept is declared successful/complete, perform a bounded
   chroma test on the fixed chroma macroblock grid;
3. determine whether chroma filtering produces visible/numerical benefit and what relative
   threshold/strength is appropriate.

Whether step 2 must be part of the **same Stage 2 feasibility gate** is a matter worth Claude and
Dave reviewing now.

---

## 7. Questions for Claude

Claude is asked to review both Dave's assumptions and ChatGPT's responses.

### Q1 - Index premise

Is this refined statement correct?

> The custom index does not reveal the fixed 8x8/16x16 grid itself. Its potentially unique value is
> authoritative per-macroblock transform geometry, especially FRAME/FIELD/NONE for luma in mixed
> frame pictures, telling the filter which candidate horizontal transform seams actually apply.

If not, please identify precisely what is missing or overstated.

### Q2 - Mixed luma geometry

Given the Stage 1 measurements showing widespread mixed FRAME/FIELD macroblocks, do you agree that
the original motivation for an index has been materially strengthened rather than weakened?

### Q3 - Chroma blocking

Does the prior-art evidence support the proposition that chroma blocking is a legitimate target of
post-deblocking even though MPEG-2 4:2:0 chroma DCT organisation is always frame-structured?

Please distinguish:

- evidence that chroma deblocking is historically/practically useful;
- evidence specific to interlaced MPEG-2 4:2:0;
- remaining gaps.

### Q4 - Chroma geometry

Do you agree that, for the project's 4:2:0 frame-picture material:

- luma `dct_type` should not be copied into chroma seam geometry;
- chroma transform seams principally occur at the 8x8 chroma block boundaries corresponding to
  luma 16x16 macroblock boundaries?

Please identify any qualification concerning field prediction or sample access.

### Q5 - Index value for chroma

If chroma geometry is regular, what useful index metadata -- if any -- should the first chroma
experiment consume?

Candidates are:

- effective per-MB QP;
- picture type;
- coding state;
- no metadata at all beyond frame correspondence.

Please resist adding metadata without evidence.

### Q6 - Stage 2 scope

Should the current Stage 2 design remain:

```text
core luma ablation first
then chroma follow-up
```

or should a bounded chroma experiment be made mandatory before the Stage 2 feasibility gate closes?

ChatGPT currently favours:

> luma ablation first, but do not close the overall deblocking feasibility question without at least
> a bounded chroma test if visible chroma blocking exists in the target material.

### Q7 - Chroma strength

What does the prior art support regarding:

- chroma threshold relative to luma;
- chroma correction strength relative to luma;
- separate horizontal/vertical chroma control?

If the literature does not support a concrete ratio, please say so rather than infer one.

### Q8 - Possible confusion with chroma upsampling

Earlier discussion noted that some perceived interlaced chroma artifacts may instead involve 4:2:0
chroma upsampling/interlacing issues rather than DCT blocking.

What practical tests should distinguish:

```text
compression block artifact
```

from:

```text
interlaced chroma upsampling / siting artifact
```

without expanding this project unnecessarily?

### Q9 - Stage 2 design impact

Please identify any changes that should be made to `Stage2_Experiment_Design_v0_1.md` because of
this discussion.

Classify them as:

- MUST CHANGE before ratification;
- SHOULD CHANGE;
- no change required.

---

## 8. ChatGPT provisional conclusion

The current evidence supports all of the following simultaneously:

1. **Dave's index intuition was substantially correct.**  
   The important unique information is not the regular grid coordinate itself but the
   macroblock-by-macroblock transform geometry that selects which luma seams actually apply.

2. **Stage 1 materially strengthened that case.**  
   Mixed FRAME/FIELD organisation is pervasive in the tested clips.

3. **Dave's chroma intuition is also plausible and supported in general.**  
   4:2:0 chroma still has quantised 8x8 transform blocks and can exhibit blocking; practical MPEG
   post-processors have chroma deblocking.

4. **But chroma is geometrically different from luma.**  
   Luma `dct_type` does not define 4:2:0 chroma transform geometry.

5. **Therefore chroma does not weaken the index premise; it separates the problem into two paths.**  
   The index's unique transform-state value is mainly for luma. Chroma may still benefit from
   deblocking on its regular grid, probably with independent thresholds/strength and possibly
   QP assistance.

6. **The remaining question is experimental, not conceptual.**  
   We need to determine whether chroma blocking is materially visible on Dave's target captures and
   whether a bounded chroma filter improves it without creating colour smearing or interlace
   artifacts.

This brief does not modify repository authority or the current Stage 2 draft. It is an input to
Claude/Dave review before Stage 2 v0.1 is ratified.

---

## 9. Source documents used

This brief is based on the existing project research/review trail:

- `ChatGPT_MPEG2_Deblocking_Codec_Mechanics_v0_1.md`
- `Claude_MPEG2_Deblocking_Prior_Art_v0_1.md`
- `ChatGPT_FINAL_CROSS_REVIEW_OF_Claude_RESPONSE_v0_1.md`
- `Stage1_Evidence_and_Gate_Report_v0_3.md`
- `Stage2_Experiment_Design_v0_1.md`

No new external research was performed for this brief.

---

## 10. Change log

### v0.1 - 2026-10-07

- Recorded Dave's original index and chroma assumptions.
- Clarified fixed-grid knowledge versus authoritative per-MB transform geometry.
- Summarised the Stage 0 mechanics finding that MPEG-2 4:2:0 chroma remains frame-organised for DCT.
- Recorded that chroma can nevertheless exhibit DCT/quantisation blocking.
- Summarised prior-art evidence for practical chroma deblocking and the interlaced-4:2:0 research gap.
- Separated index value for luma from possible QP/fixed-grid chroma filtering.
- Raised whether a bounded chroma experiment should be mandatory before the Stage 2 feasibility gate closes.
- Added explicit questions for Claude review.
