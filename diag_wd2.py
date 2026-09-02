import os, json, glob

PARTS = r"D:\gengxin\LostCities-extend\LostCities-extend-1-21\data\lce\lostcities\parts"
sibs = sorted(glob.glob(os.path.join(PARTS, "wd1imp_0_1_*.json")))
out = []
for p in sibs:
    name = os.path.basename(p)
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        out.append(f"{name}: PARSE ERROR {e}")
        continue
    sl = d.get("slices", [])
    # 第 5 层 (index 4), 第 0 行
    try:
        row = sl[4][0]
        out.append(f"{name}: L4R0 = {row!r}  (len={len(row)})")
    except Exception as e:
        out.append(f"{name}: no L4R0 ({e})")

with open(r"D:\gengxin\LostCities-extend\LostCities-extend-1-21\diag_wd2.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
print("done")
