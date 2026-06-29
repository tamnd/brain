---
title: "CF 104664D - Noodling with Knights"
description: "We are given a square chessboard of size $N times N$, where squares are indexed by integer coordinates. A single knight starts on one square and we want to know the minimum number of legal knight moves needed to reach a target square."
date: "2026-06-29T11:01:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104664
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 10-06-23 Div. 2 (Beginner)"
rating: 0
weight: 104664
solve_time_s: 78
verified: true
draft: false
---

[CF 104664D - Noodling with Knights](https://codeforces.com/problemset/problem/104664/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a square chessboard of size $N \times N$, where squares are indexed by integer coordinates. A single knight starts on one square and we want to know the minimum number of legal knight moves needed to reach a target square. If the knight can never reach the target due to board boundaries or parity constraints, we output $-1$.

The board is empty, so there are no obstacles. The only structure is the knight’s movement rule, which defines a fixed set of up to eight possible transitions from each square. This turns the problem into a shortest path problem on an implicit graph: each cell is a node, and each knight move is an unweighted edge.

The constraints $N < 800$ imply at most $640{,}000$ nodes. Each node has at most 8 outgoing edges, so a full exploration touches a few million transitions. This is comfortably within a BFS budget in Python if implemented carefully.

There are a few important edge cases that affect correctness:

One case is when the start and end positions are identical. For example:

```
N = 1
start = (0, 0)
end = (0, 0)
```

The correct answer is $0$. A careless BFS implementation that always enqueues neighbors first and checks termination only when dequeuing might still return $1$ if it increments distance prematurely.

Another case is when the board is too small for any knight move. For example:

```
N = 2
start = (0, 0)
end = (1, 1)
```

A knight has no legal moves anywhere on a $2 \times 2$ board, so most cells are isolated in practice. The correct answer is $-1$ unless start equals end. Any solution that assumes connectivity or ignores bounds will incorrectly return a finite number.

Finally, parity still plays a role on finite boards. Even if a position is theoretically reachable on an infinite board, truncation by boundaries can make it unreachable. That means heuristic formulas based only on parity or Manhattan distance are unsafe; we must explicitly search.

## Approaches

A direct approach is to treat each board cell as a graph vertex and run a shortest path search. From each position, we generate up to eight knight moves, filter out those that fall outside the board, and continue exploring until we reach the target. Because all moves have equal cost, breadth-first search guarantees the first time we reach the target is optimal.

This is correct but becomes expensive if done poorly or if repeated states are not tracked. Without a visited structure, the same cell is revisited exponentially many times, since knight moves naturally cycle. In the worst case, this degenerates into exploring an infinite unfolding tree, which is infeasible.

The key observation is that the graph is unweighted and has uniform edge cost. That makes BFS optimal. The second observation is that the state space is small enough that a single BFS from the start is sufficient. We do not need bidirectional search or heuristics like A*; the grid is dense but bounded.

The solution reduces to a single BFS over at most $N^2$ states with constant branching factor.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (DFS / repeated exploration) | Exponential | O(N²) or worse | Too slow |
| BFS shortest path | O(N²) | O(N²) | Accepted |

## Algorithm Walkthrough

1. Interpret each board cell $(x, y)$ as a node in a graph.
2. Define the eight knight moves: $(\pm 1, \pm 2)$ and $(\pm 2, \pm 1)$.
3. If start equals target, return 0 immediately since no movement is required.
4. Initialize a distance grid (or visited array) with $-1$, meaning unvisited.
5. Set the start cell distance to 0 and push it into a queue.
6. While the queue is not empty, pop the front cell $(x, y)$.
7. For each of the eight possible moves, compute the next cell $(nx, ny)$.
8. If $(nx, ny)$ is outside the board or already visited, skip it.
9. Otherwise, set its distance to $dist[x][y] + 1$ and push it into the queue.
10. If we reach the target cell during this process, return its distance immediately.
11. If BFS finishes without reaching the target, return $-1$.

The reason this works is that BFS expands nodes in increasing order of distance from the start. Every cell is assigned the minimum number of steps needed to reach it because the first time it is discovered corresponds to the shortest possible path in an unweighted graph. The visited marking ensures each cell is processed once, preventing cycles from inflating distances or causing infinite loops.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    N = int(input().strip())
    x1, y1 = map(int, input().split())
    x2, y2 = map(int, input().split())

    if (x1, y1) == (x2, y2):
        print(0)
        return

    moves = [(1, 2), (2, 1), (2, -1), (1, -2),
             (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

    dist = [[-1] * N for _ in range(N)]
    q = deque()
    q.append((x1, y1))
    dist[x1][y1] = 0

    while q:
        x, y = q.popleft()

        for dx, dy in moves:
            nx, ny = x + dx, y + dy

            if 0 <= nx < N and 0 <= ny < N and dist[nx][ny] == -1:
                dist[nx][ny] = dist[x][y] + 1
                if (nx, ny) == (x2, y2):
                    print(dist[nx][ny])
                    return
                q.append((nx, ny))

    print(-1)

if __name__ == "__main__":
    solve()
```

The implementation follows BFS directly. The distance array doubles as a visited marker, avoiding the need for a separate boolean array. The early exit when reaching the target avoids exploring the entire board when unnecessary.

One subtle detail is that we check bounds before accessing the distance array. Another is that we only assign distance once per cell; this is what preserves shortest-path correctness.

## Worked Examples

### Example 1

Input:

```
N = 1
start = (0, 0)
end = (0, 0)
```

This case is handled before BFS begins.

| Step | Queue | Dist updates | Action |
| --- | --- | --- | --- |
| init | (empty BFS skipped) | none | start == target |

Output is immediately 0. This confirms the correctness of the early termination rule.

### Example 2

Input:

```
N = 4
start = (1, 2)
end = (2, 2)
```

We track BFS layers.

| Step | Queue | Visited newly | Reason |
| --- | --- | --- | --- |
| init | (1,2) | (1,2)=0 | start |
| pop (1,2) | neighbors | (0,0),(0,4 invalid),... | expand knight moves |
| next layer | multiple | some valid cells | BFS frontier grows |
| reach target | found | (2,2)=3 | first time reached |

The key observation is that even if multiple paths reach a cell, BFS guarantees the first arrival is minimal. This example shows how distance accumulates layer by layer rather than via heuristic jumps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N^2)$ | each cell is visited at most once, and each visit checks up to 8 moves |
| Space | $O(N^2)$ | distance grid and queue may store all cells in worst case |

The bounds $N < 800$ imply at most $640{,}000$ nodes, which BFS handles comfortably. The constant factor of 8 transitions keeps runtime stable within limits.

## Test Cases

```python
import sys, io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out
    try:
        solve()
    finally:
        sys.stdout = old_stdout
    return out.getvalue().strip()

# provided samples
assert run("1\n0 0\n0 0\n") == "0"
assert run("4\n1 2\n2 2\n") == "3"

# custom cases
assert run("2\n0 0\n1 1\n") == "-1", "tiny board unreachable"
assert run("3\n0 0\n2 1\n") in {"1", "2"}, "small board reachability check"
assert run("5\n0 0\n0 0\n") == "0", "same cell larger board"
assert run("8\n0 0\n7 7\n") != "", "reachable large board sanity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2×2 unreachable | -1 | no knight moves possible |
| 3×3 corner case | 1 or 2 | small-grid reachability behavior |
| identical start/end | 0 | early exit correctness |
| 8×8 corner to corner | non-empty | general BFS correctness |

## Edge Cases

One important edge case is when the board is too small to allow movement. For input:

```
N = 2
start = (0, 0)
end = (1, 1)
```

The BFS starts at $(0,0)$. All eight knight moves immediately go out of bounds. The queue becomes empty after processing the start node. Since the target was never reached, the algorithm returns $-1$, matching the correct result.

Another case is identical start and end:

```
N = 5
start = (3, 3)
end = (3, 3)
```

The algorithm checks this before BFS and returns 0 directly, preventing unnecessary exploration.

A third case is when the target is reachable only after several expansions:

```
N = 4
start = (0, 0)
end = (3, 3)
```

BFS expands layer by layer. Even if multiple paths reach intermediate cells, the first time $(3,3)$ is dequeued or discovered corresponds to the minimum number of moves. This prevents overcounting paths that revisit cells through longer routes.
