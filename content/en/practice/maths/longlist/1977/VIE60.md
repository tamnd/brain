---
title: "IMO 1977 LL VIE60"
description: "Suppose x0, x1, . . . , xn are integers and x0 > x1 > \cdot \cdot \cdot > xn."
date: "2026-05-29T11:51:44+07:00"
tags: ["imo", "longlist", "mathematics", "olympiad"]
categories: ["mathematics"]
year: 1977
type: "longlist"
origin: "VIE"
weight: 197700060
draft: false
---

# IMO 1977 LL VIE60

**Origin:** VIE

## Problem

Suppose x0, x1, . . . , xn are integers and x0 > x1 > \cdot \cdot \cdot > xn.
Prove that at least one of the numbers |F(x0)|, |F(x1)|, |F(x2)|, . . . ,
|F(xn)|, where
F(x) = xn + a1xn−1 + \cdot \cdot \cdot + an,
ai \inR, i = 1, . . . , n,
is greater than n!
2n .

## Solution

By Lagrange’s interpolation formula we have
F(x) =
n

j=0
F(xj)
$
i̸=j(x −xj)
$
i̸=j(xi −xj).
Since the leading coeﬃcient in F(x) is 1, it follows that
1 =
n

j=0
F(xj)
$
i̸=j(xi −xj) .
Since

-
i̸=j
(xi −xj)

=
j−1
-
i=0
|xi −xj|
n
-
i=j+1
|xi −xj| \geqj!(n −j)!,

we have
1 \leq
n

j=0
|F(xj)|
$
i̸=j(xi −xj)

\leq1
n!
n

j=0
n
j

|F(xj)| \leq2n
n! max |F(xj)|.
Now the required inequality follows immediately.
