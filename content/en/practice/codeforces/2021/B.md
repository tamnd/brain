---
title: "CF 2021B - Maximize Mex"
description: "We start with an array of non-negative integers. The only operation allowed is to pick an element and add x to it. We may repeat this operation any number of times on any element. Adding x repeatedly has a very specific effect."
date: "2026-06-08T12:41:11+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2021
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 977 (Div. 2, based on COMPFEST 16 - Final Round)"
rating: 1200
weight: 2021
solve_time_s: 39
verified: false
draft: false
---

[CF 2021B - Maximize Mex](https://codeforces.com/problemset/problem/2021/B)

**Rating:** 1200  
**Tags:** brute force, greedy, math, number theory  
**Solve time:** 39s  
**Verified:** no  

## Solution
## Problem Understanding

We start with an array of non-negative integers. The only operation allowed is to pick an element and add `x` to it. We may repeat this operation any number of times on any element.

Adding `x` repeatedly has a very specific effect. An element can only move through values that share the same remainder modulo `x`. For example, if `x = 3` and an element is `2`, then it can become `5`, `8`, `11`, and so on, but it can never become `0`, `1`, `3`, or `4`.

The goal is to maximize the MEX of the final array. Recall that the MEX is the smallest non-negative integer that does not appear in the array. To make the MEX as large as possible, we want to make sure that `0, 1, 2, ...` appear consecutively for as long as possible.

The total number of array elements across all test cases is at most `2·10^5`. That immediately rules out any approach that tries to simulate operations explicitly, since a single value can be increased an arbitrary number of times. We need a method whose complexity is roughly linear or `O(n log n)` per test case.

The tricky part is that operations only increase values. A number can help create some larger value with the same remainder modulo `x`, but it can never be reduced. Any solution that ignores this restriction will produce incorrect answers.

Consider the array `[1]` with `x = 2`. The answer is `0`. We have no way to create a `0` because operations only increase numbers. A careless approach that only checks remainders might incorrectly think the element with remainder `1` can be used to build every odd number.

Another subtle case is `[0, 0, 0]` with `x = 1`. Since every value has the same remainder, we can transform the dup
