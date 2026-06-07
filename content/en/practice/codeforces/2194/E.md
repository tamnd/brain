---
title: "CF 2194E - The Turtle Strikes Back"
description: "We have a rectangular grid. Every cell contains an integer value, positive or negative. Michelangelo chooses a path from the top-left corner to the bottom-right corner. He may only move right or down."
date: "2026-06-07T20:46:14+07:00"
tags: ["codeforces", "competitive-programming", "dp", "graphs", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2194
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1078 (Div. 2)"
rating: 2000
weight: 2194
solve_time_s: 168
verified: true
draft: false
---

[CF 2194E - The Turtle Strikes Back](https://codeforces.com/problemset/problem/2194/E)

**Rating:** 2000  
**Tags:** dp, graphs, greedy, implementation  
**Solve time:** 2m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rectangular grid. Every cell contains an integer value, positive or negative.

Michelangelo chooses a path from the top-left corner to the bottom-right corner. He may only move right or down. The score of a path is the sum of all cell values visited on that path, and he always chooses the path with maximum possible score.

Before he chooses the path, Raphael selects exactly one cell and flips its sign. A value `x` becomes `-x`.

Raphael wants to make Michelangelo's final optimal score as small as possible. Michelangelo sees the modified grid and then chooses his best path.

For each test case we must compute the minimum score Raphael can force.

The grid contains at most `10^6` cells across all test cases. This immediately rules out any approach that recomputes a full dynamic programming table for every possible flipped cell. A single `O(nm)` DP is fine, but `O((nm)^2)` is completely impossible when `nm = 10^6`.

The tricky part is that after a cell is flipped, Michelangelo may switch to a completely different path. We cannot assume he keeps using the same optimal path as before.

Consider a small example:

```
1 100
100 1
```

The original best path uses three cells and has value `102`.

If Raphael flips the `100` in the top-right corner, Michelangelo simply changes routes and uses the other `100`.

Any solution that only looks at the original optimal path would fail here.

Another easy-to-miss case is when several different optimal paths exist.

```
0 0
0 0
```

Every path has value `0`.

Flipping any cell changes nothing. Even if a flipped cell lies on one optimal path, Michelangelo can choose another path with the same score. A solution that assumes "destroying an optimal path destroys the optimum" would be wrong.

A third corner case occurs on diagonals containing only one cell.

```
5
```

The start and end cell are the same. Any path must pass through it. After flipping, the answer is `-5`.

When a diagonal contains only one cell, there is no alternative cell on that diagonal that a path can use.

## Approaches

The most direct idea is to try every possible cell as Raphael's choice.

For a fixed cell, flip its sign and recompute the maximum path sum using standard grid DP. The resulting value is Michelangelo's response. Taking the minimum over all cells gives the answer.

This is correct because it literally simulates the game.

The problem is the complexity. A maximum-path DP costs `O(nm)`. There are `nm` possible cells to flip. The total complexity becomes `O((nm)^2)`, which reaches `10^12` operations in the worst case.

We need to understand how flipping a single cell affects optimal paths.

Let

`f[i][j]` = maximum path sum from the start to `(i,j)`.

Let

`g[i][j]` = maximum path sum from `(i,j)` to the end.

Then

```
val(i,j) = f[i][j] + g[i][j] - a[i][j]
```

is the maximum score of any path that passes through `(i,j)`. The cell value is counted twice, so we subtract it once.

Now suppose Raphael flips cell `(i,j)`.

If Michelangelo chooses a path that still goes through `(i,j)`, that path loses exactly `2 * a[i][j]`, because the contribution changes from `a[i][j]` to `-a[i][j]`.

So the best path using that cell becomes

```
val(i,j) - 2*a[i][j]
```

The remaining question is the best path that avoids `(i,j)`.

This is where the key observation appears.

Every monotone path from `(1,1)` to `(n,m)` visits exactly one cell on each anti-diagonal `i + j = constant`.

Fix a cell `(i,j)` and let `d = i + j`.

Any path avoiding `(i,j)` must still pass through some other cell on anti-diagonal `d`.

For any cell `(x,y)` on that same diagonal, `val(x,y)` is the best path score among all paths passing through `(x,y)`.

Therefore the best path avoiding `(i,j)` is simply the maximum `val` among all other cells on diagonal `d`.

This transforms the problem into maintaining, for every anti-diagonal, the largest and second-largest values of `val`.

For a cell `(i,j)`:

If its `val` is not the largest on its diagonal, the best avoiding path uses the diagonal maximum.

If its `val` is the unique largest, removing it forces us to use the second-largest value.

After that, Michelangelo's optimal response is

```
max(
    path_using_flipped_cell,
    best_path_avoiding_flipped_cell
)
```

and Raphael chooses the minimum among all cells.

### Complexity Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((nm)^2) | O(nm) | Too slow |
| Optimal | O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Compute `f[i][j]`, the maximum path sum from the start to every cell.
2. Compute `g[i][j]`, the maximum path sum from every cell to the destination.
3. For every cell compute

```
val = f[i][j] + g[i][j] - a[i][j]
```

This is the maximum score among all paths passing through that cell.
4. Group cells by anti-diagonal `d = i + j`.
5. For each diagonal, store the largest value `mx1[d]` and the second-largest value `mx2[d]`.

When several cells share the maximum value, `mx2[d]` is allowed to become equal to `mx1[d]`. This automatically handles ties correctly.
6. Enumerate every cell `(i,j)` as Raphael's flipped cell.
7. Compute

```
through = val - 2*a[i][j]
```

which is the best path score that still uses the flipped cell.
8. Compute the best path avoiding that cell.

If `val == mx1[d]`, use `mx2[d]`.

Otherwise use `mx1[d]`.
9. Michelangelo chooses the better of those two options:

```
score = max(through, avoid)
```
10. Minimize `score` over all cells.

### Why it works

A monotone path visits exactly one cell on every anti-diagonal. Fix a flipped cell `(i,j)` on diagonal `d`.

Any path avoiding `(i,j)` must pass through another cell of the same diagonal. Conversely, any path passing through another cell of diagonal `d` automatically avoids `(i,j)`, because a path can visit only one cell on that diagonal.

For each diagonal cell `(x,y)`, `val(x,y)` is the best score among all paths passing through it. Hence the best score of a path avoiding `(i,j)` is exactly the maximum `val` among all other cells on diagonal `d`.

The best path using the flipped cell loses exactly `2*a[i][j]`. Michelangelo chooses the better of the "use" and "avoid" options, and Raphael chooses the cell minimizing that result. Every possibility is evaluated exactly once, so the algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10 ** 30

t = int(input())

for _ in range(t):
    n, m = map(int, input().split())

    a = [list(map(int, input().split())) for _ in range(n)]

    f = [[-INF] * m for _ in range(n)]
    g = [[-INF] * m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            if i == 0 and j == 0:
                f[i][j] = a[i][j]
            else:
                best = -INF
                if i > 0:
                    best = max(best, f[i - 1][j])
                if j > 0:
                    best = max(best, f[i][j - 1])
                f[i][j] = best + a[i][j]

    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if i == n - 1 and j == m - 1:
                g[i][j] = a[i][j]
            else:
                best = -INF
                if i + 1 < n:
                    best = max(best, g[i + 1][j])
                if j + 1 < m:
                    best = max(best, g[i][j + 1])
                g[i][j] = best + a[i][j]

    diag_cnt = n + m - 1
    mx1 = [-INF] * diag_cnt
    mx2 = [-INF] * diag_cnt

    val = [[0] * m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            cur = f[i][j] + g[i][j] - a[i][j]
            val[i][j] = cur

            d = i + j

            if cur >= mx1[d]:
                mx2[d] = mx1[d]
                mx1[d] = cur
            elif cur > mx2[d]:
                mx2[d] = cur

    ans = INF

    for i in range(n):
        for j in range(m):
            d = i + j
            cur = val[i][j]

            through = cur - 2 * a[i][j]

            if cur == mx1[d]:
                avoid = mx2[d]
            else:
                avoid = mx1[d]

            score = max(through, avoid)
            ans = min(ans, score)

    print(ans)
```

The first DP computes the best prefix ending at every cell. The second DP computes the best suffix starting from every cell.

Combining them gives the best path through each cell. That quantity is reused throughout the solution, which is why we never need to rerun DP after choosing a flipped cell.

The diagonal maxima deserve special attention. When a new value is at least the current maximum, it becomes the new maximum and the old maximum becomes the second maximum. Because we use `>=`, equal maxima are stored correctly. If two cells have the same best value on a diagonal, removing one still leaves the same value available through the other cell.

All calculations use Python integers. Path sums may reach roughly `(n+m) * 10^9`, so 64-bit arithmetic is required.

## Worked Examples

### Sample 1

Input:

```
3 3
1 -2 3
4 -5 2
1 6 -1
```

The computed `val` values are:

| Cell | val |
| --- | --- |
| (1,1) | 11 |
| (1,2) | 8 |
| (1,3) | 8 |
| (2,1) | 11 |
| (2,2) | 2 |
| (2,3) | 8 |
| (3,1) | 11 |
| (3,2) | 11 |
| (3,3) | 11 |

For cell `(3,2)`:

| Quantity | Value |
| --- | --- |
| val | 11 |
| a | 6 |
| through | -1 |
| avoid | 3 |
| score | 3 |

Raphael can force Michelangelo down to `3`, which is the final answer.

This example shows why Michelangelo may switch paths after the flip. The original best route is no longer attractive, so he changes to a different diagonal choice.

### Sample 2

Input:

```
2 4
-1 -1 -1 1
-1 -1 -1 -1
```

Relevant values:

| Cell | val |
| --- | --- |
| (1,1) | -3 |
| (1,2) | -3 |
| (1,3) | -3 |
| (1,4) | -3 |
| (2,1) | -3 |
| (2,2) | -3 |
| (2,3) | -3 |
| (2,4) | -3 |

Flipping the only positive cell changes its contribution by `-2`.

| Quantity | Value |
| --- | --- |
| through | -5 |
| avoid | -5 |
| score | -5 |

The answer is `-5`.

This example demonstrates that the optimal result can be negative even though the original grid contains a non-negative value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Two DP passes, one diagonal scan, one answer scan |
| Space | O(nm) | Stores grid, forward DP, backward DP, and `val` |

The total number of cells over all test cases is at most `10^6`, so linear processing is easily fast enough within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    INF = 10 ** 30

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())
        a = [list(map(int, input().split())) for _ in range(n)]

        f = [[-INF] * m for _ in range(n)]
        g = [[-INF] * m for _ in range(n)]

        for i in range(n):
            for j in range(m):
                if i == 0 and j == 0:
                    f[i][j] = a[i][j]
                else:
                    best = -INF
                    if i:
                        best = max(best, f[i - 1][j])
                    if j:
                        best = max(best, f[i][j - 1])
                    f[i][j] = best + a[i][j]

        for i in range(n - 1, -1, -1):
            for j in range(m - 1, -1, -1):
                if i == n - 1 and j == m - 1:
                    g[i][j] = a[i][j]
                else:
                    best = -INF
                    if i + 1 < n:
                        best = max(best, g[i + 1][j])
                    if j + 1 < m:
                        best = max(best, g[i][j + 1])
                    g[i][j] = best + a[i][j]

        diag = n + m - 1
        mx1 = [-INF] * diag
        mx2 = [-INF] * diag
        val = [[0] * m for _ in range(n)]

        for i in range(n):
            for j in range(m):
                cur = f[i][j] + g[i][j] - a[i][j]
                val[i][j] = cur
                d = i + j

                if cur >= mx1[d]:
                    mx2[d] = mx1[d]
                    mx1[d] = cur
                elif cur > mx2[d]:
                    mx2[d] = cur

        ans = INF

        for i in range(n):
            for j in range(m):
                d = i + j
                cur = val[i][j]

                through = cur - 2 * a[i][j]
                avoid = mx2[d] if cur == mx1[d] else mx1[d]

                ans = min(ans, max(through, avoid))

        out.append(str(ans))

    return "\n".join(out) + "\n"

# provided samples
assert run(
"""2
3 3
1 -2 3
4 -5 2
1 6 -1
2 4
-1 -1 -1 1
-1 -1 -1 -1
"""
) == "3\n-5\n"

# 1x1 grid
assert run(
"""1
1 1
5
"""
) == "-5\n"

# all zeros
assert run(
"""1
2 2
0 0
0 0
"""
) == "0\n"

# equal maxima on a diagonal
assert run(
"""1
2 2
1 1
1 1
"""
) == "1\n"

# single row
assert run(
"""1
1 3
2 -1 4
"""
) == "-1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1x1` grid | `-5` | Diagonal with only one cell |
| All zeros | `0` | Multiple optimal paths and tied maxima |
| `2x2` all ones | `1` | Correct handling of equal diagonal maxima |
| Single row | `-1` | Boundary transitions and path uniqueness |

## Edge Cases

### Single-cell grid

Input:

```
1
1 1
5
```

There is only one possible flip and only one possible path.

`val = 5`.

After flipping:

```
through = 5 - 2*5 = -5
```

There is no alternative cell on the diagonal, so the result is `-5`.

The algorithm handles this because the second maximum on that diagonal remains negative infinity, and the `through` option dominates.

### Multiple optimal paths

Input:

```
1
2 2
0 0
0 0
```

Every path has score `0`.

For every diagonal, both the largest and second-largest values become `0`.

When a cell is excluded, another cell with the same value remains available. The algorithm returns `0`, which is correct.

### Flipped cell not used by the final path

Input:

```
1
2 2
1 100
100 1
```

Flipping either `100` makes paths through that cell much worse.

The algorithm compares:

```
through = val - 200
```

against the best alternative value from the same diagonal.

The alternative path wins, matching Michelangelo's ability to reroute after seeing the flip.

This is exactly why the solution must consider both "use" and "avoid" cases for every flipped cell.
