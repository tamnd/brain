---
title: "CF 1165B - Polycarp Training"
description: "We are given a list of contests, each with a certain number of problems. Polycarp trains day by day, and on day $k$, he must pick exactly one unused contest and solve exactly $k$ problems from it."
date: "2026-06-13T08:42:45+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1165
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 560 (Div. 3)"
rating: 1000
weight: 1165
solve_time_s: 85
verified: false
draft: false
---

[CF 1165B - Polycarp Training](https://codeforces.com/problemset/problem/1165/B)

**Rating:** 1000  
**Tags:** data structures, greedy, sortings  
**Solve time:** 1m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a list of contests, each with a certain number of problems. Polycarp trains day by day, and on day $k$, he must pick exactly one unused contest and solve exactly $k$ problems from it. A contest can be partially used: if it has more problems than needed, the rest are discarded. If it has fewer than $k$ problems, it cannot be used for that day.

The process is sequential in days. On each day, we either assign a previously unused contest that is large enough, or we stop if no such contest exists. Each contest can be used at most once, so the ordering of assignments matters.

The goal is to maximize how many consecutive days he can complete this process.

The constraints allow up to $2 \cdot 10^5$ contests. A solution that is quadratic in the number of contests would be too slow since it could require on the order of $10^{10}$ operations. This immediately suggests we need at most $O(n \log n)$ or $O(n)$ behavior, likely involving sorting and a greedy selection strategy.

A subtle failure case appears when large contests are used too early. For example, if we consume a large contest on a small day, we might block a future day that requires an even larger threshold, while a smaller contest would have been sufficient earlier. Conversely, skipping small contests early can also reduce flexibility later. This indicates we must carefully match small day requirements with just-enough large contests.

## Approaches

A direct simulation tries to assign a contest to each day $k = 1, 2, 3, \dots$. For each day, we scan all remaining contests and pick any one with size at least $k$. This is correct because it directly follows the rules. However, each day requires scanning up to $O(n)$ contests, and we may have $O(n)$ days, leading to $O(n^2)$ operations, which is too slow for $2 \cdot 10^5$.

The key observation is that we never need to consider contests in their original order. Only their sizes matter. Once sorted, we can reason about feasibility in a greedy way: if we are at day $k$, we only care whether there exists any unused contest with size at least $k$. Since we want to maximize the number of days, we try to satisfy small requirements using small contests first, preserving larger ones for later days.

This leads to a greedy matching strategy. We sort contest sizes in increasing order and maintain a pointer to the smallest unused contest that can satisfy the current day. We advance through the sorted array, and whenever a contest size is at least the current day requirement, we use it and move to the next day. Otherwise, we skip it because it is too small and can never be useful for future larger days either.

This works because each day’s requirement is strictly increasing, so a contest that is too small now will never become useful later.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(n^2)$ | $O(1)$ or $O(n)$ | Too slow |
| Greedy + Sorting | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Sort all contest sizes in non-decreasing order. Sorting is necessary because we want to process smaller contests first and avoid wasting large ones early.
2. Initialize a pointer `i = 0` that tracks the current smallest unused contest, and a variable `day = 1` representing the current training day requirement.
3. While `i < n`, check whether the current contest `a[i]` can support the current day, meaning `a[i] >= day`.
4. If `a[i] < day`, this contest is too small even for the current requirement, so we discard it and increment `i`. This is safe because future days require even more problems, so this contest will never become useful.
5. If `a[i] >= day`, we assign this contest to day `day`, increment both `day` and `i`, since
