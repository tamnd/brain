---
title: "CF 103076E - Death Star"
description: "Let $n = s + t$ as in equation (1) of Section 7.2.1.3, and let the admissible chords be described by strictly increasing indices $n ct cdots c1 ge 0,$ subject to the constraints $ct - c1 < m,$ and, in the present exercise, the additional adjacency exclusion $c{j+1} cj + 1 quad…"
date: "2026-07-04T00:23:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103076
codeforces_index: "E"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2021"
rating: 0
weight: 103076
solve_time_s: 159
verified: false
draft: false
---

[CF 103076E - Death Star](https://codeforces.com/problemset/problem/103076/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 39s  
**Verified:** no  

## Solution
## Solution

Let $n = s + t$ as in equation (1) of Section 7.2.1.3, and let the admissible chords be described by strictly increasing indices

$n > c_t > \cdots > c_1 \ge 0,$

subject to the constraints

$c_t - c_1 < m,$

and, in the present exercise, the additional adjacency exclusion

$c_{j+1} > c_j + 1 \quad (t > j \ge 1).$

The adjacency condition rewrites as a uniform gap condition

$c_{j+1} \ge c_j + 2 \quad (t > j \ge 1).$

Define a transformed sequence

$d_j = c_j - (j-1), \quad 1 \le j \le t.$

From $c_{j+1} \ge c_j + 2$ we obtain

$d_{j+1} = c_{j+1} - j \ge c_j + 2 - j = (c_j - (j-1)) + 1 = d_j + 1,$

so

$n - (t-1) > d_t > \cdots > d_1 \ge 0.$

Thus $(d_t,\ldots,d_1)$ is an ordinary $t$-combination drawn from the reduced set ${0,1,\ldots,n-(t-1)-1}$.

Conversely, given any strictly increasing sequence $d_t > \cdots > d_1 \ge 0$ in this reduced range, defining $c_j = d_j + (j-1)$ produces a sequence satisfying $c_{j+1} \ge c_j + 2$ by reversing the above calculation. This establishes a bijection between admissible chords and ordinary $t$-combinations of size $n-(t-1)$.

The spacing constraint is transformed by substitution into

$c_t - c_1 = (d_t + t - 1) - d_1 = (d_t - d_1) + (t - 1).$

Hence the original bound $c_t - c_1 < m$ becomes

$d_t - d_1 < m - (t-1).$

Therefore the modified piano-chord problem with adjacency exclusion is equivalent to the original problem of Exercise 57 applied to parameters

$n' = n - (t-1), \quad m' = m - (t-1).$

In particular, all enumeration and generation procedures from Exercise 57 apply verbatim after this reduction, replacing $n$ by $n-(t-1)$ and $m$ by $m-(t-1)$.

This completes the proof. ∎
