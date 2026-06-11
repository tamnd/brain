---
title: "CF 1373B - 01 Game"
description: "The solution is not correct and complete. Part (a) is essentially correct. The classification of $N$-survivors $le N^3$ is valid, and the argument that a composite $N$-survivor cannot have three prime factors is sufficient."
date: "2026-06-11T11:13:04+07:00"
tags: ["codeforces", "competitive-programming", "games"]
categories: ["algorithms"]
codeforces_contest: 1373
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 90 (Rated for Div. 2)"
rating: 900
weight: 1373
solve_time_s: 159
verified: false
draft: false
---

[CF 1373B - 01 Game](https://codeforces.com/problemset/problem/1373/B)

**Rating:** 900  
**Tags:** games  
**Solve time:** 2m 39s  
**Verified:** no  

## Solution
## Correctness

The solution is not correct and complete.

Part (a) is essentially correct. The classification of $N$-survivors $\le N^3$ is valid, and the argument that a composite $N$-survivor cannot have three prime factors is sufficient. The resulting identity

$$\pi(N^3)=\pi(N)+f(N^3,N)-1-f_2(N^3,N)$$

follows.

Part (b) derives the standard formula

$$f_2(N^3,N)
=
\sum_{\substack{N<p\le N^{3/2}\\ p\ \text{prime}}}
\bigl(\pi(N^3/p)-\pi(p-1)\bigr),$$

which is correct. However, the exercise explicitly asks to "use your method to evaluate $f_2(10^9,10^3)$ by hand." The solution simply states the numerical value

$$f_2(10^9,10^3)=563,158$$

without any computation, derivation, or verification. Therefore the requested evaluation is not actually carried out.

Part (c) proves the recurrence

$$f(x,p_j)=f(x,p_{j-1})-f(x/p_j,p_{j-1}),$$

but it does not explain how to use this recurrence to evaluate $f(N^3,N)$ from values of $\pi(x)$ for $x\le N^2$. The exercise asks for an evaluation method analogous to part (b). The proposed solution merely restates the recurrence and then asserts that repeated application computes $f(N^3,N)$. The crucial reduction to quantities obtainable from $\pi(x)$ is missing.

Part (d) is largely hand-waving. The exercise asks for discussion of data structures supporting efficient evaluation. The solution mentions memoization and claims that the number of distinct values is $O(N^{2/3})$, but no argument is given. Since the stated purpose of the exercise is to obtain an $O(N^{2/3})$ algorithm, the complexity discussion is an important part of the problem.

## Gaps and Errors

1. **Critical error:** Part (b) does not perform the requested evaluation of $f_2(10^9,10^3)$ by hand. The numerical answer is asserted without derivation.
2. **Critical error:** Part (c) does not explain how to evaluate $f(N^3,N)$ from values of $\pi(x)$ for $x\le N^2$. The recurrence is proved, but the computational method requested by the exercise is not developed.
3. **Critical error:** The solution does not establish the advertised $O(N^{2/3})$ framework. The complexity claim appears in part (d) without proof.
4. **Justification gap:** The claim that "the number of distinct values is $O(N^{2/3})$" is stated without argument.
5. **Justification gap:** The statement that $f(N^3,N)$ "can be obtained from the table of values $\pi(x)$ for $x\le N^2$" is asserted but not demonstrated.
6. **Claim used without proof:** The numerical value

$$f_2(10^9,10^3)=563,158$$

is presented without computation or reference.

## Summary

The solution contains the key identity for part (a) and the correct semiprime counting formula for part (b), but it does not complete the computational tasks required in parts (b) and (c), and it does not justify the complexity claims that are central
