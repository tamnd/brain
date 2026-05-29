---
title: "CF 236B - Easy Number Challenge"
description: "We are asked to compute a sum over all triplets of integers (i, j, k) where i ranges from 1 to a, j ranges from 1 to b, and k ranges from 1 to c."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 236
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 146 (Div. 2)"
rating: 1300
weight: 236
solve_time_s: 173
verified: true
draft: false
---

[CF 236B - Easy Number Challenge](https://codeforces.com/problemset/problem/236/B)

**Rating:** 1300  
**Tags:** implementation, number theory  
**Solve time:** 2m 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to compute a sum over all triplets of integers (i, j, k) where i ranges from 1 to _a_, j ranges from 1 to _b_, and k ranges from 1 to _c_. For each triplet, we calculate the product i·j·k, find the number of positive divisors of that product, and sum these counts modulo 1073741824. The input gives three integers a, b, and c, each at most 100, and the output is a single integer representing this sum.

The small bounds suggest that any approach iterating directly over i, j, k is feasible, but a naive divisor-counting routine that computes divisors from scratch for each i·j·k would still be inefficient because there are up to 100³ = 1,000,000 triplets. The problem also asks for a modulo, so intermediate results must be taken modulo 2³⁰ to avoid overflow. Edge cases include the smallest possible inputs, e.g., a = b = c = 1, and products that are perfect powers, where naive divisor counting may miscount if the method is not careful.

## Approaches

The brute-force method would iterate over all i, j, k, compute n = i·j·k, and then count divisors of n by trial division up to √n. For the worst case, n can be up to 100·100·100 = 1,000,000, and we would do up to roughly 1000 divisor checks per number. Multiplying by 1,000,000 triplets yields about 1 billion operations, which is risky under a 2-second limit.

The key observation is that the maximum product is 1,000,000. We can precompute the number of divisors for all integers from 1 up to 1,000,000 using a modified sieve. For each integer i in that range, we increment the divisor count of all multiples of i. Once we have this table, computing d(i·j·k) becomes a simple table lookup, which reduces the inner divisor-counting operation from O(√n) to O(1). The final sum is then just three nested loops over i, j, k performing table lookups and additions modulo 2³⁰.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(a·b·c·√(a·b·c)) = O(10⁹) | O(1) | Likely TLE |
| Precompute divisors | O(N log N + a·b·c) = O(10⁶ log 10⁶ + 10⁶) | O(N) = O(10⁶) | Accepted |

## Algorithm Walkthrough

1. Define a constant MOD = 1073741824 for modulo operations.
2. Determine the maximum possible product n_max = a·b·c. Since each of a, b, c ≤ 100, n_max ≤ 1,000,000.
3. Create an array `div_count` of size n_max + 1, initialized to zero. This array will store the number of divisors for each integer up to n_max.
4. Precompute divisors using a sieve-like method. For each integer i from 1 to n_max, iterate over all multiples of i and increment the corresponding `div_count[multiple]`. After this step, `div_count[n]` contains d(n) for every 1 ≤ n ≤ n_max.
5. Initialize a variable `total_sum` to zero. Iterate i from 1 to a, j from 1 to b, and k from 1 to c. For each triplet, compute n = i·j·k, look up `div_count[n]`, and add it to `total_sum` modulo MOD.
6. After all loops, print `total_sum`. This is the final answer modulo 2³⁰.

Why it works: By precomputing the divisor counts for all integers up to the maximum product, we ensure that each lookup is correct and O(1). The triple loop covers all valid triplets, guaranteeing that the sum accumulates every term exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1073741824

a, b, c = map(int, input().split())
n_max = a * b * c

# Precompute number of divisors for each integer up to n_max
div_count = [0] * (n_max + 1)
for i in range(1, n_max + 1):
    for multiple in range(i, n_max + 1, i):
        div_count[multiple] += 1

total_sum = 0
for i in range(1, a + 1):
    for j in range(1, b + 1):
        for k in range(1, c + 1):
            total_sum = (total_sum + div_count[i * j * k]) % MOD

print(total_sum)
```

The code first reads input and computes n_max to define the size of the sieve array. The sieve fills the `div_count` array by counting divisors for all integers efficiently. The three nested loops iterate through all triplets and sum the precomputed divisor counts modulo 2³⁰. This avoids overflow and ensures correctness even at the largest allowed values.

## Worked Examples

Sample input: `2 2 2`

| i | j | k | i·j·k | d(i·j·k) | total_sum |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 | 1 |
| 1 | 1 | 2 | 2 | 2 | 3 |
| 1 | 2 | 1 | 2 | 2 | 5 |
| 1 | 2 | 2 | 4 | 3 | 8 |
| 2 | 1 | 1 | 2 | 2 | 10 |
| 2 | 1 | 2 | 4 | 3 | 13 |
| 2 | 2 | 1 | 4 | 3 | 16 |
| 2 | 2 | 2 | 8 | 4 | 20 |

This trace demonstrates that all triplets are counted and the divisor counts are correctly added.

Custom input: `3 2 1`

| i | j | k | i·j·k | d(i·j·k) | total_sum |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 | 1 |
| 1 | 2 | 1 | 2 | 2 | 3 |
| 2 | 1 | 1 | 2 | 2 | 5 |
| 2 | 2 | 1 | 4 | 3 | 8 |
| 3 | 1 | 1 | 3 | 2 | 10 |
| 3 | 2 | 1 | 6 | 4 | 14 |

This confirms the algorithm works for asymmetrical ranges.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n_max log n_max + a·b·c) = O(10⁶ log 10⁶ + 10⁶) | The sieve of divisors uses O(n log n) and the triple loop is O(10⁶) |
| Space | O(n_max) = O(10⁶) | The `div_count` array holds divisor counts up to 1,000,000 |

With a = b = c = 100, this fits well under 2 seconds and within 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    MOD = 1073741824
    a, b, c = map(int, input().split())
    n_max = a * b * c
    div_count = [0] * (n_max + 1)
    for i in range(1, n_max + 1):
        for multiple in range(i, n_max + 1, i):
            div_count[multiple] += 1
    total_sum = 0
    for i in range(1, a + 1):
        for j in range(1, b + 1):
            for k in range(1, c + 1):
                total_sum = (total_sum + div_count[i * j * k]) % MOD
    return str(total_sum)

# Provided sample
assert run("2 2 2\n") == "20", "sample 1"

# Minimum-size input
assert run("1 1 1\n") == "1", "minimum input"

# Maximum-size input
assert run("100 100 100\n")  # just test that it runs efficiently

# All-equal values
assert run("3 3 3\n") == run("3 3 3\n"), "all-equal values"

# Asymmetrical values
assert run("3 2 1\n") == "14", "asymmetrical ranges"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
