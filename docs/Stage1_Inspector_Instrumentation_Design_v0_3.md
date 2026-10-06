# Stage 1 Inspector Instrumentation Design

**Filename:** `Stage1_Inspector_Instrumentation_Design_v0_3.md`
**Version:** 0.3
**Date:** 2026-10-06
**Drafted by:** ChatGPT
**Status:** WORKING STAGE 1 DESIGN - REVISED AFTER CLAUDE SOURCE REVIEW; PENDING DAVE APPROVAL. No C source changes are authorised by this document.
**Purpose:** Define the throwaway Stage 1 MPEG-2 inspector metadata flow, temporary binary
record semantics, and Python analyzer contract before making a minimal instrumentation patch to
the pristine reference decoder.

---

## 0. Authority, inputs and limits

### 0.1 Project authority

Normal project authority remains:

- `05_DECISIONS.md`
- `06_DEBLOCK_CONCEPT.md`
- `02_INDEX_FORMAT_SPEC.md`

This Stage 1 document is a working task/design document, not a fourth repository knowledge
document.

Where this document conflicts with those repository documents, the repository documents prevail.

### 0.2 Evidence/design inputs used

This draft uses:

- the pristine `REFERENCE-mpeg2dec-src.zip`;
- `ChatGPT_REFERENCE_vs_INTERIM_Source_Comparison_v0_2.md` ("SC");
- `Claude_REVIEW_OF_ChatGPT_REFERENCE_vs_INTERIM_Source_Comparison_v0_1.md`;
- `Claude_REVIEW_OF_ChatGPT_Stage1_Inspector_Instrumentation_Design_v0_1.md` ("S1R");
- the current repository documents listed above;
- Dave's K-07 clarification made after the repository draft:
  FRAME/FIELD/NONE describes applicable coded residual transform geometry, not merely the
  presence or value of `dct_type`.

### 0.3 Labels

- **SOURCE FACT** - directly observed in the pristine reference decoder or ratified repository
  knowledge.
- **DECIDED** - already ratified in project authority.
- **PROPOSED** - Stage 1 design choice in this document; requires review/acceptance before coding.
- **OPEN** - intentionally unresolved.
- **DEFERRED** - deliberately not implemented in the first Stage 1 pass unless evidence requires it.

### 0.4 Scope

This document designs three things together:

**A. Metadata flow**
- picture metadata lifetime;
- I/P/B reordering;
- output-emission ordinal;
- field-picture handling;
- sequence flush/restart behaviour;
- damaged-stream policy.

**B. Record semantics and temporary format**
- per-output-frame fields;
- per-macroblock fields;
- FRAME/FIELD/NONE derivation;
- temporary binary representation.

**C. Python analyzer contract**
- structural validation;
- summaries and distributions;
- early correspondence checks;
- evidence needed for later Stage 2 work.

Only after A-C are reviewed will the pristine C source be patched.

---

# Part A - Metadata flow

## 1. Core invariant

**DECIDED / SOURCE FACT**

The project invariant remains:

> temporary index record N must describe the decoder output frame that is intended ultimately to
> correspond to VapourSynth frame N.

The original/interim logger cannot establish this because it logs picture information while the
picture is being decoded, before MPEG-2 reference-picture reordering is applied.

The Stage 1 temporary index therefore uses an independent **output-emission ordinal**:

```text
0, 1, 2, 3, ...
```

It does not use `Bitstream_Framenum`, `Sequence_Framenum`, or `temporal_reference` as the record
identity.

Those values may be retained only as diagnostics.

---

## 2. Reference-decoder output behaviour

### 2.1 Source facts

The pristine decoder does the following:

1. `Decode_Picture()` calls `Update_Picture_Buffers()`.
2. The current picture is decoded by `picture_data()`.
3. `frame_reorder()` decides which decoded frame buffer is output.
4. Actual frame output occurs through `Write_Frame()`.

For frame pictures:

- a B picture is decoded into `auxframe` and output from `auxframe`;
- an I/P picture is decoded into `backward_reference_frame`;
- when an I/P picture is decoded, the previous reference picture has become
  `forward_reference_frame` and is the one output;
- the final delayed reference picture is output by `Output_Last_Frame_of_Sequence()`.

Therefore metadata must follow the same lifetime and rotation as the frame pixels.

---

## 3. Metadata-slot model

### 3.1 Proposed slots

**PROPOSED**

Maintain three metadata slots mirroring the decoder's three logical frame-buffer roles:

```text
forward_meta
backward_meta
aux_meta
```

Each slot describes the decoded picture/frame currently carried by the corresponding pixel buffer:

```text
forward_meta   <-> forward_reference_frame
backward_meta  <-> backward_reference_frame
aux_meta       <-> auxframe
```

Every picture-level field later written to the record header is captured into the slot while that
picture is current. At emission time, record fields are taken from the slot, not from decoder
globals. This is required because `frame_reorder()` temporarily swaps at least
`progressive_frame` while outputting a delayed reference picture.

The slots are logical objects. Implementation may use pointers to slot structures so that slot
rotation is a pointer swap rather than a bulk copy.

### 3.2 Slot lifetime for frame pictures

**PROPOSED**

For a B frame picture:

```text
current pixels    = auxframe
current metadata  = aux_meta
```

Before decoding the B picture:

- clear `aux_meta`;
- capture all picture-level and macroblock-level data into `aux_meta`.

At output:

```text
Write_Frame(auxframe, ...)
emit_record(aux_meta)
```

The exact order of those two calls is not significant for correspondence provided both use the
same output event and failures are handled consistently.

For an I/P frame picture at the beginning of a coded frame:

```text
pixel rotation:
    tmp = forward_reference_frame
    forward_reference_frame = backward_reference_frame
    backward_reference_frame = tmp
```

Mirror it exactly:

```text
metadata rotation:
    tmp_meta = forward_meta
    forward_meta = backward_meta
    backward_meta = tmp_meta
```

Then:

- clear `backward_meta`;
- decode the new I/P picture into `backward_reference_frame`;
- capture its metadata into `backward_meta`;
- when `frame_reorder()` outputs `forward_reference_frame`, emit `forward_meta`.

At sequence end:

```text
Write_Frame(backward_reference_frame, ...)
emit_record(backward_meta)
```

### 3.3 First reference picture

