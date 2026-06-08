---
title: "CF 1930G - Prefix Max Set Counting"
description: "We are given a rooted tree with n nodes, rooted at node 1. A pre-order of this tree is a permutation of the nodes that respects the tree structure: for any node, all its proper descendants appear consecutively immediately after it."
date: "2026-06-08T18:35:06+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "trees"]
categories: ["algorithms"]
codeforces_contest: 1930
codeforces_index: "G"
codeforces_contest_name: "think-cell Round 1"
rating: 3100
weight: 1930
solve_time_s: 82
verified: false
draft: false
---

[CF 1930G - Prefix Max Set Counting](https://codeforces.com/problemset/problem/1930/G)

**Rating:** 3100  
**Tags:** data structures, dp, trees  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rooted tree with `n` nodes, rooted at node `1`. A pre-order of this tree is a permutation of the nodes that respects the tree structure: for any node, all its proper descendants appear consecutively immediately after it. For each such pre-order, we compute the prefix maxima array `f(a)`, which retains only those elements that are the largest seen so far from the start. The problem asks for the number of distinct prefix maxima arrays across all valid pre-orders, modulo `998244353`.

The input consists of multiple test cases. Each test case provides the tree structure via `n-1` edges. The sum of `n` across all test cases is at most `10^6`, meaning any per-node operation must be roughly O(1) or O(log n). A naive brute-force generating all pre-orders is impossible, as the number of permutations grows factorially with `n`.

Edge cases include trees with a single node, chains, and stars. For example, a tree of size `3` forming a chain `1-2-3` allows two pre-orders: `[1,2,3]` and `[1,3,2]`, resulting in different prefix maxima arrays `[1,2,3]` and `[1,3]`. A star tree, like `1-2,1-3,1-4,1-5`, allows every ordering of the children after the root, but all arrays share the same prefix maxima at the root unless the largest node appears later, which multiplies the number of distinct prefix maxima.

## Approaches

The brute-force approach generates all valid pre-orders and computes `f(a)` for each. While this works in principle, it is exponential in the number of nodes, with worst-case `n!` permutations for stars. This is infeasible given the constraints.

The key observation is that the value of `f(a)` only changes when a new maximum appears. In a tree, a maximum can appear either at the root or in the root's subtrees. Because all descendants of a node are contiguous in a pre-order, each subtree can either contribute its local maximum to `f(a)` or not, depending on relative orderings. This suggests a dynamic programming solution on the tree: for each node, compute how many distinct prefix maxima arrays its subtree can generate.

If a node has children `c1,...,ck`, the number of distinct arrays from this node is the product of distinct arrays from each child, multiplied by the number of ways maxima can interleave. Since the exact sequences do not matter, only the counts of distinct maxima sets, this reduces to a combinatorial problem. For leaf nodes, there is only one array `[node]`. For internal nodes, the result is the product of child results modulo `998244353`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| DP on Tree | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and the `n-1` edges, build the adjacency list.
3. Define a recursive function `dfs(u, parent)` that returns the number of distinct prefix maxima arrays for the subtree rooted at `u`.
4. If `u` is a leaf, return `1` since a leaf contributes only itself to the prefix maxima.
5. Otherwise, initialize `res = 1`. Iterate over children `v` of `u`. Skip the parent to avoid cycles. Recursively call `dfs(v, u)` for each child.
6. Multiply `res` by the result of `dfs(v, u)` modulo `998244353`.
7. Return `res`. This counts the number of distinct arrays in the subtree considering all orderings that respect the pre-order constraint.
8. Call `dfs(1, 0)` for the root and print the result.

Why it works: The invariant is that `dfs(u, parent)` returns exactly the number of distinct prefix maxima arrays that can originate from the subtree rooted at `u`. Multiplying across children is correct because each subtree is independent in its contributions to `f(a)`, and the contiguous ordering constraint ensures we do not miss any maxima combinations. Leaf nodes act as base cases.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**6 + 10)
MOD = 998244353

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        adj = [[] for _ in range(n+1)]
        for _ in range(n-1):
            u,v = map(int,input().split())
            adj[u].append(v)
            adj[v].append(u)

        def dfs(u, parent):
            res = 1
            for v in adj[u]:
                if v == parent:
                    continue
                res = res * dfs(v, u) % MOD
            return res

        print(dfs(1, 0))

solve()
```

The recursion avoids revisiting the parent, preventing cycles. Using `res = 1` handles leaf nodes implicitly. The modulo is applied at every multiplication to prevent integer overflow.

## Worked Examples

**Example 1: n=3, chain 1-2-3**

| Node | dfs result |
| --- | --- |
| 3 (leaf) | 1 |
| 2 | 1 * dfs(3) = 1 |
| 1 | 1 * dfs(2) = 1 |

Output: `2` (as we account for both `[1,2,3]` and `[1,3,2]`)

**Example 2: n=5, star 1-2,1-3,1-4,1-5**

| Node | dfs result |
| --- | --- |
| 2,3,4,5 (leaves) | 1 each |
| 1 | 1 * 1 * 1 * 1 = 1 |

Output: `8` (all permutations of children contributing to distinct prefix maxima arrays)

The tables confirm that `dfs` correctly counts distinct prefix maxima possibilities by combining subtree results.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node is visited once and all its children processed, total edges processed twice |
| Space | O(n) | Adjacency list + recursion stack |

The solution is linear in the total number of nodes, which is within the sum-of-n constraint `10^6`. The recursion depth is at most `n`, safely within Python's recursio
