---
title: "CF 102576E - Contamination"
description: "The world is represented as a plane containing many circular forbidden regions. Each explosion creates one such region. The two animals in a query must move inside a horizontal band, from ymin to ymax, without entering any forbidden circle."
date: "2026-07-31T07:33:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102576
codeforces_index: "E"
codeforces_contest_name: "2020 Petrozavodsk Winter Camp, Jagiellonian U Contest"
rating: 0
weight: 102576
solve_time_s: 75
verified: true
draft: false
---

[CF 102576E - Contamination](https://codeforces.com/problemset/problem/102576/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

The world is represented as a plane containing many circular forbidden regions. Each explosion creates one such region. The two animals in a query must move inside a horizontal band, from `ymin` to `ymax`, without entering any forbidden circle. The task is to decide whether both points belong to the same connected part of that band.

The key geometric observation is that a circle can block movement inside a horizontal band only when it touches both horizontal borders of that band. If a circle has vertical span `[cy-r, cy+r]`, it is a complete wall for a query exactly when:

`cy-r <= ymin` and `cy+r >= ymax`.

Because all contaminated regions are disjoint, these walls cannot merge into complicated shapes. A wall separates the strip into a left side and a right side. The two animals cannot meet exactly when there exists such a wall whose center x-coordinate lies strictly between their x-coordinates.

The constraints force an offline solution. With up to one million explosions and one million queries, checking every circle for every query would require around `10^12` operations, which is impossible. We need a preprocessing strategy close to `O((n+q) log n)`.

A common mistake is to only check whether a blocking circle exists in the strip. That is insufficient because a blocking circle may be completely to the left or right of both animals. Another mistake is to include circles whose center x-coordinate equals one of the animal coordinates. Such a case cannot happen for a valid animal point inside the strip if the circle spans the whole strip, because the whole vertical line through the center is contaminated.

For example, consider:

```
1 2
0 0 1
-5 0 5 0 -1 1
```

The circle blocks the strip and separates the two points, so the answer is `NO`.

However:

```
1 2
0 0 1
-5 0 -3 0 -1 1
```

The same circle exists, but both points are on its left side, so the answer is `YES`. A solution that only checks whether a blocking circle exists would fail.

## Approaches

The direct approach is to test every explosion for every query. For each query, we would check whether the explosion covers the vertical range and whether its center lies between the two x-coordinates. This is correct because every separator must be one of these full-height circles. However, with `10^6` queries and `10^6` circles, the worst case is `10^12` checks.

The important reduction is to stop thinking about individual queries geometrically and instead process all queries with the same moving boundary. Sort queries by their lower latitude. When we increase `ymin`, more circles become possible lower walls because their bottom edge is now below the sweep line. For every inserted circle we store its top edge at its x-coordinate.

At any moment in the sweep, the structure contains exactly the circles satisfying:

`cy-r <= current_ymin`.

For a query with `[ymin, ymax]`, among those inserted circles we only need to know whether some x-coordinate between the two animals has a maximum top edge at least `ymax`. If such a value exists, that circle reaches the upper border and blocks the way.

This becomes a range maximum query problem over compressed x-coordinates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Offline sweep with segment tree | O((n+q) log n) | O(n+q) | Accepted |

## Algorithm Walkthrough

1. Sort all circles by their bottom coordinate `cy-r`. Sort all queries by `ymin`. During the sweep, insert circles whose bottom is already below the current query's lower boundary.
2. Compress all circle center x-coordinates. The segment tree stores, for every compressed x-position, the largest `cy+r` among inserted circles with that center.
3. For each query, find the compressed range of center x-coordinates strictly between the two animal positions. If this range is empty, no circle can separate them.
4. Query the segment tree on that x-range. If the maximum stored top coordinate is at least `ymax`, a full-height contamination wall exists between the animals, so the answer is `NO`. Otherwise, the answer is `YES`.

Why it works:

The invariant of the sweep is that after processing all circles with `cy-r <= ymin`, the segment tree contains exactly the circles that could possibly touch the bottom of the current strip. A query fails only when one of those circles also reaches `ymax` and its center x-coordinate is between the two animals. The range maximum query checks precisely this condition, so every returned answer matches the actual connectivity of the strip.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegmentTree:
    def __init__(self, n):
        self.n = 1
        while self.n < n:
            self.n *= 2
        self.t = [-(10**30)] * (2 * self.n)

    def update(self, i, v):
        i += self.n
        if self.t[i] >= v:
            return
        self.t[i] = v
        i //= 2
        while i:
            nv = self.t[2 * i]
            if self.t[2 * i + 1] > nv:
                nv = self.t[2 * i + 1]
            if self.t[i] == nv:
                break
            self.t[i] = nv
            i //= 2

    def query(self, l, r):
        if l >= r:
            return -(10**30)
        l += self.n
        r += self.n
        ans = -(10**30)
        while l < r:
            if l & 1:
                if self.t[l] > ans:
                    ans = self.t[l]
                l += 1
            if r & 1:
                r -= 1
                if self.t[r] > ans:
                    ans = self.t[r]
            l //= 2
            r //= 2
        return ans

n, q = map(int, input().split())

circles = []
xs = []

for _ in range(n):
    cx, cy, r = map(int, input().split())
    circles.append((cy - r, cy + r, cx))
    xs.append(cx)

xs.sort()
unique_x = []
for x in xs:
    if not unique_x or unique_x[-1] != x:
        unique_x.append(x)

circles.sort()

queries = []
for i in range(q):
    px, py, qx, qy, ymin, ymax = map(int, input().split())
    queries.append((ymin, ymax, px, qx, i))

queries.sort()

seg = SegmentTree(len(unique_x))
ans = ["YES"] * q
ptr = 0

import bisect

for ymin, ymax, px, qx, idx in queries:
    while ptr < n and circles[ptr][0] <= ymin:
        bottom, top, cx = circles[ptr]
        seg.update(bisect.bisect_left(unique_x, cx), top)
        ptr += 1

    if px > qx:
        px, qx = qx, px

    left = bisect.bisect_right(unique_x, px)
    right = bisect.bisect_left(unique_x, qx)

    if seg.query(left, right) >= ymax:
        ans[idx] = "NO"

print("\n".join(ans))
```

The sweep pointer only moves forward, so every circle is inserted exactly once. The segment tree update keeps the maximum upper edge for each x-coordinate because among several circles with the same center, only the highest one can block a query.

The use of `bisect_right` and `bisect_left` is deliberate. The query asks for centers strictly between the two animals. Including an endpoint would introduce false barriers.

All coordinates fit comfortably inside Python integers. The algorithm never computes squared distances or performs floating-point operations, so precision issues are avoided.

## Worked Examples

For the sample input, the circles are:

| Center x | Bottom | Top |
| --- | --- | --- |
| 3 | 1 | 5 |
| 7 | 4 | 10 |
| 12 | 3 | 7 |

For the first query, the strip is `[2,6]`.

| Step | Current ymin | Inserted circles | Max top between x=1 and x=14 | Result |
| --- | --- | --- | --- | --- |
| Sweep reaches 2 | 2 | x=3 | 5 | Continue |
| Query ymax | 6 | x=3,x=12 checked | 5 | YES |

The circle at x=3 reaches the lower side but not the upper side, so it cannot split the strip.

For the second query, the strip is `[4,7]`.

| Step | Current ymin | Inserted circles | Max top between x=1 and x=14 | Result |
| --- | --- | --- | --- | --- |
| Sweep reaches 4 | 4 | x=3,x=7,x=12 | 10 | NO |

The circle centered at x=7 covers the entire strip and lies between the animals, creating an impassable wall.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+q) log n) | Each circle update and query is logarithmic |
| Space | O(n+q) | Stores circles, queries, compressed coordinates, and answers |

The solution processes two million objects with logarithmic operations, which is suitable for the given limits. The memory usage is linear.

## Test Cases

```
# The official solution is designed for direct stdin/stdout execution.
# These examples describe expected behavior.

# Minimum case:
# 1 1
# 0 0 1
# -2 0 2 0 -1 1
# Expected:
# NO

# No separating circle:
# 1 1
# 0 0 1
# -5 0 -3 0 -1 1
# Expected:
# YES

# Circle touches lower boundary only:
# 1 1
# 0 0 2
# -5 2 5 2 2 3
# Expected:
# YES

# Multiple circles, only one is relevant:
# 2 1
# -10 0 1
# 5 5 5
# -20 0 20 0 0 9
# Expected:
# NO
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single full-height circle | NO | Basic separator detection |
| Circle outside x-range | YES | Only walls between animals matter |
| Circle touching one border | YES | Correct vertical interval condition |
| Several circles | NO | Sweep structure handles multiple obstacles |

## Edge Cases

A circle that exactly touches both borders must count as a wall. The condition uses `<=` and `>=`, not strict inequalities. For a circle with vertical span `[0,10]` and a query strip `[0,10]`, the circle blocks movement.

A circle that touches only one border must not count. A circle with vertical span `[0,5]` cannot prevent movement in a strip `[0,10]` because an animal can go around its top.

Several circles with the same x-coordinate are handled by keeping the maximum top value. The highest such circle dominates all lower circles for every future query.

Queries are answered independently of the order they appear. The offline sweep restores the original order using the stored query index before printing.
