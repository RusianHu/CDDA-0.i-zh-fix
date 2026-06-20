# 中文缺漏补丁：物品名称

这个 mod 用于补充 0.I 发行包 zh_CN 翻译中仍显示英文的玩家可见物品名称。

## 当前覆盖

- `data/json/items/armor/boots.json` 中缺失 zh_CN 的 `name.str_sp`。
- 覆盖 107 个鞋袜、足部护具及成对脚部装备条目。
- 例如 `socks (pair)` 已覆盖为 `袜子（双）`。

## 扫描说明

本次检查直接读取 `lang/mo/zh_CN/LC_MESSAGES/cataclysm-dda.mo`，并与 `data/json/items` 中的物品名称字段比对。扫描到的未翻译项里包含大量 `abstract`、`fake`、模板对象和复数字段；这些通常不是玩家直接看到的名称，所以没有全部强行覆盖。

## 实现方式

CDDA 随包 mod `alt_map_key` 已使用同 ID + `copy-from` 覆盖原对象字段。本 mod 采用同样方式，只替换 `name` 字段，其他物品属性继承原版定义。
