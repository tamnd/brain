---
title: "CF 1772G - Gaining Rating"
description: "Monocarp wants to increase his chess rating from x to y by playing a set of n opponents with fixed ratings. Each game affects only Monocarp's rating: if his current rating is at least the opponent's, he wins and gains 1; otherwise, he loses and drops 1."
date: "2026-06-09T12:20:32+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "implementation", "math", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1772
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 839 (Div. 3)"
rating: 2200
weight: 1772
solve_time_s: 41
verified: false
draft: false
---

[CF 1772G - Gaining Rating](https://codeforces.com/problemset/problem/1772/G)

**Rating:** 2200  
**Tags:** binary search, greedy, implementation, math, sortings, two pointers  
**Solve time:** 41s  
**Verified:** no  

## Solution
## Problem Understanding

Monocarp wants to increase his chess rating from `x` to `y` by playing a set of `n` opponents with fixed ratings. Each game affects only Monocarp's rating: if his current rating is at least the opponent's, he wins and gains 1; otherwise, he loses and drops 1. The twist is that he must play opponents evenly: he cannot play one opponent more times than another until all have been played equally.

The input gives the number of test cases, and for each test case the number of opponents, Monocarp’s initial and target ratings, and the list of opponents' ratings. The output should be the minimum number of games needed to reach the target rating, or `-1` if it is impossible.

The constraints are significant: `n` can reach `2·10^5` and the sum over all test cases is also bounded by `2·10^5`. Ratings themselves can go up to `10^12`, which prevents solutions that iterate rating by rating. We must avoid brute-force simulations that consider every game individually.

Edge cases arise when all opponents are stronger than Monocarp initially. For example, `x=1`, `y=3`, and opponents `[2,3]` is impossible, because any game would cause him to lose, moving him further from `y`. Another subtle case is when there is only one opponent; then the "even-play" constraint is trivial but still must be respected.

## Approaches

The naive approach is to simulate Monocarp’s games round by round, selecting opponents in a cyclic fashion to satisfy the even-play constraint. After each game, update the rating depending on win/loss. Stop when reaching `y` or declare impossible if the rating drops below the smallest opponent in a cycle. This is correct but far too slow, because reaching `y` could take up to `y - x` games, which can be `10^12` in the worst case.

The key observation is that the outcome of a round-robin cycle of `n` games depends only on the number of opponents Monocarp can beat at his current rating. Suppose he plays one game against each opponent in a cycle. Let `w` be the number of opponents he can beat. Then his net gain after one full cycle is `2·w - n`. If `2·w - n` is non-positive, Monocarp cannot make progress unless he beats everyone eventually. Otherwise, the number of cycles needed to reach `y` is simply the ceiling of `(y-x)/net_gain_per_cycle`.

Sorting the opponent ratings lets us quickly determine `w` for any current rating. If at any point Monocarp’s rating is less than all opponent ratings, the problem is impossible. The process reduces the problem to iteratively finding the maximum opponents Monocarp can beat, computing net gains, and calculating the number of full cycles needed, with at most one partial cycle at the end.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O((y-x)·n) | O(n) | Too slow, fails for large `y-x` |
| Cycle-based Greedy | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the opponents’ ratings. This allows us to efficiently determine how many opponents Monocarp can beat at any rating.
2. If Monocarp's current rating `x` is already greater than or equal to all opponents, he can win every game. The number of games is simply `y - x`.
3. Otherwise, iterate while `x < y`. In each step, count the number `w` of opponents with ratings less than or equal to `x`. This is the number of opponents Monocarp can beat in a cycle.
4. If `w == 0`, Monocarp cannot win any game this round, and the minimum rating he can reach will decrease due to the even-play constraint. In this case, reaching `y` is impossible, return `-1`.
5. Calculate the net gain in rating per complete cycle of `n` games as `gain = 2*w - n`. This comes from winning `w` games (+1 each) and losing `n - w` games (-1 each).
6. If `gain <= 0` and `x < max(a_i)`, Monocarp cannot progress, return `-1`. Otherwise, calculate the number of cycles needed to reach `y`: `cycles_needed = ceil((y-x)/gain)`. Update `x` and the total games played accordingly: `games_played += cycles_needed * n`.
7. If `x` overshoots `y`, subtract extra games corresponding to the l
