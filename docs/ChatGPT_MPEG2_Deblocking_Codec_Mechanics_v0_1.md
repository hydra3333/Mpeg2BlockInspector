# ChatGPT MPEG-2 Deblocking Codec Mechanics Research

**Filename:** `ChatGPT_MPEG2_Deblocking_Codec_Mechanics_v0_1.md`
**Version:** 0.1
**Date:** 2026-10-06
**Author:** ChatGPT
**Status:** Stage 0 research evidence input; not repository authority.
**Controlling project proposal:** `MPEG2_Macroblock_Index_VapourSynth_Deblocking_Project_Proposal_v0_5.md`
**Research brief:** `research_proposal_01_v1.0.md`

---

## 1. Purpose

This document is ChatGPT's first independent Stage 0 research pass on MPEG-2 coding mechanics relevant to a possible metadata-assisted post-deblocking filter.

Its focus is deliberately different from Claude's prior-art track.

Primary subjects:

- MPEG-2 macroblock and 8x8 transform geometry;
- frame-DCT versus field-DCT;
- field-picture versus frame-picture structure;
- MPEG-2 4:2:0 chroma geometry;
- quantiser semantics;
- skipped/intra/inter/coded-block semantics;
- coded order versus display order;
- implications for `.idx2`;
- implications for a simple post-deblocking algorithm;
- scalar-reference and AVX2 suitability.

This is an evidence input only.

Nothing in this file becomes project truth until reviewed, challenged, and ratified by Dave.

---

## 2. Evidence labels used here

**RESEARCHED**
A claim directly supported by a cited source.

**HYPOTHESIS**
An inference, design implication, interpretation, or proposal derived from the researched facts.

**OPEN**
A question that remains unresolved and requires further source reading, source-code inspection, or experiment.

**VERIFIED**
Not used here except for simple arithmetic. Under the project rules, external research alone does not make a fact VERIFIED.

---

## 3. Source set and reading depth

### S1 - ISO/IEC 13818-2 / ITU-T H.262 MPEG-2 Video specification

Title:
`ISO/IEC 13818-2:1995 / ITU-T Recommendation H.262 (1995)`

Year:
1995

Venue:
ISO/IEC / ITU-T international standard.

Relevance:
MPEG-2-specific; normative decoding syntax/process.

Reading depth:
**PARTIAL TEXT / RELEVANT SECTIONS READ**, including extracted text and visual inspection of relevant pages/figures.

Relevant subjects read:

- frame reordering;
- macroblock structure;
- frame-DCT and field-DCT structure;
- macroblock modes;
- dct_type;
- quantiser_scale_code;
- q_scale_type;
- quantiser scale mapping;
- weighting matrices;
- coded block pattern;
- skipped macroblocks;
- temporal_reference.

Accessible copy used:
https://burgerlib.readthedocs.io/en/latest/is138182.pdf

A second ITU-hosted result exposing the quantiser table was also found:
https://www.itu.int/rec/dologin_pub.asp?id=T-REC-H.262-199507-S!!PDF-E&lang=s&type=items

Confidence:
High for claims directly grounded in the cited clauses/figures.

---

### S2 - FFmpeg MPEG-1/2 decoder source

Title:
`libavcodec/mpeg12dec.c`

Organisation:
FFmpeg project.

Relevance:
Practical MPEG-2 decoder implementation.

Reading depth:
**PARTIAL SOURCE READ**, focused on macroblock parsing, dct_type/interlaced_dct, qscale, skip handling, and block decoding.

Primary source:
https://www.ffmpeg.org/doxygen/8.1/mpeg12dec_8c_source.html

Additional current/trunk references:
https://ffmpeg.org/doxygen/trunk/mpeg12dec_8c_source.html
https://www.ffmpeg.org/doxygen/9.0/mpeg12dec_8c_source.html

Confidence:
High for what FFmpeg itself does; not a substitute for the MPEG-2 standard.

---

### S3 - FFmpeg MPEG quantiser data

Title:
`libavcodec/mpegvideodata.c`

Organisation:
FFmpeg project.

Relevance:
Practical implementation of MPEG-2 nonlinear qscale table.

Reading depth:
**PARTIAL SOURCE READ**.

Source:
https://www.ffmpeg.org/doxygen/8.1/mpegvideodata_8c_source.html

Confidence:
High for FFmpeg implementation; consistent with ISO/IEC 13818-2 Table 7-6.

---

### S4 - Linux V4L2 MPEG-2 stateless decoder controls

Title:
`Codec Control Reference - MPEG-2`

Organisation:
Linux kernel documentation.

Relevance:
MPEG-2 syntax/state representation used by decoder APIs.

Reading depth:
**PARTIAL DOCUMENT READ**.

Source:
https://www.kernel.org/doc/html/v5.1/media/uapi/v4l/ext-ctrls-codec.html

Confidence:
High as corroborating implementation documentation.

---

### S5 - Chapter 13: MPEG-2 technical text

Title:
`Chapter 13: MPEG-2`

Relevance:
Secondary MPEG-2 technical explanation.

Reading depth:
**PARTIAL TEXT / SEARCH RESULT EXCERPT**.

Source:
https://ez.analog.com/cfs-filesystemfile/__key/communityserver-discussions-components-files/331/2251.video_2D00_demy5.pdf

Confidence:
Moderate; used only as corroboration where the standard is clearer.

---

