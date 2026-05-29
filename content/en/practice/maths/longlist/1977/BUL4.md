---
title: "IMO 1977 LL BUL4"
description: "We are given n points in space. Some pairs of these points"
date: "2026-05-29T11:51:44+07:00"
tags: ["imo", "longlist", "mathematics", "olympiad"]
categories: ["mathematics"]
year: 1977
type: "longlist"
origin: "BUL"
weight: 197700004
draft: false
---

# IMO 1977 LL BUL4

**Origin:** BUL

## Problem

We are given n points in space. Some pairs of these points
are connected by line segments so that the number of segments equals
[n2/4], and a connected triangle exists. Prove that any point from which
the maximal number of segments starts is a vertex of a connected triangle.

## Solution

Consider any vertex vn from which the maximal number d of seg-
ments start, and suppose it is not a vertex of a triangle. Let A =
{v1, v2, . . . , vd} be the set of points that are connected to vn, and let
B = {vd+1, vd+2, . . . , vn} be the set of the other points. Since vn is not
a vertex of a triangle, there is no segment both of whose vertices lie in
A; i.e., each segment has an end in B. Thus, if dj denotes the number of
segments at vj and m denotes the total number of segments, we have
m \leqdd+1 + dd+2 + \cdot \cdot \cdot + dn \leqd(n −d) \leq
n2

= m.
This means that each inequality must be equality, implying that each
point in B is a vertex of d segments, and each of these segments has the
other end in A. Then there is no triangle at all, which is a contradiction.
