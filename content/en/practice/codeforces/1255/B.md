---
title: "CF 1255B - Fridge Lockers"
description: "We are given a complete system of lockers where each locker belongs to one person and has a weight. We are allowed to install exactly $m$ undirected connections between distinct lockers. Each connection between locker $u$ and $v$ costs $au + av$."
date: "2026-06-15T23:12:05+07:00"
tags: ["codeforces", "competitive-programming", "graphs", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1255
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 601 (Div. 2)"
rating: 1100
weight: 1255
solve_time_s: 827
verified: false
draft: false
---

[CF 1255B - Fridge Lockers](https://codeforces.com/problemset/problem/1255/B)

**Rating:** 1100  
**Tags:** graphs, implementation  
**Solve time:** 13m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a complete system of lockers where each locker belongs to one person and has a weight. We are allowed to install exactly $m$ undirected connections between distinct lockers. Each connection between locker $u$ and $v$ costs $a_u + a_v$.

The structural constraint is the key difficulty: a locker is considered unsafe unless only its owner can access it under the rule that ownership is tied to knowledge of all incident edges. If a locker is connected in a way that allows any other person to infer all required unlocking information independently, then that locker becomes accessible to someone else and is no longer valid.

The condition simplifies to a graph property: every vertex must have at least one incident edge, otherwise it is trivially accessible to everyone. More importantly, any configuration that allows a vertex to be isolated or insufficiently “covered” violates privacy. The problem essentially forces us to ensure a structure where every node participates in at least one edge, while we are free to repeat edges.

We must construct exactly $m$ edges minimizing total cost.

The constraints $n \le 1000$, $m \le n$, suggest that $O(n^2)$ constructions are fine, but anything exponential or involving heavy combinatorial search is not.

A subtle edge case appears when $m < n-1$. If we try to “connect everything minimally,” a tree uses $n-1$ edges, so we cannot even form a connected structure. However, the problem does not require connectivity, only validity of privacy conditions. This is where many incorrect greedy constructions fail: they implicitly assume a spanning tree is necessary.

Another edge case is when all weights are large or zero. Since cost depends only on pair sums, repeatedly using the smallest-weight vertex is crucial; naive uniform connection strategies fail to minimize cost.

## Approaches

A brute-force approach would try all possible multisets of $m$ edges among $\binom{n}{2}$ pairs, enforcing validity constraints and computing cost. Even restricting to simple graphs, this is $\binom{n^2}{m}$-scale, which is completely infeasible.

The key simplification comes from the cost structure: every edge cost is additive in its endpoints. This suggests that optimal solutions reuse the smallest-weight vertex heavily, because pairing a large weight with another large weight is always worse than pairing it with the minimum weight.

The second structural insight is that since edges can repeat, we are not constructing a combinatorial structure like a tree or matching. We are distributing $m$ independent edges, each chosen optimally given the current state.

Once we fix a vertex $p$ with minimum weight, every optimal edge should involve $p$, except possibly a few initial edges required to satisfy feasibility when $m$ is large relative to constraints. This reduces the problem to deciding how to connect everything through a hub.

A valid construction is to first ensure every vertex is “touched” at least once by connecting it to the minimum-weight vertex, forming a star. This uses $n-1$ edges. If $m > n-1$, remaining edges should reuse the same cheapest pair $(p, q)$, where $q$ is the second smallest vertex, because that minimizes repeated cost.

If $m < n-1$, we cannot even ensure that all vertices are incident in a way that satisfies validity constraints, so no solution exists.

Thus the solution is driven by a star backbone plus repeated minimum-cost edges.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over edge sets | Exponential | Exponential | Too slow |
| Star construction with greedy reuse | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Find the index $p$ of the minimum weight element.

This vertex is the optimal hub because any edge involving it is cheaper than replacing it with a heavier endpoint.
2. If $m < n - 1$, immediately output $-1$.

We cannot even connect all vertices once, which is required for validity.
3. Construct a star by connecting $p$ to every other vertex.

This uses $n-1$ edges and guarantees every vertex is incident to at least one edge.
4. If $m = n-1$, output this construction.

The star is already optimal because every edge uses the cheapest possible center.
5. If $m > n-1$, choose any vertex $q \neq p$ (typically the second smallest weight).

The edge $(p, q)$ has minimal possible cost among all repeated edges involving $p$.
6. Append $m - (n-1)$ copies of edge $(p, q)$.

Repetition is allowed, and this choice keeps incremental cost minimal.

### Why it works

The cost of any edge is linear in its endpoints, so minimizing total cost reduces to minimizing how often large weights appear in edges. Any feasible solution must already touch every vertex at least once, which forces at least $n-1$ edge endpoints to be distributed. The cheapest way to distribute these endpoints is to centralize all connections at the minimum-weight vertex. After that point, any additional edge is independent of connectivity requirements, so each one should again minimize endpoint sum, which is achieved by repeatedly using the smallest available pair.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        p = min(range(n), key=lambda i: a[i])

        if m < n - 1:
            print(-1)
            continue

        edges = []

        for i in range(n):
            if i != p:
                edges.append((p + 1, i + 1))

        if m == n - 1:
            cost = sum(a[u - 1] + a[v - 1] for u, v in edges)
            print(cost)
            for u, v in edges:
                print(u, v)
            continue

        # m > n - 1
        q = 0 if p != 0 else 1
        cost = sum(a[u - 1] + a[v - 1] for u, v in edges)

        extra
```