### S6 - Forchhammer MPEG-2 restoration paper

Title:
`A unified approach to restoration, deinterlacing and resolution enhancement in decoding MPEG-2 video`

Author:
Soren Forchhammer

Year:
2002

Venue:
IEEE Transactions on Circuits and Systems for Video Technology, Vol. 12, No. 9.

Relevance:
MPEG-2-specific; post-decode restoration / quality estimation.

Reading depth:
**PARTIAL TEXT / EXCERPT**.

Accessible result:
https://www.researchgate.net/publication/3308434_Forchhammer_S_A_unified_approach_to_restoration_deinterlacing_and_resolution_enhancement_in_decoding_mpeg-2_video_IEEE_Trans_Circuits_Syst_Video_Technol_129_803-811

Confidence:
Moderate for the limited claims used here.

---

### S7 - MPEG-2 postprocess deblocker patent

Title:
`Deblocker for postprocess deblocking`

Patent:
US7574060B2

Year:
2009 grant; earlier filing/publication history exists.

Relevance:
MPEG-2-specific post-decode deblocking architecture using decoder side information.

Reading depth:
**PARTIAL TEXT / RELEVANT DESCRIPTION READ**.

Source:
https://patents.google.com/patent/US7574060B2/en

Confidence:
Moderate.
A patent demonstrates an implemented/design approach, not proof that the approach is optimal.

---

## 4. Core MPEG-2 spatial structure

### 4.1 Macroblock dimensions and 4:2:0 block count

**RESEARCHED (S1).**

For 4:2:0 MPEG-2, one macroblock consists of:

- four 8x8 luminance blocks;
- one 8x8 Cb block;
- one 8x8 Cr block.

Thus the spatial coverage of a 4:2:0 macroblock is:

- luma: 16x16 samples;
- each chroma plane: 8x8 samples.

The standard's Figure 6-10 explicitly shows the four luma blocks in a 2x2 arrangement and one block for each chroma component.

### 4.2 Immediate deblocking implication

**HYPOTHESIS.**

For progressive/frame-DCT 4:2:0 luma, potential transform-block discontinuities exist:

- at the internal vertical luma boundary x = 8 within each 16x16 macroblock;
- at the internal horizontal luma boundary y = 8 within each 16x16 macroblock;
- at macroblock boundaries, which are simultaneously boundaries between 8x8 luma blocks.

For 4:2:0 chroma:

- there is only one 8x8 Cb and one 8x8 Cr transform block per 16x16 luma macroblock;
- therefore there is no additional internal 8x8 chroma transform seam inside a macroblock;
- chroma DCT-block boundaries occur where luma macroblock boundaries occur spatially.

This means that "8x8 versus 16x16" needs different wording for luma and chroma.

For luma, both internal and macroblock-aligned 8x8 boundaries exist.

For 4:2:0 chroma, every transform boundary is also a macroblock boundary in luma coordinates.

---

## 5. Frame-DCT versus field-DCT in frame pictures

### 5.1 MPEG-2 permits both organisations

**RESEARCHED (S1).**

In frame pictures where both frame and field DCT coding may be used, the internal organisation of a macroblock differs according to DCT mode.

The standard states:

- frame-DCT blocks are composed of lines from the two fields alternately;
- field-DCT blocks are composed of lines from only one of the two fields.

The standard's Figures 6-13 and 6-14 visually show the different organisations.

### 5.2 `dct_type` is macroblock-level syntax

**RESEARCHED (S1).**

`dct_type` is a one-bit macroblock syntax element indicating whether that macroblock is frame-DCT or field-DCT coded.

The standard specifies that it is present when:

- `picture_structure` is frame picture;
- `frame_pred_frame_dct == 0`;
- and the macroblock is intra or has coded pattern information.

If `dct_type == 1`, the macroblock is field-DCT coded.

If `dct_type` is not present, its effective value is derived according to MPEG-2 rules.

Notably:

- in field pictures there is no frame/field DCT distinction;
- if `frame_pred_frame_dct == 1`, effective DCT type is frame;
- for uncoded/skipped macroblocks, `dct_type` is unused because no transform block is coded.

### 5.3 FFmpeg corroboration

**RESEARCHED (S2).**

FFmpeg reads an interlaced-DCT flag at macroblock level in frame pictures when `frame_pred_frame_dct` permits it.

The decoder code independently corroborates that this is real macroblock-level state rather than merely picture-level metadata.

### 5.4 Important correction to a simplistic fixed-grid model

**RESEARCHED FACT + HYPOTHESIS.**

The 16x16 macroblock raster itself remains fixed.

However, the transform support of the luma 8x8 blocks is not represented by a single simple contiguous 8x8 raster when a macroblock uses field-DCT.

Therefore the statement:

> all relevant deblocking boundaries are fixed by the pixel grid

is too simplistic for interlaced MPEG-2 luma.

The macroblock location is fixed, but the transform grouping inside it depends on `dct_type`.

This supports Dave's prior recollection that field- and frame-related blocking may coexist within one displayed frame.

The exact visible artifact behaviour remains an experimental question.

---

## 6. What field-DCT geometry means in displayed-frame coordinates

### 6.1 Frame-DCT luma

**RESEARCHED (S1).**

In frame-DCT mode, each 8x8 luma block contains alternating lines from the top and bottom fields.

Because those field lines are interleaved in ordinary frame storage, the block corresponds to the familiar contiguous 8x8 region in displayed-frame coordinates.

