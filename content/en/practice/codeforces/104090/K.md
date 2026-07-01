---
title: "CF 104090K - Master of Both"
description: "In a ZDD, each level corresponds to a variable, and a node labeled $k$ represents a decision on $xk$, where the low edge excludes the variable and the high edge includes it in the represented family of sets."
date: "2026-07-02T02:34:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104090
codeforces_index: "K"
codeforces_contest_name: "The 2022 ICPC Asia Hangzhou Regional Programming Contest"
rating: 0
weight: 104090
solve_time_s: 123
verified: false
draft: false
---

[CF 104090K - Master of Both](https://codeforces.com/problemset/problem/104090/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 3s  
**Verified:** no  

## Solution
In a ZDD, each level corresponds to a variable, and a node labeled $k$ represents a decision on $x_k$, where the low edge excludes the variable and the high edge includes it in the represented family of sets. The sink $\perp$ represents the empty family, while $\top$ represents the family containing only the empty set.

The ZDD shown is a single node labeled $x_3$ whose low edge goes to $\perp$ and high edge goes to $\top$. This means that when $x_3=0$, no subset is accepted, and when $x_3=1$, the only accepted subset is the empty continuation after choosing $x_3$.

Thus the represented family consists of exactly one set: ${3}$. All other variables $x_1,x_2,x_4,x_5,x_6$ do not appear in any node, so they must be forced to $0$ in every satisfying assignment.

Therefore the Boolean function is the indicator of the single assignment in which $x_3=1$ and all other variables are $0$:

$$f(x_1,x_2,x_3,x_4,x_5,x_6) = x_3 \cdot \overline{x_1}\,\overline{x_2}\,\overline{x_4}\,\overline{x_5}\,\overline{x_6}.$$

Equivalently, it is the characteristic function of the singleton set ${{3}}$ in subset representation.
