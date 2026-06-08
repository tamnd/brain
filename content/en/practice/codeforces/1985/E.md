---
title: "CF 1985E - Secret Box"
description: "We are asked to place a small box with integer side lengths inside a larger box in 3D space. The small box must have a specific volume $k$ and must align with the axes, with all corners at integer coordinates."
date: "2026-06-08T16:21:13+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "combinatorics", "math"]
categories: ["algorithms"]
codeforces_contest: 1985
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 952 (Div. 4)"
rating: 1200
weight: 1985
solve_time_s: 151
verified: true
draft: false
---

[CF 1985E - Secret Box](https://codeforces.com/problemset/problem/1985/E)

**Rating:** 1200  
**Tags:** brute force, combinatorics, math  
**Solve time:** 2m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to place a small box with integer side lengths inside a larger box in 3D space. The small box must have a specific volume $k$ and must align with the axes, with all corners at integer coordinates. The challenge is to pick the side lengths of this small box in such a way that the number of valid placements inside the larger box is maximized. A valid placement occurs when the box fits entirely inside the larger box without exceeding its boundaries.

The input consists of the dimensions $x, y, z$ of the large box and the desired volume $k$ of the secret box. For each test case, we must output the maximum number of distinct integer placements for any choice of integer dimensions of the secret box. If no set of integer dimensions produces volume $k$ that can fit inside the large box, the answer is zero.

The constraints allow each side of the large box to be up to 2000 and $k$ up to $x \cdot y \cdot z$. There are up to 2000 test cases, but the sum of all $x$, $y$, and $z$ across all tests does not exceed 2000. This implies that, in total, our nested loops over side lengths or factors of $k$ will not exceed roughly $2000^3$ across all test cases. $k$ can be very large, so care must be taken to avoid 32-bit overflow.

A naive approach could miss cases where one or more side lengths are larger than the corresponding dimension of the box, producing zero placements. For example, a large box of size $2 \times 2 \times 2$ with $k = 7$ cannot fit any integer-dimension box because no integer triplet multiplies to 7 within the limits.

## Approaches

The brute-force approach is to enumerate all possible integer triplets $(a, b, c)$ such that $a \cdot b \cdot c = k$. For each triplet, compute how many placements fit inside the large box using $(x-a+1) \cdot (y-b+1) \cdot (z-c+1)$, counting only if all three factors are positive. This works because the number of valid placements along each axis is simply the number of positions the box can start without exceeding the boundary. The difficulty of this brute-force is factoring $k$ and generating all triples. A naive cubic loop over $a, b, c$ up to $\sqrt[3]{k}$ is too slow when $k$ is very large, up to $2000^3$ in theory.

The key insight is that we only need to consider divisors of $k$. First, generate all divisors of $k$ up to $\sqrt{k}$. For each divisor $a$, consider all divisors $b$ of $k // a$ and set $c = k // (a \cdot b)$. This guarantees $a \cdot b \cdot c = k$. Then check if $a \le x$, $b \le y$, and $c \le z$. If so, compute the placement count $(x-a+1) \cdot (y-b+1) \cdot (z-c+1)$ and track the maximum. This reduces the number of iterations dramatically because the number of divisors grows slowly, roughly $O(k^{1/3})$ for generating triples.

The problem has symmetry: the ordering of $a, b, c$ matters relative to $x, y, z$ because the box cannot be rotated. All six permutations must be considered for each valid triple to capture the correct fit. Without considering all permutations, some optimal arrangements may be missed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k^(1/3) * k^(1/3)) | O(1) | Too slow for large k |
| Divisor-based Triple Search | O(d(k)^2) | O(d(k)) | Accepted, efficient |

Here $d(k)$ is the number of divisors of $k$, which is manageable for $k \le 2000^3$ since we only need integer factorization of moderate-sized $k$.

## Algorithm Walkthrough

1. Read the number of test cases and loop over each case. Extract $x, y, z, k$.
2. Initialize a variable to track the maximum number of placements for this test case.
3. Enumerate all divisors $a$ of $k$. For each divisor $a$, $a$ represents a possible length along the x-axis.
4. For each $a$, enumerate all divisors $b$ of $k // a$. Compute $c = k // (a \cdot b)$ to ensure $a \cdot b \cdot c = k$.
5. Generate all permutations of the triple $(a, b, c)$. For each permutation, check if $a \le x$, $b \le y$, and $c \le z$. If so, compute the number of placements along each axis as $(x-a+1) \cdot (y-b+1) \cdot (z-c+1)$.
6. Track the maximum placement count among all permutations.
7. After all divisors and permutations are checked, output the maximum count or zero if no placement was possible.

Why it works: By factoring $k$ and considering all permutations, we are guaranteed to examine all integer side-length combinations that produce volume $k$. Checking the fit against $x, y, z$ ensures validity. Considering permutations captures all ways the box can align with the axes. The maximum computed placement count is exact because we evaluate every feasible candidate.

## Python Solution

```python
import sys
input = sys.stdin.readline
from itertools import permutations
from math import isqrt

def divisors(n):
    small, large = [], []
    for i in range(1, isqrt(n) + 1):
        if n % i == 0:
            small.append(i)
            if i != n // i:
                large.append(n // i)
    return small + large[::-1]

t = int(input())
for _ in range(t):
    x, y, z, k = map(int, input().split())
    max_places = 0
    divs_a = divisors(k)
    for a in divs_a:
        if a > x:
            continue
        remaining = k // a
        divs_b = divisors(remaining)
        for b in divs_b:
            c = remaining // b
            for (aa, bb, cc) in permutations([a, b, c]):
                if aa <= x and bb <= y and cc <= z:
                    places = (x - aa + 1) * (y - bb + 1) * (z - cc + 1)
                    if places > max_places:
                        max_places = places
    print(max_places)
```

The solution first generates divisors efficiently, then constructs valid triples. Permutations ensure we check all axis alignments. We avoid overflow because Python handles large integers, and we skip divisors exceeding box dimensions early. Multiplying positions uses the formula $(dimension - side + 1)$ along each axis.

## Worked Examples

Sample 1: $x = 3, y = 3, z = 3, k = 8$

| a | b | c | permutation | fits? | placements |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 8 | (1,1,8) | no | - |
| 1 | 2 | 4 | (2,1,4) | no | - |
| 2 | 2 | 2 | (2,2,2) | yes | (3-2+1)_(3-2+1)_(3-2+1)=2_2_2=8 |

The maximum placements is 8, confirming the first sample output.

Sample 2: $x = 3, y = 3, z = 3, k = 18$

| a | b | c | permutation | fits? | placements |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 9 | (2,1,9) | no | - |
| 2 | 3 | 3 | (2,3,3) | yes | (3-2+1)_(3-3+1)_(3-3+1)=2_1_1=2 |

Maximum placements is 2, matching the sample.

These tables illustrate the generation of all triples via divisors and permutations, and correct calculation of placement counts.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(d(k)^2 * 6) | d(k) is number of divisors of k; generating permutations multiplies by 6 |
| Space | O(d(k)) | storing divisors of k and intermediate lists |

The divisor-based approach is efficient for all $k \le 2000^3$ because the sum of all box dimensions is capped. The number of divisors grows slowly, so nested loops over divisors remain within feasible operations for 2000 test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin
```
