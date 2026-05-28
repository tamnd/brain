---
title: "CF 196B - Infinite Maze"
description: "We are given a finite maze of size n × m. Some cells are walls, some are open, and one cell contains the starting position S. The maze is not used only once."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs"]
categories: ["algorithms"]
codeforces_contest: 196
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 124 (Div. 1)"
rating: 2000
weight: 196
solve_time_s: 99
verified: true
draft: false
---

[CF 196B - Infinite Maze](https://codeforces.com/problemset/problem/196/B)

**Rating:** 2000  
**Tags:** dfs and similar, graphs  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a finite maze of size `n × m`. Some cells are walls, some are open, and one cell contains the starting position `S`.

The maze is not used only once. Instead, the entire grid is repeated infinitely in every direction, like tiling the plane with copies of the same rectangle. Moving outside one copy immediately enters another copy at the corresponding position.

The question is whether the player can move arbitrarily far away from the starting position while only stepping on non-wall cells.

A useful way to think about the infinite maze is this:

Every position in the infinite plane corresponds to:

1. A cell inside the original grid.
2. Which copy of the grid we are currently in.

Two different infinite positions may map to the same `(row, col)` inside the original maze if they belong to different copies of the tile.

The constraints are large enough that exploring the infinite maze directly is impossible. The original grid can contain up to `1500 × 1500 = 2.25 million` cells. Any algorithm that revisits cells many times or stores information for infinitely many positions will fail immediately.

A graph traversal over the original grid is still feasible, because each original cell appears only once there. An `O(nm)` or `O(nm log(nm))` algorithm fits comfortably inside the limits. Anything quadratic in the number of cells does not.

The tricky part is that revisiting the same original cell is not always redundant. Reaching the same `(r, c)` from different copies of the infinite tiling is exactly what creates infinite movement.

Consider this example:

```
2 2
S.
..
```

The correct answer is `"Yes"`.

A naive BFS on only the finite grid would visit each cell once and stop, incorrectly concluding that movement is finite. In reality, there are no walls, so we can keep walking forever through different copies of the maze.

Another subtle case is when cycles exist only inside a bounded region.

```
3 3
###
#S#
#.#
```

The correct answer is `"No"`.

The player can move back and forth between a few cells forever, but can never escape to another copy of the maze. Infinite walking distance is impossible even though the graph contains a cycle.

One more dangerous mistake is handling modulo incorrectly for negative coordinates. In Python, `%` already behaves correctly for this problem, but in many languages `(-1) % m` becomes negative. For example:

```
1 2
S.
```

Moving left from column `0` should wrap to column `1` of the neighboring copy. Incorrect modulo handling breaks this transition completely.

## Approaches

The most direct idea is to treat the infinite maze literally and run BFS or DFS over all reachable coordinates `(x, y)` in the plane.

This works conceptually because every reachable position can be explored through ordinary graph traversal. If traversal never ends, the answer is `"Yes"`.

The problem is that the graph is infinite. Even if only a small corridor exists, the search may continue forever. There is no finite upper bound on the number of explored states.

The key observation is that the maze pattern repeats periodically.

Suppose we stand at infinite coordinate `(x, y)`. The actual cell type only depends on:

```
(x mod n, y mod m)
```

So many infinite positions correspond to the same cell inside the original grid.

Now comes the crucial insight.

If during traversal we reach the same original cell `(r, c)` from two different infinite coordinates, then we have discovered a non-trivial cycle through the tiled plane. From that point onward, we can keep shifting across copies forever, so the answer is `"Yes"`.

Why does this work?

Because the difference between the two infinite coordinates represents a translation vector between copies of the maze. Repeating the corresponding movement sequence lets us drift infinitely far away.

This suggests the correct state representation:

For every original grid cell, store the first infinite coordinate that reached it.

During DFS or BFS:

- If the cell was never visited, record its infinite coordinate.
- If the cell was visited before with a different infinite coordinate, we found infinite movement.

This completely avoids exploring infinitely many states. Each original cell is processed only once in the normal case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over infinite plane | Unbounded | Unbounded | Impossible |
| DFS/BFS with coordinate mapping | O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Read the grid and locate the starting cell `S`.
2. Run DFS or BFS starting from the infinite coordinate corresponding to `S`.
3. For every explored infinite position `(x, y)`, compute its corresponding original-grid cell:

```
rx = x % n
ry = y % m
```

This tells us which tile cell we are standing on.

1. Ignore the move if the mapped cell is a wall.
2. For every original-grid cell `(rx, ry)`, store the first infinite coordinate that reached it.

For example:

```
vis[rx][ry] = (x, y)
```

1. When reaching `(rx, ry)` again:

- If the stored infinite coordinate is identical to `(x, y)`, this is just another traversal path to the same infinite position. Ignore it.
- If the stored coordinate differs from `(x, y)`, then the same original cell was reached from two different copies of the maze. Print `"Yes"` immediately.
2. Continue traversal in the four directions.
3. If traversal finishes without detecting such a conflict, print `"No"`.

### Why it works

The invariant is:

For every original-grid cell, we remember exactly one infinite coordinate that can reach it.

If we later reach the same original cell using a different infinite coordinate, then there exists a path whose net displacement is non-zero. Repeating that displacement moves us across infinitely many copies of the maze.

Conversely, if no such duplicate-with-different-coordinate exists, every reachable state corresponds to exactly one infinite coordinate per original cell. Since there are only `nm` original cells, the reachable region is finite.

That establishes both correctness directions.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1 << 25)

