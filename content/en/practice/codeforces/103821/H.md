---
title: "CF 103821H - FAT Sequences"
description: "Let $f$ be represented by a reduced ordered binary decision diagram, and let $F(p)$ denote the reliability polynomial under the specialization $p1=cdots=pn=p$."
date: "2026-07-02T08:23:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103821
codeforces_index: "H"
codeforces_contest_name: "(Aleppo + HAIST + SVU + Private) CPC 2022"
rating: 0
weight: 103821
solve_time_s: 127
verified: false
draft: false
---

[CF 103821H - FAT Sequences](https://codeforces.com/problemset/problem/103821/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 7s  
**Verified:** no  

## Solution
## Solution

Let $f$ be represented by a reduced ordered binary decision diagram, and let $F(p)$ denote the reliability polynomial under the specialization $p_1=\cdots=p_n=p$. For each node $v$ of the BDD, let $F_v(p)$ denote the corresponding subfunction value of $F(p)$ obtained by restricting to the sub-BDD rooted at $v$. For sink nodes, the definitions are fixed by $F_{\bot}(p)=0$ and $F_{\top}(p)=1$.

For a branch node $v$ labeled by some variable $x_j$ with LO successor $v_0$ and HI successor $v_1$, the evaluation of the reliability polynomial under identical probabilities follows directly from conditioning on the value of $x_j$, since each variable equals $1$ with probability $p$ and $0$ with probability $1-p$. This yields

$$F_v(p) = (1-p)F_{v_0}(p) + pF_{v_1}(p).$$

This recurrence matches the structure of Algorithm C in Section 7.1.4, where the computation proceeds bottom-up over the BDD and each node value is a combination of its successors.

To compute the derivative, differentiate the identity above with respect to $p$. Writing $F_v'(p)=\frac{d}{dp}F_v(p)$ gives

$$F_v'(p)
= \frac{d}{dp}\bigl((1-p)F_{v_0}(p) + pF_{v_1}(p)\bigr).$$

Applying the product rule to each term yields

$$F_v'(p)
= -(F_{v_0}(p)) + (1-p)F_{v_0}'(p) + F_{v_1}(p) + pF_{v_1}'(p).$$

Rearranging terms produces a form aligned with the same bottom-up structure:

$$F_v'(p)
= (1-p)F_{v_0}'(p) + pF_{v_1}'(p) + \bigl(F_{v_1}(p)-F_{v_0}(p)\bigr).$$

This expresses both $F_v(p)$ and $F_v'(p)$ solely in terms of the two successors, so the computation can be done in a single traversal of the BDD in reverse topological order, exactly as in Algorithm C, provided each node is processed only after its LO and HI successors have been evaluated.

The modified algorithm associates with each node $v$ a pair of values $(F_v, D_v)$, where $D_v$ represents $F_v'(p)$. For sink nodes,

$$(F_{\bot},D_{\bot})=(0,0), \qquad (F_{\top},D_{\top})=(1,0).$$

For every branch node $v$ with successors $v_0$ and $v_1$, the computation is

$$F_v \leftarrow (1-p)F_{v_0} + pF_{v_1},$$

$$D_v \leftarrow (1-p)D_{v_0} + pD_{v_1} + (F_{v_1}-F_{v_0}).$$

Because the BDD is ordered and acyclic, every node is evaluated exactly once in an order consistent with increasing variable index, so all successor values are available when needed, matching the evaluation discipline of Algorithm C.

The value returned for the original function is the pair at the root node $r$, namely $F_r(p)$ and $F_r'(p)$.

This completes the construction of the modified algorithm and the justification of the derivative recurrence. ∎
