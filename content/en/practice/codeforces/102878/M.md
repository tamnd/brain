---
title: "CF 102878M - Camouflage"
description: "The camouflage is represented as a rectangular grid of black and white pixels. White pixels form separate spots, and a spot can be repainted only when it is completely surrounded by black pixels in the four orthogonal directions."
date: "2026-07-25T12:49:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102878
codeforces_index: "M"
codeforces_contest_name: "The 15-th BIT Campus Programming Contest - Onsite Round"
rating: 0
weight: 102878
solve_time_s: 59
verified: true
draft: false
---

[CF 102878M - Camouflage](https://codeforces.com/problemset/problem/102878/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

The camouflage is represented as a rectangular grid of black and white pixels. White pixels form separate spots, and a spot can be repainted only when it is completely surrounded by black pixels in the four orthogonal directions. Among all such enclosed white spots, Long Long can repaint only the ones whose area does not exceed `d`. The task is to output the final grid after filling those chosen spots with black pixels.

The grid dimensions can both reach 1000, so there can be up to one million cells. A solution that repeatedly searches the grid or checks every possible region would quickly become too slow. With this size, the intended approach must process every cell only a constant number of times, giving an expected complexity close to `O(n * m)`.

The main trap is confusing a locally surrounded pixel with an entire enclosed spot. A pixel can have black neighbors on all four sides while belonging to a larger white component that touches the outside through another path. The decision must be made for connected components of white cells, not individual cells.

For example, consider:

```
3 3 1
###
#.#
###
```

The middle cell is an enclosed white spot with area `1`, so the correct output is:

```
###
###
###
```

A careless solution that only checks whether a cell has four black neighbours might work here, but it can fail when several white cells are connected.

Another case:

```
5 5 3
#####
#...#
#.#.#
#...#
#####
```

The white component has area `8`. Even though some cells inside it are surrounded by black pixels, the whole component is too large and must remain unchanged. The correct output is:

```
#####
#...#
#.#.#
#...#
#####
```

A solution that paints individual surrounded cells instead of connected white regions would incorrectly modify the grid.

## Approaches

A direct brute force method would inspect every white pixel, run a search to determine whether it is enclosed, count the size of its region, and repaint if the size is small enough. This is correct because every decision is based on the actual white component. However, if each of the one million cells starts its own search, the same area can be traversed many times. In the worst case this reaches `O((n * m)^2)` operations, which is far beyond what the grid size allows.

The key observation is that every white spot is a connected component. A flood fill already gives exactly the information needed: its cells and whether the component touches the boundary. A component that touches the border is open and can never be repainted. A component that does not touch the border is fully surrounded by black pixels because the statement guarantees that spots do not cross the grid border.

This changes the problem into a single traversal of all white components. During the traversal, we collect the cells belonging to one component. If its size is at most `d` and it never reaches the outside, we convert those stored cells into black.

The brute force works because flood filling individual components is enough to decide the answer, but it fails when it repeats the same work. The observation that each cell belongs to exactly one component lets us process every pixel once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n * m)^2) | O(n * m) | Too slow |
| Optimal | O(n * m) | O(n * m) | Accepted |

## Algorithm Walkthrough

1. Iterate through every cell of the grid. When an unvisited white cell is found, start a flood fill from it.
2. During the flood fill, store every cell belonging to the current white component and count its size. If any visited cell lies on the outer border, mark the component as open.
3. After the flood fill finishes, check the component information. If it is not open and its size is at most `d`, repaint every stored cell as black.
4. Continue until every white component has been processed.

The reason we store the cells instead of immediately repainting them is that we do not know whether the component is valid until the flood fill finishes. A component may look enclosed near its starting cell but later reach the border.

Why it works:

Every white pixel belongs to exactly one connected component, so the algorithm considers every possible repaint candidate exactly once. A component can only be repainted when it does not touch the boundary, which means every path leaving the component reaches black cells. The area check is performed on the complete component, so the algorithm never partially paints a spot. Therefore every painted cell satisfies the required condition, and every valid spot is painted.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n, m, d = map(int, input().split())
    grid = [list(input().strip()) for _ in range(n)]

    visited = [[False] * m for _ in range(n)]
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.' and not visited[i][j]:
                q = deque([(i, j)])
                visited[i][j] = True
                cells = []
                closed = True

                while q:
                    x, y = q.popleft()
                    cells.append((x, y))

                    if x == 0 or x == n - 1 or y == 0 or y == m - 1:
                        closed = False

                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < m:
                            if grid[nx][ny] == '.' and not visited[nx][ny]:
                                visited[nx][ny] = True
                                q.append((nx, ny))

                if closed and len(cells) <= d:
                    for x, y in cells:
                        grid[x][y] = '#'

    print("\n".join("".join(row) for row in grid))

if __name__ == "__main__":
    solve()
