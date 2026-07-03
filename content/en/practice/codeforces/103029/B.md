---
title: "CF 103029B - John, Katya"
description: "The exercise refers to the “basic compression lemma (85)”, but the statement of (85) is not included in the provided excerpt of Section 7.2.1.3."
date: "2026-07-04T02:20:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103029
codeforces_index: "B"
codeforces_contest_name: "Quick (fast) contest #1"
rating: 0
weight: 103029
solve_time_s: 66
verified: false
draft: false
---

[CF 103029B - John, Katya](https://codeforces.com/problemset/problem/103029/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** no  

## Solution
The exercise refers to the “basic compression lemma (85)”, but the statement of (85) is not included in the provided excerpt of Section 7.2.1.3.

Without the exact formulation of (85), the claim to be proved is not well-determined, since the section contains several distinct “compression” transformations between representations of combinations, including the mappings between bit strings $a_{n-1}\ldots a_0$, decreasing sequences $c_t\ldots c_1$, and nonnegative compositions $q_t\ldots q_0$.

The proof depends on identifying which of these transformations is being asserted as a lemma in equation (85). Once that statement is available, the argument can be carried out directly by showing the map is well-defined, invertible, and preserves the required structure (typically lexicographic order or adjacency in the generation sequence), using the monotonicity constraints in (3), (6), or (11) depending on the formulation.

Provide the explicit statement of equation (85), and the full proof can be written in Knuth’s notation and style.
