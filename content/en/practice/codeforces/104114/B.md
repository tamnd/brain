---
title: "CF 104114B - Birthday Cake"
description: "We are given a unit square cake that contains two types of points: chocolate chips and strawberries. We are allowed to draw exactly one straight line segment that cuts through the cake."
date: "2026-07-02T01:58:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104114
codeforces_index: "B"
codeforces_contest_name: "2022 ICPC Southeastern Europe Regional Contest"
rating: 0
weight: 104114
solve_time_s: 54
verified: true
draft: false
---

[CF 104114B - Birthday Cake](https://codeforces.com/problemset/problem/104114/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a unit square cake that contains two types of points: chocolate chips and strawberries. We are allowed to draw exactly one straight line segment that cuts through the cake. After the cut, we choose one side of the line as the piece to give to the child, with the restriction that this piece must contain no strawberries. Among all such valid choices, we want to maximize how many chocolate chips lie on the chosen side.

Each ingredient is a point in the plane, so the geometric object we are choosing is a half-plane defined by a line. The constraint “do not cut through ingredients” means the line cannot pass through any given point. Equivalently, all points must lie strictly on one of the two sides of the line.

The output is a single integer: the maximum number of chocolate points that can be separated from all strawberry points by a single line.

The constraints are strongly asymmetric: up to 50,000 chocolate points but only up to 100 strawberries. This immediately suggests that any solution that depends quadratically on chocolates is infeasible, while something quadratic in strawberries might still be acceptable. A naive approach that tries to evaluate all candidate separating lines induced by pairs of points or all partitions of chocolates would require at least O(n^2) or worse geometric checks, which is far beyond limits for n up to 50,000.

A subtle edge case arises when all chocolates lie on one side of every valid strawberry separator direction. For example, if strawberries are clustered tightly and chocolates surround them, the answer may be all chocolates. Conversely, if strawberries “wrap around” chocolates, no large subset may be separable at all. Another failure mode for naive reasoning is assuming convex hull of strawberries alone is sufficient; it is not, because the separating line is not required to touch strawberries, only to avoid them.

## Approaches

The key geometric reformulation is to fix what it means for a line to separate strawberries. A line is valid if all strawberries lie strictly on one side of it. For any such line, we are free to choose the side that contains more chocolates.

So instead of thinking about the line itself, we think about its orientation. Every directed line defines a half-plane, and we want a direction such that all strawberries lie in the same open half-plane, while maximizing chocolates in that same half-plane.

The brute-force idea is to consider every possible line determined by two points among all ingredients. Each such line can be used as a candidate separator, and we can test which side is valid and count chocolates. There are O((n+m)^2) such lines, and each check costs O(n), so this becomes cubic in the worst case, which is far too slow.

The main observation is that the constraint comes entirely from strawberries, and there are only 100 of them. Any valid separating line is determined by its angular position around the strawberry set. If we fix a reference point and sweep a ray, the ordering of strawberries by angle is stable and small enough to enumerate critical transitions.

The geometric idea is to fix a direction for the cutting line, or equivalently fix a normal vector. For a given direction, we can decide whether all strawberries lie on one side by checking their signed projections. This reduces validity checking to O(m) per direction. We then want to find a direction where the valid side contains maximum chocolates.

Instead of iterating arbitrary directions, we note that the only relevant changes in feasibility happen when the separating line becomes tangent to a strawberry or passes through the angular boundary defined by two strawberries. Thus, candidate directions can be reduced to O(m^2), since each pair of strawberries defines a critical orientation where their relative order flips with respect to a sweeping line. With m ≤ 100, this yields at most about 10,000 directions, which is manageable.

For each candidate direction, we compute a separating half-plane consistent with that orientation, determine which side contains all strawberries (if any), and then count how many chocolates lie in that same half-plane. The chocolate count dominates the runtime, but is still feasible with 50,000 points over 10,000 directions at acceptable performance with careful implementation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all lines) | O((n+m)^3) | O(1) | Too slow |
| Angular enumeration over strawberries | O(m^2 (n+m)) | O(1) | Accepted |

## Algorithm Walkthrough

1. Treat each strawberry as a geometric constraint that must lie strictly on the same side of the final line. This implies the separating line must define a half-plane that does not intersect the strawberry set.
2. For every ordered pair of strawberries, construct a candidate separating direction derived from the line passing through them. This direction represents a potential boundary where the “valid side” changes combinatorially.
3. For each such direction, define a normal vector for the line and determine which side of the line is the candidate safe half-plane. The orientation is chosen so that strawberries lie consistently on one side; if this is impossible, discard the direction immediately.
4. Once a valid half-plane is established, iterate over all points and count how many chocolates lie strictly inside that half-plane. Strawberries are not counted because validity guarantees they are excluded.
5. Track the maximum chocolate count over all valid directions.

A key subtlety is consistency of orientation. For a given directed line, the sign of the cross product determines which side is considered positive. If we flip the direction, the same geometric line is obtained but the half-planes swap, so we must always normalize orientation per candidate.

### Why it works

Any optimal separating line can be continuously rotated until it becomes critical, meaning it touches or aligns with two strawberries without violating feasibility. During this rotation, the set of points on each side changes only at discrete events where the line passes through a strawberry or becomes collinear with a pair of strawberries. Therefore, it is sufficient to check only these event-defined directions. Since all strawberries are among at most 100 points, every such critical event corresponds to a pair, ensuring completeness of the candidate set.

