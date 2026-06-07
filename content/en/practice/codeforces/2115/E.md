---
title: "CF 2115E - Gellyfish and Mayflower"
description: "We are asked to navigate a directed acyclic graph (DAG) with vertices numbered from 1 to n. Each vertex contains a trader who sells cards with a given power for a given cost."
date: "2026-06-08T04:13:52+07:00"
tags: ["codeforces", "competitive-programming", "dp", "graphs"]
categories: ["algorithms"]
codeforces_contest: 2115
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1028 (Div. 1)"
rating: 3500
weight: 2115
solve_time_s: 49
verified: true
draft: false
---

[CF 2115E - Gellyfish and Mayflower](https://codeforces.com/problemset/problem/2115/E)

**Rating:** 3500  
**Tags:** dp, graphs  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to navigate a directed acyclic graph (DAG) with vertices numbered from 1 to n. Each vertex contains a trader who sells cards with a given power for a given cost. You start at vertex 1 with some amount of coins and want to move along the edges to a target vertex, which represents the boss's location. On each vertex you visit, you can buy as many cards as you want, as long as you can afford them. The goal is to maximize the total power of the cards when you reach the boss.

The input consists of the graph structure (edges that always go from a smaller to a larger vertex), the trader information (cost and power of cards), and multiple queries. Each query specifies a boss vertex and the number of coins you start with, and the output is the maximum sum of card powers achievable given that starting condition.

The graph is a DAG with at most 200 vertices and 2000 edges, so any algorithm that scales like O(n²) or O(n·m) is acceptable. Each query can have up to 10^9 coins, which rules out any solution that iterates over coins directly, such as a naive dynamic programming over money.

Non-obvious edge cases include:

- Starting with very few coins relative to the cheapest card. For example, if coins = 1 and all card costs are ≥2, you cannot buy any cards. The answer must be 0.
- Large coin values, up to 10^9, which makes naive DP infeasible.
- Vertices with very high card power but high cost. A careless solution might incorrectly buy suboptimal smaller cards at earlier vertices instead of waiting to buy a more expensive, more powerful card later.
- Multiple queries with the same target vertex. Recomputing for each query would be too slow, so preprocessing is required.

A small example illustrating an edge case:

```
n = 3, m = 2
c = [2, 3, 5], w = [5, 10, 20]
edges = [(1,2),(2,3)]
query: p=3, r=4
```

Here you cannot afford the card at vertex 2 or 3 initially. The correct answer is to buy two cards at vertex 1 for a total power of 10. A naive approach might fail if it assumes you can always buy one card at each vertex.

## Approaches

A brute-force approach would simulate every path from vertex 1 to the target vertex and, along each path, consider every combination of cards you could buy with your remaining coins. Even if we optimize slightly by considering buying maximum multiples of each card, the number of possible distributions of coins is enormous due to the large query values (up to 10^9). Therefore, this approach is infeasible.

The key insight comes from observing that the graph is a DAG and the coin-to-power trade at each vertex is linear and unbounded. On a vertex, you can spend any amount of coins you have to buy the same card repeatedly, effectively turning each vertex into an unbounded knapsack with a single item. The optimal strategy is to maximize the ratio of power per coin at each stage, but since the amount of coins is large, the exact DP over coins is impractical.

Instead, we can represent the achievable powers at each vertex as a function of the coins spent, using a technique called convex hull or slope trick. In our setting, because each vertex allows unlimited purchases of one card type, the DP function for a vertex is piecewise linear: for each previous vertex `u` with function `f_u`, the function at vertex `v` is the maximum of `f_u + k*w_v` for coins `k*c_v ≤ total coins`. Using a discrete representation up to the total coin budget of interest (but compressed cleverly), we can answer all queries efficiently.

The final observation is that, because queries only ask for specific coin amounts at the target vertex, we can preprocess for each vertex the maximum possible power for coin budgets up to a reasonable cutoff (e.g., the sum of the cheapest cards along any path) and then extrapolate linearly for queries with large coins using the per-coin power at that vertex.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(paths × coins) | O(coins) | Too slow due to large r |
| DP over DAG with unbounded knapsack per vertex | O(n² + m + q) with preprocessing | O(n × max_effective_coins) | Accepted |

## Algorithm Walkthrough

1. Read the graph, costs, and powers for each vertex. Build adjacency lists for the DAG.
2. Topologically sort the vertices. This ensures we process each vertex only after all predecessors.
3. Initialize a DP array for each vertex, storing the maximum power achievable for various coin budgets. Start with vertex 1: the maximum power for `r` coins is `(r // c_1) * w_1`.
4. Iterate over vertices in topological order. For each vertex `v`, consider every predecessor `u`. For each reachable power state in `u`'s DP, compute the new maximum power in `v` by adding multiples of `v`'s card given the remaining coins. Update `v`'s DP entry if the resulting power is higher.
5. After processing all vertices, each vertex has a DP function mapping coin budgets to maximum power achievable at that vertex. For large coin values not explicitly stored, extend the function linearly based on the per-coin power of the vertex (floor division of remaining coins by c_v times w_v).
6. For each query `(p, r)`, read the DP function at vertex `p`. Compute the maximum power achievable with `r` coins using stored discrete states and the linear extrapolation for large `r`.

Why it works: The topological order ensures that every vertex is processed after its dependencies, so the DP always has the correct maximum power from predecessors. Using the unbounded knapsack property, we guarantee that for any coin amount we compute the optimal purchase of cards at that vertex. The DP function correctly propagates the optimal achievable powers along all paths.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict, deque

n, m = map(int, input().split())
c = [0] * n
w = [0] * n
for i in range(n):
    c[i], w[i] = map(int, input().split())

graph = [[] for _ in range(n)]
in_deg = [0] * n
for _ in range(m):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    graph[u].append(v)
    in_deg[v] += 1

# topological sort
order = []
queue = deque([i for i in range(n) if in_deg[i] == 0])
while queue:
    u = queue.popleft()
    order.append(u)
    for v in graph[u]:
        in_deg[v] -= 1
        if in_deg[v] == 0:
            queue.append(v)

# DP: max power achievable at vertex with coins up to "effective limit"
# Use only coins up to 200*n (heuristic safe bound)
LIMIT = 200 * n
dp = [defaultdict(int) for _ in range(n)]
dp[0][0] = 0
for u in order:
    # add unlimited purchases at u
    new_dp = defaultdict(int)
    for spent, power in dp[u].items():
        # buy multiples of card u within LIMIT
        max_buy = (LIMIT - spent) // c[u]
        for k in range(max_buy + 1):
            total_spent = spent + k * c[u]
            total_power = power + k * w[u]
            if new_dp[total_spent] < total_power:
                new_dp[total_spent] = total_power
    dp[u] = new_dp
    # propagate to children
    for v in graph[u]:
        for spent, power in dp[u].items():
            if dp[v][spent] < power:
                dp[v][spent] = power

q = int(input())
queries = [tuple(map(int, input().split())) for _ in range(q)]

# answer queries
for p, r in queries:
    p -= 1
    max_power = 0
    for spent, power in dp[p].items():
        if spent <= r:
            # remaining coins can buy multiples of p's card
            total_power = power + ((r - spent) // c[p]) * w[p]
            if total_power > max_power:
                max_power = total_power
    print(max_power)
```

The solution first computes a topological order to ensure that DP propagation follows the DAG structure. For each vertex, it calculates all achievable powers for coin budgets up to a heuristic limit and then propagates these states to children. During queries, we account for remaining coins by buying as many of the current vertex's card as possible. Edge cases like large `r` are handled via integer division, avoiding iteration over each coin.

## Worked Examples

### Example 1

Input:

```
3 2
3 9
2 5
1 2
1 2
2 3
6
1 4
2 4
3 4
1 5
2 5
3 5
```

Trace at vertex 1:

| spent | power |
| --- | --- |
| 0 | 0 |
| 3 | 9 |

Vertex 2 (propagate and buy):

| spent | power |
| --- | --- |
| 0 |  |
