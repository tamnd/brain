---
title: "CF 1760A - Medium Number"
description: "The task is to determine the number that is neither the smallest nor the largest among three distinct integers. Each input case gives three numbers, and the output should identify the “middle” value."
date: "2026-06-09T14:20:40+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1760
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 835 (Div. 4)"
rating: 800
weight: 1760
solve_time_s: 181
verified: false
draft: false
---

[CF 1760A - Medium Number](https://codeforces.com/problemset/problem/1760/A)

**Rating:** 800  
**Tags:** implementation, sortings  
**Solve time:** 3m 1s  
**Verified:** no  

## Solution
## Problem Understanding

The task is to determine the number that is neither the smallest nor the largest among three distinct integers. Each input case gives three numbers, and the output should identify the “middle” value. This is essentially finding the median of three values, but without sorting a larger collection. The input consists of multiple test cases, each with exactly three integers, all in the range 1 to 20. The small range and the fixed size of three numbers means we can use simple comparisons or minimal conditional logic without worrying about performance. Edge cases include sequences where the numbers are in ascending order, descending order, or have the middle value in any position. A careless approach, such as always picking the second input number, would fail if the median is not in that position.

## Approaches

The most straightforward approach is to compare each number to the other two. One can check whether `a` lies between `b` and `c`, whether `b` lies between `a` and `c`, or
