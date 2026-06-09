---
title: "CF 1835F - Good Graph"
description: "Investigate the \"improved\" KS test suggested in the answer to exercise 6. Let $X1, X2, ldots, Xn$ be independent observations drawn from a continuous distribution function $F(x)$."
date: "2026-06-09T06:49:51+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dfs-and-similar", "graph-matchings", "graphs", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1835
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 880 (Div. 1)"
rating: 3500
weight: 1835
solve_time_s: 64
verified: false
draft: false
---

[CF 1835F - Good Graph](https://codeforces.com/problemset/problem/1835/F)

**Rating:** 3500  
**Tags:** bitmasks, dfs and similar, graph matchings, graphs, implementation  
**Solve time:** 1m 4s  
**Verified:** no  

## Solution
## Exercise 3.3.1.22 [_HM46_]

Investigate the "improved" KS test suggested in the answer to exercise 6.

## Setup

Let $X_1, X_2, \ldots, X_n$ be independent observations drawn from a continuous distribution function $F(x)$. Denote by $F_n(x)$ the empirical distribution function:

$F_n(x) = \frac{1}{n}\sum_{i=1}^{n} \mathbf{1}_{\{X_i \le x\}}.$

The classical Kolmogorov-Smirnov statistics are

$K_n^+ = \sup_x \bigl(F_n(x) - F(x)\bigr), \qquad K_n^- = \sup_x \bigl(F(x) - F_n(x)\bigr),$

and the two-sided statistic is

$K_n = \max(K_n^+, K_n^-).$

The "improved" KS test referred to in exercise 6 modifies the statistic to account for the nonuniform variance of $F_n(x)$ at different values of $F(x)$, analogous to the weighting used in the chi-square statistic in equation (4). Specifically, define

$K_n^\ast = \sup_{x} \frac{|F_n(x) - F(x)|}{\sqrt{F(x)(1 - F(x))}}, \eqno(22.1)$

so that deviations near the boundaries $F(x) \approx 0$ or $F(x) \approx 1$ are magnified in proportion to their standard deviation under the binomial approximation.

We are asked to investigate the distribution of $K_n^\ast$ and its practical effect compared with the classical KS test.

## Solution

Consider first the variance structure of the classical empirical distribution. For each $x$, $n F_n(x)$ has a binomial distribution with parameters $n$ and $F(x)$. Hence,

$\operatorname{Var}(F_n(x)) = \frac{F(x)(1 - F(x))}{n}.$

The classical KS statistic $K_n$ treats all deviations equally, whereas the improved statistic $K_n^\ast$ scales each deviation by its standard deviation:

$\frac{F_n(x) - F(x)}{\sqrt{F(x)(1 - F(x)) / n}} = \sqrt{n}\,\frac{F_n(x) - F(x)}{\sqrt{F(x)(1 - F(x))}}.$

This transformation stabilizes the variance across $x \in [0,1]$. Consequently, the distribution of $\sqrt{n} K_n^\ast$ depends asymptotically only on the standardized Brownian bridge process $B(t)/\sqrt{t(1-t)}$, where $B(t)$ is a standard Brownian bridge on $[0,1]$. By the argument in Section 3.3.1, the classical KS statistic converges in distribution:

$\Pr\bigl(\sqrt{n} K_n \le x\bigr) \to 1 - 2\sum_{k=1}^{\infty}(-1)^{k-1} e^{-2 k^2 x^2}.$

For the improved statistic, the analogous asymptotic behavior is

$\Pr\bigl(\sqrt{n} K_n^\ast \le x\bigr) \to \Pr\left(\sup_{0 < t < 1} \frac{|B(t)|}{\sqrt{t(1-t)}} \le x\right).$

Let us analyze this process. Let $t = \sin^2 \theta$, $0 < \theta < \pi/2$. Then

$\frac{dt}{d\theta} = 2 \sin \theta \cos \theta = \sin 2\theta, \qquad t(1-t) = \sin^2 \theta \cos^2 \theta = \frac{\sin^2 2\theta}{4}.$

Define $Z(\theta) = 2 B(\sin^2 \theta) / \sin 2\theta$, so that $K_n^\ast = \sup_\theta |Z(\theta)|$. Then $Z(\theta)$ is a Gaussian process with mean $0$ and unit variance at each $\theta$, because

$\operatorname{Var}\bigl(B(t)/(t(1-t))^{1/2}\bigr) = \frac{t(1-t)}{t(1-t)} = 1.$

However, $Z(\theta)$ exhibits strong correlations for nearby $\theta$. Classical techniques for extreme values of Gaussian processes (Rice formula, or Pickands’ constants) can be applied. In practice, for moderate $n$, the critical values of $K_n^\ast$ are slightly larger than those of $K_n$, reflecting the increased weighting of the tails.

To illustrate, suppose $n = 100$ and $F(x)$ is uniform on $[0,1]$. For a given realization of $F_n(x)$, the maximal deviation near $x = 0.01$ and $x = 0.99$ is divided by $\sqrt{0.01\cdot 0.99} \approx 0.0995$, thereby magnifying small absolute deviations by a factor of about $10$. In contrast, near $x = 0.5$, the weighting factor is $1/\sqrt{0.25} = 2$, which is only twice the classical deviation. Therefore, $K_n^\ast$ is more sensitive to deviations near the boundaries of $F(x)$, which are precisely where classical KS is least sensitive due to smaller binomial variance.

We can also approximate $\Pr(\sqrt{n} K_n^\ast \le x)$ using Monte Carlo simulation. Let $X_1, \ldots, X_n$ be independent draws from $F$, compute $F_n$, then calculate $K_n^\ast$. Repeating this procedure $M$ times yields the empirical distribution of $\sqrt{n} K_n^\ast$ and allows estimation of critical values at standard significance levels.

## Verification

The transformation $F_n(x) \mapsto (F_n(x) - F(x))/\sqrt{F(x)(1-F(x))}$ correctly standardizes the binomial variance. The mapping $t = \sin^2 \theta$ ensures that the variance is constant for all $\theta \in (0,\pi/2)$. The limiting Gaussian process argument follows the classical Donsker theorem for the empirical process, and the supremum over a standardized bridge is a standard method for obtaining weighted KS statistics. The sensitivity near $x \approx 0$ or $x \approx 1$ is quantitatively consistent with the binomial variance, which is smaller at the boundaries, and thus the weighting increases the effective test power for detecting deviations in the tails.

## Notes

Alternative weighting functions could be used, for example $\bigl(F(x)(1-F(x))\bigr)^{-\alpha}$ for $0 < \alpha < 1$, providing intermediate sensitivity between classical KS ($\alpha = 0$) and the fully improved KS ($\alpha = 1/2$). Multivariate analogues can be defined by replacing the Brownian bridge $B(t)$ with the corresponding $s$-dimensional Kiefer process. The argument generalizes to any continuous $F$, provided $F$ is strictly increasing and differentiable, ensuring the variance-stabilizing transformation is well defined.

This completes the proof.

∎
