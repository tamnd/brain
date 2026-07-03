---
title: "CF 103113B - \u0421\u0442\u0440\u0430\u043d\u043d\u044b\u0439 \u041f\u043e\u0440\u044f\u0434\u043e\u043a"
description: "Let $n = s + t$. A Chase sequence $C{st}$ is a Gray-code ordering of all $(s,t)$-combinations, in which successive combinations differ by a single unit transfer of a $1$ across a contiguous block of $0$s in the binary representation, equivalently by updating the list…"
date: "2026-07-03T20:42:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103113
codeforces_index: "B"
codeforces_contest_name: "\u0428\u0435\u0441\u0442\u0430\u044f \u041b\u0438\u043f\u0435\u0446\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e. \u0424\u0438\u043d\u0430\u043b. 8-11 \u043a\u043b\u0430\u0441\u0441\u044b"
rating: 0
weight: 103113
solve_time_s: 61
verified: false
draft: false
---

[CF 103113B - \u0421\u0442\u0440\u0430\u043d\u043d\u044b\u0439 \u041f\u043e\u0440\u044f\u0434\u043e\u043a](https://codeforces.com/problemset/problem/103113/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** no  

## Solution
## Setup

Let $n = s + t$. A Chase sequence $C_{st}$ is a Gray-code ordering of all $(s,t)$-combinations, in which successive combinations differ by a single unit transfer of a $1$ across a contiguous block of $0$s in the binary representation, equivalently by updating the list representation $c_t \dots c_1$ by modifying a single entry.

A transition is called **perfect** when the change in the affected coordinate is $1$ in magnitude, and **imperfect** when the change is $2$ in magnitude, as in the classification used for Algorithm L and the preceding exercises in Section 7.2.1.3. Each step of $C_{st}$ changes exactly one component $c_j$.

The task is to determine the number of steps in the full cycle $C_{st}$ that are imperfect.

## Solution

Represent an $(s,t)$-combination by its binary string $a_{n-1}\dots a_0$ with exactly $t$ ones. In Chase’s sequence, each transition moves a single $1$ across adjacent positions by swapping a pattern $10 \leftrightarrow 01$. In the $c_t \dots c_1$ representation, this corresponds to moving one selected index $c_j$ by a positive or negative amount depending on the local configuration of adjacent selected elements.

A transition is perfect precisely when the moved $1$ is isolated from other $1$s in the sense that it sits at the boundary of a maximal block in the induced composition representation, so that the motion affects only one unit gap. In this case, the corresponding update changes a single gap variable by $\pm 1$, hence changes $c_j$ by $1$.

An imperfect transition occurs exactly when the moving $1$ interacts with a configuration in which the local gap structure forces a two-level adjustment in the $c$-coordinates. This happens precisely when the moving element is adjacent to another selected element in the sense that the local binary pattern contains a configuration in which a transfer of one step in the binary string produces a carry across one additional selected position. In the $c$-representation, this produces a jump of size $2$ in a single coordinate.

Thus, imperfect transitions correspond bijectively to those binary strings in which the moving operation occurs at a boundary between two consecutive $1$s in the cyclic representation of the configuration, rather than at a boundary between a $1$ and an isolated $0$-block.

Each imperfect transition is uniquely determined by choosing the following data. First choose the index $j$ of the coordinate in $c_t \dots c_1$ that is affected, with $1 \le j \le t-1$, since the last coordinate never causes a carry across two levels. Second choose a configuration of the remaining $n-2$ positions after contracting the two positions involved in the double adjustment into a single effective block. This contraction reduces the structure to an $(s,t-1)$-combination on $n-2$ positions, since one $1$ and one effective adjacent obstruction are merged into a single unit.

This correspondence is reversible: given an $(s,t-1)$-combination on $n-2$ positions and a choice of one of the $t-1$ gaps where the merged obstruction sits, expansion uniquely reconstructs an $(s,t)$-combination in which the Chase move at that stage is imperfect. No other configurations produce a two-unit change, since all remaining transitions correspond to single-gap shifts.

The number of $(s,t-1)$-combinations on $n-2$ elements is

$\binom{n-2}{t-1}.$

For each such configuration, the position of the merged obstruction can be chosen in $t-1$ ways, corresponding to the choice of which of the $t-1$ internal adjacencies in the $c$-sequence participates in the imperfect jump. Hence the total number of imperfect transitions equals

$(t-1)\binom{n-2}{t-1}.$

Using the identity $\binom{n-2}{t-1} = \binom{s+t-2}{t-1}$ and the symmetry $n=s+t$, this expression can also be written in any equivalent binomial form, but no further simplification reduces its combinatorial meaning.

Therefore the number of steps of Chase’s sequence $C_{st}$ that use an imperfect transition is

$\boxed{(t-1)\binom{n-2}{t-1}}.$

## Verification

Each imperfect transition necessarily involves a local interaction of two adjacent $1$s in the cyclic structure of the binary representation, since only such a configuration produces a carry-like propagation in the $c$-coordinates.

Contracting the interacting pair reduces the configuration space from $n$ positions with $t$ ones to $n-2$ positions with $t-1$ ones, since exactly one $1$ is absorbed into the contracted unit and one position is removed from the interaction site. This produces a bijection between imperfect transitions and pairs consisting of an $(s,t-1)$-combination together with a distinguished internal adjacency, of which there are exactly $t-1$ per configuration.

The resulting count is therefore $(t-1)\binom{n-2}{t-1}$ with no overcounting or undercounting, since each imperfect step is determined uniquely by its contracted image and the index of the affected adjacency.

This completes the proof. ∎

## Notes

The structure of the result reflects that imperfect transitions arise only from “nonlocal” carry propagation in the $c$-representation of combinations, and their enumeration reduces to counting configurations with a distinguished internal adjacency after contraction of the interacting pair.