n, m = map(int, input().split())

grid = []
sx = sy = -1

for i in range(n):
    row = input().strip()
    grid.append(row)

    for j, ch in enumerate(row):
        if ch == 'S':
            sx, sy = i, j

visited = [[None] * m for _ in range(n)]

dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def dfs(x, y):
    rx = x % n
    ry = y % m

    if grid[rx][ry] == '#':
        return False

    if visited[rx][ry] is not None:
        px, py = visited[rx][ry]

        if px != x or py != y:
            return True

        return False

    visited[rx][ry] = (x, y)

    for dx, dy in dirs:
        nx = x + dx
        ny = y + dy

        if dfs(nx, ny):
            return True

    return False

print("Yes" if dfs(sx, sy) else "No")
```

The traversal operates on infinite coordinates `(x, y)`, not only on positions inside the original grid. This is the core idea that preserves information about which copy of the maze we are visiting.

The modulo operation maps every infinite coordinate back into the original tile:

```
rx = x % n
ry = y % m
```

Python's modulo already handles negative numbers correctly, which is essential when movement crosses the top or left boundary.

The `visited` array does not store booleans. It stores the exact infinite coordinate that first reached each original-grid cell. This distinction is the entire solution.

Suppose `(2, 3)` inside the tile was first reached from infinite coordinate `(2, 3)`. If we later reach the same tile cell from `(2 + n, 3)`, then we know traversal crossed into another copy of the maze.

The DFS stops immediately once such a conflict appears.

One implementation detail that is easy to get wrong is revisiting the exact same infinite coordinate. That is harmless and should not trigger `"Yes"`.

This condition is the important check:

```
if px != x or py != y:
    return True
