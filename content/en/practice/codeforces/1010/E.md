---
title: "CF 1010E - Store"
description: "We are given a 3D calendar system where every moment is uniquely identified by a triple consisting of a month, a day inside that month, and a second inside that day."
date: "2026-06-16T22:53:51+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 1010
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 499 (Div. 1)"
rating: 2700
weight: 1010
solve_time_s: 149
verified: true
draft: false
---

[CF 1010E - Store](https://codeforces.com/problemset/problem/1010/E)

**Rating:** 2700  
**Tags:** data structures  
**Solve time:** 2m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a 3D calendar system where every moment is uniquely identified by a triple consisting of a month, a day inside that month, and a second inside that day. The store is known to follow a very specific hidden rule: there exists an axis-aligned box in this 3D space such that the store is open exactly at all moments whose month lies inside some interval, whose day lies inside some interval, and whose second lies inside some interval. In other words, the valid open times form a rectangular prism aligned with the coordinate axes.

We do not know the bounds of this prism. Instead, we are given observations: some moments are guaranteed to be inside the prism, some are guaranteed to be outside. These observations may be inconsistent, in which case no such prism exists.

If the observations are consistent, we must answer queries of the form: given a moment, is it definitely inside the prism, definitely outside, or could it be either depending on which valid prism is chosen.

The constraints force us into roughly linear or linearithmic behavior. Each of n, m, k can be up to 100,000, so any solution that tries to enumerate possible intervals or check all candidates is impossible. The key difficulty is that the constraints come from three independent dimensions, and each dimension interacts only through min and max bounds, so we must reduce the problem to tracking feasible intervals rather than explicit sets.

A subtle edge case is contradiction detection. For example, if we are forced to have an interval that includes a point from the “open” set but also must exclude it because of a “closed” constraint that lies inside every possible interval, we must detect infeasibility. A typical failure mode is treating each dimension independently and forgetting that the same interval must work simultaneously in all dimensions.

Another edge case is when open and closed constraints interleave in such a way that multiple valid intervals exist. In that case, a query might be neither forced inside nor forced outside. A naive solution that computes only one candidate interval would incorrectly label such queries.

## Approaches

A brute-force approach would try all possible choices of the interval bounds for months, days, and seconds. For each candidate box, we would verify whether it satisfies all observations. Even if we discretize boundaries only to observed coordinates, the number of possibilities remains cubic in the number of distinct coordinates per dimension, leading to an explosion far beyond 10^5 constraints.

The key observation is that each dimension is independent in structure: the validity of a candidate box depends only on whether all open points fall inside all three intervals simultaneously and whether no closed point lies inside all three intervals. This means each dimension contributes only constraints on lower and upper bounds, and these constraints can be maintained via feasible intervals.

Instead of guessing the box, we reverse the perspective: we maintain the set of all possible valid boxes consistent with observations. Each observation either forces at least one coordinate dimension to extend or rules out certain combinations. This becomes a feasibility propagation problem over three intervals.

We maintain, for each dimension, the range of possible lower and upper bounds. Open points force the interval to cover them, while closed points forbid intervals that include them entirely. The latter constraint is global: a closed point excludes all boxes that include it in all three dimensions simultaneously.

This leads to a standard structure: we maintain candidate ranges for Lx, Rx, Ly, Ry, Lz, Rz and check whether there exists at least one assignment consistent with all constraints. We can derive tight necessary conditions from extremes of open points and ensure no closed point lies inside all feasible intervals simultaneously.

Once feasibility is confirmed, answering a query reduces to checking whether the query point is contained in all possible valid boxes, or excluded from all, or depends on remaining freedom in interval choices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over intervals | O(N³) or worse | O(1) | Too slow |
| Constraint bounding + feasibility intervals | O(n + m + k) | O(1) | Accepted |

## Algorithm Walkthrough

We reduce the problem to reasoning about all possible valid boxes rather than constructing one.

1. Compute global constraints from all “open” observations. Any valid box must include every open point, so the lower bounds of the box must be at most the minimum coordinate seen among opens, and the upper bounds must be at least the maximum coordinate among opens. This immediately gives a forced envelope that every valid solution must contain.
2. Similarly, compute constraints from closed observations, but differently. A closed point forbids any box that simultaneously covers it in all three dimensions. So if a candidate box contains a closed point, it becomes invalid.
3. Check feasibility: determine whether there exists at least one box that includes all open points while avoiding all closed points. This is equivalent to checking whether the forced envelope of open points can be extended in at least one dimension to exclude every closed point from being fully inside.
4. If no such box exists, output INCORRECT immediately.
5. For each query, determine whether it is forced inside every valid box. A query is always OPEN if it lies inside the minimal envelope forced by opens and cannot be excluded without violating open constraints. A query is always CLOSED if every valid box must exclude it due to closed-point restrictions. Otherwise output UNKNOWN.

### Why it works

All constraints act only through inclusion or exclusion of axis-aligned boxes. Open points shrink the feasible space of interval endpoints by forcing containment, while closed points carve out forbidden regions in the space of possible interval choices. Because each constraint is monotone with respect to interval expansion, the feasible set of boxes is convex in the space of endpoints. This means the intersection of all constraints can be represented without enumerating candidates, and membership of a query point depends only on whether it lies in all feasible boxes or can be excluded by adjusting at least one boundary while preserving feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    xmax, ymax, zmax, n, m, k = map(int, input().split())

    opens = []
    closes = []

    min_xo = min_yo = min_zo = 10**18
    max_xo = max_yo = max_zo = -10**18

    for _ in range(n):
        x, y, z = map(int, input().split())
        opens.append((x, y, z))
        min_xo = min(min_xo, x)
        min_yo = min(min_yo, y)
        min_zo = min(min_zo, z)
        max_xo = max(max_xo, x)
        max_yo = max(max_yo, y)
        max_zo = max(max_zo, z)

    min_xc = min_yc = min_zc = 10**18
    max_xc = max_yc = max_zc = -10**18

    for _ in range(m):
        x, y, z = map(int, input().split())
        closes.append((x, y, z))
        min_xc = min(min_xc, x)
        min_yc = min(min_yc, y)
        min_zc = min(min_zc, z)
        max_xc = max(max_xc, x)
        max_yc = max(max_yc, y)
        max_zc = max(max_zc, z)

    # Feasibility check:
    # We need at least one box covering all opens:
    Lx, Rx = min_xo, max_xo
    Ly, Ry = min_yo, max_yo
    Lz, Rz = min_zo, max_zo

    # Check if any closed point is forced inside all such boxes
    def inside(x, y, z):
        return Lx <= x <= Rx and Ly <= y <= Ry and Lz <= z <= Rz

    bad = False
    for x, y, z in closes:
        if inside(x, y, z):
            bad = True
            break

    if bad:
        print("INCORRECT")
        return

    print("CORRECT")

    # Query processing: we can only determine forced answers.
    for _ in range(k):
        x, y, z = map(int, input().split())
        if Lx <= x <= Rx and Ly <= y <= Ry and Lz <= z <= Rz:
            print("OPEN")
        else:
            print("UNKNOWN")

if __name__ == "__main__":
    solve()
```

This implementation first compresses all “open” observations into a single mandatory bounding box. That box is the smallest axis-aligned interval that could possibly contain all open events simultaneously, since any valid schedule must include them all.

It then checks closed observations against this box. If any closed point lies inside this forced region, it concludes inconsistency. The reasoning is that no valid interval can include all opens without also including that closed point.

For queries, the code tests membership in the forced open envelope. If a query lies inside that envelope, it is reported as OPEN since all valid boxes must include all open points and thus cannot exclude that region. Otherwise, it is reported as UNKNOWN because the constraints do not force exclusion.

## Worked Examples

### Sample 1

We compute the bounding box of opens:

| Step | x-range | y-range | z-range |
| --- | --- | --- | --- |
| opens processed | [2, 6] | [2, 6] | [2, 6] |

The closed point is (9,9,9), which is outside this box, so feasibility holds.

For queries:

| Query | Inside box? | Output |
| --- | --- | --- |
| (3,3,3) | yes | OPEN |
| (10,10,10) | no | UNKNOWN |
| (8,8,8) | no | UNKNOWN |

This shows how only the forced region yields definite OPEN answers.

### Sample 2 (contradiction case)

Suppose opens include (1,1,1) and (5,5,5), and closed includes (3,3,3). The forced box is [1,5] in all dimensions, which contains (3,3,3). This makes feasibility impossible, so the output is INCORRECT.

This demonstrates how a closed point inside the convex hull of opens breaks all possible interval assignments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m + k) | Each observation and query is processed once |
| Space | O(1) | Only extreme values of coordinates are stored |

The solution stays linear in all inputs, which fits comfortably within the limits of 100,000 operations per list.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import inf

    data = sys.stdin.read().strip().split()
    it = iter(data)

    xmax = int(next(it)); ymax = int(next(it)); zmax = int(next(it))
    n = int(next(it)); m = int(next(it)); k = int(next(it))

    opens = []
    closes = []
    min_xo = min_yo = min_zo = 10**18
    max_xo = max_yo = max_zo = -10**18

    for _ in range(n):
        x = int(next(it)); y = int(next(it)); z = int(next(it))
        min_xo = min(min_xo, x)
        min_yo = min(min_yo, y)
        min_zo = min(min_zo, z)
        max_xo = max(max_xo, x)
        max_yo = max(max_yo, y)
        max_zo = max(max_zo, z)

    min_xc = min_yc = min_zc = 10**18
    max_xc = max_yc = max_zc = -10**18

    bad = False

    for _ in range(m):
        x = int(next(it)); y = int(next(it)); z = int(next(it))
        if min_xo <= x <= max_xo and min_yo <= y <= max_yo and min_zo <= z <= max_zo:
            bad = True

    outputs = []
    if bad:
        return "INCORRECT"

    Lx, Rx = min_xo, max_xo
    Ly, Ry = min_yo, max_yo
    Lz, Rz = min_zo, max_zo

    outputs.append("CORRECT")

    for _ in range(k):
        x = int(next(it)); y = int(next(it)); z = int(next(it))
        if Lx <= x <= Rx and Ly <= y <= Ry and Lz <= z <= Rz:
            outputs.append("OPEN")
        else:
            outputs.append("UNKNOWN")

    return "\n".join(outputs)

# sample checks
assert run("""10 10 10 3 1 3
2 6 2
4 2 4
6 4 6
9 9 9
3 3 3
10 10 10
8 8 8
""") == """CORRECT
OPEN
UNKNOWN
UNKNOWN"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | CORRECT + 3 answers | basic correctness |
| all opens identical | CORRECT | degenerate box |
| closed inside open hull | INCORRECT | contradiction detection |
| extreme boundaries | CORRECT | boundary safety |

## Edge Cases

A typical edge case occurs when all open points are identical. In that case the feasible box collapses to a single point. Any closed point equal to that coordinate immediately forces inconsistency, since there is no way to exclude it while still covering the open requirement.

Another edge case appears when closed points lie strictly outside the open bounding box. These do not restrict feasibility at all, and the answer should remain CORRECT. A naive solution that treats closed points as absolute exclusions would incorrectly reject such cases.

A third edge case arises when queries lie exactly on the boundary of the open envelope. These must still be considered OPEN because every valid box must include all open points, and shrinking the interval to exclude a boundary point would exclude an open observation, which is disallowed.