### 6.2 Field-DCT luma

**RESEARCHED (S1).**

In field-DCT mode, each 8x8 luma block contains samples from only one field.

Therefore eight vertical samples in a field-DCT block correspond to every-other frame line across the macroblock's 16-line luma height.

The standard Figure 6-14 shows the macroblock's field lines being separated into field-specific 8-line blocks.

### 6.3 Deblocking consequence

**HYPOTHESIS.**

For field-DCT luma, blindly treating y = 8 in displayed-frame coordinates as an internal 8x8 horizontal transform boundary would be wrong.

The transform blocks are field-separated, not ordinary top-half/bottom-half contiguous raster blocks.

A deblocker that filters across horizontal transform boundaries in field-DCT macroblocks probably needs parity-aware sample selection.

That may mean operating on:

- top-field samples separately;
- bottom-field samples separately;

rather than using adjacent raster rows as though the macroblock were frame-DCT coded.

### 6.4 Vertical luma boundary

**HYPOTHESIS.**

The x = 8 left/right division remains meaningful for both frame-DCT and field-DCT because the field reorganisation is vertical rather than horizontal.

However, in field-DCT mode, samples used by each 8x8 transform are field-parity-specific vertically.

Any vertical-edge filter spanning several rows should therefore still be careful not to mix temporal fields unnecessarily.

### 6.5 Horizontal macroblock boundaries

**HYPOTHESIS.**

At the boundary between vertically adjacent field-DCT macroblocks, the corresponding transform boundary for a given field is separated by two raster lines in full-frame coordinates.

A field-aware filter may need to compare same-parity lines across the macroblock boundary rather than simply the immediately adjacent raster lines.

This needs verification against the eventual decoded-memory layout and experiment.

---

## 7. Mixed frame-DCT and field-DCT neighbours

### 7.1 The syntax permits macroblock-by-macroblock DCT type

**RESEARCHED (S1, S2).**

Since `dct_type` is macroblock-level state in suitable frame pictures, adjacent coded macroblocks can in principle differ in DCT type.

### 7.2 Why this matters

**HYPOTHESIS.**

A boundary may have:

- frame-DCT macroblock on the left and field-DCT macroblock on the right;
- frame-DCT above and field-DCT below;
- or same-type neighbours.

Therefore a correct MPEG-2-aware deblocking algorithm may need boundary geometry derived from **both sides**, not just from the current macroblock.

This makes a one-bit per-macroblock `dct_type` potentially high-value metadata.

### 7.3 Open question

**OPEN.**

How common is mixed frame/field DCT on the user's LG MPEG-2 captures?

This should be measured during Stage 1 with the draft inspector/analyzer.

If almost all macroblocks are one mode, the practical value may be smaller than the syntax suggests.

---

## 8. 4:2:0 chroma and field-DCT

### 8.1 Chroma remains frame-organised for DCT

**RESEARCHED (S1).**

For MPEG-2 4:2:0, the standard states that chrominance blocks are always organised in frame structure for DCT coding.

This is explicitly different from 4:2:2 and 4:4:4, where chroma can follow the same frame/field DCT treatment as luma.

### 8.2 Field-based prediction can still occur

**RESEARCHED (S1).**

The standard also notes that field-based predictions may be made for these 4:2:0 chroma blocks.

Thus:

- chroma DCT organisation remains frame structure;
- prediction mode may still be field based.

DCT geometry and motion-prediction geometry are therefore separate issues.

### 8.3 Important project implication

**HYPOTHESIS.**

The first deblocking design should not apply luma field-DCT geometry blindly to chroma.

For 4:2:0:

- luma filtering geometry may depend on `dct_type`;
- chroma transform geometry does not depend on luma `dct_type` in the same way.

### 8.4 Does chroma blocking still exist?

**HYPOTHESIS strongly supported by transform structure.**

Yes, chroma can still exhibit blocking.

The fact that chroma is frame-organised does not remove quantisation or DCT block boundaries.

It means only that the chroma transform block geometry remains a normal 8x8 frame-organised block.

Because there is one 8x8 block per chroma plane per macroblock, chroma blocking would occur primarily at macroblock boundaries.

This should be confirmed visually and with real captures.

---

## 9. Field pictures versus frame pictures

### 9.1 Field picture definition

**RESEARCHED (S1).**

A field picture contains only lines from one field.

The standard states that in field pictures each block consists of successive lines in that picture.

There is no frame/field DCT distinction in a field picture.

### 9.2 Consequence for index design

**HYPOTHESIS.**

`picture_structure` is essential if field pictures are present.

A deblocker must know whether one `.idx2` output record corresponds to:

- a frame picture;
- a pair of field pictures assembled as one output frame;
- or another display mapping produced by the decoder/source filter.

This is more fundamental than merely storing a single picture coding type byte.

---

## 10. Coded order versus display order

### 10.1 MPEG-2 explicitly reorders frames

**RESEARCHED (S1).**

The standard distinguishes:

- coded order: order in the bitstream / reconstruction order;
- display order: order of reconstructed frames at decoder output.

When B-frames are present these orders differ.

The standard gives the example:

coded order:
`1I, 4P, 2B, 3B`

display order:
`1I, 2B, 3B, 4P`

### 10.2 Consequence for `.idx2`

**RESEARCHED FACT + PROJECT IMPLICATION.**

