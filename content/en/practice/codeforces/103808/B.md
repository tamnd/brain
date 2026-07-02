---
title: "CF 103808B - Desordenado"
description: "Let $f(x1,dots,xn)$ be represented by an ordered reduced BDD with root node $r$. For each node $k$ in the BDD, write $V(k)$ for its variable index, and write $mathrm{LO}(k)$ and $mathrm{HI}(k)$ for its two successors. The sinks are $bot$ and $top$."
date: "2026-07-02T08:38:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103808
codeforces_index: "B"
codeforces_contest_name: "XXVI Spain Olympiad in Informatics, Day 2"
rating: 0
weight: 103808
solve_time_s: 124
verified: false
draft: false
---

[CF 103808B - Desordenado](https://codeforces.com/problemset/problem/103808/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 4s  
**Verified:** no  

## Solution
## Solution

Let $f(x_1,\dots,x_n)$ be represented by an ordered reduced BDD with root node $r$. For each node $k$ in the BDD, write $V(k)$ for its variable index, and write $\mathrm{LO}(k)$ and $\mathrm{HI}(k)$ for its two successors. The sinks are $\bot$ and $\top$.

For every node $k$, define a Boolean function $f_k$ on the variables $x_{V(k)}, x_{V(k)+1}, \dots, x_n$ as the subfunction represented by the BDD rooted at $k$. Let $T(k)$ denote the truth table of $f_k$ in the order used in Section 7.1.1, namely lexicographic order on $(x_{V(k)},\dots,x_n)$ starting from all zeros.

The structure of a BDD implies the decomposition

$$f_k(x_{V(k)},\dots,x_n) = 
\begin{cases}
f_{\mathrm{LO}(k)}(x_{V(k)+1},\dots,x_n) & \text{if } x_{V(k)}=0,\\
f_{\mathrm{HI}(k)}(x_{V(k)+1},\dots,x_n) & \text{if } x_{V(k)}=1.
\end{cases}$$

This identity determines the corresponding decomposition of truth tables. If $T(k)$ has length $2^m$, where $m = n - V(k) + 1$, then each of $T(\mathrm{LO}(k))$ and $T(\mathrm{HI}(k))$ has length $2^{m-1}$. The ordering convention for truth tables implies that the first half of $T(k)$ corresponds to $x_{V(k)}=0$ and the second half corresponds to $x_{V(k)}=1$. Therefore

$$T(k) = T(\mathrm{LO}(k)) \, T(\mathrm{HI}(k)).$$

For sinks, the corresponding subfunctions are constants. If $k=\bot$, then $f_k$ is identically $0$, hence

$$T(\bot) = 00\cdots 0 \quad (2^m \text{ zeros for the appropriate } m).$$

If $k=\top$, then $f_k$ is identically $1$, hence

$$T(\top) = 11\cdots 1.$$

Algorithm C is modified by replacing the arithmetic combination of subresults with concatenation of binary strings. The evaluation proceeds bottom-up over the BDD in reverse topological order induced by the variable ordering. For each node $k$, once $T(\mathrm{LO}(k))$ and $T(\mathrm{HI}(k))$ have been computed, the value $T(k)$ is formed by concatenation. Because the BDD is reduced, each node is computed once, and because it is ordered, all dependencies are strictly forward in the variable index, so this evaluation order is well defined.

The correctness follows by induction on the variable index. For sinks the statement holds by definition. For a branch node $k$, assume $T(\mathrm{LO}(k))$ and $T(\mathrm{HI}(k))$ correctly represent the subfunctions obtained by fixing $x_{V(k)}=0$ and $x_{V(k)}=1$. The lexicographic structure of the truth table splits exactly into these two halves, so concatenation yields precisely the truth table of $f_k$. This completes the inductive step.

Applying the construction to the root node produces $T(r)$, which is the fully elaborated truth table of $f$ in the standard $2^n$-bit ordering.

Therefore the modified Algorithm C outputs $T(r)$, the truth table of $f$.

$$\boxed{T(r)}$$
