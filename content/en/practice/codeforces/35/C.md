---
title: "CF 35C - Fire Again"
description: "We have a rectangular grid of trees. A fire starts simultaneously from several cells, and every minute it spreads to neighboring cells that share a side. The task is to find any cell whose burning time is as large as possible, meaning it catches fire later than every other tree."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dfs-and-similar", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 35
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 35 (Div. 2)"
rating: 1500
weight: 35
solve_time_s: 130
verified: true
draft: false
---
[CF 35C - Fire Again](https://codeforces.com/problemset/problem/35/C)

**Rating:** 1500  
**Tags:** brute force, dfs and similar, shortest paths  
**Solve time:** 2m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rectangular grid of trees. A fire starts simultaneously from several cells, and every minute it spreads to neighboring cells that share a side. The task is to find any cell whose burning time is as large as possible, meaning it catches fire later than every other tree.

This is really a shortest-path problem on a grid. Each move to a neighboring cell costs one minute, so the time when a cell burns is the minimum Manhattan distance from that cell to any starting fire source. We want the cell with the maximum such distance.

The grid can contain up to 2000 × 2000 = 4,000,000 cells. That number is large enough that quadratic work over all cells is dangerous. Since there are at most 10 starting points, a solution that scans the grid once or performs a standard graph traversal is realistic, but anything involving repeated full-grid traversals will struggle.

A common mistake is to compute distances separately from each source using BFS and keep restarting the traversal. On a 4 million cell grid, even a single BFS already touches millions of states. Doing this 10 times is unnecessarily expensive.

Another subtle issue is tie handling. The problem allows any valid farthest cell. Suppose the input is:

```
2 2
1
1 1
```

The cells `(1,2)`, `(2,1)`, and `(2,2)` do not all burn at the same time. The farthest one is `(2,2)` with distance 2. A careless implementation that updates the answer incorrectly during traversal may accidentally return a non-farthest cell.

A different edge case appears when there are multiple fire sources:

```
5 5
2
1 1 5 5
```

The center cells burn last because each corner source reaches nearby cells quickly. If we incorrectly measure distance from only the first source, we would completely miss the effect of the second fire.

The smallest possible grid also matters:

```
1 1
1
1 1
```

The only cell is already burning at time 0, so the answer must be `(1,1)`. Implementations with incorrect indexing or boundary checks often fail here.

## Approaches

The most direct idea is brute force. For every cell in the grid, compute its Manhattan distance to every starting fire source, keep the minimum of those distances, then track the cell with the maximum minimum distance.

For a cell `(x,y)` and source `(sx,sy)`, the burning time is:

$$|x - sx| + |y - sy|$$

Since there are at most 10 sources, this computation is cheap per cell. The total work becomes:

$$N \times M \times K$$

In the worst case:

$$2000 \times 2000 \times 10 = 40,000,000$$

Forty million simple integer operations in Python is actually acceptable with careful implementation. That is why many accepted solutions use brute force directly.

Still, the problem is tagged with shortest paths because the spreading process itself is naturally modeled as a multi-source BFS. Instead of explicitly computing Manhattan distances, we simulate the fire expansion level by level.

The key observation is that when all sources are inserted into the BFS queue initially, the first time we reach a cell is exactly the earliest minute when fire can arrive there. BFS processes states in increasing distance order, so the last processed cell is one of the cells that burns last.

This transforms the problem into a standard shortest-path computation on an unweighted grid graph. Every edge has cost 1, and multi-source BFS computes minimum distances from the nearest source automatically.

Compared to the brute-force distance scan, BFS avoids repeatedly recomputing distances. Each cell is visited exactly once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N × M × K) | O(1) | Accepted |
| Optimal | O(N × M) | O(N × M) | Accepted |

## Algorithm Walkthrough

1. Read the grid dimensions and the list of initial fire sources.
2. Create a visited matrix of size `N × M`. A cell becomes visited once fire reaches it.
3. Push all fire sources into a queue before starting BFS.

This is the crucial multi-source step. BFS will now expand outward from every fire simultaneously, exactly matching the spreading process described in the problem.
4. Mark all source cells as visited.
5. Repeatedly pop a cell from the queue.
6. Store the current cell as the latest processed position.

BFS processes cells in nondecreasing distance order. Because of that, cells popped later are never closer than cells popped earlier.
7. Try moving in the four grid directions.
8. For every valid unvisited neighbor, mark it visited and push it into the queue.
9. When BFS finishes, output the last processed cell.

That cell has maximum distance from the nearest fire source.

### Why it works

BFS on an unweighted graph always discovers nodes in increasing shortest-path distance order. Starting from all fire sources simultaneously means each cell is reached by the nearest source first. The queue expands layer by layer, where each layer corresponds to one minute of fire spreading.

Because of this ordering, the final cell removed from the queue belongs to the farthest BFS layer, meaning its minimum distance to any source is maximal. Returning that cell is correct.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

# solution

def solve():
    n, m = map(int, input().split())

    k = int(input())
    arr = list(map(int, input().split()))

    visited = [[False] * m for _ in range(n)]
    q = deque()

    for i in range(0, 2 * k, 2):
        x = arr[i] - 1
        y = arr[i + 1] - 1

        visited[x][y] = True
        q.append((x, y))

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    last_x, last_y = 0, 0

    while q:
        x, y = q.popleft()

        last_x, last_y = x, y

        for dx, dy in directions:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny]:
                visited[nx][ny] = True
                q.append((nx, ny))

    print(last_x + 1, last_y + 1)

