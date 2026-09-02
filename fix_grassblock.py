import os, glob

ROOT = r"D:\gengxin\LostCities-extend\LostCities-extend-1-21\data\lce"
BAD = "minecraft:short_grass_block"
GOOD = "minecraft:grass_block"

changed = 0
total = 0
for p in glob.glob(os.path.join(ROOT, "**", "*.json"), recursive=True):
    try:
        t = open(p, encoding="utf-8").read()
    except Exception:
        continue
    if BAD in t:
        n = t.count(BAD)
        total += n
        t = t.replace(BAD, GOOD)
        open(p, "w", encoding="utf-8").write(t)
        changed += 1

with open(r"D:\gengxin\LostCities-extend\LostCities-extend-1-21\fix_grassblock_report.txt", "w", encoding="utf-8") as f:
    f.write(f"changed_files={changed}\nreplaced={total}\n")
print("done")
