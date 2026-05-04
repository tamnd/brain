#!/usr/bin/env python3
"""Add minimal frontmatter to .md files that don't have it.
Extracts the title from the first # heading.
"""
import os
import re
import sys

def extract_title(content):
    for line in content.splitlines():
        m = re.match(r'^#\s+(.+)', line)
        if m:
            return m.group(1).strip()
    return None

def strip_leading_heading(content):
    """Remove the first # heading line if present (it becomes the title in frontmatter)."""
    lines = content.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if re.match(r'^#\s+', line):
            # Remove the heading and any immediately following blank line
            rest = lines[i+1:]
            if rest and rest[0].strip() == '':
                rest = rest[1:]
            return ''.join(rest)
    return content

def needs_frontmatter(path):
    with open(path, 'r', encoding='utf-8') as f:
        first = f.read(3)
    return first != '---'

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    title = extract_title(content)
    if not title:
        print(f'  SKIP (no h1): {path}')
        return

    body = strip_leading_heading(content).rstrip('\n')

    # Escape quotes in title
    title_escaped = title.replace('"', '\\"')

    new_content = f'---\ntitle: "{title_escaped}"\n---\n\n{body}\n'

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f'  OK: {path}  →  "{title}"')

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
