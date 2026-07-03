---
title: "CF 103439B - New Queries On Segment Deluxe"
description: "Let the given bit string be $a{25}dots a0$, where $s=12$ zeros and $t=14$ ones. In Chase’s sequence $C{st}$ as defined in (41), successive combinations are obtained by exchanging an adjacent pattern $10 leftrightarrow 01$, so a single move swaps a $1$ with a neighboring $0$."
date: "2026-07-03T07:46:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103439
codeforces_index: "B"
codeforces_contest_name: "XXII Open Cup, Grand Prix of Southeastern Europe"
rating: 0
weight: 103439
solve_time_s: 131
verified: false
draft: false
---

[CF 103439B - New Queries On Segment Deluxe](https://codeforces.com/problemset/problem/103439/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 11s  
**Verified:** no  

## Solution
## Solution

Let the given bit string be $a_{25}\dots a_0$, where $s=12$ zeros and $t=14$ ones. In Chase’s sequence $C_{st}$ as defined in (41), successive combinations are obtained by exchanging an adjacent pattern $10 \leftrightarrow 01$, so a single move swaps a $1$ with a neighboring $0$.

The sequence begins with the configuration in which all zeros precede all ones, namely

$00\dots 011\dots 1.$

From this starting point, any $1$ must move left across each $0$ that originally lies to its left until reaching its final position in the target string. Each such exchange is an adjacent swap of a $10$ pair. Hence the number of steps required to reach a given configuration equals the number of inversions of the form $(1,0)$, meaning pairs of positions $i<j$ with $a_i=1$ and $a_j=0$.

For each position $i$ containing a $1$, let $Z(i)$ denote the number of zeros in positions $i,i+1,\dots,25$. Each such zero contributes exactly one swap with the $1$ at position $i$, so the total number of swaps needed is

$\sum_{a_i=1} Z(i).$

The given string is

$11001001000011111101101010.$

Compute $Z(i)$ by suffix counting of zeros from right to left. The resulting values are:

$$\begin{aligned}
Z(1)&=12,\quad Z(2)=12,\quad Z(5)=10,\quad Z(8)=8,\\
Z(13)&=4,\quad Z(14)=4,\quad Z(15)=4,\quad Z(16)=4,\quad Z(17)=4,\quad Z(18)=4,\\
Z(20)&=3,\quad Z(21)=3,\quad Z(23)=2,\quad Z(25)=1.
\end{aligned}$$

Summing over all positions containing a $1$ gives

$$12+12+10+8+4+4+4+4+4+4+3+3+2+1=75.$$

This value is the number of adjacent exchanges required to transform the initial configuration into the given bit string in Chase’s sequence $C_{st}$, hence it equals the number of combinations preceding it.

Therefore the number of combinations preceding the given bit string is

$\boxed{75}.$

This completes the solution. ∎
