#!/usr/bin/env python3
"""
add_tags.py - Add missing tags: frontmatter to content files.

Usage: python3 scripts/add_tags.py content
"""

import os
import re
import sys


MATHS_TAGS = {
    12: ["algebra", "field-theory", "polynomials"],
    13: ["algebra", "commutative-algebra", "rings"],
    14: ["algebra", "algebraic-geometry"],
    15: ["algebra", "linear-algebra", "matrices"],
    16: ["algebra", "ring-theory"],
    17: ["algebra", "lie-algebras"],
    18: ["category-theory", "homological-algebra"],
    19: ["k-theory", "algebra"],
    20: ["algebra", "group-theory"],
    22: ["topology", "lie-groups"],
    26: ["analysis", "real-analysis"],
    28: ["analysis", "measure-theory"],
    30: ["analysis", "complex-analysis"],
    31: ["analysis", "potential-theory"],
    32: ["analysis", "complex-analysis"],
    33: ["analysis", "special-functions"],
    34: ["analysis", "differential-equations"],
    35: ["analysis", "pde", "differential-equations"],
    37: ["analysis", "dynamical-systems"],
    39: ["analysis", "functional-equations"],
    40: ["analysis", "sequences", "series"],
    41: ["analysis", "approximation"],
    42: ["analysis", "harmonic-analysis"],
    43: ["analysis", "harmonic-analysis", "groups"],
    44: ["analysis", "integral-transforms"],
    45: ["analysis", "integral-equations"],
    46: ["analysis", "functional-analysis"],
    47: ["analysis", "operator-theory"],
    49: ["analysis", "calculus-of-variations", "optimization"],
    51: ["geometry"],
    52: ["geometry", "convex-geometry"],
    53: ["geometry", "differential-geometry"],
    54: ["topology", "general-topology"],
    55: ["topology", "algebraic-topology"],
    57: ["topology", "manifolds"],
    58: ["analysis", "manifolds"],
    60: ["probability", "stochastic-processes"],
    62: ["statistics", "probability"],
    65: ["numerical-analysis", "computation"],
    68: ["computer-science", "algorithms"],
    70: ["physics", "mechanics"],
    74: ["physics", "mechanics"],
    76: ["physics", "fluid-mechanics"],
    78: ["physics", "optics"],
    80: ["physics", "thermodynamics"],
    81: ["physics", "quantum-mechanics"],
    82: ["physics", "statistical-mechanics"],
    83: ["physics", "relativity"],
    85: ["physics", "astronomy"],
    86: ["physics", "geophysics"],
    90: ["optimization", "operations-research"],
    91: ["game-theory", "economics"],
    92: ["biology", "mathematics"],
    93: ["systems-theory", "control-theory"],
    94: ["information-theory", "circuits"],
    97: ["mathematics-education"],
}


def parse_frontmatter(content):
    """Return (frontmatter_lines, body_lines, has_frontmatter) tuple."""
    if not content.startswith("---"):
        return None, None, False
    lines = content.splitlines(keepends=True)
    if len(lines) < 2:
        return None, None, False
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, None, False
    return lines[1:end], lines[end + 1:], True


def get_title_from_frontmatter(fm_lines):
    """Extract title value from frontmatter lines."""
    for line in fm_lines:
        m = re.match(r'^title:\s*["\']?(.*?)["\']?\s*$', line)
        if m:
            return m.group(1).strip().strip('"\'')
    return ""


def has_tags(fm_lines):
    """Return True if frontmatter already contains a tags: key."""
    for line in fm_lines:
        if re.match(r'^\s*tags\s*:', line):
            return True
    return False


def find_insert_position(fm_lines):
    """
    Return index (within fm_lines) after which to insert tags line.
    Prefer after description:, else after title:, else at end.
    """
    desc_idx = None
    title_idx = None
    for i, line in enumerate(fm_lines):
        if re.match(r'^\s*description\s*:', line):
            desc_idx = i
        if re.match(r'^\s*title\s*:', line):
            title_idx = i
    if desc_idx is not None:
        return desc_idx
    if title_idx is not None:
        return title_idx
    return len(fm_lines) - 1


def format_tags(tags):
    """Format tags list as YAML inline array string."""
    items = ", ".join(f'"{t}"' for t in tags)
    return f"tags: [{items}]\n"


