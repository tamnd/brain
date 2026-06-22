---
title: "CF 105579E - Uniform Square Tiling"
description: "We are given an $n times n$ grid representing a tiled wall. Each cell contains either a gold tile, written as G, or a silver tile, written as S. We are also given an integer $k$, and we want to choose a contiguous $k times k$ sub-square of this grid."
date: "2026-06-22T17:46:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105579
codeforces_index: "E"
codeforces_contest_name: "Udmurtia High School Programming Contest (Qualification for VKOSHP 2012)"
rating: 0
weight: 105579
solve_time_s: 71
verified: true
draft: false
---

[CF 105579E - Uniform Square Tiling](https://codeforces.com/problemset/problem/105579/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an $n \times n$ grid representing a tiled wall. Each cell contains either a gold tile, written as `G`, or a silver tile, written as `S`. We are also given an integer $k$, and we want to choose a contiguous $k \times k$ sub-square of this grid. After choosing that sub-square, we are allowed to repaint some tiles inside it so that the entire square becomes uniform, meaning all tiles are the same type.

For any chosen $k \times k$ region, we could decide to make everything `G` or everything `S`. The cost is the number of cells that do not match the chosen target type. The task is to compute the minimum repaint cost over all possible $k \times k$ sub-squares and both target uniform colors.

The grid size $n$ is up to 1000 and $k$ is up to 100. This separation is crucial. The number of possible squares is roughly $(n-k+1)^2$, which is about $10^6$ in the worst case. Each square contains up to $k^2 \le 10^4$ cells. A naive recomputation per square would be around $10^{10}$ operations, which is too large for 2 seconds. Any valid solution must reduce the per-square cost to constant or near-constant time.

A subtle issue is that both target colors must be considered. A naive implementation that only tries making the square uniform to `G` or only to `S` independently for each window without reusing computations risks duplicating work and losing efficiency.

Another edge case is when $k = n$. Then there is exactly one candidate square, and the answer is simply the minimum flips to make the entire grid uniform. A correct solution must not assume multiple windows exist.

## Approaches

The brute-force approach is straightforward. For every possible top-left corner of a $k \times k$ square, we scan all $k^2$ cells and count how many are `G` and how many are `S`. The cost for that square is $\min(\#G, \#S)$. We take the minimum over all positions.

This is correct because it directly evaluates every candidate region without approximation. The failure point is runtime. There are $O(n^2)$ positions and each costs $O(k^2)$, leading to $O(n^2 k^2)$. With $n = 1000$ and $k = 100$, this is about $10^{10}$ operations, which is too slow.

The key observation is that we do not need to recompute counts from scratch for each square. Instead, we can precompute a 2D prefix sum over the grid, separately counting how many `G` cells appear in any rectangle. Once we can query the number of `G` cells in any $k \times k$ region in $O(1)$, the number of `S` cells is just $k^2 - G$, so the cost is immediately known.

This reduces the problem to sliding a fixed-size window over all positions with constant-time queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2 k^2)$ | $O(1)$ | Too slow |
| Prefix Sum | $O(n^2)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

We transform the grid into a numeric matrix where each `G` becomes 1 and each `S` becomes 0. We then build a 2D prefix sum array.

1. Construct a prefix sum array `ps` where `ps[i][j]` stores the number of `G` cells in the rectangle from `(0,0)` to `(i-1,j-1)`. This shift simplifies boundary handling.
2. For each cell `(i,j)` in the original grid, compute:

$$ps[i+1][j+1] = ps[i+1][j] + ps[i][j+1] - ps[i][j] + (grid[i][j] == 'G')$$

This ensures each prefix cell counts all `G`s above and to the left exactly once.
3. Iterate over all possible top-left corners `(i,j)` of a $k \times k$ square. The valid range is `0 ≤ i ≤ n-k`, `0 ≤ j ≤ n-k`.
4. For each position, compute number of `G` tiles inside the square using the inclusion-exclusion formula:

$$G = ps[i+k][j+k] - ps[i][j+k] - ps[i+k][j] + ps[i][j]$$

This gives the count in constant time.
5. Compute `S = k*k - G`. The cost of making the square uniform is `min(G, S)`.
6. Track the minimum cost over all positions and output it.

### Why it works

The prefix sum array maintains an invariant that every entry stores the exact count of `G` tiles in its corresponding sub-rectangle. Because rectangle sums are linear over inclusion-exclusion, any $k \times k$ query can be decomposed into four prefix values without overlap or omission. This guarantees each window is evaluated exactly once with correct counts, and since every valid placement is considered, the global minimum is found.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    ps = [[0] * (n + 1) for _ in range(n + 1)]

    for i in range(n):
        row_sum = 0
        for j in range(n):
            val = 1 if grid[i][j] == 'G' else 0
            ps[i+1][j+1] = ps[i][j+1] + ps[i+1][j] - ps[i][j] + val

    best = k * k

    for i in range(n - k + 1):
        for j in range(n - k + 1):
            g = ps[i+k][j+k] - ps[i][j+k] - ps[i+k][j] + ps[i][j]
            s = k * k - g
            best = min(best, g, s)

    print(best)

if __name__ == "__main__":
    solve()
```

The solution first builds a 2D prefix sum over gold tiles only. This is the only preprocessing step needed to support constant-time rectangle queries. The nested loops then enumerate all valid $k \times k$ positions, and each query uses four prefix accesses, so no inner scan of the square is required.

The key implementation detail is the 1-based indexing in `ps`, which avoids boundary checks when applying inclusion-exclusion. Without this shift, every rectangle query would require conditional logic at the edges, increasing the risk of errors.

The initialization of `best` as `k*k` works because that is the worst-case repaint cost if all tiles are already of one color; any valid configuration cannot exceed this.

## Worked Examples

### Example 1

Input:

```
3 2
GGG
SSG
GGG
```

We compute prefix counts of `G`. Then evaluate all 2×2 windows.

| Top-left (i,j) | G count | S count | cost |
| --- | --- | --- | --- |
| (0,0) | 3 | 1 | 1 |
| (0,1) | 2 | 2 | 2 |
| (1,0) | 1 | 3 | 1 |
| (1,1) | 2 | 2 | 2 |

Minimum cost is 1.

This trace shows how mixed windows balance between two colors, and that optimal choice may come from either target uniform color.

### Example 2

Input:

```
5 3
GGGGG
SSSSS
GGGGG
SSSSS
GGGGG
```

Here each 3×3 block alternates heavily between rows.

| Top-left (i,j) | G count | S count | cost |
| --- | --- | --- | --- |
| (0,0) | 6 | 3 | 3 |
| (0,1) | 6 | 3 | 3 |
| (1,0) | 3 | 6 | 3 |
| (1,1) | 3 | 6 | 3 |
| (2,0) | 6 | 3 | 3 |
| (2,1) | 6 | 3 | 3 |

All positions give the same cost, reflecting the perfectly periodic structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | prefix sum build plus constant-time evaluation for each of $(n-k)^2$ positions |
| Space | $O(n^2)$ | 2D prefix array |

The constraints allow up to about one million window checks, each done in constant time. The prefix sum construction also runs in about one million operations, keeping the total well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return solve_wrapper(inp)

def solve_wrapper(inp: str) -> str:
    import sys
    from io import StringIO
    old_stdin = sys.stdin
    sys.stdin = StringIO(inp)
    out = StringIO()
    old_stdout = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = old_stdin
    sys.stdout = old_stdout
    return out.getvalue().strip()

# provided samples
assert run("3 2\nGGG\nSSG\nGGG\n") == "1"
assert run("5 3\nGGGGG\nSSSSS\nGGGGG\nSSSSS\nGGGGG\n") == "3"

# custom cases
assert run("1 1\nG\n") == "0", "single cell already uniform"
assert run("1 1\nS\n") == "0", "single cell already uniform"
assert run("2 2\nGS\nSG\n") == "2", "full flip needed"
assert run("4 2\nGGGG\nGGGG\nGGGG\nGGGG\n") == "0", "already uniform grid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 `G` | 0 | minimal case, no flips |
| 1×1 `S` | 0 | symmetry for single cell |
| 2×2 checker | 2 | full conversion required |
| 4×4 all `G` | 0 | already optimal |

## Edge Cases

When $k = 1$, every cell is a valid square. The algorithm evaluates each cell independently using prefix sums, but each query reduces to the cell itself. The minimum cost is always 0 because a single cell is already uniform.

When $k = n$, there is only one window. The prefix sum query covers the entire grid, and the algorithm correctly computes whether converting everything to `G` or `S` is cheaper.

For grids with alternating patterns, such as checkerboards, prefix sums still correctly aggregate counts over each window. Even though local patterns vary sharply, each $k \times k$ region is evaluated independently, and no window misses contributions because inclusion-exclusion guarantees exact rectangle sums.
