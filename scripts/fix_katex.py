#!/usr/bin/env python3
r"""Fix common KaTeX-invalid sequences that ChatGPT writes in math blocks.

Patterns fixed (inside $...$ and $$...$$, not in code blocks):
  \*   → *       (asterisk — not a valid LaTeX command)
  \+   → +       (plus — not a valid LaTeX command)
  \=   → =       (equals — not a valid LaTeX command)
  align\* inside $$ → align*   (escaped star in env name)

Idempotent; skips fenced code blocks.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content"

_FENCE = re.compile(r'^[ \t]*(```|~~~)')
# Matches inline math $...$ (non-greedy, no newlines)
_INLINE = re.compile(r'\$([^$\n]+?)\$')
# Matches block math $$...$$  (dotall)
_BLOCK = re.compile(r'\$\$(.*?)\$\$', re.DOTALL)

# (pattern, replacement) pairs applied inside math
_MATH_FIXES: list[tuple[re.Pattern, str]] = [
    (re.compile(r'\\([*+=])'), r'\1'),          # \* \+ \= → bare char
    (re.compile(r'align\\(\*)'), r'align\1'),   # align\* → align*
]


def _fix_math(m: re.Match) -> str:
    inner = m.group(1) if m.lastindex == 1 else m.group(0)
    delim = '$' if m.group(0).startswith('$') and not m.group(0).startswith('$$') else '$$'
    changed = inner
    for pat, repl in _MATH_FIXES:
        changed = pat.sub(repl, changed)
    if delim == '$':
        return f'${changed}$'
    return f'$${changed}$$'


def fix(text: str) -> tuple[str, bool]:
    lines = text.split('\n')
    out_lines: list[str] = []
    in_fence = False
    in_block = False
    block_buf: list[str] = []
    block_start: int = -1

    i = 0
    while i < len(lines):
        line = lines[i]

        if _FENCE.match(line):
            in_fence = not in_fence
            out_lines.append(line)
            i += 1
            continue

        if in_fence:
            out_lines.append(line)
            i += 1
            continue

        stripped = line.strip()
        if stripped == '$$':
            if not in_block:
                in_block = True
                block_buf = [line]
                block_start = len(out_lines)
            else:
                in_block = False
                block_buf.append(line)
                block_text = '\n'.join(block_buf)
                # apply fixes to block interior (between the $$ markers)
                interior = '\n'.join(block_buf[1:-1])
                fixed_interior = interior
                for pat, repl in _MATH_FIXES:
                    fixed_interior = pat.sub(repl, fixed_interior)
                if fixed_interior != interior:
                    block_buf = [block_buf[0]] + fixed_interior.split('\n') + [block_buf[-1]]
                out_lines.extend(block_buf)
                block_buf = []
            i += 1
            continue

        if in_block:
            block_buf.append(line)
            i += 1
            continue

        # Inline math: apply fixes
        new_line = _INLINE.sub(_fix_math, line)
        out_lines.append(new_line)
        i += 1

    if block_buf:  # unclosed block — emit as-is
        out_lines.extend(block_buf)

    new = '\n'.join(out_lines)
    return new, new != text


def main() -> int:
    if not ROOT.is_dir():
        print(f"fix_katex: content dir not found: {ROOT}", file=sys.stderr)
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
            print(f"fixed {rel}: katex-invalid-sequences")
            fixed += 1

    if fixed:
        print(f"katex fixes: {fixed} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
