import os, glob, re

ROOT = r"D:\gengxin\LostCities-extend\LostCities-extend-1-21\data\lce"
VALID_STRUCT = {"minecraft:structure_void", "minecraft:structure_block"}

# 匹配 minecraft:structure_ 后跟字母/下划线（捕获所有损坏变体）
struct_pat = re.compile(r"minecraft:structure_[A-Za-z_]*")

grass_re = "minecraft:grass"
grass_fix = "minecraft:short_grass"

changed_files = 0
grass_total = 0
struct_total = 0
corrupt_tokens = set()

for p in glob.glob(os.path.join(ROOT, "**", "*.json"), recursive=True):
    try:
        txt = open(p, encoding="utf-8").read()
    except Exception:
        continue
    if grass_re not in txt and "minecraft:structure_" not in txt:
        continue

    new = txt
    if grass_re in new:
        n = new.count(grass_re)
        grass_total += n
        new = new.replace(grass_re, grass_fix)

    def repl(m):
        global struct_total
        tok = m.group(0)
        if tok in VALID_STRUCT:
            return tok
        struct_total += 1
        corrupt_tokens.add(tok)
        return "minecraft:structure_void"

    new, k = struct_pat.subn(repl, new)
    if k:
        pass

    if new != txt:
        open(p, "w", encoding="utf-8").write(new)
        changed_files += 1

print("修改文件数:", changed_files)
print("替换 minecraft:grass ->", grass_fix, ":", grass_total, "处")
print("替换损坏 structure_ -> minecraft:structure_void :", struct_total, "处")
print("损坏 token 种类:", len(corrupt_tokens))
with open("fix_report.txt", "w", encoding="utf-8") as f:
    f.write(f"changed_files={changed_files}\n")
    f.write(f"grass_fixed={grass_total}\n")
    f.write(f"struct_fixed={struct_total}\n")
    for t in sorted(corrupt_tokens):
        f.write(t + "\n")
