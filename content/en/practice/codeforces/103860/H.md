---
title: "CF 103860H - Harie Programming Contest"
description: "Let $H$ be an $mtimes n$ parity-check matrix over $mathbb{F}2$, and let $$f(x)= [Hx=0], qquad x=(x1,dots,xn)^T.$$ Fix a variable order $x1,dots,xn$."
date: "2026-07-02T08:00:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103860
codeforces_index: "H"
codeforces_contest_name: "The 7th China Collegiate Programming Contest, Finals (CCPC Finals 2021)"
rating: 0
weight: 103860
solve_time_s: 125
verified: false
draft: false
---

[CF 103860H - Harie Programming Contest](https://codeforces.com/problemset/problem/103860/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 5s  
**Verified:** no  

## Solution
## Solution

Let $H$ be an $m\times n$ parity-check matrix over $\mathbb{F}_2$, and let

$$f(x)= [Hx=0], \qquad x=(x_1,\dots,x_n)^T.$$

Fix a variable order $x_1,\dots,x_n$. For $0\le k\le n$, write $H_k$ for the $m\times k$ submatrix consisting of the first $k$ columns of $H$, and define

$$r_k = \operatorname{rank}(H_k).$$

For a partial assignment $u=(x_1,\dots,x_k)$, the syndrome is

$$s(u)=H_k u \in \mathbb{F}_2^m.$$

The subfunction induced by $u$ on the remaining variables $x_{k+1},\dots,x_n$ is

$$f_u(x_{k+1},\dots,x_n) = [H_{k+1..n}(x_{k+1},\dots,x_n) = s(u)].$$

Two assignments $u,u'$ yield the same subfunction if and only if $s(u)=s(u')$, since equality of syndromes gives identical affine constraints on the remaining variables.

The map $u\mapsto s(u)$ has image equal to the column space of $H_k$, which has cardinality $2^{r_k}$. Hence the number of distinct subfunctions at level $k$ in the BDD equals $2^{r_k}$.

Each distinct subfunction corresponds to a unique BDD node at level $k$. Therefore the number of nonterminal nodes equals

$$\sum_{k=0}^{n-1} 2^{r_k},$$

since $k=n$ contributes only terminal subfunctions.

At level $n$, every assignment yields either consistency $s(u)=0$ or inconsistency $s(u)\ne 0$, so all consistent leaves merge into a single $\top$ node and all inconsistent leaves merge into a single $\bot$ node. This contributes exactly $2$ sink nodes.

Hence

$$B(f)=\sum_{k=0}^{n-1} 2^{r_k} + 2.$$

Since $r_0=0$, this is equivalently

$$B(f)=3+\sum_{k=1}^{n-1} 2^{r_k}.$$

For the Hamming code, $n=2^m-1$, and $H$ has as columns all nonzero vectors of $\mathbb{F}_2^m$. With the standard ordering in which the first $m$ columns form an invertible matrix, the rank growth satisfies

$$r_k = k \quad (1\le k\le m), \qquad r_k=m \quad (m\le k\le n).$$

Substituting into the formula gives

$$B(f)=\sum_{k=0}^{m}2^k + \sum_{k=m+1}^{n-1}2^m + 2.$$

The first sum is

$$\sum_{k=0}^{m}2^k = 2^{m+1}-1.$$

The second sum contains $n-1-m$ terms, hence equals

$$(n-1-m)2^m.$$

With $n=2^m-1$, this becomes

$$(2^m-2-m)2^m.$$

Therefore

$$B(f)=(2^{m+1}-1) + (2^m-2-m)2^m + 2.$$

Simplifying,

$$(2^{m+1}-1)+2 = 2^{m+1}+1,$$

so

$$B(f)=2^{m+1}+1 + 2^{2m} - (m+2)2^m.$$

Since $2^{m+1} = 2\cdot 2^m$, this becomes

$$B(f)=2^{2m} - m2^m + 1.$$

Thus for the Hamming code,

$$\boxed{B(f)=2^{2m}-m2^m+1}.$$

For part (c), the received word $y=(y_1,\dots,y_n)$ and independent channel probabilities $p_k=\Pr[y_k=x_k]$ induce likelihood weights on assignments $x$:

$$\Pr(x\mid y) \propto \prod_{k=1}^n \bigl(p_k^{[x_k=y_k]} (1-p_k)^{[x_k\ne y_k]}\bigr).$$

The MAP codeword maximizes this product over all $x$ satisfying $f(x)=1$. In the BDD of $f$, each root-to-$\top$ path corresponds to a codeword. Assign each HI edge at level $k$ the factor

$$p_k \text{ if } y_k=1,\quad (1-p_k) \text{ if } y_k=0,$$

and each LO edge the complementary factor.

The MAP codeword is obtained by computing a maximum-weight path from the root to $\top$, where path weight is the product of edge weights. Equivalently, taking logarithms converts this to a longest-path problem in the acyclic BDD:

$$\sum \log(\text{edge weight}).$$

Dynamic programming on the BDD, evaluating nodes in topological order, yields the optimal value at the root, and backtracking yields the corresponding codeword.

This completes the solution. ∎
