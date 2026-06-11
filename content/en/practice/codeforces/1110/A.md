---
title: "CF 1110A - Parity"
description: "The problem gives a number $n$ not in decimal form, but in some arbitrary base $b$. The digits of $n$ are listed from the most significant to the least significant, and the task is to decide whether $n$ is even or odd in decimal."
date: "2026-06-12T05:07:30+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1110
codeforces_index: "A"
codeforces_contest_name: "Codeforces Global Round 1"
rating: 900
weight: 1110
solve_time_s: 309
verified: false
draft: false
---

[CF 1110A - Parity](https://codeforces.com/problemset/problem/1110/A)

**Rating:** 900  
**Tags:** math  
**Solve time:** 5m 9s  
**Verified:** no  

## Solution
## Problem Understanding

The problem gives a number $n$ not in decimal form, but in some arbitrary base $b$. The digits of $n$ are listed from the most significant to the least significant, and the task is to decide whether $n$ is even or odd in decimal. For example, if the base is 13 and the digits are [3, 2, 7], then the decimal value of $n$ is $3\cdot13^2 + 2\cdot13 + 7 = 540$, which is even.

The constraints allow up to $10^5$ digits, and each digit can be as large as 99 (since $b \le 100$). Computing the full decimal number is impossible because the value of $n$ can be astronomically large, far beyond standard integer limits. This rules out any approach that tries to directly calculate $n$ and then check its parity.

An edge case arises when there is only one digit or when the base is even. For a single-digit number, the parity is determined solely by that digit. For larger numbers, the interplay between the parity of the base and the digits matters, because multiplying an odd or even digit by powers of the base can affect the final parity in predictable ways.

A careless approach would try to compute $n$ directly or reduce modulo 2 at the wrong point. For example, summing the products $a_i \cdot b^{k-i}$ without considering modular arithmetic would overflow. Another subtle case is when the base is even: then all terms except the last are guaranteed to be even, so only the last digit matters. This observation is crucial.

## Approaches

The brute-force method would construct $n$ by summing $a_1 \cdot b^{k-1} + a_2 \cdot b^{k-2} + \dots + a_k$. This works for small $k$ and $b$, but with $k$ up to $10^5$, this approach would require multiplying very large numbers repeatedly. Even with modular arithmetic to reduce modulo 2, it would still require iterating over all digits and computing powers of $b$, which is unnecessary.

The optimal approach leverages modular arithmetic and the parity property. A number is even if it is divisible by 2, which can be determined modulo 2. Observe that any power of an even base is even, so when $b$ is even, all digits except the last are multiplied by an even number, contributing 0 modulo 2. Only the last digit $a_k$ affects parity. When $b$ is odd, every power of $b$ is odd. Therefore, each term contributes $a_i \cdot 1 \mod 2 = a_i \mod 2$, so the parity of $n$ is the sum of all digits modulo 2.

This insight reduces the problem to either checking the last digit (even base) or summing all digits modulo 2 (odd base). The brute-force approach iterates over digits anyway, but the optimal approach does only one simple modulo operation per digit, avoiding big integer operations entirely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k log n) | O(1) | Too slow due to huge numbers |
| Optimal | O(k) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the base `b` and the number of digits `k`. These define the structure of the number in its given base.
2. Read the `k` digits into a list `a`. They are ordered from most significant to least significant.
3. Check if `b` is even. If it is, then every power of `b` greater than zero is even. Therefore, all contributions except the last digit are irrelevant to parity.
4. If `b` is even, print "even" if the last digit `a[-1]` is even, otherwise print "odd".
5. If `b` is odd, iterate over all digits and compute the sum modulo 2. If the sum is divisible by 2, print "even"; otherwise print "odd".

Why it works: When reducing modulo 2, multiplication by an even number results in 0, so only digits multiplied by odd powers of an odd base contribute. The algorithm maintains the invariant that the current modulo-2 sum accurately reflects the parity of the entire number at each step. This ensures correctness without computing the full value.

## Python Solution

```python
import sys
input = sys.stdin.readline

b, k = map(int, input().split())
a = list(map(int, input().split()))

if b % 2 == 0:
    print("even" if a[-1] % 2 == 0 else "odd")
else:
    total = sum(a) % 2
    print("even" if total == 0 else "odd")
```

The solution first reads input efficiently using `sys.stdin.readline`. It checks the base parity immediately. For even bases, only the last digit is checked, which avoids unnecessary computation. For odd bases, it sums all digits modulo 2, ensuring the result matches the parity of the number without ever constructing the full integer. Off-by-one errors are avoided by correctly indexing the last digit as `a[-1]`.

## Worked Examples

Sample 1: `13 3` with digits `[3, 2, 7]`.

| Step | Description | Value |
| --- | --- | --- |
| Read b, k | base 13, 3 digits | b=13, k=3 |
| Read digits | digits list | a=[3,2,7] |
| Check b parity | 13 is odd | sum(a) % 2 = (3+2+7)%2 = 12%2 = 0 |
| Output | even | "even" |

This demonstrates that when the base is odd, summing all digits modulo 2 correctly determines parity.

Sample 2: `2 5` with digits `[1, 0, 0, 1, 1]`.

| Step | Description | Value |
| --- | --- | --- |
| Read b, k | base 2, 5 digits | b=2, k=5 |
| Read digits | digits list | a=[1,0,0,1,1] |
| Check b parity | 2 is even | last digit a[-1] = 1 -> odd |
| Output | odd | "odd" |

This shows that for even bases, only the last digit matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) | One pass over the digits list to sum modulo 2 (or take the last element) |
| Space | O(k) | Storing the list of digits |

Given `k <= 10^5`, O(k) operations are well within the 1-second limit, and memory usage for 100,000 integers fits comfortably within 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    b, k = map(int, input().split())
    a = list(map(int, input().split()))
    if b % 2 == 0:
        return "even" if a[-1] % 2 == 0 else "odd"
    else:
        return "even" if sum(a) % 2 == 0 else "odd"

# Provided samples
assert run("13 3\n3 2 7\n") == "even", "sample 1"
assert run("10 9\n1 2 3 4 5 6 7 8 9\n") == "odd", "sample 2"
assert run("99 5\n32 92 85 74 4\n") == "odd", "sample 3"
assert run("2 1\n2\n") == "even", "sample 4"

# Custom cases
assert run("2 5\n0 0 0 0 0\n") == "even", "all zeros even base"
assert run("2 5\n1 1 1 1 1\n") == "odd", "all ones even base"
assert run("3 4\n1 2 0 2\n") == "odd", "odd base multiple digits"
assert run("100 2\n99 50\n") == "even", "even base, last digit even"
assert run("5 3\n2 4 1\n") == "odd", "odd base, sum odd"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 5, [0,0,0,0,0] | even | even base, last digit zero |
| 2 5, [1,1,1,1,1] | odd | even base, last digit odd |
| 3 4, [1,2,0,2] | odd | odd base, sum modulo 2 |
| 100 2, [99,50] | even | even base, last digit even |
| 5 3, [2,4,1] | odd | odd base, sum modulo 2 |

## Edge Cases

For a single-digit number in any base, the algorithm correctly reduces to checking that digit modulo 2. For `b` even, it uses `a[-1] % 2`. For `b` odd, `sum(a) % 2` is identical to `a[0] % 2`. For maximum-size input with 100
