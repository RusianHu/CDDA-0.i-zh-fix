# 中文缺漏补丁：物品名称

这个 mod 用于补充 0.I 发行包 zh_CN 翻译中仍显示英文的玩家可见物品名称。

## 当前覆盖

- `data/json/items/armor/boots.json` 中缺失 zh_CN 的 `name.str_sp`。
- `data/json/items/gun` 与 `data/json/items/magazine` 中缺失 zh_CN 或仍保留半英文品牌名的顶层物品名称。
- `data/json/items/comestibles`、`generic`、`melee`、`tool` 中少量完全未翻译的普通可见物品名称。
- 覆盖 107 个鞋袜、足部护具及成对脚部装备条目。
- 例如 `socks (pair)` 已覆盖为 `袜子（双）`。
- 覆盖鞋袜相关变体名称，例如 `blue striped stockings (pair)`。
- 覆盖 53 个枪械与弹匣顶层名称，其中包括截图中的 `Glock 43` 与 `Glock 43 magazine`。
- 覆盖 15 个通用物品名称，包括未装底火弹壳、长矛、糖衣花生、细切薯条和改装无线电。

## 实现方式

本 mod 从 CDDA 0.I 原版 JSON 克隆完整同 ID `ITEM` 定义，只修改 `name` 字段，再由 mod 覆盖原物品。

注意：不能只写 `{ "id": "...", "name": ... }` 这种局部物品定义，否则会丢失体积、重量、口袋等字段。也不能写成 `id` 与 `copy-from` 相同的自引用形式，否则会触发 `JSON contains circular dependency`。
