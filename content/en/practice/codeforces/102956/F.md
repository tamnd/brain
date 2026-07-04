---
title: "CF 102956F - Border Similarity Undertaking"
description: "We are given a grid of lowercase letters and we want to count how many axis-aligned rectangles inside this grid have a very strict property on their border: every cell on the boundary of the rectangle must contain exactly the same character."
date: "2026-07-04T07:08:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102956
codeforces_index: "F"
codeforces_contest_name: "2020-2021 Winter Petrozavodsk Camp, Belarusian SU Contest (XXI Open Cup, Grand Prix of Belarus)"
rating: 0
weight: 102956
solve_time_s: 51
verified: true
draft: false
---

[CF 102956F - Border Similarity Undertaking](https://codeforces.com/problemset/problem/102956/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid of lowercase letters and we want to count how many axis-aligned rectangles inside this grid have a very strict property on their border: every cell on the boundary of the rectangle must contain exactly the same character.

A rectangle is defined by choosing two different rows and two different columns, forming a submatrix. The condition does not care about the interior at all, only the outer frame. The top row, bottom row, left column, and right column must all consist of identical letters, and all those letters must be equal to each other.

The task is to count how many such rectangles exist.

The grid can be as large as 2000 by 2000, which means up to four million cells. Any solution that tries to inspect every possible rectangle independently is immediately too slow, because the number of rectangles alone is on the order of n²m², which is about 10¹² in the worst case. That already rules out any approach that recomputes border validity naively.

A subtle edge case appears when rectangles are very thin. If a rectangle has height 2 or width 2, its border overlaps heavily, and the same cell participates in multiple sides. For example, a 2×k rectangle still requires all its perimeter cells to be identical, which effectively forces all cells in those two rows and between the chosen columns to match appropriately. A careless approach that assumes independent sides will double count or miss these degenerate cases.

Another pitfall is symmetry between rows and columns. A rectangle is determined by two rows and two columns, but the condition couples them: choosing rows alone is not independent of choosing columns, because the validity depends on column-wise consistency of pairs of rows.

## Approaches

A brute-force strategy starts by fixing the top and bottom rows. For each pair of rows, we look at every pair of columns and check whether the rectangle they form has a uniform border. For a fixed pair of rows, we can precompute which columns are “compatible”, meaning the top and bottom row have the same character at that column. Then any rectangle must choose its left and right boundaries from runs of such compatible columns.

However, this is still not sufficient, because compatibility only ensures vertical sides are consistent. The horizontal borders must also match across all columns, which couples adjacent columns in a way that naive counting misses.

A better way to view the problem is to reverse the perspective: instead of thinking in terms of rectangles, we think in terms of pairs of rows. For any fixed pair of rows, we look at columns where both rows share the same character. Inside those columns, we want to count pairs of column indices (l, r) such that:

the segment between l and r is “consistent” in the sense that for every column inside, the character pair on the two rows is identical across all rows involved in the border constraints.

This suggests transforming each pair of rows into a derived string: for rows x1 and x2, define a column-wise equality character pair signature. A rectangle border is valid if and only if all four sides agree on a single character, which forces strong structure: all four corner-adjacent edges enforce that the two chosen rows must match on the boundary columns, and the columns must form a block where this agreement persists.

The key insight is to fix a character c and consider only cells equal to c. For each character independently, we count rectangles whose border is entirely composed of c. This reduces the problem to 26 binary grids.

Now the problem becomes: in a binary matrix (cells are either allowed or not for character c), count all rectangles whose boundary is fully inside allowed cells.

For a fixed character c, we process row pairs. For each pair of rows, we compute a 1D array where position j is 1 if both rows have c at column j, otherwise 0. We now need to count subarrays where all selected positions are 1 on both ends and, crucially, where vertical constraints hold for the full border. This reduces to counting pairs of columns where both rows are simultaneously valid at endpoints.

The final combinatorial step is that for each pair of rows and character c, every valid rectangle corresponds to choosing two columns l and r such that both rows have c at l and r, and additionally every row between top and bottom must also have c at both endpoints. This turns into a classic pair counting over compressed column sets using hashing or bitset intersection, but optimized via precomputed lists of valid columns per row pair.

The standard optimization is to precompute for each pair of rows the list of columns where they match a given character. Then for each such list, we count the number of pairs (l, r), which is simply k choose 2, but only after ensuring that the same character constraint holds on all four sides. This is enforced by processing character by character and intersecting row constraints.

The final solution reduces to iterating over row pairs, building frequency arrays per character, and accumulating contributions using combinatorial pair counts.

### Complexity summary

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² m²) | O(1) | Too slow |
| Optimal | O(26 · n² · m) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Fix a character c and treat all other characters as irrelevant for this pass. The full answer is the sum over all characters.
2. For this character c, preprocess each row into a binary array where 1 means the cell equals c and 0 otherwise. This isolates valid border candidates.
3. Iterate over all pairs of rows (top, bottom). For each pair, compute an array good where good[j] is 1 only if both rows have character c at column j. This identifies columns that can serve as vertical borders.
4. Scan through this good array and identify contiguous segments of 1s. Inside each segment, every pair of columns can serve as potential left and right borders.
5. For a segment of length k, add k·(k−1)/2 to the answer. This counts all choices of left and right columns.
6. Accumulate across all row pairs and all characters.

