---
title: "CF 103447J - Local Minimum"
description: "We are given a rectangular grid of numbers. For each cell, we look at all values that lie either in the same row or in the same column as that cell, including the cell itself. Among all those values, we check whether the current cell’s value is the smallest."
date: "2026-07-03T07:32:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103447
codeforces_index: "J"
codeforces_contest_name: "The 2021 China Collegiate Programming Contest (Harbin)"
rating: 0
weight: 103447
solve_time_s: 40
verified: true
draft: false
---

[CF 103447J - Local Minimum](https://codeforces.com/problemset/problem/103447/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular grid of numbers. For each cell, we look at all values that lie either in the same row or in the same column as that cell, including the cell itself. Among all those values, we check whether the current cell’s value is the smallest. The task is to count how many cells satisfy this condition.

Another way to think about it is that every cell defines a “cross” made of its row and column. We take the minimum value inside that cross, and we want to count how many cells are equal to that minimum.

The grid size can be as large as 1000 by 1000, which gives up to one million cells. Any solution that inspects each cell by scanning its entire row and column directly would potentially do about 2n or 2m work per cell, leading to roughly 10^12 operations in the worst case. That is far beyond what fits into a one second limit.

A subtle edge case comes from repeated minimum values inside a row or column. For example, if a row is `1 2 1`, both cells containing `1` are candidates from the row perspective, but one of them might fail when considering its column.

Another tricky situation is when the row minimum and column minimum disagree. A cell might be the minimum in its row but not in its column, or vice versa, so we must always consider the union of both constraints correctly.

## Approaches

The naive idea is straightforward. For each cell `(i, j)`, we scan the entire row `i` to find the minimum value, and we also scan the entire column `j` to find the minimum value. Then we compare the cell value with the minimum of these two results. If they match, we count it.

This is correct because the minimum over the union of row and column is simply the minimum of the row minimum and column minimum. However, recomputing these minima for every cell is wasteful. Each row scan costs O(m), each column scan costs O(n), and doing this for all n·m cells leads to O(n·m·(n+m)), which in the worst case is about 2×10^9 to 2×10^12 operations depending on constants, which is too slow.

The key observation is that row minima and column minima do not depend on the query cell. They depend only on the grid structure. So we can precompute the minimum value for each row and each column once. After that, each cell can be checked in constant time by comparing it with the smaller of its row minimum and column minimum.

This reduces the problem to a single pass over the grid after preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·m·(n+m)) | O(1) | Too slow |
| Optimal | O(n·m) | O(n+m) | Accepted |

## Algorithm Walkthrough

We first compute two auxiliary arrays, one storing the minimum value of each row and one storing the minimum value of each column.

1. Initialize an array `rowMin` of size `n`, filled with very large values. This will store the smallest value seen in each row.
2. Initialize an array `colMin` of size `m`, also filled with very large values. This will store the smallest value seen in each column.
3. Scan the entire matrix once. For each cell `(i, j)`, update `rowMin[i] = min(rowMin[i], a[i][j])` and `colMin[j] = min(colMin[j], a[i][j])`. This step builds exact minima for every row and column in linear time over all cells.
4. After preprocessing, scan the matrix again. For each cell `(i, j)`, compute `t = min(rowMin[i], colMin[j])`. If `a[i][j] == t`, increment the answer.
5. Output the final count.

The reason we take `min(rowMin[i], colMin[j])` is that the union of values in row `i` and column `j` has its minimum either in the row or in the column. There is no other source for a smaller value, since every element is already accounted for in one of these two sets.

### Why it works

For any cell `(i, j)`, every value considered in its cross belongs either to row `i` or column `j`. The minimum over that union must be either the smallest element in row `i` or the smallest element in column `j`, whichever is smaller. The preprocessing step ensures these values are correct globally. Therefore, comparing `a[i][j]` with `min(rowMin[i], colMin[j])` exactly checks whether the cell achieves the minimum in its cross, and no cell can be incorrectly classified.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]
    
    INF = 10**18
    rowMin = [INF] * n
    colMin = [INF] * m

    for i in range(n):
        for j in range(m):
            v = a[i][j]
            if v < rowMin[i]:
                rowMin[i] = v
            if v < colMin[j]:
                colMin[j] = v

    ans = 0
    for i in range(n):
        for j in range(m):
            if a[i][j] == min(rowMin[i], colMin[j]):
                ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by reading the grid into memory, which is necessary because we need two passes over the data. The first pass constructs row and column minima independently. This avoids any repeated scanning later.

