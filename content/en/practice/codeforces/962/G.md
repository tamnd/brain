---
title: "CF 962G - Visible Black Areas"
description: "We are given a simple orthogonal polygon, meaning its edges are horizontal or vertical and it never self-intersects. The interior of this polygon is considered “black”. We also have a fixed axis-aligned rectangular window. The window is static and we look only through it."
date: "2026-06-17T01:45:02+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dsu", "geometry", "trees"]
categories: ["algorithms"]
codeforces_contest: 962
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 42 (Rated for Div. 2)"
rating: 2800
weight: 962
solve_time_s: 32
verified: false
draft: false
---

[CF 962G - Visible Black Areas](https://codeforces.com/problemset/problem/962/G)

**Rating:** 2800  
**Tags:** data structures, dsu, geometry, trees  
**Solve time:** 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a simple orthogonal polygon, meaning its edges are horizontal or vertical and it never self-intersects. The interior of this polygon is considered “black”. We also have a fixed axis-aligned rectangular window. The window is static and we look only through it.

Inside the window, parts of the polygon’s interior may appear as several disconnected black regions. The task is to count how many connected components of the polygon’s interior are visible within the window.

Connectivity is in the usual geometric sense: two points are connected if you can move between them while staying inside the black region, not crossing polygon boundaries, and staying inside the window.

The key difficulty is that the polygon can be large, and its interaction with the rectangle can split a single connected region into multiple visible components. This happens when the window cuts through corridors of the polygon or clips away connecting passages.

The constraints allow up to 15,000 vertices, and coordinates up to 15,000. This immediately rules out any approach that tries to rasterize the entire plane at high resolution and then run a naive flood fill over all cells, since the full grid would be quadratic in size and still need careful geometric clipping. A solution must operate close to linear or near-linear in the number of polygon edges, plus small overhead.

A subtle edge case appears when the window intersects the polygon boundary in such a way that thin corridors exist outside the window but are necessary to connect regions inside it. A naive approach that only considers visible polygon edges without correctly accounting for connectivity through clipped regions will incorrectly split components.

Another edge case is when the window fully contains a narrow passage that connects two large areas, but the passage is partially outside the polygon boundary within the window intersection. A local scan might incorrectly treat the two sides as separate components if it does not reconstruct true connectivity of the clipped interior.

## Approaches

A brute-force idea is to discretize the entire coordinate plane into unit cells and mark which ones lie inside the polygon. Then we intersect with the window and run a flood fill to count connected components. This is conceptually simple: point-in-polygon tests or scanline filling could mark interior cells, and BFS/DFS could count components.

However, the coordinate range goes up to 15,000 in both directions. A full grid would contain about 225 million cells, and even a linear scan over this grid is too slow and too memory-heavy. More importantly, building such a grid correctly for a polygon with up to 15,000 edges requires careful per-row intersection processing, which is itself expensive.

The key observation is that the polygon is axis-aligned and simple, which allows us to reduce the problem to a graph built from its edges and intersection structure with the window. Instead of reasoning over area, we reason over boundary segments and how they partition space inside the window.

We can treat the intersection of the polygon with the window as a planar subdivision problem restricted to a rectangle. The interior connectivity is determined by how polygon edges intersect the window boundary and how they form vertical and horizontal barriers.

A standard approach for orthogonal polygons is to compress the plane into a set of vertical and horizontal slabs defined by all polygon vertices and window boundaries. Inside this compressed structure, each cell is either inside or outside the polygon, and adjacency can be modeled via DSU or BFS over a sparse grid induced by edges.

However, a more efficient perspective is to treat polygon edges as obstacles and simulate connectivity of free space inside the window. We process vertical sweep lines over x-coordinates where events occur at polygon vertices and window boundaries. Between consecutive x-events, the vertical structure is fixed and can be processed via interval union over y-segments. DSU is used to maintain connectivity of vertical strips across x-slices.

The polygon being orthogonal ensures that edges alternate direction, so vertical and horizontal constraints form a grid-like graph. Each vertical slab contributes at most O(n) intervals, and DSU merges intervals that remain connected through horizontal edges.

This reduces the problem to maintaining connectivity of segments in a sweep line, where we track how polygon interior regions intersect the current vertical strip inside the window.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Grid + flood fill | O(W·H) | O(W·H |  |
