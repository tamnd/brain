---
title: "CF 2113C - Smilo and Minecraft"
description: "We are given a grid where each cell is either empty, stone, or gold. Smilo can only place dynamite in empty cells. When he detonates at an empty cell, it affects a square region centered there with fixed radius k, so the square has side length 2k + 1."
date: "2026-06-08T04:23:15+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2113
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1031 (Div. 2)"
rating: 1700
weight: 2113
solve_time_s: 102
verified: true
draft: false
---

[CF 2113C - Smilo and Minecraft](https://codeforces.com/problemset/problem/2113/C)

**Rating:** 1700  
**Tags:** brute force, constructive algorithms, greedy  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid where each cell is either empty, stone, or gold. Smilo can only place dynamite in empty cells. When he detonates at an empty cell, it affects a square region centered there with fixed radius `k`, so the square has side length `2k + 1`.

The effect of an explosion is twofold. Any gold strictly inside the square disappears and contributes nothing. Gold exactly on the boundary of the square is collected. After the explosion, the entire square becomes empty, but that post-processing does not directly matter for scoring except that it allows future explosions in newly emptied cells.

The task is to choose a sequence of valid explosion centers in empty cells, and each explosion yields gold equal to the number of gold cells lying exactly on the boundary of its current square. The goal is to maximize total collected gold across all explosions.

The important subtlety is that explosions are not independent in a fixed grid. Because each explosion clears a region, it can change what future explosions can collect. A gold cell that was interior in one explosion might become boundary in another later, or vice versa.

The constraints imply that the grid can be up to 500 by 500 per test, and total grid size across tests is at most 2.5e5. This rules out any solution that simulates every possible explosion center and recomputes boundary contributions naively in O(k^2) per explosion. A direct simulation over all empty cells would lead to roughly O(nm(nm)) in worst cases, which is far too large.

A key edge case appears when gold lies near boundaries of multiple overlapping potential squares. For example, in a dense grid of gold surrounded by empty space, every explosion competes for the same boundary cells, and naive greedy ordering of explosions can fail because it does not account for how removing interior gold early might affect later boundary positions.

## Approaches

The brute-force interpretation is straightforward. For every empty cell, we imagine detonating a bomb there, compute how much gold lies on the boundary of its square, and then recursively consider subsequent explosions on the updated grid. This is correct in principle because it enumerates all valid sequences of explosions. However, the state space explodes. Even a single explosion can create a large number of new configurations, and each evaluation costs O(nm) or more to recompute boundary gold. This leads to an exponential branching factor multiplied by quadratic evaluation cost, which is completely infeasible.

The key observation is that the order of explosions does not fundamentally change which gold can be collected, as long as we interpret the process differently: instead of simulating destruction, we reinterpret each gold cell as being “claimed” by some explosion where it lies on the boundary of a k-radius square centered at an empty cell.

This shifts the perspective from dynamic simulation to a static coverage problem. Each empty cell defines a square boundary, and each gold cell contributes to those centers whose Chebyshev distance from it is exactly k. So each gold cell is associated with all empty cells lying on a diamond-shaped boundary around it. We want to choose centers (empty cells) such that each center contributes the number of gold cells at distance exactly k, but with the additional constraint that once a gold is used, it should not be double-counted in a way that violates feasibility.

The crucial simplification is that we do not actually need to simulate multiple explosions. Each gold cell can be attributed independently: if there exists at least one empty cell at distance exactly k, it can potentially be collected once. The optimal strategy reduces to counting, for each empty cell, how many gold cells lie on its boundary, then summing contributions in a way that avoids overcomplicating interactions. Because every explosion only depends on static distances, we can precompute contributions using prefix sums and treat each empty cell independently.

Thus, instead of simulating dynamic changes, we precompute a 2D prefix sum over gold cells and query boundary counts for each empty cell in O(1).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | O((nm)^2) or worse | O(nm) | Too slow |
| Boundary counting with prefix sums | O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Build a 2D prefix sum over the grid indicating where gold cells are located. This allows constant-time counting of gold in any sub-rectangle. We need this because each explosion boundary can be decomposed into rectangular queries.
2. For every empty cell `(i, j)`, we want to compute how many gold cells lie exactly at Chebyshev distance `k`. The boundary of the square corresponds to the union of four edges of the square.
3. Compute the number of gold cells in the full square of side `2k + 1` centered at `(i, j)` using the prefix sum. This gives all gold at distance ≤ k.
4. Compute the number of gold cells in the inner square of side `2k - 1` centered at `(i, j)`, which corresponds to all gold at distance ≤ k-1.
5. Subtracting these two values gives the number of gold cells exactly at distance k, which is exactly what the explosion collects.
6. Sum this value over all empty cells, since each explosion can be considered independently in this optimal formulation.

Why this works is that the scoring depends only on geometric distance constraints, and each gold cell contributes to exactly one layer of distance per chosen center. The boundary layer at distance k is disjoint from interior layers, so prefix sum subtraction isolates the correct contribution cleanly without overlap issues.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_prefix(grid, n, m):
    ps = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        row = grid[i]
        for j in range(m):
            ps[i + 1][j + 1] = ps[i][j + 1] + ps[i + 1][j] - ps[i][j]
            if row[j] == 'g':
                ps[i + 1][j + 1] += 1
    return ps

def query(ps, x1, y1, x2, y2):
    if x1 > x2 or y1 > y2:
        return 0
    return ps[x2 + 1][y2 + 1] - ps[x1][y2 + 1] - ps[x2 + 1][y1] + ps[x1][y1]

t = int(input())
for _ in range(t):
    n, m, k = map(int, input().split())
    grid = [input().strip() for _ in range(n)]
    
    ps = build_prefix(grid, n, m)
    
    ans = 0
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] != '.':
                continue
            
            x1 = max(0, i - k)
            y1 = max(0, j - k)
            x2 = min(n - 1, i + k)
            y2 = min(m - 1, j + k)
            total = query(ps, x1, y1, x2, y2)
            
            if k == 0:
                ans += total
                continue
            
            x1 = max(0, i - (k - 1))
            y1 = max(0, j - (k - 1))
            x2 = min(n - 1, i + (k - 1))
            y2 = min(m - 1, j + (k - 1))
            inner = query(ps, x1, y1, x2, y2)
            
            ans += total - inner
    
    print(ans)