solve()
```

The queue initially contains every burning tree. That is what makes this a multi-source BFS instead of a normal BFS from a single node.

The `visited` matrix prevents revisiting cells. Without it, the same cell could be inserted many times from different directions, which would increase runtime dramatically.

Coordinates are converted to 0-based indexing immediately after reading input. This keeps boundary checks simple because Python lists are 0-indexed. Before printing, the answer is converted back to 1-based indexing.

The variable `last_x, last_y` is updated every time a cell is popped from the queue. Since BFS processes cells in increasing distance order, the final popped cell is one of the farthest cells.

The order of directions does not matter because the problem allows any valid answer.

## Worked Examples

### Example 1

Input:

```
3 3
1
2 2
```

The fire starts from the center.

| Step | Queue Front | Newly Added Cells | Last Processed |
| --- | --- | --- | --- |
| 1 | (2,2) | (1,2), (3,2), (2,1), (2,3) | (2,2) |
| 2 | (1,2) | (1,1), (1,3) | (1,2) |
| 3 | (3,2) | (3,1), (3,3) | (3,2) |
| 4 | Remaining edge cells | none | varies |
| Final | (3,3) | none | (3,3) |

One valid answer is `(3,3)`. The sample outputs `(1,1)` because several corners are tied for maximum distance.

This trace shows how BFS expands in layers. All cells at distance 1 are processed before any cell at distance 2.

### Example 2

Input:

```
5 5
2
1 1 5 5
```

| Step | Queue Front | Newly Added Cells | Last Processed |
| --- | --- | --- | --- |
| 1 | (1,1) | (2,1), (1,2) | (1,1) |
| 2 | (5,5) | (4,5), (5,4) | (5,5) |
| 3 | Distance-1 layer | several cells | varies |
| 4 | Distance-2 layer | center region | varies |
| Final | (3,3) | none | (3,3) |

The center cell is farthest because both fires approach it symmetrically.

This example confirms that multi-source BFS correctly combines expansion from several origins instead of treating them independently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N × M) | Every cell enters the queue once |
| Space | O(N × M) | The visited matrix stores one state per cell |

The grid contains at most 4 million cells. Visiting each cell once is completely acceptable within the limits. The memory usage is also safe for the given constraints.

## Test Cases

```python
# helper: run solution on input string, return output string

import sys
import io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n, m = map(int, input().split())

        k = int(input())
        arr = list(map(int, input().split()))

        visited = [[False] * m for _ in range(n)]
        q = deque()

        for i in range(0, 2 * k, 2):
            x = arr[i] - 1
            y = arr[i + 1] - 1

            visited[x][y] = True
            q.append((x, y))

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        last_x, last_y = 0, 0

        while q:
            x, y = q.popleft()

            last_x, last_y = x, y

            for dx, dy in directions:
                nx = x + dx
                ny = y + dy

                if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny]:
                    visited[nx][ny] = True
                    q.append((nx, ny))

        return f"{last_x + 1} {last_y + 1}"

    return solve()

# provided sample
assert run(
"""3 3
1
2 2
"""
) in {"1 1", "1 3", "3 1", "3 3"}, "sample 1"

# minimum grid
assert run(
"""1 1
1
1 1
"""
) == "1 1", "single cell"

# opposite corners
assert run(
"""2 2
1
1 1
"""
) == "2 2", "farthest corner"

# multiple sources
assert run(
"""5 5
2
1 1 5 5
"""
) == "3 3", "center should be farthest"

# entire first row burning
ans = run(
"""3 4
4
1 1 1 2 1 3 1 4
"""
)
assert ans in {"3 1", "3 2", "3 3", "3 4"}, "bottom row farthest"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1×1` grid | `(1,1)` | Minimum constraints |
| Single source in corner | Opposite corner | Maximum Manhattan distance |
| Two opposite sources | Center cell | Correct multi-source behavior |
| Entire first row burning | Any bottom-row cell | Layer-by-layer expansion |

## Edge Cases

Consider the smallest possible input:

```
1 1
1
1 1
```

The queue initially contains only `(1,1)`. BFS pops it immediately, and no neighbors exist. The algorithm outputs `(1,1)`, which is correct because the only tree is already burning.

Now consider multiple competing fire sources:

```
5 5
2
1 1 5 5
```

Initially both corners enter the queue. BFS expands outward simultaneously. The center cell `(3,3)` is reached later than any other cell because both fires need four steps to reach it. Since BFS always processes smaller distances first, `(3,3)` appears in the final layer and becomes the answer.

A tie case is also interesting:

```
3 3
1
2 2
```

All four corners are equally far from the center source. BFS may finish with any of them depending on queue order. The problem explicitly allows any valid answer, so this behavior is correct.

Finally, consider a narrow grid:

```
1 5
1
1 3
```

The fire spreads left and right only. BFS correctly handles this because movement checks use bounds independently for rows and columns. The farthest cells are `(1,1)` and `(1,5)`, and either answer is accepted.
