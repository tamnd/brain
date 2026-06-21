---
title: "CF 105608B - \u0414\u0432\u0435 \u043c\u0438\u0448\u0435\u043d\u0438"
description: "We are given two circular targets on a plane. Each target is defined by its center coordinates and a radius. From these two circles, we are asked to determine which of four “scores” from 0 to 3 are achievable, where each score corresponds to a geometric relation between the two…"
date: "2026-06-22T05:50:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105608
codeforces_index: "B"
codeforces_contest_name: "\u041e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 1\u0421, \u043e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u0442\u0443\u0440 2024-2025"
rating: 0
weight: 105608
solve_time_s: 50
verified: true
draft: false
---

[CF 105608B - \u0414\u0432\u0435 \u043c\u0438\u0448\u0435\u043d\u0438](https://codeforces.com/problemset/problem/105608/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two circular targets on a plane. Each target is defined by its center coordinates and a radius. From these two circles, we are asked to determine which of four “scores” from 0 to 3 are achievable, where each score corresponds to a geometric relation between the two circles.

The first circle can contribute score 1 if it is not fully contained inside the second circle. Symmetrically, the second circle can contribute score 2 if it is not fully contained inside the first circle. A score of 3 is possible if the two circles intersect or touch each other. Score 0 is always possible by definition, so it is always included in the answer set.

The key quantity is the distance between the centers of the circles. The statement defines it as the Euclidean distance, but the provided code uses the squared distance under a square root, effectively computing the actual distance in floating-point form.

Even though the problem looks like it involves multiple conditions, the output is just a subset of the set {0, 1, 2, 3}, printed in increasing order.

The constraints are small enough that each test case is independent and can be solved in constant time. The computation involves only a few arithmetic operations, so the intended solution must run in O(1) per test case.

The main edge cases come from geometric boundary conditions. Circles that are exactly tangent can easily flip conditions depending on whether inequalities are strict or non-strict. Another subtle case occurs when one circle is fully inside the other, but their boundaries still touch at exactly one point. In such a configuration, containment conditions and intersection conditions interact in a way that can confuse incorrect implementations if strict inequalities are used incorrectly.

For example, if circle 1 is entirely inside circle 2, then score 1 should not be included. A naive check like comparing radii alone would fail when centers are offset.

## Approaches

A brute-force approach is not really combinatorial here because there are no large structures to search. Instead, the naive idea is to interpret each condition geometrically in a literal way: for containment, we might try to check whether every point of one circle lies inside another, and for intersection we might attempt to reason about overlapping regions using geometry formulas derived from first principles.

Such an approach would quickly become unnecessarily complex and error-prone. Checking containment point-by-point is impossible in continuous geometry, and even discretizing points would be meaningless and inefficient. The brute-force interpretation fails because geometry provides closed-form distance conditions that replace any need for sampling or enumeration.

The key insight is that all required conditions reduce to comparisons involving only the distance between centers and the radii. Once we compute that distance, each of the three nontrivial scores corresponds to a simple inequality.

Containment of circle 1 in circle 2 depends on whether the farthest point of circle 1 is still inside circle 2, which reduces to checking whether the distance between centers plus radius of circle 1 exceeds radius of circle 2. The same logic applies symmetrically for the reverse containment condition.

Intersection depends on whether the sum of radii is at least the distance between centers. This captures both proper intersection and tangency.

Thus the entire problem collapses into evaluating three independent inequalities.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute geometric reasoning / sampling | O(infinite / impractical) | O(1) | Not applicable |
| Direct formula checks | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We compute the Euclidean distance between the centers of the two circles and then evaluate three independent geometric conditions.

1. Read the coordinates and radii of both circles. This defines the full geometric configuration.
2. Compute the distance between the centers using the Euclidean formula. This single value fully determines all spatial relationships between the circles.
3. Start the answer set with 0, since it is always included regardless of geometry.
4. Check whether circle 1 is not fully contained in circle 2 by testing whether the distance plus radius of circle 1 is greater than radius of circle 2. If true, include 1 in the answer.
5. Check the symmetric condition for circle 2 not being fully contained in circle 1. If true, include 2 in the answer.
6. Check whether the circles intersect or touch by verifying that the distance between centers is at most the sum of radii. If true, include 3 in the answer.
7. Output all collected values in increasing order.

The reasoning behind each condition is purely geometric. For containment, we measure the farthest possible point of one circle relative to the other center. For intersection, we compare how far apart centers are versus how far the circles extend outward.

### Why it works

The algorithm relies on the fact that any relationship between two circles is fully determined by three quantities: the two radii and the distance between centers. Every condition in the problem statement can be rewritten as a direct inequality involving these values. Since these inequalities are both necessary and sufficient, evaluating them independently cannot miss any valid score or include any invalid one. The independence of conditions ensures there is no hidden dependency between checks.

## Python Solution

```python
import sys
input = sys.stdin.readline

x1, y1, r1 = map(int, input().split())
x2, y2, r2 = map(int, input().split())

dx = x1 - x2
dy = y1 - y2
d = (dx * dx + dy * dy) ** 0.5

ans = [0]

if r1 + d > r2:
    ans.append(1)

if r2 + d > r1:
    ans.append(2)

if d <= r1 + r2:
    ans.append(3)

print(*ans)
```

The implementation follows the geometric derivations directly. The distance computation is done using squared differences and a square root, matching the intended Euclidean metric. Each condition is checked independently, and results are appended in increasing order automatically because we start from 0 and evaluate conditions in ascending label order.

A subtle implementation detail is the use of floating-point arithmetic for distance. While squared distance comparisons could avoid floating-point precision issues, the problem’s intended solution uses the square root form, so this remains correct under typical constraints.

## Worked Examples

### Example 1

Input:

```
0 0 1
3 0 1
```

Here the centers are 3 units apart.

| Step | d | r1 + d > r2 | r2 + d > r1 | d ≤ r1 + r2 | ans |
| --- | --- | --- | --- | --- | --- |
| Init | 3 | - | - | - | [0] |
| Check 1 | 3 | 1 + 3 > 1 → yes | - | - | [0, 1] |
| Check 2 | 3 | - | 1 + 3 > 1 → yes | - | [0, 1, 2] |
| Check 3 | 3 | - | - | 3 ≤ 2 → no | [0, 1, 2] |

This shows a disjoint configuration where neither circle contains the other, but they are too far apart to intersect.

### Example 2

Input:

```
0 0 5
1 0 1
```

Here the smaller circle lies inside the larger one.

| Step | d | r1 + d > r2 | r2 + d > r1 | d ≤ r1 + r2 | ans |
| --- | --- | --- | --- | --- | --- |
| Init | 1 | - | - | - | [0] |
| Check 1 | 1 | 5 + 1 > 1 → yes | - | - | [0, 1] |
| Check 2 | 1 | - | 1 + 1 > 5 → no | - | [0, 1] |
| Check 3 | 1 | - | - | 1 ≤ 6 → yes | [0, 1, 3] |

This confirms that containment is asymmetric and intersection still holds even when one circle is strictly inside another.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations and comparisons are performed |
| Space | O(1) | Only a fixed-size answer list is used |

The computation is constant-time per test case, which easily satisfies typical competitive programming constraints even for large inputs.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import sqrt

    x1, y1, r1 = map(int, input().split())
    x2, y2, r2 = map(int, input().split())

    dx = x1 - x2
    dy = y1 - y2
    d = (dx * dx + dy * dy) ** 0.5

    ans = [0]

    if r1 + d > r2:
        ans.append(1)

    if r2 + d > r1:
        ans.append(2)

    if d <= r1 + r2:
        ans.append(3)

    return " ".join(map(str, ans))

# provided samples (conceptual placeholders since original statement omits them)
assert run("0 0 1\n3 0 1") == "0 1 2", "disjoint circles"

# touching circles
assert run("0 0 1\n2 0 1") == "0 1 2 3", "tangent case"

# full containment
assert run("0 0 5\n1 0 1") == "0 1 3", "inner circle"

# identical circles
assert run("0 0 2\n0 0 2") == "0 3", "coincident circles"

# far apart
assert run("0 0 1\n10 0 1") == "0 1 2", "no intersection"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| tangent circles | 0 1 2 3 | boundary intersection correctness |
| containment case | 0 1 3 | asymmetric inclusion logic |
| identical circles | 0 3 | full overlap edge case |
| distant circles | 0 1 2 | non-intersecting separation |

## Edge Cases

A key edge case is tangency, where circles touch at exactly one point. For example, circles with centers distance equal to r1 + r2 should still count as intersecting. The condition d ≤ r1 + r2 correctly includes this case, and the algorithm adds score 3.

Another subtle case is complete overlap where both circles have identical centers and radii. In that situation, each circle is fully contained in the other only in a degenerate sense, but the inequality r + d > r fails in both directions, so scores 1 and 2 are excluded. At the same time, intersection still holds because distance is zero, which is less than or equal to sum of radii.

A third case is strict containment with separation, where one circle sits entirely inside another but does not touch the boundary. For instance, a large circle centered at (0,0) with radius 10 and a small circle at (1,0) with radius 1 produces d = 1. The condition r1 + d > r2 correctly detects asymmetry, ensuring only the appropriate score is included while still marking intersection as true.
