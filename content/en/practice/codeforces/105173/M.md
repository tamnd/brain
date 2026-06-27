---
title: "CF 105173M - House"
description: "We are given a set of distinct points on the plane, and we want to count how many ways we can choose five of them so that they form a specific geometric configuration called a “house”. A valid house consists of five labeled points $A, B, C, D, E$ with a rigid structure."
date: "2026-06-27T08:21:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105173
codeforces_index: "M"
codeforces_contest_name: "The 2024 CCPC National Invitational Contest (Northeast), The 18th Northeast Collegiate Programming Contest"
rating: 0
weight: 105173
solve_time_s: 29
verified: false
draft: false
---

[CF 105173M - House](https://codeforces.com/problemset/problem/105173/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of distinct points on the plane, and we want to count how many ways we can choose five of them so that they form a specific geometric configuration called a “house”.

A valid house consists of five labeled points $A, B, C, D, E$ with a rigid structure. The first four points form a right-angled quadrilateral with equal opposite sides, which forces it to be a rectangle in a fixed cyclic order. The fifth point $E$ is attached to one side of this rectangle and forms an isosceles triangle with two vertices of that side, with an additional constraint that the angle at one corner is obtuse in a specific direction.

The output is the number of distinct 5-point subsets that can be assigned roles $A, B, C, D, E$ satisfying all these geometric constraints. Two houses are considered different if they use different coordinates for at least one of the five points, so we are effectively counting valid labeled structures induced by subsets of points.

The constraints are $n \le 300$, which immediately suggests that cubic or slightly worse-than-quadratic solutions may pass, but anything quartic over all point combinations will not. An $O(n^3)$ solution is on the boundary but acceptable with careful constant factors. This strongly hints that we should enumerate a geometric core structure in $O(n^2)$, then attach the fifth point efficiently.

A subtle issue is overcounting due to multiple valid labelings of the same geometric configuration. Since the problem uses fixed roles $A, B, C, D, E$, any symmetry in the rectangle or triangle can generate multiple interpretations if not carefully anchored. A naive counting method that only finds rectangles or only finds triangles independently would either miss constraints or double count configurations.

Another pitfall is treating the rectangle condition too loosely. For example, selecting four points that form a rectangle but in the wrong order may violate the perpendicularity conditions depending on assignment. Similarly, picking an isosceles triangle point $E$ without enforcing the obtuse angle condition can incorrectly include symmetric configurations where $E$ lies on the wrong side of the base.

## Approaches

The brute-force idea is straightforward: choose any 5 points, try all permutations assigning them to $A, B, C, D, E$, and check all geometric conditions directly. This is correct because it directly verifies the definition. However, the number of choices is $\binom{n}{5} \cdot 120$, which in the worst case is far beyond $300^5$, making it completely infeasible.

The key structure is that four of the points form a very rigid shape: a rectangle. Instead of searching for arbitrary quadruples, we can generate all rectangles from the point set. Rectangles in a point set can be found in $O(n^2)$ by using the fact that diagonals share the same midpoint and length. Once a rectangle is fixed, the role o
