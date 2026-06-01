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
  fix-yaml-escapes      Double-quoted YAML values containing LaTeX-style
                        backslash sequences (e.g. \\geq, \\leq) that are invalid
                        in YAML 1.1/1.2 strict mode (Hugo v0.146+). Converts
                        affected double-quoted strings to single-quoted, which
                        treats backslashes as literals.
  dedup-keys            Duplicate top-level YAML keys in the front matter
                        (Hugo v0.161 strict mode rejects them). Keeps the first
                        occurrence of each key and drops subsequent duplicates.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content"

# Valid characters immediately following a backslash in a YAML double-quoted
# string (YAML 1.2 spec §7.3.1).  Anything else is an invalid escape.
_VALID_DQUOTE_NEXT: frozenset[str] = frozenset(
    "0abtTnNvfre \t\"\\/_LPxuU"
)


def _has_invalid_yaml_escape(inner: str) -> bool:
    """Return True if *inner* (the content between the double quotes) contains
    a backslash followed by a character that is not a valid YAML escape."""
    i = 0
    while i < len(inner):
        if inner[i] == "\\":
            if i + 1 >= len(inner) or inner[i + 1] not in _VALID_DQUOTE_NEXT:
                return True
            i += 2
        else:
            i += 1
    return False


def _extract_fm(text: str):
    """Return (open_fence, fm_body, close_fence, rest) or None."""
    m = re.match(r"\A(﻿?---[ \t]*\n)(.*?\n)(---[ \t]*\n)(.*)", text, re.DOTALL)
    if not m:
        return None
    return m.group(1), m.group(2), m.group(3), m.group(4)


def _fix_yaml_escapes(fm_body: str) -> tuple[str, int]:
    """Convert double-quoted YAML values with invalid escapes to single-quoted.

    Only handles simple single-line key: "value" patterns, which cover
    the description/title fields that are the source of LaTeX-escape issues
    in the brain corpus.
    """
    # Matches: optional indent, key name, colon+space, double-quoted value
    # The value regex captures the inner content, allowing escaped chars.
    pattern = re.compile(
        r'^(\s*[\w][\w .\-]*?\s*:\s*)"((?:[^"\\]|\\.)*)"([ \t]*)$',
        re.MULTILINE,
    )
    count = 0

    def replacer(m: re.Match) -> str:
        nonlocal count
        inner = m.group(2)
        if not _has_invalid_yaml_escape(inner):
            return m.group(0)
        count += 1
        # Escape existing single quotes for YAML single-quoted syntax
        sq_inner = inner.replace("'", "''")
        return f"{m.group(1)}'{sq_inner}'{m.group(3)}"

    new_body = pattern.sub(replacer, fm_body)
    return new_body, count


def _dedup_yaml_keys(fm_body: str) -> tuple[str, int]:
    """Remove duplicate top-level YAML keys, keeping the first occurrence."""
    # A top-level key line: no leading whitespace, word chars, then colon.
    key_re = re.compile(r"^([\w][\w .\-]*?)\s*:", )
    lines = fm_body.splitlines(keepends=True)
    seen: set[str] = set()
    result: list[str] = []
    removed = 0
    skip_until_next_key = False

    for line in lines:
        m = key_re.match(line) if not line.startswith(" ") else None
        if m:
            key = m.group(1).strip()
            if key in seen:
                removed += 1
                skip_until_next_key = True
                continue
            seen.add(key)
            skip_until_next_key = False
        elif skip_until_next_key and (line.startswith(" ") or line.startswith("\t")):
            # continuation of a multi-line duplicate value — skip it too
            removed += 1
            continue
        else:
            skip_until_next_key = False
        result.append(line)
    return "".join(result), removed


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

    # 5. Fix invalid YAML escape sequences in double-quoted values
    #    (Hugo v0.146+ strict YAML rejects e.g. \geq, \leq, \cdot).
    parts = _extract_fm(s)
    if parts:
        open_, body, close_, rest = parts
        new_body, n = _fix_yaml_escapes(body)
        if n:
            s = open_ + new_body + close_ + rest
            reasons.append(f"fix-yaml-escapes({n})")

    # 6. Remove duplicate top-level YAML keys (Hugo v0.161 strict mode rejects them).
    parts = _extract_fm(s)
    if parts:
        open_, body, close_, rest = parts
        new_body, n = _dedup_yaml_keys(body)
        if n:
            s = open_ + new_body + close_ + rest
            reasons.append(f"dedup-keys({n})")

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
