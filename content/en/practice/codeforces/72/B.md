---
title: "CF 72B - INI-file"
description: "We are given a text file written in INI format. Every meaningful line is either a section declaration such as [network] or a key-value assignment such as port=8080. Spaces around keys, values, and section brackets are irrelevant and must be removed in the final output."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 72
codeforces_index: "B"
codeforces_contest_name: "Unknown Language Round 2"
rating: 2200
weight: 72
solve_time_s: 105
verified: true
draft: false
---

[CF 72B - INI-file](https://codeforces.com/problemset/problem/72/B)

**Rating:** 2200  
**Tags:** *special, implementation  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a text file written in INI format. Every meaningful line is either a section declaration such as `[network]` or a key-value assignment such as `port=8080`. Spaces around keys, values, and section brackets are irrelevant and must be removed in the final output. Lines whose first non-space character is `;` are comments and should be ignored completely.

The file behaves like a sequence of updates. A key belongs either to the current section or to the global scope if no section has been declared yet. If the same key appears multiple times inside the same section, only the last occurrence survives. Different sections are independent, so the same key name may exist in several sections.

The output must be normalized in three ways. Global keys come first. Sections are printed afterward in lexicographical order. Inside each scope, keys are also printed in lexicographical order. Empty lines, comments, and redundant spaces disappear entirely.

The constraints are tiny compared to most competitive programming problems. There are at most 510 lines, and the total input size is only 10000 characters. Even relatively inefficient parsing strategies would pass comfortably. The main challenge is not performance, but correctly reproducing the exact semantics of overwriting, whitespace trimming, and section handling.

Several edge cases can silently break a careless implementation.

A section may appear multiple times in the file. All keys belonging to that section must be merged together.

Input:

```
4
[a]
x=1
[a]
y=2
```

Correct output:

```
[a]
x=1
y=2
```

A naive implementation that creates a new section object every time `[a]` appears would incorrectly print two separate sections.

Keys must overwrite earlier values inside the same section.

Input:

```
4
[a]
x=1
x=7
y=2
```

Correct output:

```
[a]
x=7
y=2
```

If we simply append assignments into a list, both `x` lines would remain.

Whitespace handling is also subtle.

Input:

```
3
  a   =   5
[b]
   c =  7
```

Correct output:

```
a=5
[b]
c=7
```

If spaces are not stripped carefully around both sides of `=`, the output format becomes invalid.

Comment detection depends on the first non-space character.

Input:

```
2
   ;hello
x=1
```

Correct output:

```
x=1
```

Checking only `line[0] == ';'` would fail because the semicolon is not literally the first character.

## Approaches

The most direct solution is to simulate the file exactly as written. We scan every line, maintain the current section, and store key-value pairs in a structure associated with that section. Whenever we encounter a duplicate key, we overwrite the old value. After parsing finishes, we sort sections and keys before printing.

A truly brute-force implementation could store every assignment in a list and, during output, scan backward to find the last value for each key. If there are `m` assignments, this can require checking almost every earlier assignment repeatedly. In the worst case, this becomes `O(m^2)` operations.

That approach still passes here because the input is small, but it is unnecessarily complicated and error-prone. The structure of the problem gives us a cleaner observation: only the latest value for each `(section, key)` pair matters. Earlier assignments become irrelevant immediately after a later overwrite appears.

That observation naturally leads to hash maps. We maintain one dictionary per section. Assigning a key simply becomes:

```
sections[current][key] = value
```

Any previous value is automatically replaced. Once parsing is done, we only need lexicographical sorting for output formatting.

The parsing itself is mostly implementation work. We must distinguish between comments, section headers, and assignments while trimming spaces correctly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m²) | O(m) | Accepted but unnecessary |
| Optimal | O(m log m) | O(m) | Accepted |

Here, `m` is the number of distinct stored keys plus sorting overhead.

## Algorithm Walkthrough

