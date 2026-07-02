---
title: "CF 103824F - \u6298\u78e8\u738b(hard version)"
description: "Let $v$ be a node of the reduced ordered BDD for $f$, and let $Fv(p)$ denote the reliability polynomial of the subfunction represented at $v$ under the specialization $p1=cdots=pn=p$. Let $F'v(p)$ denote its derivative with respect to $p$."
date: "2026-07-02T08:19:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103824
codeforces_index: "F"
codeforces_contest_name: "2022 Summer Camp of XTU Qualifying Round"
rating: 0
weight: 103824
solve_time_s: 55
verified: false
draft: false
---

[CF 103824F - \u6298\u78e8\u738b(hard version)](https://codeforces.com/problemset/problem/103824/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** no  

## Solution
## Solution

Let $v$ be a node of the reduced ordered BDD for $f$, and let $F_v(p)$ denote the reliability polynomial of the subfunction represented at $v$ under the specialization $p_1=\cdots=p_n=p$. Let $F'_v(p)$ denote its derivative with respect to $p$.

For sink nodes the values are fixed by definition of the reliability polynomial. If $v=\bot$, then $F_v(p)=0$ and $F'_v(p)=0$. If $v=\top$, then $F_v(p)=1$ and $F'_v(p)=0$.

Let $v$ be a branch node labeled by variable $x_k$ with low successor $v_L$ and high successor $v_H$. The reliability polynomial satisfies the decomposition inherited from the definition in Algorithm C, since conditioning on $x_k=0$ contributes weight $1-p$ and conditioning on $x_k=1$ contributes weight $p$. Therefore

$$F_v(p)=(1-p)F_{v_L}(p)+pF_{v_H}(p).$$

Differentiating this identity with respect to $p$ yields

$$F'_v(p)=-(F_{v_L}(p))+(1-p)F'_{v_L}(p)+F_{v_H}(p)+pF'_{v_H}(p).$$

These two recurrences determine both the reliability value and its derivative at every node once values for successors are known.

A direct evaluation proceeds in a postorder traversal of the BDD directed acyclic graph. Each node is computed once because reduced ordered BDDs identify isomorphic subfunctions, so sharing guarantees that both $F_v(p)$ and $F'_v(p)$ are defined consistently for every node reached from the root.

The computation assigns to each node $v$ a pair of numbers $(F_v, F'_v)$ according to the recurrence. At sinks the pair is $(0,0)$ or $(1,0)$. At branch nodes the pair is formed from the already computed pairs of $v_L$ and $v_H$ using the formulas above. Since each node has exactly two outgoing arcs and the graph is acyclic under the variable ordering, this bottom-up propagation reaches the root after all dependencies are resolved.

The value $F(p)$ for the original Boolean function $f$ is $F_r(p)$ at the root node $r$, and its derivative is $F'_r(p)$.

This completes the construction of a modified Algorithm C that simultaneously evaluates the reliability polynomial at $p$ and its derivative. ∎
