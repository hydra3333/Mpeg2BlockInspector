# Mpeg2BlockInspector
Accept an mpeg2 video stream piped from ffmpeg and extract macroblock information

### 1. Assessment of MPEG2 blocking

1. **No In-Loop Deblocking:** Unlike H.264/AVC, H.265/HEVC, or AV1, the MPEG-2 standard (ISO/IEC 13818-2) contains **no in-loop deblocking filter**. The normative decoding process takes the IDCT output, adds motion compensation predictors, and writes directly to the decoded frame buffer. 
2. **Metadata Discarded:** Decoders (`libavcodec`, reference decoders, hardware ASICs) determine the exact coding method for each $16\times16$ macroblock (e.g., Frame DCT vs. Field DCT, Field MC vs. Frame MC, intra vs. inter) as they parse the bitstream slices. Once the macroblock pixels are reconstructed, **all of this metadata is immediately thrown away** to conserve memory.
3. **Downstream Filters Get Bare Pixels:** Source filters like `bestsource`, `ffms2`, and `d2vsource` receive raw pixel planes from the underlying decoder. None of them pass a per-macroblock metadata map downstream to VapourSynth or AviSynth.

### 2. Modifying the C Reference Decoder

The standard approach for this experiment is to take the **official MSSG (MPEG Software Simulation Group) Reference Decoder** (which is written in simple, ANSI C from the mid-1990s) and add **10 to 15 lines of C code** to dump a structured log (or JSON). 

You can then parse that log in Python with zero performance penalty.

#### Why the MSSG Reference Decoder is Ideal:
* It is tiny (~15 `.c` files, no complex build systems, compiles with standard `gcc` or `clang`).
* It does not optimize or obscure internal state like FFmpeg does.
* All macroblock decisions are parsed explicitly in one function inside `macroblk.c` / `getvlc.c`.

---

### 4. What the Data Looks Like in the Bitstream

For a 720×480 DVD frame ($45 \times 30 = 1,350$ macroblocks per frame), the reference decoder reads these key syntax elements:

1. **Frame-Level (`gethdr.c`):**
   * `picture_structure`: `1` (Top Field), `2` (Bottom Field), `3` (Frame Picture).
   * `picture_coding_type`: `1` (I-frame), `2` (P-frame), `3` (B-frame).
   * `frame_pred_frame_dct`: If `1`, all blocks in this frame are forced to Frame-DCT. If `0`, macroblocks are free to choose.

2. **Macroblock-Level (`macroblk.c` / `getblk.c`):**
   * `macroblock_type`: Indicates Intra, Forward Pred, Backward Pred, etc.
   * `macroblock_motion_forward / backward`: Frame-based vs. Field-based motion vectors.
   * `dct_type`: **This is the critical bit.** 
     * `0`: **Frame DCT** (The 8x8 luminance blocks take interleaved lines from both fields — good for static areas).
     * `1`: **Field DCT** (The 8x8 luminance blocks take lines from only Field 1 or Field 2 — used when there is high interlaced motion).
   * `quantizer_scale_code`: The exact quantization factor applied to this macroblock (indicates how heavily compressed/blocked this specific MB is).

---

### 5. Implementation Blueprint

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

### Summary

* **Do decoders deblock MPEG-2?** No. They produce raw reconstructed blocks.
* **Does the bitstream know the exact field/frame block layout?** Yes, via the `dct_type` and `motion_type` syntax elements per macroblock.
* **Should you rewrite the decoder in pure Python?** No; it is too complex and slow.
* **Recommended approach:** Compile the standard, open-source MSSG MPEG-2 C reference decoder with a few `printf` statements inserted into `macroblk.c`, and pipe the human-readable output into Python. This gives you exact per-block metadata down to the quantization scale and field/frame DCT split for your VHS-C captures.
