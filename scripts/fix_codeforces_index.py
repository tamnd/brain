#!/usr/bin/env python3
"""Regenerate the top-level Codeforces _index.md from all present contest _index.md files.

Run by brain_on.sh after every git pull so the index reflects all servers' solved contests.
"""
import re
from collections import defaultdict
from pathlib import Path

CF_DIR = Path(__file__).resolve().parent.parent / "content" / "en" / "practice" / "codeforces"


def _cf_contest_label(name: str) -> str:
    n = name.lower()
    if "div. 4" in n: return "Div. 4"
    if "div. 3" in n: return "Div. 3"
    if "div. 1" in n and "div. 2" in n: return "Div. 1+2"
    if "div. 1" in n: return "Div. 1"
    if "div. 2" in n: return "Div. 2"
    if "educational" in n: return "Educational"
    if "global" in n: return "Global"
    if "april fools" in n: return "April Fools"
    if "kotlin" in n: return "Kotlin"
    if "beta" in n: return "Beta"
    if "icpc" in n or "ioi" in n: return "ICPC/IOI"
    return "Special"


def _build_top_index(cf_dir: Path) -> str:
    contest_dirs = sorted(
        (d for d in cf_dir.iterdir() if d.is_dir() and d.name.isdigit()),
        key=lambda d: int(d.name),
    )

    contests = []
    for contest_dir in contest_dirs:
        index_file = contest_dir / "_index.md"
        if not index_file.exists():
            continue
        text = index_file.read_text(encoding="utf-8")
        contest_id = int(contest_dir.name)

        title_m = re.search(r'^title:\s*"(.*?)"', text, re.MULTILINE)
        contest_name = title_m.group(1) if title_m else f"Round {contest_id}"
        ctype_m = re.search(r'^contest_type:\s*"(.*?)"', text, re.MULTILINE)
        contest_type = ctype_m.group(1) if ctype_m else _cf_contest_label(contest_name)
        rrange_m = re.search(r'^rating_range:\s*"(.*?)"', text, re.MULTILINE)
        rating_range = rrange_m.group(1) if rrange_m else ""
        np_m = re.search(r'^n_problems:\s*(\d+)', text, re.MULTILINE)
        nv_m = re.search(r'^n_verified:\s*(\d+)', text, re.MULTILINE)
        cy_m = re.search(r'^contest_year:\s*(\d+)', text, re.MULTILINE)
        n_problems = int(np_m.group(1)) if np_m else len(list(contest_dir.glob("[A-Z]*.md")))
        n_verified = int(nv_m.group(1)) if nv_m else 0
        year = int(cy_m.group(1)) if cy_m else 0

        contests.append({
            "id": contest_id, "name": contest_name, "type": contest_type,
            "rating": rating_range, "n": n_problems, "v": n_verified, "year": year,
        })

    total_problems = sum(c["n"] for c in contests)
    total_verified = sum(c["v"] for c in contests)
    n_contests = len(contests)

    by_year: dict[int, list[dict]] = defaultdict(list)
    for c in contests:
        by_year[c["year"]].append(c)

    body_parts = []
    for year in sorted(by_year.keys()):
        grp = by_year[year]
        yr_problems = sum(c["n"] for c in grp)
        yr_verified = sum(c["v"] for c in grp)
        yr_label = str(year) if year else "Unknown"
        body_parts.append(
            f"## {yr_label} — {len(grp)} contests, {yr_problems} problems, {yr_verified} verified\n\n"
        )
        rows = []
        for c in grp:
            rows.append(
                f"| [{c['id']}]({c['id']}/) "
                f"| [{c['name']}](https://codeforces.com/contest/{c['id']}) "
                f"| {c['n']} | {c['v']}/{c['n']} "
                f"| {c['type']} | {c['rating']} |"
            )
        body_parts.append(
            "| # | Contest | Problems | Verified | Type | Difficulty |\n"
            "|---|---|---|---|---|---|\n"
            + "\n".join(rows) + "\n\n"
        )

    summary = f"{n_contests} contests, {total_problems} problems, {total_verified} verified."

    return (
        '---\n'
        'title: "Codeforces Solutions"\n'
        f'description: "Codeforces problem solutions with full editorials. {summary}"\n'
        'tags: ["codeforces", "competitive-programming"]\n'
        'categories: ["algorithms"]\n'
        'weight: 4\n'
        'draft: false\n'
        '---\n\n'
        '# Codeforces Solutions\n\n'
        'Each problem has a full editorial: problem analysis, approach, algorithm walkthrough, '
        'a Python solution with explanation, worked examples, and edge cases. '
        'The original problem statement is not reproduced here.\n\n'
        f'**{summary}**\n\n'
        + "".join(body_parts)
    )


def main() -> None:
    if not CF_DIR.exists():
        return
    index_path = CF_DIR / "_index.md"
    new_content = _build_top_index(CF_DIR)
    if not index_path.exists() or index_path.read_text(encoding="utf-8") != new_content:
        index_path.write_text(new_content, encoding="utf-8")
        n = sum(1 for d in CF_DIR.iterdir() if d.is_dir() and d.name.isdigit() and (d / "_index.md").exists())
        print(f"rebuilt index: codeforces {n} contests")


if __name__ == "__main__":
    main()
