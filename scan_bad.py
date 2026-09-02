import os, glob, re

ROOT = os.path.join(os.getcwd(), "data", "lce")
cnt_grass = 0
cnt_struct = 0
files_struct = set()
samples = set()
grass_files = 0

for p in glob.glob(os.path.join(ROOT, "**", "*.json"), recursive=True):
    try:
        txt = open(p, encoding="utf-8").read()
    except Exception:
        continue
    if "minecraft:grass" in txt:
        cnt_grass += txt.count("minecraft:grass")
        grass_files += 1
    for m in re.findall(r"minecraft:structure_[A-Za-z_]*", txt):
        if m != "minecraft:structure_void":
            samples.add(m)
            cnt_struct += 1
            files_struct.add(p)

print("minecraft:grass 出现次数:", cnt_grass, " 文件数:", grass_files)
print("损坏 structure_ 出现次数:", cnt_struct, " 涉及文件数:", len(files_struct))
print("损坏样本(前15):", sorted(samples)[:15])
with open("scan_result.txt", "w", encoding="utf-8") as f:
    f.write(f"grass={cnt_grass}\ngrass_files={grass_files}\nstruct={cnt_struct}\n")
    for s in sorted(samples):
        f.write(s + "\n")
