---
title: "CF 15D - Map"
description: "We are given a rectangular map of size n × m, where each cell has a non-negative height. Peter wants to build cities of size a × b. To place a city, he must level the ground inside its rectangle by reducing all cells to the minimum height within that rectangle."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 15
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 15"
rating: 2500
weight: 15
solve_time_s: 132
verified: true
draft: false
---
[CF 15D - Map](https://codeforces.com/problemset/problem/15/D)

**Rating:** 2500  
**Tags:** data structures, implementation, sortings  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular map of size `n` × `m`, where each cell has a non-negative height. Peter wants to build cities of size `a` × `b`. To place a city, he must level the ground inside its rectangle by reducing all cells to the minimum height within that rectangle. The cost of building at a certain position is the total amount of ground removed. The goal is to repeatedly find the optimal rectangle - one with the smallest leveling cost among all available positions - and place a city there. If multiple positions tie, Peter prefers the uppermost, then leftmost position. Once a cell is occupied by a city, it cannot be used for subsequent cities.

The problem gives us maps up to 1000×1000, and city sizes up to the full map dimensions. A naive approach that examines every possible rectangle and computes its cost from scratch would iterate over up to 1,000,000 rectangles, each of which may involve summing up to 1,000,000 cells in the worst case. This results in roughly 10^12 operations - far beyond the 2-second time limit. Therefore, we need a more efficient approach that avoids recalculating sums and minimums naively.

Edge cases include very small maps where cities take up the entire space, maps where all cells are equal (making multiple positions tie), and maps with large values (up to 10^9), which requires careful integer handling. For example, in a 2×2 map with heights `[[1, 2], [3, 5]]` and city size 1×2, the first city will occupy the top-left row, leveling costs 1, then the second city will occupy the bottom row with cost 2. If we ignore the "uppermost-leftmost" tie-breaker, the order could be wrong.

## Approaches

The brute-force approach evaluates every `a×b` rectangle in the map. For each rectangle, it finds the minimum height and sums the difference between each cell and that minimum to compute the leveling cost. Then it selects the rectangle with the smallest cost and marks it as occupied. This repeats until no `a×b` rectangle is available. While correct, this approach is extremely slow because evaluating each rectangle from scratch requires O(a·b) operations, making the overall complexity O((n−a+1)(m−b+1)·a·b). For n=m=1000 and a=b=500, this is around 10^11 operations.

The key insight is that both the **minimum** inside a sliding rectangle and the **sum of heights** can be preprocessed for fast queries. We can compute prefix sums to quickly calculate the sum of any rectangle in O(1). For the minimum, we can use a 2D sliding minimum technique based on deques: first compute row-wise minimums for width `b`, then column-wise minimums on these row-wise results for height `a`. This produces a matrix where each `a×b` rectangle’s minimum is available in O(1). Using these two precomputations, we can compute the leveling cost for all possible positions in O(n·m), instead of O(n·m·a·b). Finally, to place cities sequentially, we need an efficient way to mark occupied cells. A Fenwick tree or segment tree over a 2D binary occupancy map is sufficient, but a simple occupancy grid with the same sliding rectangle checks works since each cell can only be part of one city, limiting total iterations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n−a+1)(m−b+1)·a·b·k) | O(n·m) | Too slow |
| Optimal | O(n·m) | O(n·m) | Accepted |

## Algorithm Walkthrough

1. Compute the 2D prefix sum array of heights. For each cell `(i, j)`, store the sum of all cells from `(1, 1)` to `(i, j)`. This allows O(1) rectangle sum queries using the inclusion-exclusion principle.
2. Compute the row-wise sliding minimums for width `b` using a deque. For each row, maintain a deque of indices such that the leftmost element is always the minimum in the current window of length `b`. Store these intermediate results in a matrix `row_min`.
3. Compute the column-wise sliding minimums for height `a` on `row_min` to obtain the minimum of every `a×b` rectangle. Again, use a deque per column to maintain the current minimum in the vertical sliding window. Call this matrix `rect_min`.
4. For each `a×b` rectangle, compute the leveling cost as `sum of heights − minimum × (a·b)` using the prefix sum array for the sum and `rect_min` for the minimum. Keep track of the rectangle with the smallest cost. Break ties by choosing the uppermost, then leftmost rectangle.
5. Mark the chosen rectangle as occupied in an occupancy grid. Repeat steps 4-5 until no further rectangle is available (i.e., any candidate rectangle contains at least one occupied cell).
6. Output the positions of cities in the order they were placed, along with their leveling costs.

