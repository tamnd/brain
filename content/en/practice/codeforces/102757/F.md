---
title: "CF 102757F - Maze Design"
description: "The maze is a corridor with exactly three rows and n columns. Each cell is either open or blocked. Alice may begin on any open cell in the first column and can move up, down, left, or right through open cells."
date: "2026-07-29T00:26:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102757
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 10-09-20 Div. 2"
rating: 0
weight: 102757
solve_time_s: 58
verified: true
draft: false
---

[CF 102757F - Maze Design](https://codeforces.com/problemset/problem/102757/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

The maze is a corridor with exactly three rows and `n` columns. Each cell is either open or blocked. Alice may begin on any open cell in the first column and can move up, down, left, or right through open cells. The goal is to determine whether at least one possible path reaches any open cell in the last column. The input contains the width of the corridor and three binary strings describing the rows, where `0` represents a walkable position and `1` represents a wall. The output is `Solvable!` if the last column can be reached and `Unsolvable!` otherwise.

The width can reach `10^4`, so the maze contains only about `3 * 10^4` cells. A solution that examines every cell a constant number of times is easily fast enough. A brute-force search over possible paths is impossible because the number of possible walks grows exponentially as the maze becomes larger. The constraint strongly points toward a graph traversal where each cell is processed once.

The tricky cases come from the fact that the starting point is not fixed. A common mistake is to start only from the top-left cell, but Alice can choose any row in the first column. For example:

```
2
10
00
10
```

The correct output is:

```
Solvable!
```

A search beginning only at row 0 would fail immediately because the top-left cell is blocked, even though the middle-left cell can reach the second column.

Another edge case is when cells near the destination are open but disconnected from the left side. For example:

```
3
011
010
010
```

The correct output is:

```
Unsolvable!
```

The last column contains open cells, but there is no path from the first column to those cells. A careless approach that checks only whether the final column contains a `0` would produce the wrong answer.

A final boundary case is a completely open maze:

```
2
00
00
00
```

The correct output is:

```
Solvable!
```

The path may simply move straight across any row. Any implementation that accidentally requires movement through all three rows or tries to find a unique path would fail here.

## Approaches

The direct approach is to treat every open cell as a graph vertex. Two vertices are connected when their cells share a side. A brute-force solution could enumerate possible paths from the first column and stop when one reaches the last column. This is correct because every valid movement sequence corresponds to a path in the graph. The problem is the number of possible paths. A maze with many branching points can create an exponential number of choices, so exploring paths individually quickly becomes infeasible.

The useful observation is that the question only asks whether a path exists. We do not need the path itself, its length, or the number of paths. Once a cell is reachable, the exact way it was reached no longer matters. This means we can mark cells as visited and expand outward from all possible starting positions at once.

A breadth-first search or depth-first search is enough because every open cell is considered at most once. The three-row shape does not require any special maze algorithm. It only reduces the number of possible neighbors each cell can have. The graph has a linear number of vertices and edges, so a standard traversal finishes within the limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of branches | O(n) | Too slow |
| Graph Traversal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create a queue containing every open cell in the first column. These are all valid starting positions because Alice may choose any row.
2. Repeatedly remove a cell from the queue and inspect its four possible neighbors. If a neighbor is inside the maze, open, and not visited yet, mark it visited and add it to the queue. The visited array prevents repeated work and infinite movement cycles.
3. While processing cells, check whether any visited cell belongs to the final column. Reaching any row of that column means the maze has a solution.
4. If the queue becomes empty without reaching the final column, report `Unsolvable!`. Every reachable position has already been explored, so no missing path can exist.

Why it works: The traversal maintains the invariant that every cell marked visited is reachable from some starting cell in the first column. Initially this is true because only valid starting cells are inserted. Whenever a new cell is added, it is reached through a valid movement from an already reachable cell, so the invariant remains true. The search continues until all reachable cells are exhausted. If the final column is visited, the recorded path proves the maze is solvable. If it is never visited, all possible reachable positions have been checked, proving that no valid path exists.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n = int(input())
    maze = [input().strip() for _ in range(3)]

    visited = [[False] * n for _ in range(3)]
    q = deque()

    for r in range(3):
        if maze[r][0] == '0':
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
                if not visited[nr][nc] and maze[nr][nc] == '0':
                    visited[nr][nc] = True
                    q.append((nr, nc))

    print("Unsolvable!")

if __name__ == "__main__":
    solve()
```

The input is read as three strings because the maze height is fixed. The visited array has the same dimensions as the maze and records whether a position has already been discovered.

The initialization step inserts all three possible cells in the first column. This is the most common implementation mistake in this problem, because assuming only one start position changes the problem.

The queue stores row and column pairs. Every time a cell is removed, the code checks whether it is in the final column before exploring neighbors. The boundary checks prevent indexing outside the three rows or the `n` columns.

Each valid neighbor is marked before insertion rather than after removal. This avoids adding the same cell multiple times when two different paths reach it.

## Worked Examples

For the first sample:

```
2
00
10
00
```

The BFS state changes as follows.

| Step | Queue after processing | Visited cells | Result |
| --- | --- | --- | --- |
| Start | (0,0), (1,0), (2,0) | First column rows 0,1,2 | Search begins |
| Process (0,0) | (1,0), (2,0), (0,1) | Added top-right cell | Continue |
| Process (0,1) | (2,0) | Last column reached | Solvable! |

The example shows why starting from every row matters. The top row alone already provides a valid route.

For the second sample:

```
2
01
10
10
```

| Step | Queue after processing | Visited cells | Result |
| --- | --- | --- | --- |
| Start | (2,0) | Bottom-left only | Search begins |
| Process (2,0) | Empty | No new open neighbors | Stop |
| End | Empty | Last column never visited | Unsolvable! |

This case demonstrates that an open cell in the final column is not enough. It must be connected to the starting side.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | There are only `3n` cells, and each is processed once. |
| Space | O(n) | The visited array and queue store at most all cells in the maze. |

The largest maze contains about thirty thousand cells, so a linear traversal easily fits within the time and memory limits.

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

def solve():
    input = sys.stdin.readline

    n = int(input())
    maze = [input().strip() for _ in range(3)]

    visited = [[False] * n for _ in range(3)]
    q = deque()

    for r in range(3):
        if maze[r][0] == '0':
            visited[r][0] = True
            q.append((r, 0))

    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        pass

    while q:
        r, c = q.popleft()
        if c == n - 1:
            print("Solvable!")
            return

        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < n:
                if not visited[nr][nc] and maze[nr][nc] == '0':
                    visited[nr][nc] = True
                    q.append((nr, nc))

    print("Unsolvable!")

assert run("""2
00
10
00
""") == "Solvable!\n"

assert run("""2
01
10
10
""") == "Unsolvable!\n"

assert run("""2
10
00
10
""") == "Solvable!\n"

assert run("""3
011
010
010
""") == "Unsolvable!\n"

assert run("""5
00000
00000
00000
""") == "Solvable!\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| First sample | Solvable! | Normal path through the maze |
| Second sample | Unsolvable! | Disconnected destination cells |
| `10/00/10` | Solvable! | Multiple possible starting rows |
| `011/010/010` | Unsolvable! | Open cells that cannot be reached |
| Fully open 3 by 5 maze | Solvable! | Large simple connected case |

## Edge Cases

For the multiple-start case:

```
2
10
00
10
```

The algorithm ignores the blocked cells in the first row and third row, then inserts only the middle-left cell into the queue. From `(1,0)` it moves to `(1,1)`, which is in the final column, so the answer is `Solvable!`.

For the disconnected destination case:

```
3
011
010
010
```

The only starting cell is `(1,0)`. The traversal cannot move anywhere else because every possible route is blocked. The cells in the last column are never marked visited, so the algorithm correctly prints `Unsolvable!`.

For the fully open maze:

```
2
00
00
00
```

All three cells in the first column enter the queue. The search immediately expands across the corridor and reaches column `1`. Since reaching any row of the last column is enough, the algorithm returns `Solvable!`.

The editorial can be adapted further if you want a shorter contest-style explanation or a more tutorial-style version for beginners.
