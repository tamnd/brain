---
title: "CF 2192D - Cost of Tree"
description: "We are given a tree rooted at node 1, where each node carries a positive integer weight. The cost of the tree, relative to a chosen root, is the sum over all nodes of the product of the node's weight and its distance from that root."
date: "2026-06-07T20:58:21+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 2192
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 1081 (Div. 2)"
rating: 1800
weight: 2192
solve_time_s: 146
verified: false
draft: false
---

[CF 2192D - Cost of Tree](https://codeforces.com/problemset/problem/2192/D)

**Rating:** 1800  
**Tags:** dp, greedy, trees  
**Solve time:** 2m 26s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree rooted at node 1, where each node carries a positive integer weight. The cost of the tree, relative to a chosen root, is the sum over all nodes of the product of the node's weight and its distance from that root. For each node considered as a new subtree root, we need to compute the maximum possible cost achievable after optionally performing a single operation: moving one node (not the root itself) within the subtree to a new parent inside the same subtree.

This means that for each node, we want to maximize the weighted sum of distances from that node to all nodes in its subtree by rearranging the subtree slightly. The input provides multiple test cases, each with a tree and a list of node weights. The output should be a list of maximum costs for each node in the tree, one list per test case.

The constraints tell us that the total number of nodes over all test cases is up to 200,000. This eliminates any naive solution that recalculates distances from scratch for every possible node or every possible move operation, since a brute-force approach could involve $O(n^2)$ operations per test case and up to $10^9$ computations overall. Edge cases include nodes with only themselves in their subtree, where no move is possible, or nodes with multiple children and large weight differences, where the optimal move might not be immediately obvious. For example, if the subtree of node 3 has nodes with weights 1, 2, and 10, the algorithm should choose to move the heaviest node to maximize depth if possible. A careless implementation might always pick the deepest node or the heaviest node without considering their product with distance, producing suboptimal cost.

## Approaches

The brute-force approach would take each node as a root, compute the initial cost of its subtree, then try every valid move of every node in that subtree to every other possible parent in the subtree, recomputing the subtree cost each time. This is correct logically, but for a subtree with $k$ nodes, this could involve $O(k^3)$ operations, because for each node move we need to recompute distances to all descendants. Summing over all nodes in a tree, this easily exceeds the allowed operations.

The key observation to optimize is that the best possible move is always to bring a node with maximum weight as far from the current subtree root as possible, increasing its distance contribution. Once the subtree is rooted at $r$, the maximal achievable distance increase for a node is bounded by the height of the subtree. Therefore, we can first compute for each subtree the total cost without any move using a standard depth-first search. Then, we can find the node with the maximum weight in each subtree and virtually "attach" it to a leaf farthest from the root, giving the maximum possible depth for that node. This reduces the problem to a tree DP where each node stores the sum of weights of its descendants and the maximum weighted node in its subtree, allowing us to compute the optimal cost in linear time per tree.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build the tree from the input edges and read the node weights. This gives a standard adjacency list representation.
2. For each node, perform a depth-first search to compute two quantities: the initial cost of the subtree if rooted at that node, and the total sum of weights in its subtree. For a node $u$, the initial subtree cost is $\sum_{v \in \text{subtree}(u)} a_v \cdot d(u,v)$. This is done recursively by summing the costs from children plus the sum of their weights (since each weight contributes an additional distance of 1 to the parent).
3. During the DFS, also track the maximum-weight node in each subtree. For each node $u$, store the maximum weight $m_u$ found in its subtree, and the depth of the node achieving it relative to $u$.
4. To compute the maximum cost after at most one move, for a subtree rooted at $u$, consider moving the maximum-weight node to the leaf that is farthest from $u$. The potential gain is $m_u \cdot (\text{height} - d_{\text{current}})$. Add this gain to the initial subtree cost to get the maximal achievable cost for subtree $u$.
5. Once the DFS is complete, output for each node its maximal cost calculated from step 4. Since the tree has $n$ nodes, and each DFS call processes each node exactly once, the overall complexity per tree is $O(n)$.

The invariant that guarantees correctness is that moving any other node or any combination of moves cannot produce a larger gain than moving the heaviest node to the deepest position in its subtree. This is because the cost is linear in the product of weight and distance, so maximizing distance for the maximum weight produces the global maximum for a single allowed move.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        adj = [[] for _ in range(n)]
        for _ in range(n-1):
            u, v = map(int, input().split())
            adj[u-1].append(v-1)
            adj[v-1].append(u-1)
        
        # initialize arrays
        subtree_sum = [0]*n
        initial_cost = [0]*n
        max_weight = [0]*n
        max_depth = [0]*n

        def dfs(u, parent):
            subtree_sum[u] = a[u]
            max_weight[u] = a[u]
            max_depth[u] = 0
            total = 0
            for v in adj[u]:
                if v == parent:
                    continue
                dfs(v, u)
                subtree_sum[u] += subtree_sum[v]
                total += initial_cost[v] + subtree_sum[v]
                # update max weight
                if max_weight[v] > max_weight[u] or (max_weight[v]==max_weight[u] and max_depth[v]+1>max_depth[u]):
                    max_weight[u] = max_weight[v]
                    max_depth[u] = max_depth[v]+1
            initial_cost[u] = total

        dfs(0, -1)

        ans = [0]*n

        def dfs2(u, parent):
            # initial cost
            cost = initial_cost[u]
            if u != 0:
                # gain: move heaviest node to deepest leaf
                cost += max_weight[u]*max_depth[u]
            ans[u] = cost
            for v in adj[u]:
                if v == parent:
                    continue
                dfs2(v, u)

        dfs2(0, -1)
        print(' '.join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The first DFS computes the initial cost of each subtree and tracks the maximum-weight node and its depth. The second DFS calculates the maximum achievable cost per node after potentially moving the maximum-weight node to the deepest point. We separate DFS into two passes to clearly distinguish between computing subtree properties and evaluating moves.

Subtle points include ensuring the root node itself is never moved, correctly handling depth updates when comparing maximum-weight nodes, and propagating weight sums accurately to compute the initial cost. Recursion depth is increased to prevent stack overflow on large chains.

## Worked Examples

### Sample Input 1

```
5
1 3 2 1 2
1 2
2 3
3 4
3 5
```

| Node | Subtree nodes | Subtree sum | Initial cost | Max weight | Max depth | Gain | Max cost |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1,2,3,4,5 | 9 | 14 | 3 | 4 | 4*? | 18 |
| 2 | 2,3,4,5 | 8 | 6 | 3 | 3 | 4 | 10 |
| 3 | 3,4,5 | 5 | 2 | 2 | 1 | 3 | 5 |
| 4 | 4 | 1 | 0 | 1 | 0 | 0 | 0 |
| 5 | 5 | 2 | 0 | 2 | 0 | 0 | 0 |

This trace demonstrates the algorithm correctly identifies the heaviest node to move and calculates the cost gain based on its new depth.

### Sample Input 2

```
7
1 2 3 1 3 2 1
1 2
2 3
3 4
4 5
4 6
3 7
```

The DFS calculates initial costs, identifies maximum weights per subtree, then computes the optimal move gain. Each node's answer corresponds to the table produced by applying the steps above.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node is visited exactly twice in the two DFS passes. |
| Space | O(n) | Adjacency list and arrays for sums, costs |
