# VapourSynth-mpeg2Deblock

Tools for finding and, in time, reducing MPEG-2 blocking in video, using information that MPEG-2 decoders normally throw away.

## Licence and notices - please read first

- Original material developed for this project is licensed under the **GNU Affero General Public License, version 3 or any later version**. The licence text is in [`LICENSE`](LICENSE).
- [`NOTICE.md`](NOTICE.md) sets out what that licence does and does not cover:
  - **MPEG reference-decoder-derived source** (the `Mpeg2BlockInspector` sources) keeps its original copyright, attribution and licence notices. Those notices are not replaced by this project's licence.
  - **Test recordings** under `VHSC_samples/` are **not** covered by the AGPL. They are included only so the project can be tested. Copying, redistributing or using them for any other purpose is not permitted; see `NOTICE.md` for the exact terms.
  - **Third-party material** remains under its own copyright, licence and notice terms.

## What is in this repository

| Item | What it is |
|---|---|
| `Mpeg2BlockInspector.exe` | A Windows x64 command-line tool derived from the MSSG MPEG-2 reference decoder. It reads an MPEG-2 video stream and writes a binary per-macroblock index of how each part of each picture was coded. |
| VapourSynth plugin | A VapourSynth (API4) plugin that will use that index for deblocking. **In development; not yet available.** Its name and details are not final. |
| `tools/Stage1_Inspector_Analyzer_v0_2.py` | A Python script that reads and checks an index produced by the inspector. |
| `TESTING/` | Windows batch scripts used to run the inspector against the test recordings. |
| `VHSC_samples/` | Test recordings and their reference indexes. Restricted use; see `NOTICE.md`. |
| `vs/VapourSynth-mpeg2Deblock/` | The Visual Studio 2026 solution (`VapourSynth-mpeg2Deblock.slnx`) and project files. |

## System requirements

- **Windows, 64-bit (x64).**
- **A CPU with AVX2.** This means Intel processors from the Haswell generation (2013) onwards, or AMD processors from Excavator (2015) or Zen (2017) onwards. Some low-cost Intel Pentium, Celeron and Atom-class processors made after 2013 do not have AVX2. On a processor without AVX2 the programs stop with an "illegal instruction" error (code `0xC000001D`). That is expected, not a fault.
- **No Visual C++ Redistributable is needed.** Release builds include the Microsoft C/C++ runtime inside the program file.

## Building

- Visual Studio 2026 with the "Desktop development with C++" workload and the **MSVC x64 Spectre-mitigated libraries** component. The builds enable Spectre mitigation and stop if those libraries are missing.
- Open `vs\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock.slnx` and build **Release | x64** (or Debug | x64).
- The build settings live in the project files. Do not override them on the command line.

## Using Mpeg2BlockInspector

Let `ffmpeg` extract the MPEG-2 video stream and pipe it straight into the inspector. No temporary file is needed:

```cmd
ffmpeg -v error -i "capture.mpg" -c:v copy -an -f mpeg2video - | Mpeg2BlockInspector.exe -b - -m "capture.idx"
```

- `-b -` reads the MPEG-2 stream from standard input (the pipe).
- `-m file` writes the macroblock index to `file`. With `-m`, no decoded pictures are written.
- The index appears only when the run succeeds. It is first written under a temporary name and renamed at the end, so a failed run never leaves a partial index behind.
- Exit code `0` means success, and `1` means failure.
- The index is a binary file. Use `tools/Stage1_Inspector_Analyzer_v0_2.py` to read and check it.

## Background: original design notes

The notes below are the original research sketch, written before the inspector was built. They explain the idea behind the project. Their code fragments, the text log format they describe (`FRAME` / `MB` lines) and some of the file names they mention (for example `macroblk.c`) **do not** describe the inspector in this repository, which writes the binary index described above.

### 1. Assessment of MPEG2 blocking

1. **No In-Loop Deblocking:** Unlike H.264/AVC, H.265/HEVC, or AV1, the MPEG-2 standard (ISO/IEC 13818-2) contains **no in-loop deblocking filter**. The normative decoding process takes the IDCT output, adds motion compensation predictors, and writes directly to the decoded frame buffer. 
2. **Metadata Discarded:** Decoders (`libavcodec`, reference decoders, hardware ASICs) determine the exact coding method for each $16\times16$ macroblock (e.g., Frame DCT vs. Field DCT, Field MC vs. Frame MC, intra vs. inter) as they parse the bitstream slices. Once the macroblock pixels are reconstructed, **all of this metadata is immediately thrown away** to conserve memory.
3. **Downstream Filters Get Bare Pixels:** Source filters like `bestsource`, `ffms2`, and `d2vsource` receive raw pixel planes from the underlying decoder. None of them pass a per-macroblock metadata map downstream to VapourSynth or AviSynth.

