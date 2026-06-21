---
title: "CF 105900D - Delirium at Unballoon"
description: "We are comparing two containers filled with ice cream: a cylindrical bottle and a cone with an extra dome on top. The bottle is a simple cylinder with radius rL and height hL, completely filled. Its capacity is just the usual cylinder volume."
date: "2026-06-21T15:17:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105900
codeforces_index: "D"
codeforces_contest_name: "VI UnBalloon Contest Mirror"
rating: 0
weight: 105900
solve_time_s: 50
verified: true
draft: false
---

[CF 105900D - Delirium at Unballoon](https://codeforces.com/problemset/problem/105900/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are comparing two containers filled with ice cream: a cylindrical bottle and a cone with an extra dome on top.

The bottle is a simple cylinder with radius `rL` and height `hL`, completely filled. Its capacity is just the usual cylinder volume.

The cone side consists of a right circular cone with radius `rC` and height `hC`, also filled completely, and then a solid hemisphere of the same radius `rC` is placed on top of it and also filled with ice cream. So the cone container effectively has two parts contributing to volume.

The task is to decide whether the bottle holds strictly more ice cream than the cone-with-hemisphere structure. If yes, we output `Injusto`, otherwise we output `Justo`.

The input sizes are very small, all dimensions are at most 100. This immediately rules out any need for advanced optimization. A direct constant time computation is sufficient, and even floating point arithmetic would technically work, although it introduces unnecessary precision risk.

The only subtle issue is that the volumes involve π, but since both sides include π as a factor, it cancels out completely if we compare algebraically. A careless implementation that keeps π and uses floating point comparisons can still pass, but it is avoidable and less robust.

Edge cases are mostly about equality and borderline comparisons. For example, when both containers are identical in capacity, the answer must be `Justo` because the condition requires the bottle to be strictly greater.

## Approaches

A brute force interpretation would compute both volumes directly using geometry formulas. The bottle is straightforward: a cylinder volume `π rL^2 hL`. The cone is the sum of a cone volume `(1/3)π rC^2 hC` and a hemisphere volume `(2/3)π rC^3`.

This approach is already O(1), so there is no algorithmic bottleneck. The only potential inefficiency is unnecessary use of floating point arithmetic and π, which introduces rounding issues when comparing values that should be exact integers after scaling.

The key observation is that π is common to every term. If we multiply everything by 3/π, we convert all volumes into integers:

the bottle becomes `3 rL^2 hL`, and the cone becomes `rC^2 hC + 2 rC^3`. After this transformation, the comparison is purely integer-based and exact.

This reduces the problem to a single integer comparison.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct geometry with floats | O(1) | O(1) | Works but precision risk |
| Scaled integer comparison | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

### Optimal approach

1. Read the four integers `rL, hL, rC, hC`. These define two geometric solids whose volumes we will compare.
2. Compute the scaled bottle volume as `Vb = 3 * rL * rL * hL`. This comes from multiplying the cylinder volume by 3 and removing π.
3. Compute the scaled cone-plus-hemisphere volume as `Vc = rC * rC * hC + 2 * rC * rC * rC`. The first term corresponds to the cone, the second to the hemisphere after scaling.
4. Compare `Vb` and `Vc`. If `Vb` is strictly greater, output `Injusto`. Otherwise output `Justo`.

The reasoning behind scaling is that it preserves ordering exactly while eliminating irrational constants.

### Why it works

Both original volumes are proportional to π. Since π is positive and identical in both expressions, multiplying or dividing by π does not change the ordering. Similarly, multiplying everything by 3 clears the fraction in the cone formula. After this transformation, both expressions become integers that exactly represent proportional volumes, so comparing them is mathematically equivalent to comparing the original volumes.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    rL, hL, rC, hC = map(int, input().split())

    bottle = 3 * rL * rL * hL
    cone = rC * rC * hC + 2 * rC * rC * rC

    if bottle > cone:
        print("Injusto")
    else:
        print("Justo")

if __name__ == "__main__":
    solve()
```

The implementation follows the algebraic simplification directly. The only care needed is consistent use of integer arithmetic. All intermediate values fit comfortably within 32-bit integers since the maximum magnitude is around `3 * 100^3 = 3e6`.

The decision step uses strict inequality as required by the statement. Any tie defaults to `Justo`.

## Worked Examples

### Example 1

Input:

```
1 4 1 10
```

| Step | Bottle value `3 rL^2 hL` | Cone value `rC^2 hC + 2 rC^3` | Decision |
| --- | --- | --- | --- |
| Compute values | 3 * 1 * 1 * 4 = 12 | 1 * 1 * 10 + 2 * 1 = 12 | equal |

Since values are equal, bottle is not strictly larger, so output is `Justo`.

This shows the equality case where both shapes store exactly the same amount after normalization.

### Example 2

Input:

```
78 57 60 40
```

| Step | Bottle value | Cone value | Decision |
| --- | --- | --- | --- |
| Compute values | 3 * 78^2 * 57 = 1041192 | 60^2 * 40 + 2 * 60^3 = 864000 | bottle larger |

Since the bottle value exceeds the cone value, output is `Injusto`.

This demonstrates a case where the cubic term in the cone is large but still dominated by the cylindrical bottle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations on four integers |
| Space | O(1) | No auxiliary structures used |

The computation is constant-time and trivially fits within the constraints. Even with many test cases, the same reasoning would still scale linearly with input size.

## Test Cases

```python
import sys, io

def solve():
    rL, hL, rC, hC = map(int, sys.stdin.readline().split())

    bottle = 3 * rL * rL * hL
    cone = rC * rC * hC + 2 * rC * rC * rC

    print("Injusto" if bottle > cone else "Justo")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("1 4 1 10\n") == "Justo"
assert run("78 57 60 40\n") == "Injusto"

# custom cases
assert run("1 1 1 1\n") == "Justo", "tie case"
assert run("2 100 1 1\n") == "Injusto", "large bottle dominance"
assert run("1 1 5 5\n") == "Justo", "large cone dominance"
assert run("10 10 10 10\n") == "Justo", "balanced larger values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 | Justo | equality handling |
| 2 100 1 1 | Injusto | large bottle dominance |
| 1 1 5 5 | Justo | cone dominates via hemisphere term |
| 10 10 10 10 | Justo | symmetric medium case |

## Edge Cases

One important edge case is equality after scaling. For instance, `1 4 1 10` produces identical scaled volumes. The algorithm computes both expressions exactly and correctly falls into the `Justo` branch because the condition is strict.

Another case is when the cone radius is large but height is small. Even though the hemisphere term grows cubically, the bottle can still dominate if its radius or height is large enough. The integer comparison handles this without any instability.

A final edge scenario is maximal values around 100. Even then, the largest intermediate value is about `3 * 100^3 = 3,000,000`, well within integer limits, so no overflow or precision issues arise.
