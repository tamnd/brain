---
title: "CF 1717D - Madoka and The Corruption Scheme"
description: "We are asked to determine the smallest possible number of a winner in a single-elimination tournament with $2^n$ players. Each round halves the number of participants, and Madoka can choose both the initial pairing of players and the winner of each match."
date: "2026-06-09T19:47:31+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1717
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 818 (Div. 2)"
rating: 1900
weight: 1717
solve_time_s: 62
verified: false
draft: false
---

[CF 1717D - Madoka and The Corruption Scheme](https://codeforces.com/problemset/problem/1717/D)

**Rating:** 1900  
**Tags:** combinatorics, constructive algorithms, greedy, math  
**Solve time:** 1m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to determine the smallest possible number of a winner in a single-elimination tournament with $2^n$ players. Each round halves the number of participants, and Madoka can choose both the initial pairing of players and the winner of each match. However, sponsors can reverse the outcome of up to $k$ matches anywhere in the tournament. Our goal is to compute the smallest number that Madoka can guarantee will win regardless of the sponsors' actions.

The inputs are $n$, the number of rounds, and $k$, the maximum number of matches whose outcomes can be changed. The output is the minimum winning player number modulo $10^9 + 7$.

The constraints indicate $n$ can be as large as $10^5$, which means $2^n$ participants is astronomically large. Clearly, any algorithm that simulates matches individually is impossible. We must rely on combinatorial reasoning and properties of powers of two to solve the problem efficiently. Also, $k$ can be very large, up to $10^9$, so we cannot iterate over all possible sponsor changes.

A subtle edge case arises when $k$ is at least the total number of matches in the tournament, $2^n - 1$. In that case, the sponsors can overturn all matches leading to the smallest player losing immediately, so the guaranteed winner must be the second smallest, or more generally the first player who cannot be completely blocked by sponsor changes.

Another edge case is the smallest tournament, $n = 1$. With $k = 1$, the sponsors can flip the only match, forcing the winner to be player 2 instead of 1. A naive approach that ignores sponsor interference would incorrectly output 1.

## Approaches

The brute-force approach would try to simulate every possible initial bracket arrangement and all $2^{2^n-1}$ combinations of match outcomes and sponsor flips. This would involve iterating over an astronomical number of possibilities. Even for $n = 20$, $2^n$ exceeds one million, making this approach completely infeasible.

The key insight comes from observing the structure of a perfect binary tournament. Each player's path to victory is determined by the number of matches they must win. Sponsor changes can block a player only by flipping matches on their path. If we imagine the tournament as a complete binary tree with players as leaves, the maximum number of matches that can be flipped in a path from a leaf to the root is $n$. For a player to be guaranteed to win, the number of possible flips that could affect them must be smaller than the number of matches they need to win to reach the root. This reduces the problem to a combinatorial one: we can compute the smallest player number $x$ such that no more than $k$ paths can prevent them from winning, which can be expressed in terms of powers of two.

Concretely, the problem reduces to computing $\min(2^n, k+1)$. Player 1 can be forced to lose if $k \ge 1$, but the first $k+1$ players include at least one who cannot be blocked by all sponsor changes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(2^n)) | O(2^n) | Infeasible |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute $2^n$ directly. This is the total number of participants.
2. Compare $2^n$ with $k + 1$. The reasoning is that if the sponsors can flip $k$ matches, the first $k$ players could potentially lose. Therefore, the earliest player guaranteed to win is $k + 1$, or 1 if $k = 0$.
3. Take the minimum of $2^n$ and $k + 1$. This handles the case when $k$ exceeds the number of players minus one.
4. Output the result modulo $10^9 + 7$.

Why it works: Each match flip can eliminate one player from the tournament pat
