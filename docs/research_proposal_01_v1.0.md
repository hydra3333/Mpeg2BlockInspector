# MPEG-2 Deblocking Stage 0 Research Proposal 01

**Filename:** `research_proposal_01_v1.0.md`  
**Version:** 1.0  
**Date:** 2026-10-06  
**Status:** Agreed research brief for the first independent Stage 0 research pass.  
**Controlling project proposal:** `MPEG2_Macroblock_Index_VapourSynth_Deblocking_Project_Proposal_v0_5.md`

---

## 1. Purpose

This document defines the first independent research pass for Stage 0 of the MPEG-2 Macroblock Index + VapourSynth Deblocking project.

The objective is to investigate MPEG-2 deblocking/post-processing prior art and alternative algorithm approaches before the project commits to a final `.idx2` format or production implementation.

This research is an **evidence input**, not project authority.

Research findings become durable project knowledge only after:

1. independent research and review by ChatGPT and Claude;
2. three-way comparison and challenge between Dave, ChatGPT and Claude;
3. Dave's ratification of the resulting conclusions; and
4. incorporation of ratified conclusions into the repository knowledge files.

The current permanent repository knowledge set is:

- `02_INDEX_FORMAT_SPEC.md`
- `05_DECISIONS.md`
- `06_DEBLOCK_CONCEPT.md`

Research and review documents must not silently become competing authorities.

Working rule:

> Research documents are evidence inputs. Repository knowledge documents become project truth only after Dave's ratification.

---

## 2. Research split

The research is deliberately divided so that ChatGPT and Claude do not simply perform identical searches.

### 2.1 Claude research track

Claude will concentrate primarily on:

- MPEG-2 deblocking/post-processing prior art;
- historical implementations;
- alternative algorithm families;
- evidence for and against metadata-assisted filtering;
- evidence that pixel-only methods may already be sufficient.

### 2.2 ChatGPT research track

ChatGPT will concentrate more heavily on:

- MPEG-2 coding mechanics relevant to filtering;
- macroblock and 8x8 transform geometry;
- frame-DCT versus field-DCT mechanics;
- field-picture versus frame-picture handling;
- MPEG-2 4:2:0 chroma mechanics;
- quantiser semantics;
- metadata semantics and likely value;
- candidate filtering mathematics;
- implementation complexity;
- scalar-reference suitability;
- eventual AVX2 suitability.

### 2.3 Overlap

Some overlap is intentional where independent confirmation is useful.

For interlace and chroma:

- Claude will report what prior art explicitly documents or implements.
- ChatGPT will separately investigate the MPEG-2 coding mechanics themselves.

The two research tracks will later be compared and challenged.

Disagreements are to be preserved explicitly and resolved through targeted verification rather than silently reconciled.

---

## 3. Claude research assignment

Claude is to undertake an independent research pass covering the following questions.

1. Published MPEG-1/MPEG-2 post-decode deblocking and post-processing algorithms.
2. Historical practical implementations in MPEG-2 decoders or video post-processing software.
3. Whether useful approaches filter:
   - 8x8 DCT-block boundaries;
   - 16x16 macroblock boundaries;
   - or both.
4. How prior algorithms distinguish compression blocking from genuine image edges and detail.
5. How quantiser information is used, especially MPEG-2 macroblock quantiser scale.
6. Whether coding information such as:
   - intra/inter/skipped status;
   - coded-block pattern;
   - coefficient activity;
   - motion information;
   materially improves deblocking.
7. Treatment of interlaced MPEG-2 in prior art, including frame-DCT/field-DCT issues where explicitly documented.
8. Treatment of MPEG-2 4:2:0 chroma in prior art.
9. What metadata each promising approach actually requires.
10. Algorithms that appear particularly:
    - simple;
    - deterministic;
    - suitable for a scalar reference implementation;
    - suitable for later AVX2 implementation.
11. Evidence against the proposed metadata-assisted approach, including cases where:
    - pixel-only methods are good enough;
    - codec metadata provides little measurable advantage;
    - implementation complexity is unlikely to justify the gain.
12. Two or three candidate algorithm families worth carrying forward into Stage 0 concept discussion.

Candidate algorithm families are to be labelled **HYPOTHESIS**, because they are design inferences from research rather than researched facts.

No production code is to be written during this research pass.

The `.idx2` format is not to be redesigned during this research pass.

The purpose is to discover what algorithm is worth trying and therefore what metadata the eventual index may actually need.

---

## 4. Evidence discipline

Every substantive research claim must be distinguishable by evidence strength.

### 4.1 Research-status labels

Use the project terminology:

- **RESEARCHED** - supported by a cited source.
- **HYPOTHESIS** - inference, proposal, interpretation, or technical belief not directly established by cited evidence.
- **VERIFIED** - reserved for later project verification by Dave's tests or cold reading of authoritative source code/standards as defined by the controlling proposal.

Claude's research does not become **VERIFIED** merely because it is well sourced.

### 4.2 Source reading depth

For every source, state how deeply it was actually read.

Use one of:

- **FULL TEXT READ**
- **ABSTRACT ONLY**
- **SECONDARY DESCRIPTION**
- **PARTIAL TEXT / EXCERPT**
- another explicit description if none of the above fits.

An abstract-only claim is weaker evidence than a claim based on the full paper, and the research document must not hide that distinction.

### 4.3 Source relevance classification

