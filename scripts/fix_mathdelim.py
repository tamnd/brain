#!/usr/bin/env python3
r"""Normalize block-math delimiters: \[ and \] → $$ on their own lines.

Idempotent: files already using $$ are untouched. Prints one line per
repaired file (read by brain_on.sh) and a summary at the end.

Skips content inside fenced code blocks (``` or ~~~) so that LaTeX
source examples are never altered.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content"

_FENCE = re.compile(r'^[ \t]*(```|~~~)')


def fix(text: str) -> tuple[str, bool]:
    lines = text.split('\n')
    out = []
    in_code = False

    for line in lines:
        if _FENCE.match(line):
            in_code = not in_code
            out.append(line)
            continue

        if not in_code and line.strip() in (r'\[', r'\]'):
            # Preserve any leading indentation, replace the delimiter only.
            indent = line[: len(line) - len(line.lstrip())]
            out.append(indent + '$$')
        else:
            out.append(line)

    new = '\n'.join(out)
    return new, new != text


def main() -> int:
    if not ROOT.is_dir():
        print(f"fix_mathdelim: content dir not found: {ROOT}", file=sys.stderr)
        return 0

    fixed = 0
    for path in ROOT.rglob("*.md"):
        try:
            old = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as e:
            print(f"skip {path}: {e}", file=sys.stderr)
            continue
        new, changed = fix(old)
        if changed:
            path.write_text(new, encoding="utf-8")
            rel = path.relative_to(ROOT.parent)
            print(f"fixed {rel}: normalize-math-delim")
            fixed += 1

    if fixed:
        print(f"math-delim fixes: {fixed} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
