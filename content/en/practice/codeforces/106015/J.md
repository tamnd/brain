---
title: "CF 106015J - Halzoom's Coffee Grid"
description: "The grid represents a field of values, where each cell contains a non-negative number describing a “smell strength”."
date: "2026-06-22T16:48:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106015
codeforces_index: "J"
codeforces_contest_name: "Game of Coders 4 - Over the Garden Wall"
rating: 0
weight: 106015
solve_time_s: 66
verified: true
draft: false
---

[CF 106015J - Halzoom's Coffee Grid](https://codeforces.com/problemset/problem/106015/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

The grid represents a field of values, where each cell contains a non-negative number describing a “smell strength”. The task is not to find a single best rectangle, but to inspect every possible subrectangle of the grid and check whether its total sum equals a given target value k.

Every time such a rectangle exists, all cells inside it become “important”. In the final output, a cell is preserved if it belongs to at least one valid rectangle whose sum is exactly k. If it never appears in any such rectangle, it is replaced by zero.

The key difficulty is that rectangles overlap heavily, so a single cell may be validated by many different choices of top-left and bottom-right corners.

The constraints n, m ≤ 100 are small enough that quadratic or cubic methods in each dimension might pass, but anything approaching enumerating all rectangles directly becomes too slow. The grid size allows around 10^8 cells in total work only if each operation is extremely cheap and well optimized, otherwise it will time out in Python.

A naive idea would be to compute the sum of every possible rectangle using prefix sums and then mark cells, but that leads to four nested loops over n and m, producing around 10^8 rectangles, and for each rectangle we would still need to mark its area, which makes it far beyond feasible limits.

A second subtle issue appears when k equals zero. Since all values are non-negative, valid rectangles in this case are formed entirely of zeros. Any solution relying on shrinking or expanding windows must handle long zero segments carefully, otherwise it may miss valid subarrays or overcount them.

## Approaches

The brute-force method is to enumerate all pairs of top and bottom rows, all pairs of left and right columns, compute the sum of the rectangle using a precomputed prefix sum table, and if it matches k, mark all cells in that rectangle.

Even with prefix sums allowing O(1) rectangle sum queries, the number of rectangles is still O(n^2 m^2). With n = m = 100, this is 10^8 rectangles. Since each successful rectangle requires additional marking work over potentially O(nm) cells in the worst case, the total cost quickly becomes infeasible.

The key observation is that we do not actually need to inspect arbitrary 2D rectangles directly. If we fix the top and bottom rows, the problem collapses into a one-dimensional problem over columns. For each column, we accumulate the sum between these two rows, producing a compressed array. Every valid rectangle between these rows is now just a contiguous subarray whose sum equals k.

Because all numbers in the grid are non-negative, this 1D subarray problem can be solved efficiently using a two-pointer sliding window. This avoids hashing or prefix sum lookup per pair and reduces each row-pair computation to linear time in m.

Once we find all valid subarrays for a fixed pair of rows, we still need to mark entire rectangles efficiently. Directly filling every cell per rectangle would reintroduce a cubic factor. Instead, we store updates in a 2D difference array so each rectangle contributes in O(1), and a final prefix sum reconstruction determines which cells were ever covered.

This transforms the problem from enumerating rectangles explicitly to enumerating row bands and finding valid column intervals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over all rectangles | O(n^2 m^2 (n+m)) | O(1) | Too slow |
| Fix rows + prefix sums | O(n^2 m^2) | O(nm) | Borderline too slow |
| Fix rows + sliding window + 2D diff | O(n^2 m) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Fix a top row index and gradually extend a bottom row index downward. For each extension, maintain a running column-wise sum of values between the two rows. This compresses the 2D grid into a 1D array representing vertical sums for the current band.
2. For the current row band, search for all contiguous subarrays in this 1D array whose sum equals k using a sliding window. Since all values are non-negative, expanding the right pointer increases the sum and shrinking the left pointer decreases it, guaranteeing linear behavior.
3. Every time a subarray with sum k is found, interpret it as a rectangle spanning from the current top row to bottom row and from left column l to right column r.
4. Instead of marking every cell in that rectangle directly, apply a 2D difference update so the rectangle is recorded in constant time. This ensures that even if a rectangle is large, its contribution is still O(1).
5. After processing all row pairs and all valid column intervals, convert the difference array into a prefix sum grid. Each cell in this final grid indicates how many valid rectangles include it.
6. Produce the final answer by keeping original grid values for cells with positive coverage and setting others to zero.

The correctness hinges on the fact that every rectangle is uniquely determined by a pair of rows and a valid subarray in the compressed column representation. The sliding window enumerates all such subarrays exactly once for each row pair, and the difference array guarantees that all cells in each rectangle are consistently marked without omission or duplication affecting correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]

    diff = [[0] * (m + 1) for _ in range(n + 1)]

    for top in range(n):
        col_sum = [0] * m

        for bot in range(top, n):
            for j in range(m):
                col_sum[j] += a[bot][j]

            l = 0
            cur = 0

            for r in range(m):
                cur += col_sum[r]

                while l <= r and cur > k:
                    cur -= col_sum[l]
                    l += 1

                if cur == k:
                    diff[top][l] += 1
                    diff[top][r + 1] -= 1
                    diff[bot + 1][l] -= 1
                    diff[bot + 1][r + 1] += 1

    for i in range(n):
        for j in range(m):
            diff[i][j] += diff[i - 1][j] if i > 0 else 0
    for i in range(n):
        for j in range(m):
            diff[i][j] += diff[i][j - 1] if j > 0 else 0

    out = []
    for i in range(n):
        row = []
        for j in range(m):
            if diff[i][j] > 0:
                row.append(str(a[i][j]))
            else:
                row.append("0")
        out.append(" ".join(row))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution maintains a dynamic column-sum array for each pair of rows, then uses a sliding window to enumerate all valid column intervals. Each interval is converted into a rectangle update using a 2D difference structure. The final double prefix sum reconstructs coverage counts, and the output step simply filters the original grid based on whether a cell was ever included in any valid rectangle.

