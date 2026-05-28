---
title: "CF 193A - Cutting Figure"
description: "We are given a rectangular grid where some cells are painted with . All painted cells initially form one connected component using 4-directional adjacency, meaning movement is allowed only through shared sides. We may delete painted cells one by one."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "graphs", "trees"]
categories: ["algorithms"]
codeforces_contest: 193
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 122 (Div. 1)"
rating: 1700
weight: 193
solve_time_s: 101
verified: true
draft: false
---

[CF 193A - Cutting Figure](https://codeforces.com/problemset/problem/193/A)

**Rating:** 1700  
**Tags:** constructive algorithms, graphs, trees  
**Solve time:** 1m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular grid where some cells are painted with `#`. All painted cells initially form one connected component using 4-directional adjacency, meaning movement is allowed only through shared sides.

We may delete painted cells one by one. Deleting a cell removes it completely from the figure. The goal is to find the minimum number of deletions needed so that the remaining painted cells are no longer connected.

There is one subtle detail in the definition: an empty set and a set containing exactly one cell are still considered connected. That means reducing the figure to zero or one cell does not count as disconnecting it.

The grid dimensions are at most `50 × 50`, so the total number of cells is at most `2500`. A connectivity check with DFS or BFS over the whole grid costs `O(nm)`, which is tiny here. Even repeating that connectivity test many times is completely fine.

The first instinct is to try removing each painted cell and check whether the remaining figure becomes disconnected. Since there are at most `2500` painted cells, this gives roughly `2500 × 2500 = 6.25 million` operations, easily within limits.

The tricky part is not performance, it is understanding what answers are even possible.

A careless implementation often misses the following edge cases.

Consider a figure with only one painted cell.

```
1 1
#
```

The correct answer is `-1`.

Deleting the only cell leaves the empty set, which is still defined as connected. There is no way to make the figure disconnected.

Now consider two adjacent cells.

```
1 2
##
```

The correct answer is also `-1`.

Deleting either cell leaves exactly one painted cell, which is connected by definition.

Another common mistake is assuming every connected shape can be disconnected by deleting one cell. A solid cycle disproves that.

```
3 3
###
#.#
###
```

The correct answer is `2`.

No single cell acts as an articulation point here. Removing any one cell still leaves a connected path around the cycle.

On the other hand, thin structures often disconnect immediately.

```
3 1
#
#
#
```

The correct answer is `1`.

Removing the middle cell splits the figure into two disconnected parts.

## Approaches

The brute-force idea is straightforward. For every painted cell, temporarily remove it and run a DFS or BFS over the remaining painted cells. If the remaining cells are disconnected, then the answer is `1`. If no single removal works, we try removing two cells.

Trying all pairs explicitly would cost about `2500²` connectivity checks, and each check scans the whole grid. That becomes roughly:

```
2500 × 2500 × 2500 ≈ 1.5 × 10^10
```

which is far too slow.

The key observation is that the answer can only be `1`, `2`, or `-1`.

Why?

If the figure contains fewer than three painted cells, disconnecting it is impossible because after deletions we would end with zero or one cell, both still considered connected.

For any connected figure with at least three cells, the answer never exceeds `2`. This comes from a graph property of connected polyominoes on a grid. If there is no articulation point, we can always disconnect the figure by deleting two carefully chosen cells.

So instead of searching all pairs, we only need to answer one question:

```
Does there exist a single painted cell whose removal disconnects the figure?
```

If yes, answer `1`.

Otherwise, if the figure has at least three painted cells, answer `2`.

This turns the problem into articulation-point detection by brute force simulation. Since the grid is small, we do not even need Tarjan's algorithm. We can simply remove each cell once and test connectivity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all pairs | O(K³) | O(K) | Too slow |
| Remove one cell and test connectivity | O(K²) | O(K) | Accepted |

Here `K` is the number of painted cells.

## Algorithm Walkthrough

1. Read the grid and count the number of painted cells.
2. If the number of painted cells is less than `3`, print `-1`.

With fewer than three cells, every possible deletion leaves at most one cell, which is still connected by definition.
3. For every painted cell:

Temporarily mark it as deleted.
4. Run a DFS or BFS from any remaining painted cell.

Count how many painted cells are reachable after the deletion.
5. Compare the reachable count with the expected remaining number of cells.

If they differ, the figure became disconnected, so print `1`.
6. Restore the deleted cell and continue checking other cells.
7. If no single deletion disconnects the figure, print `2`.

### Why it works

The algorithm explicitly checks whether any painted cell is an articulation point of the grid graph.

If removing some cell disconnects the figure, then one deletion is sufficient, and the algorithm finds it by direct simulation.

If no single cell disconnects the figure, then the answer cannot be `1`. For connected grid figures with at least three cells, two deletions are always enough, so the answer must be `2`.

The special case for fewer than three painted cells handles the definition that empty and single-cell sets are still connected.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
grid = [list(input().strip()) for _ in range(n)]

cells = []

for i in range(n):
    for j in range(m):
        if grid[i][j] == '#':
            cells.append((i, j))

total = len(cells)

if total < 3:
    print(-1)
    sys.exit()

dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def dfs(si, sj, visited):
    stack = [(si, sj)]
    visited[si][sj] = True
    count = 1

    while stack:
        x, y = stack.pop()

        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < n and 0 <= ny < m:
                if not visited[nx][ny] and grid[nx][ny] == '#':
                    visited[nx][ny] = True
                    stack.append((nx, ny))
                    count += 1

    return count

for x, y in cells:
    grid[x][y] = '.'

    start = None

    for i, j in cells:
        if grid[i][j] == '#':
            start = (i, j)
            break

    if start is not None:
        visited = [[False] * m for _ in range(n)]
        connected_count = dfs(start[0], start[1], visited)

        if connected_count != total - 1:
            print(1)
            sys.exit()

    grid[x][y] = '#'

print(2)
```

The solution stores all painted cells first because we repeatedly iterate over them during simulations.

The early check `total < 3` is essential. Without it, a case like `##` would incorrectly produce `1`, even though deleting one cell leaves a single connected cell.

The DFS uses an iterative stack instead of recursion. Python recursion depth would still be safe here, but iterative DFS avoids unnecessary risk.

For each simulated deletion, we search for any remaining painted cell to use as the DFS starting point. Since the original figure is connected, any mismatch between the DFS count and `total - 1` means the figure split into multiple components.

Restoring the deleted cell after every iteration is easy to forget. Missing this step silently corrupts later checks.

## Worked Examples

### Example 1

Input:

```
5 4
####
#..#
#..#
#..#
####
```

This is a hollow rectangle.

| Deleted Cell | Reachable Cells After DFS | Remaining Cells | Disconnected? |
| --- | --- | --- | --- |
| (0,0) | 13 | 13 | No |
| (0,1) | 13 | 13 | No |
| (0,2) | 13 | 13 | No |
| ... | ... | ... | ... |

Every single deletion still leaves a cycle around the border, so the figure remains connected.

The algorithm never finds an articulation point and prints `2`.

This example demonstrates why cycles are important. Connectivity survives every single-cell removal.

### Example 2

Input:

```
3 1
#
#
#
```

| Deleted Cell | Reachable Cells After DFS | Remaining Cells | Disconnected? |
| --- | --- | --- | --- |
| Top | 2 | 2 | No |
| Middle | 1 | 2 | Yes |

When the middle cell is removed, the top and bottom cells become isolated from each other.

The DFS reaches only one remaining cell instead of two, so the algorithm immediately prints `1`.

This example shows articulation-point behavior directly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(K²) | We try removing each painted cell once, and each DFS scans at most all painted cells |
| Space | O(K) | DFS visited array and stack |

Here `K` is the number of painted cells, at most `2500`.

At worst, we perform about `2500` DFS traversals over a `2500`-cell grid, roughly `6.25 million` operations. That comfortably fits within the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())
    grid = [list(input().strip()) for _ in range(n)]

    cells = []

    for i in range(n):
        for j in range(m):
            if grid[i][j] == '#':
                cells.append((i, j))

    total = len(cells)

    if total < 3:
        print(-1)
        return

    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def dfs(si, sj, visited):
        stack = [(si, sj)]
        visited[si][sj] = True
        count = 1

        while stack:
            x, y = stack.pop()

            for dx, dy in dirs:
                nx = x + dx
                ny = y + dy

                if 0 <= nx < n and 0 <= ny < m:
                    if not visited[nx][ny] and grid[nx][ny] == '#':
                        visited[nx][ny] = True
                        stack.append((nx, ny))
                        count += 1

        return count

    for x, y in cells:
        grid[x][y] = '.'

        start = None

        for i, j in cells:
            if grid[i][j] == '#':
                start = (i, j)
                break

        if start is not None:
            visited = [[False] * m for _ in range(n)]
            cnt = dfs(start[0], start[1], visited)

            if cnt != total - 1:
                print(1)
                return

        grid[x][y] = '#'

    print(2)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue()