If `.idx2` record N is intended to correspond to VapourSynth frame N, the index must ultimately be emitted or reordered into **display order**, not simply syntax parse order.

This supports v0.5 section 6.5's plan to emit Stage 1 records where the decoder outputs a frame rather than where it first parses a picture.

### 10.3 `temporal_reference`

**RESEARCHED (S1).**

For ordinary non-low-delay operation:

- each coded frame's `temporal_reference` increments in display order modulo 1024;
- two field pictures forming one coded frame normally share the same temporal_reference;
- the value resets around GOP headers according to MPEG-2 rules.

### 10.4 Is temporal_reference alone sufficient?

**HYPOTHESIS: no, not universally.**

It is useful diagnostic metadata but is not a globally unique frame identifier because:

- it is only 10 bits;
- it resets with GOP structure;
- low-delay "big picture" rules complicate it;
- error/editing conditions may create complications.

For Stage 1 diagnostics it may be highly useful.

For final `.idx2` correspondence, a simple monotonically assigned display-record ordinal generated by the inspector is probably clearer.

---

## 11. Picture structure, repeat_first_field, and display semantics

### 11.1 Repeat-first-field exists in the decoding/display process

**RESEARCHED (S1).**

MPEG-2 has `repeat_first_field`, and the decoding process can output/repeat fields according to picture structure and flags.

### 11.2 Project implication

**OPEN / HYPOTHESIS.**

The critical project question is not merely "how MPEG-2 specifies display timing", but:

> What exact frame sequence does BestSource expose to VapourSynth for the target material?

The reference decoder's concept of output/display events and BestSource's frame exposure must be compared.

This is why Stage 5 remains necessary even if the MPEG-2 standard mapping is understood perfectly.

---

## 12. Quantiser semantics

### 12.1 `quantiser_scale_code` is not itself the final scale

**RESEARCHED (S1).**

`quantiser_scale_code` is a 5-bit integer from 1 to 31.

Zero is forbidden.

The active value is initially supplied at slice level and remains in effect until another value appears at slice or macroblock level.

A macroblock may therefore inherit the current quantiser scale rather than carry a new code explicitly.

### 12.2 `q_scale_type`

**RESEARCHED (S1).**

`q_scale_type`, carried in picture coding information, chooses one of two mappings from 5-bit `quantiser_scale_code` to actual `quantiser_scale`.

For `q_scale_type = 0`:

actual scale is linear:

1 -> 2
2 -> 4
...
31 -> 62

For `q_scale_type = 1`:

the mapping is nonlinear:

1, 2, 3, 4, 5, 6, 7, 8,
10, 12, 14, 16, 18, 20, 22, 24,
28, 32, 36, 40, 44, 48, 52, 56,
64, 72, 80, 88, 96, 104, 112.

FFmpeg contains the same nonlinear table.

### 12.3 `.idx2` implication

**HYPOTHESIS / RECOMMENDATION FOR LATER DISCUSSION.**

If the deblocker wants a comparable quantisation-severity scalar, storing the **actual derived quantiser scale** is probably more useful than storing only the raw 5-bit code.

The original draft's intended range of 1..112 appears consistent with that interpretation.

However, the final field semantics must be defined explicitly.

### 12.4 Skipped macroblocks and quantiser value

**RESEARCHED FACT + OPEN DESIGN QUESTION.**

A skipped macroblock contains no encoded macroblock data.

Therefore it does not carry its own new quantiser_scale_code.

The current active quantiser state may exist in the decoder, but assigning that value to a skipped macroblock would be a project-defined derived value, not a syntax element belonging to that skipped macroblock.

The `.idx2` specification must say whether a skipped macroblock stores:

- zero / not-applicable;
- inherited current quantiser scale;
- or some separately flagged derived value.

This should not be left ambiguous.

---

## 13. Quantisation weighting matrices

### 13.1 Quantiser scale is only part of inverse quantisation

**RESEARCHED (S1).**

MPEG-2 inverse quantisation also uses weighting matrices.

The standard's reconstruction arithmetic combines:

- quantised coefficient level;
- weighting matrix element;
- quantiser scale;
- intra/non-intra rules.

### 13.2 4:2:0 matrix selection

**RESEARCHED (S1).**

For 4:2:0, the standard uses:

- one matrix for intra blocks;
- one matrix for non-intra blocks;

for both luma and chroma in that chroma format.

Matrices can be default or downloaded/customised.

### 13.3 Implication for "quantiser means blocking strength"

**HYPOTHESIS.**

Macroblock quantiser scale is a useful coarse proxy for likely quantisation damage, but it is not a complete description of actual coefficient quantisation.

Two macroblocks with the same quantiser scale can differ in effective frequency weighting if different quantisation matrices are active.

### 13.4 Does `.idx2` need matrix information?

**OPEN.**

Probably not per macroblock.

Potential approaches later:

- assume matrix changes are rare and inspect actual target captures;
- store sequence/picture-level matrix identity only if non-default/custom matrices occur;
- ignore matrices if experiment shows little benefit;
- or incorporate a small derived severity scalar if justified.

No decision should be made before inspecting real streams.

---

## 14. Intra, inter, skipped, and coded-block state

### 14.1 `macroblock_intra`

**RESEARCHED (S1).**

The macroblock type syntax indicates whether a macroblock is intra coded.

### 14.2 Skipped macroblocks

**RESEARCHED (S1).**

A skipped macroblock has no coded macroblock data.

