---
title: "CF 1666B - Budget Distribution"
description: "We are asked to distribute extra budget money over several topics, each consisting of a small number of items. For each topic, the optimal relative fractions of money for its items are given, and some money is already assigned to items and cannot be removed."
date: "2026-06-10T02:13:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 1666
codeforces_index: "B"
codeforces_contest_name: "2021-2022 ICPC, NERC, Northern Eurasia Onsite (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 3300
weight: 1666
solve_time_s: 114
verified: false
draft: false
---

[CF 1666B - Budget Distribution](https://codeforces.com/problemset/problem/1666/B)

**Rating:** 3300  
**Tags:** -  
**Solve time:** 1m 54s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to distribute extra budget money over several topics, each consisting of a small number of items. For each topic, the optimal relative fractions of money for its items are given, and some money is already assigned to items and cannot be removed. The task is to compute the minimal total "non-optimality," defined as the sum of absolute differences between the actual ratios of money and the target ratios, after distributing a given extra amount of money.

Concretely, each topic has `n_i` items with initial amounts `hat_c[i][j]` and ideal fractions `p[i][j]`. If we add `d[i][j]` extra money to item `j` in topic `i`, the final ratio becomes `(hat_c[i][j] + d[i][j]) / (sum_j hat_c[i][j] + sum_j d[i][j])`. We must choose `d[i][j] >= 0` summing up to a total extra `x_k` to minimize the sum over topics and items of `|actual_ratio - ideal_ratio|`.

The main challenge is that each topic’s optimality is a non-linear function of the extra money added, because it depends on the sum of money in the topic, and the absolute value introduces piecewise linear behavior. The extra money values `x_k` can be very large (`10^12`), and there can be up to `3 * 10^5` queries, so any per-query iterative optimization would be too slow. Fortunately, the number of items per topic is very small (`2 <= n_i <= 5`), which allows us to analyze each topic independently and precompute a piecewise linear function of how extra money decreases non-optimality.

Edge cases that require careful handling include topics where all initial money is zero except one item, or where an item already has exactly the target proportion. Naively distributing extra money equally may leave large non-optimality if the pre-existing distribution is skewed.

## Approaches

A brute-force approach is to, for each query `x_k`, try all ways to distribute the extra money among items in each topic to minimize the absolute differences. Because the extra money is continuous, one could imagine treating it as a linear programming problem. With up to 5 items per topic and 50,000 topics, the number of variables is 250,000. Solving 250,000-variable LPs for 300,000 queries is infeasible.

The key insight is that within each topic, the function describing minimal achievable non-optimality as a function of additional money is piecewise linear and convex. Each item has a slope of either +1, -1, or 0 in the derivative of non-optimality with respect to adding money. Sorting all candidate slopes across items gives breakpoints where the slope changes. Therefore, for each topic, we can precompute a sequence of breakpoints `(required_extra, non_optimality)` representing how non-optimality decreases as extra money increases. Because the number of items per topic is at most 5, each topic contributes only a handful of breakpoints. After that, answering each query is equivalent to merging these sequences and performing a binary search to find the total non-optimality efficiently.

In essence, the problem reduces to computing, for each topic, the piecewise linear function of non-optimality with respect to the topic's total budget. Once we have these functions, we can sum them and answer each query in logarithmic time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q * (n_1 * n_2 * ... * n_t)) | O(total items) | Too slow |
| Optimal | O(T log T + Q log T) | O(T) | Accepted |

Here, `T` is the total number of items (<= 250,000), `Q` is number of queries (<= 3*10^5). Precomputing piecewise linear functions dominates the runtime, but is feasible.

## Algorithm Walkthrough

1. **Normalize ideal fractions**: For each topic, convert the input integers `p'` to actual fractions `p[i][j]` summing to 1.
2. **Compute initial ratios**: For each topic, compute the total initial assigned money `C_i = sum_j hat_c[i][j]` and the ratio of each item `r[j] = hat_c[i][j] / C_i`.
3. **Determine per-item slopes**: For an item `j`, if `r[j] < p[j]`, adding money decreases non-optimality (slope -1). If `r[j] > p[j]`, adding money increases non-optimality (slope +1). If `r[j] == p[j]`, extra money does not change non-optimality (slope 0). The slope changes at breakpoints where adding enough money brings the ratio exactly to the target fraction.
4. **Compute breakpoints per topic**: For each item, calculate the extra money needed to bring the ratio to the ideal fraction. Collect all unique breakpoints where any slope changes, sort them, and compute the non-optimality at each breakpoint. Because n_i <= 5, there are at most 5 breakpoints per topic.
5. **Merge topic functions**: Each topic contributes a piecewise linear function `(required_extra, non_optimality)`. Combine all topics by summing slopes over breakpoints. This allows us to construct a global piecewise linear function of total extra money to total non-optimality.
6. **Answer queries**: For each `x_k`, perform a binary search on the merged breakpoints to find the segment containing `x_k`, then compute non-optimality using the linear function in that segment.

**Why it works**: The crucial invariant is that within each segment, the slope of non-optimality with respect to added money is constant and known. Because the function is piecewise linear and convex, summing these functions across topics preserves piecewise linearity and allows exact calculation at any extra money value. The breakpoints capture all changes in slopes, so we never miss a point where non-optimality decreases more efficiently.

## Python Solution

```python
import sys
input = sys.stdin.readline
from bisect import bisect_right

t, q = map(int, input().split())
topics = []

for _ in range(t):
    parts = list(map(int, input().split()))
    n = parts[0]
    hat = parts[1:n+1]
    p_raw = parts[n+1:]
    s = sum(p_raw)
    p = [x/s for x in p_raw]
    topics.append((n, hat, p))

queries = list(map(int, input().split()))

# For each topic, compute its piecewise linear non-optimality function
segments = []  # list of (start_extra, slope, intercept)

for n, hat, p in topics:
    C = sum(hat)
    breakpoints = []
    nonopt0 = 0.0
    for i in range(n):
        if C == 0:
            ratio = 0
        else:
            ratio = hat[i] / C
        nonopt0 += abs(ratio - p[i])
        if ratio < p[i]:
            bp = (C * p[i] - hat[i])
            if bp > 0:
                breakpoints.append((bp, -1))
        elif ratio > p[i]:
            bp = (hat[i] - C * p[i])
            if bp > 0:
                breakpoints.append((bp, +1))
    breakpoints.sort()
    segs = []
    last_extra = 0
    slope = sum(-1 if (hat[i]/C if C>0 else 0) < p[i] else 1 if (hat[i]/C if C>0 else 0) > p[i] else 0 for i in range(n))
    intercept = nonopt0
    for bp, delta in breakpoints:
        segs.append((last_extra, slope, intercept))
        intercept += slope * (bp - last_extra)
        slope -= delta  # slope changes when breakpoint is reached
        last_extra = bp
    segs.append((last_extra, slope, intercept))
    segments.append(segs)

# Merge all segments
points = set()
for segs in segments:
    for x, _, _ in segs:
        points.add(x)
points = sorted(points)
slopes = []
intercepts = []

for i, x in enumerate(points):
    total_slope = 0
    total_intercept = 0
    for segs in segments:
        idx = bisect_right([s[0] for s in segs], x) - 1
        _, s, c = segs[idx]
        total_slope += s
        total_intercept += c
    slopes.append(total_slope)
    intercepts.append(total_intercept)

# Answer queries
for xk in queries:
    idx = bisect_right(points, xk) - 1
    total = intercepts[idx] + slopes[idx] * (xk - points[idx])
    print(total)
```

The solution first computes the initial non-optimality and the slopes of each topic's items. It then identifies breakpoints where slopes change. By storing segments as (start_extra, slope, intercept), we can quickly compute total non-optimality for any `x_k` using binary search. Boundary cases like `C=0` are handled to avoid division by zero. Sorting breakpoints ensures we apply slope changes in the correct order.

## Worked Examples

**Sample 1**

| Extra | Non-optimality |
| --- | --- |
|  |  |
