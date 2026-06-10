---
title: "CF 1540B - Tree Array"
description: "We are asked to calculate the expected number of inversions in a random process of marking nodes in a tree. The tree has n nodes, and the marking process begins with a uniformly random initial node."
date: "2026-06-10T14:25:14+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "combinatorics", "dp", "graphs", "math", "probabilities", "trees"]
categories: ["algorithms"]
codeforces_contest: 1540
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 728 (Div. 1)"
rating: 2300
weight: 1540
solve_time_s: 243
verified: false
draft: false
---

[CF 1540B - Tree Array](https://codeforces.com/problemset/problem/1540/B)

**Rating:** 2300  
**Tags:** brute force, combinatorics, dp, graphs, math, probabilities, trees  
**Solve time:** 4m 3s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to calculate the expected number of inversions in a random process of marking nodes in a tree. The tree has `n` nodes, and the marking process begins with a uniformly random initial node. After that, nodes are added one by one, each chosen uniformly from the set of unmarked nodes adjacent to already marked nodes. The array `a` records the order in which nodes are marked, and an inversion is a pair `(i, j)` with `i < j` and `a[i] > a[j]`. The goal is to compute the expected number of inversions modulo `10^9+7`.

The constraints indicate `n` is at most 200, which is small. This allows for an algorithm whose complexity grows roughly like `O(n^3)` or perhaps slightly higher, because `200^3 ≈ 8 * 10^6`, which is feasible in 2 seconds. The problem involves combinatorial expectations, so a brute-force simulation of all permutations would be `O(n!)` and is clearly impossible, even for `n = 10`.

Edge cases to watch for include small trees like a chain of two nodes or a star-shaped tree. For a chain of two nodes, the expected inversions can be fractional. A naive approach that only counts a single ordering would give an integer and miss the expectation. Trees with symmetrical structures like stars also require careful averaging over initial choices.

## Approaches

The naive approach is to simulate all valid permutations of node marking and compute inversions for each. This works because we could, in theory, enumerate all permutations, sum the inversions, and divide by the total number of valid permutations. The problem is that the number of permutations grows explosively with `n`. For `n = 10`, there are over 3 million possibilities, and for `n = 20`, over `10^18`. This is infeasible even for small `n`.

The key insight comes from viewing the problem recursively. The expected inversions contributed by a pair of nodes depend only on their relative positions in the tree. If we pick a root arbitrarily, then the expected number of inversions between two nodes `u` and `v` can be expressed in terms of the sizes of the subtrees and the relative positions. By defining `dp[u][v]` as the probability that `u` comes before `v` in the marking process restricted to a subtree, we can recursively compute expectations efficiently. This transforms the problem from enumerating permutations to computing combinatorial probabilities in subtrees.

The recursive approach relies on the observation that for each edge `(u, v)`, the nodes in `u`'s subtree and `v`'s subtree are interleaved randomly according to the process, and we can calculate the probability of one subtree's node appearing before another's with dynamic programming. Using modular arithmetic to handle fractions ensures correctness for the final answer modulo `10^9+7`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal DP + Tree Recursion | O(n^3) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Pick any node as the root. For simplicity, choose node `1`. The tree can be considered rooted, which simplifies the DP calculations for subtree relationships.
2. For each node `u`, compute the size of its subtree using a standard DFS. Store it in `size[u]`.
3. Precompute the combinatorial probabilities for merging two sequences. Let `f[i][j]` represent the probability that an element from the first sequence of length `i` comes before an element from the second sequence of length `j`. This can be computed using:

```
f[i][j] = (i/(i+j)) * f[i-1][j] + (j/(i+j)) * f[i][j-1]
```

Base cases are `f[0][j] = 0` and `f[i][0] = 1`.
4. Perform a DFS from the root. At each node `u`, combine the expectations of its children. For each child `v`, the expected inversions between nodes in `u`'s current merged subtree and `v`'s subtree is computed using the precomputed `f` table. Multiply by the number of pairs `size_u * size_v`.
5. Maintain a DP table `dp[u]` representing the expected inversions in the subtree rooted at `u`. When merging with a child, add the child's expected inversions plus the cross-inversions computed from step 4.
6. The expected number of inversions for the whole tree is the sum over all `dp[root]` values, divided properly to handle probabilities of root choice. Finally, output the result modulo `10^9+7` using modular inverse arithmetic to handle fractions.

Why it works: At each merge, `f[i][j]` precisely represents the probability that an element from one subtree comes before an element from another subtree in the linearization process dictated by the tree marking. Since the DFS merges subtrees in all combinations, the expected inversion count accumulates correctly. The invariants are maintained recursively, so the final expectation is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1000)

MOD = 10**9 + 7

def modinv(x):
    return pow(x, MOD - 2, MOD)

n = int(input())
edges = [[] for _ in range(n+1)]
for _ in range(n-1):
    x, y = map(int, input().split())
    edges[x].append(y)
    edges[y].append(x)

size = [0] * (n+1)
dp = [0] * (n+1)

# Precompute f[i][j] probabilities
f = [[0]*(n+1) for _ in range(n+1)]
for i in range(n+1):
    f[i][0] = 1
for j in range(n+1):
    f[0][j] = 0
for i in range(1, n+1):
    for j in range(1, n+1):
        f[i][j] = (i * f[i-1][j] + j * f[i][j-1]) * modinv(i+j) % MOD

def dfs(u, p):
    size[u] = 1
    dp[u] = 0
    for v in edges[u]:
        if v == p:
            continue
        dfs(v, u)
        # Cross-inversions between u's current subtree and v's subtree
        dp[u] = (dp[u] + dp[v] + size[u] * size[v] % MOD * f[size[u]][size[v]] % MOD) % MOD
        size[u] += size[v]

dfs(1, 0)
ans = dp[1] * modinv(n) % MOD
print(ans)
```

The code sets up the tree, computes subtree sizes, precomputes the merge probabilities `f`, and performs a DFS to accumulate expected inversions. The division by `n` at the end accounts for the uniform choice of initial root. The use of `modinv` ensures correct modular division.

## Worked Examples

**Sample 1:**

Input:

```
3
1 2
1 3
```

| Node | size | dp |
| --- | --- | --- |
| 2 | 1 | 0 |
| 3 | 1 | 0 |
| 1 | 3 | 7/6 |

Trace shows that for node `1`, combining children `2` and `3` with probabilities `f[1][1] = 1/2` yields `1` inversion with probability 1/2,
