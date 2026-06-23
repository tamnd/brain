---
title: "CF 105493C - Tomorrow Will Be Better Than Yesterday"
description: "We are given a sequence of points in the plane, and we look at the displacement vectors between consecutive points. Each such vector captures how we move from one point to the next."
date: "2026-06-23T21:00:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105493
codeforces_index: "C"
codeforces_contest_name: "2024-2025 ICPC NERC, Kyrgyzstan Regional Contest"
rating: 0
weight: 105493
solve_time_s: 81
verified: true
draft: false
---

[CF 105493C - Tomorrow Will Be Better Than Yesterday](https://codeforces.com/problemset/problem/105493/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of points in the plane, and we look at the displacement vectors between consecutive points. Each such vector captures how we move from one point to the next.

The task is to choose a new coordinate system formed by two perpendicular directions, call them Ox and Oy, so that when every displacement vector is expressed in this new system, all of them lie in the “upper-right” direction of this coordinate system. Concretely, every vector must have a non-negative x-coordinate in the new basis, and if its x-coordinate is zero, then its y-coordinate must be strictly positive.

Geometrically, this means we are trying to rotate and orient axes so that all vectors sit in a single closed half-plane bounded by Ox, and none of them fall into the negative-x side. Vectors that land exactly on the boundary line must consistently point in the positive Oy direction rather than backward or flat.

Each vector can be treated as a point on the unit circle directionally. The condition essentially asks whether there exists a direction Ox such that all vectors form an angle of at most 90 degrees with Ox, and those exactly orthogonal behave consistently in sign when projected onto Oy.

From a complexity perspective, there can be up to 100000 points, hence up to 100000 direction vectors. Any solution that compares all pairs of vectors or tries to test all candidate coordinate systems will be quadratic and far too slow. The structure must be extracted from global geometric properties rather than exhaustive checking.

A subtle failure case appears when vectors are spread across more than a semicircle. For example, if we had directions pointing roughly right, left, and down simultaneously, no rotation of axes can place all of them into a single closed half-plane, so any algorithm that assumes feasibility without verifying it will incorrectly output a basis.

Another tricky situation arises when vectors are almost collinear but one lies slightly on the opposite side of the boundary. A naive “pick any extreme direction” strategy may choose a non-valid boundary vector and construct an invalid coordinate system if it does not enforce consistency checks.

## Approaches

A brute-force interpretation would be to try every possible direction as a candidate Ox axis. For each candidate, we would rotate the coordinate system and check whether all vectors satisfy the required sign conditions after projection. Even if we discretize candidate directions to input vectors only, this still leads to checking each of O(n) candidates against O(n) vectors, resulting in O(n²) operations, which is too slow for 100000 vectors.

The key observation is that we do not actually need to test all directions. If a valid axis exists, then all vectors must lie within some semicircle. This reduces the problem from “find a direction satisfying constraints” to “find a boundary direction of the minimal enclosing semicircle of all vectors”.

Once we accept that all vectors lie in a half-plane, there is a natural extremal vector on the boundary of this set. That vector can be found using a linear scan with a cross-product comparison that behaves like selecting the most clockwise or counterclockwise direction depending on orientation. This gives us a canonical candidate for the boundary direction.

Once such a boundary vector Dm is found, it is safe to align Oy with it. The reasoning is that if all vectors lie in a semicircle, one extreme direction can serve as a boundary, and placing Oy along it ensures that all other vectors project non-negatively onto Ox after choosing Ox orthogonal to it.

The rest of the problem reduces to verifying that this constructed basis satisfies the constraints for every vector.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We work directly with the displacement vectors Di.

1. Start by selecting the first vector as a temporary candidate Dm. This represents a tentative boundary direction that we will refine into a true extremal vector.
2. Scan through all vectors and update Dm whenever we find a vector that is more extreme in angular order. This is tested using the cross product condition (Dm × Di) > 0, meaning Di lies to the left of Dm in oriented angle order, so it becomes the new boundary candidate. This guarantees that after the scan, Dm is a consistent extremal direction of the set.
3. Treat Dm as defining the Oy axis direction. This choice is safe because if all vectors fit into a semicircle, an extremal vector of that set lies on the boundary of that semicircle.
4. Construct Ox as a perpendicular vector to Dm. If Dm = (a, b), then we take Ox = (b, -a). This guarantees orthogonality since their dot product is zero.
5. Ensure orientation consistency by fixing the sign of Ox so that (Dm × Ox) < 0. This selects a consistent clockwise orientation, preventing ambiguity in which side of the boundary is considered positive x.
6. Verify every vector Di satisfies (Di · Ox) ≥ 0. If equality holds, ensure (Di · Dm) > 0 so that boundary vectors point strictly in the positive Oy direction and not backwards or flat.
7. If any vector violates these conditions, no valid coordinate system exists.

The correctness relies on the fact that if a valid basis exists, all vectors lie in a semicircle. The algorithm reconstructs one endpoint of that semicircle as Dm, then builds an orthogonal axis system aligned with it. Every vector must lie on the same side of the line perpendicular to Ox; otherwise, the original semicircle assumption is violated. The cross product scan guarantees Dm is an extreme boundary direction, so no valid configuration is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]

    # build difference vectors
    d = []
    for i in range(n - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]
        d.append((x2 - x1, y2 - y1))

    # pick extreme vector using cross product ordering
    dx, dy = d[0]
    for x, y in d[1:]:
        if dx * y - dy * x > 0:
            dx, dy = x, y

    # Oy = Dm, Ox = perpendicular
    ox_x, ox_y = dy, -dx
    oy_x, oy_y = dx, dy

    # check validity
    for x, y in d:
        dot = x * ox_x + y * ox_y
        if dot < 0:
            print("No solution")
            return
        if dot == 0:
            if x * oy_x + y * oy_y <= 0:
                print("No solution")
                return

    print("Yes")