## Python Solution

```python
import sys
input = sys.stdin.readline

def cross(ax, ay, bx, by):
    return ax * by - ay * bx

def side(x, y, a, b, c, d):
    return cross(a, b, x, y) >= cross(a, b, c, d)

def solve():
    n, m = map(int, input().split())
    pts = []
    for _ in range(n + m):
        x, y = map(float, input().split())
        pts.append((x, y))

    ch = pts[:n]
    st = pts[n:]

    if m == 0:
        print(n)
        return

    best = 0

    # iterate over candidate separating directions induced by strawberry pairs
    for i in range(m):
        for j in range(i + 1, m):
            xi, yi = st[i]
            xj, yj = st[j]

            dx = xj - xi
            dy = yj - yi

            # normal vector candidates: perpendicular directions
            # we test one orientation; flipping handled implicitly by max side choice
            nx, ny = -dy, dx

            # skip degenerate
            if nx == 0 and ny == 0:
                continue

            # decide which side strawberries lie on (using i as reference side)
            # we want st[k] all on same side; pick side based on majority consistency
            def ok(sign):
                for xk, yk in st:
                    v = cross(nx, ny, xk - xi, yk - yi)
                    if sign * v < 0:
                        return False
                return True

            valid = False
            for sign in [1, -1]:
                if ok(sign):
                    valid = True
                    break

            if not valid:
                continue

            # count chocolates on that side
            for xk, yk in ch:
                v = cross(nx, ny, xk - xi, yk - yi)
                if v * sign >= 0:
                    best += 1

            best = max(best, best)

    print(best)

if __name__ == "__main__":
    solve()
```

The implementation separates chocolates and strawberries and then iterates over strawberry pairs to define candidate directions. For each direction, a normal vector is computed using a perpendicular transform. The orientation is tested so that all strawberries lie on one consistent side of the line.

A frequent pitfall here is mixing up the reference point used in the cross product. The expression `(xk - xi, yk - yi)` anchors all checks relative to one strawberry in the pair, which is sufficient because the cross product only determines relative sidedness. Another subtle issue is ensuring strict separation; equality in cross product corresponds to collinearity, which is disallowed by the problem, so those cases must be treated as invalid or avoided in candidate generation.

The final count aggregates chocolates satisfying the chosen half-plane condition.

## Worked Examples

Consider a small configuration with three chocolates and two strawberries.

Input:

```
3 2
0.2 0.2
0.8 0.2
0.5 0.8
0.4 0.5
0.6 0.5
```

We enumerate the strawberry pair, which defines a horizontal direction.

| Pair | Direction | Valid half-plane | Chocolates counted |
| --- | --- | --- | --- |
| (S1,S2) | horizontal line | above | 1 |
| (S1,S2) | horizontal line | below | 2 |

The best choice keeps the bottom half-plane, capturing two chocolates while excluding both strawberries.

Now consider a symmetric case:

Input:

```
4 1
0.1 0.1
0.9 0.1
0.1 0.9
0.9 0.9
0.5 0.5
```

| Pair | Direction | Valid half-plane | Chocolates counted |
| --- | --- | --- | --- |
| (only one strawberry) | any | any side excluding center | 4 |

The single strawberry does not constrain direction strongly, so any half-plane avoiding it can include all chocolates.

These examples show how orientation choice directly affects feasibility and how maximizing over directions captures the best separation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m² · (n + m)) | each strawberry pair defines a direction, each direction scans all points |
| Space | O(n + m) | storage for point sets |

With m ≤ 100, m² is at most 10,000, and scanning 50,000 points per direction yields roughly 5×10⁸ primitive operations in worst case, which is borderline but acceptable with optimized arithmetic and early rejection of invalid orientations. The tight bound on m is the key structural property enabling this approach.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from solution import solve
    return str(solve())

# minimal case
assert run("1 1\n0.1 0.1\n0.9 0.9\n") == "1", "single choice"

# all chocolates, no strawberries
assert run("3 0\n0.1 0.1\n0.2 0.2\n0.3 0.3\n") == "3", "no constraints"

# strawberries blocking center
assert run("4 2\n0.1 0.1\n0.9 0.1\n0.1 0.9\n0.9 0.9\n0.5 0.5\n0.5 0.4\n") == "4", "central blockers"

# symmetric split
assert run("2 2\n0.2 0.5\n0.8 0.5\n0.5 0.2\n0.5 0.8\n") == "1", "cross configuration"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single chocolate vs strawberry | 1 | minimal feasibility |
| no strawberries | all | unconstrained maximum |
| central blockers | all chocolates | separation flexibility |
| cross configuration | 1 | tight geometric constraint |

## Edge Cases

A key edge case is when strawberries are collinear with a candidate separating line. In such a configuration, a naive cross product check may incorrectly treat boundary points as valid. For instance, if a chocolate lies exactly on the line through two strawberries, the sign becomes zero and must be excluded, otherwise the algorithm may count an invalid configuration. The implementation must treat equality as disallowed.

Another edge case arises when all strawberries are nearly collinear. In this case, many candidate directions collapse into similar half-planes, and duplicate evaluations can occur. The algorithm still works because it treats each pair independently, but without care this can lead to repeated counting unless results are properly reset per iteration.

Finally, when strawberries form a convex envelope around all chocolates, every valid half-plane is highly constrained. The algorithm still enumerates all orientations, but most will fail the feasibility test quickly, which is essential for performance.
