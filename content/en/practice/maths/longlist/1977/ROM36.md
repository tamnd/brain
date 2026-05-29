---
title: "IMO 1977 LL ROM36"
description: "Consider a sequence of numbers (a1, a2, . . . , a2n). Deﬁne the"
date: "2026-05-29T11:51:44+07:00"
tags: ["imo", "longlist", "mathematics", "olympiad"]
categories: ["mathematics"]
year: 1977
type: "longlist"
origin: "ROM"
weight: 197700036
draft: false
---

# IMO 1977 LL ROM36

**Origin:** ROM

## Problem

Consider a sequence of numbers (a1, a2, . . . , a2n). Deﬁne the
operation
S((a1, a2, . . . , a2n)) = (a1a2, a2a3, . . . , a2n−1a2n, a2na1).
Prove that whatever the sequence (a1, a2, . . . , a2n) is, with ai \in{−1, 1}
for i = 1, 2, . . . , 2n, after ﬁnitely many applications of the operation we
get the sequence (1, 1, . . ., 1).

## Solution

It can be shown by simple induction that Sm(a1, . . . , a2n) = (b1, . . . , b2n),
where
bk =
m
-
i=0
a(m
i )
k+i (assuming that ak+2n = ak).
If we take m = 2n all the binomial coeﬃcients
m
i

apart from i = 0 and
i = m will be even, and thus bk = akak+m = 1 for all k.
