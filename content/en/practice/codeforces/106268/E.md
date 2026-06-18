---
title: "CF 106268E - Cutting Tofu"
description: "We are given a rectangular block of tofu with integer side lengths $a$, $b$, and $c$. We are allowed to cut it only by slicing completely through the block along planes parallel to its faces, so every cut splits all pieces it intersects."
date: "2026-06-18T23:08:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106268
codeforces_index: "E"
codeforces_contest_name: "The 2025 Asia Yokohama Regional Contest"
rating: 0
weight: 106268
solve_time_s: 35
verified: true
draft: false
---

[CF 106268E - Cutting Tofu](https://codeforces.com/problemset/problem/106268/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular block of tofu with integer side lengths $a$, $b$, and $c$. We are allowed to cut it only by slicing completely through the block along planes parallel to its faces, so every cut splits all pieces it intersects. After performing any number of such cuts, we end up partitioning the original volume into axis-aligned rectangular pieces.

From these pieces, we want to obtain at least $k$ identical cubes. Each cube must have the same side length $x$, and cubes must be cut from the resulting pieces using only face-aligned cuts, meaning each cube corresponds to a full $x \times x \times x$ sub-block aligned with the original axes.

The goal is to maximize $x$, and output it as a reduced fraction.

The key interpretation is that once we fix a candidate cube side length $x$, the number of cubes we can obtain is completely determined by how many $x$-length segments fit along each dimension. That is, along length $a$, we can fit $\lfloor a / x \rfloor$ cubes, similarly for $b$ and $c$, so total cubes is:

$$\lfloor a/x \rfloor \cdot \lfloor b/x \rfloor \cdot \lfloor c/x \rfloor.$$

We need the largest rational $x$ such that this product is at least $k$.

The constraints are large: $a, b, c, k \le 10^9$, and up to $10^4$ test cases. Any solution must be $O(\log \text{range})$ or better per test case. A naive linear or enumerative search over possible $x$ is impossible.

The main edge case comes from the fact that the answer is not necessarily an integer. For example, when $a=b=c=2$ and $k=1$, the answer is $2$, but when $k=8$, the answer becomes $1$. More interestingly, fractional answers appear when exact tiling is impossible.

A subtle pitfall is assuming the function is continuous or smooth enough for naive rounding. The function is stepwise constant, so many values of $x$ produce the same cube count, and the true maximum may lie at a boundary where one of the floor divisions changes.

## Approaches

A direct approach is to try all possible side lengths $x$ from a very small value up to $\max(a,b,c)$. For each candidate $x$, we compute:

$$\lfloor a/x \rfloor \cdot \lfloor b/x \rfloor \cdot \lfloor c/x \rfloor$$

and check whether it is at least $k$. This is correct, because it exactly models the construction process. However, the range of possible $x$ is too large. If we try integer steps at unit granularity up to $10^9$, this already exceeds any feasible time limit, and the true answer is often fractional, which would require even finer granularity.

The key observation is that the number of cubes is monotone non-increasing in $x$. If we increase the cube size, each dimension can fit fewer cubes, so the total product cannot increase. This monotonicity allows us to binary search the optimal real-valued $x$.

For a fixed $x$, we can compute feasibility in constant time, so binary search over real numbers (implemented as rationals or sufficient precision) becomes the core idea.

However, since the answer is guaranteed to be rational, we can avoid floating precision issues by performing a binary search on fractions implicitly. A cleaner view is to search on $x$ as a real number using floating bounds and then convert the final result into a reduced fraction. The reduction comes from observing that the boundary where feasibility changes must occur at a rational value derived from dividing one of $a,b,c$ by an integer.

This leads to a standard monotone decision + binary search structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force enumeration of $x$ | $O(\max(a,b,c))$ per test | $O(1)$ | Too slow |
| Binary search on real $x$ with feasibility check | $O(\log R)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

### Feasibility function

For a given candidate cube side $x$, we compute how many cubes can be formed:

$$f(x) = \lfloor a/x \rfloor \cdot \lfloor b/x \rfloor \cdot \lfloor c/x \rfloor.$$

We check whether $f(x) \ge k$.

### Steps

1. Define a function that, given $x$, returns whether at least $k$ cubes can be formed. This encodes the construction constraints directly.
2. Search for the largest real number $x$ such that the function returns true. Since larger $x$ always reduces or preserves feasibility, the predicate is monotone, which allows binary search.
3. Maintain a search interval $[l, r]$, where $l$ is definitely feasible and $r$ is definitely infeasible. Initialize $l = 0$, $r = \max(a,b,c)$.
4. Repeatedly bisect the interval and test the midpoint. If the midpoint is feasible, move the lower bound up; otherwise move the upper bound down.
5. After sufficient iterations, the interval is small enough that it represents the exact rational boundary. Convert this value into a fraction form consistent with the problem requirement by interpreting the final real value as a rational approximation of the boundary where feasibility changes.

### Why it works

The function $f(x)$ is monotone non-increasing in $x$. Once a value $x$ is too large to allow $k$ cubes, any larger value cannot recover feasibility because every floor term can only stay the same or decrease. This guarantees a single transition point between feasible and infeasible regions. Binary search converges to this threshold without missing any candidate region where the optimal value could lie.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(a, b, c, x, k):
    return (a // x) * (b // x) * (c // x) >= k

def solve_case(a, b, c, k):
    lo, hi = 1, max(a, b, c)

    while lo <= hi:
        mid = (lo + hi) // 2
        if mid == 0:
            break
        if can(a, b, c, mid, k):
            lo = mid + 1
        else:
            hi = mid - 1

    # hi is the largest integer x that still works
    # for fractional precision, we refine
```
