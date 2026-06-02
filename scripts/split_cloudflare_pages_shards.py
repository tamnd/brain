#!/usr/bin/env python3
"""Split a tago build into Cloudflare Pages subdomain deployments."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import tomllib
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from xml.sax.saxutils import escape


TEXT_SUFFIXES = {".html", ".css", ".js", ".json", ".xml", ".webmanifest", ".txt"}
SHARED_ROOT_DIRS = ("css", "js")
SHARED_ROOT_FILES = (
    "404.html",
    "apple-touch-icon.png",
    "favicon-16x16.png",
    "favicon-32x32.png",
    "favicon.ico",
    "favicon.svg",
    "site.webmanifest",
)
LOCAL_SHARED_PREFIXES = (
    "/css/",
    "/js/",
    "/_worker",
    "/apple-touch-icon.png",
    "/favicon",
    "/site.webmanifest",
    "/en.search-data.json",
    "/sitemap.xml",
)


@dataclass(frozen=True)
class Site:
    name: str
    project: str
    domain: str
    output: Path
    file_budget: int
    source_prefix: str | None = None

    @property
    def base_url(self) -> str:
        return f"https://{self.domain}"


def slash(path: str) -> str:
    if not path.startswith("/"):
        path = "/" + path
    if not path.endswith("/"):
        path += "/"
    return path


def load_config(path: Path) -> tuple[Site, list[Site]]:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    main_data = data["main"]
    main = Site(
        name="main",
        project=main_data["project"],
        domain=main_data["domain"],
        output=Path(main_data["output"]),
        file_budget=int(main_data["file_budget"]),
    )
    shards: list[Site] = []
    for item in data.get("shards", []):
        shards.append(
            Site(
                name=item["name"],
                project=item["project"],
                domain=item["domain"],
                output=Path(item["output"]),
                file_budget=int(item["file_budget"]),
                source_prefix=slash(item["source_prefix"]),
            )
        )
    return main, shards


def remove(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def copy_shared(public: Path, out: Path) -> None:
    for dirname in SHARED_ROOT_DIRS:
        src = public / dirname
        if src.exists():
            shutil.copytree(src, out / dirname, dirs_exist_ok=True)
    for filename in SHARED_ROOT_FILES:
        src = public / filename
        if src.exists():
            dst = out / filename
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    for worker in public.glob("_worker*.js"):
        shutil.copy2(worker, out / worker.name)


def main_copy_ignore(public: Path, shards: list[Site]):
    public = public.resolve()
    excluded = {Path(s.source_prefix.strip("/")) for s in shards if s.source_prefix}

    def ignore(src: str, names: list[str]) -> set[str]:
        src_path = Path(src).resolve()
        ignored: set[str] = set()
        for name in names:
            child = src_path / name
            try:
                rel = child.relative_to(public)
            except ValueError:
                continue
            if rel in excluded:
                ignored.add(name)
        return ignored

    return ignore


def path_to_url(path: Path, root: Path) -> str | None:
    rel = path.relative_to(root)
    if rel.name != "index.html" or rel.parts[0].startswith("."):
        return None
    if len(rel.parts) == 1:
        return "/"
    return "/" + "/".join(rel.parts[:-1]) + "/"


def shard_path_for(url_path: str, shard: Site) -> str | None:
    assert shard.source_prefix is not None
    url_path = slash(url_path)
    if url_path == shard.source_prefix:
        return "/"
    if not url_path.startswith(shard.source_prefix):
        return None
    return "/" + url_path[len(shard.source_prefix) :]


def map_url(url: str, current: Site, main: Site, shards: list[Site]) -> str:
    if not url.startswith("/") or url.startswith("//"):
        return url

    if current.name != "main" and url.startswith(LOCAL_SHARED_PREFIXES):
        return url

    match = re.match(r"(?P<path>[^?#]*)(?P<suffix>[?#].*)?$", url)
    if not match:
        return url
    raw_path = match.group("path") or "/"
    suffix = match.group("suffix") or ""
    compare_path = slash(raw_path)

    for shard in shards:
        mapped = shard_path_for(compare_path, shard)
        if mapped is None:
            continue
        if current.name == shard.name:
            return mapped + suffix
        return f"{shard.base_url}{mapped}{suffix}"

    if current.name == "main":
        return url
    return f"{main.base_url}{url}"


def replace_canonical(text: str, current: Site, main: Site, shards: list[Site]) -> str:
    def repl(match: re.Match[str]) -> str:
        old = match.group("url")
        for prefix in (main.base_url, "https://brain.tamnd.com"):
            if old.startswith(prefix):
                mapped = map_url(old[len(prefix) :] or "/", current, main, shards)
                if mapped.startswith("/"):
                    mapped = current.base_url + mapped
                return match.group("prefix") + mapped + match.group("quote")
        return match.group(0)

    return re.sub(
        r'(?P<prefix><link rel="canonical" href=")(?P<url>[^"]+)(?P<quote>")',
        repl,
        text,
    )


def rewrite_text(text: str, current: Site, main: Site, shards: list[Site]) -> str:
    text = replace_canonical(text, current, main, shards)

    text = re.sub(
        r'(?P<prefix>(?:href|src|action|content|poster)=["\'])'
        r'(?P<url>/(?!/)[^"\'<>{}\s]*)',
        lambda m: m.group("prefix") + map_url(m.group("url"), current, main, shards),
        text,
    )
    text = re.sub(
        r"url\((?P<quote>['\"]?)(?P<url>/(?!/)[^)'\"\s]+)(?P=quote)\)",
        lambda m: f"url({m.group('quote')}{map_url(m.group('url'), current, main, shards)}{m.group('quote')})",
        text,
    )
    return text


def rewrite_tree(root: Path, current: Site, main: Site, shards: list[Site]) -> int:
    changed = 0
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        original = path.read_text(encoding="utf-8")
        rewritten = rewrite_text(original, current, main, shards)
        if rewritten != original:
            path.write_text(rewritten, encoding="utf-8")
            changed += 1
    return changed


def split_search_data(public: Path, main: Site, shards: list[Site]) -> None:
    src = public / "en.search-data.json"
    if not src.exists():
        return
    data = json.loads(src.read_text(encoding="utf-8"))
    main_data: dict[str, object] = {}
    shard_data: dict[str, dict[str, object]] = {s.name: {} for s in shards}

    for key, value in data.items():
        assigned = False
        for shard in shards:
            mapped = shard_path_for(key, shard)
            if mapped is not None:
                shard_data[shard.name][mapped] = value
                assigned = True
                break
        if not assigned:
            main_data[key] = value

    (main.output / "en.search-data.json").write_text(
        json.dumps(main_data, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    for shard in shards:
        dest = shard.output / "en.search-data.json"
        dest.write_text(
            json.dumps(shard_data[shard.name], ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )


def write_urlset(path: Path, urls: list[str]) -> None:
    today = datetime.now(UTC).date().isoformat()
    body = ['<?xml version="1.0" encoding="UTF-8"?>']
    body.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for url in sorted(set(urls)):
        body.append("  <url>")
        body.append(f"    <loc>{escape(url)}</loc>")
        body.append(f"    <lastmod>{today}</lastmod>")
        body.append("  </url>")
    body.append("</urlset>")
    path.write_text("\n".join(body) + "\n", encoding="utf-8")


def write_sitemap_index(path: Path, urls: list[str]) -> None:
    body = ['<?xml version="1.0" encoding="UTF-8"?>']
    body.append('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for url in urls:
        body.append("  <sitemap>")
        body.append(f"    <loc>{escape(url)}</loc>")
        body.append("  </sitemap>")
    body.append("</sitemapindex>")
    path.write_text("\n".join(body) + "\n", encoding="utf-8")


def generate_sitemaps(main: Site, shards: list[Site]) -> None:
    main_urls: list[str] = []
    for path in main.output.rglob("index.html"):
        if path.name == "404.html":
            continue
        url_path = path_to_url(path, main.output)
        if url_path is not None:
            main_urls.append(main.base_url + url_path)
    write_urlset(main.output / "sitemap-main.xml", main_urls)
    write_sitemap_index(
        main.output / "sitemap.xml",
        [f"{main.base_url}/sitemap-main.xml"]
        + [f"{shard.base_url}/sitemap.xml" for shard in shards],
    )

    for shard in shards:
        urls: list[str] = []
        for path in shard.output.rglob("index.html"):
            url_path = path_to_url(path, shard.output)
            if url_path is not None:
                urls.append(shard.base_url + url_path)
        write_urlset(shard.output / "sitemap.xml", urls)


def write_redirects(main: Site, shards: list[Site]) -> None:
    lines: list[str] = []
    for shard in shards:
        assert shard.source_prefix is not None
        lines.append(f"{shard.source_prefix} {shard.base_url}/ 302")
        lines.append(f"{shard.source_prefix}* {shard.base_url}/:splat 301")
    (main.output / "_redirects").write_text("\n".join(lines) + "\n", encoding="utf-8")

    for shard in shards:
        assert shard.source_prefix is not None
        aliases = [
            f"{shard.source_prefix}* /:splat 301",
            f"/{shard.name}/* /:splat 301",
        ]
        (shard.output / "_redirects").write_text("\n".join(aliases) + "\n", encoding="utf-8")


def validate(site: Site) -> dict[str, int | str]:
    files = [p for p in site.output.rglob("*") if p.is_file()]
    oversized = [str(p) for p in files if p.stat().st_size > 24 * 1024 * 1024]
    tago_db = [str(p) for p in files if p.name == ".tago-cache.db"]
    if oversized:
        raise SystemExit(f"{site.name}: oversized files remain: {oversized[:5]}")
    if tago_db:
        raise SystemExit(f"{site.name}: tago DB leaked into output: {tago_db[:5]}")
    if len(files) > site.file_budget:
        raise SystemExit(f"{site.name}: {len(files)} files exceeds budget {site.file_budget}")
    return {
        "site": site.name,
        "domain": site.domain,
        "project": site.project,
        "files": len(files),
        "bytes": sum(p.stat().st_size for p in files),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("deploy-shards.toml"))
    parser.add_argument("--public", type=Path, default=Path("public"))
    args = parser.parse_args()

    main_site, shards = load_config(args.config)
    public = args.public
    if not public.is_dir():
        raise SystemExit(f"missing build output: {public}")

    for out in [main_site.output, *(s.output for s in shards)]:
        remove(out)

    shutil.copytree(public, main_site.output, ignore=main_copy_ignore(public, shards))
    for shard in shards:
        assert shard.source_prefix is not None
        source = public / shard.source_prefix.strip("/")
        if not source.is_dir():
            raise SystemExit(f"missing shard source: {source}")
        shutil.copytree(source, shard.output)
        copy_shared(public, shard.output)

    for root in [main_site.output, *(s.output for s in shards)]:
        for path in root.rglob("*"):
            if path.is_file() and (path.name == ".tago-cache.db" or path.stat().st_size > 24 * 1024 * 1024):
                path.unlink()

    rewrite_tree(main_site.output, main_site, main_site, shards)
    for shard in shards:
        rewrite_tree(shard.output, shard, main_site, shards)
    split_search_data(public, main_site, shards)
    write_redirects(main_site, shards)
    generate_sitemaps(main_site, shards)

    summary = [validate(main_site)] + [validate(s) for s in shards]
    summary_path = Path("deploy-shards-summary.json")
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    for item in summary:
        print(f"{item['site']}: {item['files']} files, {item['bytes']} bytes -> {item['domain']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
