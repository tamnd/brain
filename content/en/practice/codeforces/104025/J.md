---
title: "CF 104025J - Stones"
description: "Let the ZDD represent a family $mathcal{F}$ of subsets of ${x1,dots,xn}$, ordered by the variable indices, and let each node $k$ be labeled by $V(k)in{1,dots,n}$."
date: "2026-07-02T04:17:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104025
codeforces_index: "J"
codeforces_contest_name: "The 16-th BIT Campus Programming Contest - Onsite Round"
rating: 0
weight: 104025
solve_time_s: 124
verified: false
draft: false
---

[CF 104025J - Stones](https://codeforces.com/problemset/problem/104025/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 4s  
**Verified:** no  

## Solution
## Solution

Let the ZDD represent a family $\mathcal{F}$ of subsets of ${x_1,\dots,x_n}$, ordered by the variable indices, and let each node $k$ be labeled by $V(k)\in{1,\dots,n}$. Let $\mathrm{LO}(k)$ and $\mathrm{HI}(k)$ denote its children, with the ZDD semantics that $\mathrm{LO}(k)$ excludes $x_{V(k)}$ and $\mathrm{HI}(k)$ includes $x_{V(k)}$.

Introduce terminal nodes $\bot$ and $\top$, with $\top$ representing the family ${\emptyset}$ and $\bot$ representing the empty family. Then the number of solutions contributed by $\top$ is $1$ and by $\bot$ is $0$.

For each node $k$, let $F(k)$ denote the number of solutions represented by the sub-ZDD rooted at $k$, where solutions are counted as full assignments of the variables not yet fixed along the path. If a path reaches a node labeled $j$ after having last seen variable index $i<j$, then the variables $x_{i+1},\dots,x_{j-1}$ are unconstrained and each contributes a factor of $2$.

To express this formally, extend the variable index to terminals by setting $V(\top)=V(\bot)=n+1$. Then every arc from a node $k$ to a child $c\in{\mathrm{LO}(k),\mathrm{HI}(k)}$ skips exactly $V(c)-V(k)-1$ variables, contributing a factor $2^{V(c)-V(k)-1}$.

The contribution from each child is therefore the number of partial solutions in the subtree multiplied by the number of free assignments induced by skipped variables. This yields the recurrence

$$F(k)=\sum_{c\in\{\mathrm{LO}(k),\mathrm{HI}(k)\}} 2^{V(c)-V(k)-1}\,F(c),$$

with base values

$$F(\bot)=0,\qquad F(\top)=1.$$

This recurrence is evaluated in a single traversal exactly as in Algorithm C for BDD counting, except that the multiplicative factor depends on variable-level gaps rather than being uniform.

To implement this as a modification of Algorithm C, store computed values of $F(k)$ in a table to avoid recomputation. When processing a node $k$, first recursively compute $F(\mathrm{LO}(k))$ and $F(\mathrm{HI}(k))$, then combine them using the factor determined by their level differences from $V(k)$ as shown in the recurrence. The memoization structure is identical to Algorithm C, since each node is evaluated once in a reduced ZDD.

This computes the number of satisfying assignments of the Boolean function represented by the ZDD, since each root-to-terminal path corresponds to a unique partial assignment, and each skipped variable doubles the number of consistent full extensions.

This completes the proof. ∎