The first I/P reference picture of a sequence is decoded and retained but not immediately
output.

Its metadata remains in `backward_meta`.

When the next reference picture is decoded, both the pixel-buffer and metadata rotations move the
first picture into the forward slot, from which it is emitted.

This mirrors the reference decoder's existing reorder mechanism rather than constructing a second
independent reorder algorithm.

---

## 4. Metadata capture point

### 4.1 Picture-level data

**PROPOSED**

Picture-level fields are copied into the current metadata slot at the start of processing the
picture, after the relevant MPEG-2 headers/extensions have been parsed and before macroblocks are
accumulated.

The pristine decoder has completed picture-header extension parsing before `Decode_Picture()` is
entered, so the picture fields used by this design are available at that point.

All record-header fields, including `progressive_frame`, are later emitted from the metadata slot.
Do not reread picture globals at delayed output time.

Fields are listed in Part B.

### 4.2 Macroblock-level data

**PROPOSED**

Macroblock metadata is captured in the existing macroblock decode loop only after sufficient
syntax has been decoded to determine its final Stage 1 semantics.

In particular, transform state must **not** be recorded merely when `dct_type` is read.

It is recorded only after the effective coded-block pattern is known, because a non-intra
macroblock can read a real `dct_type` bit and still have an effective coded block pattern of zero.

Each macroblock position also participates in the per-picture coverage check defined in section 8.

### 4.3 Skipped macroblocks and stale `macroblock_type`

**SOURCE FACT / PROPOSED HANDLING**

`skipped_macroblock()` decodes no fresh `macroblock_type`; the decoder carries the previous
macroblock's value forward with only the INTRA flag cleared.

Therefore **every field normally derived from `macroblock_type` flags must be gated on
"not skipped"**.

A skipped macroblock receives:

```text
coding_state      = SKIPPED
transform_state   = NONE
macroblock_quant_update = 0
dct_type_bit_read = 0
```

Its current/effective quantiser scale may be recorded, but it is explicitly an inherited decoder
state, not a quantiser value coded by the skipped macroblock.

Prediction diagnostics for skipped macroblocks are populated only through the explicit skipped
prediction path described in section 15; they must never be obtained by pretending the stale
`macroblock_type` is fresh syntax.

For B-picture skipped macroblocks, inherited prediction direction can be semantically meaningful,
but it must be labelled as inherited rather than coded for the current macroblock.

## 5. Output-emission event

### 5.1 Proposed rule

**PROPOSED**

One temporary record is emitted only when the reference decoder logically emits one completed
output frame.

For the initial frame-picture implementation, instrument the same branches that call
`Write_Frame()`:

```text
B picture output:
    pixel buffer     = auxframe
    metadata slot    = aux_meta

delayed I/P output:
    pixel buffer     = forward_reference_frame
    metadata slot    = forward_meta

end-of-sequence delayed output:
    pixel buffer     = backward_reference_frame
    metadata slot    = backward_meta
```

### 5.2 Ordinal

Maintain one file-wide 64-bit output ordinal:

```text
output_ordinal = 0
```

Increment only after a record is successfully emitted.

Do not reset it at a new MPEG sequence.

### 5.3 Diagnostic coded identities

The metadata slot may retain:

- bitstream frame number supplied to `Decode_Picture()`;
- sequence frame number supplied to `Decode_Picture()`;
- `temporal_reference`;
- sequence ordinal.

These are diagnostics only.

They are never the primary record key.

---

## 6. Field pictures

### 6.1 Known source behaviour

**SOURCE FACT**

For field pictures:

- `picture_data()` decodes half the normal frame macroblock count;
- the second field does not rotate the I/P reference buffers again;
- frame output occurs only once a frame picture is complete;
- an incomplete final field can be dropped by `Output_Last_Frame_of_Sequence()`.

The two field pictures contributing to one output frame can carry separate coding context.

### 6.2 Design principle

**PROPOSED**

Field pairing belongs in the same metadata-slot mechanism used for frame reordering.

The first field begins/initialises the metadata slot.

The second field completes/merges into that same slot.

Only the completed output frame may produce one temporary index record.

No "one record per coded field" mode is allowed because it would violate the record-N/output-frame
invariant.

### 6.3 Exact merge semantics

**DEFERRED CONDITIONALLY**

The exact macroblock merge rule for top/bottom field pictures is not required for the first code
pass **if and only if both supplied test samples contain zero field pictures**.

The first Stage 1 implementation must therefore detect and count field pictures.

If none are seen:

- frame-picture instrumentation may proceed;
- exact field-pair merge implementation remains deferred.

If one or more are seen:

- the run is not accepted as a valid Stage 1 index run;
- the tool reports the field-picture count;
- the output index is rejected/removed;
- field-pair merge semantics must be designed and implemented before analyzer work proceeds on that
  material.

### 6.4 Fail-safe rule

The first implementation must never silently treat a field picture as an ordinary FRAME
transform picture merely because the decoder's operational `dct_type` value is zero.

---

## 7. Sequence boundaries and repeated sequence headers

### 7.1 What starts a new decoder sequence

**SOURCE FACT / PROPOSED**

A repeated MPEG sequence header does **not** by itself restart the reference decoder's
`video_sequence()`.

Only a `SEQUENCE_END_CODE` ends the current sequence and causes the next decoder sequence to start.

Maintain a file-wide `sequence_ordinal` beginning at zero and increment it only when the decoder
begins a new `video_sequence()` after a true sequence end.

`sequence_framenum == 0` at `Decode_Picture()` is a suitable indicator of the first picture of a
new decoder sequence; a repeated sequence header within the same sequence does not reset it.

Record `sequence_ordinal` in every output-frame header.

### 7.2 Output ordinal continuity

The output-emission ordinal does not reset at a sequence boundary.

### 7.3 Metadata slots

After the reference decoder has flushed the final delayed frame of a true sequence:

- all three metadata slots are cleared;
- sequence-start geometry/chroma state is refreshed for the next decoder sequence;
- the file writer remains open;
- output ordinal remains continuous.

### 7.4 Mid-sequence dimension or chroma changes

**SOURCE FACT / PROPOSED HARD FAILURE**

The reference decoder allocates picture buffers and macroblock geometry once per decoder sequence.
A repeated sequence header can update `horizontal_size`, vertical size or `chroma_format` without
causing buffer reallocation.

