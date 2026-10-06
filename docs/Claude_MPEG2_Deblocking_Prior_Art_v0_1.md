# Claude - MPEG-2 Deblocking Prior Art - Research v0.1

**Filename:** `Claude_MPEG2_Deblocking_Prior_Art_v0_1.md`
**Version:** 0.1
**Date:** 2026-10-06
**Author:** Claude (independent research track, Stage 0)
**Status:** EVIDENCE INPUT ONLY. Not project authority. Nothing here is DECIDED or VERIFIED.
**Brief:** `research_proposal_01_v1.0.md` (agreed research brief)
**Controlling proposal:** `MPEG2_Macroblock_Index_VapourSynth_Deblocking_Project_Proposal_v0_5.md`

---

## 0. How to read this document

Labels (project terminology, brief section 4.1):

- **RESEARCHED** - supported by a cited source in the Source Register (section 2), referenced as [Sxx].
- **HYPOTHESIS** - my inference, interpretation or proposal. Not established by the cited evidence.
- Nothing in this document is **VERIFIED**. Only Dave's tests or a cold read of authoritative
  source code/standards can make something VERIFIED.

Every RESEARCHED claim must be read together with the reading depth of its source. A claim
from an ABSTRACT ONLY or SECONDARY DESCRIPTION source is weaker than one from FULL TEXT READ.

