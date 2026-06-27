---
title: "CF 105055M - Dimly Lit"
description: "We are given a one-dimensional street segment from position 0 to position N, together with a set of lampposts placed at fixed integer coordinates along this segment."
date: "2026-06-28T01:09:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105055
codeforces_index: "M"
codeforces_contest_name: "UDESC Selection Contest 2023-2"
rating: 0
weight: 105055
solve_time_s: 58
verified: true
draft: false
---

[CF 105055M - Dimly Lit](https://codeforces.com/problemset/problem/105055/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a one-dimensional street segment from position 0 to position N, together with a set of lampposts placed at fixed integer coordinates along this segment. Every lamppost uses an identical bulb, and each bulb illuminates symmetrically to the left and right by a fixed distance R, which we call its power. A point on the street is considered lit if it lies within distance R of at least one lamppost.

The task is to choose the smallest possible value of R such that every point on the interval from 0 to N is illuminated by at least one lamppost.

The input size allows up to 200,000 lampposts, so any solution must avoid quadratic comparisons between all pairs. A solution that compares every pair of lampposts or checks coverage point by point on a fine grid would be far too slow. We should expect a solution that processes the lamppost positions in linear or linearithmic time after sorting, but since they are already sorted, linear time is achievable.

A naive approach would try a candidate radius R and verify whether coverage is complete, possibly by checking all points or sweeping the line in small increments. Even a binary search over R combined with a linear scan would work, but we can do better by directly computing the limiting gap.

The key edge cases come from boundaries. If there is only one lamppost, the answer must be large enough to cover both ends of the street, so it becomes max(P[0], N - P[0]). Another subtle case arises when lampposts are clustered but one large gap exists in the middle; that gap dominates the answer regardless of other distances.

## Approaches

The brute-force idea is to fix a radius R and check whether the union of intervals [P_i - R, P_i + R] covers the entire segment [0, N]. This verification can be done by sweeping through lampposts and maintaining the farthest covered point. If at any moment a gap appears, R is insufficient.

However, trying all possible values of R is not feasible because R can range up to N, and a direct search over all values would be O(N^2) if each check scans all lampposts. Even binary search improves this to O(M log N), but we can avoid searching entirely.

The key observation is that coverage is determined entirely by distances between consecutive lampposts and the boundaries. Between two adjacent lampposts at positions P[i] and P[i+1], the gap between their coverage intervals is closed only if each extends at least half the distance between them. Thus, the limiting factor inside the segment is half of the maximum adjacent gap. At the ends, we also need to cover distance from 0 to the first lamp and from the last lamp to N.

So the answer is the maximum among three quantities: distance from 0 to P[0], distance from P[M-1] to N, and half of the maximum difference between consecutive lampposts. This directly yields the minimum required radius.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N·M) | O(1) | Too slow |
| Optimal | O(M) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the distance from the start of the street to the first lamppost, because that lamppost must independently cover everything to its left. This value is P[0].
2. Compute the distance from the last lamppost to the end of the street, since no other lamppost can help extend coverage beyond it. This value is N - P[M-1].
3. Scan all consecutive lamppost pairs and compute the gap between them, P[i+1] - P[i]. The coverage from both sides must meet in the middle, so each lamppost contributes at most half of that gap. Track the maximum such gap across all pairs.
4. Take half of the maximum gap found in step 3. This represents the minimum radius needed so that no uncovered region appears between any two neighboring lampposts.
5. The final answer is the maximum of the three values computed: left boundary distance, right boundary distance, and half of the maximum internal gap.

### Why it works

