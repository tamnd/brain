---
title: "CF 103466I - Space Station"
description: "We are given a collection of space stations indexed from 0 to n. Each station has an integer energy value, and station 0 is our starting point."
date: "2026-07-03T06:49:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103466
codeforces_index: "I"
codeforces_contest_name: "The 2019 ICPC Asia Nanjing Regional Contest"
rating: 0
weight: 103466
solve_time_s: 19
verified: false
draft: false
---

[CF 103466I - Space Station](https://codeforces.com/problemset/problem/103466/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 19s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of space stations indexed from 0 to n. Each station has an integer energy value, and station 0 is our starting point. At the beginning, we already possess energy equal to the value of station 0, and whenever we visit a station we permanently gain its energy.

Movement is constrained: we are only allowed to move from our current position to a station whose energy is not larger than the energy we currently hold. Since energy only increases as we visit stations, this means that any move must respect a dynamic threshold that never decreases over time.

The task is to count how many distinct orders of visiting all stations exactly once are possible under this rule, starting from station 0. The answer is required modulo 1e9 + 7.

The key structural constraint is that n can be as large as 100000, while energies are very small integers bounded by 0 to 50. This mismatch immediately signals that the solution cannot depend on the number of stations directly in a quadratic or cubic way, but must instead compress states using the small value range of energies.

A naive approach that tries to simulate all possible permutations would clearly fail because even n = 20 already produces 20! possibilities, which is infeasible. Even a DP over subsets would explode beyond 2^n.

A subtle edge case appears when many stations share the same energy value. For example, if all stations have equal energy, then every permutation is valid since the constraint never blocks movement. The answer in that case should be (n+1)! modulo M. Any approach that incorrectly treats equal-energy transitions as restricted will undercount heavily.

Another corner case is when station 0 has the maximum energy. Then all other stations must have energy ≤ a0, so again any ordering is valid. This tests whether the algorithm correctly handles the fact that the initial threshold already includes all eligible n
