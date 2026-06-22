#!/usr/bin/env python3
import argparse
import gettext
import json
import os
import re
from pathlib import Path


SKIP_ID_PREFIXES = ( "fake_", "pseudo_" )
SKIP_PATH_PARTS = { "classes" }
ASCII_ALLOW = re.compile(
    r"^(?:mm|cm|ml|mL|L|LR|ACP|S&W|NATO|FMJ|JHP|AP|SP|CB|LFN|FTX|XTP|"
    r"CBM|EMP|LED|LCD|USB|UPS|AR|AI|RDX|HMTD|APEX|FEMA|DARPA|LIXA|NRE|"
    r"UHMWPE|H&K|S&W|M\d+[A-Z]?|Mk\.?\d*|[A-Z]?\d+[A-Z]?|[A-Z]+-\d+[A-Z]*|"
    r"\+P|P\+|Auto|Magnum|BLK|BMG|AE|RPG|BB|I|II|III|IV|V|VI|VII|VIII|IX|X)$"
)


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    return data if isinstance(data, list) else [data]


def iter_item_names(root):
    item_root = root / "data" / "json" / "items"
    for path in item_root.rglob("*.json"):
        rel_parts = set(path.relative_to(item_root).parts)
        if rel_parts & SKIP_PATH_PARTS:
            continue
        try:
            data = load_json(path)
        except Exception:
            continue
        for entry in data:
            if not isinstance(entry, dict) or entry.get("type") != "ITEM" or "abstract" in entry:
                continue
            item_id = str(entry.get("id", ""))
            if not item_id or item_id.startswith(SKIP_ID_PREFIXES):
                continue
            name = entry.get("name")
            if isinstance(name, str):
                yield path, item_id, "name", name
            elif isinstance(name, dict):
                for field in ( "str", "str_sp" ):
                    value = name.get(field)
                    if isinstance(value, str):
                        yield path, item_id, field, value


def load_mod_overrides(mod_dir):
    overrides = {}
    for path in mod_dir.glob("*.json"):
        if path.name == "modinfo.json":
            continue
        try:
            data = load_json(path)
        except Exception:
            continue
        for entry in data:
            if not isinstance(entry, dict) or entry.get("type") != "ITEM":
                continue
            item_id = entry.get("id")
            name = entry.get("name")
            if isinstance(name, str):
                overrides[(item_id, "name")] = name
            elif isinstance(name, dict):
                for field in ( "str", "str_sp" ):
                    if isinstance(name.get(field), str):
                        overrides[(item_id, field)] = name[field]
    return overrides


def ascii_leftovers(text):
    words = re.findall(r"[A-Za-z][A-Za-z0-9+&./-]*", text)
    return [word for word in words if not ASCII_ALLOW.match(word)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="CDDA game root")
    parser.add_argument("--mod-dir", default="data/mods/zh_CN_missing_item_names")
    parser.add_argument("--limit", type=int, default=80)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    mod_dir = (root / args.mod_dir).resolve()
    mo_path = root / "lang" / "mo" / "zh_CN" / "LC_MESSAGES" / "cataclysm-dda.mo"
    with mo_path.open("rb") as handle:
        trans = gettext.GNUTranslations(handle)
    overrides = load_mod_overrides(mod_dir)

    total = 0
    missing = []
    covered_missing = []
    ascii_hits = []
    for path, item_id, field, source in iter_item_names(root):
        total += 1
        zh = trans.gettext(source)
        patched = overrides.get((item_id, field))
        if zh == source:
            row = (str(path.relative_to(root)), item_id, field, source, patched or "")
            if patched:
                covered_missing.append(row)
            else:
                missing.append(row)
        final_text = patched or zh
        leftovers = ascii_leftovers(final_text)
        if leftovers:
            ascii_hits.append((str(path.relative_to(root)), item_id, field, source, final_text, ",".join(leftovers)))

    print(f"visible top-level item name fields: {total}")
    print(f"base fully untranslated: {len(missing) + len(covered_missing)}")
    print(f"covered by this mod: {len(covered_missing)}")
    print(f"still fully untranslated: {len(missing)}")
    print(f"ascii leftovers after this mod: {len(ascii_hits)}")
    print()
    print("Still fully untranslated sample:")
    for row in missing[: args.limit]:
        print("\t".join(row[:4]))
    print()
    print("ASCII leftover sample:")
    for row in ascii_hits[: args.limit]:
        print("\t".join(row))


if __name__ == "__main__":
    main()
