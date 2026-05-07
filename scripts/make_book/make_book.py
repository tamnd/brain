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
LEADING_H1_RE = re.compile(r"\A\s*#[^\n#].*\n+")
CHAPTER_TITLE_RE = re.compile(r"^(?:Chapter|Appendix)\s+([\w\d]+)\.\s+(.+)$")
PART_TITLE_RE = re.compile(r"^([\w\d]+)\.\s+(.+)$")


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


TEMPLATE = r"""// Springer SVMono-inspired book template, LaTeX-flavoured.
//   Trim: 15.5 x 23.4 cm  (Springer royal octavo).
//   Body + math: New Computer Modern (Knuth's Computer Modern, modern build).
//   All headings: serif bold (no sans-serif), matching SVMono.

#import "@preview/cmarker:0.1.8"
#import "@preview/mitex:0.2.7": mi, mitex

#let serif = (
  "New Computer Modern",
  "Latin Modern Roman",
  "Libertinus Serif",
  "STIX Two Text",
  "Times New Roman", "Times",
)
#let math-font = (
  "New Computer Modern Math",
  "Latin Modern Math",
  "STIX Two Math",
)
#let mono = (
  "New Computer Modern Mono",
  "DejaVu Sans Mono", "Menlo", "Liberation Mono", "Courier",
)

#set document(title: __TITLE_STR__, author: __AUTHOR_STR__)

#set page(
  width: 15.5cm, height: 23.4cm,
  margin: (inside: 23mm, outside: 17mm, top: 24mm, bottom: 25mm),
  binding: left,
)
#set text(font: serif, size: 10.5pt, lang: "en")
#show math.equation: set text(font: math-font)

#set par(
  justify: true,
  leading: 0.6em,
  first-line-indent: (amount: 1.2em, all: false),
  spacing: 0.7em,
)
#set list(indent: 1em, body-indent: 0.6em)
#set enum(indent: 1em, body-indent: 0.6em)
#set table(stroke: 0.4pt + luma(170), inset: 5pt)
#show table.cell.where(y: 0): set text(weight: "bold")
#show raw: set text(font: mono, size: 0.92em)
#show link: set text(rgb("#1f4ea1"))

// Springer SVMono heading levels:
//   1 = part divider     (visual via book-part)
//   2 = chapter heading  (visual via chapter-opener)
//   3 = section
//   4 = subsection
//   5 = paragraph (run-in italic)
// Levels 1/2 carry only outline + bookmark; visual rendering is external.
// Plain `set` show rules avoid wrapping headings in extra blocks, which keeps
// Typst's "first paragraph after a heading is not indented" detection working.
#show heading.where(level: 1): _ => []
#show heading.where(level: 2): _ => []
#show heading.where(level: 3): set text(weight: "bold", size: 12pt)
#show heading.where(level: 3): set block(above: 1.6em, below: 0.7em)
#show heading.where(level: 4): set text(weight: "bold", size: 11pt)
#show heading.where(level: 4): set block(above: 1.2em, below: 0.5em)
#show heading.where(level: 5): set text(weight: "bold", style: "italic", size: 10.5pt)
#show heading.where(level: 5): set block(above: 0.9em, below: 0.2em)

#let math-renderer(body, block: false) = if block { mitex(body) } else { mi(body) }
#let chapter-render(path) = cmarker.render(
  read(path),
  math: math-renderer,
  h1-level: 2,
  smart-punctuation: true,
)

#let chapter-opener(num, name) = {
  pagebreak(weak: true, to: "odd")
  heading(level: 2, outlined: true, bookmarked: true, numbering: none)[#num. #name]
  block(width: 100%, above: 0pt, below: 0pt)[
    #set par(first-line-indent: 0pt, leading: 0.5em, justify: false)
    #text(weight: "bold", size: 17pt)[Chapter #num] \
    #text(weight: "bold", size: 22pt)[#name]
  ]
  v(3cm)
}

#let book-part(label, name, preamble: none) = {
  pagebreak(weak: true, to: "odd")
  heading(level: 1, outlined: true, bookmarked: true, numbering: none)[Part #label. #name]
  set page(header: none, footer: none)
  v(1fr)
  align(center)[
    #set par(first-line-indent: 0pt, leading: 0.6em)
    #text(size: 14pt, tracking: 0.20em, fill: luma(70))[PART #upper(label)]
    #v(0.7cm)
    #text(weight: "bold", size: 28pt)[#name]
    #if preamble != none {
      v(1.2cm)
      block(width: 75%)[
        #set par(justify: true, first-line-indent: 0pt, leading: 0.6em)
        #set text(size: 11pt, style: "italic")
        #preamble
      ]
    }
  ]
  v(1fr)
  pagebreak(weak: true, to: "odd")
}

// ============================================================
// Title page
// ============================================================
#set page(numbering: none, header: none, footer: none)
#align(center)[
  #v(3cm)
  #text(weight: "bold", size: 30pt)[__TITLE__]
  #v(0.6cm)
  __SUBTITLE_BLOCK__
  #v(4cm)
  #text(size: 14pt)[__AUTHOR__]
  #v(0.4cm)
  #text(size: 11pt, fill: luma(80))[__DATE__]
  #v(1fr)
  #text(size: 9pt, style: "italic", fill: luma(120))[Typeset with Typst]
]
#pagebreak(to: "odd")

// ============================================================
// Table of contents
// ============================================================
#set page(numbering: "i")
#counter(page).update(1)
#block[
  #set par(first-line-indent: 0pt)
  #text(weight: "bold", size: 22pt)[Contents]
]
#v(0.6em)
#set outline(depth: 2)
#show outline.entry.where(level: 1): it => {
  v(0.8em, weak: true)
  set text(weight: "bold", size: 11pt)
  it
}
#show outline.entry.where(level: 2): it => {
  set text(size: 10pt)
  pad(left: 0.8em, it)
}
#outline(title: none, indent: auto)

#pagebreak(to: "odd")

// ============================================================
// Main matter
// ============================================================
#set page(
  numbering: "1",
  header: context {
    let pn = counter(page).get().first()
    let here-page = here().page()
    let parts-here = query(heading.where(level: 1)).filter(h => h.location().page() == here-page)
    let chaps-here = query(heading.where(level: 2)).filter(h => h.location().page() == here-page)
    if parts-here.len() > 0 or chaps-here.len() > 0 { return [] }

    let chapters-before = query(heading.where(level: 2).before(here()))
    let sections-before = query(heading.where(level: 3).before(here()))
    let chap = if chapters-before.len() > 0 { chapters-before.last() } else { none }
    let sec = if sections-before.len() > 0 { sections-before.last() } else { none }
    if sec != none and chap != none and sec.location().page() < chap.location().page() {
      sec = none
    }

    set text(size: 9pt, style: "italic", fill: luma(70))
    if calc.even(pn) {
      grid(columns: (auto, 1fr, auto),
        [#pn], [], align(right, if chap != none { chap.body } else []),
      )
    } else {
      grid(columns: (auto, 1fr, auto),
        align(left, if sec != none { sec.body } else if chap != none { chap.body } else []),
        [], [#pn],
      )
    }
  },
  footer: none,
)
#counter(page).update(1)

__BODY__
"""