A subtle point is that the sliding window only works because all grid values are non-negative. If negative values were allowed, the monotonicity required for shrinking and expanding the window would break, and a hash-based prefix sum approach would be necessary instead.

The difference array also avoids the common mistake of trying to directly paint rectangles. Without it, the solution would degrade to updating O(nm) cells per rectangle, which is too slow.

## Worked Examples

Consider a small grid where valid rectangles exist only in a few regions. We track a single row band and the resulting column compression.

For a fixed pair of rows, suppose the compressed array becomes [1, 0, 1, 3].

We track the sliding window:

| r | col_sum[r] | cur_sum | l | action |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 0 | expand |
| 1 | 0 | 1 | 0 | expand |
| 2 | 1 | 2 | 0 | expand |
| 3 | 3 | 5 | 0 | shrink l=1 |
| 3 | 3 | 5 | 1 | shrink l=2 |
| 3 | 3 | 3 | 2 | match |

At r = 3, we detect a valid subarray [2,3] when k = 3. This produces a rectangle covering rows top..bot and columns 2..3.

This trace shows that even when zeros appear in the array, the window correctly preserves valid sums and does not skip potential matches.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n² m) | There are O(n²) row pairs, and each processes columns in O(m) using a sliding window |
| Space | O(nm) | Used for grid storage and the 2D difference array |

With n, m ≤ 100, the total operations are around 10^6, which fits comfortably within time limits in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout
    return out

# sample
assert run("""5 5 5
1 1 1 1 5
1 7 1 1 1
1 1 1 1 1
1 1 1 1 1
1 1 1 1 5
""") == """1 0 1 1 5
1 0 1 1 0
1 1 1 1 1
1 1 1 1 1
1 0 1 1 5"""

# all zeros, k=0
assert run("""2 3 0
0 0 0
0 0 0
""") == """0 0 0
0 0 0"""

# no valid rectangles
assert run("""2 2 10
1 1
1 1
""") == """0 0
0 0"""

# single row
assert run("""1 5 3
1 1 1 0 0
""") == """1 1 1 0 0"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all zeros | all zeros | k=0 behavior and zero handling |
| no solution | all zero grid | absence of valid rectangles |
| single row | partial prefix kept | 1D reduction correctness |

## Edge Cases

When k equals zero, every valid rectangle must consist entirely of zeros. The sliding window still behaves correctly because the sum starts at zero and only expands when encountering positive values. For an input like a row of zeros, every subarray is valid, and the difference array marks the full grid, which is correct since every cell lies in some zero-sum rectangle.

For grids with isolated non-zero spikes, only rectangles that perfectly balance to k will be detected. Since the sliding window shrinks whenever the sum exceeds k, it avoids falsely extending rectangles beyond valid boundaries, even when large values appear in the middle of a row band.

Small grids such as 1x1 are naturally handled because the row-pair loop degenerates into a single iteration and the sliding window directly evaluates the only possible subarray.
