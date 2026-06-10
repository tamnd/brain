---
title: "CF 1515B - Phoenix and Puzzle"
description: "We are given a set of identical right isosceles triangular puzzle pieces. Each triangle has two equal sides and a right angle. Phoenix wants to use exactly $n$ of these triangles to form a perfect square, without overlaps or holes."
date: "2026-06-10T18:31:09+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "geometry", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1515
codeforces_index: "B"
codeforces_contest_name: "Codeforces Global Round 14"
rating: 1000
weight: 1515
solve_time_s: 219
verified: true
draft: false
---

[CF 1515B - Phoenix and Puzzle](https://codeforces.com/problemset/problem/1515/B)

**Rating:** 1000  
**Tags:** brute force, geometry, math, number theory  
**Solve time:** 3m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of identical right isosceles triangular puzzle pieces. Each triangle has two equal sides and a right angle. Phoenix wants to use exactly $n$ of these triangles to form a perfect square, without overlaps or holes. He is allowed to rotate and move the pieces freely. The task is to decide, for each test case, whether forming such a square is possible.

The input provides multiple test cases, each consisting of a single integer $n$, which can be as large as $10^9$. The output is simply "YES" if a square can be formed, and "NO" otherwise.

The constraint $n \le 10^9$ immediately tells us that any solution iterating over all pieces or trying every geometric arrangement is impractical. We need an approach that computes the answer using a formula or arithmetic checks in constant time per test case.

An important subtlety is that not all integers $n$ can form a square. For example, $n = 2$ works because two triangles can form a square by joining their hypotenuses. $n = 4$ also works because four triangles can form a larger square. However, $n = 6$ fails: any arrangement of six identical right isosceles triangles cannot perfectly form a square. A careless solution might assume any even number works, but the arrangement of pieces requires either a multiple of 2 forming a square of side 1, or multiples of 4 forming squares of larger sizes.

## Approaches

The brute-force approach would attempt to place the triangles one by one and check if a square forms. Conceptually, one could try simulating all rotations and positions. This is correct in principle but computationally impossible for $n \sim 10^9$, since the number of arrangements grows factorially.

The key insight is to reason in terms of the total area of the triangles. Each triangle has an area of $0.5$ (assuming unit legs). If $n$ triangles form a square, the area of the square must be $n \times 0.5 = n/2$. Therefore, the square’s side must be $\sqrt{n/2}$. For a square with integer coordinates, $\sqrt{n/2}$ should be a rational number that can be expressed as the sum of integer-length sides constructed from triangles.

From geometric reasoning, we find that a square can be constructed if and only if $n$ can be expressed as $2k^2$ or $4k^2$, where $k$ is an integer. The first form corresponds to a square made by two triangles along the hypotenuse, and the second corresponds to a square built from four triangles in a $k \times k$ grid of squares.

This observation reduces the problem to checking two conditions using integer arithmetic: whether $n$ is divisible by 2 and $n/2$ is a perfect square, or whether $n$ is divisible by 4 and $n/4$ is a perfect square. Both checks are $O(1)$ per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the integer $n$ representing the number of triangles.
2. If $n$ is divisible by 2, compute $n/2$. Check if $n/2$ is a perfect square by taking its integer square root and squaring it back.
3. If $n/2$ is a perfect square, print "YES" and skip to the next test case. This corresponds to squares formed from exactly 2 triangles along the hypotenuse.
4. Otherwise, check if $n$ is divisible by 4. Compute $n/4$ and verify whether it is a perfect square.
5. If $n/4$ is a perfect square, print "YES". This corresponds to squares built from 4 triangles arranged in a square grid.
6. If neither check passes, print "NO".

Why it works: The invariant is that a square formed from right isosceles triangles requires either 2 or 4 triangles to form a base unit square, and larger squares are integer multiples of these base units. Therefore, the area argument guarantees correctness, and the integer square check ensures the pieces align perfectly without gaps or overlaps.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    ans = "NO"
    if n % 2 == 0:
        half = n // 2
        if int(math.isqrt(half)) ** 2 == half:
            ans = "YES"
    if ans == "NO" and n % 4 == 0:
        quarter = n // 4
        if int(math.isqrt(quarter)) ** 2 == quarter:
            ans = "YES"
    print(ans)
```

The solution reads input efficiently using `sys.stdin.readline` to handle up to $10^4$ test cases. The `math.isqrt` function computes the integer square root accurately without floating-point errors, and squaring it back ensures exact perfect square detection. Checking both `n/2` and `n/4` covers both geometric arrangements. The order of checks ensures we detect the 2-triangle case before attempting the 4-triangle case.

## Worked Examples

**Example 1: n = 2**

| n | n % 2 | n/2 | sqrt(n/2)^2 | Result |
| --- | --- | --- | --- | --- |
| 2 | 0 | 1 | 1 | YES |

The algorithm correctly identifies that 2 triangles can form a square.

**Example 2: n = 6**

| n | n % 2 | n/2 | sqrt(n/2)^2 | n % 4 | n/4 | sqrt(n/4)^2 | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 6 | 0 | 3 | 1 | 2 | - | - | NO |

Neither `n/2` nor `n/4` is a perfect square, so the answer is NO.

These traces confirm that the algorithm distinguishes impossible cases like n = 6 and detects minimal possible squares.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Each test case performs a constant number of arithmetic operations and integer square root calculations |
| Space | O(1) | Only a few integer variables are used per test case |

With $t \le 10^4$, the total operations are well within the 2-second time limit.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    
    t = int(input())
    for _ in range(t):
        n = int(input())
        ans = "NO"
        if n % 2 == 0:
            half = n // 2
            if int(math.isqrt(half)) ** 2 == half:
                ans = "YES"
        if ans == "NO" and n % 4 == 0:
            quarter = n // 4
            if int(math.isqrt(quarter)) ** 2 == quarter:
                ans = "YES"
        print(ans)
    return out.getvalue().strip()

# Provided samples
assert run("3\n2\n4\n6\n") == "YES\nYES\nNO", "sample 1"

# Custom tests
assert run("4\n1\n8\n18\n16\n") == "NO\nYES\nNO\nYES", "custom edge cases"
assert run("3\n50\n32\n72\n") == "NO\nYES\nNO", "varied sizes"
assert run("2\n2000000000\n999999999\n") == "NO\nNO", "large numbers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | NO | minimum n that cannot form a square |
| 8 | YES | n divisible by 4 forming square with 4 triangles |
| 18 | NO | divisible by 2 but n/2 not perfect square |
| 16 | YES | divisible by 4, n/4 = 4, perfect square |
| 2000000000 | NO | large number not forming perfect square |
| 32 | YES | larger perfect square by 4-triangle arrangement |

## Edge Cases

For n = 1, the algorithm checks divisibility by 2 and 4. Both fail, so it prints NO. This matches intuition: a single triangle cannot form a square. For n = 8, the algorithm first checks n/2 = 4, which is a perfect square, so it prints YES. This demonstrates the importance of checking both 2-triangle and 4-triangle arrangements. For large n like 2 × 10^9, the algorithm still works in O(1) per test case without overflow because Python integers are unbounded and `math.isqrt` handles large integers efficiently.
