---
title: "CF 106130J - \u9003\u51fa\u751f\u5929"
description: "We are given a grid with $n+2$ rows and $m$ columns. The top row and the bottom row are safe, while the $n$ middle rows each contain exactly one stone statue. Each statue sits at a specific column in its row and faces either left or right."
date: "2026-06-19T19:51:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106130
codeforces_index: "J"
codeforces_contest_name: "GDUT 2025 Monthly competition"
rating: 0
weight: 106130
solve_time_s: 57
verified: true
draft: false
---

[CF 106130J - \u9003\u51fa\u751f\u5929](https://codeforces.com/problemset/problem/106130/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid with $n+2$ rows and $m$ columns. The top row and the bottom row are safe, while the $n$ middle rows each contain exactly one stone statue. Each statue sits at a specific column in its row and faces either left or right. From its position, it emits a horizontal laser along its row in the direction it faces, and every cell covered by that laser becomes forbidden. The statue cell itself is also forbidden.

A cell is blocked if it is either occupied by a statue or lies on a laser ray. The start position is the top-right corner of the grid, and the goal is the bottom-left corner. At each step, the player can move one cell up, down, left, or right, but cannot leave the grid or enter any blocked cell.

The task is to determine whether a path exists from start to goal using only valid moves through unblocked cells.

The grid size is at most about one million cells. This immediately suggests that any algorithm visiting each cell a constant number of times is feasible, while anything quadratic in a row or involving repeated recomputation per query would be too slow.

A subtle failure case comes from misunderstanding the laser effect. The laser is not a single cell but an entire ray, so treating only the statue positions as blocked is incorrect.

For example, if a row has a statue at column 3 facing right, then every cell in that row from column 3 to $m$ is unsafe. A naive approach that only blocks column 3 would incorrectly allow traversal through the laser zone, producing a false “YES”.

Another edge case is when the laser leaves no safe cells in a row at all. If a statue at column 1 faces left, then the entire row becomes unsafe, effectively acting as a full barrier.

## Approaches

The most direct way to think about the problem is to model it as a graph. Every cell in the grid is a node, and edges connect orthogonally adjacent cells if both endpoints are safe. Once this graph is built, we can run a standard reachability search from the start cell.

Constructing the graph is straightforward because the grid is explicit. For each middle row, we mark all cells hit by the laser as blocked. Then we perform a BFS or DFS over the remaining cells.

The brute force idea is already close to optimal. The main cost is visiting each cell at most once and checking up to four neighbors, which gives $O(nm)$ time. There is no hidden combinatorial explosion because the constraints are purely geometric and static.

The key observation is that the laser constraints only modify which cells exist in the graph; they do not introduce time dynamics or dependencies between steps. Once the blocked cells are precomputed, the problem reduces to plain grid connectivity.

So the task collapses to: build a blocked grid, then run BFS.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Grid BFS | $O(nm)$ | $O(nm)$ | Accepted |
| Same with preprocessing | $O(nm)$ | $O(nm)$ | Accepted |

## Algorithm Walkthrough

We first convert the problem into a static grid of free and blocked cells, then run BFS.

1. Create a 2D boolean array `blocked` of size $(n+2) \times m$, initially all false. This represents whether a cell can be entered.
2. For each of the $n$ middle rows, read the statue position $c_i$ and direction $d_i$. Mark the statue cell itself as blocked.
3. If the statue faces right, every cell from $c_i$ to $m$ in that row becomes blocked. If it faces left, every cell from $1$ to $c_i$ becomes blocked. This directly encodes the laser ray as a contiguous segment.
4. Run BFS starting from $(1, m)$ if it is not blocked. We maintain a queue and a visited array.
5. From each cell, try moving in the four directions. We only enqueue a neighbor if it is inside the grid, not blocked, and not visited before.
6. Stop early if we reach $(n+2, 1)$.

The key idea behind BFS here is that every move has equal cost, so reachability in an unweighted grid is exactly what BFS computes.

### Why it works

Once the blocked cells are fixed, the grid becomes a standard 4-neighbor graph. BFS explores exactly the connected component containing the start cell. If the target lies in the same component, BFS will eventually reach it; otherwise it is unreachable because no alternative path exists outside this component.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    n, m = map(int, input().split())
    
    # grid has n+2 rows
    blocked = [[False] * m for _ in range(n + 2)]
    
    # read statues
    for i in range(n):
        c, d = input().split()
        c = int(c) - 1
        r = i + 1
        
        blocked[r][c] = True
        
        if d == 'R':
            for j in range(c, m):
                blocked[r][j] = True
        else:
            for j in range(0, c + 1):
                blocked[r][j] = True
    
    sr, sc = 0, m - 1
    tr, tc = n + 1, 0
    
    if blocked[sr][sc] or blocked[tr][tc]:
        print("NO")
        return
    
    q = deque()
    q.append((sr, sc))
    visited = [[False] * m for _ in range(n + 2)]
    visited[sr][sc] = True
    
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]
    
    while q:
        r, c = q.popleft()
        if (r, c) == (tr, tc):
            print("YES")
            return
        
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n + 2 and 0 <= nc < m:
                if not blocked[nr][nc] and not visited[nr][nc]:
                    visited[nr][nc] = True
                    q.append((nr, nc))
    
    print("NO")

