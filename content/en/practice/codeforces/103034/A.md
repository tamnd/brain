---
title: "CF 103034A - Pacman and Power Pellet"
description: "Let $$Fn(z)=prod{j=0}^{n-1}(1+z+cdots+z^{sj}), qquad left(!binom{S(n)}{k}!right)=[z^k]Fn(z).$$ Then $Fn=F{n-1}(1+z+cdots+z^{s{n-1}})$, so coefficient extraction gives $$left(!binom{S(n)}{k}!right) = sum{r=0}^{s{n-1}}left(!binom{S(n-1)}{k-r}!"
date: "2026-07-04T05:21:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103034
codeforces_index: "A"
codeforces_contest_name: "April Fools Contest 2021 Archive (ZS)"
rating: 0
weight: 103034
solve_time_s: 139
verified: false
draft: false
---

[CF 103034A - Pacman and Power Pellet](https://codeforces.com/problemset/problem/103034/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 19s  
**Verified:** no  

## Solution
## Solution

Let

$$F_n(z)=\prod_{j=0}^{n-1}(1+z+\cdots+z^{s_j}),
\qquad 
\left(\!\binom{S(n)}{k}\!\right)=[z^k]F_n(z).$$

Then $F_n=F_{n-1}(1+z+\cdots+z^{s_{n-1}})$, so coefficient extraction gives

$$\left(\!\binom{S(n)}{k}\!\right)
=
\sum_{r=0}^{s_{n-1}}\left(\!\binom{S(n-1)}{k-r}\!\right),$$

with the convention that $\left(!\binom{S(n-1)}{k-r}!\right)=0$ when $k-r<0$. This is the exact analogue of Pascal’s rule, derived directly from convolution of coefficients.

Fix $k$. For each $n$, the sequence $\left(!\binom{S(n)}{k}!\right)$ is strictly increasing in $n$ whenever $k\le \sum_{j=0}^{n-1}s_j$, since enlarging $n$ introduces new nonnegative contributions in the convolution above, and at least one term becomes strictly positive when $k$ is feasible for the new factor. In particular, for every fixed $k$ there is a unique minimal $n$ with $\left(!\binom{S(n)}{k}!\right)>0$.

### Existence of the representation

Let $N\ge 0$ and fix $t$. Define $n_t$ as the largest index of the form $s_j\cdot j$ such that

$$\left(\!\binom{S(n_t)}{t}\!\right)\le N.$$

Such an $n_t$ exists because $\left(!\binom{S(n)}{t}!\right)$ eventually exceeds $N$ as $n$ grows, and it is increasing in $n$.

Set

$$N^{(t-1)} = N - \left(\!\binom{S(n_t)}{t}\!\right).$$

From the convolution identity,

$$\left(\!\binom{S(n_t)}{t}\!\right)
=
\left(\!\binom{S(n_t-1)}{t}\!\right)
+
\left(\!\binom{S(n_t-1)}{t-1}\!\right)
+
\cdots
+
\left(\!\binom{S(n_t-1)}{t-s_{n_t-1}}\!\right),$$

so subtracting $\left(!\binom{S(n_t)}{t}!\right)$ removes all configurations whose last coordinate lies in $[0,s_{n_t-1}]$. The remainder $N^{(t-1)}$ is therefore representable using only indices strictly less than $n_t$.

Repeating the same construction produces $n_{t-1}\le n_t$ such that

$$N^{(t-1)}=\left(\!\binom{S(n_{t-1})}{t-1}\!\right)+N^{(t-2)},$$

and continuing yields

$$N=
\left(\!\binom{S(n_t)}{t}\!\right)+
\left(\!\binom{S(n_{t-1})}{t-1}\!\right)+\cdots+
\left(\!\binom{S(n_1)}{1}\!\right),$$

with $n_t\ge n_{t-1}\ge\cdots\ge n_1\ge 0$ and each $n_i$ drawn from the allowed set ${s_0\cdot 0,s_1\cdot 1,\dots}$ because each subtraction step only permits indices compatible with the support of the convolution defining $S(\cdot,\cdot)$.

### Uniqueness

Suppose two representations exist:

$$N=\sum_{i=1}^t \left(\!\binom{S(n_i)}{i}\!\right)
=\sum_{i=1}^t \left(\!\binom{S(m_i)}{i}\!\right),
\qquad
n_t\ge\cdots\ge n_1,\; m_t\ge\cdots\ge m_1.$$

Let $r$ be the largest index such that $n_r\ne m_r$. Without loss of generality $n_r>m_r$. Then monotonicity in $n$ gives

$$\left(\!\binom{S(n_r)}{r}\!\right)\ge \left(\!\binom{S(m_r+1)}{r}\!\right)>\left(\!\binom{S(m_r)}{r}\!\right).$$

All higher-index terms $i>r$ cancel by equality of prefixes, so the left-hand side exceeds the right-hand side, contradicting equality of $N$. This forces $n_r=m_r$ for all $r$, proving uniqueness.

This completes the representation theorem. ∎

### Formula for $|\partial P_{N_t}|$

In Corollary C, the boundary operator $\partial$ acts by reducing exactly one coordinate in the combinatorial structure encoded by the representation. Each term

$$\left(\!\binom{S(n_i)}{i}\!\right)$$

contributes precisely the number of ways to decrease one of the $i$ selected units, which corresponds to choosing one of the $i$ positions contributing to that term. Reducing such a position converts a contribution counted by $S(n_i,i)$ into one counted by $S(n_i,i-1)$.

Summing over all levels yields

$$|\partial P_{N_t}|
=
\sum_{i=1}^t \left(\!\binom{S(n_i)}{i-1}\!\right),$$

with the convention $\left(!\binom{S(n_i)}{0}!\right)=1$.

The boundary decomposes uniquely across levels because the representation of $N$ is unique and each reduction affects exactly one summand without overlap between different $i$. ∎
