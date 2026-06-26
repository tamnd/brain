---
title: "CF 105712G - Knight Polygon"
description: "We reduce the fraction first, then construct a base loop with fixed unit area contribution. 1. Reduce $p/q$ to lowest terms."
date: "2026-06-26T07:56:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105712
codeforces_index: "G"
codeforces_contest_name: "Rutgers University Programming Contest Fall 2024"
rating: 0
weight: 105712
solve_time_s: 39
verified: false
draft: false
---

[CF 105712G - Knight Polygon](https://codeforces.com/problemset/problem/105712/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** no  

## Solution
## Algorithm Walkthrough

We reduce the fraction first, then construct a base loop with fixed unit area contribution.

1. Reduce $p/q$ to lowest terms. If the construction we build only supports integer areas, we immediately see that any non-integer reducible requirement cannot be represented, so infeasibility cases come from structural parity constraints of the gadget.
2. Transform the area requirement into an integer target $A$ by scaling the polygon construction so that one gadget contributes exactly 1 unit of area. This is achieved by choosing a base cycle whose shoelace area is known.
3. Build a fundamental knight cycle, a closed loop of constant size, whose vertices are chosen so that each edge is a valid knight move and the polygon is simple. The cycle is designed so that it encloses a small region with signed area exactly 1.
4. Repeat this cycle $A$ times in a chain-like fashion. Each repetition is shifted far enough in the plane so that polygons do not intersect. This preserves simplicity while summing areas.
5. Connect consecutive cycles using a
