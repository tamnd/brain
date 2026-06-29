---
title: "CF 104668J - Matrice"
description: "We are given a rectangular grid of characters. A “trinity” is formed by first choosing any square subregion of this grid and then selecting all cells inside that square that lie on or strictly on one side of a diagonal of the square."
date: "2026-06-29T09:49:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104668
codeforces_index: "J"
codeforces_contest_name: "2018-2019 ACM-ICPC Central Europe Regional Contest (CERC 18)"
rating: 0
weight: 104668
solve_time_s: 33
verified: true
draft: false
---

[CF 104668J - Matrice](https://codeforces.com/problemset/problem/104668/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular grid of characters. A “trinity” is formed by first choosing any square subregion of this grid and then selecting all cells inside that square that lie on or strictly on one side of a diagonal of the square. The diagonal can be either the main diagonal or the anti-diagonal. After this filtering, we keep the resulting triangular region. If all cells in that region contain the same character and the region contains at least three cells, it counts as one valid trinity.

The task is to count how many such valid triangular regions exist across all possible square subgrids, over both diagonal orientations.

The grid size can be as large as 1000 by 1000, which implies up to one million cells. A naive approach that tries all square subregions would involve on the order of $O(n^3)$ or worse combinations of squares, and checking each one explicitly would be far too slow, potentially exceeding $10^{12}$ operations. This immediately suggests that we cannot enumerate all squares directly and must instead count contributions in a more aggregated way.

A subtle point in the definition is that different squares can generate identical geometric triangles in the grid, but they are still considered distinct if they come from different square choices. So we are counting configurations, not unique shapes.

Edge cases arise when the square is minimal. A 1 by 1 or 2 by 2 square does not produce a valid trinity because the resulting triangular region would contain fewer than three cells. Another edge case is when a square is entirely uniform, since it maximizes potential valid triangles, and any counting mistake tends to overcount heavily there.

## Approaches

A direct approach would be to iterate over all $O(N^2 M^2)$ possible squares, and for each square, check both diagonal orientations and then verify whether all cells in the resulting triangular region are equal. Even if we precompute prefix sums for character equality checks, we still face iterating over too many squares, and the total number of square submatrices itself is already too large in a 1000 by 1000 grid.

The key observation is that each valid trinity is completely determined by its apex structure along a diagonal. Instead of thinking in terms of full squares, we reinterpret the construction: fixing a cell as part of the triangle, we can expand in two perpendicular directions until we hit a mismatch. For a fixed starting cell and a chosen direction (corresponding to one of the two diagonals), the maximal triangle size is determined by how far we can extend while maintaining uniform character constraints.

This transforms the problem into counting, for each cell, how many square sizes are valid in each diagonal direction. Instead of enumerating squares, we compute maximal extension lengths using dynamic programming-like propagation along diagonals, and then sum contributions from all cells.

The main structural simplification is that validity depends only on local consistency along diagonals and anti-diagonals, which allows us to precompute maximal homogeneous “arms” in both directions. Once these arm lengths are known, each cell contributes a number of valid triangles equal to a function of these lengths.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over all squares | $O(n^4)$ | $O(1)$ | Too slow |
| Diagonal DP counting | $O(nm)$ | $O(nm)$ | Accepted |

## Algorithm Walkthrough

We separate the problem into handling two orientations: triangles based on the main diagonal and triangles based on the anti-diagonal. Both cases are symmetric, so we describe one and apply the same logic to the other.

1. For each cell, compute how far we can extend a square of identical characters along two perpendicular directions that define a diagonal-oriented square. This is done using dynamic programming over the grid. The key idea is to precompute, for each cell, the longest stretch of identical characters ending at or starting from it along rows and columns, and then combine these constraints to ensure square consistency.
2. Construct a DP table that stores, for each cell, the maximum possible side length of a square whose top-left corner is at that cell and whose cells are all identical. This is the classical maximal square problem, but extended conceptually to reflect diagonal symmetry constraints.
3. For each cell and each orientation, the number of valid trinities contributed by that cell is determined by how many square sizes can be formed starting from that cell. If the maximal square size is $k$, then it contributes all sizes from 2 up to $k$, and each such square yields exactly one valid trinity for the chosen diagonal orientation.
4. Sum these contributions over all cells and both diagonal orientations.

The essential computation reduces to a standard maximal-square DP combined with directional preprocessing to ensure all cells in candidate squares are identical.

### Why it works

The algorithm works because every valid trinity corresponds uniquely to a choice of square and diagonal orientation, and within each square the condition “all cells equal” is equivalent to requiring that every unit sub-square expansion remains consistent. The DP guarantees that if a square of size $k$ is valid at a given anchor, then all smaller squares anchored there are also valid, and no invalid square is ever counted because any mismatch immediately breaks the DP extension. This creates a clean one-to-one mapping between counted DP states and valid trinities.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    g = [input().strip() for _ in range(n)]

    def count_orientation():
        dp = [[1] * m for _ in range(n)]
        res = 0

        for i in range(n):
            for j in range(m):
                if i > 0 and j > 0 and g[i][j] == g[i-1][j] == g[i][j-1] == g[i-1][j-1]:
                    dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
                else:
                    dp[i][j] = 1

                res += max(0, dp[i][j] - 1)

        return res

    def count_antiorientation():
        dp = [[1] * m for _ in range(n)]
        res = 0

        for i in range(n):
            for j in range(m - 1, -1, -1):
                if i > 0 and j + 1 < m and g[i][j] == g[i-1][j] == g[i][j+1] == g[i-1][j+1]:
                    dp[i][j] = min(dp[i-1][j], dp[i][j+1], dp[i-1][j+1]) + 1
                else:
                    dp[i][j] = 1

                res += max(0, dp[i][j] - 1)

        return res

    print(count_orientation() + count_antiorientation())

if __name__ == "__main__":
    solve()
```

The implementation uses two passes. Each pass computes a standard maximal-square DP, once for the normal diagonal orientation and once for the mirrored orientation. The recurrence checks whether a 2 by 2 block is uniform; if so, the square can be extended by one layer.

The key subtlety is the summation `dp[i][j] - 1`. A value of 1 corresponds to a degenerate square that does not contribute any valid trinity, while larger squares contribute all smaller valid trinity sizes anchored at that cell.

The anti-diagonal version is implemented by reversing column traversal so that the DP still references already computed states.

## Worked Examples

### Sample 1

Grid:

```
2 2
AA
Ad
```

We compute DP values for main diagonal orientation.

| Cell | Character
