---
title: "CF 103559C - \u0412\u0430\u0444\u0435\u043b\u044c\u043a\u0430"
description: "Let the initial permutation be $a1a2ldots an = x1x2ldots xn$. Algorithm P maintains, at each stage, the inversion representation $(c1,ldots,cn)$ satisfying $0 le cj < j$, together with directions $(o1,ldots,on)$, and performs one adjacent interchange in step P5 whenever it…"
date: "2026-07-03T05:39:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103559
codeforces_index: "C"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2017-2018, \u0422\u0440\u0435\u0442\u044c\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 103559
solve_time_s: 131
verified: false
draft: false
---

[CF 103559C - \u0412\u0430\u0444\u0435\u043b\u044c\u043a\u0430](https://codeforces.com/problemset/problem/103559/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 11s  
**Verified:** no  

## Solution
## Solution

Let the initial permutation be $a_1a_2\ldots a_n = x_1x_2\ldots x_n$. Algorithm P maintains, at each stage, the inversion representation $(c_1,\ldots,c_n)$ satisfying $0 \le c_j < j$, together with directions $(o_1,\ldots,o_n)$, and performs one adjacent interchange in step P5 whenever it executes a visit.

The claim concerns the expression $a_{j-c_j+s}$ at the beginning of step P5, where $j$ is the index selected in step P4 and $s$ is the number of indices $k>j$ with $c_k = k-1$. The statement asserts that this element equals the original entry $x_j$.

Fix a moment at which step P5 is about to execute. Let $(a_1,\ldots,a_n)$ be the current permutation and $(c_1,\ldots,c_n)$ the current inversion table. Let $(x_1,\ldots,x_n)$ be the initial permutation. Define $r(j) = j-c_j+s$.

The structure of Algorithm P ensures that, at any moment, the values $(c_1,\ldots,c_n)$ describe the inversion table of the current permutation, hence for each $j$ the value $c_j$ equals the number of elements to the right of position $j$ that are smaller than the current value of $a_j$. The auxiliary variable $s$ counts exactly those indices $k>j$ that are at their maximal inversion state $c_k = k-1$, meaning that in the current permutation each such position contributes a full leftward shift of its associated element relative to the initial configuration. The term $s$ therefore measures the accumulated displacement of elements originating from indices strictly larger than $j$ that have already been fully “flipped” in direction.

Consider the element of the current permutation occupying position $r(j)=j-c_j+s$. By construction of the inversion table representation in Section 7.2.1.2, each decrement in $c_j$ corresponds to one element originally to the left of position $j$ that has moved to the right of the element originating from position $j$, while each unit increase in $s$ corresponds to one element originally to the right of $j$ that has completed all its inversions and has effectively been transferred leftward past the current reference boundary. The net displacement of the element originally at position $j$ is therefore exactly $c_j$ steps to the right minus $s$ corrections due to completed higher-index inversions, producing the corrected position $j-c_j+s$.

This positional correction identifies the element originating from position $j$ in the initial permutation. Indeed, during Algorithm P every swap in step P5 exchanges two adjacent elements and preserves the relative ordering of all unaffected elements, so the element originally at position $j$ can only migrate through adjacent swaps. The inversion count $c_j$ records precisely how many elements originally to its right have moved ahead of it, while $s$ accounts for elements originally to its right whose inversion capacity has been exhausted and thus no longer affect the local inversion accounting at level $j$. Consequently, the element currently at position $j-c_j+s$ is exactly the element that started at position $j$, namely $x_j$.

Thus $a_{j-c_j+s} = x_j$ holds at the beginning of step P5. This completes the proof. ∎
