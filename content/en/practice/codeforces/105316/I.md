---
title: "CF 105316I - Nested Circles"
description: "We are given several circles on a 2D integer grid, each defined by a center point and a radius. After reading all circles, we receive a sequence of query points. For each query point, we must count how many of the given circles contain or touch that point."
date: "2026-06-23T15:10:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105316
codeforces_index: "I"
codeforces_contest_name: "2024 Aleppo Collegiate Programming Contest"
rating: 0
weight: 105316
solve_time_s: 46
verified: true
draft: false
---

[CF 105316I - Nested Circles](https://codeforces.com/problemset/problem/105316/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several circles on a 2D integer grid, each defined by a center point and a radius. After reading all circles, we receive a sequence of query points. For each query point, we must count how many of the given circles contain or touch that point.

A circle “covers” a point when the Euclidean distance between the point and the circle’s center is less than or equal to the radius. Since all coordinates are integers and radii are small (at most 10), we are essentially checking a bounded geometric condition repeatedly.

The input size suggests multiple test cases, with up to 100,000 circles and 100,000 queries in total across all cases. This immediately rules out any solution that checks every circle for every query. A naive approach would perform up to 10¹⁰ distance checks in the worst case, which is far beyond the time limit.

A subtle but important constraint is that the radius is very small, at most 10. This strongly hints that each circle only affects a tiny local region of the plane, and that we can exploit this locality rather than treating circles as global geometric objects.

One edge case that exposes naive mistakes is when many circles overlap heavily at a single point. For example, if all circles are centered at (1, 1) with radius 10, then every query near that point should count all circles. A naive solution still works logically, but is too slow. The real risk is in optimizations that try to skip checks incorrectly based on bounding boxes without precise distance verification, which can lead to off-by-one errors at the boundary where x² + y² equals r² exactly.

## Approaches

The brute-force method is straightforward: for each query point, iterate over every circle and compute whether the point lies within it using squared distance. This is correct because the definition is direct and independent per circle. However, it performs n × q distance checks per test case. With total constraints reaching 10⁵ for both n and q, this becomes about 10¹⁰ operations, which is not feasible.

The key observation comes from the radius bound. Each circle only influences points within a (2r + 1) × (2r + 1) square, and since r ≤ 10, this region is at most 21 × 21 = 441 grid points. This suggests a reversal of perspective: instead of asking for each point which circles contain it, we can distribute each circle’s contribution to all integer points it covers.

We can precompute a frequency map over grid points. For every circle, we iterate over all integer offsets (dx, dy) such that dx² + dy² ≤ r², and increment a counter for the corresponding point (x + dx, y + dy). After processing all circles, each query becomes a direct dictionary lookup.

This works because the total number of lattice points per circle is bounded by a constant (~300-400), so preprocessing is linear in n with a small constant factor.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Precompute coverage map | O(n · r² + q) | O(n · r²) | Accepted |

## Algorithm Walkthrough

We transform each circle into the set of integer grid points it covers and accumulate contributions.

1. Create a hash map (or dictionary) that will store, for each integer point, how many circles cover it. This map represents a precomputed answer for all possible query points.
2. For each circle with center (cx, cy) and radius r, iterate over all integer offsets dx from −r to r. For each dx, iterate over dy from −r to r, and check whether dx² + dy² ≤ r². This condition ensures we only include points inside or on the circle boundary.
3. For every valid (dx, dy), increment the counter at key (cx + dx, cy + dy). This effectively “paints” the circle onto the grid, increasing coverage counts for all affected integer points.
4. After processing all circles, each query point (qx, qy) is answered by reading the stored value in the map. If the point is not present, its value is zero.

The crucial idea is that we shift computation from query time to preprocessing time. Each circle contributes only to a small fixed neighborhood, making the overall work manageable.

### Why it works

The correctness relies on the fact that each circle contributes independently to each lattice point. The preprocessing step enumerates exactly the integer points satisfying the circle inequality for each circle. Since every such point is visited exactly once per circle, the stored value at any coordinate equals the number of circles whose geometric condition includes that point. Querying simply retrieves this precomputed aggregation, so no information is lost or double-counted incorrectly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, q = map(int, input().split())

        mp = {}

        circles = []
        for _ in range(n):
            x, y, r = map(int, input().split())
            circles.append((x, y, r))

        # precompute offsets for each possible radius (small bound r <= 10)
        for x, y, r in circles:
            rr = r * r
            for dx in range(-r, r + 1):
                dy_limit = int((rr - dx * dx) ** 0.5)
                for dy in range(-dy_limit, dy_limit + 1):
                    px = x + dx
                    py = y + dy
                    key = (px, py)
                    mp[key] = mp.get(key, 0) + 1

        for _ in range(q):
            x, y = map(int, input().split())
            out.append(str(mp.get((x, y), 0)))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution first builds a dictionary that stores coverage counts for all integer points affected by any circle. For each circle, it enumerates only valid integer offsets inside the circle using the equation dx² + dy² ≤ r². The inner loop is tightly bounded by the radius constraint, so it remains efficient.

A subtle implementation detail is using squared distances instead of Euclidean distance, avoiding floating-point precision issues. Another detail is using a dictionary keyed by tuples, which is efficient enough given the bounded total number of generated points.

## Worked Examples

Consider a simple case with two circles and three queries.

Input:

```
1
2 3
0 0 1
2 0 1
0 0
1 0
2 0
```

We track coverage generation.

| Circle | dx,dy generated | Updated points |
| --- | --- | --- |
| (0,0,r=1) | (0,0),(±1,0),(0,±1) | (0,0),(1,0),(-1,0),(0,1),(0,-1) |
| (2,0,r=1) | (0,0),(±1,0),(0,±1) | (2,0),(3,0),(1,0),(2,1),(2,-1) |

Now query results:

| Query | Lookup | Answer |
| --- | --- | --- |
| (0,0) | 1 | 1 |
| (1,0) | 2 | 2 |
| (2,0) | 1 | 1 |

This confirms overlapping contributions are accumulated correctly.

Now consider a boundary-touch case.

Input:

```
1
1 2
0 0 2
2 0
3 0
```

| Query | Condition | Result |
| --- | --- | --- |
| (2,0) | 2² + 0² = 4 ≤ 4 | 1 |
| (3,0) | 3² = 9 > 4 | 0 |

This demonstrates that boundary inclusion is handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · r² + q) | Each circle contributes at most about 400 lattice points, and each query is O(1) average lookup |
| Space | O(n · r²) | Dictionary stores only covered integer points |

