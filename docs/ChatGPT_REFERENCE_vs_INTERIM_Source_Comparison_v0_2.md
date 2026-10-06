# ChatGPT Cold Source Comparison - MPEG-2 Reference Decoder vs Interim Inspector

**Filename:** `ChatGPT_REFERENCE_vs_INTERIM_Source_Comparison_v0_2.md`
**Version:** 0.2
**Date:** 2026-10-06
**Author:** ChatGPT
**Status:** Stage 1 source-comparison and design evidence. Not a final inspector specification.
**Cross-review incorporated:** `Claude_REVIEW_OF_ChatGPT_REFERENCE_vs_INTERIM_Source_Comparison_v0_1.md`

**Compared archives:**
- `REFERENCE-mpeg2dec-src.zip`
- `UPDATED-INTERIM-ONLY-src.zip`

**User expectation:** only two original C source files should contain substantive changes.

---

## 1. Executive result

The user's expectation is confirmed.

The pristine reference tree contains:

- 16 `.c` files;
- 4 `.h` files;
- 20 original source/header files total.

After normalising line endings, **exactly two original files have substantive content changes**:

1. `getpic.c`
2. `mpeg2dec.c`

The other 18 original source/header files are content-identical after LF/CRLF normalisation.

All 20 original files were converted from LF line endings in the pristine archive to CRLF in the
interim archive.

Therefore the apparent whole-tree byte differences are overwhelmingly line-ending conversion,
not source changes.

The interim archive also contains:

- Visual Studio solution/project files;
- `mpeg2dec_googleAI_enhanced.c`.

The user has stated that `mpeg2dec_googleAI_enhanced.c` is being deleted. It is not listed as a
`ClCompile` item in `Mpeg2BlockInspector.vcxproj`, so deleting it does not remove a source file
currently compiled by that project.

---

## 2. Mechanical comparison result

### 2.1 Original files unchanged after EOL normalisation

The following 18 files match the pristine reference exactly after converting CRLF/LF to a common
line-ending representation:

```text
config.h
display.c
getbits.c
getblk.c
gethdr.c
getvlc.c
getvlc.h
global.h
idct.c
idctref.c
motion.c
mpeg2dec.h
recon.c
spatscal.c
store.c
subspic.c
systems.c
verify.c
```

### 2.2 Original files with substantive changes

```text
getpic.c
mpeg2dec.c
```

Whitespace-insensitive diff statistics:

```text
getpic.c:
    31 insertions
     3 deletions

mpeg2dec.c:
    24 insertions
     4 deletions
```

These statistics exclude the large amount of formatting/re-indentation performed in the two
files.

---

## 3. Whole-tree formatting observation

The interim conversion changed all original files from LF to CRLF.

In addition, `getpic.c` and `mpeg2dec.c` were extensively reformatted beyond their semantic edits:

- indentation changed;
- pointer spacing changed;
- operator spacing changed;
- brace/continuation formatting changed.

This makes ordinary textual diffs of those two files thousands of lines long even though the
actual semantic modifications are small.

**Project implication:** the ratified plan to rebuild the real inspector as a minimal patch against
the pristine reference source is strongly justified. The reformatted interim files should be
treated as exploratory input, not as the clean authoritative patch base.

---

## 4. Substantive changes in `getpic.c`

There are three functional modifications.

### G-01 - Picture/header logging added at `Decode_Picture()` entry

The interim code adds:

```c
printf("FRAME,%d,%s,Structure=%d,FramePredFrameDCT=%d\n",
    bitstream_framenum,
    ... picture type ...,
    picture_structure,
    frame_pred_frame_dct);
fflush(stdout);
```

This occurs before:

- `picture_data()`;
- `frame_reorder()`.

#### Assessment

The information itself is useful exploratory metadata:

- picture coding type;
- picture structure;
- `frame_pred_frame_dct`.

However, the comment:

> `CUSTOM LOGGING: Output Frame Header Information`

is misleading.

At this point the decoder is processing the coded picture. The reference decoder's actual display
/output reordering happens later in `frame_reorder()`.

