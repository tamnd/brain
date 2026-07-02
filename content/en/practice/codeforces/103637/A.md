---
title: "CF 103637A - Agile permutation"
description: "Let $x in [0,1)$ and write its dyadic expansion $$x = 0.x1 x2 x3 ldots,qquad xj in {0,1}.$$ Let $rj(x)$ denote the $j$-th Rademacher function, $$rj(x) = (-1)^{xj}."
date: "2026-07-02T22:20:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103637
codeforces_index: "A"
codeforces_contest_name: "2019-2020 10th BSUIR Open Programming Championship. Semifinal"
rating: 0
weight: 103637
solve_time_s: 133
verified: false
draft: false
---

[CF 103637A - Agile permutation](https://codeforces.com/problemset/problem/103637/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 13s  
**Verified:** no  

## Solution
## Solution

Let $x \in [0,1)$ and write its dyadic expansion

$$x = 0.x_1 x_2 x_3 \ldots,\qquad x_j \in \{0,1\}.$$

Let $r_j(x)$ denote the $j$-th Rademacher function,

$$r_j(x) = (-1)^{x_j}.$$

Let $k$ have binary expansion

$$k = (b_m \cdots b_1 b_0)_2,\qquad b_j \in \{0,1\},$$

and let the Walsh function be defined by

$$w_k(x) = \prod_{j \ge 0} r_{j+1}(x)^{b_j}.$$

### Transformation under $x \mapsto 1-x$

For dyadic expansions, replacing $x$ by $1-x$ flips every binary digit in the sense that each Rademacher function changes sign:

$$r_j(1-x) = -r_j(x),$$

since the $j$-th binary digit is complemented under $x \mapsto 1-x$ in the dyadic system, hence $(-1)^{(1-x_j)} = -(-1)^{x_j}$.

Applying this to $w_k$,

$$w_k(1-x)
= \prod_{j \ge 0} r_{j+1}(1-x)^{b_j}
= \prod_{j \ge 0} (-r_{j+1}(x))^{b_j}.$$

Each factor contributes a sign $-1$ exactly when $b_j = 1$, hence

$$w_k(1-x)
= (-1)^{\sum_{j \ge 0} b_j} \prod_{j \ge 0} r_{j+1}(x)^{b_j}.$$

Let $\nu(k) = \sum_{j \ge 0} b_j$ be the number of $1$-bits in the binary expansion of $k$. Then

$$w_k(1-x) = (-1)^{\nu(k)} w_k(x).$$

### Comparison with the claimed identity

The statement to test is

$$w_k(-x) = (-1)^k w_k(x).$$

Since Walsh functions are typically defined on $[0,1)$ and extended periodically, $-x$ corresponds to $1-x$ in this setting. The derived identity shows that the correct exponent depends on the Hamming weight $\nu(k)$, not on $k$ itself.

To disprove the claim, take $k=2$. Then $k=(10)_2$, so $\nu(k)=1$. The identity above gives

$$w_2(1-x) = -w_2(x),$$

while

$$(-1)^k = (-1)^2 = 1.$$

Hence

$$w_2(1-x) \ne (-1)^k w_2(x)$$

for all $x$ where $w_2(x) \ne 0$.

The claimed identity fails.

$$\boxed{\text{False}}$$
