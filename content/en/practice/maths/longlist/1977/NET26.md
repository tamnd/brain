---
title: "IMO 1977 LL NET26"
description: "Let p be a prime number greater than 5. Let V be the collection"
date: "2026-05-29T11:51:44+07:00"
tags: ["imo", "longlist", "mathematics", "olympiad"]
categories: ["mathematics"]
year: 1977
type: "longlist"
origin: "NET"
weight: 197700026
draft: false
---

# IMO 1977 LL NET26

**Origin:** NET

## Problem

Let p be a prime number greater than 5. Let V be the collection
of all positive integers n that can be written in the form n = kp + 1 or
n = kp −1 (k = 1, 2, . . .). A number n \inV is called indecomposable in V
if it is impossible to ﬁnd k, l \inV such that n = kl. Prove that there exists
a number N \inV that can be factorized into indecomposable factors in V
in more than one way.

## Solution

The result is an immediate consequence (for G = {−1, 1}) of the following
generalization.
(1) Let G be a proper subgroup of Z∗
n (the multiplicative group of residue
classes modulo n coprime to n), and let V be the union of elements

of G. A number m \inV is called indecomposable in V if there do
not exist numbers p, q \inV , p, q ̸\in{−1, 1}, such that pq = m. There
exists a number r \inV that can be expressed as a product of elements
indecomposable in V in more than one way.
First proof. We shall start by proving the following lemma.
Lemma. There are inﬁnitely many primes not in V that do not divide n.
Proof. There is at least one such prime: In fact, any number other than
\pm1 not in V must have a prime factor not in V , since V is closed
under multiplication. If there were a ﬁnite number of such primes, say
p1, p2, . . . , pk, then one of the numbers p1p2 \cdot \cdot \cdot pk +n, p2
1p2 \cdot \cdot \cdot pk +n is
not in V and is coprime to n and p1, . . . , pk, which is a contradiction.
[This lemma is actually a direct consequence of Dirichlet’s theorem.]
Let us consider two such primes p, q that are congruent modulo n. Let pk
be the least power of p that is in V . Then pk, qk, pk−1q, pqk−1 belong to
V and are indecomposable in V . It follows that
r = pk \cdot qk = pk−1q \cdot pqk−1
has the desired property.
Second proof. Let p be any prime not in V that does not divide n, and let
pk be the least power of p that is in V . Obviously pk is indecomposable
in V . Then the number
r = pk \cdot (pk−1 + n)(p + n) = p(pk−1 + n) \cdot pk−1(p + n)
has at least two diﬀerent factorizations into indecomposable factors.
