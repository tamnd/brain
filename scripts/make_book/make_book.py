#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Build a PDF (and optional EPUB) book from a Hugo content folder.

The folder is expected to look like:

    book/
      _index.md             # book root with `title`, `description` in frontmatter
      01/
        _index.md           # part metadata: `title`, `weight`
        1.md                # chapter 1: H1 + body, math via \\(...\\) and $$...$$
        2.md
        ...
      02/
        ...
      app/                  # appendices: chapter files use a.md, b.md, ...
        _index.md
        a.md
        ...

Output: a Typst document is rendered with the cmarker and mitex packages and
compiled to PDF via the `typst` binary. EPUB is produced via pandoc.

Usage:
    uv run scripts/make_book/make_book.py BOOK_DIR --pdf OUT.pdf [--epub OUT.epub]
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import yaml


FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
INLINE_MATH_RE = re.compile(r"\\\((.+?)\\\)", re.DOTALL)
DISPLAY_MATH_RE = re.compile(r"\\\[(.+?)\\\]", re.DOTALL)


@dataclass
class Doc:
    path: Path
    meta: dict
    body: str

    @property
    def title(self) -> str:
        return str(self.meta.get("title") or self.path.stem)

    @property
    def description(self) -> str:
        return str(self.meta.get("description") or "")

    @property
    def weight(self) -> int:
        w = self.meta.get("weight")
        return int(w) if isinstance(w, (int, float)) else 10_000


@dataclass
class Part:
    dir: Path
    index: Doc
    chapters: list[Doc] = field(default_factory=list)

    @property
    def title(self) -> str:
        return self.index.title

    @property
    def weight(self) -> int:
        return self.index.weight


def split_frontmatter(text: str) -> tuple[dict, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        meta = {}
    if not isinstance(meta, dict):
        meta = {}
    return meta, text[m.end():]


def convert_math(text: str) -> str:
    text = DISPLAY_MATH_RE.sub(lambda m: f"\n$$\n{m.group(1).strip()}\n$$\n", text)
    text = INLINE_MATH_RE.sub(lambda m: f"${m.group(1)}$", text)
    return text


def load_doc(path: Path) -> Doc:
    raw = path.read_text(encoding="utf-8")
    meta, body = split_frontmatter(raw)
    return Doc(path=path, meta=meta, body=convert_math(body))


def chapter_sort_key(p: Path) -> tuple[int, object]:
    stem = p.stem
    if stem.isdigit():
        return (0, int(stem))
    return (1, stem.lower())


def discover_book(book_dir: Path) -> tuple[Doc, list[Part]]:
    root_idx = book_dir / "_index.md"
    if not root_idx.exists():
        sys.exit(f"error: {root_idx} not found")
    root = load_doc(root_idx)

    parts: list[Part] = []
    for sub in sorted(p for p in book_dir.iterdir() if p.is_dir()):
        idx = sub / "_index.md"
        if not idx.exists():
            continue
        part_doc = load_doc(idx)
        chap_paths = sorted(
            (
                p
                for p in sub.iterdir()
                if p.is_file() and p.suffix == ".md" and p.name != "_index.md"
            ),
            key=chapter_sort_key,
        )
        if not chap_paths:
            continue
        parts.append(
            Part(dir=sub, index=part_doc, chapters=[load_doc(c) for c in chap_paths])
        )
    parts.sort(key=lambda p: (p.weight, p.dir.name))
    return root, parts


def typst_str(s: str) -> str:
    """Encode a Python string as a Typst string literal."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


TEMPLATE = r"""#import "@preview/cmarker:0.1.8"
#import "@preview/mitex:0.2.7": mi, mitex

#let math-renderer(body, block: false) = if block { mitex(body) } else { mi(body) }

#let chapter-render(path) = cmarker.render(
  read(path),
  math: math-renderer,
  h1-level: 2,
  smart-punctuation: true,
)

#set document(title: __TITLE__, author: __AUTHOR__)

#set page(
  paper: "a4",
  margin: (inside: 2.4cm, outside: 2.0cm, top: 2.4cm, bottom: 2.4cm),
)
#set text(
  font: ("New Computer Modern", "Libertinus Serif"),
  size: 10.5pt,
  lang: "en",
)
#show raw: set text(font: ("DejaVu Sans Mono", "Menlo"), size: 9.5pt)
#set par(justify: true, leading: 0.62em, first-line-indent: (amount: 1.2em, all: false))
#show link: set text(rgb("#1f4ea1"))
#set table(stroke: 0.4pt + luma(160))
#show table.cell.where(y: 0): strong

