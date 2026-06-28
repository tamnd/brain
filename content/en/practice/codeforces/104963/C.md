---
title: "CF 104963C - \u041d\u0430\u043b\u043e\u0433"
description: "We are given a collection of apartments, each with an initial area. Daniil can reduce the area of any apartment by repeatedly applying an operation: choose a factor $y$, pay $y$ coins, and divide the current area by $y$, but only if the result remains an integer."
date: "2026-06-28T18:20:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104963
codeforces_index: "C"
codeforces_contest_name: "\u0412\u044b\u0441\u0448\u0430\u044f \u043f\u0440\u043e\u0431\u0430 - 2022. \u0417\u0430\u043a\u043b\u044e\u0447\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f"
rating: 0
weight: 104963
solve_time_s: 29
verified: false
draft: false
---

[CF 104963C - \u041d\u0430\u043b\u043e\u0433](https://codeforces.com/problemset/problem/104963/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of apartments, each with an initial area. Daniil can reduce the area of any apartment by repeatedly applying an operation: choose a factor $y$, pay $y$ coins, and divide the current area by $y$, but only if the result remains an integer. This operation can be applied multiple times to the same apartment, meaning the final area of each apartment must be some divisor obtained through a sequence of factorizations of the original value.

The cost is not tied to the number of steps but to the product of chosen division factors across steps. If an apartment of area $a$ is reduced through factors $y_1, y_2, \dots, y_t$, the total cost is $y_1 + y_2 + \dots + y_t$, and the final area becomes $a / (y_1 y_2 \cdots y_t)$. The goal is to distribute at most $k$ coins across apartments so that the maximum final apartment area is as small as possible.

The output is a single number: the smallest possible value of the maximum apartment area after optimal reductions.

The constraints $n \le 10^5$ and $a_i \le 10^6$ immediately rule out any per-query factorization or per-value dynamic programming over large ranges. A solution must precompute information up to $10^6$ and then process all apartments in near-linear or $O(n \log A)$ time. Since $k$ can be as large as $10^9$, any approach that simulates coin spending step by step is impossible.

A naive interpretation might try to simulate all sequences of divisions per apartment or greedily reduce the largest apartment repeatedly. Both fail because the same reduction cost depends on factor choices, not just on final value.

A subtle edge case arises when an apartment has a prime area. For example, $a_i = 997$. The only way to reduce it is dividing by 997 at cost 997, which is extremely expensive. Any greedy strategy that repeatedly reduces the current maximum without considering cost efficiency will waste budget on composite numbers first and then get stuck with primes that dominate the maximum.

Another edge case is when all apartments are equal and composite, for example $a = [12, 12, 12]$. The optimal strategy might reduce some apartments aggressively while leaving others unchanged, so treating all apartments uniformly leads to suboptimal budget usage.

## Approaches

A brute-force strategy would try to assign each apartment a final value $b_i$ such that $b_i$ divides $a_i$, and the cost to reduce $a_i$ to $b_i$ is computed by searching all sequences of valid divisions. For each apartment, we would enumerate all reachable divisors and their minimum cost, then try combinations across apartments to ensure the maximum $b_i$ is minimized under total cost $k$. This quickly explodes because even a single number up to $10^6$ can have thousands of divisor chains, and combining choices across $10^5$ apartments makes it exponential.

The key observation is that we never need the exact sequence of operations. We only care about the best way to reduce each number to a threshold value $x$, and whether it is possible to make all apartments at most $x$ with total cost $\le k$. This transforms the problem into a decision problem: for a fixed $x$, compute the minimum cost required to reduce each $a_i$ to at most $x$, then sum over all apartments. If we can answer this quickly, we can binary search the smallest feasible $x$.

The second crucial insight is how to compute the minimal cost for reducing a number $a$ down to
