---
title: "CF 1119F - Niyaz and Small Degrees"
description: "We are given a weighted tree. For every degree limit $x$, we may delete any set of edges. Deleting an edge pays its weight. After all deletions, every vertex must have degree at most $x$. For each $x$, we need the minimum total deleted weight."
date: "2026-06-12T04:29:34+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "trees"]
categories: ["algorithms"]
codeforces_contest: 1119
codeforces_index: "F"
codeforces_contest_name: "Codeforces Global Round 2"
rating: 3400
weight: 1119
solve_time_s: 48
verified: false
draft: false
---

[CF 1119F - Niyaz and Small Degrees](https://codeforces.com/problemset/problem/1119/F)

**Rating:** 3400  
**Tags:** data structures, dp, trees  
**Solve time:** 48s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a weighted tree.

For every degree limit $x$, we may delete any set of edges. Deleting an edge pays its weight. After all deletions, every vertex must have degree at most $x$.

For each $x$, we need the minimum total deleted weight.

The tree has up to $250\,000$ vertices. Any solution that independently solves the problem for every $x$ is immediately ruled out. Even an $O(n)$ algorithm per value of $x$ would become $O(n^2)$, which is far beyond the limit.

The non-obvious part is that the constraint is local. A vertex only cares about how many incident edges survive. This suggests a DP that decides, for each edge, whether it is kept or deleted.

## Approaches

Suppose $x$ is fixed.

Root the tree arbitrarily.

For a vertex $u$, define:

$f_u^0$: minimum cost inside the subtree of $u$ when the edge from $u$ to its parent is kept.

$f_u^1$: minimum cost inside the subtree of $u$ when the edge from $u$ to its parent is deleted.

Consider a child $v$ connected by an edge of weight $w$.

If we keep $(u,v)$, the contribution is $f_v^0$.

If we delete $(u,v)$, we pay

$$w + f_v^1.$$

The extra price of deleting instead of keeping is

$$\Delta_v = w + f_v^1 - f_v^0.$$

Start from the state where every child edge is kept.

Then each deleted child edge adds $\Delta_v$.

Some $\Delta_v$ are already non-positive. Such edges should always be deleted because doing so never increases the answer.

After forcing all non-positive $\Delta_v$, the remaining task is simple:

A vertex of degree $d$ must end with degree at most $x$.

Hence it must delete enough incident edges. Among all remaining candidates, we choose the smallest positive $\Delta_v$.

This gives an $O(n\log n)$ DP for one fixed value of $x$.

Unfortunately we need all values of $x$.

The crucial observation is that when $x$ decreases, only vertices whose degree becomes larger than $x$ start imposing constraints. Vertices with degree already at most $x$ are irrelevant.

Process $x$ from $n-1$ down to $1$.

Maintain the induced forest consisting only of vertices whose degree is greater than the current limit.

Whenever $x$ decreases by one, a new batch of vertices becomes active.

The DP is recomputed only inside the newly formed active components. To support the "take the smallest $k$ deltas" operation efficiently, each vertex maintains a balanced structure containing candidate $\Delta$ values and the sum of the currently chosen ones. The original solutions use either multisets with rollback or a binary trie supporting insertion, deletion and "sum of the smallest $k$ values".

The resulting complexity is $O(n\log n)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Solve every $x$ independently | $O(n^2\log n)$ | $O(n)$ | Too slow |
| Offline activation + tree DP | $O(n\log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Compute the original degree of every vertex.
2. Group vertices by degree.
3. Process limits $x=n-1,n-2,\ldots,1$.
4. When the limit becomes $x$, activate every vertex whose degree is now greater than $x$.
5. Active vertices form a forest.
6. For each active component, run the tree DP.
7. For every child $v$, compute

$$\Delta_v=w+f_v^1-f_v^0.$$

1. All non-positive $\Delta_v$ are taken immediately because deleting such an edge is never worse.
2. Let $k$ be the number of additional incident edges that must be removed to satisfy the degree bound.
3. Among remaining positive $\Delta_v$, add the sum of the smallest $k$ values.
4. This gives $f_u^0$ and $f_u^1$.
5. Sum the contribution of all active components to obtain the answer for this $x$.
6. For $x=0$, every edge must be deleted, so the answer is simply the sum of all edge weights.

### Why it works

For a fixed $x$, every child edge contributes either the "keep" cost or the "delete" cost.

The difference between these choices is exactly $\Delta_v$.

After all mandatory deletions with non-positive $\Delta_v$ are taken, every remaining deletion increases the objective by a positive amount. To satisfy the degree restriction, the optimal strategy is to pay the smallest available increases. This is a standard exchange argument: replacing a chosen deletion by a larger $\Delta$ can only worsen the answer.

The offline sweep works because a vertex affects the DP only when its degree exceeds the current limit. As $x$ decreases, vertices become active exactly once, allowing all updates to be charged to a single activation event.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n\log n)$ | Each activation and each DP data-structure operation costs logarithmic time |
| Space | $O(n)$ | Tree, DP arrays and balanced structures |

The constraints allow roughly a few million logarithmic operations. $O(n\log n)$ comfortably fits within the 3-second limit for $n=250\,000$.
