#!/usr/bin/env python3
"""Rewrite generated root-relative URLs for GitHub project Pages."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TEXT_SUFFIXES = {
    ".html",
    ".css",
    ".js",
    ".json",
    ".xml",
    ".webmanifest",
}


def _prefix_url(value: str, base_path: str) -> str:
    if not value.startswith("/"):
        return value
    if value.startswith("//") or value.startswith(base_path + "/") or value == base_path:
        return value
    return base_path + value


def rewrite_text(text: str, base_path: str) -> str:
    # HTML/XML/JS/JSON string values that are root-relative URLs.
    text = re.sub(
        r'(?P<prefix>(?:href|src|action|content|url|poster)=["\']|["\'])'
        r'(?P<url>/(?!/)[^"\'<>{}\s]*)',
        lambda m: m.group("prefix") + _prefix_url(m.group("url"), base_path),
        text,
    )

    # Inline JS single-quoted root paths, such as var INDEX_URL = '/en.search-data.json'.
    text = re.sub(
        r"(?P<prefix>')(?P<url>/(?!/)[^'\s]*)",
        lambda m: m.group("prefix") + _prefix_url(m.group("url"), base_path),
        text,
    )

    # CSS url(/path) and url('/path') forms.
    text = re.sub(
        r"url\((?P<quote>['\"]?)(?P<url>/(?!/)[^)'\"\s]+)(?P=quote)\)",
        lambda m: f"url({m.group('quote')}{_prefix_url(m.group('url'), base_path)}{m.group('quote')})",
        text,
    )
    return text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--base-path", default="/brain")
    args = parser.parse_args()

    base_path = "/" + args.base_path.strip("/")
    changed = 0
    for path in args.directory.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        original = path.read_text(encoding="utf-8")
        rewritten = rewrite_text(original, base_path)
        if rewritten != original:
            path.write_text(rewritten, encoding="utf-8")
            changed += 1

    print(f"rewrote {changed} files for GitHub Pages base path {base_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
