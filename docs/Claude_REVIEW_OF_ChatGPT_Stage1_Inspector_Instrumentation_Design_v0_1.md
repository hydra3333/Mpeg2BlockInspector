# Claude - Review of Stage 1 Inspector Instrumentation Design v0.1

**Filename:** `Claude_REVIEW_OF_ChatGPT_Stage1_Inspector_Instrumentation_Design_v0_1.md`
**Version:** 0.1
**Date:** 2026-10-06
**Author:** Claude
**Reviews:** `Stage1_Inspector_Instrumentation_Design_v0_1.md` (cited as "S1D", with its section
numbers)
**Source examined:** `REFERENCE-mpeg2dec-src.zip` (pristine; identical to the copy reviewed
earlier). File:line citations refer to that tree and may drift by a line or two.
**Status:** Stage 1 working review. Not project authority.

---

## 1. Verdict

**Approve with corrections.** The design is sound and maps well onto the pristine decoder. The
metadata-slot model, emission at the `Write_Frame()` call sites, emission-count ordinal, NONE
derivation, rename-on-success publication and the early count gate are all supported by the
source.

Corrections needed before coding (details in sections 2 and 3):

1. **Skipped macroblocks carry a stale `macroblock_type`.** Every flag-derived field (QUANT update,
   dct_type-bit-read, coding state, motion direction) must be gated on "not skipped" (Q6, F1).
2. **The damage gate must not rely on `Fault_Flag` alone.** Several recovery paths never pass the
   resync label, and missing slices raise no fault at all. A per-picture macroblock coverage check
   should be the primary gate (Q9, F2).
3. **The matrix "load" flags are unreliable** at picture time; compare the matrix arrays with the
   defaults instead (Q8).
4. **Prediction normalisation should move from C to Python**; store raw values (Q7).
5. **Repeated sequence headers do not start a new sequence**; a mid-sequence size or chroma change is
   not reallocated and must invalidate the run (F3).

No third source/header file is needed (Q10).

---

## 2. Answers to S1D section 36

### Q1 - Does metadata rotation mirror pixel rotation correctly for frame pictures?

**Yes.** `Update_Picture_Buffers()` rotates forward/backward only for non-B pictures and only when
`!Second_Field` (getpic.c 704-723); B pictures always use `auxframe` (getpic.c 704-707). Mirroring
the same condition at the same point in `Decode_Picture()` (called at getpic.c 83) gives the
correct lifetime. At I/P output, `frame_reorder()` writes `forward_reference_frame` after the new
picture has been decoded into `backward_reference_frame` (getpic.c 771), so `forward_meta` then
holds the previous reference, as S1D 3.2 states.

Two notes:

- **progressive_frame:** `frame_reorder()` temporarily swaps the global `progressive_frame` to the
  old reference's value around the I/P `Write_Frame()` (getpic.c 768-773). The record header must
  take `progressive_frame` (and every other picture field) from the slot, never from globals at
  emission time.
- **Sequence start:** frame buffers are freed and re-allocated per sequence
  (mpeg2dec.c 223-230 and `Deinitialize_Sequence()`). `Decode_Picture()` receives
  `sequence_framenum == 0` for the first picture of each sequence, so slot clearing and the
  sequence ordinal can be driven from getpic.c alone.

### Q2 - Any other output paths?

**No other relevant ones.** `Write_Frame()` is called only at getpic.c 749
(`Output_Last_Frame_of_Sequence`), 765 (B) and 771 (delayed I/P). `Display_Second_Field()` is
X11-only under `#ifdef DISPLAY`; the build must not define DISPLAY. `Substitute_Frame_Buffer()`
(Ersatz) alters buffers but does not output. Hook the three call sites in getpic.c rather than
inside `Write_Frame()`, which lives in store.c and would add a third file.

### Q3 - Is the FRAME/FIELD/NONE rule ever wrong for frame pictures?

**Correct for non-scalable MPEG-2 frame pictures.** Intra macroblocks always get the full pattern
(getpic.c 1135-1136), so they can never be NONE. Two guards are needed:

- **Scalability:** `Decode_SNR_Macroblock()` can overwrite `dct_type` (getpic.c 592), and data
  partitioning switches `ld`. Invalidate the run if `Two_Streams` is set or
  `base.scalable_mode != SC_NONE`. (Unlikely in DVD-recorder captures; cheap to guard.)
- **MPEG-1 input:** if `base.MPEG2_Flag == 0`, mark the run unsupported rather than interpret it.

### Q4 - Can effective CBP be captured in getpic.c without behaviour change?

