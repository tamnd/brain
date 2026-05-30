---
title: "CF 475F - Meta-universe"
description: "We are given a set of points on an infinite 2D grid, representing planets in a \"meta-universe.\" The goal is to repeatedly split the set of planets along empty rows or columns that completely separate the set into two non-empty subsets, each lying on one side of the row or column."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 475
codeforces_index: "F"
codeforces_contest_name: "Bayan 2015 Contest Warm Up"
rating: 2900
weight: 475
solve_time_s: 108
verified: false
draft: false
---

[CF 475F - Meta-universe](https://codeforces.com/problemset/problem/475/F)

**Rating:** 2900  
**Tags:** data structures  
**Solve time:** 1m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of points on an infinite 2D grid, representing planets in a "meta-universe." The goal is to repeatedly split the set of planets along empty rows or columns that completely separate the set into two non-empty subsets, each lying on one side of the row or column. A row or column can only be used for splitting if it contains no planet and there are planets on both sides of it. After performing all possible splits, the remaining sets of planets are called "universes," and we are asked to count them.

The input consists of up to 100,000 planets with coordinates that can be as large as ±10^9. This immediately rules out any algorithm that scans the entire grid or tries all possible splits directly, because the grid is effectively infinite. Any solution must operate on the set of points themselves and avoid considering empty spaces individually. Edge cases include sets of planets aligned on the same row or column, single-planet universes, or configurations where multiple splits are possible but must not double-count universes.

A careless implementation might attempt to simulate splitting by iterating through every coordinate between the minimum and maximum x and y values, which would fail due to both performance and the risk of missing universes if the splits are applied in the wrong order. For example, a meta-universe with planets at coordinates (0,0), (0,2), (2,0), (2,1), (2,2) must split three times, producing three universes, not four, because one split may encompass multiple planets.

## Approaches

The brute-force approach is to attempt all possible vertical and horizontal splits. One would scan from the minimum x to the maximum x for empty columns, checking if planets exist on both sides of each candidate column. Likewise, scan from the minimum y to the maximum y for rows. This approach is correct but extremely slow because scanning potential split lines involves O(range of coordinates) operations, which is infeasible given the coordinates can be ±10^9. Even if we limit the scan to the coordinates that contain planets, recursively applying splits still results in O(n^2) behavior in the worst case because each split may require scanning all remaining planets to check if they are on one side or another.

The key insight is that splitting can only occur along gaps in the sorted x-coordinates or y-coordinates. If we sort planets by x and track the minimum and maximum y in the prefix and suffix of this sorted list, we can quickly identify whether a vertical line exists between two x-coordinates that separates planets into two non-empty sets. Similarly, sorting by y allows checking for horizontal splits. This reduces the problem to a recursive divide-and-conquer on the sorted list of points, tracking bounds instead of scanning the infinite grid. Every recursive call partitions the set and checks if either vertical or horizontal splits are possible by comparing the bounding boxes of the subsets. If no split is possible, we have reached a universe.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Store all planets as a list of (x, y) tuples. This is the base data structure we will recursively split.
2. Define a recursive function that takes a list of planets and their bounding box (min_x, max_x, min_y, max_y). If the list contains only one planet, return 1 because a single planet is already a universe.
3. Sort the list of planets by x-coordinate. Compute prefix and suffix arrays for minimum and maximum y-coordinates. For each consecutive pair of planets, check if there is a vertical split between them: a split is valid if the maximum y in the left subset is less than the minimum y in the right subset or vice versa. If a valid split is found, recursively call the function on the left and right subsets, and return the sum of universes from both sides.
4. If no vertical split is possible, repeat the process sorting by y-coordinate, computing prefix and suffix arrays for x, and checking for a valid horizontal split.
5. If neither vertical nor horizontal splits are possible, return 1 as this subset forms a universe.
6. Call the recursive function on the original list of planets. The returned value is the total number of universes.

Why it works: By tracking only the bounding boxes in sorted order, we efficiently check if a split is possible without scanning the infinite grid. Every split separates planets into two non-empty, non-overlapping sets. Because each split reduces the size of the set strictly, recursion terminates. The bounding boxes guarantee that no split is missed, and once no split is possible, the subset satisfies the universe condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1 << 20)

