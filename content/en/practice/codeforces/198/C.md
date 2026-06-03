---
title: "CF 198C - Delivering Carcinogen"
description: "We are asked to compute the minimum time for Qwerty's ship to intercept a moving planet in a 2D plane. The star Diatar is at the origin, Persephone orbits the star in a perfect circle of radius $R$ at constant linear speed $vp$, and Qwerty's ship starts at some arbitrary…"
date: "2026-06-03T16:20:50+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "geometry"]
categories: ["algorithms"]
codeforces_contest: 198
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 125 (Div. 1)"
rating: 2400
weight: 198
solve_time_s: 45
verified: false
draft: false
---

[CF 198C - Delivering Carcinogen](https://codeforces.com/problemset/problem/198/C)

**Rating:** 2400  
**Tags:** binary search, geometry  
**Solve time:** 45s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to compute the minimum time for Qwerty's ship to intercept a moving planet in a 2D plane. The star Diatar is at the origin, Persephone orbits the star in a perfect circle of radius $R$ at constant linear speed $v_p$, and Qwerty's ship starts at some arbitrary position $(x, y)$ with maximum speed $v$ that is strictly faster than Persephone. The ship cannot approach the star closer than a radius $r < R$. The goal is to determine how quickly Qwerty can meet the planet, given these motion constraints.

The input provides the planet's initial coordinates $(x_p, y_p)$ and orbital speed $v_p$, and the ship's initial coordinates $(x, y)$, maximum speed $v$, and minimum safe distance $r$. The output is the minimum possible delivery time.

The problem's constraints ensure that $v > v_p$ and both the ship and planet start outside the forbidden zone around the star. Because all coordinates and speeds are up to $10^4$, the algorithm must operate efficiently. A naive approach that simulates the ship's motion in small time increments would require tiny step sizes to guarantee precision within $10^{-6}$, leading to billions of iterations and exceeding the 2-second time limit. Therefore, a more analytical or numerical approach is required.

Non-obvious edge cases include scenarios where the ship starts already aligned with the planet's orbit, requiring direct interception along the tangent, or where the ship must skim close to the safe radius $r$ to minimize time. A careless solution that ignores the inner forbidden circle would compute a shorter path than physically possible.

## Approaches

The brute-force method would attempt to simulate the ship's trajectory over time. At each small time step, it would move the ship in the direction of the planet's predicted position, compute distance to the forbidden radius, and adjust motion. While conceptually corre