if __name__ == "__main__":
    solve()
```

The implementation first builds the blocked map row by row, directly encoding each laser as a filled interval. Then it runs a standard BFS over the grid. The visited array ensures each cell is processed once, and the direction array encodes the four possible moves.

Care must be taken with indexing: the input uses 1-based columns and rows offset by 1 due to the extra boundary rows, so we convert everything to 0-based indexing internally.

## Worked Examples

### Example 1

Consider a small grid where a laser blocks most of the middle row:

Input:

```
1 3
2 R
```

Start is at $(1,3)$, goal at $(3,1)$. The middle row has a statue at column 2 facing right, so cells $(2,2)$ and $(2,3)$ are blocked, leaving only $(2,1)$ usable.

| Step | Cell | Queue State | Action |
| --- | --- | --- | --- |
| 1 | (1,3) | (1,3) | start |
| 2 | (2,3 blocked) | (1,3) | skip |
| 3 | (1,2) | (1,2) | move left |
| 4 | (2,1) | (2,1) | move down |
| 5 | (3,1) | reached | success |

This trace shows how BFS naturally finds a narrow passage created by the laser boundary.

### Example 2

Input:

```
2 2
1 L
2 R
```

Here both middle rows are heavily constrained.

| Step | Cell | Queue State | Action |
| --- | --- | --- | --- |
| 1 | (1,2) | (1,2) | start |
| 2 | (1,1) | (1,1) | move left |
| 3 | blocked row cells | - | cannot descend |
| 4 | - | empty | BFS ends |

No path can pass through either middle row because each row eliminates all possible crossings in at least one direction, preventing any continuous vertical traversal.

These examples show how the algorithm distinguishes between usable and fully blocking laser configurations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm)$ | Each cell is marked at most once and visited at most once during BFS |
| Space | $O(nm)$ | Storage for blocked and visited grids |

The constraints allow up to about $10^6$ cells, so a linear traversal over the grid is comfortably within limits in both time and memory.

## Test Cases

```python
import sys, io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n, m = map(int, sys.stdin.readline().split())
    blocked = [[False] * m for _ in range(n + 2)]
    
    for i in range(n):
        c, d = sys.stdin.readline().split()
        c = int(c) - 1
        r = i + 1
        blocked[r][c] = True
        if d == 'R':
            for j in range(c, m):
                blocked[r][j] = True
        else:
            for j in range(0, c + 1):
                blocked[r][j] = True
    
    sr, sc = 0, m - 1
    tr, tc = n + 1, 0
    
    if blocked[sr][sc] or blocked[tr][tc]:
        return "NO"
    
    q = deque([(sr, sc)])
    vis = [[False] * m for _ in range(n + 2)]
    vis[sr][sc] = True
    
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]
    
    while q:
        r, c = q.popleft()
        if (r, c) == (tr, tc):
            return "YES"
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n + 2 and 0 <= nc < m:
                if not blocked[nr][nc] and not vis[nr][nc]:
                    vis[nr][nc] = True
                    q.append((nr, nc))
    
    return "NO"

# provided samples (placeholders)
# assert run("2 2\n2 R\n1 R\n") == "NO"
# assert run("4 6\n2 L\n4 R\n6 R\n4 L\n") == "YES"

# custom tests
assert run("1 1\n1 L\n") == "NO", "single blocked path"
assert run("1 2\n1 R\n") == "NO", "full row blocked"
assert run("1 2\n2 L\n") == "NO", "start isolated"
assert run("0 3\n") == "YES", "empty grid trivial"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 with blocking | NO | smallest grid fully blocked |
| full row laser | NO | complete row obstruction |
| start isolated case | NO | unreachable start handling |
| empty middle rows | YES | trivial connectivity |

## Edge Cases

A critical edge case occurs when the start or goal cell lies inside a laser zone. For instance, if a configuration causes the top-right cell to be marked as blocked, the BFS must immediately reject the path. The algorithm handles this by checking both endpoints before starting the search, ensuring no wasted traversal.

Another case is a row where the laser covers the entire row. In such a situation, that row becomes a hard separator in the grid. The BFS naturally respects this because no transitions exist across that row, so the search space splits into disconnected components.

Finally, if both endpoints are in different disconnected regions created by alternating laser directions, BFS simply exhausts the reachable region without ever reaching the target, correctly returning “NO”.
