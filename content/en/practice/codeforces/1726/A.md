---
title: "CF 1726A - Mainak and Array"
description: "We have a collection of planets, and every planet belongs to some orbit. Multiple planets may share the same orbit. There are two ways to destroy planets. The first destroys exactly one planet for a cost of 1. The second destroys every planet on a chosen orbit for a cost of c."
date: "2026-06-09T18:58:55+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1726
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 819 (Div. 1 + Div. 2) and Grimoire of Code Annual Contest 2022"
rating: 900
weight: 1726
solve_time_s: 149
verified: false
draft: false
---

[CF 1726A - Mainak and Array](https://codeforces.com/problemset/problem/1726/A)

**Rating:** 900  
**Tags:** greedy, math  
**Solve time:** 2m 29s  
**Verified:** no  

## Solution
## Problem Understanding

We have a collection of planets, and every planet belongs to some orbit. Multiple planets may share the same orbit.

There are two ways to destroy planets. The first destroys exactly one planet for a cost of 1. The second destroys every planet on a chosen orbit for a cost of `c`.

For each orbit, we must decide how to remove all planets on that orbit. The goal is to minimize the total cost over all orbits.

The constraints are very small. There are at most 100 planets and orbit numbers are also at most 100. Even quadratic solutions would easily fit, but the structure of the problem allows a much simpler approach.

A common mistake is to think globally and try to combine decisions between different orbits. The cost contribution of one orbit is completely independent of every other orbit.

Consider the input:

```
1
5 2
7 7 7 7 7
```

There are five planets on orbit 7. Destroying them one by one costs 5. Destroying the whole orbit costs 2. The correct contribution is `min(5, 2) = 2`.

Now consider:

```
1
2 2
1 2
```

Each orbit appears once. Destroying a whole orbit costs 2, while destroying
