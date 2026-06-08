---
title: "CF 2202B - ABAB Construction"
description: "The value $V = 7frac{1}{16}$ corresponds to the chi-square statistic computed from $k = 11$ categories, as in Eq. (5). The number of degrees of freedom is therefore $nu = k - 1 = 10$."
date: "2026-06-09T04:49:17+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2202
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1082 (Div. 2)"
rating: 1200
weight: 2202
solve_time_s: 128
verified: false
draft: false
---

[CF 2202B - ABAB Construction](https://codeforces.com/problemset/problem/2202/B)

**Rating:** 1200  
**Tags:** dp, greedy, implementation  
**Solve time:** 2m 8s  
**Verified:** no  

## Solution
The value $V = 7\frac{1}{16}$ corresponds to the chi-square statistic computed from $k = 11$ categories, as in Eq. (5). The number of degrees of freedom is therefore $\nu = k - 1 = 10$. To determine whether $V$ is improbably high, one consults the line of Table 1 corresponding to $\nu = 10$, which lists the percentage points of the chi-square distribution for 10 degrees of freedom. This line provides the approximate threshold values against which $V$ can be compared to assess its extremity.

Since $7\frac{1}{16} = 7.0625$ lies between the 50 percent and 75 percent entries for $\nu = 10$, it is not considered significantly high; nevertheless, the appropriate line to use in the table is the one with $\nu = 10$.

∎
