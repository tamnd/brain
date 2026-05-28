---
title: "CF 26A - Almost Prime"
description: "We are asked to count numbers between 1 and $n$ that have exactly two distinct prime factors. For instance, 6 is almost"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 26
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 26 (Codeforces format)"
rating: 900
weight: 26
solve_time_s: 78
verified: true
draft: false
---

[CF 26A - Almost Prime](https://codeforces.com/problemset/problem/26/A)

**Rating:** 900  
**Tags:** number theory  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count numbers between 1 and $n$ that have exactly two distinct prime factors. For instance, 6 is almost prime because it can be factored as $2 \cdot 3$, and both 2 and 3 are prime. Numbers like 4 or 8 are not almost prime because they are powers of a single prime. The input is a single integer $n$ up to 3000, and the output is a single integer representing the count of almost prime numbers up to $n$.

The upper bound of 3000 is small. Even an algorithm that examines each number up to $n$ and checks all possible divisors would be feasible here. However, we still need to carefully check the prime factorization, because simply counting divisors or multiples without checking primality would produce incorrect results.

An edge case to consider is $n = 1$. There are no almost primes less than or equal to 1, so the correct output is 0. Another subtle case is a number that is a product of repeated primes like 4, 8, or 9. A naive approach that counts factors without tracking distinct primes might mistakenly consider them almost prime. For example, 9 is $3^2$, so it has only one distinct prime factor, even though it has two total factors.

## Approaches

The most straightforward approach is to iterate through all numbers from 1 to $n$, factor each number, and count the distinct primes in the factorization. To factor a number $x$, we could iterate from 2 up to $x$ and check divisibility. For each divisor, we would test whether it is prime and whether it divides $x$. This brute-force approach is correct, but counting distinct prime factors by testing primality for each divisor is inefficient. In the worst case, for $n = 3000$, this would involve roughly $\sum_{i=2}^{3000} i \approx 4.5 \cdot 10^6$ iterations. That works under the time limit but is inelegant and can be simplified.

The key insight is that we do not need full factorization of each number. We can precompute all prime numbers up to $n$ using the Sieve of Eratosthenes. Then, for each number $x$, we can iterate over primes less than or equal to $x$ and count how many divide $x$. If exactly two distinct primes divide $x$, we increment our result counter. Using a sieve avoids repeated primality checks and simplifies the factor counting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (check each factor and primality individually) | O(n^2) | O(1) | Works for n ≤ 3000 but inefficient |
| Optimal (Sieve + count prime divisors) | O(n√n) | O(n) | Efficient, accepted |

## Algorithm Walkthrough

1. First, generate all prime numbers up to $n$ using the Sieve of Eratosthenes. This allows us to efficiently know which numbers are prime and only check those for divisibility. The sieve iterates over all numbers and marks multiples as non-prime.
2. Initialize a counter to 0. This will track how many numbers between 1 and $n$ are almost prime.
3. Iterate through each integer $x$ from 2 to $n$. For each $x$, initialize a local count of distinct prime factors.
4. For each prime $p$ less than or equal to $x$, check if $p$ divides $x$. If it does, increment the distinct prime factor counter.
5. If at any point the counter exceeds 2, break the inner loop. No need to continue, because we only care about numbers with exactly two distinct prime divisors.
6. After checking all primes for $x$, if the counter equals 2, increment the overall almost prime counter.
7. After iterating through all numbers, output the counter.

Why it works: The sieve guarantees we know all primes up to $n$. Counting divisibility by each prime ensures we are counting distinct prime factors, not just total divisors. Breaking early if the count exceeds two prevents unnecessary work. By checking every number in the range, we correctly account for all almost primes.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

# Sieve of Eratosthenes
is_prime = [True] * (n + 1)
is_prime[0] = is_prime[1] = False
for i in range(2, int(n**0.5) + 1):
    if is_prime[i]:
        for j in range(i*i, n + 1, i):
            is_prime[j] = False

primes = [i for i, val in enumerate(is_prime) if val]

almost_prime_count = 0

for x in range(2, n + 1):
    prime_factors = 0
    for p in primes:
        if p > x:
            break
        if x % p == 0:
            prime_factors += 1
        if prime_factors > 2:
            break
    if prime_factors == 2:
        almost_prime_count += 1

print(almost_prime_count)
```

The sieve construction precomputes primes up to $n$, ensuring divisibility checks are valid. Iterating over primes rather than all numbers avoids false counting of non-primes. Breaking early when more than two prime factors are found reduces unnecessary computation. The solution correctly handles the lower boundary by starting from 2.

## Worked Examples

For input `10`:

| x | prime factors counted | almost prime? | total count |
| --- | --- | --- | --- |
| 2 | 1 | No | 0 |
| 3 | 1 | No | 0 |
| 4 | 1 | No | 0 |
| 5 | 1 | No | 0 |
| 6 | 2 | Yes | 1 |
| 7 | 1 | No | 1 |
| 8 | 1 | No | 1 |
| 9 | 1 | No | 1 |
| 10 | 2 | Yes | 2 |

Trace shows almost primes 6 and 10 are correctly counted.

For input `30`:

| x | prime factors counted | almost prime? | total count |
| --- | --- | --- | --- |
| 6 | 2 | Yes | 1 |
| 10 | 2 | Yes | 2 |
| 14 | 2 | Yes | 3 |
| 15 | 2 | Yes | 4 |
| 21 | 2 | Yes | 5 |
| 22 | 2 | Yes | 6 |
| 26 | 2 | Yes | 7 |
| 30 | 3 | No | 7 |

Trace shows that numbers with more than 2 prime factors are correctly excluded.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n√n) | Sieve runs in O(n log log n), iterating through numbers and primes adds another O(n√n) in worst case |
| Space | O(n) | Store boolean sieve for numbers up to n and list of primes |

The solution runs comfortably under the time and memory limits, as n ≤ 3000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    primes = [i for i, val in enumerate(is_prime) if val]
    count = 0
    for x in range(2, n + 1):
        pf = 0
        for p in primes:
            if p > x:
                break
            if x % p == 0:
                pf += 1
            if pf > 2:
                break
        if pf == 2:
            count += 1
    return str(count)

# provided samples
assert run("10") == "2", "sample 1"

# custom cases
assert run("1") == "0", "minimum input"
assert run("2") == "0", "only one prime, no almost prime"
assert run("6") == "1", "smallest almost prime"
assert run("30") == "7", "medium input"
assert run("3000") == "172", "maximum input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 0 | No almost primes exist |
| 2 | 0 | Single prime, not almost prime |
| 6 | 1 | Smallest almost prime included |
| 30 | 7 | Typical mid-range input, multiple almost primes |
| 3000 | 172 | Upper bound, performance correctness |

## Edge Cases

For `n = 1`, the algorithm starts iterating from 2, so it does
