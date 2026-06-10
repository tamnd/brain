---
title: "CF 1553G - Common Divisor Graph"
description: "The solution correctly addresses the exercise. It implements left-to-right addition of two numbers in base $b$, emits digits only when they cannot be affected by future carries, and never revises a committed digit."
date: "2026-06-10T13:06:04+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "dsu", "graphs", "hashing", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1553
codeforces_index: "G"
codeforces_contest_name: "Harbour.Space Scholarship Contest 2021-2022 (open for everyone, rated, Div. 1 + Div. 2)"
rating: 2700
weight: 1553
solve_time_s: 75
verified: false
draft: false
---

[CF 1553G - Common Divisor Graph](https://codeforces.com/problemset/problem/1553/G)

**Rating:** 2700  
**Tags:** brute force, constructive algorithms, dsu, graphs, hashing, math, number theory  
**Solve time:** 1m 15s  
**Verified:** no  

## Solution
## Correctness

The solution correctly addresses the exercise. It implements left-to-right addition of two numbers in base $b$, emits digits only when they cannot be affected by future carries, and never revises a committed digit. The use of a buffer to store tentative digits and a counter to track consecutive $b-1$ digits ensures that no digit is output prematurely. The algorithm handles unequal lengths via zero-padding, manages final carries properly, and supports arbitrary base $b \ge 2$. Step-by-step reasoning, example execution, and complexity analysis are provided.

## Gaps and Errors

1. **Critical implementation gap**: None. The solution reads actual digits, uses the correct base, and performs addition left-to-right with safe emission.
2. **Justification gaps**: The solution implicitly assumes that flushing digits before the trailing run of $b-1$ digits is always safe. This is correct, but a formal proof could explicitly argue that no carry from future positions can propagate through a smaller digit to affect these flushed digits. This is minor, as it follows directly from the standard carry propagation rules.
3. **Edge cases**: All critical edge cases are addressed, including full runs of $b-1$, final carries, and numbers of unequal length.

No steps are circular or incorrect. Every algorithmic claim is justified either by explanation, invariant maintenance, or example.

## Summary

The proposed solution is conceptually sound, correctly implemented, linear in time, handles all edge cases, and faithfully follows the left-to-right, carry-safe emission rule required by Exercise 4.3.1.6.

VERDICT: PASS - the solution is correct and complete.
