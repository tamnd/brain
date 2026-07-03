---
title: "CF 102980B - \u041f\u043e\u0432\u0440\u0435\u0436\u0434\u0435\u043d\u043d\u044b\u0439 \u043f\u0430\u0440\u043e\u043b\u044c"
description: "Let $mathcal{A}$ be a set of $t$-combinations and let $ $$kappat N = min{ where $partial mathcal{A}$ is the set of all $(t-1)$-subsets obtained by deleting one element from a member of $mathcal{A}$."
date: "2026-07-04T03:25:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102980
codeforces_index: "B"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2020-2021, \u041f\u0435\u0440\u0432\u0430\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102980
solve_time_s: 71
verified: false
draft: false
---

[CF 102980B - \u041f\u043e\u0432\u0440\u0435\u0436\u0434\u0435\u043d\u043d\u044b\u0439 \u043f\u0430\u0440\u043e\u043b\u044c](https://codeforces.com/problemset/problem/102980/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** no  

## Solution
## Solution

Let $\mathcal{A}$ be a set of $t$-combinations and let $|\mathcal{A}| = N$. The operator $\kappa_t N$ denotes the minimum possible size of the shadow of any family of $N$ $t$-combinations, that is

$$\kappa_t N = \min_{|\mathcal{A}| = N} |\partial \mathcal{A}|,$$

where $\partial \mathcal{A}$ is the set of all $(t-1)$-subsets obtained by deleting one element from a member of $\mathcal{A}$.

From the definition of $\partial$, each $t$-combination contributes exactly $t$ distinct $(t-1)$-subsets before identifications from overlaps. Hence for every $\mathcal{A}$,

$$|\partial \mathcal{A}| \le t |\mathcal{A}| = tN.$$

This bound is attained when $N=1$, since a single $t$-combination has exactly $t$ distinct $(t-1)$-subsets. Therefore,

$$\kappa_t 1 = t.$$

Consequently,

$$\kappa_t 1 - 1 = t - 1.$$

To determine whether any larger value can occur, consider $N \ge 2$. Any two distinct $t$-combinations share at least one $(t-1)$-subset only when they differ in exactly one element; in that case their shadows overlap in at least one element, reducing the total shadow size strictly below $tN$. Hence for $N \ge 2$,

$$\kappa_t N \le tN - 1,$$

since at least one overlap occurs in the shadow of any non-singleton family. This implies

$$\kappa_t N - N \le (t-1)N - 1,$$

which is strictly less than $t-1$ for all $N \ge 2$.

For $N=0$, $\kappa_t 0 = 0$ and the difference is $0$.

For $N=1$, the value is $t-1$, and this is the only case where the upper bound $t$ shadow size is achieved without overlap.

Thus the maximum of $\kappa_t N - N$ over all $N \ge 0$ is attained at $N=1$ and equals

$$\boxed{t-1}.$$

This completes the proof. ∎