Therefore, at each `Decode_Picture()` call, the inspector compares current header-derived geometry
against the geometry captured when the current decoder sequence began.

At minimum invalidate the run if:

```text
(horizontal_size + 15) / 16 != allocated/captured mb_width
(vertical-size-derived mb_height) != allocated/captured mb_height
current chroma_format != sequence-start chroma_format
```

A mid-sequence geometry/chroma change must not be represented as merely another per-record
dimension change, because the reference decoder itself has not reallocated consistently for it.

### 7.5 Per-record geometry fields

For valid streams, the temporary record header still stores coded dimensions, macroblock
dimensions and chroma format per output record.

The analyzer reports any change, but the inspector invalidates changes that conflict with the
allocated sequence geometry as described above.

## 8. Damaged-stream and macroblock-coverage handling

### 8.1 Principle

**PROPOSED**

Plausible-looking metadata from a decoder recovery path is more dangerous than a clear failure.

`Fault_Flag` alone is not a sufficient validity gate. The pristine decoder has error/recovery
paths that do not pass the ordinary resynchronisation label, and a missing slice can leave
macroblock positions completely unvisited without raising `Fault_Flag`.

The primary Stage 1 validity rule is therefore **complete, exactly-once macroblock coverage** for
each accepted frame picture.

### 8.2 Per-picture coverage map

**PROPOSED PRIMARY GATE**

At the start of each frame picture:

- clear the current metadata slot's macroblock-valid bits;
- set `coverage_count = 0`.

Whenever one macroblock position is successfully represented, including an explicitly skipped
macroblock:

1. compute its raster macroblock position;
2. require that position's valid bit is currently zero;
3. write the macroblock metadata;
4. set the valid bit;
5. increment `coverage_count`.

If a position would be written twice, invalidate the run immediately.

When the picture completes, require:

```text
coverage_count == MBAmax
every expected macroblock position valid exactly once
```

This catches, for frame pictures:

- macroblock decode faults;
- faults on the first MBA increment of a slice;
- too many macroblocks;
- prematurely ended pictures;
- missing trailing slices;
- missing middle slices that jump over macroblock positions.

A picture that fails coverage is never eligible for publication as a valid Stage 1 record.

### 8.3 Secondary sticky recovery diagnostics

In addition to coverage, maintain sticky run/picture diagnostics at known recovery/error paths,
including:

- ordinary macroblock `goto resync`;
- `start_of_slice()` failure on the first MBA increment;
- "too many macroblocks in picture";
- premature picture end;
- any other source-review-confirmed recovery path encountered during implementation.

These are secondary diagnostics. They do not replace the coverage gate.

### 8.4 Fatal errors and orphaned `.s1tmp`

The reference decoder's fatal `Error()` path can exit the process directly.

The rename-on-success publication policy still protects the requested output name, but an orphaned
`.s1tmp` file may remain after a fatal process exit.

Such an orphan is **never** a valid Stage 1 index and must be ignored/deleted.

### 8.5 No invented repair

Stage 1 instrumentation must not invent missing macroblock metadata or guess values for uncovered
regions merely to complete a record.

## 9. Temporary-file publication policy

### 9.1 Proposed safe-write behaviour

**PROPOSED**

Write to a temporary sibling file, for example:

```text
requested_name.s1tmp
```

Only after a clean decode and successful file finalisation is it renamed to the requested
temporary-index filename.

On:

- unsupported field pictures in the first implementation;
- damaged/resynchronised input;
- incomplete metadata record;
- write failure;
- internal consistency failure;

the temporary file is closed and removed, and the program exits non-zero.

### 9.2 Diagnostics

All **new Stage 1 instrumentation diagnostics** go to `stderr`.

Binary metadata is written only to the explicit metadata file.

The reference decoder's historical stdout behaviour is not used as the index channel.

---

## 10. Early correspondence gate

### 10.1 Required samples

The first acceptance run uses both supplied program-stream samples:

```text
TEST_4A_A003.mpg
TEST_4A_A003_blocky.mpg
```

The existing ffmpeg elementary-video pipeline remains the expected input path.

### 10.2 Cheap first check

**PROPOSED ACCEPTANCE GATE**

Before analyzer results are trusted for either sample:

```text
inspector emitted record count == BestSource VapourSynth frame count
```

The comparison is performed independently for both samples.

This is deliberately not the full Stage 5 correspondence proof.

It is a cheap early detector for:

- wrong reorder handling;
- extra/missing sequence flush output;
- accidental field-record emission;
- dropped/duplicated output events.

### 10.3 Failure rule

A count mismatch stops Stage 1 analyzer interpretation for that sample until explained.

Do not continue on the assumption that an off-by-one or other difference is harmless.

If a mismatch occurs, the first diagnostic check should be for `SEQUENCE_END_CODE` boundaries followed by leading B pictures/open-GOP behaviour. The pristine reference decoder can output such leading B pictures from fresh reference buffers differently from an FFmpeg-based decoder. This is a diagnostic hypothesis, not permission to accept a mismatch.

---

# Part B - Record semantics and temporary format

## 11. Design goals for the temporary format

The Stage 1 format is deliberately:

- binary;
- versioned;
- little-endian;
- fixed-width at the field level;
- easy to write from C;
- easy to parse from Python;
- intentionally wasteful compared with a production index;
- disposable.

It is **not** the final `.idx2`.

No Stage 1 packing decision becomes a Stage 3 format decision merely because it works here.

---

## 12. Stage 1 macroblock semantics

### 12.1 Supported stream guard

**PROPOSED HARD REQUIREMENT**

Temporary format v1 accepts only ordinary non-scalable MPEG-2 video.

Invalidate the run if any of the following is true:

```text
base.MPEG2_Flag == 0
Two_Streams != 0
base.scalable_mode != SC_NONE
```

MPEG-1 and scalable/data-partitioned MPEG-2 are outside this Stage 1 v1 semantics.

### 12.2 Coding state

**PROPOSED**

One normalized byte:

```text
0 = UNKNOWN / INVALID
1 = SKIPPED
2 = INTRA
3 = INTER
```

The analyzer must reject UNKNOWN/INVALID in a supposedly valid record.

For skipped macroblocks, coding state is set from the skip path itself, never from the stale
`macroblock_type`.

### 12.3 Transform state

**PROPOSED, aligned with clarified K-07**