In normal non-scalable P/B operation, a skipped macroblock is reconstructed from prediction and has no coded residual DCT coefficients.

The standard states that skipped macroblocks are prediction-only and all DCT coefficients are considered zero.

### 14.3 Filtering implication of skipped status

**HYPOTHESIS.**

Skipped status may be useful for deblocking, but not necessarily in the simplistic sense "skipped means clean".

A skipped macroblock:

- has no newly quantised residual;
- but its prediction may come from previously reconstructed, already quantised reference pictures;
- therefore visible block structure may persist or propagate through prediction.

Thus skipped status is potentially useful context, not proof that no filtering is needed.

### 14.4 `coded_block_pattern`

**RESEARCHED (S1).**

For non-intra blocks, coded-block-pattern information identifies which transform blocks have coded residual data.

For 4:2:0 there are six block positions.

The standard derives `pattern_code[i]` for each block.

For intra macroblocks, block presence semantics differ because intra blocks are intrinsically coded.

### 14.5 Potential value to the deblocker

**HYPOTHESIS.**

A six-bit per-macroblock coded-block mask may be substantially more useful than a simple `is_inter` flag if the algorithm wants to know which individual 8x8 residual blocks were coded.

Possible uses:

- identify boundaries where one residual block is coded and its neighbour is not;
- identify internal 8x8 regions with zero coded residual in inter macroblocks;
- distinguish motion-prediction-only areas from coded residual texture.

### 14.6 But coded-block pattern is not coefficient activity

**RESEARCHED FACT + HYPOTHESIS.**

CBP tells us whether a block has coded residual information, not how much high-frequency energy it contains.

It therefore cannot by itself distinguish:

- one tiny coefficient;
- many strong coefficients;
- smooth low-frequency residual;
- highly textured residual.

A richer coefficient-activity measure might improve filtering decisions, but that requires evidence before expanding `.idx2`.

---

## 15. Coefficient activity as possible metadata

### 15.1 What the decoder knows

**RESEARCHED (S2) + HYPOTHESIS.**

A decoder necessarily parses quantised DCT coefficients and therefore could derive block-level measures such as:

- number of nonzero AC coefficients;
- highest nonzero scan position;
- sum of absolute quantised AC coefficients;
- perhaps low/high-frequency energy summaries.

FFmpeg's block decoder maintains information such as a last nonzero index as part of decoding.

### 15.2 Potential value

**HYPOTHESIS.**

A small activity measure might help distinguish:

- genuinely textured blocks where filtering should be conservative;
- flat/low-activity blocks where visible block steps are more suspicious.

This could be more informative than coding mode alone.

### 15.3 Cost/complexity concern

**HYPOTHESIS.**

Adding coefficient-derived metadata can easily make the index and algorithm overcomplicated.

The first Python experiment should therefore test progressively:

A. pixels only;
B. pixels + quantiser;
C. pixels + quantiser + dct_type;
D. optionally CBP;
E. only then coefficient activity.

If B/C already solve most of the problem, richer metadata should be rejected.

---

## 16. Motion information

### 16.1 MPEG-2 carries rich motion modes

**RESEARCHED (S1).**

Depending on picture structure and macroblock type, MPEG-2 supports:

- frame-based prediction;
- field-based prediction;
- 16x8 prediction in field pictures;
- dual-prime;
- forward/backward/bidirectional prediction.

### 16.2 Is detailed motion metadata needed for deblocking?

**HYPOTHESIS.**

Probably not in the first candidate algorithm.

Motion information may explain why a decoded discontinuity exists, but a post-deblocking filter already has the final pixels.

Detailed vectors would significantly enlarge `.idx2`.

A strong case would be needed before storing them.

### 16.3 Possible minimal use

**HYPOTHESIS.**

Macroblock motion/prediction mode might be useful as a coarse classification if experiments show systematic behavior differences.

But actual vector components should remain out of scope unless evidence demonstrates a clear benefit.

---

## 17. Picture type I/P/B

### 17.1 Syntax fact

**RESEARCHED (S1).**

Pictures are classified as I, P, or B.

### 17.2 Likely filtering value

**HYPOTHESIS.**

Picture type may be useful for diagnostics and perhaps contextual tuning, but it should not automatically control filtering strength.

Blocking is fundamentally local to reconstructed transform/prediction error and quantisation.

An I-picture can be heavily blocked.
A P/B picture can be relatively clean.

Therefore picture type is likely lower-value than:

- actual pixels;
- quantiser;
- dct_type;
- possibly coded-block/activity data.

This should be tested rather than assumed.

---

## 18. What information appears highest-value so far

The following ranking is provisional.

### Tier A - likely essential or very high value

**HYPOTHESIS based on researched mechanics.**

1. Display-record ordinal / frame correspondence.
2. Picture structure.
3. Per-macroblock `dct_type` or an equivalent effective-DCT organisation.
4. Per-macroblock actual quantiser scale.
5. Macroblock coordinates implicit from fixed raster layout.

### Tier B - likely useful, should be tested

1. Intra/inter/skipped state.
2. Coded-block pattern.
3. Picture coding type.
4. Possibly frame_pred_frame_dct as picture-level diagnostic/context.

### Tier C - only if experiments justify

1. Per-block coefficient activity.
2. Prediction mode.
3. Motion type.
4. Motion vectors.
5. Quantisation-matrix identity/derived severity.

This ranking is not a final `.idx2` design.

