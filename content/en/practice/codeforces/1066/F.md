---
title: "CF 1066F - Yet another 2D Walking"
description: "We are given a set of points in the first quadrant of the grid, and Maksim starts at the origin. In one move he can step to any of the four neighboring lattice points, so every move costs one unit of Manhattan distance. The key restriction is not geometric but structural."
date: "2026-06-15T08:13:18+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 1066
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 515 (Div. 3)"
rating: 2100
weight: 1066
solve_time_s: 282
verified: true
draft: false
---

[CF 1066F - Yet another 2D Walking](https://codeforces.com/problemset/problem/1066/F)

**Rating:** 2100  
**Tags:** dp  
**Solve time:** 4m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of points in the first quadrant of the grid, and Maksim starts at the origin. In one move he can step to any of the four neighboring lattice points, so every move costs one unit of Manhattan distance.

The key restriction is not geometric but structural. The points are grouped by their “level”, defined as the maximum of their coordinates. Level 1 contains points that lie inside or on the square from the origin up to 1 in either direction, level 2 extends that square to size 2, and so on. Maksim must visit all points in increasing order of these levels, and he is not allowed to start visiting any point of level k+1 until every point of level k has been visited.

So the problem becomes: we must choose an order of visiting points that respects this layered constraint, and we want to minimize total Manhattan travel distance starting from (0, 0).

The constraints are large, with up to 200,000 points and coordinates up to 10^9. Any solution that tries to build a graph between all points or run shortest path algorithms over states is immediately impossible. Even sorting all pairs or doing per-step shortest path computations would be too slow. We need something that reduces the structure to a linear or near-linear sweep over levels.

A subtle failure case appears when points of the same level are scattered in a way that makes greedy ordering look tempting. For example, points at level 3 like (3, 0), (0, 3), and (3, 3) can mislead a naive approach that tries to connect nearest neighbors locally. Locally optimal transitions can increase the cost across level boundaries, which is where the true constraint forces a global decision.

## Approaches

A brute-force interpretation is to think of this as a shortest path problem over states that include which points have been visited and the current position. That would imply a state space of size 2^n or at least n! permutations, both completely infeasible. Even if we restrict ourselves to visiting points in level order, we still have to decide the best ordering inside each level. That already resembles a traveling salesman problem, which is not solvable exactly at this scale.

The key simplification comes from the geometry of Manhattan distance combined with the level constraint. Since levels are defined by max(x, y), each level k consists of points lying on the boundary of the square [0, k] × [0, k], with at least one coordinate equal to k. The crucial observation is that movement inside a level does not affect future levels except through the final exit point of that level and the entry point into the next level.

So for each level, we only care about how we traverse its boundary points and where we end up when leaving the level. The structure of Manhattan distance implies that optimal movement within a level can be reduced to maintaining only two extreme states: the best cost of finishing at the left-bottom-most side versus the right-top-most side of the level boundary ordering induced by sorting.

This transforms the problem into a sweep over increasing levels, maintaining a small dynamic programming state per level. For each level, we sort its points by one coordinate and compute transitions that simulate walking along the boundary in either direction. The DP keeps track of the minimal cost to finish processing all points up to a level and end at one of two representative boundary positions.

The brute force fails because it tries to reason about individual point-to-point transitions, while the correct solution compresses each level into a structured path problem with only two meaningful exit configurations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (TSP-like over all points) | O(n!) | O(n) | Too slow |
| Level DP with boundary compression | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We group all points by their level k = max(x, y). Each group is processed independently in increasing order of k.

1. Compute the level for each point and store points in a dictionary keyed by level.

This ensures we process constraints in the exact order required by the problem.
2. Sort all distinct levels in increasing order.

The constraint forbids skipping ahead, so this ordering defines the global structure of the walk.
3. For each level, sort its points by x-coordinate, and use y as tie-breaker.

This ordering aligns points along the boundary so that Manhattan transitions inside the level become monotone.
4. Maintain a dynamic programming state with two values: the minimum cost to finish processing up to the previous level and end at either the “leftmost” or “rightmost” boundary endpoint of that level’s traversal.

These two states capture all meaningful ways the walk can exit a level because any interior ending position can be mapped to one of these extremes without increasing future cost.
5. For each level, compute the cost of traversing all its points starting from each of the two DP states from the previous level.

For each start state, simulate two possible traversal directions of the sorted points (left-to-right and right-to-left), accumulating distances between consecutive points.
6. After computing both traversal directions, update the DP for the current level by taking minimum over all transitions and recording the resulting two possible endpoints.

This preserves optimal substructure: once a level is completed, only its exit position matters.
7. After processing all levels, return the minimum DP value over the two possible final endpoints.

### Why it works

Inside each level, the points lie on the boundary of a growing square. Any optimal path that visits all points in that level can be transformed into a monotone walk along the boundary without increasing cost, because detours inside the square can always be shortcut using Manhattan geometry. This reduces each level to a one-dimensional ordering problem with only two directions. The DP preserves optimality because transitions between levels depend only on the endpoint of the previous level, not the internal path used to reach it.

## Python Solution

```
PythonRun
```

The implementation groups points by level using a hash map, then processes levels in increasing order. The DP state is intentionally kept small: two costs and two endpoint representatives. The helper distance function encodes Manhattan movement directly, which is sufficient since no other metric is involved.

A subtle point is that we always consider both traversal directions of each level. Missing one direction breaks correctness because optimal entry direction depends on how the previous level ended.

## Worked Examples

### Example 1

Input:

```

```

Levels:

(1,1), (1,2),(2,1)

| Step | Level | Start | Order | Cost | End |
| --- | --- | --- | --- | --- | --- |
| 0 | - | (0,0) | - | 0 | (0,0) |
| 1 | 1 | (0,0) | (1,1) | 2 | (1,1) |
| 2 | 2 | (1,1) | (1,2)->(2,1) | 3 | (2,1) |

Total = 5.

This trace shows how the algorithm compresses each level into a single traversal, carrying only endpoint information forward.

### Example 2

Input:

```

```

All points are in level 2.

| Step | Level | Start | Order | Cost | End |
| --- | --- | --- | --- | --- | --- |
| 0 | - | (0,0) | - | 0 | (0,0) |
| 1 | 2 | (0,0) | (1,1)->(1,2)->(2,1)->(2,2) | 6 | (2,2) |

This case demonstrates that within a single level, the algorithm effectively reduces the problem to a linear traversal over the sorted boundary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting points within each level dominates total work |
| Space | O(n) | Storage of points grouped by level and DP state |

The solution fits comfortably within limits because each point is sorted once and processed in constant DP transitions.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point | 2 | base movement from origin |
| line on same y | 5 | monotone traversal correctness |
| full 2x2 square | 6 | boundary compression correctness |

## Edge Cases

A key edge case is when all points belong to the same level. In that situation, the algorithm reduces to a single sweep over sorted boundary points starting from the origin. The DP does not rely on transitions between levels, so correctness depends entirely on the internal traversal logic. The example with a 2x2 square confirms that both traversal directions are considered and the minimal one is chosen.

Another edge case occurs when levels are sparse, for example a single point per level. Here the DP degenerates into repeatedly choosing the cheapest transition between isolated points. Since each level has only one valid traversal, both forward and backward costs coincide, so the algorithm naturally reduces to summing Manhattan distances between successive level representatives.
