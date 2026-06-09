---
title: "CF 1829E - The Lakes"
description: "We are given a two-dimensional grid representing terrain, where each cell contains a non-negative integer indicating the depth of water at that location."
date: "2026-06-09T07:18:08+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dsu", "graphs", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1829
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 871 (Div. 4)"
rating: 1100
weight: 1829
solve_time_s: 80
verified: true
draft: false
---

[CF 1829E - The Lakes](https://codeforces.com/problemset/problem/1829/E)

**Rating:** 1100  
**Tags:** dfs and similar, dsu, graphs, implementation  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a two-dimensional grid representing terrain, where each cell contains a non-negative integer indicating the depth of water at that location. A "lake" is defined as a contiguous region of nonzero cells that are connected orthogonally, meaning we can move between them using up, down, left, or right moves without stepping onto a zero-depth cell. The volume of a lake is the sum of all depths of its constituent cells. The task is to find the largest possible lake volume in each grid.

The input consists of multiple test cases. Each test case defines the dimensions of the grid and the depth values of each cell. The maximum grid size is 1000 by 1000, and the sum of all cells across all test cases does not exceed $10^6$. This means any algorithm that touches each cell a constant number of times will run comfortably under the time limit. However, algorithms that attempt to compare every pair of cells or perform a global operation per nonzero cell (like $O(n^2)$ per test case) would be too slow.

Non-obvious edge cases include grids that contain only zeros, grids where all nonzero cells are isolated, and lakes that touch the grid boundary. For example, a single-cell lake with depth 5 in a 1x1 grid should return 5. A naive DFS that forgets to mark visited cells may double-count a lake, producing a volume larger than the correct value. Similarly, forgetting to handle boundaries correctly may result in out-of-bounds errors.

## Approaches

The brute-force approach is conceptually straightforward. For each nonzero cell, perform a DFS or BFS to explore the connected nonzero region, summing the depths to compute the lake volume. Keep track of visited cells to avoid double-counting. At the end, return the maximum volume encountered. This approach is correct, but its worst-case performance is proportional to the total number of cells, since each cell is visited once and each neighbor check is constant. Given the constraints, this is acceptable, but the naive implementation without marking visited cells or using recursion carefully could run into stack overflows or redundant computations.

The optimal approach relies on the same principle but uses iterative BFS to avoid recursion depth issues. By processing each cell exactly once and summing the connected component on-the-fly, we guarantee that we visit every cell at most once. The key insight is that each lake is an independent connected component, and the largest volume comes from the component with the highest sum. Since we only traverse cells that are part of nonzero lakes, we skip unnecessary checks efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS/BFS | O(n*m) per test case | O(n*m) | Accepted |
| Optimal iterative BFS | O(n*m) per test case | O(n*m) | Accepted |

## Algorithm Walkthrough

1. Initialize a variable `max_volume` to zero. This will track the largest lake volume found.
2. Create a 2D array `visited` of the same size as the grid to track which cells have already been included in a lake.
3. Iterate over every cell `(i, j)` in the grid. If `a[i][j]` is zero or already visited, skip it.
4. If the cell is nonzero and unvisited, start a BFS from that cell. Initialize a queue with `(i, j)` and a variable `current_volume` to zero.
5. While the queue is not empty, pop a cell `(x, y)`. Mark it as visited, and add `a[x][y]` to `current_volume`.
6. Examine all four neighbors of `(x, y)`. For each neighbor `(nx, ny)` within grid bounds, if `a[nx][ny] > 0` and not visited, append it to the queue.
7. After the BFS completes, compare `current_volume` with `max_volume`. If it is larger, update `max_volume`.
8. Continue iterating through the grid until all cells have been processed.
9. Return `max_volume` for this test case.

Why it works: The BFS ensures that every connected nonzero region is fully explored once, summing all its depths. The `visited` array guarantees no cell is counted twice. Since all possible lakes are explored independently, the maximum lake volume is correctly identified.

## Python Solution

```python
import sys
from collections import deque
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        grid = [list(map(int, input().split())) for _ in range(n)]
        visited = [[False]*m for _ in range(n)]
        max_volume = 0
        
        for i in range(n):
            for j in range(m):
                if grid[i][j] > 0 and not visited[i][j]:
                    q = deque()
                    q.append((i,j))
                    visited[i][j] = True
                    current_volume = 0
                    while q:
                        x, y = q.popleft()
                        current_volume += grid[x][y]
                        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < n and 0 <= ny < m and grid[nx][ny] > 0 and not visited[nx][ny]:
                                visited[nx][ny] = True
                                q.append((nx, ny))
                    max_volume = max(max_volume, current_volume)
        print(max_volume)

if __name__ == "__main__":
    solve()
```

The solution separates reading input, processing each test case, and BFS exploration. Using `deque` for BFS ensures efficient popping from the front. Marking cells as visited immediately when they are enqueued avoids multiple visits and maintains correctness. The four-direction neighbor check respects grid boundaries to avoid index errors.

## Worked Examples

### Sample 1

Input:

```
3 3
1 2 0
3 4 0
0 0 5
```

| Cell visited | Queue state | current_volume | max_volume |
| --- | --- | --- | --- |
| (0,0) | [(0,0)] | 0 | 0 |
| (0,1) | [(0,1)] | 1 | 0 |
| (1,0) | [(1,0)] | 3 | 0 |
| (1,1) | [] | 10 | 10 |
| (2,2) | [(2,2)] | 5 | 10 |

Explanation: The BFS first explores the connected lake of cells (0,0),(0,1),(1,0),(1,1) totaling 10. The isolated cell (2,2) forms a lake of volume 5. Maximum is correctly 10.

### Sample 2

Input:

```
1 1
0
```

Trace: Cell is zero, skipped. `max_volume` remains 0. Correctly outputs 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n*m) per test case | Each cell is visited once, and each neighbor is checked four times |
| Space | O(n*m) | Grid and visited arrays, plus queue up to n*m in worst case |

Given the sum of all cells across test cases does not exceed $10^6$, this solution comfortably runs within the 3-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    f = io.StringIO()
    with redirect_stdout(f):
        solve()
    return f.getvalue().strip()

# Provided samples
assert run("5\n3 3\n1 2 0\n3 4 0\n0 0 5\n1 1\n0\n3 3\n0 1 1\n1 0 1\n1 1 1\n5 5\n1 1 1 1 1\n1 0 0 0 1\n1 0 5 0 1\n1 0 0 0 1\n1 1 1 1 1\n5 5\n1 1 1 1 1\n1 0 0 0 1\n1 1 4 0 1\n1 0 0 0 1\n1 1 1 1 1") == "10\n0\n7\n16\n21"

# Custom cases
assert run("1\n1 1\n5") == "5", "single cell lake"
assert run("1\n2 2\n0 0\n0 0") == "0", "all zeros"
assert run("1\n2 2\n1 1\n1 1") == "4", "full lake"
assert run("1\n3 3\n0 1 0\n1 0 1\n0 1 0") == "1", "diagonal not connected"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 with 5 | 5 | Single cell lake |
| 2x2 all zeros | 0 | Zero lake case |
| 2x2 all ones | 4 | Full connected lake |
| 3x3 cross of ones | 1 | Only orthogonal connections count, diagonals ignored |

## Edge Cases

A grid with only zeros: BFS is never
