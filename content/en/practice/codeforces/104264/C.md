---
title: "CF 104264C - Morco"
description: "Let $f(x1,x2,x3,x4,x5)$ be a Boolean function and let $B{min}(f)$ denote the minimum, over all variable orderings, of the number of nodes in its reduced ordered binary decision diagram, including the sink nodes $bot$ and $top$."
date: "2026-07-01T21:31:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104264
codeforces_index: "C"
codeforces_contest_name: "TheForces Round #9 (Fool-Forces)"
rating: 0
weight: 104264
solve_time_s: 40
verified: false
draft: false
---

[CF 104264C - Morco](https://codeforces.com/problemset/problem/104264/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** no  

## Solution
## Setup

Let $f(x_1,x_2,x_3,x_4,x_5)$ be a Boolean function and let $B_{\min}(f)$ denote the minimum, over all variable orderings, of the number of nodes in its reduced ordered binary decision diagram, including the sink nodes $\bot$ and $\top$.

For an ordering $x_{i_1},\dots,x_{i_5}$, each node of the corresponding BDD represents a distinct subfunction of $f$ obtained by fixing a prefix of variables. At depth $k$, such a node corresponds to a subfunction on $5-k$ variables. The size of the BDD equals the number of distinct subfunctions that arise along all partial assignments, together with the two constant subfunctions $\bot$ and $\top$.

The task is to determine all Boolean functions on five variables that maximize $B_{\min}(f)$ and to compute that maximum value.

## Solution

Fix an ordering of the variables. The BDD constructed from this ordering has one node for each distinct subfunction of the form

$$f(a_1,\dots,a_k,x_{k+1},\dots,x_5), \quad 0 \le k \le 5,$$

together with identification of identical subfunctions by reduction.

At depth $k$, there are at most $2^k$ distinct assignments $(a_1,\dots,a_k)$, hence at most $2^k$ subfunctions at that level. Therefore the total number of nodes is bounded by

$$1 + 2 + 4 + 8 + 16 = 2^5 - 1$$

internal nodes in the full unmerged decision tree structure. After reduction, only identical subfunctions are merged, so the size is maximized precisely when no two distinct partial assignments produce the same subfunction, except when forced by constancy at the leaves.

The sinks contribute exactly two nodes, $\bot$ and $\top$. Hence any BDD satisfies

$$B(f) \le (2^5 - 1) + 2 = 2^5 + 1 = 33.$$

This upper bound is attained exactly when every partial assignment yields a distinct subfunction, and none of these subfunctions coincide across different nodes of the full decision tree except at the two constant leaves. In that case, no reduction is possible beyond merging identical constant leaves, and every internal node of the complete binary decision tree survives in the reduced ordered BDD.

Such functions exist. A random Boolean function on five variables has, with positive probability, all $2^k$ subfunctions at depth $k$ distinct for every $k$, since the equalities defining collisions between distinct subfunctions impose strict algebraic constraints on the truth table. Any function with this property achieves a BDD isomorphic to the full decision tree with only the two sinks merged.

For any such function, every variable ordering produces the same situation: each restriction by a partial assignment yields a distinct subfunction, so no reordering can create shared nodes. Therefore the minimal BDD size is already achieved by every ordering.

Thus

$$B_{\min}(f) = 33$$

for all functions $f$ whose distinct subfunctions under all partial assignments are pairwise different except for the constant ones. No function can exceed this value.

The functions maximizing $B_{\min}(f)$ are exactly those Boolean functions on five variables whose set of all cofactors

$$\{ f|_{x_{i_1}=a_1,\dots,x_{i_k}=a_k} \}$$

contains no repetitions except the two constant functions, for every choice of ordering and every partial assignment.

Therefore the largest possible value of $B_{\min}(f)$ is

$$\boxed{33}.$$

## Verification

The full binary decision tree of height $5$ has internal-node count

$$\sum_{k=0}^{4} 2^k = 2^5 - 1 = 31.$$

Adding the two sinks $\bot$ and $\top$ gives $33$ nodes total, matching the bound.

No reduced ordered BDD can exceed the full decision tree size since every node corresponds to a distinct subfunction and there are at most $2^5$ partial assignments, hence at most $31$ non-sink positions plus two sinks.

## Notes

The extremal functions are exactly those with maximal cofactor complexity, in which the Shannon decomposition tree has no repeated subproblems except at constants. For larger $n$, the same argument yields the general maximum $2^n + 1$, achieved precisely when the BDD contains no sharing beyond the two sinks.
