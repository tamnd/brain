---
title: "CF 102163A - Hasan the lazy judge"
description: "We have horizontal line segments and vertical line segments on an integer coordinate plane. A valid plus sign is formed by choosing one horizontal segment and one vertical segment that intersect at a point C."
date: "2026-08-20T14:18:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "A"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 1454
verified: false
draft: false
---

[CF 102163A - Hasan the lazy judge](https://codeforces.com/problemset/problem/102163/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 24m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We have horizontal line segments and vertical line segments on an integer coordinate plane. A valid plus sign is formed by choosing one horizontal segment and one vertical segment that intersect at a point C. The four arms of the plus sign are the distances from C to the two endpoints of the horizontal segment and the two endpoints of the vertical segment.

For a horizontal segment [x 1 ​ ,x 2 ​ ] and a vertical segment [y 1 ​ ,y 2 ​ ], intersecting at (x,y), its value is

min(x−x 1 ​ , x 2 ​ −x, y−y 1 ​ , y 2 ​ −y).

We need the maximum value over every possible intersecting pair. The input contains T independent test cases, followed by the horizontal segments and then the vertical segments. Coordinates are at most 10 5.

The tempting solution is to examine every horizontal and every vertical segment. With N,M≤10 5, that means up to 10 10 pairs in one test case. A one-second limit makes such a quadratic approach impossible. We need something close to O((N+M)logC), where C≤10 5 is the coordinate range, or at least a small logarithmic factor more.

There are several boundary cases that matter. A segment can be too short to contain a plus sign of positive size. For example,

```

```

The only two segments intersect, but every arm has length zero, so the answer is `0`. A solution that assumes the answer is always positive would be wrong.

The intersection may also occur exactly at an endpoint. For example,

```

```

The segments meet at (1,2), but the horizontal segment has no arm to the left of the intersection. The answer is `0`. When checking a candidate length d, the intersection must be allowed at the boundaries of the trimmed segments, so the horizontal condition is inclusive.

Duplicate coordinates are another easy source of mistakes. For example,

```

```

The answer is `2`. Two horizontal segments can have exactly the same y-coordinate, and a data structure must count both independently. Using a boolean instead of a frequency can cause an incorrect deletion when one of the duplicate segments stops being active.

Finally, the horizontal and vertical segment endpoints are not necessarily given in increasing order by the statement's wording. A robust implementation normalizes every segment so that its first coordinate is no greater than its second coordinate.

## Approaches

The brute-force solution follows directly from the geometry. For every horizontal segment and every vertical segment, we test whether their coordinate ranges overlap in the required way. If they intersect at (x,y), we compute the four arm lengths and update the answer.

This is correct because every possible plus sign is determined by exactly one horizontal and one vertical segment, so examining every pair cannot miss a candidate. The problem is the NM pair count. With N=M=10 5, there can be 10 10 pairs in a single test case, far beyond what the time limit permits.

The useful observation is that we can turn the optimization problem into a decision problem. Suppose we ask whether a plus sign of size at least d exists.

For a horizontal segment [x 1 ​ ,x 2 ​ ], the intersection must be at least d units from both horizontal endpoints. Thus its x-coordinate must satisfy

x 1 ​ +d≤x≤x 2 ​ −d.

This interval is nonempty exactly when

x 2 ​ −x 1 ​ ≥2d.

Likewise, for a vertical segment [y 1 ​ ,y 2 ​ ], a suitable intersection must satisfy

y 1 ​ +d≤y≤y 2 ​ −d,

which requires y 2 ​ −y 1 ​ ≥2d.

So after fixing d, every sufficiently long horizontal segment becomes an active interval in the x-direction, carrying its y-coordinate. A vertical segment becomes a query at its x-coordinate, asking whether some active horizontal y-coordinate lies inside

[y 1 ​ +d, y 2 ​ −d].

This is exactly an offline sweep-line problem. Sort vertical segments by x. As we move from left to right, insert a horizontal segment when x reaches x 1 ​ +d, and remove it after x 2 ​ −d. At a vertical segment's x, the active horizontal segments are precisely those whose trimmed horizontal interval contains that x.

A Fenwick tree over the y-coordinates stores how many active horizontal segments exist at every y. A range sum tells us whether at least one active horizontal segment has a y-coordinate in the vertical segment's trimmed range.

The feasibility condition is monotonic. If a plus sign of size d exists, the same intersection also gives a plus sign of every smaller size. That makes binary search on d possible.

The implementation can make the sweep cheaper than sorting fresh events during every binary-search iteration. The order of horizontal segments by x 1 ​ never changes when we add the same d to every x 1 ​, and the order by x 2 ​ never changes when we subtract the same d. We sort these orders once and reuse them for every feasibility check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NM) | O(N+M) | Too slow |
| Optimal | O((N+M)logClogC) | O(N+M+C) | Accepted |

