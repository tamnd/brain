---
title: "CF 105745E - Cube"
description: "We are given eight points in three-dimensional space, and the task is to decide whether these points can be the vertices of a cube after an appropriate ordering. The points are not guaranteed to already be nicely arranged, and they may be given in any order."
date: "2026-06-25T21:08:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105745
codeforces_index: "E"
codeforces_contest_name: "AGM 2025 Qualification Round"
rating: 0
weight: 105745
solve_time_s: 17
verified: false
draft: false
---

[CF 105745E - Cube](https://codeforces.com/problemset/problem/105745/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are given eight points in three-dimensional space, and the task is to decide whether these points can be the vertices of a cube after an appropriate ordering. The points are not guaranteed to already be nicely arranged, and they may be given in any order. The question is purely geometric: can we reinterpret these points as the corners of a regular hexahedron where all edges have equal length and all faces are squares?

The key object we are trying to recognize is a rigid structure. A cube has a very specific distance pattern among its vertices. If you take any vertex, it has exactly three neighbors at the same distance, and those three edges are mutually orthogonal. All other vertices are either at a la
