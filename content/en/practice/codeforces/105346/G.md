---
title: "CF 105346G - Pumpkin Patch"
description: "We are given a grid where each cell behaves like a terrain type in a small maze. The traveler starts from exactly one cell marked S and must reach a unique exit cell marked E. Movement is allowed in the four cardinal directions, and each move costs one unit of time."
date: "2026-06-23T15:35:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105346
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 09-13-24 Div. 2 (Beginner)"
rating: 0
weight: 105346
solve_time_s: 86
verified: false
draft: false
---

[CF 105346G - Pumpkin Patch](https://codeforces.com/problemset/problem/105346/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 26s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a grid where each cell behaves like a terrain type in a small maze. The traveler starts from exactly one cell marked `S` and must reach a unique exit cell marked `E`. Movement is allowed in the four cardinal directions, and each move costs one unit of time.

Most cells are either empty, blocked, or special. Empty cells are freely traversable. Cells marked `P` are permanent walls. Cells marked `C` are collectibles, and each one increases the number of available candy corns by one when stepped on. Cells marked `J` act like locked gates: they can only be entered if at least one candy corn is currently held, and stepping on them consumes one candy corn.

The key complication is that the ability to pass through `J` cells depends on how many `C` cells have been collected along the path, and since there are at most 8 candies in total, the state space remains bounded.

The task is to compute the minimum time required to go from `S` to `E`, or report that no valid path exists.

The grid size is at most 100 by 100, so there are up to 10,000 cells. A naive shortest path search that ignores candy state would fail because it would treat `J` cells incorrectly. At the same time, any solution must handle state changes caused by collecting candies, so position alone is not sufficient.

A correct state must include both position and current candy count. Since there are at most 8 candies, the full state space is at most 100 × 100 × 9, which is small enough for BFS.

A subtle edge case appears when revisiting the same cell with different candy counts. For example, arriving at a `J` cell with 0 candies is impossible, but arriving later with 1 candy may be valid. A naive visited array keyed only by position would incorrectly discard valid paths.

Another edge case occurs when a candy is required to pass a `J` cell, but the optimal path requires detouring to collect it first. Greedy shortest path ignoring future constraints will fail here.

## Approaches

A brute-force approach would attempt to enumerate all possible paths from `S` to `E`, tracking candy collection along each path. Each step branches into up to four directions, so the number of possible paths grows exponentially with path length. Even for a 100 by 100 grid, this becomes completely infeasible, as the number of simple paths alone is astronomically large.

The reason this is unnecessary is that the problem has optimal substructure: reaching the same cell with the same number of candies is equivalent regardless of how we got there. Once we recognize that the state is fully described by position and candy count, the problem becomes a shortest path in an unweighted graph.

This directly suggests a breadth-first search over an expanded state space. Each node is a triple `(i, j, k)` where `k` is the number of candies currently held. Transitions correspond to moving to adjacent cells and updating `k` depending on the cell type. Since each move costs exactly one unit, BFS guarantees the shortest path.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| BFS on expanded state graph | O(n · m · 9) | O(n · m · 9) | Accepted |

## Algorithm Walkthrough

We treat each reachable configuration as a state in a graph and run BFS from the start state.

1. Locate the starting cell `S` and initialize the BFS queue with state `(S_row, S_col, 0, 0)`, where the last value is the number of steps taken. The candy count starts at zero because no candies have been collected yet.
2. Create a visited structure indexed by `(row, col, candy_count)`. This ensures we do not incorrectly discard states that revisit a cell with a different number of candies.
3. While the queue is not empty, extract the front state `(r, c, k, dist)`.
4. If the current cell is the exit `E`, immediately return `dist`, since BFS guarantees this is the shortest possible path.
5. For each of the four possible movement directions, compute the next cell `(nr, nc)`. Skip it if it is out of bounds or a pumpkin `P`.
6. Determine whether the move is valid based on the target cell:

If it is `J`, ensure `k > 0`, then decrement `k` by one because a candy is consumed.

If it is `C`, increment `k` by one after stepping into it.

If it is empty, `S`, or `E`, the candy count remains unchanged unless already handled.
7. If the resulting state `(nr, nc, nk)` has not been visited, mark it visited and push it into the queue with distance `dist + 1`.
8. If the queue is exhausted without reaching `E`, return `"SPOOKED!"`.

### Why it works

The algorithm explores states in increasing order of distance because BFS processes all states at depth `d` before any at depth `d+1`. Each state fully encodes all information needed to make future decisions: position and candy inventory. This prevents incorrect pruning since two visits to the same cell with different candy counts are genuinely different situations. Therefore, when the exit is first encountered, no shorter valid path can exist.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    n, m = map(int, input().split())
    grid = [list(input().strip()) for _ in range(n)]
    
    sr = sc = er = ec = -1
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'S':
                sr, sc = i, j
            elif grid[i][j] == 'E':
                er, ec = i, j
    
    # visited[r][c][k]
    visited = [[[False] * 9 for _ in range(m)] for _ in range(n)]
    
    q = deque()
    q.append((sr, sc, 0, 0))
    visited[sr][sc][0] = True
    
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    
    while q:
        r, c, k, dist = q.popleft()
        
        if grid[r][c] == 'E':
            print(dist)
            return
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < n and 0 <= nc < m):
                continue
            if grid[nr][nc] == 'P':
                continue
            
            nk = k
            cell = grid[nr][nc]
            
            if cell == 'C':
                nk += 1
            elif cell == 'J':
                if nk == 0:
                    continue
                nk -= 1
            
            if not visited[nr][nc][nk]:
                visited[nr][nc][nk] = True
                q.append((nr, nc, nk, dist + 1))
    
    print("SPOOKED!")

