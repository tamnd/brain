---
title: "IMO 1977 LL FRG11"
description: "Let n and z be integers greater than 1 and (n, z) = 1. Prove:"
date: "2026-05-29T11:51:44+07:00"
tags: ["imo", "longlist", "mathematics", "olympiad"]
categories: ["mathematics"]
year: 1977
type: "longlist"
origin: "FRG"
weight: 197700011
draft: false
---

# IMO 1977 LL FRG11

**Origin:** FRG

## Problem

Let n and z be integers greater than 1 and (n, z) = 1. Prove:
(a) At least one of the numbers zi = 1+z+z2+\cdot \cdot \cdot+zi, i = 0, 1, . . . , n−1,
is divisible by n.
(b) If (z−1, n) = 1, then at least one of the numbers zi, i = 0, 1, . . ., n−2,
is divisible by n.

## Solution

(a) Suppose to the contrary that none of the numbers z0, z1, . . . , zn−1 is
divisible by n. Then two of these numbers, say zk and zl (0 \leqk < l \leq
n −1), are congruent modulo n, and thus n | zl −zk = zk+1zl−k−1.
But since (n, z) = 1, this implies n | zl−k−1, which is a contradiction.
(b) Again suppose the contrary, that none of z0, z1, . . . , zn−2 is divisible
by n. Since (z−1, n) = 1, this is equivalent to n ∤(z−1)zj, i.e., zk ̸\equiv1
(mod n) for all k = 1, 2, . . ., n −1. But since (z, n) = 1, we also have
that zk ̸\equiv0 (mod n). It follows that there exist k, l, 1 \leqk < l \leqn −1
such that zk \equivzl, i.e., zl−k \equiv1 (mod n), which is a contradiction.
