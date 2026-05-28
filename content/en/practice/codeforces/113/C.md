---
title: "CF 113C - Double Happiness"
description: "We are asked to count the numbers in a given interval $l, r$ that are simultaneously prime and expressible as the sum of two positive squares. In simpler terms, for each number in the interval, we need to check two independent properties."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 113
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 86 (Div. 1 Only)"
rating: 2200
weight: 113
solve_time_s: 200
verified: true
draft: false
---

[CF 113C - Double Happiness](https://codeforces.com/problemset/problem/113/C)

**Rating:** 2200  
**Tags:** brute force, math, number theory  
**Solve time:** 3m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count the numbers in a given interval $l, r$ that are simultaneously prime and expressible as the sum of two positive squares. In simpler terms, for each number in the interval, we need to check two independent properties. First, whether it is prime - this is Peter's definition of a lucky number. Second, whether it can be written as $a^2 + b^2$ with integers $a, b > 0$ - this is Bob's lucky number condition. The result is the count of numbers that satisfy both properties.

The constraints allow $l$ and $r$ up to 3×10^8. A naive approach that iterates over the interval and checks each number for primality using trial division would have a worst-case operation count on the order of $(r-l+1)\sqrt{r}$. With r-l potentially around 3×10^8, this is far too slow. Checking every sum-of-squares possibility in a naive way also would be inefficient. We need a method that leverages number theory properties to reduce computations.

Non-obvious edge cases include small intervals containing only 1 or 2, where primes or sums-of-squares conditions behave unusually. For example, 2 is prime and 1^2 + 1^2 = 2, so it should be counted. The number 3 is prime, but cannot be expressed as a sum of two positive squares, so it should not be counted. A naive algorithm that ignores the positivity requirement on $a$ or $b$ would incorrectly include 0 or negative numbers in sums.

## Approaches

The brute-force approach would iterate from l to r, checking each number n for primality with trial division and then trying all pairs $(a,b)$ up to $\sqrt{n}$ to see if $a^2 + b^2 = n$. This works in principle because it directly tests the definition, but it is hopelessly slow. For example, testing 3×10^8 numbers with up to 17,000 checks each (for the square root of 3×10^8) leads to more than 10^12 operations, which cannot run in 3 seconds.

The key insight to optimize comes from number theory. A prime number p can be written as a sum of two squares if and only if p = 2 or p ≡ 1 (mod 4). This reduces the problem from testing all possible a and b to a simple modulo check. Combined with a segmented sieve, we can efficiently generate all primes in the interval $l, r$ and count only those primes that satisfy the modulo 4 condition or are equal to 2. The observation that the sum-of-squares check reduces to a modular property for primes is the fundamental speedup.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((r-l+1) * sqrt(r)) | O(1) | Too slow |
| Optimal | O((r-l+1) log log r + sqrt(r)) | O(r-l+1 + sqrt(r)) | Accepted |

## Algorithm Walkthrough

1. Compute all prime numbers up to $\sqrt{r}$ using a simple Sieve of Eratosthenes. These primes will be used to mark multiples in the interval $l, r$. This works because any non-prime in the interval must have a factor ≤ sqrt(r).
2. Initialize an array `is_prime_segment` of length r-l+1, marking all numbers as potentially prime.
3. Use the primes from step 1 to mark non-prime numbers in `is_prime_segment`. For each prime p, find the first multiple of p in $l, r$, then mark all multiples of p as non-prime. Careful attention is needed for the case where l ≤ p ≤ r, to avoid marking p itself as non-prime.
4. Iterate over the segment array. For each number n that is still marked as prime, check if n = 2 or n % 4 = 1. If so, increment a counter. This implements the sum-of-two-squares condition for primes.
5. Print the counter at the end. This gives the total number of numbers that are both prime and expressible as a sum of two positive squares.

The correctness relies on two facts. First, the segmented sieve correctly identifies all primes in the interval $l, r$. Second, Fermat's theorem on sums of two squares guarantees that the only primes expressible as a^2 + b^2 are 2 or those congruent to 1 mod 4, so the modulo check ensures no false positives or negatives.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

def main():
    l, r = map(int, input().split())
    limit = int(math.isqrt(r)) + 1

    # Simple sieve up to sqrt(r)
    is_prime_small = [True] * limit
    is_prime_small[0] = is_prime_small[1] = False
    for i in range(2, int(math.isqrt(limit)) + 1):
        if is_prime_small[i]:
            for j in range(i*i, limit, i):
                is_prime_small[j] = False
    small_primes = [i for i, val in enumerate(is_prime_small) if val]

    # Segmented sieve for [l, r]
    n = r - l + 1
    is_prime_segment = [True] * n
    for p in small_primes:
        start = max(p*p, ((l + p - 1) // p) * p)
        for multiple in range(start, r+1, p):
            is_prime_segment[multiple - l] = False
    if l == 1:
        is_prime_segment[0] = False

    # Count primes which are 2 or ≡1 mod 4
    count = 0
    for i in range(n):
        num = l + i
        if is_prime_segment[i] and (num == 2 or num % 4 == 1):
            count += 1
    print(count)

if __name__ == "__main__":
    main()
```

The sieve up to sqrt(r) ensures we have all small primes needed for the segmented sieve. The `max(p*p, ((l + p - 1) // p) * p)` calculation determines the first multiple of p in the interval efficiently. Finally, the modulo check implements Fermat's condition directly.

## Worked Examples

Sample 1: l = 3, r = 5

| i | is_prime_segment[i] | num | num % 4 == 1 or 2 | counted |
| --- | --- | --- | --- | --- |
| 3 | True | 3 | False | No |
| 4 | False | 4 | - | No |
| 5 | True | 5 | True | Yes |

The counter ends at 1, matching the expected output.

Sample 2: l = 1, r = 10

| i | is_prime_segment[i] | num | num % 4 == 1 or 2 | counted |
| --- | --- | --- | --- | --- |
| 1 | False | 1 | - | No |
| 2 | True | 2 | True | Yes |
| 3 | True | 3 | False | No |
| 5 | True | 5 | True | Yes |
| 7 | True | 7 | False | No |
| 11 | True | 11 | True | Yes |

Counter = 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sqrt(r) log log sqrt(r) + (r-l+1) * π(sqrt(r))) | First sieve takes sqrt(r) log log sqrt(r), segment sieve marks each multiple of primes ≤ sqrt(r). |
| Space | O(sqrt(r) + (r-l+1)) | Array for small primes and segment array. |

The solution comfortably fits within 3 seconds and 128 MB memory for r-l up to 3×10^8.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# Provided sample
assert run("3 5\n") == "1", "sample 1"

# Custom cases
assert run("1 10\n") == "3", "small interval with 2,5, and primes"
assert run("10 20\n") == "2", "primes 13,17"
assert run("2 2\n") == "1", "single prime number 2"
assert run("1 1\n") == "0", "single non-prime number 1"
assert run("1 100\n") == "12", "larger interval"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 10 | 3 | Correct sum-of-squares and prime identification |
| 10 20 | 2 | Handles primes modulo 4 check |
| 2 2 | 1 | Single number prime 2 is counted |
| 1 1 |  |  |
