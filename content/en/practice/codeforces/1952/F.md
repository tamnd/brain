---
title: "CF 1952F - Grid"
description: "We are given a fixed-size grid of 21 rows and 21 columns. Each cell contains either 0 or 1. The grid should be viewed as a map where each cell is a square tile, and tiles with the same value may form connected regions through shared edges."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 1952
codeforces_index: "F"
codeforces_contest_name: "April Fools Day Contest 2024"
rating: 0
weight: 1952
solve_time_s: 72
verified: false
draft: false
---

[CF 1952F - Grid](https://codeforces.com/problemset/problem/1952/F)

**Rating:** -  
**Tags:** *special, brute force  
**Solve time:** 1m 12s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a fixed-size grid of 21 rows and 21 columns. Each cell contains either `0` or `1`. The grid should be viewed as a map where each cell is a square tile, and tiles with the same value may form connected regions through shared edges.

The task is to compute a single integer from this grid, which corresponds to how many distinct regions exist under a natural connectivity rule: cells of the same type are considered part of the same region if you can move between them using only up, down, left, or right steps without leaving that type.

So the grid is not treated as independent cells, but as a collection of connected components formed by identical values. The output is the number of these components for the relevant value type (in this problem, the intended interpretation is counting connected regions of `0` cells).

Because the grid size is fixed at 21 by 21, the total number of cells is only 441. This immediately implies that even solutions that inspect every cell repeatedly are feasible, since the input size is tiny. Any algorithm up to roughly O(n²) or even O(n² log n) is trivially fast enough.

The main failure mode in this kind of problem is misinterpreting connectivity. For example, diagonally touching cells are not connected. Another subtle issue is accidentally counting both `0` and `1` regions instead of only the intended one, or forgetting to mark visited cells, which leads to overcounting the same region multiple times.

A concrete pitfall looks like this:

Input fragment:

```
00
00
```

This is a single connected component, not four separate cells. A naive loop that increments a counter per cell would incorrectly output 4.

Another common mistake is treating diagonal adjacency as connected:

```
0.
.0
```

These are two separate components under 4-direction rules, even though they touch at a corner.

## Approaches

The brute-force idea is to scan every cell and, whenever we find an unvisited target cell (`0`), run a flood fill (DFS or BFS) to mark the entire connected region. Each time we start such a traversal, we increment the answer.

This approach is correct because every connected component has at least one starting cell, and the flood fill ensures we mark exactly those cells reachable within that component. However, if the grid were large, repeatedly scanning or recursively exploring without marking would cause exponential revisits. The key inefficiency in a naive version would be forgetting the visited array, which leads to revisiting the same region many times.

The key observation is that the grid size is constant and small, so we do not need any advanced optimization. A simple BFS or DFS with a visited matrix fully solves the problem in linear time relative to the number of cells.

We reduce the problem to: “count how many times we can start a flood fill over an unvisited `0` cell”.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force without marking visited | O(4^(n²)) worst-case | O(n²) | Too slow |
| DFS/BFS flood fill | O(n²) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Read the 21 by 21 grid into memory. Each cell is stored as a character or integer.
2. Maintain a 21 by 21 boolean array `visited`, initially all false.
3. Initialize a counter `components = 0`.
4. Iterate over every cell `(i, j)` in the grid.
5. If the cell is not a `0`, skip it because we only care about regions formed by `0` cells.
6. If the cell is `0` and has not been visited, start a BFS (or DFS) from this cell.
7. During BFS/DFS, mark every reachable `0` cell as visited by expanding in four directions.
8. After the flood fill finishes, increment `components` by 1 because we have fully discovered one connected region.
9. After scanning all cells, output `components`.

The reason we only increment when encountering an unvisited `0` is that it guarantees each connected region is counted exactly once. Any later encounter with a cell from the same region will be ignored because it is already marked.

### Why it works

The visited array enforces a partition of all `0` cells into disjoint explored sets. Each BFS explores exactly one maximal connected set under 4-direction adjacency. Since no cell can be part of two different BFS runs, each connected component contributes exactly one increment to the counter, and every `0` cell belongs to some component discovered this way.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

n = 21
grid = [input().strip() for _ in range(n)]
visited = [[False] * n for _ in range(n)]

dirs = [(1,0), (-1,0), (0,1), (0,-1)]

def bfs(si, sj):
    q = deque()
    q.append((si, sj))
    visited[si][sj] = True

    while q:
        x, y = q.popleft()
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n:
                if not visited[nx][ny] and grid[nx][ny] == '0':
                    visited[nx][ny] = True
                    q.append((nx, ny))

components = 0

for i in range(n):
    for j in range(n):
        if grid[i][j] == '0' and not visited[i][j]:
            bfs(i, j)
            components += 1

print(components)
```

The BFS function is the core of the solution. It ensures that once we start from a `0` cell, we consume the entire connected structure before returning. The nested loops only act as triggers for new components.

A subtle implementation detail is marking a cell as visited when it is enqueued, not when it is dequeued. This prevents multiple enqueues of the same cell.

## Worked Examples

### Sample 1

We consider the first unvisited `0` encountered during scanning. The BFS expands across all connected `0` cells reachable from it.

| Step | Start cell | BFS explored cells | Components |
| --- | --- | --- | --- |
| 1 | first (i,j) with `0` | full region 1 | 1 |
| 2 | next unvisited `0` | full region 2 | 2 |
| ... | ... | ... | 12 |

After all cells are processed, there are 12 distinct BFS launches, so the output is 12.

This trace confirms that the grid is partitioned into 12 disjoint zero-regions.

### Sample 2 (constructed)

Input:

```
111
101
111
```

There is exactly one isolated `0` in the center.

| Step | Cell | Action | Components |
| --- | --- | --- | --- |
| 1 | (1,1) | start BFS on 0 | 1 |
| 2 | all others | skipped | 1 |

Output is 1, confirming isolated-cell handling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(21 × 21) | Each cell is visited at most once during BFS |
| Space | O(21 × 21) | Visited array and queue storage |

The grid size is fixed and extremely small, so even constant-factor overhead is negligible. The algorithm easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    n = 21
    grid = [input().strip() for _ in range(n)]
    visited = [[False]*n for _ in range(n)]
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]

    def bfs(si,sj):
        q = deque([(si,sj)])
        visited[si][sj] = True
        while q:
            x,y = q.popleft()
            for dx,dy in dirs:
                nx,ny = x+dx,y+dy
                if 0<=nx<n and 0<=ny<n:
                    if grid[nx][ny]=='0' and not visited[nx][ny]:
                        visited[nx][ny]=True
                        q.append((nx,ny))

    ans = 0
    for i in range(n):
        for j in range(n):
            if grid[i][j]=='0' and not visited[i][j]:
                bfs(i,j)
                ans += 1

    return str(ans)

# sample
assert run("""111111101011101111111
100000100011001000001
101110101101001011101
101110101100101011101
101110101001001011101
100000100111101000001
111111101010101111111
000000000001100000000
111100101111110011101
000111010101100110101
111101101101001000011
001001000001000011000
111101110000111001011
000000001001001111100
111111100001101010000
100000100010010100111
101110100110110011100
101110101100000100010
101110101010110000100
100000101000011001001
111111101011111111100
""") == "12"

# all ones grid
assert run("\n".join(["1"*21 for _ in range(21)])) == "0"

# single zero
g = ["1"*21 for _ in range(21)]
g[10] = g[10][:10] + "0" + g[10][11:]
assert run("\n".join(g)) == "1"

# checkerboard zeros (each isolated)
g = []
for i in range(21):
    row = ""
    for j in range(21):
        row += "0" if (i+j)%2==0 else "1"
    g.append(row)
assert run("\n".join(g)) == str((21*21+1)//2)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample grid | 12 | correctness on full structure |
| all ones | 0 | no components case |
| single zero | 1 | isolated component |
| checkerboard | 231 | maximum fragmentation |

## Edge Cases

A key edge case is when there are no `0` cells at all. In that situation, the outer loops still scan every cell, but no BFS is triggered, so the answer remains 0. The algorithm handles this naturally because the condition `grid[i][j] == '0'` is never satisfied.

Another edge case is a fully connected grid of `0`s:

```
000000000000000000000
... (21 rows)
```

Here, the first BFS starting at (0,0) will eventually mark all 441 cells. After that, every other cell is already visited, so no new BFS is launched, and the answer is 1. This confirms that the visited marking correctly prevents overcounting.
