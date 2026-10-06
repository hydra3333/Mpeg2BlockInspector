# ChatGPT Cold Review of Repository Drafts v0.1

**Filename:** `ChatGPT_COLD_REVIEW_OF_Repository_Drafts_v0_1.md`
**Version:** 0.1
**Date:** 2026-10-06
**Author:** ChatGPT
**Status:** Cold technical review for Dave and Claude. Not repository authority.

**Reviewed drafts:**
- `06_DEBLOCK_CONCEPT.md` v0.1 DRAFT
- `05_DECISIONS.md` v0.1 DRAFT
- `02_INDEX_FORMAT_SPEC.md` v0.1 DRAFT

---

## 1. Overall verdict

The three drafts are strong and faithfully preserve the converged project direction.

I find no architectural disagreement with:

- the frame-owned processing model;
- the prohibition on independent whole-field deblocking as the algorithmic model;
- FRAME/FIELD/NONE transform-state semantics;
- the luma seam geometry;
- the 4:2:0 chroma distinction;
- Families A/B/C and their roles;
- keeping the custom `.idx2` architecture provisional;
- keeping the index specification deliberately minimal;
- the decision-file / concept-file / index-spec separation.

The drafts should be revised before ratification, but the required changes are limited.

I classify the findings as:

- **MUST FIX:** six items affecting evidence/status precision or experiment interpretation.
- **SHOULD FIX:** six wording/knowledge-management refinements.
- **ACCEPT AS DRAFTED:** the remaining structure and content.

After these corrections I would be comfortable recommending the three files for Dave's
ratification.

---

## 2. MUST FIX 1 - O-01 incorrectly makes the FFmpeg/BestSource check a Stage 1 blocker

### Location

`06_DEBLOCK_CONCEPT.md`, open question O-01, currently:

> Can BestSource expose or preserve FFmpeg's MPEG-2 per-macroblock QP side data in the intended
> workflow? - Before Stage 1 tooling is committed

### Problem

This contradicts the explicit drafting qualification agreed before Claude started these files.

The FFmpeg/BestSource QP path should be investigated early, but it must **not necessarily block**
the Stage 1 throwaway inspector/analyzer.

Stage 1 tooling may still be needed to measure:

- real LG `dct_type` behaviour;
- FRAME/FIELD/NONE frequency;
- field pictures;
- quantiser distributions;
- prediction modes;
- other properties needed for the feasibility experiment.

### Required change

Replace the timing with wording such as:

> **Early architecture investigation; need not block Stage 1 throwaway inspector/analyzer tooling.**

The architecture should be settled before committing to the final index path, not before all
Stage 1 research tooling.

---

## 3. MUST FIX 2 - K-09 mixes a researched positive fact with an unproven negative search result

### Location

`06_DEBLOCK_CONCEPT.md` K-09 currently says:

> FFmpeg's MPEG-2 decoder can export per-macroblock quantiser information as frame side data
> attached to output frames; no equivalent per-macroblock dct_type export has been found.

The section says all K-01 to K-09 are:

> PROPOSED -> ACCEPTED (RESEARCHED)

### Problem

The first clause is supported by positive evidence.

The second clause is an **absence-of-evidence result**:

> no equivalent export has been found so far.

The research did not establish that no such interface can exist anywhere in FFmpeg or BestSource.

It therefore must not silently become an ACCEPTED (RESEARCHED) fact that FFmpeg does not export
`dct_type`.

### Required change

Keep K-09 as the positive researched finding only:

> **K-09 - RESEARCHED:** FFmpeg's MPEG-2 decoder can export per-macroblock quantiser information
> as frame side data associated with output frames.

Move the negative finding to OPEN/HYPOTHESIS wording, for example:

> **OPEN:** No standard per-macroblock MPEG-2 `dct_type` frame-side-data export has been identified
> in the research performed so far.

This can be a new open item or part of O-01/O-02 architecture investigation.

---

## 4. MUST FIX 3 - K-08 is over-labelled as uniformly RESEARCHED

### Location

K-08:

> Motion compensation can propagate blocking from reference pictures to positions off the current
> picture's transform grid, limiting any grid-based post-filter.

Section 3 globally labels all K items as ACCEPTED (RESEARCHED).

### Problem

The evidence supports:

