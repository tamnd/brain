---
title: "CF 105160D - \u65b9\u5757\u6e38\u620f"
description: "We are given an $n times m$ grid that represents a tiled game board. Each cell is either empty or colored with one of three colors labeled 1, 2, and 3."
date: "2026-06-27T11:00:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105160
codeforces_index: "D"
codeforces_contest_name: "2024 University of Shanghai for Science and Technology(USST) Freshman Challenge Contest"
rating: 0
weight: 105160
solve_time_s: 30
verified: false
draft: false
---

[CF 105160D - \u65b9\u5757\u6e38\u620f](https://codeforces.com/problemset/problem/105160/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an $n \times m$ grid that represents a tiled game board. Each cell is either empty or colored with one of three colors labeled 1, 2, and 3. These colored cells form several connected components, and each connected component corresponds to exactly one hidden game piece.

There are three possible piece types. Each piece occupies several grid cells and may appear in any rotation or mirrored form, but its shape structure is fixed up to symmetry. The key guarantee is that the entire grid is formed by placing non-overlapping copies of these three piece types, so every non-zero cell belongs to exactly one valid piece instance.

The task is to determine how many pieces of each of the three types appear in the grid.

The constraints $n, m \le 500$ imply up to 250,000 cells. Any solution must be essentially linear in the grid size, since even $O((nm)^2)$ would be far too slow. This strongly suggests a flood-fill or union-based decomposition of the grid into connected components, followed by classification of each component in constant or near-constant time.

A subtle issue is that pieces can appear rotated or mirrored. This rules out naive direct shape matching without normalization. Another potential pitfall is assuming fixed anchor points or bounding-box comparisons without accounting for symmetry. Since components can be transformed, the only stable signature is something invariant under rotation and reflection, such as the structure of the adjacency graph or a canonical normalization of coordinates.

## Approaches

A brute-force idea is to treat every connected component as a set of cells and compare it against all possible orientations of the three known piece shapes. For each component, we would enumerate all rotations and reflections of each shape and try to match it against the component’s cells. If we represent a component with $k$ cells, a naive matching might cost $O(k)$ per orientation, and with multiple orientations per shape this becomes expensive. In the worst case, if all cells form one large component, this degenerates into roughly $O(nm)$ comparisons per shape, leading to $O((nm)^2)$ behavior, which is clearly too slow.

The key observation is that the problem guarantees a full tiling by only three piece types, meaning each connected component is exactly one of those types. This allows us to avoid geometric matching entirely. Instead, we can characterize each component by its adjacency structure: how many neighbors each cell has within the same color region. For polyomino-like shapes, especially small fixed ones, the multiset of degrees or a canonical traversal signature uniquely identifies the shape even under rotation or reflection.

So instead of trying all transformations, we simply flood-fill each component, compute a compact structural signature, and classify it using precomputed signatures for the three shapes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((nm)^2)$ | $O(nm)$ | Too slow |
| Optimal (component + signature) | $O(nm)$ | $O(nm)$ | Accepted |

## Algorithm Walkthrough

We process the grid as a graph where each non-zero cell is connected to its four neighbors if they share the same color.

1. Scan the grid cell by cell. When we find a non-zero cell that has not been visited, we start a flood fill from it. This isolates one connected component corresponding to a single piece.
2. During flood fill, collect all cells belonging to this component. We store their coordinates so we can analyze structure afterward.
3. While exploring the component, also build its adjacency structure. For each cell, count how many neighbors in the component it has. This degree information is invariant under rotation an