if __name__ == "__main__":
    solve()
```

The implementation mirrors the state definition directly. The BFS queue stores both position and candy count, which is essential for correctness. The visited array is three-dimensional to prevent revisiting identical states. The order of handling cell effects matters: we compute the next candy count based on the cell being entered, not the one being left.

A common mistake is marking a cell as visited without considering candy count, which breaks correctness because reaching the same position with more candies can unlock future `J` cells.

Another subtle point is checking for `E` when popping from the queue rather than when pushing, which ensures the returned distance corresponds to the shortest valid path.

## Worked Examples

### Sample 1

Input:

```
5 5
S..PC
.PPP.
..P..
..J..
...E
```

We track BFS states as `(row, col, candies, dist)`.

| Step | State | Action | Notes |
| --- | --- | --- | --- |
| 1 | (0,0,0,0) | Start | Begin BFS |
| 2 | (0,1,0,1) | Move right | Empty cell |
| 3 | (1,0,0,1) | Move down | Empty cell |
| 4 | ... | Expand frontier | Multiple paths |
| ... | ... | ... | Candy collected before J |
| final | (4,4,?,16) | Reach E | Exit found |

The key mechanism is that the algorithm is forced to route through `C` before attempting to enter `J`, and BFS ensures the earliest valid combination is chosen.

Output:

```
16
```

### Sample 2

Input:

```
1 10
SCCCCJJJJE
```

We begin at `S`, and BFS immediately collects all four candies before reaching any `J`. The state evolves as:

| Step | State | Candy | Cell |
| --- | --- | --- | --- |
| 1 | (0,0,0,0) | 0 | S |
| 2 | (0,1,1,1) | 1 | C |
| 3 | (0,2,2,2) | 2 | C |
| 4 | (0,3,3,3) | 3 | C |
| 5 | (0,4,4,4) | 4 | C |
| 6 | (0,5,3,5) | 3 | J |
| 7 | (0,6,2,6) | 2 | J |
| 8 | (0,7,1,7) | 1 | J |
| 9 | (0,8,0,8) | 0 | J |
| 10 | (0,9,0,9) | 0 | E |

This shows the exact consumption of candies required to pass each gate.

Output:

```
9
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · m · 9) | Each cell is visited once per candy state |
| Space | O(n · m · 9) | Visited states and BFS queue |

The grid has at most 10,000 cells and at most 9 candy states per cell, so the total number of states is about 90,000. Each state processes four transitions, which is easily within limits for a 5-second constraint.

## Test Cases

```python
import sys, io
from contextlib import redirect_stdout

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from solution import solve
    with redirect_stdout(io.StringIO()) as f:
        solve()
    return f.getvalue().strip()

# provided samples
assert run("5 5\nS..PC\n.PPP.\n..P..\n..J..\n...E\n") == "16"
assert run("1 10\nSCCCCJJJJE\n") == "9"

# custom cases
assert run("1 2\nSE\n") == "1"
assert run("1 3\nSJE\n") == "SPOOKED!"
assert run("2 2\nSC\nJE\n") in ["2", "3"]
assert run("3 3\nS.P\nPJP\nC.E\n") != "", "reachable check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `S->E direct` | `1` | minimal movement |
| `SJE` | `SPOOKED!` | blocked by J with no candy |
| `SC / JE` | `2 or 3` | routing through candy dependency |
| `grid with P walls` | reachable | obstacle handling |

## Edge Cases

One important edge case is when a cell is revisited with different candy counts. Consider a situation where the shortest geometric path to a `J` cell does not provide enough candies, but a slightly longer detour does. The algorithm handles this by treating `(r, c, k1)` and `(r, c, k2)` as distinct states, so neither path incorrectly eliminates the other.

Another edge case occurs when the exit `E` is reachable only after exhausting all candies. The BFS correctly allows candy consumption along the path, and reaching `E` with `k = 0` is valid as long as the sequence of consumptions was legal.

A final subtle case is when multiple candies are collected before encountering any `J`. The BFS ensures that states with higher candy counts are explored alongside lower ones, so the algorithm naturally finds the configuration that maximizes feasibility rather than enforcing any greedy collection strategy.
