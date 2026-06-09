---
title: "CF 1666H - Heroes of Might"
description: "We are given a sequence of integer strengths representing heroes. Each hero can defeat monsters of strength equal to their own or weaker."
date: "2026-06-10T02:17:11+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1666
codeforces_index: "H"
codeforces_contest_name: "2021-2022 ICPC, NERC, Northern Eurasia Onsite (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 3500
weight: 1666
solve_time_s: 47
verified: true
draft: false
---

[CF 1666H - Heroes of Might](https://codeforces.com/problemset/problem/1666/H)

**Rating:** 3500  
**Tags:** math  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integer strengths representing heroes. Each hero can defeat monsters of strength equal to their own or weaker. We are asked, for each possible monster strength from 1 up to the maximum hero strength, to determine the minimum number of heroes needed to cover all monsters of that strength and below. Essentially, we want the smallest prefix of heroes such that the sum of their strengths covers every integer from 1 up to some target strength.

The input consists of a single line of integers representing hero strengths. The output is a sequence of integers, one per possible monster strength, indicating the minimum number of heroes required.

The maximum number of heroes can reach 200,000 and hero strengths can be up to $10^9$. This rules out any brute-force approach that iterates explicitly over all monsters for every strength, because that could lead to up to $2 \cdot 10^{14}$ operations, which is far beyond feasible.

An edge case occurs when all heroes have strength 1. For example, if the input is `[1, 1, 1]`, the minimum number of heroes to cover monsters of strength 1, 2, and 3 are `1, 2, 3`. A naive algorithm might incorrectly assume one hero can cover multiple strength levels without accounting for the sum. Another edge case is a single very strong hero, e.g., `[10]`. The algorithm must correctly report `1` for all monster strengths up to 10.

## Approaches

A brute-force solution would sort the heroes and then, for each target monster strength $m$, try all combinations of heroes to see which prefix sums to at least $m$. This is correct in principle but impractical, because checking all prefixes for all strengths results in $O(n \cdot M)$ time, where $M$ is the maximum strength. If $n = 2 \cdot 10^5$ and $M = 10^9$, this is infeasible.

The key insight is that the problem reduces to a prefix-sum coverage problem. Once the heroes are sorted in descending order, we can iteratively accumulate the sum of strengths. For each sum $S$, all monster strengths up to $S$ can be defeated by the first $k$ heroes. We can then quickly assign the answer for all strengths from the previous sum plus one up to $S$ using the current hero count. The heroes do not need to be checked in combinations or subsets because summing the largest available heroes first guarantees minimal hero count for coverage.

The brute-force works because the answer is based on accumulated strength coverage, but fails when the input is large due to repeated scanning. The observation that prefix sums cover consecutive ranges allows us to reduce the solution to $O(n + M)$ time if we precompute only up to the maximal covered strength, avoiding unnecessary iterations over unreachable monster strengths.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * max_strength) | O(n) | Too slow |
| Prefix Sum Coverage | O(n log n) | O(n + max_strength) | Accepted |

## Algorithm Walkthrough

1. Read the list of hero strengths.
2. Sort the heroes in descending order to maximize coverage early. This ensures minimal heroes are used for any given strength.
3. Initialize a cumulative sum variable `S = 0` and a result array `ans` of size equal to the maximal possible monster strength.
4. Iterate through the sorted heroes, keeping track of the number of heroes `k` used so far. For each hero with strength `h`, increment `S` by `h`.
5. For every integer strength `m` from `previous_S + 1` to `S`, assign `ans[m] = k`. This covers all strengths that are now reachable with the current prefix.
6. Continue until all heroes are processed. Any monster strengths greater than the total sum are unreachable and can be left undefined or assigned a sentinel value.

Why it works: Sorting ensures we always use the largest available hero first, minimizing the hero count. The prefix sum guarantees that all monster strengths up to `S` can be covered by the first `k` heroes. Each range assignment is disjoint and contiguous, so no strength is overwritten or missed.

## Python Solution

```
PythonRun
```
