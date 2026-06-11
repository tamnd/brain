---
title: "CF 1370A - Maximum GCD"
description: "We are asked to find the largest possible greatest common divisor among all pairs of distinct integers from 1 to n. For a given n, we need the maximum gcd of any two numbers a and b where 1 ≤ a < b ≤ n."
date: "2026-06-11T11:24:46+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1370
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 651 (Div. 2)"
rating: 800
weight: 1370
solve_time_s: 94
verified: true
draft: false
---

[CF 1370A - Maximum GCD](https://codeforces.com/problemset/problem/1370/A)

**Rating:** 800  
**Tags:** greedy, implementation, math, number theory  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to find the largest possible greatest common divisor among all pairs of distinct integers from 1 to n. For a given n, we need the maximum gcd of any two numbers a and b where 1 ≤ a < b ≤ n. The input consists of multiple test cases, each specifying a value of n, and the output is a single integer per test case.

The constraints tell us that n can go up to 10^6, and there can be up to 100 test cases. A naive solution that tries all pairs of integers would perform roughly n²/2 gcd computations in the worst case. For n = 10^6, this is on the order of 5 × 10^11 operations, far too large to run in one second. We need an approach that runs in near-linear or logarithmic time relative to n.

Edge cases include the smallest n = 2, where the only pair is (1, 2) and gcd is 1. Another subtlety arises when n is odd versus even. For example, if n = 3, the pairs are (1, 2), (1, 3), (2, 3), all of which have gcd 1. For n = 5, the pair (2, 4) has gcd 2, which is larger than 1. Any solution that does not account for these patterns might underestimate the maximum gcd.

## Approaches

The brute-force approach is straightforward: iterate over all pairs (a, b), compute gcd(a, b) for each, and track the maximum. This is correct because it directly tests every possible combination, but it is too slow when n reaches 10^6. For t = 100 test cases, it would need more than 10^13 operations in the worst scenario, which is clearly impractical.

The optimal approach hinges on the observation that the largest possible gcd must be at least n//2. Consider the number n itself. If we look for a multiple of k ≤ n that forms a pair with gcd k, the largest k that allows two distinct multiples in [1, n] is n//2. This works because the pair (k, 2k) is always in the range when k ≤ n//2. No larger value of k can produce two distinct multiples within the range. Therefore, for each n, the maximum gcd is simply n//2.

This insight reduces the problem to a single integer division per test case, making the solution O(1) per case and O(t) overall.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases t. This tells us how many independent values of n we need to process.
2. For each test case, read the integer n.
3. Compute n divided by 2 using integer division. Assign this value to max_gcd. This works because the largest integer that has at least two multiples in [1, n] is exactly n//2.
4. Output max_gcd for this test case.
5. Repeat steps 2-4 for all test cases.

Why it works: For any k > n//2, the only multiple of k in [1, n] is k itself, which cannot form a pair of distinct numbers. For k ≤ n//2, the pair (k, 2k) is valid, ensuring gcd k. Thus n//2 is the maximum possible gcd among all pairs.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    print(n // 2)
```

The code reads the number of test cases, then iterates over each n. The integer division operator `//` ensures we always round down, which is critical for odd n values. Printing directly after computing avoids storing unnecessary data and keeps memory usage minimal.

## Worked Examples

Sample 1:

Input n = 3

| n | n // 2 | max_gcd |
| --- | --- | --- |
| 3 | 1 | 1 |

The pair (1, 2) or (1, 3) or (2, 3) all have gcd 1. n//2 correctly gives 1.

Sample 2:

Input n = 5

| n | n // 2 | max_gcd |
| --- | --- | --- |
| 5 | 2 | 2 |

The pair (2, 4) has gcd 2, which is the maximum. n//2 correctly identifies this.

These traces demonstrate that for both small odd and even n, the algorithm selects the correct maximal gcd.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | One integer division per test case, constant time |
| Space | O(1) | No additional memory aside from input and output |

Given t ≤ 100, the solution performs at most 100 simple operations, comfortably within the time limit. Memory is negligible, far below the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n = int(input())
        print(n // 2)
    return output.getvalue().strip()

# Provided samples
assert run("2\n3\n5\n") == "1\n2", "sample 1 & 2"

# Minimum-size input
assert run("1\n2\n") == "1", "minimum n"

# Maximum-size input
assert run("1\n1000000\n") == "500000", "maximum n"

# Odd n
assert run("1\n7\n") == "3", "odd n"

# Even n
assert run("1\n8\n") == "4", "even n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 | 1 | minimum n handling |
| 1000000 | 500000 | maximum n handling |
| 7 | 3 | odd n case |
| 8 | 4 | even n case |

## Edge Cases

For n = 2, the only pair is (1, 2). The algorithm computes 2//2 = 1, which matches the actual maximum gcd. For odd n like 7, the largest pair with maximal gcd is (3, 6), giving gcd 3. The algorithm outputs 7//2 = 3, correctly identifying this. For large n = 10^6, the algorithm computes 500000, which is the gcd of the pair (500000, 1000000), demonstrating that the solution scales to the upper constraint without issue.
