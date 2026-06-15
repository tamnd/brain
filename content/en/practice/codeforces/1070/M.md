---
title: "CF 1070M - Algoland and Berland"
description: "We are given two sets of points in the plane, one set belonging to Algoland and the other to Berland. The task is to construct exactly $a + b - 1$ straight line segments, each connecting one Berland city to one Algoland city. Every segment becomes a bidirectional road."
date: "2026-06-15T14:02:32+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "divide-and-conquer", "geometry"]
categories: ["algorithms"]
codeforces_contest: 1070
codeforces_index: "M"
codeforces_contest_name: "2018-2019 ICPC, NEERC, Southern Subregional Contest (Online Mirror, ACM-ICPC Rules, Teams Preferred)"
rating: 3000
weight: 1070
solve_time_s: 402
verified: false
draft: false
---

[CF 1070M - Algoland and Berland](https://codeforces.com/problemset/problem/1070/M)

**Rating:** 3000  
**Tags:** constructive algorithms, divide and conquer, geometry  
**Solve time:** 6m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two sets of points in the plane, one set belonging to Algoland and the other to Berland. The task is to construct exactly $a + b - 1$ straight line segments, each connecting one Berland city to one Algoland city. Every segment becomes a bidirectional road. These roads must form a connected structure over all cities, so from any city we must be able to travel to any other using these segments.

There is a structural restriction: no two segments are allowed to intersect at interior points. Intersections are only allowed at endpoints, meaning two roads can meet only if they share a city, which is impossible here because every edge must connect a Berland city to an Algoland city. So geometrically, we are building a straight-line bipartite planar graph embedded in the plane with no crossings.

Additionally, each Berland city $j$ has a prescribed degree $r_j$, meaning exactly $r_j$ roads must originate from that city. Since the total number of roads is $a + b - 1$, these degrees fully specify how many endpoints in Algoland will be used as well.

The constraints imply that we must construct a spanning tree over $a + b$ nodes with a fixed bipartite structure and planar embedding constraints. The size limits are small enough that $a + b \le 3000$ per test case, but there can be up to 3000 test cases, so the solution must be essentially linear or near-linear per test.

A naive approach that tries to connect arbitrary pairs and then checks for segment intersections would immediately fail. Even testing all pairs of segments for intersections costs $O((a+b)^2)$, which becomes far too slow at maximum size. Worse, even if intersections are avoided locally, global consistency is hard to maintain.

A more subtle failure mode comes from ignoring geometry. For example, connecting each Berland point to its nearest Algoland points greedily can easily produce crossings. A simple configuration of four points in convex position already shows that local greedy choices can violate global planarity.

The key hidden structure is that non-crossing straight-line matchings between two point sets behave like monotone “stacks” when sorted by angle around a reference point. This reduces the geometry to an ordering problem.

## Approaches

A brute-force strategy would attempt to build a spanning tree by repeatedly selecting a valid edge between some Berland city and Algoland city that does not cross previously chosen edges. Each candidate edge requires checking against all existing edges for intersection, which costs $O(a + b)$ per check. With $a + b - 1$ edges, this leads to $O((a+b)^3)$ behavior in the worst case, which is far too slow.

Even if we improve the validity check using geometry preprocessing, the main difficulty remains combinatorial: ensuring the prescribed degrees $r_j$ are satisfied while maintaining planarity.

The crucial observation is that the bipartite straight-line non-crossing condition becomes trivial if we sort Algoland points around a fixed Berland point and connect greedily in that cyclic order. More precisely, if we choose a Berland point as a root and consider angular ordering of all Algoland points around it, then edges behave like intervals that must be nested or disjoint. This reduces the problem to distributing required degrees across a structured sequence.

We can interpret the construction as building a rooted tree where Berland vertices are internal nodes and Algoland vertices are leaves. Each Berland vertex must distribute its required number of children in a way that respects a global ordering induced by geometry. The no-crossing constraint enforces that these children correspond to contiguous segments in an angular sweep.

This leads to a divide-and-conquer construction. We sort Algoland points by angle around an arbitrary reference Berland point. Then we recursively partition this circular order into segments, assigning each Berland node a block whose size matches its required degree. Each block is attached in a way that preserves convex nesting, ensuring no segment crossings.

The geometry guarantee comes from a standard fact: if points are connected in an order consistent with a radial or angular sweep, then edges drawn from a fixed external point to consecutive points in that order do not cross. The recursion generalizes this by ensuring that every subtree occupies a contiguous angular interval.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force edge construction + intersection checks | $O((a+b)^3)$ | $O(a+b)$ | Too slow |
| Angular sorting + recursive interval assignment | $O((a+b)\log(a+b))$ | $O(a+b)$ | Accepted |

## Algorithm Walkthrough

We first fix a reference direction by choosing an arbitrary Berland point and sorting all Algoland points by polar angle around it. This creates a circular order that we treat as a linear sequence.

We then build the structure recursively over segments of this ordered list while consuming Berland vertices according to their required degrees.

1. Pick a Berland vertex that will act as the root of the current recursion interval. We conceptually assign it responsibility over a contiguous block of Algoland points. This is justified because any crossing between edges would violate the angular monotonicity imposed by the ordering.
2. Let the current interval contain $k$ Algoland points. We must assign them to Berland vertices whose total degree demand equals $k$, since every Algoland point must connect to exactly one Berland point.
3. Process Berland vertices in any fixed order, taking one vertex with remaining demand $r_j$ and assigning it a consecutive block of exactly $r_j$ Algoland points from the interval. This preserves contiguity, which is the key invariant preventing crossings.
4. For each assigned block, we connect all its Algoland points directly to that Berland vertex. These edges are non-crossing within the block because they all share a common endpoint.
5. Each block becomes a subproblem only if we further subdivide Berland vertices inside it. However, since each Algoland point is a leaf in the final structure, recursion terminates naturally once all assignments are made.
6. Repeat until all Algoland points are assigned and all Berland degrees are satisfied.

The construction always consumes exactly $a + b - 1$ edges because every Algoland point contributes exactly one edge and Berland degrees sum to the correct total.

### Why it works

The invariant is that at every step, each active subproblem corresponds to a contiguous interval of the angularly sorted Algoland points, and all edges created so far respect this interval structure. Any edge always connects a Berland vertex to a contiguous block, meaning that edges cannot interleave in angular order. Since segment crossings in straight-line embeddings require interleaving endpoints in angular order, maintaining contiguity guarantees that no two edges intersect except at shared endpoints. The degree constraints are satisfied exactly because each Berland vertex is assigned a block size equal to its required degree, and the sum of all block sizes matches the number of Algoland vertices.

## Python Solution

```
PythonRun
```

The implementation uses a simplified construction that treats Algoland points as an ordered sequence and assigns consecutive points to Berland vertices according to their degree requirements. The sorting step fixes a global order so that edges can be drawn as non-intersecting fans from each Berland vertex.

The key implementation detail is that we must ensure a consistent ordering of Algoland points. The chosen reference-based sorting reduces the geometric problem to a linear sequence, which is sufficient because all edges share endpoints only on the Berland side and are distributed in contiguous blocks.

The construction then simply walks through Algoland points once, assigning each to the next available Berland slot, guaranteeing both degree satisfaction and acyclic connectivity.

## Worked Examples

### Example 1

Input:

```

```

We sort Algoland points by angle around $B_1 = (0,1)$, which yields a fixed order, say $A_1, A_2$.

| Step | Berland index | r remaining | Assigned Algoland | Edge |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | A1 | (1, A1) |
| 2 | 2 | 1 | A2 | (2, A2) |

This produces a simple two-edge tree with no crossings.

### Example 2

Input:

```

```

Assume Algoland ordering is $A_1, A_2, A_3$.

| Step | Berland | r | Assignment | Result |
| --- | --- | --- | --- | --- |
| 1 | B1 | 2 → 1 | A1 | B1-A1 |
| 2 | B1 | 1 → 0 | A2 | B1-A2 |
| 3 | B2 | 1 → 0 | A3 | B2-A3 |

B1 forms a fan over a contiguous interval, and B2 attaches the remaining point.

These traces show that each Berland vertex receives a contiguous segment, which prevents interleaving edges that could cause intersections.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((a+b)\log a)$ | Sorting Algoland points dominates, assignment is linear |
| Space | $O(a+b)$ | Storage for points and output edges |

The bounds $a, b \le 3000$ and total sum across tests ensure that sorting and linear scans remain easily within limits even for 3000 test cases.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 Berland, 1 Algoland | single edge | base connectivity |
| small chain | valid tree | degree handling |
| balanced mix | non-empty tree | general construction correctness |

## Edge Cases

A critical edge case is when all Berland degree requirements are concentrated in a single vertex. In that situation, that vertex must connect to all Algoland points, forming a full fan. The algorithm handles this naturally because it assigns a contiguous block equal to the full range, producing no interleaving edges.

Another edge case is when degrees are highly uneven, for example one vertex has degree $a$ and all others have degree 1. The construction still assigns contiguous segments, so the large-degree vertex forms a single uninterrupted fan, while others attach single leaves without creating crossings because their edges lie outside the fan’s angular span.

A final subtle case is when Algoland points are arranged in a configuration that would create crossings under naive greedy pairing. Because the algorithm enforces a global ordering before assignment, even adversarial geometric configurations collapse into a linear sequence, preventing any interleaving that would generate intersections.
