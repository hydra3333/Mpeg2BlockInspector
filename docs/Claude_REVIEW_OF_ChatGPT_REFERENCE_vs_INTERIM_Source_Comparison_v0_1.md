# Claude - Review of ChatGPT Reference vs Interim Source Comparison v0.1

**Filename:** `Claude_REVIEW_OF_ChatGPT_REFERENCE_vs_INTERIM_Source_Comparison_v0_1.md`
**Version:** 0.1
**Date:** 2026-10-06
**Author:** Claude
**Reviews:** `ChatGPT_REFERENCE_vs_INTERIM_Source_Comparison_v0_1.md` (cited as "SC")
**Source examined:** `REFERENCE-mpeg2dec-src.zip` (pristine reference decoder) only.
**Status:** Stage 1 design input. Evidence only; not project authority. Project authority remains
`06_DEBLOCK_CONCEPT.md`, `05_DECISIONS.md` and `02_INDEX_FORMAT_SPEC.md`.

---

## 1. Scope and verdict

I concur with SC.

Limit: only the pristine source was available to me, not `UPDATED-INTERIM-ONLY-src.zip`. I could
therefore check SC's reference-side claims but not its interim-side diff findings (G-01 to G-03,
M-01 to M-04), which I accept as reported.

Reference-side claims confirmed by reading the pristine source:

| SC claim | Pristine source |
|---|---|
| `picture_data()` runs before `frame_reorder()` in `Decode_Picture()` | getpic.c 105-109 |
| dct_type is read only for frame pictures with frame_pred_frame_dct = 0 and macroblock_type containing PATTERN or INTRA; otherwise 0 | getpic.c 388-392 |
| `skipped_macroblock()` decodes no new macroblock_type; it clears INTRA only | getpic.c 849-901 (clear at 896) |
| Logged `ld->quantizer_scale` is the derived scale (q_scale_type mapping) | getpic.c 1046-1050; slice header gethdr.c 341-342 |

Line numbers refer to the pristine files as supplied and may be off by a line or two.

The four points below are additions for the Stage 1 instrumentation design (SC section 9).

---

## 2. Point 1 - Display-order emission point and metadata retention (SC 9 Q1, Q2)

Source facts:

- Picture output happens only through `Write_Frame()`. It is called from `frame_reorder()`
  (getpic.c 754-783) and from `Output_Last_Frame_of_Sequence()` (getpic.c 743-750).
- In `frame_reorder()`, once `Sequence_Framenum != 0` and the picture is a frame picture or a
  second field (getpic.c 762):
  - B picture: writes `auxframe` (the current picture);
  - I or P picture: writes `forward_reference_frame` (the PREVIOUS reference picture).
- `Update_Picture_Buffers()` (getpic.c 696-735) rotates the forward/backward reference pointers at
  the start of each non-B coded frame (not on the second field); B pictures decode into `auxframe`.
- At the end of a sequence, `Output_Last_Frame_of_Sequence()` writes `backward_reference_frame`
  (the last reference picture still held).
- `Write_Frame()` is called regardless of output type; `store_one()` switches on `Output_Type`
  (store.c 61-100).

Design proposal (HYPOTHESIS):

- Hold per-picture metadata in slots that mirror the three frame buffers (forward reference,
  backward reference, B/aux) and rotate them exactly as `Update_Picture_Buffers()` rotates the
  pixel buffers.
- Emit one index record at each `Write_Frame()` call site, taking metadata from the slot that
  corresponds to the buffer being written.
- The record ordinal should be a simple count of emissions, not `Bitstream_Framenum - 1`
  (which happens to equal display index in steady state but is a coded-picture counter).

---

## 3. Point 2 - Correspondence hazards visible in the source (SC 9 Q7; 06 O-08)

1. **Trailing unpaired field is dropped.** `Output_Last_Frame_of_Sequence()` prints "last frame
   incomplete, not stored" and writes nothing when `Second_Field` is set (getpic.c 746-747).
2. **Field pair yields one output.** Output is triggered only for frame pictures or the second
   field (getpic.c 762). The two field pictures of one output frame can differ in picture type and
   quantiser context, so a merge rule for the record is needed (02 section 3 item 1).
3. **Per-sequence counting and flush.** `video_sequence()` (mpeg2dec.c 657-698) resets
   `Sequence_Framenum` and calls `Output_Last_Frame_of_Sequence()` at the end of each sequence.
   Stage 1 should check whether the target captures' repeated sequence headers or any
   sequence_end codes cause extra end-of-sequence flushes, and whether BestSource behaves the same.
4. **Damaged streams.** Invalid VLC codes set `Fault_Flag` (e.g. getvlc.c 522-527) and the slice
   is abandoned. Behaviour relative to BestSource on damaged input must be tested (02 section 3
   item 5).

---

## 4. Point 3 - Edge case in deriving NONE (06 section 4.3; K-07)

Source facts:

- `coded_block_pattern` value 0 is decodable: `CBPtab2[1] = {0,9}`, i.e. the 9-bit code
  `000000001` returns 0 (getvlc.h 250).
- A non-intra macroblock with MACROBLOCK_PATTERN set therefore reads a real dct_type bit
  (getpic.c 388-392) even if its coded_block_pattern is 0, in which case no blocks are coded.

Consequence: K-07's wording ("skipped and no-residual macroblocks carry no dct_type") is not exact
for this case. The meaning of NONE (no current coded residual transform) is unaffected; only its
derivation needs care.

Proposed derivation rule for Stage 1 (HYPOTHESIS):

```text
NONE   if skipped
       or (not intra and effective coded_block_pattern == 0)
FRAME  if coded and dct_type bit read as 0,
       or coded and frame_pred_frame_dct == 1 (genuine frame DCT; bit not transmitted)
FIELD  if coded and dct_type bit read as 1
```

Field pictures: dct_type is also derived as 0, but transform blocks there are field lines. The
Stage 1 format should identify these by picture_structure rather than label them FRAME (06 4.6).

Recommendation: treat this as a clarification of how NONE is derived, recorded in the Stage 1
design; it does not reopen K-07's meaning.

---

## 5. Point 4 - Skipped macroblock fields are inherited, not meaningless (SC G-03 Problem 2)

SC is right that a skipped macroblock's `macroblock_type` is not fresh syntax. In B pictures it is
nevertheless normatively significant: a skipped B macroblock repeats the previous macroblock's
prediction direction (and motion vectors), which is why the decoder carries the value forward.

Suggestion: the Stage 1 analyzer may report skipped-macroblock prediction state as "inherited"
(diagnostic only) rather than discard it, consistent with D-14.

Related: in the pristine decoder a skipped macroblock's `dct_type` is simply stale from the
previous macroblock (the interim code forces 0). Either is operationally harmless because the
residual is zero, and neither may be reported as FRAME/FIELD (Point 3).

---

## 6. Summary for the Stage 1 instrumentation design

1. Emit records at `Write_Frame()` call sites; carry metadata in slots rotated with the frame
   buffers; ordinal = emission count.
2. Define handling for: dropped trailing field, field-pair merge, per-sequence flushes, damaged
   streams.
3. Derive NONE from skipped / (non-intra and cbp == 0); FRAME/FIELD only for coded macroblocks;
   mark field pictures by picture_structure.
4. Report skipped-macroblock prediction state as inherited, diagnostic only.

---

## 7. Change log

### v0.1 - 2026-10-06

- First review of `ChatGPT_REFERENCE_vs_INTERIM_Source_Comparison_v0_1.md` against the pristine
  reference source; four additions for the Stage 1 instrumentation design.
