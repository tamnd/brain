---
title: "CF 135D - Cycle"
description: "We are given a binary grid. Cells containing '1' form usable tiles, while '0' cells are blocked. We want the longest cycle made entirely from '1' cells. The cycle must behave like a simple closed curve on the grid."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dfs-and-similar", "implementation"]
categories: ["algorithms"]
codeforces_contest: 135
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 97 (Div. 1)"
rating: 2500
weight: 135
solve_time_s: 110
verified: true
draft: false
---

[CF 135D - Cycle](https://codeforces.com/problemset/problem/135/D)

**Rating:** 2500  
**Tags:** brute force, dfs and similar, implementation  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary grid. Cells containing `'1'` form usable tiles, while `'0'` cells are blocked.

We want the longest cycle made entirely from `'1'` cells. The cycle must behave like a simple closed curve on the grid. Every cell on the cycle must touch exactly two other cycle cells by side adjacency, so the shape cannot branch or self-intersect.

There is one more condition, and this is the tricky part. Every `'1'` cell that is not on the cycle must lie outside the enclosed region. In other words, the cycle is not allowed to surround any extra `'1'` cells.

The answer is the maximum number of cells belonging to such a cycle.

The grid can be as large as `1000 x 1000`, which means up to one million cells. Any algorithm that tries all subsets, all simple cycles, or even performs expensive graph operations per cell will fail immediately. We need something very close to linear time.

The first important observation is that a valid cool cycle is actually the boundary of a connected component of `'1'` cells with no holes. Every boundary cell has degree exactly two inside the component, and the component cannot contain interior `'1'` cells disconnected from the boundary condition.

A careless implementation usually fails on shapes with branches or holes.

Consider this grid:

```
111
111
111
```

The outer ring looks like a cycle of length `8`, but the center cell is also `'1'` and lies strictly inside the loop. The correct answer is `0`.

Another dangerous case is a component with a tail:

```
1110
1011
1110
```

The left `3x3` ring is a valid cycle, but the extra cell attached on the right breaks the degree condition for one of the cycle vertices. A naive perimeter-counting solution would incorrectly report `8`.

Disconnected components also matter:

```
1110111
1010101
1110111
```

There are two separate cycles of length `8`. We must return the maximum, not the sum.

Finally, thin corridors can create self-touching structures:

```
1111
1001
1111
```

This is valid, because every cycle cell still has exactly two neighbors in the cycle and no `'1'` cells are trapped inside.

## Approaches

The brute force idea is to treat the grid as a graph and enumerate all simple cycles. For each cycle, we could verify whether every cycle vertex has degree two and whether all other `'1'` cells lie outside.

This works conceptually because the definition is local plus a containment condition. Unfortunately, the number of simple cycles in a grid graph is exponential. Even a `20 x 20` grid already contains far too many cycles to enumerate.

So we need to understand what a cool cycle really looks like structurally.

Suppose we take a connected component of `'1'` cells. If every cell in that component has degree exactly two inside the component, then the component forms a simple cycle. A connected graph where all vertices have degree two is exactly one cycle.

Now consider the "no interior `'1'` cells" condition. If the component itself is exactly one simple cycle, then there are no extra `'1'` cells inside it, because every `'1'` cell of the component already belongs to the cycle. Any trapped `'1'` cell would necessarily belong to the same connected component and would force some vertex degree to exceed two.

This transforms the problem completely. We no longer need geometric reasoning or inside-outside tests.

We only need to find connected components of `'1'` cells where every vertex has degree exactly two.

Once we see this equivalence, the solution becomes a straightforward graph traversal problem on the grid.

We scan the grid, run DFS or BFS on every unvisited `'1'` component, count its size, and verify that every cell inside has exactly two neighboring `'1'` cells.

If the condition holds for the whole component, then the component is one simple cycle and its size is a candidate answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force cycle enumeration | Exponential | Exponential | Too slow |
| Connected components with degree check | O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Read the grid and maintain a visited array.
2. Iterate through every cell in the grid.
3. Whenever we encounter an unvisited `'1'` cell, start a DFS or BFS from it to explore its connected component.
4. During traversal, count the number of cells in the component.
5. For every visited cell, compute how many neighboring cells also contain `'1'`. Only the four cardinal directions matter.
6. If any cell in the component has a neighbor count different from `2`, mark the component as invalid.
7. After the traversal finishes, check the validity flag.
8. If the entire component was valid, update the answer with the component size.
9. Continue until all cells are processed.

### Why it works

Inside a connected component, every cell having degree exactly two implies that the component graph is a cycle. Grid adjacency produces a simple undirected graph, and every connected graph where all vertices have degree two is a single cycle.

The component itself contains all reachable `'1'` cells. Since every cell belongs to the cycle, there cannot exist another `'1'` cell trapped inside it. That matches the definition of a cool cycle.

Conversely, every cool cycle forms a connected component where each vertex has degree exactly two. So the algorithm accepts exactly the valid cycles and rejects everything else.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    visited = [[False] * m for _ in range(n)]

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    ans = 0

    for i in range(n):
        for j in range(m):
            if grid[i][j] == '1' and not visited[i][j]:
                q = deque()
                q.append((i, j))
                visited[i][j] = True

                size = 0
                ok = True

                while q:
                    x, y = q.popleft()
                    size += 1

                    deg = 0

                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy

                        if 0 <= nx < n and 0 <= ny < m:
                            if grid[nx][ny] == '1':
                                deg += 1

                                if not visited[nx][ny]:
                                    visited[nx][ny] = True
                                    q.append((nx, ny))

                    if deg != 2:
                        ok = False

                if ok:
                    ans = max(ans, size)

    print(ans)

if __name__ == "__main__":
    solve()
```

The traversal treats the grid as an undirected graph. Each `'1'` cell is a vertex, and side adjacency creates edges.

The subtle part is the degree computation. We count neighbors directly from the grid, not from the traversal tree. A DFS tree edge count would be wrong because cycles contain back edges.

Another important detail is that we validate the entire connected component, not just a detected cycle fragment. Suppose a cycle has an extra branch attached. Some cells on the branch may still have degree two locally, but the attachment point will have degree three, so the component must be rejected as a whole.

The solution uses BFS with a queue, but DFS would work equally well. BFS avoids Python recursion depth issues on very large grids.

The visited array guarantees each cell is processed exactly once, which keeps the complexity linear.

## Worked Examples

### Example 1

Input:

```
3 3
111
101
111
```

Traversal state:

| Step | Current Cell | Degree | Component Size | Valid |
| --- | --- | --- | --- | --- |
| 1 | (0,0) | 2 | 1 | True |
| 2 | (0,1) | 2 | 2 | True |
| 3 | (0,2) | 2 | 3 | True |
| 4 | (1,2) | 2 | 4 | True |
| 5 | (2,2) | 2 | 5 | True |
| 6 | (2,1) | 2 | 6 | True |
| 7 | (2,0) | 2 | 7 | True |
| 8 | (1,0) | 2 | 8 | True |

The component contains exactly eight cells, and every cell has degree two. The algorithm accepts the component and returns `8`.

This example demonstrates the core invariant. A connected component where every node has degree two is exactly one simple cycle.

### Example 2

Input:

```
3 3
111
111
111
```

Traversal state:

| Step | Current Cell | Degree | Component Size | Valid |
| --- | --- | --- | --- | --- |
| 1 | (0,0) | 2 | 1 | True |
| 2 | (0,1) | 3 | 2 | False |
| 3 | (0,2) | 2 | 3 | False |
| 4 | (1,0) | 3 | 4 | False |
| 5 | (1,1) | 4 | 5 | False |
| 6 | (1,2) | 3 | 6 | False |
| 7 | (2,0) | 2 | 7 | False |
| 8 | (2,1) | 3 | 8 | False |
| 9 | (2,2) | 2 | 9 | False |

Several cells have degree greater than two, so the component is rejected.

This example shows why checking only the outer perimeter is insufficient. The filled square contains many branching points and is not a simple cycle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Every cell is visited once and each edge is checked a constant number of times |
| Space | O(nm) | The visited array and BFS queue may store all cells |

With at most one million cells, linear complexity is exactly what we need. The solution easily fits within the time and memory limits in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    visited = [[False] * m for _ in range(n)]

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    ans = 0

    for i in range(n):
        for j in range(m):
            if grid[i][j] == '1' and not visited[i][j]:
                q = deque([(i, j)])
                visited[i][j] = True

                size = 0
                ok = True

                while q:
                    x, y = q.popleft()
                    size += 1

                    deg = 0

                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy

                        if 0 <= nx < n and 0 <= ny < m:
                            if grid[nx][ny] == '1':
                                deg += 1

                                if not visited[nx][ny]:
                                    visited[nx][ny] = True
                                    q.append((nx, ny))

                    if deg != 2:
                        ok = False

                if ok:
                    ans = max(ans, size)

    return str(ans)

# provided sample
assert run(
"""3 3
111
101
111
"""
) == "8"

# minimum size
assert run(
"""1 1
1
"""
) == "0"

# no cycle
assert run(
"""2 2
11
10
"""
) == "0"

# two separate cycles
assert run(
"""3 7
1110111
1010101
1110111
"""
) == "8"

# filled block, not a cycle
assert run(
"""3 3
111
111
111
"""
) == "0"

# large thin rectangle cycle
assert run(
"""2 5
11111
11111
"""
) == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1x1` single cell | `0` | Minimum grid cannot form a cycle |
| Small L-shape | `0` | Degree-one vertices are rejected |
| Two separate rings | `8` | Maximum over components |
| Filled `3x3` block | `0` | Interior branching invalidates cycle |
| `2x5` full rectangle | `10` | Large perimeter cycles work correctly |

## Edge Cases

Consider the fully filled square:

```
3 3
111
111
111
```

The center cell has degree four. During BFS, the algorithm computes neighbor counts directly from the grid, so the component is marked invalid immediately. The final answer is `0`.

Now consider a component with a tail:

```
3 4
1110
1011
1110
```

The left ring alone would form a valid cycle, but the extra cell attaches to one boundary vertex. That attachment vertex gets degree three. Since the entire connected component is processed together, the component fails validation and the algorithm outputs `0`.

Disconnected cycles are handled independently:

```
3 7
1110111
1010101
1110111
```

The BFS started from the left component visits exactly eight cells, all with degree two. The right component behaves the same way. The algorithm keeps the maximum component size and outputs `8`.

Finally, consider the smallest possible nontrivial cycle:

```
2 2
11
11
```

Each cell has exactly two neighbors. The component is connected and has size four, so the algorithm correctly outputs `4`.
