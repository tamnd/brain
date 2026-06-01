#!/usr/bin/env python3
"""Fix display math rendering issues in $$...$$ blocks.

Two problems:
1. Blank lines inside $$ break KaTeX (terminates block early).
2. Inline-opened $$ (content on same line as opener) with newlines causes
   Goldmark setext-heading mis-parsing (a bare '=' or '-' on its own line
   is treated as a setext heading marker).

Fix: for inline-opened blocks, collapse all internal newlines to spaces.
For block-form $$ (opener alone on its own line), collapse blank lines only.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content"


def fix(text: str) -> tuple[str, bool]:
    parts = re.split(r'(\$\$)', text)
    out: list[str] = []
    inside = False
    for part in parts:
        if part == '$$':
            inside = not inside
            out.append(part)
        elif inside:
            # inline-open: content doesn't start with \n
            if not part.startswith('\n'):
                fixed = re.sub(r'\n+', ' ', part).strip()
            else:
                # block-form: only collapse blank lines
                fixed = re.sub(r'\n{2,}', '\n', part)
            out.append(fixed)
        else:
            out.append(part)
    new = ''.join(out)
    return new, new != text


def main() -> None:
    changed = []
    for path in sorted(ROOT.rglob('*.md')):
        text = path.read_text(encoding='utf-8')
        new, did_change = fix(text)
        if did_change:
            path.write_text(new, encoding='utf-8')
            changed.append(str(path.relative_to(ROOT.parent)))
    if changed:
        for c in changed:
            print(f'fixed display-math: {c}')


if __name__ == '__main__':
    main()
