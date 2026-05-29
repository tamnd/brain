---
title: "IMO 1977 LL HUN25"
description: "Prove the identity"
date: "2026-05-29T11:51:44+07:00"
tags: ["imo", "longlist", "mathematics", "olympiad"]
categories: ["mathematics"]
year: 1977
type: "longlist"
origin: "HUN"
weight: 197700025
draft: false
---

# IMO 1977 LL HUN25

**Origin:** HUN

## Problem

Prove the identity
(z + a)n = zn + a
n

k=1
n
k

(a −kb)k−1(z + kb)n−k.

## Solution

Let
fn(z) = zn + a
n

k=1
n
k

(a −kb)k−1(z + kb)n−k.
We shall prove by induction on n that fn(z) = (z + a)n. This is trivial for
n = 1. Suppose that the statement is true for some positive integer n −1.
Then
f ′
n(z) = nzn−1 + a
n−1

k=1
n
k

(n −k)(a −kb)k−1(z + kb)n−k−1
= nzn−1 + na
n−1

k=1
n −1
k

(a −kb)k−1(z + kb)n−k−1
= nfn−1(z) = n(z + a)n−1.
It remains to prove that fn(−a) = 0. For z = −a we have by the lemma
of (SL81-13),
fn(−a) = (−a)n + a
n

k=1
n
k

(−1)n−k(a −kb)n−1
= a
n

k=0
n
k

(−1)n−k(a −kb)n−1 = 0.
