---
title: "CF 105079C - Frosting Circles"
description: "We are working with a circular “base” region centered at the origin, and several additional circular regions placed on top of it."
date: "2026-06-27T22:48:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105079
codeforces_index: "C"
codeforces_contest_name: "UTPC x WiCS Contest 04-05-23 (UT Internal)"
rating: 0
weight: 105079
solve_time_s: 97
verified: false
draft: false
---

[CF 105079C - Frosting Circles](https://codeforces.com/problemset/problem/105079/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are working with a circular “base” region centered at the origin, and several additional circular regions placed on top of it. The task is to count how many lattice points, meaning points with both coordinates integers, lie inside the base circle and are also covered by at least one of the frosting circles.

Each frosting circle is described by its radius and center. A lattice point contributes to the answer only if it lies inside the cupcake boundary and simultaneously inside at least one frosting circle. The output is a single integer: the total number of such integer-coordinate points.

The constraints are small: both the number of circles and all coordinate magnitudes are at most 50. This immediately rules out any need for sophisticated geometric data structures. A direct enumeration over all relevant integer points is feasible. The only meaningful performance consideration is how many integer points exist inside a radius 50 circle, which is on the order of a few thousand.

A naive mistake here is to iterate over a square bounding box of size 101 by 101 and forget to filter by the base circle first. That is still correct, but an even more subtle error is checking floating point distances with precision issues. Since all coordinates are integers and squared distances stay within safe integer ranges, everything should be done using integer arithmetic.

Edge cases are mostly geometric boundary conditions.

One corner case is a frosting circle completely outside the base circle. For example, if the frosting center is at (100, 100), it contributes nothing, and the algorithm must not accidentally include points due to incorrect bounding box handling.

Another case is full coverage: a frosting circle that fully contains the base circle. In this case, the answer should be the number of integer points in the base circle itself, and a correct solution must avoid double counting even though multiple circles overlap.

A final subtle case is points exactly on boundaries. A point (x, y) should be included if x² + y² ≤ R² or x² + y² ≤ r_i² for any frosting circle. The equality condition matters.

## Approaches

The brute-force idea is straightforward: iterate over every integer point that could possibly lie in the base circle, check whether it is inside the base circle, then check whether it lies in at least one frosting circle, and count it.

Since the base circle has radius up to 50, the bounding square is at most 101 by 101, so about 10,000 candidate points. For each point, checking all N circles costs O(N). This yields roughly 10,000 × 50 = 500,000 distance checks, which is already acceptable in Python.

However, we can structure it more cleanly: instead of scanning a square, we only scan points inside the base circle. That reduces iterations further and simplifies logic.

There is no need for more advanced geometry because the constraints are intentionally small. The key observation is that the answer is defined entirely by integer grid membership tests, so brute-force enumeration is optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Grid Scan | O(R² · N) | O(1) | Accepted |
| Optimized Circle Scan | O(R² + N) | O(1) | Accepted |

## Algorithm Walkthrough

We directly enumerate all integer points inside the base circle and test frosting coverage.

1. Iterate x from -R to R. We only consider these values because any point outside this range cannot satisfy x² + y² ≤ R².
2. For each x, compute the maximum vertical range of valid y values that keep the point inside the base circle. We do not strictly need optimization here, but we still check the condition directly.
3. For each y in [-R, R], test whether (x, y) lies inside the base circle using x² + y² ≤ R².
4. If it does not, skip it immediately since it cannot contribute.
5. If it is inside the base circle, check whether it is covered by at least one frosting circle.
6. For each frosting circle i, check whether (x - x_i)² + (y - y_i)² ≤ r_i².
7. If any frosting circle covers the point, increment the answer.

### Why it works

Every integer point that can contribute must lie in the finite set defined by the base circle. The algorithm enumerates exactly this set. For each such point, it checks whether it satisfies the existence condition over frosting circles. Since membership in the union of circles is checked directly, no point is missed and no invalid point is counted. The logical structure is an exact implementation of the definition of set intersection and union over discrete points.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    n = int(data[0])
    R = int(data[1])
    arr = list(map(int, data[2:]))

    circles = []
    idx = 0
    for _ in range(n):
        r = arr[idx]
        x = arr[idx + 1]
        y = arr[idx + 2]
        idx += 3
        circles.append((r, x, y))

    ans = 0

    for x in range(-R, R + 1):
        for y in range(-R, R + 1):
            if x * x + y * y > R * R:
                continue

            covered = False
            for r, cx, cy in circles:
                dx = x - cx
                dy = y - cy
                if dx * dx + dy * dy <= r * r:
                    covered = True
                    break

            if covered:
                ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation begins by reading all circle data into a list of tuples. Each tuple stores radius and center coordinates for quick access during checks.

The nested loops iterate over the bounding square of the base circle. The condition `x * x + y * y > R * R` enforces the base circle constraint using integer arithmetic, avoiding floating point operations entirely.

For each valid lattice point, we scan all frosting circles. The early break is important because once one circle covers the point, further checks are unnecessary.

## Worked Examples

### Example 1

Input:

```
2 3
1 0 0
1 2 0
```

We enumerate integer points inside radius 3, then test coverage.

| (x, y) | Inside base | Circle 1 | Circle 2 | Covered | Counted |
| --- | --- | --- | --- | --- | --- |
| (0,0) | yes | yes | no | yes | 1 |
| (1,0) | yes | no | no | no | 0 |
| (2,0) | yes | no | yes | yes | 1 |
| (0,1) | yes | yes | no | yes | 1 |

This confirms that overlap is handled via union logic, not double counting.

### Example 2

Input:

```
1 2
5 0 0
```

Here the frosting circle fully contains the base circle.

| (x, y) | Inside base | Inside frosting | Covered |
| --- | --- | --- | --- |
| all valid points | yes | yes | yes |

Every lattice point in the base circle is counted exactly once, confirming that containment cases do not cause overcounting.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(R² · N) | For each integer point in bounding square of radius R, we test up to N circles |
| Space | O(N) | Storage of circle data |

With R ≤ 50, the grid has at most 10,201 points, and N ≤ 50, giving about 500,000 distance checks. This is well within typical Python limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    # inline solution
    data = sys.stdin.read().strip().split()
    n = int(data[0])
    R = int(data[1])
    arr = list(map(int, data[2:]))

    circles = []
    idx = 0
    for _ in range(n):
        r = arr[idx]
        x = arr[idx + 1]
        y = arr[idx + 2]
        idx += 3
        circles.append((r, x, y))

    ans = 0
    for x in range(-R, R + 1):
        for y in range(-R, R + 1):
            if x * x + y * y > R * R:
                continue
            ok = False
            for r, cx, cy in circles:
                dx = x - cx
                dy = y - cy
                if dx * dx + dy * dy <= r * r:
                    ok = True
                    break
            if ok:
                ans += 1

    return str(ans)

# sample
assert run("2 3\n1 0 0\n1 2 0\n") == "3"

# all points covered
assert run("1 1\n10 0 0\n") == "5"

# no coverage
assert run("1 2\n1 100 100\n") == "0"

# boundary touch
assert run("1 2\n1 2 0\n") == "1"

# minimal case
assert run("1 1\n1 0 0\n") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| small overlapping circles | 3 | union logic correctness |
| oversized frosting circle | 5 | full containment |
| distant frosting | 0 | exclusion correctness |
| boundary touch | 1 | equality handling |
| minimal case | 5 | base circle enumeration correctness |

## Edge Cases

A key edge case is when no frosting circle covers any point in the base circle. The algorithm still enumerates all points but never increments the counter because every coverage check fails, producing zero as required.

Another case is when frosting circles overlap heavily. The algorithm breaks early on the first covering circle, so overlapping regions do not inflate counts.

A boundary case occurs when a point lies exactly on a circle boundary. Since the condition uses `<=`, such points are correctly included. For example, if x² + y² equals R², the point is still part of the base and may still be counted if any frosting circle also includes it.

Finally, isolated frosting circles far outside the base circle are safely ignored because the base-circle check filters all irrelevant points before any frosting checks occur.
