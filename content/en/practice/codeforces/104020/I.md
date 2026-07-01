---
title: "CF 104020I - Imperfect Imperial Units"
description: "We are given a collection of conversion rules between abstract measurement units. Each rule states that one unit is equivalent to a scaled amount of another unit."
date: "2026-07-02T04:41:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104020
codeforces_index: "I"
codeforces_contest_name: "2022 Benelux Algorithm Programming Contest (BAPC 22)"
rating: 0
weight: 104020
solve_time_s: 27
verified: false
draft: false
---

[CF 104020I - Imperfect Imperial Units](https://codeforces.com/problemset/problem/104020/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of conversion rules between abstract measurement units. Each rule states that one unit is equivalent to a scaled amount of another unit. The system is consistent in the sense that any unit that is connected through these rules can be converted into any other unit along a unique path.

After reading all conversion rules, we must answer queries of the form: given a quantity in one unit, compute its value in another unit if a conversion path exists. If no chain of conversions connects the two units, the answer is impossible.

The key abstraction is that units form nodes in a graph and each conversion rule forms a weighted edge. The weight encodes a multiplicative factor, and queries ask for the product of weights along a path.

The constraints are deliberately asymmetric: the number of conversion rules is small, at most 100, but the number of queries is large, up to 10,000. This strongly suggests that preprocessing the structure of the unit system once and then answering queries quickly is the intended strategy. Any solution that recomputes a path search per query risks repeating essentially the same traversal many times.

A subtle numerical issue appears because conversion factors are floating-point values, and repeated multiplication along long chains can accumulate precision error. The required tolerance is relatively strict, so path representations must avoid unnecessary repeated recomputation of floating products.

A few edge cases matter.

If two units exist in different disconnected components, such as “meter” and “inch” with no chain between them, a query between them must output impossible even though both appear in the input.

If a unit is connected through multiple intermediate steps, like A to B to C, we must ensure that we do not accidentally recompute inconsistent scaling paths due to floating drift.

Finally, queries may ask conversion in either direction relative to the stored rule, so the representation must support bidirectional scaling.

## Approaches

A direct approach treats each query independently. For every query, we perform a graph search from the source unit to the target unit, multiplying conversion factors along the path. Because each search can touch all nodes and edges, this gives a worst case of about 10,000 searches over a graph with up to 100 nodes and 100 edges. That is already borderline but still plausible; however, the real issue is redundancy. The same graph is traversed repeatedly, and since each pair of units has a unique conversion path, every query recomputes something that is globally fixed.

The structure of the problem is more rigid than general weighted graphs. Each connected component behaves like a tree of multiplicative relations. Once we assign a consistent “base ratio” for each unit relative to a representative root, every conversion reduces to a simple ratio lookup. This removes graph traversal entirely during queries.

The key insight is to assign each unit a canonical value relative to an arbitrary root in its connected component. If we know that unit A equals x times the root and unit B equals y times the root, then A to B conversion is simply x / y. This turns path products into node labels.

We build these labels using a single traversal per component, either BFS or DFS, propagating known ratios from one node to its neighbors.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Repeated BFS/DFS per query | O(q(n + e)) | O(n + e) | Too slow |
| Component labeling with DFS/BFS | O(n + e + q) | O(n + e) | Accepted |

## Algorithm Walkthrough

1. Build a graph where each unit is a node, and each conversion rule a
