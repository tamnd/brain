---
title: "CF 102947D - Firewood"
description: "Let $n,m ge 1$. The goal is to generate all partitions of $n$ into at most $m$ parts, meaning sequences $a1 ge a2 ge cdots ge ak ge 1,quad k le m,quad a1+cdots+ak=n."
date: "2026-07-04T07:29:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102947
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 02-05-21 Div. 1 (Advanced)"
rating: 0
weight: 102947
solve_time_s: 125
verified: false
draft: false
---

[CF 102947D - Firewood](https://codeforces.com/problemset/problem/102947/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 5s  
**Verified:** no  

## Solution
## Solution

Let $n,m \ge 1$. The goal is to generate all partitions of $n$ into at most $m$ parts, meaning sequences

$a_1 \ge a_2 \ge \cdots \ge a_k \ge 1,\quad k \le m,\quad a_1+\cdots+a_k=n.$

The key observation is that such partitions correspond bijectively to partitions of $n+m$ into exactly $m$ positive parts via a uniform shift.

Given any partition of $n$ into at most $m$ parts, write it in padded form as an $m$-tuple

$a_1 \ge a_2 \ge \cdots \ge a_m \ge 0,\quad a_1+\cdots+a_m=n.$

Define

$b_i = a_i + 1.$

Then

$b_1 \ge b_2 \ge \cdots \ge b_m \ge 1,$

and

$b_1+\cdots+b_m = n+m.$

Conversely, every partition $b_1 \ge \cdots \ge b_m \ge 1$ of $n+m$ into exactly $m$ parts produces a unique partition of $n$ into at most $m$ parts by subtracting $1$ from each component. The number of zero entries among the $a_i$ is exactly the number of unit parts among the $b_i$, and deleting zeros recovers a partition with at most $m$ positive parts. This correspondence is therefore bijective.

Algorithm H generates all partitions of an integer into exactly $m$ positive parts. Applying it to $n+m$ instead of $n$ produces all $m$-tuples $b_1,\dots,b_m$ with

$b_1+\cdots+b_m=n+m,\quad b_i\ge 1.$

The required modification is therefore confined to step H1, replacing the original initialization for input $n$ by the initialization for input $n+m$.

In step H1 of Algorithm H, the assignment

$a_1 \leftarrow n - m + 1,\quad a_j \leftarrow 1 \ (1<j\le m)$

is replaced by the assignment obtained by substituting $n+m$ for $n$, namely

$a_1 \leftarrow (n+m) - m + 1 = n+1,\quad a_j \leftarrow 1 \ (1<j\le m),$

with the sentinel $a_{m+1} \leftarrow -1$ unchanged.

The algorithm then generates all partitions of $n+m$ into exactly $m$ parts. After each output, replacing each $a_i$ by $a_i-1$ yields a nonincreasing $m$-tuple of nonnegative integers summing to $n$, and deleting zeros yields precisely the partitions of $n$ into at most $m$ parts.

This modification does not affect any later step of Algorithm H, since all invariants used there depend only on relative differences between parts and preservation of the sum, both unchanged under uniform translation by $1$. ∎
