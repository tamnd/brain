---
title: "CF 103811L - Lockout"
description: "Let the contribution of a minterm corresponding to an assignment $x1 ldots xn$ be $$C(x1,ldots,xn)=prod{i=1}^n (1-pi)^{1-xi}pi^{xi}."
date: "2026-07-02T08:30:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103811
codeforces_index: "L"
codeforces_contest_name: "La Salle-Pui Ching Programming Challenge \u57f9\u6b63\u5587\u6c99\u7de8\u7a0b\u6311\u6230\u8cfd 2021"
rating: 0
weight: 103811
solve_time_s: 125
verified: false
draft: false
---

[CF 103811L - Lockout](https://codeforces.com/problemset/problem/103811/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 5s  
**Verified:** no  

## Solution
## Solution

Let the contribution of a minterm corresponding to an assignment $x_1 \ldots x_n$ be

$$C(x_1,\ldots,x_n)=\prod_{i=1}^n (1-p_i)^{1-x_i}p_i^{x_i}.$$

Taking logarithms converts maximization of the product into maximization of a sum:

$$\log C(x_1,\ldots,x_n)=\sum_{i=1}^n \bigl((1-x_i)\log(1-p_i)+x_i\log p_i\bigr).$$

For each index $i$, define the two local weights

$$w_i(0)=\log(1-p_i), \qquad w_i(1)=\log p_i.$$

Then the objective becomes $\sum_{i=1}^n w_i(x_i)$, and maximizing the minterm contribution is equivalent to maximizing this sum subject to $f(x_1,\ldots,x_n)=1$.

A root-to-$\top$ path in the BDD fixes some variables and skips others according to the ordering property. If a node has variable index $j$ and its successor has index $k>j+1$, then variables $j+1,\ldots,k-1$ do not appear on that path. For each such skipped variable $i$, its value may be chosen independently, so its optimal contribution is

$$m_i=\max(\log(1-p_i),\log p_i).$$

Thus every transition in the BDD contributes a fixed gap term determined solely by the indices of the endpoints, together with the contribution of the chosen branch.

Define a dynamic programming value $H(v)$ for each node $v$, interpreted as the maximum achievable log-contribution from $v$ to $\top$.

For a sink node,

$$H(\top)=0, \qquad H(\bot)=-\infty.$$

For a branch node $v$ labeled by variable $x_j$, let its low and high successors be $\mathrm{LO}(v)$ and $\mathrm{HI}(v)$. For any successor $u$ of $v$, define the gap contribution

$$G(j,u)=\sum_{i=j+1}^{V(u)-1} m_i,$$

where $V(u)$ is the variable index of node $u$ and for sinks we take $V(\top)=n+1$.

Then the recurrence is

$$H(v)=\max\Bigl(w_j(0)+G(j,\mathrm{LO}(v))+H(\mathrm{LO}(v)),\; w_j(1)+G(j,\mathrm{HI}(v))+H(\mathrm{HI}(v))\Bigr).$$

The root has index $j_0=V(\mathrm{ROOT})$, and its initial gap contributes $\sum_{i=1}^{j_0-1} m_i$. The optimal value is obtained by adding this initial gap to $H(\mathrm{ROOT})$, and an optimal assignment is recovered by following at each node the branch achieving the maximum in the recurrence.

Correctness follows from the decomposition of any complete assignment into three independent parts: the fixed decision at the current variable, the independent optimal choices for skipped variables, and the optimal continuation in the sub-BDD. Each complete assignment corresponds to exactly one root-to-$\top$ path together with independent choices on gaps, and the recurrence exhausts all such possibilities without omission or duplication. The acyclicity of the BDD ordering ensures that $H(v)$ is well-defined by backward induction on decreasing variable indices, since all successors have larger indices.

The constructed assignment satisfies $f(x_1,\ldots,x_n)=1$ because only $\top$-reachable paths are considered, and its minterm contribution is maximal because every local decision and every skipped-variable choice is individually optimal under the additive decomposition of $\log C$.

This completes the solution. ∎
