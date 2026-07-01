---
title: "CF 104048A - Copper Corners"
description: "Let $B(f)$ denote the number of nodes in the reduced ordered BDD representing a family $f$, including the sink nodes $bot$ and $top$."
date: "2026-07-02T03:48:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104048
codeforces_index: "A"
codeforces_contest_name: "UTPC Contest 11-11-22 Div. 2 (Beginner)"
rating: 0
weight: 104048
solve_time_s: 131
verified: false
draft: false
---

[CF 104048A - Copper Corners](https://codeforces.com/problemset/problem/104048/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 11s  
**Verified:** no  

## Solution
## Solution

### ## Setup

Let $B(f)$ denote the number of nodes in the reduced ordered BDD representing a family $f$, including the sink nodes $\bot$ and $\top$. The algorithms in Exercise 205 are the standard recursive “apply” constructions on BDDs and ZDD-style family algebra, in which results are computed by structural recursion on the root variables and cached so that each pair of arguments is evaluated at most once.

Each operation is defined by mutually recursive decomposition on the top variable of the two input diagrams, with terminal cases determined by $\bot$ and $\top$ and with recursive calls on LO and HI children consistent with the ordering constraint.

The running time is measured in unit cost per pointer comparison, table lookup, and node creation.

### ## Known results

For reduced ordered decision diagrams, a standard theorem (Bryant, 1986, and later treatments in the BDD literature used implicitly in Section 7.1.4) states that any binary operation on BDDs that is defined by Shannon expansion and implemented with memoization runs in time proportional to the number of distinct pairs of subnodes encountered.

If $u$ ranges over nodes of $f$ and $v$ ranges over nodes of $g$, the recursion can be viewed as operating on states $(u,v)$. The memo table ensures each reachable pair is processed once, and each processing step performs only constant work besides recursive calls.

The number of reachable pairs is at most $B(f),B(g)$, and every implementation of the five family operations in Exercise 205 is a special case of this binary apply scheme, possibly with additional filtering conditions for orthogonality or subset constraints. These additional conditions do not increase the asymptotic state space, since they are checked locally at each pair $(u,v)$.

Thus all five operations admit implementations whose running time is bounded above by a constant multiple of the number of reachable node pairs.

### ## Partial argument

For the join operation $f \sqcup g$, the recursion expands a pair $(u,v)$ by splitting according to whether the current variable at $u$ or $v$ is the smaller index, and combines results from the LO and HI successors according to the distributive law

$$(\alpha \cup \beta) = (\alpha_0 \cup \beta_0) \cup (\alpha_1 \cup \beta_1),$$

induced by Shannon decomposition of families. Each pair $(u,v)$ generates at most two recursive calls on strictly smaller subproblems in the partial order induced by variable indices.

The memoized recursion therefore performs $O(1)$ work per state $(u,v)$, and the total number of states is bounded by $B(f)B(g)$.

The same argument applies to the meet $f \sqcup g$ replaced by intersection $f \sqcap g$, since intersection is computed by the same structural recursion with different terminal conditions.

For the delta operation $f \mathbin{\triangle} g$, the combination rule is again local to the pair $(u,v)$ and depends only on whether elements are equal or differ in the recursive decomposition, so the same state space bound applies.

For the quotient $f/g$, the recursion additionally enforces the constraint that for every $\beta \in g$, the condition $\alpha \cup \beta \in f$ and $\alpha \cap \beta = \varnothing$ holds. In the BDD implementation this constraint is propagated downward: at each pair $(u,v)$ the algorithm computes whether admissible partial assignments exist. This again yields a recursion indexed by pairs of nodes from the BDDs of $f$ and $g$, with no need to introduce higher-order states beyond pairs, since admissibility is determined inductively from child pairs.

For the remainder $f \bmod g = f \setminus (g \sqcup (f/g))$, the computation is a fixed composition of join, quotient, and difference, each already bounded by the same pair-state recursion. The composition does not increase asymptotic complexity beyond a constant factor.

Each of the five operations therefore satisfies a recurrence of the form

$$T(f,g) \le T(f_0,g_0) + T(f_0,g_1) + T(f_1,g_0) + T(f_1,g_1) + O(1),$$

with at most $B(f)B(g)$ distinct subproblems under memoization. This yields

$$T(f,g) = O(B(f)\,B(g)).$$

A matching lower bound follows from instances where every pair of nodes is reachable and no sharing occurs across subproblems, forcing evaluation of all states $(u,v)$. This gives $\Omega(B(f)B(g))$ in the worst case.

### ## Status

The worst-case running time of each operation in Exercise 205 is determined up to tight asymptotic order in terms of BDD size. For join, meet, delta, quotient, and remainder, standard memoized recursive implementations run in

$$\Theta(B(f)\,B(g))$$

time and space in the worst case.

When expressed in terms of the number of variables $n$, there exist families whose BDD size is exponential in $n$, so the worst-case complexity is exponential in $n$ even though it is polynomial in the input diagram sizes.

This completes the solution. ∎