1. Create a dictionary for global keys and another dictionary that maps section names to their own dictionaries.
2. Initialize the current section as the global scope. We can represent it with an empty string.
3. Read each line and strip only the trailing newline character.
4. Remove leading and trailing spaces from the entire line. This simplifies later checks.
5. If the line is empty after trimming, ignore it. The statement says redundant lines should disappear.
6. If the first character is `;`, ignore the line because it is a comment.
7. If the line represents a section header, extract the section name.

A section line begins with `[` and ends with `]` after trimming spaces. We remove the brackets and trim the inside again because spaces around brackets are irrelevant.
8. If this section has not appeared before, create an empty dictionary for it.
9. Update the current section to this section name.
10. Otherwise, the line must be a key-value assignment. Split the string at the first `=` character.

Splitting only once is important because values themselves may contain symbols that should remain untouched.
11. Trim spaces around the key and value separately.
12. Store the assignment into the dictionary of the current section.

If the key already exists there, the new value overwrites the old one automatically.
13. After processing all lines, print global keys first in sorted order.
14. Then print all sections in sorted lexicographical order. For each section, print its keys in sorted order.

### Why it works

At every moment during parsing, each dictionary stores exactly the latest value seen for every key in that scope. When a duplicate assignment appears, replacing the stored value matches the problem requirement that only the last occurrence survives.

Sections are independent because each one has its own dictionary. Repeated appearances of the same section continue modifying the same dictionary, which correctly merges scattered definitions throughout the file.

The final sorting step guarantees lexicographical order regardless of the original input order.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    sections = {"": {}}
    current = ""

    for _ in range(n):
        line = input().rstrip("\n").strip()

        if not line:
            continue

        if line[0] == ';':
            continue

        if line[0] == '[' and line[-1] == ']':
            section = line[1:-1].strip()

            if section not in sections:
                sections[section] = {}

            current = section
        else:
            key, value = line.split("=", 1)

            key = key.strip()
            value = value.strip()

            sections[current][key] = value

    global_keys = sections[""]

    for key in sorted(global_keys):
        print(f"{key}={global_keys[key]}")

    for section in sorted(s for s in sections if s != ""):
        print(f"[{section}]")

        for key in sorted(sections[section]):
            print(f"{key}={sections[section][key]}")

if __name__ == "__main__":
    solve()
```

The solution keeps every scope in a dictionary. The empty string represents the global scope because keys before the first section belong nowhere else.

The parsing logic starts by trimming the whole line. This is critical because comments may start after leading spaces and section brackets may also contain surrounding spaces.

The section parsing uses:

```
section = line[1:-1].strip()
```

Without the second `strip()`, an input like `[  abc  ]` would incorrectly store the section name with spaces.

Assignments use:

```
line.split("=", 1)
```

The second argument prevents accidental extra splitting. Even though the official constraints keep values simple, this is the safest parsing style.

The overwrite behavior comes naturally from dictionary assignment. No explicit duplicate handling is required.

During output, the global scope is printed first, then every real section in sorted order. Keys inside each scope are also sorted before printing.

## Worked Examples

### Sample 1

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

Trace:

| Step | Line | Current Section | Action | Stored State |
| --- | --- | --- | --- | --- |
| 1 | `a= 1` | global | store `a=1` | global:`{a:1}` |
| 2 | `b=a` | global | store `b=a` | global:`{a:1,b:a}` |
| 3 | `a = 2` | global | overwrite `a` | global:`{a:2,b:a}` |
| 4 | `; comment` | global | ignore | unchanged |
| 5 | `[z]` | z | create section | z:`{}` |
| 6 | `1=2` | z | store `1=2` | z:`{1:2}` |
| 7 | `[y]` | y | create section | y:`{}` |
| 8 | `2=3` | y | store `2=3` | y:`{2:3}` |
| 9 | `[z]` | z | switch section | unchanged |
| 10 | `2=1` | z | store `2=1` | z:`{1:2,2:1}` |
| 11 | `[w]` | w | create empty section | w:`{}` |

Final output:

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

This trace shows two important properties. Re-entering section `z` continues modifying the same dictionary, and duplicate global keys overwrite earlier values.

### Custom Example

Input:

```
8
  ;ignore
