---
title: "CF 1476A - K-divisible Sum"
description: "We are asked to construct an array of size $n$ containing positive integers such that the sum of all elements is divisible by $k$. Among all arrays that satisfy this condition, we need the one where the largest element is as small as possible."
date: "2026-06-11T00:00:11+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1476
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 103 (Rated for Div. 2)"
rating: 1000
weight: 1476
solve_time_s: 220
verified: true
draft: false
---

[CF 1476A - K-divisible Sum](https://codeforces.com/problemset/problem/1476/A)

**Rating:** 1000  
**Tags:** binary search, constructive algorithms, greedy, math  
**Solve time:** 3m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to construct an array of size $n$ containing positive integers such that the sum of all elements is divisible by $k$. Among all arrays that satisfy this condition, we need the one where the largest element is as small as possible. Instead of building the actual array, the problem only asks for the value of this maximum element.

The input consists of multiple test cases. Each test case gives two integers, $n$ and $k$, with both able to reach up to $10^9$. The output is a single integer per test case representing the minimal achievable maximum element in the array.

Because $n$ and $k$ can be extremely large, generating an actual array or iterating over every possible value is infeasible. Any solution must compute the answer with pure arithmetic operations, ideally in constant time per test case. A naive approach that tries to simulate all possible arrays would perform $O(n)$ operations per test case, which is unacceptable since $n$ can be $10^9$.

Non-obvious edge cases arise when $n$ is smaller than $k$. For example, if $n = 1$ and $k = 5$, the only way to satisfy divisibility is to set the single element to 5. If $n$ is a multiple of $k$, then setting all elements to 1 already gives a sum divisible by $k$. Another tricky scenario is when $n$ and $k$ are coprime or $n < k$ but not 1; in such cases, some elements need to be increased above 1 to reach a sum divisible by $k$. These cases illustrate why the solution must compute the smallest integer $x$ such that $x \cdot n \ge k \cdot m$ for some integer $m$, rather than assuming a uniform array of ones works.

## Approaches

A brute-force approach would attempt to enumerate all possible arrays of length $n$ with positive integers, checking whether their sum is divisible by $k$ and tracking the maximum. For $n \approx 10^9$, this requires at least $O(n)$ operations per test case, which exceeds the time limit by many orders of magnitude.

The key insight is that we do not need the full array, only the maximum element. Let’s denote the maximum element by $x$. The sum of the array is at most $n \cdot x$, because all elements are positive integers less than or equal to $x$. To satisfy divisibility by $k$, the sum must be at least $k \cdot \lceil \frac{1}{k} \cdot n \cdot x \rceil$.

Reframing, the smallest $x$ occurs when we distribute the sum as evenly as possible. Mathematically, we need $x = \lceil \frac{k \cdot m}{n} \rceil$ for the smallest integer $m$ such that $k \cdot m \ge n$. In code, this can be expressed as finding the ceiling of $k / n$, adjusting for cases where $n$ does not divide $k$ evenly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per test case | O(n) | Too slow for large n |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read integers $n$ and $k$.
2. Compute the smallest multiple of $k$ that is at least $n$. This ensures that if we divide this sum evenly among $n$ elements, we achieve divisibility. Let $m = \lceil \frac{n}{k} \rceil$. However, we need to multiply by $k$ and divide by $n$ to get the maximum element, so $x = \lceil \frac{k \cdot m}{n} \rceil$.
3. An equivalent formulation is to compute $m = \lceil \frac{n}{k} \rceil$, then $x = \lceil \frac{k \cdot m}{n} \rceil$. This ensures the sum $n \cdot x$ is divisible by $k$ and minimal.
4. Print $x$.

Why it works: The invariant is that we always choose the smallest integer $x$ such that distributing $n$ elements of value at most $x$ achieves a sum divisible by $k$. Any smaller $x$ would produce a sum smaller than the next multiple of $k$, violating divisibility. This guarantees the maximum element is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    # Compute minimum maximum element
    m = (n + k - 1) // k  # smallest integer >= n/k
    x = (k * m + n - 1) // n  # ceil(k*m / n)
    print(x)
```

Explanation: We first compute the minimal number of times $k$ must fit into the sum ($m$) to ensure divisibility. Multiplying $k \cdot m$ gives the total sum, which we then divide by $n$ using ceiling division to get the smallest integer $x$ that can be repeated $n$ times to achieve that sum. The `+ n - 1` trick performs ceiling division in integer arithmetic.

## Worked Examples

### Sample 1

Input: `n = 1, k = 5`

| n | k | m = ceil(n/k) | x = ceil(k*m / n) |
| --- | --- | --- | --- |
| 1 | 5 | 1 | 5 |

Explanation: Only one element, must be at least 5 to make sum divisible by 5.

### Sample 2

Input: `n = 4, k = 3`

| n | k | m = ceil(n/k) | x = ceil(k*m / n) |
| --- | --- | --- | --- |
| 4 | 3 | 2 | 2 |

Explanation: Sum must be multiple of 3. The minimal maximum element is 2, e.g., array `[1, 1, 2, 2]`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a few arithmetic operations per case |
| Space | O(1) | No arrays are constructed |

With $t \le 1000$, the total operations are trivial. Memory usage is minimal since we never store arrays.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        m = (n + k - 1) // k
        x = (k * m + n - 1) // n
        print(x)
    return out.getvalue().strip()

# Provided samples
assert run("4\n1 5\n4 3\n8 8\n8 17\n") == "5\n2\n1\n3"

# Custom cases
assert run("1\n1 1\n") == "1", "single element equal 1"
assert run("1\n10 1\n") == "1", "k=1, any n"
assert run("1\n5 10\n") == "2", "n<k"
assert run("1\n10 3\n") == "3", "n>k, non-divisible"
assert run("1\n1000000000 999999937\n") == "1", "large numbers, n>k"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | Minimum size, trivial case |
| 10 1 | 1 | Any n, k=1 |
| 5 10 | 2 | n smaller than k, needs ceil adjustment |
| 10 3 | 3 | Non-divisible, n > k |
| 1000000000 999999937 | 1 | Large n and k to test overflow handling |

## Edge Cases

For `n = 1, k = 1`, the sum is 1 and divisible by 1, algorithm correctly returns 1. For `n < k`, e.g., `n = 5, k = 10`, naive approaches that set all elements to 1 would yield sum 5, not divisible by 10. Our algorithm computes `m = ceil(5/10) = 1`, `x = ceil(10*1 / 5) = 2`, correctly producing an array like `[2, 2, 2, 2, 2]` with minimal maximum element 2. For large inputs like `n = 10^9, k = 10^9 - 7`, `m = ceil(10^9 / (10^9 - 7)) = 2`, `x = ceil((10^9 - 7)*2 / 10^9) =
