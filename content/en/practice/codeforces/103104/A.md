---
title: "CF 103104A - CRC Test"
description: "Fix an integer $t ge 1$. Let $N ge 0$ be given. Define $kappat N$ in the discrete sense (as in earlier parts of Section 7.2.1.3) as the unique integer $m ge t-1$ such that $$binom{m}{t} le N < binom{m+1}{t},$$ and set $$kappat N = binom{m}{t-1}."
date: "2026-07-03T21:43:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103104
codeforces_index: "A"
codeforces_contest_name: "2021 Hubei Provincial Collegiate Programming Contest"
rating: 0
weight: 103104
solve_time_s: 160
verified: false
draft: false
---

[CF 103104A - CRC Test](https://codeforces.com/problemset/problem/103104/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 40s  
**Verified:** no  

## Solution
## Setup

Fix an integer $t \ge 1$. Let $N \ge 0$ be given. Define $\kappa_t N$ in the discrete sense (as in earlier parts of Section 7.2.1.3) as the unique integer $m \ge t-1$ such that

$$\binom{m}{t} \le N < \binom{m+1}{t},$$

and set

$$\kappa_t N = \binom{m}{t-1}.$$

Now define the continuous extension as follows. For $x \ge t-1$, the function $x \mapsto \binom{x}{t}$ is strictly increasing, hence invertible onto $[0,\infty)$. For each $N \ge 0$, let $x \ge t-1$ satisfy

$$N = \binom{x}{t},$$

and define

$$\widetilde{\kappa}_t N = \binom{x}{t-1}.$$

The goal is to prove

$$\kappa_t N \le \widetilde{\kappa}_t N$$

for all integers $t \ge 1$ and $N \ge 0$.

## Solution

Let $N \ge 0$ and choose $x \ge t-1$ such that $N = \binom{x}{t}$. Let $m$ be the integer determined by

$$\binom{m}{t} \le \binom{x}{t} < \binom{m+1}{t}.$$

Since $x \mapsto \binom{x}{t}$ is strictly increasing on $[t-1,\infty)$, the inequalities imply $m \le x < m+1$.

The function $x \mapsto \binom{x}{t-1}$ is also strictly increasing on $[t-2,\infty)$. For real $x \ge m \ge t-1$, the monotonicity yields

$$\binom{m}{t-1} \le \binom{x}{t-1}.$$

By the definition of $\kappa_t N$ in the discrete sense,

$$\kappa_t N = \binom{m}{t-1}.$$

By the definition of the continuous extension,

$$\widetilde{\kappa}_t N = \binom{x}{t-1}.$$

Substitution into the inequality gives

$$\kappa_t N \le \widetilde{\kappa}_t N.$$

This completes the proof. ∎

## Verification

For real $x \ge t-1$, the expression

$$\binom{x}{t} = \frac{x(x-1)\cdots(x-t+1)}{t!}$$

is a product of $t$ linear factors, each nondecreasing in $x$ on $[t-1,\infty)$, hence the product is strictly increasing. The same argument applies to $\binom{x}{t-1}$ on $[t-2,\infty)$.

If $m$ is defined by $\binom{m}{t} \le \binom{x}{t} < \binom{m+1}{t}$, monotonicity forces $m \le x < m+1$, since otherwise the strict increase would contradict the ordering.

The inequality $\binom{m}{t-1} \le \binom{x}{t-1}$ follows directly from monotonicity with $m \le x$.

All substitutions are consistent with the definitions of $\kappa_t N$ and $\widetilde{\kappa}_t N$.

## Notes

The argument relies only on monotonicity of generalized binomial coefficients on $[t-1,\infty)$ and does not require convexity or differentiability. Equality holds when $x$ is an integer because then $N = \binom{x}{t}$ forces $m = x$, so both definitions give $\binom{x}{t-1}$.
