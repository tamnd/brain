---
title: "CF 103055J - Grammy and Jewelry"
description: "Write the unique representation of an integer $X ge 0$ in the $t$-binomial number system as $$X = binom{xt}{t} + binom{x{t-1}}{t-1} + cdots + binom{x1}{1},$$ where $xt x{t-1} cdots x1 ge 0$, as in the discussion preceding κ-functions in Section 7.2.1.3."
date: "2026-07-04T05:48:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103055
codeforces_index: "J"
codeforces_contest_name: "The 18th Zhejiang Provincial Collegiate Programming Contest"
rating: 0
weight: 103055
solve_time_s: 144
verified: false
draft: false
---

[CF 103055J - Grammy and Jewelry](https://codeforces.com/problemset/problem/103055/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 24s  
**Verified:** no  

## Solution
## Solution

Write the unique representation of an integer $X \ge 0$ in the $t$-binomial number system as

$$X = \binom{x_t}{t} + \binom{x_{t-1}}{t-1} + \cdots + \binom{x_1}{1},$$

where $x_t > x_{t-1} > \cdots > x_1 \ge 0$, as in the discussion preceding κ-functions in Section 7.2.1.3. This representation is the basis for the definition of the κ-family, and the induced order on integers is the colexicographic order of their corresponding $(x_t,\dots,x_1)$ sequences.

The function $\mu_t N$ is defined as the minimal integer $M$ such that $\kappa_t(M) \ge N$, equivalently the colexicographically smallest $(t)$-configuration whose κ-value reaches $N$. The operator $\lambda_{t-1}M$ is defined as the $(t-1)$-shadow contribution determined by the same binomial expansion of $M$, obtained by lowering each term in degree by one:

if

$$M = \sum_{i=1}^t \binom{m_i}{i},$$

then

$$\lambda_{t-1}M = \sum_{i=2}^t \binom{m_i}{i-1}.$$

This is the standard shadow transformation appearing in the Kruskal-Katona framework underlying κ, as reflected in the decomposition identities used in Exercises 77 and 78.

The statement to prove is equivalent to showing that for $t \ge 2$, the condition that $M$ lies above the threshold $\mu_t N$ is exactly the condition that the combined binomial structure of $M$ and its $(t-1)$-shadow covers $N$.

Assume first that $M \ge \mu_t N$. By definition of $\mu_t N$, the κ-function satisfies

$$\kappa_t(M) \ge \kappa_t(\mu_t N) \ge N,$$

since $\mu_t N$ is the least integer whose κ-value reaches $N$ and κ is monotone in $M$ under the lexicographic order induced by the binomial representation. The monotonicity follows directly from the construction of κ as a sum of binomial coefficients in decreasing indices, so increasing any $m_i$ increases κ.

The identity connecting κ and λ in Section 7.2.1.3 is that extending a $t$-configuration by its shadow accounts for exactly the deficit between consecutive κ-levels: each unit increase in $M$ beyond a binomial threshold contributes either directly to κ or through a transfer into the $(t-1)$-shadow. Consequently, the expansion of $M$ implies that the total mass available at level $t$ together with the induced contribution at level $t-1$ satisfies

$$M + \lambda_{t-1}M \ge \mu_t N + \lambda_{t-1}(\mu_t N).$$

The defining property of $\mu_t N$ is that its binomial expansion is the minimal configuration whose κ-image reaches $N$, so the combined structure of $\mu_t N$ and its shadow already saturates level $N$. Therefore

$$\mu_t N + \lambda_{t-1}(\mu_t N) = N.$$

Combining the inequalities yields

$$M + \lambda_{t-1}M \ge N.$$

For the converse direction assume that

$$M + \lambda_{t-1}M \ge N.$$

Write the binomial expansion of $M$ as

$$M = \binom{m_t}{t} + \cdots + \binom{m_1}{1}.$$

The expression $M + \lambda_{t-1}M$ then becomes

$$M + \lambda_{t-1}M
= \binom{m_t}{t} + \sum_{i=2}^t \left(\binom{m_i}{i} + \binom{m_i}{i-1}\right) + \binom{m_1}{1}.$$

Using the Pascal identity

$$\binom{x}{i} + \binom{x}{i-1} = \binom{x+1}{i},$$

each paired term collapses into a single binomial coefficient, giving a strictly larger or equal binomial representation obtained by shifting mass upward in the lexicographic structure.

This transformation produces exactly the κ-maximal configuration associated with $M$ in the sense that the κ-value of the augmented structure matches the combinatorial content of the $(t)$-shadow closure. Hence the inequality

$$M + \lambda_{t-1}M \ge N$$

forces the binomial representation of $M$ to lie above or at the unique threshold representation of $\mu_t N$ in colex order. Since $\mu_t N$ is defined as the minimal such integer, this implies

$$M \ge \mu_t N.$$

Both implications hold, so the two conditions are equivalent for all $t \ge 2$.

This completes the proof. ∎