For B-picture streams, coded/decode order differs from display/output order.

For field pictures, `Decode_Picture()` is called for each field picture; both fields forming one
coded frame can share the same frame counter.

**Conclusion:** this logging point cannot by itself establish final:

> `.idx2` record N == VapourSynth frame N

correspondence.

It is coded-picture instrumentation, not an authoritative output/display-frame record.

**Severity for final index use:** HIGH.

---

### G-02 - Skipped macroblocks force `dct_type = 0`

The interim code adds:

```c
dct_type = 0; /* skipped macroblocks default to Frame-DCT */
```

after `skipped_macroblock()`.

#### Assessment

Operationally, setting `dct_type = 0` is harmless for the existing reference decoder's block
placement because a skipped macroblock has no coded residual transform blocks.

Semantically, the new comment and any interpretation of this as FRAME metadata are wrong for this
project.

The ratified conceptual distinction is:

```text
FRAME
FIELD
NONE
```

where `NONE` means no current coded residual transform state is applicable/asserted.

A skipped macroblock is not evidence of a coded frame-DCT transform.

The reference decoder also derives or retains `dct_type = 0` in cases where no applicable coded
residual transform geometry exists. Again, an operational value of zero is not by itself proof
that a coded FRAME transform exists.

Cross-review adds an important edge case: a non-intra macroblock can have
`MACROBLOCK_PATTERN` set, therefore read a real `dct_type` bit, and then decode an effective
`coded_block_pattern == 0`. In that case a `dct_type` syntax bit was genuinely present, but there
is still no coded residual transform block whose geometry needs servicing.

**Required Stage 1 semantics:** syntax-bit presence and applicable transform geometry must be
kept distinct. Do not map every operational or transmitted `dct_type == 0` to authoritative
FRAME metadata. `NONE` means that no current coded residual transform geometry applies; it does
not necessarily mean that no `dct_type` bit was read.

**Severity for final index use:** HIGH.

---

### G-03 - Per-macroblock text logging added

The interim code adds:

```c
printf("MB,%d,%d,%d,%s,%d,%d,%d\n",
    framenum,
    MBA / mb_width,
    MBA % mb_width,
    (MBAinc == 1 ? (dct_type == 1 ? "FIELD" : "FRAME") : "SKIPPED"),
    macroblock_type,
    motion_type,
    ld->quantizer_scale);
fflush(stdout);
```

#### Useful aspects

This exposes:

- picture/frame counter used by the current decoder loop;
- macroblock row/column;
- a coarse FRAME/FIELD/SKIPPED label;
- `macroblock_type`;
- `motion_type`;
- the decoder's current **derived** `quantizer_scale`.

The quantiser value is particularly relevant because the reference decoder has already mapped the
raw 5-bit code through MPEG-2 `q_scale_type` semantics.

#### Problem 1 - FRAME/FIELD/SKIPPED is not the required semantic state

For non-skipped coded macroblocks, the expression:

```c
dct_type == 1 ? "FIELD" : "FRAME"
```

can print FRAME where no coded residual transform geometry exists. This includes the ordinary
case where no applicable `dct_type` syntax element is present, and also the cross-review edge case
where a real `dct_type` bit is read but the effective coded block pattern is zero.

For skipped macroblocks, the logger prints SKIPPED, which avoids printing the forced `dct_type=0`
as FRAME, but it still does not express the separate transform-state concept cleanly.

The final research instrumentation needs to distinguish at least conceptually:

```text
transform state = FRAME
transform state = FIELD
transform state = NONE
```

independently from:

```text
macroblock coding state = skipped / intra / inter / ...
```

#### Problem 2 - numeric `macroblock_type` is not authoritative for skipped macroblocks

`skipped_macroblock()` does not decode a fresh `macroblock_type` syntax value.

The reference routine carries/derives prediction behaviour and clears the INTRA flag. In
particular, skipped B-picture macroblocks can inherit prediction direction and motion information
from the previous macroblock, so the carried state may be normatively meaningful even though it is
not newly coded syntax.

