#
import vapoursynth as vs
core = vs.core
#
source_filename = r"E:\SOFTWARE-Win11\MULTIMEDIA\Mpeg2BlockInspector\Mpeg2BlockInspector\VHSC_samples\TEST_2A_A001.mpg"
#
clip = core.bs.VideoSource(source_filename)
SOURCE_FRAME_COUNT = clip.num_frames
#
# Print info to stderr
sys.stderr.write(f"\n--- [vpy] Vapoursynth Information ---\n")
sys.stderr.write(  f"--- [vpy] core.num_threads     = {core.num_threads}\n")
sys.stderr.write(  f"--- [vpy] core.num_threads/2   ={core.num_threads // 2}\n")
sys.stderr.write(  f"--- [vpy] core.max_cache_size  = {core.max_cache_size}\n")
sys.stderr.write(  f"--- [vpy] core.used_cache_size = {core.used_cache_size}\n")
sys.stderr.write(  f"--- [vpy] core.core_version    = {core.core_version}\n")
sys.stderr.write(  f"--- [vpy] core.api_version     = {core.api_version}\n")
sys.stderr.write(f"\n--- [vpy] Clip Information ---\n")
sys.stderr.write(  f"--- [vpy] Original source frames = {SOURCE_FRAME_COUNT}\n")
sys.stderr.write(  f"--- [vpy] ---------------------------\n\n")
#
sys.stderr.flush()
clip.set_output()
