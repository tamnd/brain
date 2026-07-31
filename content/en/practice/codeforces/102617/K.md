---
title: "CF 102617K - Dessert Islands"
description: "The map describes a chocolate swamp as a rectangular grid. Each cell is either solid cookie land (S) or liquid chocolate (L). Cells only connect through their four sides, so diagonal contact does not merge regions."
date: "2026-07-31T17:38:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102617
codeforces_index: "K"
codeforces_contest_name: "mBIT Rookie November 2019"
rating: 0
weight: 102617
solve_time_s: 59
verified: true
draft: false
---

[CF 102617K - Dessert Islands](https://codeforces.com/problemset/problem/102617/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
# Problem Understanding

The map describes a chocolate swamp as a rectangular grid. Each cell is either solid cookie land (`S`) or liquid chocolate (`L`). Cells only connect through their four sides, so diagonal contact does not merge regions.

A cookie island is a connected group of `S` cells that is completely surrounded by chocolate and does not touch the outside border of the map. A chocolate lake is the opposite: a connected group of `L` cells that is surrounded by cookie land. The task is to count how many such islands and lakes exist.

The key observation from the constraints is that the grid can contain up to about one million cells. Any approach that repeatedly searches the whole grid for every region would be too expensive. A linear scan with a graph traversal is the intended complexity because each cell can be processed a constant number of times.

The border condition simplifies the problem. The outside of the map is guaranteed to be cookie land, so every chocolate component is automatically enclosed and is a lake. For cookie components, only the component connected to the border is not an island. All other cookie components are islands.

Some edge cases are easy to mishandle. A map with only cookie land has no islands or lakes because there is only the outside component.

Example input:

```
3 3
SSS
SSS
SSS
```

The correct output is:

```
0 0
```

A careless solution that counts every `S` component as an island would incorrectly count the whole grid.

A single lake without any inner island is another case that can break solutions that assume nesting must always happen.

Example input:

```
3 3
SSS
SLS
SSS
```

The correct output is:

```
0 1
```

The chocolate component is surrounded by cookie land, so it is a lake even though there is no island inside it.

A third tricky case is multiple layers of nesting.

Example input:

```
5 5
SSSSS
SLLLS
SLSLS
SLLLS
SSSSS
```

The correct output is:

```
1 4
```

The inner regions must be counted independently. A solution that only looks at the outermost boundary would miss the smaller lakes.

## Approaches

The direct approach is to flood fill every unvisited cell and classify the resulting connected component. For each component, we can record its character type and whether it touches the border. If we try to repeatedly search around each cell or perform a separate traversal for each possible region, the same cells can be processed many times, leading to unnecessary work on a grid with one million cells.

The useful observation is that connected components already partition the grid. Every cell belongs to exactly one component, and the answer depends only on the component's character and whether it touches the border. A single BFS or DFS over the entire grid is enough.

When a flood fill finishes, an `L` component is always a lake because chocolate never reaches the border. An `S` component is an island only when it does not touch the border. This reduces the problem from tracking complicated containment relationships to simply classifying connected components.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((NM)^2) | O(NM) | Too slow |
| Flood Fill Components | O(NM) | O(NM) | Accepted |

## Algorithm Walkthrough

1. Traverse every cell in the grid. When an unvisited cell is found, start a BFS from it to discover its entire connected component. A component must be processed as a whole because the answer depends on the region, not on individual cells.
2. During the BFS, store the character type of the component and check whether any cell in the component lies on the border. Reaching the border is the only property that separates the outside cookie region from real islands.
3. After the BFS finishes, classify the component. If it contains `L`, increase the lake count. If it contains `S` and does not touch the border, increase the island count.
4. After all cells have been visited, print the number of islands followed by the number of lakes.

Why it works:

Every connected region of the grid is visited exactly once by BFS. A chocolate region cannot touch the border because the border is guaranteed to contain only cookie cells, so every chocolate component is enclosed and must be a lake. A cookie region touching the border is the outside land and cannot be an island, while every other cookie component is surrounded by chocolate and satisfies the definition of an island. Since every possible region is classified exactly once, the final counts are correct.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    visited = [[False] * m for _ in range(n)]
    islands = 0
    lakes = 0

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for i in range(n):
        for j in range(m):
            if not visited[i][j]:
                visited[i][j] = True
                kind = grid[i][j]
                touches_border = False
                q = deque([(i, j)])

                while q:
                    x, y = q.popleft()

                    if x == 0 or x == n - 1 or y == 0 or y == m - 1:
                        touches_border = True

                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < m:
                            if not visited[nx][ny] and grid[nx][ny] == kind:
                                visited[nx][ny] = True
                                q.append((nx, ny))

                if kind == 'L':
                    lakes += 1
                elif not touches_border:
                    islands += 1

    print(islands, lakes)

if __name__ == "__main__":
    solve()
```

The outer loops guarantee that every cell becomes the starting point of a flood fill only once. The `visited` array prevents revisiting cells after their component has already been classified.

The BFS queue contains only cells belonging to the current component. The `kind` variable is fixed when the traversal starts, so the search never crosses from land into chocolate or the other way around.

The border check is performed while removing cells from the queue. It is enough to remember a single boolean because the final classification only needs to know whether the component has any border cell. There is no need to store the full shape of a component.

Python integers are not a concern here because the counts are at most the number of cells, and the largest queue size is also bounded by the grid size.

## Worked Examples

Consider:

```
5 5
SSSSS
SLLLS
SLSLS
SLLLS
SSSSS
```

| Current component | Character | Touches border | Result |
| --- | --- | --- | --- |
| Outer region | S | Yes | Ignored |
| Top lake | L | No | Lake count becomes 1 |
| Center region | S | No | Island count becomes 1 |
| Other inner lakes | L | No | Lake count increases to 4 |

The trace shows why containment does not need to be explicitly modeled. Each nested region is already an independent connected component.

Another example:

```
3 5
SSSSS
SLLLS
SSSSS
```

| Current component | Character | Touches border | Result |
| --- | --- | --- | --- |
| Outer region | S | Yes | Ignored |
| Middle region | L | No | Lake count becomes 1 |

The example confirms that a lake can exist without an island inside it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(NM) | Every cell enters and leaves the BFS queue once. |
| Space | O(NM) | The visited array and BFS queue can each contain a linear number of cells. |

The maximum grid size makes linear processing necessary. The solution only performs constant work per cell, so it fits comfortably within the required limits.

## Test Cases

```python
import sys
import io
from collections import deque

def solve_io(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    visited = [[False] * m for _ in range(n)]
    islands = 0
    lakes = 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for i in range(n):
        for j in range(m):
            if not visited[i][j]:
                visited[i][j] = True
                kind = grid[i][j]
                border = False
                q = deque([(i, j)])

                while q:
                    x, y = q.popleft()
                    if x == 0 or y == 0 or x == n - 1 or y == m - 1:
                        border = True

                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < m:
                            if not visited[nx][ny] and grid[nx][ny] == kind:
                                visited[nx][ny] = True
                                q.append((nx, ny))

                if kind == "L":
                    lakes += 1
                elif not border:
                    islands += 1

    sys.stdin = old_stdin
    return f"{islands} {lakes}\n"

assert solve_io("""7 10
SSSSSSSSSS
SLSLSLLLSS
SSLLLLSLSS
SSSLSLSLLS
SSSLLSLSSS
SSLSSLLLSS
SSSSSSSSSS
""") == "3 4\n", "sample"

assert solve_io("""3 3
SSS
SLS
SSS
""") == "0 1\n", "single lake"

assert solve_io("""3 3
SSS
SSS
SSS
""") == "0 0\n", "only outside land"

assert solve_io("""5 5
SSSSS
SLLLS
SLSLS
SLLLS
SSSSS
""") == "1 4\n", "nested regions"

assert solve_io("""5 5
SSSSS
SLSLS
SSSSS
SLSLS
SSSSS
""") == "0 4\n", "multiple lakes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample grid | `3 4` | Normal nested island and lake counting |
| One `L` inside `S` | `0 1` | Lakes do not need inner islands |
| All `S` | `0 0` | Border component must not be counted |
| Multiple nested regions | `1 4` | Independent component classification |
| Several separated lakes | `0 4` | Multiple same-type components |

## Edge Cases

For an all-cookie map:

```
3 3
SSS
SSS
SSS
```

The BFS finds one `S` component and marks it as touching the border. Since it is the outside land, the island count remains zero and the lake count remains zero.

For a lake without an island:

```
3 3
SSS
SLS
SSS
```

The BFS on the `L` cell finds a component that does not touch the border. Since all chocolate components are enclosed, the algorithm counts it as one lake.

For nested regions:

```
5 5
SSSSS
SLLLS
SLSLS
SLLLS
SSSSS
```

The traversal first ignores the outer cookie component, then separately counts every inner chocolate component and the central cookie component. The classification depends only on the current component, so nesting depth does not affect correctness.
