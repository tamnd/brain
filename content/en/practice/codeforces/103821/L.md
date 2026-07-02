---
title: "CF 103821L - ResliPhobia"
description: "Let $w(x1,ldots,xn)$ denote the contribution of a minterm $$(1-p1)^{1-x1}p1^{x1}cdots (1-pn)^{1-xn}pn^{xn}.$$ Maximizing this quantity over all assignments satisfying $f(x1,ldots,xn)=1$ is equivalent to maximizing a product of independent local factors along a path in the BDD of…"
date: "2026-07-02T08:25:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103821
codeforces_index: "L"
codeforces_contest_name: "(Aleppo + HAIST + SVU + Private) CPC 2022"
rating: 0
weight: 103821
solve_time_s: 127
verified: false
draft: false
---

[CF 103821L - ResliPhobia](https://codeforces.com/problemset/problem/103821/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 7s  
**Verified:** no  

## Solution
## Solution

Let $w(x_1,\ldots,x_n)$ denote the contribution of a minterm

$$(1-p_1)^{1-x_1}p_1^{x_1}\cdots (1-p_n)^{1-x_n}p_n^{x_n}.$$

Maximizing this quantity over all assignments satisfying $f(x_1,\ldots,x_n)=1$ is equivalent to maximizing a product of independent local factors along a path in the BDD of $f$, because each variable $x_i$ contributes exactly one factor depending only on whether the LO or HI branch is taken at a node labeled $i$.

Let each BDD node $v$ labeled by variable index $i=V(v)$ be assigned a value $W(v)$ defined as the maximum possible contribution from $v$ to the terminal node $\top$. For the sink nodes, the boundary conditions are

$$W(\top)=1,\qquad W(\bot)=0.$$

The value $1$ at $\top$ corresponds to the empty product, and $0$ reflects that any path reaching $\bot$ contributes nothing to a valid solution.

For a branch node $v$ labeled $i$, with LO successor $v_0$ and HI successor $v_1$, any assignment extending a path through $v$ must choose exactly one of the two variable settings. The contribution of extending through the LO edge is $(1-p_i)W(v_0)$, and the contribution through the HI edge is $p_iW(v_1)$. The optimal continuation from $v$ therefore satisfies

$$W(v)=\max\bigl((1-p_i)W(v_0),\; p_iW(v_1)\bigr).$$

Because the BDD is a directed acyclic graph ordered by variable indices, the values $W(v)$ can be computed in reverse topological order from sinks toward the root. This recurrence is well-defined since every successor of $v$ has strictly larger variable index.

Once $W(\text{root})$ is computed, an optimal satisfying assignment is obtained by following choices that achieve the maximum at each node. Starting at the root node $r$, if $r$ is a sink the assignment is already determined. If $r$ is a branch node labeled $i$, then if

$$(1-p_i)W(v_0)\ge p_iW(v_1)$$

the assignment sets $x_i=0$ and proceeds to $v_0$, otherwise it sets $x_i=1$ and proceeds to $v_1$. Repeating this process yields a path that necessarily ends in $\top$, since any path contributing positive weight corresponds to a satisfying assignment of $f$.

The correctness follows from the fact that every satisfying assignment corresponds bijectively to a root-to-$\top$ path in the BDD, and the contribution of the assignment factors multiplicatively along edges exactly as in the recurrence defining $W(v)$. Hence the computed path maximizes the total product among all satisfying assignments.

This completes the proof. ∎
