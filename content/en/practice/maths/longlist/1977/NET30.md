---
title: "IMO 1977 LL NET30"
description: "A triangle ABC with \angleA = 30◦and \angleC = 54◦is given. On"
date: "2026-05-29T11:51:44+07:00"
tags: ["imo", "longlist", "mathematics", "olympiad"]
categories: ["mathematics"]
year: 1977
type: "longlist"
origin: "NET"
weight: 197700030
draft: false
---

# IMO 1977 LL NET30

**Origin:** NET

## Problem

A triangle ABC with \angleA = 30◦and \angleC = 54◦is given. On
BC a point D is chosen such that \angleCAD = 12◦. On AB a point E is
chosen such that \angleACE = 6◦. Let S be the point of intersection of AD
and CE. Prove that BS = BC.

## Solution

Suppose \angleSBA = x. By the trigonometric form of Ceva’s theorem we
have
sin(96◦−x)
sin x
sin 18◦
sin 12◦
sin 6◦
sin 48◦= 1.
(1)
We claim that x = 12◦is a solution of this equation. To prove this, it
is enough to show that sin 84◦sin 6◦sin 18◦= sin 48◦sin 12◦sin 12◦, which
is equivalent to sin 18◦= 2 sin 48◦sin 12◦= cos 36◦−cos60◦. The last
equality can be checked directly.
Since the equation is equivalent to (sin 96◦cot x −cos 96◦) sin 6◦sin 18◦=
sin 48◦sin 12◦, the solution x \in[0, \pi) is unique. Hence x = 12◦.
Second solution.
We know that if a, b, c, a′, b′, c′ are points on the unit
circle in the complex plane, the lines aa′, bb′, cc′ are concurrent if and
only if
(a −b′)(b −c′)(c −a′) = (a −c′)(b −a′)(c −b′).
(1)
We shall prove that x = 12◦. We may suppose that ABC is the triangle
in the complex plane with vertices a = 1, b = ϵ9, c = ϵ14, where ϵ =
cos \pi
15 + i sin \pi
15. If a′ = ϵ12, b′ = ϵ28, c′ = ϵ, our task is the same as
proving that lines aa′, bb′, cc′ are concurrent, or by (1) that
(1 −ϵ28)(ϵ9 −ϵ)(ϵ14 −ϵ12) −(1 −ϵ)(ϵ9 −ϵ12)(ϵ14 −ϵ28) = 0.
The last equality holds, since the left-hand side is divisible by the mini-
mum polynomial of ϵ: z8 + z7 −z5 −z4 −z3 + z + 1.
