---
title: "CF 162C - Prime factorization"
description: "We are asked to take a positive integer and express it as a product of prime numbers, showing each prime the number of times it appears in the factorization. For example, the number 245 can be expressed as 5 multiplied by 7 twice, so the output would be 577."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 162
codeforces_index: "C"
codeforces_contest_name: "VK Cup 2012 Wild-card Round 1"
rating: 1800
weight: 162
solve_time_s: 76
verified: true
draft: false
---

[CF 162C - Prime factorization](https://codeforces.com/problemset/problem/162/C)

**Rating:** 1800  
**Tags:** *special  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to take a positive integer and express it as a product of prime numbers, showing each prime the number of times it appears in the factorization. For example, the number 245 can be expressed as 5 multiplied by 7 twice, so the output would be 5_7_7. The input is a single integer n, constrained between 2 and 10000. The output is the prime factors in non-decreasing order, with multiplicity reflected by repeated printing of each factor.

The upper bound of n being 10000 allows us to consider algorithms that perform up to roughly 10^6 operations without hitting time limits, so a simple trial division approach is feasible. However, careless implementations can go wrong with small edge cases like prime numbers themselves, numbers that are perfect squares of primes, or numbers with multiple repeated small factors. For instance, n = 13 should output 13, not produce an empty factorization, and n = 16 should output 2_2_2_2, not just 2_8 or 4*4, because we require prime factors only.

## Approaches

The most straightforward approach is to iterate from 2 to n and repeatedly divide n by any number that divides it evenly. Each division corresponds to one occurrence of that factor. This brute-force method works because we eventually try every integer up to n, so we will catch all prime factors. For n = 10000, in the worst case, this might require 10000 iterations, and each iteration could involve repeated divisions, leading to roughly O(n) complexity. This is acceptable for n ≤ 10000, but we can do better.

The key insight is that we only need to check divisors up to the square root of n. Any factor larger than √n must be paired with a smaller factor, so once we've divided out all smaller factors, any remaining n itself must be prime. This reduces the number of iterations significantly, turning a potential O(n) approach into O(√n), which is much faster and still trivial to implement for n ≤ 10000.

The optimal approach combines trial division up to √n with handling any remaining prime after that. By printing each factor immediately when found, we naturally maintain the required non-decreasing order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted for n ≤ 10000 |
| Optimal (√n trial division) | O(√n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer n from input. This is the number we need to factorize.
2. Initialize a variable d to 2, which represents the current candidate divisor. We start with 2 because it is the smallest prime.
3. While d*d ≤ n, check if n is divisible by d. If n % d == 0, print d (or store it) and divide n by d. Repeat this step until n is no longer divisible by d. This captures all powers of d in the factorization.
4. Increment d by 1 and repeat step 3. We only need to go up to √n because any factor larger than √n would have a corresponding smaller factor that has already been divided out.
5. After the loop, if n > 1, print n as it is a remaining prime factor. This handles the case where n itself is prime or there is a large prime factor left.

Why it works: At each step, we divide out the smallest prime factor available. The invariant is that n is always the remaining portion of the number not yet factorized, and all primes less than d have already been fully divided out. This guarantees that we do not miss any factor and that the factors are output in non-decreasing order.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
d = 2
factors = []

while d * d <= n:
    while n % d == 0:
        factors.append(str(d))
        n //= d
    d += 1

if n > 1:
    factors.append(str(n))

print('*'.join(factors))
```

The code follows the algorithm step by step. We maintain a list of factors as strings for convenient joining with '*'. The inner while loop ensures all powers of each prime are captured. Incrementing d ensures we test all possible divisors up to √n. Finally, appending n if it is greater than 1 covers any remaining prime larger than √n. A common mistake is to forget this final check, which would give incorrect results for prime numbers or numbers with large prime factors.

## Worked Examples

Sample Input 1: 245

| Step | n | d | factors |
| --- | --- | --- | --- |
| init | 245 | 2 | [] |
| divide by 2? | 245 | 2 | [] |
| increment d | 245 | 3 | [] |
| increment d | 245 | 4 | [] |
| increment d | 245 | 5 | [] |
| divide by 5 | 49 | 5 | ['5'] |
| increment d | 49 | 6 | ['5'] |
| ... | 49 | 7 | ['5'] |
| divide by 7 | 7 | 7 | ['5', '7'] |
| divide by 7 | 1 | 7 | ['5', '7', '7'] |
| loop ends | 1 | 8 | ['5', '7', '7'] |

Output: 5_7_7. The trace shows that all factors are captured in non-decreasing order, and repeated factors appear the correct number of times.

Sample Input 2: 13

| Step | n | d | factors |
| --- | --- | --- | --- |
| init | 13 | 2 | [] |
| divide by 2? | 13 | 2 | [] |
| increment d | 13 | 3 | [] |
| increment d | 13 | 4 | [] |
| loop ends | 13 | 5 | [] |
| remaining n > 1 | 13 | 5 | ['13'] |

Output: 13. The algorithm correctly handles a prime number by appending it at the end.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(√n) | The outer loop iterates up to √n, inner loop divides out powers of each prime. For n ≤ 10000, this is a few hundred iterations. |
| Space | O(log n) | We store the list of factors. The maximum number of factors is O(log n) because the smallest prime factor is 2, so the number of times 2 can divide n is log2(n). |

This complexity is well within the 3-second limit and the 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    d = 2
    factors = []

    while d * d <= n:
        while n % d == 0:
            factors.append(str(d))
            n //= d
        d += 1

    if n > 1:
        factors.append(str(n))

    return '*'.join(factors)

# Provided sample
assert run("245\n") == "5*7*7", "sample 1"

# Custom cases
assert run("16\n") == "2*2*2*2", "all 2s"
assert run("13\n") == "13", "prime number"
assert run("10000\n") == "2*2*2*2*5*5*5*5", "mixed small primes"
assert run("9973\n") == "9973", "large prime"
assert run("72\n") == "2*2*2*3*3", "small composite with multiple primes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 16 | 2_2_2*2 | repeated small prime factor |
| 13 | 13 | prime number handling |
| 10000 | 2_2_2_2_5_5_5*5 | combination of repeated primes |
| 9973 | 9973 | large prime number |
| 72 | 2_2_2_3_3 | multiple distinct small primes |

## Edge Cases

For a prime number like 13, the loop checking divisors up to √13 will not divide out anything. After the loop, n is still 13, so appending it ensures the prime is captured correctly. For powers of a single prime like 16, the inner loop divides out 2 four times, demonstrating that repeated factors are counted correctly. For a number with both small and large primes like 10000, the algorithm correctly captures multiple occurrences of 2 and 5 without missing any factor. This method avoids common mistakes like stopping after the first factor or forgetting to handle remaining primes above √n.
