---
title: "CF 103109A - Pok\u00e9mon Permutation"
description: "Let $kappat$ be the function defined in the section, with inverse $mut$ in the sense that $$M ge mut N quad Longleftrightarrow quad kappat(M) ge N,$$ for $t ge 2$."
date: "2026-07-03T21:13:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103109
codeforces_index: "A"
codeforces_contest_name: "mBIT Advanced Spring 2021"
rating: 0
weight: 103109
solve_time_s: 156
verified: false
draft: false
---

[CF 103109A - Pok\u00e9mon Permutation](https://codeforces.com/problemset/problem/103109/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 36s  
**Verified:** no  

## Solution
## Solution

Let $\kappa_t$ be the function defined in the section, with inverse $\mu_t$ in the sense that

$$M \ge \mu_t N \quad \Longleftrightarrow \quad \kappa_t(M) \ge N,$$

for $t \ge 2$. Let $\lambda_{t-1} M$ denote the $(t-1)$-level contribution in the binomial representation of $\kappa_t(M)$, so that the defining decomposition from the construction of $\kappa_t$ gives

$$\kappa_t(M) = M + \lambda_{t-1} M.$$

This identity follows from the representation of $\kappa_t(M)$ as a sum of binomial contributions in which the top-level term is $M$ and the remaining contribution is exactly the $(t-1)$-structure applied to $M$.

Assume first that $M \ge \mu_t N$. By the defining property of $\mu_t$, this is equivalent to $\kappa_t(M) \ge N$. Substituting the decomposition of $\kappa_t(M)$ yields

$$M + \lambda_{t-1} M \ge N.$$

Conversely, assume $M + \lambda_{t-1} M \ge N$. Rewriting the left-hand side using the same decomposition gives $\kappa_t(M) \ge N$, hence by the defining equivalence of $\mu_t$,

$$M \ge \mu_t N.$$

Both implications are reversible since each step uses an equality in the decomposition of $\kappa_t(M)$ and the defining equivalence between $\mu_t$ and $\kappa_t$. Therefore,

$$M \ge \mu_t N \quad \Longleftrightarrow \quad M + \lambda_{t-1} M \ge N.$$

This completes the proof. ∎
