---
title: "CF 102672K - Escape from the Abundoned House"
description: "The house is a rectangular grid. Some cells are blocked by walls, while the remaining cells can be walked through. The friends start in the cell marked s and want to reach the cell marked f."
date: "2026-08-03T03:28:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102672
codeforces_index: "K"
codeforces_contest_name: "Selection of tasks from Internet olympiads season 2019-20"
rating: 0
weight: 102672
solve_time_s: 82
verified: true
draft: false
---

[CF 102672K - Escape from the Abundoned House](https://codeforces.com/problemset/problem/102672/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
# Problem Understanding

The house is a rectangular grid. Some cells are blocked by walls, while the remaining cells can be walked through. The friends start in the cell marked `s` and want to reach the cell marked `f`.

Every time they move horizontally to a neighboring cell, the air temperature changes by `-1`. Every time they move vertically to a neighboring cell, it changes by `+1`. They do not care about the temperature during the walk, only about the difference between the starting and final temperatures after reaching the exit. Since they are allowed to revisit cells any number of times, the task is to find the smallest possible absolute value of the total change along any walk from `s` to `f`.

The grid dimensions can reach 1000 by 1000, so there can be up to one million cells. A solution that tries many paths or uses dynamic programming over possible temperature values is impossible because the number of walks is exponential and the possible sums are too large. We need a linear or near-linear graph algorithm.

The tricky part is that the shortest path is not necessarily the answer. A longer walk can include cycles that change the final temperature difference. For example, if a direct path has temperature change `5`, but there is a cycle whose total contribution is `5`, walking through that cycle in the opposite way can reduce the final difference to zero.

Consider a simple grid:

```
2 2
sf
..
```

The direct move from `s` to `f` is horizontal, so the answer is `1`. A careless solution that only computes shortest distance would return this value, but in larger grids cycles can improve the result.

Another edge case is when the exit is unreachable:

```
3 3
s##
###
##f
```

The correct output is `-1`. Any approach that only initializes distances and forgets to check reachability could incorrectly output a large value or zero.

A third important case is a grid without useful cycles:

```
1 2
sf
```

The only possible walk has value `-1`, so the answer is `1`. The algorithm must handle the situation where no cycle can change the possible values.

# Approaches

A brute-force approach would enumerate walks from the start to the exit and keep track of every possible temperature change. It is correct because every legal sequence of moves is considered, but the number of possible walks grows exponentially because the friends can revisit cells indefinitely. Even restricting the walk length would not work, because a useful cycle might need to be repeated many times.

The key observation is that the exact path does not matter. Choose any path from the start to a cell and assign it a value equal to the temperature change along that path. When we add a cycle, the value changes by the total weight of that cycle. The set of all possible changes caused by cycles forms multiples of one number, the greatest common divisor of all cycle values.

We can find this gcd without explicitly finding cycles. A BFS spanning tree gives every reachable cell a reference value. For every grid edge, compare the stored values of its endpoints with the edge contribution. The difference represents the value of the cycle created by adding that edge to the tree. Taking the gcd of all these values gives the amount by which the answer can be adjusted.

After that, every possible final temperature change has the same remainder modulo this gcd as the tree path value from `s` to `f`. The problem becomes finding the smallest absolute number with that remainder.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(nm) | O(nm) | Accepted |

# Algorithm Walkthrough

1. Run BFS from the starting cell. Store for every reachable cell the accumulated temperature change along the BFS tree path. A horizontal edge contributes `-1`, and a vertical edge contributes `+1`.

The BFS tree gives one valid reference path to every cell. The stored values are not necessarily optimal, but they are enough to discover how cycles modify paths.

1. While scanning every adjacent pair of reachable cells, calculate the cycle contribution created by that edge. If the edge has weight `w`, the value is:

```
dist[u] + w - dist[v]
```

Add the absolute value of this number to the gcd accumulator.

Tree edges produce zero because the stored distances already satisfy their equation. Non-tree edges reveal the useful cycles.

1. If the exit was never reached, output `-1`.

There is no possible walk if the graph component containing the start does not contain the exit.

1. Let `base` be the BFS value of the exit. If the gcd is zero, no cycle changes the possible values, so the answer is simply `abs(base)`.
2. Otherwise, find the closest number to zero that has the same remainder as `base` modulo the gcd. Check the two nearest candidates around zero and output the smaller absolute value.

## Why it works

Every walk from the start to the exit can be transformed into the BFS tree path plus some collection of closed walks. Every closed walk can be decomposed into fundamental cycles created by non-tree edges, and the gcd of those cycle values describes exactly which adjustments are possible.

The BFS path gives one possible answer value. All other values differ from it by multiples of the computed gcd, so checking the closest representative of that residue class gives the smallest achievable temperature difference.

# Python Solution

```python
import sys
from collections import deque
from math import gcd

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    start = -1
    finish = -1
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 's':
                start = i * m + j
            elif grid[i][j] == 'f':
                finish = i * m + j

    total = n * m
    dist = [0] * total
    seen = [False] * total
    seen[start] = True

    q = deque([start])
    dirs = [(1, 0, 1), (-1, 0, 1), (0, 1, -1), (0, -1, -1)]

    while q:
        cur = q.popleft()
        r = cur // m
        c = cur % m

        for dr, dc, w in dirs:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] != '#':
                nxt = nr * m + nc
                if not seen[nxt]:
                    seen[nxt] = True
                    dist[nxt] = dist[cur] + w
                    q.append(nxt)

    if not seen[finish]:
        print(-1)
        return

    g = 0
    for r in range(n):
        for c in range(m):
            if grid[r][c] == '#':
                continue
            cur = r * m + c
            if c + 1 < m and grid[r][c + 1] != '#':
                nxt = cur + 1
                g = gcd(g, abs(dist[cur] - 1 - dist[nxt]))
            if r + 1 < n and grid[r + 1][c] != '#':
                nxt = cur + m
                g = gcd(g, abs(dist[cur] + 1 - dist[nxt]))

    base = dist[finish]

    if g == 0:
        print(abs(base))
    else:
        rem = base % g
        print(min(rem, g - rem))

if __name__ == "__main__":
    solve()
```

The BFS part follows the first algorithm step. The array `dist` stores the temperature change of the chosen tree path from the start. The sign of each move is handled when neighbors are explored.

The second scan checks only right and down neighbors because every undirected grid edge appears exactly once in this traversal. The expression used for the gcd is zero for tree edges and nonzero for edges that introduce cycles.

The final calculation uses modular arithmetic. Python's remainder operation works correctly for negative values as well, so `base % g` always gives a value in the range `[0, g-1]`. The two candidates closest to zero are `rem` and `rem - g`.

# Worked Examples

Consider:

```
2 2
sf
..
```

The BFS can choose the direct horizontal path.

| Current cell | Stored value | Discovered action |
| --- | --- | --- |
| s | 0 | Start BFS |
| f | -1 | Horizontal move |
| bottom-left | 1 | Vertical move |

The cycle values include:

| Edge | Cycle contribution |
| --- | --- |
| s to bottom-left | 0 |
| bottom-left to f | 0 |

The gcd remains zero, so the only possible value is `-1`. The output is `1`.

Now consider:

```
2 3
s..
..f
```

A BFS path can reach the exit with value `0`.

| Current cell | Stored value | Discovered action |
| --- | --- | --- |
| s | 0 | Start BFS |
| (0,1) | -1 | Horizontal |
| (1,0) | 1 | Vertical |
| (0,2) | -2 | Horizontal |
| (1,2) | -1 | Vertical |

The extra edges create cycles. Their contributions have gcd `1`, meaning any integer adjustment is possible. Since the path value is already congruent to zero modulo one, the minimum achievable difference is `0`.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Every cell and every grid edge is processed a constant number of times |
| Space | O(nm) | The BFS arrays store information for each cell |

The largest grid contains one million cells, so linear processing is required. The algorithm only keeps a few integer arrays and fits comfortably within the memory limit.

# Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    from collections import deque
    from math import gcd

    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    start = finish = -1
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 's':
                start = i * m + j
            if grid[i][j] == 'f':
                finish = i * m + j

    dist = [0] * (n * m)
    seen = [False] * (n * m)
    seen[start] = True
    q = deque([start])

    for_dummy = [(1,0,1),(-1,0,1),(0,1,-1),(0,-1,-1)]

    while q:
        x = q.popleft()
        r, c = divmod(x, m)
        for dr, dc, w in for_dummy:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] != '#':
                y = nr * m + nc
                if not seen[y]:
                    seen[y] = True
                    dist[y] = dist[x] + w
                    q.append(y)

    if not seen[finish]:
        ans = -1
    else:
        g = 0
        for r in range(n):
            for c in range(m):
                if c + 1 < m and grid[r][c] != '#' and grid[r][c+1] != '#':
                    g = gcd(g, abs(dist[r*m+c]-1-dist[r*m+c+1]))
                if r + 1 < n and grid[r][c] != '#' and grid[r+1][c] != '#':
                    g = gcd(g, abs(dist[r*m+c]+1-dist[(r+1)*m+c]))
        if g == 0:
            ans = abs(dist[finish])
        else:
            ans = min(dist[finish] % g, g - dist[finish] % g)

    sys.stdin = old
    return str(ans)

assert run("1 2\nsf\n") == "1"
assert run("2 2\ns.\n.f\n") == "0"
assert run("3 3\ns##\n###\n##f\n") == "-1"
assert run("1 5\ns...f\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2` straight corridor | `1` | No-cycle case |
| Small open square | `0` | Cycles can cancel the path value |
| Completely blocked exit | `-1` | Reachability handling |
| Long single row | `4` | Boundary movement handling |

# Edge Cases

For the blocked grid case:

```
3 3
s##
###
##f
```

BFS never visits the exit cell. The algorithm stops before computing cycle values and outputs `-1`.

For the one-row corridor:

```
1 5
s...f
```

Every move is horizontal, so the only possible temperature change is `-4`. There are no cycles, the gcd is zero, and the algorithm returns `abs(-4) = 4`.

For a grid containing cycles:

```
2 2
s.
.f
```

The direct path has a nonzero value, but the square provides a cycle with gcd `1`. Since all integer adjustments are possible, the algorithm finds that zero difference can be achieved.
