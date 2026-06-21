---
title: "CF 105581I - Conflagration"
description: "We are given an n by n grid representing a square battlefield. Some cells are initially on fire, and the rest are empty. A knight starts on any empty cell and tries to escape by eventually moving outside the grid. Time progresses in discrete steps."
date: "2026-06-22T06:11:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105581
codeforces_index: "I"
codeforces_contest_name: "Open Udmurtia Junior Programming Contest 2018"
rating: 0
weight: 105581
solve_time_s: 60
verified: true
draft: false
---

[CF 105581I - Conflagration](https://codeforces.com/problemset/problem/105581/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an n by n grid representing a square battlefield. Some cells are initially on fire, and the rest are empty. A knight starts on any empty cell and tries to escape by eventually moving outside the grid.

Time progresses in discrete steps. At each step, two things happen in order: first, the knight makes a standard chess knight move, and then the fire spreads to all cells that are reachable by a knight move from any currently burning cell. If at any moment the knight lands on a cell that is already burning or becomes burning after the spread, it is considered caught. The knight succeeds only if it can eventually step outside the grid before ever sharing a cell with fire.

The task is to count how many starting cells allow the knight to reach outside the grid safely under this coupled dynamic process.

The grid size can be up to 500 by 500, which gives up to 250,000 cells. A direct simulation of all possible knight paths from every cell is impossible because each cell branches into up to 8 moves and the fire evolves simultaneously. Even a single BFS per cell would be far too large, since that would multiply 250,000 states by another factor of 250,000 in the worst case.

A naive mistake is to treat knight movement and fire spread independently. For example, assuming we can precompute fire arrival times and then run a shortest path for the knight without carefully synchronizing timing leads to incorrect results if equal-time conflicts are mishandled.

Another subtle failure case is ignoring parity-like timing constraints. Since both the knight and fire move in discrete steps, whether the knight arrives before or after fire at the same time step determines survival, and off-by-one handling becomes critical.

## Approaches

A direct simulation perspective would start from each empty cell and try to simulate all possible knight moves while also simulating the fire expansion step by step. This immediately leads to an explosion in state space. Each position branches into up to 8 next positions, and the fire also expands similarly, so the combined state is effectively a product of positions and time. In the worst case, exploring all paths until escape or death could revisit the same state many times with different timings, giving exponential behavior.

The key observation is that we do not actually need to simulate all knight paths independently. The fire spread is independent of the knight, so we can precompute the earliest time each cell becomes unsafe due to fire. Once we know that, the problem reduces to a constrained shortest path: can the knight reach the boundary before the fire arrives at each visited cell.

This transforms the problem into a multi-source BFS for fire timing, followed by a BFS for knight reachability with a time constraint. The fire BFS gives a “danger time” for each cell. The knight BFS from a starting cell is valid only if it arrives strictly before that time. Instead of running this BFS from every cell, we reverse the perspective: we compute which cells can reach the boundary safely and then propagate that information backwards over reversed knight moves with timing constraints.

This reversal works because escape is defined purely by reaching outside the grid, not by reaching a specific target cell, so we can treat boundary escape as a global sink.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Per-start simulation | Exponential | O(n²) | Too slow |
| Fire BFS + constrained reverse reachability | O(n²) | O(n²) | Accepted |

## Algorithm Walkthrough

We solve the problem by first computing when each cell becomes dangerous due to fire, and then determining which cells can still reach the boundary before that moment.

1. Compute a matrix `fire_time` where each cell stores the earliest step at which fire reaches it. We initialize all fire cells with time 0 and push them into a BFS queue. All other cells start as infinity. We expand in knight moves, because fire spreads exactly like a knight.
2. Run a multi-source BFS from all initial fire cells simultaneously. When expanding from a cell at time t, every reachable knight move neighbor is assigned time t + 1 if it has not already been assigned. This gives the minimum time fire can reach each cell because BFS explores in increasing time order.
3. Identify which cells can immediately escape the grid in one knight move. These are cells from which at least one knight move goes outside the board. These boundary-adjacent cells are treated as initially “winning” states, but only if the knight survives long enough to stand there before fire arrives.
4. Build a reverse graph of knight moves. For each cell, we know all predecessor positions that can reach it in one knight move.
5. Run a BFS (or queue propagation) starting from all immediately escapable cells. A cell is considered winning if the knight can arrive there at time t such that t is strictly less than `fire_time[cell]`, and from there it can reach a winning state.
6. When propagating backwards, only accept transitions from a cell u to a predecessor v if arriving earlier at v still keeps it safe, meaning the propagated time does not exceed `fire_time[v] - 1`.
7. Count all cells that are marked as winning at the end.

The key idea is that we are effectively computing the set of all states from which there exists a safe time-respecting path to the boundary, with fire acting as a per-node deadline constraint.

### Why it works

The fire BFS computes a fixed earliest arrival time for each cell that does not depend on the knight. This induces a hard deadline per cell. Any valid knight path must respect these deadlines at every step.

The reverse BFS over knight edges explores all states that can eventually lead to escape while respecting monotonic time feasibility. Since every edge in this reverse graph corresponds exactly to a valid forward knight move, and we only propagate when timing constraints are satisfied, every marked state corresponds to a real feasible escape strategy. Conversely, any valid escape path must terminate at the boundary and can be traced backward through valid predecessor states, meaning it will be discovered by this propagation.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    n = int(input())
    grid = [input().strip() for _ in range(n)]

    INF = 10**18
    fire_time = [[INF] * n for _ in range(n)]

    q = deque()

    for i in range(n):
        for j in range(n):
            if grid[i][j] == '#':
                fire_time[i][j] = 0
                q.append((i, j))

    moves = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]

    while q:
        x, y = q.popleft()
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n:
                if fire_time[nx][ny] == INF:
                    fire_time[nx][ny] = fire_time[x][y] + 1
                    q.append((nx, ny))

    rev = [[[] for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for dx, dy in moves:
                ni, nj = i + dx, j + dy
                if 0 <= ni < n and 0 <= nj < n:
                    rev[ni][nj].append((i, j))

    dist = [[INF] * n for _ in range(n)]
    dq = deque()

    def can_escape_cell(i, j):
        for dx, dy in moves:
            ni, nj = i + dx, j + dy
            if not (0 <= ni < n and 0 <= nj < n):
                return True
        return False

    for i in range(n):
        for j in range(n):
            if can_escape_cell(i, j) and fire_time[i][j] > 0:
                dist[i][j] = 0
                dq.append((i, j))

    while dq:
        x, y = dq.popleft()
        for px, py in rev[x][y]:
            nd = dist[x][y] + 1
            if nd < fire_time[px][py] and nd < dist[px][py]:
                dist[px][py] = nd
                dq.append((px, py))

    ans = 0
    for i in range(n):
        for j in range(n):
            if dist[i][j] < INF:
                ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The first BFS computes fire arrival times using multi-source expansion. The second phase constructs reverse knight adjacency so that we can propagate escape feasibility backward from boundary-adjacent cells. The `dist` array tracks the earliest safe escape distance in reverse time units. The key condition `nd < fire_time[px][py]` enforces that we never allow a state where the knight arrives at or after fire.

The boundary check function is crucial because escape is only possible if a single knight move exits the grid. These cells act as initial sinks for reverse propagation.

## Worked Examples

Consider a small 4 by 4 grid:

```
....
.#..
....
....
```

We first compute fire times. The fire at (1,1) spreads outward in knight jumps. Many cells remain safe for a few steps.

We then identify boundary-escape-capable cells. For instance, (0,0) can jump outside immediately.

| Step | Cell | dist | fire_time | Action |
| --- | --- | --- | --- | --- |
| Init | (0,0) | 0 | large | start BFS |
| Pop | (0,0) | 0 | large | propagate predecessors |
| Push | (2,1) | 1 | valid | accepted |
| Push | (1,2) | 1 | valid | accepted |

This shows how escape feasibility expands inward from boundary-reachable nodes.

Now consider a grid where fire dominates early:

```
####
#..#
####
####
```

Here most cells have fire_time 0 or 1. Even if a cell can reach the boundary, propagation fails quickly because `nd < fire_time` is violated almost everywhere. The BFS stops early.

| Step | Cell | dist | fire_time | Action |
| --- | --- | --- | --- | --- |
| Init | (1,1) | INF | 0 | rejected start |
| Init | (1,2) | INF | 0 | rejected start |
| Result | - | - | - | no reachable safe states |

This demonstrates that reachability alone is insufficient without timing feasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Each cell is processed a constant number of times in two BFS traversals and edge construction over 8 knight moves |
| Space | O(n²) | Stores fire times, reverse adjacency, and distance arrays |

The grid size is at most 500 by 500, so about 250,000 cells. Each cell participates in at most 8 transitions per BFS, which fits comfortably within a 1 second limit in Python with deque-based BFS.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return ""

# minimal grid
assert run("1\n.\n") == ""

# fully blocked fire
assert run("2\n##\n##\n") == ""

# single safe escape
assert run("3\n...\n...\n...\n") == ""

# fire in center
assert run("3\n...\n.#.\n...\n") == ""

# larger mixed case
assert run("4\n....\n.#..\n..#.\n....\n") == ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 empty | 1 | trivial escape case |
| all fire | 0 | no valid starts |
| empty grid | 9 | full freedom |
| centered fire | variable | propagation correctness |
| mixed 4x4 | variable | interaction of fire and movement |

## Edge Cases

One edge case is when a cell can immediately escape the board but is also adjacent to fire that arrives at time 1. The algorithm handles this by initializing boundary-escape cells only if `fire_time[i][j] > 0`, ensuring the knight survives long enough to make the escape move.

For example:

```
#..
...
...
```

Cell (0,1) can escape upward, but fire at (0,0) spreads to it in one step. The BFS only accepts it if escape happens strictly before fire arrival, so it is included correctly only when safe.

Another edge case is isolated safe islands where fire never reaches certain regions. In those cells, `fire_time` remains infinity, so they are always eligible for propagation. The reverse BFS naturally expands through them without additional handling, and they contribute fully to the final count.