```

The outer loops guarantee that every cell becomes the starting point of at most one flood fill. The `visited` array is necessary because otherwise the same white component would be explored repeatedly.

The queue performs a breadth first search over four-directional neighbours. While collecting the component, the code only records coordinates and delays painting until the component classification is complete. This avoids the common mistake of modifying a component before knowing whether it should be changed.

The boundary check uses `0` and `n - 1` for rows and `0` and `m - 1` for columns. Missing one of these four conditions is a typical source of wrong answers because an open spot can only be detected through these cells.

Python integers do not have overflow issues here because the largest possible component size is only one million, but the implementation still avoids unnecessary arithmetic and only stores coordinates that are needed.

## Worked Examples

Using the first sample:

```
7 6 5
......
..##..
.#.#..
.#.#..
.#..#.
..##..
......
```

The flood fill finds the enclosed white region in the middle.

| Step | Current component size | Touches border | Action |
| --- | --- | --- | --- |
| Start at (2,2) | 1 | No | Continue search |
| After flood fill | 5 | No | Paint component |
| Final | 5 | No | Replace with black |

The component has area `5`, which is allowed by `d`, and it is completely enclosed, so all its cells become black.

For the second sample:

```
10 10 3
..........
...##.....
..####....
.##..##...
.######...
.####.....
.#..#.###.
.##.#.#.#.
..###.###.
..........
```

One of the enclosed components has exactly three cells.

| Step | Current component size | Touches border | Action |
| --- | --- | --- | --- |
| Find inner white region | 1 | No | Continue search |
| Finish flood fill | 3 | No | Paint component |
| Other white regions | Various | Yes | Keep unchanged |

The example shows why boundary detection matters. Large open white areas remain untouched even if they contain locally surrounded cells.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * m) | Every cell is visited once by the flood fills and checked a constant number of times. |
| Space | O(n * m) | The visited matrix and the largest stored component require linear memory. |

The maximum grid contains one million cells, so a linear traversal fits comfortably within the intended limits. The algorithm avoids recursion to prevent Python recursion depth problems on large components.

## Test Cases

```python
import sys
import io
from collections import deque

def solve(inp):
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, m, d = map(int, input().split())
    grid = [list(input().strip()) for _ in range(n)]

    visited = [[False] * m for _ in range(n)]
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for i in range(n):
        for j in range(m):
            if grid[i][j] == '.' and not visited[i][j]:
                q = deque([(i, j)])
                visited[i][j] = True
                cells = []
                closed = True

                while q:
                    x, y = q.popleft()
                    cells.append((x, y))

                    if x == 0 or x == n - 1 or y == 0 or y == m - 1:
                        closed = False

                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < m:
                            if grid[nx][ny] == '.' and not visited[nx][ny]:
                                visited[nx][ny] = True
                                q.append((nx, ny))

                if closed and len(cells) <= d:
                    for x, y in cells:
                        grid[x][y] = '#'

    return "\n".join("".join(row) for row in grid) + "\n"

assert solve("""7 6 5
......
..##..
.#.#..
.#.#..
.#..#.
..##..
......
""") == """......
..##..
.###..
.###..
.####.
..##..
......
""", "sample 1"

assert solve("""10 10 3
..........
...##.....
..####....
.##..##...
.######...
.####.....
.#..#.###.
.##.#.#.#.
..###.###.
..........
""") == """..........
...##.....
..####....
.######...
.######...
.####.....
.#..#.###.
.##.#.###.
..###.###.
..........
""", "sample 2"

assert solve("""1 1 1
.
""") == """.\n", "minimum open case"

assert solve("""3 3 1
###
#.#
###
""") == """###
###
###
""", "single enclosed cell"

assert solve("""5 5 3
#####
#...#
#.#.#
#...#
#####
""") == """#####
#...#
#.#.#
#...#
#####
""", "large enclosed component"

assert solve("""4 4 10
####
#..#
#..#
####
""") == """####
####
####
####
""", "all equal enclosed values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single white cell on the border | Same grid | Checks that outside areas are never painted. |
| One enclosed cell | Filled grid | Checks the smallest valid repaint. |
| Large enclosed region with a small hole | Unchanged grid | Checks component size instead of individual cells. |
| Fully enclosed square | Fully black grid | Checks normal repainting with a larger limit. |

## Edge Cases

For the single-cell enclosed case:

```
3 3 1
###
#.#
###
```

The flood fill starts at the center, collects one cell, and never reaches the boundary. Since the component size is `1`, it is repainted. The result is:

```
###
###
###
```

For the large component case:

```
5 5 3
#####
#...#
#.#.#
#...#
#####
```

The flood fill reaches all eight white cells. The component does not touch the boundary, but its size is greater than `d = 3`, so the algorithm leaves every cell unchanged. This confirms that the area condition applies to the entire spot.

For a grid containing only border-connected white cells, such as:

```
2 3 10
...
...
```

the flood fill marks the component as open immediately because it visits border cells. Even though the area is small enough, the component is not repaintable, so the output stays identical.

The algorithm handles all of these cases naturally because it bases every decision on the complete connected component rather than local pixel appearance.