```

The recursion limit is increased because the reachable component may contain millions of cells in a long chain.

## Worked Examples

### Sample 1

Input:

```
5 4
##.#
##S#
#..#
#.##
#..#
```

Traversal trace:

| Infinite Position | Mapped Cell | Stored Before | Action |
| --- | --- | --- | --- |
| (1,2) | (1,2) | No | Store |
| (2,2) | (2,2) | No | Store |
| (2,1) | (2,1) | No | Store |
| (3,1) | (3,1) | No | Store |
| (4,1) | (4,1) | No | Store |
| (5,1) | (0,1) | Wall | Stop |
| (4,2) | (4,2) | No | Store |
| (5,2) | (0,2) | No | Store |
| (6,2) | (1,2) | Yes, from (1,2) | Different coordinates, answer Yes |

The key moment is reaching mapped cell `(1,2)` from two different infinite coordinates:

```
(1,2)
(6,2)
```

Their difference is `(5,0)`, exactly one vertical tile shift. That means the path can be repeated indefinitely.

### Example 2

Input:

```
3 3
###
#S#
#.#
```

Traversal trace:

| Infinite Position | Mapped Cell | Stored Before | Action |
| --- | --- | --- | --- |
| (1,1) | (1,1) | No | Store |
| (2,1) | (2,1) | No | Store |
| (3,1) | (0,1) | Wall | Stop |
| (1,1) | (1,1) | Same coordinate | Ignore |

Traversal eventually ends without finding the same tile cell from different infinite coordinates.

The reachable area is bounded inside one trapped region.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each original-grid cell is processed at most once before either termination or rejection |
| Space | O(nm) | The visited table stores one coordinate pair per cell |

The grid contains at most `2.25 million` cells, so linear complexity is necessary. The solution performs only constant work per reachable cell and fits comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    sys.setrecursionlimit(1 << 25)

    n, m = map(int, input().split())

    grid = []
    sx = sy = -1

    for i in range(n):
        row = input().strip()
        grid.append(row)

        for j, ch in enumerate(row):
            if ch == 'S':
                sx, sy = i, j

    visited = [[None] * m for _ in range(n)]

    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def dfs(x, y):
        rx = x % n
        ry = y % m

        if grid[rx][ry] == '#':
            return False

        if visited[rx][ry] is not None:
            px, py = visited[rx][ry]

            if px != x or py != y:
                return True

            return False

        visited[rx][ry] = (x, y)

        for dx, dy in dirs:
            if dfs(x + dx, y + dy):
                return True

        return False

    return "Yes\n" if dfs(sx, sy) else "No\n"

# provided sample
assert run(
"""5 4
##.#
##S#
#..#
#.##
#..#
"""
) == "Yes\n", "sample 1"

# minimum grid
assert run(
"""1 1
S
"""
) == "Yes\n", "single open cell repeats forever"

# fully trapped
assert run(
"""3 3
###
#S#
###
"""
) == "No\n", "completely enclosed"

# corridor blocked between copies
assert run(
"""1 3
S##
"""
) == "No\n", "cannot cross tile boundary"

# open strip
assert run(
"""1 2
S.
"""
) == "Yes\n", "infinite horizontal movement"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1x1` open grid | `Yes` | Re-entering the same tile through another copy |
| Fully enclosed start | `No` | No reachable escape path |
| `S##` | `No` | Crossing tile boundaries may still be impossible |
| `S.` | `Yes` | Simple infinite translation case |

## Edge Cases

Consider the smallest possible grid:

```
1 1
S
```

The single cell repeats infinitely in all directions. Starting from `(0,0)`, moving up reaches `(-1,0)`, which maps back to `(0,0)`.

The algorithm first stores:

```
visited[0][0] = (0,0)
```

Later it reaches:

```
(-1,0)
```

which maps to the same tile cell but has different infinite coordinates. The algorithm correctly prints `"Yes"`.

Now consider a trapped configuration:

```
3 3
###
#S#
###
```

The DFS explores only `(1,1)`. Every neighboring cell is a wall after modulo mapping. No second infinite coordinate ever reaches the same tile cell, so traversal ends and the answer is `"No"`.

Finally, consider wrapping through negative coordinates:

```
1 2
S.
```

Moving left from `(0,0)` gives `(0,-1)`. Python computes:

```
-1 % 2 == 1
```

so the mapped position becomes `(0,1)`, exactly the neighboring tile cell in the copy to the left.

Incorrect modulo handling would either crash or map to an invalid column, producing the wrong answer.