### 2. Modifying the C Reference Decoder

Source: https://github.com/aholtzma/mpeg2dec

The standard approach for this experiment is to take the **official MSSG (MPEG Software Simulation Group) Reference Decoder** (which is written in simple, ANSI C from the mid-1990s) and add **10 to 15 lines of C code** to dump a structured log (or JSON). 

You can then parse that log in Python with zero performance penalty.

#### Why the MSSG Reference Decoder is Ideal:
* It is tiny (~15 `.c` files, no complex build systems, compiles with standard `gcc` or `clang`).
* It does not optimize or obscure internal state like FFmpeg does.
* All macroblock decisions are parsed explicitly in one function inside `macroblk.c` / `getvlc.c`.

---

### 3. What the Data Looks Like in the Bitstream

For a 720x480 DVD frame ($45 \times 30 = 1,350$ macroblocks per frame), the reference decoder reads these key syntax elements:

1. **Frame-Level (`gethdr.c`):**
   * `picture_structure`: `1` (Top Field), `2` (Bottom Field), `3` (Frame Picture).
   * `picture_coding_type`: `1` (I-frame), `2` (P-frame), `3` (B-frame).
   * `frame_pred_frame_dct`: If `1`, all blocks in this frame are forced to Frame-DCT. If `0`, macroblocks are free to choose.

2. **Macroblock-Level (`macroblk.c` / `getblk.c`):**
   * `macroblock_type`: Indicates Intra, Forward Pred, Backward Pred, etc.
   * `macroblock_motion_forward / backward`: Frame-based vs. Field-based motion vectors.
   * `dct_type`: **This is the critical bit.** 
     * `0`: **Frame DCT** (The 8x8 luminance blocks take interleaved lines from both fields -- good for static areas).
     * `1`: **Field DCT** (The 8x8 luminance blocks take lines from only Field 1 or Field 2 -- used when there is high interlaced motion).
   * `quantizer_scale_code`: The exact quantization factor applied to this macroblock (indicates how heavily compressed/blocked this specific MB is).

---

### 4. Implementation Blueprint

#### Step 1: The C-Side Modification (MSSG Decoder)
Inside the MSSG decoder source, locate `macroblk.c` in function `macroblock_modes(...)`:

```c
/* In macroblk.c: immediately after dct_type is decoded */
if (picture_structure == FRAME_PICTURE && !frame_pred_frame_dct) {
    dct_type = Get_Bits(1);
} else {
    dct_type = 0;
}

/* --- ADD YOUR LOGGING HERE --- */
fprintf(stdout, "MB,%d,%d,%d,%d,%d,%d\n", 
        current_frame_id, 
        mb_row, 
        mb_col, 
        macroblock_type, 
        dct_type, 
        quantizer_scale);
```

#### Step 2: The Python Driver Script
You can wrap the compiled executable with Python to inspect any `.mpg` file:

```python
import subprocess
import json
import pandas as pd # Optional, for easy analysis

def analyze_mpeg2_structure(mpg_path, max_frames=100):
    # Run the patched reference decoder
    cmd = ["./mpeg2dec_custom", "-b", mpg_path, "-f", "-n", str(max_frames)]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    
    current_frame = None
    frames_data = []
    
    for line in process.stdout:
        tokens = line.strip().split(',')
        if tokens[0] == "FRAME":
            # FRAME, FrameID, PictureType, Structure, FramePredDCT
            current_frame = {
                "frame_id": int(tokens[1]),
                "type": tokens[2],
                "structure": tokens[3],
                "frame_pred_frame_dct": int(tokens[4]),
                "macroblocks": []
            }
            frames_data.append(current_frame)
        elif tokens[0] == "MB" and current_frame is not None:
            # MB, FrameID, Row, Col, MB_Type, DCT_Type, QuantScale
            current_frame["macroblocks"].append({
                "row": int(tokens[2]),
                "col": int(tokens[3]),
                "mb_type": int(tokens[4]),
                "dct_type": "Field" if int(tokens[5]) == 1 else "Frame",
                "quant": int(tokens[6])
            })
            
    return frames_data

# Example analysis:
# data = analyze_mpeg2_structure("vhs_capture.mpg", max_frames=50)
# frame0_field_dct_count = sum(1 for mb in data[0]["macroblocks"] if mb["dct_type"] == "Field")
# print(f"Frame 0 has {frame0_field_dct_count} Field-coded Macroblocks.")
```

