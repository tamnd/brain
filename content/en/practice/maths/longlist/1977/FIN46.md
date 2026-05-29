---
title: "IMO 1977 LL FIN46"
description: "Let f be a strictly increasing function deﬁned on the set of real"
date: "2026-05-29T11:51:44+07:00"
tags: ["imo", "longlist", "mathematics", "olympiad"]
categories: ["mathematics"]
year: 1977
type: "longlist"
origin: "FIN"
weight: 197700046
draft: false
---

# IMO 1977 LL FIN46

**Origin:** FIN

## Problem

Let f be a strictly increasing function deﬁned on the set of real
numbers. For x real and t positive, set
g(x, t) = f(x + t) −f(x)
f(x) −f(x −t).
Assume that the inequalities
2−1 < g(x, t) < 2
hold for all positive t if x = 0, and for all t \leq|x| otherwise.
Show that
14−1 < g(x, t) < 14
for all real x and positive t.

## Solution

We need to consider only the case t > |x|. There is no loss of generality
in assuming x > 0.
To obtain the estimate from below, set
a1 = f

−x + t

−f(−(x + t)),
a2 = f(0) −f

−x + t

,
a3 = f
x + t

−f(0),
a4 = f(x + t) −f
x + t

.
Since −(x + t) < x −t and x < (x + t)/2, we have f(x) −f(x −t) \leq
a1 + a2 + a3. Since 2−1 < aj+1/aj < 2, it follows that
g(x, t) >
a4
a1 + a2 + a3
>
a3/2
4a3 + 2a3 + a3
= 14−1.
To obtain the estimate from above, set

b1 = f(0) −f

−x + t

,
b2 = f
x + t

−f(0),
b3 = f
2(x + t)

−f
x + t

,
b4 = f(x + t) −f
2(x + t)

.
If t < 2x, then x −t < −(x + t)/3 and therefore f(x) −f(x −t) \geqb1.
If t \geq2x, then (x + t)/3 \leqx and therefore f(x) −f(x −t) \geqb2. Since
2−1 < bj+1/bj < 2, we get
g(x, t) < b2 + b3 + b4
min{b1, b2} < b2 + 2b2 + 4b2
b2/2
= 14.
