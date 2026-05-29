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
            queue.pending.append(QueueItem(source_path=rel, priority=0, added_at=utcnow()))
        elif state.files[rel].source_hash != h:
            changed.append(rel)
            queue.pending.append(QueueItem(source_path=rel, priority=1, added_at=utcnow()))

    # Higher priority first, then stable sort by path
    queue.pending.sort(key=lambda x: (-x.priority, x.source_path))
    return new_files, changed
