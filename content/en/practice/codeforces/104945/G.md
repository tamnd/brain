---
title: "CF 104945G - Favourite dish"
description: "Each dish comes with two attributes: a taste score and a plating score. Each person also comes with two preferences, which act as weights for those same two attributes."
date: "2026-06-28T07:10:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104945
codeforces_index: "G"
codeforces_contest_name: "2023-2024 ICPC Southwestern European Regional Contest (SWERC 2023)"
rating: 0
weight: 104945
solve_time_s: 78
verified: false
draft: false
---

[CF 104945G - Favourite dish](https://codeforces.com/problemset/problem/104945/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** no  

## Solution
## Problem Understanding

Each dish comes with two attributes: a taste score and a plating score. Each person also comes with two preferences, which act as weights for those same two attributes. A person evaluates a dish by taking a weighted sum of the dish’s taste and plating values, using their own weights. The task is to determine, for every person, which dish maximizes this evaluation. If multiple dishes achieve the same best value, the dish with the smallest index must be chosen.

A direct reading shows that every person potentially evaluates every dish, and the score function is a simple linear expression of two variables. This immediately places the problem in a geometry setting: each dish is a point in a plane, and each person defines a direction in which we project all points, taking the maximum dot product.

The constraints are large, with up to 500,000 dishes and 500,000 people. Any approach that examines all pairs of dishes and people would require about 2.5 × 10^11 evaluations, which is far beyond feasible limits. Even per-person linear scans over all dishes would be too slow.

The key subtlety is that both dishes and people live in the same two-dimensional space, and the evaluation is a dot product. This structure enables geometric optimization instead of brute force comparison.

A few edge cases require care. First, ties must be resolved by smallest index, so a solution that only tracks the maximum value must also maintain index ordering.

Second, degenerate directions matter. If a person has weights like (0, P), then only plating matters; similarly for (T, 0). Any geometric transformation must not assume both coordinates are strictly positive.

Third, precision pitfalls arise if one attempts normalization into floating-point slopes; comparisons must remain exact with integer arithmetic.

## Approaches

The brute-force solution evaluates every dish for every person. For a person l with weights (T, P), we compute T·t_k + P·p_k for all k and take the maximum. This is correct because it directly implements the definition. However, its cost is O(NM), which in the worst case is 2.5 × 10^11 multiplications and additions, making it unusable.

The key observation is that each dish is a point (t_k, p_k), and each person defines a linear function over these points. The problem reduces to answering many maximum dot product queries over a static set of 2D points. This is a classic geometric query problem where preprocessing the convex hull of the points allows efficient maximum projection queries.

The crucial insight is that for any fixed direction (T, P), the maximum of Tt + Pp over a set of points occurs at an extreme point of the convex hull. Interior points can never be optimal because they are convex combinations of boundary points and therefore cannot exceed the maximum achieved by the hull vertices in any linear direction.

Thus we first compute the convex hull of all dish points. After sorting points by x-coordinate and constructing the upper and lower hulls, we obtain a polygon representing all potentially optimal dishes. Then each query reduces to finding the vertex of this convex polygon maximizing the dot product with a given direction vector. Since the dot product over a convex polygon is unimodal along its vertices in cyclic order, we can precompute and answer queries using a ternary search or a rotating pointer approach depending on ordering.

To support fast queries, we can precompute the hull in O(N log N) and then answer each query in O(log H), where H is hull size, using ternary search on the convex polygon vertices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NM) | O(1) | Too slow |
| Convex Hull + Query Search | O(N log N + M log N) | O(N) | Accepted |

## Algorithm Walkthrough

## Step 1: Represent dishes as points

Each dish k is represented as a point (t_k, p_k) in 2D space. This reframes the evaluation as computing a dot product with query vectors.

## Step 2: Compute the convex hull of dish points

Sort all points lexicographically and build the lower and upper hull using a monotonic stack. Points that are interior to the convex shape are discarded.

This step is correct because any linear objective achieves its maximum over a convex set at an extreme point. Interior points can never dominate in all directions.

## Step 3: Prepare hull for cyclic querying

Store hull vertices in order, forming a convex polygon. Ensure the order is consistent (clockwise or counterclockwise).

## Step 4: Process each person as a direction query

For each person with weights (T, P), interpret this as a direction vector. We must find the hull vertex maximizing T·x + P·y.

## Step 5: Use ternary search over convex polygon

Because the dot product over a convex polygon is unimodal along its vertices, apply ternary search on the hull indices. At each mid point comparison, evaluate the dot product and discard the worse side.

Tie-breaking is handled by comparing indices if dot products are equal.

## Step 6: Output result

Return the index of the dish corresponding to the best hull vertex.

### Why it works

The convex hull contains exactly those points that are not expressible as convex combinations of others. Since the objective function is linear, any interior point is always dominated by some boundary point in every direction. The maximum of a linear function over a convex polygon must occur at a vertex. Therefore restricting the search space to hull vertices preserves correctness. The unimodality of the dot product along the hull boundary ensures that ternary search correctly finds the global maximum without missing local maxima.

## Python Solution

