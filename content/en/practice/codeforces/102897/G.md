---
title: "CF 102897G - New Game"
description: "Let $C subseteq mathcal{P}({0,1,dots,n-1})$ be a clutter, meaning that no two distinct sets in $C$ are comparable under inclusion. Let $Mt$ denote the number of $t$-element sets in $C$."
date: "2026-07-04T10:13:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102897
codeforces_index: "G"
codeforces_contest_name: "The 3rd Hangzhou Normal University Freshman Programming Contest"
rating: 0
weight: 102897
solve_time_s: 154
verified: false
draft: false
---

[CF 102897G - New Game](https://codeforces.com/problemset/problem/102897/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 34s  
**Verified:** no  

## Solution
## Solution

Let $C \subseteq \mathcal{P}({0,1,\dots,n-1})$ be a clutter, meaning that no two distinct sets in $C$ are comparable under inclusion. Let $M_t$ denote the number of $t$-element sets in $C$.

For each $t$, write $C_t = {\alpha \in C : |\alpha| = t}$ so that $|C_t| = M_t$ and $C = \bigcup_{t=0}^n C_t$ is a disjoint union.

### (a) Necessary and sufficient condition

For a fixed integer $k$, consider a $k$-subset $S \subseteq {0,1,\dots,n-1}$. The set $S$ is forbidden if and only if it lies inside some set $T \in C_t$ with $t>k$. For such a fixed $T$, the number of $k$-subsets contained in $T$ equals $\binom{t}{k}$. Therefore, if all level sets $C_t$ are chosen, the total number of incidences between chosen larger sets and $k$-subsets is

$$\sum_{t=k+1}^n M_t \binom{t}{k}.$$

Each such incidence accounts for a potential obstruction, and every forbidden $k$-set must lie in this union. Hence the number of $k$-sets that remain available for level $k$ is at most

$$\binom{n}{k} - \sum_{t=k+1}^n M_t \binom{t}{k}.$$

Since the sets in $C_k$ must all be chosen among the available $k$-subsets, a necessary condition is

$$M_k \le \binom{n}{k} - \sum_{t=k+1}^n M_t \binom{t}{k}.
\tag{1}$$

This inequality is also sufficient. Indeed, process the levels in decreasing order of size. Choose any $M_n$ sets at level $n$. Having chosen all levels above $k$, at most $\sum_{t=k+1}^n M_t \binom{t}{k}$ distinct $k$-subsets are excluded, so at least the right-hand side of (1) remain available. The hypothesis (1) ensures that $M_k$ choices can be made at level $k$ without violating incomparability with previously chosen sets. Proceeding downward constructs a clutter realizing the vector $(M_0,M_1,\dots,M_n)$.

Thus a vector is feasible if and only if all inequalities (1) hold for $k=0,1,\dots,n$.

This completes part (a). ∎

### (b) Enumeration for $n=4$

For $n=4$, the inequalities (1) become explicit constraints.

For $k=4$,

$$M_4 \le 1.$$

For $k=3$,

$$M_3 \le 4 - M_4 \binom{4}{3} = 4 - 4M_4.$$

For $k=2$,

$$M_2 \le 6 - 3M_3 - 6M_4.$$

For $k=1$,

$$M_1 \le 4 - 2M_2 - 3M_3 - 4M_4.$$

For $k=0$,

$$M_0 \le 1 - (M_1 + M_2 + M_3 + M_4).$$

The last inequality forces

$$M_0 + M_1 + M_2 + M_3 + M_4 \le 1,$$

so at most one of the entries $M_1,M_2,M_3,M_4$ can be nonzero, and $M_0$ is determined accordingly.

We now examine all possibilities.

If all $M_1=M_2=M_3=M_4=0$, then $M_0$ satisfies $0 \le M_0 \le 1$, hence $M_0 \in {0,1}$, giving

$$(0,0,0,0,0), \quad (1,0,0,0,0).$$

If $M_1=1$ and all others except $M_0$ are zero, then all inequalities are satisfied and $M_0=0$, giving

$$(0,1,0,0,0).$$

If $M_2=1$ and all others zero except possibly $M_0$, then $M_0=0$, giving

$$(0,0,1,0,0).$$

If $M_3=1$ and all others zero except possibly $M_0$, then $M_0=0$, giving

$$(0,0,0,1,0).$$

If $M_4=1$ and all others zero except possibly $M_0$, then $M_0=0$, giving

$$(0,0,0,0,1).$$

No other choice is possible because any two positive entries among $M_1,\dots,M_4$ would violate $M_0 \ge 0$.

Thus all feasible size vectors for $n=4$ are

$$(0,0,0,0,0),\ (1,0,0,0,0),\ (0,1,0,0,0),\ (0,0,1,0,0),\ (0,0,0,1,0),\ (0,0,0,0,1).$$

This completes the solution. ∎
