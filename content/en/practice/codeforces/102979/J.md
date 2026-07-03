---
title: "CF 102979J - Junkyeom's Contest"
description: "Let $U$ denote the set underlying the multicombinations (92). In the representation (6), each multicombination is a nonincreasing sequence $$dt ge d{t-1} ge cdots ge d1,qquad s ge dt,$$ and its complement with respect to $U$ is formed by taking the elements of $U$ not…"
date: "2026-07-04T04:10:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102979
codeforces_index: "J"
codeforces_contest_name: "2020-2021 Winter Petrozavodsk Camp, Day 9 Contest (XXI Open Cup, Grand Prix of Suwon)"
rating: 0
weight: 102979
solve_time_s: 138
verified: false
draft: false
---

[CF 102979J - Junkyeom's Contest](https://codeforces.com/problemset/problem/102979/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 18s  
**Verified:** no  

## Solution
## Solution

Let $U$ denote the set underlying the multicombinations (92). In the representation (6), each multicombination is a nonincreasing sequence

$$d_t \ge d_{t-1} \ge \cdots \ge d_1,\qquad s \ge d_t,$$

and its complement with respect to $U$ is formed by taking the elements of $U$ not represented by the given selection, then writing them again as a nonincreasing sequence of the same type. The hint lists these complements explicitly:

$$3211,\;3210,\;3200,\;3110,\;3100,\;3000,\;2110,\;2100,\;2000,\;1100,\;1000.$$

In the setting of (92), every object in $U$ is represented exactly once either by membership in a multicombination or by membership in its complement, so complementation defines a mapping

$$\mathcal{C}: \mathcal{M}_{s,t} \to \mathcal{M}_{t,s},$$

where $\mathcal{M}_{s,t}$ denotes the set of multicombinations (92). The definition uses only set complement inside $U$, hence for any multicombination $A \subseteq U$,

$$\mathcal{C}(A) = U \setminus A.$$

Applying complement twice restores the original set, since

$$U \setminus (U \setminus A) = A,$$

so $\mathcal{C}$ is an involution. This implies that $\mathcal{C}$ is a bijection between the family of objects under consideration and its image.

The structure of (92) is symmetric in the parameters $s$ and $t$ because the complement of a choice of $t$ elements from an $(s+t)$-element universe is a choice of $s$ elements from the same universe. In the multicombination encoding (6), this symmetry corresponds to replacing the sequence $(d_t,\dots,d_1)$ by the complementary sequence listed in the hint, which is again nonincreasing and satisfies the same bounds with $s$ and $t$ interchanged.

Hence the complement operation transforms every configuration counted in the $\partial$ half of Corollary C into a unique configuration counted in the opposite $\partial$ half, and conversely, since $\mathcal{C}$ is its own inverse. This establishes a bijection between the two classes.

Therefore any identity or statement proved for one $\partial$ half holds for the other $\partial$ half by transporting objects through the complement bijection.

This completes the proof. ∎