#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  v(2em)
  block(text(weight: "bold", size: 26pt, it.body))
  v(0.3em)
  line(length: 100%, stroke: 0.6pt + luma(120))
  v(1.6em)
}
#show heading.where(level: 2): it => {
  pagebreak(weak: true)
  v(1.2em)
  block(text(weight: "bold", size: 18pt, it.body))
  v(0.4em)
}
#show heading.where(level: 3): it => {
  v(0.8em)
  block(text(weight: "bold", size: 13pt, it.body))
  v(0.1em)
}
#show heading.where(level: 4): it => {
  v(0.4em)
  block(text(weight: "bold", size: 11pt, style: "italic", it.body))
}

// ---------- Cover ----------
#set page(numbering: none, header: none, footer: none)
#align(center + horizon)[
  #text(weight: "bold", size: 36pt)[#__TITLE__]
  #v(0.8cm)
  #if __SUBTITLE_NONEMPTY__ [
    #text(size: 14pt, style: "italic")[#__SUBTITLE__]
    #v(1.2cm)
  ]
  #text(size: 12pt)[#__AUTHOR__]
  #v(0.3cm)
  #text(size: 11pt, fill: luma(80))[#__DATE__]
]
#pagebreak()

// ---------- Front matter (TOC) ----------
#set page(
  numbering: "i",
  header: none,
  footer: context align(center, text(9pt, fill: luma(120))[#counter(page).display("i")]),
)
#counter(page).update(1)
#show outline.entry.where(level: 1): it => {
  v(0.6em, weak: true)
  strong(it)
}
#outline(title: [Contents], depth: 2, indent: auto)
#pagebreak()