Effort actually spent: about 22 web searches and page reads (within the brief's 15-25 range).
This is a first serious pass, not an exhaustive survey. Section 8 lists known gaps.

Format exceptions (brief section 9): diacritics have been removed from two names to stay
US-ASCII: "Bjontegaard" (Bjontegaard with a slashed o) and "Didee" (Didee with an acute e).
No other meaning is affected.

Quotation policy: all source content is paraphrased. No source is quoted verbatim.

---

## 1. Summary in plain English

1. **The practical MPEG-2 prior art is mostly "MPEG-4 Annex F style" 1-D boundary filtering
   on the 8x8 grid, driven by the quantiser.** The MPEG-4 informative post-filter, libpostproc
   (MPlayer/FFmpeg) and DGDecode's in-decoder post-processing are all in this family. They use
   the stream's quantiser per macroblock where available, and an "emulated" fixed quantiser
   when blind. [S01][S02][S03][S06]

2. **Using the real stream quantiser is the one coding-metadata use that is widespread in
   practical MPEG-2 tools.** Practitioner documentation says decoder-integrated post-processing
   (which has the real quantiser) works better than the blind equivalent, but I found no
   measurement of how much better. [S06][S07]

3. **Interlace is handled in prior art, but I found no MPEG-2 post-filter that uses the
   per-macroblock dct_type.** Practical tools switch the whole frame between progressive and
   field-based processing (DGDecode follows the progressive_frame flag per frame). A 2005 MERL
   paper explicitly recognises that one frame can mix frame-based and field-based coding, and
   handles it WITHOUT metadata by testing for horizontal blocking at two positions within each
   field. [S06][S07][S10]

4. **This is the strongest evidence against the project's core premise.** If a pixel-only
   detector can cope with mixed frame/field coding, the dct_type in the index may add little.
   It is not conclusive: MERL report only that their deblocking is comparable to Annex F, with
   no ablation against a dct_type-aware filter. [S10] (HYPOTHESIS on the significance)

5. **The quantiser alone may not need a custom indexer.** FFmpeg's MPEG-2 decoder has, since
   about version 4.4 (2020), been able to export a per-macroblock quantiser table as frame side
   data. A 2026 VapourSynth project already uses this route (for H.264) alongside BestSource.
   I found no evidence that libavcodec exports dct_type. [S18][S19] (the last sentence is
   HYPOTHESIS - absence of evidence)

6. **In-loop codecs (H.264, VC-1) show what fuller metadata is used for:** H.264 sets a
   per-boundary strength from intra/inter, non-zero coefficients and motion differences, with
   QP-scaled thresholds; VC-1 uses field/frame type to choose boundaries and filters same-polarity
   lines only. These are in-loop designs, so they are design ideas, not proof of post-filter
   value. [S12][S22]

7. **Candidate families for Stage 0 (HYPOTHESIS, section 6):** (A) an Annex F / libpostproc-style
   QP-scaled boundary filter with dct_type-selected vertical geometry; (B) a MERL-style
   field-separate pixel-only filter as the control; (C) a shifted-DCT re-quantisation filter
   (spp / Nosratinia family) using the per-macroblock quantiser, as a quality reference.
   The most useful Stage 2 experiment is an ablation: the same filter with and without
   dct_type and quantiser, on ground-truth material.

---

## 2. Source register

Fields: identifier; bibliographic detail; URL; reading depth; codec relevance; filtering context.
Where publication detail is uncertain or conflicting, that is stated.

### S01 - Kim, Yi, Kim, Ra (1999): two-mode deblocking filter

- S. D. Kim, J. Yi, H. M. Kim, J. B. Ra, "A deblocking filter with two separate modes in
  block-based video coding", IEEE Transactions on Circuits and Systems for Video Technology,
  vol. 9, no. 1, February 1999. Page range CONFLICTS between sources: 156-160 (patent
  citations) versus 156-169 (CiNii). An earlier version appeared at VCIP '98, SPIE vol. 3309,
  pp. 252-259 (1998).
- URLs: https://dspace.kaist.ac.kr/handle/10203/75582?mode=full ;
  https://cir.nii.ac.jp/crid/1571135649279334400 ;
  https://dspace.kaist.ac.kr/handle/10203/115388
- Depth: ABSTRACT ONLY.
- Relevance: generic block-based video (low bit-rate, H.263/MPEG-4 era). 8x8 DCT.
- Context: post-decode/post-processing.

### S02 - MPEG-4 Part 2 informative post-processing (Annex F, "F.3")

- ISO/IEC 14496-2:2001, Information technology - Coding of audio-visual objects - Part 2:
  Visual, 2nd edition, informative annex on post-processing for coding noise reduction.
  Standard itself NOT read (paywalled).
- Described in: US patents 8139651 and 7729426 ("Video deblocking filter"), RE42516 and related
  reissues ("Method of removing blocking artifacts..."), 8369420 ("Multimode filter...").
  URLs: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8139651 ;
  https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/RE42516 ;
  https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8369420
- Depth: SECONDARY DESCRIPTION (patent text excerpts).
- Relevance: MPEG-4 Part 2, 8x8 DCT; directly adjacent to MPEG-1/2 (same block size).
- Context: decoder-side non-normative post-processing.

### S03 - libpostproc (MPlayer/FFmpeg), M. Niedermayer, 2001-2003 onward

- FFmpeg libpostproc, postprocess.c / postprocess.h, Doxygen pages (versions 0.5 to 2.7 and
  trunk group page).
- URLs: https://ffmpeg.org/doxygen/0.11/postprocess_8h.html ;
  https://ffmpeg.org/doxygen/2.7/postprocess_8c.html ;
  https://ffmpeg.org//doxygen/trunk/group__lpp.html
- Depth: PARTIAL TEXT / EXCERPT (API signatures, filter table, function comments; not the
  algorithm source).
- Relevance: used with MPEG-1/2/4-family decoders; 8x8 grid.
- Context: decoder-side non-normative post-processing.

### S04 - FFmpeg spp / fspp / pp7 / uspp filters

- FFmpeg libavfilter vf_spp, vf_fspp, vf_pp7, vf_uspp (ported from MPlayer libmpcodecs,
  Niedermayer and others; FFmpeg ports from 2013).
- URLs: https://trac.ffmpeg.org/wiki/Postprocessing?version=9 ;
  https://ffmpeg.org/doxygen/trunk/libavfilter_2vf__fspp_8c.html ;
  https://ffmpeg.org/pipermail/ffmpeg-devel/2013-June/144596.html
- Depth: PARTIAL TEXT / EXCERPT (wiki, Doxygen, mailing-list patch).
- Relevance: generic 8x8 DCT; uses stream QP where available.
- Context: post-decode.

### S05 - Nosratinia: re-application of JPEG

- A. Nosratinia, "Enhancement of JPEG-compressed images by re-application of JPEG", Kluwer
  Academic Publishers journal article. Venue/year UNCERTAIN: the FFmpeg source comment dates it
  1999 and names it "Embedded Post-Processing for Enhancement of Compressed Images"; the preprint
  footer reads Kluwer 2002. I believe (HYPOTHESIS, not checked) it appeared in the Journal of VLSI
  Signal Processing.
- URL: http://www.utdallas.edu/~aria/papers/vlsisp99.pdf
- Depth: FULL TEXT READ (preprint).
- Relevance: JPEG/DCT-derived (8x8). Directly the basis of FFmpeg fspp [S04].
- Context: generic image post-processing.
- Also used as a SECONDARY source for its literature review (Reeve and Lim 1984; Ramamurthi and
  Gersho 1986; Zakhor 1992; Yang, Galatsanos, Katsaggelos 1993/1995; Minami and Zakhor 1995;
  Xiong, Orchard, Zhang 1997; Chou, Crouse, Ramchandran 1998; Shen and Kuo 1998 review).

### S06 - DGDecode / MPEG2Dec3 documentation

- DGDecode manual (DGMPGDec package; based on MPEG2Dec3 v1.10, itself from MPEG2Dec2).
  URL: https://www.rationalqm.us/dgmpgdec/DGDecodeManual.html
- Mirrors: https://avisynth.org.ru/docs/english/externalfilters/dgdecode.htm ;
  https://avisynth.org.ru/docs/english/externalfilters/mpeg2dec3.htm
- Depth: FULL TEXT READ of the manual page as served (the parameter table text did not render;
  parameter meanings taken from the mirrors, PARTIAL).
- Relevance: MPEG-1/MPEG-2-specific decoder.
- Context: decoder-side non-normative post-processing (in-decoder, with stream quantiser), plus
  a blind variant (BlindPP).

### S07 - Doom9 forum threads (practitioner sources)

- t-98205 (2005): DGDecode iPP behaviour.
  https://forum.doom9.org/archive/index.php/t-98205.html
- p=914166 (circa 2006): "All existing deblocking algorithms implementations" survey thread.
  https://forum.doom9.org/showthread.php?p=914166
- t-38231 (2002): deblocking non-MPEG sources; quantiser information lost after decoding.
  https://forum.doom9.org/archive/index.php/t-38231.html
- t-90420 (2005): DGMPGDec 1.2.1 release notes (adds Manao's Deblock).
  https://forum.doom9.org/archive/index.php/t-90420.html
- Depth: SECONDARY DESCRIPTION (forum posts; opinion and practice, not measurement).
- Relevance: MPEG-1/2 practice (AviSynth era).
- Context: post-decode.

### S08 - Deblock_QED (AviSynth script, Didee)

- Script versions from 2006-2008, AviSynth wiki (http://avisynth.nl/index.php/Deblock_QED,
  not fetched); code excerpts read in forum posts.
- URLs: https://forum.doom9.org/showthread.php?p=949526 ;
  https://forum.doom9.org/showthread.php?p=1061390 ;
  https://www.digitalfaq.com/forum/video-restore/8785-different-types-noise-post54893.html
- Depth: PARTIAL TEXT / EXCERPT (script fragments and author comments).
- Relevance: generic 8x8 grid; widely used on MPEG-2 material.
- Context: post-decode, pixel-only (blind).

### S09 - Manao's Deblock (H.264-derived blind deblocker)

- Included in DGDecode from DGMPGDec 1.2.1 (2005) [S07 t-90420]; parameters quant, aOffset,
  bOffset [S06].
- Depth: SECONDARY DESCRIPTION.
- Relevance: H.264/AVC-derived algorithm applied blind to an 8x8 grid.
- Context: post-decode, pixel-only.

### S10 - Nie, Kong, Vetro, Sun, Barner (2005): interlaced fuzzy post-filtering

- Y. Nie, H.-S. Kong, A. Vetro, H. Sun, K. E. Barner, "Fast adaptive fuzzy post-filtering for
  coding artifacts removal in interlaced video", IEEE ICASSP 2005, vol. 2, pp. 993-996.
  MERL Technical Report TR2005-018. (MERL's BibTeX lists four authors; the paper lists five.)
- URLs: https://www.merl.com/publications/TR2005-018 ;
  https://shadow.merl.com/publications/docs/TR2005-018.pdf
- Depth: FULL TEXT READ (technical report version; one table and some equations garbled in
  extraction).
- Relevance: interlaced SD video (720x576 and 720x480 test sequences); block-DCT video. The
  codec is not named in the text I read; HYPOTHESIS that it is MPEG-2-class material.
- Context: post-decode, pixel-only.

### S11 - MERL earlier/companion papers

- H.-S. Kong, Y. Nie, A. Vetro, H. Sun, K. E. Barner, "Adaptive fuzzy post-filtering for highly
  compressed video", IEEE ICIP 2004, vol. 3, pp. 1803-1806. MERL TR2004-131.
  https://www.merl.com/publications/TR2004-131
- Y. Nie et al., "Implementation of edge map guided fuzzy filtering for artifact reduction in
  highly compressed video", IEEE ICCE 2005, pp. 325-326. MERL TR2005-007.
  https://merl.com/publications/TR2005-007
- Depth: ABSTRACT ONLY / PARTIAL (search excerpts).
- Relevance: generic block-DCT video. Context: post-decode.

### S12 - List et al. (2003): H.264/AVC adaptive deblocking filter

- P. List, A. Joch, J. Lainema, G. Bjontegaard, M. Karczewicz, "Adaptive deblocking filter",
  IEEE Transactions on Circuits and Systems for Video Technology, vol. 13, no. 7,
  pp. 614-619, July 2003. DOI 10.1109/TCSVT.2003.815175.
- URL (copy): https://mcube.lab.nycu.edu.tw/wiki/core/uploads/Research/SelectedTopics/Adaptive%20Deblocking%20filter.pdf
- Depth: PARTIAL TEXT / EXCERPT (first pages via search) plus SECONDARY descriptions
  (Wikipedia "Deblocking filter"; patent summaries of boundary strength).
- Relevance: H.264/AVC-derived. Context: in-loop codec filter.

### S13 - US patent 8326064: MPEG-2 metadata steering deblocking in re-encoding

- "Image re-encoding method to decode image data which is orthogonally transformed per first
  block and encoded by a first encoding method".
  https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8326064
- Depth: PARTIAL TEXT / EXCERPT.
- Relevance: MPEG-2 input, H.264 output (transcoding).
- Context: encoder-side technique (sets the H.264 encoder's deblocking from MPEG-2 metadata).

### S14 - "Reduced complexity MPEG2 video post-processing for HD display"

- IEEE Xplore document 4607548. Authors, venue and year NOT confirmed (the Xplore page did not
  render; ResearchGate listing suggests circa 2008).
  https://ieeexplore.ieee.org/document/4607548/ ;
  https://www.researchgate.net/publication/224327503_Reduced_complexity_MPEG2_video_post-processing_for_HD_display
- Depth: ABSTRACT ONLY. Caution: the ResearchGate search snippet mixes text from several
  related papers, so only the Xplore abstract wording is relied on.
- Relevance: MPEG-2-specific. Context: decoder-side post-processing.

### S15 - "Reduction of blocking artifacts in MPEG-2 video using a block classification technique"

- Authors, venue and year NOT identified (ResearchGate 3852166; the page refused access).
  https://www.researchgate.net/publication/3852166_Reduction_of_blocking_artifacts_in_MPEG-2_video_using_a_block_classification_technique
- Depth: ABSTRACT ONLY (truncated search snippet).
- Relevance: MPEG-2-specific. Context: post-decode, uses coding information.

### S16 - Liu and Bovik (2002): DCT-domain blind measurement and reduction

- S. Liu, A. C. Bovik, "Efficient DCT-domain blind measurement and reduction of blocking
  artifacts", IEEE TCSVT, vol. 12, no. 12, pp. 1139-1149, December 2002.
- URL (draft): https://www.live.ece.utexas.edu/publications/2002/sliu_csvt2002_dctblind.pdf
- Depth: PARTIAL TEXT / EXCERPT (draft fragments via search).
- Relevance: JPEG/DCT-derived; mentions video post-processing. Context: generic restoration,
  blind.

### S17 - Jiang, Zhang, Timofte (2021): FBCNN

- J. Jiang, K. Zhang, R. Timofte, "Towards flexible blind JPEG artifacts removal", ICCV 2021,
  pp. 4997-5006. DOI 10.1109/ICCV48922.2021.00495. arXiv 2109.14573.
  https://openaccess.thecvf.com/content/ICCV2021/html/Jiang_Towards_Flexible_Blind_JPEG_Artifacts_Removal_ICCV_2021_paper.html
- Depth: ABSTRACT ONLY plus SECONDARY review summary.
- Relevance: JPEG; deep learning. Context: generic restoration.

### S18 - FFmpeg per-macroblock QP export for MPEG-2 (AVVideoEncParams)

- FFmpeg commit "mpegvideo: use the AVVideoEncParams API for exporting QP tables"
  (A. Khirnov; tagged n4.4 era; APIchanges entry dated 2020 adds AV_VIDEO_ENC_PARAMS_MPEG2).
  https://git.kx.studio/falkTX/FFmpeg/commit/baecaa16c16dc2bca7ca15ed3c379d7343955adb
- Related: libavutil/video_enc_params.h,
  https://code.ffmpeg.org/Traneptora/FFmpeg/src/branch/master/libavutil/video_enc_params.h ;
  tools/venc_data_dump.c (example consumer).
- Depth: PARTIAL TEXT / EXCERPT (commit summary and header comments).
- Relevance: MPEG-2 decoder metadata export. Context: decoder infrastructure, not a filter.

### S19 - QPMBDeblock (PyPI, 2026)

- QPMBDeblock 0.5.0, authors PingWer and Mhanz3500, released 2026-09-20, licence CC BY-NC-SA
  4.0. https://pypi.org/project/QPMBDeblock/ ; https://github.com/PingWer/QPMBDeblock
- Depth: FULL TEXT READ (project description page only; code not read).
- Relevance: H.264 only (NOT MPEG-2). Context: VapourSynth post-decode, metadata-assisted.

### S20 - VapourSynth-DeblockPP7

- HomeOfVapourSynthEvolution/VapourSynth-DeblockPP7 README.
  https://github.com/HomeOfVapourSynthEvolution/VapourSynth-DeblockPP7
- Depth: PARTIAL TEXT (README).
- Relevance: generic 8x8 DCT. Context: VapourSynth post-decode, constant QP only.

### S21 - Selur forum (2026): practitioner deblocker choice

- "Deblocking filters requested for HD version of ..." thread, January 2026.
  https://forum.selur.net/archive/index.php/thread-4302.html
- Depth: SECONDARY DESCRIPTION (one practitioner's opinion; HD source of unstated codec).
- Relevance: weak. Context: post-decode, includes neural deblocking (DPIR).

### S22 - Microsoft patent application: in-loop deblocking for interlaced video (VC-1)

- US 2005/0084012, "In-loop deblocking for interlaced video".
  https://patents.justia.com/patent/20050084012
- Depth: ABSTRACT ONLY.
- Relevance: VC-1/WMV9 interlaced frame-coded pictures. Context: in-loop codec filter.

### S23 - US patent 6320905: low-memory MPEG post-processor

- "Postprocessing system for removing blocking artifacts in block-based codecs".
  https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6320905
- Depth: PARTIAL TEXT / EXCERPT.
- Relevance: MPEG video below about 4 Mbit/s. Context: post-decode, pixel-only.

### S24 - US patents 7539248 / 7496141 / 7400679 / 7397854: adaptive de-blocking for MPEG decoders

- "Adaptive de-blocking filtering apparatus and method for MPEG video decoder".
  https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7496141
- Depth: PARTIAL TEXT / EXCERPT (background section).
- Relevance: MPEG-1/2 decoders. Context: post-decode.

### S25 - Adaptive post-filtering using DC-predicted AC activity

- "Adaptive post-filtering for reducing blocking and ringing artifacts in low bit-rate video
  coding", Signal Processing: Image Communication (ISSN 0923-5965). Authors, volume and year NOT
  confirmed.
  https://datalearner.com/academic/journal-papers/0923-5965/volumes-and-issues/79/paper-detail/103023
- Depth: ABSTRACT ONLY.
- Relevance: generic block-based video; tested with an H.263+ (TMN8) decoder.
- Context: post-decode.

---

## 3. Findings by research question

### Q1. Published MPEG-1/MPEG-2 post-decode deblocking algorithms

- RESEARCHED: The most influential published post-filter in the MPEG family is the two-mode
  filter of Kim et al. (1999), which selects between a strong mode for flat regions and a
  frequency-based smoothing mode elsewhere, filtering 1-D across block boundaries in each
  direction. It was adopted as an informative post-processing filter in MPEG-4 Part 2.
  [S01][S02][S24]
- RESEARCHED: Earlier general block-DCT post-processing (1984-1998) falls into a few families:
  space-invariant low-pass filtering (found inadequate); space-varying filtering with block or
  boundary classification; projection onto convex sets (POCS) and constrained optimisation;
  MAP estimation with Markov random field priors (computationally heavy); and oversampled
  wavelet or transform-domain denoising. [S05, secondary]
- RESEARCHED: Shifted re-quantisation (re-apply the block transform and quantiser at many
  pixel shifts, then average) was reported to match or beat POCS, wavelet and adaptive filters
  on JPEG test images, at moderate cost, and is the basis of FFmpeg's fspp. [S05][S04]
- RESEARCHED: MPEG-2-specific post-processing papers exist (block classification using coding
  information; reduced-complexity HD-display post-processing), but I could read only their
  abstracts. [S14][S15]
- HYPOTHESIS: Most MPEG-2-specific academic work I found is either consumer-electronics
  hardware oriented (TV post-processing) or general block-DCT work evaluated on MPEG test
  sequences. I found little that is genuinely MPEG-2-syntax-aware.

### Q2. Historical practical implementations

- RESEARCHED: libpostproc provides horizontal and vertical deblocking (hb/vb and the faster
  h1/v1 variants), an "accurate" deblock variant, and deringing. Its entry point takes the
  frame, a per-macroblock QP table with a stride, and the picture type. [S03]
- RESEARCHED: One libpostproc filter's own comment notes that it can only smooth blocks at
  the expected grid positions and cannot follow blocks that have moved. [S03]
- RESEARCHED: FFmpeg's spp, fspp, pp7 and uspp filters use the QP stored in the stream for each
  area unless the user forces a constant QP. A "use_bframe_qp" option exists because B-frames
  often have larger QP. [S04]
- RESEARCHED: DGDecode (the dominant AviSynth MPEG-2 decoder) performs deblocking and deringing
  inside the decoder, with separate switches for luma horizontal, luma vertical, chroma
  horizontal and chroma vertical deblocking, plus sensitivity controls (moderate_h,
  moderate_v). Its blind counterpart BlindPP uses an "emulated quantizer" instead. [S06]
- RESEARCHED: The DGDecode documentation tells users not to use BlindPP on MPEG2Source output
  because the decoder's own post-processing works better; the MPEG2Dec3 page describes BlindPP
  as less accurate than decoder-integrated post-processing but still efficient. [S06]
- RESEARCHED: Deblock_QED (pixel-only) runs two instances of an H.264-style deblocker, one tuned
  for 8x8 block borders and one for block interiors, and composites them through an 8x8 grid
  mask. [S08]
- RESEARCHED: VapourSynth has DeblockPP7 (constant QP only, no per-macroblock table). [S20]
- RESEARCHED: A 2026 VapourSynth tool extracts per-macroblock QP and macroblock maps from H.264
  via libavcodec side data, frame-synchronised with a BestSource clip, and uses them to guide
  deblocking. It does not support MPEG-2. [S19]
- RESEARCHED: Practitioners in 2002 already identified the core problem: once video is
  decoded, the quantiser information is lost to downstream filters, and they proposed passing
  it from the source filter to the deblocker. [S07 t-38231]

### Q3. 8x8 DCT-block boundaries, 16x16 macroblock boundaries, or both

- RESEARCHED: Every practical filter I found operates on the 8x8 grid (libpostproc, Annex F,
  DGDecode, Deblock_QED, BlindPP). DGDecode explicitly requires 8-pixel alignment (no crop or
  resize before deblocking). [S02][S03][S06][S08]
- RESEARCHED: MERL found that with interlaced, mixed frame/field coding, horizontal blocking can
  appear not only at the 8x8 horizontal block boundary but also along the horizontal centreline
  of the block, as seen within a field. [S10]
- RESEARCHED: Motion compensation is a second source of blocking in MPEG-1/2: copying a block from
  a reference frame can create a discontinuity at the edge of the copied block, and existing
  blocking in the reference propagates into the current frame. [S24]
- RESEARCHED: H.264's in-loop filter treats macroblock edges more strongly than internal block
  edges under some conditions (for example, intra macroblock edges). [S12]
- HYPOTHESIS: Because MPEG-2 motion compensation works at macroblock granularity (16x16, or
  16x8 for field prediction), 16x16 edges of inter macroblocks may carry motion-compensation
  steps even where no residual was coded. No MPEG-2 post-filter I found treats 16x16 edges
  differently from 8x8 edges. This is a question for experiment and for ChatGPT's mechanics
  track.

### Q4. Distinguishing blocking from genuine edges

RESEARCHED techniques found:

- **Step versus local activity.** If the discontinuity at a boundary is small relative to local
  activity, it is likely quantisation; very large steps are treated as edges and filtered mildly
  or not at all (Chou et al. 1998, via [S05]).
- **Flatness count plus QP range test.** Annex F counts near-equal neighbouring pixel pairs
  across a 10-pixel span (threshold THR1, typically 2) to choose flat-region "DC offset" mode
  (count at least THR2, typically 6). In that mode it filters only if the max-min range of the
  boundary pixels is under twice the QP. [S02]
- **QP-gated min/max checks** in libpostproc (functions taking QP). [S03]
- **Gap detection in the field domain** (MERL): a row is marked when the step across the
  boundary exceeds every neighbouring pixel difference on one side; a boundary is declared
  blocky when enough rows are marked. Horizontal edges in fields need stricter tests, including
  checks of neighbouring vertical boundaries. [S10]
- **Implicit, transform-domain** (spp family): re-quantising shifted DCTs with the original
  quantiser preserves strong edges because large coefficients survive. [S05]
- **Edge-preserving weights** (MERL fuzzy filters): weights fall with intensity difference from
  the centre pixel. [S10][S11]
- **Clamped correction** with QP-derived thresholds (H.264 alpha, beta, and clipping). [S12]

### Q5. How quantiser information is used

- RESEARCHED: Annex F uses QP directly as a threshold (range under 2 x QP) and in the default
  mode's limits. [S02]
- RESEARCHED: libpostproc consumes a per-macroblock QP table plus picture type. [S03]
- RESEARCHED: spp/fspp derive their DCT thresholds from QP (the patch shows a threshold scaled
  by qp) and take QP from the stream when available. [S04]
- RESEARCHED: Nosratinia found the best denoising when the secondary quantisation equalled the
  original quantisation matrix; scaling it up or down was worse. The method needs the
  quantisation matrix as well as the scale. [S05]
- RESEARCHED: H.264 derives its decision thresholds from QP. [S12]
- RESEARCHED: A forum design discussion notes that knowing the quantiser and quantiser matrix
  per block bounds the possible coefficient error, but that for inter blocks the coded
  coefficients belong to the motion-compensated residual, not the picture. [S07 p=914166]
- RESEARCHED: One MPEG-2 post-processing paper's abstract describes a DCT-based control scheme;
  a search snippet suggests the quantiser was estimated from the decoded stream rather than read
  from it. [S14] (weak - snippet)
- RESEARCHED: Deep-learning work finds that estimating a compression-level parameter (JPEG
  quality factor) and conditioning on it improves blind restoration, and lets the user trade
  artefact removal against detail. [S17]
- HYPOTHESIS: The MPEG-2 quantiser semantics (quantiser_scale_code versus the actual scale under
  q_scale_type, plus intra/non-intra matrices) are NOT the same unit as MPEG-4 or H.264 QP.
  Any borrowed QP threshold needs re-derivation. This belongs to ChatGPT's track.
- HYPOTHESIS: Per-macroblock quantiser is the best-supported metadata item in the prior art,
  both by practice and by the deep-learning finding that knowing the compression level helps.

### Q6. Do intra/inter/skipped, coded-block pattern, coefficient activity or motion help?

- RESEARCHED: In H.264 (in-loop), boundary strength depends on intra coding, presence of
  non-zero coefficients, reference pictures and motion-vector differences. Boundaries between
  inter blocks with no coefficients and matching motion get no filtering. [S12]
- RESEARCHED: An MPEG-2-to-H.264 re-encoding patent sets deblocking on/off and strength from
  MPEG-2 picture type, intra macroblock type, quantiser scale and DCT type. [S13]
- RESEARCHED: Several post-filters predict or measure block activity from DC values or DCT
  coefficients to classify blocks (for example S15's abstract mentions coding information such
  as DCT data; another post-filter predicts low-frequency AC activity from the DC values of a
  block and its eight neighbours, then filters low- and high-activity blocks differently).
  [S15][S25]
- RESEARCHED: libpostproc takes picture type; spp exposes a B-frame QP option. [S03][S04]
- GAP: I found NO MPEG-2 post-processing study that measures the benefit of intra/inter/skipped
  status, coded-block pattern or motion vectors over a QP-only or pixel-only filter.
- HYPOTHESIS: The H.264 logic (skip filtering between coefficient-free inter blocks with matching
  motion) does not transfer directly to a post-filter, because in MPEG-2 the reference picture's
  blocking is copied into such blocks and is still visible. The post-filter cannot assume these
  boundaries are clean.

### Q7. Interlaced MPEG-2 in prior art

- RESEARCHED: DGDecode offers field-based post-processing (iPP). If iPP is not set, it follows
  the progressive_frame flag picture by picture; forcing it is advised only when that flag is
  unreliable. [S06][S07 t-98205]
- RESEARCHED: MPEG2Dec3's documentation recommends field-based post-processing for interlaced
  sources. [S06]
- RESEARCHED: MERL (2005) state that a single interlaced frame may be coded with frame-based and
  field-based coding jointly, which makes the artefacts more complicated. They process each
  field separately, check vertical boundaries per field, and check horizontal blocking at both
  the 8x8 block boundary and the block centreline within the field, with stricter detection
  because field vertical resolution is halved. They do this without coding information. [S10]
- RESEARCHED: In VC-1's in-loop filter for interlaced frame-coded pictures, filtering uses only
  lines of the same field polarity, and boundary selection uses field/frame type and transform
  size information. [S22]
- GAP / possibly novel: I found no MPEG-2 POST-filter that uses the per-macroblock dct_type to
  choose filtering geometry. Either this does not exist publicly, or my search missed it.
- HYPOTHESIS: MERL's "centreline" observation is consistent with field-DCT macroblocks in a frame
  picture, but whether it exactly matches MPEG-2 field-DCT geometry is a question for ChatGPT's
  mechanics track and for the standard.

### Q8. 4:2:0 chroma in prior art

- RESEARCHED: DGDecode and libpostproc-derived tools switch chroma horizontal and vertical
  deblocking separately from luma. [S06]
- RESEARCHED: The MPEG-4 informative deblocking filter is applied to both luminance and
  chrominance. [S02]
- RESEARCHED: H.264's in-loop filter treats luma and chroma edges differently. [S12]
- GAP: I found nothing in the prior art about interlaced 4:2:0 chroma specifically (for example
  whether chroma deblocking should be field-based when luma is). The question Dave raised about
  chroma blocking remains open on the prior-art side.

### Q9. Metadata each approach requires

| Approach | Metadata used | Source |
|---|---|---|
| Annex F / Kim et al. two-mode | per-block QP | [S01][S02] |
| libpostproc | per-MB QP table, picture type | [S03] |
| DGDecode in-decoder PP | stream quantiser; progressive_frame (per picture) | [S06][S07] |
| BlindPP / Deblock / Deblock_QED | none (user "emulated" quant / strength) | [S06][S08][S09] |
| spp / fspp / pp7 | per-MB QP (or constant); B-frame QP option | [S04][S20] |
| Nosratinia re-application | quantiser matrix and scale | [S05] |
| MERL interlaced fuzzy | none (pixel-only, field-aware) | [S10] |
| H.264 in-loop | QP, intra, non-zero coeffs, refs, MVs | [S12] |
| VC-1 interlaced in-loop | field/frame type, transform size | [S22] |
| MPEG-2-to-H.264 re-encode | picture type, intra, q scale, DCT type | [S13] |

HYPOTHESIS: For MPEG-2 post-filtering, the prior art supports QP as clearly useful, picture type
as occasionally used, and dct_type as plausible but untested.

### Q10. Simple, deterministic, scalar-then-AVX2 candidates

- RESEARCHED: Annex F-style filtering is 1-D, integer, operates on short pixel runs either side
  of the boundary, and was implemented with MMX/SSE in libpostproc and DGDecode. [S02][S03][S06]
- RESEARCHED: The MERL interlaced filter reduced fuzzy-weight cost by replacing a Gaussian with
  a piecewise linear function and reported run times comparable to the MPEG-4 method. [S10]
- RESEARCHED: Shifted re-quantisation costs, by the author's own analysis, roughly 58
  multiplications and 254 additions per pixel when half the shifts are skipped; it is regular
  DCT work, and fast variants exist (fspp). [S05][S04]
- RESEARCHED: Iterative POCS and MAP methods are computationally heavy. [S05]
- HYPOTHESIS: Annex F-style filters are the best fit for a scalar reference followed by AVX2.
  Fuzzy filters involve per-pixel data-dependent weights and divisions, which vectorise less
  cleanly. The spp family vectorises well but is several times more expensive.

### Q11. Evidence against the metadata-assisted approach

The brief makes this a first-class task. Findings, strongest first:

1. **Pixel-only handling of mixed frame/field coding exists.** MERL handle the exact problem
   that motivates carrying dct_type, without any coding information, and report deblocking
   comparable to the MPEG-4 method at similar cost. [S10] Limits: no ablation against a
   metadata-aware filter; four test sequences; subjective deblocking comparison.
2. **The quantiser can be had without a custom indexer.** FFmpeg's MPEG-2 decoder can export
   per-macroblock QP on request. A VapourSynth project already pairs such side data with
   BestSource for H.264. If the gate shows that QP is the only metadata worth having, the
   reference-decoder indexer may be unnecessary. [S18][S19] (HYPOTHESIS that BestSource does or
   could pass this through; not checked.)
3. **Blind filters are the norm in practice.** Practitioners widely use BlindPP, Deblock and
   Deblock_QED on MPEG-2 sources, and in 2026 at least one recommends neural deblocking (DPIR)
   over conventional filters. [S06][S08][S21] (S21 is anecdotal and about an HD source.)
4. **Blind compression-level estimation works for JPEG.** FBCNN predicts the quality factor
   from pixels and uses it to steer restoration. [S17] Limits: JPEG, not video; one global
   factor, not per-macroblock.
5. **The only claim that the stream quantiser helps is qualitative.** DGDecode documentation says
   decoder-integrated post-processing is better than BlindPP, but gives no measurement. [S06]
6. **Post-filters cannot stop propagation.** Motion compensation copies existing blocking from
   reference pictures into the current picture, and a post-filter cannot prevent that. [S24]
   HYPOTHESIS: this limits every post-filter equally, but it means inter
   pictures may show reference-picture blocking at positions and strengths that the current
   picture's own metadata does not describe.
7. **Grid assumption is fragile to any shift.** FBCNN found existing methods fail on non-aligned
   double compression even with a one-pixel shift; DGDecode requires exact 8-pixel alignment.
   [S17][S06] HYPOTHESIS: low risk for this project (no crop or resize before filtering), but
   any capture chain that re-encodes or rescales would break every grid-based method.

HYPOTHESIS overall: the prior art does not show that dct_type metadata is necessary; it does
weakly support per-macroblock QP. The project's distinguishing bet (dct_type-aware geometry)
is untested rather than refuted. That makes it a legitimate experiment, provided the experiment
is designed to falsify it (section 6.4).

---

## 4. Specific observations relevant to this project

- HYPOTHESIS: Dave's mixed field/frame recollection is consistent with MERL's statement that a
  single interlaced frame may combine frame-based and field-based coding. [S10]
- HYPOTHESIS: The per-picture approach in DGDecode (switch whole frames to field mode) cannot
  represent the per-macroblock mixing that Dave's inspector output shows within single rows.
  This is the gap the index could fill, if it matters visually.
- HYPOTHESIS: Because the target material is VHS-sourced, analogue noise may dominate fine
  detail and partly mask blocking. That could favour simpler filters and reduce the measurable
  benefit of metadata. Only Dave's clips can settle this.

---

## 5. Points to raise with ChatGPT's mechanics track

These are places where my prior-art findings depend on coding mechanics I have deliberately not
researched (brief section 6).

1. Does MERL's horizontal "block centreline within a field" correspond exactly to MPEG-2
   field-DCT luma geometry in frame pictures? [S10]
2. How should a QP threshold borrowed from Annex F or libpostproc map onto MPEG-2
   quantiser_scale_code, q_scale_type and the intra/non-intra matrices?
3. What exactly does libavcodec's MPEG-2 export (AV_VIDEO_ENC_PARAMS_MPEG2) contain: the code,
   the scale, per-macroblock or per-slice, and in display order? Does it cover skipped
   macroblocks? [S18]
4. Does any libavcodec interface expose dct_type per macroblock? (I found none.)
5. Interlaced 4:2:0 chroma: is chroma block geometry affected by dct_type? (Prior art is silent.)
6. Are 16x16 inter-macroblock edges in MPEG-2 systematically different from internal 8x8 edges
   because of macroblock-granular motion compensation? [S24]

---

## 6. Candidate algorithm families for Stage 0 (ALL HYPOTHESIS)

These are design inferences, not findings. Each is chosen so that it can be tested against the
others on ground-truth material.

### 6.1 Family A - QP-scaled two-mode boundary filter, with dct_type-selected geometry

- Basis: Annex F / Kim et al. two-mode filter and libpostproc. [S01][S02][S03]
- Idea: filter 1-D across 8x8 boundaries; choose flat-region or detail mode from a local
  flatness count; gate and limit corrections by the per-macroblock quantiser; select the
  vertical (horizontal-edge) geometry per macroblock from dct_type (frame lines versus field
  lines), in the spirit of VC-1's same-polarity filtering [S22].
- Metadata: per-macroblock quantiser (with correct MPEG-2 semantics); dct_type; picture
  structure; optionally intra/skipped.
- Global strength: scales the QP-derived thresholds and correction limits (consistent with
  proposal D-07).
- Fit: integer, short-support, proven SIMD history. Strong scalar-then-AVX2 candidate.
- Risk: QP mapping must be re-derived for MPEG-2; mixed-DCT neighbour boundaries need a rule.

### 6.2 Family B - field-separate pixel-only filter (the control)

- Basis: MERL interlaced fuzzy post-filter [S10], optionally with Annex F-style 1-D filtering
  in place of fuzzy weights.
- Idea: process each field; test vertical boundaries per field; test horizontal blocking at
  both candidate positions with stricter rules; no metadata (or QP only as an optional gate).
- Metadata: none (or QP only).
- Purpose: this is the falsification baseline. If Family A cannot beat Family B on Dave's
  material, dct_type is not worth indexing.

### 6.3 Family C - shifted-DCT re-quantisation with per-macroblock quantiser

- Basis: Nosratinia, FFmpeg spp/fspp/pp7. [S04][S05]
- Idea: re-quantise shifted 8x8 DCTs using the actual MPEG-2 quantiser (and matrix) of the
  macroblock under each pixel, then average; optionally run on fields for field-DCT
  macroblocks.
- Metadata: per-macroblock quantiser and quantiser matrices; dct_type if field-aware.
- Fit: heavier (tens of multiplies per pixel) but regular and vectorisable.
- Purpose: a quality reference that uses the quantiser in its most principled way. Possibly too
  slow or too soft for production.

### 6.4 Suggested Stage 2 ablation (HYPOTHESIS)

Run on ground-truth encodes and on Dave's clips:

1. unfiltered;
2. Family B (no metadata);
3. Family A with QP only (dct_type ignored, MERL-style dual-position detection);
4. Family A with QP and dct_type;
5. optionally Family C.

The difference between 3 and 4 is the measured value of dct_type. The difference between 2 and
3 is the measured value of QP. These two numbers are what the feasibility gate needs.

---

## 7. What the eventual index might need (HYPOTHESIS, not a redesign)

The brief forbids redesigning `.idx2`; this only records what the families above would consume.

- Family A: quantiser (MPEG-2 semantics settled), dct_type, picture structure; possibly
  intra/skipped.
- Family B: nothing, or quantiser only.
- Family C: quantiser and quantiser matrices (intra and non-intra), plus dct_type if
  field-aware.
- None of the prior art I found needed coded-block pattern, coefficient activity or motion
  vectors for a post-filter. These remain possible but unsupported.

---

## 8. Known gaps and limits of this pass

1. Most key papers were read at abstract depth only; only S05, S06, S10 and S19 were read in
   full. Paywalled: the MPEG-4 Part 2 standard, Kim et al. 1999, Liu and Bovik 2002, List et al.
   2003 (partial), and both MPEG-2-specific papers (S14, S15).
2. Authors and years are unconfirmed for S14 and S15.
3. No quantitative evidence found on the value of intra/inter/skipped, coded-block pattern or
   motion vectors for an MPEG-2 post-filter.
4. No prior art found on interlaced 4:2:0 chroma deblocking.
5. I did not read the libpostproc or DGDecode source code, so their exact QP thresholds and
   field handling are unverified.
6. I did not check whether BestSource can pass libavcodec's per-macroblock QP side data to
   VapourSynth.
7. I did not confirm whether libpostproc remains in current FFmpeg releases. (HYPOTHESIS that it
   may have been moved out recently; to be checked.)
8. Neural deblocking (DPIR and similar) was not researched beyond one practitioner mention and
   one JPEG paper; it is outside the project's deterministic scope but relevant to item 11.
9. Videohelp forum material was found only incidentally; a targeted search there may add
   practitioner evidence on interlaced MPEG-2 deblocking.
10. Consumer-electronics TV post-processing (Philips, Samsung, Sony, and similar) is likely a large
    body of MPEG-2-specific work, mostly in patents. Only a few patents were sampled.

---

## 9. Change log

### v0.1 - 2026-10-06

- First independent research pass for Stage 0, per `research_proposal_01_v1.0.md`.
- 25 source entries (S01-S25) with reading depth, codec relevance and filtering context.
- Findings for questions 1-11; candidate families for question 12 labelled HYPOTHESIS.
- Proposed Stage 2 ablation design (section 6.4).
- Known gaps listed (section 8).
