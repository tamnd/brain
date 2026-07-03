---
title: "CF 102994C - An Unsure Catch"
description: "Let $n=s+t$ as in (1), and let an $(s,t)$-combination be written in the form $ct cdots c2 c1$ satisfying (3), that is $n ct cdots c2 c1 ge 0."
date: "2026-07-04T02:26:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102994
codeforces_index: "C"
codeforces_contest_name: "Moscow Pre-Finals Workshop 2020 - Legilimens+Coffee Chicken Contest (XX Open Cup, Grand Prix of Nanjing)"
rating: 0
weight: 102994
solve_time_s: 137
verified: false
draft: false
---

[CF 102994C - An Unsure Catch](https://codeforces.com/problemset/problem/102994/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 17s  
**Verified:** no  

## Solution
## Solution

Let $n=s+t$ as in (1), and let an $(s,t)$-combination be written in the form $c_t \cdots c_2 c_1$ satisfying (3), that is

$n > c_t > \cdots > c_2 > c_1 \ge 0.$

Define the associated nonnegative integers $q_t, \ldots, q_0$ by (11) and (12):

$q_t = s - d_t,\quad q_{t-1} = d_t - d_{t-1},\quad \ldots,\quad q_1 = d_2 - d_1,\quad q_0 = d_1,$

where the integers $d_j$ are related to the combination by (7),

$c_j = d_j + j - 1 \quad (1 \le j \le t).$

From these relations,

$q_t + \cdots + q_1 + q_0 = s,$

so every $(s,t)$-combination determines a composition of $s$ into $t+1$ nonnegative parts.

To prove the compression lemma (85), it suffices to show that this correspondence is bijective.

Injectivity follows from reconstructing $d_1, \ldots, d_t$ uniquely from $q_0, \ldots, q_t$. From (12),

$d_1 = q_0,$

$d_2 = q_1 + d_1,$

$d_3 = q_2 + d_2,$

and in general

$d_j = q_{j-1} + d_{j-1} \quad (2 \le j \le t).$

Thus each $d_j$ is determined uniquely by the $q$-sequence, and then each $c_j = d_j + j - 1$ is uniquely determined. Hence distinct combinations yield distinct $q$-sequences.

Surjectivity is obtained by reversing the construction. Let $q_t, \ldots, q_0$ be any composition of $s$ into $t+1$ nonnegative parts. Define $d_1 = q_0$ and recursively

$d_j = q_{j-1} + d_{j-1} \quad (2 \le j \le t),$

then set

$c_j = d_j + j - 1 \quad (1 \le j \le t).$

The recursion implies $d_1 \le d_2 \le \cdots \le d_t$, hence

$c_1 < c_2 < \cdots < c_t,$

and also

$c_t \le (q_0 + \cdots + q_{t-1}) + (t-1) = (s - q_t) + (t-1) < s + t = n,$

so $n > c_t > \cdots > c_1 \ge 0$ holds, making $c_t \cdots c_1$ a valid $(s,t)$-combination.

Thus every composition of $s$ arises from a unique combination, and every combination yields a composition, so the correspondence is bijective. This establishes the compression lemma (85). ∎
