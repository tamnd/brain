---
title: "CF 105163I - This is an easy problem"
description: "The task is centered around inspecting the binary representation of an integer and reasoning about individual bits."
date: "2026-06-27T10:54:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105163
codeforces_index: "I"
codeforces_contest_name: "The 19th Heilongjiang Provincial Collegiate Programming Contest"
rating: 0
weight: 105163
solve_time_s: 32
verified: false
draft: false
---

[CF 105163I - This is an easy problem](https://codeforces.com/problemset/problem/105163/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 32s  
**Verified:** no  

## Solution
## Problem Understanding

The task is centered around inspecting the binary representation of an integer and reasoning about individual bits. Instead of treating the number as a single value, we interpret it as a sequence of independent binary positions, where each position contributes either a zero or a one depending on whether that bit is set.

The goal can be understood as scanning through all relevant bit positions of the given integer and checking, for each position, whether that bit is active. The check is performed using a bitmask of the form `(1 << i)`, which isolates the i-th bit, and a bitwise AND with the number. If the result is zero, that position contains a zero bit.

From a constraints perspective, the intended approach strongly suggests that the input size per test is small enough for a fixed upper bound scan over bits, typically 30 or 32 iterations per number. This immediately rules out anything that depends on per-bit recursion or combinational exploration across multiple numbers, since those would be unnecessary overhead. The problem is designed so that an O(number of bits) scan is sufficient.

A common edge case in problems like this comes from negative numbers if signed integers are involved. For example, if `x = -1` in a fixed-width representation, all bits are set, so no zero bits exist. A careless implementation that assumes only non-negative input or ignores sign extension may produce inconsistent results. Another edge case appears when `x = 0`, where every bit is zero, and the answer depends on whether the implementation considers a fixed bit width or only significant bits. If we only scan until the highest set bit, we would incorrectly return zero zero-bits, while a fixed-width interpretation would return all positions as zero.

## Approaches

The brute-force idea is to explicitly test every bit position independently. For each index `i`, we construct a mask `1 << i` and check whether `(x & (1 << i))` equals zero. This directly follows the definition of binary representation and is correct because bitwise AND isolates the contribution of that single position.

This approach is already optimal in structure because the number of bit positions is constant with respect to the input value. Even for 32-bit or 64-bit integers, the total work is bounded by a small constant, so there is no meaningful asymptotic improvement possible. The only inefficiency would come from unnecessary work outside the fixed bit scan, which is not present here.

The key observation is that each
