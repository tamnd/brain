---
title: "CF 104598H - Model Evaluation"
description: "The task gives two square grids of numbers, both of size $N times N$, representing pixel intensities of two images. For each query, we are given a rectangular subregion inside these grids, specified by two opposite corners."
date: "2026-06-30T03:07:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104598
codeforces_index: "H"
codeforces_contest_name: "GPL 2023 Advanced"
rating: 0
weight: 104598
solve_time_s: 86
verified: true
draft: false
---

[CF 104598H - Model Evaluation](https://codeforces.com/problemset/problem/104598/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

The task gives two square grids of numbers, both of size $N \times N$, representing pixel intensities of two images. For each query, we are given a rectangular subregion inside these grids, specified by two opposite corners. For that rectangle, we compute the sum of values in image $A$ and the sum of values in image $B$, then output the absolute difference between those two sums.

Each query is independent, so we are repeatedly asked to evaluate a rectangular sum in two matrices and compare them.

The constraints make the naive idea infeasible. With $N \le 800$, the grid has up to $6.4 \times 10^5$ cells, and there can be up to $7 \times 10^4$ queries. If each query recomputes a rectangle sum by scanning all cells in the region, the worst case rectangle is the whole grid, leading to about $800^2 \cdot 70000$ operations, which is far beyond time limits.

A common edge case involves large rectangles where $r_1 > r_2$ or $c_1 > c_2$. The problem statement allows coordinates in any order, so a naive implementation that assumes ordered corners will silently compute incorrect subregions unless it normalizes coordinates first.

Another pitfall is overflow. Each cell can be up to $10^9$, so a full $800 \times 800$ sum reaches $6.4 \times 10^{14}$, which does not fit in 32-bit integers and requires 64-bit arithmetic.

## Approaches

A brute-force solution processes each query by iterating over every cell inside the rectangle and summing values in both grids. This is straightforward and correct, but its cost per query depends on the rectangle area. In the worst case, each query touches $O(N^2)$ cells, leading to $O(N^2 Q)$, which is too slow for large $Q$.

The key observation is that rectangle sums can be precomputed using a prefix-sum table. Instead of recomputing sums for every query, we preprocess each grid into a 2D prefix sum array so that any subrectangle sum can be obtained in constant time using inclusion-exclusion. Since we need sums for both images, we build two prefix sum arrays and answer each query by subtracting them and taking absolute value.

This reduces each query from scanning $O(N^2)$ cells to $O(1)$, which changes the problem from infeasible to efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N^2 Q)$ | $O(1)$ | Too slow |
| Prefix Sums | $O(N^2 + Q)$ | $O(N^2)$ | Accepted |

## Algorithm Walkthrough

We build a standard 2D prefix sum for each image.

1. Read both grids $A$ and $B$. These are treated as matrices indexed from 1 to $N$. This simplifies boundary handling in prefix sums.
2. Construct prefix sums $SA$ and $SB$, where each entry stores the sum of the submatrix from $(1,1)$ to $(i,j)$. Each value is computed using previously computed prefixes, ensuring each cell is processed once.
3. For each query, normalize coordinates so that $r_1 \le r_2$ and $c_1 \le c_2$. This avoids incorrect ranges when input corners are given in reverse order.
4. Compute the sum of the rectangle in $A$ using inclusion-exclusion:

$$SA(r_2,c_2) - SA(r_1-1,c_2) - SA(r_2,c_1-1) + SA(r_1-1,c_1-1)$$

The same computation is applied to $SB$.
5. Output the absolute difference between the two results.

Each query now uses only constant-time arithmetic.

### Why it works

A 2D prefix sum encodes cumulative area sums so that any rectangle can be decomposed into four prefix regions. Inclusion-exclusion cancels overlapping areas exactly once. Because every cell contributes to exactly one combination of prefix terms, the computed value matches the true rectangle sum. The subtraction between two independently correct rectangle sums preserves correctness of the final absolute difference.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_prefix(grid, n):
    ps = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        row_sum = 0
        for j in range(1, n + 1):
            row_sum += grid[i-1][j-1]
            ps[i][j] = ps[i-1][j] + row_sum
    return ps

def rect_sum(ps, r1, c1, r2, c2):
    return (
        ps[r2][c2]
        - ps[r1-1][c2]
        - ps[r2][c1-1]
        + ps[r1-1][c1-1]
    )

