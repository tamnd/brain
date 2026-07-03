---
title: "CF 102992A - Ah, It's Yesterday Once More"
description: "The representation (57) expresses a positive integer $N$ in degree-$t$ combinatorial form by selecting an index $v$ such that $$binom{n}{t} N ge binom{n}{t} - binom{v}{t},$$ and then writing $N$ as a sum of binomial coefficients with decreasing upper indices."
date: "2026-07-04T04:42:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102992
codeforces_index: "A"
codeforces_contest_name: "2020-2021 ACM-ICPC, Asia Nanjing Regional Contest (XXI Open Cup, Grand Prix of Nanjing)"
rating: 0
weight: 102992
solve_time_s: 152
verified: false
draft: false
---

[CF 102992A - Ah, It's Yesterday Once More](https://codeforces.com/problemset/problem/102992/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 32s  
**Verified:** no  

## Solution
## Solution

The representation (57) expresses a positive integer $N$ in degree-$t$ combinatorial form by selecting an index $v$ such that

$$\binom{n}{t} > N \ge \binom{n}{t} - \binom{v}{t},$$

and then writing $N$ as a sum of binomial coefficients with decreasing upper indices. Equation (60) converts such a representation into the value $\kappa_t N$ as a corresponding linear combination of binomial coefficients of degree $t-1$:

$$\kappa_t N = \binom{n}{t-1} + \binom{n-1}{t-2} + \cdots + \binom{n-v}{t-1-v}.$$

The difficulty arises when $v-1=0$, since then the right-hand side of (60) includes a term of the form $\binom{n-v}{0}$ and the standard degree reduction interpretation used in Section 7.2.1.3 fails to remain within the canonical range of indices. This creates a potential ambiguity in the representation (57).

Let $N>0$. The representation (57) is constructed by a greedy choice of $v$, and the only possible failure of uniqueness occurs at the boundary where the subtraction step produces $v=0$. If $v>0$, the construction is strictly decreasing in $v$, so the representation is unique. If $v=0$, then the construction terminates immediately with the trivial last term, but there is a second admissible representation obtained by reducing the previous step in the construction by one unit of index shift. This produces exactly two candidates: one with parameter $v=0$, and one with parameter $v=1$ arising from the carry of the binomial expansion identity

$$\binom{n}{t} = \binom{n-1}{t} + \binom{n-1}{t-1}.$$

No third representation is possible, since any further decomposition would require a second independent splitting of a binomial coefficient, which contradicts the greedy maximality condition defining (57). Hence a positive integer $N$ has at most two representations when $v=0$ is admitted.

Both representations yield the same value of $\kappa_t N$. In the case $v>0$, equation (60) applies directly. In the case $v=0$, the last term becomes

$$\binom{n}{k-1},$$

while in the alternative representation the index shift replaces the terminal term by

$$\binom{n-1}{k-2} + \binom{n}{k-1} = \binom{n}{k-1}$$

by Pascal’s identity. Hence both representations produce identical contributions at the boundary, and all preceding terms are unchanged because they depend only on higher indices in the same greedy expansion. Therefore both representations give the same value of $\kappa_t N$.

This proves that the ambiguity in representation does not affect the evaluation of $\kappa_t N$.

Now consider the product $\kappa_k \kappa_{k+1} \cdots \kappa_t N$. Repeated application of (60) expands each $\kappa_i$ as a sum of binomial coefficients whose upper indices decrease according to the same greedy structure. At each stage, the only possible branching occurs in the same boundary case $v=0$, but the previous argument shows that both branches coincide in value, so the entire iterated application is well defined independently of representation choice.

Unfolding the repeated application gives a telescoping structure. At level $t$, we obtain a term $\binom{n}{k-1}$ corresponding to no boundary shift. Each time a boundary case is triggered, the upper index decreases by $1$ and the lower index decreases by $1$ as well, producing terms of the form

$$\binom{n-i}{k-1-i}$$

for successive $i$. The process continues until the first index $v$ in the representation is reached, at which point the construction terminates.

Hence the full expansion is

$$\kappa_k \kappa_{k+1} \cdots \kappa_t N
=
\binom{n}{k-1}
+
\binom{n-1}{k-2}
+
\cdots
+
\binom{n-v}{k-1+v-t}.$$

No additional terms can appear, since each application of $\kappa_i$ reduces the effective index by at most one, and termination occurs exactly when the representation parameter $v$ is reached.

This completes the proof. ∎
