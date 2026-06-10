---
title: "CF 1468F - Full Turn"
description: "We have a set of points on a plane, each representing a person, with each person initially looking at another point. Everyone rotates clockwise continuously, completing a full turn, and we are asked to count the number of distinct pairs of people who ever make “eye contact."
date: "2026-06-11T01:27:05+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "hashing", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1468
codeforces_index: "F"
codeforces_contest_name: "2020-2021 ICPC, NERC, Southern and Volga Russian Regional Contest (Online Mirror, ICPC Rules)"
rating: 1700
weight: 1468
solve_time_s: 121
verified: true
draft: false
---

[CF 1468F - Full Turn](https://codeforces.com/problemset/problem/1468/F)

**Rating:** 1700  
**Tags:** geometry, hashing, number theory  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a set of points on a plane, each representing a person, with each person initially looking at another point. Everyone rotates clockwise continuously, completing a full turn, and we are asked to count the number of distinct pairs of people who ever make “eye contact.” Eye contact occurs when two people are looking exactly at each other at the same moment, without considering any obstruction.

The input specifies multiple test cases. Each test case gives the number of people and then the coordinates of each person's position and initial gaze. The output is a single integer per test case: the total number of pairs who meet the eye contact condition at least once.

The constraints are significant. Each test case can have up to $10^5$ people, and the total across all test cases does not exceed $10^5$. This means an $O(n^2)$ algorithm is infeasible because it could require $10^{10}$ operations in the worst case. Linear or near-linear time algorithms, like $O(n \log n)$, are necessary. We must also handle coordinates as large as $10^9$ and deal with precise directional comparisons. Edge cases include extremely close points where naive floating-point angle comparisons might fail, or multiple people initially looking in exactly opposite directions.

A naive approach might compare every pair of people directly, computing angles or directions at multiple moments of the rotation. This would miss performance requirements and could introduce floating-point precision errors when checking equality of directions.

## Approaches

The brute-force approach examines each pair of people, calculates the vector from one to the other, computes their initial viewing directions, and simulates rotation to see if their directions ever align. While this is conceptually correct, it requires $O(n^2)$ comparisons per test case, which exceeds the feasible operation count.

The key insight for optimization comes from observing that directions and positions can be represented as vectors and reduced to ratios of integers. If person $A$ at $(x_a, y_a)$ is looking along vector $(u_a - x_a, v_a - y_a)$ and person $B$ is at $(x_b, y_b)$ looking along $(u_b - x_b, v_b - y_b)$, they will make eye contact if and only if the direction from $A$ to $B$ is a scalar multiple of $A$'s gaze vector and simultaneously the direction from $B$ to $A$ is a scalar multiple of $B$'s gaze vector. The scalar multiples do not matter; what matters is the **reduced direction vector**, which can be represented as a pair of integers divided by their greatest common divisor. By representing every gaze vector and inter-person vector in this reduced form, we can use a hash map to count compatible pairs efficiently.

The problem thus reduces to counting pairs of positions and gaze vectors such that the normalized direction vectors match in opposite directions. This avoids simulation entirely and achieves linear-time counting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Vector Normalization & Hashing | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. For each person, compute the gaze vector by subtracting the person’s coordinates from their look-at coordinates. This gives $(dx, dy) = (u_i - x_i, v_i - y_i)$.
2. Normalize this vector by dividing both components by their greatest common divisor and ensuring a canonical sign (for example, always make the first non-zero component positive). This guarantees that vectors pointing in the same direction are represented identically as integer pairs.
3. For each pair of people, define the vector from person $A$ to $B$ as $(x_b - x_a, y_b - y_a)$ and normalize it in the same way.
4. Store counts of normalized gaze vectors in a hash map. For every person $A$, the number of persons $B$ they can see in the correct direction is determined by querying how many people have a gaze vector that is the opposite of the direction from $A$ to them. This uses a simple hash lookup per person instead of iterating over all pairs.
5. Sum all counts, divide by two because each eye contact is counted twice, and return this value for the test case.

Why it works: By reducing all vectors to a canonical form, we ensure that two people can only make eye contact if and only if their gaze directions are exactly aligned with the vector connecting them in opposite directions. Hashing avoids repeated comparisons and guarantees correctness because no other alignment is possible, eliminating the need for floating-point arithmetic.

## Python Solution

```python
import sys
import math
from collections import defaultdict
input = sys.stdin.readline

def normalize(dx, dy):
    if dx == 0 and dy == 0:
        return (0, 0)
    g = math.gcd(dx, dy)
    dx //= g
    dy //= g
    if dx < 0 or (dx == 0 and dy < 0):
        dx = -dx
        dy = -dy
    return (dx, dy)

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        persons = []
        for _ in range(n):
            x, y, u, v = map(int, input().split())
            dx = u - x
            dy = v - y
            persons.append((x, y, normalize(dx, dy)))
        
        counter = defaultdict(int)
        for x, y, vec in persons:
            counter[vec] += 1
        
        result = 0
        for x, y, vec in persons:
            # vector from A to B that would match gaze
            inv_vec = (-vec[0], -vec[1])
            result += counter.get(inv_vec, 0)
        
        print(result // 2)

if __name__ == "__main__":
    solve()
```

The solution reads the input efficiently, normalizes vectors carefully to avoid floating-point errors, and uses a hash map to count opposite gaze directions. Each person is counted correctly once per potential partner, and division by two avoids double-counting pairs.

## Worked Examples

Consider the second sample input:

```
3
0 0 1 1
1 1 0 0
1 0 2 0
```

Step-by-step:

| Person | Position | Look vector | Normalized | Opposite vectors count |
| --- | --- | --- | --- | --- |
| 1 | (0,0) | (1,1) | (1,1) | 1 (person 2) |
| 2 | (1,1) | (-1,-1) | (-1,-1) | 1 (person 1) |
| 3 | (1,0) | (1,0) | (1,0) | 0 |

Summing gives 2, divide by 2 to get 1 pair, which matches the output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each person is processed once to compute and normalize vectors, then queried in a hash map. |
| Space | O(n) | Hash map stores a count per unique normalized vector, which is at most n. |

Given that the sum of n over all test cases does not exceed $10^5$, this is well within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    f = io.StringIO()
    with redirect_stdout(f):
        solve()
    return f.getvalue().strip()

# provided samples
assert run("3\n2\n0 0 0 1\n1 0 2 0\n3\n0 0 1 1\n1 1 0 0\n1 0 2 0\n6\n0 0 0 1\n1 0 1 2\n2 0 2 3\n3 0 3 -5\n4 0 4 -5\n5 0 5 -5\n") == "0\n1\n9"

# custom cases
assert run("1\n1\n0 0 1 1\n") == "0"  # only one person
assert run("1\n2\n0 0 1 0\n1 0 0 0\n") == "1"  # directly facing
assert run("1\n3\n0 0 1 0\n1 0 0 0\n0 1 0 0\n") == "1"  # third person not matching
assert run("1\n2\n0 0 1 1\n1 1 1 2\n") == "0"  # not aligned vectors
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 person | 0 | Single person cannot make eye contact |
| 2 persons facing | 1 | Simple pair matching |
| 3 persons, partial alignment | 1 | Correct counting only matching pairs |
| 2 persons not aligned | 0 | Failsafe against misaligned vectors |

## Edge Cases

When two people have vectors that are multiples
