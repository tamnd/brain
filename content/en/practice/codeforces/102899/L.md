---
title: "CF 102899L - KK \u5b66\u4e94\u5b50\u68cb"
description: "Let $U$ denote the set of all multicombinations $dt ldots d2 d1$ satisfying (6), that is $$s ge dt ge cdots ge d2 ge d1 ge 0.$$ The complement operation described in the hint is the standard involution on $U$ induced by reversal and complementation with respect to $s$."
date: "2026-07-04T08:23:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102899
codeforces_index: "L"
codeforces_contest_name: "The 2nd Hangzhou Normal University Freshman Programming Contest"
rating: 0
weight: 102899
solve_time_s: 64
verified: false
draft: false
---

[CF 102899L - KK \u5b66\u4e94\u5b50\u68cb](https://codeforces.com/problemset/problem/102899/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** no  

## Solution
## Solution

Let $U$ denote the set of all multicombinations $d_t \ldots d_2 d_1$ satisfying (6), that is

$$s \ge d_t \ge \cdots \ge d_2 \ge d_1 \ge 0.$$

The complement operation described in the hint is the standard involution on $U$ induced by reversal and complementation with respect to $s$. For each $d = d_t \ldots d_1 \in U$, define its complement $d^\ast = d_t^\ast \ldots d_1^\ast$ by

$$d_j^\ast = s - d_{t+1-j}, \qquad 1 \le j \le t.$$

Since $0 \le d_{t+1-j} \le s$, each $d_j^\ast$ lies in ${0,1,\ldots,s}$. The inequalities

$$d_{t+1-j} \ge d_{t-j}$$

imply

$$s - d_{t+1-j} \le s - d_{t-j},$$

so

$$d_j^\ast \ge d_{j+1}^\ast,$$

which places $d^\ast$ again in $U$. Applying the transformation twice returns the original sequence, since

$$(d^\ast)_j^\ast = s - d^\ast_{t+1-j} = s - (s - d_j) = d_j.$$

Thus the mapping is an involution on $U$.

For the case illustrated in the hint, the elements of $U$ are the $4$-tuples with entries in ${0,1,2,3}$ in nonincreasing order, and the complement operation reverses the list and replaces each entry $x$ by $3-x$. This produces the listed pairs

$$3211 \leftrightarrow 1100,\quad 3210 \leftrightarrow 2100,\quad \ldots,\quad 3000 \leftrightarrow 0003,$$

which accounts for all complements stated in the hint.

Corollary C splits the family of multicombinations into two complementary parts determined by a threshold condition on the entries. The two halves are exchanged by the involution $d \mapsto d^\ast$, since reversing and replacing each entry $d_j$ by $s-d_{t+1-j}$ transforms any condition of the form $d_1 \le k$ into the complementary condition $d_t \ge s-k$, and similarly for any extremal condition defining the second half.

Therefore every element in the “$\partial$ half” of Corollary C is mapped bijectively onto an element of the complementary half under $d \mapsto d^\ast$, and vice versa. The two halves therefore have equal cardinality, and any identity established for one half transfers immediately to the other by applying this involution.

This completes the proof. ∎
