---
title: "CF 104752I - Inspecting the Scores"
description: "Each game consists of a fixed number of matches. In every match, exactly one of three things can happen: Franco solves it, Rafa solves it, or nobody solves it."
date: "2026-06-28T22:59:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104752
codeforces_index: "I"
codeforces_contest_name: "Concurso de programaci\u00f3n ANIEI 2023"
rating: 0
weight: 104752
solve_time_s: 29
verified: false
draft: false
---

[CF 104752I - Inspecting the Scores](https://codeforces.com/problemset/problem/104752/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 29s  
**Verified:** no  

## Solution
## Problem Understanding

Each game consists of a fixed number of matches. In every match, exactly one of three things can happen: Franco solves it, Rafa solves it, or nobody solves it. The score starts at 1, and every solved match multiplies the current score by a fixed factor, A if Franco solved that match and B if Rafa solved it. Unsolved matches do not change the score.

A “game outcome” is determined entirely by assigning each of the N matches to one of these three states. Two outcomes are different if at least one match has a different solver assignment. For each outcome, we compute the resulting final score by multiplying contributions along the sequence, then we sum these scores over all possible outcomes.

The task is to compute this total sum for many test cases.

The constraints are small per test case for N, since N is at most 1000, but the number of test cases is large up to 100000. This immediately suggests that each test must be solved in roughly O(N) or O(N log N) at worst, while any O(N^2) or exponential enumeration is impossible. The multiplicative structure also hints that answers for different N are independent and do not require interactions across test cases.

A naive interpretation would try to enumerate all 3^N assignments of matches. Even for N = 30 this becomes infeasible, since 3^30 is already far beyond any limit. Another common pitfall is to try to simulate each sequence directly and accumulate results without noticing the strong factorization structure, which leads to repeated recomputation.

A subtle edge case appears when A = B = 1. In that situation every solved configuration contributes a score of 1, and the answer is simply the total number of assignments, which is 3^N. Any solution that relies on modular inverses or geometric progression formulas must still handle this degenerate case correctly. Another edge case is N = 0, but here N starts from 1 so it does not occur.

## Approaches

A brute-force approach assigns each of the N matches one of three labels: 0 for unsolved, 1 for Franco, 2 for Rafa. For each assignment, we compute the product of A for every 1 and B for every 2. This is correct by definition, but it explores 3^N states. With N = 1000 this is completely infeasible, since even N = 20 already produces millions of states.

The key observation is that matches are independent in structure. Each match contributes multiplicatively, and choices at different positions do not interact except through multiplication. This means the global sum over all sequences can be factorized into a product of per-position contributions.

At a single match, we have exactly three choices: contribute 1 (unsolved), contribute A (Franco), or contribute B (Rafa). If we sum over all possibilities for that single position, its total contribution is 1 + A + B. Since positions are independent, the total sum over all sequences becomes (1 + A + B)^N.

Thus the problem reduces to fast exponentiation under a large modulus.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | O(3^N) | O(N) | Too slow |
| Factorization + Fast Power | O(log N) per test | O(1) | Accepted |

## Algorithm Walkthrough

We compute the answer for each test case independently using modular exponentiation.

1. Read N, A, B for a test case. These define the number of independent match positions and the three possible multiplicative effects per position.
2. Compute the base value S = 1 + A + B modulo 10^9+7. This represents the total contribution of a single match when summing over all three possibilities.
3. Compute S^N modulo 10^9+7 using binary exponentiation. This works because the effect of each match multiplies independently across positions.
4. Output the result.

Binary exponentiation repeatedly squares the base and reduces the exponent by half, ensuring logarithmic time complexity.

### Why it works

Each full game outcome is a length-N sequence where each position contributes independently to both the score and the count of configurations. The total sum over all outcomes i
