---
title: "CF 104603M - Multiple Downloads"
description: "The solution does not correctly establish the existence of a sequence satisfying Definition R5 while enforcing the prefix constraint."
date: "2026-06-30T02:56:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104603
codeforces_index: "M"
codeforces_contest_name: "2023 Argentinian Programming Tournament (TAP)"
rating: 0
weight: 104603
solve_time_s: 61
verified: false
draft: false
---

[CF 104603M - Multiple Downloads](https://codeforces.com/problemset/problem/104603/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** no  

## Solution
## Correctness

The solution does not correctly establish the existence of a sequence satisfying Definition R5 while enforcing the prefix constraint. The central requirement of the exercise is to exhibit a construction compatible with $\infty$-distribution (Definition D / R5), but the argument assumes, without justification, that the set of sequences satisfying R5 is closed under arbitrary prefix constraints and that feasibility of prefixes can be extended step-by-step. This is not established and is not generally valid.

Additionally, the argument incorrectly treats R5-sequences as if they admit a simple tree extension property where every feasible prefix can be extended to a full R5 sequence. That property is not proven and is not immediate from the definition of $\infty$-distributed sequences, which are defined by limiting frequency conditions, not by a finitely branching consistency condition.

The conclusion that a greedy extension preserving the inequality can always be made is also unsupported and does not interact correctly with the global limiting-frequency constraints required by R5.

## Gaps and Errors

The first critical issue is the assumption that the set $\mathcal{R}$ of R5 sequences is nonempty and that one may fix a sequence $A \in \mathcal{R}$ without constructing it. While existence of normal sequences is known in TAOCP context, it is not justified here, and more importantly, it is irrelevant because the construction requires modifying the sequence while preserving $\infty$-distribution, which is not shown to be stable under prefix forcing.

This is a justification gap that affects the entire construction.

The second critical issue is the claim that “feasibility is preserved upward in the tree of prefixes of sequences in $\mathcal{R}$.” This implicitly assumes that every finite prefix that occurs in some R5 sequence can be extended to an R5 sequence, i.e., that the set of prefixes is extendable. This is equivalent to a compactness or Kolmogorov extension property, but no such theorem is established in the solution or in the referenced section.

This is a critical error because the greedy construction depends entirely on this property.

The third issue is the local extension argument comparing $s0$ and $s1$. The reasoning that one of them must preserve the prefix inequality is correct as a combinatorial observation, but it is irrelevant unless both candidates are guaranteed to remain feasible in $\mathcal{R}$. The argument never shows that feasibility and the inequality constraint can be satisfied simultaneously at every step.

This is a justification gap.

Finally, the appeal to “compactness of the full shift (König’s lemma)” is used as a black box to conclude existence of a global extension. However, the construction does not actually define a finitely branching tree of guaranteed feasible nodes, because feasibility is defined via asymptotic distribution conditions, not via finite constraints. Thus there is no established infinite tree whose nodes correspond exactly to R5-compatible prefixes.

This is a critical error.

## Summary

The proposed proof relies on an unproven and incorrect assumption that $\infty$-distributed sequences form a prefix-extendable tree structure, and it uses a greedy construction that does not preserve or control the global distribution constraints required by Definition R5. The main construction step is therefore invalid.

VERDICT: FAIL - the argument incorrectly assumes prefix-extendability of $\infty$-distributed sequences and does not justify preservation of Definition R5 under the construction.