// ---------- Body ----------
#set page(
  numbering: "1",
  header: context {
    let n = counter(page).get().first()
    if calc.even(n) {
      align(left, text(9pt, fill: luma(120))[#__TITLE__])
    } else {
      align(right, text(9pt, fill: luma(120), style: "italic")[#__SHORT_TITLE__])
    }
  },
  footer: context align(center, text(9pt, fill: luma(120))[#counter(page).display("1")]),
)
#counter(page).update(1)

__BODY__
"""


def render_typst(root: Doc, parts: list[Part], *, author: str, date: str) -> str:
    title = root.title
    subtitle = root.description
    short_title = title

    body_parts: list[str] = []
    for part in parts:
        part_title = part.title
        # Hugo part titles are usually like "I. Foundations". Prepend "Part " for
        # full parts but leave appendix-style titles ("Appendices") alone.
        if re.match(r"^[IVXLCDM]+\.\s", part_title):
            display = f"Part {part_title}"
        else:
            display = part_title
        body_parts.append(f"#heading(level: 1)[{escape_typst_content(display)}]")
        for ch in part.chapters:
            rel = ch.path.relative_to(part.dir.parent).as_posix()
            body_parts.append(f"#chapter-render({typst_str(rel)})")
    body = "\n\n".join(body_parts)

    return (
        TEMPLATE
        .replace("__TITLE__", typst_str(title))
        .replace("__AUTHOR__", typst_str(author))
        .replace("__SUBTITLE__", typst_str(subtitle))
        .replace("__SUBTITLE_NONEMPTY__", "true" if subtitle.strip() else "false")
        .replace("__DATE__", typst_str(date))
        .replace("__SHORT_TITLE__", typst_str(short_title))
        .replace("__BODY__", body)
    )


def escape_typst_content(s: str) -> str:
    """Escape a string for use inside a Typst content block [...]."""
    return (
        s.replace("\\", "\\\\")
        .replace("[", "\\[")
        .replace("]", "\\]")
        .replace("#", "\\#")
        .replace("*", "\\*")
        .replace("_", "\\_")
        .replace("$", "\\$")
        .replace("`", "\\`")
        .replace("@", "\\@")
        .replace("<", "\\<")
        .replace(">", "\\>")
    )


def stage_workspace(book_dir: Path, parts: list[Part], workdir: Path) -> None:
    """Mirror book content into workdir with frontmatter stripped and math
    delimiters normalised so cmarker can pick up on them."""
    for part in parts:
        out_part = workdir / part.dir.relative_to(book_dir)
        out_part.mkdir(parents=True, exist_ok=True)
        for ch in part.chapters:
            (workdir / ch.path.relative_to(book_dir)).write_text(
                ch.body, encoding="utf-8"
            )


def build_pdf(typst_main: Path, out_pdf: Path) -> None:
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["typst", "compile", str(typst_main), str(out_pdf)],
        check=True,
    )


def build_epub(root: Doc, parts: list[Part], out_epub: Path, *, author: str) -> None:
    """Concatenate part/chapter markdown into a single document and run pandoc."""
    if shutil.which("pandoc") is None:
        sys.exit("error: pandoc not found; install with `brew install pandoc`")

    pieces: list[str] = []
    pieces.append(f"% {root.title}")
    pieces.append(f"% {author}")
    pieces.append("")
    for part in parts:
        title = part.title
        if re.match(r"^[IVXLCDM]+\.\s", title):
            title = f"Part {title}"
        pieces.append(f"# {title}\n")
        for ch in part.chapters:
            # Demote chapter H1 -> H2 to fit under part H1.
            body = re.sub(r"(?m)^# ", "## ", ch.body, count=1)
            # Remaining H2 -> H3, H3 -> H4, ... by adding one #.
            body = re.sub(r"(?m)^(#{2,5})(?= )", lambda m: "#" + m.group(1), body)
            pieces.append(body.strip())
            pieces.append("")
    combined = "\n".join(pieces)

    with tempfile.TemporaryDirectory() as td:
        md = Path(td) / "book.md"
        md.write_text(combined, encoding="utf-8")
        out_epub.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                "pandoc",
                "-f",
                "markdown+tex_math_dollars+tex_math_single_backslash+raw_tex+pipe_tables",
                "-t",
                "epub3",
                "--mathml",
                "--toc",
                "--toc-depth=2",
                "--metadata",
                f"title={root.title}",
                "--metadata",
                f"author={author}",
                "-o",
                str(out_epub),
                str(md),
            ],
            check=True,
        )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("book_dir", type=Path, help="path to the book content folder")
    ap.add_argument("--pdf", type=Path, help="output PDF path")
    ap.add_argument("--epub", type=Path, help="output EPUB path (uses pandoc)")
    ap.add_argument(
        "--author",
        default="tamnd",
        help="author name to embed (default: tamnd)",
    )
    ap.add_argument(
        "--date",
        default=dt.date.today().isoformat(),
        help="date to embed on the cover (default: today)",
    )
    ap.add_argument(
        "--keep-workspace",
        action="store_true",
        help="keep the temporary typst workspace for inspection",
    )
    args = ap.parse_args()

    if not args.pdf and not args.epub:
        ap.error("at least one of --pdf or --epub is required")

    book_dir = args.book_dir.resolve()
    if not book_dir.is_dir():
        sys.exit(f"error: {book_dir} is not a directory")

    root, parts = discover_book(book_dir)
    if not parts:
        sys.exit(f"error: no parts found under {book_dir}")

    print(f"book: {root.title!r}", file=sys.stderr)
    for part in parts:
        print(
            f"  part {part.dir.name}: {part.title!r} ({len(part.chapters)} chapters)",
            file=sys.stderr,
        )

    if args.pdf:
        if shutil.which("typst") is None:
            sys.exit("error: typst not found; install with `brew install typst`")
        ws = Path(tempfile.mkdtemp(prefix="make_book_"))
        try:
            stage_workspace(book_dir, parts, ws)
            typst_src = render_typst(root, parts, author=args.author, date=args.date)
            main_typ = ws / "main.typ"
            main_typ.write_text(typst_src, encoding="utf-8")
            print(f"compiling typst -> {args.pdf}", file=sys.stderr)
            build_pdf(main_typ, args.pdf.resolve())
        finally:
            if args.keep_workspace:
                print(f"workspace kept at {ws}", file=sys.stderr)
            else:
                shutil.rmtree(ws, ignore_errors=True)

    if args.epub:
        print(f"building epub -> {args.epub}", file=sys.stderr)
        build_epub(root, parts, args.epub.resolve(), author=args.author)

    return 0


if __name__ == "__main__":
    sys.exit(main())