def solve():
    n, q = map(int, input().split())

    A = [list(map(int, input().split())) for _ in range(n)]
    B = [list(map(int, input().split())) for _ in range(n)]

    psa = build_prefix(A, n)
    psb = build_prefix(B, n)

    out = []
    for _ in range(q):
        r1, c1, r2, c2 = map(int, input().split())
        if r1 > r2:
            r1, r2 = r2, r1
        if c1 > c2:
            c1, c2 = c2, c1

        sa = rect_sum(psa, r1, c1, r2, c2)
        sb = rect_sum(psb, r1, c1, r2, c2)
        out.append(str(abs(sa - sb)))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

After reading the input, both matrices are stored explicitly so that indexing matches the prefix construction. The prefix arrays are 1-indexed to avoid repeated boundary checks inside queries.

The rectangle sum function applies the standard inclusion-exclusion identity. The normalization step for query coordinates is essential because the input does not guarantee ordering of corners.

## Worked Examples

Consider the first sample.

We build prefix sums for both matrices, then process query $(1,1,1,3)$. After normalization it remains unchanged. The rectangle sum is computed in constant time from the prefix arrays, producing 11 for $A$ and 9 for $B$, so the output is 2.

For the second query $(3,3,1,2)$, normalization produces $(1,2,3,3)$. The prefix sums give equal totals for both matrices, so the difference is 0.

These examples confirm that both ordered and reversed coordinate inputs are handled correctly, and that prefix sums return consistent rectangle aggregates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N^2 + Q)$ | prefix construction plus constant-time queries |
| Space | $O(N^2)$ | storage of two prefix tables |

The bounds allow up to 800×800 preprocessing, which is well within limits. Each of the up to 70000 queries is answered in constant time, ensuring the solution fits comfortably in time constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, q = map(int, input().split())
    A = [list(map(int, input().split())) for _ in range(n)]
    B = [list(map(int, input().split())) for _ in range(n)]

    def build(ps):
        n = len(ps)
        for i in range(n):
            for j in range(n):
                ps[i][j] += (ps[i-1][j] if i else 0) + (ps[i][j-1] if j else 0) - (ps[i-1][j-1] if i and j else 0)
        return ps

    psa = build(A)
    psb = build(B)

    def get(ps, r1, c1, r2, c2):
        res = ps[r2][c2]
        if r1: res -= ps[r1-1][c2]
        if c1: res -= ps[r2][c1-1]
        if r1 and c1: res += ps[r1-1][c1-1]
        return res

    out = []
    for _ in range(q):
        r1, c1, r2, c2 = map(int, input().split())
        r1, r2 = sorted([r1-1, r2-1])
        c1, c2 = sorted([c1-1, c2-1])
        out.append(str(abs(get(psa, r1, c1, r2, c2) - get(psb, r1, c1, r2, c2))))

    return "\n".join(out)

# provided sample
assert run("""3 2
3 1 7
2 5 2
5 8 4
5 2 2
1 3 7
4 9 4
1 1 1 3
3 3 1 2
""") == "2\n0"

# custom cases
assert run("""1 1
5
3
1 1 1 1
""") == "2", "single cell"

assert run("""2 1
1 2
3 4
4 3
2 1
1 1 2 2
""") == "0", "equal sums"

assert run("""2 1
1 1
1 1
2 2
2 2
1 1 2 2
""") == "0", "all equal"

assert run("""3 1
1 2 3
4 5 6
7 8 9
9 8 7
6 5 4
3 2 1
1 1 3 3
""") == "0", "full symmetry"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 grids | 2 | single-cell subtraction correctness |
| 2x2 swapped values | 0 | cancellation across full grid |
| identical matrices | 0 | baseline correctness |
| reversed structured grid | 0 | consistent rectangle aggregation |

## Edge Cases

A single-cell query such as $(i,j,i,j)$ tests whether prefix subtraction degenerates correctly. In that case, all outer prefix terms cancel and only the single cell remains, so both sums reduce to that entry and the difference is computed correctly.

A reversed coordinate query such as $(r_2,c_2,r_1,c_1)$ tests whether normalization is applied. Without sorting, prefix subtraction would access invalid regions and produce incorrect results, but after swapping coordinates the rectangle becomes valid and inclusion-exclusion applies cleanly.

A full-grid query tests whether large prefix sums exceed 32-bit bounds. Using Python integers avoids overflow and preserves correctness even when sums reach $10^{14}$ scale.
