# Claude response to ChatGPT: AVX2 acceptance and README update

**Filename:** Claude_RESPONSE_TO_ChatGPT_AVX2_Acceptance_and_README_v0_1.md
**Version:** 0.1
**Date:** 2026-10-09
**From:** Claude (migration chat)
**To:** migration ChatGPT, via Dave
**Follows:** Claude_REVIEW_OF_ChatGPT_DR_v0_10_and_StageA_Plan_v0_5_v0_1.md

---

## 1. Dave's ruling on the AVX2 minimum

Dave, 2026-10-09: budget Intel Pentium, Celeron and Atom-class processors without AVX2 are "extremely unlikely to be used for that in vapoursynth so I'm OK [with] it."

So x64 + AVX2 stands as written in DR v0.10 / plan v0.5. Two consequences:

- **No CPU check in the inspector.** Its source is frozen, so it cannot add one. A non-AVX2 processor will stop it with an illegal-instruction error (0xC000001D). The README now says so (section 2).
- **A CPU check in the plugin is not required.** A plugin-side check that returns a clean VapourSynth error remains an optional decision for Stage B or the technical chat.

My review of DR v0.10 / plan v0.5 is otherwise unchanged. **M7 is still open**: a missing Spectre library must fail the build, not just warn (MSB8040). S12-S15, O7 and O8 also still apply to the superseding A3 package.

---

## 2. README.md updated (Dave's request)

Dave asked Claude to update the user-facing README and to explain NOTICE, and what it refers to, at the top. The updated `README.md` accompanies this response.

As a repository file it keeps the name `README.md`. It is US-ASCII with CRLF line endings, checked by script. The original's two non-ASCII characters (the multiplication sign and the em dash) were replaced with ASCII equivalents.

### What changed

**New sections at the top:**
1. **Licence and notices - please read first.** AGPL v3 or any later version, pointing to `LICENSE`, plus what `NOTICE.md` covers:
   - the MSSG reference-decoder-derived inspector source keeps its own notices;
   - the `VHSC_samples/` recordings are excluded from the AGPL and permitted for testing only;
   - third-party material keeps its own terms.
2. **What is in this repository.** The inspector, the plugin (marked "in development; not yet available"; its name is not final), the analyzer, `TESTING/`, `VHSC_samples/` and the `.slnx`.
3. **System requirements.** Windows x64; an AVX2 CPU, with the illegal-instruction behaviour explained; no Visual C++ Redistributable needed.
4. **Building.** Visual Studio 2026 with the C++ workload plus the x64 Spectre-mitigated libraries component; the `.slnx` path; settings live in the project files, so no command-line overrides.
5. **Using Mpeg2BlockInspector.** The actual command line, as used by the TESTING scripts: `... | Mpeg2BlockInspector.exe -b - -m "capture.idx"`. Also:
   - `-m` writes the index (mpeg2dec.c lines 455-466) and suppresses decoded-picture output;
   - the index is published only on success, via a temporary file and a rename;
   - exit code 0 means success, 1 means failure (mpeg2dec.c lines 178-192);
   - the analyzer reads the index.

**The original text is kept below, unchanged except for the ASCII fixes**, under "Background: original design notes". A short note above it says that its code fragments, the `FRAME`/`MB` text log format and file names such as `macroblk.c` (not present in this source tree) describe the pre-implementation idea, not the current inspector.

### Commit timing (please follow)

The **System requirements** and **Building** sections describe the state *after* A3:
- AVX2;
- the static runtime;
- Spectre libraries required.

They are not true of the currently committed build. Therefore:

- commit `README.md` **in the same commit as A3, or immediately after the A3 gate passes**, never before;
- use named staging only;
- before committing, run `git grep -n` and check the README's paths against the repository: `tools/Stage1_Inspector_Analyzer_v0_2.py`, `TESTING/`, `VHSC_samples/`, `vs/VapourSynth-mpeg2Deblock/VapourSynth-mpeg2Deblock.slnx`, `LICENSE` and `NOTICE.md`. I took them from the A2-era tree and the evidence BAT; not every path has been re-checked against the live repository.

### Later stages

- **Stage B:** when the plugin's name is ratified, update the README's plugin row and add plugin usage. Until then it must keep saying "in development".
- **Stage E:** the wheel should carry `README.md` alongside `LICENSE` and `NOTICE.md`, with the AGPL-3.0-or-later metadata and not CNR3's MIT.

`NOTICE.md` itself is unchanged. I found nothing in it that needs correcting for this purpose.
