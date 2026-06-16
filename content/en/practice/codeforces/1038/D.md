---
title: "CF 1038D - Slime"
description: "We are given a line of slimes, each carrying an integer value, and we repeatedly perform an operation where one slime absorbs an adjacent slime. If a slime with value $x$ eats a neighbor with value $y$, that neighbor disappears and the eater’s value becomes $x - y$."
date: "2026-06-16T18:30:25+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1038
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 508 (Div. 2)"
rating: 1800
weight: 1038
solve_time_s: 107
verified: false
draft: false
---

[CF 1038D - Slime](https://codeforces.com/problemset/problem/1038/D)

**Rating:** 1800  
**Tags:** dp, greedy, implementation  
**Solve time:** 1m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a line of slimes, each carrying an integer value, and we repeatedly perform an operation where one slime absorbs an adjacent slime. If a slime with value $x$ eats a neighbor with value $y$, that neighbor disappears and the eater’s value becomes $x - y$. This operation can be applied repeatedly until only a single slime remains.

The order of these absorptions is completely flexible as long as we always choose adjacent slimes. Different orders lead to different final values, because subtraction depends on which values end up being subtracted from which accumulators.

The task is to choose an order of merges that maximizes the final remaining value.

The constraint $n \le 5 \cdot 10^5$ immediately rules out any approach that simulates all possible merge sequences or even dynamic programming over all subsegments. Any quadratic or cubic behavior is too large; even $O(n \log n)$ is acceptable, while anything linear or linear-logarithmic is required.

A subtle difficulty comes from the fact that values can be negative. This makes greedy intuition like “always eat the largest neighbor” unreliable. For example, if a slime eats a negative value, it increases, while eating a positive value decreases it. This sign interaction is the core source of non-triviality.

A naive mistake is to assume that the best strategy is always to accumulate everything into the first or last element. That fails because intermediate merge orders can flip signs of contributions.

Another common incorrect idea is to think the answer is simply the alternating sum or something based on parity. That ignores that we control the order of subtractions, not just a fixed expression.

## Approaches

A brute-force approach would try every possible sequence of adjacent merges. Each state consists of a current array, and each move reduces its length by one. The number of possible binary merge trees over $n$ elements is Catalan in nature, roughly exponential in $n$. Even for $n = 30$, this becomes infeasible. Each transition also requires copying or updating a list, making the runtime explode far beyond limits.

The key observation is that each element is eventually either subtracted an even or odd number of times from some final accumulator depending on the merge structure. Instead of thinking in terms of sequences of operations, we can reinterpret the process as building an expression over the original array where each value appears with a coefficient of either $+1$ or $-1$, determined by how merges are arranged.

A more structured way to see it is that every final configuration corresponds to choosing a direction of “propagation” of influence, and optimal play always reduces to combining contributions in a way that maximizes the net result. The crucial simplification is that the optimal answer depends only on global extrema and parity structure: we can avoid simulating merges entirely and compute the best achievable result using a greedy sweep that tracks how far we can extend an accumulating segment and how signs flip when we absorb elements.

This reduces the problem from exponential state space exploration to a linear traversal with a constant amount of state.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

The core idea is to process the array while maintaining the best achievable value of a growing final slime, considering that each absorption either adds or subtracts future contributions depending on how we interpret the merge direction.

We observe that the final result can be viewed as repeatedly extending a segment and deciding whether a new element contributes positively or negatively to the current accumulator, but the optimal structure always reduces to a greedy choice of pairing smaller segments first and preserving high-impact elements.

The correct simplification for this problem is that the optimal answer is obtained by taking the maximum of two structured
