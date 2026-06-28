---
title: "CF 104819C - Triangle"
description: "We are given a collection of identical right triangles with side lengths 3, 4, and 5. Each triangle is a rigid tile, and we are allowed to place multiple copies on a plane without overlap."
date: "2026-06-28T13:00:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104819
codeforces_index: "C"
codeforces_contest_name: "2023 Sun Yat-sen University Collegiate Programming Contest, Onsite"
rating: 0
weight: 104819
solve_time_s: 52
verified: true
draft: false
---

[CF 104819C - Triangle](https://codeforces.com/problemset/problem/104819/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of identical right triangles with side lengths 3, 4, and 5. Each triangle is a rigid tile, and we are allowed to place multiple copies on a plane without overlap. The goal is to determine whether it is possible to arrange all $n$ triangles into a single shape that has an axis of symmetry, meaning the final union of all triangles can be reflected across some straight line and match itself exactly.

The input consists only of $n$, the number of available triangles. We must answer whether a valid symmetric arrangement exists that uses every triangle exactly once.

The constraint $n \le 10^9$ immediately removes any approach that tries to construct or simulate geometry explicitly. Any solution must depend on structural properties of how these triangles can combine, not on enumeration. A linear scan, a DP over placements, or any geometric construction per triangle is infeasible because even $O(n)$ operations is already too large at the upper bound.

A subtle edge case arises from what “axisymmetric shape” enforces. A single triangle already breaks reflection symmetry because a 3-4-5 right triangle has no line that maps it onto itself. So for $n = 1$, the answer must be NO. On the other hand, two triangles can potentially form a symmetric structure if they are arranged as mirror images. Any approach that only checks area divisibility or ignores symmetry requirements would incorrectly claim that all $n$ are valid because area is always divisible and there are no packing constraints in the statement.

## Approaches

A naive way to think about the problem is to imagine placing triangles one by one and trying all possible orientations and positions while maintaining a global symmetry condition. Each new triangle could either lie on the symmetry axis or be paired with a mirrored counterpart. This quickly turns into an exponential search over placements, since after placing a few triangles the number of geometric configurations grows combinatorially. Even if we discretize possible placements, the search space grows far beyond feasible limits.

The key observation is that symmetry imposes a global pairing constraint. Every triangle that is not exactly on the symmetry axis must have a mirrored partner. Since all triangles are congruent and have no internal symmetry, none of them can sit alone on the axis without breaking shape consistency. This means every triangle must be part of a mirrored pair.

That immediately reduces the problem to a parity condition. If $n$ is even, we can pair triangles arbitrarily and place each pair as two mirrored copies forming a symmetric unit. A concrete construction exists: two 3-4-5 triangles can always be arranged to form a 3 by 4 rectangle, which is symmetric with respect to both its midlines. Repeating such paired blocks yields a globally symmetric shape.

If $n$ is odd, one triangle will always remain unpaired. That leftover triangle cannot be placed on the symmetry axis without breaking mirror equivalence, since it has no reflective symmetry itself. Hence any odd $n$ is impossible.

The brute-force exploration becomes unnecessary once we recognize that the entire geometric complexity collapses into whether we can perfectly pair the triangles.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force geometric placement search | Exponential | Exponential | Too slow |
| Parity observation (pairing symmetry argument) | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the integer $n$. This is the number of identical right triangles available for construction.
2. Check whether $n$ is divisible by 2. This condition tests whether we can partition all triangles into mirrored pairs, which is required by axis symmetry.
3. If $n \% 2 = 0$, output YES. This corresponds to pairing every triangle with another triangle and arranging each pair symmetrically in the plane.
4. Otherwise output NO, since at least one triangle would remain without a mirror partner, making global symmetry impossible.

### Why it works

The invariant is that any valid axisymmetric arrangement partitions all tiles into orbits under reflection: each orbit has either size 2 (a pair of mirrored triangles) or size 1 (a triangle lying exactly on the axis). Because a 3-4-5 triangle has no reflective symmetry, it cannot form a valid size-1 orbit that preserves the shape under reflection. Therefore every orbit must have size 2, forcing the total number of triangles to be even. This invariant fully characterizes feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())

if n % 2 == 0:
    print("YES")
else:
    print("NO")
```

The implementation directly applies the parity condition derived above. No geometric simulation is required. The only subtlety is ensuring correct input parsing for a single integer and performing a constant-time modulus check.

The decision does not depend on triangle geometry explicitly in code because that complexity has already been reduced into the pairing constraint.

## Worked Examples

### Example 1

Input:

```
1
```

| Step | n | n % 2 | Decision |
| --- | --- | --- | --- |
| Read input | 1 | - | - |
| Parity check | 1 | 1 | NO |

This demonstrates the impossibility of placing a single asymmetric triangle into any reflection-symmetric configuration.

### Example 2

Input:

```
4
```

| Step | n | n % 2 | Pairing interpretation | Decision |
| --- | --- | --- | --- | --- |
| Read input | 4 | 0 | 2 mirrored pairs | YES |

This shows how even counts allow full pairing. Each pair can be arranged as a symmetric rectangle, and combining such blocks preserves global symmetry.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a single parity check on the input integer |
| Space | $O(1)$ | No additional storage beyond the input value |

The solution is constant time and trivially fits within the constraints of $n \le 10^9$, since no loop or construction depends on $n$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    n = int(input().strip())
    return "YES\n" if n % 2 == 0 else "NO\n"

# sample-style checks
assert run("1") == "NO\n"
assert run("2") == "YES\n"

# custom cases
assert run("3") == "NO\n"
assert run("4") == "YES\n"
assert run("1000000000") == "YES\n"
assert run("999999999") == "NO\n"
assert run("10") == "YES\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | NO | minimum case, single unpaired triangle |
| 2 | YES | smallest valid symmetric pairing |
| 3 | NO | odd case beyond minimum |
| 4 | YES | basic paired construction |
| 10 | YES | general even behavior |
| 999999999 | NO | large odd boundary case |
| 1000000000 | YES | large even boundary case |

## Edge Cases

For $n = 1$, the algorithm immediately returns NO because the parity check fails. This matches the geometric reality that a single 3-4-5 triangle cannot be reflected to form a consistent axisymmetric shape.

For large odd values such as $n = 10^9 - 1$, the computation still reduces to a single modulus operation. The value is odd, so the output is NO, reflecting that one triangle remains unpaired regardless of scale.

For large even values such as $n = 10^9$, the algorithm outputs YES. Conceptually, all triangles can be partitioned into $n/2$ mirrored pairs, each pair forming a symmetric unit that can be tiled without affecting global symmetry.
