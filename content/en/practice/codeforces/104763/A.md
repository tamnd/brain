---
title: "CF 104763A - Jellyfish Art"
description: "The input is a single integer N, which determines the size of a text drawing of a jellyfish. The drawing has two distinct parts. The body occupies the first N rows. Every body row contains exactly 2N - 1 consecutive 'J' characters."
date: "2026-06-28T21:49:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104763
codeforces_index: "A"
codeforces_contest_name: "UTPC Contest 11-03-23 Div. 2 (Beginner)"
rating: 0
weight: 104763
solve_time_s: 135
verified: true
draft: false
---

[CF 104763A - Jellyfish Art](https://codeforces.com/problemset/problem/104763/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

The input is a single integer `N`, which determines the size of a text drawing of a jellyfish.

The drawing has two distinct parts. The body occupies the first `N` rows. Every body row contains exactly `2N - 1` consecutive `'J'` characters. Below the body come the tentacles, also occupying `N` rows. Each tentacle row contains exactly `N` `'S'` characters separated by single spaces, so the row has the form `"S S S ... S"`.

The constraints are very small. Even at the maximum value of `N = 100`, the output contains only `2N = 200` lines, and each line is at most `199` characters long. The total number of printed characters is only on the order of twenty thousand, so any straightforward construction of the required strings easily fits within the time and memory limits.

The main difficulty is formatting the output exactly as specified. The body width must be `2N - 1`, not `2N`, and the tentacles must contain spaces only between adjacent `'S'` characters, never after the final one.

One easy mistake appears when `N = 1`.

Input:

```
1
```

The correct output is

```
J
S
```

A careless implementation that always inserts spaces between tentacles without considering that there is only one tentacle could accidentally print `"S "` with a trailing space.

Another common formatting mistake is computing the body width incorrectly.

Input:

```
2
```

The correct output is

```
JJJ
JJJ
S S
S S
```

Printing `2N = 4` `'J'` characters instead of `2N - 1 = 3` produces an incorrect body.

A final formatting pitfall is leaving a trailing space after the last tentacle.

Input:

```
3
```

The correct tentacle row is

```
S S S
```

Printing

```
S S S
```

looks similar to a human reader but does not match the required output exactly.

## Approaches

The most direct approach is to construct every output line exactly as it should appear and print it. For the body, we create one string containing `2N - 1` `'J'` characters and print it `N` times. For the tentacles, we create one string by joining `N` copies of `"S"` with single spaces and print it `N` times.

Since the problem itself only asks us to generate the picture, this direct construction is already optimal. Even in the worst case, we generate only about twenty thousand characters, which is trivial for modern hardware.

There is no hidden optimization or advanced algorithm. The key observation is that every row of the body is identical, and every row of the tentacles is identical. Instead of rebuilding the same string repeatedly character by character, we can construct each distinct row once and reuse it. This keeps the implementation simple while avoiding unnecessary work.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Accepted |
| Optimal | O(N²) | O(N) | Accepted |

The complexity is dominated by the number of characters that must be printed, so no algorithm can asymptotically do better than the output size.

## Algorithm Walkthrough

1. Read the integer `N`.
2. Construct the body row as `'J' * (2 * N - 1)`. This produces exactly the required width for every body row.
3. Print the body row exactly `N` times. Since every body row is identical, reusing the same string is sufficient.
4. Construct the tentacle row using `' '.join(['S'] * N)`. Joining with spaces automatically places exactly one space between adjacent tentacles and avoids a trailing space.
5. Print the tentacle row exactly `N` times. Every tentacle row has the same appearance, so the same string can be reused.

### Why it works

The required picture consists of two rectangular sections. Every body row must be identical, containing exactly `2N - 1` consecutive `'J'` characters. Every tentacle row must also be identical, containing `N` `'S'` characters separated by single spaces. The algorithm constructs one correct representative for each section and prints each one the required number of times. Since every generated row exactly matches the specification, the complete drawing is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

body = "J" * (2 * n - 1)
tentacles = " ".join(["S"] * n)

for _ in range(n):
    print(body)

for _ in range(n):
    print(tentacles)
```

The program begins by reading the single input value.

The first constructed string is the body row. Multiplying a string by `2 * n - 1` produces the exact required width. Computing this once avoids rebuilding the same row repeatedly.

The tentacle row is created with `" ".join(["S"] * n)`. This is safer than manually appending spaces because `join` guarantees there is exactly one space between adjacent `'S'` characters and no trailing space at the end of the line.

The two loops correspond directly to the two sections of the drawing. The first loop prints the body rows, while the second prints the tentacle rows. Since the problem contains only one test case, no additional outer loop is needed.

## Worked Examples

### Sample 1

Input:

```
3
```

| Step | `N` | Constructed row | Output produced |
| --- | --- | --- | --- |
| Read input | 3 | - | - |
| Build body | 3 | `JJJJJ` | - |
| Print body | 3 | `JJJJJ` | 3 body rows |
| Build tentacles | 3 | `S S S` | - |
| Print tentacles | 3 | `S S S` | 3 tentacle rows |

The body width is `2 × 3 - 1 = 5`, producing `JJJJJ`. The tentacle row contains three `'S'` characters separated by single spaces. Every printed row matches the required format.

### Sample 2

Input:

```
6
```

| Step | `N` | Constructed row | Output produced |
| --- | --- | --- | --- |
| Read input | 6 | - | - |
| Build body | 6 | `JJJJJJJJJJJ` | - |
| Print body | 6 | `JJJJJJJJJJJ` | 6 body rows |
| Build tentacles | 6 | `S S S S S S` | - |
| Print tentacles | 6 | `S S S S S S` | 6 tentacle rows |

This example confirms that the same precomputed strings can be reused regardless of the value of `N`. The body width becomes `11`, and each tentacle row contains six tentacles with correct spacing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N²) | Printing each character dominates the running time. |
| Space | O(N) | Two output strings of length proportional to `N` are stored. |

Since `N` is at most `100`, the total output size is very small. The algorithm easily satisfies both the one second time limit and the available memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    body = "J" * (2 * n - 1)
    tentacles = " ".join(["S"] * n)

    for _ in range(n):
        print(body)
    for _ in range(n):
        print(tentacles)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided samples
assert run("3\n") == (
    "JJJJJ\n"
    "JJJJJ\n"
    "JJJJJ\n"
    "S S S\n"
    "S S S\n"
    "S S S\n"
), "sample 1"

assert run("6\n") == (
    "JJJJJJJJJJJ\n"
    "JJJJJJJJJJJ\n"
    "JJJJJJJJJJJ\n"
    "JJJJJJJJJJJ\n"
    "JJJJJJJJJJJ\n"
    "JJJJJJJJJJJ\n"
    "S S S S S S\n"
    "S S S S S S\n"
    "S S S S S S\n"
    "S S S S S S\n"
    "S S S S S S\n"
    "S S S S S S\n"
), "sample 2"

# custom cases
assert run("1\n") == (
    "J\n"
    "S\n"
), "minimum size"

assert run("2\n") == (
    "JJJ\n"
    "JJJ\n"
    "S S\n"
    "S S\n"
), "small even size"

out = run("100\n")
lines = out.strip().split("\n")
assert len(lines) == 200, "correct number of rows"
assert all(line == "J" * 199 for line in lines[:100]), "body width"
assert all(line == " ".join(["S"] * 100) for line in lines[100:]), "tentacles"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | One `J` row and one `S` row | Minimum input size |
| `2` | Body width of `3` and two tentacle rows | Correct computation of `2N - 1` |
| `100` | 200 correctly formatted rows | Maximum constraint and output size |
| `3` | `S S S` without trailing spaces | Correct spacing between tentacles |

## Edge Cases

When `N = 1`, the algorithm computes the body row as `"J" * 1`, producing a single `'J'`. The tentacle row is created by joining a one element list, which naturally produces `"S"` without extra spaces.

Input:

```
1
```

Execution builds `body = "J"` and `tentacles = "S"`, then prints each once.

Output:

```
J
S
```

When `N = 2`, the body width calculation becomes `2 × 2 - 1 = 3`. The algorithm constructs `"JJJ"` instead of `"JJJJ"`, avoiding the most common off by one error.

Input:

```
2
```

Execution builds `body = "JJJ"` and `tentacles = "S S"`.

Output:

```
JJJ
JJJ
S S
S S
```

For `N = 3`, the tentacle row is generated using `join`, so spaces appear only between adjacent tentacles.

Input:

```
3
```

The algorithm computes `tentacles = "S S S"` and prints it three times. No trailing space is added, matching the required output exactly.
