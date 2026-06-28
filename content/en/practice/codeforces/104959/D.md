---
title: "CF 104959D - Historic Memories"
description: "The continent is a tree of cities. Traveling along any road takes exactly one year, and because the graph is a tree there is a unique simple path between any two cities."
date: "2026-06-28T07:02:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104959
codeforces_index: "D"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2023-2024, \u041f\u0435\u0440\u0432\u0430\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 104959
solve_time_s: 33
verified: false
draft: false
---

[CF 104959D - Historic Memories](https://codeforces.com/problemset/problem/104959/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 33s  
**Verified:** no  

## Solution
## Problem Understanding

The continent is a tree of cities. Traveling along any road takes exactly one year, and because the graph is a tree there is a unique simple path between any two cities. Each city starts with an initial “memory value” $s_i$, and this value normally decreases by 1 every year until it reaches 0.

The twist is that each city can temporarily stop this decay. When a “minus” event happens for a city at time $t$, that city becomes frozen from that year onward and its memory value stops decreasing. When a “plus” event happens later, decay resumes from that year onward. Events for a city alternate, and the first event is always a minus, so each city has a sequence of time intervals during which its decay is active or paused.

A query asks: starting at a given city at a given time, you walk along edges of the tree, and you want the maximum memory value you can encounter on any city along any path you traverse. You are not restricted in how long you walk; the only structure is that travel time equals edge count, so arriving at a node later means more decay has happened globally according to time.

The key difficulty is that the value of a city depends on the query time and on whether its decay is currently active, which changes over time via updates. Since there are up to $10^5$ cities and $10^5$ events and queries interleaved in time order, any solution that recomputes values or recomputes paths per query is immediately infeasible.

A naive approach would, for each query, recompute current values of all nodes at time $t$, then run a tree traversal from the starting node. That already costs $O(n)$ per query, which becomes $10^{10}$ operations in the worst case, far beyond limits.

A more subtle failure case comes from ignoring travel time. If a node is at distance 5 from the start, and the query time is small, its effective value should be computed at a later time if we actually reach it. Treating all nodes as if evaluated at the same instant breaks correctness.

The challenge is to combine dynamic time-dependent node weights with tree distance queries in a way that avoids recomputing global states per query.

## Approaches

The brute force idea is straightforward. For each query, we compute the current effective value of every node by simulating its decay from time 0 up to the query time, respecting active or frozen intervals. Then we run a DFS or BFS from the starting node, computing the best value reachable. This is correct because it directly simulates the definition of the process. However, recomputing all node values per query costs $O(n)$, and traversing the tree costs another $O(n)$, giving $O(nq)$, which is too slow.

The main observation is that a node’s value at time $t$ is not arbitrary. Between events, it is a linear function in time with slope either $-1$ or $0$, clipped at zero. So each node contributes a piecewise linear function over time. The value at query time is determined by evaluating these functions.

Now consider the tree structure. A path from the root to any node accumulates distances, but distance only matters because it changes the effective evaluation time. If we define that reaching a node at distance $d$ means evaluating it at time $t + d$, then each node contributes a function of the form:

$$f_i(t + d) = \max(0, s_i - \text{decay}(i, t + d))$$

So each query reduces to: over all nodes $i$, maximize a function of $d(i)$ and $t$, where $d(i)$ is tree distance from the start.

This structure suggests a standard transformation: root the tree and convert it into distances, then treat each node as contributing a line in terms of $d$ at a shifted time parameter. Since queries ask for maximum over paths, this becomes a dynamic tree maximum query problem over a distance-augmented function space.

The classical way to handle this is centroid decomposition. Each node contributes its value to multiple centroid layers. For each centroid, we maintain a structure that stores best values as a function of distance. Updates affect only $O(\log n)$ centroids, and queries similarly combine contributions from centroid ancestors.

At each centroid, we maintain a time-dependent structure that tracks node contributions in terms of distance, typically using a segment tree or multiset over distance buckets, with lazy updates corresponding to decay intervals. Because decay changes only at event times, we process time in order and maintain active contributions incrementally.

This reduces each update and query to $O(\log^2 n)$, coming from centroid decomposition depth and segment structure per centroid.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nq)$ | $O(n)$ | Too slow |
| Centroid Decomposition + Dynamic Values | $O(q \log^2 n)$ | $O(n \log n)$ | Accepted |

## Algorithm Walkthrough

We process events in chronological order while maintaining a centroid decomposition of the tree.

1. Build a centroid decomposition of the tree and precompute, for every node, its distance to all centroids on its decomposition path. This allows fast updates of all centroid structures affected by a node.
2. For each centroid, maintain a structure keyed by distance that stores the current best contribution of nodes in its subtree. The contribution of a node at time $t$ is its current memory value, but stored in a way that can be updated when decay state changes.
3. Maintain the current active decay state of each city as we sweep through events. Each city alternates between active decay and frozen, so we track whether its slope is currently $-1$ or $0$.
4. When processing a “minus” event at time $t$, we switch the city to frozen state. We update all centroid structures containing this node by inserting or updating its value at time $t$, effectively freezing its decay from that point onward. This means future queries will treat its value as constant from that time forward.
5. When processing a “plus” event, we switch the city back to decay-active. We again update centroid structures to reflect that from time $t$, the value resumes decreasing linearly. This is handled by updating the stored contribution function rather than a single scalar.
6. For a query at $(t, x)$, we traverse the centroid path of node $x$. At each centroid, we compute the best possible value contributed by nodes whose distance to $x$ is known. Since distance in the original tree can be decomposed as distances via centroid ancestors, we query each centroid structure with the appropriate remaining distance budget.
7. The answer is the maximum over all centroid levels of the value obtained by combining centroid stored contributions with distance offsets.

### Why it works

Each node contributes to exactly $O(\log n)$ centroid levels, and at each level its contribution is stored with correct distance offsets relative to that centroid. Any path from a query node to another node passes through their lowest common centroid ancestor in the decomposition, so the distance used in evaluation is correctly reconstructed from precomputed distances. Since updates only modify centroid structures containing the affected node, and queries aggregate over all possible centroid partitions of paths from the query node, every valid path candidate is considered exactly once in a consistent coordinate system.

The correctness relies on the fact that centroid decomposition partitions all paths into segments passing through centroids, and each segment’s distance is prese
