---
title: "CF 1834F - Typewriter"
description: "The solution correctly identifies what the “improved KS test” is trying to do: it replaces the unweighted empirical process by a variance-stabilized version, dividing by the binomial standard deviation $sqrt{F(x)(1-F(x))}$."
date: "2026-06-09T06:53:23+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 1834
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 879 (Div. 2)"
rating: 2500
weight: 1834
solve_time_s: 93
verified: false
draft: false
---

[CF 1834F - Typewriter](https://codeforces.com/problemset/problem/1834/F)

**Rating:** 2500  
**Tags:** brute force, math  
**Solve time:** 1m 33s  
**Verified:** no  

## Solution
## Correctness

The solution correctly identifies what the “improved KS test” is trying to do: it replaces the unweighted empirical process by a variance-stabilized version, dividing by the binomial standard deviation $\sqrt{F(x)(1-F(x))}$. It also correctly connects the empirical process to a Brownian bridge limit via Donsker’s theorem and reformulates the asymptotic statistic as a supremum of a transformed Gaussian process.

The main structural idea, namely that

$$\sqrt{n}(F_n(x)-F(x)) \Rightarrow B(F(x)),$$

and therefore

$$\sqrt{n}K_n^\ast \Rightarrow \sup_{0<t<1} \frac{|B(t)|}{\sqrt{t(1-t)}},$$

is correct and is the essential answer to what the exercise asks.

The qualitative discussion that this weighting increases sensitivity near the boundaries is also correct and consistent with the variance structure.

However, the solution stops at a fairly superficial level of analysis and does not properly investigate the distributional properties of the limiting object or the implications for the “improved test.” In particular, it does not determine whether the supremum is finite, how it behaves near $t=0,1$, or whether the transformation leads to a nondegenerate limit law usable for testing. These are central to the “investigate” part of the question.

## Gaps and Errors

### 1. Critical issue: boundary behavior of the transformed process

The process

$$\frac{B(t)}{\sqrt{t(1-t)}}$$

is not well-behaved at $t \to 0$ or $t \to 1$. The solution implicitly assumes it is a standard Gaussian process on $(0,1)$ with manageable supremum behavior, but does not address that:

- $B(t) \sim \mathcal{N}(0,t(1-t))$ implies normalization is fine pointwise,
- but as $t \to 0$, the scaling behaves like $B(t)/\sqrt{t} \sim \mathcal{N}(0,1)$ in distribution, while the process becomes highly irregular,
- the supremum over $(0,1)$ requires careful treatment of endpoint behavior, since fluctuations accumulate near the boundaries.

This is a **critical gap**, because it affects whether $K_n^\ast$ has a proper limiting distribution at all in the naive form presented.

### 2. Justification gap: change of variables to $\theta$

The substitution $t=\sin^2\theta$ is correct algebraically, but the claim that this “ensures constant variance” and produces a well-behaved Gaussian process is misleading.

While the marginal variance becomes 1, the transformation does not regularize the process in a way that simplifies extreme-value analysis. The dependence structure remains singular near the endpoints. This step is presented as structurally simplifying the problem but does not actually resolve the core difficulty.

### 3. Missing investigation of whether the statistic is useful

The exercise asks to “investigate the improved KS test,” which in TAOCP typically means:

- does it yield a usable limiting distribution,
- does it improve power,
- does it preserve distribution-free property,
- does it introduce pathologies.

The solution does not address:

- whether $\sup |B(t)|/\sqrt{t(1-t)}$ is finite almost surely,
- whether its distribution is tractable or even well-defined without truncation,
- whether the statistic remains distribution-free under general $F$ (it does, but must be argued carefully).

This is a **major completeness gap**.

### 4. Unsupported claims about “standard techniques”

The invocation of Rice formula and Pickands constants is not developed or justified. While not necessary for a full solution, it is used to suggest analytic tractability without actually deriving anything. This is a **justification gap** rather than a structural flaw.

### 5. Minor issue: overstatement about “unit variance implies standard process”

The statement that the transformed process has unit variance at each point is correct but insufficient to characterize the process as “standardized.” Gaussian processes are not determined by pointwise variance alone; covariance structure is essential. This is slightly misleading in context.

## Summary

The solution correctly identifies the limiting form of the improved KS statistic and connects it to a variance-normalized Brownian bridge. However, it does not properly analyze the key difficulty introduced by the weighting near the boundaries, nor does it fully investigate whether the resulting supremum defines a well-behaved or practically useful test statistic. The treatment of the transformed process is therefore incomplete at the level expected by the exercise.

VERDICT: FAIL - it does not properly handle the boundary behavior and resulting well-posedness of the weighted KS statistic.
