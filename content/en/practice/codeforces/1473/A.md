---
title: "CF 1473A - Replacing Elements"
description: "We are given an array of positive integers and a threshold value, $d$. In one operation, we can pick any element and replace it with the sum of any two other distinct elements."
date: "2026-06-11T00:27:37+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1473
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 102 (Rated for Div. 2)"
rating: 800
weight: 1473
solve_time_s: 164
verified: false
draft: false
---

[CF 1473A - Replacing Elements](https://codeforces.com/problemset/problem/1473/A)

**Rating:** 800  
**Tags:** greedy, implementation, math, sortings  
**Solve time:** 2m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of positive integers and a threshold value, $d$. In one operation, we can pick any element and replace it with the sum of any two other distinct elements. The goal is to determine whether, after some sequence of operations, every element of the array can be made less than or equal to $d$. The input consists of multiple test cases, each giving the array and $d$, and we are to output YES or NO for each case.

Given the constraints, $n$ can be up to 100, $d$ up to 100, and each element up to 100. This tells us that a naive brute-force simulation of every possible operation sequence is feasible only for tiny arrays; the total number of potential operations is combinatorial in $n$, so enumerating all sequences would be astronomically large. Therefore, we must find a property that lets us make a decision without simulating every operation.

A non-obvious edge case occurs when most elements are above $d$ but the two smallest elements are small enough that their sum does not exceed $d$. For example, consider $a = [1, 2, 5]$ with $d = 3$. The largest element is above $d$, but the two smallest sum to $3$, so replacing the largest with their sum yields all elements $\le d$. A careless approach might just check the maximum element and fail to notice this potential transformation.

Another edge case is when all elements are initially below $d$, in which case no operation is needed. Conversely, if the two smallest elements themselves sum to more than $d$, there is no operation that can reduce larger elements, so the answer is immediately NO.

## Approaches

A brute-force approach would try every combination of three indices repeatedly, replacing elements and checking whether all elements fall below $d$. While correct in principle, this is far too slow because each step has $O(n^3)$ choices and we may need to repeat operations many times. For $n = 100$, even a single iteration would require up to $10^6$ steps, and sequences can be arbitrarily long.

The key observation is that only the two smallest elements matter for reducing any larger element. Any element larger than $d$ can only be replaced by the sum of two other elements. The smallest possible sum is the sum of the two smallest elements. If this sum is less than or equal to $d$, we can always replace any large element with that sum.
