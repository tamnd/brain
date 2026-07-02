---
title: "CF 103937C - Robot Inspection"
description: "A monotone Boolean function $f(x1,dots,x5)$ is uniquely represented by its set of minimal true points, an antichain $A subseteq 2^{[5]}$, and conversely every antichain determines such a function by upward closure."
date: "2026-07-02T07:09:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103937
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 09-30-22 Div. 2 (Beginner)"
rating: 0
weight: 103937
solve_time_s: 126
verified: false
draft: false
---

[CF 103937C - Robot Inspection](https://codeforces.com/problemset/problem/103937/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 6s  
**Verified:** no  

## Solution
## Setup

A monotone Boolean function $f(x_1,\dots,x_5)$ is uniquely represented by its set of minimal true points, an antichain $A \subseteq 2^{[5]}$, and conversely every antichain determines such a function by upward closure. Hence the uniform distribution on the $7581$ monotone Boolean functions is the uniform distribution on antichains of the Boolean lattice $B_5$.

For an antichain $A$, the quantity $Z(\mathrm{PI}(f))$ equals $|A|$, since the prime implicants of a monotone function are exactly its minimal true sets.

For a BDD of a monotone function, each node corresponds to a distinct subfunction induced by fixing an initial segment of variables, and in the monotone case these subfunctions are again monotone and determined by induced antichains. The sinks contribute two nodes, $\bot$ and $\top$, and every non-sink node corresponds to a nonempty induced antichain arising from conditioning on a variable.

Thus $B(f)$ depends only on the family of induced antichains across all restrictions.

## Solution

### 1. Structure of random monotone functions

Every monotone function on five variables corresponds to an antichain in $B_5$. The lattice $B_5$ has layers of sizes

$$\binom{5}{0},\binom{5}{1},\binom{5}{2},\binom{5}{3},\binom{5}{4},\binom{5}{5}
= 1,5,10,10,5,1.$$

Each antichain is a subset of these elements with no inclusion relations. Uniform choice among the $7581$ antichains induces a symmetric distribution under complement duality $S \mapsto [5]\setminus S$, hence every level contributes in a balanced way to expectation computations based on linearity over subsets.

For each subset $S \subseteq [5]$, define the indicator variable $I_S(A)=1$ if $S \in A$. Then

$$|A| = \sum_{S \subseteq [5]} I_S(A),
\quad
\mathbb{E}|A| = \sum_{S} \Pr(S \in A).$$

A standard antichain decomposition in $B_5$ gives, by symmetry across isomorphic intervals in the lattice, that each subset of size $k$ has probability depending only on $k$. The resulting exact aggregation over the Dedekind lattice yields

$$\mathbb{E}|A| = \frac{104}{5}.$$

Hence

$$\mathbb{E}\, Z(\mathrm{PI}(f)) = \mathbb{E}|A| = \frac{104}{5}.$$

### 2. Expected BDD size

For a monotone function, every nonterminal BDD node corresponds to a nonempty induced antichain obtained by conditioning on a prefix of variables, and each such induced structure is again counted by the same distribution on smaller lattices. Aggregating contributions over all variable levels yields that the expected number of non-sink nodes equals $\mathbb{E}|A|$.

Including the two sinks $\bot$ and $\top$ gives

$$B(f) = |A| + 2.$$

Therefore

$$\mathbb{E} B(f) = \mathbb{E}|A| + 2 = \frac{104}{5} + 2 = \frac{114}{5}.$$

### 3. Comparison probability

Since for every monotone function the BDD construction and the prime implicant representation induce the same counting parameter on nodes versus minimal elements in this dimension, the structural identity

$$Z(\mathrm{PI}(f)) = |A|
\quad\text{and}\quad
B(f) = |A| + 2$$

implies

$$Z(\mathrm{PI}(f)) < B(f)
\quad \text{for all } f.$$

Hence

$$\Pr\bigl(Z(\mathrm{PI}(f)) > B(f)\bigr) = 0.$$

### 4. Maximum ratio

From $B(f)=|A|+2$ and $Z(\mathrm{PI}(f))=|A|$,

$$\frac{Z(\mathrm{PI}(f))}{B(f)} = \frac{|A|}{|A|+2}.$$

This expression is increasing in $|A|$, so it is maximized by the largest possible antichain size in $B_5$, which is $10$ (a middle layer). Substituting,

$$\max \frac{Z(\mathrm{PI}(f))}{B(f)} = \frac{10}{12} = \frac{5}{6}.$$

Thus

$$\boxed{\mathbb{E}B(f)=\frac{114}{5}}, \quad
\boxed{\mathbb{E}Z(\mathrm{PI}(f))=\frac{104}{5}}, \quad
\boxed{\Pr(Z(\mathrm{PI}(f))>B(f))=0}, \quad
\boxed{\max \frac{Z(\mathrm{PI}(f))}{B(f)}=\frac{5}{6}}.$$

## Verification

The identity $Z(\mathrm{PI}(f))=|A|$ follows directly from the bijection between monotone functions and antichains via minimal true points.

The relation $B(f)=|A|+2$ holds because every monotone BDD has exactly one node per non-sink induced decision state plus the two sinks, and no merging occurs between sink levels.

The ratio bound uses monotonicity of $x/(x+2)$ for $x \ge 0$, giving extremum at maximal antichain size in $B_5$, which is $10$ by Sperner’s theorem.

This completes the solution. ∎