- propagation/copying of reference-picture blocking through motion compensation;
- practical limitations of filters tied to expected grid positions.

But the complete sentence also contains a synthesis/inference:

- that propagated blocking lies off the **current** transform grid;
- and that this necessarily limits every current-grid post-filter in the stated way.

That conclusion is technically plausible and well supported, but in the review trail it was
explicitly developed as an inference/hypothesis.

### Required change

Do not globally label every K item RESEARCHED.

Either:

1. label K-08 **PROPOSED -> ACCEPTED (HYPOTHESIS supported by RESEARCHED evidence)**; or
2. split it into:
   - researched underlying facts;
   - the off-grid/achievable-bound conclusion as HYPOTHESIS.

Also soften section 10 from:

> No grid-based post-filter ... can address it.

to something like:

> A post-filter restricted to the current picture's known grid seams cannot systematically target
> blocking that has been propagated to off-grid locations; this can bound achievable improvement
> in P/B pictures.

This retains the design implication without making an unnecessarily absolute claim.

---

## 5. MUST FIX 4 - Step 2 versus 2b does not yet isolate only "the Family A kernel"

### Locations

`05_DECISIONS.md` D-18 rationale:

> Each comparison then changes one variable.

`06_DEBLOCK_CONCEPT.md` section 9.2:

> 2 vs 2b : value of the Family A kernel itself

### Problem

Step 2 is Family B.

Step 2b is Family A with:

- Family A's own filtering/decision behaviour;
- an emulated/fixed quantiser;
- pixel-detected geometry.

Unless the experiment is explicitly constructed so that step 2 and step 2b share every detector,
eligibility rule, threshold mechanism and support rule except the final correction kernel, the
comparison changes more than a single "kernel" variable.

The extra step 2b is still very useful because it makes these comparisons clean:

```text
2b vs 3 = value of real per-MB QP with Family A otherwise held constant
3  vs 4 = value of authoritative transform geometry with Family A + real QP held constant
5  vs 4 = value of real QP with authoritative geometry held constant
```

But step 2 vs 2b is primarily an **overall Family B versus metadata-blind Family A comparison**,
not necessarily a pure kernel isolation.

### Required change

In D-18, replace:

> Each comparison then changes one variable.

with:

> The added step allows the value of real QP to be isolated cleanly within Family A, and supports
> cleaner subsequent transform-state comparisons.

In section 9.2 replace:

> 2 vs 2b : value of the Family A kernel itself

with:

> 2 vs 2b : Family B control versus Family A under metadata-blind / fixed-QP conditions

Optionally add:

> This is not a single-variable kernel isolation unless the detector, eligibility logic and all
> non-kernel behaviour are explicitly held identical.

No additional experiment step is required merely to fix this wording.

---

## 6. MUST FIX 5 - O-10 points to the wrong comparison for its wording

### Location

O-10 currently asks:

> Does authoritative transform state beat a strong pixel-only interlace-aware control?

but says it is answered by:

> Stage 2 (step 3 vs 4)

### Problem

Step 3 versus step 4 isolates **pixel-detected versus authoritative transform geometry within
Family A**.

The strong Family B pixel-only control is step 2.

Therefore:

- **3 vs 4** answers the value of authoritative transform state within Family A.
- **2 vs 4** compares the complete metadata-assisted Family A approach against the strong Family B
  control.

### Required change

Either change O-10 to:

> Does authoritative transform-state geometry improve Family A over pixel-detected geometry?

with:

> Stage 2 (step 3 vs 4)

or split it into two questions:

- O-10a: value of authoritative transform geometry - 3 vs 4;
- O-10b: metadata-assisted Family A versus strong pixel-only Family B - 2 vs 4.

I prefer the split because both questions are important to the feasibility gate.

---

## 7. MUST FIX 6 - "Every macroblock edge is an 8x8 transform boundary" conflicts with NONE

### Location

`06_DEBLOCK_CONCEPT.md` section 4.5:

> Every 16x16 macroblock edge is also an 8x8 luma transform boundary.

### Problem

The same document carefully defines NONE as:

> no current coded residual transform geometry is asserted for this macroblock.

For a NONE/NONE relationship, calling the shared edge a current coded-transform boundary is too
strong.

The macroblock/coding-grid edge certainly exists and may show a prediction discontinuity, but a
current residual transform need not exist on either side.

