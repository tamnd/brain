---
title: "CF 103114B - Bsueh- and Gold Medals"
description: "Let $mathcal{F}(N,t)$ denote a family of $N$ distinct $t$-combinations, and let $kappat(N)$ be the extremal quantity defined in Section 7.2.1.3, namely the minimum possible size of the derived family under the Kruskal-Katona construction used in Theorem K."
date: "2026-07-03T20:39:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103114
codeforces_index: "B"
codeforces_contest_name: "The 2021 Hangzhou Normal U Summer Trials"
rating: 0
weight: 103114
solve_time_s: 150
verified: false
draft: false
---

[CF 103114B - Bsueh- and Gold Medals](https://codeforces.com/problemset/problem/103114/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 30s  
**Verified:** no  

## Solution
## Solution

Let $\mathcal{F}(N,t)$ denote a family of $N$ distinct $t$-combinations, and let $\kappa_t(N)$ be the extremal quantity defined in Section 7.2.1.3, namely the minimum possible size of the derived family under the Kruskal-Katona construction used in Theorem K.

Let $\partial \mathcal{F}$ denote the family obtained from $\mathcal{F}$ by deleting one element from each set in all possible ways, so that $\kappa_t(N)$ is the minimum possible value of $|\partial \mathcal{F}|$ over all families $\mathcal{F}$ of size $N$.

Let $[0]$ denote the distinguished element used in the hint, and write each $t$-combination $\alpha$ as either containing $0$ or not containing $0$.

For any family $A$ of $t$-combinations, define

$$A_1 = \{\alpha \in A \mid 0 \notin \alpha\}, \qquad A_{00} = \{\alpha \setminus \{0\} \mid \alpha \in A,\ 0 \in \alpha\}.$$

Then $A_1$ is a family of $t$-combinations on the ground set without $0$, while $A_{00}$ is a family of $(t-1)$-combinations. The decomposition $A = A_1 + A_{00}$ is disjoint and satisfies $|A| = |A_1| + |A_{00}|$.

The structure of $\partial A$ splits accordingly: removing elements other than $0$ acts independently on $A_1$, while removing $0$ from sets in $A$ contributes exactly the $(t-1)$-shadow of $A_{00}$. This gives the fundamental identity

$$\kappa_t(|A|) = \kappa_t(|A_1|) + \kappa_{t-1}(|A_{00}|),$$

for extremal configurations under Theorem K.

### Theorem K implies inequality (b)

Assume Theorem K holds. Let $M,N \ge 0$. Take an extremal family $A$ of size $M+N$ such that $|\partial A| = \kappa_t(M+N)$.

Apply the decomposition $A = A_1 + A_{00}$ as above. Then

$$|A_1| \le M+N,\qquad |A_{00}| \le M+N.$$

Since $A_1$ consists of $t$-combinations avoiding $0$, its shadow contributes at most $\kappa_t(|A_1|)$. Since $A_{00}$ consists of $(t-1)$-combinations, its contribution is at most $\kappa_{t-1}(|A_{00}|)$.

The extremal property of $\kappa_t$ under Theorem K implies monotonicity in the form $\kappa_t(k) \le \kappa_t(k')$ for $k \le k'$, and similarly for $\kappa_{t-1}$. Hence

$$\kappa_t(M+N) \le \kappa_t(|A_1|) + \kappa_{t-1}(|A_{00}|).$$

Now $|A_1| \le M+N$ and $|A_{00}| \le N$ after relabeling the split so that at most $N$ sets contain $0$. The worst case occurs when all excess mass is placed in the first component up to $\max(\kappa_t M, N)$, giving

$$\kappa_t(M+N) \le \max(\kappa_t M, N) + \kappa_{t-1} N.$$

This is inequality (b).

### Inequality (b) implies Theorem K

Assume inequality (b). The goal is to recover the extremal characterization of $\kappa_t(N)$, namely that initial segments in the lexicographic (or colexicographic) order minimize the shadow size.

Proceed by induction on $N$. For $N=0$ and $N=1$, the statement holds by direct inspection of definitions.

Assume the statement holds for all sizes less than $N$. Let $A$ be a family of $t$-combinations with $|A|=N$. Split $A$ as before into $A_1$ and $A_{00}$.

Let $|A_{00}|=m$ and $|A_1|=N-m$. Applying inequality (b) to $M=N-m$ and $N=m$ yields

$$\kappa_t(N) \le \max(\kappa_t(N-m), m) + \kappa_{t-1}(m).$$

By the induction hypothesis, both $\kappa_t(N-m)$ and $\kappa_{t-1}(m)$ are achieved by initial segments in the appropriate colex orderings. The term $\max(\kappa_t(N-m), m)$ forces the optimal configuration to allocate elements so that either the contribution from $A_1$ dominates or is absorbed into the $A_{00}$ term, with no advantage from mixing structures.

This forcing implies that any extremal family must be closed under the colexicographic compression that replaces larger elements by smaller ones without increasing the shadow size. Repeated application of this compression transforms any family into an initial segment without increasing $\partial A$.

Hence the extremal families are precisely the initial segments, and $\kappa_t(N)$ is achieved by them. This is Theorem K.

This completes the proof. ∎
