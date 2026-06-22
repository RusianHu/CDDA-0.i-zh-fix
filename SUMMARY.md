# CDDA 0.I zh_CN 物品名称补漏 mod 总结

## 目标

这个 mod 面向 CDDA 0.I 发行包，补充 zh_CN 环境中仍显示英文或半英文的玩家可见物品名称。

它不修改原版游戏数据文件，通过独立 mod 覆盖同 ID 物品的 `name` 字段实现。

## 当前覆盖范围

- 鞋袜、足部护具及成对脚部装备：107 个。
- 枪械与弹匣顶层名称：56 个。
- 通用物品名称：15 个。

合计覆盖 178 个物品名称条目。

## 已处理的典型问题

- `socks (pair)` -> `袜子（双）`
- `Glock 43` -> `格洛克 43 手枪`
- `Glock 43 magazine` -> `格洛克 43 弹匣`
- `micro conceal carry pistol` -> `微型隐蔽携带手枪`
- `primerless 9x18mm casing` -> `无底火 9x18mm 弹壳`

## 审计方式

仓库包含脚本：

```text
tools/audit_item_name_gaps.py
```

它会扫描基础游戏 `data/json/items` 下玩家可见的顶层 `ITEM.name` 字段，并统计：

- 基础 zh_CN 中完全未翻译的名称；
- 已被本 mod 覆盖的缺漏；
- 翻译后仍残留英文 token 的名称。

最近一次审计结果记录在：

```text
docs/audit_2026-06-22.md
```

## 最近校验

已通过：

```text
cataclysm-tiles.exe --check-mods zh_CN_missing_item_names
cataclysm-tiles.exe --check-mods dda no_npc_food package_bionic_professions translate_dialogue MMA zh_CN_missing_item_names
cataclysm-tiles.exe --jsonverify
```

## 使用方式

把本目录作为 CDDA mod 放入 `data/mods/zh_CN_missing_item_names`，然后在世界 mod 列表中启用：

```json
"zh_CN_missing_item_names"
```
