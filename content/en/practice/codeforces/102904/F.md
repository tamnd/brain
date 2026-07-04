---
title: "CF 102904F - Exercise"
description: "Let $a1 ge cdots ge an ge 0$ and $a'1 ge cdots ge a'n ge 0$ be partitions of $n$, padded with zeros to length $n$."
date: "2026-07-04T10:15:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102904
codeforces_index: "F"
codeforces_contest_name: "\u0426\u0438\u043a\u043b \u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434, \u0421\u0435\u0437\u043e\u043d 2020-21, \u041f\u044f\u0442\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102904
solve_time_s: 70
verified: false
draft: false
---

[CF 102904F - Exercise](https://codeforces.com/problemset/problem/102904/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** no  

## Solution
## Solution

Let $a_1 \ge \cdots \ge a_n \ge 0$ and $a'_1 \ge \cdots \ge a'_n \ge 0$ be partitions of $n$, padded with zeros to length $n$. Their conjugates are defined by

$$b_k = |\{ i \mid a_i \ge k \}|, \qquad b'_k = |\{ i \mid a'_i \ge k \}|.$$

The goal is to compare the lexicographic order of $b_1 b_2 \cdots b_n$ and $b'_1 b'_2 \cdots b'_n$ with the lexicographic order of the reversed sequences $a_n \cdots a_1$ and $a'_n \cdots a'_1$.

Let $r_i = a_{n-i+1}$ and $r'_i = a'_{n-i+1}$ be the reversed sequences. Lexicographic comparison of $r$ and $r'$ is determined by the smallest index $i$ such that $r_i \ne r'_i$, equivalently the largest index $j = n-i+1$ such that $a_j \ne a'_j$.

Let $j$ be the largest index with $a_j \ne a'_j$. Then $a_{j+1} = a'_{j+1}, \ldots, a_n = a'_n = 0$, and the reversed sequences first differ at position $i = n-j+1$.

Assume $a_j < a'_j$; the opposite case is symmetric. Then for all $k > a'_j$, both $a_j$ and $a'_j$ are $< k$, so the rows $1,\ldots,j$ do not contribute to $b_k$ or $b'_k$. For $k \le a_j$, both rows $j$ contribute, and the difference between $b_k$ and $b'_k$ is determined entirely by indices $1,\ldots,j-1$, where $a$ and $a'$ coincide. Hence $b_k = b'_k$ for all $k \le a_j$.

At $k = a_j + 1$, row $j$ contributes to $b'_k$ but not to $b_k$, since $a_j < a'_j$. Thus $b'_{a_j+1} = b_{a_j+1} + 1$, so $b < b'$ in lexicographic order.

We now relate this to the reversed sequences. Since $j$ is the largest index with a difference, the first difference in $r$ and $r'$ occurs at position $n-j+1$, where $r_{n-j+1} = a_j$ and $r'_{n-j+1} = a'_j$. Hence $r < r'$ lexicographically.

This shows that if $a_n \cdots a_1 < a'_n \cdots a'_1$, then $b_1 \cdots b_n < b'_1 \cdots b'_n$.

For the converse, assume $b < b'$ and let $k$ be the smallest index with $b_k \ne b'_k$. Then $b_1 = b'_1, \ldots, b_{k-1} = b'_{k-1}$, so for all $i$ with $a_i \ge k-1$, the counts of such indices agree in $a$ and $a'$. The first discrepancy in row structure must occur at the highest row index $j$ such that one of $a_j, a'_j$ crosses the threshold $k$. This implies $a_j < a'_j$ and that all higher indexed rows are equal.

Thus $j$ is exactly the largest index where $a_j \ne a'_j$, and the first difference in the reversed sequences occurs at position $n-j+1$ with $a_j < a'_j$. Hence $a_n \cdots a_1 < a'_n \cdots a'_1$.

Both implications hold, so the two lexicographic comparisons are equivalent.

This completes the proof. ∎
