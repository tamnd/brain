---
title: "IMO 1977 LL USS51"
description: "Several segments, which we shall call white, are given, and"
date: "2026-05-29T11:51:44+07:00"
tags: ["imo", "longlist", "mathematics", "olympiad"]
categories: ["mathematics"]
year: 1977
type: "longlist"
origin: "USS"
weight: 197700051
draft: false
---

# IMO 1977 LL USS51

**Origin:** USS

## Problem

Several segments, which we shall call white, are given, and
the sum of their lengths is 1. Several other segments, which we shall call
black, are given, and the sum of their lengths is 1. Prove that every such
system of segments can be distributed on the segment that is 1.51 long in
the following way: Segments of the same color are disjoint, and segments
of diﬀerent colors are either disjoint or one is inside the other. Prove
that there exists a system that cannot be distributed in that way on the
segment that is 1.49 long.

## Solution

We shall use the following algorithm:
Choose a segment of maximum length (“basic” segment) and put on it
unused segments of the opposite color without overlapping, each time
of the maximum possible length, as long as it is possible. Repeat the
procedure with remaining segments until all the segments are used.
Let us suppose that the last basic segment is black. Then the length of
the used part of any white basic segment is greater than the free part,
and consequently at least one-half of the length of the white segments has
been used more than once. Therefore all basic segments have total length
at most 1.5 and can be distributed on a segment of length 1.51.
On the other hand, if we are given two white segments of lengths 0.5 and
two black segments of lengths 0.999 and 0.001, we cannot distribute them
on a segment of length less than 1.499.