def determine_tags(filepath, fm_lines):
    """
    Determine which tags to add based on file path and frontmatter content.
    Returns a list of tags, or None if no rule matches.
    """
    # Normalize path separators
    norm = filepath.replace(os.sep, "/")

    title = get_title_from_frontmatter(fm_lines)
    title_lower = title.lower()
    basename = os.path.basename(filepath)

    # --- General special files ---
    if norm.endswith("content/en/_index.md"):
        return ["mathematics", "programming", "knowledge"]

    if norm.endswith("content/en/maths/_index.md"):
        return ["mathematics", "msc"]

    # --- Maths book _index.md files (e.g. content/en/maths/30/_index.md) ---
    maths_index_match = re.search(r'/maths/(\d+)/_index\.md$', norm)
    if maths_index_match:
        msc_num = int(maths_index_match.group(1))
        if msc_num in MATHS_TAGS:
            return list(MATHS_TAGS[msc_num])
        # No matching rule for this MSC number
        return None

    # --- Lean files ---
    if "/programming/lean/" in norm:
        tags = ["lean", "proof-assistant"]

        # Preface / index files
        if basename == "_index.md" or basename == "00.md":
            tags = ["lean", "proof-assistant", "type-theory"]
            return tags

        # Chapter 1
        if "/lean/01/" in norm:
            tags += ["type-theory", "functional-programming"]

        # Chapter 2
        elif "/lean/02/" in norm:
            tags += ["type-theory", "logic", "proof-theory"]
            # Keyword tags from title
            if "propositions as types" in title_lower:
                tags.append("propositions-as-types")
            if "implication" in title_lower or "conjunction" in title_lower or "disjunction" in title_lower or "negation" in title_lower:
                if "logic" not in tags:
                    tags.append("logic")
            if "equality" in title_lower:
                tags.append("equality")
            if "quantifier" in title_lower:
                tags.append("quantifiers")
            if "classical" in title_lower:
                tags.append("classical-logic")
            if "induction" in title_lower:
                tags.append("induction")
            if "tactic" in title_lower:
                tags.append("tactics")
            if "rewriting" in title_lower or "rewrite" in title_lower:
                tags.append("rewriting")

        # Lean _index.md (chapter index or top level)
        return tags

    # --- Algorithm files ---
    if "/programming/algorithms/" in norm:
        tags = ["algorithms", "computer-science"]

        # Chapter-specific base tags
        if "/algorithms/01/" in norm:
            tags += ["complexity", "foundations"]
        elif "/algorithms/02/" in norm:
            tags += ["arrays", "strings"]
        elif "/algorithms/03/" in norm:
            tags += ["data-structures", "linked-lists"]

        # Keyword tags from title
        if "complexity" in title_lower or "big o" in title_lower:
            if "complexity" not in tags:
                tags.append("complexity")
        if "dynamic programming" in title_lower:
            tags.append("dynamic-programming")
        if "greedy" in title_lower:
            tags.append("greedy")
        if "recursion" in title_lower or "recursive" in title_lower:
            tags.append("recursion")
        if "sorting" in title_lower or " sort" in title_lower or title_lower.startswith("sort"):
            tags.append("sorting")
        if "graph" in title_lower:
            tags.append("graphs")
        if "tree" in title_lower or "trees" in title_lower:
            tags.append("trees")
        if "hash" in title_lower:
            tags.append("hashing")
        if "binary search" in title_lower:
            tags.append("binary-search")
        if "loop invariant" in title_lower:
            tags.append("correctness")
        if "divide and conquer" in title_lower:
            tags.append("divide-and-conquer")
        if "randomization" in title_lower or "randomized" in title_lower:
            tags.append("randomized-algorithms")

        return tags

    # --- System design files ---
    if "/programming/system-design/" in norm:
        return ["system-design", "architecture", "engineering"]

    return None


def process_file(filepath):
    """
    Process a single markdown file. Return True if modified, False otherwise.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    fm_lines, body_lines, has_fm = parse_frontmatter(content)
    if not has_fm:
        return False

    if has_tags(fm_lines):
        return False

    tags = determine_tags(filepath, fm_lines)
    if tags is None:
        return False

    # Deduplicate while preserving order
    seen = set()
    unique_tags = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            unique_tags.append(t)

    insert_after = find_insert_position(fm_lines)
    tags_line = format_tags(unique_tags)

    new_fm = fm_lines[:insert_after + 1] + [tags_line] + fm_lines[insert_after + 1:]

    new_content = "---\n" + "".join(new_fm) + "---\n" + "".join(body_lines)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 add_tags.py <content_dir>")
        sys.exit(1)

    content_dir = sys.argv[1]
    if not os.path.isdir(content_dir):
        print(f"Error: {content_dir} is not a directory")
        sys.exit(1)

    modified = 0
    skipped_no_rule = 0
    skipped_has_tags = 0
    skipped_no_fm = 0

    for root, dirs, files in os.walk(content_dir):
        # Sort for deterministic output
        dirs.sort()
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            filepath = os.path.join(root, fname)

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            fm_lines, body_lines, has_fm = parse_frontmatter(content)
            if not has_fm:
                skipped_no_fm += 1
                continue

            if has_tags(fm_lines):
                skipped_has_tags += 1
                continue

            tags = determine_tags(filepath, fm_lines)
            if tags is None:
                skipped_no_rule += 1
                continue

            changed = process_file(filepath)
            if changed:
                # Deduplicate for display
                seen = set()
                display_tags = []
                for t in tags:
                    if t not in seen:
                        seen.add(t)
                        display_tags.append(t)
                rel = os.path.relpath(filepath, content_dir)
                print(f"  TAGGED  {rel}")
                print(f"          tags: {display_tags}")
                modified += 1

    print()
    print(f"Done. Modified: {modified}, already had tags: {skipped_has_tags}, "
          f"no matching rule: {skipped_no_rule}, no frontmatter: {skipped_no_fm}")


if __name__ == "__main__":
    main()