The second pass performs the actual condition check. The expression `min(rowMin[i], colMin[j])` is computed in O(1), so each cell contributes constant work. This is the step that replaces the expensive brute-force search.

A common implementation mistake is trying to recompute row or column minima inside the second loop. That would silently reintroduce an extra factor of n or m and break performance.

## Worked Examples

Consider the sample matrix:

```
3 3
1 5 9
4 3 7
2 6 2
```

First we compute row and column minima.

| Step | Row/Col | Index | Value | Updated State |
| --- | --- | --- | --- | --- |
| scan | rowMin | 0 | 1 | [1, inf, inf] |
| scan | rowMin | 1 | 3 | [1, 3, inf] |
| scan | rowMin | 2 | 2 | [1, 3, 2] |
| scan | colMin | 0 | 1 | [1, inf, inf] |
| scan | colMin | 1 | 5 | [1, 3, inf] |
| scan | colMin | 2 | 9 | [1, 3, 2] |

Now evaluate each cell:

| Cell | Value | min(rowMin[i], colMin[j]) | Match? |
| --- | --- | --- | --- |
| (0,0) | 1 | 1 | yes |
| (0,1) | 5 | 3 | no |
| (0,2) | 9 | 2 | no |
| (1,0) | 4 | 1 | no |
| (1,1) | 3 | 3 | yes |
| (1,2) | 7 | 2 | no |
| (2,0) | 2 | 1 | no |
| (2,1) | 6 | 3 | no |
| (2,2) | 2 | 2 | yes |

The answer is 3.

This trace shows how row and column constraints interact independently. Each qualifying cell exactly matches the best achievable value in its cross.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n·m) | Each cell is processed a constant number of times across two passes |
| Space | O(n+m) | Storage for row minima and column minima |

The grid size is at most one million cells, so a linear scan over all entries is comfortably within time limits. The memory footprint is dominated by storing the matrix and two auxiliary arrays, which is well under the 512 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]
    
    INF = 10**18
    rowMin = [INF] * n
    colMin = [INF] * m

    for i in range(n):
        for j in range(m):
            v = a[i][j]
            rowMin[i] = min(rowMin[i], v)
            colMin[j] = min(colMin[j], v)

    ans = 0
    for i in range(n):
        for j in range(m):
            if a[i][j] == min(rowMin[i], colMin[j]):
                ans += 1

    return str(ans)

# provided sample
assert run("""3 3
1 5 9
4 3 7
2 6 2
""") == "3"

# minimum size
assert run("""1 1
5
""") == "1"

# all equal
assert run("""2 3
7 7 7
7 7 7
""") == "6"

# row dominance
assert run("""2 2
1 100
100 100
""") == "2"

# column dominance
assert run("""2 2
1 2
100 2
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 grid | 1 | base correctness |
| all equal matrix | 6 | every cell qualifies |
| row-heavy matrix | 2 | row minima dominate |
| column-heavy matrix | 2 | column minima dominate |

## Edge Cases

A 1×1 grid is the simplest boundary. The row and column are the same single element, so both minima equal the value, and the single cell must be counted. The algorithm initializes `rowMin[0]` and `colMin[0]` to that value, and the final check passes immediately.

In a uniform matrix where every entry is identical, every row minimum and column minimum is the same value. For any cell `(i, j)`, `min(rowMin[i], colMin[j])` equals the cell value, so all entries are counted. The second pass correctly increments for every position without exception.

In cases where one row contains a very small value while columns do not, the row minimum dominates most comparisons. The algorithm still works because it always recomputes the correct global row and column minima before evaluation, ensuring no dependency on local structure or traversal order.
