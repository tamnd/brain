---
title: "IMO 1967 LL CZS12"
description: "Given a segment AB of the length 1, deﬁne the set M of points"
date: "2026-05-29T11:51:44+07:00"
tags: ["imo", "longlist", "mathematics", "olympiad"]
categories: ["mathematics"]
year: 1967
type: "longlist"
origin: "CZS"
weight: 196700012
draft: false
---

# IMO 1967 LL CZS12

**Origin:** CZS

## Problem

Given a segment AB of the length 1, deﬁne the set M of points
in the following way: it contains the two points A, B, and also all points
obtained from A, B by iterating the following rule: (∗) for every pair of
points X, Y in M, the set M also contains the point Z of the segment
XY for which Y Z = 3XZ.
(a) Prove that the set M consists of points X from the segment AB for
which the distance from the point A is either
AX = 3k
4n
or
AX = 3k −2
4n
,
where n, k are nonnegative integers.
(b) Prove that the point X0 for which AX0 = 1/2 = X0B does not belong
to the set M.

## Solution

Let us denote by Mn the set of points of the segment AB obtained from A
and B by not more than n iterations of (∗). It can be proved by induction
that
Mn =
.
X \inAB | AX = 3k
4n or 3k −2
4n
for some k \inN
;
.
Thus (a) immediately follows from M = % Mn. It also follows that if
a, b \inN and a/b \inM, then 3 | a(b −a). Therefore 1/2 ̸\inM.
