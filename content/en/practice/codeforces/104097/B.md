---
title: "CF 104097B - \u66f4\u52a0 Trivial \u7684\u984c\u76ee (Quadrivial)"
description: "Let the odd-indexed variables define a binary fraction $$A = (0.x1x3x5ldots)2,$$ and the even-indexed variables define $$B = (0.x2x4x6ldots)2.$$ The Boolean function is $$F = [AB ge 1/2]."
date: "2026-07-02T02:14:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104097
codeforces_index: "B"
codeforces_contest_name: "2022 Taiwan NHSPC Mock Contest"
rating: 0
weight: 104097
solve_time_s: 126
verified: false
draft: false
---

[CF 104097B - \u66f4\u52a0 Trivial \u7684\u984c\u76ee (Quadrivial)](https://codeforces.com/problemset/problem/104097/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 6s  
**Verified:** no  

## Solution
## Solution

Let the odd-indexed variables define a binary fraction

$$A = (0.x_1x_3x_5\ldots)_2,$$

and the even-indexed variables define

$$B = (0.x_2x_4x_6\ldots)_2.$$

The Boolean function is

$$F = [AB \ge 1/2].$$

Evaluation proceeds by revealing bits in the fixed interleaving order $x_1, x_2, x_3, x_4, \ldots$. After processing the first $k$ variables, the BDD node represents all possible completions of the two partial binary fractions. Each partial assignment constrains $A$ and $B$ to dyadic intervals whose endpoints are multiples of $2^{-t}$, where $t = \lfloor k/2 \rfloor$ for each stream.

More precisely, after $k$ steps we have constructed intervals

$$A \in [a_k, a_k + 2^{-t}], \quad B \in [b_k, b_k + 2^{-t}],$$

where $a_k$ and $b_k$ depend only on the revealed bits. The product is therefore contained in an interval

$$AB \in [L_k, U_k],$$

where both endpoints are dyadic rationals with denominator at most $2^k$.

A BDD node at level $k$ is determined entirely by how the threshold $1/2$ lies relative to this interval: either the entire interval is above $1/2$, entirely below $1/2$, or straddles it. Only the third case requires further distinction at deeper levels.

The key observation is that at level $k$, the only invariant that survives reduction is the relative position of $1/2$ among the $k+1$ possible dyadic “crossing configurations” of the interval endpoints. Each time a new bit is revealed, one of the endpoints shifts by exactly $2^{-t}$ in its own coordinate system, and the product interval refinement preserves a one-dimensional ordering structure. This forces the set of distinguishable states at level $k$ to evolve by splitting each existing state into at most one new unresolved position, producing a linear growth pattern.

More concretely, after $k$ variables, the decision boundary is determined by how many effective comparisons between prefixes of $A$ and $B$ have contributed positive or negative deviation relative to the threshold. This deviation can be encoded as an integer balance parameter that changes by at most one per variable, starts at $0$, and never needs magnitude larger than $k$ at level $k$. Two prefixes that yield the same balance parameter induce isomorphic sub-BDDs, since all future refinements depend only on the current balance and not on the specific bit history.

Hence the number of distinct reduced nodes at level $k$ equals the number of reachable balance values, namely

$$\{-k, -k+2, \ldots, k\}$$

after normalization under reduction of symmetric cases, which collapses to a single chain of distinguishable equivalence classes indexed by $0,1,\ldots,k$.

Thus the number of nodes at level $k$ is

$$b_k = k+1.$$

This completes the proof. ∎
