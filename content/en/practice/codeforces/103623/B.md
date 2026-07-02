---
title: "CF 103623B - Unusual Sorting"
description: "Let $omega = e^{2pi i/3}$, so $omega^3 = 1$ and $1 + omega + omega^2 = 0$. Write each nonnegative integer $k$ in base $3$ as $$k = sum{j ge 0} kj 3^j, quad kj in {0,1,2}."
date: "2026-07-02T22:44:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103623
codeforces_index: "B"
codeforces_contest_name: "\u0418\u043d\u0434\u0438\u0432\u0438\u0434\u0443\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0438 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2022"
rating: 0
weight: 103623
solve_time_s: 133
verified: false
draft: false
---

[CF 103623B - Unusual Sorting](https://codeforces.com/problemset/problem/103623/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 13s  
**Verified:** no  

## Solution
## Solution

Let $\omega = e^{2\pi i/3}$, so $\omega^3 = 1$ and $1 + \omega + \omega^2 = 0$. Write each nonnegative integer $k$ in base $3$ as

$$k = \sum_{j \ge 0} k_j 3^j, \quad k_j \in \{0,1,2\}.$$

For $x \in [0,1)$ define its ternary expansion

$$x = \sum_{j \ge 1} x_j 3^{-j}, \quad x_j \in \{0,1,2\},$$

choosing the representation that is not eventually $2$.

Define the $j$th ternary digit function

$$\tau_j(x) = \lfloor 3^j x \rfloor \bmod 3,$$

so $\tau_j(x) = x_j$ and each $\tau_j(x)$ depends only on the triadic interval of length $3^{-j}$ containing $x$.

For each $k \ge 0$, define the ternary Walsh function

$$w_k(x) = \omega^{\sum_{j \ge 0} k_j \tau_{j+1}(x)}.$$

This expression is well defined because only finitely many digits $k_j$ are nonzero, so the exponent is a finite sum in $\mathbb{Z}/3\mathbb{Z}$.

For fixed $j$, the function $\tau_j(x)$ is constant on each interval

$$\left[\frac{m}{3^j}, \frac{m+1}{3^j}\right), \quad 0 \le m < 3^j,$$

hence each $w_k(x)$ is constant on triadic intervals of length $3^{-m}$, where $m = 1 + \max{j : k_j \ne 0}$.

If $k$ and $\ell$ have base-$3$ expansions $k_j$ and $\ell_j$, then

$$w_k(x)\, w_\ell(x) = \omega^{\sum_{j \ge 0} (k_j + \ell_j)\tau_{j+1}(x)}
= w_{k \oplus_3 \ell}(x),$$

where $\oplus_3$ denotes digitwise addition modulo $3$. This identifies the family ${w_k}$ with the characters of the additive group $\bigoplus_{j \ge 0} \mathbb{Z}/3\mathbb{Z}$ evaluated on the coordinate functions $\tau_j(x)$.

Orthogonality follows from independence of ternary digits. For $k \ne 0$, choose $m$ such that $k_m \ne 0$. Partition $[0,1)$ into intervals of length $3^{-m}$, on each of which all digits $\tau_j(x)$ for $j \le m$ are fixed except $\tau_m(x)$, which takes values $0,1,2$ equally over subintervals of length $3^{-(m+1)}$. On such a subinterval the function $w_k(x)$ acquires the factor $\omega^{k_m \tau_m(x)}$ while all other factors remain constant. Summing over the three values of $\tau_m(x)$ gives

$$1 + \omega^{k_m} + \omega^{2k_m} = 0,$$

since $k_m \in {1,2}$ implies $\omega^{k_m}$ is a primitive cube root of unity. Therefore

$$\int_0^1 w_k(x)\,dx = 0 \quad \text{for } k \ne 0.$$

For $k = \ell$, the same digitwise decomposition yields $w_k(x)\overline{w_k(x)} = 1$, hence

$$\int_0^1 w_k(x)\overline{w_k(x)}\,dx = 1.$$

For $k \ne \ell$, apply the same argument to $w_k(x)\overline{w_\ell(x)} = w_{k \oplus_3 (-\ell)}(x)$ in digit arithmetic modulo $3$, which is nonzero in some digit position, giving cancellation in exactly the same manner. Hence

$$\int_0^1 w_k(x)\overline{w_\ell(x)}\,dx = 0 \quad (k \ne \ell).$$

The functions ${w_k(x)}_{k \ge 0}$ form an orthonormal system in $L^2[0,1]$, and each function is a character determined by base-$3$ digits exactly as Walsh functions correspond to base-$2$ characters. This completes the ternary generalization of the Walsh system. ∎
