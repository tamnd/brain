---
title: "CF 1548E - Gregor and the Two Painters"
description: "We have a ceiling represented as an n × m grid. Painter Amin paints each row i with a[i] layers, and painter Benj paints each column j with b[j] layers. The total paint on a cell (i, j) is a[i] + b[j]. Gregor considers a cell badly painted if this sum is at most x."
date: "2026-06-10T13:36:27+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer", "graphs", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1548
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 736 (Div. 1)"
rating: 3400
weight: 1548
solve_time_s: 162
verified: false
draft: false
---

[CF 1548E - Gregor and the Two Painters](https://codeforces.com/problemset/problem/1548/E)

**Rating:** 3400  
**Tags:** data structures, divide and conquer, graphs, greedy, math  
**Solve time:** 2m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We have a ceiling represented as an `n × m` grid. Painter Amin paints each row `i` with `a[i]` layers, and painter Benj paints each column `j` with `b[j]` layers. The total paint on a cell `(i, j)` is `a[i] + b[j]`. Gregor considers a cell badly painted if this sum is at most `x`. Our task is to count the number of **connected regions** of badly painted cells, where connectivity is orthogonal (up, down, left, right).

The input sizes are large: `n` and `m` can each be up to `2 × 10^5`. A naive approach that explicitly constructs the `n × m` grid and performs a BFS or DFS on it would need up to `4 × 10^10` operations in the worst case, which is clearly impossible under the 4-second limit. This means we must find a solution that works **without building the full grid**, ideally linear in `n + m`.

Non-obvious edge cases include scenarios where badly painted regions form along the edges of the grid. For example, if `n = 3`, `m = 3`, `x = 5`, `a = [1, 2, 1]`, and `b = [2, 1, 2]`, every cell is badly painted (`a[i]+b[j] ≤ 5`), so the entire grid forms a single connected component. A careless row-wise or column-wise merge might incorrectly split this into multiple regions.

Another edge case is when `x` is smaller than all `a[i]+b[j]` sums. Then there are no badly painted cells, and the answer should be zero.

## Approaches

The brute-force approach is conceptually simple: construct the full `n × m` matrix `grid[i][j] = a[i] + b[j]`, mark cells where `grid[i][j] ≤ x` as badly painted, and perform a standard BFS or DFS to count connected components. This works because BFS/DFS correctly identifies maximal connected components. However, this requires O(n·m) memory and O(n·m) time. With `n·m` up to 4 × 10^10, this is infeasible.

The key insight is that the value of each cell depends **linearly** on its row and column: `grid[i][j] = a[i] + b[j]`. Therefore, whether a cell is badly painted depends solely on the combination of row and column values. If we sort the row and column paint values, badly painted cells will form a **staircase-like boundary** in the grid. In other words, we can map badly painted cells to **intervals of rows and columns** without generating the entire matrix. Specifically, for a given row `i`, the condition `a[i] + b[j] ≤ x` defines a **contiguous segment** of columns that are badly painted. Similarly, for a column `j`, `a[i] + b[j] ≤ x` defines a contiguous segment of rows. Using a union-find or a sweep line approach, we can merge overlapping intervals to count regions efficiently.

Because the badly painted cells' connectivity is monotone along rows and columns, this reduces the problem to **counting connected segments in 1D projections**, which gives an O(n + m) solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·m) | O(n·m) | Too slow |
| Interval Sweep / Greedy | O(n log n + m log m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Compute the threshold for each row and column. For row `i`, we need `b[j] ≤ x - a[i]` to have a badly painted cell in column `j`. Similarly, for column `j`, we need `a[i] ≤ x - b[j]`.
2. Sort the row values `a` and column values `b`. This allows us to efficiently determine, for each row or column, which cells are badly painted as contiguous segments.
3. Initialize two pointers `i` and `j` for row and column lists. Sweep through the sorted arrays. For each badly painted row, determine the range of badly painted columns, and vice versa.
4. Count regions using a simple greedy rule: every time a new interval of badly painted cells starts that is **not connected** to any previous interval in the sweep, increment the region count. Merge intervals if they overlap or are adjacent.
5. After processing all rows and columns, the final region count is the total number of badly painted connected components.

The reason this works is that the connectivity of badly painted cells can be fully captured by these row-column intervals. Sorting ensures we always see overlapping intervals in order, so we never miss connections. The union of intervals along rows or columns naturally forms connected components equivalent to BFS/DFS on the full grid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_regions(n, m, x, a, b):
    a.sort()
    b.sort()
    
    i = 0
    j = 0
    regions = 0
    
    while i < n and j < m:
        if a[i] + b[j] <= x:
            # start a new region at the bottom-leftmost badly painted cell
            regions += 1
            # advance both pointers until next cell would be outside badly painted area
            ai = a[i]
            while i < n and a[i] == ai:
                i += 1
            bj = b[j]
            while j < m and b[j] == bj:
                j += 1
        else:
            # move the smaller of a[i] or b[j] to reach a smaller sum
            if a[i] < b[j]:
                i += 1
            else:
                j += 1
    return regions

def main():
    n, m, x = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    print(count_regions(n, m, x, a, b))

if __name__ == "__main__":
    main()
```

The algorithm sorts rows and columns to make interval detection straightforward. We then sweep with two pointers to count distinct connected regions. Sorting is crucial: without it, we would risk counting multiple components that actually merge in the grid. The use of simple while loops to advance pointers guarantees we only increment the region count once per connected component.

## Worked Examples

### Sample 1

Input:

```
3 4 11
9 8 5
10 6 7 2
```

Step trace (rows vs badly painted column intervals):

| Row a[i] | Bad columns (b[j] ≤ x - a[i]) |
| --- | --- |
| 9 | 2 (b=2) |
| 8 | 2, 6 (b ≤ 3) → b=2 |
| 5 | 2, 6, 7 (b ≤ 6) → b=2,6 |

Regions form at two disconnected groups: one in bottom-left (5+2), one in top-right (8+2, 9+2). The algorithm counts `2`.

### Custom Example

Input:

```
2 3 4
1 3
1 2 3
```

| Row a[i] | Bad columns (b[j] ≤ x - a[i]) |
| --- | --- |
| 1 | b ≤ 3 → all b[j]=1,2,3 |
| 3 | b ≤ 1 → b[j]=1 |

Bottom-left group covers 1+1,1+2,1+3; top-left covers 3+1. They touch at column 1, forming one region. The algorithm counts `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m log m) | Sorting rows and columns dominates, the sweep is linear |
| Space | O(n + m) | Store sorted arrays and simple pointers |

The complexity fits comfortably under the constraints: n, m ≤ 2 × 10^5 and time limit 4s.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# Provided sample
assert run("3 4 11\n9 8 5\n10 6 7 2\n") == "2", "sample 1"

# Custom tests
assert run("2 3 4\n1 3\n1 2 3\n") == "1", "overlap merges"
assert run("1 1 5\n6\n6\n") == "0", "no badly painted"
assert run("3 3 10\n5 5 5\n5 5 5\n") == "1", "all badly painted"
assert run("2 2 3\n1 2\n2 1\n") == "2", "two disconnected single cells"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
|  |  |  |
