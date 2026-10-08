import sys
import os
import struct
#
import vapoursynth as vs
core = vs.core
#
# Run similar to :
# "%path_vspipe%" --info "%path_vpy%" 2>>"%mpg_log%" 1>&2
# "%path_vspipe%" --container y4m "%path_vpy%" NUL 2>>"%mpg_log%" 1>&2
#
# Optional overrides (one .vpy for any sample):
# "%path_vspipe%" --arg "src=%mpg_file%" --arg "idx=%mpg_index%" --info "%path_vpy%" ...
#
DEFAULT_SOURCE = r"E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock\VHSC_samples\TEST_4A_A003_blocky.mpg"
#
source_filename = globals().get("src") or DEFAULT_SOURCE
index_filename = globals().get("idx") or (os.path.splitext(source_filename)[0] + ".idx")
#
MAX_DIFFS_SHOWN = 20
SHOW_FIRST = 100
PICT_TYPE_FROM_INDEX = {1: "I", 2: "P", 3: "B"}   # MPEG-2 picture_coding_type
#
def log(text=""):
    sys.stderr.write(f"--- [vpy] {text}\n")
#
def read_index_picture_types(path):
    """Return the I/P/B letter for each record of a Stage 1 .idx, in record order.
    Reads only the 32-byte file header and the 64-byte record headers; MB payloads are skipped.
    Hard-aborts (raises) on any structural problem."""
    with open(path, "rb") as f:
        fh = f.read(32)
        if len(fh) != 32:
            raise ValueError("index: truncated file header")
        magic, version, hsize, endian, final_count, file_flags, reserved = struct.unpack("<8sHHIQII", fh)
        if magic != b"S1MBIDX1" or version != 1 or hsize != 32 or endian != 0x01020304:
            raise ValueError(f"index: bad file header magic={magic!r} version={version} size={hsize}")
        if not (file_flags & 1):
            raise ValueError("index: file not marked complete")
        types = []
        while True:
            rh = f.read(64)
            if not rh:
                break
            if len(rh) != 64:
                raise ValueError(f"index: truncated record header after record {len(types)}")
            rmagic, rsize, ordinal = struct.unpack_from("<4sIQ", rh, 0)
            pictype = rh[30]
            mb_count = struct.unpack_from("<I", rh, 40)[0]
            if rmagic != b"FRM1" or ordinal != len(types) or rsize != 64 + mb_count * 8:
                raise ValueError(f"index: bad record header at record {len(types)}")
            types.append(PICT_TYPE_FROM_INDEX.get(pictype, "?"))
            f.seek(mb_count * 8, 1)
        if len(types) != final_count:
            raise ValueError(f"index: {len(types)} records but header says {final_count}")
    return types
#
def bs_pict_type(frame):
    """BestSource _PictType as a one-letter string, or None if the property is absent."""
    if "_PictType" not in frame.props:
        return None
    v = frame.props["_PictType"]
    if isinstance(v, (bytes, bytearray)):
        v = v.decode("ascii", "replace")
    return str(v)[:1]
#
clip = core.bs.VideoSource(source_filename)
SOURCE_FRAME_COUNT = clip.num_frames
#
sys.stderr.write("\n")
log("--------------------------------------------------------------")
log(f"--- Vapoursynth Information '{source_filename}' ---")
log(f"core.num_threads       = {core.num_threads}")
log(f"core.max_cache_size    = {core.max_cache_size}")
log(f"core.core_version      = {core.core_version}")
log(f"core.api_version       = {core.api_version}")
log("--- Clip Information ---")
log(f"Original source frames = {SOURCE_FRAME_COUNT}")
#
# --- Per-frame picture-type comparison: BestSource _PictType vs Stage 1 index ---
log("--- Picture-type comparison (BestSource vs index) ---")
log(f"index file             = '{index_filename}'")
if not os.path.isfile(index_filename):
    log("RESULT: SKIPPED - index file not found")
else:
    index_types = read_index_picture_types(index_filename)
    log(f"index records          = {len(index_types)}")
    if len(index_types) != SOURCE_FRAME_COUNT:
        log(f"COUNT MISMATCH: BestSource {SOURCE_FRAME_COUNT} vs index {len(index_types)}"
            " (comparing the overlapping range only)")
    first = clip.get_frame(0)
    if bs_pict_type(first) is None:
        log("RESULT: NOT POSSIBLE - BestSource does not set _PictType on this clip")
        log("frame 0 properties     = " + ", ".join(sorted(first.props.keys())))
    else:
        n_compare = min(SOURCE_FRAME_COUNT, len(index_types))
        diffs = []
        missing = 0
        bs_types = []
        for n in range(n_compare):
            t = bs_pict_type(clip.get_frame(n))
            if t is None:
                missing += 1
                t = "-"
            bs_types.append(t)
            if t != index_types[n]:
                diffs.append((n, t, index_types[n]))
        log(f"frames compared        = {n_compare}")
        log(f"first {SHOW_FIRST} BestSource    = {''.join(bs_types[:SHOW_FIRST])}")
        log(f"first {SHOW_FIRST} index         = {''.join(index_types[:SHOW_FIRST])}")
        if missing:
            log(f"frames without _PictType = {missing}")
        for n, t_bs, t_idx in diffs[:MAX_DIFFS_SHOWN]:
            log(f"DIFF frame {n}: BestSource={t_bs} index={t_idx}")
        if len(diffs) > MAX_DIFFS_SHOWN:
            log(f"... {len(diffs) - MAX_DIFFS_SHOWN} further differences not shown")
        if not diffs and len(index_types) == SOURCE_FRAME_COUNT:
            log(f"RESULT: MATCH - all {n_compare} frames have the same picture type")
        else:
            log(f"RESULT: {len(diffs)} DIFFERENCE(S) in {n_compare} frames compared")
log("--------------------------------------------------------------")
sys.stderr.write("\n")
#
sys.stderr.flush()
clip.set_output()
