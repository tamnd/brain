---
title: "CF 1999A - A+B Again?"
description: "The task asks for the sum of the digits of a two-digit number for multiple test cases. Each input number $n$ is guaranteed to be between 10 and 99 inclusive, so the first digit is always nonzero."
date: "2026-06-08T14:19:23+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1999
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 964 (Div. 4)"
rating: 800
weight: 1999
solve_time_s: 77
verified: false
draft: false
---

[CF 1999A - A+B Again?](https://codeforces.com/problemset/problem/1999/A)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 1m 17s  
**Verified:** no  

## Solution
## Problem Understanding

The task asks for the sum of the digits of a two-digit number for multiple test cases. Each input number $n$ is guaranteed to be between 10 and 99 inclusive, so the first digit is always nonzero. The input begins with $t$, the number of test cases, followed by $t$ lines each containing a single two-digit integer. The output for each test case is a single integer representing the sum of the tens and units digits.

Given the constraints, the number of test cases $t$ is small, up to 90, and each $n$ is fixed in size. There is no need for complex algorithms or data structures because even a straightforward approach that computes the sum for each number individually is sufficiently fast. Edge cases are straightforward: the smallest two-digit number is 10, which has a digit sum of 1, and the largest is 99, with a digit sum of 18. A careless approach might attempt to convert numbers to strings unnecessarily or mishandle 10, but a simple arithmetic approach using division and modulo avoids these pitfalls.

## Approaches

The brute-force approach is to convert each number to a string, split it into characters, convert those characters back to integers, and sum them. This works correctly because each number is guaranteed to have exactly two digits. The downside is that it involves string operations, which are unnecessary for numbers of this size.

The optimal approach is purely arithmetic. For a two-digit number $n$, the tens digit can be computed as $n // 10$ and the units digit as $n % 10$. Summing these two values gives the digit sum directly, avoiding any string manipulation and operating in constant time per test case. Given that $t$ is at most 90, this approach will complete in well under one second.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Convert to string and sum digits | O(t) | O(1) | Accepted |
| Arithmetic digit extraction | O(t) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer $t$ from input, which represents the number of test cases.
2. Loop over each test case from 1 to $t$.
3. For the current test case, read the integer $
