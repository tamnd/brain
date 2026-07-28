---
title: "CF 102756F - Maze Design"
description: "The maze is a corridor with exactly three rows and n columns. Each character describes one tile. A 0 tile is a place Alice can stand on, while a 1 tile is blocked."
date: "2026-07-29T00:37:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102756
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 10-09-20 Div. 1"
rating: 0
weight: 102756
solve_time_s: 46
verified: true
draft: false
---

[CF 102756F - Maze Design](https://codeforces.com/problemset/problem/102756/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

The maze is a corridor with exactly three rows and `n` columns. Each character describes one tile. A `0` tile is a place Alice can stand on, while a `1` tile is blocked. Alice may begin on any open tile in the first column and wants to reach any open tile in the last column by moving only up, down, left, or right. The task is to decide whether such a path exists.

The input size is the main clue. The width can reach `10^4`, but the height is fixed at only three rows. A general grid algorithm that explores every reachable tile is already enough because there are only `3 * n` positions. Any approach that tries to enumerate possible paths is impossible, since the number of paths grows exponentially with the number of columns.

The small height is the hidden structure. A careless solution might treat this as a normal large grid and add unnecessary complexity, but the maze has only three layers. Another common mistake is to only check whether every column has an open tile. That is not sufficient because a gap between rows can disconnect the path.

For example:

```
2
00
10
00
```

The answer is:

```
Solvable!
```

A path can start at the top left, move right, move down, and reach the final column. A column-by-column check works here, but it does not prove connectivity.

Another case is:

```
2
01
10
10
```

The answer is:

```
Unsolvable!
```

The last column contains an open tile, and the first column contains an open tile, but they are separated by blocked cells. A solution that only checks the existence of open cells at both ends would incorrectly accept it.

The safest way to reason about the problem is to view open tiles as graph vertices. Since the graph has only `3n` vertices, searching the reachable component is easily fast enough.

## Approaches

The direct approach is to run a graph traversal from every possible starting tile in the first column. Each open tile is a node, and edges connect neighboring open tiles. A breadth first search or depth first search visits every reachable tile and tells us whether the last column can be reached. This is correct because graph traversal explores exactly the connected component containing the starting node.

However, starting a separate traversal from every possible first-column tile repeats work. In the worst case there are three starting positions, so the repetition is not actually harmful here, but it is unnecessary. More importantly, the problem becomes much clearer when we recognize that all valid starts are connected through the same graph. We can add all first-column open tiles to one initial search and explore the whole reachable region at once.

The observation that the maze height is fixed allows us to model the entire passage as a tiny graph with `O(n)` nodes. A single BFS or DFS processes each tile at most once, giving a simple linear solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(n) | Accepted, but unnecessary repeated searches |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the three maze rows and create a visited array for the three by `n` grid. The grid dimensions are fixed, so this representation stores every possible position directly.
2. Put every open tile in the first column into the BFS queue and mark it visited. Alice is allowed to start from any of these positions, so the search should begin from all of them simultaneously.
3. Repeatedly remove a position from the queue and inspect its four neighboring positions. If a neighbor is inside the maze, is open, and has not been visited, mark it visited and add it to the queue.
4. During the search, check whether a visited position lies in the last column. If one exists, the maze has a valid route from the beginning to the end.
5. If the queue becomes empty without reaching the last column, every reachable position has been explored and no solution exists.

Why it works: the invariant maintained by BFS is that every visited tile is reachable from some valid starting tile in the first column. When BFS finishes, every tile connected to the starting region has been visited. If the last column contains a visited tile, there is a valid path. If it does not, no path can exist because every possible movement from the starting region was already explored.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n = int(input())
    grid = [input().strip() for _ in range(3)]

    visited = [[False] * n for _ in range(3)]
    q = deque()

    for r in range(3):
        if grid[r][0] == '0':
            visited[r][0] = True
            q.append((r, 0))

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while q:
        r, c = q.popleft()

        if c == n - 1:
            print("Solvable!")
            return

        for dr, dc in directions:
            nr = r + dr
            nc = c + dc

            if 0 <= nr < 3 and 0 <= nc < n:
                if not visited[nr][nc] and grid[nr][nc] == '0':
                    visited[nr][nc] = True
                    q.append((nr, nc))

    print("Unsolvable!")

if __name__ == "__main__":
    solve()
```

The code starts BFS from all possible entry tiles instead of choosing one arbitrary start. This matches the problem definition because Alice may begin anywhere in the first column.

The boundary check prevents accessing rows outside `0` to `2` or columns outside `0` to `n - 1`. Marking a cell visited before adding it to the queue prevents duplicate queue entries and guarantees each tile is processed once.

The early return when reaching column `n - 1` is safe because reaching any tile in the final column is enough to solve the maze. There is no need to continue exploring after success has already been proven.

## Worked Examples

For the first example:

```
2
00
10
00
```

The BFS state evolves as follows.

| Step | Queue before processing | Current tile | New visited tiles | Result |
| --- | --- | --- | --- | --- |
| 1 | (0,0), (2,0) | (0,0) | (0,1) | Continue |
| 2 | (2,0), (0,1) | (2,0) | (2,1) | Continue |
| 3 | (0,1), (2,1) | (0,1) | None | Continue |
| 4 | (2,1) | (2,1) | Final column reached | Solvable! |

The trace shows that BFS does not need to follow a single planned route. It explores every possible route until it finds a successful one.

For the second example:

```
2
01
10
10
```

| Step | Queue before processing | Current tile | New visited tiles | Result |
| --- | --- | --- | --- | --- |
| 1 | (0,0) | (0,0) | None | Continue |
| 2 | Empty | None | None | No final column reached |

The only starting tile is blocked from reaching the second column, so the search correctly rejects the maze.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | There are only `3n` cells, and each cell is visited at most once |
| Space | O(n) | The visited array and BFS queue store at most all cells |

The fixed height keeps the graph small. A linear scan over the maze is comfortably within the limit for `n = 10^4`.

## Test Cases

```python
import sys
import io
from collections import deque

def solve_input(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    grid = [input().strip() for _ in range(3)]

    visited = [[False] * n for _ in range(3)]
    q = deque()

    for r in range(3):
        if grid[r][0] == '0':
            visited[r][0] = True
            q.append((r, 0))

    while q:
        r, c = q.popleft()
        if c == n - 1:
            return "Solvable!\n"

        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < n:
                if not visited[nr][nc] and grid[nr][nc] == '0':
                    visited[nr][nc] = True
                    q.append((nr, nc))

    return "Unsolvable!\n"

assert solve_input("""2
00
10
00
""") == "Solvable!\n", "sample 1"

assert solve_input("""2
01
10
10
""") == "Unsolvable!\n", "sample 2"

assert solve_input("""2
00
00
00
""") == "Solvable!\n", "all open"

assert solve_input("""2
11
00
11
""") == "Unsolvable!\n", "blocked entry"

assert solve_input("""10000
""" + "0" * 10000 + "\n" + "1" * 10000 + "\n" + "0" * 10000 + "\n") == "Solvable!\n", "maximum width"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | Solvable! | A route that changes rows |
| Sample 2 | Unsolvable! | A disconnected final column |
| All open maze | Solvable! | Simple fully connected case |
| Blocked entry | Unsolvable! | No possible starting position |
| Width 10000 case | Solvable! | Linear performance at maximum size |

## Edge Cases

The first important edge case is when multiple starting positions exist. In:

```
2
00
00
00
```

the BFS begins with all three cells in the first column. The algorithm does not assume Alice starts on a specific row, so every possible entrance is handled.

The second case is when the final column has open cells but they cannot be reached:

```
2
01
10
10
```

The search starts at `(0,0)`. Its neighbors are either outside the grid or blocked, so the queue becomes empty. Since no final-column cell was visited, the algorithm outputs `Unsolvable!`.

The third case is a long narrow maze:

```
10000
00000000000000000000...000
11111111111111111111...111
00000000000000000000...000
```

with `10000` columns. The BFS still visits each reachable tile once. It does not depend on recursion depth or the number of possible paths, so it handles the maximum width safely.
