---
title: "CF 102623D - Disaster Recovery"
description: "We have an undirected graph with cities as vertices and proposed roads as edges. The cost of a road between cities x and y is the sum of two values attached to its endpoints, specifically the Fibonacci value of city x plus the Fibonacci value of city y."
date: "2026-08-01T08:56:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102623
codeforces_index: "D"
codeforces_contest_name: "2020 Lenovo Cup USST Campus Online Invitational Contest"
rating: 0
weight: 102623
solve_time_s: 90
verified: false
draft: false
---

[CF 102623D - Disaster Recovery](https://codeforces.com/problemset/problem/102623/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We have an undirected graph with cities as vertices and proposed roads as edges. The cost of a road between cities `x` and `y` is the sum of two values attached to its endpoints, specifically the Fibonacci value of city `x` plus the Fibonacci value of city `y`.

The first goal is to choose roads that connect every city while spending the minimum possible amount of money. This is exactly the minimum spanning tree problem. However, there is an additional requirement: among all minimum-cost spanning trees, we must choose one whose largest city degree is as small as possible. The output is this smallest possible maximum degree.

The important structure comes from the special form of the edge weights. The Fibonacci values increase with the city index, and the weight of an edge is determined only by its two endpoints. The constraints allow up to `100000` cities and `200000` roads. A quadratic algorithm would already be around `10^10` operations, which is far beyond the limit. We need something close to linear or `O(m log n)`.

A common mistake is to build any minimum spanning tree and then measure its largest degree. That is not enough because different MSTs can have different degree distributions. Another mistake is to choose any edge that connects a new city to an already connected component. That can break the minimum-cost condition because a cheaper endpoint may exist inside the same component.

Consider this small example:

```
4 3
1 2
1 3
2 4
```

The answer is `2`.

When city 4 is added, it only has one possible connection, so its edge is forced. A method that tries to balance degrees without respecting edge weights may choose a different edge if one existed, but that could increase the total cost and no longer be an MST.

Another important case is when several edges connect the same new city to the same already connected component.

```
5 5
1 2
1 3
2 4
3 4
1 5
```

When city 4 is processed, both `(2,4)` and `(3,4)` connect the same component. The cheaper one must be chosen because the MST cost has priority. Only after fixing the cost can we use the remaining freedom to reduce degrees.

## Approaches

The direct approach is to run Kruskal's algorithm, sorting all edges by their Fibonacci-sum weights and building one MST. This is correct for finding the minimum cost because Kruskal always produces an MST.

However, it does not solve the whole problem. Equal-cost choices or different valid MST choices can lead to different maximum degrees, and trying all possible MSTs is impossible. In the worst case there can be exponentially many spanning trees.

The key observation is that the edge weight has a special ordering. For any edge `(u,v)` with `u < v`, its weight is dominated by the larger endpoint. Every edge whose larger endpoint is smaller than `v` is processed before every edge whose larger endpoint is larger than `v`. This means we can think about the MST construction city by city in increasing index order.

When city `v` is considered, all cities with smaller indices have already formed some connected components. Every edge involving `v` goes from `v` to one of those components. To keep the total cost minimal, for every previous component that must be connected to `v`, we have to choose the cheapest edge from `v` into that component. Since `v` is fixed, this means choosing the smallest indexed neighbor inside that component.

If several edges have the same cost, they are interchangeable for the MST cost. Only those ties matter for the second objective, so among equal candidates we choose the vertex with the currently smallest degree. This local choice is enough because future decisions only depend on the degree values inside each already-built component.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over MST choices | Exponential | O(n+m) | Too slow |
| Kruskal plus secondary handling | O(m log m) | O(n+m) | Accepted |

## Algorithm Walkthrough

1. Group every road by its larger endpoint. When processing city `v`, only roads ending at `v` are needed because all roads with smaller larger endpoints have already been handled.
2. Maintain a disjoint set union structure for the cities with indices smaller than or equal to the current city. The components represent which old cities are already connected in the partial MST.
3. Process cities from `1` to `n`. For the current city `v`, inspect every neighbor with a smaller index. Find the DSU component of that neighbor.
4. For every component adjacent to `v`, keep only the best candidate edge. The best candidate is the one whose other endpoint has the smallest index, because that gives the smallest Fibonacci value and therefore the cheapest edge. If several candidates have the same index, use the one with smaller current degree.
5. Add one chosen edge from `v` to each adjacent component. Increase the degree of both endpoints. The number of chosen edges is exactly the number of old components that `v` has to merge with.
6. Merge `v` and all touched components in the DSU. The partial tree is now correct for the prefix ending at `v`.
7. After all cities are processed, the answer is the largest degree among all cities.

The invariant is that after processing city `v`, the chosen edges form a minimum-cost spanning forest of the graph induced by cities `1` through `v`. The only choices that can affect the final degree distribution are edges with equal cost, because choosing a more expensive edge would violate the primary objective. Among those equal-cost choices, selecting the currently least-loaded endpoint keeps the maximum degree as small as possible.

The next part contains the implementation, proof details, examples, tests, and complexity discussion.