For frame pictures:

```text
0 = NONE
1 = FRAME
2 = FIELD
```

`NONE` means:

> no applicable coded residual transform geometry exists for this macroblock.

It does **not** mean:

- no visible blocking can exist;
- no `dct_type` bit was necessarily read;
- the macroblock should automatically be excluded from later deblocking.

### 12.4 Transform-state derivation for frame pictures

The Stage 1 semantic rule is:

```text
if skipped:
    NONE

else if non-intra and effective coded_block_pattern == 0:
    NONE

else:
    coded residual transform exists

    if frame_pred_frame_dct == 1:
        FRAME

    else:
        dct_type == 0 -> FRAME
        dct_type == 1 -> FIELD
```

This deliberately distinguishes:

```text
syntax bit presence
```

from:

```text
applicable residual-transform geometry
```

For non-skipped macroblocks, the diagnostic "dct_type syntax bit read" flag is determined from the
same syntax-presence condition used by the pristine decoder. It is always zero for skipped
macroblocks.

### 12.5 Field pictures

Initial Stage 1 format version 1 does not publish valid macroblock transform-state records for field
pictures.

Field-picture presence is detected as described in Part A.

A future Stage 1 format revision may extend this after field-pair semantics are designed.

## 13. Quantiser semantics

### 13.1 Effective derived scale

**SOURCE FACT / DECIDED DIRECTION**

With the scalable/data-partitioned paths rejected by section 12.1, the current effective MPEG-2
quantiser scale is taken from `base.quantizer_scale`.

It is already the derived scale after `q_scale_type` mapping.

Store it as one unsigned byte:

```text
effective_quantiser_scale
```

Expected MPEG-2 values fit in one byte.

### 13.2 Ownership

The stored value means:

> decoder's effective/current derived quantiser scale at this macroblock position.

It does not mean:

> a quantiser value was explicitly coded in this macroblock.

For skipped macroblocks the value is inherited/current decoder state.

### 13.3 Macroblock quantiser-update flag

Store one byte:

```text
0 = no fresh MACROBLOCK_QUANT update in this macroblock
1 = non-skipped macroblock carried MACROBLOCK_QUANT and updated the scale
```

**Critical gate:** inspect `macroblock_type & MACROBLOCK_QUANT` only for a non-skipped macroblock.

A skipped macroblock always stores:

```text
macroblock_quant_update = 0
```

because its `macroblock_type` is stale.

A slice-header quantiser update is not falsely attributed to a macroblock by this flag.

### 13.4 Raw 5-bit code

**DEFERRED**

Do not modify `gethdr.c` merely to preserve raw `quantiser_scale_code` in the first pass.

The first analyzer needs the derived scale.

If later evidence shows raw code is useful, add it deliberately.

This helps preserve the two-C-file minimal patch target.

## 14. Effective coded-block pattern

### 14.1 Need

The inspector must know the effective coded-block pattern in order to derive NONE correctly.

### 14.2 Temporary storage

**PROPOSED**

For the Stage 1 4:2:0 target material, store the effective coded-block pattern in one byte:

```text
effective_cbp
```

For 4:2:0 the six residual-block bits fit in one byte.

This is diagnostic Stage 1 storage, not a decision to include CBP in final `.idx2`.

### 14.3 Chroma-format guard

Temporary format v1 is accepted for analyzer use only when:

```text
chroma_format == CHROMA420
```

If a different chroma format is encountered:

- report it;
- invalidate the Stage 1 run;
- do not silently truncate a wider CBP.

This does not alter the broader repository knowledge; it limits only the first throwaway evidence
tool to the current target material.

---

## 15. Prediction diagnostic

### 15.1 Status

Per D-14, prediction type is diagnostic only.

Claude's source review shows that normalising prediction modes in C would discard important
context:

- the same numeric `motion_type` value has different meanings in frame and field pictures;
- some values are coded while others are derived by the decoder;
- skipped B pictures inherit prediction direction from the previous macroblock.

Therefore Stage 1 stores raw/near-raw diagnostic values and normalises them in Python.

### 15.2 Temporary v1 motion bytes

Store three bytes:

```text
motion_type_raw
motion_dir_bits
motion_source
```

`motion_type_raw`:

> decoder's raw/derived motion-type value after the macroblock path, range 0..3.

`motion_dir_bits`:

```text
bit 0 = forward prediction direction
bit 1 = backward prediction direction
bits 2-7 = zero
```

`motion_source`:

```text
0 = NONE / NOT APPLICABLE
1 = CURRENT MACROBLOCK CODED / DIRECT CURRENT-MB SYNTAX
2 = DERIVED BY DECODER FOR CURRENT MB
3 = INHERITED FOR SKIPPED B MACROBLOCK
```

### 15.3 Stale-flag gate

The normal non-skipped extraction path may read motion-direction flags from `macroblock_type`.

The skipped path must **not** reuse that normal extraction as if the flags were fresh.

For skipped macroblocks:

- P-picture prediction diagnostics are populated only from the decoder's explicit skipped/No-MC
  derivation and marked `DERIVED`;
- B-picture inherited direction may be preserved, but only through an explicit skipped-B path and
  marked `INHERITED`;
- if the implementation cannot distinguish one of these safely, store NONE/0 rather than guess.

### 15.4 Python owns semantic names

The analyzer combines:

```text
picture_structure
motion_type_raw
motion_dir_bits
motion_source
coding_state
```

to produce readable prediction-mode labels.

If the normalisation logic later needs correction, the C inspector does not need rebuilding.

## 16. Per-macroblock flags and coverage bits

One byte is reserved for Stage 1 validity/diagnostic flags.

Proposed bits:

```text
bit 0 = macroblock position written/valid for this picture
bit 1 = quantiser inherited/current rather than updated by MACROBLOCK_QUANT
bit 2 = prediction state derived or inherited
bit 3 = dct_type syntax bit was actually read
bits 4-7 = reserved, must be zero
```

Bit 0 is also the per-picture coverage map:

- it starts zero for every macroblock position;
- writing a position whose bit is already one is a duplicate-coverage failure;
- picture completion requires all expected positions to be one.

The `dct_type syntax bit read` flag is diagnostic evidence for the K-07 edge case.

For skipped macroblocks:

```text
macroblock_quant_update = 0
dct_type syntax bit read = 0
```