### Required change

Use wording such as:

> Every 16x16 macroblock edge lies on the regular 8x8 luma coding grid. Where coded transforms are
> present it is also a transform-block boundary. For FRAME/FIELD/NONE combinations, the edge
> remains a macroblock boundary that may show a reconstructed-pixel discontinuity even when one or
> both sides have no current coded transform.

Then retain O-04 for the NONE/NONE filtering decision.

This change makes sections 4.3 and 4.5 consistent.

---

## 8. SHOULD FIX 1 - Evidence levels should be per K item, not globally RESEARCHED

### Location

`06_DEBLOCK_CONCEPT.md` section 3:

> All items: PROPOSED -> ACCEPTED (RESEARCHED).

### Recommendation

Give each K item an explicit evidence-level column.

Suggested classification:

- K-01: RESEARCHED
- K-02: RESEARCHED
- K-03: RESEARCHED from the standard; implementation handling not yet VERIFIED
- K-04: RESEARCHED, with field-picture scope clarified
- K-05: RESEARCHED
- K-06: RESEARCHED
- K-07: RESEARCHED syntax fact + proposed implementation constraint
- K-08: HYPOTHESIS supported by researched evidence, unless split
- K-09: RESEARCHED positive FFmpeg QP-export fact only

This better implements D-21 and prevents inference from being promoted merely because it sits in a
knowledge table.

---

## 9. SHOULD FIX 2 - Narrow K-04 to avoid field-picture ambiguity

### Current wording

> 4:2:0 chroma DCT organisation is always frame-organised and does not follow luma dct_type.

### Recommendation

Use:

> In MPEG-2 4:2:0 **frame pictures**, chroma blocks are organised in frame structure for DCT coding
> and do not follow the per-macroblock luma `dct_type` reorganisation.

Then preserve section 4.6:

> field pictures require their own geometry path.

This is more precise and avoids making "frame-organised" sound like a processing prescription for
field pictures.

---

## 10. SHOULD FIX 3 - K-03 verification wording should separate normative truth from implementation verification

### Location

After K-03:

> It must still be VERIFIED by a cold read of the reference decoder source.

### Problem

K-03 is a normative MPEG-2 geometry claim derived from H.262.

The reference decoder source is important to verify **how the inspector's decoder implements and
exposes that state**, not to make the standard's geometry true.

### Recommendation

Replace with:

> K-03 is RESEARCHED from H.262. Before inspector output is relied on, the reference decoder source
> must be cold-read to verify how it represents, derives and exposes the corresponding
> frame/field-DCT state.

This keeps standard knowledge and implementation verification conceptually separate.

---

## 11. SHOULD FIX 4 - "No pixel detection of seam positions" should be scoped to Family A

### Location

Section 5, detection vocabulary:

> No pixel detection of seam positions.

### Problem

Family B intentionally performs pixel-domain seam detection as the control.

### Recommendation

Use:

> In the metadata-directed Family A path, seam positions are supplied by MPEG-2 geometry and
> metadata; pixel detection of seam positions is not required.

Then Family B remains an intentional exception for falsification.

---

## 12. SHOULD FIX 5 - Quantiser storage remains open even if the algorithm operates on derived scale

### Location

`06_DEBLOCK_CONCEPT.md` section 6:

> The useful severity value is the actual derived quantiser scale, not the raw 5-bit code.

This is acceptable algorithmically but can be read as a format decision.

### Recommendation

Use:

> The algorithm should reason in terms of the derived MPEG-2 quantiser scale. Whether `.idx2`
> stores that derived value directly or stores sufficient syntax to derive it remains an index
> format decision.

This aligns exactly with `02_INDEX_FORMAT_SPEC.md` C-4 and the pre-drafting instruction not to
freeze the representation.

---

## 13. SHOULD FIX 6 - Decision status vocabulary in 05 is internally inconsistent

### Location

`05_DECISIONS.md` section 0 says status values are:

- DECIDED
- PROPOSED
- SUPERSEDED

but the inherited entries use:

- DECIDED WITH SIMPLIFICATION
- DECIDED FOR CURRENT SCOPE
- CLARIFIED

### Recommendation

Do not alter the inherited D-01 to D-08 wording merely for tidiness.

Instead define:

