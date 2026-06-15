---
title: "CF 1297F - Movie Fan"
description: "We are given several movies, each movie has a time window during which it can be watched in the cinema. If a movie is watched inside its window, it is considered “on time”."
date: "2026-06-16T05:02:32+07:00"
tags: ["codeforces", "competitive-programming", "*special", "data-structures", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1297
codeforces_index: "F"
codeforces_contest_name: "Kotlin Heroes: Episode 3"
rating: 0
weight: 1297
solve_time_s: 138
verified: false
draft: false
---

[CF 1297F - Movie Fan](https://codeforces.com/problemset/problem/1297/F)

**Rating:** -  
**Tags:** *special, data structures, greedy, implementation, sortings  
**Solve time:** 2m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several movies, each movie has a time window during which it can be watched in the cinema. If a movie is watched inside its window, it is considered “on time”. If it is watched after its window ends, it becomes an online watch and incurs a penalty equal to how late it is.

Each day Polycarp can watch at most $m$ movies. The task is to assign every movie to a day so that no day exceeds this capacity, and each movie gets exactly one watching day. The assigned day can be anywhere in time, but watching inside $[a_i, b_i]$ is free of penalty, while watching after $b_i$ adds a delay cost of $t_i - b_i$.

If it is possible to schedule all movies within their windows, the answer should reflect that. Otherwise, we must still produce a full schedule, but among all valid schedules we want to minimize the worst lateness across all movies that are forced to be watched after their ending day.

The constraints force us away from any simulation over actual calendar days. The days can go up to $10^9$, so iterating day by day is impossible. What matters is only the order of deadlines and arrivals, not the absolute values.

A naive approach would try to simulate each day and assign up to $m$ movies greedily. This immediately breaks when gaps between important days are large. For example, if one movie starts at day $1$ and another at day $10^9$, simulating all intermediate days is impossible.

A second subtle issue appears when many movies share the same tight deadline. If we do not prioritize correctly, we might fill early capacity with movies that have loose deadlines and later fail on urgent ones. This leads to hidden infeasibility even when a valid schedule exists.

## Approaches

A brute-force strategy would simulate day by day. For each day, we collect all movies that have started but not yet been assigned, and then assign up to $m$ of them. We would choose arbitrarily or perhaps by earliest deadline. This is correct in spirit because it respects capacity and window constraints.

The failure point is complexity. Days range up to (
