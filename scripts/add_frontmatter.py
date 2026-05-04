#!/usr/bin/env python3
"""Add minimal frontmatter to .md files that don't have it.

Handles two patterns:
  1. Maths book _index.md: "## Book Outline: NN — Title"
     → title: "NN. Title", weight: NN, description from first sentence
     → strips the ## Book Outline header line
  2. General h1 files: "# Title"
     → title from h1, strips the h1 line
"""
import os
import re
import sys


def needs_frontmatter(path):
    with open(path, 'r', encoding='utf-8') as f:
        first = f.read(3)
    return first != '---'


def first_sentence(text):
    """Extract first sentence from a paragraph (up to ~120 chars)."""
    text = text.strip()
    m = re.match(r'([^.!?]+[.!?])', text)
    if m:
        s = m.group(1).strip()
        return s if len(s) <= 150 else s[:150].rsplit(' ', 1)[0] + '...'
    return text[:120].rsplit(' ', 1)[0] if len(text) > 120 else text


def process_book_outline(path, content):
    """Handle ## Book Outline: NN — Title pattern."""
    m = re.search(r'^##\s+Book Outline:\s*(\d+)\s*[—–-]+\s*(.+)$', content, re.MULTILINE)
    if not m:
        return False
    number = int(m.group(1))
    name = m.group(2).strip()
    title = f"{number:02d}. {name}"

    # Extract description from first "This volume..." paragraph
    body_after = content[m.end():].lstrip('\n')
    desc = ''
    for line in body_after.splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            desc = first_sentence(line)
            break

    # Remove the ## Book Outline line and the blank line that follows
    new_body = re.sub(r'^##\s+Book Outline:.*\n(\n)?', '', content, count=1, flags=re.MULTILINE)
    new_body = new_body.strip()

    title_esc = title.replace('"', '\\"')
    desc_esc = desc.replace('"', '\\"')

    fm = f'---\ntitle: "{title_esc}"\n'
    if desc_esc:
        fm += f'description: "{desc_esc}"\n'
    fm += f'weight: {number}\n---\n'

    with open(path, 'w', encoding='utf-8') as f:
        f.write(fm + '\n' + new_body + '\n')

    print(f'  BOOK: {path}  →  "{title}"')
    return True


def process_h1(path, content):
    """Handle # Title pattern."""
    lines = content.splitlines(keepends=True)
    title = None
    title_line = -1
    for i, line in enumerate(lines):
        m = re.match(r'^#\s+(.+)', line)
        if m:
            title = m.group(1).strip()
            title_line = i
            break

    if title is None:
        print(f'  SKIP (no heading): {path}')
        return True

    rest = lines[title_line + 1:]
    if rest and rest[0].strip() == '':
        rest = rest[1:]
    body = ''.join(rest).strip()

    title_esc = title.replace('"', '\\"')
    fm = f'---\ntitle: "{title_esc}"\n---\n'
    new_content = fm + ('\n' + body + '\n' if body else '\n')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f'  H1:   {path}  →  "{title}"')
    return True


def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if re.search(r'^##\s+Book Outline:', content, re.MULTILINE):
        process_book_outline(path, content)
    else:
        process_h1(path, content)


def main(root):
    changed = 0
    for dirpath, _, filenames in os.walk(root):
        for fname in sorted(filenames):
            if not fname.endswith('.md'):
                continue
            path = os.path.join(dirpath, fname)
            if needs_frontmatter(path):
                process_file(path)
                changed += 1
    print(f'\nDone. Processed {changed} files.')


if __name__ == '__main__':
    root = sys.argv[1] if len(sys.argv) > 1 else 'content'
    main(root)
