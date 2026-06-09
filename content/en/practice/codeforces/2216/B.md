---
title: "CF 2216B - THU Packing Puzzle"
description: "The value $V = 7frac{1}{16}$ corresponds to the chi-square statistic computed from $k = 11$ categories, as in Eq. (5). The number of degrees of freedom is therefore $nu = k - 1 = 10$."
date: "2026-06-09T04:52:32+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2216
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1092 (Unrated, Div. 2, Based on THUPC 2026 \u2014 Finals)"
rating: 1300
weight: 2216
solve_time_s: 40
verified: false
draft: false
---

[CF 2216B - THU Packing Puzzle](https://codeforces.com/problemset/problem/2216/B)

**Rating:** 1300  
**Tags:** greedy  
**Solve time:** 40s  
**Verified:** no  

## Solution
The value $V = 7\frac{1}{16}$ corresponds to the chi-square statistic computed from $k = 11$ categories, as in Eq. (5). The number of degrees of freedom is therefore $\nu = k - 1 = 10$. To determine whether $V$ is improbably high, one consults the line of Table 1 corresponding to $\nu = 10$, which lists the percentage points of the chi-square distribution for 10 degrees of freedom. This line provides the approximate threshold values against which $V$ can be compared to assess its extremity.

Since $7\frac{1}{16} = 7.0625$ lies between the 50 percent and 75 percent entries for $\nu = 10$, it is not considered significantly high; nevertheless, the appropriate line to use in the table is the one with $\nu = 10$.

∎