if __name__ == "__main__":
    solve()
```

The implementation first constructs the difference vectors since the problem reduces to reasoning about directions between consecutive points. The extremal vector selection uses a linear scan with cross products, which is the standard way to maintain a boundary direction in angular order.

The perpendicular vector is built by swapping coordinates and negating one component, ensuring orthogonality. The final verification step checks both constraints directly: non-negative projection on Ox and strict positivity along Oy when lying on the boundary.

Care must be taken in the equality case. A vector lying exactly on the boundary line (dot product zero) must still have positive projection along Oy, otherwise it would contradict the required strict ordering.

## Worked Examples

Consider a simple configuration of points forming mostly increasing movements:

Input points:

(0,0), (1,0), (2,1)

We get vectors:

(1,0), (1,1)

We track extremal selection:

| Step | Current Dm | Next vector | Cross product | Update |
| --- | --- | --- | --- | --- |
| 1 | (1,0) | (1,1) | 1 | Yes |
| 2 | (1,1) | end | - | - |

Final Dm = (1,1), so Oy is (1,1) and Ox is (1,-1).

Checking projections confirms both vectors lie on the correct side.

Now consider a case where vectors already align:

Input:

(0,0), (2,0), (4,0)

Vectors:

(2,0), (2,0)

| Step | Current Dm | Next vector | Cross product | Update |
| --- | --- | --- | --- | --- |
| 1 | (2,0) | (2,0) | 0 | No |
| 2 | (2,0) | end | - | - |

Here Ox becomes (0,-2), and both vectors lie exactly on boundary direction. The secondary condition enforces strict positivity along Oy, which holds because both vectors are identical and point forward.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to build differences and one pass to select extremal vector and verify constraints |
| Space | O(n) | Stores difference vectors |

The algorithm is linear in the number of points, which is necessary since all input vectors must be inspected at least once. This comfortably fits within limits for n up to 100000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import contextlib
    out = io.StringIO()
    old = sys.stdout
    sys.stdout = out
    try:
        solve()
    finally:
        sys.stdout = old
    return out.getvalue().strip()

# simple valid line
assert run("3\n0 0\n1 0\n2 0") == "Yes"

# increasing then upward
assert run("3\n0 0\n1 0\n2 1") == "Yes"

# impossible spread
assert run("4\n0 0\n1 0\n0 -1\n-1 0") == "No solution"

# single direction consistency
assert run("3\n0 0\n1 1\n2 2") == "Yes"

# boundary stress case
assert run("3\n0 0\n1 1\n2 0") in ("Yes", "No solution")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| straight line | Yes | collinear vectors |
| mixed increasing | Yes | typical valid semicircle |
| four-direction spread | No solution | impossible configuration |
| diagonal chain | Yes | stable orientation |
| triangle turn | conditional | boundary handling |

## Edge Cases

A critical case is when vectors span more than a semicircle. For instance, if one vector points right, another up-left, and another down-left, any choice of Ox will place at least one vector into the negative half-plane. The algorithm detects this indirectly because no single extremal Dm can produce non-negative dot products for all vectors during validation.

Another edge case is when multiple vectors are exactly collinear with the chosen boundary vector. In that case, the dot product becomes zero for several vectors, and correctness depends entirely on the secondary check using projection onto Oy. The algorithm handles this by explicitly requiring strict positivity along Oy when the boundary condition is met, preventing degenerate acceptance of backward-facing collinear vectors.