Given that total n and q across all test cases are at most 10⁵ and r ≤ 10, the constant factor stays small enough to run comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, q = map(int, input().split())
        mp = {}

        for _ in range(n):
            x, y, r = map(int, input().split())
            rr = r * r
            for dx in range(-r, r + 1):
                dy_limit = int((rr - dx * dx) ** 0.5)
                for dy in range(-dy_limit, dy_limit + 1):
                    px, py = x + dx, y + dy
                    mp[(px, py)] = mp.get((px, py), 0) + 1

        for _ in range(q):
            x, y = map(int, input().split())
            out.append(str(mp.get((x, y), 0)))

    return "\n".join(out)

# provided sample (formatted minimal example)
assert run("""1
2 3
0 0 1
2 0 1
0 0
1 0
2 0
""") == "1\n2\n1"

# minimum case
assert run("""1
1 1
0 0 1
0 0
""") == "1"

# no coverage
assert run("""1
1 1
0 0 1
5 5
""") == "0"

# boundary check
assert run("""1
1 2
0 0 2
2 0
3 0
""") == "1\n0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single overlap | 1 2 1 | overlapping coverage accumulation |
| minimum case | 1 | basic inclusion |
| far query | 0 | absence handling |
| boundary case | 1 0 | exact circle boundary correctness |

## Edge Cases

A key edge case is when a query lies exactly on the circle boundary. For a circle centered at (0, 0) with radius 2, the point (2, 0) must be counted, since 2² = 4 equals r². The algorithm includes this point because the condition dx² + dy² ≤ r² explicitly allows equality, and integer enumeration guarantees (2, 0) is generated when dx = 2, dy = 0.

Another case is multiple circles overlapping at identical coordinates. If ten circles all share center (5, 5) with radius 1, then the map entry at (5, 5) is incremented ten times during preprocessing. A query at (5, 5) simply reads that accumulated value, confirming linear accumulation behavior without interference between circles.
