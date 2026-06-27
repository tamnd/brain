---
title: "CF 105017G - Game of Cards"
description: "Two players start with two equal-sized collections of numbers. These numbers are not directly compared; instead, they are gradually “decomposed” during a game."
date: "2026-06-28T02:09:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105017
codeforces_index: "G"
codeforces_contest_name: "Winter Cup 4.0 Online Mirror Contest"
rating: 0
weight: 105017
solve_time_s: 52
verified: false
draft: false
---

[CF 105017G - Game of Cards](https://codeforces.com/problemset/problem/105017/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** no  

## Solution
## Problem Understanding

Two players start with two equal-sized collections of numbers. These numbers are not directly compared; instead, they are gradually “decomposed” during a game. On each turn, the current player chooses a prime number not exceeding a fixed limit L, then forces the opponent to take one of their numbers that is divisible by that prime and divide it by that prime. If the opponent has no number divisible by the chosen prime, the current player immediately wins.

The crucial detail is that every move removes exactly one occurrence of a prime factor (not necessarily the entire factorization, just one copy of the chosen prime from some number on the opponent’s side). The players alternate turns, starting with Rami, and both play perfectly.

The input describes two multisets of integers, one for each player. The task is to determine which player eventually wins under optimal play.

The constraints allow up to 100000 numbers, each up to 1e6. This rules out any approach that repeatedly factorizes numbers naively in O(sqrt(x)) per value without preprocessing, since that would lead to roughly 10^10 operations in the worst case. Instead, each number must be factorized efficiently, ideally in logarithmic or near-constant amortized time using a sieve-based method.

A subtle point is that the game is not about which prime is chosen, because once a prime is chosen, the only requirement is that the opponent has at least one occurrence of it. The identity of the chosen prime only determines which token is consumed, not the structure of the game tree.

Another edge case arises when both players have exactly the same total “removable prime content”. In that case, the alternation of turns means the second player, Yessine, gets the final move and forces a win.

## Approaches

At first glance, one might try to simulate the game. Each turn would require checking all primes up to L and finding a divisible card, then updating it. Even if we maintain factor counts per card, the branching factor of choosing primes makes simulation unnecessary, because the choice does not affect the future structure beyond consuming one unit of progress from the opponent.

The key observation is that each number contributes independently to a total number of “available moves” for its owner’s opponent. Every time a number contains a prime factor p ≤ L, that factor represents one unit that can be consumed during the game. No matter how the prime is chosen, consuming p simply reduces the exponent of p in some number by one.

This reduces the entire game to a simple counting process. Each player has a total number of removable prime factors in their multiset. Let R be the total number of such factors in Rami’s numbers, and Y be the total in Yessine’s numbers. Every move removes exactly one unit from the opponent’s total. Rami removes from Y, Yessine removes from R.

The game alternates until one side cannot move. This becomes a simple alternating depletion process, and the winner depends only on which side runs out of removable units first. Since Rami starts, he wins exactly when Y is strictly greater than R; otherwise Yessine survives at least as long and wins.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulate moves with factor updates | O(N √A) or worse | O(N) | Too slow |
| Sieve factor counting + greedy reduction model | O(N log A) | O(A max) | Accepted |

## Algorithm Walkthrough

We convert each number into its prime factorization and only keep primes up to L.

1. Build a smallest-prime-factor sieve up to 1e6. This allows us to factor any number in logarithmic time by repeatedly dividing by its smallest prime factor.
2. Initialize two counters, R and Y, representing how many removable prime occurrences exist in Rami’s and Yessine’s arrays respectively.
3. For every number in Rami’s list, repeatedly extract its prime factors using the sieve. For each prime factor p, if p ≤ L, increase R by 1.
4. Repeat the same process for Yessine’s list, accum