---

## 19. Important implication for the draft `.idx2`

### 19.1 One byte of flags can still be plausible

**HYPOTHESIS.**

A compact per-macroblock record remains plausible if the first algorithm needs only:

- effective dct_type;
- skipped;
- intra;
- perhaps a few bits of coded/prediction status;
- quantiser scale in another byte.

### 19.2 But CBP does not fit for free

A 4:2:0 coded-block pattern can require six block bits.

If Stage 2 shows CBP materially improves decisions, the two-byte macroblock record may need to grow or be redesigned.

### 19.3 Do not optimise size prematurely

**HYPOTHESIS.**

A two-hour PAL index of several hundred megabytes is not trivial, but it is manageable on modern storage.

Correctness and useful metadata should be established before compressing the format.

A later format can use:

- per-frame headers;
- packed flags;
- optional planes/sections;
- or other compact representation,

only after the algorithm needs are known.

---

## 20. Candidate filtering geometry implied by MPEG-2 mechanics

This section is design inference, not prior-art research.

### 20.1 Progressive/frame-DCT luma candidate geometry

**HYPOTHESIS.**

Test edges at every luma 8x8 transform boundary:

- x multiples of 8;
- y multiples of 8.

Use macroblock metadata for each side to select thresholds/eligibility.

### 20.2 Field-DCT luma candidate geometry

**HYPOTHESIS.**

Treat the two field parities separately for vertical-direction filtering.

Do not simply filter across y=8 using adjacent raster rows.

A field-aware horizontal-boundary operator may need same-parity samples:

for one field:
... y-4, y-2 | y, y+2 ...

and for the other field:
... y-3, y-1 | y+1, y+3 ...

Exact indexing depends on where the transform boundary falls relative to macroblock coordinates.

This must be derived carefully before coding.

### 20.3 Vertical edges in field-DCT macroblocks

**HYPOTHESIS.**

x=8 remains an internal transform separation, but the sample support should preserve field parity vertically when measuring local activity.

### 20.4 4:2:0 chroma geometry

**HYPOTHESIS.**

Filter only at chroma 8x8 block boundaries, corresponding to luma macroblock boundaries.

No chroma equivalent of the internal luma x=8/y=8 seam exists inside a 4:2:0 macroblock.

---

## 21. Candidate edge/blocking decision variables

This is a design hypothesis list for later Stage 0 synthesis.

A simple boundary test could use:

1. decoded pixel step across the transform boundary;
2. local activity/gradient on each side;
3. quantiser scale on the two neighbouring macroblocks;
4. effective DCT organisation;
5. optional intra/inter/skipped classification;
6. optional coded-block pattern.

Possible guiding principle:

> If the boundary discontinuity is large relative to nearby within-block variation and is plausible for the local quantisation scale, treat it as likely blocking; otherwise preserve it as a likely genuine edge.

This is intentionally not a final equation.

Claude's prior-art research should determine whether established algorithms support or contradict this family.

---

## 22. Quantiser-aware thresholding: what is justified now

### 22.1 Research evidence

**RESEARCHED (S6, S7).**

At least some MPEG-2 restoration/deblocking work uses quantisation information as a quality or filtering input.

The Forchhammer paper extracts picture type and macroblock quantisation step size from the MPEG stream to estimate pixel quality.

The MPEG-2 postprocess deblocker patent explicitly describes passing quantiser scale and coding information from the MPEG-2 decoder to the deblocker.

### 22.2 Project implication

**HYPOTHESIS.**

Using the actual decoder-side quantiser scale is not an exotic project invention.

There is precedent for MPEG-2 post-processing using bitstream side information.

However, this does not prove that the proposed project algorithm will outperform pixel-only methods.

---

## 23. Strongest current justification for `.idx2`

### 23.1 Not block positions

**RESEARCHED/HYPOTHESIS.**

The regular macroblock raster and progressive/frame-DCT 8x8 positions are already inferable from pixels.

The index is valuable only for coding state unavailable from decoded pixels.

### 23.2 Strongest candidates

Current strongest candidates are:

- field-DCT versus frame-DCT organisation;
- actual macroblock quantiser scale;
- skipped/intra/inter state;
- possibly coded-block pattern.

### 23.3 Falsification requirement remains active

**HYPOTHESIS.**

If a pixel-only algorithm plus fixed 8x8 geometry performs nearly as well on the real captures, the index may not justify its complexity.

Stage 2 must include an ablation comparison:

- pixels only;
- pixels + selected metadata.

---

## 24. AVX2 suitability

### 24.1 Regular frame-DCT path

**HYPOTHESIS.**

A small-support edge filter across regular 8x8 boundaries is highly suitable for AVX2 because:

- many edges share identical geometry;
- samples can be loaded in vectors;
- threshold and clamp operations vectorise naturally;
- horizontal and vertical passes can be separated.

### 24.2 Field-DCT path

**HYPOTHESIS.**

Field-DCT geometry is still vectorisable but may require:

- strided loads;
- parity-aware row handling;
- separate kernels or dispatch paths.

This increases complexity but does not look prohibitive.

### 24.3 Metadata branching

**HYPOTHESIS.**

Per-macroblock metadata should be converted into simple masks/thresholds before inner pixel loops where possible.

The production AVX2 design should avoid unpredictable per-pixel branching.

### 24.4 Scalar oracle first

The current project decision to implement a scalar/reference algorithm before AVX2 remains well justified.

