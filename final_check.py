import os, glob, re

ROOT = r"D:\gengxin\LostCities-extend\LostCities-extend-1-21\data\lce"
cnt = {"grass": 0, "short_grass": 0, "grass_block": 0, "short_grass_block": 0, "struct_bad": 0}
struct_pat = re.compile(r"minecraft:structure_[A-Za-z_]*")
for p in glob.glob(os.path.join(ROOT, "**", "*.json"), recursive=True):
    try:
        t = open(p, encoding="utf-8").read()
    except Exception:
        continue
    cnt["grass"] += t.count("minecraft:grass\"") + t.count("minecraft:grass,")
    cnt["short_grass"] += t.count("minecraft:short_grass")
    cnt["grass_block"] += t.count("minecraft:grass_block")
    cnt["short_grass_block"] += t.count("minecraft:short_grass_block")
    for m in struct_pat.findall(t):
        if m not in ("minecraft:structure_void", "minecraft:structure_block"):
            cnt["struct_bad"] += 1

# 注意：short_grass 计数会包含 short_grass_block 的部分，需扣除
cnt["short_grass"] -= cnt["short_grass_block"]

with open(r"D:\gengxin\LostCities-extend\LostCities-extend-1-21\final_check.txt", "w", encoding="utf-8") as f:
    f.write(
        f"裸 minecraft:grass(应为0)      = {cnt['grass']}\n"
        f"minecraft:short_grass(装饰草)  = {cnt['short_grass']}\n"
        f"minecraft:grass_block(草方块)  = {cnt['grass_block']}\n"
        f"误改 short_grass_block(应为0)  = {cnt['short_grass_block']}\n"
        f"损坏 structure_(应为0)         = {cnt['struct_bad']}\n"
    )
print("done")