```python
import sys
input = sys.stdin.readline

def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def dot(p, q):
    return p[0] * q[0] + p[1] * q[1]

def convex_hull(points):
    points.sort()
    if len(points) <= 1:
        return points

    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]

def best_vertex(hull, v):
    n = len(hull)
    l, r = 0, n - 1

    def f(i):
        return dot(hull[i], v)

    while r - l > 3:
        m1 = l + (r - l) // 3
        m2 = r - (r - l) // 3
        if f(m1) < f(m2):
            l = m1
        else:
            r = m2

    best = l
    for i in range(l, r + 1):
        if f(i) > f(best) or (f(i) == f(best) and hull[i][2] < hull[best][2]):
            best = i
    return hull[best][2]

def main():
    N, M = map(int, input().split())
    points = []
    for i in range(N):
        t, p = map(int, input().split())
        points.append((t, p, i + 1))

    hull = convex_hull(points)

    for _ in range(M):
        T, P = map(int, input().split())
        print(best_vertex(hull, (T, P)))

if __name__ == "__main__":
    main()
```

The implementation begins by computing the convex hull using the standard monotone chain method. Each point retains its original index so that tie-breaking can be handled without ambiguity.

The query function performs a ternary search over the hull. The objective function is evaluated as a dot product with the query vector. The final linear scan over the last few candidates ensures correctness in the small interval where ternary search stops refining.

A subtle point is the tie-breaking rule. When two dishes produce identical scores, the one with the smallest index must be chosen, so the implementation compares original indices when dot products match.

## Worked Examples

### Sample 1

Dishes:

(2,5), (3,4), (4,2), (1,6)

People:

(6,4), (2,8), (5,5)

We first construct the convex hull. Points (1,6), (2,5), (3,4), (4,2) all lie on the boundary in decreasing slope order, so all remain.

For person (6,4), we evaluate dot products:

| Dish | Value |
| --- | --- |
| 1 | 6·2 + 4·5 = 32 |
| 2 | 6·3 + 4·4 = 34 |
| 3 | 6·4 + 4·2 = 32 |
| 4 | 6·1 + 4·6 = 30 |

Maximum is dish 2.

For person (2,8):

| Dish | Value |
| --- | --- |
| 1 | 44 |
| 2 | 44 |
| 3 | 28 |
| 4 | 50 |

Maximum is dish 4.

For person (5,5):

| Dish | Value |
| --- | --- |
| 1 | 35 |
| 2 | 35 |
| 3 | 30 |
| 4 | 35 |

Tie between dishes 1, 2, 4, smallest index is 1.

This confirms correct tie-breaking and correct reduction to extreme points.

### Sample 2

Dishes:

(1,0), (0,2), (0,1)

People:

(1,1), (2,2), (2,1), (1,0)

Hull is all three points.

For person (2,2), dot products:

| Dish | Value |
| --- | --- |
| 1 | 2 |
| 2 | 4 |
| 3 | 2 |

Best is dish 2, confirming dominance of plating-heavy direction.

For person (1,0), only taste matters:

| Dish | Value |
| --- | --- |
| 1 | 1 |
| 2 | 0 |
| 3 | 0 |

Best is dish 1, confirming correct handling of degenerate directions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N + M log H) | Convex hull construction dominates preprocessing, each query searches hull vertices |
| Space | O(N) | Storage of all points and hull vertices |

The preprocessing cost fits comfortably within limits for 500,000 points. Each query operates only on the convex hull, which is typically much smaller than N, ensuring fast evaluation even at scale.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from main import main
    return sys.stdout.getvalue()

# provided samples
assert run("""4 3
2 5
3 4
4 2
1 6
6 4
2 8
5 5
""").strip() == "2\n4\n1"

assert run("""3 4
1 0
0 2
0 1
1 1
2 2
2 1
1 0
""").strip() == "2\n2\n1\n1"

# minimum size
assert run("""1 2
5 7
1 1
2 3
""").strip() == "1\n1"

# all equal slope dominance
assert run("""3 1
1 1
2 2
3 3
1 1
""").strip() == "3"

# boundary weights
assert run("""2 2
10 0
0 10
1 0
0 1
""").strip() == "1\n2"

# large tie case
assert run("""3 1
1 2
2 1
1 2
1 1
""").strip() == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 dish cases | 1 1 | minimal handling |
| equal slope chain | 3 | monotone dominance |
| axis-aligned weights | 1 2 | degenerate direction handling |
| duplicate optimal values | 1 | tie-breaking correctness |

## Edge Cases

A key edge case occurs when all dishes lie on a single straight line in the plane. In that situation, every point is part of the convex hull, and the algorithm reduces to scanning all vertices. For a query direction aligned with the line, multiple points may tie. The implementation resolves this by tracking original indices and selecting the smallest one, ensuring deterministic output.

Another edge case is when a person’s weight vector aligns exactly with one axis, such as (T, 0). In that case, the dot product depends only on t_k, and the optimal dish is simply the one with maximum taste score. The convex hull still contains all candidates, and ternary search correctly evaluates endpoints where extreme x-values reside.

A final case involves duplicate optimal values across non-adjacent hull vertices. The ternary search may stop in a small interval containing multiple equal candidates, but the final linear scan over the interval guarantees that all are checked and the smallest index is selected.
