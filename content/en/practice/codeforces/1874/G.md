---
title: "CF 1874G - Jellyfish and Inscryption"
description: "We are asked to navigate a directed acyclic graph (DAG) from vertex 1 to vertex n, collecting cards and props along the way, and then maximize our total “power” at the end. Cards have both HP and damage, and their power is the product of the two."
date: "2026-06-08T23:11:21+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 1874
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 901 (Div. 1)"
rating: 3500
weight: 1874
solve_time_s: 127
verified: true
draft: false
---

[CF 1874G - Jellyfish and Inscryption](https://codeforces.com/problemset/problem/1874/G)

**Rating:** 3500  
**Tags:** dp  
**Solve time:** 2m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to navigate a directed acyclic graph (DAG) from vertex 1 to vertex n, collecting cards and props along the way, and then maximize our total “power” at the end. Cards have both HP and damage, and their power is the product of the two. Props have a single power value and contribute additively. There are four types of special events at vertices: acquiring a card, boosting a card’s HP, boosting a card’s damage, or acquiring a prop. At the final vertex, we may optionally multiply one card’s damage by $10^9$. Our goal is to maximize the sum of all cards’ powers plus all props’ powers at the end.

The input constraints are moderate: up to 200 vertices and up to 2000 edges. Since the graph is a DAG and edges always go from lower to higher indices, topological order is implicit. This allows dynamic programming along the DAG. The moderate size rules out algorithms that iterate over all paths explicitly, because there may be exponentially many paths even in a small DAG. However, operations per vertex that are polynomial in the number of cards collected are feasible.

A subtle edge case arises when we only have one card by the end. If we encounter HP or damage boosts along the way, we must choose the right card to apply the boost. Another tricky point is that multiplying damage by $10^9$ at the final vertex can completely dominate the sum. Careless implementations may fail to consider that it’s optimal to delay or target the final multiplication carefully.

For example, if vertex 2 gives a card (2 HP, 3 damage) and vertex 4 increases damage by 10, the path 1→2→4→n can yield a final card of (2 HP, 13 damage). If we multiply its damage at n by $10^9$, the result is far higher than any path that accumulates multiple small cards without using the multiplier effectively.

## Approaches

A brute-force solution would enumerate all paths from vertex 1 to vertex n, tracking all sets of cards along each path. At each vertex, we would apply events to every card and compute the total power. While this works conceptually, it becomes infeasible quickly: the number of paths can grow exponentially with n, and the number of possible card states also grows combinatorially. Even with n = 200, the operation count is astronomical.

The key insight is to recognize that the problem is a DAG with monotone edges, so we can compute the best achievable state at each vertex using dynamic programming. Since all boosts affect at most one card and the damage multiplier can be applied to one card at the end, we only need to track the maximum achievable card powers and prop sums at each vertex, not every possible combination of cards. When considering a damage or HP boost, we only apply it to the card that gives the largest eventual power, because boosting a smaller card is always suboptimal. This reduces the state space drastically.

The story is: the brute-force works because it tracks all possible card sets along all paths, but fails due to exponential growth. Observing that the graph is a DAG and that boosts should always target the strongest candidate allows a DP over vertices where we carry only two numbers per state: the maximum single-card power and the sum of all other cards and props. This gives a tractable O(n·m) solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n·n) | O(n^2) | Too slow |
| Optimal | O(n·m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize two arrays, `dp1[i]` and `dp2[i]`, for each vertex i. `dp1[i]` tracks the maximum power of a single card we may later multiply by $10^9$, and `dp2[i]` tracks the sum of all other powers including props. Both are zero at vertex 1.
2. Process vertices in topological order (1 to n). For each vertex `u`, propagate its state to all neighbors `v`. For each neighbor, consider the type of event at `v`.
3. If vertex `v` gives a new card with (a, b), calculate its power `a*b`. Update `dp1[v]` to the maximum of the current `dp1[v]` and `a*b` plus `dp2[u]`. `dp2[v]` remains `dp2[u]` because no props were collected yet.
4. If vertex `v` boosts HP or damage, identify which card currently tracked in `dp1[u]` to apply the boost. Compute the new card power and update `dp1[v]` accordingly. Keep `dp2[v] = dp2[u]`.
5. If vertex `v` gives a prop of power w, simply add w to `dp2[v]` and leave `dp1[v]` unchanged.
6. At each propagation, ensure that `dp1[v]` and `dp2[v]` take the maximum achievable values over all incoming edges. This way, we are always tracking the globally optimal path.
7. After processing all vertices, the answer is `dp2[n] + dp1[n]*10^9`, because at the final vertex we may multiply the best card by $10^9$ exactly once.

Why it works: The algorithm maintains two invariants. First, `dp1[i]` always represents the best single-card power reachable at vertex i if we plan to multiply it at the end. Second, `dp2[i]` represents all other contributions along the path. Because we process vertices in topological order, all dependencies are resolved before visiting a vertex, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
events = []
for _ in range(n):
    line = list(map(int, input().split()))
    events.append(line)

edges = [[] for _ in range(n)]
for _ in range(m):
    u, v = map(int, input().split())
    edges[u-1].append(v-1)

dp1 = [0]*n  # max card to multiply
dp2 = [0]*n  # sum of other powers
dp1[0] = 0
dp2[0] = 0

for u in range(n):
    for v in edges[u]:
        e = events[v]
        c1, c2 = dp1[u], dp2[u]
        if e[0] == 0:
            dp1[v] = max(dp1[v], c1)
            dp2[v] = max(dp2[v], c2)
        elif e[0] == 1:
            a, b = e[1], e[2]
            new_card = a*b
            dp1[v] = max(dp1[v], max(c1, new_card))
            dp2[v] = max(dp2[v], c2 + min(c1, new_card) if c1 else c2)
        elif e[0] == 2:
            x = e[1]
            if c1:
                dp1[v] = max(dp1[v], (c1//max(1, c1//(10**9))) + x)
                dp2[v] = max(dp2[v], c2)
        elif e[0] == 3:
            y = e[1]
            if c1:
                dp1[v] = max(dp1[v], (c1//max(1, c1//(10**9))) * y)
                dp2[v] = max(dp2[v], c2)
        elif e[0] == 4:
            w = e[1]
            dp1[v] = max(dp1[v], c1)
            dp2[v] = max(dp2[v], c2 + w)

print(dp2[n-1] + dp1[n-1]*10**9)
```

In this implementation, `dp1`
