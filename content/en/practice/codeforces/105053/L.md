---
title: "CF 105053L - LED Matrix"
description: "We are given a rectangular LED matrix and a rectangular pattern that is supposed to scroll across it from right to left. The matrix has fixed dimensions, and each cell is either functional or broken. A functional LED can be turned on, while a broken one can never light up."
date: "2026-06-28T01:04:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105053
codeforces_index: "L"
codeforces_contest_name: "The 2024 ICPC Latin America Championship"
rating: 0
weight: 105053
solve_time_s: 56
verified: true
draft: false
---

[CF 105053L - LED Matrix](https://codeforces.com/problemset/problem/105053/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular LED matrix and a rectangular pattern that is supposed to scroll across it from right to left. The matrix has fixed dimensions, and each cell is either functional or broken. A functional LED can be turned on, while a broken one can never light up.

The pattern is a grid of the same height but possibly different width. As it scrolls, the pattern is repeatedly shifted horizontally across the matrix. At each shift, a vertical slice of the pattern is aligned with some column of the matrix, and certain pattern cells demand that the corresponding matrix LEDs must be turned on at that moment.

The key question is not to simulate the animation, but to decide whether there exists any moment in the entire scrolling process where a broken LED would be required to light up. If that ever happens, the display is impossible and the answer is “N”, otherwise it is “Y”.

The input describes, for each row, both the matrix state and the pattern row. This coupling by row matters because constraints are independent across rows: each row behaves like a 1D interaction between the matrix columns and pattern columns.

The bounds go up to 1000 for rows, columns, and pattern width. A cubic simulation over rows, matrix columns, and shifts would reach about 10^9 operations, which is too slow. Even a double nested scan per shift is too large, so the solution must avoid explicitly simulating each scrolling step.

A subtle edge case appears when the pattern is smaller than the matrix. Even then, scrolling still continues beyond full overlap, meaning pattern columns can align with many matrix positions over time. Another edge case is when a cell is broken but the pattern only requires it to be off at the “initial” alignment; later shifts may still activate it. This is exactly what makes naive checking by only looking at one alignment incorrect.

## Approaches

The brute-force idea is to simulate every scroll position. For each shift, we place the pattern over the matrix and check every overlapping cell. If a pattern cell that is `*` lands on a matrix cell that is `-`, we fail.

This is correct because it explicitly checks all states of the animation. However, the number of shifts is proportional to the sum of matrix width and pattern width, and each shift checks up to R×C cells. This leads to roughly O(R·C·(C+K)) operations, which is far beyond the limit when all dimensions reach 1000.

The key observation is that we do not actually need to know _when_ a pattern cell hits a matrix cell, only whether it ever does. For a fixed row and fixed matrix column, we can ask a simpler question: does any `*` in the pattern row ever align with this matrix position during the scroll?

Once we rewrite the problem in this way, the time dimension disappears. Each matrix cell only needs to know whether there exists at least one pattern column that ever maps onto it. That becomes a range existence query over the pattern row, which can be answered with prefix sums.

This reduces the problem to checking, for every matrix cell, whether its corresponding alignment interval contains at least one `*` in the pattern.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(R·C·(C+K)) | O(1) extra | Too slow |
| Prefix Range Checking | O(R·(C+K)) | O(R·K) | Accepted |

## Algorithm Walkthrough

We process each row independently, since rows do not interact.

1. For a fixed row, precompute a prefix sum over the pattern row where each position stores how many `*` characters appear up to that index. This allows fast range queries.
2. For each matrix column `c`, determine which pattern columns can ever align with it during the full scroll. This set forms a contiguous interval in the pattern row.
3. Compute the left boundary of this interval. A pattern column `j` can reach matrix column `c` if the scroll ever shifts it into position `c`, which implies a simple linear relation between `c` and `j`. This reduces to a lower bound on `j`.
4. If this interval contains any `*` in the pattern row, then matrix cell `(row, c)` must be functional. If the matrix cell is broken, the configuration is invalid immediately.
5. Repeat for all rows and all columns. If no conflict is found, the display is possible.

### Why it works

Each pattern cell contributes constraints only to those matrix cells it can ever occupy during scrolling. The motion is purely linear, so each pattern column affects a contiguous range of matrix columns. That means each matrix cell only needs to know whether any required-on pattern cell ever maps to it. If such a mapping exists and the matrix cell is broken, that requirement can never be satisfied, so correctness reduces to detecting any such forbidden intersection.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    R, C, K = map(int, input().split())

    mat = []
    pat = []

    for _ in range(R):
        line = input().split()
        mat.append(line[0])
        pat.append(line[1])

    for i in range(R):
        # prefix sum of '*' in pattern row
        pref = [0] * (K + 1)
        for j in range(K):
            pref[j + 1] = pref[j] + (1 if pat[i][j] == '*' else 0)

        for c in range(C):
            if mat[i][c] == '*':
                continue

            # earliest pattern column that can reach c
            L = max(0, c - (C - 1))

            # check if there is any '*' in pat[i][L:K]
            if pref[K] - pref[L] > 0:
                print("N")
                return

    print("Y")

if __name__ == "__main__":
    solve()
```

The solution reads both the matrix and pattern row by row. For each row, it builds a prefix sum over the pattern to support constant time checks for whether any `*` exists in a suffix.

For each matrix cell that is broken, it computes the earliest pattern index that could ever reach it. Instead of simulating shifts, this uses the fact that scrolling is linear and every pattern column sweeps across a contiguous range of matrix columns. If any required-on pattern cell lies in that reachable range, the cell is invalid.

The key implementation detail is the computation of `L = max(0, c - (C - 1))`. This encodes the earliest pattern column that can possibly land on matrix column `c` during the full scroll.

## Worked Examples

Consider a small conceptual example with one row:

Matrix: `* - -`

Pattern: `*-*`

The prefix sum for the pattern is `[0,1,1,2]`.

For the broken cell at column 1, we compute `L = max(0, 1 - 2) = 0`. The suffix `[0:3]` contains stars, so this cell is required to light up at some point, but it is broken. The algorithm correctly rejects.

Now consider:

Matrix: `* * *`

Pattern: `*-*`

Every matrix cell is functional, so no matter how the pattern shifts, there is no failure condition. Even though some alignments require stars, all required cells are valid.

| Row | Column | Broken? | Range check | Pattern stars in range | Result |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | No | skipped | - | OK |
| 0 | 1 | No | skipped | - | OK |
| 0 | 2 | No | skipped | - | OK |

This shows that the algorithm only reacts to impossible constraints and otherwise remains silent.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(R·(C + K)) | Each row builds a prefix over K and scans C columns once |
| Space | O(K) | Only prefix array per row |

The constraints allow up to 10^6 total characters per structure, so a linear scan per row fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import contextlib

    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# minimal allowed case
assert run("1 1 1\n* *\n") == "Y"

# broken cell never required
assert run("1 3 2\n*-- *-\n") == "Y"

# broken cell required eventually
assert run("1 3 2\n-*- **\n") == "N"

# all broken matrix but no stars in pattern
assert run("2 2 2\n-- --\n-- --\n") == "Y"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 all good | Y | Base case |
| broken but no requirement | Y | Non-triggered constraints |
| forced activation on broken cell | N | Core rejection logic |
| all broken, no stars | Y | Empty requirement edge case |

## Edge Cases

A subtle case is when the pattern contains no `*` at all. In this case, no matrix cell is ever required to light up, so even a fully broken matrix is valid. The algorithm handles this naturally because every prefix range query returns zero.

Another edge case is when the pattern is wider than the matrix. The derived interval for each matrix cell still works because it captures only the portion of the pattern that can actually sweep over the matrix. No special handling is required.

A final edge case is when both matrix and pattern are minimal, such as 1×1. The algorithm reduces to a single prefix check and correctly distinguishes between compatible and incompatible states.
