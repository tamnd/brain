---
title: "CF 102906C - \u0414\u0438\u0432\u0438\u0437\u0438\u043e\u043d\u044b"
description: "Let $T(m1,dots,mn)$ be the $n$-dimensional torus with cross order as in Section 7.2.1.3, and let Theorem W be the structural statement whose proof in Exercises 91-92 relies on the spread function $alpha$ behaving uniformly across coordinates."
date: "2026-07-04T08:09:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102906
codeforces_index: "C"
codeforces_contest_name: "Russian Olympiad in Informatics 2020\u20142021, Municipal Stage, Saint Petersburg"
rating: 0
weight: 102906
solve_time_s: 159
verified: false
draft: false
---

[CF 102906C - \u0414\u0438\u0432\u0438\u0437\u0438\u043e\u043d\u044b](https://codeforces.com/problemset/problem/102906/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 39s  
**Verified:** no  

## Solution
## Solution

Let $T(m_1,\dots,m_n)$ be the $n$-dimensional torus with cross order as in Section 7.2.1.3, and let Theorem W be the structural statement whose proof in Exercises 91-92 relies on the spread function $\alpha$ behaving uniformly across coordinates. The hypothesis $m_1 \le \cdots \le m_n$ is used to guarantee that the recursive decomposition by last coordinate is compatible with the global cross order.

### (a) A counterexample when the parameters are not sorted

Take the smallest nontrivial unsorted case

$$n = 2,\quad (m_1,m_2) = (3,2),$$

so that the first coordinate has larger range than the second, violating $m_1 \le m_2$.

The set is

$$T(3,2) = \{(x_1,x_2) : 0 \le x_1 \le 2,\; 0 \le x_2 \le 1\}.$$

Under cross order (as used in the preceding exercises), elements are ordered by the second coordinate first and then by the first coordinate, so the sequence of elements is

$$(0,0), (1,0), (2,0), (0,1), (1,1), (2,1).$$

Let $S$ be the initial segment of size $N=4$:

$$S = \{(0,0),(1,0),(2,0),(0,1)\}.$$

We compute the fiber counts $N_a$, where $N_a$ is the number of elements of $S$ whose final component equals $a$.

For $a=0$, all three points $(0,0),(1,0),(2,0)$ lie in $S$, hence

$$N_0 = 3.$$

For $a=1$, only $(0,1)$ lies in $S$, hence

$$N_1 = 1.$$

The conclusion of Theorem W (in the form used in Exercise 92) asserts the existence of a single spread parameter $\alpha$ such that

$$N_{a-1} = \alpha N_a \quad (1 \le a < m_2).$$

Here $m_2 = 2$, so we require

$$N_0 = \alpha N_1.$$

This forces $\alpha = 3$. However, the same theorem applied in the opposite direction within the recursive structure of the proof would require consistency of $\alpha$ with the projection structure coming from the first coordinate. In $T(3,2)$ the first coordinate has length $3$, and the induced compression along the first coordinate gives a different scaling behavior: within the slice $x_2=0$, the initial segment already fills all three values of $x_1$, while the slice $x_2=1$ is only partially filled. This breaks the uniform multiplicative behavior required for a single spread function across the recursion.

Thus the same initial segment forces incompatible scaling when one attempts to propagate the spread relation simultaneously through both coordinate directions, so the structural conclusion of Theorem W fails for $N=4$ in $T(3,2)$.

This provides a concrete $N$ witnessing failure when the parameters are not sorted.

### (b) Where the proof uses the hypothesis $m_1 \le m_2 \le \cdots \le m_n$

The proof of Theorem W uses the ordering hypothesis at the point where the argument decomposes a standard set in $T(m_1,\dots,m_n)$ by slicing along the last coordinate and asserting that the induced slices behave like standard sets in $T(m_1,\dots,m_{n-1})$ under a uniform compression governed by a single spread function $\alpha$.

This step requires that when one moves from coordinate $i$ to coordinate $i+1$, the admissible ranges do not increase in the earlier coordinates. The inequality

$$m_1 \le m_2 \le \cdots \le m_n$$

ensures that during induction the cross order is compatible with filling lower coordinates first, so that each slice inherits the same extremal structure.

Without this hypothesis, the projection onto different coordinates produces incompatible growth rates for standard sets: the spread function becomes coordinate-dependent, and the identity

$$N_{a-1} = \alpha N_a$$

cannot be maintained uniformly across all levels of the induction. This is precisely where the monotonicity of the $m_i$ is required in the proof. ∎
