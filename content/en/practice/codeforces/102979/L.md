---
title: "CF 102979L - Lights On The Road"
description: "Theorem W is proved in Section 7.2.1.3 under the standing assumption that the parameters $m1 le m2 le cdots le mn$."
date: "2026-07-04T03:44:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102979
codeforces_index: "L"
codeforces_contest_name: "2020-2021 Winter Petrozavodsk Camp, Day 9 Contest (XXI Open Cup, Grand Prix of Suwon)"
rating: 0
weight: 102979
solve_time_s: 149
verified: false
draft: false
---

[CF 102979L - Lights On The Road](https://codeforces.com/problemset/problem/102979/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 29s  
**Verified:** no  

## Solution
## Solution

Theorem W is proved in Section 7.2.1.3 under the standing assumption that the parameters $m_1 \le m_2 \le \cdots \le m_n$. The conclusion describes a uniform recursive structure of cross-order segments in the torus $T(m_1,\dots,m_n)$, expressed through a spread function $\alpha$ that is independent of the slice index. Exercise 92 isolates the key invariant used in the proof: for a standard set $S \subseteq T(m_1,\dots,m_{n-1},m)$, the fiber sizes $N_a$ satisfy

$$N_{m-1}=N,\qquad N_{a-1}=\alpha N_a \quad (1 \le a < m),$$

where $\alpha$ depends only on standard sets in $T(m_1,\dots,m_{n-1})$.

### (a) Counterexample when the parameters are not sorted

Take $n=2$ and the unsorted parameters $(m_1,m_2)=(3,2)$. The torus is

$$T(3,2)=\{(i,j)\mid 0\le i<3,\ 0\le j<2\}.$$

List its elements in cross order as induced in the construction used in Theorem W (which reduces to lexicographic order when applied coordinatewise in the proof):

$$(0,0),(0,1),(1,0),(1,1),(2,0),(2,1).$$

Let $S$ be the initial segment consisting of the first $N=3$ elements:

$$S=\{(0,0),(0,1),(1,0)\}.$$

Define fiber counts with respect to the second coordinate (the role played by the last coordinate in the inductive step of Theorem W):

$$N_a = |\{(i,a)\in S\}|.$$

Then

$$N_0=2,\qquad N_1=1.$$

If the conclusion of Theorem W were valid without ordering, there would exist a constant $\alpha$ such that

$$N_0 = \alpha N_1.$$

This forces $\alpha=2$.

Now extend one more step in the same initial segment construction to $N=4$:

$$S'=\{(0,0),(0,1),(1,0),(1,1)\}.$$

Then

$$N_0'=2,\qquad N_1'=2.$$

The same rule would require $N_0'=\alpha N_1'$, hence $\alpha=1$.

The contradiction $\alpha=2$ and $\alpha=1$ shows that no single spread parameter can satisfy the conclusion of Theorem W for all initial segments in $T(3,2)$. Hence the theorem fails when the parameters are not in nondecreasing order, and $N=3$ already provides a witness where the structure breaks.

### (b) Where the proof uses the ordering hypothesis

The proof of Theorem W uses the condition

$$m_1 \le m_2 \le \cdots \le m_n$$

at the point where slices of a standard set in $T(m_1,\dots,m_n)$ are compared after projecting onto coordinate subtoruses.

In the inductive step, the argument assumes that when a coordinate is fixed at level $a$, the remaining structure behaves like a standard set in a smaller torus with a well-defined spread function that is independent of which coordinate is chosen last. This independence relies on the fact that enlarging a coordinate direction does not produce a smaller “bottleneck” than earlier coordinates, so the compression and cross-order arguments preserve monotonicity of the fiber structure.

When the ordering hypothesis is dropped, the proof breaks precisely at the step where one identifies a uniform spread function $\alpha$ across all coordinates. If some $m_i > m_{i+1}$, then projecting onto coordinate $i$ and coordinate $i+1$ yields incompatible growth rates for corresponding slices, and the inductive identification of a single $\alpha$ fails. This invalidates the transition from local compression behavior in $T(m_1,\dots,m_{n-1})$ to a global recurrence for $T(m_1,\dots,m_n)$.

This completes the proof. ∎
