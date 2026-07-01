---
title: "CF 104217G - Journey to Nome"
description: "Let the given BDD for $f(x1,dots,xn)$ be a rooted directed acyclic graph whose branch nodes are labeled by variables $V(u)in{1,dots,n}$ and whose sink nodes are $bot,top$, with orderedness ensuring that along every directed path the labels strictly increase."
date: "2026-07-01T23:54:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104217
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 03-03-23 Div. 2 (Beginner)"
rating: 0
weight: 104217
solve_time_s: 30
verified: false
draft: false
---

[CF 104217G - Journey to Nome](https://codeforces.com/problemset/problem/104217/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 30s  
**Verified:** no  

## Solution
## Solution

Let the given BDD for $f(x_1,\dots,x_n)$ be a rooted directed acyclic graph whose branch nodes are labeled by variables $V(u)\in{1,\dots,n}$ and whose sink nodes are $\bot,\top$, with orderedness ensuring that along every directed path the labels strictly increase.

A vector $(x_1,\dots,x_n)$ satisfies $f(x_1,\dots,x_n)=1$ exactly when the evaluation path determined by starting at the root and following the LO edge for value $0$ and the HI edge for value $1$ terminates at $\top$.

To generate all such vectors it suffices to traverse all root-to-$\top$ paths in the BDD while accounting for variables that are not tested along a path. If a path reaches a node labeled $V(u)=j$ after having most recently fixed variable $x_k$ with $k<j-1$, then variables $x_{k+1},\dots,x_{j-1}$ are unconstrained by the BDD structure and may be chosen arbitrarily.

Define a recursive procedure $\mathrm{ENUM}(u,k,a_1,\dots,a_k)$, where $u$ is a BDD node, $k$ is the last assigned variable index, and $(a_1,\dots,a_k)$ is the current partial vector.

At a sink node, the procedure behaves as follows. If $u=\bot$, no completion is possible and the procedure returns without output. If $u=\top$, then all completions of $(a_1,\dots,a_k)$ to an $n$-tuple are valid outputs, so the procedure outputs every vector $(a_1,\dots,a_n)$ with $a_{k+1},\dots,a_n\in{0,1}$.

At a branch node $u$ with $V(u)=j$, the variables $x_{k+1},\dots,x_{j-1}$ are not yet assigned. The procedure therefore first enumerates all $2^{j-k-1}$ assignments to these variables, extending the current prefix to $(a_1,\dots,a_k,b_{k+1},\dots,b_{j-1})$ with each $b_i\in{0,1}$. After this expansion, it continues the BDD descent by assigning $x_j=0$ and invoking $\mathrm{ENUM}(\mathrm{LO}(u),j,\dots)$, and separately assigning $x_j=1$ and invoking $\mathrm{ENUM}(\mathrm{HI}(u),j,\dots)$.

The initial call is $\mathrm{ENUM}(\mathrm{ROOT},0)$ with an empty prefix.

Correctness follows from the invariant that at every call $\mathrm{ENUM}(u,k,a_1,\dots,a_k)$ the prefix encodes exactly the variables $x_1,\dots,x_k$, and every extension of this prefix corresponds to a unique path in the BDD consistent with the ordering constraint. Orderedness ensures that no variable is revisited after leaving a node, so every assignment is determined exactly once by choices at branch nodes together with free choices on skipped indices. Reduction of the BDD ensures that no spurious duplicate nodes generate duplicate inconsistent substructures, since identical subgraphs are shared and thus induce identical continuation sets.

If $(x_1,\dots,x_n)$ satisfies $f=1$, its evaluation path reaches $\top$ at some node $u$, and the recursion necessarily produces it when the procedure reaches $u$ and expands the unconstrained variables exactly as above. Conversely, any vector produced by the procedure follows a path that reaches $\top$, since output occurs only from the sink $\top$ and all preceding transitions respect the LO and HI semantics of the BDD evaluation. Hence the procedure outputs exactly the set of satisfying assignments.

This completes the proof. ∎
