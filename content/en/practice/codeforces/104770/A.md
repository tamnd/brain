---
title: "CF 104770A - Square Illumination"
description: "We are given a rectangular plaza with dimensions $n times m$. Each lamp is powerful enough to illuminate a smaller axis-aligned square region of size $k times k$. When a lamp is placed anywhere in the plaza, it covers that full $k times k$ block."
date: "2026-06-28T19:51:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104770
codeforces_index: "A"
codeforces_contest_name: "The XXXI Saint-Petersburg High School Programming Contest (SpbKOSHP 2023) | Qualification for the XXIV Russia Open High School Programming Contest (VKOSHP 2023)"
rating: 0
weight: 104770
solve_time_s: 63
verified: true
draft: false
---

[CF 104770A - Square Illumination](https://codeforces.com/problemset/problem/104770/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular plaza with dimensions $n \times m$. Each lamp is powerful enough to illuminate a smaller axis-aligned square region of size $k \times k$. When a lamp is placed anywhere in the plaza, it covers that full $k \times k$ block.

The goal is to cover the entire $n \times m$ rectangle using as few such $k \times k$ lamps as possible. Lamps can overlap and can extend beyond the border of the plaza, but coverage outside the rectangle does not help.

The task reduces to deciding how many $k \times k$ squares are needed to fully tile or cover an $n \times m$ grid.

The constraints allow $n, m, k$ up to $10^9$. This immediately rules out any approach that iterates over rows or columns one unit at a time. Any valid solution must be constant time arithmetic.

A naive misunderstanding comes from thinking about “fitting” squares without considering partial coverage at the borders. For example, if $n = 4, k = 3$, a single lamp placed at the top-left does not fully cover the bottom row, even though $4 < 2 \cdot 3$ might tempt a greedy assumption.

Another subtle case is when dimensions are multiples of $k$. If $n = 6, k = 2$, then coverage is clean. But if $n = 7, k = 2$, the last strip still needs a full extra lamp even though only one row remains uncovered.

These boundary effects are exactly what makes the ceiling behavior essential.

## Approaches

A brute-force approach would simulate placing lamps row by row and column by column. One could imagine scanning the grid and placing a lamp whenever a cell is uncovered, marking its entire $k \times k$ region as covered.

This works conceptually, but the cost is enormous. In the worst case, each lamp covers about $k^2$ cells, so the number of placements is roughly $(n \cdot m) / k^2$. With $n, m \le 10^9$, the grid size is up to $10^{18}$, making simulation impossible.

The key observation is that coverage is perfectly periodic in both dimensions. Each lamp covers a $k$-by-$k$ block, so along one axis we only care how many full blocks of size $k$ fit, and whether a remainder exists. Each axis becomes an independent rounding-up problem.

Along the length $n$, we need $\lceil n / k \rceil$ segments. Along width $m$, we need $\lceil m / k \rceil$ segments. Every pair of such segments corresponds to one lamp placement in a grid of blocks, so the total is their product.

This reduces a 2D geometric covering problem into two independent 1D ceiling divisions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nm)$ | $O(1)$ | Too slow |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute how many full $k$-length segments are needed to cover $n$. This is done using ceiling division, which counts an extra segment if $n$ is not divisible by $k$. This ensures no uncovered strip remains at the bottom edge.
2. Compute how many full $k$-length segments are needed to cover $m$ using the same ceiling logic. This ensures no uncovered strip remains on the right edge.
3. Multiply the two results. Each horizontal segment must be paired with each vertical segment, forming a grid of lamp placements that fully covers the rectangle.

### Why it works

Each lamp covers exactly a $k \times k$ axis-aligned block. Any valid placement strategy partitions the plane into regions where each region can be fully covered by one lamp only if it lies inside a single $k \times k$ block of a covering grid.

Ceiling division along each axis produces the minimal number of such blocks needed to span that axis completely. Since coverage is rectangular and independent across axes, the Cartesian product of these partitions yields the minimal number of lamps. No arrangement can reduce the count because reducing either axis count would leave a segment longer than $k$ uncovered.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    
    # ceiling division without floats
    need_n = (n + k - 1) // k
    need_m = (m + k - 1) // k
    
    print(need_n * need_m)

if __name__ == "__main__":
    solve()
```

The solution reads the three integers and computes ceiling division using the standard integer trick $(x + k - 1) // k$. This avoids floating-point errors and works safely up to $10^9$.

The multiplication step is safe within Python’s integer range, and no additional overflow handling is required.

## Worked Examples

### Example 1

Input: $n = 10, m = 9, k = 3$

| Step | n value | m value | Computation |
| --- | --- | --- | --- |
| 1 | 10 | 9 | need_n = ceil(10/3) = 4 |
| 2 | 10 | 9 | need_m = ceil(9/3) = 3 |
| 3 | - | - | result = 4 × 3 = 12 |

This shows that even though 10 and 9 are not multiples of 3, each axis independently requires an extra partial block. The grid of block positions is 4 by 3.

### Example 2

Input: $n = 4, m = 6, k = 2$

| Step | n value | m value | Computation |
| --- | --- | --- | --- |
| 1 | 4 | 6 | need_n = ceil(4/2) = 2 |
| 2 | 4 | 6 | need_m = ceil(6/2) = 3 |
| 3 | - | - | result = 2 × 3 = 6 |

Here both dimensions divide evenly, so no extra partial coverage is needed. The lamps form a perfect 2 by 3 tiling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a constant number of arithmetic operations are performed |
| Space | $O(1)$ | No additional data structures are used |

The solution is constant time and easily satisfies the constraints up to $10^9$, since it performs only two integer divisions and one multiplication.

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

# provided samples
assert run("10 9 3\n") == "12"
assert run("4 6 2\n") == "6"

# minimum case
assert run("1 1 1\n") == "1"

# exact multiples
assert run("6 8 2\n") == "12"

# non-multiples both directions
assert run("7 7 3\n") == "9"

# large values
assert run("1000000000 1000000000 1\n") == "1000000000000000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | 1 | smallest valid case |
| 6 8 2 | 12 | clean tiling without remainder |
| 7 7 3 | 9 | both dimensions require ceiling |
| 10^9 10^9 1 | 10^18 | stress test for large multiplication |

## Edge Cases

A key edge case is when one dimension is smaller than $k$. For example, $n = 2, m = 10, k = 3$.

Here, $need_n = \lceil 2/3 \rceil = 1$ and $need_m = \lceil 10/3 \rceil = 4$, giving a total of 4 lamps.

Even though the height is smaller than the lamp size, at least one row of lamps is still required because coverage does not allow fractional placement.

Another edge case is when both dimensions are exact multiples, such as $n = 6, m = 6, k = 3$. Then $need_n = 2$, $need_m = 2$, and the answer is 4. Any attempt to “merge” coverage across boundaries fails because each lamp is fixed to a $k \times k$ square; no overlap optimization can reduce the grid count.

Finally, when $k = 1$, every cell requires its own lamp. The formula produces $n \cdot m$, matching the intuition that each unit square must be individually illuminated.