**Yes.** `coded_block_pattern` is a local of `decode_macroblock()` (getpic.c 1013), set at 1103 or
1135 and not returned. Smallest safe change: assign it to a file-static variable immediately after
line 1136. Adding an out-parameter would also work but touches the prototype (getpic.c 64-67) and
the call (getpic.c 225). Neither alters decoding. If `decode_macroblock()` returns early on a
fault, the macroblock must not be marked written (coverage check, F2).

### Q5 - Can "dct_type bit actually read" be determined in getpic.c?

**Yes.** `macroblock_modes()` is in getpic.c, not gethdr.c. In the slice loop, after a successful
`decode_macroblock()` for a non-skipped macroblock, recompute the same condition as getpic.c
388-392:

```text
picture_structure == FRAME_PICTURE
&& !frame_pred_frame_dct
&& (macroblock_type & (MACROBLOCK_PATTERN | MACROBLOCK_INTRA))
```

Never evaluate it for skipped macroblocks (F1).

### Q6 - Can MACROBLOCK_QUANT presence be recorded cleanly?

**Yes, with a gate.** For non-skipped macroblocks, `macroblock_type & MACROBLOCK_QUANT` is fresh
syntax. For skipped macroblocks, `macroblock_type` is the previous macroblock's value with only
INTRA cleared (getpic.c 896), so a stale QUANT flag would be misattributed. Record the update flag
as 0 for skipped macroblocks. Read the effective scale from `base.quantizer_scale` (the loop sets
`ld = &base`, getpic.c 189; the scalability guard in Q3 removes the DP case).

### Q7 - Is skipped prediction normalisation safe enough?

**Not in C. Store raw values and normalise in Python.** Reasons:

- `MC_FRAME` and `MC_16X8` are both 2 (mpeg2dec.h 80-81); the meaning depends on
  `picture_structure`.
- `motion_type` starts at 0 and is read only when a motion flag is set (getpic.c 279, 317-330);
  intra macroblocks without concealment vectors have no meaningful motion type.
- P-picture "No_MC" macroblocks get a derived `MC_FRAME` (getpic.c 1191-1206); skipped macroblocks
  get a derived type (getpic.c 876-886).
- In B pictures a skipped macroblock normatively repeats the previous macroblock's prediction
  direction via the stale `macroblock_type`.

Proposed v1 bytes instead of `prediction_mode`/`prediction_source`:

```text
motion_type_raw    : as held by the decoder after the macroblock (0..3)
motion_dir_bits    : bit0 = forward, bit1 = backward (from macroblock_type)
motion_source      : 0 = none, 1 = coded, 2 = derived (No_MC / skipped), 3 = inherited (skipped B)
```

Same byte count; the analyzer normalises using `picture_structure`. Mistakes are then fixable in
Python without rebuilding the inspector.

### Q8 - Are the matrix load flags reliable at picture time?

**No.** `quant_matrix_extension()` overwrites `load_intra_quantizer_matrix` and
`load_non_intra_quantizer_matrix` (gethdr.c 614, 624). An extension with load = 0 clears the flag
while a custom matrix loaded earlier stays in effect. Instead, at picture capture compare the
arrays directly, which needs no gethdr.c change:

```text
custom_intra       = base.intra_quantizer_matrix     != default_intra_quantizer_matrix (global.h 169)
custom_non_intra   = base.non_intra_quantizer_matrix != all 16
custom_chroma_*    = chroma arrays != their luma counterparts (4:2:0: report only)
```

Rename the header fields from `*_loaded` to `*_custom_in_effect`.

### Q9 - Is the Fault_Flag resync path a sufficient damage gate?

**No.** Recovery paths found:

| Path | Location | Passes resync label? |
|---|---|---|
| Decode fault in a macroblock | getpic.c 198-200 via `goto resync` | Yes |
| Fault on first MBAinc of a slice | getpic.c 964-968 (`start_of_slice`) returns 0 | **No** |
| "Too many macroblocks in picture" | getpic.c 216-219 returns -1 | **No** (no fault) |
| Picture ends early: missing trailing slices | getpic.c 922-928 "Premature end of picture" | **No** (also the path for a non-slice start code) |
| Missing middle slice | slice header jumps MBA (getpic.c 974); skipped positions never visited | **No** (silent) |
| Odd number of field pictures | getpic.c 75-80 | No (field case) |
| Fatal `Error()` | mpeg2dec.c 264-269 `exit(1)` | n/a (process exits) |

`Fault_Flag` is also cleared at getpic.c 166, 199 and 917, so a sticky run-level flag must be set
at the hook points, not read later.

