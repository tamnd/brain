---
title: "CF 102979G - Generate The Array"
description: "Let Theorem W be applied to the torus $T(m1,dots,mn)$ with cross order as in Section 7.2.1.3, and let $S$ be an initial segment in that order."
date: "2026-07-04T03:30:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102979
codeforces_index: "G"
codeforces_contest_name: "2020-2021 Winter Petrozavodsk Camp, Day 9 Contest (XXI Open Cup, Grand Prix of Suwon)"
rating: 0
weight: 102979
solve_time_s: 163
verified: false
draft: false
---

[CF 102979G - Generate The Array](https://codeforces.com/problemset/problem/102979/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 43s  
**Verified:** no  

## Solution
## Solution

Let Theorem W be applied to the torus $T(m_1,\dots,m_n)$ with cross order as in Section 7.2.1.3, and let $S$ be an initial segment in that order. The theorem relies on the recursive decomposition of $S$ into slices by fixing the last coordinate and applying the spread function $\alpha$ to standard sets in $T(m_1,\dots,m_{n-1})$.

### (a)

Take $n=2$ and choose parameters in unsorted order

$$m_1 = 2,\quad m_2 = 3.$$

The torus $T(2,3)$ consists of pairs $(x,y)$ with $0 \le x < 2$ and $0 \le y < 3$, ordered in cross order (lexicographic in the second coordinate blocks determined by the first coordinate, as in the construction of standard sets).

Now compare this with the swapped (sorted) situation $T(3,2)$. In $T(3,2)$, each level set ${(x,y): y=\text{const}}$ has size $3$, so the spread map $\alpha$ acts uniformly on 3-element standard sets in the first coordinate. In $T(2,3)$, the analogous slices have size $2$, so the induced recursion uses $\alpha$ on 2-element standard sets.

Take

$$N = 2.$$

In $T(2,3)$, the first two elements in cross order lie entirely in the first fiber $x=0$, namely

$$(0,0),\ (0,1).$$

Thus the projection onto the second coordinate of the initial segment of size $N$ occupies two distinct values in a single fiber of size $3$.

In $T(3,2)$, the first two elements in cross order lie instead in different fibers:

$$(0,0),\ (1,0).$$

Their projections onto the second coordinate coincide, since both have second coordinate $0$, so the induced slice counts differ from the previous case.

The conclusion of Theorem W identifies the structure of $S$ via a uniform recursion in terms of $\alpha$ applied consistently across all coordinate directions. For $N=2$, the induced decomposition of initial segments into fiber sizes depends on whether the first or second coordinate has larger modulus. Since the two constructions above produce different fiber distributions for the same $N$, the statement of Theorem W fails when the parameters are not sorted.

Thus $N=2$ is a value for which the claimed structural conclusion does not remain invariant under unsorted $(m_1,m_2)$.

### (b)

The proof of Theorem W uses the hypothesis

$$m_1 \le m_2 \le \cdots \le m_n$$

at the point where initial segments are decomposed recursively by fixing the last coordinate and comparing sizes of standard subsets in lower-dimensional tori.

In that step, the argument requires that when passing from $T(m_1,\dots,m_{n-1})$ to $T(m_1,\dots,m_{n-1},m_n)$, the spread function $\alpha$ acts monotonically with respect to inclusion of standard sets, so that each fiber of size $m_n$ can be filled in a way compatible with the recursive structure of initial segments.

If the parameters are not sorted, a coordinate with smaller modulus may appear later in the recursion, and the induction step comparing slices fails because the construction assumes that larger coordinate ranges dominate earlier ones in the cross-order stratification. This is exactly where the proof uses $m_{n-1} \le m_n$: it guarantees that the last coordinate provides the coarsest partition, so that the counting identity

$$N_a = \alpha(N_{a+1})$$

applies uniformly across all fibers without rebalancing between unequal coordinate sizes.

Without the ordering assumption, the induction breaks at the stage where fiber sizes are assumed compatible with the same spread operation, and the recursive identification of standard sets is no longer valid.

This completes the proof. ∎
