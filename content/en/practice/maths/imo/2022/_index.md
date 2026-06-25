---
title: "IMO 2022"
description: "IMO 2022 — 6/6 solved."
tags: ["imo", "mathematics", "olympiad"]
categories: ["mathematics"]
imo_year: 2022
weight: 2022
draft: false
---

# IMO 2022

[Official IMO 2022 problems](https://www.imo-official.org/year_info.aspx?year=2022) &nbsp;·&nbsp; 6/6 solved.

| # | Status | Time |
|---|--------|------|
| [1](1.md) | solved | 1m06s |
| [2](2.md) | solved | 43s |
| [3](3.md) | solved | 42s |
| [4](4.md) | solved | 50s |
| [5](5.md) | solved | 1m28s |
| [6](6.md) | solved | 1m27s |

**Problem 1** &nbsp; *solved* · 1m06s · [Solution →](1.md)

The Bank of Oslo issues two types of coin: aluminium (denoted A) and bronze (denoted B). Marianne has $n$ aluminium coins and $n$ bronze coins, arranged in a row in some arbitrary initial order. A chain is any subsequence of consecutive coins of the same type. Given a fixed positive integer $k\le 2n$, Marianne repeatedly performs the following operation: she identifies the longest chain containing the $k^{th}$ coin from the left, and moves all coins in that chain to the left end of the row. For example, if $n = 4$ and $k = 4$, the process starting from the ordering AABBBABA would be

AABBBABA → BBBAAABA → AAABBBBA → BBBBAAAA → BBBBAAAA → ...

Find all pairs $(n, k)$ with $1 \le k \le 2n$ such that for every initial ordering, at some moment during the process, the leftmost $n$ coins will all be of the same type.

**Problem 2** &nbsp; *solved* · 43s · [Solution →](2.md)

Let $\mathbb{R}^+$ denote the set of positive real numbers. Find all functions $f : \mathbb{R}^+ \to \mathbb{R}^+$ such that for each $x \in \mathbb{R}^+$, there is exactly one $y \in \mathbb{R}^+$ satisfying

$$
xf (y) + yf (x) \le 2
$$.

Working

**Problem 3** &nbsp; *solved* · 42s · [Solution →](3.md)

Let $k$ be a positive integer and let $S$ be a finite set of odd prime numbers. Prove that there is at most one way (up to rotation and reflection) to place the elements of $S$ around a circle such that the product of any two neighbours is of the form $x^2 + x + k$ for some positive integer $x$.

Working

**Problem 4** &nbsp; *solved* · 50s · [Solution →](4.md)

Let $ABCDE$ be a convex pentagon such that $BC = DE$. Assume that there is a
point $T$ inside $ABCDE$ with $TB = TD$, $TC = TE$ and $\angle ABT = \angle TEA$. Let line $AB$ intersect
lines $CD$ and $CT$ at points $P$ and $Q$, respectively. Assume that the points $P, B, A, Q$ occur on their
line in that order. Let line $AE$ intersect lines $CD$ and $DT$ at points $R$ and $S$, respectively. Assume
that the points $R, E, A, S$ occur on their line in that order. Prove that the points $P, S, Q, R$ lie on
a circle.

**Problem 5** &nbsp; *solved* · 1m28s · [Solution →](5.md)

Find all triples $(a,b,p)$ of positive integers with $p$ prime and
$$
a^p = b! + p
$$

**Problem 6** &nbsp; *solved* · 1m27s · [Solution →](6.md)

Let $n$ be a positive integer. A Nordic square is an $n \times n$ board containing all the integers from $1$ to $n^2$ so that each cell contains exactly one number. Two different cells are considered adjacent if they share an edge. Every cell that is adjacent only to cells containing larger numbers is called a valley. An uphill path is a sequence of one or more cells such that:

(i) the first cell in the sequence is a valley,

(ii) each subsequent cell in the sequence is adjacent to the previous cell, and

(iii) the numbers written in the cells in the sequence are in increasing order.

Find, as a function of $n$, the smallest possible total number of uphill paths in a Nordic square.
