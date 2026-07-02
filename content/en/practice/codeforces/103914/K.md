---
title: "CF 103914K - Symmetry: Convex"
description: "We are given a strictly convex polygon with vertices listed in counterclockwise order. From this polygon, we look at a growing sequence of prefixes: the polygon formed by the first 3 vertices, then the first 4, and so on until all n vertices."
date: "2026-07-02T07:28:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103914
codeforces_index: "K"
codeforces_contest_name: "Heltion Contest 1"
rating: 0
weight: 103914
solve_time_s: 23
verified: false
draft: false
---

[CF 103914K - Symmetry: Convex](https://codeforces.com/problemset/problem/103914/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a strictly convex polygon with vertices listed in counterclockwise order. From this polygon, we look at a growing sequence of prefixes: the polygon formed by the first 3 vertices, then the first 4, and so on until all n vertices. For each prefix polygon, we must determine all straight lines that act as axes of symmetry of that polygon.

A line is considered a valid answer if reflecting the polygon with respect to that line maps the polygon onto itself. Because the polygon is convex and vertices are given in order, symmetry is entirely determined by how vertex indices are paired under reflection.

The output is not a single value per prefix but potentially multiple lines. For each i, we must output every symmetry axis of the polygon formed by vertices p1 through pi.

The constraints are very large: the total number of vertices over all test cases is up to 3 · 10^5, and T can be as large as 10^5. This immediately rules out any approach that recomputes symmetries from scratch for each prefix in quadratic or even linear time per prefix. Even O(n^2) total over all test cases would be too slow.

A key structural difficulty is that each prefix polygon is not independent. When a new vertex is added, symmetry can only be preserved or destroyed, and any valid symmetry must align with the circular structure of the vertex sequence.

A naive mistake is to assume that every prefix might have many symmetries and try to test all possible reflection axes by pairing points. For example, a regular polygon prefix might have multiple symmetries, but an arbitrary convex prefix usually has none beyond accidental ones.

Another subtle edge case arises when early prefixes are degenerate in symmetry while later ones lose all symmetry. For instance, a triangle (i = 3) always has up to 3 reflection axes depending on geometry, but adding a fourth arbitrary convex point usually reduces symmetry to at most 1 or 0 axes. Any solution that recomputes independently per prefix will time out immediately.

## Approaches

A direct brute-force approach would treat each prefix Ci independently. For a fixed i, we could try every pair of vertices and attempt to define a candidate reflection axis as the perpendicular bisector of that pair, then verify whether reflecting all vertices preserves the set. This is already O(i^3) in the worst case if done carefully, because for each candidate axis we must validate all points.

Even if optimized, checking symmetry of a convex polygon for one axis is O(i), and there are O(i) candidate axes derived from pairs of points, leading to O(i^2) per prefix and O(n^3) total across all prefixes. This is far beyond the limit.

The key structural observation is that symmetry of a convex polygon is extremely rigid. Any reflection symmetry must map the ordered cycle of vertices onto itself. This implies that if a symmetry exists, it acts as an involution on indices, pairing vertices symmetrically around some axis. In a convex polygon, such an involution is fully determined by a “center” position in the cyclic order: either a vertex maps to a vertex (axis through opposite vertices) or an edge maps to an edge (axis through midpoints).

Now consider adding vertices on
