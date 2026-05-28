---
title: "CF 16A - Flag"
description: "We are given a rectangular grid representing a country’s flag. Each cell in the grid has a color, encoded as a digit from 0 to 9. The dimensions of the flag are rows by columns. The goal is to determine whether the flag is “striped” according to the new ISO standard."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 16
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 16 (Div. 2 Only)"
rating: 800
weight: 16
solve_time_s: 68
verified: true
draft: false
---
[CF 16A - Flag](https://codeforces.com/problemset/problem/16/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular grid representing a country’s flag. Each cell in the grid has a color, encoded as a digit from 0 to 9. The dimensions of the flag are $n$ rows by $m$ columns. The goal is to determine whether the flag is “striped” according to the new ISO standard. A flag is striped if every row contains cells of the same color, and consecutive rows do not share the same color.

The input is small, with $n, m \leq 100$. This means that even an $O(n \cdot m)$ solution is acceptable, because the total number of cells is at most 10,000, which is trivial for modern CPUs.

Some non-obvious edge cases include flags with a single row, where there is no previous row to compare to, and flags with a single column, where each row still needs to be uniform. For example, a flag with one row of three cells `111` should return `YES` because all cells in that row are identical, even though there is no row above or below to compare colors. Another tricky scenario is when two adjacent rows accidentally share the same color, like `111` followed by `111`. This should return `NO` because the stripes are not distinct.

## Approaches

A brute-force approach would iterate over every cell, checking two conditions: each row is uniform and each consecutive row is different from the previous one. This is correct because the problem explicitly defines the properties of a valid flag. The complexity is $O(n \cdot m)$, which is acceptable for this problem size.

The key insight is that we can simplify the check: instead of verifying each individual cell against every other cell in the row repeatedly, we only need to compare each cell to the first cell of the row. If any cell differs, the row is invalid. For checking consecutive rows, we just compare the first cell of the current row to the first cell of the previous row. This reduces unnecessary comparisons but does not change the asymptotic complexity.

The brute-force works because it checks every requirement explicitly, but the observation about row-first-cell comparison reduces the cognitive and implementation complexity, making the code cleaner and less error-prone.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·m) | O(1) | Accepted |
| Optimized row-first check | O(n·m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the dimensions $n$ and $m$ from input and store the flag as a list of strings, where each string represents a row. This preserves the row structure for easy checking.
2. Iterate over each row starting from the first. For each row, check that all cells are identical. Compare each character in the row to the first character. If any character differs, output `NO` and stop.
3. If the current row is not the first, compare its first character with the first character of the previous row. If they are the same, output `NO` and stop.
4. If all rows pass both checks, output `YES`.

**Why it works:** The algorithm ensures that every row is uniform by comparing all cells to the row’s first cell. By checking consecutive rows’ first cells, it ensures that adjacent rows are different. These two checks satisfy the definition of a striped flag. No other checks are necessary because color digits are guaranteed to be 0-9.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
flag = [input().strip() for _ in range(n)]

for i in range(n):
    row = flag[i]
    if any(c != row[0] for c in row):
        print("NO")
        sys.exit(0)
    if i > 0 and row[0] == flag[i - 1][0]:
        print("NO")
        sys.exit(0)

print("YES")
```

The code first reads the flag into a list of strings. The `any(c != row[0] for c in row)` construct checks row uniformity efficiently. The second condition ensures stripes are different. Using `sys.exit(0)` immediately terminates the program when a violation is found, which avoids unnecessary iteration over the remaining rows.

## Worked Examples

**Sample 1**

Input:

```
3 3
000
111
222
```

| Step | Row | Uniform? | First cell vs previous row? |
| --- | --- | --- | --- |
| 0 | 000 | Yes | N/A |
| 1 | 111 | Yes | 1 != 0, OK |
| 2 | 222 | Yes | 2 != 1, OK |

Output: `YES`

Explanation: Each row is uniform and no two consecutive rows have the same color.

**Custom Input 2**

Input:

```
2 3
111
111
```

| Step | Row | Uniform? | First cell vs previous row? |
| --- | --- | --- | --- |
| 0 | 111 | Yes | N/A |
| 1 | 111 | Yes | 1 == 1, FAIL |

Output: `NO`

Explanation: Consecutive rows share the same color.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n·m) | We scan each row entirely once. |
| Space | O(n·m) | Storing the grid as a list of strings requires one string per row. |

For $n, m \leq 100$, the algorithm handles at most 10,000 cells, well within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    n, m = map(int, input().split())
    flag = [input().strip() for _ in range(n)]
    for i in range(n):
        row = flag[i]
        if any(c != row[0] for c in row):
            print("NO")
            return sys.stdout.getvalue().strip()
        if i > 0 and row[0] == flag[i - 1][0]:
            print("NO")
            return sys.stdout.getvalue().strip()
    print("YES")
    return sys.stdout.getvalue().strip()

# Provided sample
assert run("3 3\n000\n111\n222\n") == "YES", "sample 1"

# Custom cases
assert run("1 5\n33333\n") == "YES", "single row"
assert run("5 1\n1\n2\n3\n4\n5\n") == "YES", "single column, distinct"
assert run("2 4\n7777\n7777\n") == "NO", "repeated color"
assert run("3 3\n123\n456\n789\n") == "NO", "row not uniform"
assert run("3 2\n11\n22\n22\n") == "NO", "last two rows same"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5\n33333 | YES | Single row is valid |
| 5 1\n1\n2\n3\n4\n5 | YES | Single-column flag with distinct colors |
| 2 4\n7777\n7777 | NO | Adjacent rows share color |
| 3 3\n123\n456\n789 | NO | Row not uniform |
| 3 2\n11\n22\n22 | NO | Last two rows same color |

## Edge Cases

A flag with one row, such as:

```
1 4
4444
```

Algorithm checks the row uniformity: `all(c == row[0] for c in row)` passes. Since there is no previous row, the adjacent-row check is skipped. Output is `YES`.

A flag with one column:

```
3 1
1
2
2
```

Row uniformity trivially passes because each row has one cell. The adjacent-row check fails for the last two rows because `2 == 2`. Output is `NO`.

These examples confirm that the algorithm handles minimal dimensions and edge comparisons correctly.
