---
title: "CF 1344A - Hilbert's Hotel"
description: "We are dealing with an infinite hotel where each room, labeled by an integer, has exactly one guest. A shuffling rule is applied where each guest moves from their current room $k$ to a new room $k + a{k bmod n}$, where $a$ is an array of length $n$."
date: "2026-06-11T15:07:52+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1344
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 639 (Div. 1)"
rating: 1600
weight: 1344
solve_time_s: 320
verified: false
draft: false
---

[CF 1344A - Hilbert's Hotel](https://codeforces.com/problemset/problem/1344/A)

**Rating:** 1600  
**Tags:** math, number theory, sortings  
**Solve time:** 5m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We are dealing with an infinite hotel where each room, labeled by an integer, has exactly one guest. A shuffling rule is applied where each guest moves from their current room $k$ to a new room $k + a_{k \bmod n}$, where $a$ is an array of length $n$. The task is to determine whether this shuffling produces a unique guest in every room or if collisions occur.

The input consists of multiple test cases, each specifying $n$ and the array $a$. The output is "YES" if the shuffle preserves uniqueness and "NO" otherwise. With $n$ up to $2 \cdot 10^5$ and $t$ up to $10^4$, the total array elements across all test cases are bounded at (2 \cdot 10^5\
