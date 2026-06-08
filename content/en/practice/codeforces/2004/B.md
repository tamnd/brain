---
title: "CF 2004B - Game with Doors"
description: "We are asked to prevent two people, Alice and Bob, from meeting in a row of 100 rooms separated by 99 doors. Each person is confined to a segment of rooms: Alice to [l, r] and Bob to [L, R], but we do not know their exact positions within their segments."
date: "2026-06-08T13:43:13+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2004
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 169 (Rated for Div. 2)"
rating: 1000
weight: 2004
solve_time_s: 134
verified: false
draft: false
---

[CF 2004B - Game with Doors](https://codeforces.com/problemset/problem/2004/B)

**Rating:** 1000  
**Tags:** brute force, greedy  
**Solve time:** 2m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to prevent two people, Alice and Bob, from meeting in a row of 100 rooms separated by 99 doors. Each person is confined to a segment of rooms: Alice to `[l, r]` and Bob to `[L, R]`, but we do not know their exact positions within their segments. A door between two consecutive rooms can be locked, and if all doors between two rooms are unlocked, the rooms are reachable from each other. The goal is to lock as few doors as possible so that Alice and Bob cannot reach each other, regardless of where they are within their segments.

The input gives multiple test cases. Each test case consists of two segments, one for Alice and one for Bob. The output is the minimum number of doors that need to be locked to separate them for that test case.

The constraints are small: each segment is within `[1,100]`, and the number of test cases is up to `10^4`. Because the rooms are limited to 100, even a brute-force approach that examines each door is feasible, but the problem has a clear structure that allows a constant-time computation per test case.

A non-obvious edge case occurs when the segments overlap. For instance, if Alice occupies `[2, 5]` and Bob `[4, 6]`, their segments overlap from 4 to 5. A naive approach that only considers the endpoints of the segments might miss the correct minimal separation, which in this case is locking doors 4 and 5, not just one door at the boundary.

## Approaches

The brute-force approach would iterate over all doors between Alice’s and Bob’s segments and count the minimum set that separates any possible position of Alice from any possible position of Bob. This works because there are at most 99 doors and segments of length at most 100. However, for `t = 10^4` test cases, even O(100) per test case is acceptable, but it is unnecessary because the problem has a simpler structure.

The key insight is that the problem reduces to computing the overlap of the two segments. If Alice’s segment is entirely to the left of Bob’s segment (i.e., `r < L`), the minimal number of doors to lock is `L - r`. If Bob’s segment is entirely to the left of Alice’s (`R < l`), the number of doors is `l - R`. If the segments overlap (`l ≤ R` and `L ≤ r`), we can think of the minimal separation as locking all doors in the overlapping region, which amounts to `max(0, min(r, R) - max(l, L) + 1)`. Since Alice and Bob cannot be in the same room, we always need to count at least one door in case of direct adjacency.

This transforms the problem into a simple arithmetic calculation per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(100 * t) | O(1) | Acceptable but unnecessary |
| Optimal | O(t) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the segments `[l, r]` for Alice and `[L, R]` for Bob.
2. Compute the overlap or gap between the segments. If Alice’s right end is before Bob’s left end (`r < L`), there is a gap of `L - r` doors. Locking this many doors between `r` and `L` separates them.
3. If Bob’s right end is before Alice’s left end (`R < l`), there is a gap of `l - R` doors. Locking this many doors separates them.
4. If the segments overlap (`l ≤ R` and `L ≤ r`), calculate the intersection length `min(r, R) - max(l, L) + 1`. Locking all doors in this overlap ensures separation.
5. Output the computed number for each test case.

Why it works: The algorithm directly models the problem constraints. The minimal number of doors needed to separate two segments is exactly the number of doors in the gap if disjoint or the number of doors covering the overlap if segments intersect. This guarantees that no matter where Alice and Bob are, there is at least one locked door between them, preventing any meeting.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    l, r = map(int, input().split())
    L, R =
```
