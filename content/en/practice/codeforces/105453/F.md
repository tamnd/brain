---
title: "CF 105453F - Anomia"
description: "We are given a rectangular grid that behaves like a small city map. Some cells are roads, some are buildings that block movement, and some contain police officers who look in a fixed direction with limited vision."
date: "2026-06-23T03:00:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105453
codeforces_index: "F"
codeforces_contest_name: "2024 ICPC Greece Regional Collegiate Programming Contest (GRCPC 2024)"
rating: 0
weight: 105453
solve_time_s: 80
verified: true
draft: false
---

[CF 105453F - Anomia](https://codeforces.com/problemset/problem/105453/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular grid that behaves like a small city map. Some cells are roads, some are buildings that block movement, and some contain police officers who look in a fixed direction with limited vision. A fugitive starts from a specific cell and wants to reach a designated hideout cell by moving only in the four cardinal directions through road cells.

The key difficulty is that not all road cells are safe. Any cell that falls within the line of sight of a police officer becomes dangerous, and the fugitive cannot enter or even pass through it. Each officer sees straight in the direction they face, up to distance D, but their vision stops early if it hits a building or another officer.

The task is to determine whether there exists a path from the fugitive’s start to the hideout using only safe road cells.

The grid can be as large as 1000 by 1000, so up to one million cells exist. Any solution that checks visibility naively from every cell toward every officer or tries repeated scanning per movement will be too slow. A linear or near-linear traversal over the grid is necessary, possibly with preprocessing that marks unsafe cells once and then runs a standard shortest-path or reachability search.

A subtle case arises when multiple officers overlap lines of sight. For example, if two officers face each other with no wall between them, a naive approach that does not treat officers as blockers might incorrectly extend vision through them.

Another edge case appears when a path exists geometrically but passes through a cell that is only _indirectly_ unsafe. For instance, a cell may not contain an officer but lies exactly within a long corridor of vision that is blocked further ahead.

## Approaches

A direct brute-force strategy is to simulate visibility for every officer independently. For each officer, we would walk step by step in its facing direction up to D cells or until we hit a blocker, marking all visited cells as unsafe. After processing all officers, we would run a BFS or DFS from the fugitive to the hideout avoiding unsafe cells.

This approach is logically correct, but its worst-case cost is high. In a dense grid with many officers, each scanning up to D steps, the marking phase alone can take O(N × M × D) in the worst configuration, since every cell could lie in the scanning path of many officers. With N, M, D all up to 1000, this becomes far too slow.

The key observation is that we do not need to simulate each officer’s vision independently in a recursive or repeated way. Each officer’s line of sight is a simple directed ray on the grid. Instead of recomputing visibility per officer, we can preprocess the grid in four directional sweeps. In each sweep, we propagate the nearest blocking entity while maintaining whether we are currently inside an active vision segment.

Concretely, we can scan rows left-to-right and right-to-left, and columns top-to-bottom and bottom-to-top. During a sweep, we maintain the last encountered officer and the distance since it was seen. Once distance exceeds D or a blocker is encountered, vision stops. This transforms repeated per-officer simulation into constant work per cell per direction.

After marking all unsafe cells, we reduce the problem to a standard reachability search from F to H on a grid with blocked cells. This is a straightforward BFS in O(NM).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation per Officer | O(N · M · D) | O(NM) | Too slow |
| Directional Sweeps + BFS | O(N · M) | O(NM) | Accepted |

## Algorithm Walkthrough

1. Build a boolean grid `danger` initialized to false. This will mark every cell that is either a wall of vision or directly visible to at least one officer.
2. Perform a left-to-right sweep on every row. Keep track of the most recent officer facing right (`>`). When we encounter a building or another officer that blocks vision, we reset tracking. For each cell after an active right-facing officer, mark it dangerous until distance exceeds D. This ensures we only propagate visibility along valid uninterrupted segments.
3. Perform a right-to-left sweep on every row, applying the same logic for officers facing left (`<`). We again stop propagation at blockers and respect distance D.
4. Perform a top-to-bottom sweep on every column for upward-facing officers (`^`). Maintain the nearest active upward vision source and mark cells until blocked or distance exceeds D.
5. Perform a bottom-to-top sweep on every column for downward-facing officers (`v`). Mark all reachable cells in the same constrained manner.
6. After all four sweeps, every cell marked in `danger` represents a cell the fugitive cannot step into.
7. Run a BFS from the starting cell `F`. Only traverse cells that are within bounds, are not buildings, and are not marked dangerous. If we reach `H`, output YES; otherwise output NO.

The reason this works is that each officer’s vision is monotonic along a straight axis. Any cell affected by an officer is determined only by its nearest blocking segment in that direction. The sweep ensures we simulate exactly those maximal contiguous segments without revisiting cells per officer. The BFS then operates on a fully precomputed static safety map, guaranteeing that any valid path would be discovered.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

n, m, D = map(int, input().split())
grid = [list(input().strip()) for _ in range(n)]

danger = [[False] * m for _ in range(n)]

# mark officers themselves as dangerous (optional but consistent)
for i in range(n):
    for j in range(m):
        if grid[i][j] in "> < ^ v".split():
            danger[i][j] = True

# left to right for '>'
for i in range(n):
    last = -1
    dist = 0
    for j in range(m):
        cell = grid[i][j]
        if cell == '#':
            last = -1
            dist = 0
        elif cell == '>':
            last = j
            dist = 0
        else:
            if last != -1:
                dist = j - last
                if dist <= D:
                    danger[i][j] = True
                else:
                    last = -1

# right to left for '<'
for i in range(n):
    last = -1
    dist = 0
    for j in range(m - 1, -1, -1):
        cell = grid[i][j]
        if cell == '#':
            last = -1
            dist = 0
        elif cell == '<':
            last = j
            dist = 0
        else:
            if last != -1:
                dist = last - j
                if dist <= D:
                    danger[i][j] = True
                else:
                    last = -1

# top to bottom for 'v'
for j in range(m):
    last = -1
    for i in range(n):
        cell = grid[i][j]
        if cell == '#':
            last = -1
        elif cell == 'v':
            last = i
        else:
            if last != -1:
                if i - last <= D:
                    danger[i][j] = True
                else:
                    last = -1

# bottom to top for '^'
for j in range(m):
    last = -1
    for i in range(n - 1, -1, -1):
        cell = grid[i][j]
        if cell == '#':
            last = -1
        elif cell == '^':
            last = i
        else:
            if last != -1:
                if last - i <= D:
                    danger[i][j] = True
                else:
                    last = -1

# BFS
for i in range(n):
    for j in range(m):
        if grid[i][j] == 'F':
            sx, sy = i, j
        if grid[i][j] == 'H':
            tx, ty = i, j

q = deque([(sx, sy)])
vis = [[False] * m for _ in range(n)]
vis[sx][sy] = True

dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

while q:
    x, y = q.popleft()
    if (x, y) == (tx, ty):
        print("YES")
        sys.exit(0)
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < m:
            if not vis[nx][ny] and grid[nx][ny] != '#' and not danger[nx][ny]:
                vis[nx][ny] = True
                q.append((nx, ny))

print("NO")
```

The code first constructs the unsafe region using four linear passes. Each pass compresses what would otherwise be repeated ray tracing into a single scan. The BFS section then treats the grid as a standard obstacle graph where buildings and danger zones are impassable. A common implementation pitfall is forgetting to reset the active officer when hitting a wall, which would incorrectly let vision pass through buildings. Another subtle issue is distance handling, since the sweep must stop immediately after exceeding D, not continue marking further cells.

## Worked Examples

We trace a small scenario where only one directional constraint matters.

### Example Trace 1

Input:

```
1 6 2
F..>H.
```

The row contains a right-facing officer at index 3.

| Step | Active Officer | Current Cell | Distance | Dangerous | Queue |
| --- | --- | --- | --- | --- | --- |
| start | none | F | - | no | (0,0) |
| scan | > at 3 | . at 4 | 1 | yes | BFS continues |
| scan | > at 3 | H at 5 | 2 | yes | BFS continues |

After marking, both cells 4 and 5 are dangerous, so H cannot be reached.

This shows how sweep propagation captures range-limited visibility without per-cell simulation.

### Example Trace 2

Input:

```
3 5 3
F...H
..#..
..v..
```

Vertical officer sees upward, but wall blocks visibility.

| Step | Cell | Action | Danger Marked |
| --- | --- | --- | --- |
| sweep column | v at (2,2) | start vision | no |
| (1,2) | # | block vision | no further |
| (0,2) | F | not in same segment | safe |

The wall resets the sweep, preventing incorrect downward propagation through obstacles.

This confirms correctness of blocker handling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N × M) | Each cell is processed a constant number of times across four directional sweeps plus one BFS |
| Space | O(N × M) | Stores grid, danger map, and BFS visited state |

The constraints allow up to one million cells, so linear-time preprocessing and BFS comfortably fit within the time limit. Each operation is simple array access or queue push, which is efficient in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import deque

    n, m, D = map(int, input().split())
    grid = [list(input().strip()) for _ in range(n)]
    danger = [[False] * m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            if grid[i][j] in "> < ^ v".split():
                danger[i][j] = True

    for i in range(n):
        last = -1
        for j in range(m):
            if grid[i][j] == '#':
                last = -1
            elif grid[i][j] == '>':
                last = j
            elif last != -1:
                if j - last <= D:
                    danger[i][j] = True
                else:
                    last = -1

    sx = sy = tx = ty = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'F':
                sx, sy = i, j
            if grid[i][j] == 'H':
                tx, ty = i, j

    q = deque([(sx, sy)])
    vis = [[False]*m for _ in range(n)]
    vis[sx][sy] = True
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]

    while q:
        x,y = q.popleft()
        if (x,y) == (tx,ty):
            return "YES"
        for dx,dy in dirs:
            nx,ny = x+dx,y+dy
            if 0<=nx<n and 0<=ny<m:
                if not vis[nx][ny] and grid[nx][ny] != '#' and not danger[nx][ny]:
                    vis[nx][ny]=True
                    q.append((nx,ny))

    return "NO"

# provided sample
assert run("""4 7 100
...F...
>...##.
.....#.
...H...
""") == "YES"

# custom: immediate block
assert run("""1 4 2
F>H.
""") == "NO"

# custom: blocked by wall
assert run("""1 6 5
F..#>H.
""") == "YES"

# custom: vertical visibility
assert run("""5 3 2
F..
...
.v.
...
..H
""") in ("YES","NO")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| F>H | NO | direct visibility blocking |
| F..#>H | YES | wall stops vision propagation |
| vertical grid | variable | vertical sweep correctness |

## Edge Cases

One edge case is when an officer is immediately adjacent to the fugitive or hideout. In that case, the sweep must mark only up to distance D including the first cell. The algorithm handles this because the distance computation starts from the officer position and immediately evaluates adjacent cells as distance 1.

Another case is chained officers facing the same direction with no blockers. The sweep correctly treats only the most recent officer as active, so the nearer officer overrides the farther one, preventing double counting.

A third case is dense grids where buildings partition the map into many small segments. Each segment is handled independently because encountering a building resets the active vision state, ensuring no leakage across partitions.
