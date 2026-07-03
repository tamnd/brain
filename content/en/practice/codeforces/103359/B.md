---
title: "CF 103359B - \u041b\u043e\u0432\u0443\u0448\u043a\u0430 \u0434\u043b\u044f \u0414\u0436\u0435\u0440\u0440\u0438"
description: "Let $n = s + t$ as in (1), and consider a $t$-combination $ct cdots c1$ with $n ct cdots c1 ge 0$ together with the additional adjacency restriction $c{j+1} cj + 1 qquad (t j ge 1).$ Define new integers $c'j = cj - (j-1), qquad 1 le j le t."
date: "2026-07-03T13:26:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103359
codeforces_index: "B"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2020-2021, \u0422\u0440\u0435\u0442\u044c\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 103359
solve_time_s: 70
verified: false
draft: false
---

[CF 103359B - \u041b\u043e\u0432\u0443\u0448\u043a\u0430 \u0434\u043b\u044f \u0414\u0436\u0435\u0440\u0440\u0438](https://codeforces.com/problemset/problem/103359/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
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
