---
title: "CF 105167K - Keen on R\u00f6sti"
description: "We are given a queue of $n$ students arranged in a fixed order, and a probabilistic process that repeatedly acts on the student at the front."
date: "2026-06-27T10:37:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105167
codeforces_index: "K"
codeforces_contest_name: "ETH Zurich Competitive Programming Contest Spring 2024"
rating: 0
weight: 105167
solve_time_s: 30
verified: false
draft: false
---

[CF 105167K - Keen on R\u00f6sti](https://codeforces.com/problemset/problem/105167/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a queue of $n$ students arranged in a fixed order, and a probabilistic process that repeatedly acts on the student at the front. Each round behaves the same way: the front student either receives the only available Rösti with probability $\frac{a}{b}$, which immediately ends the process, or fails with probability $1 - \frac{a}{b}$. In the failure case, that student pays one coin and moves to the back of the queue.

We are asked to compute the expected total number of coins paid by a specific student, Oli, who starts at position $k$.

The key subtlety is that the queue order changes deterministically except for the front-to-back rotation, while the stopping condition depends only on a global success event. Every student contributes exactly one coin each time they are at the front and fail, and we only care about counting how many such failures involve Oli before the first success occurs anywhere.

The constraints allow $n$ up to $10^9$, so any simulation over queue states is impossible. Even a linear pass over positions is too large. The probability values are also large integers up to $10^9$, which forces modular arithmetic under $10^9+7$.

A naive approach would simulate the queue. Each step is $O(1)$, but in the worst case the process could run for arbitrarily many steps before success. The expected number of steps is infinite in a naive simulation perspective, so direct simulation is not feasible.

A more subtle edge case appears when $a = b$. In that case, the first student always succeeds immediately, so no one ever moves and Oli’s expected cost is exactly $0$. Any solution that blindly inverts probabilities without checking this degeneracy would fail due to division by zero in modular arithmetic.

Another edge case is $a = 0$, which would mean the process never terminates, but the constraints explicitly forbid it since $a \ge 1$. Still, a correct derivation must avoid assuming termination properties that depend on stronger conditions than given.

## Approaches

The brute-force view tracks the queue explicitly. At each step, we identify the front student, sample whether they succeed, and if not, we rotate the queue and increment cost for that student. We stop when success occurs. This correctly models the process but does not lead to a computable expectation in closed form and cannot be simulated efficiently because the stopping time is unbounded.

The key structural observation is that the identity of the front student cycles deterministically with period $n$, independent of probabilities. The only randomness is whether a given “visit to the front” produces success. Therefore the process can be viewed as a sequence of independent Bernoulli trials applied to successive front positions, while the queue rotation only determines which student is charged on each trial.

From Oli’s perspective, every full cycle of $n$ failures shifts his position by exactly $n$,
