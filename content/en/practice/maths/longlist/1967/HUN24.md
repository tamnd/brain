---
title: "IMO 1967 LL HUN24"
description: "Father has left to his children several identical gold coins."
date: "2026-05-29T11:51:44+07:00"
tags: ["imo", "longlist", "mathematics", "olympiad"]
categories: ["mathematics"]
year: 1967
type: "longlist"
origin: "HUN"
weight: 196700024
draft: false
---

# IMO 1967 LL HUN24

**Origin:** HUN

## Problem

Father has left to his children several identical gold coins.
According to his will, the oldest child receives one coin and one-seventh of
the remaining coins, the next child receives two coins and one-seventh of
the remaining coins, the third child receives three coins and one-seventh of
the remaining coins, and so on through the youngest child. If every child
inherits an integer number of coins, ﬁnd the number of children and the
number of coins.

## Solution

Let the kth child receive xk coins. By the condition of the problem, the
number of coins that remain after him was 6(xk −k). This gives us a
recurrence relation
xk+1 = k + 1 + 6(xk −k) −k −1
= 6
7xk + 6
7,

which, together with the condition x1 = 1 + (m −1)/7, yields
xk = 6k−1
7k (m −36) + 6
for
1 \leqk \leqn.
Since we are given xn = n, we obtain 6n−1(m−36) = 7n(n−6). It follows
that 6n−1 | n −6, which is possible only for n = 6. Hence, n = 6 and
m = 36.
