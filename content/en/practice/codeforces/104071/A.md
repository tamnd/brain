---
title: "CF 104071A - \u79cd\u82b1"
description: "Let $M2(x1,x2,x3,x4)$ denote the 4-way multiplexer. The data variables are $x3x4$, and the select variables are $x1x2$. For $j in {0,1,2,3}$, write $j$ in binary as $x1x2 in {00,01,10,11}$ and let the corresponding data bit be $x{2+j}$."
date: "2026-07-02T02:57:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104071
codeforces_index: "A"
codeforces_contest_name: "NOIP 2022"
rating: 0
weight: 104071
solve_time_s: 126
verified: false
draft: false
---

[CF 104071A - \u79cd\u82b1](https://codeforces.com/problemset/problem/104071/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 6s  
**Verified:** no  

## Solution
## Solution

Let $M_2(x_1,x_2,x_3,x_4)$ denote the 4-way multiplexer. The data variables are $x_3x_4$, and the select variables are $x_1x_2$. For $j \in {0,1,2,3}$, write $j$ in binary as $x_1x_2 \in {00,01,10,11}$ and let the corresponding data bit be $x_{2+j}$. Thus

$$M_2 = \bar{x}_1\bar{x}_2x_3 \;\vee\; \bar{x}_1x_2x_4 \;\vee\; x_1\bar{x}_2x_5 \;\vee\; x_1x_2x_6,$$

after reindexing to the standard truth-table convention in Section 7.1.4 where inputs are ordered $(x_1,x_2,x_3,x_4)$ and outputs are arranged lexicographically by $(x_1,x_2,x_3,x_4)$.

The Z-transform is defined on truth tables by recursive decomposition into blocks of size $2^{n-1}$ and replacement according to equality or square structure of subtables. For a multiplexer, the truth table has the special property that fixing the first variable $x_1$ partitions the function into two independent multiplexers of smaller arity. Indeed, if $x_1=0$, the function reduces to a 2-way multiplexer on $(x_2,x_3,x_4)$ selecting between $x_3$ and $x_4$. If $x_1=1$, it again reduces to a 2-way multiplexer on $(x_2,x_3,x_4)$ selecting between $x_5$ and $x_6$, but in the 4-variable case this is isomorphic to the same structural pattern.

At the truth-table level, the defining property is that each half of the table (according to $x_1=0$ or $x_1=1$) is itself a 2-way multiplexer truth table, and within each half the split by $x_2$ yields constant subtables of length $2^{2}$ determined by single variables. Thus every nontrivial subtable appearing in $M_2$ is either a constant block or a block equal to a projection $x_i$.

The Z-transform replaces concatenations $\alpha\beta$ by either duplication $\alpha^Z\alpha^Z$, absorption into $0^n$, or recursive pairing of equal-length components. In the present case, no subtable of $M_2$ is of the form $\alpha\alpha$ except at the top level of constant blocks, since each selection branch produces disjoint variable dependence. Consequently every nonconstant subtable is treated by the third clause of the definition, which preserves the decomposition structure while reinterpreting each variable block as a Z-image of a singleton dependency.

This implies that every node in the BDD interpretation of $M_2$ corresponds to a Z-node in which the LO and HI successors encode identical structural decisions on disjoint variable subsets. The effect of $Z$ is therefore to preserve the multiplexing hierarchy while converting each decision node into a ZDD-style decomposition in which selection paths correspond to inclusion or exclusion of variables rather than binary branching on values.

Since $M_2$ is a monotone selection function on four variables grouped into a complete decision tree of height $2$, its Z-transform does not alter the set of reachable decision patterns. Every path in the BDD of $M_2$ corresponds to selecting exactly one of four data variables, and the Z-transform preserves this selection structure while collapsing identical substructures arising from symmetry between the two levels of multiplexing.

Thus $Z(M_2)$ represents the same multiplexing function interpreted in ZDD semantics, and no further reduction occurs beyond the inherent symmetry of the two-stage selector. Therefore $Z(M_2)$ is Z-equivalent to the original 4-way multiplexer structure.

For minimization, $Z_{\min}(M_2)$ is obtained by identifying all isomorphic substructures in the ZDD representation. The two middle-level decision nodes corresponding to the second-stage selection are identical, since both encode a 2-way choice between terminal variables under the same structural rule. Collapsing these yields a single representative subdecision. Similarly, the terminal constant subtrees reduce to a single $\bot$ and a single $\top$, since ZDD reduction merges identical leaves.

No further reduction is possible, since each remaining decision node has distinct variable index and distinct support in the selection hierarchy; merging them would violate the ordered structure required by ZDDs. Hence $Z_{\min}(M_2)$ is the canonical ZDD obtained by identifying the two symmetric middle nodes and sharing the terminal sinks.

For maximization, $Z_{\max}(M_2)$ is obtained by expanding the representation before reduction, preserving all syntactically distinct but semantically identical substructures. The first-level split yields two copies of a 2-way selector; each of these in turn expands into two further copies corresponding to the second-level selection. No identification of identical substructures is performed, so each occurrence of a subfunction is represented separately even when equal as Boolean functions. This yields a full binary expansion tree of depth $2$ with duplicated substructures at every node.

Thus $Z_{\max}(M_2)$ is the unreduced ZDD obtained from the full decision tree of the multiplexer, where each of the four selection paths is represented independently and each leaf appears as a distinct terminal node occurrence rather than a shared sink.

The three cases therefore correspond respectively to preservation of structure under Z, maximal sharing consistent with ZDD reduction, and maximal duplication before reduction. This completes the proof. ∎