Here C≤10 5 is the maximum coordinate. The first logarithm comes from the Fenwick operations and the second from binary search.

## Algorithm Walkthrough

1. Normalize every horizontal segment so that x 1 ​ ≤x 2 ​, and every vertical segment so that y 1 ​ ≤y 2 ​. Compute the largest possible answer from the half-length of every segment. A plus of size d needs total length at least 2d on both selected segments, so no answer can exceed the maximum half-length.
2. Sort the vertical segments by their x-coordinate. During a feasibility check, they will be processed from left to right, matching the direction of the sweep.
3. Sort the horizontal segments once by x 1 ​, and once by x 2 ​. For a fixed candidate d, a horizontal segment starts being usable at x 1 ​ +d and stops being usable after x 2 ​ −d. Adding or subtracting the same d does not change either sorting order, so these orders can be reused across all checks.
4. To check a candidate d, ignore every horizontal segment with x 2 ​ −x 1 ​ <2d. Such a segment cannot provide both horizontal arms of length d. Likewise, ignore every vertical segment with y 2 ​ −y 1 ​ <2d.
5. Sweep through the vertical segments in increasing x. Maintain a Fenwick tree indexed by y. For every eligible horizontal segment whose x 1 ​ +d≤x, add one at its y-coordinate. These are exactly the horizontal segments whose left arm can already contain the current intersection.
6. Remove every eligible horizontal segment satisfying x 2 ​ −d<x. The strict inequality is deliberate. When x=x 2 ​ −d, the right arm has exactly length d, so the horizontal segment must still be active at that coordinate.
7. For an eligible vertical segment, query the Fenwick tree over

[y 1 ​ +d, y 2 ​ −d].

If the range contains at least one active horizontal segment, the current d is feasible. The corresponding horizontal and vertical segments intersect at a point with all four arm lengths at least d.

1. Binary search the largest feasible d. If the check succeeds, move the lower bound upward. Otherwise move the upper bound downward.

### Why it works

For a fixed d, a horizontal segment is active at exactly those x-coordinates satisfying x 1 ​ +d≤x≤x 2 ​ −d. The sweep inserts it at the first such coordinate and removes it immediately after the last such coordinate. Consequently, at every processed vertical x, the Fenwick tree contains exactly the y-coordinates of horizontal segments that can support a plus of size d at that x.

The Fenwick query succeeds exactly when one of those horizontal segments has y inside [y 1 ​ +d,y 2 ​ −d]. That condition gives at least d units of vertical room on both sides of the intersection. Together with the horizontal activation condition, all four arms are at least d. Thus the feasibility check is exact.

Since feasibility for d implies feasibility for every smaller value, binary search returns the largest possible plus size.

## Python Solution

```
Python
```

The input phase stores each segment after normalizing its endpoints. The maximum possible answer is computed at the same time, which gives binary search a tight upper bound.

The two sorted copies of the horizontal segments are the key preprocessing optimization. `by_left` controls insertions, while `by_right` controls removals. Their order is valid for every candidate `d`, because adding the same value to all left endpoints and subtracting the same value from all right endpoints preserves their relative order.

Each call to `check` creates a fresh Fenwick tree. This avoids a subtle cleanup problem that can occur if a successful check exits early while leaving old frequencies in the tree. A fresh tree also keeps the correctness argument simple.

The insertion condition uses `x1 + d <= x`. The removal condition uses `x2 - d < x`. These inequalities make the active interval exactly inclusive at both ends. Reversing either boundary would incorrectly reject a plus whose arm has exactly length `d`.

The Fenwick tree uses the actual y-coordinate as its index. Since coordinates are at most 10 5, no coordinate compression is necessary. Python integers also have no overflow issue for the Fenwick counts.

## Worked Examples

### Sample 1

The input is

```

```

Consider d=2. The three horizontal segments have lengths 4,2,6, so the first and third can potentially support this value. The two vertical segments have lengths 4,3, so both are candidates.

The sweep behaves as follows.

