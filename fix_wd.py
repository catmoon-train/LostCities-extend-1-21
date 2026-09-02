import os, json, re

P = r"D:\gengxin\LostCities-extend\LostCities-extend-1-21\data\lce\lostcities\parts\wd1imp_0_1_6.json"

with open(P, encoding="utf-8") as f:
    d = json.load(f)

pal = d["palette"]["palette"]
defined = set()
for e in pal:
    if isinstance(e, dict) and "char" in e:
        defined.add(e["char"])

xsize = d.get("xsize", 16)
fixed_rows = []

for li, layer in enumerate(d["slices"]):
    for ri, row in enumerate(layer):
        bad = [c for c in row if c not in defined]
        if bad:
            # 替换为 xsize 个空格（palette 中 ' ' = minecraft:air）
            new_row = " " * xsize
            fixed_rows.append((li, ri, row, new_row, bad))
            d["slices"][li][ri] = new_row

with open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

with open(r"D:\gengxin\LostCities-extend\LostCities-extend-1-21\fix_wd_report.txt", "w", encoding="utf-8") as f:
    if fixed_rows:
        for li, ri, old, new, bad in fixed_rows:
            f.write(f"fixed layer {li} row {ri}: bad_chars={bad}\n  old={old!r}\n  new={new!r}\n")
    else:
        f.write("no undefined-char rows found\n")
print("done")
