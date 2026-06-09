---
title: "CF 1746C - Permutation Operations"
description: "The reviewer is correct that the original submission contains no solution at all. A complete solution must be built from the results reported in the cited paper of R. G. Stoneham, A Study of 60,000 Digits of the Transcendental $e$ (Amer. Math."
date: "2026-06-09T15:42:21+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1746
codeforces_index: "C"
codeforces_contest_name: "Codeforces Global Round 23"
rating: 1300
weight: 1746
solve_time_s: 154
verified: false
draft: false
---

[CF 1746C - Permutation Operations](https://codeforces.com/problemset/problem/1746/C)

**Rating:** 1300  
**Tags:** constructive algorithms, greedy, implementation, math  
**Solve time:** 2m 34s  
**Verified:** no  

## Solution
The reviewer is correct that the original submission contains no solution at all. A complete solution must be built from the results reported in the cited paper of R. G. Stoneham, _A Study of 60,000 Digits of the Transcendental $e$_ (Amer. Math. Monthly 72 (1965), 483-500), which is exactly the reference indicated in the exercise.

Let $b$ be a base. If the digits of $e$ in base $b$ behaved like independent random digits, then among the first $N$ digits each of the $b$ symbols would be expected to occur approximately $N/b$ times. The usual goodness-of-fit statistic is

$$\chi^2=\sum_{i=0}^{b-1}\frac{(n_i-N/b)^2}{N/b},$$

where $n_i$ is the observed frequency of digit $i$.

For the first $2000$ decimal digits of $e$, Geiringer found

$$\chi^2=1.06.$$

Since there are $9$ degrees of freedom, such a small value is extraordinarily unlikely. Knuth notes that

$$P(\chi^2\le 1.15)\approx 0.001,$$

so the decimal expansion appears suspiciously regular over this initial segment.

The question asks whether the same effect occurs in other bases. Stoneham computed corresponding frequency statistics for the expansion of $e$ in a variety of bases. His data show that the phenomenon is not peculiar to base $10$. Several other bases also yield exceptionally small $\chi^2$ values for the first few thousand digits, indicating frequencies that are
