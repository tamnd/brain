---
title: "IMO 1977 LL HUN24"
description: "Determine all real functions f(x) that are deﬁned and contin-"
date: "2026-05-29T11:51:44+07:00"
tags: ["imo", "longlist", "mathematics", "olympiad"]
categories: ["mathematics"]
year: 1977
type: "longlist"
origin: "HUN"
weight: 197700024
draft: false
---

# IMO 1977 LL HUN24

**Origin:** HUN

## Problem

Determine all real functions f(x) that are deﬁned and contin-
uous on the interval (−1, 1) and that satisfy the functional equation
f(x + y) = f(x) + f(y)
1 −f(x)f(y)
(x, y, x + y \in(−1, 1)).

## Solution

Setting x = y = 0 gives us f(0) = 0. Let us put g(x) = arctanf(x). The
given functional equation becomes tan g(x + y) = tan(g(x) + g(y)); hence
g(x + y) = g(x) + g(y) + k(x, y)\pi,
where k(x, y) is an integer function. But k(x, y) is continuous and k(0, 0) =
0, therefore k(x, y) = 0. Thus we obtain the classical Cauchy’s functional
equation g(x + y) = g(x) + g(y) on the interval (−1, 1), all of whose
continuous solutions are of the form g(x) = ax for some real a. Moreover,
g(x) \in(−\pi, \pi) implies |a| \leq\pi/2.
Therefore f(x) = tan ax for some |a| \leq\pi/2, and this is indeed a solution
to the given equation.