def split_chapter_title(title: str) -> tuple[str, str]:
    """`Chapter 1. Foo` -> ('1', 'Foo'); fallback returns ('', title)."""
    m = CHAPTER_TITLE_RE.match(title.strip())
    if m:
        return m.group(1), m.group(2).strip()
    return "", title


def split_part_title(title: str) -> tuple[str, str]:
    """`I. Foundations` -> ('I', 'Foundations'); fallback returns ('', title)."""
    m = PART_TITLE_RE.match(title.strip())
    if m:
        return m.group(1), m.group(2).strip()
    return "", title


def render_typst(root: Doc, parts: list[Part], *, author: str, date: str) -> str:
    title = root.title
    subtitle = root.description

    body_parts: list[str] = []
    for part in parts:
        label, name = split_part_title(part.title)
        preamble = part.index.description.strip()
        args = [typst_str(label), typst_str(name)]
        kwargs = ""
        if preamble:
            kwargs = f", preamble: [{escape_typst_content(preamble)}]"
        body_parts.append(f"#book-part({', '.join(args)}{kwargs})")
        for ch in part.chapters:
            num, ch_name = split_chapter_title(ch.title)
            rel = ch.path.relative_to(part.dir.parent).as_posix()
            body_parts.append(
                f"#chapter-opener({typst_str(num)}, {typst_str(ch_name)})"
            )
            body_parts.append(f"#chapter-render({typst_str(rel)})")
    body = "\n\n".join(body_parts)

    if subtitle.strip():
        subtitle_block = (
            f"#text(font: sans, weight: \"regular\", size: 13pt, "
            f"fill: luma(60), style: \"italic\")[{escape_typst_content(subtitle)}]"
        )
    else:
        subtitle_block = ""

    return (
        TEMPLATE
        .replace("__TITLE_STR__", typst_str(title))
        .replace("__AUTHOR_STR__", typst_str(author))
        .replace("__TITLE__", escape_typst_content(title))
        .replace("__AUTHOR__", escape_typst_content(author))
        .replace("__SUBTITLE_BLOCK__", subtitle_block)
        .replace("__DATE__", escape_typst_content(date))
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
    delimiters normalised so cmarker can pick up on them. The leading H1 line
    (e.g. `# Chapter 1. ...`) is stripped because the chapter heading is
    rendered externally via `chapter-opener` for Springer-style typography."""
    for part in parts:
        out_part = workdir / part.dir.relative_to(book_dir)
        out_part.mkdir(parents=True, exist_ok=True)
        for ch in part.chapters:
            stripped = LEADING_H1_RE.sub("", ch.body, count=1)
            (workdir / ch.path.relative_to(book_dir)).write_text(
                stripped, encoding="utf-8"
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
