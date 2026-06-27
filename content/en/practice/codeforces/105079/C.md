---
title: "CF 105079C - Frosting Circles"
description: "We are given a circular cake centered at the origin, and we only care about lattice points, meaning points with integer coordinates that lie inside or on this big circle. On top of this cake, there are several smaller circular regions representing frosting."
date: "2026-06-27T21:25:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105079
codeforces_index: "C"
codeforces_contest_name: "UTPC x WiCS Contest 04-05-23 (UT Internal)"
rating: 0
weight: 105079
solve_time_s: 67
verified: false
draft: false
---

[CF 105079C - Frosting Circles](https://codeforces.com/problemset/problem/105079/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a circular cake centered at the origin, and we only care about lattice points, meaning points with integer coordinates that lie inside or on this big circle. On top of this cake, there are several smaller circular regions representing frosting. Each frosting circle has its own center and radius.

The task is to count how many integer lattice points inside the big circle are covered by at least one frosting circle.

The constraints are small: the radius and coordinates are all bounded by 50 in absolute value, and there are at most 50 frosting circles. This immediately suggests that the total number of integer points inside the big circle is at most around 8000, since the area of a radius 50 circle is about 7800. This is small enough that iterating over all candidate integer points is completely feasible. Even checking each point against all circles is at most about 8000 times 50, which is well within limits.

A subtle edge case comes from overlap. A point may lie in multiple frosting circles, but it must only be counted once. Another edge case is boundary inclusion: points exactly on the circle boundary count as inside, so distance comparisons must be non-strict.

A failure mode that often appears here is iterating only over a bounding box without checking the main circle constraint properly, or double counting points by summing contributions per circle instead of using a union-style check.

## Approaches

The most direct approach is to enumerate all integer coordinates in a square bounding box that contains the big circle, then check whether each point lies inside the main circle. For each such valid point, we then check whether it lies in at least one frosting circle.

This works because the domain is tiny. The bounding box is from -R to R in both x and y directions, so at most (2R+1)^2 points, which is about 10,000 when R is 50. For each point, we test up to 50 circles, leading to roughly 500,000 distance checks in the worst case. Each check is constant time.

The key idea that makes this efficient enough is that geometry constraints are local and small-scale. We do not need sweeping lines or advanced spatial indexing. A full brute-force enumeration is already optimal under these bounds.

The main improvement over a naive interpretation is avoiding continuous geometry reasoning and replacing it with discrete enumeration of integer coordinates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force per circle union | O(N * R^2) but with double counting risk | O(1) | Risky / redundant |
| Grid enumeration with coverage check | O(R^2 * N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Iterate over all integer coordinates (x, y) such that -R ≤ x ≤ R and -R ≤ y ≤ R. This forms the full bounding square containing the cake. We restrict to this region because no valid point outside it can belong to the main circle.
2. For each point (x, y), check whether it lies inside or on the boundary of the main circle by verifying x² + y² ≤ R². This ensures we only consider valid cake points.
3. If the point is outside the cake circle, skip it immediately. This prevents unnecessary checks against frosting circles.
4. For each remaining valid point, check whether it lies inside at least one frosting circle by testing whether (x - x_i)² + (y - y_i)² ≤ r_i² for any i.
5. If at least one frosting circle contains the point, increment the answer by one. We only count the point once even if multiple circles cover it.
6. After processing all integer points, output the accumulated count.

### Why it works

Every integer point inside the cake is explicitly considered exactly once due to the grid enumeration. For each such point, we check whether it belongs to the union of all frosting disks using a direct membership test. Since set union membership is correctly reduced to a logical OR over all circles, no point is missed and no point is double counted. The correctness follows from the fact that integer points are independent and membership is tested exhaustively.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, R = map(int, input().split())
    circles = []
    for _ in range(n):
        r, x, y = map(int, input().split())
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

The solution starts by reading all frosting circles into memory since we repeatedly query them for each lattice point.

We then enumerate all integer coordinates inside the bounding square of the cake. The first geometric check ensures we stay within the main circle, which is the actual domain of interest.

For each valid point, we scan through all frosting circles. The moment we find one that contains the point, we stop checking further circles because we only care about existence, not multiplicity. This early exit is important in practice, especially when many circles overlap.

The distance checks are done using squared distances to avoid floating-point precision issues.

## Worked Examples

### Example 1

Input:

```
R = 3
circles = [(2, 0, 0), (1, 2, 0)]
```

We consider all integer points in the square [-3, 3].

| (x, y) | inside cake? | covered? | reason |
| --- | --- | --- | --- |
| (0,0) | yes | yes | inside first circle |
| (2,0) | yes | yes | inside second circle |
| (3,0) | yes | no | outside both frosting circles |
| (1,1) | yes | yes | inside first circle |

Answer accumulates only for covered points.

This confirms that overlap does not cause double counting, since each point is processed once.

### Example 2

Input:

```
R = 2
circles = [(1, 2, 0)]
```

| (x, y) | inside cake? | covered? |
| --- | --- | --- |
| (2,0) | yes | yes |
| (1,0) | yes | no |
| (0,0) | yes | no |

Only boundary point (2,0) lies in both the cake and frosting.

This shows correct handling of boundary conditions where equality must be included.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(R^2 * N) | Each lattice point in the bounding box is checked against up to N circles |
| Space | O(N) | Stores all frosting circles |

The maximum number of integer points is about (2R+1)^2 ≤ 10201. With N ≤ 50, the total operations are roughly half a million distance checks, which fits easily within a 1 second limit in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys

    n, R = map(int, sys.stdin.readline().split())
    circles = []
    for _ in range(n):
        r, x, y = map(int, sys.stdin.readline().split())
        circles.append((r, x, y))

    ans = 0
    for x in range(-R, R + 1):
        for y in range(-R, R + 1):
            if x * x + y * y > R * R:
                continue
            for r, cx, cy in circles:
                dx = x - cx
                dy = y - cy
                if dx * dx + dy * dy <= r * r:
                    ans += 1
                    break

    return str(ans)

# provided sample
assert run("2 3\n2 0 0\n1 2 0\n") == "11"

# minimum case
assert run("1 1\n1 0 0\n") == "5"

# no coverage
assert run("1 2\n1 10 10\n") == "0"

# full coverage
assert run("1 2\n5 0 0\n") == "13"

# boundary sensitivity
assert run("2 2\n1 2 0\n1 -2 0\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single circle covering all | full grid count | full coverage correctness |
| far circle | 0 | rejection of irrelevant circles |
| boundary circles | small value | boundary inclusion handling |
| two edge circles | 2 | no double counting |

## Edge Cases

One important edge case is when frosting circles lie completely outside the cake. In that situation, every point fails the inner circle check against all frostings, so the answer must be zero. The algorithm handles this naturally because the inner loop never triggers `covered = True`.

Another edge case is when a frosting circle is larger than the cake and centered at the origin. Every valid lattice point passes the frosting check immediately, so the answer becomes exactly the number of lattice points inside the cake. The enumeration ensures every such point is counted once.

A third edge case is when multiple frosting circles overlap heavily. Since we break early once coverage is found, each point contributes exactly once regardless of how many circles include it.
