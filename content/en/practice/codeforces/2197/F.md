---
title: "CF 2197F - Double Bracket Sequence"
description: "The value $V = 7frac{1}{16}$ corresponds to the chi-square statistic computed from $k = 11$ categories, as in Eq. (5). The number of degrees of freedom is therefore $nu = k - 1 = 10$."
date: "2026-06-09T04:47:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "flows", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2197
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 1079 (Div. 2)"
rating: 2500
weight: 2197
solve_time_s: 125
verified: false
draft: false
---

[CF 2197F - Double Bracket Sequence](https://codeforces.com/problemset/problem/2197/F)

**Rating:** 2500  
**Tags:** data structures, dp, flows, greedy  
**Solve time:** 2m 5s  
**Verified:** no  

## Solution
The value $V = 7\frac{1}{16}$ corresponds to the chi-square statistic computed from $k = 11$ categories, as in Eq. (5). The number of degrees of freedom is therefore $\nu = k - 1 = 10$. To determine whether $V$ is improbably high, one consults the line of Table 1 corresponding to $\nu = 10$, which lists the percentage points of the chi-square distribution for 10 degrees of freedom. This line provides the approximate threshold values against which $V$ can be compared to assess its extremity.

Since $7\frac{1}{16} = 7.0625$ lies between the 50 percent and 75 percent entries for $\nu = 10$, it is not considered significantly high; nevertheless, the appropriate line to use in the table is the one with $\nu = 10$.

∎
