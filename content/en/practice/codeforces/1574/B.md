---
title: "CF 1574B - Combinatorics Homework"
description: "The proposed solution appears to be a complete and well-explained editorial for Codeforces 1575A, but it does not address Exercise 4.2.2.16 from TAOCP at all."
date: "2026-06-10T11:04:15+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1574
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 114 (Rated for Div. 2)"
rating: 1100
weight: 1574
solve_time_s: 155
verified: false
draft: false
---

[CF 1574B - Combinatorics Homework](https://codeforces.com/problemset/problem/1574/B)

**Rating:** 1100  
**Tags:** combinatorics, greedy, math  
**Solve time:** 2m 35s  
**Verified:** no  

## Solution
The proposed solution appears to be a complete and well-explained editorial for **Codeforces 1575A**, but it does **not address Exercise 4.2.2.16 from TAOCP at all**. The exercise is about floating-point arithmetic, repeated application of the $\otimes$ operation, and stability of standard deviation formulas, whereas the solution discusses sorting strings in an odd-even custom lexicographic order.

Specifically:

- There is no discussion of $(\cdots((x_1 \otimes x_2) \otimes \cdots \otimes x_n))$ or its behavior when $x_k = 1.111111$ with eight-digit decimal arithmetic.
- There is no analysis of what happens when Eq. (14), Eq. (15), or Eq. (16) are used to calculate the standard deviation of repeated identical numbers.
- There is no proof that $S_k \ge 0$ in Eq. (16) for arbitrary $x_1, \dots, x_k$.
- The entire solution is about a completely unrelated Codeforces problem involving string sorting.

This is a **critical error**, because the solution does not even attempt to solve the assigned TAOCP problem.

VERDICT: FAIL - the solution addresses an unrelated problem instead of Exercise 4.2.2.16 and contains no relevant reasoning.
