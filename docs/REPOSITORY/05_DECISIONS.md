# 05 - Project Decisions

**Document:** `05_DECISIONS.md`
**Version:** 1.0 (RATIFIED)
**Date:** 2026-10-06
**Drafted by:** Claude (per D-23)
**Status:** RATIFIED. Ratified by Dave on 2026-10-06. This file is the project's decision authority (D-20).
**Controlling proposal:** `MPEG2_Macroblock_Index_VapourSynth_Deblocking_Project_Proposal_v0_5.md`

---

## 0. Role of this file

This file is the project's decision authority (D-20). Proposal v0.5 section 11 is retained as
history; D-01 to D-08 are copied below verbatim from it.

Record fields: ID; status; date; origin; issue; alternatives considered; decision; rationale;
evidence; supersedes / superseded by. Superseded decisions are marked, never deleted.

Status values: **DECIDED** (ratified by Dave), **PROPOSED** (awaiting ratification),
**SUPERSEDED**. DECIDED-class statuses also include the inherited headings DECIDED WITH
SIMPLIFICATION, DECIDED FOR CURRENT SCOPE and CLARIFIED (D-02, D-07, D-08); all three were
ratified by Dave and carry the same authority as DECIDED.

Source abbreviations follow `06_DEBLOCK_CONCEPT.md` section 0.3.

---

## 1. Decision index

| ID | Title | Status | Date |
|---|---|---|---|
| D-01 | Order of work | DECIDED | 2026-10-06 |
| D-02 | `.idx2` validity/correspondence | DECIDED WITH SIMPLIFICATION | 2026-10-06 |
| D-03 | Python reference prototype | DECIDED | 2026-10-06 |
| D-04 | Claude research and review | DECIDED | 2026-10-06 |
| D-05 | Starter knowledge documents | DECIDED | 2026-10-06 |
| D-06 | Reference decoder / inspector sources | DECIDED | 2026-10-06 |
| D-07 | Strength evolution | DECIDED FOR CURRENT SCOPE | 2026-10-06 |
| D-08 | Existing-filter baseline | CLARIFIED | 2026-10-06 |
| D-09 | Frame-owned processing model | DECIDED | 2026-10-06 |
| D-10 | Family A as leading hypothesis | DECIDED | 2026-10-06 |
| D-11 | Family B as mandatory control | DECIDED | 2026-10-06 |
| D-12 | Family C optional | DECIDED | 2026-10-06 |
| D-13 | First metadata set: quantiser + transform state | DECIDED | 2026-10-06 |
| D-14 | Prediction type as Stage 1 diagnostic only | DECIDED | 2026-10-06 |
| D-15 | Stage 2 measures metadata values independently | DECIDED | 2026-10-06 |
| D-16 | Stage 2 results by I/P/B picture type | DECIDED | 2026-10-06 |
| D-17 | Custom `.idx2` provisional | DECIDED | 2026-10-06 |
| D-18 | Ablation step 2b | DECIDED | 2026-10-06 |
| D-19 | Decision numbering | DECIDED | 2026-10-06 |
| D-20 | This file is the decision authority | DECIDED | 2026-10-06 |
| D-21 | Labelling of accepted knowledge | DECIDED | 2026-10-06 |
| D-22 | Scope of `02_INDEX_FORMAT_SPEC.md` | DECIDED | 2026-10-06 |
| D-23 | Drafting status and repository file conventions | DECIDED | 2026-10-06 |

---

## 2. D-01 to D-08 (verbatim from proposal v0.5 section 11)

Origin: proposal v0.4/v0.5 review, ratified by Dave 2026-10-06. Text below is copied verbatim;
section references inside it ("section 3", "section 9") refer to proposal v0.5.

### D-01. Order of work - DECIDED

Accept the single order of work in section 3: conceptual algorithm design, evidence/test tooling, Python experimental prototype, feasibility gate, then index specification/inspector/C++/API4/AVX2.

Technical hypotheses inside those stages are not thereby ratified as facts.

### D-02. `.idx2` validity/correspondence - DECIDED WITH SIMPLIFICATION