---

## 25. Python prototype suitability

### 25.1 Mechanics complexity is manageable

**HYPOTHESIS.**

Nothing discovered so far makes a Python Stage 2 prototype conceptually impractical.

The algorithm may be slow, but Python can represent:

- field-parity sample selection;
- boundary masks;
- quantiser-derived thresholds;
- coded-block masks;
- small-support corrections.

### 25.2 Recommended role

Python should remain:

- correctness oracle;
- research platform;
- ablation-test platform.

It should not be judged by production throughput.

NumPy may be considered if convenient, but a simple literal implementation may be preferable initially for auditability.

---

## 26. Stage 1 analyzer fields suggested by this research

The throwaway analyzer should, at minimum, be capable of reporting:

### Picture/frame level

- display-record ordinal;
- coded-order picture ordinal if available;
- temporal_reference;
- I/P/B type;
- picture_structure;
- frame_pred_frame_dct;
- q_scale_type;
- progressive_frame;
- top_field_first;
- repeat_first_field;
- dimensions.

### Macroblock level

- macroblock x/y;
- effective dct_type where meaningful;
- intra/inter/skipped;
- actual derived quantiser scale;
- whether quantiser was explicitly updated at this macroblock;
- coded-block pattern if implemented experimentally;
- motion/prediction mode only if easy to expose.

### Summary statistics

- frame-DCT macroblock count;
- field-DCT macroblock count;
- skipped count;
- intra count;
- quantiser distribution;
- mixed-DCT neighbour count horizontally;
- mixed-DCT neighbour count vertically;
- CBP distribution if available.

These are research diagnostics, not final `.idx2` requirements.

---

## 27. Specific questions to answer with the user's real LG captures

1. How often does field-DCT occur?
2. How often are frame-DCT and field-DCT macroblocks mixed within the same frame?
3. Are mixed-DCT neighbours common or rare?
4. What quantiser-scale distribution occurs in visibly blocky regions?
5. Does quantiser vary sharply across adjacent macroblocks?
6. How many macroblocks are skipped in P/B pictures?
7. Which luma block boundaries are visibly objectionable:
   - internal 8x8;
   - macroblock boundary;
   - both?
8. Is chroma blocking visibly significant?
9. Do blocked areas correlate with CBP/no-CBP transitions?
10. Are custom quantisation matrices used?
11. Are field pictures present, or primarily frame pictures with interlaced content?
12. Does BestSource expose one frame per MPEG-2 display frame in the expected way?
13. Do damaged/discontinuous recordings disturb that mapping?

---

## 28. Source/index correspondence risk

### 28.1 Fundamental issue

**RESEARCHED (S1) + PROJECT FACT.**

The MPEG-2 decoder internally works with coded pictures and reorders output.

BestSource separately exposes decoded VapourSynth frames.

The two must agree on frame sequence for `.idx2` record N to correspond to VapourSynth frame N.

### 28.2 Recommended simple approach

**HYPOTHESIS consistent with D-02.**

Do not add heavy hashing/identity infrastructure.

Use:

- display-record ordinal;
- dimensions;
- total record count;
- perhaps diagnostic temporal_reference / picture type in Stage 1.

User responsibility remains selecting the correct index.

Stage 5 proves correspondence on representative material.

---

## 29. What should probably NOT be frozen yet

Do not yet freeze:

- final per-macroblock record size;
- raw code versus derived quantiser field semantics;
- CBP inclusion;
- coefficient activity inclusion;
- motion mode inclusion;
- exact field-DCT filtering coordinates;
- chroma strength relation to luma;
- picture-type influence;
- source identity scheme;
- final strength scale.

Each depends on Stage 1/2 evidence.

---

## 30. Preliminary conclusions

### C1

**RESEARCHED.**

MPEG-2 4:2:0 macroblocks contain four 8x8 luma blocks and one 8x8 block for each chroma plane.

### C2

**RESEARCHED.**

In frame pictures, luma macroblocks can use frame-DCT or field-DCT organisation at macroblock granularity under MPEG-2 syntax rules.

### C3

**RESEARCHED.**

In 4:2:0, chroma remains frame-organised for DCT even when luma uses field-DCT.

### C4

**RESEARCHED.**

`quantiser_scale_code` must be interpreted through `q_scale_type`; the derived quantiser scale spans different linear/nonlinear mappings and is not equivalent to the raw 5-bit code.

### C5

**RESEARCHED.**

Quantiser scale is not the entire quantisation story because weighting matrices also affect inverse quantisation.

### C6

**RESEARCHED.**

Skipped macroblocks contain no coded residual DCT coefficients, but are reconstructed from prediction.

### C7

**RESEARCHED.**

Coded order and display order differ when B-frames are present.

### C8

**HYPOTHESIS.**

The strongest current reasons to carry `.idx2` metadata are likely:

- correct field/frame-DCT luma geometry;
- actual quantiser scale;
- selected macroblock/block coding state.

### C9

**HYPOTHESIS.**

Detailed motion vectors are unlikely to be justified for the first algorithm.

### C10

**HYPOTHESIS.**

CBP is a stronger candidate for experimental inclusion than detailed motion metadata because it maps directly to the six 4:2:0 transform blocks.

### C11

**HYPOTHESIS.**

A simple metadata-assisted deblocker still appears technically feasible as:

- scalar/Python reference first;
- then C++ scalar;
- then AVX2.