Therefore the numeric `macroblock_type` printed for a skipped macroblock must not be labelled as a
fresh syntax value. If exposed by the Stage 1 analyzer, skipped prediction state should be marked
explicitly as **inherited/derived diagnostic state**.

#### Problem 3 - `motion_type` is not universally meaningful

For macroblocks without applicable motion syntax, a numeric motion type can represent a derived or
default implementation state rather than an explicitly coded motion mode.

The Stage 1 analyzer should report prediction/motion state only where its semantics are explicitly
defined.

#### Problem 4 - quantiser semantics need explicit naming

`ld->quantizer_scale` is the decoder's current **derived quantiser scale**, not the raw
`quantiser_scale_code`.

For a macroblock that does not explicitly change quantiser scale, the value is inherited decoder
state.

For skipped macroblocks it is likewise not a quantiser code carried by that skipped macroblock.

That can still be useful if the research field is explicitly named/defined as something like:

> effective/current derived quantiser scale applying at this macroblock position

rather than:

> this macroblock's coded quantiser.

#### Problem 5 - output order

`framenum` here follows the decoder's coded-picture processing sequence and is not sufficient by
itself to establish the required display-output record order.

#### Problem 6 - output channel and flushing

One text line is emitted for every macroblock and `fflush(stdout)` is called after every line.

For PAL 720x576 this is 1620 macroblock flushes per frame.

This is acceptable as small-sample exploratory instrumentation but is unnecessarily expensive for
long captures and is not suitable for the final binary index path.

Existing reference-decoder messages can also use stdout, so stdout text is not a robust binary
index channel.

**Severity for final index use:** HIGH overall; useful exploratory code only.

---

## 5. Substantive changes in `mpeg2dec.c`

There are four closely related functional changes supporting piped elementary-stream input.

### M-01 - standard-input support

The interim code accepts:

```text
-b -
```

and assigns:

```c
base.Infile = _fileno(stdin);
```

On Windows it changes stdin to binary mode:

```c
_setmode(_fileno(stdin), _O_BINARY);
```

#### Assessment

This is directionally correct and directly supports the intended pipeline:

```text
ffmpeg ... -f mpeg2video - | Mpeg2BlockInspector -b -
```

Setting binary mode is necessary on Windows to prevent text-mode translation.

---

### M-02 - seek-based stream sniffing is skipped for stdin

For `-b -`, the code calls `Initialize_Buffer()` directly and skips the original:

- initial stream-type sniff;
- `lseek()` rewind;
- second buffer initialisation after rewind.

#### Assessment

This is necessary because a pipe is non-seekable.

The consequence is that piped input is effectively assumed to be an MPEG video elementary stream.

That is compatible with the agreed ffmpeg pipeline, where ffmpeg explicitly emits:

```text
-f mpeg2video
```

It is not a general-purpose pipe auto-detection implementation.

That limitation is acceptable for the current project if explicitly documented.

---

### M-03 - stdin is not closed as an ordinary file

The interim code changes:

```c
close(base.Infile);
```

to:

```c
if (base.Infile != _fileno(stdin))
    close(base.Infile);
```

#### Assessment

Reasonable for Windows stdin usage.

Minor portability note:

`_fileno()` is a Microsoft/Windows spelling but this call is outside the `_WIN32` conditional.

The current project is Windows-only, so this is not presently a functional blocker.

---

### M-04 - command-line lookahead permits literal `-` as a filename

Original:

```c
NextArg = (argv[i+1][0]=='-');
```

Interim:

```c
NextArg = (argv[i + 1][0] == '-' && argv[i + 1][1] != '\0');
```

#### Assessment

This is necessary for:

```text
-b -
```

Without it, the original parser interprets the literal single hyphen as the next command option
rather than as the stdin pseudo-filename.

This change is appropriate.

---

## 6. `mpeg2dec.c` issues that remain

The stdin modifications are useful exploratory work, but they are not yet the desired final
command-line/input implementation.