Include simple versioning and record/frame correspondence checks from version 1. Avoid a complex source-identity mechanism by default: the user bears responsibility for choosing the index belonging to the input file.

The intended simple correspondence model is expected to centre on displayed frame number / VapourSynth frame number, but the exact picture/field/display-order mapping must be established by research and Stage 5 testing before the format is frozen.

### D-03. Python reference prototype - DECIDED

Use Python for Stage 2 if practical. Its purpose is an experimental algorithmic oracle/reference, not production speed. Short test clips and deliberately slow execution are acceptable.

If the selected algorithm proves genuinely impractical to express/test faithfully in Python, that is grounds to revisit the implementation language rather than force Python.

### D-04. Claude research and review - DECIDED

Claude may perform both independent research and review. ChatGPT and Claude may deliberately investigate different research questions, then exchange and contrast findings. Duplication is used selectively where independent confirmation is valuable.

Citations/evidence and Dave's ratification remain required before research becomes project truth.

### D-05. Starter knowledge documents - DECIDED

Begin with the three-document set in section 9. Add documents only when a demonstrated project-management or technical need exists.

Research division between ChatGPT and Claude does not itself require extra permanent documents; durable findings should be incorporated into the appropriate project document.

### D-06. Reference decoder / inspector sources - DECIDED

Dave can provide both the pristine reference decoder source and the current working inspector C source.

The working inspector is the practical starting point. The pristine source is the comparison authority. A mechanical diff will establish the actual changes before further instrumentation work.

### D-07. Strength evolution - DECIDED FOR CURRENT SCOPE

Initial work uses one manually selected global strength. A future `auto` mode or adaptive strength with explicit limiting may be considered later if evidence supports it. It is not part of the initial feasibility requirement.

### D-08. Existing-filter baseline - CLARIFIED

Do not assume that an existing MPEG-2-specific deblocking filter is available. Research first establishes what relevant historical/generic post-processing algorithms or implementations exist and whether comparison is meaningful. The unfiltered decode and ground-truth source remain mandatory baselines.

---

## 3. Decisions D-09 to D-17 (DECIDED by Dave, 2026-10-06)

Origin: ChatGPT final cross-review (FCR section 14, candidates D-A to D-I), numbered per D-19.

### D-09 - Frame-owned processing model - DECIDED

- **Origin:** FCR D-A; Dave's requirement (CR section 6; FCR section 1).
- **Issue:** Interlaced frame pictures can mix frame-DCT and field-DCT macroblocks, so neither a
  whole-frame nor a whole-field fixed grid is correct.
- **Alternatives considered:** (a) frame-raster filtering throughout; (b) split into two fields
  and deblock each independently; (c) frame-owned, metadata-directed filtering with
  field-parity-aware sample access.
- **Decision:** (c). The decoded frame is the processing object; metadata gives seam geometry;
  same-field-polarity access is used only where geometry requires it; no separate-field
  deblocking pass.
- **Rationale:** (a) mixes temporally different fields; (b) hides per-macroblock seam variation
  behind one field grid; (c) uses authoritative geometry without field mixing.
- **Evidence:** PA-add 3; CM 5-6; CRV R1; GRSP 2-3; FCR 1-2. Concept: `06` section 2.

### D-10 - Family A as leading hypothesis - DECIDED

- **Origin:** FCR D-B.
- **Issue:** Which algorithm family carries the project's metadata-assisted hypothesis.
- **Alternatives considered:** Families A, B, C (`06` section 8).
- **Decision:** Family A (short-support, quantiser-aware, edge-preserving boundary filtering with
  metadata-directed geometry) is the leading Stage 2 hypothesis. Kernel undecided.
- **Rationale:** Deterministic, short-support, scalar- and AVX2-friendly; uses metadata only where
  it has a plausible purpose.
- **Evidence:** PA 6.1, PA-add 3.4; CR 10; FCR 12.

### D-11 - Family B as mandatory control - DECIDED

