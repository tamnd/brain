---
title: "IMO 1967 LL MON30"
description: "Given m+n numbers ai (i = 1, 2, . . . , m), bj (j = 1, 2, . . ., n),"
date: "2026-05-29T11:51:44+07:00"
tags: ["imo", "longlist", "mathematics", "olympiad"]
categories: ["mathematics"]
year: 1967
type: "longlist"
origin: "MON"
weight: 196700030
draft: false
---

# IMO 1967 LL MON30

**Origin:** MON

## Problem

Given m+n numbers ai (i = 1, 2, . . . , m), bj (j = 1, 2, . . ., n),
determine the number of pairs (ai, bj) for which |i −j| \geqk, where k is a
nonnegative integer.

## Solution

We assume w.l.o.g. that m \leqn. Let r and s be the numbers of pairs for
which i −j \geqk and of those for which j −i \geqk. The desired number is
r + s. We easily ﬁnd that
r =
. (m −k)(m −k + 1)/2,
k < m,
0,
k \geqm,
s =
⎧
⎨
⎩
m(2n −2k −m + 1)/2,
k < n −m,
(n −k)(n −k + 1)/2,
n −m \leqk < n,
0,
k \geqn.