> DECIDED-class statuses include DECIDED, DECIDED WITH SIMPLIFICATION, DECIDED FOR CURRENT SCOPE,
> and CLARIFIED where the clarification was ratified by Dave.

Or add a separate "qualifier" column later.

The important point is that the decision authority must not imply D-08 is unratified merely
because its historical heading says CLARIFIED.

---

## 14. Index-spec review

### 14.1 C-5 downgrade

**AGREE.**

Claude was correct to leave C-5 PROPOSED.

Proposal v0.5 section 6.5 was itself PROPOSAL; it should not be promoted silently.

### 14.2 C-1 and open item 4

C-1 already establishes that records follow the output/display sequence mapping to VapourSynth.

Section 3 item 4 currently reopens:

> Display versus decode order ...

Recommendation:

change item 4 to:

> Edge cases in the output/display mapping: repeat_first_field / pulldown, open-GOP leading
> B-pictures, field pictures, and mid-stream sequence changes.

The principle "display/output order, not parse order" is no longer open; the difficult mapping
cases are.

### 14.3 C-3

**AGREE**, subject to the NONE/macroblock-edge wording correction in the concept document.

### 14.4 C-4

**AGREE.**

It correctly leaves raw code versus derived scale and matrix representation unfrozen.

### 14.5 Overall

`02_INDEX_FORMAT_SPEC.md` is appropriately minimal and should remain that way.

Do not restore the old 16-byte-header / 2-byte-MB layout until Stage 3 evidence justifies an
actual format.

---

## 15. Decision-file review

### D-01 to D-08

No substantive mismatch observed against the proposal-v0.5 decision text available in the review
trail.

### D-09 to D-17

The proposed decisions faithfully represent the converged research, subject to:

- D-13 remaining PROPOSED;
- D-15 wording following the corrected experiment interpretation above;
- D-17 remaining PROPOSED until the feasibility work.

### D-18

Keep the decision to add step 2b.

Correct only the overclaim that all comparisons become single-variable comparisons.

### D-18 evidence in chat

I do **not** consider this a problem.

A project decision may legitimately originate from Dave's explicit ruling in chat. The decision
record itself is the durable record of that ruling.

There is no need to manufacture a separate evidence file merely to make every decision point to
another Markdown file.

### D-19 to D-23

No technical objection.

---

## 16. File-format verification

Mechanically checked from the supplied ZIP:

```text
02_INDEX_FORMAT_SPEC.md
    US-ASCII: PASS
    CRLF:     100
    bare LF:  0

05_DECISIONS.md
    US-ASCII: PASS
    CRLF:     275
    bare LF:  0

06_DEBLOCK_CONCEPT.md
    US-ASCII: PASS
    CRLF:     407
    bare LF:  0
```

Claude's format report is confirmed.

---

## 17. Ratification recommendation after revision

After the MUST FIX items and the small SHOULD FIX wording changes are incorporated:

### `06_DEBLOCK_CONCEPT.md`

Recommend Dave ratify:

- K items at their corrected individual evidence levels;
- D-09 to D-17 if he agrees with the proposed decisions;
- the frame-owned processing model;
- the current Stage 2 experiment;
- the listed OPEN items.

The document should remain explicit that the actual filtering kernel, thresholds and strength
mapping are not yet decided.

### `05_DECISIONS.md`

Recommend it become the single decision authority as already decided by D-20.

When Dave ratifies D-09 to D-17, change their statuses from PROPOSED to DECIDED without rewriting
their technical substance unless Dave changes a decision.

### `02_INDEX_FORMAT_SPEC.md`

Recommend ratifying only its constraints, not a binary layout.

It should remain DRAFT / NOT FROZEN through the feasibility gate.

---

## 18. Final cold-review verdict

**APPROVE SUBJECT TO LIMITED REVISION.**

The drafts faithfully capture the project.

The corrections above do not change the agreed architecture.

They prevent four specific kinds of future confusion:

1. treating a negative search result as a researched absence;
2. confusing macroblock/coding-grid boundaries with current coded-transform seams in NONE states;
3. overclaiming what the experimental comparisons isolate;
4. accidentally making the FFmpeg/BestSource investigation a blocker for Stage 1 throwaway
   research tooling.

Once those are corrected, I consider the three-document repository set ready for Dave's
ratification review.