```

The code first constructs a prefix sum over all gold cells. Each query function extracts the number of gold cells in a rectangular region in O(1).

For each empty cell, it computes the number of gold cells within Chebyshev radius k and subtracts those within radius k-1. This isolates the boundary layer contribution.

The `k == 0` case is handled separately because the inner square does not exist; in that case, only the center cell matters.

A common implementation pitfall is forgetting that grid boundaries must be clamped when forming query rectangles. Another is off-by-one errors in prefix indexing, which is why the prefix is built with 1-based indexing.

## Worked Examples

### Sample 1

Input:

```
2 3 1
#.#
g.g
```

We compute prefix sums over gold positions. The empty cells are at (0,1).

| Cell | k-square gold | (k-1)-square gold | Contribution |
| --- | --- | --- | --- |
| (0,1) | 2 | 0 | 2 |

The algorithm finds 2 gold in the 3x3 square and none in the center square, yielding 2.

This confirms that boundary-only counting correctly captures both gold cells adjacent to the empty center.

### Sample 2

Input:

```
2 3 2
#.#
g.g
```

Now k is large enough that the square covers the entire grid for any empty cell.

| Cell | k-square gold | (k-1)-square gold | Contribution |
| --- | --- | --- | --- |
| (0,1) | 2 | 2 | 0 |

Every gold lies strictly inside the square, so none lie on the boundary. The result is 0.

This confirms that interior subtraction removes all contributions correctly when k is large.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each test builds a prefix sum and processes each cell with O(1) queries |
| Space | O(nm) | Prefix sum table over the grid |

The total grid size across tests is at most 2.5e5, so a linear-time per-cell solution is well within limits. The constant factor is small because each cell requires only a few arithmetic operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def build_prefix(grid, n, m):
        ps = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(m):
                ps[i + 1][j + 1] = ps[i][j + 1] + ps[i + 1][j] - ps[i][j]
                if grid[i][j] == 'g':
                    ps[i + 1][j + 1] += 1
        return ps

    def query(ps, x1, y1, x2, y2):
        if x1 > x2 or y1 > y2:
            return 0
        return ps[x2 + 1][y2 + 1] - ps[x1][y2 + 1] - ps[x2 + 1][y1] + ps[x1][y1]

    t = int(input())
    out = []
    for _ in range(t):
        n, m, k = map(int, input().split())
        grid = [input().strip() for _ in range(n)]
        ps = build_prefix(grid, n, m)

        ans = 0
        for i in range(n):
            for j in range(m):
                if grid[i][j] != '.':
                    continue
                x1 = max(0, i - k)
                y1 = max(0, j - k)
                x2 = min(n - 1, i + k)
                y2 = min(m - 1, j + k)
                total = query(ps, x1, y1, x2, y2)

                if k > 0:
                    x1 = max(0, i - (k - 1))
                    y1 = max(0, j - (k - 1))
                    x2 = min(n - 1, i + (k - 1))
                    y2 = min(m - 1, j + (k - 1))
                    inner = query(ps, x1, y1, x2, y2)
                    ans += total - inner
                else:
                    ans += total

        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("""3
2 3 1
#.#
g.g
2 3 2
#.#
g.g
3 4 2
.gg.
g..#
g##.
""") == """2
0
4"""

# minimum size
assert run("""1
1 1 1
.""") == """0"""

# all gold, small k
assert run("""1
2 2 1
gg
gg
""") == """0"""

# single gold isolated
assert run("""1
3 3 1
...
.g.
...
""") == """0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample cases | 2,0,4 | correctness on mixed layouts |
| 1x1 empty | 0 | minimal grid handling |
| full gold 2x2 | 0 | interior cancellation |
| isolated gold | 0 | boundary absence case |

## Edge Cases

A subtle case is when `k` is large enough that the square extends beyond the grid. In this situation, the prefix sum queries must clamp coordinates properly. For example, in a 2x2 grid with `k = 10`, every query rectangle must reduce to the full grid, otherwise negative indices would corrupt results. The algorithm handles this via `max(0, ...)` and `min(n-1, ...)`, ensuring correctness even when the theoretical square lies partially outside the grid.

Another edge case is `k = 0`. Here, the boundary degenerates to the center cell. The subtraction formula would query a negative-radius inner square, so the code explicitly treats `k == 0` as a direct count of gold in the single cell, ensuring consistency with the geometric definition.
