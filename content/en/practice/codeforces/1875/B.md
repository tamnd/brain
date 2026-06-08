---
title: "CF 1875B - Jellyfish and Game"
description: "We are asked to simulate a turn-based exchange game between two players, Jellyfish and Gellyfish. Jellyfish owns an array of apples with integer values, and Gellyfish owns a different array."
date: "2026-06-09T00:57:22+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1875
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 901 (Div. 2)"
rating: 1200
weight: 1875
solve_time_s: 34
verified: false
draft: false
---

[CF 1875B - Jellyfish and Game](https://codeforces.com/problemset/problem/1875/B)

**Rating:** 1200  
**Tags:** brute force, greedy, implementation  
**Solve time:** 34s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to simulate a turn-based exchange game between two players, Jellyfish and Gellyfish. Jellyfish owns an array of apples with integer values, and Gellyfish owns a different array. They play for $k$ rounds, taking turns: Jellyfish moves on odd rounds, Gellyfish on even rounds. On their turn, a player may swap one of their apples with one of the opponent's or do nothing. Both aim to maximize the sum of their own apples. We need to calculate Jellyfish's final sum after $k$ rounds, assuming both play optimally.

The key input parameters are the sizes of the arrays $n$ and $m$, and the number of rounds $k$. Each apple value is up to $10^9$, and $k$ can be extremely large ($10^9$), far exceeding the arrays’ lengths. This immediately implies that simulating each round directly is infeasible. We must exploit the observation that no player will ever swap in a way that reduces their sum, and once all advantageous swaps are exhausted, additional rounds have no effect.

Edge cases include when the arrays are already optimal (largest values on Jellyfish's side), when $k$ is smaller than the number of potential swaps, or when $k$ exceeds the number of swaps needed. For example, if Jellyfish has `[1, 2]` and Gellyfish `[3, 4]` with $k=10^9$, only the two swaps that increase Jellyfish's sum are relevant; the rest of the rounds do nothing.

## Approaches

The brute-force approach would iterate over each of the $k$ rounds, finding the optimal swap for the player whose turn it is. On eac
