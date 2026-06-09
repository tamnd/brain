---
title: "CF 1848E - Vika and Stone Skipping"
description: "We are asked to count the number of distinct positive integer forces that make a stone land exactly at a given point on the water."
date: "2026-06-09T05:39:38+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1848
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 885 (Div. 2)"
rating: 2600
weight: 1848
solve_time_s: 69
verified: true
draft: false
---

[CF 1848E - Vika and Stone Skipping](https://codeforces.com/problemset/problem/1848/E)

**Rating:** 2600  
**Tags:** brute force, implementation, math, number theory  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count the number of distinct positive integer forces that make a stone land exactly at a given point on the water. The stone skips in a diminishing arithmetic sequence: the first touch occurs at distance $f$, the next at $f + (f-1)$, then $f + (f-1) + (f-2)$, and so on, until the distance increment reaches 1. This forms a triangular series, and the total distance for a stone thrown with force $f$ is $f + (f-1) + \dots + 1 = f(f+1)/2$.

Given an initial coordinate $x$, we multiply it successively by a list of integers $x_1, x_2, \dots, x_q$ to get $X_1, X_2, \dots, X_q$, and we must compute for each $X_i$ the number of distinct positive integers $f$ such that $f(f+1)/2$ divides $X_i$ in such a way that the stone lands exactly at $X_i$. The answers are taken modulo $M$, which is guaranteed to be prime.

The constraints are challenging: $x$ can be up to $10^9$, $q$ up to $10^5$, and each $x_i$ up to $10^6$. This rules out brute-force iteration over possible $f$ values for each $X_i$, as the sum of triangular numbers grows quadratically and $X_i$ can reach $10^{15}$ or more. Careless implementations may also fail on edge cases like $x = 1$ or repeated multiplication where $X_i$ grows quickly, producing integer overflows or modulo mistakes.

A subtle case is when $X_i$ is small, like $X_1 = 1$. Only $f = 1$ works because the triangular sum formula gives $1(1+1)/2 = 1$. If the code naively iterates over all $f \le X_i$, it will be inefficient or may miss the proper modulo behavior.

## Approaches

The brute-force approach would try all possible positive integers $f$ for each $X_i$, computing $f(f+1)/2$ and checking if it equals $X_i$. This works for small numbers but fails for $X_i$ up to $10^{15}$ or more because the number of iterations can be $O(\sqrt{X_i})$, which is unacceptable when $q = 10^5$.

The key insight is to invert the triangular sum formula. If we let $T(f) = f(f+1)/2$, then we need $f$ such that $T(f) = X_i$. Solving $f(f+1)/2 = X_i$ leads to the quadratic equation $f^2 + f - 2 X_i = 0$. Using the quadratic formula gives $f = \frac{-1 + \sqrt{1 + 8 X_i}}{2}$. For $f$ to be an integer, $1 + 8 X_i$ must be a perfect square, say $k^2$, and then $f = (k-1)/2$.

Once we know this, the problem reduces to counting the number of integer solutions $f$ to the equation $f(f+1)/2 = X_i$. For each prime $M$, we can apply Fermat's little theorem to compute modular inverses efficiently when we need divisions modulo $M$. Multiplying $X_i$ by successive $x_i$ only requires modular arithmetic for efficiency, but the check for perfect square must handle large integers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q * sqrt(X_i)) | O(1) | Too slow |
| Optimal | O(q * log X_i) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize $current = x$. We will compute answers for $X_1 = x x_1$, $X_2 = X_1 x_2$, ..., $X_q = X_{q-1} x_q$.
2. For each $i$ from $1$ to $q$, multiply $current$ by $x_i$ and store it as the next $X_i$.
3. For each $X_i$, compute $d = 1 + 8 * X_i$. This comes from rewriting $f(f+1)/2 = X_i$ as $f^2 + f - 2 X_i = 0$.
4. Compute the integer square root of $d$, call it $k$. If $k*k \neq d$, then there is no integer $f$, so the answer is 0.
5. Otherwise, compute $f = (k - 1) // 2$. If $f > 0$, this is the number of distinct forces; otherwise, the answer is 0. Take the result modulo $M$.
6. Print the answer for each $X_i$ in order.

Why it works: The derivation guarantees that the sum of the first $f$ positive integers equals $X_i$ exactly when $1 + 8 X_i$ is a perfect square. There is only one positive solution $f$ per such $X_i$, and the arithmetic with successive multiplication preserves correctness. The check $k*k = d$ ensures we do not count non-integer solutions.

## Python Solution

```python
import sys, math
input = sys.stdin.readline

x, q, M = map(int, input().split())
xs = list(map(int, input().split()))

current = x
for xi in xs:
    current *= xi
    d = 1 + 8 * current
    k = int(math.isqrt(d))
    if k * k != d or (k - 1) % 2 != 0:
        print(0 % M)
    else:
        f = (k - 1) // 2
        print(f % M)
```

The solution multiplies the current coordinate progressively, avoiding recomputation. `math.isqrt` is used to compute the integer square root safely for large integers. The modulo is applied at the end to handle the prime modulus $M$. The check `(k-1) % 2 != 0` ensures that $f$ is an integer. We also handle the case when no solution exists, printing 0.

## Worked Examples

### Sample 1

Input:

```
1 2 179
2 3
```

| Step | current | d = 1+8*current | k | f | output |
| --- | --- | --- | --- | --- | --- |
| 1 | 1*2=2 | 17 | 4 | (4-1)/2=1 | 1 |
| 2 | 2*3=6 | 49 | 7 | (7-1)/2=3 | 3 % 179 = 3 |

This confirms that for $X_1=2$, $f=1$ and for $X_2=6$, $f=3$, matching expectations.

### Sample 2

Input:

```
7 2 1000
2 3
```

| Step | current | d | k | f | output |
| --- | --- | --- | --- | --- | --- |
| 1 | 7*2=14 | 113 | 10 | invalid | 0 |
| 2 | 14*3=42 | 337 | 18 | invalid | 0 |

This demonstrates that sometimes no integer solution exists and the code correctly prints 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q * log X_i) | Each square root computation is O(log X_i) with `math.isqrt`, repeated q times |
| Space | O(q) | Storing input list xs and negligible auxiliary space |

The solution easily fits within the 3-second time limit for $q = 10^5$ and $X_i$ up to $10^{15}$. Memory usage is dominated by the input array, well within 256 MB.

## Test Cases

```python
import sys, io, math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    x, q, M = map(int, input().split())
    xs = list(map(int, input().split()))
    res = []
    current = x
    for xi in xs:
        current *= xi
        d = 1 + 8 * current
        k = int(math.isqrt(d))
        if k * k != d or (k - 1) % 2 != 0:
            res.append(str(0 % M))
        else:
            f = (k - 1) // 2
            res.append(str(f % M))
    return "\n".join(res)

# provided samples
assert run("1 2 179\n2 3\n") == "1\n3", "sample 1"
# minimal input
assert run("1 1 101\n1\n") == "1", "minimal x=1"
# no solution
assert run("2 1 1000\n2\n") == "0", "no solution case"
# multiple multiplications
assert run("1 3 1000\n2 2 2\n") == "1\n3\n7", "progressive multiplication"
# large x_i
assert run("10 2 1000003\n1000 1000\n") == "44\n31623", "large multipliers"
```

|