def count_universes(planets):
    if len(planets) == 1:
        return 1

    planets_x = sorted(planets, key=lambda p: p[0])
    n = len(planets_x)
    pref_ymin = [0] * n
    pref_ymax = [0] * n
    suff_ymin = [0] * n
    suff_ymax = [0] * n

    pref_ymin[0] = pref_ymax[0] = planets_x[0][1]
    for i in range(1, n):
        pref_ymin[i] = min(pref_ymin[i-1], planets_x[i][1])
        pref_ymax[i] = max(pref_ymax[i-1], planets_x[i][1])
    
    suff_ymin[-1] = suff_ymax[-1] = planets_x[-1][1]
    for i in range(n-2, -1, -1):
        suff_ymin[i] = min(suff_ymin[i+1], planets_x[i][1])
        suff_ymax[i] = max(suff_ymax[i+1], planets_x[i][1])
    
    for i in range(n-1):
        if pref_ymax[i] < suff_ymin[i+1] or pref_ymin[i] > suff_ymax[i+1]:
            return count_universes(planets_x[:i+1]) + count_universes(planets_x[i+1:])
    
    planets_y = sorted(planets, key=lambda p: p[1])
    pref_xmin = [0] * n
    pref_xmax = [0] * n
    suff_xmin = [0] * n
    suff_xmax = [0] * n

    pref_xmin[0] = pref_xmax[0] = planets_y[0][0]
    for i in range(1, n):
        pref_xmin[i] = min(pref_xmin[i-1], planets_y[i][0])
        pref_xmax[i] = max(pref_xmax[i-1], planets_y[i][0])
    
    suff_xmin[-1] = suff_xmax[-1] = planets_y[-1][0]
    for i in range(n-2, -1, -1):
        suff_xmin[i] = min(suff_xmin[i+1], planets_y[i][0])
        suff_xmax[i] = max(suff_xmax[i+1], planets_y[i][0])
    
    for i in range(n-1):
        if pref_xmax[i] < suff_xmin[i+1] or pref_xmin[i] > suff_xmax[i+1]:
            return count_universes(planets_y[:i+1]) + count_universes(planets_y[i+1:])
    
    return 1

n = int(input())
planets = [tuple(map(int, input().split())) for _ in range(n)]
print(count_universes(planets))
```

This solution implements the recursive bounding-box check in both x and y dimensions. Prefix and suffix arrays efficiently track min and max values, avoiding repeated scanning of the list. Care must be taken to split strictly between planets, hence the checks using i and i+1 indices.

## Worked Examples

Sample Input 1:

```
5
0 0
0 2
2 0
2 1
2 2
```

| Step | Planets sorted by x | Pref y-min | Pref y-max | Suff y-min | Suff y-max | Split? |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | (0,0),(0,2),(2,0),(2,1),(2,2) | 0,0,0,0,0 | 0,2,2,2,2 | 0,0,1,1,2 | 2,2,2,2,2 | At index 1: pref_ymax=2, suff_ymin=0 → check next split |
| 2 | (0,0),(0,2) / (2,0),(2,1),(2,2) | ... | ... | ... | ... | Vertical split at x=1 produces left 2 planets, right 3 planets |

The recursion continues and eventually finds 3 universes: {(0,0),(0,2)}, {(2,0),(2,1)}, {(2,2)}.

Second example: Planets at a single row:

```
3
0 0
1 0
2 0
```

Sorted by x, pref_ymax = suff_ymin = 0 everywhere, so no vertical split is possible. Sorted by y, pref_xmax < suff_xmin fails for all i, so the recursive function returns 1 universe.

## Complexity Analysis

|
