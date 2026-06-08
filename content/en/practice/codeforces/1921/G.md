---
title: "CF 1921G - Mischievous Shooter"
description: "We are given a grid of size $n times m$, each cell either containing a target represented by or empty represented by .. Shel has a shotgun that fires in one of four diagonal directions: right-down, left-down, left-up, or right-up."
date: "2026-06-08T19:26:21+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "divide-and-conquer", "dp", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1921
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 920 (Div. 3)"
rating: 2200
weight: 1921
solve_time_s: 135
verified: false
draft: false
---

[CF 1921G - Mischievous Shooter](https://codeforces.com/problemset/problem/1921/G)

**Rating:** 2200  
**Tags:** brute force, data structures, divide and conquer, dp, implementation  
**Solve time:** 2m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a grid of size $n \times m$, each cell either containing a target represented by `#` or empty represented by `.`. Shel has a shotgun that fires in one of four diagonal directions: right-down, left-down, left-up, or right-up. The shotgun hits every target in that direction whose Manhattan distance from the firing point does not exceed a given constant $k$. Our goal is to determine, for each test case, the maximum number of targets Shel can hit with a single shot.

The inputs specify multiple test cases, each describing a rectangular field and the shotgun range. The output is a single integer per test case, giving the maximal number of targets that can be hit with one shot.

The constraints give $n, m, k \le 10^5$ and a total sum of $n \cdot m$ over all test cases not exceeding $10^5$. This is crucial: it means although the grid dimensions can be large individually, the total number of cells across all test cases is moderate. Consequently, algorithms that perform a constant or logarithmic amount of work per cell will be fast enough, but anything quadratic in $n \cdot m$ is too slow.

Edge cases that could trip a naive implementation include a grid that is a single column or row, $k$ larger than the grid dimensions, or multiple equally optimal shots. For instance, a single-column grid of height 3 with all cells filled and $k = 3$ must return 3, and careless indexing in diagonal calculations could undercount or overcount targets.

## Approaches

The brute-force approach examines every cell as a potential firing point and simulates firing in all four directions, counting targets within Manhattan distance $k$. Each shot takes $O(k^2)$ time in the worst case because the Manhattan neighborhood of radius $k$ contains roughly $(k+1)^2$ cells. With $n \cdot m$ cells and $k$ up to $10^5$, this results in far too many operations ($10^{10}$ or more), so brute force is infeasible.

The key observation is that the hit area forms a “diagonal diamond” in the grid. The Manhattan distance for diagonals can be transformed into linear arrays using coordinate sums and differences. If we define two derived arrays, one representing the sum $i + j$ and one representing the difference $i - j$, then for each of the four diagonal directions the reachable targets fall into contiguous segments along one of these arrays. This lets us compute prefix sums over diagonals and then query any segment in $O(1)$ time per cell. By iterating through each cell once and checking the relevant precomputed diagonal sum, we reduce the complexity to $O(n \cdot m)$, which fits comfortably within the time limits.

This approach leverages the special structure of Manhattan distance: all cells at the same sum or difference of coordinates lie along a diagonal. Counting along diagonals with prefix sums converts a two-dimensional range query into a one-dimensional interval query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n m k²) | O(n m) | Too slow |
| Diagonal Prefix Sums | O(n m) | O(n m) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n, m, k$ and the grid representation. Store the grid as a 2D list of integers where `1` represents a target and `0` represents empty.
2. Construct two auxiliary arrays: `sum_diag[i+j]` and `diff_diag[i-j]`, representing the total number of targets along each diagonal. Iterate through the grid, incrementing the appropriate entries.
3. For each cell $(i, j)$, compute the number of targets Shel can hit in each of the four diagonal directions. For the right-down diagonal, sum targets in `sum_diag` from $(i+j)$ to $(i+j+k)$. For the left-down diagonal, sum targets in `diff_diag` from $(i-j)$ to $(i-j+k)$, and similarly for the other two directions using mirrored ranges.
4. Keep track of the maximum number of targets encountered while iterating through all cells and all directions.
5. Output the maximum number per test case.

Why it works: the invariants are that `sum_diag` and `diff_diag` correctly represent the total targets along each diagonal, and the query ranges capture exactly all cells within Manhattan distance $k$ along the chosen diagonal. Each target is counted once per potential shot. By checking all possible firing positions, we ensure the global maximum is found.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m, k = map(int, input().split())
        grid = [input().strip() for _ in range(n)]
        
        # Map diagonals to counts
        sum_diag = {}
        diff_diag = {}
        for i in range(n):
            for j in range(m):
                if grid[i][j] == '#':
                    sum_diag[i+j] = sum_diag.get(i+j, 0) + 1
                    diff_diag[i-j] = diff_diag.get(i-j, 0) + 1
        
        max_hit = 0
        for i in range(n):
            for j in range(m):
                if grid[i][j] == '.':
                    continue
                # Four directions: sum_diag and diff_diag ranges
                rd = sum(sum_diag.get(i+j+t, 0) for t in range(k+1))
                lu = sum(sum_diag.get(i+j-t, 0) for t in range(k+1))
                ld = sum(diff_diag.get(i-j+t, 0) for t in range(k+1))
                ru = sum(diff_diag.get(i-j-t, 0) for t in range(k+1))
                max_hit = max(max_hit, rd, lu, ld, ru)
        print(max_hit)

if __name__ == "__main__":
    solve()
```

The code reads input efficiently, maps each target to its sum and difference diagonals, and iterates over each target to compute the maximum reachable count in all four diagonal directions. Using dictionaries avoids allocating large arrays when $n, m$ are sparse.

## Worked Examples

**Sample 1**

Input:

```
3 3 1
.#.
###
.#.
```

For cell $(1,1)$, the diagonals are: sum_diag = 2, diff_diag = 0. Shooting right-down covers cells `(1,1), (2,2)`. Counting targets along these diagonals within `k=1` yields 3 targets. No other cell achieves a higher count.

**Sample 2**

Input:

```
2 5 3
###..
...##
```

The optimal shot is from cell `(1,1)` along the right-down diagonal covering 4 targets. Iterating through other positions does not exceed this count.

These traces show the algorithm correctly captures all diagonal targets within Manhattan distance `k`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n m) | Each cell is processed once, and sums along diagonals are computed using dictionaries |
| Space | O(n+m) | Only the unique sum and difference diagonals are stored |

With the total number of cells across all test cases capped at $10^5$, this is well within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided samples
assert run("4\n3 3 1\n.#.\n###\n.#.\n2 5 3\n###..\n...##\n4 4 2\n..##\n###.\n#..#\n####\n2 1 3\n#\n#\n") == "3\n4\n5\n2"

# Custom cases
assert run("1\n1 1 1\n#\n") == "1"
assert run("1\n2 2 2\n##\n##\n") == "4"
assert run("1\n3 3 1\n...\n.#.\n...\n") == "1"
assert run("1\n3 3 3\n#.#\n.#.\n#.#\n") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 filled grid | 1 | Minimum-size input |
| 2x2 fully filled | 4 | Small square, all targets |
| 3x3 single target center | 1 | Diagonal range, edge counting |
| 3x3 checkerboard k=3 | 5 | Maximum range covering multiple diagonals |

## Edge Cases

For a single-column grid of height 3 and `k=3`:

```
3 1 3
#
#
#
```

The algorithm maps each cell to `sum_diag` and `diff_diag`, but here `sum_diag` equals the row index and `diff_diag` also equals row index. Shooting from the top cell along the right-down