### 6.1 No explicit index output filename

Current instrumentation writes text metadata to stdout.

The agreed Stage 1/final architecture needs an explicit binary index output file.

### 6.2 Diagnostics are not separated robustly

The eventual inspector requirement is:

- binary index to the requested index file;
- diagnostics/errors to stderr;
- never mix textual diagnostics with binary index bytes.

The current reference program has historical stdout usage, so this must be reviewed deliberately.

### 6.3 Pipe format assumption should be explicit

`-b -` assumes clean MPEG-2 elementary-video bytes.

That is appropriate when fed by the agreed ffmpeg command but should produce a clear documented
contract/error model.

### 6.4 Command-line help does not document stdin convention

The current help text still describes ordinary filenames.

### 6.5 Formatting/rewrite issue

As with `getpic.c`, the entire file was reformatted.

The useful stdin patch should eventually be reapplied minimally to pristine source rather than
accepting the converted file wholesale.

---

## 7. High-priority semantic findings for Stage 1

### Finding A - exactly two original source files changed

CONFIRMED.

This validates the user's recollection and gives us a very small real change surface.

### Finding B - the source conversion did not secretly modify the other decoder modules

CONFIRMED after line-ending normalisation.

The other 18 original source/header files match.

### Finding C - current FRAME records are not output/display records

CONFIRMED from source control flow.

`FRAME,...` is emitted before `frame_reorder()`.

### Finding D - current FRAME/FIELD logging conflates decoder defaults with transform semantics

CONFIRMED.

`dct_type == 0` does not always mean that a coded frame-DCT transform is present.

Conversely, the presence of a real `dct_type` syntax bit does not guarantee that coded residual
transform geometry exists: a non-intra macroblock can decode `coded_block_pattern == 0`.

The future analyzer/index must derive NONE from applicable residual-transform semantics, not merely
from the presence or value of the `dct_type` bit.

### Finding E - the current quantiser output is the derived scale

CONFIRMED from reference source.

`decode_macroblock()` sets:

```c
ld->quantizer_scale =
    ld->q_scale_type
        ? Non_Linear_quantizer_scale[quantizer_scale_code]
        : (quantizer_scale_code << 1);
```

for MPEG-2.

Thus the logged `ld->quantizer_scale` is already the derived scale used by decoding, not the raw
5-bit code.

For inherited/skipped cases its ownership/meaning must be documented carefully.

### Finding F - stdin support is conceptually sound for the intended ffmpeg pipeline

CONFIRMED at source level.

The modifications:

- permit `-b -`;
- set Windows stdin binary mode;
- avoid seeking a pipe.

They should be preserved in concept but later reapplied as a minimal clean patch.

---

## 8. Recommended treatment of the interim source

Do **not** incrementally "clean up" the heavily reformatted interim C files and make them the new
authority.

Recommended approach remains:

1. pristine reference source is the authority;
2. this comparison document records the useful interim modifications;
3. Stage 1 defines exactly what research instrumentation is required;
4. apply those changes as a small reviewable patch to pristine source;
5. preserve original formatting/comments except where a specific approved modification requires a
   change;
6. compare the resulting patch mechanically.

The interim tree remains useful as:

- proof that pipe input can be made to work;
- proof-of-concept logging;
- a source of implementation ideas.

It should not become the clean baseline.

---

## 9. Stage 1 instrumentation design consequences from cross-review

Claude's review of v0.1 against the pristine reference source confirms the reference-side findings
and adds four concrete design consequences.

### 9.1 Display/output record emission and metadata retention

Reference-source control flow shows that decoded pictures are actually written only through
`Write_Frame()`:

- `frame_reorder()` writes the current B-picture buffer (`auxframe`) immediately in output order;
- for I/P pictures, `frame_reorder()` writes the **previous** reference picture;
- `Output_Last_Frame_of_Sequence()` writes the final delayed reference picture;
- `Update_Picture_Buffers()` rotates the forward/backward reference buffers while B pictures use
  `auxframe`.

