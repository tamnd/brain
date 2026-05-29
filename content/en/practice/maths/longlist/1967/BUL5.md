---
title: "IMO 1967 LL BUL5"
description: "Solve the system"
date: "2026-05-29T11:51:44+07:00"
tags: ["imo", "longlist", "mathematics", "olympiad"]
categories: ["mathematics"]
year: 1967
type: "longlist"
origin: "BUL"
weight: 196700005
draft: false
---

# IMO 1967 LL BUL5

**Origin:** BUL

## Problem

Solve the system
x2 + x −1 = y,
y2 + y −1 = z,
z2 + z −1 = x.

## Solution

If one of x, y, z is equal to 1 or −1, then we obtain solutions (−1, −1, −1)
and (1, 1, 1). We claim that these are the only solutions to the system.
Let f(t) = t2 + t −1. If among x, y, z one is greater than 1, say x > 1, we
have x < f(x) = y < f(y) = z < f(z) = x, which is impossible. It follows
that x, y, z \leq1.
Suppose now that one of x, y, z, say x, is less than −1. Since mint f(t) =
−5/4, we have x = f(z) \in[−5/4, −1). Also, since f([−5/4, −1)) =
(−1, −11/16) \subseteq(−1, 0) and f((−1, 0)) = [−5/4, −1), it follows that
y = f(x) \in(−1, 0), z = f(y) \in[−5/4, −1), and x = f(z) \in(−1, 0),
which is a contradiction. Therefore −1 \leqx, y, z \leq1.
If −1 < x, y, z < 1, then x > f(x) = y > f(y) = z > f(z) = x, a
contradiction. This proves our claim.
