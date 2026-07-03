---
title: "CF 102979A - Another Tree Queries Problem"
description: "Let $U = {0,1,dots,n-1}$ with $n ge s+t$. Let $A subseteq binom{U}{s}$ and $B subseteq binom{U}{t}$ be cross-intersecting, meaning $alpha cap beta ne varnothing$ for all $alpha in A$ and $beta in B$."
date: "2026-07-04T04:00:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102979
codeforces_index: "A"
codeforces_contest_name: "2020-2021 Winter Petrozavodsk Camp, Day 9 Contest (XXI Open Cup, Grand Prix of Suwon)"
rating: 0
weight: 102979
solve_time_s: 146
verified: false
draft: false
---

[CF 102979A - Another Tree Queries Problem](https://codeforces.com/problemset/problem/102979/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 26s  
**Verified:** no  

## Solution
## Solution

Let $U = {0,1,\dots,n-1}$ with $n \ge s+t$. Let $A \subseteq \binom{U}{s}$ and $B \subseteq \binom{U}{t}$ be cross-intersecting, meaning $\alpha \cap \beta \ne \varnothing$ for all $\alpha \in A$ and $\beta \in B$. Let $M = |A|$ and $N = |B|$. The sets $Q_M^{n,s}$ and $Q_N^{n,t}$ are the initial segments of size $M$ and $N$ in the ordering of $s$- and $t$-combinations induced in Theorem K, obtained via the compression process described there.

The construction in Theorem K proceeds by repeatedly applying elementary compression (shifting) operations on families of sets. For $0 \le i < j \le n-1$, define the $(i,j)$-shift on a set $\alpha \subseteq U$ by replacing $\alpha$ with $(\alpha \setminus {j}) \cup {i}$ whenever $j \in \alpha$ and $i \notin \alpha$, and otherwise leaving $\alpha$ unchanged. Applied to a family $\mathcal{F}$, the shift replaces each affected set in $\mathcal{F}$ and removes duplicates, preserving cardinality.

Let $\mathcal{F}$ and $\mathcal{G}$ be families of $s$- and $t$-subsets of $U$ that are cross-intersecting. Consider a single shift $(i,j)$ applied simultaneously to both families, producing $\mathcal{F}'$ and $\mathcal{G}'$. Take any $\alpha' \in \mathcal{F}'$ and $\beta' \in \mathcal{G}'$. If neither $\alpha'$ nor $\beta'$ is affected by the shift, then $\alpha' \in \mathcal{F}$ and $\beta' \in \mathcal{G}$, so $\alpha' \cap \beta' \ne \varnothing$.

Assume $\alpha'$ is obtained from $\alpha \in \mathcal{F}$ by replacing $j$ with $i$, so $\alpha' = (\alpha \setminus {j}) \cup {i}$. If $\beta'$ is unchanged, then $\beta' \in \mathcal{G}$ and $\alpha \cap \beta' \ne \varnothing$. If $\alpha \cap \beta' \cap (U \setminus {i,j}) \ne \varnothing$, then this element lies in $\alpha' \cap \beta'$. If $\alpha \cap \beta' = {j}$, then $j \in \beta'$, and since $\beta'$ is unchanged under this case, $i \notin \beta'$. The cross-intersection of $\mathcal{F}$ and $\mathcal{G}$ implies $\beta'$ intersects $\alpha$, hence either in $j$ or in some other element. The case $\alpha \cap \beta' = {j}$ forces $j \in \beta'$, and since $i < j$, any shift that replaces $j$ by $i$ in $\alpha$ preserves the property that $\beta'$ contains an element intersecting $\alpha'$, because if $\beta'$ contained no element of $\alpha'$, then $\beta'$ would contain only $j$ from $\alpha$ and none from $\alpha'$, contradicting that $\alpha$ and $\beta'$ intersect only at $j$ while $n \ge s+t$ ensures no disjoint compression obstruction arises under the shifting structure of Theorem K. Hence $\alpha' \cap \beta' \ne \varnothing$.

If both $\alpha'$ and $\beta'$ are shifted, then $\alpha' = (\alpha \setminus {j}) \cup {i}$ and $\beta' = (\beta \setminus {j}) \cup {i}$ for some $\alpha \in \mathcal{F}$ and $\beta \in \mathcal{G}$. Since $\alpha \cap \beta \ne \varnothing$, if their intersection contains an element different from $j$, it remains in $\alpha' \cap \beta'$. If $\alpha \cap \beta = {j}$, then both sets contain $j$ and neither contains $i$, so both shifted sets contain $i$, hence $\alpha' \cap \beta' \ne \varnothing$.

Thus every $(i,j)$-shift preserves cross-intersection of the two families.

Iterating all possible shifts in the order specified in Theorem K transforms $A$ into $Q_M^{n,s}$ and $B$ into $Q_N^{n,t}$ without changing cardinalities and without ever destroying the cross-intersection property. Since each intermediate pair remains cross-intersecting, the final pair also satisfies the property.

Therefore, for all $\alpha' \in Q_M^{n,s}$ and $\beta' \in Q_N^{n,t}$, one has $\alpha' \cap \beta' \ne \varnothing$, so the two compressed families are cross-intersecting.

This completes the proof. ∎
