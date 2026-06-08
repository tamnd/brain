---
title: "CF 2216E - Oriented Journey"
description: "The value $V = 7frac{1}{16}$ corresponds to the chi-square statistic computed from $k = 11$ categories, as in Eq. (5). The number of degrees of freedom is therefore $nu = k - 1 = 10$."
date: "2026-06-09T04:55:34+07:00"
tags: ["codeforces", "competitive-programming", "communication", "constructive-algorithms", "interactive"]
categories: ["algorithms"]
codeforces_contest: 2216
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1092 (Unrated, Div. 2, Based on THUPC 2026 \u2014 Finals)"
rating: 2200
weight: 2216
solve_time_s: 121
verified: false
draft: false
---

[CF 2216E - Oriented Journey](https://codeforces.com/problemset/problem/2216/E)

**Rating:** 2200  
**Tags:** communication, constructive algorithms, interactive  
**Solve time:** 2m 1s  
**Verified:** no  

## Solution
The value $V = 7\frac{1}{16}$ corresponds to the chi-square statistic computed from $k = 11$ categories, as in Eq. (5). The number of degrees of freedom is therefore $\nu = k - 1 = 10$. To determine whether $V$ is improbably high, one consults the line of Table 1 corresponding to $\nu = 10$, which lists the percentage points of the chi-square distribution for 10 degrees of freedom. This line provides the approximate threshold values against which $V$ can be compared to assess its extremity.

Since $7\frac{1}{16} = 7.0625$ lies between the 50 percent and 75 percent entries for $\nu = 10$, it is not considered significantly high; nevertheless, the appropriate line to use in the table is the one with $\nu = 10$.

∎
