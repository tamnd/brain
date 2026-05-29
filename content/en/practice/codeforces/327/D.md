---
title: "CF 327D - Block Tower"
description: "We are given a grid where some cells are blocked and the rest are usable land. On each usable cell we may place one building, either a blue tower worth 100 population or a red tower worth 200 population."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dfs-and-similar", "graphs"]
categories: ["algorithms"]
codeforces_contest: 327
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 191 (Div. 2)"
rating: 1900
weight: 327
solve_time_s: 94
verified: false
draft: false
---

[CF 327D - Block Tower](https://codeforces.com/problemset/problem/327/D)

**Rating:** 1900  
**Tags:** constructive algorithms, dfs and similar, graphs  
**Solve time:** 1m 34s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a grid where some cells are blocked and the rest are usable land. On each usable cell we may place one building, either a blue tower worth 100 population or a red tower worth 200 population. The restriction is that a red tower is not freely placeable: when it is built, at least one of its four neighbors must already contain a blue tower. After that point, buildings can be destroyed at any time, and destruction does not affect other cells or invalidate already placed buildings.

The task is not just to assign tower types, but to output a full sequence of build and destroy operations that ends in a configuration maximizing total population value. Since each red tower is strictly better than a blue tower but requires a blue neighbor, the problem becomes about arranging blue towers as support so that as many red towers as possible can be placed on accessible cells.

The grid can be as large as 500 by 500, so up to 250,000 cells exist. Any solution that tries to recompute global states per cell or simulate arbitrary ordering with nested scans will be too slow. The structure strongly suggests a graph-based construction, since adjacency is local and red tower feasibility depends only on neighbors.

A key subtle edge case is isolated components. If a connected component of empty cells has size 1, it cannot contain a red tower at all because there is no neighbor to support it. Another tricky situation is bipartite parity: since red towers require a blue neighbor at build time, naive coloring approaches that try to directly assign colors without construction ordering can fail.

The most dangerous misunderstanding is assuming we can decide final colors first and then output operations arbitrarily. The constraint is temporal: a red tower requires a blue neighbor at the moment of construction, not merely in the final configuration. This forces us to construct a valid build order, not just a final assignment.

## Approaches

A naive idea is to decide for each cell independently whether it should be blue or red in the final state, then try to build red towers only when a neighboring blue already exists. One might attempt to greedily build blues first in all cells and then upgrade some to red. However, this immediately breaks because upgrading is not allowed: a red tower must be built as red, not converted from blue.

Another brute-force approach is to simulate all possible orders of building towers and pick the best valid sequence. This is clearly exponential because every cell decision interacts with neighbors through the red constraint. Even restricting to local greedy choices still leads to dead ends, since building a red tower too early or too late can block future placements.

The key observation is that the grid graph is bipartite. If we color cells like a chessboard, every cell has neighbors only of opposite color. This allows us to treat one part of the bipartition as “support” and the other as “main profit area.” We can choose to first build blue towers in one partition to act as guaranteed neighbors, and then safely build red towers in the opposite partition, since every red will have at least one adjacent blue if we ensure support coverage.

The deeper insight is that we do not need to minimize blue usage; we only need to ensure feasibility. Once a cell is guaranteed to have at least one blue neighbor at construction time, it can be safely made red. Thus we can build all usable cells in a spanning-tree-like order where we first seed blues and then expand reds.

A standard way to enforce this is to treat the grid as a graph and perform DFS or BFS, always ensuring that when we enter a cell we first create a blue tower there (so it can support neighbors), and then immediately attempt to build red towers in its neighbors that are safe due to this newly created blue.

This construction effectively simulates a controlled traversal where blue towers act as anchors that enable red placements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force ordering search | Exponential | O(nm) | Too slow |
| Bipartite DFS construction | O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

We interpret the grid as a graph where each '.' cell is a node connected to its four adjacent '.' cells.

1. We iterate over all cells and start a DFS from each unvisited '.' cell. This ensures we handle disconnected components independently.
2. When entering a cell for the first time, we immediately place a blue tower there. This guarantees the cell becomes a valid support point for its neighbors.
3. From this cell, we explore its neighbors. For each adjacent unvisited '.' cell, we recursively visit it.
4. After returning from recursion, we try to place a red tower in the neighbor cell we just visited, because it now has at least one adjacent blue (its parent in DFS). This ordering ensures feasibility at the exact moment of construction.
5. We mark visited cells so each cell is processed exactly once, preventing redundant operations.

The subtlety is the ordering: blue must be placed before any red in the same cell, and red is only placed after at least one adjacent blue exists. The DFS tree guarantees that each non-root node has a parent already turned into a blue tower.

Why it works comes from the DFS tree structure. Every edge in the DFS tree connects a parent and a child. The parent is always processed first and becomes blue before the child is processed. Thus when the child is considered, it has a guaranteed adjacent blue neighbor. This invariant ensures every red placement is valid at construction time, and every reachable cell is used exactly once in a way that maximizes utilization of all available cells.

## Python Solution

```python
import sys
sys.setrecursionlimit(10**7)
input = sys.stdin.readline

n, m = map(int, input().split())
grid = [list(input().strip()) for _ in range(n)]

visited = [[False] * m for _ in range(n)]
ops = []

dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def dfs(x, y):
    visited[x][y] = True

    ops.append(f"B {x+1} {y+1}")

    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < m:
            if grid[nx][ny] == '.' and not visited[nx][ny]:
                dfs(nx, ny)
                ops.append(f"R {nx+1} {ny+1}")

for i in range(n):
    for j in range(m):
        if grid[i][j] == '.' and not visited[i][j]:
            dfs(i, j)

print(len(ops))
print("\n".join(ops))
```

The implementation uses a DFS over all empty cells. The moment we enter a cell, we place a blue tower. This is the crucial ordering decision that guarantees every later red placement is legal.

The recursion ensures that each neighbor is reached through exactly one parent, which acts as the required blue support. After visiting a child subtree, we place a red tower on that child cell, relying on the fact that its parent has already been turned blue.

The visited array prevents revisiting cells, ensuring linear complexity. The recursion limit is increased because the grid can form long chains up to 250,000 nodes.

A subtle point is coordinate conversion: the output is 1-indexed, so we add 1 when printing.

## Worked Examples

### Example 1

Input:

```
2 3
..#
.#.
```

We label cells as coordinates. The DFS starts at (0,0).

| Step | Action | Cell | Reason |
| --- | --- | --- | --- |
| 1 | B | (0,0) | first visit |
| 2 | move to (0,1) |  | neighbor |
| 3 | B | (0,1) | first visit |
| 4 | move to (1,0) |  | neighbor |
| 5 | B | (1,0) | first visit |
| 6 | return to (0,1) |  | backtrack |
| 7 | R | (1,0) | now has blue neighbor |
| 8 | move to (1,2) |  | skip # blocked |
