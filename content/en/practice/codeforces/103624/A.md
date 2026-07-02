---
title: "CF 103624A - Queen Anne's Revenge"
description: "Let $omega = e^{2pi i/3}$, so $omega^3 = 1$ and $1 + omega + omega^2 = 0$. Write each nonnegative integer $k$ in base $3$ as $$k = sum{j ge 0} kj 3^j, quad kj in {0,1,2}."
date: "2026-07-02T22:42:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103624
codeforces_index: "A"
codeforces_contest_name: "UTPC Contest 03-25-22 Div. 2 (Beginner)"
rating: 0
weight: 103624
solve_time_s: 127
verified: false
draft: false
---

[CF 103624A - Queen Anne's Revenge](https://codeforces.com/problemset/problem/103624/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 7s  
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
