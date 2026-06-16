---
title: "CF 1725F - Field Photography"
description: "Each row initially contains a contiguous block of contestants placed on an extremely large integer line of columns. Row $i$ occupies every position from $Li$ to $Ri$, so geometrically each row is just a closed interval."
date: "2026-06-16T16:52:35+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "data-structures", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1725
codeforces_index: "F"
codeforces_contest_name: "COMPFEST 14 - Preliminary Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 2100
weight: 1725
solve_time_s: 175
verified: false
draft: false
---

[CF 1725F - Field Photography](https://codeforces.com/problemset/problem/1725/F)

**Rating:** 2100  
**Tags:** bitmasks, data structures, sortings  
**Solve time:** 2m 55s  
**Verified:** no  

## Solution
## Problem Understanding

Each row initially contains a contiguous block of contestants placed on an extremely large integer line of columns. Row $i$ occupies every position from $L_i$ to $R_i$, so geometrically each row is just a closed interval.

We are allowed to shift an entire row left or right by any positive integer $k$. Each such move adds $k$ into a global accumulator using bitwise OR. For a query value $W$, we must choose a seq
