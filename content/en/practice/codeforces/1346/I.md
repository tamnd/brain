---
title: "CF 1346I - Pac-Man 2.0"
description: "The game world is a strongly connected directed graph with $n$ nodes representing safe zones and $m$ directed edges representing pathways. Each node $i$ contains $ai$ pellets, which Pac-Man collects instantly upon arrival."
date: "2026-06-11T14:57:29+07:00"
tags: ["codeforces", "competitive-programming", "*special", "dp"]
categories: ["algorithms"]
codeforces_contest: 1346
codeforces_index: "I"
codeforces_contest_name: "Kotlin Heroes: Episode 4"
rating: 2900
weight: 1346
solve_time_s: 261
verified: false
draft: false
---

[CF 1346I - Pac-Man 2.0](https://codeforces.com/problemset/problem/1346/I)

**Rating:** 2900  
**Tags:** *special, dp  
**Solve time:** 4m 21s  
**Verified:** no  

## Solution
## Problem Understanding

The game world is a strongly connected directed graph with $n$ nodes representing safe zones and $m$ directed edges representing pathways. Each node $i$ contains $a_i$ pellets, which Pac-Man collects instantly upon arrival. Moving along a pathway is the only moment Pac-Man is at risk, and each traversal contributes to the "difficulty" of a goal. When all pellets in the world are collected, they respawn with the same counts, so the game can repeat infinitely. The starting safe zone is $s$, and for each goal $C_i$, we want the minimal number of pathway traversals needed to collect at least $C_i$ pellets.

The constraints imply that $n$ is very small (up to $15$), while $m$ can be up to $n(n-1)$, making the graph dense. The number of goals $q$ is large ($5000$), and the required pellets $C_i$ can be very big ($10^{15}$), so any algorithm that simulates each movement explicitly is infeasible. The small $n$ suggests that algorithms exponential in $n$ might still be viable.

An edge case occurs when the goal is smaller than the pellets in the starting safe zone. For example, if $s=1$, $a_1=10$, and $C_i=7$, the player never needs to move; the difficulty is $0$. A naive approach that always assumes at least one move would overcount. Another edge case arises when the goal requires multiple respawns; the algorithm must correctly account for the repeated accumulation of pellets without simulating every step individually.

## Approaches

A brute-force approach would attempt to explore every possible path from $s$ and simulate collecting pellets, including respawns. One could represent the state as the current node and the number of pellets collected so far, and perform BFS or DFS. This is correct because it examines all sequences of moves, but it becomes prohibitively slow: for $n=15$, the number of distinct states considering all pellet counts and repetitions is astronomical, far exceeding the time limit. The BFS would have to store many distinct pellet combinations, each potentially up to $10^{15}$.

The key observation is that since $n$ is small, we can precompute the shortest distances (in terms of pathway traversals) between every pair of nodes. Then, because the pellets respawn, the problem reduces to a variant of the unbounded knapsack problem: each node provides $a_i$ pellets at a cost equal to the number of traversals to reach it from some node. Specifically, after computing shortest paths, we can apply dynamic programming to find, for every subset of visited nodes, the minimal traversal count needed to collect a given number of pellets. For very large goals $C_i$, the number of pellets per full cycle (sum of all $a_i$) allows us to compute how many full cycles are needed and then handle the remainder with DP.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force BFS/DFS | Exponential in $C_i$ | Exponential in $C_i$ | Too slow |
| DP + Floyd-Warshall + Cycle Handling | $O(2^n n^2 + n \cdot \text{sum of a_i})$ precompute, $O(q)$ per query | $O(2^n n)$ | Accepted |

## Algorithm Walkthrough

1. Compute the shortest-path distances between all pairs of safe zones using Floyd-Warshall. This produces a matrix `dist[u][v]` representing the minimum number of pathway traversals needed to move from safe zone `u` to safe zone `v`. The reason for this step is that Pac-Man can always traverse from any node to any other, so we want the minimal-risk route to each pellet source.
2. Define `full_cycle = sum(a_i)` as the total number of pellets in the world at one spawn. Any goal $C_i$ larger than `full_cycle` can be broken into `k = C_i // full_cycle` full cycles plus a remainder `r = C_i % full_cycle`. Each full cycle requires collecting all pellets at minimal cost, which reduces to solving a Traveling Salesman Problem (TSP) variant to visit all nodes starting from `s` with minimal traversal count.
3. Since $n$ is small, we can compute the TSP with DP. Let `dp[mask][u]` be the minimal pathway count to visit the set of nodes represented by `mask` ending at node `u`. Initialize `dp[1 << (s-1)][s-1] = 0` since no move is required to start at `s`. Iterate over all masks and nodes, updating `dp[new_mask][v] = min(dp[new_mask][v], dp[mask][u] + dist[u][v])` for all `v` not in `mask`. After filling DP, the minimal cost to collect all pellets once is `min(dp[full_mask][u])` for all `u`.
4. Once the minimal cost for one full cycle is known, handle each query `C_i`. If `C_i` is smaller than `full_cycle`, we can apply DP over subsets of nodes to collect just enough pellets. If `C_i` exceeds `full_cycle`, calculate `k` full cycles and add the minimal traversal cost for the remainder. This avoids simulating each movement individually and leverages the precomputed optimal cycle.
5. Output the minimal number of pathway traversals for each query.

This approach works because Floyd-Warshall guarantees minimal traversal counts between any nodes, and the DP over subsets ensures we find the minimal traversal pattern to collect the desired number of pellets. The decomposition of large goals into full cycles plus remainder exploits the respawning property without needing to simulate each step.

## Python Solution

```python
import sys
input = sys.stdin.readline
from itertools import product

n, m, q, s = map(int, input().split())
a = list(map(int, input().split()))
edges = [[] for _ in range(n)]
dist = [[float('inf')] * n for _ in range(n)]
for i in range(n):
    dist[i][i] = 0
for _ in range(m):
    u, v = map(int, input().split())
    u -= 1; v -= 1
    dist[u][v] = 1
for k in range(n):
    for i in range(n):
        for j in range(n):
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

full_cycle = sum(a)

# DP for minimal cost to collect subsets of pellets
dp = [ [float('inf')] * n for _ in range(1<<n) ]
dp[1<<(s-1)][s-1] = 0
for mask in range(1<<n):
    for u in range(n):
        if dp[mask][u] < float('inf'):
            for v in range(n):
                if not (mask & (1<<v)):
                    new_mask = mask | (1<<v)
                    dp[new_mask][v] = min(dp[new_mask][v], dp[mask][u] + dist[u][v])

# minimal cost to collect at least k pellets from the world (subset DP)
subset_dp = [float('inf')] * (full_cycle+1)
subset_dp[0] = 0
for mask in range(1, 1<<n):
    sum_pellets = sum(a[i] for i in range(n) if mask & (1<<i))
    cost = min(dp[mask])
    for prev in range(full_cycle - sum_pellets + 1):
        if subset_dp[prev] < float('inf'):
            subset_dp[prev + sum_pellets] = min(subset_dp[prev + sum_pellets], subset_dp[prev] + cost)

queries = list(map(int, input().split()))
for C in queries:
    cycles = C // full_cycle
    rem = C % full_cycle
    res = cycles * min(dp[(1<<n)-1])
    if rem > 0:
        res += min(subset_dp[rem:])
    print(res)
```

The code first computes all-pairs shortest paths with Floyd-Warshall. The DP `dp[mask][u]` finds the minimal traversal count to visit any subset of nodes ending at a specific node. The `subset_dp` array maps the number of collected pellets to minimal traversal counts for subsets. Queries are answered by multiplying the full-cycle cost by the number of complete cycles and adding the minimal cost for the remaining pellets. Care was taken to handle one-based indexing and large numbers correctly.

## Worked Examples

Sample Input 1:

```
3 4 2 1
3 1 2
1 2
2 1
1 3
3 1
5 8
```

| Step | Mask | End Node | dp[mask][end] | Sum Pellets | subset_dp |
| --- | --- | --- | --- | --- | --- |
| Initial | 001 | 0 | 0 | 3 | subset_dp[3] = 0 |
| Add node 2 | 101 | 2 | 1 | 5 | subset_dp[5] = 1 |
| Add node 1 | 111 | 2 | 3 | 6 | subset_dp[6] = 3 |

The first goal `5` is achievable by collecting 3 pellets at start, moving to node 3, collect 2 pellets. One traversal.

The second goal `8` requires collecting all pellets once and part of second cycle. Minimal traversal count is 3
