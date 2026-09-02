import os, glob, re, json

ROOT = r"D:\gengxin\LostCities-extend\LostCities-extend-1-21\data\lce"

# 1) 残留坏方块检查
grass_left = 0
struct_bad = 0
for p in glob.glob(os.path.join(ROOT, "**", "*.json"), recursive=True):
    try:
        txt = open(p, encoding="utf-8").read()
    except Exception:
        continue
    if "minecraft:grass\"" in txt or "minecraft:grass," in txt or ":grass]" in txt or "\"minecraft:grass\"" in txt:
        grass_left += txt.count("minecraft:grass")
    for m in re.findall(r"minecraft:structure_[A-Za-z_]*", txt):
        if m not in ("minecraft:structure_void", "minecraft:structure_block"):
            struct_bad += 1

print("[残留检查] minecraft:grass:", grass_left, " 损坏structure_:", struct_bad)

# 2) 楼层/地下室 part 一致性
PARTS = os.path.join(ROOT, "lostcities", "parts")
BUILD = os.path.join(ROOT, "lostcities", "buildings")
part_files = set(fn[:-5] for fn in os.listdir(PARTS) if fn.endswith(".json"))
stems = set(re.sub(r'_parts\d+$', '', pf) for pf in part_files)

def has_prefix_floor(prefix, floor):
    return f"{prefix}_{floor}" in stems

issues = 0
for bfn in sorted(os.listdir(BUILD)):
    if not bfn.endswith(".json"):
        continue
    try:
        b = json.load(open(os.path.join(BUILD, bfn), encoding="utf-8"))
    except Exception:
        continue
    raw = b.get("parts")
    prefixes = []
    if isinstance(raw, str):
        prefixes = [raw]
    elif isinstance(raw, list):
        for x in raw:
            if isinstance(x, str):
                prefixes.append(x)
            elif isinstance(x, dict):
                for v in x.values():
                    if isinstance(v, str):
                        prefixes.append(v)
    elif isinstance(raw, dict):
        for v in raw.values():
            if isinstance(v, str):
                prefixes.append(v)
            elif isinstance(v, list):
                prefixes.extend(p for p in v if isinstance(p, str))
    if not prefixes:
        prefixes = [bfn[:-5]]

    minf = int(b.get("minfloors", b.get("floors", 1)))
    maxf = int(b.get("maxfloors", b.get("floors", 1)))
    maxc = int(b.get("maxcellars", b.get("cellars", 0)))
    for pre in prefixes:
        miss = []
        for fl in range(0, maxf + 1):
            if not has_prefix_floor(pre, fl):
                miss.append(f"F{fl}")
        for cl in range(-maxc, 0):
            if not has_prefix_floor(pre, cl):
                miss.append(f"C{cl}")
        if miss:
            issues += 1
            print(f"  [{bfn}] 前缀={pre} minf={minf} maxf={maxf} maxc={maxc} 缺失: {','.join(miss)}")

print("[楼层一致性] 缺失建筑数:", issues)
with open("verify_report.txt", "w", encoding="utf-8") as f:
    f.write(f"grass_left={grass_left}\nstruct_bad={struct_bad}\nfloor_issues={issues}\n")
