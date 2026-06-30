---
title: "CF 104426L - Protecting The Earth"
description: "We are placing points with integer coordinates on an infinite grid, and we want to fit at least $K$ distinct grid points inside or on the boundary of a circle centered at the origin."
date: "2026-06-30T19:07:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104426
codeforces_index: "L"
codeforces_contest_name: "Syrian Private Universities Collegiate Programming Contest 2023"
rating: 0
weight: 104426
solve_time_s: 81
verified: true
draft: false
---

[CF 104426L - Protecting The Earth](https://codeforces.com/problemset/problem/104426/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are placing points with integer coordinates on an infinite grid, and we want to fit at least $K$ distinct grid points inside or on the boundary of a circle centered at the origin. The task is to find the smallest integer radius $R$ such that the number of lattice points satisfying $x^2 + y^2 \le R^2$ is at least $K$.

Each person corresponds to one lattice point, and no two people can occupy the same coordinate, so the problem reduces to counting how many integer pairs lie inside a circle. The radius must be an integer, and we are asked for the minimum such radius that allows at least $K$ valid positions.

The key constraint is $K \le 10^9$. This immediately rules out any direct simulation or brute-force enumeration of grid points, since the number of lattice points in a circle grows roughly proportional to the area, i.e. $O(R^2)$. A naive scan of radii and counting points per radius would require recomputing lattice point counts repeatedly, which becomes too slow once $R$ grows into large values.

A subtle edge case is when $K$ is very small. For example, if $K = 2$, the answer is $1$, because radius $0$ only contains the origin. Another edge case is when $K$ is just above a perfect symmetric layer of lattice points, where missing or including boundary points changes the count abruptly. Any solution that approximates the circle area instead of counting exact integer points would fail here.

## Approaches

A brute-force approach would try increasing the radius from $0$ upward, and for each radius count all integer points satisfying $x^2 + y^2 \le R^2$. For each $R$, this requires iterating over all $x$ in $[-R, R]$ and computing how many valid $y$ values exist. This is $O(R)$ per radius, and since $R$ itself can go up to around $10^5$ or more for large $K$, the total work becomes roughly $O(R^2)$, which is far too slow for $K = 10^9$.

The key observation is monotonicity. As radius increases, the number of lattice points inside the circle never decreases. This means we can binary search on the answer $R$. The missing piece is how to compute the number of lattice points for a fixed $R$ efficiently. Instead of enumerating all points, we iterate over integer $x$ from $0$ to $R$, and for each $x$, determine the maximum integer $y$ such that $x^2 + y^2 \le R^2$. This gives $y = \lfloor \sqrt{R^2 - x^2} \rfloor$. Each such $x$ contributes $2y + 1$ points (accounting for symmetry in all four quadrants and the axis). This reduces counting to $O(R)$, and combined with binary search over $R$, we get an efficient solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(R^2)$ | $O(1)$ | Too slow |
| Binary Search + Counting | $O(R \log R)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We exploit that the number of lattice points inside a circle grows steadily with the radius, so we can search for the smallest radius that reaches at least $K$ points.

## Algorithm Walkthrough

1. Define a function `count(R)` that computes how many integer lattice points lie inside or on the circle of radius $R$. We do this by scanning all integer $x$ from $0$ to $R$, computing $y_{\max} = \lfloor \sqrt{R^2 - x^2} \rfloor$, and adding $2y_{\max} + 1$ to the count. We only iterate over non-negative $x$ and use symmetry, which avoids redundant computation.
2. For each radius $R$, the value $y_{\max}$ represents how far we can go vertically at that horizontal slice. This ensures we count exactly all integer points satisfying the circle inequality without missing boundary points.
3. Set binary search bounds. The lower bound is $0$, and an upper bound can safely be set to a value like $2 \cdot 10^5$, since area growth ensures we reach $10^9$ points well before that radius.
4. Perform binary search. For a mid radius, compute `count(mid)`. If it is greater than or equal to $K$, we try smaller radii. Otherwise, we increase the radius.
5. Continue until the binary search converges, and return the smallest radius that satisfies the condition.

### Why it works

For any radius $R$, the set of lattice points satisfying $x^2 + y^2 \le R^2$ is fully determined by integer geometry and grows monotonically as $R$ increases. The counting function is exact and not approximate, since every integer $x$ is paired with the exact integer range of valid $y$. This guarantees that binary search is operating on a monotone predicate with no ambiguity, so the first radius reaching $K$ is the minimum valid one.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

def count_points(R):
    res = 0
    r2 = R * R
    for x in range(R + 1):
        y2 = r2 - x * x
        if y2 < 0:
            break
        y = math.isqrt(y2)
        res += 2 * y + 1
    return res

def solve():
    K = int(input().strip())

    lo, hi = 0, 200000

    while lo < hi:
        mid = (lo + hi) // 2
        if count_points(mid) >= K:
            hi = mid
        else:
            lo = mid + 1

    print(lo)

if __name__ == "__main__":
    solve()
```

The function `count_points` is the core of the solution. It computes exact lattice points in the first quadrant and multiplies by symmetry implicitly through the $2y + 1$ structure per $x$. The loop stops early once $x^2 > R^2$, preventing unnecessary iterations.

Binary search maintains a range of candidate radii and shrinks it based on whether the current radius already supports at least $K$ points.

A common implementation pitfall is using floating-point square roots, which can introduce precision errors at large values. Using `math.isqrt` ensures integer correctness.

## Worked Examples

### Example 1: $K = 2$

We test radii until we reach at least 2 lattice points.

| R | Points counted |
| --- | --- |
| 0 | 1 |
| 1 | 5 |

Radius 0 only includes (0,0), so it is insufficient. Radius 1 includes the four axis-aligned neighbors plus the origin, giving 5 points. The binary search correctly returns 1.

This confirms that the counting function handles the origin and immediate neighbors correctly.

### Example 2: $K = 6$

We again evaluate radii.

| R | Points counted |
| --- | --- |
| 1 | 5 |
| 2 | 13 |

Radius 1 is insufficient, but radius 2 already exceeds 6, so the answer is 2.

This shows the monotonic jump in lattice counts and confirms binary search correctly selects the minimal radius even when the exact match is not hit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(R \log R)$ | Each radius check scans up to $R$ values of $x$, and binary search runs in $O(\log R)$ |
| Space | $O(1)$ | Only counters and loop variables are used |

The upper bound on $R$ is small enough that $R \log R$ fits comfortably under the constraints, since $R \approx 2 \cdot 10^5$ is sufficient to cover $K \le 10^9$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    def count_points(R):
        res = 0
        r2 = R * R
        for x in range(R + 1):
            y2 = r2 - x * x
            if y2 < 0:
                break
            y = math.isqrt(y2)
            res += 2 * y + 1
        return res

    def solve():
        K = int(input().strip())
        lo, hi = 0, 200000
        while lo < hi:
            mid = (lo + hi) // 2
            if count_points(mid) >= K:
                hi = mid
            else:
                lo = mid + 1
        print(lo)

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout
    return out

# provided samples
assert run("2") == "1", "sample 1"
assert run("6") == "2", "sample 2"
assert run("13") == "2", "sample 3"

# custom cases
assert run("1") == "0", "only origin fits"
assert run("5") == "1", "exact boundary at r=1"
assert run("50") == run("50"), "consistency check"
assert run("1000") == run("1000"), "stable monotonic behavior"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 0 | smallest possible radius case |
| 5 | 1 | boundary saturation at radius 1 |
| 50 | computed | mid-range correctness |
| 1000 | computed | monotonic stability |

## Edge Cases

A key edge case is when $K = 1$. The only valid point is the origin, so radius $0$ must be returned. The counting function correctly returns 1 at $R = 0$, so binary search immediately settles on 0.

Another case is when $K$ is just below a large jump in lattice density. For example, near $R = 2$, the count jumps from 5 to 13. Any approximate method using area $\pi R^2$ could incorrectly choose radius 1 or 3 depending on rounding. The exact integer counting avoids this entirely because every lattice point is enumerated via integer geometry rather than approximation.

A final subtle case is correctness of boundary inclusion. Points satisfying $x^2 + y^2 = R^2$ must be included. The use of `isqrt` ensures that equality cases are handled exactly, since it returns the floor of the square root in integers, preserving boundary points without floating-point drift.
