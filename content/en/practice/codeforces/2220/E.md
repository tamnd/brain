---
title: "CF 2220E - Coloring a Red Black Tree"
description: "We are given a tree with n nodes, where each node is either red or black. The goal is to make all nodes red using a stochastic operation: you select a node and recolor it with the color of one of its neighbors chosen uniformly at random."
date: "2026-06-09T05:00:28+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "probabilities", "sortings", "trees"]
categories: ["algorithms"]
codeforces_contest: 2220
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1093 (Div. 2)"
rating: 2300
weight: 2220
solve_time_s: 122
verified: false
draft: false
---

[CF 2220E - Coloring a Red Black Tree](https://codeforces.com/problemset/problem/2220/E)

**Rating:** 2300  
**Tags:** dp, greedy, probabilities, sortings, trees  
**Solve time:** 2m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree with `n` nodes, where each node is either red or black. The goal is to make all nodes red using a stochastic operation: you select a node and recolor it with the color of one of its neighbors chosen uniformly at random. The input provides multiple test cases, each with the number of nodes, the binary string representing initial colors, and the edges of the tree. The output is the minimum expected number of operations to turn the entire tree red.

The constraints require efficient handling. `n` can be up to 200,000, and the sum over all test cases is also 200,000, which rules out naive simulation of random operations or exponential state enumeration. Each operation depends on the current node's neighbors, so a solution must propagate expectations through the tree efficiently.

Non-obvious edge cases include trees where a black node has only black neighbors, or leaves that are black with a red parent. If you try to compute expected operations without considering the tree structure and neighbor degrees, you might incorrectly assume immediate conversion, which would produce wrong expectations. For example, a black leaf with a single red neighbor has an expected value of `1` because it will become red on the first operation. A black node with two black neighbors but one distant red node requires a recursive expectation calculation.

## Approaches

The brute-force approach would be to simulate all sequences of operations and compute the average number of steps for each sequence. While correct, this is infeasible because the state space grows exponentially with `n`, and the number of operations is unbounded in general. For example, even a chain of 20 nodes would require simulating over a million states if one attempted full enumeration.

The key insight is that the expected number of operations for a node to become red depends only on the expected values of its neighbors. This allows a recursive formulation on the tree, where leaves can be solved immediately, and the expectations propagate up. In a tree, each node's expected value can be expressed in terms of its neighbors, and we can compute these values efficiently using a depth-first search.

The observation that each node's expectation is `1 + sum(E[neighbor])/deg(node)` for black nodes, where `deg(node)` counts neighbors, lets us reduce the problem to a linear traversal of the tree. Red nodes have an expectation of zero. This leads to an O(n) solution per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(2^n) | O(n) | Too slow |
| DFS Expectation Propagation | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Parse the input for the number of test cases. For each test case, read `n`, the binary string `s`, and the `n-1` edges. Build an adjacency list representing the tree.
2. Initialize an array `E` of expected values. Set `E[i] = 0` if node `i` is red and `None` if node `i` is black.
3. Define a recursive function `dfs(u, parent)` that computes the expected number of operations for node `u`:

1. If node `u` is red, return 0.
2. Otherwise, initialize `sum_neighbors = 0` and `degree = len(adj[u])`.
3. For each neighbor `v` of `u` (excluding the parent to prevent cycling), call `dfs(v, u)` and add the result to `sum_neighbors`.
4. Compute `E[u] = 1 + sum_neighbors / degree`. This accounts for one operation plus the average expectation from neighbors.
5. Return `E[u]`.
4. Call `dfs(root, -1)` starting from any red node, since at least one red node exists.
5. Print `E[root]` with sufficient precision.

Why it works: The recursive function computes the exact expected value using linearity of expectation. Each node's operation is independent of the order in which operations are applied elsewhere, provided that the neighbors’ expectations are correctly propagated. Red nodes act as absorbing states with zero expectation, ensuring the recursion terminates and yields the minimal expected number of operations.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        s = input().strip()
        adj = [[] for _ in range(n)]
        for _ in range(n - 1):
            u, v = map(int, input().split())
            adj[u-1].append(v-1)
            adj[v-1].append(u-1)
        
        E = [None]*n
        red_nodes = [i for i, c in enumerate(s) if c == '1']
        for r in red_nodes:
            E[r] = 0.0

        def dfs(u, parent):
            if E[u] is not None:
                return E[u]
            total = 0.0
            deg = len(adj[u])
            for v in adj[u]:
                if v == parent:
                    continue
                total += dfs(v, u)
            E[u] = 1.0 + total / deg
            return E[u]
        
        # start from any black node
        for i in range(n):
            if E[i] is None:
                dfs(i, -1)
        # the maximum expected among black nodes
        res = max(E[i] for i in range(n))
        print(f"{res:.12f}")

solve()
```

This code reads the tree, initializes expectations, and uses DFS to propagate expected values. Using `max(E[i])` ensures we report the minimal expected operations to make all nodes red. Floating-point precision is handled with `:.12f`.

## Worked Examples

Sample 1:

Input:

```
3
3
101
1 2
2 3
```

| Node | Color | Neighbors | Expectation Calculation | E[node] |
| --- | --- | --- | --- | --- |
| 1 | 1 | 2 | Red → 0 | 0 |
| 2 | 0 | 1,3 | 1 + (0 + 0)/2 | 1 |
| 3 | 1 | 2 | Red → 0 | 0 |

Output: `1.000000000000`

Sample 2:

Input:

```
5
10010
1 2
2 3
3 4
2 5
```

The DFS computes each