**Stage 1 design proposal (HYPOTHESIS):**

- maintain per-picture metadata slots that mirror the forward-reference, backward-reference and
  auxiliary/B-picture pixel buffers;
- rotate the metadata slots exactly when the corresponding frame buffers rotate;
- emit one temporary-index/display record at the same logical event that writes the matching pixel
  buffer;
- number records with a simple monotonically increasing **output-emission ordinal** rather than
  reusing `Bitstream_Framenum`, `Sequence_Framenum` or another coded-picture counter.

This is the leading design for proving:

> temporary index record N == decoder output frame N

before the separate BestSource/VapourSynth correspondence proof.

It remains a design hypothesis until implemented and tested.

### 9.2 Field, sequence and damaged-stream correspondence hazards

The pristine source exposes several cases the Stage 1 design must handle explicitly.

#### Trailing unpaired field

`Output_Last_Frame_of_Sequence()` does not store an incomplete final frame when only one field of
a pair has been decoded.

The temporary index must not emit a display-frame record for data that the decoder itself drops.

#### Two field pictures -> one output frame

Output occurs only once the frame picture is complete (frame picture or second field).

The two coded field pictures contributing to one output frame may have different picture-level and
macroblock-level coding context.

A deliberate **field-pair metadata merge rule** is therefore required; concatenating or blindly
overwriting field metadata is not acceptable.

#### Per-sequence reset and flush

The decoder resets `Sequence_Framenum` per video sequence and flushes delayed output at sequence
end.

Stage 1 must test the supplied captures for repeated sequence headers / sequence-end behaviour and
later compare the resulting output sequence with BestSource.

#### Damaged streams

The reference decoder can abandon a slice after invalid VLC / fault conditions.

Stage 1 correspondence testing must include the rule:

> index output must describe what this decoder actually outputs, and any divergence from
> BestSource on damaged input must fail correspondence testing rather than be silently assumed
> equivalent.

### 9.3 Correct derivation of FRAME / FIELD / NONE

The v0.1 document correctly rejected the interim logger's direct mapping of `dct_type` to
FRAME/FIELD, but the cross-review identifies a more precise edge case.

A non-intra macroblock may have `MACROBLOCK_PATTERN` set and therefore read a genuine `dct_type`
bit, while subsequently decoding an effective coded block pattern of zero.

Therefore:

> `NONE` is a semantic statement about **applicable coded residual transform geometry**, not a
> statement that the `dct_type` syntax bit was necessarily absent.

A suitable Stage 1 derivation hypothesis is:

```text
NONE
    if skipped
    or (not intra and effective coded_block_pattern == 0)

FRAME
    if a coded residual transform is present and dct_type is frame
    or, in a frame picture, frame_pred_frame_dct == 1 makes frame DCT implicit

FIELD
    if a coded residual transform is present and dct_type is field
```

This is deliberately stated semantically rather than as final C code.

#### Field pictures

Field pictures must not be labelled FRAME merely because the decoder's operational `dct_type`
value is zero.

They require their own geometry path identified by `picture_structure`.

### 9.4 Skipped prediction state

For skipped macroblocks:

- no fresh macroblock-type syntax is decoded;
- prediction state may nevertheless be inherited/derived and significant, especially for
  B-pictures;
- stale/forced `dct_type` must not be reported as FRAME/FIELD because no coded residual transform
  geometry exists.

The Stage 1 analyzer may report inherited prediction state as a **diagnostic**, explicitly marked
as inherited rather than freshly coded.

This is consistent with the decision to keep prediction mode diagnostic initially.

### 9.5 Quantiser research value

The v0.1 conclusion remains unchanged:

- `ld->quantizer_scale` is the decoder's current **derived MPEG-2 quantiser scale**;
- it may be inherited rather than explicitly updated at a macroblock;
- skipped/no-residual macroblocks do not thereby contain their own coded quantiser value.

For Stage 1, the useful diagnostic set is therefore likely to distinguish:

```text
effective/current derived quantiser scale
quantiser explicitly updated here?  yes/no
raw quantiser_scale_code             optional diagnostic
```