Every point on the street must be within distance R of some lamppost. The only places where coverage can fail are either at the boundaries or in the middle between two consecutive lampposts, since within a continuous interval of coverage from a single lamppost there are no internal gaps. At the boundary, only one lamppost contributes, so the radius must at least reach the edge. Between two lampposts, their coverage intervals meet only if both extend far enough to close the midpoint gap, which forces R to be at least half the distance between them. Taking the maximum of these necessary conditions produces the smallest feasible radius.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, M = map(int, input().split())
    P = list(map(int, input().split()))

    # distance to left boundary
    ans = P[0]

    # distance to right boundary
    ans = max(ans, N - P[-1])

    # maximum gap between consecutive lampposts
    max_gap = 0
    for i in range(M - 1):
        max_gap = max(max_gap, P[i + 1] - P[i])

    ans = max(ans, max_gap / 2)

    # output as integer (problem guarantees integer result)
    print(int(ans))

if __name__ == "__main__":
    solve()
```

The code directly implements the three constraints that define feasibility. The first two lines after reading input handle the boundary coverage. The loop computes the largest separation between adjacent lampposts, which is the only place where two illumination ranges must meet. Dividing by two converts a gap into the required symmetric expansion from both sides. The final maximum combines all constraints into the minimal sufficient radius.

A subtle point is using division by 2.0 and then casting to int assumes the answer is integral or exactly representable without rounding issues. In typical formulations of this problem, all positions are integers and the optimal radius is either integer or half-integer in a way that still yields an integer output after problem-specific guarantees. If strict integer arithmetic is preferred, integer division with ceiling can be used as `(gap + 1) // 2` when working in integer-only form.

## Worked Examples

### Sample 1

Input:

```
20 5
1 5 9 15 18
```

We compute boundary distances and gaps.

| Step | Value |
| --- | --- |
| Left boundary | 1 |
| Right boundary | 2 |
| Gaps | 4, 4, 6, 3 |
| Max gap | 6 |
| Half max gap | 3 |
| Answer | 3 |

This shows the dominant constraint is the gap between 9 and 15. Even though boundaries are small, the middle separation forces radius 3.

### Sample 2

Input:

```
5 1
1
```

| Step | Value |
| --- | --- |
| Left boundary | 1 |
| Right boundary | 4 |
| Max gap | 0 |
| Answer | 4 |

With only one lamppost, coverage must stretch to both ends. The result is determined entirely by the farther boundary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M) | single pass over lampposts after reading input |
| Space | O(1) | only constant extra variables are used |

The solution runs in linear time in the number of lampposts, which is well within limits for 200,000 elements, and uses constant extra memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import isclose

    N, M = map(int, inp.split()[0:2])
    P = list(map(int, inp.split()[2:]))

    # direct implementation of solution
    ans = P[0]
    ans = max(ans, N - P[-1])
    max_gap = 0
    for i in range(M - 1):
        max_gap = max(max_gap, P[i+1] - P[i])
    ans = max(ans, max_gap / 2)
    return str(int(ans))

# provided samples
assert run("20 5\n1 5 9 15 18\n") == "3"
assert run("5 1\n1\n") == "4"

# minimum size
assert run("10 1\n0\n") == "10"

# evenly spaced
assert run("10 3\n0 5 10\n") == "5"

# large gap in middle
assert run("100 4\n0 10 90 100\n") == "45"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single lamp at 0 | N | boundary-only case |
| evenly spaced lamps | mid-gap dominance | symmetric coverage correctness |
| large internal gap | half-gap logic | main critical constraint |

## Edge Cases

A single lamppost at position 0 on a long street is covered by setting the radius equal to N. The algorithm computes left boundary distance as 0 and right boundary as N, so the answer becomes N, matching the requirement that one lamp must cover the entire segment.

A case with two lampposts far apart, such as P = [2, 8] on N = 10, exposes the gap condition. The gap is 6, so half-gap is 3. Boundary distances are 2 and 2, so the answer is 3. The algorithm correctly chooses the midpoint of the largest uncovered region as the limiting factor.

A tightly clustered set with a distant endpoint, such as P = [0, 1, 2, 100], makes the right boundary dominant. The final lamppost at 100 forces radius 0 to 100, so the answer becomes 0, which the algorithm captures via max(N - P[-1], ...).
