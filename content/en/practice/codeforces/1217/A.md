---
title: "CF 1217A - Creating a Character"
description: "We are given a character with two base attributes: strength and intelligence. On top of that, we receive a fixed number of experience points that must all be distributed, where each point increases either strength or intelligence by exactly one."
date: "2026-06-13T17:42:07+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "math"]
categories: ["algorithms"]
codeforces_contest: 1217
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 72 (Rated for Div. 2)"
rating: 1300
weight: 1217
solve_time_s: 149
verified: false
draft: false
---

[CF 1217A - Creating a Character](https://codeforces.com/problemset/problem/1217/A)

**Rating:** 1300  
**Tags:** binary search, math  
**Solve time:** 2m 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a character with two base attributes: strength and intelligence. On top of that, we receive a fixed number of experience points that must all be distributed, where each point increases either strength or intelligence by exactly one.

For each test case, we are not asked to find a single optimal build. Instead, we must count how many distinct final configurations are possible after distributing all experience points, under a single constraint: final strength must be strictly greater than final intelligence.

A configuration is determined entirely by how many experience points go into strength versus intelligence. If we let x be the number of points added to strength, then exp - x goes to intelligence. This reduces the problem to counting valid integer values of x.

The key difficulty is that both attributes must be non-negative after allocation, and all exp points must be used, while also satisfying a strict inequality between the final values.

The constraints allow up to 100 queries, with values up to 10^8. This immediately rules out any quadratic or linear scan per query over all possible allocations. Any solution must be O(1) per test case.

A common mistake is to try iterating all splits of experience points and checking validity. That would require exp iterations per query, which is up to 10^8 and therefore impossible. Another subtle mistake is forgetting that the inequality depends on the final values after allocation, not the initial ones.

Edge cases appear when intelligence is already much larger than strength. In such cases, even giving all experience to strength may not be enough to satisfy strict inequality, resulting in zero valid builds.

Another edge case occurs when exp is zero. Then there is exactly one configuration, but it is valid only if initial strength is already strictly greater than intelligence.

## Approaches

A brute-force method considers every possible way to split exp into strength and intelligence increases. For each x from 0 to exp, we compute final strength as str + x and final intelligence as int + (exp - x), then check whether the inequality holds. This is correct because it enumerates all possible distributions. However, it requires exp + 1 checks per test case, which becomes infeasible when exp reaches 10^8.

The key observation is that the inequality can be transformed into a simple constraint on x. Writing it out:

str + x > int + (exp - x)

Rearranging gives:

2x > int + exp - str

This turns the problem into counting integers x in a range [0, exp] that satisfy a single linear inequality. Instead of iterating, we directly compute the smallest x that satisfies it, and then count how many integers remain up to exp.

This reduces each query to constant time arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(exp) | O(1) | Too |
