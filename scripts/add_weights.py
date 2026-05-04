#!/usr/bin/env python3
"""Add numeric weight: to frontmatter so Hugo sorts numerically, not alphabetically.

Stem → weight mapping:
  "00"      → 0
  "01"      → 1000
  "01.1"    → 1001
  "01.10"   → 1010
  "01.02"   → 1002   (zero-padded minor)
  directory → same rule on dirname (for _index.md)
"""
import os, re, sys

CONTENT_DIR = os.path.join(os.path.dirname(__file__), "..", "content", "en")


def stem_to_weight(stem: str):
    m = re.fullmatch(r"(\d+)\.0*(\d+)", stem)   # e.g. 01.10, 01.02, 01.2
    if m:
        return int(m.group(1)) * 1000 + int(m.group(2))
    m = re.fullmatch(r"0*(\d+)", stem)           # plain number: 00, 01, 02 …
    if m:
        return int(m.group(1)) * 1000
    return None


def patch_file(path: str, weight: int):
    with open(path) as f:
        raw = f.read()
    if not raw.startswith("---"):
        return False
    end = raw.find("---", 3)
    if end == -1:
        return False
    fm = raw[3:end]
    body = raw[end + 3:]
    if re.search(r"^weight\s*:", fm, re.MULTILINE):
        return False  # already has weight
    new_fm = fm.rstrip("\n") + f"\nweight: {weight}\n"
    with open(path, "w") as f:
        f.write(f"---{new_fm}---{body}")
    return True


changed = 0
for root, dirs, files in os.walk(CONTENT_DIR):
    dirs.sort()
    for fname in sorted(files):
        if not fname.endswith(".md"):
            continue
        path = os.path.join(root, fname)
        if fname == "_index.md":
            stem = os.path.basename(root)
        else:
            stem = fname[:-3]
        w = stem_to_weight(stem)
        if w is None:
            continue
        if patch_file(path, w):
            print(f"  weight={w:6d}  {os.path.relpath(path, CONTENT_DIR)}")
            changed += 1

print(f"\nPatched {changed} files.")
