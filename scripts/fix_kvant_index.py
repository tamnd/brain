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
        um = re.search(r'kvant_(\d{4})_(\d+)', text)
        out.append({
            "num": num,
            "verified": bool(vm and vm.group(1) == "true"),
            "time_str": _fmt_time(int(tm.group(1))) if tm else "—",
            "year": int(um.group(1)) if um else 0,
            "issue": int(um.group(2)) if um else 0,
        })
    out.sort(key=lambda d: d["num"])
    return out


def _build_index(subject_dir: Path, subject: str) -> str:
    sols = _list_solutions(subject_dir)
    solved = len(sols)
    verified = sum(1 for s in sols if s["verified"])
    title = "Mathematics" if subject == "math" else "Physics"

    years_with_data = [s["year"] for s in sols if s["year"]]
    year_start = min(years_with_data) if years_with_data else 0
    year_end = max(years_with_data) if years_with_data else 0

    fm = (
        f'---\n'
        f'title: "Kvant {title}"\n'
        f'description: "Kvant {title.lower()} problem solutions ({solved} solved, {verified} verified), '
        f'{year_start}–{year_end}."\n'
        f'tags: {json.dumps(TAGS[subject])}\n'
        f'categories: {json.dumps(CATEGORIES[subject])}\n'
        f'kvant_total: {solved}\n'
        f'kvant_verified: {verified}\n'
        f'kvant_year_start: {year_start}\n'
        f'kvant_year_end: {year_end}\n'
        f'weight: 20\n'
        f'draft: false\n'
        f'---\n\n'
    )

    subj_word = "mathematics" if subject == "math" else "physics"
    intro = (
        f'# Kvant {title}\n\n'
        f'[Kvant](https://kvant.digital) (Квант) is a popular science magazine covering mathematics '
        f'and physics, published in the Soviet Union and Russia since 1970. '
        f'This page collects solutions to **{solved} {subj_word} problems** '
        f'from the magazine\'s problem section, covering the years {year_start} to {year_end}.'
        + (f' {verified} solutions have been independently verified.' if verified else '')
        + '\n\n'
    )

    grouped: dict[int, dict[int, list[dict]]] = {}
    no_meta: list[dict] = []
    for s in sols:
        if s["year"] == 0:
            no_meta.append(s)
        else:
            grouped.setdefault(s["year"], {}).setdefault(s["issue"], []).append(s)

    body_parts = []
    for year in sorted(grouped):
        issues = grouped[year]
        year_count = sum(len(v) for v in issues.values())
        issue_nums = sorted(issues)
        issue_range = (
            f"Issue {issue_nums[0]}" if len(issue_nums) == 1
            else f"Issues {issue_nums[0]}–{issue_nums[-1]}"
        )
        year_verified = sum(1 for iss in issues.values() for s in iss if s["verified"])
        verified_note = f", {year_verified} verified" if year_verified else ""
        body_parts.append(
            f'## {year}\n\n'
            f'{year_count} problems across {issue_range}{verified_note}.\n\n'
        )
        for issue_num in issue_nums:
            issue_sols = issues[issue_num]
            issue_url = f"https://www.kvant.digital/view/kvant_{year}_{issue_num}/"
            rows = [
                f"| [{s['num']}]({s['num']}.md) "
                f"| {'✓' if s['verified'] else '·'} "
                f"| {s['time_str']} |"
                for s in issue_sols
            ]
            table = "| # | ✓ | Time |\n|---|---|------|\n" + "\n".join(rows)
            body_parts.append(
                f'### [Issue {issue_num}]({issue_url})\n\n'
                f'{table}\n\n'
            )

    if no_meta:
        rows = [
            f"| [{s['num']}]({s['num']}.md) "
            f"| {'✓' if s['verified'] else '·'} "
            f"| {s['time_str']} |"
            for s in no_meta
        ]
        table = "| # | ✓ | Time |\n|---|---|------|\n" + "\n".join(rows)
        body_parts.append(f'## Unknown Issue\n\n{table}\n\n')

    return fm + intro + "".join(body_parts)


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
