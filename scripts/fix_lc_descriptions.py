#!/usr/bin/env python3
"""Backfill smart-truncated descriptions in LeetCode frontmatter.

Re-extracts description from the solution body so already-truncated
frontmatter descriptions are replaced with properly sentence-bounded ones.
"""
import re
import sys
from pathlib import Path

MAX_CHARS = 280


def smart_truncate(text: str, max_chars: int = MAX_CHARS) -> str:
    if len(text) <= max_chars:
        return text
    window = text[:max_chars]
    last = -1
    for ch in ".!?":
        idx = window.rfind(ch)
        if idx > last:
            last = idx
    if last >= max_chars * 2 // 5:
        return text[: last + 1].strip()
    cut = window.rfind(" ")
    if cut > 0:
        return window[:cut].rstrip(",:;") + "…"
    return window + "…"


def extract_desc_from_body(body: str) -> str:
    """Re-derive a clean description from the solution markdown body.

    Skips the standard LeetCode header (link, Difficulty, Topics, ## Solution)
    and grabs the first prose paragraph after it.
    """
    # Drop code blocks first
    text = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    # Skip past "## Solution" heading — actual prose follows after it
    solution_split = re.split(r"^##\s+Solution\b.*$", text, maxsplit=1, flags=re.MULTILINE)
    if len(solution_split) == 2:
        text = solution_split[1]
    # Strip remaining headings, inline math, markdown formatting
    text = re.sub(r"#+\s+.*\n", "", text)
    text = re.sub(r"\$\$[^$]+\$\$", "", text)
    text = re.sub(r"\$[^$\n]+\$", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)  # links → link text
    text = re.sub(r"[*_`#>\\|]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return smart_truncate(text)


DESC_RE = re.compile(r'^(description:\s*)"(.*)"(\s*)$', re.MULTILINE)


def fix_file(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")

    # Split frontmatter from body — must find "---" on its own line
    if not raw.startswith("---"):
        return False
    m_close = re.search(r"^\-{3}\s*$", raw[3:], re.MULTILINE)
    if not m_close:
        return False
    fm_end = 3 + m_close.start()
    fm = raw[:fm_end]
    body = raw[fm_end:]

    # Re-derive description from body
    new_desc = extract_desc_from_body(body)
    if not new_desc:
        return False

    # Check existing description
    m = DESC_RE.search(fm)
    if not m:
        return False
    old_desc = m.group(2).replace('\\"', '"')
    if old_desc == new_desc:
        return False

    escaped = new_desc.replace('"', '\\"')
    new_fm = DESC_RE.sub(
        lambda _: f'{m.group(1)}"{escaped}"{m.group(3)}', fm, count=1
    )
    if new_fm == fm:
        return False

    path.write_text(new_fm + body, encoding="utf-8")
    return True


def main() -> None:
    root = Path("/Users/apple/github/tamnd/brain/content")
    files = sorted(root.rglob("*.md"))
    lc_files = [
        f for f in files
        if re.search(r"/leetcode/\d", str(f)) and f.stem.isdigit()
    ]

    changed = 0
    for f in lc_files:
        if fix_file(f):
            changed += 1
            if "--quiet" not in sys.argv:
                print(f"fixed: {f.relative_to(root)}")

    print(f"\n{changed}/{len(lc_files)} files updated.")


if __name__ == "__main__":
    main()
