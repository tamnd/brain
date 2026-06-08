---
title: "CF 2044A - Easy Problem"
description: "We are asked to count ordered pairs of positive integers $(a, b)$ such that $a + b = n$, for multiple test cases. Each test case gives a single integer $n$, and we must output the total number of pairs $(a, b)$ that satisfy the equation."
date: "2026-06-08T09:22:27+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 2044
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 993 (Div. 4)"
rating: 800
weight: 2044
solve_time_s: 77
verified: true
draft: false
---

[CF 2044A - Easy Problem](https://codeforces.com/problemset/problem/2044/A)

**Rating:** 800  
**Tags:** brute force, math  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count ordered pairs of positive integers $(a, b)$ such that $a + b = n$, for multiple test cases. Each test case gives a single integer $n$, and we must output the total number of pairs $(a, b)$ that satisfy the equation. The key is that both $a$ and $b$ must be strictly positive.

The constraints are small: $2 \le n \le 100$ and up to 99 test cases. Because $n$ is at most 100, any solution that runs in linear time per test case is perfectly acceptable. The naive approach will be fast enough, but we can still reason about a closed-form formula.

The smallest possible $n$ is 2. In that case, the only pair is $(1,1)$. If a solution ignores the positivity requirement and counts zero or negative numbers, it would produce an incorrect answer. Similarly, if the algorithm double-counted symmetric pairs or miscounted boundary values like $n=2$ or $n=100$, it would be wrong.

## Approaches

A brute-force approach iterates through all possible values of $a$ from 1 to $n-1$ and counts the pairs where $b = n - a$ is positive. This works because $b$ is uniquely determined by $a$, and $a$ can never reach $n$ since then $b$ would be zero. The brute-force solution is correct but unnecessarily verbose for such a small problem.

The key insight is that for a given $n$, all pairs are of the form $(1, n-1), (2, n-2), ..., (n-1, 1)$. Each $a$ from 1 to $n-1$ produces a valid $b$, so the number of pairs is simply $n-1$. This is a closed-form solution and eliminates loops entirely, which is the simplest and most direct approach.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per test case | O(1) | Accepted due to small n |
| Closed-Form | O(1) per test case | O(1) | Accepted and simplest |

## Algorithm Walkthrough

1. Read the number of test cases $t$. This determines how many times we will repeat the calculation.
2. For each test case, read the integer $n$. This is the sum we want to split into two positive integers.
3. Compute the number of valid pairs as $n-1$. This works because the pairs are exactly $(1, n-1), (2, n-2), ..., (n-1, 1)$, and there are $n-1$ terms.
4. Print the result immediately or store it in a list to print after all test cases.

Why it works: the invariant is that for every integer $a$ in the range 1 to $n-1$, $b = n - a$ is automatically positive. No values are skipped or double-counted, and every possible pair is accounted for.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    print(n - 1)
```

The solution first reads the number of test cases. For each test case, it reads $n$ and prints $n-1$. Using `sys.stdin.readline` ensures fast input handling, even though the input size is small. No additional data structures are needed. The subtraction handles all valid $n \ge 2$ automatically, avoiding off-by-one errors.

## Worked Examples

Trace Sample 1 input `3\n2\n4\n6\n`:

| Test Case | n | Computation | Result |
| --- | --- | --- | --- |
| 1 | 2 | 2 - 1 | 1 |
| 2 | 4 | 4 - 1 | 3 |
| 3 | 6 | 6 - 1 | 5 |

The table shows that for each $n$, subtracting 1 correctly counts all valid pairs. For $n=2$, only $(1,1)$ exists. For $n=4$, the pairs $(1,3),(2,2),(3,1)$ sum to 4, giving 3 pairs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case requires a single subtraction. |
| Space | O(1) | No arrays or auxiliary storage are needed. |

Given $t \le 99$ and $n \le 100$, the solution is instantaneous on modern hardware and well within memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n = int(input())
        output.append(str(n-1))
    return "\n".join(output)

# Provided samples
assert run("3\n2\n4\n6\n") == "1\n3\n5", "sample 1"

# Custom cases
assert run("1\n2\n") == "1", "minimum n"
assert run("1\n100\n") == "99", "maximum n"
assert run("2\n3\n5\n") == "2\n4", "small n, odd and even"
assert run("1\n50\n") == "49", "mid-range n"
assert run("1\n99\n") == "98", "odd n near max"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n2\n | 1 | Minimum n value |
| 1\n100\n | 99 | Maximum n value |
| 2\n3\n5\n | 2\n4 | Small n, mixture of odd and even |
| 1\n50\n | 49 | Mid-range n |
| 1\n99\n | 98 | Odd n near maximum, boundary handling |

## Edge Cases

The edge case with $n=2$ is handled correctly. The algorithm computes $2-1=1$, giving the single pair $(1,1)$. The edge case with maximum $n=100$ produces $99$, which is exactly the count of $(1,99),(2,98),...,(99,1)$. No loops are required, so the solution avoids off-by-one errors entirely. The positivity requirement is naturally enforced because $a$ starts from 1 and goes up to $n-1$.
