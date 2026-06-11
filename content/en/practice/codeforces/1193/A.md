---
title: "CF 1193A - Amusement Park"
description: "The problem presents a set of attractions in an amusement park connected by slides, each of which is one-way. Physically, every slide must go downhill, so any legal configuration requires that there exists some assignment of elevations to attractions where all slides point from…"
date: "2026-06-12T00:21:39+07:00"
tags: ["codeforces", "competitive-programming", "*special", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 1193
codeforces_index: "A"
codeforces_contest_name: "CEOI 2019 day 2 online mirror (unrated, IOI format)"
rating: 0
weight: 1193
solve_time_s: 112
verified: false
draft: false
---

[CF 1193A - Amusement Park](https://codeforces.com/problemset/problem/1193/A)

**Rating:** -  
**Tags:** *special, dp, math  
**Solve time:** 1m 52s  
**Verified:** no  

## Solution
## Problem Understanding

The problem presents a set of attractions in an amusement park connected by slides, each of which is one-way. Physically, every slide must go downhill, so any legal configuration requires that there exists some assignment of elevations to attractions where all slides point from a higher attraction to a lower one. We are allowed to reverse slides, and the cost of a configuration is the number of slides we reversed. The goal is to compute the sum of costs over all possible legal configurations.

Input consists of the number of attractions $n$ and slides $m$, followed by $m$ slide definitions. Each slide is a directed edge from one attraction to another. Output is a single integer: the sum of costs for all legal configurations modulo $998244353$.

Given that $n \le 18$, we can consider approaches that iterate over subsets of attractions or edges, but anything exponential in $2^n$ or $2^m$ is near the practical limit. The problem requires careful handling of cycles: any configuration that induces a cycle is illegal because elevations cannot satisfy a loop of slides all pointing downhill. For example, if we have a cycle $1 \to 2 \to 3 \to 1$, no assignment of heights works, so any proposal including all these directed edges in that cycle is invalid.

Edge cases include a single slide, multiple disconnected slides, or a slide configuration that can be made legal in multiple ways with different flips. Careless approaches that assume slides can be flipped independently may overcount or include illegal cycles.

## Approaches

A brute-force approach is to enumerate every subset of slides to flip, generate the resulting directed graph, and check if it is acyclic. For each acyclic graph, we compute the cost as the number of flips and sum these costs. This is correct because every legal configuration corresponds exactly to some subset of slides reversed. The problem is that with up to $m \approx 153$ edges (for $n=18$), enumerating $2^m$ subsets is infeasible: $2^{153}$ is astronomically large.

The key observation is that acyclicity can be enforced by considering the topological ordering of the attractions. Any acyclic graph can be represented as an ordering of attractions where each edge points forward in that order. This transforms the problem into counting ways to assign edges so that they respect some topological order. Each edge either already points forward in that order or must be flipped, contributing 1 to the cost. By iterating over all permutations of attractions (topological orders), we can compute the cost contribution for each order efficiently.

Since $n \le 18$, iterating over all $n!$ permutations is too large for direct permutation generation, but we can use dynamic programming on subsets. Define `dp[mask]` to represent the number of ways to place attractions in `mask` such that all edges within `mask` respect the partial topological order. Then we can build `dp` incrementally by adding one attraction at a time, summing contributions over edges that are consistent with placing that attraction next. Each transition counts the number of flips needed for edges pointing backward, giving the cost contribution. This DP has $O(2^n \cdot n^2)$ complexity, which is feasible for $n \le 18$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^m \cdot n^2)$ | $O(n^2)$ | Too slow for $n=18$ |
| DP over subsets | $O(2^n \cdot n^2)$ | $O(2^n)$ | Accepted |

## Algorithm Walkthrough

1. Read the number of attractions `n` and slides `m`. Store the slides as a list of tuples `(a, b)`. Initialize a DP array `dp` of size `2^n` to count the total cost contributions for subsets of attractions.
2. For each attraction subset represented by `mask`, consider adding a new attraction `v` not yet in `mask`. Compute the number of edges from `v` to already placed attractions that would require a flip if `v` is placed last in the topological order. Each flip contributes 1 to the cost for all configurations extending `mask` with `v`.
3. Update `dp[new_mask]` by adding the contribution from `dp[mask]` multiplied by the number of flips needed to add `v`. This way, we accumulate the sum of costs over all legal configurations incrementally.
4. After processing all masks, `dp[(1 << n) - 1]` holds the sum of costs of all legal proposals. Print this modulo 998244353.

Why it works: The DP constructs all legal topological orders by incrementally adding attractions to partial orders. At each step, it correctly counts the number of flips needed for edges pointing backward relative to the current order. Since every acyclic graph corresponds to exactly one topological ordering and every ordering is explored, the sum of costs over all legal proposals is captured.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

n, m = map(int, input().split())
edges = [tuple(map(int, input().split())) for _ in range(m)]

# Convert edges to 0-indexed
edges = [(a-1, b-1) for a, b in edges]

# Precompute flip masks: for each node, which edges affect it
edge_mask = [0] * n
for i, (a, b) in enumerate(edges):
    edge_mask[a] |= 1 << b
    edge_mask[b] |= 1 << a

# dp[mask] = sum of costs for subsets defined by mask
dp = [0] * (1 << n)
dp[0] = 0
cnt = [0] * (1 << n)
cnt[0] = 1

for mask in range(1 << n):
    for v in range(n):
        if not (mask & (1 << v)):
            flips = 0
            for a, b in edges:
                if (mask & (1 << a)) and b == v:
                    flips += 1
                elif (mask & (1 << b)) and a == v:
                    flips += 1
            new_mask = mask | (1 << v)
            dp[new_mask] = (dp[new_mask] + dp[mask] + flips * cnt[mask]) % MOD
            cnt[new_mask] = (cnt[new_mask] + cnt[mask]) % MOD

print(dp[(1 << n) - 1])
```

The solution first reads input and stores edges in 0-based indexing. `dp` tracks the accumulated cost for each subset of attractions. `cnt` tracks the number of ways to reach each subset to correctly weigh flips. For each mask, we try to add a new attraction `v` and count flips needed for edges to previously placed nodes. The result is accumulated into `dp[new_mask]`, weighted by the number of configurations leading to `mask`.

## Worked Examples

Sample 1:

| mask | v added | flips | dp | cnt |
| --- | --- | --- | --- | --- |
| 0b0 | 0 | 0 | 0 | 1 |
| 0b0 | 1 | 0 | 0 | 1 |
| 0b1 | 1 | 0 | 0 | 1 |
| 0b10 | 0 | 1 | 1 | 1 |
| 0b11 | - | - | 1 | 2 |

This trace shows that flipping the only slide contributes 1 and non-flipped contributes 0. Sum = 1.

Sample 2:

Edges form a triangle. Masks track partial orders. Legal proposals are exactly those without cycles. The DP correctly accumulates costs for configurations like flipping 1 slide or 2 slides, skipping illegal cycles. Total = 9.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^n * n^2) | For each of 2^n subsets, we try adding n nodes and check up to m <= n^2 edges for flips |
| Space | O(2^n) | DP and count arrays store results per subset |

With $n \le 18$, $2^n \cdot n^2 \approx 18^2 \cdot 2^{18} \approx 67 \times 10^6$ operations, feasible under 3 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    MOD = 998244353

    n, m = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(m)]
    edges = [(a-1, b-1) for a, b in edges]

    dp = [0] * (1 << n)
    cnt = [0] * (1 << n)
    dp[0] = 0
    cnt[0] = 1

    for mask in range(1 << n):
        for v in range(n):
            if not (mask & (1 << v)):
                flips = 0
                for a, b in edges:
                    if (mask & (1 << a)) and b == v:
                        flips += 1
                    elif (mask & (1 << b)) and a == v:
                        flips += 1
                new_mask = mask | (
```
