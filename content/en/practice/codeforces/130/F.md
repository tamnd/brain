---
title: "CF 130F - Prime factorization"
description: "The task is to decompose a given integer n into its prime factors and print them in non-decreasing order, with each prime repeated according to its multiplicity. Essentially, if a number is a product of primes like $n = 2^2 cdot 3^1 cdot 5^2$, the output should be 2 2 3 5 5."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 130
codeforces_index: "F"
codeforces_contest_name: "Unknown Language Round 4"
rating: 1600
weight: 130
solve_time_s: 108
verified: true
draft: false
---

[CF 130F - Prime factorization](https://codeforces.com/problemset/problem/130/F)

**Rating:** 1600  
**Tags:** *special  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to decompose a given integer _n_ into its prime factors and print them in non-decreasing order, with each prime repeated according to its multiplicity. Essentially, if a number is a product of primes like $n = 2^2 \cdot 3^1 \cdot 5^2$, the output should be `2 2 3 5 5`. The input is a single integer between 2 and 250, which is small enough that we do not need advanced factorization algorithms like Pollard's rho or sieves optimized for very large numbers.

Because the upper bound is only 250, we can perform operations proportional to $n$ or $\sqrt{n}$ comfortably within a 2-second time limit. The main edge cases arise when _n_ itself is prime (e.g., 2, 3, 197), in which case the factorization is just `n`, or when _n_ is a perfect square of a prime (e.g., 49 = 7*7), which tests whether the algorithm correctly handles repeated factors. A naive approach that divides by every number up to _n_ will work here because $n \le 250$, but we can do slightly better by only considering potential divisors up to $\sqrt{n}$.

Another subtlety is ordering: factors must be printed in non-decreasing order, and multiplicities must be fully expanded, not summarized as powers. For example, 8 = 2^3 must print as `2 2 2`, not `2^3`.

## Approaches

The brute-force approach iterates over all integers from 2 to _n_, testing divisibility. Every time a divisor _d_ divides _n_, it is printed, and _n_ is divided by _d_ until it no longer divides. This works because any integer greater than 1 is either prime or can be factored into primes. For small _n_, the number of division attempts is roughly $n$, which is acceptable for $n \le 250$.

The observation that allows for optimization is that no factor greater than $\sqrt{n}$ (except possibly _n_ itself) needs to be considered in repeated trials. Once we have removed all smaller factors, any remaining number must be prime. This lets us loop only up to $\sqrt{n}$ and handle the last leftover number separately. This slightly reduces the number of unnecessary checks while keeping the algorithm simple and readable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted for n ≤ 250 |
| Optimal | O(√n) | O(1) | Accepted and cleaner |

## Algorithm Walkthrough

1. Read the integer _n_ from input. Initialize a variable `num` to store the remaining number as we extract factors.
2. Iterate over all integers `i` starting from 2 up to $\sqrt{n}$. For each `i`, test if it divides `num`.
3. While `i` divides `num`, print `i` and divide `num` by `i`. Continue this loop until `i` no longer divides `num`. This ensures repeated prime factors are printed the correct number of times.
4. After finishing the loop up to $\sqrt{n}$, if `num` is still greater than 1, it must be a prime factor itself, so print `num`.
5. Separate all printed numbers by spaces.

Why it works: Every integer greater than 1 can be uniquely factorized into primes. By iterating up to $\sqrt{n}$ and removing all factors, any number left must be prime, so the algorithm prints each prime factor exactly the correct number of times. The invariant is that at each iteration, `num` equals the product of all remaining unfactored prime components.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
num = n
i = 2
factors = []

while i * i <= num:
    while num % i == 0:
        factors.append(i)
        num //= i
    i += 1

if num > 1:
    factors.append(num)

print(' '.join(map(str, factors)))
```

The solution first reads the integer and initializes `num` to track the remaining part to factor. The outer loop runs over potential divisors up to $\sqrt{num}$, and the inner loop removes all occurrences of the current divisor. We append all found factors to a list to maintain order. The final check for `num > 1` handles the case when the remaining number is prime and larger than $\sqrt{n}$. Joining the factors into a single string ensures correct output formatting.

## Worked Examples

For input `245`:

| i | num | factors |
| --- | --- | --- |
| 2 | 245 | [] |
| 3 | 245 | [] |
| 4 | 245 | [] |
| 5 | 245 | [] |
| 5 | 49 | [5] |
| 5 | 49 | [5] (inner loop ends) |
| 6 | 49 | [5] |
| 7 | 49 | [5] |
| 7 | 7 | [5, 7] |
| 7 | 1 | [5, 7, 7] |

Output is `5 7 7`, as expected. This trace demonstrates correct handling of repeated prime factors and order.

For input `13`:

| i | num | factors |
| --- | --- | --- |
| 2 | 13 | [] |
| 3 | 13 | [] |
| 4 | 13 | [] |
| 5 | 13 | [] |
| num>1 check | 13 | [13] |

Output is `13`, showing that prime numbers greater than $\sqrt{n}$ are correctly handled.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(√n) | Outer loop iterates up to √n, inner loop divides out each factor once. |
| Space | O(log n) | Storing factors; worst case is all 2s, requiring log₂(n) entries. |

With n ≤ 250, √n is at most 16, so the solution runs in negligible time with trivial memory use.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    num = n
    i = 2
    factors = []
    while i * i <= num:
        while num % i == 0:
            factors.append(i)
            num //= i
        i += 1
    if num > 1:
        factors.append(num)
    return ' '.join(map(str, factors))

# provided samples
assert run("245\n") == "5 7 7", "sample 1"

# custom cases
assert run("2\n") == "2", "minimum prime"
assert run("4\n") == "2 2", "perfect square of smallest prime"
assert run("250\n") == "2 5 5 5", "composite with multiple factors"
assert run("13\n") == "13", "prime greater than √n"
assert run("81\n") == "3 3 3 3", "power of a prime"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 | 2 | minimum prime |
| 4 | 2 2 | repeated small prime |
| 250 | 2 5 5 5 | multiple distinct prime factors |
| 13 | 13 | prime greater than √n |
| 81 | 3 3 3 3 | power of a prime handled correctly |

## Edge Cases

The smallest input, `n = 2`, produces a single factor `2`. The algorithm initializes `num = 2`, enters the loop, sees 2*2 > 2 so skips inner loop, then checks `num > 1` and prints `2`. For `n = 49`, the loop correctly removes 7 twice, showing that repeated factors beyond √n are fully expanded. For primes larger than √n, like `n = 13`, the final check ensures the lone prime factor is output. This approach handles all non-obvious scenarios without special branching.
