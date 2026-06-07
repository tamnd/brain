---
title: "CF 2106C - Cherry Bomb"
description: "We are given two arrays of length $n$, $a$ and $b$. Array $a$ is fully known, and $b$ has some missing elements marked as $-1$. The goal is to fill in the missing elements in $b$ such that the sum $ai + bi$ is constant for all $i$. Each element in $b$ must remain within $[0, k]$."
date: "2026-06-08T04:52:01+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2106
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1020 (Div. 3)"
rating: 1000
weight: 2106
solve_time_s: 72
verified: true
draft: false
---

[CF 2106C - Cherry Bomb](https://codeforces.com/problemset/problem/2106/C)

**Rating:** 1000  
**Tags:** greedy, math, sortings  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two arrays of length $n$, $a$ and $b$. Array $a$ is fully known, and $b$ has some missing elements marked as $-1$. The goal is to fill in the missing elements in $b$ such that the sum $a_i + b_i$ is constant for all $i$. Each element in $b$ must remain within $[0, k]$. We need to count all valid ways to do this.

The constraints imply that $n$ can reach $2 \cdot 10^5$ across all test cases, and each element can be as large as $10^9$. Any solution that iterates over all possible values of missing $b_i$ would be too slow, because a single missing element could have $k+1$ options, which is prohibitive. Therefore, the solution must reason about valid ranges and avoid brute-force enumeration.

Non-obvious edge cases include situations where some $b_i$ are already fixed. If two fixed $b_i$ require different constants $x$, there is no valid completion. For example, $a = [2, 1]$, $b = [1, 0]$ cannot be complementary because $2 + 1 \neq 1 + 0$. Another edge case occurs when the required $b_i$ value to satisfy the complement rule exceeds $k$ or is negative. These scenarios must be filtered carefully.

## Approaches

The brute-force approach would generate all possible replacements for missing elements of $b$ and check if the resulting array is complementary. This is correct but too slow. Suppose $m$ elements are missing, each has up to $k+1$ possibilities. The total number of combinations is $(k+1)^m$, which is infeasible when $k \approx 10^9$ even for small $m$.

The key observation is that a complementary pair requires $x = a_i + b_i$ to be the same for all $i$. For positions where $b_i$ is known, this fixes $x = a_i + b_i$. If these fixed positions disagree, no solution exists. For missing $b_i$, the value is determined as $b_i = x - a_i$. This immediately gives a valid check: $0 \le b_i \le k$. Therefore, we reduce the problem to finding the allowed range of $x$ from known $b_i$ and counting how many choices satisfy the constraints on the missing ones.

Specifically, for each missing element, the valid $x$ must satisfy $a_i \le x \le a_i + k$. Combining all constraints across the array gives a single contiguous interval of valid $x$. The length of this interval gives the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((k+1)^m) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize `x_min` as 0 and `x_max` as $k$ plus the largest $a_i$ in the array. These will track the valid range for the constant sum $x$.
2. Iterate over each index $i$ of the arrays. If $b_i$ is not missing, compute $x_i = a_i + b_i$. Update `x_min` and `x_max` to be equal to `x_i` because all fixed $b_i$ enforce the same sum. If we encounter a previously fixed `x` that is different from `x_i`, immediately return 0 because the array cannot be complementary.
3. If $b_i$ is missing, derive the valid interval for $x$ as `[a_i, a_i + k]` since $b_i = x - a_i$ must satisfy $0 \le b_i \le k$. Intersect this interval with the current `[x_min, x_max]` to tighten the possible values of $x$.
4. After processing all elements, compute the number of integer values in the final valid interval `[x_min, x_max]`. This is `max(0, x_max - x_min + 1)` and gives the total number of ways to complete $b$.
5. Output the result.

The invariant is that at every step, `[x_min, x_max]` represents all values of $x$ that satisfy both the fixed elements and the missing elements seen so far. Intersection ensures no invalid $x$ slips through, so any $x$ counted at the end will generate a valid complementary array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def cherry_bomb():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        x_min = 0
        x_max = 2 * k  # upper bound for x
        
        fixed_x = None
        possible = True
        
        for ai, bi in zip(a, b):
            if bi != -1:
                current = ai + bi
                if fixed_x is None:
                    fixed_x = current
                    x_min = x_max = current
                elif current != fixed_x:
                    possible = False
                    break
            else:
                # missing element: b_i = x - a_i in [0, k] => x in [a_i, a_i + k]
                x_min = max(x_min, ai)
                x_max = min(x_max, ai + k)
        
        if not possible or x_min > x_max:
            print(0)
        else:
            print(x_max - x_min + 1)

cherry_bomb()
```

The code separates the treatment of fixed and missing elements. Fixed elements define a strict `x`, while missing elements constrain it within a range. Using `max` and `min` to intersect intervals ensures we respect all constraints. The final count is the size of the intersection.

## Worked Examples

**Example 1**

Input arrays: `a = [1, 3, 2]`, `b = [-1, -1, 1]`

| i | a[i] | b[i] | x_min | x_max | Comment |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | -1 | 1 | 11 | missing: x in [1, 1+10] |
| 1 | 3 | -1 | 3 | 11 | missing: x in [3, 3+10], intersect with previous |
| 2 | 2 | 1 | 3 | 3 | fixed: x = 2+1 = 3, intersect => x_min = x_max = 3 |

Number of ways: `x_max - x_min + 1 = 1`

**Example 2**

Input arrays: `a = [0, 1, 0, 0, 1]`, `b = [-1, 0, 1, 0, -1]`

| i | a[i] | b[i] | x_min | x_max | Comment |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | -1 | 0 | 1 | missing: x in [0, 0+1] |
| 1 | 1 | 0 | 1 | 1 | fixed: x = 1+0=1 |
| 2 | 0 | 1 | 1 | 1 | fixed: x=0+1=1 |
| 3 | 0 | 0 | 1 | 1 | fixed: x=0+0=0 conflict |

Conflict detected, answer 0.

These traces confirm that the algorithm correctly handles both the fixed element constraints and the intervals for missing elements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | One linear pass over arrays `a` and `b` to compute intervals and check consistency |
| Space | O(n) | Input arrays are stored; no additional dynamic structures required |

Given the sum of $n$ over all test cases is at most $2 \cdot 10^5$, the solution runs well within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    cherry_bomb()
    return out.getvalue().strip()

# Provided samples
assert run("7\n3 10\n1 3 2\n-1 -1 1\n5 1\n0 1 0 0 1\n-1 0 1 0 -1\n5 1\n0 1 0 0 1\n-1 1 -1 1 -1\n5 10\n1 3 2 5 4\n-1 -1 -1 -1 -1\n5 4\n1 3 2 1 3\n1 -1 -1 1 -1\n5 4\n1 3 2 1 3\n2 -1 -1 2 0\n5 5\n5 0
```
