import sys
from typing import Callable, Optional, Tuple, List
from enum import Enum
import random  # for the in-zone request shuffle
random.seed(20260706)
#
import vapoursynth as vs
core = vs.core
#
# Run similar to :
# "%path_vspipe%" --info "%path_vpy%" 2>>"%mpg_log%" 1>&2
# "%path_vspipe%" --container y4m "%path_vpy%" NUL 2>>"%mpg_log%" 1>&2
#
source_filename = r"E:\SOFTWARE-Win11\MULTIMEDIA\VapourSynth-mpeg2Deblock\VapourSynth-mpeg2Deblock\VHSC_samples\TEST_2A_A001_blocky.mpg"
#
clip = core.bs.VideoSource(source_filename)
SOURCE_FRAME_COUNT = clip.num_frames
#
# Print info to stderr
sys.stderr.write(f"\n--- [vpy] --------------------------------------------------------------\n")
sys.stderr.write(f"--- [vpy]--- Vapoursynth Information '{source_filename}' ---\n")
sys.stderr.write(f"--- [vpy] core.num_threads       = {core.num_threads}\n")
sys.stderr.write(f"--- [vpy] core.num_threads/2     = {core.num_threads // 2}\n")
sys.stderr.write(f"--- [vpy] core.max_cache_size    = {core.max_cache_size}\n")
sys.stderr.write(f"--- [vpy] core.used_cache_size   = {core.used_cache_size}\n")
sys.stderr.write(f"--- [vpy] core.core_version      = {core.core_version}\n")
sys.stderr.write(f"--- [vpy] core.api_version       = {core.api_version}\n")
sys.stderr.write(f"--- [vpy]--- Clip Information ---\n")
sys.stderr.write(f"--- [vpy] Original source frames = {SOURCE_FRAME_COUNT}\n")
sys.stderr.write(f"--- [vpy] --------------------------------------------------------------\n\n")
#
sys.stderr.flush()
clip.set_output()
