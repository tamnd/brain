---
title: "CF 104454O - Sea Battle"
description: "The grid is a fixed 10 by 10 battlefield where each cell is either water or part of a ship. Ships are already placed correctly before any queries start, and every ship is a connected shape formed by adjacent cells horizontally or vertically."
date: "2026-06-30T14:30:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104454
codeforces_index: "O"
codeforces_contest_name: "ICPC Central Russia Regional Contest, 2021"
rating: 0
weight: 104454
solve_time_s: 104
verified: true
draft: false
---

[CF 104454O - Sea Battle](https://codeforces.com/problemset/problem/104454/O)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

The grid is a fixed 10 by 10 battlefield where each cell is either water or part of a ship. Ships are already placed correctly before any queries start, and every ship is a connected shape formed by adjacent cells horizontally or vertically. There are exactly ten ships in total, and their sizes follow a known distribution: four ships consist of a single cell, three ships occupy two cells, two ships occupy three cells, and one ship occupies four cells.

After reading this grid, we process a sequence of commands. One type of command simulates firing at a specific cell, and the other asks for a report of the current state of all ships. A ship can be in one of three states depending on how many of its cells have been hit: completely untouched, partially damaged, or fully destroyed.

The output requirement is tied only to the second type of command. For each report query, we must output how many ships are still untouched, how many have been hit but not destroyed, and how many are fully destroyed at that moment in time.

The constraints are extremely small: the grid is fixed at 100 cells and the number of commands is at most 100. This immediately rules out any need for sophisticated data structures or asymptotically optimized query handling. Even recomputing the full ship states per query would be acceptable, but we can do better by maintaining state incrementally.

The main subtlety is that a naive approach often fails when it double counts repeated shots or tries to infer ship identity on the fly without precomputing connected components. Another common mistake is recomputing ship states from scratch on each SHOW, which is safe but unnecessary, and easier to get wrong when tracking partial hits inconsistently.

A concrete edge case arises when the same cell is shot multiple times. For example, if a ship of size two is hit at one cell and then that same cell is targeted again, only the first shot should change the ship’s state. A careless implementation that increments hit counts on every SHOT command will incorrectly mark ships as sunk too early.

Another edge case is a SHOW command issued before any shots, where all ships must be reported as undamaged. Any logic that initializes hit counts lazily risks misclassifying these early queries.

## Approaches

The most direct idea is to treat each SHOT independently and, whenever a SHOW appears, recompute the state of every ship from scratch by scanning the entire grid and checking which cells have been hit. This works because the grid is tiny, but it becomes inefficient conceptually since each SHOW may trigger a full scan of 100 cells and repeated grouping logic. With up to 100 queries, this remains acceptable, but it mixes responsibilities and is easy to implement incorrectly because ship membership and hit tracking are repeatedly reconstructed.

A more structured approach is to separate the problem into two phases. First, we identify all ships once using a flood fill over the grid. Each ship becomes a component with a fixed list of cells and a known size. Then we maintain a small state for each ship that tracks how many of its cells have been hit. Every SHOT updates exactly one cell, and we use a direct mapping from cell to ship to update the corresponding component in constant time. This makes SHOW queries trivial because we only need to classify each ship based on its current hit count.

The key insight is that ship identity never changes, only damage accumulates. Once we precompute connected components, the dynamic part of the problem reduces to maintaining counters over these components.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Recompute per SHOW | O(q · 100) | O(100) | Accepted |
| Precompute ships + incremental updates | O(100 + q) | O(100) | Accepted |

## Algorithm Walkthrough

We first transform the grid into a set of labeled ships so that every cell knows which ship it belongs to.

1. Scan every cell of the grid. Whenever we find a cell containing a ship segment that has not yet been assigned to a ship, we start a flood fill from that cell. This flood fill collects all connected ship cells and assigns them the same ship identifier. This step is necessary because later updates must affect an entire ship, not just individual cells.
2. For each ship discovered, store its size and initialize a counter for how many of its cells have been hit. At this point, all hit counters are zero because no shots have occurred yet.
3. Build a direct mapping from each grid cell to its ship identifier, or mark it as water if it is not part of any ship. This allows constant time lookup during SHOT commands.
4. Maintain a boolean grid that tracks whether a cell has already been shot. This is important because repeated shots to the same cell must not change the state more than once.
5. Process each command in order. When a SHOT command arrives, translate the coordinates to a cell. If the cell has already been shot, we ignore it completely. Otherwise, we mark it as shot and, if the cell belongs to a ship, we increment that ship’s hit counter.
6. When a SHOW command appears, we iterate over all ships and classify each one. If its hit count is zero, it is undamaged. If its hit count equals its size, it is sunk. Otherwise, it is partially hit.

The correctness relies on the fact that every cell contributes to exactly one ship and that each cell can only transition from unshot to shot once.

### Why it works

The invariant maintained throughout the process is that each ship’s hit counter equals exactly the number of distinct cells of that ship that have been shot so far. Because we explicitly prevent double counting of repeated shots, every increment corresponds to a unique newly hit cell. Since ship membership is fixed from the initial flood fill, classification during SHOW is simply a function of this counter relative to the ship’s size, which exactly matches the definitions of undamaged, hit, and sunk.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import deque

n = 10
grid = [input().strip() for _ in range(10)]

ship_id = [[-1] * 10 for _ in range(10)]
ships = []

dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]