---

### 5. You can pipe the stream directly from `ffmpeg` straight into the modified decoder's `stdin` (standard input). 

This completely eliminates the need to create temporary `.m2v` files on your hard drive. The demuxing happens on the fly in RAM.

Here is how to set it up:

#### 1. The FFmpeg Command for Piping
FFmpeg can demux the `.mpg` container and write raw elementary MPEG-2 video packets straight to the standard output pipe (`-`) using the format flag `-f mpeg2video`:

```bash
ffmpeg -i "capture.mpg" -c:v copy -an -f mpeg2video -
```

#### 2. The 3-Line C Modification for Windows (in Visual Studio)

By default on Windows, `stdin` operates in "Text mode" (which mangles binary data by converting line endings). You need to tell Windows to treat `stdin` as **pure binary**.

Open **`mpeg2dec.c`** in your Visual Studio project:

1. At the top of `mpeg2dec.c`, include the Windows I/O headers:
   ```c
   #ifdef _WIN32
   #include <io.h>
   #include <fcntl.h>
   #endif
   ```

2. Inside `main()` or where the input file is opened, check if the input filename is `"-"` (or if no file is provided), and set `stdin` to binary mode:
   ```c
   if (strcmp(argv[i], "-") == 0) {
       #ifdef _WIN32
       _setmode(_fileno(stdin), _O_BINARY); /* Crucial for Windows */
       #endif
       Infile = _fileno(stdin); /* MSSG uses low-level file descriptor Infile */
   } else {
       Infile = open(argv[i], O_RDONLY | O_BINARY);
   }
   ```

*(Note: In the MSSG reference code, `getbits.c` uses standard sequential forward reads via `read(Infile, ld->Rdbfr, BUFFER_SIZE)` and never performs backwards seeks (`lseek`), so streaming from a pipe works out of the box).*

#### 3. Running It in the Command Prompt

Once compiled, you link them together with the standard vertical pipe (`|`):

```cmd
ffmpeg -v error -i "capture.mpg" -c:v copy -an -f mpeg2video - | Mpeg2BlockInspector.exe -b - > analysis.log
```

* `ffmpeg -v error`: Silences FFmpeg's general banner text so it doesn't pollute the terminal.
* `-f mpeg2video -`: Sends the raw MPEG-2 stream down the pipe.
* `Mpeg2BlockInspector.exe -b -`: Tells your tool to read from the pipe.
* `> analysis.log`: Redirects your custom macroblock `printf` output to a file.

#### 4. Running the Entire Pipeline Inside Python

If you want Python to control the entire workflow and process the stream line-by-line in real time:

```python
import subprocess

def stream_and_inspect_mpg(mpg_path):
    # Step 1: Start FFmpeg demuxer process (outputting to pipe)
    ffmpeg_cmd = [
        "ffmpeg", "-v", "error",
        "-i", mpg_path,
        "-c:v", "copy",
        "-an",
        "-f", "mpeg2video",
        "-"
    ]
    p_ffmpeg = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    # Step 2: Start your Visual Studio Inspector tool (reading from FFmpeg's pipe)
    inspector_cmd = ["Mpeg2BlockInspector.exe", "-b", "-"]
    p_inspector = subprocess.Popen(
        inspector_cmd, 
        stdin=p_ffmpeg.stdout, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.DEVNULL, 
        text=True
    )
    p_ffmpeg.stdout.close() # Allow p_ffmpeg to receive a SIGPIPE if p_inspector exits

    # Step 3: Read and analyze the block log live in Python
    for line in p_inspector.stdout:
        line = line.strip()
        if line.startswith("FRAME_HEADER"):
            print(f"[New Frame] {line}")
        elif line.startswith("MB"):
            # Process macroblock metadata...
            pass

    p_inspector.wait()

# Run it:
stream_and_inspect_mpg("my_vhs_tape.mpg")
```

#### 5. With this architecture:
1. **Zero disk space used:** No intermediate `.m2v` files written to disk.
2. **Real-time streaming:** Python gets the frame structure and `Field vs. Frame DCT` macroblock classification directly as FFmpeg demuxes the capture.
