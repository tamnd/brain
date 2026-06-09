---
title: "CF 1787H - Codeforces Scoreboard"
description: "I can't reliably produce a complete editorial and accepted implementation for Codeforces 1787H from the problem statement alone. This is a 3300-rated problem whose accepted solution uses a fairly intricate convex-DP / slope-trick optimization."
date: "2026-06-09T10:55:55+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp", "geometry"]
categories: ["algorithms"]
codeforces_contest: 1787
codeforces_index: "H"
codeforces_contest_name: "TypeDB Forces 2023 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 3300
weight: 1787
solve_time_s: 50
verified: false
draft: false
---

[CF 1787H - Codeforces Scoreboard](https://codeforces.com/problemset/problem/1787/H)

**Rating:** 3300  
**Tags:** binary search, data structures, dp, geometry  
**Solve time:** 50s  
**Verified:** no  

## Solution
I can't reliably produce a complete editorial and accepted implementation for Codeforces 1787H from the problem statement alone.

This is a 3300-rated problem whose accepted solution uses a fairly intricate convex-DP / slope-trick optimization. I was able to reconstruct the quadratic DP

$$dp_{i,j}
=
\min\bigl(
dp_{i-1,j}+c_i,\;
dp_{i-1,j-1}+j\,k_i
\bigr),
\qquad
c_i=b_i-a_i,$$

after sorting by decreasing $k$, which is the standard starting point described in community writeups.

However, I do not have enough information to reconstruct the entire $O(n\log n)$ slope-trick data structure and its implementation details with the level of confidence needed for a "complete solution editorial". Producing a full proof and code here would require me to guess crucial parts of the optimization, and that would risk giving you an incorrect editorial and incorrect code.

If you want a fully correct editorial, I would need either:

1. The official editorial text for problem H, or
2. An accepted C++ implementation, or
3. Permission to do a deeper web-based reconstruction from multiple external sources and then synthesize the solution.

Without one of those, I can only confidently provide the $O(n^2)$ DP derivation, not the accepted $O(n\log n)$ solution.
