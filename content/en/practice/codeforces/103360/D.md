---
title: "CF 103360D - \u041a\u0440\u043e\u0441\u0441\u0432\u043e\u0440\u0434 \u0434\u043b\u044f \u0434\u0440\u043e\u0438\u0434\u0430"
description: "Let $n = s + t$ as in (1), and consider a $t$-combination $ct cdots c1$ with $n ct cdots c1 ge 0$ together with the additional adjacency restriction $c{j+1} cj + 1 qquad (t j ge 1).$ Define new integers $c'j = cj - (j-1), qquad 1 le j le t."
date: "2026-07-03T13:24:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103360
codeforces_index: "D"
codeforces_contest_name: "\u0418\u043d\u0434\u0438\u0432\u0438\u0434\u0443\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0438 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2020"
rating: 0
weight: 103360
solve_time_s: 141
verified: false
draft: false
---

[CF 103360D - \u041a\u0440\u043e\u0441\u0441\u0432\u043e\u0440\u0434 \u0434\u043b\u044f \u0434\u0440\u043e\u0438\u0434\u0430](https://codeforces.com/problemset/problem/103360/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 21s  
**Verified:** no  

## Solution
## Solution

Let $n = s + t$ as in (1), and consider a $t$-combination $c_t \cdots c_1$ with

$n > c_t > \cdots > c_1 \ge 0$

together with the additional adjacency restriction

$c_{j+1} > c_j + 1 \qquad (t > j \ge 1).$

Define new integers

$c'_j = c_j - (j-1), \qquad 1 \le j \le t.$

From $c_{j+1} \ge c_j + 2$ it follows that

$c'_{j+1} = c_{j+1} - j \ge c_j + 2 - j = (c_j - (j-1)) + 1 = c'_j + 1,$

hence

$c'_t > c'_{t-1} > \cdots > c'_1 \ge 0.$

Thus $c'_t \cdots c'_1$ is an ordinary strict $t$-combination in the sense of (3), formed from a set of consecutive integers.

From $c_t \le n-1$ one obtains

$c'_t = c_t - (t-1) \le n-1-(t-1) = n-t,$

and $c'_1 \ge 0$ holds directly from $c_1 \ge 0$. Therefore each $c'_j$ lies in ${0,1,\ldots,n-t}$.

Conversely, given any ordinary combination

$n-t \ge c'_t > \cdots > c'_1 \ge 0,$

define

$c_j = c'_j + (j-1).$

Then $c_{j+1} \ge c'_{j+1} + j \ge (c'_j + 1) + j = (c'_j + (j-1)) + 2 = c_j + 2,$$

so the adjacency condition $c_{j+1} > c_j + 1$ holds, and also $c_t \le n-1$ follows from $c'_t \le n-t$. This reconstruction inverts the transformation, so it is bijective between valid piano-chord combinations and ordinary $t$-combinations on ${0,1,\ldots,n-t}$.

Hence the piano-player problem with adjacency restriction is equivalent to generating all $t$-combinations of an $(n-t+1)$-element set. By (1.2.6-2), their number is

$\binom{n-t+1}{t},$

since the underlying ground set has elements $0,1,\ldots,n-t$.

To generate all such chords lexicographically, apply Algorithm $L$ of Section 7.2.1.3 to the transformed variables $c'_t \cdots c'_1$, and then output

$c_j = c'_j + (j-1) \qquad (1 \le j \le t).$

This produces all admissible chords exactly once, preserving lexicographic order under the affine shift.

This completes the proof. ∎