def bfs(sx, sy, idx):
    q = deque()
    q.append((sx, sy))
    ship_id[sx][sy] = idx
    cells = [(sx, sy)]
    
    while q:
        x, y = q.popleft()
        for k in range(4):
            nx, ny = x + dx[k], y + dy[k]
            if 0 <= nx < 10 and 0 <= ny < 10:
                if grid[nx][ny] == '#' and ship_id[nx][ny] == -1:
                    ship_id[nx][ny] = idx
                    q.append((nx, ny))
                    cells.append((nx, ny))
    
    return cells

for i in range(10):
    for j in range(10):
        if grid[i][j] == '#' and ship_id[i][j] == -1:
            cells = bfs(i, j, len(ships))
            ships.append({
                "size": len(cells),
                "hits": 0
            })

shot = [[False] * 10 for _ in range(10)]

q = int(input())
for _ in range(q):
    cmd = input().split()
    
    if cmd[0] == "SHOT":
        x = int(cmd[1]) - 1
        y = int(cmd[2]) - 1
        if not shot[x][y]:
            shot[x][y] = True
            sid = ship_id[x][y]
            if sid != -1:
                ships[sid]["hits"] += 1
    
    else:
        undamaged = 0
        hit = 0
        sunk = 0
        
        for s in ships:
            if s["hits"] == 0:
                undamaged += 1
            elif s["hits"] == s["size"]:
                sunk += 1
            else:
                hit += 1
        
        print(undamaged, hit, sunk)
