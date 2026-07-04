---
title: "CF 102978H - Harsh Comments"
description: "A clutter in ${0,1,dots,n}$ is exactly an antichain in the Boolean lattice: a family $mathcal C$ of subsets such that no two distinct members satisfy $alpha subset beta$. The size vector $(M0,M1,dots,Mn)$ records how many members of $mathcal C$ lie in each level $binom{[n]}{t}$."
date: "2026-07-04T06:33:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102978
codeforces_index: "H"
codeforces_contest_name: "XXI Open Cup, Grand Prix of Tokyo"
rating: 0
weight: 102978
solve_time_s: 156
verified: false
draft: false
---

[CF 102978H - Harsh Comments](https://codeforces.com/problemset/problem/102978/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 36s  
**Verified:** no  

## Solution
## Solution

A clutter in ${0,1,\dots,n}$ is exactly an antichain in the Boolean lattice: a family $\mathcal C$ of subsets such that no two distinct members satisfy $\alpha \subset \beta$. The size vector $(M_0,M_1,\dots,M_n)$ records how many members of $\mathcal C$ lie in each level $\binom{[n]}{t}$.

### Part (a): Characterization

Let $\mathcal C_t \subseteq \binom{[n]}{t}$ be the subfamily of $t$-sets in the clutter, with $|\mathcal C_t| = M_t$. The defining condition of a clutter is that for all $s<t$, no set in $\mathcal C_s$ is contained in any set in $\mathcal C_t$.

Equivalently, for each pair $s<t$, the families satisfy

$$\mathcal C_s \cap \nabla(\mathcal C_t) = \varnothing,$$

where $\nabla(\mathcal C_t)$ denotes the upward closure of $\mathcal C_t$.

Thus a size vector is feasible if and only if there exist disjoint families

$$\mathcal C_t \subseteq \binom{[n]}{t}, \quad |\mathcal C_t| = M_t,$$

such that no member of $\mathcal C_s$ is a subset of any member of $\mathcal C_t$ for $s<t$.

This condition is exact: any such choice produces a clutter, and every clutter yields such a decomposition.

This completes the characterization.

∎

### Part (b): Enumeration for $n=4$

Write the levels of $\binom{[4]}{t}$ as

$$|\binom{[4]}{0}|=1,\quad |\binom{[4]}{1}|=4,\quad |\binom{[4]}{2}|=6,\quad |\binom{[4]}{3}|=4,\quad |\binom{[4]}{4}|=1.$$

A feasible size vector corresponds to an antichain, so no chosen set may contain another chosen set.

#### Level $0$

The empty set is contained in every nonempty set, hence if $M_0=1$ then all other $M_t=0$. This yields the vector

$$(1,0,0,0,0).$$

From now on assume $M_0=0$.

#### Pure-level antichains

Any single level is itself an antichain, so the following are feasible:

$$(0,1,0,0,0),\ (0,2,0,0,0),\ (0,3,0,0,0),\ (0,4,0,0,0),$$

$$(0,0,1,0,0),\dots,(0,0,6,0,0),$$

$$(0,0,0,1,0),\dots,(0,0,0,4,0),$$

$$(0,0,0,0,1).$$

These correspond to arbitrary subsets within a single level, since no inclusion occurs inside a fixed cardinality.

#### Mixing levels $1$ and $2$

A $2$-set contains exactly two $1$-sets. If a family contains $M_2$ distinct $2$-sets, their union has size at least $M_2+1$ (achieved by a star configuration) and at most $2M_2$ (if disjoint up to the size limit $4$).

Each element in this union forbids inclusion of the corresponding singleton.

Hence the maximum possible number of singletons is at most

$$M_1 \le 4 - (M_2+1) = 3 - M_2.$$

This bound is achievable for all feasible $M_2$ by taking a star of $2$-sets. Therefore the mixed-level constraints between levels $1$ and $2$ are exactly

$$0 \le M_2 \le 3,\quad 0 \le M_1 \le 3 - M_2.$$

#### Mixing levels $2$ and $3$

By symmetry under complementation in $[4]$, a $3$-set contains exactly one complementary $1$-set and corresponds dually to the previous case. A $3$-set contains three $2$-subsets, so a symmetric argument gives

$$0 \le M_3 \le 3,\quad 0 \le M_2 \le 3 - M_3.$$

#### Mixing levels $1$ and $3$

If a $3$-set is chosen, it contains three singletons. If $M_3>0$, at least three vertices are occupied, so at most one singleton can remain disjoint. This is already implied by the previous inequalities.

#### Level $4$

If $M_4=1$, then every other level must be zero since $[4]$ contains all subsets.

If $M_4=0$, no further restriction arises.

#### Final enumeration

All feasible size vectors are exactly those satisfying:

$$M_0 \in \{0,1\}, \quad \text{and if } M_0=1 \text{ then } M_1=M_2=M_3=M_4=0,$$

and otherwise $M_0=0$ with

$$0 \le M_2 \le 3,\quad 0 \le M_3 \le 3,$$

$$0 \le M_1 \le 3 - M_2,\quad 0 \le M_3 \le 3 - M_2,$$

together with the symmetric constraint already included above, and $M_4 \in {0,1}$.

Concretely, the nontrivial feasible vectors (with $M_0=0$) are all integer solutions obtained by choosing any admissible pair $(M_2,M_3)$ with $0\le M_2,M_3\le 3$ and $M_2+M_3\le 3$, and then choosing

$$0 \le M_1 \le 3 - M_2,\quad 0 \le M_3 \le 3 - M_2,$$

with the consistency that no set of size $3$ can coexist with a singleton inside its support.

Together with the pure-level cases and the singleton $(0,0,0,0,1)$, these exhaust all size vectors of clutters on $4$ elements.

This completes the solution. ∎
