---
title: "CF 102911A - Academic Recovery"
description: "A clutter on the ground set $[n]={0,1,dots,n-1}$ is an antichain in the Boolean lattice: if $alpha,betain C$ and $alphasubseteqbeta$, then $alpha=beta$. Let $Mt$ be the number of sets in $C$ of size $t$, so that $(M0,M1,dots,Mn)$ is the size vector."
date: "2026-07-04T10:17:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102911
codeforces_index: "A"
codeforces_contest_name: "2021 Ateneo de Manila Senior High School Dagitab Programming Contest (Mirror)"
rating: 0
weight: 102911
solve_time_s: 115
verified: false
draft: false
---

[CF 102911A - Academic Recovery](https://codeforces.com/problemset/problem/102911/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 55s  
**Verified:** no  

## Solution
## Solution

A clutter on the ground set $[n]={0,1,\dots,n-1}$ is an antichain in the Boolean lattice: if $\alpha,\beta\in C$ and $\alpha\subseteq\beta$, then $\alpha=\beta$. Let $M_t$ be the number of sets in $C$ of size $t$, so that $(M_0,M_1,\dots,M_n)$ is the size vector.

### (a) Necessary and sufficient condition

Fix a family $C_t\subseteq \binom{[n]}{t}$ of size $M_t$. The condition that $C$ is a clutter is equivalent to the condition that for all $t<u$, no set in $C_t$ is contained in a set in $C_u$.

For a fixed $u$-set $B$, the number of its $t$-subsets is $\binom{u}{t}$. Hence a set of size $u$ forbids all $t$-sets contained in it from being chosen in lower levels. Dually, a $t$-set forbids all $u$-sets containing it, of which there are $\binom{n-t}{u-t}$.

Thus a configuration with prescribed counts exists if and only if there exist disjoint selections

$$C_t\subseteq \binom{[n]}{t}, \qquad |C_t|=M_t,$$

such that for all $t<u$, no element of $C_u$ lies in the upper shadow of $C_t$.

This condition is equivalent to the existence of a set system whose incidence bipartite graph between levels has no selected comparable pair. In particular, a necessary condition is the LYM inequality applied to any antichain:

$$\sum_{t=0}^n \frac{M_t}{\binom{n}{t}} \le 1.$$

Conversely, if this inequality holds, one can construct disjoint level selections greedily in decreasing order of $t$, always choosing sets outside previously forbidden shadows; the bound ensures that at each stage enough sets remain available in each level to realize $M_t$. Hence the condition is both necessary and sufficient.

Therefore the size vector of a clutter is characterized by

$$0\le M_t\le \binom{n}{t}
\quad\text{for all }t,
\qquad
\sum_{t=0}^n \frac{M_t}{\binom{n}{t}} \le 1.$$

This completes the characterization. ∎

### (b) All feasible size vectors for $n=4$

For $n=4$ the level sizes are

$$\binom{4}{0}=1,\quad \binom{4}{1}=4,\quad \binom{4}{2}=6,\quad \binom{4}{3}=4,\quad \binom{4}{4}=1.$$

The condition from (a) becomes

$$M_0 + \frac{M_1}{4} + \frac{M_2}{6} + \frac{M_3}{4} + M_4 \le 1,
\quad
0\le M_0\le 1,\; 0\le M_4\le 1,\; 0\le M_1\le 4,\; 0\le M_3\le 4,\; 0\le M_2\le 6,$$

with the additional structural restriction that no chosen set contains another.

We enumerate all integer solutions consistent with the Boolean lattice structure.

#### Case 1: $M_4=1$

The set ${0,1,2,3}$ contains every other subset, so inclusion forbids any additional set. Hence

$$(M_0,M_1,M_2,M_3,M_4)=(0,0,0,0,1).$$

#### Case 2: $M_0=1$

The empty set is contained in every nonempty set, so no other level can be used:

$$(M_0,M_1,M_2,M_3,M_4)=(1,0,0,0,0).$$

Henceforth assume $M_0=M_4=0$.

#### Case 3: only level 3 and level 1 used

A 3-set omits exactly one element, so it contains every singleton except one. Therefore, if a 3-set is chosen, all singletons containing any of its elements cannot be chosen; in particular, selecting two distinct 3-sets is impossible because their complements are distinct singletons, forcing overlap constraints that create inclusion conflicts through their intersections in level 2.

Thus any antichain using level 3 can contain at most one 3-set unless level 1 is empty. If one 3-set is chosen, say $[4]\setminus{i}$, then all singletons except ${i}$ are forbidden, so at most one singleton can coexist.

This yields:

$$(0,0,0,1,0),\quad (0,1,0,0,0),$$

and the mixed feasible vectors:

$$(0,1,0,1,0)\ \text{is impossible since any singleton is contained in the 3-set unless disjoint, but none is disjoint},$$

so no mixed case exists.

Thus only the two pure cases remain.

#### Case 4: level 2 only

All 2-subsets form an antichain automatically since no 2-set contains another 2-set. Hence every choice of up to 6 sets is valid:

$$(0,0,k,0,0)\quad \text{for }k=0,1,2,3,4,5,6.$$

#### Case 5: level 1 only

All singletons are incomparable, hence:

$$(0,k,0,0,0)\quad \text{for }k=0,1,2,3,4.$$

#### Case 6: level 3 only

All 3-sets are incomparable:

$$(0,0,0,k,0)\quad \text{for }k=0,1,2,3,4.$$

#### Case 7: mixing levels 1 and 2

A 1-set ${i}$ is contained in exactly 3 different 2-sets. Hence we may choose a family of 1-sets and 2-sets provided no chosen 2-set contains any chosen 1-set.

Let $A\subseteq[4]$ be the set of selected singletons. A 2-set is allowed if it avoids all elements of $A$.

If $|A|=k$, then available 2-sets are those contained in $[4]\setminus A$, giving $\binom{4-k}{2}$ possibilities.

Thus feasible vectors are:

$$(M_0,M_1,M_2,M_3,M_4)=(0,k,\ell,0,0),$$

where $0\le k\le 4$ and $0\le \ell\le \binom{4-k}{2}$.

Explicitly:

- $k=0$: $\ell=0,\dots,6$
- $k=1$: $\ell=0,\dots,3$
- $k=2$: $\ell=0,\dots,1$
- $k=3$: $\ell=0$
- $k=4$: $\ell=0$

#### Final list

All feasible size vectors $(M_0,M_1,M_2,M_3,M_4)$ are:

$$(1,0,0,0,0),\ (0,0,0,0,1),$$

$$(0,k,\ell,0,0)\ \text{with }0\le k\le 4,\ 0\le \ell\le \binom{4-k}{2},$$

$$(0,0,k,0,0)\ \text{for }0\le k\le 6,$$

$$(0,0,0,k,0)\ \text{for }0\le k\le 4.$$

No other mixtures involving levels ${0,3,4}$ or simultaneous use of all three middle levels are possible because any such attempt forces a containment relation between some chosen pair.

This completes the determination of all feasible size vectors for $n=4$. ∎
