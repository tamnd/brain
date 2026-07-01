---
title: "CF 104377O - \u6355\u9c7c\u8fbe\u4eba\uff01"
description: "We are given a set of points in the plane, each point carrying a positive or negative value. A fisherman stands at the origin and can deploy a net in a very flexible way."
date: "2026-07-01T17:25:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104377
codeforces_index: "O"
codeforces_contest_name: "The 21st Sichuan University Programming Contest"
rating: 0
weight: 104377
solve_time_s: 61
verified: true
draft: false
---

[CF 104377O - \u6355\u9c7c\u8fbe\u4eba\uff01](https://codeforces.com/problemset/problem/104377/O)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of points in the plane, each point carrying a positive or negative value. A fisherman stands at the origin and can deploy a net in a very flexible way. The net always corresponds to a circle whose boundary passes through the origin, and everything inside or on that circle is collected. The total gain is the sum of values of all collected points.

The key geometric freedom is that we are not fixing the circle center or radius. We are allowed to choose any circle as long as it passes through the origin, and this includes the degenerate case where the circle becomes arbitrarily large, which effectively turns the boundary into a straight line through the origin, leaving a half-plane as the collected region.

So the task is to choose a geometric region defined by such a circle to maximize the sum of values of all points inside it.

The constraints are small enough that an O(n^2) geometric sweep is viable. With n up to 1000, even a solution that considers each point as a reference direction and processes all others relative to it would pass comfortably within time limits.

A subtle point is that the optimal region is not necessarily a “small circle around a cluster of positive points.” Because we can expand the circle while still forcing it to pass through the origin, we can effectively approximate any half-plane through the origin. This makes configurations where many moderately positive points lie on one side of a line much more important than tightly clustered high-value points.

A naive mistake is to think in terms of distance only, assuming we should pick a radius centered somewhere that captures nearby positive points. That ignores the constraint that the circle must pass through the origin, which fundamentally ties every valid region to a direction anchored at the origin.

Another common pitfall is to treat the problem as selecting a convex hull or bounding circle problem. For example, one might try to pick the minimal enclosing circle of positive points, but that circle is not required to pass through the origin, so it is not a valid candidate.

## Approaches

The brute-force interpretation is to enumerate every possible circle passing through the origin, then test all points inside it and compute the sum. A circle in the plane has three degrees of freedom, but the constraint that it passes through the origin reduces this to two degrees of freedom for its center. Even if we discretize center positions or attempt combinatorial enumeration of candidate circles defined by pairs of points, we quickly face an explosion in possibilities. Checking membership of all n points for each candidate yields a cubic or worse complexity, which is unnecessary given the geometric structure.

The key observation is that every circle passing through the origin induces a partition of the plane where the “far boundary behavior” is equivalent to a half-plane. As the circle’s radius grows, its boundary flattens locally around the origin, and the region approaches a half-plane whose boundary line passes through the origin.

More concretely, any optimal configuration can be represented as a choice of a directed line through the origin, keeping all points on one side of that line. Once we fix a direction, we are effectively deciding a half-plane, and every valid circle can be stretched so that it includes exactly those points lying on one side of some line through the origin.

This reduces the problem to: find a line through the origin such that the sum of values of points on one side of the line is maximized.

This is a classic angular sweeping problem. Each point has a polar angle around the origin. Any half-plane corresponds to an interval of angles of length strictly less than π. So we sort points by angle and use a sliding window of width π on the circular angle space, maintaining the sum of values inside the window.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force circles | Exponential or at best O(n^3) | O(n) | Too slow |
| Angular sweep half-plane | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We convert the geometric problem into angular coordinates, then search for the best semicircular coverage of weighted points.

1. Compute the polar angle of every point with respect to the origin. This maps each point to an angle in the range [0, 2π).
2. Duplicate the list of points by adding 2π to each angle and appending it to the array. This allows us to simulate circular wrap-around using a linear sweep.
3. Sort all points by their angle. Sorting is required so that contiguous angular intervals correspond to contiguous segments in the array.
4. Use a two-pointer sliding window. For each left endpoint, we advance the right endpoint as far as possible while maintaining that the angular span is less than π.
5. For each valid window, compute the sum of values of points inside it and track the maximum over all windows.

The reason the window size is π is that a half-plane through the origin corresponds exactly to all directions lying within any interval of length π. Any larger interval would necessarily include points from both sides of some line through the origin, violating the half-plane structure.

### Why it works

Every feasible solution corresponds to choosing a directed line through the origin, which defines a half-plane. That half-plane corresponds to a continuous angular interval of width π on the unit circle. Conversely, any such interval defines a valid half-plane. The sliding window enumerates all such intervals, so every valid geometric configuration is considered exactly once. The best window sum therefore equals the optimal circle-based selection.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

def solve():
    n = int(input())
    v = list(map(int, input().split()))
    
    pts = []
    for i in range(n):
        x, y = map(int, input().split())
        ang = math.atan2(y, x)
        pts.append((ang, v[i]))
    
    pts.sort()
    
    extended = pts + [(ang + 2 * math.pi, val) for ang, val in pts]
    
    m = len(extended)
    
    ans = -10**18
    current_sum = 0
    r = 0
    
    for l in range(n):
        if r < l:
            r = l
            current_sum = 0
        
        while r < m and extended[r][0] - extended[l][0] < math.pi - 1e-12:
            current_sum += extended[r][1]
            r += 1
        
        ans = max(ans, current_sum)
        current_sum -= extended[l][1]
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation begins by converting each point into polar angle form. The use of `atan2` ensures correct handling across all quadrants, including negative coordinates.

After sorting, we explicitly duplicate the array with angles shifted by 2π. This is what allows the sliding window to treat the circular angle space as a linear interval without special modular arithmetic.

The two-pointer sweep maintains a running sum of values inside the current angular window. The condition `< π` enforces the half-plane constraint. The subtraction step when moving the left pointer ensures the window sum stays consistent.

A common implementation mistake is forgetting floating-point precision issues when comparing angle differences. The small epsilon prevents boundary instability when points lie exactly on the π threshold.

## Worked Examples

Consider a small configuration:

Input:

```
3
1 -2 3
1 0
-1 0
0 1
```

We compute angles and values:

| Point | Angle | Value |
| --- | --- | --- |
| (1,0) | 0 | 1 |
| (-1,0) | π | -2 |
| (0,1) | π/2 | 3 |

After sorting by angle, we evaluate windows of width π:

| l | r | Window points | Sum |
| --- | --- | --- | --- |
| 0 | 2 | (1,0), (0,1) | 4 |
| 1 | 3 | (-1,0), (0,1) | 1 |
| 2 | 3 | (0,1) | 3 |

The best answer is 4, achieved by selecting a half-plane covering the positive x-axis and upper half-plane region.

This trace shows how the algorithm effectively chooses a directional split rather than a bounded geometric region.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting points by angle dominates, sliding window is linear |
| Space | O(n) | Storage for angle-value pairs and duplicated array |

With n up to 1000, this easily fits within time limits. Even in tighter constraints, the solution scales comfortably due to its single sorting step and linear scan.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    n = int(input())
    v = list(map(int, input().split()))
    pts = []
    for i in range(n):
        x, y = map(int, input().split())
        pts.append((math.atan2(y, x), v[i]))
    pts.sort()
    extended = pts + [(a + 2*math.pi, b) for a,b in pts]

    m = len(extended)
    ans = -10**18
    cur = 0
    r = 0
    for l in range(n):
        if r < l:
            r = l
            cur = 0
        while r < m and extended[r][0] - extended[l][0] < math.pi:
            cur += extended[r][1]
            r += 1
        ans = max(ans, cur)
        cur -= extended[l][1]
    return str(ans)

# provided sample-like tests
assert run("""3
1 -2 3
1 0
-1 0
0 1
""").strip() == "4"

# all negative
assert run("""2
-5 -7
1 0
-1 0
""").strip() == "-5"

# all positive clustered
assert run("""3
1 2 3
1 0
2 0
3 0
""").strip() == "6"

# symmetric points
assert run("""4
1 1 1 1
1 0
-1 0
0 1
0 -1
""").strip() == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| mixed small | 4 | correct half-plane selection |
| all negative | -5 | avoids empty-set bias issues |
| aligned positives | 6 | full inclusion stability |
| symmetric cross | 2 | angular boundary correctness |

## Edge Cases

A key edge case is when points lie exactly on the boundary line of the chosen half-plane. In angular terms, this corresponds to differences exactly equal to π. The algorithm treats the window as strictly less than π, which ensures each boundary is consistently assigned to only one side. For example, points at angles 0 and π are never included together in the same window, matching the geometric interpretation that a line through the origin places points on opposite sides.

Another subtle case occurs when all values are negative. The optimal strategy is still to pick the least negative half-plane, not an empty set. The sliding window naturally handles this because every window sum is computed, including those with minimal magnitude negative totals, ensuring the maximum is still captured correctly.
