#!/usr/bin/env python3
"""Strip ChatGPT oai_citation references from markdown files.

Idempotent: files with no such references are untouched. Prints one line
per cleaned file (read by brain_on.sh) and a summary at the end.

Removes inline patterns like:
  [oai_citation:0‡Some Title](https://example.com/?utm_source=chatgpt.com)
including any leading spaces on the same line before the citation, and
collapses lines that become blank after removal.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content"

# Matches the full oai_citation markdown link, plus any spaces before it on
# the same line (so "text  [oai_citation:...]" → "text" with no trailing gap).
_CITE_RE = re.compile(r' *\[oai_citation:[^\]]*\]\([^)]*\)')


def clean(text: str):
    new = _CITE_RE.sub("", text)
    # Collapse three or more consecutive blank lines down to two.
    new = re.sub(r'\n{3,}', '\n\n', new)
    return new, new != text


def main() -> int:
    if not ROOT.is_dir():
        print(f"fix_chatgpt: content dir not found: {ROOT}", file=sys.stderr)
        return 0

    fixed = 0
    for path in ROOT.rglob("*.md"):
        try:
            old = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as e:
            print(f"skip {path}: {e}", file=sys.stderr)
            continue
        new, changed = clean(old)
        if changed:
            path.write_text(new, encoding="utf-8")
            rel = path.relative_to(ROOT.parent)
            print(f"fixed {rel}: strip-chatgpt-citations")
            fixed += 1

    if fixed:
        print(f"chatgpt-citation strips: {fixed} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
