#!/usr/bin/env python3
"""Repair malformed Hugo front matter under content/.

Idempotent: clean files are left untouched. Prints one line per repaired
file to stdout (read by brain_on.sh) and a summary on the last line.

Repairs handled:
  unwrap-yaml-fence     Front matter wrapped in ```yaml ... ``` (Hugo would
                        not parse it at all).
  trim-closing-fence    Closing --- has 4+ dashes; the extras leak into the
                        body as a Markdown thematic break.
  trim-blank-after-open Blank lines immediately after the opening --- (some
                        parsers tolerate this, but normalising keeps diffs
                        clean and avoids surprises).
  add-frontmatter       File has no --- block at all but begins with a # h1
                        heading; generates title + weight (from numeric stem)
                        so Hugo renders it with correct metadata.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content"


def repair(text: str, path: Path | None = None):
    reasons: list[str] = []
    s = text

    # 1. Unwrap ```yaml ... ``` around the front matter. Tolerate a
    #    multi-dash inner closer (we'll re-emit it as plain ---).
    m = re.match(
        r"\A﻿?```ya?ml[ \t]*\n(---[ \t]*\n.*?\n)-{3,}[ \t]*\n```[ \t]*\n",
        s,
        flags=re.DOTALL,
    )
    if m:
        s = m.group(1) + "---\n" + s[m.end():]
        reasons.append("unwrap-yaml-fence")

    # 2. Normalise a multi-dash closing fence ("---------") to "---".
    fences = list(re.finditer(r"^-{3,}[ \t]*$", s, flags=re.MULTILINE))
    if len(fences) >= 2 and fences[0].start() == 0:
        closer = fences[1]
        matched = s[closer.start():closer.end()].rstrip()
        if matched != "---":
            s = s[:closer.start()] + "---" + s[closer.end():]
            reasons.append("trim-closing-fence")

    # 3. Trim blank lines right after the opening "---".
    s2 = re.sub(r"\A(---[ \t]*\n)(?:[ \t]*\n)+", r"\1", s)
    if s2 != s:
        s = s2
        reasons.append("trim-blank-after-open")

    # 4. Add minimal frontmatter when the file has none at all but starts with
    #    a # h1 heading (typical for hand-written chapter files in deep/).
    if path is not None and not s.lstrip("﻿").startswith("---"):
        m = re.search(r"^# (.+)", s, re.MULTILINE)
        if m:
            title = m.group(1).strip()
            stem = path.stem
            try:
                weight = int(stem)
            except ValueError:
                weight = None
            fm = ["---", f'title: "{title}"']
            if weight is not None:
                fm.append(f"weight: {weight}")
            fm.append("---\n")
            s = "\n".join(fm) + "\n" + s
            reasons.append("add-frontmatter")

    return s, reasons


def main() -> int:
    if not ROOT.is_dir():
        print(f"fix_frontmatter: content dir not found: {ROOT}", file=sys.stderr)
        return 0

    fixed = 0
    for path in ROOT.rglob("*.md"):
        try:
            old = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as e:
            print(f"skip {path}: {e}", file=sys.stderr)
            continue
        new, reasons = repair(old, path)
        if reasons:
            path.write_text(new, encoding="utf-8")
            rel = path.relative_to(ROOT.parent)
            print(f"fixed {rel}: {','.join(reasons)}")
            fixed += 1

    if fixed:
        print(f"front-matter repairs: {fixed} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