The final `.idx2` storage representation remains unfrozen.

### 9.6 Questions still open before editing pristine source

The comparison plus cross-review reduce the open design questions to:

1. Exact C data structure for the metadata slots that mirror decoder frame buffers.
2. Exact field-pair merge semantics for picture-level and macroblock-level metadata.
3. Exact temporary binary representation of FRAME/FIELD/NONE plus field-picture identity.
4. Which macroblock syntax/derived fields are required for the Stage 1 analyzer versus merely
   optional diagnostics.
5. Exact temporary index header/record format, deliberately disposable and not the final `.idx2`.
6. Error policy when a decoded picture cannot be represented safely or correspondence assumptions
   fail.
7. How to prove this decoder's output-emission ordinal against BestSource/VapourSynth frame N.

These should be resolved in the Stage 1 instrumentation design before modifying the pristine
decoder.

---

## 10. Samples received for the next phase

The following user-supplied samples are available:

```text
TEST_4A_A003.mpg
TEST_4A_A003_blocky.mpg
```

Container identification:

```text
TEST_4A_A003.mpg:
    MPEG program multiplex

TEST_4A_A003_blocky.mpg:
    MPEG system/program multiplex
```

These were not required to establish the source comparison above.

They are suitable for the subsequent Stage 1 instrumentation and analyzer validation.

---

## 11. Final comparison verdict

**PASS with important semantic caveats.**

The source-tree provenance is much cleaner than feared:

- only `getpic.c` and `mpeg2dec.c` contain substantive edits;
- the rest of the original decoder source is unchanged apart from line endings.

The two edited files contain a small and understandable set of changes.

The stdin work in `mpeg2dec.c` is largely useful.

The logging work in `getpic.c` is valuable as exploratory instrumentation, but several fields are
not semantically safe for the final project:

- picture/frame numbering is not display-order numbering;
- absent transform state can be mislabelled FRAME;
- skipped macroblock type/prediction data is not fresh syntax and must be identified as
  inherited/derived where reported;
- motion state is not universally applicable;
- quantiser ownership/inheritance is not explicit.

The incorporated cross-review also identifies the leading display-order design: metadata should
travel with the same reference/B-picture slots as the decoder's frame buffers and be emitted on the
corresponding `Write_Frame()` output event, using an independent output-emission ordinal. It also
clarifies that `NONE` is derived from residual-transform applicability, not simply from whether a
`dct_type` bit was present.

Therefore the interim inspector should **not** be promoted directly into the Stage 1 binary indexer.

The agreed strategy remains correct:

> extract the useful ideas, then build a minimal, auditable instrumentation patch against the
> pristine reference decoder.



---

## 12. Change log

### v0.2 - 2026-10-06

- Incorporated `Claude_REVIEW_OF_ChatGPT_REFERENCE_vs_INTERIM_Source_Comparison_v0_1.md`.
- Preserved the v0.1 mechanical result: exactly `getpic.c` and `mpeg2dec.c` have substantive
  changes among the original source/header files.
- Clarified FRAME/FIELD/NONE semantics: `NONE` describes absence of applicable coded residual
  transform geometry and does not necessarily imply that no `dct_type` syntax bit was read.
- Added the `MACROBLOCK_PATTERN` + effective `coded_block_pattern == 0` edge case.
- Refined skipped-macroblock prediction semantics from "not authoritative" to
  "inherited/derived diagnostic state, not fresh syntax".
- Added the leading display-order instrumentation hypothesis: metadata slots mirror decoder frame
  buffers and emit at the corresponding `Write_Frame()` event using an independent output ordinal.
- Added trailing-field, field-pair-merge, sequence-flush and damaged-stream correspondence
  hazards.
- Added field-picture handling requirement.
- Reduced the pre-edit Stage 1 design questions to the remaining unresolved items.

### v0.1 - 2026-10-06

- Initial cold mechanical and semantic comparison of the pristine reference decoder and interim
  inspector source trees.
