---
title: "CF 105962D - MA141"
description: "We are given four points in the plane in a fixed order, A, B, C, D. The task is to determine whether connecting them in that order, including the edge from D back to A, forms a geometric square. This is not a “set of four points” problem where we can reorder arbitrarily."
date: "2026-06-22T16:15:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105962
codeforces_index: "D"
codeforces_contest_name: "UNICAMP Freshman Contest 2025"
rating: 0
weight: 105962
solve_time_s: 60
verified: true
draft: false
---

[CF 105962D - MA141](https://codeforces.com/problemset/problem/105962/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given four points in the plane in a fixed order, A, B, C, D. The task is to determine whether connecting them in that order, including the edge from D back to A, forms a geometric square.

This is not a “set of four points” problem where we can reorder arbitrarily. The order matters because the edges are explicitly AB, BC, CD, and DA. So we are checking whether this exact cycle describes a square.

Each point has integer coordinates bounded within a moderate range, so all geometric computations can safely be done using integers. Since coordinates are up to 10^4 in magnitude, squared distances fit comfortably in 64-bit integers, and we never need floating point arithmetic.

A naive mistake would be to treat the four points as an unordered set and try to guess a square by sorting distances or angles. That fails because a valid square depends on the cyclic order. For example, the same four points can form a square if ordered correctly, but become a self-intersecting shape or a non-square quadrilateral if permuted.

Another common pitfall is relying on floating point geometry, especially angle comparisons. That is unnecessary and risky due to precision errors. Everything can be expressed exactly using dot products and squared lengths.

A subtle edge case is when the points form a rhombus that is not a square. All sides can be equal, but angles are not 90 degrees. Another is a rectangle that is not a square, where opposite sides are equal but adjacent sides differ. Both must be rejected.

## Approaches

The brute-force idea would be to consider all permutations of the four points, interpret them as a cycle, and test whether any ordering forms a square. For each permutation, we would compute all four side lengths and angles. Since there are 4! = 24 permutations, this is constant work per test case, and still feasible.

However, that approach is conceptually wasteful because the problem already fixes the order. We are not allowed to rearrange points; we must validate the given cycle directly.

The key observation is that a quadrilateral is a square if and only if two conditions hold: all four sides are equal, and at least one angle is a right angle. In vector terms, if AB, BC, CD, DA are edges, then we require equal squared lengths and orthogonality between adjacent edges.

This reduces the entire problem to computing four vectors, four squared lengths, and a few dot products.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Permutation brute force | O(1) | O(1) | Accepted but unnecessary |
| Geometric check (optimal) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We work directly with vectors formed by consecutive points.

1. Construct the four edge vectors AB, BC, CD, and DA. Each vector is computed by subtracting coordinates, for example AB = B − A. This encodes direction and length in a form suitable for integer arithmetic.
2. Compute squared lengths of all four edges. Squared length avoids square roots and keeps everything exact, since comparing lengths only requires equality.
3. Verify that all four squared lengths are equal. If any edge differs, the shape cannot be a square because a square has four congruent sides.
4. Pick one vertex, for example point B, and compute the dot product of adjacent edges AB and BC. The dot product being zero is equivalent to a 90 degree angle at B.
5. Check that AB and BC are perpendicular. If not, the figure is not a square even if all sides are equal, since it would only be a rhombus.
6. If both conditions hold, output “SIM”, otherwise output “NAO”.

The reasoning behind checking only one angle is that in a quadrilateral with all sides equal, having one right angle forces all angles to be right angles, which fully characterizes a square.

### Why it works

The algorithm enforces that all sides are congruent, which restricts the shape to a rhombus. In a rhombus, all vertices are symmetric under rotation by 180 degrees, and all angles are equal in pairs. If one angle is 90 degrees, all must be 90 degrees, turning the rhombus into a square. Thus, equal side lengths plus a single orthogonal adjacency condition is sufficient to guarantee the full square structure, and the fixed ordering ensures we are validating the correct cycle rather than searching for one.

## Python Solution

```python
import sys
input = sys.stdin.readline

def sq_len(ax, ay, bx, by):
    dx = bx - ax
    dy = by - ay
    return dx * dx + dy * dy

def dot(ax, ay, bx, by, cx, cy):
    # AB · BC where A->B->C
    return (bx - ax) * (cx - bx) + (by - ay) * (cy - by)

def solve():
    pts = [tuple(map(int, input().split())) for _ in range(4)]
    A, B, C, D = pts

    ax, ay = A
    bx, by = B
    cx, cy = C
    dx, dy = D

    d1 = sq_len(ax, ay, bx, by)
    d2 = sq_len(bx, by, cx, cy)
    d3 = sq_len(cx, cy, dx, dy)
    d4 = sq_len(dx, dy, ax, ay)

    if not (d1 == d2 == d3 == d4):
        print("NAO")
        return

    if dot(ax, ay, bx, by, cx, cy) != 0:
        print("NAO")
        return

    print("SIM")

if __name__ == "__main__":
    solve()
```

The implementation first loads the four points and computes squared distances for each consecutive edge in the given order. The equality check ensures we are dealing with a rhombus candidate. The dot product test at vertex B enforces a right angle between AB and BC. We do not need to explicitly check other angles or diagonal properties because those are implied by the combination of equal sides and one orthogonal corner in a closed cycle.

All computations are integer-only, avoiding precision issues entirely.

## Worked Examples

### Example 1

Input:

```
0 0
0 1
1 1
1 0
```

| Step | AB² | BC² | CD² | DA² | AB·BC | Result |
| --- | --- | --- | --- | --- | --- | --- |
| Compute edges | 1 | 1 | 1 | 1 | -1 | continue |
| Side equality | equal | equal | equal | equal | - | pass |
| Right angle test | - | - | - | - | 0 | SIM |

This is the standard axis-aligned square. All sides are equal and the angle at B is 90 degrees, so the algorithm accepts it.

### Example 2

Input:

```
0 0
0 1
1 2
1 1
```

| Step | AB² | BC² | CD² | DA² | AB·BC | Result |
| --- | --- | --- | --- | --- | --- | --- |
| Compute edges | 1 | 2 | 1 | 2 | -1 | fail |
| Side equality | not equal |  |  |  |  | NAO |

Here, the shape resembles a skewed quadrilateral. Even without checking angles, unequal side lengths immediately reject it.

The trace shows that side-length equality is the dominant filter, preventing unnecessary angle computation in invalid cases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations on four points |
| Space | O(1) | Constant storage for coordinates and intermediate values |

The constraints are small enough that even a heavier geometric approach would pass easily, but this solution is optimal in both simplicity and execution cost.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import isclose

    # re-run solution inline
    input = sys.stdin.readline

    def sq_len(ax, ay, bx, by):
        dx = bx - ax
        dy = by - ay
        return dx * dx + dy * dy

    def dot(ax, ay, bx, by, cx, cy):
        return (bx - ax) * (cx - bx) + (by - ay) * (cy - by)

    pts = [tuple(map(int, input().split())) for _ in range(4)]
    A, B, C, D = pts
    ax, ay = A
    bx, by = B
    cx, cy = C
    dx, dy = D

    d1 = sq_len(ax, ay, bx, by)
    d2 = sq_len(bx, by, cx, cy)
    d3 = sq_len(cx, cy, dx, dy)
    d4 = sq_len(dx, dy, ax, ay)

    if not (d1 == d2 == d3 == d4):
        return "NAO\n"

    if dot(ax, ay, bx, by, cx, cy) != 0:
        return "NAO\n"

    return "SIM\n"

# provided samples
assert run("0 0\n0 1\n1 1\n1 0\n") == "SIM\n"
assert run("0 0\n0 1\n1 2\n1 1\n") == "NAO\n"

# custom cases
assert run("1 0\n2 1\n1 2\n0 1\n") == "SIM\n", "rotated square"
assert run("0 0\n1 0\n2 1\n1 1\n") == "NAO\n", "rectangle not square"
assert run("0 0\n1 1\n2 2\n3 3\n") == "NAO\n", "collinear points"
assert run("0 0\n0 2\n2 2\n2 0\n") == "SIM\n", "axis aligned square"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| rotated square | SIM | non-axis aligned square |
| rectangle not square | NAO | unequal adjacent sides |
| collinear points | NAO | degeneracy rejection |
| axis aligned square | SIM | standard configuration |

## Edge Cases

One important edge case is when the square is rotated. For input such as (1,0), (2,1), (1,2), (0,1), the algorithm still computes equal squared lengths and a zero dot product at the second point, so it correctly returns “SIM”. This confirms that the method is rotation invariant.

Another case is when points form a rectangle that is not a square, such as (0,0), (1,0), (2,1), (1,1). Here side lengths differ immediately, so the algorithm rejects it without needing angle checks.

A degenerate-looking case is collinear or near-collinear ordering like (0,0), (1,1), (2,2), (3,3). Even though distances may show partial symmetry, at least one side comparison fails or the dot product is non-zero, ensuring rejection.