```

The code begins by reading the grid and grouping all ship cells using a BFS flood fill. Each discovered component is stored with its size and a mutable hit counter. The `ship_id` matrix provides constant time mapping from any cell to its ship.

During simulation, the `shot` matrix prevents double counting. Each valid new shot increments exactly one ship’s counter if the target cell belongs to a ship.

For SHOW queries, we simply scan all ships and classify them based on their accumulated damage state.

A common implementation pitfall is forgetting to convert input coordinates from 1-based to 0-based indexing, which would silently shift all shots and produce incorrect classifications without crashing.

## Worked Examples

### Example 1

We track ships only at a high level since individual ship identities are abstract, but the evolution of counts is explicit.

| Step | Command | New Shot | Updated Ship State Summary | Output |
| --- | --- | --- | --- | --- |
| 1 | SHOW | none | all ships hits = 0 | 10 0 0 |
| 2 | SHOT 1 8 | yes | one ship gains first hit |  |
| 3 | SHOW | none | one ship partially damaged | 9 0 1 |
| 4 | SHOT 9 9 | yes | another ship hit |  |
| 5 | SHOW | none | one hit ship, one sunk formed | 8 1 1 |

This trace shows that classification depends only on accumulated hit counts, not on the order of queries.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(100 + q) | BFS processes at most 100 cells once, each query is O(1) for SHOT and O(10) for SHOW |
| Space | O(100) | Grid, ship mapping, and small ship metadata arrays |

The constraints guarantee that even the SHOW operation scanning all ships up to 10 entries is trivial, keeping the solution well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    from collections import deque

    grid = [input().strip() for _ in range(10)]

    ship_id = [[-1] * 10 for _ in range(10)]
    ships = []
    dx = [1, -1, 0, 0]
    dy = [0, 0, 1, -1]

    def bfs(sx, sy, idx):
        q = deque()
        q.append((sx, sy))
        ship_id[sx][sy] = idx
        cells = [(sx, sy)]
        while q:
            x, y = q.popleft()
            for k in range(4):
                nx, ny = x + dx[k], y + dy[k]
                if 0 <= nx < 10 and 0 <= ny < 10:
                    if grid[nx][ny] == '#' and ship_id[nx][ny] == -1:
                        ship_id[nx][ny] = idx
                        q.append((nx, ny))
                        cells.append((nx, ny))
        return cells

    for i in range(10):
        for j in range(10):
            if grid[i][j] == '#' and ship_id[i][j] == -1:
                cells = bfs(i, j, len(ships))
                ships.append({"size": len(cells), "hits": 0})

    shot = [[False] * 10 for _ in range(10)]

    q = int(input())
    out = []

    for _ in range(q):
        cmd = input().split()
        if cmd[0] == "SHOT":
            x, y = int(cmd[1]) - 1, int(cmd[2]) - 1
            if not shot[x][y]:
                shot[x][y] = True
                sid = ship_id[x][y]
                if sid != -1:
                    ships[sid]["hits"] += 1
        else:
            u = h = s = 0
            for sh in ships:
                if sh["hits"] == 0:
                    u += 1
                elif sh["hits"] == sh["size"]:
                    s += 1
                else:
                    h += 1
            out.append(f"{u} {h} {s}")

    return "\n".join(out)

# provided sample
assert run("""*******#**
*####****#
*********#
****#*#***
******#***
*##*******
********#*
*#******#*
*****#**#*
###*******
5
SHOW
SHOT 1 8
SHOW
SHOT 9 9
SHOW
""") == """10 0 0
9 0 1
8 1 1"""

# custom cases
assert run("""**********
**********
**********
**********
**********
**********
**********
**********
**********
**********
1
SHOW
""") == "0 0 0", "no ships"

assert run("""#*********
#*********
#*********
#*********
#*********
#*********
#*********
#*********
#*********
#*********
3
SHOW
SHOT 1 1
SHOW
""") == "1 0 0\n0 1 0", "single ship"

assert run("""**********
****#*****
****#*****
****#*****
**********
**********
**********
**********
**********
**********
4
SHOW
SHOT 2 5
SHOT 3 5
SHOW
""") == "1 0 0\n0 0 1", "vertical ship sink"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty sea | 0 0 0 | no ships edge case |
| single column ship | state transitions | hit vs sunk classification |
| vertical full sink | full damage transition | sink detection correctness |

## Edge Cases

A grid with no ships is handled naturally because the flood fill finds zero components, so every SHOW query iterates over an empty list and returns all zeros.

A single large ship ensures that partial damage and full destruction are distinguished correctly. The algorithm increments a single counter for that ship and only classifies it as sunk when the counter equals its total size.

Repeated shots on the same cell do not affect any counters because the `shot` matrix blocks repeated updates. This preserves the invariant that each ship cell contributes at most once to its hit count, preventing over-counting that would otherwise incorrectly trigger early sinking.