- **Origin:** FCR D-C.
- **Issue:** The value of metadata cannot be measured without a strong metadata-free baseline.
- **Alternatives considered:** omit a pixel-only control; include it as candidate; include it as
  control only.
- **Decision:** Family B (pixel-only, interlace-aware) is retained as the mandatory falsification
  control, not as a candidate for adoption.
- **Rationale:** The prior art shows a pixel-only method handling mixed frame/field coding (PA
  S10); the project must beat it to justify metadata.
- **Evidence:** PA Q11, 6.2; PA-add 3.6; CR 3.4; FCR 12.

### D-12 - Family C optional - DECIDED

- **Origin:** FCR D-D.
- **Decision:** Family C (shifted-DCT re-quantisation) is an optional quality reference and must
  not delay testing Families A and B.
- **Rationale:** Heavier; may address a broader restoration problem than intended.
- **Evidence:** PA 6.3; CR 10.

### D-13 - First metadata set: quantiser + transform state - DECIDED

- **Origin:** FCR D-E.
- **Issue:** Which metadata the first experiment uses.
- **Alternatives considered:** add CBP, coefficient activity, prediction mode or motion vectors
  from the start.
- **Decision:** The first metadata experiment uses only real per-macroblock quantiser and
  authoritative transform state (FRAME/FIELD/NONE). CBP, coefficient activity, prediction mode
  and motion vectors are not initially required. Order if more is needed: CBP, then coefficient
  activity, then motion data only with compelling evidence.
- **Rationale:** Minimal index; no prior-art support found for CBP in post-filters (PA Q6).
- **Evidence:** CM 15.3, 18; CR 8; CRSP Q6; GRSP 11; FCR 8.

### D-14 - Prediction type as Stage 1 diagnostic only - DECIDED

- **Origin:** FCR D-F; CRV R4.
- **Decision:** The Stage 1 analyzer reports frame/field prediction type per macroblock if it is
  cheap and unambiguous to expose from the reference decoder. It is not a first-algorithm input.
- **Rationale:** Measure its frequency and relevance (O-12) before giving it any role.
- **Evidence:** CRV R4; GRSP 6; FCR 10.

### D-15 - Stage 2 measures metadata values independently - DECIDED

- **Origin:** FCR D-G.
- **Decision:** Stage 2 explicitly measures the separate values of the real per-macroblock
  quantiser, the transform state, and their combination, using the ladder in `06` section 9
  (as amended by D-18). The comparisons that isolate each value are defined in `06` section 9.2.
- **Rationale:** QP may be available without a custom index (K-09); the index must justify itself
  by what only it provides.
- **Evidence:** CR 11; CRSP Q5; GRSP 13; FCR 11.

### D-16 - Stage 2 results by I/P/B picture type - DECIDED

- **Origin:** FCR D-H; CRV R3.
- **Decision:** Stage 2 results are reported separately for I, P and B pictures where practical.
- **Rationale:** Off-grid propagated blocking (K-08) bounds gains in P and B pictures; the
  breakdown shows that bound.
- **Evidence:** CRV R3; GRSP 5; FCR 9.

### D-17 - Custom `.idx2` provisional - DECIDED

- **Origin:** FCR D-I.
- **Decision:** The custom reference-decoder `.idx2` architecture remains provisional until
  Stage 2 shows that metadata unavailable through a simpler decoder-side-data path provides
  worthwhile benefit.
- **Alternatives considered:** Architecture A (custom index) versus Architecture B (decoder QP
  side data plus pixel-only geometry), `06` section 9.4.
- **Evidence:** PA S18; CR 7; GRSP 9-10; FCR 7.

---

## 4. Decisions D-18 to D-23 (DECIDED by Dave, 2026-10-06)

Origin: Dave's rulings on issues I-1 to I-6 tabled by Claude before drafting (chat,
2026-10-06).

### D-18 - Ablation step 2b - DECIDED

- **Origin:** I-1.
- **Issue:** In FCR section 11, step 2 (Family B) versus step 3 (Family A kernel + real QP) changes
  both the kernel and the quantiser, so it cannot isolate the value of the real quantiser.
