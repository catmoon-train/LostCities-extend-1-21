import os, json
from collections import Counter

p = r"D:\gengxin\LostCities-extend\LostCities-extend-1-21\data\lce\lostcities\parts\wd1imp_0_1_6.json"
lines = []
lines.append(f"exists: {os.path.exists(p)}")
d = json.load(open(p, encoding="utf-8"))
lines.append(f"keys: {list(d.keys())}")
pal = d.get("palette", {})
pl = pal.get("palette", []) if isinstance(pal, dict) else []
lines.append(f"palette entries: {len(pl)}")
defined = {}
for e in pl:
    if isinstance(e, dict) and "char" in e:
        defined[e["char"]] = e.get("block", "")
lines.append("palette chars: " + ", ".join(repr(c) for c in defined))
slices = d.get("slices", [])
if isinstance(slices, dict):
    slices = list(slices.values())

def walk(o):
    r = []
    if isinstance(o, str):
        r += list(o)
    elif isinstance(o, list):
        for x in o:
            r += walk(x)
    return r

used = walk(slices)
c = Counter(used)
undef = [k for k in c if k not in defined]
lines.append("undefined chars: " + ", ".join(repr(k) for k in undef))
# 顺便展示含未定义字符的 slice 行
for s in (slices if isinstance(slices, list) else []):
    if isinstance(s, list):
        for row in s:
            if isinstance(row, str):
                for ch in row:
                    if ch not in defined:
                        lines.append("  含未定义字符的行: " + repr(row[:60]))
                        break

with open(r"D:\gengxin\LostCities-extend\LostCities-extend-1-21\diag_wd.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