Nothing in the coding mechanics discovered so far invalidates the project concept.

---

## 31. Open questions requiring further work

1. Exact same-parity sample coordinates for filtering horizontal boundaries in field-DCT macroblocks.
2. Boundary treatment when one side is frame-DCT and the other field-DCT.
3. Whether field-DCT macroblocks produce visibly different blocking on the user's material.
4. Whether chroma should use independent thresholds/strength.
5. Whether actual quantiser scale alone is adequate despite weighting matrices.
6. Whether custom matrices occur in the target LG streams.
7. Whether CBP materially improves classification.
8. Whether a cheap coefficient-activity summary materially improves classification.
9. How BestSource treats repeated fields and field pictures for the target MPEG-2 material.
10. Whether temporal_reference is useful enough to include in the draft Stage 1 index/analyzer.
11. Whether display output from the reference decoder exactly matches BestSource frame count/order on damaged streams.
12. Whether generic pixel-only filtering eliminates enough blocking that codec metadata adds little value.

---

## 32. Recommended next mechanics step

Before finalising `06_DEBLOCK_CONCEPT.md`, perform two additional mechanics tasks:

### A. Reference-decoder source inspection

Once Dave supplies the pristine reference decoder source:

- locate macroblock parsing;
- locate effective quantiser state;
- locate dct_type handling;
- locate block placement/reconstruction;
- locate frame output/reordering;
- locate skipped-macroblock handling;
- determine the safest instrumentation points.

This will convert several RESEARCHED standard-level findings into source-specific evidence for the actual inspector.

### B. Cross-review Claude's prior-art research

Compare Claude's algorithm families against the mechanics constraints in this file.

For each candidate algorithm ask:

- Does it assume regular contiguous 8x8 geometry?
- Does it handle field-DCT?
- Does it filter chroma?
- Does it use quantiser side information?
- Does it require coefficient information?
- Can it be adapted without silently becoming an H.264-style in-loop filter?
- Is it still simple enough for the project's one-strength first design?

---

## 33. Provisional research verdict

**HYPOTHESIS based on current evidence.**

The project remains technically plausible.

The mechanics research strengthens, rather than weakens, the case for testing metadata assistance because:

1. field-DCT makes luma transform geometry genuinely different at macroblock level;
2. quantiser scale is authoritative codec-side information unavailable from final pixels;
3. skipped/intra/inter/CBP state can potentially distinguish prediction-only and residual-coded regions;
4. 4:2:0 chroma requires different geometric treatment from luma in field-DCT cases.

At the same time, this research also argues for restraint:

- do not store every decoder variable;
- do not assume quantiser alone predicts artifact strength;
- do not assume picture type needs to alter strength;
- do not include motion vectors without evidence;
- do not freeze the two-byte macroblock record until the Python ablation experiments show which metadata matters.

The best next step remains the agreed one:

> combine this mechanics research with Claude's independent prior-art research, cross-review both, and only then draft the first ratifiable deblocking concept.

---

## 34. Bibliographic / web references

1. ISO/IEC 13818-2:1995 / ITU-T H.262 MPEG-2 Video.
   https://burgerlib.readthedocs.io/en/latest/is138182.pdf

2. ITU-T H.262 hosted result exposing Table 7-6 quantiser mapping.
   https://www.itu.int/rec/dologin_pub.asp?id=T-REC-H.262-199507-S!!PDF-E&lang=s&type=items

3. FFmpeg, `libavcodec/mpeg12dec.c`.
   https://www.ffmpeg.org/doxygen/8.1/mpeg12dec_8c_source.html

4. FFmpeg, current/trunk `libavcodec/mpeg12dec.c`.
   https://ffmpeg.org/doxygen/trunk/mpeg12dec_8c_source.html

5. FFmpeg, `libavcodec/mpegvideodata.c`.
   https://www.ffmpeg.org/doxygen/8.1/mpegvideodata_8c_source.html

6. Linux kernel V4L2 codec control reference, MPEG-2 controls.
   https://www.kernel.org/doc/html/v5.1/media/uapi/v4l/ext-ctrls-codec.html

7. `Chapter 13: MPEG-2`, secondary technical reference.
   https://ez.analog.com/cfs-filesystemfile/__key/communityserver-discussions-components-files/331/2251.video_2D00_demy5.pdf

8. S. Forchhammer,
   `A unified approach to restoration, deinterlacing and resolution enhancement in decoding MPEG-2 video`,
   IEEE Transactions on Circuits and Systems for Video Technology,
   2002.
   https://www.researchgate.net/publication/3308434_Forchhammer_S_A_unified_approach_to_restoration_deinterlacing_and_resolution_enhancement_in_decoding_mpeg-2_video_IEEE_Trans_Circuits_Syst_Video_Technol_129_803-811

9. US7574060B2,
   `Deblocker for postprocess deblocking`.
   https://patents.google.com/patent/US7574060B2/en

---

## 35. End-of-pass limitations

This v0.1 is not exhaustive.

Known limitations:

- the pristine reference decoder source has not yet been inspected;
- Claude's independent prior-art research has not yet been reviewed;
- the user's actual LG streams have not yet been instrumented;
- BestSource frame-output behaviour has not yet been tested against the reference decoder;
- no candidate filter has been implemented;
- no visual or objective deblocking experiment has yet been run;
- no claim here should be promoted to repository truth without the agreed three-way review and Dave's ratification.

