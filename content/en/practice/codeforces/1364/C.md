---
title: "CF 1364C - Ehab and Prefix MEXs"
description: "The exercise asks us to investigate approximate polynomial greatest common divisors (gcds) and the behavior of Euclid's algorithm when the polynomial coefficients are floating-point numbers."
date: "2026-06-11T12:24:37+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1364
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 649 (Div. 2)"
rating: 1600
weight: 1364
solve_time_s: 175
verified: false
draft: false
---

[CF 1364C - Ehab and Prefix MEXs](https://codeforces.com/problemset/problem/1364/C)

**Rating:** 1600  
**Tags:** brute force, constructive algorithms, greedy  
**Solve time:** 2m 55s  
**Verified:** no  

## Solution
## Corrected Solution for TAOCP 4.6.1.20

The exercise asks us to investigate _approximate_ polynomial greatest common divisors (gcds) and the behavior of Euclid's algorithm when the polynomial coefficients are floating-point numbers. This is a conceptual and numerical analysis question rather than a programming or combinatorial task.

## Problem Understanding

We consider two polynomials

$$f(x) = a_n x^n + a_{n-1} x^{n-1} + \dots + a_0, \quad g(x) = b_m x^m + b_{m-1} x^{m-1} + \dots + b_0$$

with coefficients $a_i, b_j \in \mathbb{R}$ (floating-point numbers). The classical Euclidean algorithm computes the exact gcd $d(x)$ via repeated polynomial division:

$$f(x) = q_1(x) g(x) + r_1(x), \quad g(x) = q_2(x) r_1(x) + r_2(x), \dots$$

until the remainder is zero, at which point the last nonzero remainder is the gcd. Over exact arithmetic, this is correct. Over floating-point coefficients, rounding errors can accumulate in the remainders and quotient computations, so the algorithm may yield a remainder that is numerically nonzero even when there is an approximate common factor.

The output of Euclid's algorithm in floating-point arithmetic is sensitive to small perturbations in coefficients. Two polynomials that are theoretically divisible may appear coprime numerically if the coefficients are perturbed by machine epsilon. This is why the notion of an _approximate gcd_ arises: we seek a polynomial $d(x)$ of maximal degree such that there exist small perturbations $\tilde{f}(x), \tilde{g}(x)$ of the original polynomials satisfying $d(x) \mid \tilde{f}(x)$ and $d(x) \mid \tilde{g}(x)$.

## Numerical Behavior of Euclid's Algorithm

Let us examine the sources of numerical error:

1. **Coefficient growth and cancellation:** Each step divides polynomials and subtracts multiples. If $f(x)$ and $g(x)$ have coefficients of widely differing magnitudes, the subtraction $f(x) - q(x) g(x)$ can cause significant cancellation, amplifying relative error.
2. **Floating-point rounding:** Standard double precision arithmetic has about $16$ decimal digits of accuracy. Each division introduces round-off error proportional to the magnitude of the coefficients. Errors accumulate linearly with the number of Euclidean steps, but they can be amplified if the polynomials have ill-conditioned roots.
3. **Ill-conditioned polynomials:** If $f(x)$ and $g(x)$ share a common factor with small leading coefficients or roots very close together, the remainder can have coefficients that are comparable in magnitude to the round-off error. The computed "remainder" may appear nonzero numerically even if the exact remainder is zero.

## Approximate Polynomial GCD Methods

Because Euclid's algorithm is numerically unstable on floating-point polynomials, the following approaches are used in practice:

1. **Subresultant PRS with scaling:** Subresultant polynomial remainder sequences normalize the coefficients to reduce growth. This improves numerical behavior but does not fully solve rounding issues.
2. **Singular value decomposition (SVD):** Represent the polynomial coefficients as a structured Sylvester matrix and compute its singular values. The smallest singular values indicate approximate common factors. The rank-deficiency of the Sylvester matrix corresponds to the degree of the approximate gcd.
3. **Total least squares and perturbation:** The polynomials are slightly perturbed within the bounds of numerical precision to maximize the degree of the gcd. Algorithms based on structured total least squares find $\tilde{f}(x)$ and $\tilde{g}(x)$ close to $f(x)$ and $g(x)$ such that $\gcd(\tilde{f}, \tilde{g})$ has maximal degree.

## Observations

- **Euclid fails for approximate gcds:** Even a single coefficient perturbation can reduce the degree of the computed gcd. For example, consider $f(x) = (x-1)(x-1.00001)$ and $g(x) = (x-1)(x-1.00002)$. Exact arithmetic would give $\gcd(f,g) = x-1$. Floating-point Euclid may produce a remainder with small but nonzero coefficients, causing it to report gcd of degree zero.
- **Stability depends on normalization:** Scaling polynomials so that leading coefficients are 1 or using orthogonal polynomial bases (like Chebyshev) reduces error propagation.
- **Degree of approximate gcd:** The correct notion is not the algebraic gcd but the maximal-degree polynomial that divides small perturbations of the input polynomials.

## Conclusion

The key facts about approximate polynomial gcds and Euclid's algorithm with floating-point coefficients are:

1. Euclid's algorithm is exact over a field with exact arithmetic, but floating-point arithmetic introduces rounding errors that accumulate, potentially giving incorrect gcd degrees.
2. Small perturbations in coefficients can make polynomials that share a factor appear coprime numerically.
3. Approximate gcd methods rely on analyzing the Sylvester matrix, using SVD, or total least squares to detect common factors robustly.
4. Any practical computation of a polynomial gcd with floating-point coefficients must account for numerical error; one cannot naively apply standard Euclid's algorithm and expect exact results.
5. Algorithmically, stabilization techniques like subresultant sequences, coefficient scaling, and matrix-based SVD approaches are essential to accurately identify approximate gcds.

This completes the discussion of approximate polynomial gcds and the limitations of Euclid's algorithm in floating-point arithmetic.
