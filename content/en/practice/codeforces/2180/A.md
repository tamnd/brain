---
title: "CF 2180A - Carnival Wheel"
description: "We are given a circular prize wheel with l numbered sections from 0 to l-1. The wheel pointer starts at a section a. Each spin moves the pointer forward by exactly b positions modulo l."
date: "2026-06-07T22:06:16+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2180
codeforces_index: "A"
codeforces_contest_name: "Codeforces Global Round 31 (Div. 1 + Div. 2)"
rating: 800
weight: 2180
solve_time_s: 94
verified: true
draft: false
---

[CF 2180A - Carnival Wheel](https://codeforces.com/problemset/problem/2180/A)

**Rating:** 800  
**Tags:** brute force, number theory  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a circular prize wheel with `l` numbered sections from `0` to `l-1`. The wheel pointer starts at a section `a`. Each spin moves the pointer forward by exactly `b` positions modulo `l`. The objective is to determine the maximum section number we can reach by spinning the wheel any number of times, including zero spins.

The constraints are moderate: `l` and `b` can each be up to 5000, and there can be up to 500 test cases. This means that any approach that simulates every spin up to `l` steps per test case is feasible, because 5000 steps multiplied by 500 test cases is around 2.5 million operations, which is acceptable in a 1-second time limit. A brute-force method that repeats spins until positions repeat would work, but it is worth investigating whether a simpler formula exists to avoid unnecessary iteration.

Non-obvious edge cases arise when `b` is larger than `l`, when `b` and `l` are not coprime, or when `b` divides `l` exactly. For example, with `l=2`, `a=0`, and `b=6`, the pointer never leaves section `0` because `(0 + k*6) mod 2` is always `0`. A careless approach that assumes `b` always generates new positions might incorrectly suggest a higher maximum. Another edge case is `b=1`, where all positions will eventually be visited, so the maximum is always `l-1`.

## Approaches

The brute-force approach is straightforward. Starting from `a`, we keep adding `b` modulo `l` and track the maximum value reached. This is correct because repeated addition modulo `l` cycles through a subset of sections that is determined by the greatest common divisor of `b` and `l`. In the worst case, the pointer can hit all `l` positions, so the maximum number of iterations is `l`. Across 500 test cases, this results in `500 * 5000 = 2.5 * 10^6` operations, which is within acceptable limits.

The key insight for an optimal solution is to realize that the positions the pointer can reach form an arithmetic progression modulo `l`. Specifically, the sequence of reachable sections is `a, (a+b) mod l, (a+2b) mod l, ...`. The cycle will close after `l / gcd(b, l)` spins because after that many spins, `(a + k*b) mod l` returns to `a`. The maximum reachable section can be computed directly without iteration using the formula `l - gcd(l, b) + ((a - 1) % gcd(l, b))` or simpler logic: the last section in the arithmetic progression before the cycle repeats.

This observation reduces the problem to computing the greatest common divisor (GCD) of `l` and `b` and then determining the maximum in the reachable subset. This avoids simulating every spin while guaranteeing correctness.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(l) per test case | O(1) | Acceptable for given limits |
| Optimal | O(1) per test case | O(1) | Fully accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read `l`, `a`, and `b`.
2. Compute `g = gcd(l, b)`. This tells us the size of the step between consecutive reachable positions modulo `l`.
3. Determine the last reachable position in the cycle. The maximum position is `l - g + a % g`. This works because positions are spaced `g` apart, starting from `a % g`, and the largest value below `l` in this arithmetic progression is `l - g + (a % g)`.
4. Print this maximum value for each test case.

The reason this works is that the pointer can only reach sections congruent to `a modulo g`. The largest section in that congruence class below `l` is `l - g + (a % g)`. Every reachable position is included in the arithmetic progression, so we do not miss any candidate for the maximum.

## Python Solution

```python
import sys
input = sys.stdin.readline
from math import gcd

t = int(input())
for _ in range(t):
    l, a, b = map(int, input().split())
    g = gcd(l, b)
    max_prize = l - g + a % g
    print(max_prize)
```

The solution begins by reading the number of test cases. For each test case, it computes the GCD of `l` and `b`, which defines the step size of the positions modulo `l`. Then it computes the maximum reachable section in the cycle using the formula `l - g + (a % g)`. This formula carefully handles the remainder to account for the starting position `a` and ensures that the value is strictly less than `l`. The result is printed immediately.

## Worked Examples

Sample Input: `l=5, a=3, b=2`

| k | Position (a + k*b) % l | Notes |
| --- | --- | --- |
| 0 | 3 | start |
| 1 | 0 | 3+2=5 % 5=0 |
| 2 | 2 | 0+2=2 %5=2 |
| 3 | 4 | 2+2=4 %5=4 |
| 4 | 1 | 4+2=6 %5=1 |
| 5 | 3 | cycle repeats |

The reachable positions are 0,1,2,3,4. Maximum is 4. GCD of 5 and 2 is 1, so `max_prize = 5-1 + 3 %1 = 4`.

Sample Input: `l=2, a=0, b=6`

| k | Position (a + k*b) % l |
| --- | --- |
| 0 | 0 |
| 1 | 0 |
| 2 | 0 |

GCD(2,6)=2. Maximum reachable: `2 - 2 + 0%2 = 0`.

These traces confirm that the formula handles cycles and fixed points correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case takes O(1) due to GCD computation and arithmetic. |
| Space | O(1) | Only a few integer variables are needed per test case. |

With `t=500` and `l,b<=5000`, this solution executes well under 1 second and uses minimal memory.

## Test Cases

```python
import sys, io
from math import gcd

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    t = int(input())
    for _ in range(t):
        l, a, b = map(int, input().split())
        g = gcd(l, b)
        output.write(str(l - g + a % g) + "\n")
    return output.getvalue().strip()

# Provided samples
assert run("4\n5 3 2\n2 0 6\n8 2 4\n100 0 1\n") == "4\n0\n6\n99", "samples"

# Custom cases
assert run("1\n1 0 1\n") == "0", "minimum size input"
assert run("1\n5000 4999 5000\n") == "4999", "l and b max, starting at last section"
assert run("1\n7 0 7\n") == "0", "b divisible by l"
assert run("1\n10 3 4\n") == "9", "small l, b and a in middle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 1 | 0 | minimum-size input |
| 5000 4999 5000 | 4999 | maximum-size inputs |
| 7 0 7 | 0 | b divisible by l, pointer cannot move |
| 10 3 4 | 9 | general small case, correct max calculation |

## Edge Cases

For `l=2, a=0, b=6`, the pointer remains at 0. The formula computes `gcd(2,6)=2`, and `max_prize = 2 - 2 + 0%2 = 0`, which matches the observed behavior. For `l=5, a=3, b=2`, the pointer cycles through all positions. GCD is 1, so `max_prize = 5-1 + 3%1 = 4`, correctly capturing the highest section. The formula correctly handles both stationary positions and full cycles.