- **Alternatives considered:** keep FCR's ladder and note the confound; add a step.
- **Decision:** Add step 2b: the Family A kernel with emulated/fixed quantiser and pixel-detected
  seams. Steps 2b and 3 locate horizontal seams without dct_type by checking both candidate
  positions (macroblock edge and field centreline), in the manner of PA S10.
- **Rationale:** The added step allows the value of the real quantiser to be isolated cleanly
  within Family A (2b vs 3), and supports a clean transform-state comparison (3 vs 4). Step 2 vs
  2b is a Family B versus metadata-blind Family A comparison, not a pure kernel isolation
  (`06` section 9.2).
- **Evidence:** FCR 11; Claude chat replies of 2026-10-06 (after GRSP, and issue I-1).

### D-19 - Decision numbering - DECIDED

- **Origin:** I-2.
- **Decision:** New decisions continue the D-nn sequence from D-09. FCR candidates D-A to D-I are
  recorded as D-09 to D-17, each noting its letter origin.

### D-20 - This file is the decision authority - DECIDED

- **Origin:** I-3.
- **Decision:** `05_DECISIONS.md` is the single decision authority. D-01 to D-08 are copied
  verbatim from proposal v0.5 section 11, which becomes history.
- **Rationale:** Avoid two competing decision records.

### D-21 - Labelling of accepted knowledge - DECIDED

- **Origin:** I-4.
- **Decision:** Knowledge items (K-nn) ratified into repository documents are labelled ACCEPTED,
  keep their evidence level (e.g. RESEARCHED) and source file visible, and keep their K numbers.
  Ratification does not make an item VERIFIED.

### D-22 - Scope of `02_INDEX_FORMAT_SPEC.md` - DECIDED

- **Origin:** I-5.
- **Decision:** `02_INDEX_FORMAT_SPEC.md` lists only justified constraints. The draft binary
  layout in proposal v0.5 section 5.1 is referenced as illustrative history, not reproduced.
  Rationale such as "the quantiser alone does not justify the index" lives in
  `06_DEBLOCK_CONCEPT.md`, with a one-line pointer from `02`.
- **Rationale:** Avoid an unfrozen layout appearing committed; keep specification and rationale
  separate.

### D-23 - Drafting status and repository file conventions - DECIDED

- **Origin:** I-6.
- **Decision:** Claude drafts `06_DEBLOCK_CONCEPT.md`, `05_DECISIONS.md` and a minimal
  `02_INDEX_FORMAT_SPEC.md` before ratification, marking every new decision and knowledge item
  PROPOSED. Repository files carry no version suffix in the filename; the version is in the header
  and change log; superseded copies go to `superseded/`; files are US-ASCII with CRLF line endings,
  mechanically checked.
- **Workflow:** Claude drafts; ChatGPT performs a cold technical review; Dave amends and ratifies.

---

## 5. Change log

### v1.0 - 2026-10-06 (RATIFIED)

- Ratified by Dave on 2026-10-06. Statuses updated only; no decision text changed.
- D-09 to D-17 changed from PROPOSED to DECIDED.
- D-01 to D-08 and D-18 to D-23 remain in force, unchanged.
- This file, `06_DEBLOCK_CONCEPT.md` and `02_INDEX_FORMAT_SPEC.md` are now the normal project
  authority; the Stage 0 research and review files are provenance only.

### v0.2 - 2026-10-06 (DRAFT)

- Corrections from `ChatGPT_COLD_REVIEW_OF_Repository_Drafts_v0_1.md`: DECIDED-class status
  vocabulary defined (section 0); D-15 points to the comparison definitions; D-18 rationale no
  longer claims every comparison changes one variable. Inherited D-01 to D-08 text unchanged.

### v0.1 - 2026-10-06 (DRAFT)

- Created by Claude. D-01 to D-08 copied verbatim from proposal v0.5 section 11 (D-20).
- D-09 to D-17 drafted as PROPOSED from FCR section 14 (D-19).
- D-18 to D-23 recorded as DECIDED from Dave's rulings I-1 to I-6.
