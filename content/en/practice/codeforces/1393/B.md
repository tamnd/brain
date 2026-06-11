---
title: "CF 1393B - Applejack and Storages"
description: "Applejack wants to build two storages using planks from a storehouse: one square and one rectangle. Each side of a storage uses exactly one plank, so a square requires four planks of the same length and a rectangle requires two pairs of equal-length planks."
date: "2026-06-11T09:58:05+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1393
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 662 (Div. 2)"
rating: 1400
weight: 1393
solve_time_s: 314
verified: false
draft: false
---

[CF 1393B - Applejack and Storages](https://codeforces.com/problemset/problem/1393/B)

**Rating:** 1400  
**Tags:** constructive algorithms, data structures, greedy, implementation  
**Solve time:** 5m 14s  
**Verified:** no  

## Solution
## Problem Understanding

Applejack wants to build two storages using planks from a storehouse: one square and one rectangle. Each side of a storage uses exactly one plank, so a square requires four planks of the same length and a rectangle requires two pairs of equal-length planks. She receives a stream of updates from the storehouse, either adding a plank of a certain length or removing one. After each update, we need to determine if it is possible to select planks to build both a square and a rectangle simultaneously.

The input gives the initial count of planks and their lengths, followed by a series of events. The output is a sequence of "YES" or "NO" responses, one for each event, indicating whether the current plank set allows constructing both storages.

Constraints are significant: up to $10^5$ planks and $10^5$ events, with plank lengths up to $10^5$. This rules out any approach that iterates through all planks per query, as that would result in $O(n \cdot q)$ complexity, which can reach $10^{10}$ operations. We need a method that maintains counts efficiently and queries feasibility in constant time.

Non-obvious edge cases arise from the overlap of plank usage. For example, having exactly four planks of one length and two of another allows building both a square and rectangle, but a naive check for "any four planks + any two pairs" might falsely assume sufficiency if it doesn't account for overlapping planks. Sparse distributions also matter: having many lengths with only one or two planks each is insufficient, even if the total plank count is high.

## Approaches

A brute-force method would store all planks in a multiset and, for each event, attempt to form all possible combinations of four and two pairs to check if a square and rectangle can be built. This is correct logically but too slow: checking all combinations is $O(n^2)$ or worse per query.

The optimal approach leverages the fact that we only care about counts of planks that are at least two (for a rectangle side) or four (for a square). We can maintain two counters: one for the number of plank lengths with at least two planks (`pairs`) and another for the number of lengths with at least four planks (`quads`). Each update increments or decrements these counters as plank counts cross thresholds. After every update, we can determine feasibility using a simple condition:

1. There must be at least one `quad` to form the square.
2. There must be at least two `pairs` in total, but one `pair` can come from the `quad` used for the square.

This avoids checking every plank individually and reduces each query to constant time updates and checks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) per query | O(n) | Too slow |
| Optimal | O(1) per query | O(1e5) | Accepted |

## Algorithm Walkthrough

1. Initialize a frequency array `count` indexed by plank length to store the number of planks for each length. Also maintain `pairs` for counts ≥2 and `quads` for counts ≥4.
2. Preprocess the initial planks. For each length, increment the `pairs` counter if the count reaches 2 and increment `quads` if it reaches 4.
3. For each event, update the frequency for the affected plank length. If the update crosses the 2 or 4 thresholds, adjust `pairs` or `quads` accordingly. Increment counters if thresholds are reached, decrement if thresholds are no longer met.
4. After updating the frequency, check if it's possible to build the storages. The condition is `quads ≥ 1` and `pairs ≥ 4`. `pairs ≥ 4` ensures we have enough planks for the square and a rectangle simultaneously.
5. Output "YES" if the condition holds, otherwise "NO".

Why it works: By counting lengths with at least two and four planks and updating these counts incrementally, we capture all possible ways to form squares and rectangles without enumerating combinations. The invariant is that the `quads` count always reflects the number of lengths available to form a square,
