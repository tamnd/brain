---
title: "CF 1331B - Limericks"
description: "The problem asks us to compute a specific numeric property related to an integer input, denoted as a. While the problem statement is written in a poetic form, the underlying task is to find the number of integers less than a that are coprime to a."
date: "2026-06-11T16:12:26+07:00"
tags: ["codeforces", "competitive-programming", "*special", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1331
codeforces_index: "B"
codeforces_contest_name: "April Fools Day Contest 2020"
rating: 0
weight: 1331
solve_time_s: 216
verified: false
draft: false
---

[CF 1331B - Limericks](https://codeforces.com/problemset/problem/1331/B)

**Rating:** -  
**Tags:** *special, math, number theory  
**Solve time:** 3m 36s  
**Verified:** no  

## Solution
## Problem Understanding

The problem asks us to compute a specific numeric property related to an integer input, denoted as `a`. While the problem statement is written in a poetic form, the underlying task is to find the number of integers less than `a` that are coprime to `a`. In other words, given `a`, we are asked to compute the value of Euler's totient function, commonly written as φ(a). This function counts the integers from 1 to `a - 1` that share no common factors with `a` other than 1.

The input is a single integer `a` in the range 4 to 998, inclusive. Because the maximum `a` is less than 1000, we can afford to use simple factorization or iteration methods without worrying about hitting time limits. Since we only have one integer per test case, an `O(sqrt(a))` approach is sufficient, as it will perform at most around 31 iterations in the worst case.

A non-obvious edge case arises when `a` is a power of a prime, such as 4, 8, or 9. For `a = 4`, the integers less than 4 that are coprime to 4 are 1 and 3, giving φ(4) = 2. A naive approach that only removes even numbers would fail for `a = 9`, which requires removing multiples of 3. Another potential pitfall is assuming `a` is prime or even; the input can be any integer in the given range.

## Approaches

The brute-force approach to compute φ(a) would be to iterate through all integers from 1 to `a - 1` and check for each whether the greatest common divisor with `a` is 1. This works because the GCD function correctly identifies coprime numbers. The operation count in the worst case is approximately `a * log(a)` if using Euclid's algorithm for GCD, which for `a` up to 998 is about 10^4 operations and acceptable for a single test case.

The optimal approach uses the multiplicative property of the Euler totient function. If `a` can be factorized as `a = p1^e1 * p2^e2 * ... * pk^ek` for distinct prime factors `pi`, then φ(a) = a * Π(1 - 1/pi). The observation that every integer less than `a` that is not divisible by any of its prime factors is coprime allows us to compute the answer in `O(sqrt(a))` time, by trial division to find prime factors. This is faster for larger ranges, but with `a` < 1000, both brute-force and factorization approaches are feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(a log a) | O(1) | Accepted |
| Factorization | O(sqrt(a)) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `a` from input. This is the number for which we will compute the totient function.
2. Initialize a variable `result` to `a`. This will hold the running product for the totient formula.
3. Iterate over all integers `i` from 2 up to `sqrt(a)` (inclusive). Each `i` is a candidate
