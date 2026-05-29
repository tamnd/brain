---
title: "IMO 1977 LL SWE42"
description: "The sequence an,k, k = 1, 2, 3, . . ., 2n, n = 0, 1, 2, . . ., is deﬁned"
date: "2026-05-29T11:51:44+07:00"
tags: ["imo", "longlist", "mathematics", "olympiad"]
categories: ["mathematics"]
year: 1977
type: "longlist"
origin: "SWE"
weight: 197700042
draft: false
---

# IMO 1977 LL SWE42

**Origin:** SWE

## Problem

The sequence an,k, k = 1, 2, 3, . . ., 2n, n = 0, 1, 2, . . ., is deﬁned
by the following recurrence formula:
a1 = 2,
an,k = 2a3
n−1,k,
an,k+2n−1 = 1
2a3
n−1,k
for k = 1, 2, 3, . . ., 2n−1, n = 0, 1, 2, . . . .
Prove that the numbers an,k are all diﬀerent.

## Solution

It can be proved by induction on n that
{an,k | 1 \leqk \leq2n} = {2m | m = 3n+3n−1s1+\cdot \cdot \cdot+31sn−1+sn (si = \pm1)}.
Thus the result is an immediate consequence of the following lemma.
Lemma. Each positive integer s can be uniquely represented in the form
s = 3n + 3n−1s1 + \cdot \cdot \cdot + 31sn−1 + sn,
where si \in{−1, 0, 1}.
(1)
Proof.
Both the existence and the uniqueness can be shown by simple
induction on s. The statement is trivial for s = 1, while for s > 1

there exist q \inN, r \in{−1, 0, 1} such that s = 3q + r, and q has a
unique representation of the form (1).
