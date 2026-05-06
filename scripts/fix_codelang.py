#!/usr/bin/env python3
"""Add language tags to code fences that use naming-convention ids.

Idempotent: files that are already correct are untouched. Prints one line
per repaired file (read by brain_on.sh) and a summary at the end.

Convention detected:
  ```id="...-python"  →  ```python id="...-python"
  ```id="...-go"      →  ```go id="...-go"

Blocks with other id suffixes (pseudocode) are left unchanged.
Blocks that already have a language tag are left unchanged.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content"

# Map id suffix → language tag.  Add more here as needed.
LANG_SUFFIXES = {
    "-python": "python",
    "-go":     "go",
}

# Matches a code fence opening that has ONLY an id= attribute (no language yet).
# Group 1 = indentation/backticks, group 2 = full id="..." value.
_FENCE_RE = re.compile(r'^(```)(id="[^"]*")$', re.MULTILINE)


def _replace(m: re.Match) -> str:
    backticks = m.group(1)
    id_attr   = m.group(2)          # e.g.  id="array-tiling-python"
    # Extract the id value (strip id=" and closing ")
    id_value = id_attr[4:-1]        # e.g.  array-tiling-python
    for suffix, lang in LANG_SUFFIXES.items():
        if id_value.endswith(suffix):
            return f"{backticks}{lang} {id_attr}"
    return m.group(0)               # no recognised suffix → leave unchanged


def repair(text: str):
    new = _FENCE_RE.sub(_replace, text)
    return new, new != text


def main() -> int:
    if not ROOT.is_dir():
        print(f"fix_codelang: content dir not found: {ROOT}", file=sys.stderr)
        return 0

    fixed = 0
    for path in ROOT.rglob("*.md"):
        try:
            old = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as e:
            print(f"skip {path}: {e}", file=sys.stderr)
            continue
        new, changed = repair(old)
        if changed:
            path.write_text(new, encoding="utf-8")
            rel = path.relative_to(ROOT.parent)
            print(f"fixed {rel}: add-lang-tag")
            fixed += 1

    if fixed:
        print(f"code-lang repairs: {fixed} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
