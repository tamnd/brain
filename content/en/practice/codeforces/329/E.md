---
title: "CF 329E - Evil"
description: "We are given a set of $n$ cities, each represented as a point on a 2D Cartesian plane. The distance between any two cities is measured using the Manhattan metric, which is the sum of the absolute differences of their coordinates."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 329
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 192 (Div. 1)"
rating: 3100
weight: 329
solve_time_s: 54
verified: false
draft: false
---

[CF 329E - Evil](https://codeforces.com/problemset/problem/329/E)

**Rating:** 3100  
**Tags:** math  
**Solve time:** 54s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of $n$ cities, each represented as a point on a 2D Cartesian plane. The distance between any two cities is measured using the Manhattan metric, which is the sum of the absolute differences of their coordinates. The goal is to construct a Hamiltonian cycle that visits every city exactly once and returns to the starting city, such that the total sum of Manhattan distances along the cycle is maximized. We are asked only for the maximum possible cycle length, not the cycle itself.

The input gives the number of cities followed by their coordinates. The constraints allow $n$ up to $10^5$ and coordinates up to $10^9$. Because $n$ is so large, any solution that explicitly enumerates all permutations of cities is infeasible. Brute-force enumeration would require $O(n!)$ operations, which is astronomically slow even for $n = 20$. This forces us to search for a solution that works in linear or linearithmic time.

Non-obvious edge cases include cities forming a perfect square or line. For instance, four cities forming a square at $(1,1), (1,2), (2,1), (2,2)$ yield a maximum Hamiltonian cycle of length 6. A naive greedy approach that just picks the farthest next city at each step may fail to achieve the global maximum, because the Manhattan metric can be decomposed into linear components along transformed axes.

## Approaches

A brute-force approach would compute all permutations of the cities, calculate the total Manhattan distance for each permutation, and select the maximum. The complexity of this method is $O(n! \cdot n)$ for calculating distances, which is completely infeasible for $n$ up to $10^5$. Even dynamic programming solutions for the Traveling Salesman Problem with $O(n \cdot 2^n)$ complexity are too slow here.

The key insight comes from the structure of Manhattan distance: $|x_i - x_j| + |y_i - y_j|$ can be rewritten using the four combinations of sums and differences: $x+y$, $x-y$, $-x+y$, $-x-y$. The longest cycle occurs when we connect points that are extremal in these transformed coordinates. In essence, for each of the four transformations, the maximum Manhattan distance between two cities is the difference between the largest and smallest transformed values. The Hamiltonian cycle can then be constructed conceptually by taking a path that alternates between these extremal points along these directions. This reduces the problem to finding maxima and minima in four linear sequences, giving an $O(n)$ solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * n) | O(n) | Too slo* |
