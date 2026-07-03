---
title: "CF 103214D - Bicoloracion"
description: "Let the universal cycle be $a0,a1,dots,a{L-1}$, indexed cyclically modulo $L$, over the alphabet ${0,1,dots,n-1}$. Every block $(ai,a{i+1},dots,a{i+t-1})$ corresponds to a $t$-multiset, hence to a $t$-combination of ${0,1,dots,n-1}$."
date: "2026-07-03T15:28:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103214
codeforces_index: "D"
codeforces_contest_name: "XXV Spain Olympiad in Informatics, Day 1"
rating: 0
weight: 103214
solve_time_s: 146
verified: false
draft: false
---

[CF 103214D - Bicoloracion](https://codeforces.com/problemset/problem/103214/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 26s  
**Verified:** no  

## Solution
## Solution

Let the universal cycle be $a_0,a_1,\dots,a_{L-1}$, indexed cyclically modulo $L$, over the alphabet ${0,1,\dots,n-1}$. Every block

$(a_i,a_{i+1},\dots,a_{i+t-1})$

corresponds to a $t$-multiset, hence to a $t$-combination of ${0,1,\dots,n-1}$. By assumption, every $t$-combination appears exactly once among these $L$ cyclic windows.

The number of distinct $t$-combinations is $\binom{n}{t}$, hence $L=\binom{n}{t}$.

Fix a symbol $x \in {0,1,\dots,n-1}$. Let $f_x$ denote the number of occurrences of $x$ in the cycle $a_0,\dots,a_{L-1}$.

Each occurrence of $x$ at position $i$ belongs to exactly $t$ cyclic windows, namely the windows starting at $i-t+1,i-t+2,\dots,i$. Therefore each occurrence of $x$ contributes exactly $t$ appearances of $x$ among all windows. The total number of windows is $L$, so the total number of pairs

$(\text{window}, \text{distinguished position occupied by } x)$

counted over all windows equals $f_x t$.

Independently, each window corresponds to a $t$-combination, and each $t$-combination containing $x$ contributes exactly one such pair. The number of $t$-combinations containing $x$ is $\binom{n-1}{t-1}$, hence the same pair count equals $\binom{n-1}{t-1}$.

Equating the two expressions gives

$f_x t = \binom{n-1}{t-1},$

so

$f_x = \frac{1}{t}\binom{n-1}{t-1}.$

Since $f_x$ is an integer, $t \mid \binom{n-1}{t-1}$. Using the identity

$\binom{n}{t} = \frac{n}{t}\binom{n-1}{t-1},$

write $\binom{n-1}{t-1}=t k$ for some integer $k$. Then

$\binom{n}{t} = \frac{n}{t}\cdot t k = nk,$

so $n \mid \binom{n}{t}$.

This completes the proof. ∎