Each source should be classified, where applicable, by both codec relevance and filtering context.

Codec relevance examples:

- MPEG-2-specific
- MPEG-1-specific
- MPEG-1/MPEG-2
- JPEG/DCT-derived
- generic block-coded video
- H.264/AVC-derived
- other adjacent codec literature

Filtering-context examples:

- post-decode/post-processing
- in-loop codec filter
- encoder-side technique
- decoder-side non-normative enhancement
- generic image restoration
- other

The purpose is to prevent adjacent deblocking literature from being presented as though it were directly MPEG-2-specific.

### 4.4 Publication metadata

For each paper or formal source, record where available:

- title;
- authors;
- publication year;
- journal/conference/venue;
- DOI or other stable identifier where available;
- URL;
- source-reading depth;
- relevance classification.

This is particularly important because later H.264/HEVC-era work may contain useful ideas without being directly applicable to MPEG-2.

### 4.5 Quotation policy

Prefer paraphrase.

Use very short quotations only where wording itself matters.

Preserve URLs and sufficient bibliographic detail so Dave and ChatGPT can independently inspect the originals.

---

## 5. Falsification requirement

The research must make a genuine attempt to show that the proposed metadata-assisted architecture may not be worthwhile.

Item 11 is therefore a first-class research task, not a token counterargument section.

Claude should actively search for evidence that:

- pixel-only deblocking is sufficient;
- codec metadata does not materially improve edge discrimination;
- transform/macroblock metadata creates excessive complexity for little benefit;
- existing generic post-processing approaches already capture most of the available improvement;
- or the particular MPEG-2 artefacts of interest are not well addressed by the proposed architecture.

A negative result is acceptable and useful.

The purpose of Stage 0 is to reduce the risk of building unnecessary infrastructure.

---

## 6. Interlace and chroma division of responsibility

Claude should cover interlace and chroma only from the perspective of documented prior art and historical implementations.

Claude should not attempt to establish the MPEG-2 coding mechanics themselves as project truth.

ChatGPT will separately investigate:

- frame-DCT versus field-DCT transform geometry;
- frame pictures versus field pictures;
- mixed frame/field-DCT behaviour;
- 4:2:0 chroma block structure;
- quantiser and coded-block semantics;
- implications for index metadata.

Any conflict between prior-art descriptions and MPEG-2 coding-mechanics research must be preserved for three-way review.

---

## 7. Research file naming

Original research files use:

`AUTHOR_TOPIC_vX_Y.md`

Examples:

- `Claude_MPEG2_Deblocking_Prior_Art_v0_1.md`
- `ChatGPT_MPEG2_Deblocking_Codec_Mechanics_v0_1.md`

Cross-review files use:

`AUTHOR_REVIEW_OF_OTHER_TOPIC_vX_Y.md`

Examples:

- `Claude_REVIEW_OF_ChatGPT_MPEG2_Deblocking_Codec_Mechanics_v0_1.md`
- `ChatGPT_REVIEW_OF_Claude_MPEG2_Deblocking_Prior_Art_v0_1.md`

The naming convention exists so that:

- original research remains distinguishable from review;
- authorship is obvious;
- version history is mechanically visible;
- three-way review can be reconstructed later;
- research evidence cannot be confused with ratified repository knowledge.

---

## 8. Claude first deliverable

Claude's first deliverable is:

`Claude_MPEG2_Deblocking_Prior_Art_v0_1.md`

Expected characteristics:

- approximately 400-700 lines is acceptable;
- approximately 15-25 searches/page reads is acceptable;
- it is a first serious research pass, not an exhaustive survey;
- known gaps must be listed explicitly;
- uncertainty must be retained explicitly;
- inaccessible/paywalled sources must be identified as such;
- source-reading depth must be stated;
- candidates in item 12 must remain labelled HYPOTHESIS.

---

## 9. File format

Research and review Markdown files should use:

- US-ASCII where practical;
- CRLF line endings;
- mechanically verified line endings/encoding before handoff.

If a necessary citation, author name, title, mathematical symbol, or standard identifier cannot be represented safely in US-ASCII without damaging meaning, preserve correctness first and flag the exception explicitly.

---

## 10. Review process

After the independent first-pass research:

1. Claude supplies `Claude_MPEG2_Deblocking_Prior_Art_v0_1.md`.
2. ChatGPT supplies `ChatGPT_MPEG2_Deblocking_Codec_Mechanics_v0_1.md`.
3. Each AI reviews the other's research.
4. Cross-review files are created using the naming convention in section 7.
5. Dave, ChatGPT and Claude compare:
   - agreements;
   - disagreements;
   - unsupported assumptions;
   - source-quality differences;
   - unresolved technical questions;
   - candidate algorithm families.
6. Dave decides what conclusions are accepted.
7. Only ratified conclusions are incorporated into:
   - `06_DEBLOCK_CONCEPT.md`;
   - `02_INDEX_FORMAT_SPEC.md`, where relevant;
   - `05_DECISIONS.md`, where a project decision has been made.

Research files remain evidence/history, not project authority.

---

## 11. Current decision

This proposal authorises the first independent Stage 0 research pass only.

It does not authorise:

- production filter code;
- final `.idx2` design;
- permanent inspector redesign;
- C++ implementation;
- VapourSynth API integration;
- AVX2 implementation.

Those remain subject to the Stage 0-2 research process and feasibility gate defined by the controlling project proposal.
