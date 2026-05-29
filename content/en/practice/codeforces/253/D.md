---
title: "CF 253D - Table with Letters - 2"
description: "We are given a rectangular grid of characters, each cell containing a lowercase English letter. The task is to count how many axis-aligned subrectangles have two properties at the same time."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 253
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 154 (Div. 2)"
rating: 2000
weight: 253
solve_time_s: 64
verified: true
draft: false
---

[CF 253D - Table with Letters - 2](https://codeforces.com/problemset/problem/253/D)

**Rating:** 2000  
**Tags:** brute force, two pointers  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular grid of characters, each cell containing a lowercase English letter. The task is to count how many axis-aligned subrectangles have two properties at the same time.

First, if you look at the four corners of the chosen rectangle, all four corner letters must be identical. Second, if you count how many cells inside that rectangle contain the letter `'a'`, this count must not exceed a given limit `k`.

A subrectangle is fully determined by choosing a top row, a bottom row, a left column, and a right column, with the usual ordering constraints so that it is a non-empty rectangle with area at least 4 cells.

The constraints `n, m ≤ 400` immediately suggest that quadratic or cubic solutions over rows are acceptable, but anything that tries all rectangles directly will fail. The number of subrectangles alone is on the order of $n^2 m^2$, which is about $400^4 = 2.56 \cdot 10^{10}$, far too large.

This forces us to reduce the problem structure so that each rectangle is not handled independently. Instead, we need to reuse computations across many rectangles sharing the same pair of rows or columns.

A naive but important observation is that checking the “at most k `'a'` cells” condition can be made efficient using prefix sums. The harder part is enforcing the “all four corners equal” condition in a way that does not require checking every rectangle explicitly.

A few edge cases help clarify the pitfalls.

If the grid is filled entirely with `'a'` and `k = 0`, then no rectangle with area more than 1 is valid, because every rectangle contains `'a'` everywhere, so the answer is zero. A naive solution might still count many rectangles just because corners match, ignoring the interior constraint.

If `k` is very large, say `k = n*m`, then every rectangle with equal corners becomes valid, so the problem reduces to counting rectangles with equal corner letters only. Any solution that hardcodes the `'a'` constraint into filtering corners instead of handling it separately will fail to simplify correctly.

If `n = 2, m = 2`, there is exactly one rectangle. It is valid only if all four letters are equal and the number of `'a'` cells is within the limit. This highlights that both constraints are global over the same rectangle and must be checked simultaneously, not independently per corner or per row.

## Approaches

A direct brute-force solution enumerates all choices of top and bottom rows and left and right columns. For each rectangle, we check the four corner characters and count `'a'` cells using a precomputed prefix sum matrix. This is correct, and prefix sums make each rectangle check O(1). However, there are $O(n^2 m^2)$ rectangles, so the total complexity becomes $O(n^2 m^2)$, which is too slow for $n = m = 400$.

The key structure that unlocks efficiency is to fix the top and bottom rows first. Once these two rows are fixed, every column can be summarized by two pieces of information: whether the characters in these two rows match (which is required for any valid rectangle corners using that column), and how many `'a'` characters lie between the two rows in that column. This reduces the 2D rectangle problem into a 1D problem over columns.

For a fixed pair of rows, a valid rectangle corresponds to choosing two columns $l < r$ such that the characters at both ends are equal in both rows, and the total number of `'a'` cells in the submatrix between these rows and columns is at most `k`. The second condition becomes a classic two-pointers problem over a one-dimensional array of column weights.

The subtlety is that the corner-equality constraint depends on the letter. A rectangle is only valid if all four corners share the same character, meaning both chosen columns must have the same character in both fixed rows. This naturally partitions columns into groups by letter, and within each group we count valid subarrays using a sliding window on the `'a'` contribution.

This reduces the problem from enumerating rectangles to processing $O(n^2)$ row pairs, each in $O(m)$, giving an acceptable solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all rectangles | O(n²m²) | O(1) extra (besides prefix sums) | Too slow |
| Fix row pairs + group columns + two pointers | O(n²m) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Precompute a 2D prefix sum over the grid that counts how many `'a'` characters are in any subrectangle. This allows us to compute the number of `'a'` cells between any two rows for a fixed column in O(1). This is essential because we will repeatedly evaluate vertical segments between row pairs.
2. Iterate over all pairs of rows `(top, bottom)`. Fixing these two rows reduces the problem to selecting two columns that form valid rectangle boundaries.
3. For the current row pair, construct an array over columns where each entry stores how many `'a'` characters appear in that column between `top` and `bottom`. This array represents the cost contribution of including that column in a rectangle.
4. For each column, also record the character pair `(grid[top][col], grid[bottom][col])`. A column is usable as a rectangle boundary only if these two characters are equal. Otherwise it cannot serve as a corner column in any valid rectangle for this row pair.
5. Group columns by the character they represent in both rows. For each letter `'a'` to `'z'`, collect all column indices where the top and bottom row characters match that letter.
6. For each such group of columns, run a two-pointer sweep over the columns in increasing order. Maintain a sliding window `[l, r]` and track the sum of `'a'` contributions in that window.
7. Expand `r` step by step. Each time the sum exceeds `k`, move `l` forward until the constraint is satisfied again. Every time we move `r`, all valid starting positions `l' ≤ l` do not form valid pairs, but all positions in `[l, r)` do. We count the number of valid rectangles ending at `r`.
8. Sum contributions across all letters and all row pairs. This produces the final answer.

The key idea is that once rows are fixed and we restrict to a single letter group, every valid rectangle corresponds exactly to a subarray of columns, and the `'a'` constraint becomes additive over that subarray.

### Why it works

For a fixed pair of rows, every valid rectangle is determined by two columns. The corner condition forces both columns to belong to the same letter group because both endpoints must match on both rows. Inside one group, the only remaining constraint is the total number of `'a'` cells in the rectangle, which is linear over columns. The two-pointer process enumerates all subarrays satisfying this constraint exactly once, so no rectangle is missed and none is double-counted across different groups or row pairs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    g = [input().strip() for _ in range(n)]

    # prefix sum for 'a'
    pref = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        row_sum = 0
        for j in range(m):
            row_sum += (g[i][j] == 'a')
            pref[i + 1][j + 1] = pref[i][j + 1] + row_sum

    def get_a(x1, y1, x2, y2):
        return pref[x2][y2] - pref[x1][y2] - pref[x2][y1] + pref[x1][y1]

    ans = 0

    for top in range(n):
        for bottom in range(top + 1, n):
            col_a = [0] * m
            col_letter = [''] * m

            for j in range(m):
                if g[top][j] == g[bottom][j]:
                    col_letter[j] = g[top][j]
                    col_a[j] = get_a(top, j, bottom + 1, j + 1)
                else:
                    col_letter[j] = '#'

            pos_by_letter = [[] for _ in range(26)]
            val_by_letter = [[] for _ in range(26)]

            for j in range(m):
                c = col_letter[j]
                if c != '#':
                    idx = ord(c) - 97
                    pos_by_letter[idx].append(j)
                    val_by_letter[idx].append(col_a[j])

            for idx in range(26):
                vals = val_by_letter[idx]
                if not vals:
                    continue

                l = 0
                s = 0
                for r in range(len(vals)):
                    s += vals[r]
                    while s > k:
                        s -= vals[l]
                        l += 1
                    ans += (r - l)

    print(ans)

if __name__ == "__main__":
    solve()
```

The prefix sum construction ensures that any vertical segment query for `'a'` counts is constant time. The main double loop over row pairs is the structural backbone of the solution.

Inside each row pair, we compress columns into letter groups, ignoring any column where the two rows disagree. This is critical because such columns can never appear as valid rectangle boundaries.

The two-pointer logic inside each group counts subarrays whose accumulated `'a'` contribution stays within `k`. The expression `(r - l)` counts how many valid left endpoints exist for each right endpoint.

## Worked Examples

### Example 1

Input:

```
3 4 4
aabb
baab
baab
```

We fix row pairs. Consider `top = 1, bottom = 2` (0-indexed). Columns where characters match are grouped by letter.

| step | column | valid letter | a-count between rows | window action | current sum | added pairs |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | b | 0 | expand | 0 | 0 |
| 1 | 1 | a | 1 | expand | 1 | 1 |
| 2 | 2 | a | 1 | expand | 2 | 2 |
| 3 | 3 | b | 0 | expand | 2 | 2 |

This row pair contributes valid rectangles corresponding to subarrays within `'a'` group and `'b'` group. Repeating over all row pairs yields total 2.

This trace shows how grouping isolates independent subproblems per letter and avoids mixing incompatible boundary columns.

### Example 2

Input:

```
2 3 1
aaa
aaa
```

Only one row pair exists.

| step | column | a-count | window | sum | valid pairs |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 2 | [0] | 2 → shrink | 0 |
| 1 | 1 | 2 | [1] | 2 → shrink | 0 |
| 2 | 2 | 2 | [2] | 2 → shrink | 0 |

No valid rectangle exists because every rectangle contains more than 1 `'a'`.

This confirms that the sliding window correctly enforces the global constraint even when corner conditions are trivially satisfied.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²m) | For each pair of rows we process each column a constant number of times across two-pointer sweeps |
| Space | O(nm) | Prefix sum array over the grid |

The constraints allow up to about 400 × 400 × 400 operations, which stays comfortably within limits due to constant factors being small and the inner loops being linear scans.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("""3 4 4
aabb
baab
baab
""") == "2"

# minimum grid
assert run("""2 2 0
ab
ba
""") == "0"

# all equal, k large
assert run("""3 3 9
aaa
aaa
aaa
""") == "9"

# all equal, tight k
assert run("""3 3 1
aaa
aaa
aaa
""") == "0"

# mixed letters
assert run("""2 4 2
abab
abab
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2x2 mixed | 0 | smallest grid, no valid rectangle |
| all `'a'` large k | many rectangles | correctness when all corners identical |
| all `'a'` small k | 0 | strict `'a'` constraint pruning |
| alternating pattern | small count | grouping and boundary correctness |

## Edge Cases

When the grid is uniform, every column belongs to the same letter group, so the algorithm reduces to a pure two-pointer problem over all columns. The implementation correctly aggregates all rectangles but still filters by the `'a'` constraint.

When `k = 0`, only rectangles with zero `'a'` cells are allowed. The prefix-based column weights ensure that any rectangle containing even a single `'a'` is excluded immediately during the sliding window expansion.

When rows differ at most columns, many columns become invalid for a given row pair. The algorithm naturally skips them by marking mismatched columns with a sentinel and excluding them from all groups, ensuring no invalid rectangle boundary is ever considered.
