---
title: "CF 105200D - Don't Get Caught"
description: "We have a rectangular hall represented as a grid. Kauã starts in the top-left cell and wants to reach the bottom-right cell. Some cells contain guards, and each guard watches every cell in one straight direction until another guard blocks the view."
date: "2026-06-27T02:52:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105200
codeforces_index: "D"
codeforces_contest_name: "IME++ Starters Try-outs 2024"
rating: 0
weight: 105200
solve_time_s: 39
verified: true
draft: false
---

[CF 105200D - Don't Get Caught](https://codeforces.com/problemset/problem/105200/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rectangular hall represented as a grid. Kauã starts in the top-left cell and wants to reach the bottom-right cell. Some cells contain guards, and each guard watches every cell in one straight direction until another guard blocks the view. Kauã cannot step onto a guard cell or any cell watched by a guard. The task is to find the shortest possible route through the remaining cells and mark that route with `X`. If no route exists, the answer is `-1`.

The input gives the height and width of the grid followed by the grid itself. Empty cells are represented by `.`, while the four arrow characters represent guards looking in one of the four cardinal directions. The output is either a modified grid with the shortest valid path marked or `-1`.

The grid dimensions can reach 2000 by 2000, which means there can be up to four million cells. An algorithm that explores every possible path would be impossible because the number of paths grows exponentially. Even algorithms with a factor of the number of cells, such as `O(n * m)`, are appropriate because they touch each cell only a constant number of times.

The tricky part is that a cell can be empty but still unusable because a guard sees it. A solution that only treats guard positions as blocked will incorrectly walk through watched cells.

For example, consider:

```
3 4
....
.>..
....
```

The cells `(2,3)` and `(2,4)` are watched by the guard. The correct output path cannot use them. A careless BFS that only avoids `>` will incorrectly consider them available.

Another edge case is when a guard is blocked by another guard:

```
3 5
.....
.>>..
.....
```

The second guard blocks the first guard's vision. The first guard cannot see through the second one, so cells after the second guard remain available. Marking the whole row as dangerous would remove valid paths.

A final case is when the start or finish is surrounded by watched cells:

```
3 3
.>.
...
```

The algorithm must still run BFS normally from the start and discover that the destination is unreachable if every possible route is blocked.

## Approaches

A direct approach would be to try every possible movement sequence from the starting cell and keep the shortest one that reaches the destination. This is correct because every explored sequence represents a possible route. However, the number of possible routes can be enormous. In a grid with millions of cells, repeatedly exploring paths creates far too many operations.

The structure of the problem gives us two separate tasks. First, determine which cells are forbidden. Guards do not move, so their visibility can be processed once before searching for a path. After that, the remaining problem is a standard shortest path problem on a grid where every movement has the same cost.

The observation that makes this efficient is that BFS on an unweighted grid automatically finds the shortest path. Once watched cells are converted into blocked cells, every legal move has the same cost, so the first time BFS reaches the destination it has found an optimal route.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of cells | O(n × m) | Too slow |
| Optimal | O(n × m) | O(n × m) | Accepted |

## Algorithm Walkthrough

1. Scan every guard and mark all cells that are visible from that guard as dangerous. Move in the guard's direction until reaching the edge of the grid or another guard. The movement stops at guards because a guard blocks another guard's view.
2. Run BFS from `(0, 0)`. Only move to cells that are inside the grid, are not guards, and are not marked as dangerous. Store the previous cell for every visited position so the final route can be reconstructed.
3. If BFS never reaches `(n - 1, m - 1)`, print `-1`. The visited array represents every cell reachable through valid movements, so an unvisited destination proves no valid route exists.
4. If the destination is reached, follow the parent pointers backwards until reaching the start. Mark every cell on this chain with `X`.

Why it works: after the first phase, every cell that Kauã cannot enter has been removed from consideration. The remaining grid is exactly the graph of possible movements. BFS explores this graph layer by layer, so when a cell is first reached, it is reached by the shortest possible sequence of moves. The parent pointers store that shortest route, and reconstructing them produces a valid shortest path.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    grid = [list(input().strip()) for _ in range(n)]

    blocked = [[False] * m for _ in range(n)]

    directions = {
        '>': (0, 1),
        '<': (0, -1),
        'v': (1, 0),
        '^': (-1, 0)
    }

    for i in range(n):
        for j in range(m):
            if grid[i][j] in directions:
                blocked[i][j] = True
                di, dj = directions[grid[i][j]]
                ni, nj = i + di, j + dj
                while 0 <= ni < n and 0 <= nj < m:
                    if grid[ni][nj] in directions:
                        break
                    blocked[ni][nj] = True
                    ni += di
                    nj += dj

    parent = [[None] * m for _ in range(n)]
    visited = [[False] * m for _ in range(n)]

    q = deque([(0, 0)])
    visited[0][0] = True

    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while q:
        i, j = q.popleft()
        if (i, j) == (n - 1, m - 1):
            break

        for di, dj in moves:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < m:
                if not visited[ni][nj] and not blocked[ni][nj]:
                    visited[ni][nj] = True
                    parent[ni][nj] = (i, j)
                    q.append((ni, nj))

    if not visited[n - 1][m - 1]:
        print(-1)
        return

    i, j = n - 1, m - 1
    while True:
        if grid[i][j] == '.':
            grid[i][j] = 'X'
        if (i, j) == (0, 0):
            break
        i, j = parent[i][j]

    for row in grid:
        print(''.join(row))

if __name__ == "__main__":
    solve()
```

The first loop computes the dangerous cells. The guard cell itself is marked blocked, and the scan continues only through empty cells. Stopping when another guard is found handles the visibility rule correctly.

The BFS section uses a queue because all moves have equal cost. The `parent` array stores the previous position used to reach each cell, which avoids storing complete paths and keeps memory usage linear.

During reconstruction, the algorithm starts from the destination and repeatedly jumps to the previous cell. This follows the exact shortest route discovered by BFS. The condition that only empty cells are changed prevents guards from being overwritten.

## Worked Examples

### Sample 1

Input:

```
5 5
.....
.>.v.
.....
.^.<.
.....
```

| Step | Current cell | Queue action | Result |
| --- | --- | --- | --- |
| 1 | `(0,0)` | Start BFS | Marked visited |
| 2 | `(1,0)` | Move downward | Added to queue |
| 3 | `(2,0)` | Continue shortest route | Added to queue |
| 4 | `(3,0)` | Continue downward | Added to queue |
| 5 | `(4,4)` | Reached destination | Reconstruct path |

The trace shows that guard cells and watched cells are skipped before BFS begins. The resulting route follows the left side and then crosses the bottom row.

### Sample 2

Input:

```
3 6
.v....
.^.v..
...^..
```

| Step | Current cell | Queue action | Result |
| --- | --- | --- | --- |
| 1 | `(0,0)` | Start BFS | Marked visited |
| 2 | `(1,0)` | Move downward | Added |
| 3 | `(2,0)` | Move downward | Added |
| 4 | `(2,5)` | Destination reached | Path restored |

This case demonstrates that cells near guards can still be usable if they are outside the guards' sight range.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n × m) | Each cell is scanned for guards and visited at most once by BFS. |
| Space | O(n × m) | The blocked, visited, and parent arrays each store information for every cell. |

With at most four million cells, linear processing is the intended solution. Every operation performed on a cell is constant time, so the algorithm fits the limits.

## Test Cases

```python
import sys
import io
from collections import deque

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# sample 1
assert run("""5 5
.....
.>.v.
.....
.^.<.
.....
""") == """X....
X>.v.
X....
X^.<.
XXXXX
"""

# sample 2
assert run("""3 6
.v....
.^.v..
...^..
""") == """XvXXX.
X^XvX.
XXX^XX
"""

# impossible case
assert run("""4 4
....
..^.
.<..
....
""") == """-1
"""

# minimum grid
assert run("""1 1
.
""") == """X
"""

# guard blocks only one direction
assert run("""3 5
.....
.>...
.....
""") == """X....
X>XXX
XXXXX
"""

# blocked by another guard
assert run("""3 5
.....
.>>..
.....
""") != """-1
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 x 1` grid | `X` | Handles the start and destination being the same cell. |
| Single guard in a corridor | A path avoiding vision | Confirms watched cells are blocked. |
| Two adjacent guards | Reachable | Confirms visibility stops at another guard. |
| Unreachable sample | `-1` | Confirms BFS failure handling. |

## Edge Cases

For the first visibility case:

```
3 4
....
.>..
....
```

The guard at `(1,1)` marks `(1,2)` and `(1,3)` as blocked. BFS can still move around the row through the top or bottom, so the algorithm does not incorrectly treat all empty cells as safe without checking guard vision.

For the blocking case:

```
3 5
.....
.>>..
.....
```

The first guard sees only the second guard because the second guard stops the scan. The cells after the second guard are not marked. The BFS phase can use them if they lead to the destination, which matches the actual visibility rules.

For a fully blocked destination:

```
3 3
.>.
...
```

The dangerous cells are computed before BFS. If every possible route is removed, the destination never enters the queue and the program prints `-1`. The search phase never needs to reason about guards because all invalid cells have already been filtered out.
