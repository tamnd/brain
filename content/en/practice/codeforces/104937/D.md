---
title: "CF 104937D - K-Good Subsequences"
description: "We are given an initial sequence a that must appear as a prefix of a longer sequence b. The values in b are integers between 1 and M. After this prefix, we are allowed to append more elements freely."
date: "2026-06-28T18:15:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104937
codeforces_index: "D"
codeforces_contest_name: "MITIT 2024 Advanced Round"
rating: 0
weight: 104937
solve_time_s: 37
verified: false
draft: false
---

[CF 104937D - K-Good Subsequences](https://codeforces.com/problemset/problem/104937/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an initial sequence `a` that must appear as a prefix of a longer sequence `b`. The values in `b` are integers between `1` and `M`. After this prefix, we are allowed to append more elements freely.

A sequence is called “K-good” if every pair of consecutive elements differs by at most `K`. We are not looking at all subsequences of `b`, only those subsequences whose adjacent differences also satisfy this constraint.

The restriction is global and adversarial: in the final sequence `b`, every K-good subsequence must have length at most `L`. In other words, it must be impossible to extract a long K-good subsequence, even if we skip elements.

The task is to extend `a` into a longer sequence `b` of maximum possible length while never allowing any K-good subsequence to exceed length `L`.

The main difficulty is that subsequences can skip arbitrarily many elements. So even if we separate values far apart in `b`, a subsequence can still pick a “path” through them as long as each step changes by at most `K`.

The constraints imply that a solution must be close to linear per test case. With up to `2⋅10^5` tests and total `N ≤ 4⋅10^5`, any quadratic or even `O(N√N)` construction per test is impossible. We need a greedy or structural characterization of how K-good subsequences behave.

A subtle edge case appears when the prefix already saturates the limit:

For example, if `a = [1, 2, 3]`, `K = 1`, `L = 3`, then any extension that allows a continuation like `4, 5` might still be unsafe because subsequences can skip and form long chains. A naive approach that only checks adjacent differences in `b` fails completely because the constraint is about subsequences, not the sequence itself.

Another edge case is when `K = 0`. Then any K-good subsequence can only consist of equal values, so the constraint becomes about limiting frequency per value. Many greedy solutions break here if they assume connectivity between values.

## Approaches

The key difficulty is understanding what a K-good subsequence really encodes. It is not arbitrary structure; it is a walk on the integer line where each step moves by at most `K`. This means a subsequence corresponds to a chain where consecutive chosen values lie within distance `K`.

If we think of values as nodes on a line, every value connects to all values in `[x-K, x+K]`. A K-good subsequence is exactly a path in this implicit graph. The constraint says that no path can be longer than `L`.

A brute-force interpretation would try to si
