import os, glob, re, json

ROOT = r"D:\gengxin\LostCities-extend\LostCities-extend-1-21\data\lce"
PARTS = os.path.join(ROOT, "lostcities", "parts")
BUILD = os.path.join(ROOT, "lostcities", "buildings")
PARTFILES = set(fn[:-5] for fn in os.listdir(PARTS) if fn.endswith(".json"))

out = []

# ---- 1) grass / structure 残留 ----
grass_left = 0
struct_bad = 0
for p in glob.glob(os.path.join(ROOT, "**", "*.json"), recursive=True):
    try:
        txt = open(p, encoding="utf-8").read()
    except Exception:
        continue
    grass_left += txt.count("minecraft:grass")
    for m in re.findall(r"minecraft:structure_[A-Za-z_]*", txt):
        if m not in ("minecraft:structure_void", "minecraft:structure_block"):
            struct_bad += 1
out.append(f"[1] 残留 minecraft:grass = {grass_left}")
out.append(f"[1] 残留 损坏structure_ = {struct_bad}")

# ---- 2) slices 未定义字符 ----
slice_issues = 0
SPECIAL = set(" ")  # 空格=air，由 palette 定义；这里只检查 palette 之外的
for p in sorted(glob.glob(os.path.join(PARTS, "*.json"))):
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        out.append(f"  [解析失败] {os.path.basename(p)}: {e}")
        continue
    pal = d.get("palette", {}).get("palette", [])
    defined = set()
    for e in pal:
        if isinstance(e, dict) and "char" in e:
            defined.add(e["char"])
    # slices 可能是 list[str] 或嵌套
    slices = d.get("slices", [])
    if isinstance(slices, dict):
        slices = list(slices.values())
    def walk(o):
        if isinstance(o, str):
            return list(o)
        if isinstance(o, list):
            r = []
            for x in o:
                r += walk(x)
            return r
        return []
    used = walk(slices)
    undef = set(c for c in used if c not in defined)
    if undef:
        slice_issues += 1
        out.append(f"  [未定义字符] {os.path.basename(p)}: {sorted(undef)[:10]}")
out.append(f"[2] slices 未定义字符文件数 = {slice_issues}")

# ---- 3) 楼层/地下室一致性（正确格式：parts = list of {{part, floor}}）----
floor_issues = 0
def strip_ns(s):
    return s.split(":", 1)[1] if ":" in s else s

for bfn in sorted(os.listdir(BUILD)):
    if not bfn.endswith(".json"):
        continue
    try:
        b = json.load(open(os.path.join(BUILD, bfn), encoding="utf-8"))
    except Exception:
        continue
    minf = int(b.get("minfloors", b.get("floors", 0)))
    maxf = int(b.get("maxfloors", b.get("floors", 0)))
    maxc = int(b.get("maxcellars", b.get("cellars", 0)))

    # 收集所有 parts 列表（parts, parts2, parts3 ...）
    mapped = {}  # floor -> [parts]
    for key in list(b.keys()):
        if re.match(r"^parts\d*$", key):
            val = b[key]
            if isinstance(val, list):
                for item in val:
                    if isinstance(item, dict) and "part" in item and "floor" in item:
                        fl = int(item["floor"])
                        mapped.setdefault(fl, []).append(strip_ns(item["part"]))
                    elif isinstance(item, str):
                        # 纯字符串形式：lce:xxx 当作整栋建筑的单 part
                        pass

    miss = []
    for fl in range(0, maxf + 1):
        if fl not in mapped or not mapped[fl]:
            miss.append(f"F{fl}")
    for cl in range(-maxc, 0):
        if cl not in mapped or not mapped[cl]:
            miss.append(f"C{cl}")
    # 检查每个 mapped part 文件是否存在
    missing_files = []
    for fl, parts in mapped.items():
        for pn in parts:
            if pn not in PARTFILES:
                missing_files.append(f"{pn}(floor {fl})")
    if miss or missing_files:
        floor_issues += 1
        out.append(f"  [{bfn}] minf={minf} maxf={maxf} maxc={maxc} 缺层:{','.join(miss)} 缺文件:{','.join(missing_files[:5])}")

out.append(f"[3] 楼层/文件缺失建筑数 = {floor_issues}")

with open("verify2_report.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
print("done")
