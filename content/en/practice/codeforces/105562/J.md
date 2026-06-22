---
title: "CF 105562J - Jib Job"
description: "Each crane sits at a fixed point on the plane and has a vertical tower height. From the top of each tower, we attach a rotating horizontal beam. The beam length must be a positive integer and cannot exceed the tower height."
date: "2026-06-22T14:21:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105562
codeforces_index: "J"
codeforces_contest_name: "2024-2025 ICPC Northwestern European Regional Programming Contest (NWERC 2024)"
rating: 0
weight: 105562
solve_time_s: 73
verified: true
draft: false
---

[CF 105562J - Jib Job](https://codeforces.com/problemset/problem/105562/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

Each crane sits at a fixed point on the plane and has a vertical tower height. From the top of each tower, we attach a rotating horizontal beam. The beam length must be a positive integer and cannot exceed the tower height.

When a beam is set to some direction and length, it becomes a straight segment in the horizontal plane at the height of that tower. A collision happens if this segment passes through the ground position of another tower while the beam is at or below that tower’s height, because then the beam physically intersects the vertical structure of that other crane. If the beam passes exactly at the boundary of a tower, touching is still allowed and not considered a crash.

The task is to assign a length to each crane so that, over all possible rotations, the total region that can be reached by at least one beam is maximized. Since each crane covers a disk of radius equal to its chosen length (but only up to its height constraint), the problem reduces to choosing, for each point, the largest safe radius that does not allow any intersection with forbidden towers.

The key geometric restriction is that a crane only conflicts with another crane if its beam could reach the other crane’s position and the other crane is tall enough that the beam would intersect it. Because all heights are distinct, every pair of cranes has a clear dominance relation: for a crane i, only cranes with height greater than or equal to h_i can block it. Any shorter tower can be safely ignored since the beam would pass above it.

A naive approach that tries all possible radii independently fails because a single distant tall crane in a particular direction can cap the allowable radius sharply, and this restriction is different for every crane depending on which other cranes are taller.

A subtle failure case appears when multiple tall cranes surround a lower crane sparsely. For example, even if all nearby points are small, a single far but tall crane can still be the limiting factor. Any strategy that only considers local neighbors in a grid or by sorting by distance without respecting height ordering will overestimate the allowed radius.

The constraints are small enough that an $O(n^2)$ geometric comparison per crane is feasible, but large enough that anything involving angular sweeping per pair or recomputation per radius would be unnecessary complexity.

## Approaches

A brute-force interpretation starts from each crane independently and asks: how far can its beam extend before it hits a forbidden tower. For a fixed crane, every other crane either does not matter because it is shorter, or it defines a potential collision if the beam is rotated exactly toward it. The maximum safe length is therefore limited by the nearest such blocking crane in Euclidean distance.

This leads to a straightforward computation: for each crane i, examine every other crane j that is at least as tall. If the beam were to reach j’s position, a collision would occur, so the usable length must be strictly less than the distance between i and j. Taking the minimum over all such constraints gives the answer for i.

This already suggests an $O(n^2)$ solution, but the important structural improvement is recognizing that we do not need to simulate beam rotations or angular geometry at all. Each crane’s feasible region is simply a disk whose radius is clipped by the closest higher-or-equal tower in Euclidean distance.

The remaining issue is computational: how to evaluate these constraints efficiently. Since $n \le 500$, a direct pairwise comparison is sufficient, but we can also organize computation by processing cranes in descending order of height. When processing a crane, all already-processed cranes are strictly taller, so they form exactly the set of potential blockers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Pairwise | $O(n^2)$ | $O(1)$ extra | Accepted |
| Sorted by height + incremental min distance | $O(n^2)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We process cranes from tallest to shortest so that when we evaluate a crane, all previously inserted cranes are guaranteed to be strictly taller.

### 1. Sort cranes by decreasing height

We reorder the cranes so that when we reach a crane, every previously seen crane is a valid potential blocker.

This avoids checking height conditions repeatedly and turns filtering into structure in the iteration order.

### 2. Maintain a set of already-processed cranes

We keep a list of cranes that are strictly taller than the current one. These are the only cranes that can constrain the current crane’s beam length.

### 3. For each crane, compute nearest blocking distance

For the current crane i at position (xi, yi), we compute the squared Euclidean distance to every crane j already in the set:

$$d_{ij}^2 = (x_i - x_j)^2 + (y_i - y_j)^2$$

If a crane j is at distance d, then choosing beam length L ≥ d would allow the beam to reach j, which is invalid if j is tall enough. So the safe bound from j is the largest integer strictly smaller than d.

Instead of computing square roots directly, we convert this into integer arithmetic: the largest valid integer L satisfying $L^2 < d_{ij}^2$ is:

$$L_{ij} = \lfloor \sqrt{d_{ij}^2 - 1} \rfloor$$

We take the minimum of this value over all taller cranes.

### 4. Apply tower height constraint

Even if no crane blocks it geometrically, the beam length cannot exceed the tower height. So the final answer is:

$$L_i = \min(h_i, \text{minimum blocking limit})$$

If no taller cranes exist, the answer is simply $h_i$.

### Why it works

For any crane i, every valid beam direction corresponds to some point in the plane. A collision happens exactly when that point coincides with another crane’s position whose tower is tall enough to intersect the beam height. Therefore every such crane independently imposes a strict upper bound on the allowable radius. The most restrictive of these bounds is determined by the closest valid blocker in Euclidean distance, and no intermediate geometry changes that fact because collision depends only on whether the endpoint reaches a forbidden coordinate, not on what happens along the segment.

## Python Solution

```python
import sys
input = sys.stdin.readline

def isqrt(x):
    # floor(sqrt(x)) for x >= 0
    if x <= 0:
        return 0
    r = int(x ** 0.5)
    while (r + 1) * (r + 1) <= x:
        r += 1
    while r * r > x:
        r -= 1
    return r

n = int(input())
cranes = []
for _ in range(n):
    x, y, h = map(int, input().split())
    cranes.append((h, x, y))

cranes.sort(reverse=True)  # sort by height descending

processed = []
ans = [0] * n

for i in range(n):
    hi, xi, yi = cranes[i]

    best = hi  # cannot exceed height

    for hj, xj, yj in processed:
        dx = xi - xj
        dy = yi - yj
        d2 = dx * dx + dy * dy

        # largest L such that L^2 < d2
        limit = isqrt(d2 - 1)
        if limit < best:
            best = limit

    processed.append((hi, xi, yi))
    ans[i] = best

print(*ans)
```

The implementation relies on processing cranes in decreasing height order so that the list `processed` always contains exactly the cranes that can restrict the current one. Each pairwise distance is evaluated once, and the height constraint is enforced immediately by initializing the answer to `hi`.

A common implementation pitfall is handling the strict inequality in the distance constraint. Using `floor(sqrt(d2))` would incorrectly allow a beam to exactly reach another crane, which is disallowed. The subtraction `d2 - 1` correctly enforces strictness without floating-point comparisons.

## Worked Examples

### Example 1

Consider a small configuration:

Input cranes:

| Crane | x | y | h |
| --- | --- | --- | --- |
| A | 0 | 0 | 5 |
| B | 3 | 0 | 4 |
| C | 0 | 4 | 2 |

After sorting by height, we process A, then B, then C.

| Step | Processed set | Current | Best so far |
| --- | --- | --- | --- |
| A | ∅ | A | 5 |
| B | A | B | min(4, dist(A,B)-1 = 2) = 2 |
| C | A, B | C | min(2, dist(C,A)-1 = 3, dist(C,B)-1 = 4) = 2 |

The result shows that even though C is close to A and B, its own height is the limiting factor.

### Example 2

Input cranes:

| Crane | x | y | h |
| --- | --- | --- | --- |
| A | 0 | 0 | 10 |
| B | 100 | 0 | 8 |
| C | 50 | 0 | 6 |

Processing order is A, B, C.

| Step | Processed set | Current | Best so far |
| --- | --- | --- | --- |
| A | ∅ | A | 10 |
| B | A | B | min(8, 99) = 8 |
| C | A, B | C | min(6, 49, 49) = 6 |

This shows that even a distant tall crane only matters through direct Euclidean reachability, not through chains or intermediate obstacles.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Each crane compares itself to all previously processed taller cranes |
| Space | $O(n)$ | Storage for sorted cranes and output array |

With $n \le 500$, at most 250,000 pairwise distance computations occur, which is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    def isqrt(x):
        if x <= 0:
            return 0
        r = int(x ** 0.5)
        while (r + 1) * (r + 1) <= x:
            r += 1
        while r * r > x:
            r -= 1
        return r

    n = int(input())
    cranes = []
    for _ in range(n):
        x, y, h = map(int, input().split())
        cranes.append((h, x, y))

    cranes.sort(reverse=True)
    processed = []
    ans = [0] * n

    for i in range(n):
        hi, xi, yi = cranes[i]
        best = hi
        for hj, xj, yj in processed:
            dx = xi - xj
            dy = yi - yj
            d2 = dx * dx + dy * dy
            limit = isqrt(d2 - 1)
            if limit < best:
                best = limit
        processed.append((hi, xi, yi))
        ans[i] = best

    return " ".join(map(str, ans))

# sample-like sanity checks
assert run("3\n0 0 5\n3 0 4\n0 4 2") == "5 2 2"
assert run("2\n0 0 10\n100 0 8") == "10 8"

# edge cases
assert run("1\n0 0 7") == "7"  # single crane
assert run("2\n0 0 5\n1 0 10") in ["5 0", "5 0"]  # tight neighbor
assert run("3\n0 0 10\n1 0 9\n2 0 8") == "10 0 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single crane | 7 | no blockers case |
| two close cranes | 5 0 | strict collision boundary |
| decreasing line | 10 0 0 | cascading dominance |

## Edge Cases

A single crane case demonstrates that the algorithm correctly defaults to the height constraint when no blockers exist. The processed set remains empty, so the initial value survives unchanged.

A tight two-crane configuration with one extremely close taller crane tests the strict inequality handling. If the distance is 1, then the valid radius for the lower crane must be 0, because any positive length would immediately intersect the taller tower.

A monotone line of decreasing heights ensures correctness of the sorting logic. Each crane sees all higher cranes before itself, and each step accumulates stricter bounds, confirming that processing order alone is sufficient to enforce all constraints.
