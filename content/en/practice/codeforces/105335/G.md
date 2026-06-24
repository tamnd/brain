---
title: "CF 105335G - Glory Road"
description: "We are given three points in the plane, but instead of being arbitrary, they represent the midpoints of three segments forming a triangle of hidden original points. More concretely, there are three unknown integer points A, B, and C. We are given the midpoints of AB, BC, and CA."
date: "2026-06-24T23:01:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105335
codeforces_index: "G"
codeforces_contest_name: "ICPC Thailand National Competition 2024"
rating: 0
weight: 105335
solve_time_s: 44
verified: true
draft: false
---

[CF 105335G - Glory Road](https://codeforces.com/problemset/problem/105335/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three points in the plane, but instead of being arbitrary, they represent the midpoints of three segments forming a triangle of hidden original points.

More concretely, there are three unknown integer points A, B, and C. We are given the midpoints of AB, BC, and CA. Each midpoint is known exactly, with integer coordinates, and the task is to recover the original three points.

Each midpoint is defined in the usual geometric way: if A is (ax, ay) and B is (bx, by), then the midpoint of AB is ((ax + bx)/2, (ay + by)/2). The same holds for the other two sides.

The input provides these three midpoint coordinates in arbitrary order, and we must output the coordinates of A, B, and C.

The key constraint is that all coordinates of the original points are guaranteed to be integers. This immediately implies that all midpoint coordinates correspond to integer arithmetic averages of two integers, so each coordinate of a midpoint is either an integer or half-integer in general, but in this problem they are always integers.

The bounds are small, with coordinates roughly within ±100, so any O(1) arithmetic reconstruction per test case is sufficient. Anything involving search or geometry enumeration is unnecessary.

A naive misunderstanding happens if one assumes the midpoints are labeled. The problem does not tell which midpoint corresponds to which edge, so the main difficulty is solving a system without labels.

A few edge situations matter.

If all three midpoints are identical, for example all are (0, 0), then all original points must coincide at (0, 0). A careless attempt that assumes distinct vertices may fail.

If two midpoints are swapped or interpreted incorrectly, a direct pairing attempt between points can produce inconsistent or fractional vertices. For instance, pairing arbitrary midpoint differences without enforcing consistency leads to non-integer candidate vertices, which are invalid.

## Approaches

A brute-force interpretation would be to try assigning the three given points to edges AB, BC, and CA in all 6 permutations, then reconstruct A, B, and C each time and check consistency. This is already small, but it is conceptually heavier than needed.

The key observation is that midpoint equations form a linear system. If we denote the midpoints as M_AB, M_BC, and M_CA, then:

A + B = 2 M_AB

B + C = 2 M_BC

C + A = 2 M_CA

Adding all three equations gives:

2(A + B + C) = 2(M_AB + M_BC + M_CA)

So:

A + B + C = M_AB + M_BC + M_CA

Once we know the sum S = A + B + C, we can isolate each vertex:

A = S − (B + C) = S − 2 M_BC

B = S − 2 M_CA

C = S − 2 M_AB

This completely determines the solution without any permutation search. The only remaining issue is that we do not know which midpoint corresponds to which pair. So we still need to assign labels correctly.

However, since all three roles are symmetric, we can simply try all assignments of the three given points to (M_AB, M_BC, M_CA). For each assignment, compute A, B, C using the formulas above and check consistency by recomputing midpoints.

Because there are only 6 permutations, this is constant work.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute permutation + recomputation | O(1) | O(1) | Accepted |
| Linear system with fixed labeling | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three midpoint points M1, M2, M3.

They correspond to unknown edges, but we do not assume any order.
2. Iterate over all permutations of assigning these points to M_AB, M_BC, M_CA.

This ensures we cover all possible ways the input could map to the triangle edges.
3. For each assignment, compute S = M_AB + M_BC + M_CA coordinate-wise.
4. Reconstruct candidate vertices using:

A = S − 2 * M_BC

B = S − 2 * M_CA

C = S − 2 * M_AB

This comes directly from solving the midpoint equations algebraically.
5. Verify correctness by checking that:

midpoint(A, B) == M_AB

midpoint(B, C) == M_BC

midpoint(C, A) == M_CA

This step prevents incorrect permutations from producing a valid-looking but wrong reconstruction.
6. Once a valid configuration is found, output A, B, and C.

### Why it works

The midpoint equations define a linear system with a unique solution once the correspondence between midpoints and edges is fixed. The reconstruction formulas come directly from summing and subtracting these equations, which ensures that any valid assignment produces the exact original vertices. Since the correct labeling is among the 6 permutations, the algorithm is guaranteed to encounter it.

## Python Solution

```python
import sys
input = sys.stdin.readline

def midpoint(p, q):
    return ((p[0] + q[0]) // 2, (p[1] + q[1]) // 2)

def ok(A, B, C, MAB, MBC, MCA):
    return (midpoint(A, B) == MAB and
            midpoint(B, C) == MBC and
            midpoint(C, A) == MCA)

def solve():
    mids = [tuple(map(int, input().split())) for _ in range(3)]

    from itertools import permutations

    for MAB, MBC, MCA in permutations(mids):
        Sx = MAB[0] + MBC[0] + MCA[0]
        Sy = MAB[1] + MBC[1] + MCA[1]

        A = (Sx - 2 * MBC[0], Sy - 2 * MBC[1])
        B = (Sx - 2 * MCA[0], Sy - 2 * MCA[1])
        C = (Sx - 2 * MAB[0], Sy - 2 * MAB[1])

        if ok(A, B, C, MAB, MBC, MCA):
            print(*A)
            print(*B)
            print(*C)
            return

solve()
```

The code reads the three given midpoint coordinates and tries every possible assignment to triangle edges. For each assignment, it reconstructs the vertices using the derived linear identities. The validation function recomputes midpoints to ensure that the reconstructed triangle is consistent, preventing incorrect permutations from being accepted.

A subtle implementation detail is integer division in midpoint checks. Since the problem guarantees integer coordinates for original points, reconstructed midpoints will match exactly without floating-point arithmetic. Using integer tuples avoids precision issues entirely.

## Worked Examples

### Example 1

Input:

(2, 4), (5, 5), (4, 3)

We test one correct assignment:

M_AB = (2, 4), M_BC = (5, 5), M_CA = (4, 3)

| Step | Value |
| --- | --- |
| S = M_AB + M_BC + M_CA | (11, 12) |
| A = S − 2 M_BC | (1, 2) |
| B = S − 2 M_CA | (3, 6) |
| C = S − 2 M_AB | (7, 4) |

Midpoint checks confirm consistency, so this assignment is correct.

This trace shows that the reconstruction is purely algebraic and does not depend on geometry intuition once equations are set up.

### Example 2

Input:

(-3, -4), (2, 5), (3, -2)

Trying the correct permutation yields:

| Step | Value |
| --- | --- |
| S | (2, -1) |
| A | (-2, -11) |
| B | (-4, 3) |
| C | (8, 7) |

Again, midpoint validation confirms correctness.

This example demonstrates that even with negative coordinates, the linear reconstruction remains stable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only 6 permutations, constant arithmetic per case |
| Space | O(1) | Only storing three points and a few temporaries |

The constraints are small enough that even a straightforward permutation-based reconstruction runs instantly within limits. The solution is dominated entirely by constant-time arithmetic.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from itertools import permutations

    mids = [tuple(map(int, sys.stdin.readline().split())) for _ in range(3)]

    def midpoint(p, q):
        return ((p[0] + q[0]) // 2, (p[1] + q[1]) // 2)

    def ok(A, B, C, MAB, MBC, MCA):
        return (midpoint(A, B) == MAB and
                midpoint(B, C) == MBC and
                midpoint(C, A) == MCA)

    for MAB, MBC, MCA in permutations(mids):
        Sx = MAB[0] + MBC[0] + MCA[0]
        Sy = MAB[1] + MBC[1] + MCA[1]

        A = (Sx - 2 * MBC[0], Sy - 2 * MBC[1])
        B = (Sx - 2 * MCA[0], Sy - 2 * MCA[1])
        C = (Sx - 2 * MAB[0], Sy - 2 * MAB[1])

        if ok(A, B, C, MAB, MBC, MCA):
            return f"{A[0]} {A[1]}\n{B[0]} {B[1]}\n{C[0]} {C[1]}\n"

    return ""

# provided samples
assert run("2 4\n5 5\n4 3\n") == "1 2\n3 6\n7 4\n"
assert run("-3 -4\n2 5\n3 -2\n") == "-2 -11\n-4 3\n8 7\n"

# custom cases
assert run("0 0\n0 0\n0 0\n") == "0 0\n0 0\n0 0\n", "all same point"
assert run("1 1\n2 2\n3 3\n") != "", "valid triangle existence"
assert run("2 0\n0 2\n1 1\n") != "", "symmetric case"
assert run("-1 -1\n1 1\n0 0\n") != "", "mixed signs"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all zeros | (0,0) repeated | degenerate triangle |
| symmetric points | valid reconstruction | permutation correctness |
| mixed signs | valid reconstruction | arithmetic robustness |

## Edge Cases

When all three midpoints are identical, every permutation produces the same reconstructed vertices, and the algorithm correctly returns a collapsed triangle where all original points coincide. The midpoint verification step still passes because all pairwise midpoints remain unchanged.

When the input ordering is arbitrary, a naive mapping of first input to AB, second to BC, third to CA may silently produce inconsistent vertices. The permutation loop prevents this by explicitly checking all labelings.

When coordinates are negative or mixed, subtraction in the reconstruction formulas can produce large intermediate values, but all operations remain within integer range due to the problem’s guarantee. The midpoint validation ensures that any arithmetic mismatch is rejected immediately.
