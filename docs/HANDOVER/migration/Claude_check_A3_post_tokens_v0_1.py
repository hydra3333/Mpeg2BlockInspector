# Claude_check_A3_post_tokens_v0_1.py
# Purpose: mechanical post-A3 gate. Compares the post-A3 native-tlog tokens
# (produced by extract_StageA_A3_checkpoint_tlog_tokens_v0_4.py run on the four
# post-A3 .command.1.tlog files) against the checkpoint tokens plus EXACTLY the
# changes predicted in StageA_A3_v0_9_Predicted_Command_Line_Delta.md.
# Any unexplained, missing or extra token -> FAIL (exit 1).
# CL tokens compare case-sensitively (/Zi and /ZI differ). LINK tokens compare
# case-insensitively (linker options are case-insensitive).
# Usage:
#   python Claude_check_A3_post_tokens_v0_1.py --checkpoint StageA_A3_checkpoint_tokens_generated_v0_4.csv --post StageA_A3_post_tokens_v0_1.csv
import argparse, csv, sys
from collections import Counter

# (configuration, tool) -> (tokens removed from checkpoint, tokens added)
# /errorReport switches are absent from native tlogs (detailed log only), as at the checkpoint.
PREDICTED = {
    ("Debug|x64", "CL"): (["/ZI"],
        ["/Zi", "/Oi", "/Ot", "/Ob2", "/arch:AVX2", "/guard:cf", "/favor:blend", "/Gy-", "/GF-"]),
    ("Release|x64", "CL"): (["/MD"],
        ["/MT", "/GL", "/Oi", "/Ot", "/Ob2", "/GF", "/Gy", "/arch:AVX2", "/guard:cf", "/favor:blend"]),
    ("Debug|x64", "LINK"): (["/DEBUG"],
        ["/DEBUG:FULL", "/GUARD:CF", "/CETCOMPAT", "/HIGHENTROPYVA",
         "/OPT:NOREF", "/OPT:NOICF", "/LARGEADDRESSAWARE", "/TSAWARE"]),
    ("Release|x64", "LINK"): (["/DEBUG"],
        ["/DEBUG:FULL", "/LTCG", "/GUARD:CF", "/CETCOMPAT", "/HIGHENTROPYVA",
         "/PDBALTPATH:%_PDB%", "/LARGEADDRESSAWARE", "/TSAWARE"]),
}

def load(path):
    d = {}
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d.setdefault((r["configuration"], r["tool"]), []).append(r["token"])
    return d

def key(tool, t):
    return t.lower() if tool == "LINK" else t

ap = argparse.ArgumentParser()
ap.add_argument("--checkpoint", required=True)
ap.add_argument("--post", required=True)
a = ap.parse_args()
cp, post = load(a.checkpoint), load(a.post)
ok = True
for k in sorted(PREDICTED):
    cfg, tool = k
    removed, added = PREDICTED[k]
    exp = Counter(key(tool, t) for t in cp.get(k, []))
    for t in removed:
        if exp[key(tool, t)] < 1:
            print(f"FAIL: {cfg} {tool}: predicted removal {t} not in checkpoint"); ok = False
        exp[key(tool, t)] -= 1
    for t in added:
        exp[key(tool, t)] += 1
    exp = +exp
    got = Counter(key(tool, t) for t in post.get(k, []))
    missing, extra = exp - got, got - exp
    for t, n in sorted(missing.items()):
        print(f"FAIL: {cfg} {tool}: expected but missing: {t} (x{n})"); ok = False
    for t, n in sorted(extra.items()):
        print(f"FAIL: {cfg} {tool}: present but not predicted: {t} (x{n})"); ok = False
    mi = sum(n for t, n in got.items() if t.lower().startswith("/manifestinput:"))
    if tool == "LINK" and mi != 1:
        print(f"FAIL: {cfg} LINK: {mi} /MANIFESTINPUT entries, expected exactly 1"); ok = False
    if not missing and not extra:
        print(f"PASS: {cfg} {tool}: {sum(got.values())} tokens = checkpoint {len(cp.get(k, []))} - {len(removed)} + {len(added)}")
extra_keys = set(post) - set(PREDICTED)
if extra_keys:
    print(f"FAIL: unexpected configuration/tool groups: {sorted(extra_keys)}"); ok = False
for t in ("/qspectre", "/fp:contract"):
    for k, toks in post.items():
        if any(x.lower().startswith(t) for x in toks):
            print(f"FAIL: {k}: {t} present"); ok = False
print("PASS: post-A3 command lines equal checkpoint plus exactly the v0.9 predicted delta." if ok else "FAIL: see above.")
sys.exit(0 if ok else 1)
