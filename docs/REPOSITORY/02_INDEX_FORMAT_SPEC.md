# 02 - Index Format Specification

**Document:** `02_INDEX_FORMAT_SPEC.md`
**Version:** 0.3 (DRAFT - deliberately minimal; constraints ratified)
**Date:** 2026-10-06
**Drafted by:** Claude (per D-23)
**Status:** DRAFT. NOT FROZEN. Index content, record sizes and field packing are not committed
until Stage 3, after the feasibility gate (D-01, D-17). Items marked DECIDED are ratified by
Dave. Constraints C-1 to C-5 are all ratified; the specification as a whole remains DRAFT / NOT
FROZEN until the feasibility gate and Stage 3.
**Decision authority:** `05_DECISIONS.md`

---

## 0. Scope of this document

Per D-22, this document lists only constraints that are already justified. It does not design the
format. The draft binary layout in proposal v0.5 section 5.1 (magic "MBX2", 16-byte header,
4-byte frame header, 2 bytes per macroblock) is illustrative history only and is not reproduced
or committed here.

Why the custom index is provisional, and what it must justify itself by: see
`06_DEBLOCK_CONCEPT.md` sections 9.4 and 3 (K-09).

Source abbreviations follow `06_DEBLOCK_CONCEPT.md` section 0.3.

---

## 1. Constraints

### C-1 - Frame correspondence invariant - DECIDED (D-02; proposal v0.5 section 5.4)

> Index record N must correspond exactly to VapourSynth frame N.

Records follow the decoder output (display) frame sequence that maps to VapourSynth frames, not
bitstream parse order (K-06, ACCEPTED (RESEARCHED)). The exact picture/field-to-frame
mapping, including repeat_first_field and field pictures, is established by research and Stage 5
testing before the format is frozen (D-02).

### C-2 - Versioning and simple structural checks - DECIDED (D-02; proposal v0.5 section 5.3)

- The index carries a format version.
- Each record carries a display-record ordinal (or equivalent simple ordinal) sufficient to detect
  missing, extra or out-of-sequence records.
- The plugin compares the index's dimensions and record count with the input clip and hard-aborts
  on any mismatch.
- No complex source-identity or hash scheme is required; the user is responsible for selecting
  the index that belongs to the input. A wrong index of identical shape is not detected.

### C-3 - No false transform state - DECIDED (K-07; ratified 2026-10-06)

Any representation of per-macroblock transform state must not encode a meaningful FRAME or FIELD
value where no coded transform state exists (skipped and no-residual macroblocks). The semantic
states are FRAME, FIELD and NONE (`06` section 4.3); how they are encoded is not decided.

### C-4 - Quantiser semantics must be explicit - DECIDED (K-05; CM 12; ratified 2026-10-06)

If a quantiser value is stored, the specification must state:

- whether it is the raw quantiser_scale_code or the derived quantiser scale under q_scale_type
  (the concept prefers the derived scale, `06` section 6);
- what value a skipped macroblock carries (not applicable, inherited, or separately flagged);
- whether, and how, weighting-matrix information is represented (O-07).

### C-5 - Stage 1-2 drafts are versioned and disposable - DECIDED (carried from proposal v0.5 section 6.5; ratified 2026-10-06)

The binary index used in Stages 1-2 is a versioned draft that may change as research shows which
fields are needed. No text index format is used.

---

## 2. Explicitly not committed

- record sizes and field packing;
- picture-level header contents beyond C-1 and C-2;
- coded-block pattern, coefficient activity, prediction mode, motion vectors (D-13, D-14);
- quantisation-matrix representation (O-07);
- field-picture representation (O-08);
- any source-identity scheme beyond C-2.

---

## 3. Open items carried from proposal v0.5 section 5.2

Still to be resolved at specification time (Stage 3):

1. A frame assembled from two field pictures may have two picture types and quantiser contexts.
2. Skipped-macroblock quantiser value (C-4).
3. Raw code versus derived scale; custom matrices (C-4).
4. Edge cases in the output/display mapping (the principle is settled by C-1):
   repeat_first_field / pulldown, open-GOP leading B pictures, field pictures, and mid-stream
   sequence changes.
5. Behaviour for truncated or damaged streams.

---

## 4. Change log

### v0.3 - 2026-10-06 (DRAFT; constraints ratified)

- Ratified by Dave on 2026-10-06: C-3, C-4 and C-5 changed from PROPOSED to DECIDED. Statuses updated only.
- The specification remains DRAFT / NOT FROZEN until the feasibility gate and Stage 3.
- This file, `06_DEBLOCK_CONCEPT.md` and `05_DECISIONS.md` are now the normal project authority;
  the Stage 0 research and review files are provenance only.

### v0.2 - 2026-10-06 (DRAFT)

- Section 3 item 4 narrowed to edge cases of the output/display mapping, per
  `ChatGPT_COLD_REVIEW_OF_Repository_Drafts_v0_1.md` section 14.2. C-5 remains PROPOSED.

### v0.1 - 2026-10-06 (DRAFT)

- Created by Claude as a deliberately minimal draft per D-22 and FCR section 16.
- Constraints C-1 to C-5 recorded; layout not reproduced.