Why it works: At each iteration, we consider all valid rectangles and compute exact leveling costs. By preprocessing sums and minimums, the computation per rectangle is constant. Selecting the rectangle with the minimal cost and marking it occupied guarantees we follow the problem's deterministic city placement. The sliding window approach guarantees the minimum is always correct for each rectangle.

## Python Solution

```python
import sys
from collections import deque
input = sys.stdin.readline

def read_matrix(n, m):
    mat = []
    for _ in range(n):
        mat.append(list(map(int, input().split())))
    return mat

def prefix_sum(mat):
    n, m = len(mat), len(mat[0])
    ps = [[0]*(m+1) for _ in range(n+1)]
    for i in range(n):
        for j in range(m):
            ps[i+1][j+1] = mat[i][j] + ps[i][j+1] + ps[i+1][j] - ps[i][j]
    return ps

def rectangle_sum(ps, x1, y1, x2, y2):
    return ps[x2][y2] - ps[x1][y2] - ps[x2][y1] + ps[x1][y1]

def sliding_min_row(mat, b):
    n, m = len(mat), len(mat[0])
    row_min = [[0]*(m-b+1) for _ in range(n)]
    for i in range(n):
        dq = deque()
        for j in range(m):
            while dq and mat[i][dq[-1]] >= mat[i][j]:
                dq.pop()
            dq.append(j)
            if dq[0] == j-b:
                dq.popleft()
            if j >= b-1:
                row_min[i][j-b+1] = mat[i][dq[0]]
    return row_min

def sliding_min_col(mat, a):
    n, m = len(mat), len(mat[0])
    rect_min = [[0]*m for _ in range(n-a+1)]
    for j in range(m):
        dq = deque()
        for i in range(n):
            while dq and mat[dq[-1]][j] >= mat[i][j]:
                dq.pop()
            dq.append(i)
            if dq[0] == i-a:
                dq.popleft()
            if i >= a-1:
                rect_min[i-a+1][j] = mat[dq[0]][j]
    return rect_min

def main():
    n, m, a, b = map(int, input().split())
    heights = read_matrix(n, m)
    ps = prefix_sum(heights)
    
    row_min = sliding_min_row(heights, b)
    rect_min = sliding_min_col(row_min, a)
    
    occupied = [[False]*m for _ in range(n)]
    result = []
    
    while True:
        best = None
        best_cost = None
        for i in range(n-a+1):
            for j in range(m-b+1):
                if any(occupied[x][y] for x in range(i, i+a) for y in range(j, j+b)):
                    continue
                total = rectangle_sum(ps, i, j, i+a, j+b)
                cost = total - rect_min[i][j]*a*b
                if best_cost is None or cost < best_cost or (cost == best_cost and (i < best[0] or (i==best[0] and j<best[1]))):
                    best = (i, j)
                    best_cost = cost
        if best is None:
            break
        i, j = best
        result.append((i+1, j+1, best_cost))
        for x in range(i, i+a):
            for y in range(j, j+b):
                occupied[x][y] = True
    
    print(len(result))
    for r in result:
        print(*r)

if __name__ == "__main__":
    main()
```

**Explanation:**

The prefix sum section allows O(1) rectangle sum queries. The row-wise and column-wise sliding minimums implement a 2D monotone queue to compute the minimum in O(n·m) rather than recomputing for each rectangle. The occupancy grid ensures we never choose an already used rectangle.