[a]
x=1
x = 9
[b]
z=3
[a]
y=2
```

Trace:

| Step | Line | Current Section | Action | State |
| --- | --- | --- | --- | --- |
| 1 | `;ignore` | global | ignore | empty |
| 2 | `[a]` | a | create section | a:`{}` |
| 3 | `x=1` | a | store | a:`{x:1}` |
| 4 | `x = 9` | a | overwrite | a:`{x:9}` |
| 5 | `[b]` | b | create section | b:`{}` |
| 6 | `z=3` | b | store | b:`{z:3}` |
| 7 | `[a]` | a | switch back | unchanged |
| 8 | `y=2` | a | store | a:`{x:9,y:2}` |

Final output:

```
[a]
x=9
y=2
[b]
z=3
```

This example demonstrates that repeated sections merge naturally and that overwriting happens within a single section only.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m) | Sorting keys and section names dominates |
| Space | O(m) | Stores all surviving key-value pairs |

Here, `m` is the number of stored assignments after parsing. Since the total input size is only 10000 characters, this solution easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())

    sections = {"": {}}
    current = ""

    for _ in range(n):
        line = input().rstrip("\n").strip()

        if not line:
            continue

        if line[0] == ';':
            continue

        if line[0] == '[' and line[-1] == ']':
            section = line[1:-1].strip()

            if section not in sections:
                sections[section] = {}

            current = section
        else:
            key, value = line.split("=", 1)

            key = key.strip()
            value = value.strip()

            sections[current][key] = value

    out = []

    for key in sorted(sections[""]):
        out.append(f"{key}={sections[''][key]}")

    for section in sorted(s for s in sections if s != ""):
        out.append(f"[{section}]")

        for key in sorted(sections[section]):
            out.append(f"{key}={sections[section][key]}")

    print("\n".join(out))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return result

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
2=1""", "sample 1"

# minimum case
assert run(
"""1
a=1
"""
) == """a=1""", "single global key"

# duplicate overwrite
assert run(
"""4
[a]
x=1
x=2
x=3
"""
) == """[a]
x=3""", "latest value survives"

# repeated sections merge
assert run(
"""5
[a]
x=1
[b]
y=2
[a]
"""
) == """[a]
x=1
[b]
y=2""", "same section reused"

# whitespace and comments
assert run(
"""5
   ; ignore
 [ sec ]
  a   =   9
b=2
 ;x
"""
) == """[sec]
a=9
b=2""", "space trimming"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single key | `a=1` | Minimum valid input |
| Duplicate assignments | `x=3` survives | Overwrite semantics |
| Repeated sections | Keys merged into same section | Correct section reuse |
| Whitespace-heavy input | Clean normalized formatting | Proper trimming and comment handling |

## Edge Cases

Consider repeated section declarations.

Input:

```
5
[a]
x=1
[b]
y=2
[a]
```

When the parser sees the second `[a]`, it does not create a new dictionary because section `a` already exists. It only switches `current` back to `"a"`. The stored data remains:

```
a -> {x:1}
b -> {y:2}
```

The final output correctly contains a single `[a]` section.

Now consider overwriting inside one section.

Input:

```
4
[a]
x=1
x=5
x=9
```

The dictionary transitions are:

```
{x:1}
{x:5}
{x:9}
```

Each assignment replaces the previous value. Only the latest survives, exactly matching the specification.

Whitespace-heavy parsing is another common source of bugs.

Input:

```
3
 [ abc ]
   k   =   v
 ;hello
```

After trimming:

```
[ abc ]
k   =   v
;hello
```

The section name becomes `"abc"` after removing brackets and stripping again. The assignment becomes `k=v`. The comment disappears entirely.

Finally, global keys must remain separate from section keys.

Input:

```
4
x=1
[a]
x=2
y=3
```

The parser stores:

```
global -> {x:1}
a -> {x:2, y:3}
```

The two `x` keys do not conflict because they belong to different scopes. The output is:

```
x=1
[a]
x=2
y=3
```
