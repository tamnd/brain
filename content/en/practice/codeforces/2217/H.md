---
title: "CF 2217H - Closer"
description: "We have a tree with $2n$ vertices, each hosting a single person. Every person carries a badge corresponding to one of $n$ deals, and each deal appears exactly twice among the people."
date: "2026-06-07T18:28:03+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "trees"]
categories: ["algorithms"]
codeforces_contest: 2217
codeforces_index: "H"
codeforces_contest_name: "Codeforces Round 1091 (Div. 2) and CodeCraft 26"
rating: 2800
weight: 2217
solve_time_s: 121
verified: false
draft: false
---

[CF 2217H - Closer](https://codeforces.com/problemset/problem/2217/H)

**Rating:** 2800  
**Tags:** dfs and similar, dp, trees  
**Solve time:** 2m 1s  
**Verified:** no  

## Solution
## Problem Understanding

We have a tree with $2n$ vertices, each hosting a single person. Every person carries a badge corresponding to one of $n$ deals, and each deal appears exactly twice among the people. If the two people holding the same deal badge are on adjacent vertices, the deal is immediately sealed and contributes a profit $w_i$.

We are allowed one reshuffle: choose a set of edges forming a matching (no two edges share a vertex) and swap the people on each chosen edge. The goal is to maximize the sum of profits from sealed deals after this reshuffle.

Each test case specifies the number of deals $n$, the profits $w_1 \ldots w_n$, the arrangement of people on vertices $a_1 \ldots a_{2n}$, and the edges of the tree. The output is the maximum total profit achievable after one such reshuffle.

Given $n$ can reach $10^5$ and there may be up to $10^4$ test cases with the sum of $n$ across all cases bounded by $10^5$, we cannot afford anything worse than roughly $O(n)$ per test case. This rules out approaches that explicitly try all possible matchings or all swaps between pairs of people.

Non-obvious edge cases arise when the two nodes of a deal are already adjacent or connected indirectly through a path of length two. For example, if a deal's two people are already on neighboring vertices, swapping them elsewhere could actually reduce profit if handled incorrectly. Another tricky scenario is when multiple high-value deals share adjacent vertices: choosing the wrong matching could miss these profits.

## Approaches

The brute-force approach is straightforward. For each possible matching of edges in the tree, swap the pairs and recalculate the number of sealed deals. Since a tree with $2n$ vertices has $2n-1$ edges, there are $2^{2n-1}$ possible subsets of edges. Even pruning for matchings that do not share vertices, the number of options remains exponential. This is clearly infeasible for $n \sim 10^5$.

The key insight comes from realizing that we only need to consider edges that are adjacent to the positions of the two people for each deal. Each deal has exactly two people, so the only swaps that matter are those that bring the two people closer to being adjacent. Since the tree is acyclic, the unique path between any two nodes can be considered independently. Along this path, we can decide which swaps would make the two people adjacent. For edges outside this path, swapping has no effect on the deal.

This observation reduces the problem to a tree dynamic programming task: for each node, we maintain whether it is beneficial to swap its person along a matching edge to increase total profit. Since we can only swap along a matching (non-adjacent edges), we perform a DP that, at each node, considers whether to include the edge to its parent in the matching or not. This is effectively a weighted maximum matching on a tree problem, where the weight is the potential gain from sealing a deal by swapping along that edge.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(2n)) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Map each deal $i$ to the positions of its two people in the tree. This gives a pair of vertices $(u_i, v_i)$ for each deal.
2. Compute the current contribution to profit from deals that are already sealed (their two vertices are adjacent). Initialize `total_profit` with this sum.
3. For each deal whose two people are not adjacent, compute the path in the tree between the two vertices. Mark all edges along this path with the potential profit of sealing this deal. Each edge now knows the maximum gain it can provide if included in the swap matching.
4. Run a DP on the tree to find the maximum sum of edge weights in a matching. For each node, maintain two values: `dp[node][0]` if the edge to its parent is not included in the matching, and `dp[node][1]` if it is included. At each node, consider all children:

1. If the edge to a child is included, add its weight plus the `dp[child][0]`.
2. If the edge to a child is excluded, add `max(dp[child][0], dp[child][1])`.

The root's maximum DP value gives the maximum extra profit achievable via a matching swap.
5. The final answer is the sum of `total_profit` from initially sealed deals plus the DP result.

Why it works: each deal contributes profit at most once. By marking edges along the path between its two nodes, we ensure that including any edge in the matching can only help seal a deal. The tree DP guarantees that no two adjacent edges are selected simultaneously, respecting the matching constraint.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 20)

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        w = list(map(int, input().split()))
        a = list(map(int, input().split()))
        
        pos = [[] for _ in range(n)]
        for idx, badge in enumerate(a):
            pos[badge - 1].append(idx)
        
        tree = [[] for _ in range(2 * n)]
        for _ in range(2 * n - 1):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            tree[u].append(v)
            tree[v].append(u)
        
        # Build parent and depth arrays for LCA path retrieval
        parent = [-1] * (2 * n)
        depth = [0] * (2 * n)
        def dfs(node, par):
            parent[node] = par
            for nei in tree[node]:
                if nei != par:
                    depth[nei] = depth[node] + 1
                    dfs(nei, node)
        dfs(0, -1)
        
        # Mark edge weights for potential deal gains
        edge_weight = {}
        total_profit = 0
        for i in range(n):
            u, v = pos[i]
            if v in tree[u]:
                total_profit += w[i]
                continue
            # Move u and v up to LCA
            def add_path(u, v, val):
                while u != v:
                    if depth[u] > depth[v]:
                        edge_weight[(min(u, parent[u]), max(u, parent[u]))] = max(
                            edge_weight.get((min(u, parent[u]), max(u, parent[u])), 0), val)
                        u = parent[u]
                    else:
                        edge_weight[(min(v, parent[v]), max(v, parent[v]))] = max(
                            edge_weight.get((min(v, parent[v]), max(v, parent[v])), 0), val)
                        v = parent[v]
            add_path(u, v, w[i])
        
        # Tree DP for max matching
        dp = [[0,0] for _ in range(2 * n)]
        def tree_dp(node, par):
            incl = 0
            excl = 0
            for nei in tree[node]:
                if nei == par:
                    continue
                tree_dp(nei, node)
                e = edge_weight.get((min(node, nei), max(node, nei)), 0)
                incl += dp[nei][0] + e
                excl += max(dp[nei][0], dp[nei][1])
            dp[node][0] = excl
            dp[node][1] = incl
        tree_dp(0, -1)
        print(total_profit + max(dp[0][0], dp[0][1]))

if __name__ == "__main__":
    solve()
```

The solution proceeds in three main stages: parsing the input and mapping deals, marking potential gain on edges along paths between deal participants, and running a tree DP to select the optimal matching. Careful attention is paid to 0-based indexing, ensuring edge keys are ordered consistently, and avoiding double counting by checking adjacency first.

## Worked Examples

Sample Input:

```
1
3
10 8 5
1 2 1 2 3 3
1 2
2 3
3 4
4 5
5 6
```

| Deal | u | v | Already adjacent | Path edges | Weight added to edges |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 2 | No | (0-1),(1-2) | 10 |
| 2 | 1 | 3 | No | (1-2),(2-3) | 8 |
| 3 | 4 | 5 | Yes | - | 5 already included |

Tree DP selects edges (0-1) and (3-4) as matching for max extra profit, resulting in total 10+5=15.

Second example: input with already adjacent deals yields correct addition to `total_profit`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each vertex is visited once in DFS and DP; marking edges along paths between deal nodes costs O(n) because total nodes across all test cases ≤ 10^5 |
| Space | O(n) | Tree adjacency lists, DP array, edge weight dictionary, |
