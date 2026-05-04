#!/usr/bin/env python3
"""
Fix content/*.md files:
  1. Add description: to frontmatter if missing (extracted from first sentence)
  2. Remove standalone --- horizontal-rule lines from the body
"""
import re
import os
import sys


def first_sentence(body):
    for line in body.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(('#', '|', '!', '-', '*', '>')):
            continue
        # Skip numbered list items (1. 2. etc)
        if re.match(r'^\d+\.', line):
            continue
        if len(line) < 20:
            continue
        # Match sentence ending with . ! ? or their full-width equivalents
        m = re.match(r'([^.!?。！？]+[.!?。！？])', line)
        if m:
            s = m.group(1).strip()
            return s if len(s) <= 160 else s[:160].rsplit(' ', 1)[0] + '...'
        return line[:160].rsplit(' ', 1)[0] if len(line) > 160 else line
    return ''


def parse_fm(text):
    """Return (frontmatter_str, body_str) or (None, text) if no frontmatter."""
    if not text.startswith('---'):
        return None, text
    end = text.find('---', 3)
    if end == -1:
        return None, text
    return text[3:end], text[end + 3:]


def add_description(fm, body):
    """Insert description into frontmatter string if missing."""
    if 'description:' in fm:
        return fm, False
    desc = first_sentence(body)
    if not desc:
        return fm, False
    desc_esc = desc.replace('"', '\\"')
    # Insert after title line if present, else at end
    lines = fm.splitlines(keepends=True)
    insert_at = len(lines)
    for i, line in enumerate(lines):
        if line.startswith('title:'):
            insert_at = i + 1
            break
    lines.insert(insert_at, f'description: "{desc_esc}"\n')
    return ''.join(lines), True


def strip_hr(body):
    """Remove standalone --- lines (horizontal rules) from body."""
    new_body = re.sub(r'(?m)^\s*---\s*\n', '', body)
    changed = new_body != body
    return new_body, changed


def process_file(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()

    fm, body = parse_fm(text)
    if fm is None:
        return  # no frontmatter — skip (handled by add_frontmatter.py)

    changed = False

    fm, desc_added = add_description(fm, body)
    if desc_added:
        changed = True

    body, hr_removed = strip_hr(body)
    if hr_removed:
        changed = True

    if not changed:
        return

    new_text = '---' + fm + '---' + body
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_text)

    flags = []
    if desc_added:
        flags.append('desc')
    if hr_removed:
        flags.append('hr-removed')
    print(f'  [{",".join(flags)}] {path}')


def main(root):
    changed = 0
    for dirpath, _, filenames in os.walk(root):
        for fname in sorted(filenames):
            if not fname.endswith('.md'):
                continue
            path = os.path.join(dirpath, fname)
            before = open(path, encoding='utf-8').read()
            process_file(path)
            after = open(path, encoding='utf-8').read()
            if before != after:
                changed += 1
    print(f'\nDone. Modified {changed} files.')


if __name__ == '__main__':
    root = sys.argv[1] if len(sys.argv) > 1 else 'content'
    main(root)