Any motion/prediction flag interpretation follows the explicit skipped path in section 15 rather
than the stale `macroblock_type`.

## 17. Per-macroblock temporary payload

**PROPOSED**

Eight bytes per macroblock:

```text
offset  size  field
------  ----  --------------------------------
0       1     transform_state
1       1     coding_state
2       1     effective_quantiser_scale
3       1     macroblock_quant_update
4       1     effective_cbp
5       1     motion_type_raw
6       1     motion_dir_bits
7       1     packed diagnostic byte
```

To preserve the eight-byte target, byte 7 is packed as:

```text
bits 0-1 = motion_source
bit  2   = macroblock position written/valid
bit  3   = quantiser inherited/current
bit  4   = prediction state derived/inherited
bit  5   = dct_type syntax bit actually read
bits 6-7 = reserved, zero
```

The exact bit positions are Stage 1 temporary-format details, not final `.idx2` decisions.

For PAL 720x576 frame pictures:

```text
45 x 36 = 1620 macroblocks
1620 x 8 = 12,960 bytes of MB metadata per frame
```

This is intentionally larger than the eventual production index.

For a two-hour 25 fps recording, the rough payload alone would be about 2.3 GiB.

That is acceptable only as throwaway research tooling on short samples and selected evidence
clips.

It is **not** acceptable as the final index format and is not proposed as one.

## 18. Per-output-record header

### 18.1 Proposed fixed-width header

Use a 64-byte little-endian record header.

Every picture-derived field below is copied from the matching metadata slot, never reread from
decoder globals at delayed output time.

Fields:

```text
offset  size  field
------  ----  ---------------------------------------------------
0       4     record_magic = "FRM1"
4       4     record_size_bytes, including header + MB payload
8       8     output_ordinal
16      4     sequence_ordinal
20      4     source_bitstream_framenum (diagnostic)
24      4     source_sequence_framenum  (diagnostic)
28      2     temporal_reference
30      1     picture_coding_type
31      1     picture_structure
32      2     coded_width
34      2     coded_height
36      2     mb_width
38      2     mb_height
40      4     mb_count
44      1     progressive_frame
45      1     top_field_first
46      1     repeat_first_field
47      1     frame_pred_frame_dct
48      1     q_scale_type
49      1     chroma_format
50      1     custom_intra_matrix_in_effect
51      1     custom_non_intra_matrix_in_effect
52      1     chroma_intra_matrix_differs_from_luma
53      1     chroma_non_intra_matrix_differs_from_luma
54      2     record_flags
56      8     reserved, must be zero
```

### 18.2 Matrix-status derivation

Do **not** use the decoder's `load_*_quantizer_matrix` flags as persistent "custom matrix in
effect" indicators; a later quantiser-matrix extension can clear those flags while leaving an
earlier custom matrix active.

At picture capture:

```text
custom_intra_matrix_in_effect
    = base.intra_quantizer_matrix differs from default_intra_quantizer_matrix

custom_non_intra_matrix_in_effect
    = base.non_intra_quantizer_matrix differs from the default all-16 matrix

chroma_intra_matrix_differs_from_luma
    = chroma intra matrix differs from current luma intra matrix

chroma_non_intra_matrix_differs_from_luma
    = chroma non-intra matrix differs from current luma non-intra matrix
```

For the Stage 1 4:2:0 target, the chroma comparison fields are diagnostic only.

### 18.3 Record flags

Proposed:

```text
bit 0 = record complete
bit 1 = per-picture macroblock coverage verified exactly once
bit 2 = no secondary recovery/fault diagnostic observed
bits 3-15 = reserved
```

A valid published Stage 1 file requires all three bits for every record.

### 18.4 Why dimensions are per record

Keeping dimensions and macroblock geometry per record makes valid sequence-to-sequence changes
visible to the analyzer.

A conflicting change inside one decoder sequence is rejected earlier under section 7.4 rather than
merely reported.

## 19. File header

### 19.1 Proposed 32-byte header

```text
offset  size  field
------  ----  ----------------------------------------------
0       8     magic = "S1MBIDX1"
8       2     format_version = 1
10      2     file_header_size = 32
12      4     endian_marker = 0x01020304
16      8     final_record_count
24      4     file_flags
28      4     reserved, must be zero
```

### 19.2 File flags

```text
bit 0 = file complete / cleanly finalized
bit 1 = field pictures encountered
bit 2 = recovery/fault diagnostic encountered
bit 3 = unsupported chroma format encountered
bit 4 = macroblock coverage failure encountered
bit 5 = unsupported MPEG-1 encountered
bit 6 = unsupported scalable/two-stream MPEG-2 encountered
bit 7 = invalid mid-sequence geometry/chroma change encountered
bits 8-31 = reserved
```

A successfully published v1 file must have:

```text
complete = 1
all unsupported/error flags = 0
```

In normal failure cases the requested final index is not published at all; these flags primarily
define the temporary/run state and protect against accidental analysis of an invalid file.

### 19.3 Final record count

The file writer patches `final_record_count` when closing cleanly.

The analyzer also independently counts records from the file and requires the two counts to match.

## 20. Temporary CLI contract

### 20.1 Proposed new option

Claude's pristine-source review confirms that `-m` is currently unused by the reference decoder option parser.

Use:

```text
-m <metadata-output-file>
```

Example intended pipeline:

```text
ffmpeg -v error -i "TEST_4A_A003.mpg" -c:v copy -an -f mpeg2video - |
Mpeg2BlockInspector -b - -m "TEST_4A_A003.stage1.idx"
```

The exact executable path is environment-specific.

### 20.2 Standard-input support

Preserve the useful interim concept:

```text
-b -
```

means read the MPEG video elementary stream from stdin.

On Windows stdin must be placed in binary mode.

The pipe is treated as an MPEG video elementary stream; no seek-based stream-type sniffing is
attempted.

### 20.3 Metadata filename required

For the Stage 1 instrumented build, `-m` should be required for an evidence run.

If omitted, either:

- operate as the pristine decoder with no Stage 1 output; or
- fail with usage text in a dedicated inspector build.

The coding review may choose the less invasive behaviour.

---

## 21. Expected source-change footprint

### 21.1 Two-file implementation is feasible

**PROPOSED / SOURCE-REVIEW CONFIRMED**

The first implementation should modify only:

```text
getpic.c
mpeg2dec.c
```

Claude's source review found no requirement for a third source/header file.

Conditions for keeping the patch to those two files:

- shared Stage 1 state between `mpeg2dec.c` and `getpic.c` uses local `extern` declarations in
  those two files rather than modifying `global.h`;
- output emission hooks remain at the three `Write_Frame()` call sites in `getpic.c`, not inside
  `store.c`;
- new decoder-sequence start detection is driven from `Decode_Picture()` / sequence frame number;
- dimensions, matrix arrays and existing decoder state are read through globals already available
  to `getpic.c`.

### 21.2 Additional-file gate

If coding reveals that another source/header file truly must change:

1. stop before making that edit;
2. identify the file;
3. state exactly why the reviewed two-file design is insufficient;
4. obtain Dave's approval.

Do not spread instrumentation through the pristine decoder for convenience.

### 21.3 Formatting invariant

Do not:

- reformat untouched code;
- rename reference-decoder symbols;
- modernize K&R function definitions;
- rewrite comments;
- normalize indentation or spacing.

The final implementation diff should show the instrumentation, not a formatting conversion.

### 21.4 Display build guard

`Write_Frame()` has only the three relevant call sites identified in `getpic.c`.

The Stage 1 Windows evidence build must not define the reference decoder's X11 `DISPLAY` path.

# Part C - Python analyzer contract

## 22. Analyzer purpose

The Stage 1 Python analyzer is a throwaway evidence tool.

Its job is to answer:

> What MPEG-2 coding metadata actually occurs in the target samples, and is the inspector output
> structurally trustworthy enough to support the later Stage 2 experiment?

It is not the VapourSynth filter and not the final index reader.

---

## 23. Structural validation

Before reporting statistics, the analyzer must validate:

1. file magic;
2. format version;
3. endian marker;
4. clean-complete file flag;
5. no unsupported field-picture flag;
6. no recovery/fault diagnostic flag;
7. no unsupported-chroma flag;
8. no macroblock-coverage-failure flag;
9. no MPEG-1/scalable/mid-sequence-geometry failure flag;
10. contiguous output ordinals starting at zero;
11. each record's `record_size_bytes`;
12. `mb_count == mb_width * mb_height` for accepted frame-picture records;
13. payload length exactly equals `mb_count * 8`;
14. every expected macroblock position marked written/valid exactly once;
15. record flag confirms coverage was verified;
16. reserved values/bits are zero where required;
17. parsed record count equals header `final_record_count`.

Any structural failure makes the run invalid.

No statistics are presented as trustworthy after an invalid-file result.

### 23.1 Duplicated-flag consistency checks

The temporary format deliberately carries a small amount of redundant state so the Python analyzer
can self-test the C instrumentation.

The following must agree exactly:

```text
quantiser_inherited_flag
    == (macroblock_quant_update == 0)

prediction_derived_or_inherited_flag
    == (motion_source == 2 or motion_source == 3)
```

Any mismatch is a **structural error** and invalidates the run.

These are not reported as interesting statistics.

### 23.2 Cross-field semantic consistency checks

The analyzer also enforces the following cheap invariants.

#### Skipped macroblocks

For every:

```text
coding_state == SKIPPED
```

require:

```text
transform_state == NONE
macroblock_quant_update == 0
dct_type_bit_read == 0
motion_source != 1
```

`motion_source == 1` means coded/current-macroblock motion syntax and is impossible for a skipped
macroblock.

#### Inherited motion

Require:

```text
motion_source == 3
```

only when:

```text
coding_state == SKIPPED
picture_coding_type == B
```

Any other use of inherited motion is a structural error.

#### No motion

If:

```text
motion_source == 0
```

require:

```text
motion_dir_bits == 0
```

#### dct_type syntax-bit diagnostic

If:

```text
dct_type_bit_read == 1
```

require:

```text
picture_structure == FRAME_PICTURE
frame_pred_frame_dct == 0
coding_state != SKIPPED
```

This follows the pristine decoder's condition for reading the MPEG-2 `dct_type` bit.

The inverse is not required: a macroblock may satisfy the surrounding picture conditions yet still
not read the bit because the applicable macroblock-type condition is false.

#### FIELD transform state

If:

```text
transform_state == FIELD
```

require:

```text
dct_type_bit_read == 1
picture_structure == FRAME_PICTURE
frame_pred_frame_dct == 0
coding_state != SKIPPED
```

A FIELD transform state cannot be produced from a stale/default `dct_type`.

### 23.3 Purpose of these checks

Together these rules are intended to catch:

- stale skipped-macroblock `macroblock_type` leaking into QUANT flags;
- stale motion-direction flags leaking into skipped records;
- stale/default `dct_type` being promoted to FRAME/FIELD semantics;
- disagreement between the C writer's primary fields and its redundant diagnostic flags.

A failure means the instrumentation cannot yet be trusted and the analyzer must stop.

## 24. Required file-level summary

For each sample report:

```text
record count
sequence count
first/last output ordinal
coded dimensions observed
macroblock dimensions observed
picture-type counts: I / P / B
picture_structure counts
field-picture count
progressive_frame distribution
q_scale_type distribution
chroma_format distribution
custom quantisation-matrix-in-effect status observed
chroma-matrix-versus-luma differences observed
coverage status
recovery/fault diagnostic status
```

If any property changes mid-stream, list the output ordinals where it changes.

---

## 25. Required transform-state analysis

Report:

### 25.1 Overall counts

```text
FRAME macroblocks
FIELD macroblocks
NONE macroblocks
```

as counts and percentages.

### 25.2 By picture type

Break FRAME/FIELD/NONE down separately for:

```text
I
P
B
```

### 25.3 Mixed transform-state frames

Report:

- number/percentage of frames containing both FRAME and FIELD states;
- number/percentage containing NONE plus coded-transform states;
- per-frame counts.

### 25.4 Neighbour transitions

For the macroblock grid, report counts of neighbouring state pairs:

Horizontal neighbours:

```text
FRAME-FRAME
FRAME-FIELD
FRAME-NONE
FIELD-FIELD
FIELD-NONE
NONE-NONE
```

Vertical neighbours likewise.

Treat unordered pairs consistently for summary totals; raw directed counts may also be available.

This provides evidence about how often mixed geometry occurs at macroblock boundaries.

---

