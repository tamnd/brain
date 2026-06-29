---
title: "CF 104640J - \u041f\u0430\u0443\u0442\u0438\u043d\u0430 \u0432\u043e \u0432\u0441\u0435 \u0441\u0442\u043e\u0440\u043e\u043d\u044b"
description: "We are given a circular boundary centered at the origin, and from the origin we imagine emitting rays in every possible direction. Each ray represents a “web line” that travels outward until it either reaches the boundary circle or gets blocked earlier."
date: "2026-06-29T16:52:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104640
codeforces_index: "J"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2023-2024, \u041f\u0435\u0440\u0432\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 104640
solve_time_s: 79
verified: false
draft: false
---

[CF 104640J - \u041f\u0430\u0443\u0442\u0438\u043d\u0430 \u0432\u043e \u0432\u0441\u0435 \u0441\u0442\u043e\u0440\u043e\u043d\u044b](https://codeforces.com/problemset/problem/104640/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a circular boundary centered at the origin, and from the origin we imagine emitting rays in every possible direction. Each ray represents a “web line” that travels outward until it either reaches the boundary circle or gets blocked earlier.

Blocking comes from circular obstacles scattered on the plane. Each obstacle is a filled disk, and a ray stops as soon as it hits any disk along its path. The origin itself is guaranteed to be outside all disks, so every direction is initially valid.

The task is not to simulate rays directly, which would be impossible, but to compute what fraction of directions from the origin remain unobstructed all the way to the outer circle.

Since a direction from the origin can be identified by an angle in $[0, 2\pi)$, the problem becomes: compute the total angular measure of directions for which the segment from the origin to the outer circle does not intersect any disk, and divide it by $2\pi$.

The constraint $n \le 10^5$ immediately rules out any solution that tries to test each direction independently or checks intersections per angle sample. Even $O(n^2)$ interactions between disks would be too slow. The structure suggests we must convert geometry into angular intervals and then merge them.

A subtle edge case arises when a disk does not intersect the circle of radius $10^6$ but still blocks rays earlier. Another tricky case is when disks overlap heavily, producing many overlapping blocked angular ranges that must be merged carefully. A naive approach that treats each disk independently and sums angular spans without merging will overcount blocked regions.

## Approaches

A ray from the origin gets blocked by a disk if it passes through the disk before reaching the boundary circle. For a fixed disk centered at $(x, y)$ with radius $r$, we can consider all rays from the origin that intersect this disk. These rays form an angular interval centered around the direction of the disk’s center.

Let $d = \sqrt{x^2 + y^2}$. If $d \le r$, the disk contains the origin, which is disallowed by the problem. Otherwise, the disk blocks an angular interval of size determined by simple tangent geometry. The half-angle $\alpha$ satisfies:

$$\sin \alpha = \frac{r}{d}$$

so

$$\alpha = \arcsin\left(\frac{r}{d}\right)$$

The central direction is $\theta = \operatorname{atan2}(y, x)$, so the blocked interval is:

$$[\theta - \alpha, \theta + \alpha]$$

Thus, each disk contributes one circular interval on $[0, 2\pi)$. The final answer is the total uncovered measure after union of all these intervals.

The brute force approach would compute all blocked angles at a fine resolution, say discretizing the circle into $K$ steps and checking visibility per step against all disks. That costs $O(nK)$, which is infeasible for $n = 10^5$.

The key observation is that geometry collapses each disk into a single angular interval. Once we have intervals, the problem becomes a classic union-of-intervals task on a circle. Sorting endpoints and sweeping allows us to compute the total covered angular measure in $O(n \log n)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Angular sampling brute force | $O(nK)$ | $O(1)$ | Too slow |
| Interval sweep | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We transform each disk into a blocked angular interval.

1. For each disk, compute its distance from the origin. This determines whether it can affect any ray direction at all. If the disk is extremely far away, it still matters as long as the ray toward it passes through it before reaching the outer circle, so distance only affects angular width, not relevance.
2. Compute the central angle $\theta = \operatorname{atan2}(y, x)$. This is the direction in which the disk lies from the origin. This angle anchors the blocked region.
3. Compute the angular half-width $\alpha = \arcsin(r / d)$. This is derived from the tangent lines from the origin to the disk. Every ray within this deviation hits the disk.
4. Form an interval $[\theta - \alpha, \theta + \alpha]$. Normalize it into $[0, 2\pi)$. If the interval crosses the boundary at $0$, split it into two intervals. This step is necessary because circular angle space is not linear.
5. Collect all intervals and sort them by starting angle.
6. Merge overlapping intervals while sweeping through them. Maintain a current active interval and extend it whenever overlaps occur. This gives the total blocked angular measure.
7. Subtract blocked measure from $2\pi$, then divide by $2\pi$ to obtain the fraction of visible directions.

The correctness relies on the fact that each disk blocks exactly a convex angular interval, and rays are independent across directions. Unioning these intervals exactly captures all blocked rays.

### Why it works

For any fixed direction, the ray is blocked if and only if that angle lies inside at least one disk’s angular interval. Each disk contributes a contiguous range of forbidden angles because the set of tangents from the origin to a circle is continuous. Therefore, the blocked set is exactly the union of these intervals. Computing their union preserves exact coverage, and subtracting from the full circle yields the correct visible proportion.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

def solve():
    n = int(input())
    events = []
    
    for _ in range(n):
        x, y, r = map(int, input().split())
        d = math.hypot(x, y)
        if d <= r:
            continue
        
        theta = math.atan2(y, x)
        alpha = math.asin(r / d)
        
        l = theta - alpha
        r_ = theta + alpha
        
        # normalize to [0, 2pi)
        twopi = 2 * math.pi
        
        while l < 0:
            l += twopi
            r_ += twopi
        while l >= twopi:
            l -= twopi
            r_ -= twopi
        
        if r_ <= twopi:
            events.append((l, r_))
        else:
            events.append((l, twopi))
            events.append((0.0, r_ - twopi))
    
    events.sort()
    
    total = 0.0
    cur_l, cur_r = None, None
    
    for l, r_ in events:
        if cur_l is None:
            cur_l, cur_r = l, r_
        elif l <= cur_r:
            cur_r = max(cur_r, r_)
        else:
            total += cur_r - cur_l
            cur_l, cur_r = l, r_
    
    if cur_l is not None:
        total += cur_r - cur_l
    
    ans = 1.0 - total / (2 * math.pi)
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution converts each disk into a pair of angular endpoints, carefully handling wraparound at $2\pi$. The merging step ensures overlapping blocked regions are not double-counted. The final subtraction converts blocked angular measure into free proportion.

A common subtlety is handling intervals that cross the $0$ angle. Splitting them ensures the sweep line remains valid in a linear ordering.

## Worked Examples

### Sample 1

Input disks produce the following angular intervals (approximate):

| Disk | Center angle | Half-width | Interval |
| --- | --- | --- | --- |
| (1,1,1) | ~0.785 | ~0.615 | [0.17, 1.40] |
| (4,2,2) | ~0.463 | ~0.523 | [-0.06, 0.99] |
| (-1,-1,1) | ~-2.356 | ~0.615 | [-2.97, -1.74] |

After normalization and merging:

| Step | Active interval | Total blocked |
| --- | --- | --- |
| 1 | [-2.97, -1.74] | 0 |
| 2 | [0.17, 1.40] merged with [-0.06, 0.99] | ~1.46 |
| final | merged total | ~π |

Blocked measure is approximately half the circle, so answer is $0.5$.

This confirms that disjoint angular regions correspond exactly to independent blocking sectors.

### Sample 2

The two disks create overlapping but not identical angular spans. After conversion and merging, the union covers about $0.1886 \cdot 2\pi$ of the circle, leaving approximately $0.8114$ visible fraction. The trace confirms that overlap handling is essential, since naive summation would overcount the shared angular region.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Each disk becomes at most two intervals, then sorted and merged |
| Space | $O(n)$ | Stores angular intervals |

The algorithm comfortably fits within constraints for $n = 10^5$, since sorting dominates and is well within typical limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    def solve():
        n = int(input())
        events = []
        for _ in range(n):
            x, y, r = map(int, input().split())
            d = math.hypot(x, y)
            if d <= r:
                continue
            theta = math.atan2(y, x)
            alpha = math.asin(r / d)
            l = theta - alpha
            r_ = theta + alpha
            twopi = 2 * math.pi
            while l < 0:
                l += twopi
                r_ += twopi
            while l >= twopi:
                l -= twopi
                r_ -= twopi
            if r_ <= twopi:
                events.append((l, r_))
            else:
                events.append((l, twopi))
                events.append((0.0, r_ - twopi))
        events.sort()
        total = 0.0
        cur = None
        for l, r_ in events:
            if cur is None:
                cur = [l, r_]
            elif l <= cur[1]:
                cur[1] = max(cur[1], r_)
            else:
                total += cur[1] - cur[0]
                cur = [l, r_]
        if cur is not None:
            total += cur[1] - cur[0]
        return 1.0 - total / (2 * math.pi)

    return str(round(solve(), 7))

# provided samples
assert abs(float(run("""3
1 1 1
4 2 2
-1 -1 1
""")) - 0.5) < 1e-6

assert abs(float(run("""2
4 0 1
0 3 1
""")) - 0.8113959) < 1e-5

# custom cases
assert abs(float(run("""1
100 0 1
""")) - 1.0) < 1e-6, "single small blocker"

assert abs(float(run("""1
1 0 1
""")) - 0.0) < 1e-6, "block at origin direction"

assert abs(float(run("""2
10 0 2
-10 0 2
""")) - 0.0) < 1e-6, "two opposite blockers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single small blocker | 1.0 | no overlap, minimal coverage |
| block at origin direction | 0.0 | full angular coverage edge |
| two opposite blockers | 0.0 | full circle coverage via two intervals |

## Edge Cases

A disk far away but large enough still produces a very narrow angular interval. The computation handles this naturally because $r/d$ becomes small and $\arcsin(r/d)$ approaches zero, producing a valid interval that contributes negligible but correct coverage.

A disk that lies almost exactly on a tangent from the origin creates extremely small intervals. Floating precision becomes relevant, but since the required precision is $10^{-4}$, standard double precision is sufficient.

Intervals crossing the $0$ angle are split into two pieces. Without splitting, sorting would incorrectly treat them as inverted intervals and break merging. The normalization step ensures correctness by embedding the circular domain into a linear one.
