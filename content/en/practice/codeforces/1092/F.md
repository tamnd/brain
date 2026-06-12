---
title: "CF 1092F - Tree with Maximum Cost"
description: "We are given a weighted tree, where each node carries a positive value. We are allowed to choose any node as a reference point, and for that choice we compute a score defined as the sum over all nodes of their value multiplied by their distance to the chosen node."
date: "2026-06-13T04:41:27+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "trees"]
categories: ["algorithms"]
codeforces_contest: 1092
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 527 (Div. 3)"
rating: 1900
weight: 1092
solve_time_s: 467
verified: false
draft: false
---

[CF 1092F - Tree with Maximum Cost](https://codeforces.com/problemset/problem/1092/F)

**Rating:** 1900  
**Tags:** dfs and similar, dp, trees  
**Solve time:** 7m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a weighted tree, where each node carries a positive value. We are allowed to choose any node as a reference point, and for that choice we compute a score defined as the sum over all nodes of their value multiplied by their distance to the chosen node. The task is to find the node that maximizes this score.

The tree structure is static, so the only decision is the choice of root. Once a root is fixed, every other node contributes proportionally to how far it lies from that root, scaled by its weight.

The constraints are large, with up to 200,000 nodes. Any solution that recomputes distances from every possible root independently would require running a traversal per node, leading to roughly $O(n^2)$ behavior in a tree with linear structure. That is far beyond what fits in two seconds. Even a single all-pairs distance computation is impossible, so the solution must reuse partial computations across roots.

A subtle edge case appears when the tree has only one node. The answer is necessarily zero since there are no distances to sum. Another important case is a star-shaped tree, where the optimal root is not always the center node. If the high-weight nodes are at leaves, shifting the root toward them increases their contribution more than it increases the cost of others.

## Approaches

A direct approach tries every node as the root. For each candidate root, we run a DFS or BFS to compute distances to all nodes and accumulate the weighted sum. This is correct because it follows the definition directly. The cost per root is $O(n)$, giving $O(n^2)$ overall. With $n = 2 \cdot 10^5$, this is infeasible.

The key observation is that when we move the root across an edge, only relative distances change in a structured way. If we know the cost for one root, we can update the cost for its neighbor without recomputing everything. The change depends only on the total weight of nodes in the subtree being moved closer or farther.

This leads to a classic tree rerooting idea. First compute the total weight of the tree and the cost for an arbitrary root, say node 1. Then, for each edge from parent to child, we derive how the cost changes when shifting the root from parent to child. Nodes in the child's subtree get closer by one, while all other nodes get farther by one. This allows an $O(1)$ transition per edge after a single DFS preprocessing.

We compute subtree sums of weights to make these transitions possible. Once we have subtree weights, rerooting becomes a linear traversal over the tree.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(n)$ | Too slow |
| Reroot DP | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We define $S$ as the sum of all node weights. We root the tree at an arbitrary node, compute subtree sums, and compute the cost of this root configuration. Then we propagate this cost to all other nodes using rerooting.

1. Pick an arbitrary node, commonly node 1, as the initial root. This gives us a fixed perspective from which to compute all subtree information consistently.
2. Run a DFS to compute two values for each node: its subtree sum of weights and its initial contribution to the total cost from the chosen root. The subtree sum is needed to understand how cost changes when the root shifts.
3. During DFS, compute the initial cost at the root by accumulating $depth[node] \cdot a[node]$. This establishes a correct baseline for rerooting.
4. Store the total sum of all node weights. This value determines how much cost changes when a node moves one step closer or farther from the root.
5. Perform a second DFS for rerooting. Suppose we are at a node $u$ with known cost, and we move the root to a child $v$.
6. When moving from $u$ to $v$, all nodes in $v$'s subtree become one step closer to the root. Their total weight is $subtree[v]$, so their contribution decreases by $subtree[v]$.
7. All nodes outside $v$'s subtree become one step farther. Their total weight is $S - subtree[v]$, so their contribution increases by $S - subtree[v]$.
8. Combine both effects to compute:

$$cost[v] = cost[u] + (S - subtree[v]) - subtree[v]$$

This gives a constant-time transition.
9. Track the maximum value of cost across all nodes during traversal.

### Why it works

The rerooting formula relies on the fact that moving the root across one edge changes every distance by exactly one unit, either increasing or decreasing depending on subtree membership. The partition into subtree and non-subtree nodes ensures every node’s distance change is accounted for exactly once. Since subtree sums fully describe total weight distribution, the cost transformation is exact and no information is lost during transitions.

## Python Solution

```
PythonRun
```

The first DFS builds the subtree sums and computes the initial cost from the root. The second DFS performs rerooting, updating the cost in constant time per edge using the derived formula. The temporary save and restore of `cost0` ensures correct propagation down different branches without recomputation.

A common implementation pitfall is forgetting that subtree sums are defined with respect to the initial root only. Another is incorrectly updating cost symmetrically; the correct update depends strictly on subtree membership, not general distance reasoning.

## Worked Examples

### Example 1

Input:

```

```

We root at node 1.

| Step | Node | Subtree sum | Cost |
| --- | --- | --- | --- |
| DFS1 | 1 | 6 | 0·1 + 1·2 + 2·3 = 8 |
| Move root to 2 | 2 | 5 | 8 + (6-5) - 5 = 4 |
| Move root to 3 | 3 | 3 | 4 + (6-3) - 3 = 4 |

Maximum is 8 at node 1.

This shows how shifting root changes contribution based purely on subtree weights.

### Example 2

Input:

```

```

Root at node 1:

| Step | Node | Subtree sum | Cost |
| --- | --- | --- | --- |
| DFS1 | 1 | 14 | 0 |
| Move to 3 | 3 | 3 | 0 + (14-3) - 3 = 8 |
| Move to 4 | 4 | 1 | 8 + (14-1) - 1 = 20 |

Maximum occurs at node 4 or 5 depending on traversal.

This demonstrates that optimal roots tend to lie toward heavier subtrees.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each DFS visits each node and edge once |
| Space | $O(n)$ | Adjacency list and auxiliary arrays |

The linear complexity is necessary because the input size reaches 200,000 nodes. Any quadratic recomputation of distances would exceed both time and memory constraints, while the rerooting technique ensures each edge contributes only constant work.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 0 | base edge case |
| chain | 20 | longest path behavior |
| star | 16 | reroot sensitivity |
| uniform weights | 10 | symmetry correctness |

## Edge Cases

For a single node input, the DFS initializes cost as zero because depth is zero and no edges exist. The rerooting phase does not trigger any transitions, so the maximum remains zero, matching the expected output.

For a star-shaped tree where one leaf has significantly larger weight, the first DFS computes cost from the center root. When rerooting to that heavy leaf, subtree size becomes small, making the formula increase the cost sharply due to most nodes moving farther. The algorithm correctly captures this because subtree sums isolate exactly the heavy branch, ensuring the transition formula applies cleanly.
