from __future__ import annotations

import hashlib
from pathlib import Path

from .models import QueueItem, TranslationQueue, TranslationState, utcnow


def file_hash(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def dest_path(source_path: str) -> str:
    """Map content/en/foo/bar.md -> content/foo/bar.md (path in target repo)."""
    parts = source_path.split("/", 2)
    if len(parts) >= 3 and parts[0] == "content" and parts[1] == "en":
        return f"content/{parts[2]}"
    return source_path


# Leaf pages in these sections carry a date and appear on home + calendar
_DATED_SECTIONS = frozenset({"docs", "languages", "maths", "practice", "programming", "research", "write"})


def _calc_priority(rel: str, base: int = 0) -> int:
    parts = rel.split("/")
    is_idx = parts[-1] == "_index.md"
    depth = len(parts) - 1
    # Top-level section _index.md (depth<=3): translate first to populate sidebar
    if is_idx and depth <= 3:
        return base + 100
    # Dated-section leaf pages: fill home/calendar next
    section = parts[2] if len(parts) > 2 else ""
    if not is_idx and section in _DATED_SECTIONS:
        return base + 20
    # Deeper _index.md: useful but not urgent — after dated leaf pages
    if is_idx:
        return base + 15
    # Undated leaf pages (deep/, spec/, wiki/): last
    return base


def scan_source(
    source_repo: Path,
    state: TranslationState,
    queue: TranslationQueue,
) -> tuple[list[str], list[str]]:
    """Walk content/en, detect new and changed .md files, append to queue.

    Returns (new_files, changed_files) — relative paths from repo root.
    Only adds files not already in queue.pending.
    """
    content_en = source_repo / "content" / "en"
    if not content_en.exists():
        raise FileNotFoundError(f"content/en not found at {source_repo}")

    pending_set = {item.source_path for item in queue.pending}
    new_files: list[str] = []
    changed: list[str] = []

    for md in sorted(content_en.rglob("*.md")):
        rel = str(md.relative_to(source_repo))
        if rel in pending_set:
            continue
        h = file_hash(md)
        if rel not in state.files:
            new_files.append(rel)
            queue.pending.append(QueueItem(source_path=rel, priority=_calc_priority(rel), added_at=utcnow()))
        elif state.files[rel].source_hash != h:
            changed.append(rel)
            queue.pending.append(QueueItem(source_path=rel, priority=_calc_priority(rel, base=10), added_at=utcnow()))

    # Higher priority first, then stable sort by path
    queue.pending.sort(key=lambda x: (-x.priority, x.source_path))
    return new_files, changed
