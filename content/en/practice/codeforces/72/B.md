---
title: "CF 72B - INI-file"
description: "We are given a text file written in a simplified INI configuration format. Every meaningful line is either a section declaration like [network] or a key-value assignment like timeout = 30. Lines may contain redundant spaces around keys, values, or section brackets."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 72
codeforces_index: "B"
codeforces_contest_name: "Unknown Language Round 2"
rating: 2200
weight: 72
solve_time_s: 118
verified: true
draft: false
---

[CF 72B - INI-file](https://codeforces.com/problemset/problem/72/B)

**Rating:** 2200  
**Tags:** *special, implementation  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a text file written in a simplified INI configuration format. Every meaningful line is either a section declaration like `[network]` or a key-value assignment like `timeout = 30`. Lines may contain redundant spaces around keys, values, or section brackets. Comment lines begin with `;` after skipping leading spaces, and must be ignored completely.

The file is processed sequentially. A section declaration changes the current active section, and every following key-value pair belongs to that section until another section appears. Key-value pairs that appear before the first section belong to a special global area outside all sections.

The output is a normalized version of the file. All spaces must be removed around keys, values, and section names. Duplicate keys inside the same section are resolved by keeping only the last occurrence from the input. The global area is printed first, then all sections in lexicographical order. Inside every section, keys are also printed in lexicographical order.

The constraints are tiny compared to most implementation-heavy problems. We have at most 510 lines and total input length at most 10000 characters. Even an $O(n^2)$ solution would comfortably pass. The challenge is not performance, it is correctly reproducing all formatting and overwrite rules.

The dangerous part of this problem is parsing. Several situations can silently break a careless implementation.

One common mistake is forgetting that spaces around section brackets must be ignored.

Input:

```
3
[ z ]
a=1
[z]
```

The two section declarations refer to the same section `"z"`. Treating raw strings literally would incorrectly create two separate sections.

Another subtle case is overwriting keys only inside the same section.

Input:

```
5
a=1
[x]
a=2
[y]
a=3
```

Correct output:

```
a=1
[x]
a=2
[y]
a=3
```

The three assignments use the same key name, but they belong to different scopes.

Comments also require care because only the first non-space character matters.

Input:

```
2
   ; hello
a=1
```

The first line must be ignored completely. Checking only `line[0] == ';'` would fail.

Another easy bug is losing insertion independence after overwrites.

Input:

```
4
[x]
b=1
a=2
b=3
```

Correct output:

```
[x]
a=2
b=3
```

The final value of `b` is `3`, but sorting is done only at output time. During parsing we only need the latest value per key.

## Approaches

A brute-force implementation can literally simulate the file structure as text. Every time we encounter a key-value pair, we scan all previously stored entries inside the current section and remove any earlier occurrence with the same key. After processing the whole file, we sort sections and keys before printing.

This works because the input is small. In the worst case, each new key scans all earlier keys, leading to roughly $O(n^2)$ operations. With only a few hundred lines, this is still fast enough.

The problem becomes cleaner once we observe that duplicate handling follows standard dictionary semantics. For every section, only the latest value of each key matters. That means we never need to keep older duplicates at all.

The natural representation is:

- a dictionary mapping section name to another dictionary
- one extra dictionary for keys outside sections

As we parse the file, we normalize spaces immediately and store:

```
section[key] = value
```

If the key already exists, assignment automatically overwrites the older value. After parsing, we simply sort section names and keys lexicographically before printing.

The key insight is that overwrite order matters only during parsing, while output order is entirely determined by lexicographical sorting. Once we separate those two concerns, the implementation becomes straightforward.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(n)$ | Accepted |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Create one dictionary for global key-value pairs and another dictionary mapping section names to their own dictionaries.
2. Maintain a variable `current_section`. Initially it is `None`, meaning we are outside all sections.
3. Read each line and remove leading and trailing spaces.
4. If the first non-space character is `;`, ignore the line completely because it is a comment.
5. If the line represents a section, extract the text between brackets and trim spaces around the name.

For example:

```
[  abc  ]
```

becomes:

```
abc
```
6. Update `current_section` to this normalized section name.

If the section has not appeared before, create an empty dictionary for it.
7. Otherwise the line is a key-value assignment. Split it at `'='`, trim spaces around both sides, and obtain the normalized key and value.
8. Store the pair in the correct dictionary.

If `current_section is None`, store it in the global dictionary.

Otherwise store it in:

```
sections[current_section]
```
9. Because dictionaries overwrite existing keys automatically, the latest occurrence survives without extra work.
10. After all lines are processed, print global keys first in lexicographical order.
11. Then print section names in lexicographical order. For each section:

- print `[section]`
- print all keys inside it in lexicographical order

### Why it works

At every moment during parsing, each dictionary contains exactly the latest value for every key in its scope. Earlier duplicates are overwritten immediately and can never affect the final answer again.

The algorithm also preserves section separation because every section has its own independent dictionary. Keys with the same name in different sections never interact.

Finally, output ordering is correct because sorting is performed explicitly during printing. Since every surviving key already stores the correct final value, sorting cannot change correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    global_keys = {}
    sections = {}

    current_section = None

    for _ in range(n):
        line = input().rstrip('\n')

        stripped = line.strip()

        if not stripped:
            continue

        if stripped[0] == ';':
            continue

        if stripped[0] == '[':
            section_name = stripped[1:-1].strip()

            current_section = section_name

            if current_section not in sections:
                sections[current_section] = {}

        else:
            key, value = stripped.split('=', 1)

            key = key.strip()
            value = value.strip()

            if current_section is None:
                global_keys[key] = value
            else:
                sections[current_section][key] = value

    out = []

    for key in sorted(global_keys):
        out.append(f"{key}={global_keys[key]}")

    for section in sorted(sections):
        out.append(f"[{section}]")

        for key in sorted(sections[section]):
            out.append(f"{key}={sections[section][key]}")

    sys.stdout.write('\n'.join(out))

solve()
```

The implementation follows the parsing rules directly.

The first important choice is normalizing every line immediately with `strip()`. This removes surrounding spaces so that section parsing and comment detection become reliable.

Comment handling checks the first non-space character after trimming:

```
if stripped[0] == ';':
```

This correctly ignores lines like:

```
   ; comment
```

Section parsing uses:

```
stripped[1:-1].strip()
```

The outer slice removes brackets, while the second `strip()` removes spaces around the actual section name.

For key-value lines, splitting is done with:

```
split('=', 1)
```

The limit `1` matters because values may theoretically contain `=` in more general parsers. Using a single split is safer and standard practice.

The overwrite rule becomes automatic because Python dictionaries replace existing values for the same key.

The output phase intentionally separates parsing order from printing order. Keys and sections are sorted only at the end, which keeps the logic simple and avoids maintaining ordered structures during parsing.

## Worked Examples

### Example 1

Input:

```
11
a= 1
b=a
a = 2
 ; comment
[z]
1=2
[y]
2=3
[z]
2=1
[w]
```

### Parsing Trace

| Line | Current Section | Action | Global | Sections |
| --- | --- | --- | --- | --- |
| `a= 1` | None | store `a=1` | `{a:1}` | `{}` |
| `b=a` | None | store `b=a` | `{a:1,b:a}` | `{}` |
| `a = 2` | None | overwrite `a` | `{a:2,b:a}` | `{}` |
| `; comment` | None | ignore | `{a:2,b:a}` | `{}` |
| `[z]` | z | create section | unchanged | `{z:{}}` |
| `1=2` | z | store key | unchanged | `{z:{1:2}}` |
| `[y]` | y | create section | unchanged | `{z:{1:2},y:{}}` |
| `2=3` | y | store key | unchanged | `{z:{1:2},y:{2:3}}` |
| `[z]` | z | switch section | unchanged | unchanged |
| `2=1` | z | store key | unchanged | `{z:{1:2,2:1},y:{2:3}}` |
| `[w]` | w | create section | unchanged | add empty `w` |

### Final Output

```
a=2
b=a
[w]
[y]
2=3
[z]
1=2
2=1
```

This example demonstrates all major rules together: overwriting keys, ignoring comments, revisiting existing sections, and lexicographical ordering.

### Example 2

Input:

```
7
 [ x ]
 b = 1
 a = 2
 b = 3
[y]
a=5
a=1
```

### Parsing Trace

| Line | Current Section | Action | State |
| --- | --- | --- | --- |
| `[ x ]` | x | create section | `x:{}` |
| `b = 1` | x | store `b=1` | `x:{b:1}` |
| `a = 2` | x | store `a=2` | `x:{b:1,a:2}` |
| `b = 3` | x | overwrite `b` | `x:{b:3,a:2}` |
| `[y]` | y | create section | add `y:{}` |
| `a=5` | y | store `a=5` | `y:{a:5}` |
| `a=1` | y | overwrite `a` | `y:{a:1}` |

### Final Output

```
[x]
a=2
b=3
[y]
a=1
```

This trace confirms that overwrites happen independently inside each section and that sorting occurs only during output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting keys and section names dominates |
| Space | $O(n)$ | All surviving key-value pairs are stored |

The total amount of input is extremely small, so this solution easily fits within both the 5 second time limit and the 256 MB memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n = int(input())

        global_keys = {}
        sections = {}

        current_section = None

        for _ in range(n):
            line = input().rstrip('\n')

            stripped = line.strip()

            if stripped[0] == ';':
                continue

            if stripped[0] == '[':
                section_name = stripped[1:-1].strip()

                current_section = section_name

                if current_section not in sections:
                    sections[current_section] = {}

            else:
                key, value = stripped.split('=', 1)

                key = key.strip()
                value = value.strip()

                if current_section is None:
                    global_keys[key] = value
                else:
                    sections[current_section][key] = value

        out = []

        for key in sorted(global_keys):
            out.append(f"{key}={global_keys[key]}")

        for section in sorted(sections):
            out.append(f"[{section}]")

            for key in sorted(sections[section]):
                out.append(f"{key}={sections[section][key]}")

        return '\n'.join(out)

    return solve()

# provided sample
assert run(
"""11
a= 1
b=a
a = 2
 ; comment
[z]
1=2
[y]
2=3
[z]
2=1
[w]
"""
) == """a=2
b=a
[w]
[y]
2=3
[z]
1=2
2=1"""

# minimum size
assert run(
"""1
a=1
"""
) == "a=1"

# overwrite inside same section
assert run(
"""5
[x]
a=1
a=2
a=3
b=4
"""
) == """[x]
a=3
b=4"""

# same key in different sections
assert run(
"""6
a=1
[x]
a=2
[y]
a=3
a=4
"""
) == """a=1
[x]
a=2
[y]
a=4"""

# spaces and comments
assert run(
"""5
   ; hello
 [ z ]
 a = 1
[z]
b=2
"""
) == """[z]
a=1
b=2"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single global key | Same single line | Minimum valid input |
| Multiple overwrites in one section | Only last value survives | Duplicate handling |
| Same key across sections | Independent values preserved | Scope separation |
| Spaces and comments | Normalized output | Correct parsing rules |

## Edge Cases

### Repeated section declarations

Input:

```
5
[x]
a=1
[y]
b=2
[x]
```

The second `[x]` does not create a new independent section. The algorithm stores sections in a dictionary keyed by section name, so switching back to `"x"` reuses the same dictionary.

Final output:

```
[x]
a=1
[y]
b=2
```

### Comment lines with leading spaces

Input:

```
3
   ; ignored
a=1
b=2
```

After `strip()`, the first line becomes:

```
; ignored
```

The parser correctly skips it because the first non-space character is `;`.

Output:

```
a=1
b=2
```

### Spaces around section names

Input:

```
4
[ abc ]
x=1
[abc]
y=2
```

Both declarations normalize to `"abc"` after:

```
stripped[1:-1].strip()
```

The algorithm merges them into the same section.

Output:

```
[abc]
x=1
y=2
```

### Keys outside sections

Input:

```
4
b=2
a=1
[x]
c=3
```

The parser starts with `current_section = None`, so the first two keys are stored in the global dictionary.

Output:

```
a=1
b=2
[x]
c=3
```

This confirms that global keys are printed before all sections and sorted independently.
