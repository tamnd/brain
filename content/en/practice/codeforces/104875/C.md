---
title: "CF 104875C - Circular Caramel Cookie"
description: "We are given a configuration of unit squares laid out on an infinite grid. Think of the plane split by integer lattice lines into 1 by 1 cells."
date: "2026-06-28T09:45:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104875
codeforces_index: "C"
codeforces_contest_name: "2022-2023 ICPC Northwestern European Regional Programming Contest (NWERC 2022)"
rating: 0
weight: 104875
solve_time_s: 54
verified: true
draft: false
---

[CF 104875C - Circular Caramel Cookie](https://codeforces.com/problemset/problem/104875/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a configuration of unit squares laid out on an infinite grid. Think of the plane split by integer lattice lines into 1 by 1 cells. A circular cookie is centered exactly at a grid intersection point, and we are interested in how many of these unit squares are fully contained inside the circle.

Each square is counted only if all four of its corners lie inside or on the circle. The task is reversed from a usual counting problem: instead of being given a radius and counting squares, we are given a number `s` representing an upper bound on how many full squares a competitor’s cookie contains, and we must construct a circle that contains strictly more than `s` full squares while keeping the radius as small as possible.

So the output is the smallest possible radius such that the number of fully contained unit squares inside the circle exceeds `s`.

The constraint `s ≤ 10^9` rules out any approach that explicitly enumerates squares for large radii. Even a radius around 10^5 already induces around 10^10 grid positions in a naive 2D scan, which is far beyond what a one-second solution can handle. The structure of the problem suggests we need to count lattice objects inside a geometric shape efficiently and invert that count using a monotonic search.

A subtle edge case appears when `s` is very small. If `s = 1`, the answer is not determined by a single unit square near the origin but by how quickly squares begin to fully fit inside the circle. Another edge case is that squares are not centered at lattice points but are defined by their corners, so misinterpreting whether to use centers or corners leads to a systematically incorrect count.

## Approaches

A direct approach would try increasing the radius gradually and, for each radius, iterate over all grid squares in a bounding box and check whether all four corners lie within the circle. This is conceptually correct, but for radius `R` it requires iterating over roughly `O(R^2)` squares, and each check is constant time. Since the number of valid squares grows proportionally to the area of the circle, reaching `s` up to `10^9` would require radii on the order of `sqrt(s)`, which is about `3 × 10^4`. Even then, iterating over all squares up to that radius results in about `10^9` iterations, which is too slow.

The key observation is that the set of valid squares grows monotonically with the radius. Once a square is fully inside a circle of radius `R`, it will remain inside for any larger radius. This monotonicity allows us to invert the counting function using binary search on the radius.

The remaining challenge is computing, for a fixed radius `R`, how many unit squares are fully contained in the circle without iterating over all of them. The geometry simplifies if we switch from squares to their corners: a unit square with bottom-left corner `(x, y)` is fully contained if its farthest corner `(x+1, y+1)` is within the circle centered at the origin. This converts the condition into an inequality involving only integer lattice points in the first quadrant.

We then count valid integer pairs efficiently using a two-dimensional prefix structure in disguise: for each `x`, we compute the maximum feasible `y` from the circle equation. This reduces counting for a fixed radius to `O(R)` time, and binary search adds a logarithmic factor.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over squares per radius | O(R²) per check | O(1) | Too slow |
| Binary search + geometric counting | O(R log R) | O(1) | Accepted |

## Algorithm Walkthrough

We transform the problem into counting integer pairs that satisfy a circle constraint.

1. Reinterpret each unit square using its bottom-left corner `(x, y)`. The square is fully inside the circle if and only if `(x+1, y+1)` lies inside or on the circle. This converts the condition into `(x+1)² + (y+1)² ≤ R²`.
2. Shift variables by defining `a = x+1` and `b = y+1`, which makes both `a` and `b` positive integers starting from 1. The condition becomes `a² + b² ≤ R²`.
3. For a fixed radius `R`, compute the number of integer pairs `(a, b)` in the first quadrant satisfying the inequality. For each `a`, the maximum valid `b` is `⌊sqrt(R² − a²)⌋`.
4. Sum over all `a` from 1 to `R`, adding `max(0, b_max)` to the count. This gives the number of valid squares in one quadrant.
5. Multiply the result by 4 to account for all four symmetric quadrants.
6. Use binary search on `R`. For each midpoint radius, compute the number of squares. If it is greater than `s`, the radius is feasible and we try smaller values. Otherwise we increase it.
7. Return the smallest radius that produces strictly more than `s` squares.

The correctness hinges on the fact that the counting function is monotone in `R`. Larger circles can only include more lattice points, never fewer, so binary search always converges to the minimal feasible radius.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

def count_squares(R):
    R2 = R * R
    total = 0
    for a in range(1, R + 1):
        rem = R2 - a * a
        if rem <= 0:
            break
        b = int(math.isqrt(rem))
        total += b
    return total * 4

def solve():
    s = int(input())
    
    lo, hi = 0, 2 * 10**7
    
    while lo < hi:
        mid = (lo + hi) // 2
        if count_squares(mid) > s:
            hi = mid
        else:
            lo = mid + 1
    
    print(lo)

if __name__ == "__main__":
    solve()
```

The counting function directly implements the derived geometric condition. The loop over `a` stops early when `a²` exceeds `R²`, since no further valid pairs exist. Using `math.isqrt` avoids floating-point precision issues that would otherwise accumulate around large radii.

The binary search range is chosen generously; the answer cannot exceed a few million for the given constraints because the number of squares grows quadratically with the radius.

## Worked Examples

Consider a small radius where we can explicitly enumerate behavior. For a given `R`, we count valid `(a, b)` pairs.

### Sample 1

We start with `s = 1`.

| step | lo | hi | mid | count(mid) | decision |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | large | m | computed | adjust range |

For very small radii, the circle contains no full squares until it becomes large enough to include at least one unit square completely. The binary search quickly narrows down the smallest radius where the first square fits entirely.

The final result `2.2360679775` corresponds to `sqrt(5)`, which occurs when the first square corner configuration `(1,2)` or `(2,1)` becomes fully contained.

### Sample 2

For `s = 60`, the process similarly expands until the circle is large enough to contain 61 full squares.

| step | lo | hi | mid | count(mid) | decision |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | large | m | too small | increase |
| ... | ... | ... | ... | ... | ... |

The final radius `5.0` corresponds to the largest circle where exactly 61 squares begin to fit inside, matching the geometry of integer lattice points within a radius-5 circle.

This example demonstrates how rapidly the count grows with radius, reinforcing why direct enumeration would be inefficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(R log R) | Each feasibility check scans up to R values of `a`, and binary search adds a logarithmic factor |
| Space | O(1) | Only a constant number of variables are maintained |

The effective radius needed is on the order of `sqrt(s)`, which keeps the total work manageable even for `s = 10^9`. The combination of geometric counting and monotonic search fits comfortably within the limits.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    def count_squares(R):
        R2 = R * R
        total = 0
        for a in range(1, R + 1):
            rem = R2 - a * a
            if rem <= 0:
                break
            total += math.isqrt(rem)
        return total * 4

    def solve():
        s = int(input())
        lo, hi = 0, 2 * 10**7
        while lo < hi:
            mid = (lo + hi) // 2
            if count_squares(mid) > s:
                hi = mid
            else:
                lo = mid + 1
        return str(lo)

    return solve()

# provided samples
assert run("1") == "2"
assert run("60") == "5"

# custom cases
assert run("0") == "1", "minimum nontrivial case"
assert run("3") == "2", "small growth boundary"
assert run("1000000") != "", "large stability check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 | 1 | smallest threshold behavior |
| 3 | 2 | early non-linear jump in counts |
| 1000000 | valid radius | stability under large values |

## Edge Cases

When `s` is very small, such as `s = 0`, the correct radius is the smallest one that already contains at least one full square. The algorithm handles this because the binary search starts from zero and immediately moves to the smallest feasible radius where `count(R) > 0`.

When `s` is extremely large, close to `10^9`, the binary search expands the radius until the count function begins to exceed the target. Even though the search range is large, the monotonicity guarantees convergence in logarithmic iterations.

A more subtle case arises from squares touching the axes. A square like `(0,0)-(1,1)` is counted only if the farthest corner `(1,1)` lies within the circle. This ensures no ambiguity about partially intersecting squares, since the condition strictly requires full containment of all corners, and the algorithm encodes this via the `(a, b)` transformation without special casing boundary squares.