Recommended primary gate: a **per-picture macroblock coverage map**. Each macroblock position must be
written exactly once, and the written count must equal `MBAmax` (getpic.c 124-128) when the
picture completes. This catches every row of the table above (including the silent ones) for
frame pictures. Keep the sticky flag at the resync label and the two `start_of_slice`/too-many paths
as secondary diagnostics.

`Error()` exits directly. The rename-on-success rule (S1D 9.1) already prevents publishing a bad
file; S1D should state that an orphaned `.s1tmp` may remain and must be ignored.

### Q10 - Is a third source/header file needed?

**No**, provided that:

- shared state between mpeg2dec.c and getpic.c (output file handle, `-m` option) is declared with
  local `extern` declarations in those two files, not added to global.h;
- emission hooks sit at the getpic.c call sites, not inside store.c;
- sequence starts are detected in `Decode_Picture()` (Q1);
- matrices and dimensions are read from existing globals (Q8, F3).

`-m` is free: the option parser case-folds (mpeg2dec.c 338) and uses only B, C, E, F, G, I, L, O,
Q, R, T, U, V and X.

---

## 3. Further findings

### F1 - Stale macroblock_type for skipped macroblocks (affects S1D 4.3, 12.1, 13.3, 16)

`skipped_macroblock()` does not decode a type; it clears INTRA only (getpic.c 896). Any field
derived from `macroblock_type` flags for a skipped macroblock is stale. S1D already sets
coding_state = SKIPPED and transform_state = NONE; extend the same gating explicitly to the QUANT
flag, the dct_type-read flag and motion fields (Q7).

### F2 - Coverage check as the primary validity rule (affects S1D 8, 16, 23)

As Q9. Proposed addition to S1D 16: bit 0 "macroblock record valid" is set only when the macroblock
was actually decoded or skipped in that picture; the analyzer already requires all valid (S1D 23
item 12). Add an inspector-side check that the count equals `MBAmax` and no position was written
twice.

### F3 - Sequence boundaries (affects S1D 7)

- `Get_Hdr()` re-parses a repeated sequence header without returning (gethdr.c 103-105); only
  `SEQUENCE_END_CODE` ends a `video_sequence()` (gethdr.c 113-114; mpeg2dec.c 607-622). Repeated
  sequence headers therefore do not flush or restart counting; only sequence_end codes do.
- `mb_width`, `Coded_Picture_Width` and the frame buffers are set once per sequence in
  `Initialize_Sequence()` (mpeg2dec.c 200-230), but each sequence header updates
  `horizontal_size` and friends. A size or chroma change without a sequence_end is therefore not
  reallocated. The inspector should invalidate the run if, at `Decode_Picture()`,
  `(horizontal_size+15)/16 != mb_width`, the vertical equivalent differs, or `chroma_format`
  differs from the value captured at sequence start.

### F4 - Leading pictures after a sequence_end (HYPOTHESIS; affects S1D 10)

After a sequence_end, the next sequence starts with fresh, unfilled reference buffers. If it opens
with leading B pictures (open GOP), the reference decoder still outputs them, while FFmpeg-based
decoders may handle them differently. If the count gate (S1D 10) fails on a sample, check for
sequence_end codes and leading B pictures first.

### F5 - Picture-level capture point is safe (S1D 4.1)

`picture_header()` parses all picture extensions via `extension_and_user_data()` before returning
(gethdr.c 312-314), so every picture-level field is set by the time `Decode_Picture()` runs.

---

## 4. Proposed edits to S1D

1. S1D 4.3 / 13.3 / 16: gate QUANT, dct_type-read and motion fields on non-skipped (F1, Q6).
2. S1D 8: replace "Fault_Flag resync" as the gate with the coverage check plus sticky flags at the
   three recovery sites (Q9, F2); mention orphaned `.s1tmp`.
3. S1D 7: state that only sequence_end restarts a sequence; add the dimension/chroma consistency
   invalidation (F3).
4. S1D 15 / 17 / 29: replace prediction normalisation with raw motion bytes; normalise in Python
   (Q7).
5. S1D 18.1 / 30: rename matrix flags to `*_custom_in_effect`, derived by array comparison (Q8).
6. S1D 3 or 18: take every header field, including `progressive_frame`, from the slot (Q1).
7. S1D 12 / 19.2: add run invalidation for scalable streams and MPEG-1 input (Q3).
8. S1D 21: record the Q10 conditions that keep the patch to two files.

---

## 5. Change log

### v0.1 - 2026-10-06

- Source review of `Stage1_Inspector_Instrumentation_Design_v0_1.md` against the pristine
  reference decoder: answers to the ten questions, five further findings, eight proposed edits.
