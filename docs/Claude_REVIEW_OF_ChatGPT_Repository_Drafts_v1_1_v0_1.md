# Claude - Review of ChatGPT Repository Drafts (05 v1.1, 06 v1.1, 02 v0.4)

**Filename:** `Claude_REVIEW_OF_ChatGPT_Repository_Drafts_v1_1_v0_1.md`
**Version:** 0.1
**Date:** 2026-10-08
**Author:** Claude
**Reviews:** `REPOSITORY_updated.zip`: `05_DECISIONS.md` v1.1, `06_DEBLOCK_CONCEPT.md` v1.1,
`02_INDEX_FORMAT_SPEC.md` v0.4 (all DRAFT / PROPOSED); `Stage1_Evidence_and_Gate_Report_v0_3.md`
**Method:** line diff of each draft against the ratified 05 v1.0 / 06 v1.0 / 02 v0.3; checked
against `Claude_REVIEW_Reconciliation_After_Handover_v0_1.md` (RR), V1-V4 and Dave's rulings.
**Status:** Review input only. Not project authority.

---

## 1. Verdict

**Approve with one MUST change.** The drafts carry every item from RR faithfully and change nothing
else that was ratified, with one exception (K-07, section 3). Format: all four files US-ASCII, CRLF,
zero bare LF (checked). The gate report in the zip is byte-identical in content to the ratified v0.3.

---

## 2. Checks passed

| Check | Result |
|---|---|
| `05` D-01..D-23 text unchanged | Yes. Only additions: index status annotations, labelled "Proposed" amendment/disposition lines, new section 5 (D-24..D-26) |
| Superseded decisions kept, not deleted (D-20) | Yes: D-11, D-17, D-18 marked "proposed supersession by D-24" with text retained |
| D-15 amendment, D-08 amendment, D-23 clarification | Present and worded as RR proposed |
| D-24 and D-25 separate; D-24 stated as scope, not finding | Yes |
| D-26 scope boundary (Q3/Q4/Q7 detail left to Stage 2 design) | Yes |
| `06` section 1 question, 5 item 1, 8.2, 9.1-9.4 | All as RR |
| K-03, K-04 upgraded; K-10 (V3), K-11 (V4) added at exact evidence levels, "not a normative H.262 claim" kept | Yes |
| Same-field chroma filtering kept as a design choice (4.7, K-11, O-14) | Yes |
| Spatial registration check required before quality conclusions (9.1) | Yes |
| Open questions changed by meaning: O-03 closed, O-06 keeps chroma strength/no-harm, O-07/O-08 partly answered, O-10a/b withdrawn, O-01/O-02/O-13 cross-check only, O-14 added | Yes |
| `02`: provisional pointer replaced; contents/packing still unfrozen; `progressive_frame` and picture type named as candidates; C-1..C-5 unchanged | Yes |

---

## 3. MUST CHANGE

### M1 - K-07 has been rewritten without being marked as changed

`06` section 3 says "K-01 to K-09 remain ACCEPTED", but K-07's text is new. It now adds the
coded_block_pattern = 0 case (a dct_type bit may have been read, yet the state is NONE) and the
field-picture note, and cites `ChatGPT_REFERENCE_vs_INTERIM_Source_Comparison_v0_2.md` 9.3.

The new content is correct (it is the derivation rule from my source-comparison review, getvlc.h 250
and getpic.c 388-392). But as drafted it would ride on the 2026-10-06 acceptance of the old wording,
and the change log does not mention it.

Fix: mark K-07 "revised in v1.1 - PROPOSED -> ACCEPTED" like K-10/K-11, and add a change-log line.
Optionally its decoder-semantics part can be labelled VERIFIED (reference decoder, same lines).

---

## 4. SHOULD CHANGE

### S1 - The 9.1 ladder mixes comparisons with development phases

Steps 2 and 3 already need a working kernel, yet step 4 is "kernel / threshold / strength
development". Read literally, the kernel is developed after it is used. Suggest one sentence: "Steps 2
and 3 use an initial candidate kernel frozen for that comparison; step 4 then develops it further."
The detail can live in Stage 2 v0.2.

### S2 - Confirm the existing-filter yardstick ruling

`05` (D-08 annotation, D-26 effect) and `06` 9.3 record that no existing-filter yardstick is planned
and call this Dave's ruling. RR left it as Dave's call; I have not seen the ruling itself. If Dave
did decide it, no change is needed beyond confirming. If not, remove the attribution.

---

## 5. OPTIONAL

1. `06` 8.1 still titles Family A "leading hypothesis"; with Family B gone, "design family" reads
   better.
2. `06` section 2 (ratified v1.0, my own wording) says same-field access is used "where the known
   geometry requires it". That is the imprecision I flagged in ChatGPT's QR answer: same-field access
   is the D-09 rule against mixing fields, not something the geometry requires. Rewording to "where
   filtering across a seam would otherwise mix fields" would remove the ambiguity.
3. `06` 4.4 could add the chroma support figure (4 same-field samples per block), now that K-11
   verifies the parity premise.
4. The D-08 amendment note sits inside the section that is "verbatim from proposal v0.5". It is
   clearly labelled, so the verbatim text is intact; it could move just below the block.
5. I have not seen `ChatGPT_REFERENCE_vs_INTERIM_Source_Comparison_v0_2.md` (cited by K-07); I
   reviewed v0.1. Not blocking, since the K-07 rule is independently checked against source.

---

## 6. At ratification

When Dave ratifies, the ratified versions should flip: D-11, D-17, D-18 to SUPERSEDED; D-15 and D-08
to their amended state; D-24..D-26 to DECIDED; K-07 (revised), K-10, K-11 to ACCEPTED; headers and
change logs to RATIFIED, as was done for v1.0.

---

## 7. Change log

### v0.1 - 2026-10-08

- Cold review of the v1.1/v0.4 repository drafts: one MUST (K-07), two SHOULD, five OPTIONAL.
