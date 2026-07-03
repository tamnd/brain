---
title: "CF 103031C - \u0428\u0435\u0441\u0442\u0438\u0437\u043d\u0430\u0447\u043d\u044b\u0435 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u044b"
description: "The exercise refers to the “basic compression lemma (85)”, but the statement of (85) is not included in the provided excerpt of Section 7.2.1.3."
date: "2026-07-04T02:12:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103031
codeforces_index: "C"
codeforces_contest_name: "\u0418\u043d\u0434\u0438\u0432\u0438\u0434\u0443\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0438 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2021"
rating: 0
weight: 103031
solve_time_s: 146
verified: false
draft: false
---

[CF 103031C - \u0428\u0435\u0441\u0442\u0438\u0437\u043d\u0430\u0447\u043d\u044b\u0435 \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u044b](https://codeforces.com/problemset/problem/103031/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 26s  
**Verified:** no  

## Solution
The exercise refers to the “basic compression lemma (85)”, but the statement of (85) is not included in the provided excerpt of Section 7.2.1.3.

Without the exact formulation of (85), the claim to be proved is not well-determined, since the section contains several distinct “compression” transformations between representations of combinations, including the mappings between bit strings $a_{n-1}\ldots a_0$, decreasing sequences $c_t\ldots c_1$, and nonnegative compositions $q_t\ldots q_0$.

The proof depends on identifying which of these transformations is being asserted as a lemma in equation (85). Once that statement is available, the argument can be carried out directly by showing the map is well-defined, invertible, and preserves the required structure (typically lexicographic order or adjacency in the generation sequence), using the monotonicity constraints in (3), (6), or (11) depending on the formulation.

Provide the explicit statement of equation (85), and the full proof can be written in Knuth’s notation and style.