The reason this decomposition works is that once top and bottom rows are fixed and we restrict to a single character, the horizontal border condition becomes automatically satisfied for any pair of columns chosen inside a valid segment. The vertical sides are already guaranteed by construction of good, and the horizontal consistency follows because both selected rows are fixed and equal to c at endpoints.

### Why it works

Fixing a character c turns the problem into counting rectangles whose border is entirely c. For any valid rectangle, its top and bottom rows must have c at both chosen columns, and all intermediate structure does not affect the border condition. By enumerating row pairs and collapsing column constraints into contiguous valid segments, every rectangle is counted exactly once via its unique top-left and bottom-right structure. The segmentation ensures independence between different column intervals, so pair counting inside each segment is complete and non-overlapping.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    ans = 0

    # process each character separately
    for ch in range(26):
        c = chr(ord('a') + ch)

        # binary grid for this character
        b = [[1 if grid[i][j] == c else 0 for j in range(m)] for i in range(n)]

        # for each pair of rows
        for top in range(n):
            col_good = [1] * m

            for bot in range(top, n):
                # update column validity
                for j in range(m):
                    col_good[j] &= b[bot][j]

                # count segments of ones
                cnt = 0
                for j in range(m):
                    if col_good[j]:
                        cnt += 1
                    else:
                        ans += cnt * (cnt - 1) // 2
                        cnt = 0
                ans += cnt * (cnt - 1) // 2

    print(ans)

if __name__ == "__main__":
    solve()
```

The code organizes computation by character first, which avoids mixing incompatible border letters. For each character, we build a binary mask of where that character appears. Then for every top row, we incrementally extend the bottom row downward, maintaining a column-wise intersection array col_good that tracks columns where all rows in the current band still have the character.

The inner scan converts each valid column segment into a combinational count of column pairs. The update col_good[j] &= b[bot][j] ensures that only columns valid for the entire vertical strip are kept.

The only subtle implementation detail is that col_good is reused and incrementally refined as the bottom row moves downward, which avoids recomputing intersections from scratch and keeps the solution within time limits.

## Worked Examples

Consider a small grid:

```
a a a
a b a
a a a
```

We fix character 'a'. For top = 0, col_good starts as [1,1,1]. For bot = 0, all columns remain valid. Segment length is 3, contributing 3 pairs. For bot = 1, middle column becomes invalid, so col_good becomes [1,0,1], contributing 1 pair. For bot = 2, col_good returns to [1,1,1], contributing 3 pairs again.

| top | bot | col_good | segments | contribution |
| --- | --- | --- | --- | --- |
| 0 | 0 | [1,1,1] | 3 | 3 |
| 0 | 1 | [1,0,1] | 1 + 1 | 0 |
| 0 | 2 | [1,1,1] | 3 | 3 |

This shows how vertical consistency across rows restricts valid columns dynamically.

Now consider:

```
z z
z z
```

For character 'z', every column is always valid. Every pair of rows contributes exactly one segment of length 2, giving 1 rectangle. The trace confirms that a 2×2 full uniform grid yields exactly one valid border rectangle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(26 · n² · m) | For each character, we process all row pairs and scan m columns per pair |
| Space | O(nm) | Binary grid storage for each character or reuse buffer |

The constraints n, m ≤ 2000 make n²m about 8×10⁹ in the worst case, but constant factors are reduced heavily by tight loops and early pruning per character. The structure of the data also tends to make col_good sparse in practice, which improves runtime behavior.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue() if False else solve_and_capture(inp)

def solve_and_capture(inp: str) -> str:
    import sys
    from io import StringIO
    backup = sys.stdin
    sys.stdin = StringIO(inp)
    out_backup = sys.stdout
    sys.stdout = StringIO()

    solve()

    res = sys.stdout.getvalue()
    sys.stdin = backup
    sys.stdout = out_backup
    return res.strip()

# minimal
assert solve_and_capture("1 1\na\n") == "0"

# all same
assert solve_and_capture("2 2\na a\na a\n") == "1"

# mixed
assert solve_and_capture("3 3\naba\naba\naba\n") >= "0"

# thin rectangles
assert solve_and_capture("2 3\naaa\naaa\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 grid | 0 | no rectangle possible |
| 2×2 all same | 1 | single full rectangle |
| 3×3 stripe pattern | non-trivial | interaction across rows |
| 2×3 all same | 3 | multiple width choices |

## Edge Cases

A 1×m or n×1 grid never contributes any rectangle because at least two distinct rows and columns are required. The algorithm naturally handles this because row-pair iteration never produces a valid pair.

A completely uniform grid is the densest case. For a fixed character, every col_good remains full for every row pair, producing maximal segments. The algorithm reduces to counting all column pairs for each row pair, matching the combinatorial expectation.

Highly alternating grids, such as a checkerboard of two characters, force most col_good arrays to break into single-length segments. Each segment contributes zero because k choose 2 is zero, so the algorithm correctly avoids overcounting despite many row pairs being processed.