| Vertical segment | x | Inserted horizontal y values | Removed horizontal y values | Query range | Result |
| --- | --- | --- | --- | --- | --- |
| [1,5] | 3 | y=3 from [1,5] | none | [3,3] | found |
| [6,9] | 2 | not reached in x order | none | [8,7] | not needed |

The first vertical segment at x=3 intersects the horizontal segment from x=1 to x=5, also at y=3. Its four arm lengths are 2,2,2,2, so d=2 is feasible.

Trying d=3 fails because the first horizontal segment has length only 4, while the third horizontal segment is at y=6 and does not intersect the relevant vertical segment with enough room. Thus the answer is `2`.

### Constructed Example 2

Consider

```

```

The horizontal segment is [1,9] at y=5, and the vertical segment is [3,7] at x=5. Their intersection is (5,5).

| Candidate d | Horizontal trimmed interval | Vertical trimmed interval | Intersection | Feasible |
| --- | --- | --- | --- | --- |
| 1 | [2,8] | [4,6] | (5,5) | yes |
| 2 | [3,7] | [5,5] | (5,5) | yes |
| 3 | [4,6] | [6,4] | empty | no |

The maximum value is `2`. This trace demonstrates why the vertical interval must be trimmed on both ends and why a segment of total length exactly 2d is still valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N+M)logClogC) | Each binary-search check performs O(N+M) Fenwick operations, each taking O(logC), and there are O(logC) candidate values. |
| Space | O(N+M+C) | The segments, two sorted horizontal orders, sorted vertical segments, and one Fenwick tree are stored. |

With C≤10 5, binary search needs at most about 17 iterations. The solution avoids the 10 10 pair enumeration of brute force and uses only linear-size storage, fitting the stated memory bound.

## Test Cases

```python
Pythonimport sysimport io

def solution(data: str) -> str:    it = iter(data.split())    t = int(next(it))    answers = []
    for _ in range(t):        n = int(next(it))        m = int(next(it))
        horizontal = []        vertical = []        hi = 0        max_coord = 0
        for _ in range(n):            x1 = int(next(it))            x2 = int(next(it))            y = int(next(it))            if x1 > x2:                x1, x2 = x2, x1            horizontal.append((x1, x2, y))            hi = max(hi, (x2 - x1) // 2)            max_coord = max(max_coord, x2, y)
        for _ in range(m):            y1 = int(next(it))            y2 = int(next(it))            x = int(next(it))            if y1 > y2:                y1, y2 = y2, y1            vertical.append((y1, y2, x))            hi = max(hi, (y2 - y1) // 2)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | `2` | Official example and ordinary intersection handling |
| One-point horizontal and vertical segments | `0` | Minimum-size segments and zero answer |
| `[1,9]` with `[3,7]` | `2` | Exact centered optimum and binary search |
| `[1,3]` with vertical segment at x=1 | `0` | Intersection at an endpoint |
| Two identical horizontal segments | `2` | Duplicate y-coordinates and Fenwick frequencies |
| 10 5 identical long segments | `49999` | Maximum input size and performance |

## Edge Cases

For a zero-length segment, consider

```
11 11 1 11 1 1
```

The initial upper bound is zero because both segments have half-length zero. Binary search immediately returns zero. The algorithm never tries to manufacture a positive arm from a segment that cannot contain one.

For an endpoint intersection, consider

```
11 11 3 22 4 1
```

The horizontal segment can support d=1 only at x=2, but the vertical line is at x=1. For d=1, the horizontal trimmed interval is [2,2], so the sweep never activates that horizontal segment when processing x=1. The check fails and the answer remains zero.

For duplicate coordinates, consider

```
12 11 5 31 5 31 5 3
```

For d=2, the horizontal segments are active from x=3 through x=3, and the vertical segment at x=3 queries y=3. The Fenwick tree contains a count of two at that coordinate. If one horizontal segment were removed, the count would become one rather than zero, which is why the implementation stores counts instead of booleans.

For segments whose lengths are exactly 2d, the trimmed interval consists of a single coordinate. Consider

```
11 11 5 31 5 3
```

For d=2, the horizontal trimmed interval is [3,3] and the vertical trimmed interval is [3,3]. Both segments are active at coordinate 3, so the answer is `2`. The inclusive insertion condition and strict removal condition are what preserve this valid boundary case.

For reversed endpoints, consider

```
11 19 1 57 3 5
```

Normalization changes the segments to [1,9] and [3,7], giving the same centered plus as the earlier example and an answer of `2`. Without normalization, subtracting endpoints directly could produce negative lengths and an invalid binary-search bound.
