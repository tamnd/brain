---
title: "CF 118B - Present from Lena"
description: "We need to print a symmetric diamond made from numbers. The middle row contains numbers increasing from 0 up to n, then decreasing back to 0. Every row above and below follows the same pattern with a smaller maximum value."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 118
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 89 (Div. 2)"
rating: 1000
weight: 118
solve_time_s: 102
verified: true
draft: false
---

[CF 118B - Present from Lena](https://codeforces.com/problemset/problem/118/B)

**Rating:** 1000  
**Tags:** constructive algorithms, implementation  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to print a symmetric diamond made from numbers. The middle row contains numbers increasing from `0` up to `n`, then decreasing back to `0`. Every row above and below follows the same pattern with a smaller maximum value.

For example, when `n = 3`, the center row is:

```
0 1 2 3 2 1 0
```

The row above it stops at `2`:

```
0 1 2 1 0
```

The pattern continues until the top and bottom rows, which contain only `0`.

The tricky part is formatting. The rows must be aligned into a rhombus shape using leading spaces. Adjacent numbers inside a row are separated by exactly one space, and there must never be trailing spaces at the end of a line.

The constraint is tiny, since `n ≤ 9`. Even a very inefficient solution would fit comfortably within the time limit. The real challenge is implementation accuracy, especially spacing and symmetry.

A common mistake is printing extra spaces at the end of a line. For example, with input:

```
2
```

the correct third row is:

```
0 1 2 1 0
```

A careless implementation might produce:

```
0 1 2 1 0
```

with a trailing space. Codeforces judges compare output exactly, so this fails.

Another common mistake is miscalculating indentation. The leading spaces decrease as we move toward the center and increase afterward. For `n = 2`, the correct shape is:

```
    0
  0 1 0
0 1 2 1 0
  0 1 0
    0
```

If we print only one leading space per level instead of two, the rhombus becomes skewed because numbers themselves already contain spaces between them.

A third subtle issue is duplicating the peak number. For example, for `n = 3`, the center row should be:

```
0 1 2 3 2 1 0
```

not:

```
0 1 2 3 3 2 1 0
```

The decreasing sequence must start from `i - 1`, not from `i`.

## Approaches

The most direct approach is to think of the output as a grid of characters and fill every position manually. We could allocate a large 2D matrix, compute exactly where each digit belongs, and then print the matrix row by row. Since the maximum output size is tiny, this works easily within limits.

The problem with that approach is not performance, but unnecessary complexity. Managing coordinates, spacing, and symmetry inside a character grid introduces many opportunities for off-by-one mistakes.

The structure of the rhombus gives a cleaner observation. Every row is completely determined by three things:

1. The amount of indentation.
2. The increasing sequence from `0` to `i`.
3. The decreasing sequence from `i - 1` back to `0`.

Once we realize each row can be constructed independently as a string, the problem becomes straightforward string building.

For row `i`:

- The indentation is `2 * (n - i)` spaces.
- The left half is `0 1 2 ... i`.
- The right half is `i-1 ... 1 0`.

We first generate the upper half including the middle row, then mirror it downward.

Because the output itself contains `O(n²)` characters, any correct solution must spend at least `O(n²)` time printing them. The optimal solution matches this lower bound exactly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force grid construction | O(n²) | O(n²) | Accepted |
| Direct row construction | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`.
2. Iterate through all row indices from `0` to `n`.

Each row index represents the maximum number appearing in that row.
3. Compute the leading spaces.

The farther a row is from the center, the more indentation it needs. Each missing number level contributes two spaces because numbers inside the row are separated by single spaces.
4. Build the increasing sequence from `0` to `i`.

This forms the left half of the row and includes the peak value.
5. Build the decreasing sequence from `i - 1` down to `0`.

We start from `i - 1` to avoid duplicating the peak number.
6. Concatenate both sequences and join them with single spaces.

Using `" ".join(...)` guarantees correct spacing and avoids trailing spaces automatically.
7. Print the row with its indentation.
8. Repeat the same logic for rows from `n - 1` down to `0`.

This creates the lower symmetric half of the rhombus.

### Why it works

Each row is uniquely defined by its maximum value `i`. The increasing sequence guarantees numbers grow toward the center, while the decreasing sequence restores symmetry afterward. The indentation depends only on the distance from the middle row, so rows align into a rhombus automatically.

Because the algorithm constructs every row according to the exact mathematical structure of the pattern, every printed line matches the required output format.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_row(i, n):
    left = [str(x) for x in range(i + 1)]
    right = [str(x) for x in range(i - 1, -1, -1)]

    row = left + right
    spaces = " " * (2 * (n - i))

    return spaces + " ".join(row)

def solve():
    n = int(input())

    for i in range(n + 1):
        print(build_row(i, n))

    for i in range(n - 1, -1, -1):
        print(build_row(i, n))

solve()
```

The `build_row` function encapsulates the structure of a single line. Separating this logic avoids duplication because the upper and lower halves use identical formatting rules.

The increasing part uses:

```
range(i + 1)
```

so the peak value `i` is included.

The decreasing part uses:

```
range(i - 1, -1, -1)
```

which starts one step below the peak. This prevents duplicating the center value.

Indentation uses:

```
2 * (n - i)
```

because every number position effectively occupies two character slots, one for the digit and one for the separating space.

Using `" ".join(row)` is safer than manually appending spaces. It guarantees exactly one space between adjacent numbers and no trailing spaces at the end of the line.

The first loop prints the upper half including the center row. The second loop prints the mirrored lower half.

## Worked Examples

### Example 1

Input:

```
2
```

#### Upper Half

| Row `i` | Leading Spaces | Increasing Part | Decreasing Part | Final Row |
| --- | --- | --- | --- | --- |
| 0 | 4 | `0` | empty | `    0` |
| 1 | 2 | `0 1` | `0` | `  0 1 0` |
| 2 | 0 | `0 1 2` | `1 0` | `0 1 2 1 0` |

#### Lower Half

| Row `i` | Leading Spaces | Increasing Part | Decreasing Part | Final Row |
| --- | --- | --- | --- | --- |
| 1 | 2 | `0 1` | `0` | `  0 1 0` |
| 0 | 4 | `0` | empty | `    0` |

This trace shows how indentation shrinks toward the center and then expands symmetrically afterward.

### Example 2

Input:

```
3
```

#### Selected Rows

| Row `i` | Leading Spaces | Increasing Part | Decreasing Part | Final Row |
| --- | --- | --- | --- | --- |
| 0 | 6 | `0` | empty | `      0` |
| 1 | 4 | `0 1` | `0` | `    0 1 0` |
| 2 | 2 | `0 1 2` | `1 0` | `  0 1 2 1 0` |
| 3 | 0 | `0 1 2 3` | `2 1 0` | `0 1 2 3 2 1 0` |

This example demonstrates the central invariant: every row increases to its maximum value exactly once, then decreases symmetrically.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | There are `2n + 1` rows, each containing up to `2n + 1` numbers |
| Space | O(n) | Temporary lists used to build one row |

The constraints are extremely small, since `n ≤ 9`. The solution runs instantly and uses negligible memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    def build_row(i, n):
        left = [str(x) for x in range(i + 1)]
        right = [str(x) for x in range(i - 1, -1, -1)]

        row = left + right
        spaces = " " * (2 * (n - i))

        return spaces + " ".join(row)

    n = int(input())

    out = []

    for i in range(n + 1):
        out.append(build_row(i, n))

    for i in range(n - 1, -1, -1):
        out.append(build_row(i, n))

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue()

# provided sample
assert run("2\n") == (
    "    0\n"
    "  0 1 0\n"
    "0 1 2 1 0\n"
    "  0 1 0\n"
    "    0"
)

# minimum valid n
assert run("0\n") == "0"

# small symmetric case
assert run("1\n") == (
    "  0\n"
    "0 1 0\n"
    "  0"
)

# larger case checks center row
assert "0 1 2 3 4 3 2 1 0" in run("4\n")

# maximum constraint
out = run("9\n")
assert "0 1 2 3 4 5 6 7 8 9 8 7 6 5 4 3 2 1 0" in out

# no duplicated peak value
assert "0 1 2 2 1 0" not in run("2\n")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | Single `0` row | Smallest possible rhombus |
| `1` | Three symmetric rows | Basic upper/lower mirroring |
| `4` | Correct center row | Increasing and decreasing construction |
| `9` | Largest valid pattern | Maximum constraint handling |
| `2` with duplicate check | No repeated center value | Off-by-one in decreasing sequence |

## Edge Cases

Consider the smallest possible rhombus:

```
0
```

The algorithm handles this naturally. The upper loop runs once with `i = 0`, producing only the number `0`. The lower loop starts from `-1`, so it does not execute. No special handling is required.

Another subtle case is avoiding duplicate center values. For input:

```
2
```

the center row must be:

```
0 1 2 1 0
```

During construction:

- Increasing sequence becomes `0 1 2`
- Decreasing sequence becomes `1 0`

The decreasing part starts from `i - 1`, so `2` is not repeated.

Spacing alignment is another common source of bugs. For input:

```
1
```

the top row requires exactly two leading spaces:

```
  0
```

The formula `2 * (n - i)` gives:

```
2 * (1 - 0) = 2
```

which aligns the rhombus correctly. Using only `n - i` spaces would shift rows too far left and break the diamond shape.