## 26. Required quantiser analysis

Report the effective derived quantiser scale:

- minimum;
- maximum;
- mean;
- median;
- histogram/counts by exact scale value;
- by I/P/B picture type;
- by FRAME/FIELD/NONE transform state;
- separately for blockier and original test samples.

Also report:

```text
macroblocks carrying MACROBLOCK_QUANT updates
macroblocks using inherited/current quantiser state
```

The analyzer must describe these as effective decoder values, not all as values explicitly coded
at the macroblock.

---

## 27. Required coding-state analysis

Report:

```text
SKIPPED
INTRA
INTER
```

overall and by I/P/B picture type.

Cross-tabulate coding state with:

```text
transform state
effective quantiser scale
```

At minimum, verify the invariant:

```text
SKIPPED -> transform_state == NONE
```

and report any violation as a structural/semantic error, not an interesting statistic.

---

## 28. Effective-CBP checks

For frame pictures, verify:

```text
non-intra + effective_cbp == 0 -> transform_state == NONE
```

Report:

- count of non-intra CBP-zero macroblocks;
- how many of them had the diagnostic flag indicating a `dct_type` syntax bit was actually read;
- any violation of the expected NONE derivation.

This is the Stage 1 evidence check for the K-07 clarification.

---

## 29. Prediction diagnostics

Python, not C, normalises prediction semantics.

Using:

```text
picture_structure
coding_state
motion_type_raw
motion_dir_bits
motion_source
```

report:

- readable prediction modes overall and by picture type;
- coded/current-MB versus decoder-derived versus inherited source;
- field-prediction prevalence in frame pictures;
- correlation with FRAME/FIELD/NONE and coding state.

The analyzer must not interpret `motion_type_raw` without `picture_structure`, because the same
numeric value can have different MPEG-2 meanings.

Skipped B-picture inherited direction must be labelled inherited, not freshly coded.

These results remain diagnostic only and do not promote prediction mode into the first deblocking
metadata set.

## 30. Quantisation-matrix occurrence

The analyzer reports whether each record has:

- a non-default intra matrix in effect;
- a non-default non-intra matrix in effect;
- a chroma intra matrix differing from the current luma intra matrix;
- a chroma non-intra matrix differing from the current luma non-intra matrix.

These statuses come from array comparisons captured in the metadata slot, not from transient
`load_*_quantizer_matrix` flags.

For the target 4:2:0 material, the first two are the principal Stage 1 prevalence question; the
chroma comparisons are diagnostic.

This answers prevalence only.

The temporary format does not store the 64 matrix values in v1.

If non-default matrices occur, whether their values need later capture remains a separate design
question.

## 31. Raw inspection modes

The analyzer should provide at least:

```text
summary              whole-file report
frame <N>            frame-header + frame MB summary
mb <N> <x> <y>       one macroblock record
dump-frame <N>       readable raster/grid dump for one frame
```

Exact command-line spelling may differ.

The important requirement is that a human can inspect individual records without writing another
tool.

---

## 32. Early sample comparison

The first accepted analyzer report should compare:

```text
TEST_4A_A003.mpg
TEST_4A_A003_blocky.mpg
```

At minimum show side-by-side differences in:

- record/frame counts;
- I/P/B counts;
- FRAME/FIELD/NONE proportions;
- effective QP distributions;
- skipped/intra/inter proportions;
- mixed FRAME/FIELD prevalence;
- custom/non-default matrix-in-effect occurrence;
- field-picture occurrence.

This comparison is evidence gathering, not yet a deblocking-quality result.

---

# Part D - Acceptance before C implementation

## 33. Design review gate

Before C source is modified:

1. Claude reviews this document against the pristine decoder source.
2. Any disagreement is resolved with Dave.
3. Dave approves the resulting Stage 1 design.

Only then does coding begin.

---

## 34. First implementation acceptance criteria

The first instrumented build is not accepted merely because it compiles.

It must satisfy all of the following.

### 34.1 Source-diff discipline

- pristine source is the base;
- substantive changes limited to `getpic.c` and `mpeg2dec.c` unless Dave approves otherwise;
- no `global.h` or `store.c` change in the reviewed design;
- no unrelated formatting change.

### 34.2 Build/run

- Windows build succeeds in the established environment;
- X11 `DISPLAY` path is not defined;
- `-b -` accepts ffmpeg elementary-video stdin;
- `-m <file>` produces the temporary index;
- metadata output never shares stdout with binary data;
- Stage 1 diagnostics use stderr.

### 34.3 Supported-stream gate

For each accepted sample:

```text
MPEG-2 only
non-scalable
single elementary video stream
4:2:0 chroma for temporary format v1
frame pictures only unless field merge has been implemented
```

Any unsupported condition invalidates the run and prevents final index publication.

### 34.4 File and coverage validation

For each accepted test sample:

- file finalizes cleanly;
- analyzer structural validation passes;
- every frame picture has exactly-once macroblock coverage;
- no duplicate or missing macroblock position;
- no recovery/fault diagnostic;
- no unsupported chroma/MPEG-1/scalability flag;
- no invalid mid-sequence geometry/chroma change;
- no field-picture flag in first implementation if field merge remains deferred.

### 34.5 Early correspondence

For each supplied test sample:

```text
temporary index record count == BestSource frame count
```

A mismatch blocks further analyzer interpretation.

If a mismatch occurs, check first for true sequence-end boundaries followed by leading B
pictures/open-GOP behaviour before assuming the metadata-slot mechanism is wrong. The mismatch
still must be explained; it is never accepted by default.

### 34.6 Semantic invariants

Analyzer confirms all structural/cross-field rules in section 23, including at minimum:

```text
SKIPPED -> NONE

SKIPPED -> macroblock_quant_update == 0

SKIPPED -> dct_type_bit_read == 0

SKIPPED -> motion_source != CODED

motion_source == INHERITED -> SKIPPED B picture only

motion_source == NONE -> motion_dir_bits == 0

quantiser_inherited_flag
    == (macroblock_quant_update == 0)

prediction_derived_or_inherited_flag
    == (motion_source == DERIVED or INHERITED)

dct_type_bit_read ->
    frame picture
    and frame_pred_frame_dct == 0
    and not SKIPPED

FIELD ->
    dct_type_bit_read == 1
    and frame picture
    and frame_pred_frame_dct == 0
    and not SKIPPED

non-intra and effective_cbp == 0 -> NONE

FRAME/FIELD never derived merely from stale/default dct_type

output ordinals contiguous from zero
```

