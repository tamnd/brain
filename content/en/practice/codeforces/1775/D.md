---
title: "CF 1775D - Friendly Spiders"
description: "We are given a colony of spiders on Mars, each identified by the number of legs it has. Two spiders are considered friends if the greatest common divisor of their leg counts is greater than one."
date: "2026-06-09T11:53:38+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs", "math", "number-theory", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 1775
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 843 (Div. 2)"
rating: 1800
weight: 1775
solve_time_s: 27
verified: false
draft: false
---

[CF 1775D - Friendly Spiders](https://codeforces.com/problemset/problem/1775/D)

**Rating:** 1800  
**Tags:** dfs and similar, graphs, math, number theory, shortest paths  
**Solve time:** 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a colony of spiders on Mars, each identified by the number of legs it has. Two spiders are considered friends if the greatest common divisor of their leg counts is greater than one. Friendship allows instant message passing; otherwise, messages must hop from one spider to another along a chain of friends. The task is to compute the shortest path in terms of message transmissions from one specific spider to another, and also to provide one valid sequence of spiders along that path.

The input provides up to 300,000 spiders, each with a leg count up to 300,000. The source and target spiders are identified by 1-based indices. With these input sizes and a 2-second limit, we cannot afford an algorithm that checks all pairwise friendships directly because that would require up to 9·10^10 gcd computations, which is infeasible. Therefore, the solution must exploit number-theoretic structure rather than naive pairwise checks.

One non-obvious edge case arises when a spider’s leg count is prime and shares no common factors with any oth
