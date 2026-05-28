#!/usr/bin/env python3
"""Backfill smart-truncated descriptions for all Codeforces brain files."""

import re
import sys
from pathlib import Path

BRAIN = Path(__file__).parent.parent
CF_DIR = BRAIN / "content/en/practice/codeforces"
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


FM_CLOSE = re.compile(r"^-{3}\s*$", re.MULTILINE)
# Matches any ## heading that could precede problem description text
PROB_SECTION = re.compile(r"^#{2}\s+Problem\s+Understanding\b", re.MULTILINE | re.IGNORECASE)


def extract_desc(body: str) -> str | None:
    """Extract first substantial paragraph from Problem Understanding section."""
    m = PROB_SECTION.search(body)
    if not m:
        return None
    after = body[m.end():]
    # Skip blank lines after the heading
    paragraphs = [p.strip() for p in after.split("\n\n") if p.strip()]
    for para in paragraphs:
        # Skip lines that are headings, table rows, or code blocks
        if para.startswith("#") or para.startswith("|") or para.startswith("```"):
            continue
        # Strip markdown bold/italic/code for clean text
        text = re.sub(r"`[^`]+`", lambda m: m.group(0)[1:-1], para)
        text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
        text = re.sub(r"\*([^*]+)\*", r"\1", text)
        text = re.sub(r"\$[^$]+\$", "", text)  # strip inline math
        text = " ".join(text.split())
        if len(text) >= 40:
            return text
    return None


def process_file(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        return False

    # Find frontmatter closing ---
    m = FM_CLOSE.search(raw, 3)
    if not m:
        return False
    fm_end = m.end()
    frontmatter = raw[3:m.start()]
    body = raw[fm_end:]

    desc_m = re.search(r'^description:\s*"(.*?)"\s*$', frontmatter, re.MULTILINE)
    if not desc_m:
        return False
    current_desc = desc_m.group(1)

    new_desc_raw = extract_desc(body)
    if not new_desc_raw:
        return False

    new_desc = smart_truncate(new_desc_raw)
    if new_desc == current_desc:
        return False

    # Replace description in frontmatter
    escaped = new_desc.replace("\\", "\\\\").replace('"', '\\"')
    new_fm = re.sub(
        r'^(description:\s*)".*?"',
        f'\\1"{escaped}"',
        frontmatter,
        flags=re.MULTILINE,
    )
    new_raw = "---" + new_fm + "---" + body
    path.write_text(new_raw, encoding="utf-8")
    return True


def main():
    files = sorted(CF_DIR.rglob("*.md"))
    files = [f for f in files if f.name != "_index.md"]
    updated = 0
    skipped = 0
    for f in files:
        try:
            if process_file(f):
                updated += 1
                print(f"  updated: {f.relative_to(BRAIN)}")
            else:
                skipped += 1
        except Exception as e:
            print(f"  ERROR {f}: {e}", file=sys.stderr)
    print(f"\nDone: {updated} updated, {skipped} unchanged out of {len(files)} files.")


if __name__ == "__main__":
    main()
