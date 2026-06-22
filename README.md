# 中文缺漏补丁：物品名称

这个 mod 用于补充 0.I 发行包 zh_CN 翻译中仍显示英文的玩家可见物品名称。

## 当前覆盖

- `data/json/items/armor/boots.json` 中缺失 zh_CN 的 `name.str_sp`。
- `data/json/items/gun` 与 `data/json/items/magazine` 中缺失 zh_CN 或仍保留半英文品牌名的顶层物品名称。
- `data/json/items/comestibles`、`generic`、`melee`、`tool` 中少量完全未翻译的普通可见物品名称。
- 覆盖 107 个鞋袜、足部护具及成对脚部装备条目。
- 例如 `socks (pair)` 已覆盖为 `袜子（双）`。
- 覆盖 56 个枪械与弹匣顶层名称，其中包括截图中的 `Glock 43` 与 `Glock 43 magazine`。
- 覆盖 15 个通用物品名称，包括未装底火弹壳、长矛、糖衣花生、细切薯条和改装无线电。

## 扫描说明

本次检查直接读取 `lang/mo/zh_CN/LC_MESSAGES/cataclysm-dda.mo`，并与 `data/json/items` 中的物品名称字段比对。扫描到的未翻译项里包含大量 `abstract`、`fake`、模板对象和复数字段；这些通常不是玩家直接看到的名称，所以没有全部强行覆盖。

第二轮扩展额外检查了“翻译结果中仍包含 `Glock` 的名称”，因为这类半翻译不会被普通缺失扫描捕获，但在游戏物品栏中很明显。

第三轮加入 `tools/audit_item_name_gaps.py`，用于扫描玩家可见顶层物品名称字段，并区分：

- 基础 zh_CN 中完全未翻译的名称；
- 已被本 mod 覆盖的缺漏；
- 翻译后仍残留英文 token 的名称。

## 实现方式

CDDA 随包 mod `alt_map_key` 已使用同 ID + `copy-from` 覆盖原对象字段。本 mod 采用同样方式，只替换 `name` 字段，其他物品属性继承原版定义。
