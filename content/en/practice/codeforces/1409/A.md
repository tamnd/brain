---
title: "CF 1409A - Yet Another Two Integers Problem"
description: "We are given two integers, and we want to transform the first into the second using a sequence of moves. Each move allows us to pick any integer step size from 1 to 10 and either add it to or subtract it from the current value."
date: "2026-06-11T07:33:39+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1409
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 667 (Div. 3)"
rating: 800
weight: 1409
solve_time_s: 90
verified: false
draft: false
---

[CF 1409A - Yet Another Two Integers Problem](https://codeforces.com/problemset/problem/1409/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 1m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two integers, and we want to transform the first into the second using a sequence of moves. Each move allows us to pick any integer step size from 1 to 10 and either add it to or subtract it from the current value.

The process is essentially a walk on the integer line. Starting at position `a`, we want to reach position `b`. Each step moves us left or right by a distance between 1 and 10 inclusive, and we want to minimize the number of such steps.

The key quantity is the absolute difference between the numbers. The direction does not matter, only how far apart they are.

The constraints are large enough that we cannot simulate every possible sequence of moves. With up to 2 × 10^4 test cases and values up to 10^9, any solution that explores states or tries greedy search over possibilities would be too slow. We need a constant-time computation per test case.

A subtle failure case for naive thinking is assuming we must always use large steps greedily without structure. For example, one might try repeatedly subtracting 10 until close to the target and then fix the remainder. This works but must be justified carefully because overshooting is allowed and can sometimes be beneficial.

A simpler misunderstanding is treating this like a restricted coin change problem with many states. That would introduce unnecessary complexity when the structure actually collapses to a simple division argument.

## Approaches

The brute-force interpretation is to view this as a shortest path problem on integers, where each node `x` connects to up to 20 neighbors: `x + k` and `x - k` for `k` from 1 to 10. A BFS from `a` to `b` would always find the minimum number of moves because each edge has equal weight. However, the range of values is up to 10^9, making the state space astronomically large. Even exploring a small fraction becomes infeasible because the graph is essentially infinite for practical purposes.

The
