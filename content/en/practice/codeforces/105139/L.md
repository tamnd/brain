---
title: "CF 105139L - LCMs"
description: "We are given a weighted complete graph whose vertices are integers starting from 2 upward. Moving directly from an integer $x$ to another integer $y$ costs $mathrm{lcm}(x,y)$."
date: "2026-06-27T17:00:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105139
codeforces_index: "L"
codeforces_contest_name: "The 2024 International Collegiate Programming Contest in Hubei Province, China"
rating: 0
weight: 105139
solve_time_s: 46
verified: false
draft: false
---

[CF 105139L - LCMs](https://codeforces.com/problemset/problem/105139/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a weighted complete graph whose vertices are integers starting from 2 upward. Moving directly from an integer $x$ to another integer $y$ costs $\mathrm{lcm}(x,y)$. A traveler starts at $a$ and wants to reach $b$, and they are allowed to visit any intermediate integers as long as they are at least 2. The goal is to choose a sequence of intermediate jumps so that the sum of LCM costs along the path is minimized.

The key difficulty is that although every pair of integers is directly connected, the cost function is highly non-linear. A direct jump might be expensive, but splitting the journey through carefully chosen intermediate numbers might reduce the total cost.

The constraints allow up to 1000 queries, and the values of $a$ and $b$ can be as large as $10^7$. This immediately rules out any approach that tries to explore paths dynamically over a large range of nodes. Even a Dijkstra over all integers is impossible because the graph size is unbounded up to $10^7$, and each node connects to infinitely many others in principle.

A naive approach would try all intermediate nodes $k$ and compute a two-step path $a \to k \to b$. That already fails because $k$ ranges up to $10^7$, making each query linear in the value range. Another naive attempt is to try multi-step shortest paths, but the structure does not allow classical shortest path techniques at this scale.

A subtle edge case appears when $a = b$. In that case, no movement is required, and the answer should be zero. Any algorithm that assumes at least one move would incorrectly output a positive cost like $\mathrm{lcm}(a,a)=a$, which is wrong because we are not forced to move.

## Approaches

The brute-force perspective starts from the definition of the problem. If we fix a path, its cost is the sum of LCMs on consecutive edges. The most straightforward idea is to treat every integer as a node and run a shortest path algorithm from $a$ to $b$. From each node $x$, we could try transitioning to every possible integer $y$, with cost $\mathrm{lcm}(x,y)$. This is correct in theory because it exactly matches the problem definition.

However, the branching factor is effectively unbounded. Even if we artificially restrict to $1 \ldots 10^7$, each node still has $10^7$ outgoing edges. A single shortest path run would require on the order of $10^{14}$ operations, which is completely infeasible.

The key structural observation is that optimal paths never need long chains of arbitrary intermediate nodes. If we look at a two-step path $a \to k \to b$, the cost is $\mathrm{lcm}(a,k) + \mathrm{lcm}(k,b)$. The behavior of LCM strongly depends on divisibility. In particular, if we choose $k$ such that it divides $a$, then $\mathrm{lcm}(a,k)=a$, which is the smallest possible value involving $a$. Similarly, if $k$ divides $b$, then $\mathrm{lcm}(k,b)=b$.

This reduces the p
