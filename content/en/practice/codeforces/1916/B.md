---
title: "CF 1916B - Two Divisors"
description: "We are given two integers, $a$ and $b$, which are the two largest proper divisors of some unknown integer $x$. Here, $1 le a < b < x$, and our task is to find any integer $x$ that fits this description."
date: "2026-06-08T19:49:16+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1916
codeforces_index: "B"
codeforces_contest_name: "Good Bye 2023"
rating: 1000
weight: 1916
solve_time_s: 38
verified: false
draft: false
---

[CF 1916B - Two Divisors](https://codeforces.com/problemset/problem/1916/B)

**Rating:** 1000  
**Tags:** constructive algorithms, math, number theory  
**Solve time:** 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two integers, $a$ and $b$, which are the two largest proper divisors of some unknown integer $x$. Here, $1 \le a < b < x$, and our task is to find any integer $x$ that fits this description. Conceptually, $x$ is the number for which $b$ is the largest divisor below $x$, and $a$ is the second-largest divisor. We must handle multiple independent test cases.

The bounds $1 \le a < b \le 10^9$ and $1 \le t \le 10^4$ tell us that brute-force iteration over all numbers up to $10^9$ would be far too slow. Any approach that attempts to list all divisors of every possible candidate number will result in at least $O(\sqrt{10^9})$ operations per test case, giving roughly $3 \cdot 10^7$ operations in the worst case for a single query, and over $3 \cdot 10^{11}$ for $10^4$ test cases. This is clearly infeasible.

Non-obvious edge cases arise when $a = 1$, since $1$ divides every integer, or when $b$ is a multiple of $a$. For instance, if $a = 1$ and $b = 2$, the smallest $x$ that has $2$ as the largest proper divisor is $4$. If $a = 3$ and $b = 11$, the product $3 \cdot 11 = 33$ produces $11$ as the largest proper divisor and $3$ as the second-largest. A naive approach that simply returns $a \cdot b$ will work in most cases, but we must understand why this is valid in all cases.

## Approaches

The brute-force approach would be to generate all numbers $x$ greater than $b$ and check all their divisors to see if $a$ and $b$ are indeed the largest two. This is correct by definition but impractical due to the high upper bound of $10^9$ and the number of test cases. Checking all divisors up to $\sqrt{x}$ for each candidate $x$ and each query results in unacceptable time complexity.

The optimal approach uses a constructive observation. For any integer $x$, if $b$ is the largest proper divisor, $x$ must be a multiple of $b$, and any other proper divisor smaller than $b$ must divide $
