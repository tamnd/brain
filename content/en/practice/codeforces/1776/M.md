---
title: "CF 1776M - Parmigiana With Seafood"
description: "This is a Type B (prove inequality) problem, not Type C. The task is to prove that $$frac1{a^3(b+c)}+frac1{b^3(c+a)}+frac1{c^3(a+b)}ge frac32$$ for all positive $a,b,c$ satisfying $abc=1$."
date: "2026-06-09T11:51:15+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 1776
codeforces_index: "M"
codeforces_contest_name: "SWERC 2022-2023 - Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 3000
weight: 1776
solve_time_s: 140
verified: false
draft: false
---

[CF 1776M - Parmigiana With Seafood](https://codeforces.com/problemset/problem/1776/M)

**Rating:** 3000  
**Tags:** binary search, dp, greedy, trees  
**Solve time:** 2m 20s  
**Verified:** no  

## Solution
## Problem-Type Check

This is a **Type B (prove inequality)** problem, not Type C.

The task is to prove that

$$\frac1{a^3(b+c)}+\frac1{b^3(c+a)}+\frac1{c^3(a+b)}\ge \frac32$$

for all positive $a,b,c$ satisfying $abc=1$.

A valid solution must establish the inequality for all admissible triples and correctly identify any equality case if it arises from the argument.

## Step-by-Step Verification

### Step 1: Rewrite the expression using $abc=1$

The solution claims

$$\frac1{a^3(b+c)}=\frac{b^3c^3}{b+c},$$

and similarly for the cyclic terms.

**Assessment:** VALID.

Since $abc=1$, we have $a=\frac1{bc}$, hence $a^{-3}=b^3c^3$.

Thus

$$\sum \frac1{a^3(b+c)}
=
\sum \frac{b^3c^3}{b+c}.$$

### Step 2: Apply Engel-Cauchy

The solution applies

\sum \frac{(b^{3/2}c^{3/2})^2}{b+c} \ge \frac{\left(\sum b^{3/2}c^{3/2}\right)^2} {(a+b)+(b+c)+(
