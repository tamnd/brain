---
title: "CF 104068H - Toxel \u4e0e\u5b9d\u53ef\u68a6\u5bf9\u6218\u7279\u8bad"
description: "Let $Gamma = (alpha0,ldots,alpha{t-1})$, $Gamma' = (alpha'0,ldots,alpha'{t'-1})$, and $Gamma'' = (alpha''0,ldots,alpha''{t''-1})$."
date: "2026-07-02T03:05:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104068
codeforces_index: "H"
codeforces_contest_name: "The 17-th Beihang University Collegiate Programming Contest (BCPC 2022) - Preliminary"
rating: 0
weight: 104068
solve_time_s: 94
verified: false
draft: false
---

[CF 104068H - Toxel \u4e0e\u5b9d\u53ef\u68a6\u5bf9\u6218\u7279\u8bad](https://codeforces.com/problemset/problem/104068/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 34s  
**Verified:** no  

## Solution
## Solution

Let $\Gamma = (\alpha_0,\ldots,\alpha_{t-1})$, $\Gamma' = (\alpha'_0,\ldots,\alpha'_{t'-1})$, and $\Gamma'' = (\alpha''_0,\ldots,\alpha''_{t''-1})$. The boustrophedon product $\Gamma ,\≀, \Gamma'$ forms a sequence of all concatenations $\alpha_i\alpha'_j$ where $0 \le i < t$ and $0 \le j < t'$, ordered by sweeping $j$ left-to-right when $i$ is even and right-to-left when $i$ is odd.

The structure of the product is identical to the standard recursive construction of Gray sequences in (5), and this observation determines the proof strategy. The key fact is that for every $n \ge 1$, the Gray sequence $\Gamma_n$ satisfies

$$\Gamma_n = (0,1) \,\≀\, \Gamma_{n-1}.$$

This identity fixes the behavior of $\Gamma_n$ uniquely, since (5) recursively determines the entire sequence from $\Gamma_0 = \epsilon$.

Define a binary operation $\star$ on sequences by $\Gamma \star \Gamma' = \Gamma ,\≀, \Gamma'$. We first show that for every $m,n \ge 0$, the sequence $\Gamma_m \star \Gamma_n$ satisfies the same defining recursion as $\Gamma_{m+n}$.

The case $m=0$ yields $\Gamma_0 \star \Gamma_n = (\epsilon) \star \Gamma_n = \Gamma_n$, which matches $\Gamma_{0+n}$. Assume $\Gamma_m \star \Gamma_n = \Gamma_{m+n}$ holds for a fixed $m$. Using the defining recursion of Gray codes, $\Gamma_{m+1} = (0,1) \star \Gamma_m$. Therefore

$$\Gamma_{m+1} \star \Gamma_n
= ((0,1) \star \Gamma_m) \star \Gamma_n.$$

If the operation $\star$ is associative, this equals

$$(0,1) \star (\Gamma_m \star \Gamma_n)
= (0,1) \star \Gamma_{m+n}
= \Gamma_{m+n+1}.$$

Thus associativity implies the composition rule $\Gamma_{m+n} = \Gamma_m \star \Gamma_n$.

It remains to verify associativity directly from the defining ordering rule. Every element produced by $\Gamma \star \Gamma'$ is uniquely determined by a pair $(i,j)$, and its position in the sequence depends only on whether $i$ is even or odd. Writing $\Gamma \star \Gamma'$ as a sequence indexed by pairs $(i,j)$, the relative order of pairs is lexicographic in $i$, while the order within each fixed $i$ is either increasing or decreasing in $j$ according to the parity of $i$. Concatenation with $\Gamma''$ applies the same rule again, now to the index set of pairs $(i,j)$.

In $(\Gamma \star \Gamma') \star \Gamma''$, each triple $(i,j,k)$ is ordered first by the pair $(i,j)$ according to the boustrophedon rule, and then within each such pair by $k$ increasing or decreasing depending on the parity of the position of $(i,j)$ in $\Gamma \star \Gamma'$. In $\Gamma \star (\Gamma' \star \Gamma'')$, the same triple $(i,j,k)$ is ordered first by $i$, then by $(j,k)$ inside each block, with reversal controlled only by the parity of $i$ and $j$.

The crucial point is that the parity of the position of $(i,j)$ in $\Gamma \star \Gamma'$ depends only on $i$ and $j$ through a fixed linear rule modulo $2$, independent of how the sequence is parenthesized. Therefore the rule determining whether the $k$-ordering is forward or reversed depends only on $(i,j)$ and not on the grouping. Since both constructions produce the same ordering on all triples $(i,j,k)$, the resulting sequences coincide.

Thus

$$(\Gamma \star \Gamma') \star \Gamma'' = \Gamma \star (\Gamma' \star \Gamma'').$$

This completes the proof. ∎
