---
title: "CF 103358B - Nutty String"
description: "Let $n ct cdots c1 ge 0$ with the constraints from exercise 57 and the additional condition $c{j+1} cj + 1 qquad (t j ge 1).$ Define the shifted variables $dj = cj - (j-1), qquad 1 le j le t."
date: "2026-07-03T13:29:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103358
codeforces_index: "B"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2020-2021, \u0412\u0442\u043e\u0440\u0430\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 103358
solve_time_s: 164
verified: false
draft: false
---

[CF 103358B - Nutty String](https://codeforces.com/problemset/problem/103358/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 44s  
**Verified:** no  

## Solution
## Solution

Let $n > c_t > \cdots > c_1 \ge 0$ with the constraints from exercise 57 and the additional condition

$c_{j+1} > c_j + 1 \qquad (t > j \ge 1).$

Define the shifted variables

$d_j = c_j - (j-1), \qquad 1 \le j \le t.$

Then for $t > j \ge 1$,

$d_{j+1} = c_{j+1} - j \ge (c_j + 2) - j = (c_j - (j-1)) + 1 = d_j + 1,$

so

$n - t + 1 > d_t > \cdots > d_1 \ge 0.$

The upper bound follows from $c_t \le n-1$, hence

$d_t = c_t - (t-1) \le (n-1) - (t-1) = n - t.$

Thus the mapping $c \mapsto d$ is a bijection between admissible sequences $c_1 < \cdots < c_t$ with no adjacent indices and ordinary $t$-combinations drawn from ${0,1,\dots,n-t}$.

The span constraint transforms as well. From $c_t - c_1 < m$,

$c_t - c_1 = (d_t + t - 1) - d_1 = (d_t - d_1) + (t-1),$

so

$d_t - d_1 < m - (t-1).$

Hence admissible chords correspond exactly to sequences

$n' > d_t > \cdots > d_1 \ge 0,$

with

$n' = n - t + 1,$

together with the reduced span condition

$d_t - d_1 < m - (t-1).$

This reduces the problem to the piano player problem of exercise 57 applied to the parameters $n'$ and $m' = m - (t-1)$.

For generation, apply Algorithm $L$ from Section 7.2.1.3 to the variables $d_t \cdots d_1$ with the modified bound $n' = n - t + 1$, while retaining the same acceptance test for the span condition. The algorithm visits all combinations in lexicographic order, and each valid chord is obtained by transforming back via

$c_j = d_j + (j-1), \qquad 1 \le j \le t.$

Correctness follows from the bijection between admissible $c$-sequences and admissible $d$-sequences, since each transformation preserves and reflects both the ordering constraints and the span inequality. This completes the proof. ∎
