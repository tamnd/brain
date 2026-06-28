---
title: "CF 104885A - \u0414\u0435\u0442\u0430\u043b\u0438 \u0438 \u0440\u0435\u0441\u0443\u0440\u0441\u044b"
description: "We are given a production setup with several workers. Each worker produces a fixed number of identical parts, and every part consumes a fixed amount of metal. All produced metal is then packed into containers, where each container can hold only a limited weight."
date: "2026-06-28T09:07:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104885
codeforces_index: "A"
codeforces_contest_name: "Municipal stage of ROI in Nizhny Novgorod 2023"
rating: 0
weight: 104885
solve_time_s: 28
verified: false
draft: false
---

[CF 104885A - \u0414\u0435\u0442\u0430\u043b\u0438 \u0438 \u0440\u0435\u0441\u0443\u0440\u0441\u044b](https://codeforces.com/problemset/problem/104885/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a production setup with several workers. Each worker produces a fixed number of identical parts, and every part consumes a fixed amount of metal. All produced metal is then packed into containers, where each container can hold only a limited weight. Each filled container costs a fixed amount of money.

The task is to compute the total cost of buying enough containers to store all the metal required for production.

Concretely, the total amount of metal is determined by multiplying the number of workers, the number of parts per worker, and the metal required per part. This gives a single total weight. Since containers have limited capacity, we must determine how many full containers are needed to hold this total weight, rounding up because partial containers are still paid as full ones. Finally, the cost is obtained by multiplying the number of containers by the price per container.

Even though the statement is partially garbled, the structure is consistent with a classic “ceil division after total aggregation” problem.

The implied input is four or five integers representing the production parameters and the container pricing. The output is a single integer: the total cost.

From a complexity standpoint, all quantities can be large enough that the product of three integers may reach up to around 10^18 if not handled carefully. This immediately rules out any simulation or iterative packing approach. The solution must work in constant time using arithmetic operations only.

A subtle issue appears when handling division: if the total metal is exactly divisible by container capacity, we must not add an extra container. Conversely, if there is any remainder, even extremely small, it still requires one additional container.

An example of a potential pitfall:

Input:

N = 2, M = 3, K = 4, L = 10, S = 5

Total metal is 2 × 3 × 4 = 24. Each container holds 10, so we need ceil(24 / 10) = 3 containers. Cost is 3 × 5 = 15.

A naive integer division approach without rounding up would compute 24 // 10 = 2 containers and produce an incorrect answer.

## Approaches

The brute-force way to think about the problem is to simulate packing metal into containers one kilogram at a time. We compute the total metal and then repeatedly subtract container capacity until nothing remains, counting how many containers are used. This is correct, because it directly mirrors the physical process of filling containers. However, this approach becomes unnecessary once we observe that only the total weight matters, not the individual distribution of parts.

The inefficiency appears when the total metal becomes large. If the total is on the order of 10^18, simulating even a single unit step is impossible. Even simulating container-by-container subtraction would require up to 10^18 operations in the worst case, which is far beyond any feasible limit.

The key observation is that the process reduces to integer division with rounding up. Once total metal is known, the number of containers depends only on whether the division by capacity has a remainder. This collapses the entire packing process into a constant-time arithmetic expression.

We compute total metal as N × M × K, then compute the ceiling of total metal divided by L, and multiply by S.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute |  |  |  |
