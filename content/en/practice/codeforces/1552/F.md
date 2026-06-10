---
title: "CF 1552F - Telepanting"
description: "We have an ant moving on a number line. It starts at position 0 and moves to the right at a constant speed of 1 unit per second. Along its path, there are n portals. Each portal is at a position xi and can teleport the ant backward to a position yi (yi < xi)."
date: "2026-06-10T13:10:11+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1552
codeforces_index: "F"
codeforces_contest_name: "Codeforces Global Round 15"
rating: 2200
weight: 1552
solve_time_s: 38
verified: false
draft: false
---

[CF 1552F - Telepanting](https://codeforces.com/problemset/problem/1552/F)

**Rating:** 2200  
**Tags:** binary search, data structures, dp, sortings  
**Solve time:** 38s  
**Verified:** no  

## Solution
## Problem Understanding

We have an ant moving on a number line. It starts at position 0 and moves to the right at a constant speed of 1 unit per second. Along its path, there are `n` portals. Each portal is at a position `x_i` and can teleport the ant backward to a position `y_i` (`y_i < x_i`). Each portal also has an initial state `s_i`: if `s_i` is 1, the portal is active; if 0, it is inactive.

When the ant reaches a portal, one of two things happens. If the portal is inactive, it simply becomes active, and the ant continues moving normally. If the portal is active, the ant is teleported to `y_i`, and the portal flips to inactive. This backward teleporting can trigger further movement and further portals if the ant reaches them again.

We are asked to compute the total time it takes for the ant to reach `x_n + 1`, the position immediately after the last portal. The answer must be given modulo `998244353`.

The key constraints are `n ≤ 2×10^5` and `x_i, y_i ≤ 10^9`. This means any solution iterating over every position the ant passes is infeasible, since the total distance can be up to 10^9. We need a method that processes portals directly rather than simulating every step.

Non-obvious edge cases include situations where a portal teleports the ant past multiple earlier portals. For example, if `x_2 = 5, y_2 = 1`, and the ant reaches it with `s_2 = 1`, it jumps ba_
