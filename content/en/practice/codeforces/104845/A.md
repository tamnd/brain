---
title: "CF 104845A - \u041f\u043e\u0434\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435 \u0431\u043e\u0434\u0440\u043e\u0441\u0442\u0438"
description: "We are given a fixed number of days, and each day Igor must choose exactly one of two actions. He can either study, which reduces his “energy” by a fixed amount, or go to sleep early, which increases it by another fixed amount."
date: "2026-06-28T11:29:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104845
codeforces_index: "A"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u041c\u043e\u0441\u043a\u043e\u0432\u0441\u043a\u043e\u0439 \u043e\u0431\u043b\u0430\u0441\u0442\u0438 2023-2024 (9-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 104845
solve_time_s: 26
verified: false
draft: false
---

[CF 104845A - \u041f\u043e\u0434\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435 \u0431\u043e\u0434\u0440\u043e\u0441\u0442\u0438](https://codeforces.com/problemset/problem/104845/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 26s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a fixed number of days, and each day Igor must choose exactly one of two actions. He can either study, which reduces his “energy” by a fixed amount, or go to sleep early, which increases it by another fixed amount. After all days are decided, the total change in energy must be exactly zero, meaning he ends where he started.

The objective is not just to find any valid schedule, but to maximize how many days are spent studying under this constraint.

If we denote the number of study days by $x$, then the remaining $N - x$ days are rest days. Each study day contributes $-B$, and each rest day contributes $+A$. The final condition is that the total sum of changes must be zero.

So the problem reduces to checking whether there exists an integer $x$ in $[0, N]$ such that:

$$x \cdot (-B) + (N - x)\cdot A = 0$$

The output is either the maximum such $x$, or $-1$ if no valid schedule exists.

The constraints are extremely large, up to $N, A, B \le 10^{18}$, so any approach that iterates over days or tries all values of $x$ is immediately impossible. Even linear scans over $x$ would be infeasible, since $10^{18}$ operations is far beyond any limit.

A subtle point is that the equation may have no integer solution even if fractional solutions exist. Another important issue is divisibility: even when algebra suggests a solution, it might not be integral.

A common mistake is treating the equation as always solvable by rearranging it, without checking whether the resulting value is an integer or within bounds. Another failure mode is ignoring the constraint $x \le N$, which leads to mathematically valid but physically impossible schedules.

Example edge failure:

Input:

```
2
1
2
```

Trying $x = 2$: energy change is $-4$, impossible to balance. Trying (x = 1
