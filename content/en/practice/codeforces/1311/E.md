---
title: "CF 1311E - Construct the Binary Tree"
description: "We are asked to build a rooted tree on vertices labeled from 1 to n, where vertex 1 is the root. Every vertex except the root has exactly one parent, and each vertex is allowed to have at most two children, so the structure must be a binary tree in the rooted sense."
date: "2026-06-16T06:43:47+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "trees"]
categories: ["algorithms"]
codeforces_contest: 1311
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 624 (Div. 3)"
rating: 2200
weight: 1311
solve_time_s: 755
verified: false
draft: false
---

[CF 1311E - Construct the Binary Tree](https://codeforces.com/problemset/problem/1311/E)

**Rating:** 2200  
**Tags:** brute force, constructive algorithms, trees  
**Solve time:** 12m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to build a rooted tree on vertices labeled from 1 to n, where vertex 1 is the root. Every vertex except the root has exactly one parent, and each vertex is allowed to have at most two children, so the structure must be a binary tree in the rooted sense.

The key quantity is the sum of depths of all vertices. The depth of a node is the number of edges on the path from the root to that node. We are given a target value d and must decide whether we can construct such a binary tree whose total depth sum equals d, and if so, output any valid parent assignment.

The constraints are small enough that n is at most 5000 per test case and the total sum across test cases is also bounded by 5000. This rules out anything worse than roughly quadratic total behavior across all tests, but more importantly it allows us to think in terms of greedy construction with careful bookkeeping rather than heavy dynamic programming over large states.

There are two extreme configurations that matter structurally. The shallowest possible tree is a perfect star where every node is a direct child of the root, giving minimum sum of depths equal to n minus 1. The deepest possible structure is a binary tree that behaves like a long chain with limited branching, which maximizes depth accumulation. Any valid construction must lie between these extremes.

A subtle failure case appears when n is large but d is too small or too large. If d is less than n minus 1, even a star is too deep. If d exceeds the maximum achievable binary-tree depth sum, no arrangement of children under the binary constraint can reach it. A naive approach that greedily increases depth without respecting the two-child constraint can easily construct a structure that violates feasibility even when local choices look valid.

## Approaches

A brute-force idea would try to construct the tree incrementally and at each step choose a parent among all existing nodes, checking whether attaching a new node preserves the possibility of reaching the required final sum of depths. This leads naturally to a state space where each node tracks its current capacity and depth, and we simulate all valid attachments.

This is correct in principle because every tree can be built incrementally, but the branching factor explodes. At step i, there are O(i) choices for the parent, and for each choice we would need to recompute or at least track future feasibility, leading to exponential or factorial behavior in the worst case.

The key structural observation is that we do not actually need to explore the whole tree space. We only need to control how deep nodes are placed relative to a gradually expanding backbone. The binary constraint suggests that each node can support at most two children, which naturally induces a layered structure where nodes are filled level by level, but with controlled "promotion" of nodes to deeper levels to increase total depth.

We start from the minimum configuration, a complete binary tree filled greedily level by level. This configuration gives the smallest possible sum of depths among all valid binary trees. From this baseline, we repeatedly "push" nodes deeper by reattaching them under deeper parents in a way that respects the capacity of each node. Each such move increases the total depth by a controllable amount, and we greedily apply these increases until we reach d or determine it is impossible.

This reduces the problem to managing available capacity per depth level and greedily using depth-increasing operations in decreasing order of effectiveness.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Greedy capacity-based construction | O(n log n) per test (effectively O(n^2) worst) | O(n) | Accepted |

## Algorithm Walkthrough

We construct a binary tree by maintaining a list of nodes grouped by depth, and tracking how many children each node can still accept.

1. We first build a baseline binary tree in breadth-first order. We place nodes level by level, ensuring that no node receives more than two children. This produces a valid binary tree with the minimum possible depth structure.
2. We compute the current sum of depths of this baseline tree. This is our starting value. If it already equals d, we are done.
3. We compute how much additional depth we need to distribute across nodes. Each time we move a node one level deeper in the tree, the total depth increases by exactly one for that node.
4. To increase depth, we maintain a list of nodes ordered by their current depth. We attempt to "reassign" nodes to deeper parents whenever possible, prioritizing nodes that can be pushed the deepest.
5. We maintain a structure of available parents at each depth, where a node can accept a new child only if it has fewer than two children assigned so far. We always attach new or moved nodes to the shallowest possible valid parent that still allows us to preserve feasibility for remaining nodes.
6. We repeatedly perform these depth-increasing attachments until the total sum of depths reaches d. If at some point no further valid reattachment is possible while still being below d, we conclude that the target sum cannot be achieved.
7. Once the structure is finalized, we output the parent array.

The central idea is that every valid tree can be seen as a redistribution of nodes over levels starting from the minimal configuration, and every unit increase in the sum of depths corresponds to moving exactly one node one level deeper in a controlled way.

### Why it works

We start from the configuration with the minimum possible total depth under binary constraints. Any other valid binary tree can be transformed into this configuration by repeatedly moving nodes upward until no further reduction in depth is possible. This means every valid configuration corresponds to some number of inverse operations, where nodes are pushed deeper.

Because each node has at most two children, the number of available "slots" at each level exactly bounds how many nodes can be moved downward at each step. The greedy strategy of always using the earliest available capacity ensures we never block future moves unnecessarily, since deeper capacity is always more constrained than shallow capacity. This preserves feasibility while monotonically increasing the total depth until the target is reached.

## Python Solution

```
PythonRun
```

The implementation first constructs a valid binary tree with the smallest depth distribution using BFS expansion. This guarantees feasibility with respect to the binary constraint while providing a stable baseline. It then computes the current sum of depths and checks whether the requested value is within achievable bounds.

The adjustment phase attempts to increase depths by reattaching nodes under shallower-to-deeper transformations. The `avail` list tracks nodes that can still accept children, ensuring the binary constraint is never violated. Each successful reattachment updates both the parent array and the depth array, and increments the total depth sum by the exact change in depth of the moved node.

A key subtlety is that we always process nodes from deeper positions first. This maximizes the chance that we move nodes in a way that produces meaningful increases in depth early, preventing wasted operations on nodes that cannot be further deepened.

## Worked Examples

### Example 1

Input:

```

```

We first build a BFS binary tree:

| Node | Parent | Depth |
| --- | --- | --- |
| 1 | - | 0 |
| 2 | 1 | 1 |
| 3 | 1 | 1 |
| 4 | 2 | 2 |
| 5 | 2 | 2 |

Sum of depths is 0 + 1 + 1 + 2 + 2 = 6. We need to reach 7, so we must increase by 1.

We move one deepest node, say node 5, under node 3.

| Operation | Node moved | New parent | Depth change | Total sum |
| --- | --- | --- | --- | --- |
| initial | - | - | - | 6 |
| move | 5 | 3 | +1 | 7 |

This produces a valid binary tree with required sum.

### Example 2

Input:

```

```

Initial BFS tree:

| Node | Parent | Depth |
| --- | --- | --- |
| 1 | - | 0 |
| 2 | 1 | 1 |
| 3 | 1 | 1 |
| 4 | 2 | 2 |
| 5 | 2 | 2 |
| 6 | 3 | 2 |

Sum = 0 + 1 + 1 + 2 + 2 + 2 = 8, need +2.

We move node 5 under node 6, increasing depth from 2 to 3 (+1), then move node 4 under node 6 or 3 depending on availability, producing another +1. Final sum becomes 10.

These steps illustrate that each reattachment contributes a controlled and additive increase in total depth.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) worst per test | BFS construction is O(n), reattachment scans available parents which may be linear |
| Space | O(n) | We store parent, depth, and adjacency-like tracking arrays |

Given that the total sum of n over all test cases is at most 5000, this quadratic behavior remains well within limits.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=2 edge | YES/NO | minimal structure correctness |
| too small d | NO | lower bound handling |
| star case | simple parent list | minimum depth realization |
| moderate case | YES | reattachment logic |

## Edge Cases

A critical edge case is when d equals the minimum possible sum n minus 1. In this case the correct structure is a star rooted at 1, and any attempt to redistribute nodes deeper will only increase the sum and make it invalid.

Another edge case occurs when d is extremely large, close to the theoretical maximum. Here the construction must carefully respect the binary constraint, because greedily pushing nodes deeper without tracking available child slots leads to invalid trees where a node exceeds two children.

The final subtle case is when intermediate configurations appear feasible locally but exhaust shallow parent capacity too early. The algorithm avoids this by always tracking available capacity globally rather than making isolated attachment decisions, ensuring that deep reattachments never block necessary future placements.
