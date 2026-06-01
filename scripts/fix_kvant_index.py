#!/usr/bin/env python3
"""Regenerate Kvant _index.md files from all present .md files.

Run by brain_on.sh after git pull, so the index always reflects the union of
all servers' solved problems rather than just what one server wrote locally.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content" / "en" / "practice"
SUBJECTS = {
    "math": ROOT / "maths" / "kvant",
    "physics": ROOT / "physics" / "kvant",
}
TAGS = {
    "math": ["kvant", "mathematics", "olympiad"],
    "physics": ["kvant", "physics", "olympiad"],
}
CATEGORIES = {
    "math": ["mathematics"],
    "physics": ["physics"],
}


def _fmt_time(s: int) -> str:
    if s < 60:
        return f"{s}s"
    m, sec = divmod(s, 60)
    return f"{m}m{sec:02d}s" if sec else f"{m}m"


def _list_solutions(subject_dir: Path) -> list[dict]:
    out = []
    for f in subject_dir.glob("*.md"):
        if f.name == "_index.md":
            continue
        try:
            num = int(f.stem)
        except ValueError:
            continue
        text = f.read_text(encoding="utf-8")
        vm = re.search(r'^verified:\s*(true|false)', text, re.MULTILINE)
        tm = re.search(r'^solve_time_s:\s*(\d+)', text, re.MULTILINE)
        out.append({
            "num": num,
            "verified": bool(vm and vm.group(1) == "true"),
            "time_str": _fmt_time(int(tm.group(1))) if tm else "—",
        })
    out.sort(key=lambda d: d["num"])
    return out


def _build_index(subject_dir: Path, subject: str) -> str:
    sols = _list_solutions(subject_dir)
    solved = len(sols)
    verified = sum(1 for s in sols if s["verified"])
    title = "Mathematics" if subject == "math" else "Physics"
    rows = [
        f"| [{s['num']}]({s['num']}.md) | {'✓ verified' if s['verified'] else 'solved'} | {s['time_str']} |"
        for s in sols
    ]
    table = "| # | Status | Time |\n|---|--------|------|\n" + (
        "\n".join(rows) if rows else "| — | — | — |"
    )
    return (
        f'---\n'
        f'title: "Kvant {title}"\n'
        f'description: "Kvant {title.lower()} problem solutions ({solved} solved, {verified} verified)."\n'
        f'tags: {json.dumps(TAGS[subject])}\n'
        f'categories: {json.dumps(CATEGORIES[subject])}\n'
        f'weight: 20\n'
        f'draft: false\n'
        f'---\n\n'
        f'# Kvant {title}\n\n'
        f'Solutions to {title.lower()} problems from [Kvant](https://kvant.digital) magazine '
        f'({solved} solved, {verified} verified).\n\n'
        f'{table}\n'
    )


def main() -> None:
    changed = []
    for subject, subject_dir in SUBJECTS.items():
        if not subject_dir.exists():
            continue
        index_path = subject_dir / "_index.md"
        new_content = _build_index(subject_dir, subject)
        if not index_path.exists() or index_path.read_text(encoding="utf-8") != new_content:
            index_path.write_text(new_content, encoding="utf-8")
            sols = _list_solutions(subject_dir)
            changed.append(f"kvant {subject}: {len(sols)} problems")
    for c in changed:
        print(f"rebuilt index: {c}")


if __name__ == "__main__":
    main()
