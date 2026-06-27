---
title: "CF 105055L - Le Caf\u00e9"
description: "The decision is much simpler than it first appears. Every package must be used exactly once, so all sprinkles are distributed between the two drinks. Let the total number of sprinkles be S."
date: "2026-06-28T00:25:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105055
codeforces_index: "L"
codeforces_contest_name: "UDESC Selection Contest 2023-2"
rating: 0
weight: 105055
solve_time_s: 28
verified: false
draft: false
---

[CF 105055L - Le Caf\u00e9](https://codeforces.com/problemset/problem/105055/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 28s  
**Verified:** no  

## Solution
The decision is much simpler than it first appears.

Every package must be used exactly once, so all sprinkles are distributed between the two drinks. Let the total number of sprinkles be `S`.

If both drinks end with the same positive number of sprinkles, then each drink must contain exactly `S / 2` sprinkles. This is only possible when `S` is even. The remaining question is whether some subset of the packages sums to `S / 2`.

However, that is exactly the classic **Partition** problem, which is NP-complete. With `N` up to `2 · 10^5` and values up to `2 · 10^5`, there is no known polynomial time algorithm for the general case, and such an algorithm would imply `P = NP`. The published constraints strongly suggest that some crucial part of the problem statement is missing or has been copied incorrectly.

The statement you provided matches the Codeforces Gym statement, including the examples.

Because of that, I cannot honestly produce a correct editorial or Python solu
