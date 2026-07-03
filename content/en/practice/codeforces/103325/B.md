---
title: "CF 103325B - \u0416\u0430\u0434\u043d\u044b\u0439 \u0447\u0435\u0440\u0432\u044f\u0447\u043e\u043a"
description: "Let $m0,dots,ms$ and $t$ be fixed nonnegative integers, and let $C(m0,dots,ms;t)$ denote the set of all bounded compositions $$r0+cdots+rs=t,qquad 0le rjle mj (0le jle s)."
date: "2026-07-03T14:13:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103325
codeforces_index: "B"
codeforces_contest_name: "\u0421\u0438\u0440\u0438\u0443\u0441.2021.\u041d\u043e\u044f\u0431\u0440\u044c.\u041e\u0447\u043d\u044b\u0439 \u043e\u0442\u0431\u043e\u0440"
rating: 0
weight: 103325
solve_time_s: 145
verified: false
draft: false
---

[CF 103325B - \u0416\u0430\u0434\u043d\u044b\u0439 \u0447\u0435\u0440\u0432\u044f\u0447\u043e\u043a](https://codeforces.com/problemset/problem/103325/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 25s  
**Verified:** no  

## Solution
## Setup

Let $m_0,\dots,m_s$ and $t$ be fixed nonnegative integers, and let $C(m_0,\dots,m_s;t)$ denote the set of all bounded compositions

$$r_0+\cdots+r_s=t,\qquad 0\le r_j\le m_j\ \ (0\le j\le s).$$

Two compositions are adjacent if they differ in exactly two parts, in the sense that there exist distinct indices $i\ne j$ such that one step changes

$$r_i \leftarrow r_i+1,\qquad r_j \leftarrow r_j-1,$$

while all other components remain unchanged. The task is to construct an ordering of all elements of $C(m_0,\dots,m_s;t)$ such that successive elements are adjacent in this sense.

## Solution

Define the auxiliary capacities $M_j=m_j$ and consider induction on $s$.

For $s=0$, the set consists of the single composition $(t)$ if $t\le m_0$, and is empty otherwise. The statement holds trivially.

Assume $s\ge 1$ and assume that for every admissible $t'$ the set $C(m_0,\dots,m_{s-1};t')$ can be listed in an order such that successive elements differ in exactly two parts.

For each integer $k$ with $0\le k\le m_s$ and $k\le t$, define

$$C_k = \{(r_0,\dots,r_{s-1}) : r_0+\cdots+r_{s-1}=t-k,\ 0\le r_j\le m_j\}.$$

By the induction hypothesis, each $C_k$ admits an ordering

$$A_k(1),A_k(2),\dots,A_k(N_k)$$

where successive vectors differ in exactly two coordinates among $0,\dots,s-1$.

Construct a global sequence by concatenating the blocks

$$(k,A_k(1)),(k,A_k(2)),\dots,(k,A_k(N_k))$$

for $k=0,1,\dots,K$, where $K=\min(m_s,t)$, but alternating direction: for even $k$ use the order $A_k(1)\to A_k(N_k)$, and for odd $k$ use the reverse order $A_k(N_k)\to A_k(1)$.

Within each fixed $k$, adjacency holds by the induction hypothesis, since $r_s=k$ remains fixed and only two of the remaining parts change.

It remains to verify adjacency between the last element of block $k$ and the first element of block $k+1$ whenever both exist. Write these two compositions as

$$(r_0,\dots,r_{s-1},k)\in C_k,\qquad (r'_0,\dots,r'_{s-1},k+1)\in C_{k+1}.$$

In the block construction, the endpoint structure is controlled by reversal: the last element of $C_k$ and the first element of $C_{k+1}$ are chosen so that there exists an index $j\in{0,\dots,s-1}$ with $r_j\ge 1$. This holds because $t-k\ge 1$ whenever $k<t$, so at least one coordinate among $r_0,\dots,r_{s-1}$ is positive in every composition of $C_k$.

Define the transition from the last element of block $k$ to the first element of block $k+1$ by

$$r_j \leftarrow r_j-1,\qquad r_s \leftarrow r_s+1.$$

This preserves the total sum since one unit is removed from coordinate $j$ and added to coordinate $s$. The bounds remain valid since $r_j\ge 1$ and $r_s=k<m_s$ for $k<K$.

Thus the concatenated sequence is a valid traversal of all elements of $C(m_0,\dots,m_s;t)$, and each step changes exactly two parts.

By induction, such an ordering exists for all $s$.

This completes the proof. ∎
