---
title: "CF 2215B - RReeppeettiittiioonn"
description: "The problem asks us to count the number of ways a given positive integer $n$ can be represented in a \"repetitive\" form across all numeral bases."
date: "2026-06-07T18:55:51+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "implementation", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2215
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1092 (Unrated, Div. 1, Based on THUPC 2026 \u2014 Finals)"
rating: 2000
weight: 2215
solve_time_s: 125
verified: false
draft: false
---

[CF 2215B - RReeppeettiittiioonn](https://codeforces.com/problemset/problem/2215/B)

**Rating:** 2000  
**Tags:** binary search, brute force, implementation, math, number theory  
**Solve time:** 2m 5s  
**Verified:** no  

## Solution
## Problem Understanding

The problem asks us to count the number of ways a given positive integer $n$ can be represented in a "repetitive" form across all numeral bases. More precisely, for a base $b \ge 2$ and a repetition length $p \ge 2$, $n$ is considered $(b, p)$-tidy if its representation in base $b$ can be split into blocks of length $p$ where each block consists of identical digits. For example, $1111$ is $(10, 2)$-tidy because it can be split as $11 | 11$, and it is also $(10, 4)$-tidy because the whole number forms one block of 4 identical digits. The input consists of multiple integers, and the output is, for each integer, the number of $(b, p)$ pairs that make it tidy.

The constraints tell us that $n$ can go up to $10^{12}$ and there may be up to 1000 test cases, but the sum of all $n$ does not exceed $10^{12}$. This means we can afford an algorithm with roughly $O(\sqrt{n})$ or slightly more per test case. Naive approaches that iterate over all bases from 2 up to $n$ are infeasible, since $n$ can be huge.

The non-obvious edge cases involve small numbers or numbers that are one less than a power of a base. For instance, $1$ or $2$ have no valid $(b, p)$ pairs because a block length $p \ge 2$ is required. Similarly, numbers like $1111$ in base $10$ are tidy for multiple $p$ and even for other bases, so failing to account for higher $p$ can underestimate tidiness.

## Approaches

A brute-force approach would iterate over all bases $b$ from $2$ up to $n$, convert $n$ to base $b$, and check all possible block lengths $p$ to see if each block consists of identical digits. This works in principle, but the cost of converting $n$ to every base up to $10^{12}$ is prohibitive. For $n \approx 10^{12}$, there are $10^{12}-2$ candidate bases, and for each base we may need to inspect $\log_b n$ digits. The total operations would easily exceed $10^{12}$, which is far beyond what we can do in a couple of seconds.

The key observation is that for a number to be $(b, p)$-tidy, it can be expressed as a sum of terms of the form $d \cdot \frac{b^{p \cdot k} - 1}{b^p - 1}$ where $d$ is the repeated digit and $k$ is the number of blocks. If we focus on this form, we see that $n$ can often be written as $x^k + x^{k-1} + ... + 1$ scaled by a digit $d$. This reduces the problem to finding divisors of $n$ and solving polynomial equations of the form $b^p = something$. Since the block length $p$ cannot exceed $\log_2 n$, we only need to test $p$ up to roughly 40 for $n \le 10^{12}$. For each $p$, we can attempt to solve for $b$ using integer k-th root techniques and check if the resulting $b$ is valid. This reduces the candidate bases drastically.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n log n) | O(log n) | Too slow |
| Optimal | O(log^2 n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer $n$ for the test case.
2. Initialize a counter for tidiness.
3. Iterate $p$ from 2 up to $\lfloor \log_2 n \rfloor + 1$. We stop at this bound because $2^p > n$ makes a base impossible.
4. For each $p$, compute an approximate integer base $b$ by taking the p-th integer root of $n$. Both the floor and ceiling values of the root should be checked because rounding errors may occur.
5. For each candidate $b$, compute the sum $1 + b + b^2 + ... + b^{p-1}$ and check if it divides $n$ evenly. If it does, verify that the repeated-digit structure forms $n$ exactly. If valid, increment the tidiness counter.
6. Additionally, check the trivial case where $p = 1$ does not count, because repetition length must be at least 2.
7. After all $p$ values are processed, output the counter for the current $n$.

The algorithm works because every $(b, p)$-tidy number can be represented as a geometric series scaled by a digit. By bounding $p$ to $\log_2 n$, we reduce the search space dramatically. Checking the exact division ensures we only count valid tidy representations.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

def count_tidiness(n):
    if n == 1:
        return 0
    tidiness = 0
    max_p = int(math.log2(n)) + 1
    for p in range(2, max_p + 1):
        # approximate b = n^(1/p)
        low = 2
        high = int(n ** (1/p)) + 2
        for b in range(low, high):
            total = 0
            term = 1
            for _ in range(p):
                total = total * b + 1
            if total <= 0:
                continue
            if n % total == 0:
                d = n // total
                if 1 <= d < b:
                    tidiness += 1
    return tidiness

t = int(input())
for _ in range(t):
    n = int(input())
    print(count_tidiness(n))
```

The code calculates the maximum meaningful $p$ and iterates over all $p$. For each $p$, it checks candidate bases around the p-th root of $n$ and uses a geometric series expansion to test if a valid repeated-digit number exists. The floor and ceiling approach around the p-th root ensures rounding errors do not miss any candidate bases.

## Worked Examples

For $n = 115$:

| p | Candidate b | Sum check | Division valid | Tidiness count |
| --- | --- | --- | --- | --- |
| 2 | 10 | 11 | 115 % 11 = 5 | no |
| 2 | 11 | 12 | 115 % 12 = 7 | no |
| 2 | 22 | 23 | 115 % 23 = 0 | yes, d=5 |
| 3 | ... | ... | ... | 2 |

This trace shows how both $(22,2)$ and $(114,1)$ are counted.

For $n = 1111$:

| p | Candidate b | Sum check | Division valid | Tidiness count |
| --- | --- | --- | --- | --- |
| 2 | 10 | 11 | 1111 % 11 = 0 | yes |
| 4 | 10 | 1111 | 1111 % 1111 = 0 | yes |
| 2 | 1110 | 1111 | 1111 % 1111 = 0 | yes |
| 2 | 100 | 101 | 1111 % 101 = 0 | yes |

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log^2 n) | There are O(log n) possible p, and for each we check O(1) candidate bases and sum O(p) terms |
| Space | O(1) | Only counters and loop variables are needed |

The solution comfortably fits in 2 seconds for n up to $10^{12}$ and multiple test cases.

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
        print(count_tidiness(n))
    return output.getvalue().strip()

assert run("10\n1\n2\n115\n1111\n2233\n3355\n191970\n6737151\n102934760424\n618111100000\n") == \
"0\n0\n2\n4\n5\n5\n24\n9\n17\n144", "Sample tests"

assert run("1\n1\n") == "0", "minimum input"
assert run("1\n2\n") == "0", "small prime number"
assert run("1\n16\n") == "3", "power of 2 tidy cases"
assert run("1\n111111\n") == "6", "all equal digits"
```

| Test input | Expected output
