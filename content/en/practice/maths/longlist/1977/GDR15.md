---
title: "IMO 1977 LL GDR15"
description: "Let n be an integer greater than 1. In the Cartesian coordinate"
date: "2026-05-29T11:51:44+07:00"
tags: ["imo", "longlist", "mathematics", "olympiad"]
categories: ["mathematics"]
year: 1977
type: "longlist"
origin: "GDR"
weight: 197700015
draft: false
---

# IMO 1977 LL GDR15

**Origin:** GDR

## Problem

Let n be an integer greater than 1. In the Cartesian coordinate
system we consider all squares with integer vertices (x, y) such that 1 \leq
x, y \leqn. Denote by pk (k = 0, 1, 2, . . . ) the number of pairs of points that
are vertices of exactly k such squares. Prove that 
k(k −1)pk = 0.

## Solution

Each segment is an edge of at most two squares and a diagonal of at most
one square. Therefore pk = 0 for k > 3, and we have to prove that
p0 = p2 + 2p3.
(1)
Let us calculate the number q(n) of considered squares. Each of these
squares is inscribed in a square with integer vertices and sides paral-
lel to the coordinate axes. There are (n −s)2 squares of side s with
integer vertices and sides parallel to the coordinate axes, and each of
them circumscribes exactly s of the considered squares. It follows that
q(n) = n−1
s=1 (n −s)2s = n2(n2 −1)/12. Computing the number of edges
and diagonals of the considered squares in two ways, we obtain that
p1 + 2p2 + 3p3 = 6q(n).
(2)
On the other hand, the total number of segments with endpoints in the
considered integer points is given by
p0 + p1 + p2 + p3 =
n2

= n2(n2 −1)
= 6q(n).
(3)
Now (1) follows immediately from (2) and (3).
