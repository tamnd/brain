---
title: "CF 104027B - Candies"
description: "We are given a collection of candy packs. Each pack contains either 2 candies or 3 candies. The task is to determine whether it is possible to distribute all candies among three people so that each person receives exactly the same total number of candies."
date: "2026-07-02T04:07:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104027
codeforces_index: "B"
codeforces_contest_name: "The 10-th BIT Campus Programming Contest for Junior Grade Group"
rating: 0
weight: 104027
solve_time_s: 30
verified: false
draft: false
---

[CF 104027B - Candies](https://codeforces.com/problemset/problem/104027/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of candy packs. Each pack contains either 2 candies or 3 candies. The task is to determine whether it is possible to distribute all candies among three people so that each person receives exactly the same total number of candies.

The input is effectively describing a multiset composed only of values 2 and 3. The output is a simple feasibility answer: whether there exists a way to partition all these packs into three groups such that the sum in each group is identical.

A first structural constraint comes from total sum. If the total number of candies is `S`, then a necessary condition is that `S` is divisible by 3. Otherwise, no equal partition exists regardless of arrangement.

A second constraint is combinatorial rather than arithmetic. Even if `S / 3` is an integer, we must ensure that the multiset of 2s and 3s can be split into three subsets each summing to `S / 3`. This is a constrained subset-sum partitioning problem with a very small alphabet of item weights.

A subtle edge case appears when greedy reasoning on counts of 2s and 3s is used without considering cross-group interactions. For example, consider packs `[3, 3, 2, 2, 2]`. Total sum is `12`, so each person must get `4`. A naive attempt might try to group `(3+1)` which is impossible, or treat 2s and 3s independently, failing to notice that valid partitions require mixing both types.

Another edge case is when total sum is divisible by 3, but no partition exists due to indivisibility constraints. For example, `[3, 3, 3, 2]` has sum `11`, already failing divisibility, but even variants like `[3, 3, 2, 2]` require careful assignment reasoning.

The key difficulty is not the arithmetic target, but whether the discrete building blocks 2 and 3 can be arranged into three equal sums simultaneously.

## Approaches

The most direct approach is to treat this as a partitioning problem. Since each person must receive exactly `S / 3` candies, we can think in terms of assigning each pack to one of three bins and checking whether any assignment works.

A brute-force idea is to enumerate all ways to assign each pack to one of three people. With `n` packs, this leads to `3^n` possibilities, which is far too large.

A slightly more structured brute force observes that the total sum per person is fixed, so we only need to consider subset combinations. One can enumerate all subsets of packs that sum to `S / 3`. Suppose there are `L` such subsets. Then we try all triples of subsets to see if they form a partition. This leads to `O(L^3)` checks. In worst cases, `L` itself can be exponential, since subset sum over even small weights produces many combinations.

The key observation is that we do not actually need to reason about individual assignments at the level of arbitrary subsets. Since all weights are only 2 or 3, the structure is highly constrained. Any valid solution is equivalent to grouping some packs of 3 together and some packs of 2 together, with occasional mixing, but mixing can be normalized.

A cleaner way to see it is to fix a person’s share `T = S / 3`. We only need to decide how many 3-packs and 2-packs go into each person. Let `x` be the number of 2-packs assigned and `y` be the number of 3-packs assigned. Then each person must satisfy `2x + 3y = T`.

So the problem becomes: can we split all 2-packs and 3-packs into three groups, each respecting the same linear equation? This reduces the global partitioning problem into checking whether the counts of 2s and 3s can be decomposed consistently across three identical linear representations.

Instead of searching over assignments, we enumerate all valid `(x, y)` solutions for one person, then check whether three such solutions can collectively consume all items. This reduces the state space dramatically because the equation `2x + 3y = T` has only `O(T)` solutions, and in practice very few since `x` is bounded and parity restricts feasibility.

We then check all triples of these candidate solutions to see if they exactly cover the available number of 2s and 3s.

This turns a combinatorial partition problem into a bounded enumeration over feasible linear decompositions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Subsets | Exponential | Exponential | Too slow |
| Enumerate (x, y) triples | O(L³), L small from constraints | O(L) | Accepted |

## Algorithm Walkthrough

1. Compute total sum `S` of all candies. If `S % 3 != 0`, stop immediately because equal partition is impossible.
2. Set target per person `T = S / 3`. This is the fixed sum each of the three groups must achieve.
3. Let `c2` be the number of 2-packs and `c3` be the number of 3-packs. We now describe one person’s selection as choosing `x` twos and `y` threes such that `2x + 3y = T`.
4. Enumerate all pairs `(x, y)` satisfying the equation and feasibility constraints `0 <= x <= c2` and `0 <= y <= c3`. Each pair represents a possible way one person could be formed.
5. Store all valid `(x, y)` pairs in a list. Each candidate represents a decomposition of one third of the final partition.
6. Try all triples of candidates `(i, j, k)` from this list. For each triple, check whether:

`x_i + x_j + x_k = c2` and `y_i + y_j + y_k = c3`.

This ensures that all 2-packs and 3-packs are used exactly once across the three people.
7. If any triple satisfies both equations, return “YES”. Otherwise return “NO”.

### Why it works

Any valid partition induces a choice of how many 2-packs and 3-packs each person receives, so it corresponds to three pairs `(x, y)` sat
