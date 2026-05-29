---
title: "IMO 1967 LL USS59"
description: "On the circle with center O and radius 1 the point A0 is"
date: "2026-05-29T11:51:44+07:00"
tags: ["imo", "longlist", "mathematics", "olympiad"]
categories: ["mathematics"]
year: 1967
type: "longlist"
origin: "USS"
weight: 196700059
draft: false
---

# IMO 1967 LL USS59

**Origin:** USS

## Problem

On the circle with center O and radius 1 the point A0 is
ﬁxed and points A1, A2, . . . , A999, A1000 are distributed in such a way
that \angleA0OAk = k (in radians). Cut the circle at points A0, A1, . . . , A1000.
How many arcs with diﬀerent lengths are obtained?

## Solution

By the arc AB we shall always mean the positive arc AB. We denote by
|AB| the length of arc AB. Let a basic arc be one of the n + 1 arcs into
which the circle is partitioned by the points A0, A1, . . . , An, where n \inN.
Suppose that ApA0 and A0Aq are the basic arcs with an endpoint at A0,
and that xn, yn are their lengths, respectively. We show by induction on
n that for each n the length of a basic arc is equal to xn, yn or xn + yn.
The statement is trivial for n = 1. Assume that it holds for n, and let
AiAn+1, An+1Aj be basic arcs. We shall prove that these two arcs have
lengths xn, yn, or xn+yn. If i, j are both strictly positive, then |AiAn+1| =

|Ai−1An| and |An+1Aj| = |AnAj−1| are equal to xn, yn, or xn +yn by the
inductive hypothesis.
Let us assume now that i = 0, i.e., that ApAn+1 and An+1A0 are
basic arcs. Then |ApAn+1| = |A0An+1−p| \geq|A0Aq| = yn and sim-
ilarly |An+1Aq| \geqxn, but |ApAq| = xn + yn, from which it follows
that |ApAn+1| = |A0Aq| = yn and consequently n + 1 = p + q. Also,
xn+1 = |An+1A0| = yn −xn and yn+1 = yn. Now, all basic arcs have
lengths yn −xn, xn, yn, xn + yn. A presence of a basic arc of length
xn + yn would spoil our inductive step. However, if any basic arc AkAl
has length xn + yn, then we must have l −q = k −p because 2\pi is ir-
rational, and therefore the arc AkAl contains either the point Ak−p (if
k \geqp) or the point Ak+q (if k < p), which is impossible; hence, the proof
is complete for i = 0. The proof for j = 0 is analogous. This completes
the induction.
It can be also seen from the above considerations that the basic arcs take
only two distinct lengths if and only if n = p + q −1. If we denote by nk
the sequence of n’s for which this holds, and by pk, qk the sequences of
the corresponding p, q, we have p1 = q1 = 1 and
(pk+1, qk+1) =
(pk + qk, qk), if {pk/(2\pi)} + {qk/(2\pi)} > 1,
(pk, pk + qk), if {pk/(2\pi)} + {qk/(2\pi)} < 1.
It is now “easy” to calculate that p19 = p20 = 333, q19 = 377, q20 = 710,
and thus n19 = 709 < 1000 < 1042 = n20. It follows that the lengths of
the basic arcs for n = 1000 take exactly three diﬀerent values.
