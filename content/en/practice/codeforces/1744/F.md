---
title: "CF 1744F - MEX vs MED"
description: "Place the square in coordinates with (A(0,0)), (B(1,0)), (C(1,1)), (D(0,1)). Then (E) lies on (AB) and (F) on (BC) with (BE=BF). Writing (E=(x,0)) gives (BE=1-x), while (F=(1,y)) gives (BF=y), hence (y=1-x) and (F=(1,1-x))."
date: "2026-06-09T15:58:55+07:00"
tags: ["codeforces", "competitive-programming", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1744
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round  828 (Div. 3)"
rating: 2000
weight: 1744
solve_time_s: 114
verified: false
draft: false
---

[CF 1744F - MEX vs MED](https://codeforces.com/problemset/problem/1744/F)

**Rating:** 2000  
**Tags:** math, two pointers  
**Solve time:** 1m 54s  
**Verified:** no  

## Solution
## Exploration

Place the square in coordinates with (A(0,0)), (B(1,0)), (C(1,1)), (D(0,1)). Then (E) lies on (AB) and (F) on (BC) with (BE=BF). Writing (E=(x,0)) gives (BE=1-x), while (F=(1,y)) gives (BF=y), hence (y=1-x) and (F=(1,1-x)).

Midpoints are

[
L=\left(\frac{x+1}{2},\frac{1-x}{2}\right),\quad
N=\left(\frac12,1-\frac{x}{2}\right),\quad
O=\left(\frac12,\frac12\right).
]

The point (K) is obtained from the intersection of (AL) with (DF).

The goal is to prove that (C(1,1),K,L,O,N) are concyclic. Since all coordinates are explicit rational expressions in (x), the most stable approach is to determine the circle through three points depending on (x) and verify the remaining two lie on it.

The most delicate point is ensuring that the circle is computed correctly from a configuration where one point, (L), depends on a parameter (x), so the coefficients of the circle also depend on (x).

## Problem Understanding

The task is to prove that five explicitly constructed points in a square lie on a common circle.

The key difficulty is that one of the defining points of the circle, (L), depends on a free parameter (x), so the circle must
