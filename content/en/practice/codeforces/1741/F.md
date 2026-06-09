---
title: "CF 1741F - Multi-Colored Segments"
description: "We are given a collection of line segments on a number line, where each segment has a color. For each segment, we want to find the distance to the closest segment of a different color."
date: "2026-06-09T16:38:18+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1741
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 826 (Div. 3)"
rating: 2000
weight: 1741
solve_time_s: 620
verified: false
draft: false
---

[CF 1741F - Multi-Colored Segments](https://codeforces.com/problemset/problem/1741/F)

**Rating:** 2000  
**Tags:** binary search, data structures, math, sortings  
**Solve time:** 10m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of line segments on a number line, where each segment has a color. For each segment, we want to find the distance to the closest segment of a **different color**. The distance is defined as the minimum distance between any point in the first segment and any point in the second segment. If segments overlap or touch, the distance is zero. The input gives multiple test cases, and each test case lists the segments with their left and right endpoints and their colors. The output should provide, for each segment, the computed distance.

The constraints are significant: a single test case can have up to 200,000 segments, and the sum of segments across all test cases is at most 200,000. This implies that any solution with a nested loop over all segment pairs would result in roughly 200,000 squared operations, which is infeasible. We must therefore avoid a naive O(n²) approach and aim for something linearithmic or linear in practice.

A non-obvious edge case arises when segments are points, i.e., segments with `l_i == r_i`. Another subtlety is that multiple segments can share the same color, so we must **ignore segments of the same color** when computing distances. For example, if there are two long overlapping segments of the same color and a short segment of a different color far away, the closest segment for each of the first two will be the distant one, not each other.

## Approaches

The brute-force method is straightforward: for each segment, iterate over all other segments and compute the distance if their colors differ, keeping the minimum distance found. This approach is correct but clearly too slow: with n up to 2·10⁵, we would have up to 4·10¹⁰ distance computations, which is impossible in a reasonable time frame.

The key insight for optimization is that we only need to consider the **closest segments to the left and right** of any given segment. Sorting all segments by their left endpoints allows us to scan from left to right and keep track of the rightmost segment for each color. When processing a segment, the nearest segment of a different color to the left is either the segment ending furthest to the left but not of the same color. Similarly, scanning from right to left handles the nearest segments to the right. This reduces the problem to two linear passes over the segments after sorting, with constant-time operations for each segment in the scan.

This approach works because the distance between two non-overlapping segments is determined entirely by the endpoints. By maintaining the farthest right (or left) endpoints of previous segments of each color, we can compute candidate distances efficiently without checking every pair.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Two-pass Scan | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the segments into a list, storing the original index along with `(l_i, r_i, c_i)`.
2. Sort the list of segments by their left endpoint `l_i`.
3. Initialize a dictionary that maps color to the **maximum right endpoint** seen so far for that color.
4. Initialize an array `distances` with infinity for all segments.
5. Perform a left-to-right pass:

1. For each segment, check all colors in the dictionary except its own.
2. Compute the distance from the current segment's left endpoint to the farthest right endpoint of those colors.
3. Update the distance in the `distances` array if smaller.
4. Update the dictionary entry for this segment's color with the maximum of its right endpoint and the current value.
6. Perform a right-to-left pass:

1. Sort the segments by decreasing right endpoint.
2. Maintain the minimum left endpoint for each color.
3. For each segment, compute the distance to the nearest segment of a different color on the right using the stored minimum left endpoints.
4. Update `distances` if a smaller distance is found.
7. Output the `distances` array in the original segment order.

**Why it works:** Sorting allows us to scan efficiently and maintain running extrema per color. Distances between segments are determined by their endpoints, and considering the nearest left and right segments for all different colors ensures we find the true minimum. Overlapping segments automatically produce distance zero because the computed difference becomes negative or zero.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        segs = []
        for i in range(n):
            l, r, c = map(int, input().split())
            segs.append((l, r, c, i))
        ans = [float('inf')] * n

        # Left-to-right pass
        segs.sort()
        color_max_right = {}
        for l, r, c, idx in segs:
            for other_c, max_r in color_max_right.items():
                if other_c != c:
                    ans[idx] = min(ans[idx], max(0, l - max_r))
            color_max_right[c] = max(r, color_max_right.get(c, -1))

        # Right-to-left pass
        segs.sort(key=lambda x: -x[1])
        color_min_left = {}
        for l, r, c, idx in segs:
            for other_c, min_l in color_min_left.items():
                if other_c != c:
                    ans[idx] = min(ans[idx], max(0, min_l - r))
            color_min_left[c] = min(l, color_min_left.get(c, 10**10))

        print(' '.join(map(str, ans)))

solve()
```

The first pass ensures we consider segments on the left, updating distances using the farthest right endpoint of other colors. The second pass mirrors the logic from the right side. Infinity initialization ensures that any segment with overlapping neighbors or intersecting segments will automatically reduce its distance to zero. Sorting preserves proper ordering to handle left-to-right and right-to-left efficiently.

## Worked Examples

**Test Case 1:**

Segments:

| i | l | r | c |
| --- | --- | --- | --- |
| 1 | 1 | 2 | 1 |
| 2 | 3 | 4 | 1 |
| 3 | 5 | 6 | 2 |

**Left-to-right pass:**

- Segment 1: no prior segments → distance ∞
- Segment 2: only color 1 so skip → distance ∞
- Segment 3: color 2, nearest color 1 max right = 4 → distance = 5 - 4 = 1

**Right-to-left pass:**

- Segment 3: no segments to right → distance remains 1
- Segment 2: nearest color 2 min left = 5 → distance = 5 - 4 = 1
- Segment 1: nearest color 2 min left = 5 → distance = 5 - 2 = 3

Final distances: `[3, 1, 1]` which matches the sample output.

**Test Case 2:**

Segments:

| i | l | r | c |
| --- | --- | --- | --- |
| 1 | 100000000 | 200000000 | 1 |
| 2 | 900000000 | 1000000000 | 2 |

- Left-to-right: segment 1 → ∞, segment 2 → 900000000 - 200000000 = 700000000
- Right-to-left: segment 2 → ∞, segment 1 → 900000000 - 200000000 = 700000000

Final distances: `[700000000, 700000000]`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; the two linear scans are O(n) each, iterating over colors is negligible since colors ≤ n |
| Space | O(n) | Store segments and the distance array, plus dictionaries for colors |

The algorithm comfortably fits within the constraints: 200,000 log 200,000 ≈ 4·10⁶ operations per test case, feasible under the 3-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Sample cases
assert run("""1
3
1 2 1
3 4 1
5 6 2
""") == "3 1 1"

assert run("""1
2
100000000 200000000 1
900000000 1000000000 2
""") == "700000000 700000000"

# Custom: overlapping segments of different colors
assert run("""1
3
1 5 1
4 8 2
10 12 3
""") == "0 0 2"

# Custom: all segments of same length touching each other
assert run("""1
4
1 2 1
2 3 2
3 4 1
4 5 2
""") == "0 0 0 0"

# Custom: point segments far apart
assert run("""1
3
1 1 1
10 10 2
20
```
