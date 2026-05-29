---
title: "IMO 1967 LL GBR18"
description: "If x is a positive rational number, show that x can be uniquely"
date: "2026-05-29T11:51:44+07:00"
tags: ["imo", "longlist", "mathematics", "olympiad"]
categories: ["mathematics"]
year: 1967
type: "longlist"
origin: "GBR"
weight: 196700018
draft: false
---

# IMO 1967 LL GBR18

**Origin:** GBR

## Problem

If x is a positive rational number, show that x can be uniquely
expressed in the form
x = a1 + a2
2! + a3
3! + \cdot \cdot \cdot ,
where a1, a2, . . . are integers, 0 \leqan \leqn −1 for n > 1, and the series
terminates.
Show also that x can be expressed as the sum of reciprocals of diﬀerent
integers, each of which is greater than 106.

## Solution

In the ﬁrst part, it is suﬃcient to show that each rational number of the
form m/n!, m, n \inN, can be written uniquely in the required form. We
prove this by induction on n.
The statement is trivial for n = 1. Let us assume it holds for n −1, and
let there be given a rational number m/n!. Let us take an \in{0, . . ., n−1}
such that m −an = nm1 for some m1 \inN. By the inductive hypothesis,
there are unique a1 \inN0, ai \in{0, . . ., i −1} (i = 1, . . . , n −1) such that
m1/(n −1)! = n−1
i=1 ai/i!, and then
m
n! =
m1
(n −1)! + an
n! =
n

i=1
ai
i! ,
as desired. On the other hand, if m/n! = n
i=1 ai/i!, multiplying by n! we
see that m −an must be a multiple of n, so the choice of an was unique
and therefore the representation itself. This completes the induction.
In particular, since ai | i! and i!/ai > (i−1)! \geq(i −1)!/ai−1, we conclude
that each rational q, 0 < q < 1, can be written as the sum of diﬀerent
reciprocals.
Now we prove the second part. Let x > 0 be a rational number. For
any integer m > 106, let n > m be the greatest integer such that y =
x−1
m −
m+1 −\cdot \cdot \cdot−1
n > 0. Then y can be written as the sum of reciprocals
of diﬀerent positive integers, which all must be greater than n. The result
follows immediately.
