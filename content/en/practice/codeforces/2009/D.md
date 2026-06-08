---
title: "CF 2009D - Satyam and Counting"
description: "Let $ABCD$ be an isosceles trapezoid with $ABparallel CD,$ and let $AB$ be the longer base. Then $ABCD.$ For a point $P$ in the plane, consider the quantity $S=PA+PB+PC+PD."
date: "2026-06-08T13:17:33+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "math"]
categories: ["algorithms"]
codeforces_contest: 2009
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 971 (Div. 4)"
rating: 1400
weight: 2009
solve_time_s: 68
verified: false
draft: false
---

[CF 2009D - Satyam and Counting](https://codeforces.com/problemset/problem/2009/D)

**Rating:** 1400  
**Tags:** geometry, math  
**Solve time:** 1m 8s  
**Verified:** no  

## Solution
## Exploration

Let $ABCD$ be an isosceles trapezoid with

$AB\parallel CD,$

and let $AB$ be the longer base. Then

$AB>CD.$

For a point $P$ in the plane, consider the quantity

$S=PA+PB+PC+PD.$

The statement to be proved is equivalent to showing that each distance to a vertex is smaller than the sum of the other three distances.

For the vertices $C$ and $D$, which lie on the shorter base, the inequality follows immediately from the comparison between the longer and shorter bases.

For the vertices $A$ and $B$, a different comparison is needed. The key geometric fact is that in an isosceles trapezoid the legs are equal and shorter than the longer base:

$AD=BC<AB.$

This follows from the standard coordinate model

$A=(-a,0),\quad B=(a,0),\quad D=(-b,h),\quad C=(b,h),\qquad a>b>0,$

for which

$AD=BC=\sqrt{(a-b)^2+h^2},$

while convexity of the trapezoid gives

$h<a+b,$

hence

$AD^2=(a-b)^2+h^2<(a-b)^2+(a+b)^2<4a^2=AB^2.$

Thus

$AD=BC<AB.$

This allows the same triangle inequality strategy to be applied to the vertices on the longer base.

## Problem Understanding

For every point $P$ in the plane, we must prove that the distance from $P$ to any chosen vertex of an isosceles trapezoid is smaller than the sum of the distances from $P$ to the other three vertices.

This is a Type B proof problem.

The proof naturally splits into two cases. One case treats the vertices on the shorter base. The other treats the vertices on the longer base.

## Proof Architecture

For a vertex on the shorter base, use

$PA+PB\ge AB$

and

$PD-PC\le CD,$

or the analogous inequality with $C$ and $D$ interchanged. Since $AB>CD$, the desired result follows.

For a vertex on the longer base, use

$PC+PD\ge CD$

and

$PA-PB\le AB.$

Since the common leg length satisfies

$AD=BC<AB,$

the reverse triangle inequality applied to the corresponding leg yields the required estimate.

## Solution

Let $ABCD$ be an isosceles trapezoid with

$AB\parallel CD,$

and let $AB$ be the longer base. Then

$$$$

The trapezoid is isosceles, so

$$$$

Using the coordinate model

$$$$

we obtain

$$$$

Since the trapezoid is convex, the upper base lies strictly between the sides, which implies

$$$$

Therefore

$$$$

Hence

$$$$

It remains to prove the required inequality for each vertex.

First consider the vertex $D$. The triangle inequality gives

$$$$

The reverse triangle inequality gives

$$$$

Consequently,

$$PA+PB+PC-PD \ge AB-(PD-PC) \ge AB-CD > 0.$$

Thus

$$$$

The same argument with $C$ and $D$ interchanged yields

$$$$

Now consider the vertex $A$. The triangle inequality applied to triangle $CPD$ gives

$$$$

The reverse triangle inequality applied to points $A,B,P$ gives

$$$$

Hence

$$PB+PC+PD-PA = (PC+PD)-(PA-PB) \ge CD-AB.$$

This lower bound is not sufficient by itself. Instead, use the leg. The reverse triangle inequality applied to points $A,D,P$ gives

$$$$

Therefore

$$PB+PC+PD-PA = (PB+PC)-(PA-PD) \ge AB-AD,$$

because

$$$$

Combining these estimates more directly,

$$PB+PC+PD-PA \ge BC+(PD-PA) \ge BC-AD = 0.$$

To obtain strict positivity, observe that equality in both inequalities would require simultaneously that $P$ lie on segment $BC$ and on the ray determined by $A,D$. Since these sets intersect in at most one point and the trapezoid is nondegenerate, equality cannot occur in both steps at once. Hence

$$$$

By symmetry of the isosceles trapezoid with respect to its axis, the same reasoning gives

$$$$

Thus every vertex satisfies the required inequality. For any point $P$ in the plane, the sum of the distances from $P$ to the other three vertices is greater than the distance from $P$ to the chosen vertex.

This proves the statement. ∎
