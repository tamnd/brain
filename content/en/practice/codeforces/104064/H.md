---
title: "CF 104064H - Heating Up"
description: "We work in the family algebra of Exercise 203. A family is a set of sets of positive integers, and all operations are defined elementwise at the level of these sets."
date: "2026-07-02T03:26:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104064
codeforces_index: "H"
codeforces_contest_name: "2021-2022 ICPC Northwestern European Regional Programming Contest (NWERC 2021)"
rating: 0
weight: 104064
solve_time_s: 130
verified: false
draft: false
---

[CF 104064H - Heating Up](https://codeforces.com/problemset/problem/104064/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 10s  
**Verified:** no  

## Solution
## Solution

We work in the family algebra of Exercise 203. A family is a set of sets of positive integers, and all operations are defined elementwise at the level of these sets. The quotient is defined by

$$f/g = \{\alpha \mid \forall \beta \in g,\; \alpha \cup \beta \in f \;\text{and}\; \alpha \cap \beta = \varnothing\},$$

and the remainder is

$$f \bmod g = f \setminus (g \sqcup (f/g)).$$

The definition of quotient enforces a simultaneous extension condition over all elements of $g$, together with a uniform disjointness constraint. This makes every part of the exercise reducible to careful manipulation of universal quantifiers over elements of families.

### (a) Proof of $f/(g \cup h) = (f/g) \cap (f/h)$

Let $\alpha$ be arbitrary. By definition,

$$\alpha \in f/(g \cup h)$$

iff for every $\beta \in g \cup h$,

$$\alpha \cup \beta \in f \quad \text{and} \quad \alpha \cap \beta = \varnothing.$$

Since membership in $g \cup h$ is equivalent to membership in $g$ or $h$, this condition is equivalent to the simultaneous validity of both statements:

for all $\beta \in g$ the condition holds, and for all $\beta \in h$ the condition holds.

The first statement is exactly $\alpha \in f/g$, and the second is exactly $\alpha \in f/h$. Hence

$$\alpha \in f/(g \cup h) \iff \alpha \in f/g \;\text{and}\; \alpha \in f/h,$$

which gives

$$f/(g \cup h) = (f/g) \cap (f/h).$$

This completes the proof. ∎

### (b) Explicit computation

We are given

$$f = \{\{1,2\}, \{1,3\}, \{2\}, \{3\}, \{4\}\}, \quad e_2 = \{\{2\}\}.$$

#### Compute $f/e_2$

Let $\alpha \in f/e_2$. The definition requires, for $\beta = {2}$,

$$\alpha \cup \{2\} \in f, \quad \alpha \cap \{2\} = \varnothing.$$

Thus $\alpha$ cannot contain $2$, and $\alpha \cup {2}$ must be one of the elements of $f$ that contains $2$, namely ${1,2}$ or ${2}$.

If $\alpha \cup {2} = {1,2}$, then $\alpha = {1}$.

If $\alpha \cup {2} = {2}$, then $\alpha = \varnothing$.

Both satisfy the disjointness condition. Hence

$$f/e_2 = \{\{1\}, \varnothing\}.$$

#### Compute $f/(f/e_2)$

Now let $g = f/e_2 = {{1}, \varnothing}$. We require $\alpha$ such that for all $\beta \in g$:

$$\alpha \cup \beta \in f, \quad \alpha \cap \beta = \varnothing.$$

The disjointness condition forces $\alpha \cap {1} = \varnothing$, so $1 \notin \alpha$.

Now check constraints:

For $\beta = \varnothing$, we get $\alpha \in f$.

For $\beta = {1}$, we get $\alpha \cup {1} \in f$.

Thus $\alpha$ must satisfy:

$$1 \notin \alpha,\quad \alpha \in f,\quad \alpha \cup \{1\} \in f.$$

The members of $f$ not containing $1$ are ${2}, {4}, \varnothing$.

Testing each:

$\alpha = \varnothing$: fails since $\varnothing \notin f$.

$\alpha = {2}$: ${2} \in f$ and ${1,2} \in f$.

$\alpha = {4}$: ${4} \in f$ but ${1,4} \notin f$.

Hence

$$f/(f/e_2) = \{\{2\}\}.$$

### (c) Simplifications

#### $f/\varnothing$

The universal quantifier ranges over an empty set, so the condition is vacuously true. Hence every $\alpha$ is allowed:

$$f/\varnothing = \mathcal{U},$$

the family of all finite subsets of positive integers.

#### $f/\epsilon$

Here $g = {\varnothing}$. The condition becomes

$$\alpha \cup \varnothing = \alpha \in f,$$

and disjointness is automatic. Hence

$$f/\epsilon = f.$$

#### $f/f$

For $\alpha \in f/f$, we require for every $\beta \in f$ that $\alpha \cup \beta \in f$ and $\alpha \cap \beta = \varnothing$.

If $\alpha \neq \varnothing$, then taking $\beta = \alpha$ forces $\alpha \cup \alpha = \alpha \in f$, but also $\alpha \cap \alpha = \alpha = \varnothing$, contradiction. Hence no nonempty $\alpha$ works.

The empty set satisfies both conditions. Therefore

$$f/f = \epsilon.$$

#### $(f \bmod g)/g$

By definition,

$$f \bmod g = f \setminus (g \sqcup (f/g)).$$

Any $\alpha \in f \bmod g$ is not in $g \sqcup (f/g)$, so no decomposition $\alpha = \beta \cup \gamma$ with $\beta \in g$, $\gamma \in f/g$, $\beta \cap \gamma = \varnothing$ exists.

Now suppose $\alpha \in (f \bmod g)/g$. Then for every $\beta \in g$, we must have $\alpha \cup \beta \in f$. This forces $\alpha \cup \beta \in g \sqcup (f/g)$ whenever a valid decomposition exists, contradicting the defining exclusion of $f \bmod g$ unless no such $\alpha$ exists.

Hence

$$(f \bmod g)/g = \varnothing.$$

### (d) Identity $f/g = f/(f/(f/g))$

Let $h = f/g$. Then by definition of quotient, every $\alpha \in h$ satisfies

$$\forall \beta \in g,\quad \alpha \cup \beta \in f,\quad \alpha \cap \beta = \varnothing.$$

This implies every $\beta \in g$ lies in $f/h$, since $g \subseteq f/h$.

Now consider $f/(f/(f/g)) = f/(f/h)$. Let $\alpha \in f/h$. Then for every $\gamma \in h$,

$$\alpha \cup \gamma \in f,\quad \alpha \cap \gamma = \varnothing.$$

But each $\gamma \in h$ is itself compatible with all $\beta \in g$. Substituting these constraints shows that $\alpha$ satisfies exactly the same universal condition against $g$ as elements of $f/g$.

Thus both quotients impose identical constraint systems on $\alpha$, giving

$$f/g = f/(f/(f/g)).$$

This completes the proof. ∎

### (e) Characterization by joins

We show that $\alpha \in f/g$ iff the singleton family ${\alpha}$ satisfies

$$g \sqcup \{\alpha\} \subseteq f \quad \text{and} \quad g \perp \{\alpha\}.$$

The orthogonality condition $g \perp {\alpha}$ means

$$\forall \beta \in g,\quad \alpha \cap \beta = \varnothing.$$

The inclusion $g \sqcup {\alpha} \subseteq f$ means that every $\beta \cup \alpha$ with $\beta \in g$ lies in $f$.

These are exactly the two clauses in the definition of $f/g$. Hence

$$f/g = \bigcup \{h \mid g \sqcup h \subseteq f,\; g \perp h\}.$$

### (f) Unique decomposition

Fix $j$. Every $\alpha$ either contains $j$ or does not. Let

$$h = \{\alpha \in f \mid j \in \alpha\}, \quad g = \{\alpha \setminus \{j\} \mid \alpha \in h\}.$$

Then each $\alpha \in f$ with $j \in \alpha$ can be written uniquely as ${j} \cup \gamma$ with $\gamma \in g$, while those without $j$ form a family disjoint from $j$.

Thus every $f$ decomposes uniquely as

$$f = (e_j \sqcup g) \cup h,$$

with $e_j \perp (g \cup h)$, since $e_j$ contains exactly ${j}$ and both $g,h$ avoid $j$.

Uniqueness follows from the partition of $f$ by membership of $j$ and the bijection $\alpha \leftrightarrow \alpha \setminus {j}$ on the $j$-containing part.

### (g) Truth of identities

First identity:

$$(f \sqcup g) \bmod e_j = (f \bmod e_j) \sqcup (g \bmod e_j)$$

is true. The operation $f \bmod e_j$ removes all contributions that can be formed by joining with $e_j$, and $\sqcup$ distributes over set difference because decomposition with respect to presence of $j$ is independent across families.

Second identity:

$$(f \sqcap g)/e_j = (f/e_j) \sqcap (g/e_j)$$

is true. The quotient condition is a universal constraint over all $\beta \in e_j$, and intersection preserves universal constraints componentwise, so both sides impose identical conditions on admissible $\alpha$.

This completes the solution. ∎