# provided sample
assert run(
"""5 4
####
#..#
#..#
#..#
####
"""
) == "2\n", "sample 1"

# single cell
assert run(
"""1 1
#
"""
) == "-1\n", "single cell impossible"

# two connected cells
assert run(
"""1 2
##
"""
) == "-1\n", "two cells still cannot disconnect"

# simple articulation point
assert run(
"""3 1
#
#
#
"""
) == "1\n", "middle cell disconnects"

# cycle structure
assert run(
"""3 3
###
#.#
###
"""
) == "2\n", "cycle has no articulation point"

# larger connected block
assert run(
"""2 2
##
##
"""
) == "2\n", "solid block needs two deletions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1x1` single `#` | `-1` | Empty set is still connected |
| `##` | `-1` | One remaining cell is connected |
| Vertical chain of length 3 | `1` | Articulation point detection |
| Hollow 3x3 square | `2` | Cycle remains connected after one deletion |
| Solid 2x2 block | `2` | Dense structures without articulation points |

## Edge Cases

Consider again the smallest possible figure.

```
1 1
#
```

The algorithm counts `1` painted cell. Since `1 < 3`, it immediately prints `-1`.

This matches the definition that the empty set is connected.

Now examine two adjacent cells.

```
1 2
##
```

Again, the algorithm exits early because the number of painted cells is `2`.

Deleting either cell leaves exactly one painted cell, which is connected, so disconnecting is impossible.

Next, consider a figure with an articulation point.

```
3 1
#
#
#
```

The algorithm tries deleting the middle cell.

After deletion:

```
#
.
#
```

DFS starting from the top reaches only one cell, while `total - 1 = 2`. The mismatch proves disconnection, so the answer becomes `1`.

Finally, consider a cycle.

```
3 3
###
#.#
###
```

Removing any one cell still leaves a path around the ring. Every DFS visits all remaining painted cells.

Since no articulation point exists, the algorithm correctly prints `2`.
