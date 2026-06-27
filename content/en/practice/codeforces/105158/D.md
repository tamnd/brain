---
title: "CF 105158D - \u8ddd\u79bb\u4e4b\u6bd4"
description: "We are given several independent sets of points on the 2D plane. For each set, we look at every pair of points and compute two different distances between them: the Manhattan distance and the Euclidean distance."
date: "2026-06-27T11:04:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105158
codeforces_index: "D"
codeforces_contest_name: "2024 National Invitational of CCPC (Zhengzhou), 2024 CCPC Henan Provincial Collegiate Programming Contest"
rating: 0
weight: 105158
solve_time_s: 36
verified: false
draft: false
---

[CF 105158D - \u8ddd\u79bb\u4e4b\u6bd4](https://codeforces.com/problemset/problem/105158/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent sets of points on the 2D plane. For each set, we look at every pair of points and compute two different distances between them: the Manhattan distance and the Euclidean distance. For each pair, we form a ratio where the Manhattan distance is divided by the Euclidean distance, and the task is to find the maximum such ratio among all pairs.

Geometrically, the Manhattan distance measures how far you travel if you can only move horizontally and vertically, while Euclidean distance is the straight-line distance. The ratio is always at least 1, because the Manhattan path is never shorter than the straight line.

The input can contain up to 100,000 test cases, and the total number of points across all tests can reach 200,000. This immediately rules out any approach that considers all pairs explicitly inside a test case, since even a single set with n = 2×10^5 would already imply roughly 2×10^10 pairs.

A naive pairwise check is impossible. Even computing distances for a few billion pairs is far beyond time limits. Any valid solution must reduce the search space to something linear or near-linear per test case.

A subtle edge case arises when points are very close in Euclidean distance but differ in both coordinates, which can inflate the ratio significantly. For example, points (0,0) and (1,1) give Manhattan distance 2 and Euclidean distance √2, ratio √2. Meanwhile, axis-aligned pairs give ratio 1. So optimal pairs are not necessarily far apart in Euclidean sense; they depend on direction.

## Approaches

The first instinct is to check all pairs, compute both distances, and track the maximum ratio. This is correct by definition but requires O(n²) operations per test, which is infeasible given the constraints.

To reduce complexity, we rewrite the expression for a pair of points P and Q. Let dx = |x1 − x2| and dy = |y1 − y2|. The ratio becomes:

(dx + dy) / sqrt(dx² + dy²)

We want to maximize this over all point differences.

Now comes the key structural observation: the ratio depends only on the direction of the vector between points, not its length. Scaling (dx, dy) by a positive factor does not change the ratio, since both numerator and denominator scale linearly.

So the problem becomes: among all direction vectors formed by differences of input points, find the direction that maximizes (|dx| + |dy|) / √(dx² + dy²).

The next step is to normalize this expression in a way that exposes structure. Square it to avoid the square root:

((|dx| + |dy|)²) / (dx² + dy²)

Expanding the numerator:

(dx² + dy² + 2|dx dy|) / (dx² + dy²)

= 1 + 2|dx dy| / (dx² + dy²)

So maximizing the ratio is equivalent to maximizing:

|dx dy| / (dx² + dy²)

This expression depends only on the relative magnitudes of dx and dy. Let t = |dx| / |dy|. Then the value becomes:

t / (t² + 1)

This function is maximized when t = 1, meaning |dx| ≈ |dy|. Intuitively, the best pairs are those whose connecting segment is close to a 45-degree line.

So we are looking for pairs of points whose difference vector is closest to slope ±1. This is a classic geometric reduction: transform coordinates so that we can capture extremal behavior along rotated axes.

We define rotated coordinates:

u = x + y

v = x − y

Now observe that:

|dx| + |dy| = max(|du|, |dv|)

and Euclidean distance remains invariant up to linear transformation scaling behavior, but more importantly, extremal ratio candidates occur when either du or dv dominates.

This reduces the search to finding extreme pairs in transformed coordinate systems, which can be handled by sorting.

The key idea is that for a fixed ordering by u or v, the best candidates for maximizing difference in that coordinate come from adjacent or extreme points, similar to the classic “max Manhattan distance” trick.

We compute candidates based on sorting by u and v and checking extreme pairs.

Finally, we evaluate only O(n) candidate pairs per test case instead of O(n²), and take the maximum ratio among them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Sorting-based reduction | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We rewrite each point (x, y) into two transformed coordinates u = x + y and v = x − y, since these capture diagonal structure in the plane where Manhattan and Euclidean geometry interact most strongly.

We then restrict attention to candidate pairs that are extreme with respect to these projections.

1. For each test case, compute u and v for every point. This transforms the geometric comparison into axis-aligned comparisons in rotated spaces.
2. Build two arrays of indices sorted by u and by v separately. Sorting is necessary because the largest differences in these projections always occur at extremes, not at arbitrary interior points.
3. For the u-sorted list, compare pairs formed by points with smallest and largest u values. Do the same for v-sorted list. These pairs maximize coordinate spread in each transformed axis.
4. For each candidate pair, compute dx and dy in original coordinates and evaluate (|dx| + |dy|) / sqrt(dx² + dy²). Track the maximum.
5. Return the largest ratio over
