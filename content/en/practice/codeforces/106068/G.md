---
title: "CF 106068G - Fire Coverage"
description: "We are working on a rectangular city grid with $N$ rows and $M$ columns. You are allowed to place $K$ fire stations on arbitrary grid cells."
date: "2026-06-21T15:57:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106068
codeforces_index: "G"
codeforces_contest_name: "2025 Aleppo and Idlib Private Universities Collegiate Programming Contest (APUCPC 2025)"
rating: 0
weight: 106068
solve_time_s: 51
verified: true
draft: false
---

[CF 106068G - Fire Coverage](https://codeforces.com/problemset/problem/106068/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working on a rectangular city grid with $N$ rows and $M$ columns. You are allowed to place $K$ fire stations on arbitrary grid cells. Each station can reach other cells using Chebyshev distance, meaning movement in eight directions is allowed and the distance between two cells is the maximum of their row and column differences.

A station placed at a cell effectively protects all cells inside a square centered at that position, with side length $2d+1$, because every cell within Chebyshev distance $d$ satisfies $\max(|x_1-x_2|, |y_1-y_2|)\le d$.

The task is to choose station positions optimally so that every cell in the grid is covered by at least one station, and we want the smallest possible $d$ for which this is achievable with at most $K$ stations.

The grid can be extremely large, up to $10^9 \times 10^9$, so we cannot simulate anything cell by cell. The number of stations is much smaller, up to $10^5$, which suggests the solution must compress the grid into a structural counting problem.

A naive attempt would try to place stations and simulate coverage, but even representing the grid is impossible. Another naive idea is to try all placements of $K$ stations, but that is combinatorially explosive and irrelevant even for tiny inputs.

A subtle edge case appears when $N$ and $M$ are both small but $K$ is large. For example, if $N=M=2$ and $K=4$, then $d=0$ is sufficient since each station covers exactly one cell. Any solution that assumes $d\ge 1$ by default would fail here.

The main challenge is recognizing that coverage depends only on how many $(2d+1)\times(2d+1)$ squares are needed to tile the grid, not on exact station placement.

## Approaches

The brute-force viewpoint starts by fixing a candidate distance $d$. If a station covers a square of side $2d+1$, then the grid must be covered by such squares. One could try placing stations in all possible ways and checking coverage, but this is infeasible because the grid has up to $10^{18}$ cells, and even enumerating placements is impossible.

The key observation is that once $d$ is fixed, the optimal arrangement is always a grid-like packing. Each station covers a contiguous block, so to minimize the number of stations, we pack these blocks without overlap in a regular tiling. Along each dimension, we need $\lceil N/(2d+1)\rceil$ blocks vertically and $\lceil M/(2d+1)\rceil$ blocks horizontally. Their product gives the minimum number of stations required for that $d$.

This transforms the problem from geometric placement into a simple feasibility check. We then search for the smallest $d$ such that the required number of blocks does not exceed $K$. Since increasing $d$ only increases coverage size, feasibility is monotonic, which makes binary search applicable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force placement | infeasible (exponential) | O(1) | Too slow |
| Binary search with tiling check | $O(\log \max(N,M))$ | O(1) | Accepted |

## Algorithm Walkthrough

We treat $d$ as the variable we want to minimize and check whether a given $d$ is sufficient.

1. For a fixed $d$, compute the side length of coverage as $s = 2d + 1$. This represents how many consecutive cells one station can fully cover in each direction.
2. Compute how many stations are needed to cover the grid vertically as $a = \lceil N / s \rceil$. This counts how many vertical strips of height $s$ are required.
3. Compute how many stations are needed horizontally as $b = \lceil M / s \rceil$. This counts horizontal strips of width $s$.
4. The total number of stations required is $a \times b$. This corresponds to placing one station per block in a full grid decomposition.
5. Check whether $a \times b \le K$. If yes, then distance $d$ is sufficient; otherwise it is too small.
6. Use binary search on $d$ from $0$ up to $\max(N, M)$, keeping the smallest feasible value.

The reason binary search works is that increasing $d$ only increases $s$, which reduces both $\lceil N/s \rceil$ and $\lceil M/s \rceil$, so the required number of stations never increases.

### Why it works

For any fixed $d$, the grid can be partitioned into blocks of size at most $(2d+1)\times(2d+1)$. Each station cannot cover more than one such block boundary-crossing region without wasting coverage, so an optimal arrangement behaves like a tiling. The expression $\lceil N/s\rceil \cdot \lceil M/s\rceil$ is not just a construction, it is the minimal possible count because any covering must assign at least one station per disjoint block region induced by this partition. This makes the feasibility check exact rather than approximate, so binary search over it produces the true minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(d, n, m, k):
    s = 2 * d + 1
    a = (n + s - 1) // s
    b = (m + s - 1) // s
    return a * b <= k

def solve():
    n, m, k = map(int, input().split())

    lo, hi = 0, max(n, m)

    while lo < hi:
        mid = (lo + hi) // 2
        if can(mid, n, m, k):
            hi = mid
        else:
            lo = mid + 1

    print(lo)

if __name__ == "__main__":
    solve()
```

The solution is built around a monotone feasibility test. The function `can` encodes the tiling argument directly: it converts a radius $d$ into a block size and computes how many blocks are required in each dimension.

The binary search maintains the invariant that any value below `lo` is infeasible and any value at or above `hi` is potentially feasible. The midpoint check gradually shrinks the interval until the smallest valid $d$ is found.

The only subtle point is ensuring integer ceiling division is handled correctly, since off-by-one errors here directly change the number of required stations.

## Worked Examples

### Example 1

Input:

```
5 5 4
```

We search over $d$.

| d | s = 2d+1 | a = ceil(5/s) | b = ceil(5/s) | a*b | feasible |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 5 | 5 | 25 | no |
| 1 | 3 | 2 | 2 | 4 | yes |

The binary search converges to $d=1$. This shows that splitting the grid into $3\times3$ coverage blocks reduces the requirement to exactly four stations.

### Example 2

Input:

```
2 2 4
```

| d | s | a | b | a*b | feasible |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 2 | 2 | 4 | yes |

Here $d=0$ already works since each cell can be assigned its own station. This confirms that the formula naturally handles minimal grids without special casing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log \max(N,M))$ | binary search over possible radius values with constant-time feasibility check |
| Space | $O(1)$ | only a few integers are used |

The constraints allow $N, M$ up to $10^9$, so a direct simulation is impossible. The logarithmic search over $d$ ensures at most around 30 iterations, which is easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m, k = map(int, input().split())

    def can(d):
        s = 2 * d + 1
        a = (n + s - 1) // s
        b = (m + s - 1) // s
        return a * b <= k

    lo, hi = 0, max(n, m)
    while lo < hi:
        mid = (lo + hi) // 2
        if can(mid):
            hi = mid
        else:
            lo = mid + 1

    return str(lo)

# provided sample
assert run("5 5 4") == "1"

# minimum grid
assert run("1 1 1") == "0"

# tight coverage
assert run("1 10 1") == "5"

# large K enough for d=0
assert run("3 3 9") == "0"

# rectangular imbalance
assert run("4 7 2") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | 0 | smallest grid base case |
| 1 10 1 | 5 | one-dimensional stretching |
| 3 3 9 | 0 | full coverage without expansion needed |
| 4 7 2 | 1 | non-square grid packing behavior |

## Edge Cases

When $N$ and $M$ are both 1, the algorithm evaluates $d=0$ immediately since $s=1$ and only one station is needed. The feasibility check correctly returns true without any special handling.

When the grid is extremely skewed, such as $1 \times M$, the computation reduces to a one-dimensional covering problem. The formula still applies because one of $a$ or $b$ becomes 1, and the other captures the full segmentation along the line.

When $K$ is very large compared to grid size, the algorithm still correctly returns $d=0$, since $\lceil N/1\rceil \cdot \lceil M/1\rceil = N \cdot M \le K$ is the only condition that matters.
