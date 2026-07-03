---
title: "CF 103448B - bb \u53bb\u98df\u5802"
description: "We are given a rectangular building on a 2D plane, aligned with the coordinate axes. Each canteen is represented as a single point. For every canteen, we want to compute its shortest Euclidean distance to any point on the rectangle, including its interior boundary and corners."
date: "2026-07-03T07:26:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103448
codeforces_index: "B"
codeforces_contest_name: "The 16-th Beihang University Collegiate Programming Contest (BCPC 2021) - Preliminary"
rating: 0
weight: 103448
solve_time_s: 40
verified: true
draft: false
---

[CF 103448B - bb \u53bb\u98df\u5802](https://codeforces.com/problemset/problem/103448/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular building on a 2D plane, aligned with the coordinate axes. Each canteen is represented as a single point. For every canteen, we want to compute its shortest Euclidean distance to any point on the rectangle, including its interior boundary and corners. After computing these distances, we pick the canteen with the smallest distance, and if multiple canteens share the same minimum value, we choose the one with the smallest index.

Geometrically, this is asking for the distance from a point to an axis-aligned rectangle, which behaves differently depending on where the point lies relative to the rectangle. If the point is horizontally and vertically aligned with the rectangle’s projection, the closest point is on an edge. If it lies diagonally outside, the closest point is a corner. If it were inside, the distance would be zero, but the problem explicitly guarantees no canteen lies inside or on the boundary, so every point is strictly outside.

The constraint n up to 100000 implies we must process each canteen in constant time. Any solution involving per-canteen geometry beyond O(1) computations is acceptable, but anything involving sorting or pairwise comparisons is unnecessary and would be wasteful. A naive geometric approach is fine only if it reduces to constant time per point.

A subtle edge case comes from correctly handling whether the closest projection lies inside the rectangle interval or outside it. For example, if a point is directly above the rectangle, the closest distance is purely vertical; if it is diagonally above-left, the closest point is the top-left corner and the distance is diagonal. Misclassifying these cases leads to incorrect distance computation.

Another edge case is equality handling. Two canteens can have exactly the same distance due to symmetry, and in that case we must carefully preserve the smallest index, meaning we cannot update the answer unless the new distance is strictly smaller.

## Approaches

The brute-force perspective is straightforward: for each canteen, we consider its distance to every point on the rectangle boundary. Since the rectangle is continuous, this becomes a geometric minimization problem rather than discrete enumeration. One could try sampling edges or breaking the rectangle into segments and computing point-to-segment distances, but that is unnecessary complexity if we recognize the standard closed-form solution for distance from a point to an axis-aligned rectangle.

The key observation is that the rectangle induces independent behavior along x and y axes. For any point (x, y), the closest point on the rectangle is obtained by clamping x into the interval [X1, X2] and y into [Y1, Y2]. This produces the nearest point on or inside the rectangle in Euclidean distance sense. The distance is then computed from the original point to this projected point.

This reduces the problem to a simple per-point computation: construct the nearest point (px, py) where px is x clipped into the rectangle’s x-range and py is y clipped into its y-range, then compute squared Euclidean distance. Squared distance is sufficient since square root is monotonic and unnecessary for comparison.

The brute-force idea would still be O(n) after simplification, but the key improvement is recognizing that the projection is independent per axis and constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Naive geometric boundary search | O(n) with heavy constant or worse | O(1) | Too slow in practice |
| Optimal clamping method | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each canteen independently and maintain the best candidate seen so far.

1. Initialize the answer index as 1 and compute its squared distance to the rectangle. This establishes a baseline that ensures we always have a valid comparison target. The distance is computed using the projection rule described below.
2. For each canteen i from 2 to n, compute its closest point on the rectangle. We do this by clamping its x-coordinate into [X1, X2]. If x is smaller than X1, we use X1; if larger than X2, we use X2; otherwise we keep x unchanged. The same logic applies for y with [Y1, Y2]. This step constructs the geometrically closest feasible point on the rectangle to the given canteen.
3. Compute squared distance between the canteen and its projected point. Squared distance is sufficient because ordering is preserved under monotonic transformation, and avoids floating point precision issues.
4. Compare this distance with the current best distance. If it is strictly smaller, update both the best distance and the best index. If it is equal, do nothing, since the earlier index must be preserved.
5. After processing all canteens, output the stored best index.

Why it works

The closest point on a convex axis-aligned rectangle to an external point is always obtained by independently minimizing horizontal and vertical displacement. Any deviation from the clamped coordinate increases at least one squared component of distance. This ensures the constructed projection is globally optimal for Euclidean distance. Since every canteen is evaluated with this exact optimal projection, the minimum over all candidates is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def clamp(v, lo, hi):
    if v < lo:
        return lo
    if v > hi:
        return hi
    return v

def dist2(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    return dx * dx + dy * dy

def solve():
    n = int(input())
    X1, Y1, X2, Y2 = map(int, input().split())

    best_idx = 1
    x0, y0 = map(int, input().split())

    px = clamp(x0, X1, X2)
    py = clamp(y0, Y1, Y2)
    best_dist = dist2(x0, y0, px, py)

    for i in range(2, n + 1):
        x, y = map(int, input().split())
        px = clamp(x, X1, X2)
        py = clamp(y, Y1, Y2)
        d = dist2(x, y, px, py)

        if d < best_dist:
            best_dist = d
            best_idx = i

    print(best_idx)

if __name__ == "__main__":
    solve()
```

The solution first reads the rectangle and initializes the answer using the first canteen. This avoids special casing inside the loop and ensures comparisons always have a valid baseline.

The clamp function enforces the geometric projection onto the rectangle interval per axis. The dist2 function avoids floating point arithmetic entirely, which is important given coordinate constraints are small but comparisons must be exact.

Tie-breaking is handled implicitly by only updating when a strictly smaller distance is found, preserving the earliest index.

## Worked Examples

Consider the sample input:

| i | (x, y) | projected (px, py) | dist² | best idx |
| --- | --- | --- | --- | --- |
| 1 | (2, 9) | (2, 4) | 25 | 1 |
| 2 | (-4, -4) | (0, 0) | 32 | 1 |
| 3 | (1, -6) | (1, 0) | 36 | 1 |
| 4 | (8, 7) | (4, 4) | 25 | 1 |

Here rectangle is from (0,0) to (4,4). The first and fourth canteens tie with distance squared 25, but index 1 is kept due to tie-breaking rule.

A second example:

Input:

```
1
0 0 10 10
12 5
```

| i | (x, y) | projected (px, py) | dist² | best idx |
| --- | --- | --- | --- | --- |
| 1 | (12, 5) | (10, 5) | 4 | 1 |

This confirms behavior when the point lies directly horizontally aligned with the rectangle, where only one coordinate contributes to the distance.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each canteen requires constant-time clamping and distance computation |
| Space | O(1) | Only a fixed number of variables are stored |

The linear scan over up to 100000 points easily fits within time limits, since each iteration uses only a few arithmetic operations and comparisons.

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

# sample-style test
assert run("""4
0 0 4 4
2 9
-4 -4
1 -6
8 7
""") == "1"

# minimum case
assert run("""1
0 0 1 1
2 2
""") == "1"

# horizontal alignment dominance
assert run("""3
0 0 10 10
5 20
-5 5
15 5
""") == "2"

# diagonal competition
assert run("""2
0 0 10 10
-1 -1
11 11
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point outside | 1 | base case correctness |
| horizontal/vertical dominance | 2 | correct clamping behavior |
| symmetric diagonal points | 1 | tie-breaking by index |

## Edge Cases

A common failure happens when the projection logic is replaced by naive absolute distance to rectangle bounds. For instance, treating distance as min(|x-X1|, |x-X2|) + min(|y-Y1|, |y-Y2|) is incorrect because Euclidean geometry does not separate additively.

Take rectangle [0,0] to [4,4] and point (-3, -3). The correct projection is (0,0) and distance squared is 18. A mistaken formula might incorrectly combine axis distances in a way that underestimates diagonal cost.

The algorithm handles this correctly because both coordinates are clamped independently, producing the true nearest point (0,0). The computed squared distance becomes (−3)^2 + (−3)^2 = 18, matching the true Euclidean minimum over the rectangle.
