---
title: "CF 1774B - Coloring"
description: "This is a Type B (prove inequality) problem, not Type C. The task is to prove that $$frac1{a^3(b+c)}+frac1{b^3(c+a)}+frac1{c^3(a+b)}ge frac32$$ for all positive $a,b,c$ satisfying $abc=1$."
date: "2026-06-09T11:59:31+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1774
codeforces_index: "B"
codeforces_contest_name: "Polynomial Round 2022 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 1500
weight: 1774
solve_time_s: 137
verified: false
draft: false
---

[CF 1774B - Coloring](https://codeforces.com/problemset/problem/1774/B)

**Rating:** 1500  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 2m 17s  
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