Any violation is a hard structural/semantic failure, not an analyzer statistic.

Prediction diagnostics for skipped macroblocks must be marked derived/inherited according to their
explicit skipped path, never fresh syntax.

### 34.7 Evidence output

Analyzer successfully produces the required comparison of original versus blockier sample.

# Part E - Explicit non-goals for Stage 1 v1

## 35. Not being designed/frozen here

This document does **not** decide:

- final `.idx2` byte layout;
- final compression/bit packing;
- production index size;
- final VapourSynth plugin reader;
- filter kernel mathematics;
- strength range;
- NONE filtering eligibility;
- chroma filtering strength;
- whether CBP belongs in final `.idx2`;
- whether prediction mode belongs in final `.idx2`;
- final handling of field pictures if the supplied samples contain none;
- full Stage 5 BestSource/VapourSynth frame-identity proof.

---

# Part F - Review questions for Claude

## 36. Claude source-review disposition

Claude reviewed v0.1 against the pristine reference decoder and returned **approve with
corrections**.

The review confirms:

1. metadata-slot rotation mirrors the reference-frame buffer lifetime for frame pictures;
2. the three relevant output call sites are all in `getpic.c`;
3. the FRAME/FIELD/NONE derivation is sound for ordinary non-scalable MPEG-2 frame pictures once
   skipped/no-residual gating is applied;
4. effective CBP can be captured in `getpic.c`;
5. `dct_type` syntax-bit presence can be diagnosed in `getpic.c`;
6. MACROBLOCK_QUANT presence can be captured safely when gated on non-skipped;
7. raw motion values should be stored and normalised in Python;
8. matrix state must be determined by array comparison, not load flags;
9. exactly-once macroblock coverage is the primary damage/validity gate;
10. no third source/header file is required under the conditions in section 21.

The five principal corrections from the review are incorporated in this v0.2:

- stale `macroblock_type` is never treated as fresh syntax for skipped macroblocks;
- per-picture coverage replaces `Fault_Flag` as the primary validity gate;
- custom-matrix status uses array comparison;
- prediction normalisation moves to Python;
- only a true sequence end starts a new decoder sequence, and unsupported mid-sequence
  geometry/chroma changes invalidate the run.

Additional source-review points incorporated:

- picture/header fields are emitted from metadata slots, including `progressive_frame`;
- MPEG-1 and scalable input are refused;
- count-mismatch diagnosis checks sequence-end plus leading-B/open-GOP behaviour early;
- `-m` is confirmed available;
- the two-file patch target is source-review feasible.

## 37. Proposed next step after review

Claude's source review has been incorporated into v0.2.

If Dave approves this revised design:

> ChatGPT prepares the minimal patch against the pristine reference source, with no unrelated
> formatting changes.

Before Dave runs it:

1. ChatGPT mechanically diffs the edited tree against the pristine source;
2. verifies that substantive edits are limited to `getpic.c` and `mpeg2dec.c`;
3. reports the exact change inventory;
4. provides the build/run instructions and analyzer together with the patch/source tree.

No coding begins until Dave approves this v0.2 working design.

---

## 38. Change log

### v0.3 - 2026-10-06

- Incorporated Claude's final consistency-test recommendation after review of v0.2.
- Defined the deliberately duplicated macroblock flags as analyzer self-tests rather than passive
  redundancy.
- Added hard equality checks between `macroblock_quant_update` and the quantiser-inherited flag,
  and between `motion_source` and the prediction-derived/inherited flag.
- Added cross-field structural checks for skipped macroblocks, inherited motion, no-motion
  direction bits, `dct_type` syntax-bit applicability and FIELD transform state.
- Declared every mismatch a structural/semantic failure that invalidates the run; none are treated
  as interesting statistics.
- No change to metadata flow, binary payload size, source-file footprint, or project architecture.

### v0.2 - 2026-10-06

- Incorporated `Claude_REVIEW_OF_ChatGPT_Stage1_Inspector_Instrumentation_Design_v0_1.md`.
- Gated every `macroblock_type`-derived field on non-skipped semantics; skipped QUANT and
  dct_type-read flags are forced zero.
- Replaced `Fault_Flag` as the primary damage gate with exactly-once per-picture macroblock
  coverage; retained recovery paths as secondary sticky diagnostics.
- Added duplicate/missing macroblock detection and coverage acceptance invariants.
- Replaced transient quantisation-matrix load flags with matrix-array comparisons.
- Replaced C-side prediction normalisation with raw motion bytes plus Python normalisation.
- Clarified that only `SEQUENCE_END_CODE` starts a new decoder sequence; repeated sequence headers
  do not.
- Added hard invalidation for mid-sequence geometry/chroma changes inconsistent with allocated
  decoder buffers.
- Required all delayed-output picture/header fields, including `progressive_frame`, to come from
  the matching metadata slot.
- Added MPEG-1 and scalable/two-stream rejection.
- Added leading-B/open-GOP diagnosis as the first investigation if the BestSource count gate fails.
- Confirmed `-m` is free and that the reviewed design can remain a two-source-file patch.
- Preserved the 8-byte-per-macroblock temporary payload while changing its prediction fields to
  raw motion diagnostics.

### v0.1 - 2026-10-06

- First Stage 1 instrumentation design draft.
- Consolidated metadata flow, field/sequence hazards, record semantics, temporary binary format and
  analyzer contract into one working document.
- Used metadata slots mirroring the decoder's reference/B-picture buffers.
- Defined output-emission ordinal as the temporary record identity.
- Defined FRAME/FIELD/NONE from applicable coded residual transform semantics.
- Added explicit effective-CBP diagnostic needed to verify NONE derivation.
- Kept raw quantiser code deferred to avoid unnecessary `gethdr.c` modification.
- Proposed an intentionally verbose 8-byte-per-macroblock temporary payload.
- Deferred field-pair implementation only if the supplied samples contain no field pictures; first
  implementation must detect/count and invalidate the run if they are present.
- Added early inspector-record-count versus BestSource-frame-count gate for both supplied samples.
- Stated the strong expectation that the minimal implementation changes only `getpic.c` and
  `mpeg2dec.c`.
