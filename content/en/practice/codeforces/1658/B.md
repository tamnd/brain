---
title: "CF 1658B - Marin and Anti-coprime Permutation"
description: "We are asked to count permutations of length $n$ where the greatest common divisor of the sequence $1 cdot p1, 2 cdot p2, dots, n cdot pn$ is strictly greater than 1. Here $p$ is a permutation of integers from 1 to $n$."
date: "2026-06-10T03:21:42+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1658
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 779 (Div. 2)"
rating: 800
weight: 1658
solve_time_s: 94
verified: true
draft: false
---

[CF 1658B - Marin and Anti-coprime Permutation](https://codeforces.com/problemset/problem/1658/B)

**Rating:** 800  
**Tags:** combinatorics, math, number theory  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count permutations of length $n$ where the greatest common divisor of the sequence $1 \cdot p_1, 2 \cdot p_2, \dots, n \cdot p_n$ is strictly greater than 1. Here $p$ is a permutation of integers from 1 to $n$. In simpler terms, each element is multiplied by its position, and we want all those products to share a common factor larger than 1.

The input consists of multiple test cases, each specifying a single $n$. The output is the number of "beautiful" permutations modulo $998244353$.

The constraints allow $n$ up to 1000 and up to 1000 test cases. A naive solution that generates all permutations would have complexity $O(n!)$, which is infeasible even for $n = 10$. We need an approach that works in roughly $O(n^2)$ or $O(n \log n)$ per test case.

Edge cases that are easy to miss include very small $n$. For $n=1$, the only permutation is $[1]$, which has $\gcd(1) = 1$ and is therefore not beautiful. For $n=2$, the permutation $[2,1]$ works because $\gcd(2,2) = 2 > 1$. These show that we cannot assume any $n > 1$ automatically has a solution.

Another subtlety is that the beautiful permutations often arise when the sequence can be rearranged so that all products are even. This suggests a combinatorial pattern rather than checking every permutation individually.

## Approaches

A brute-force approach would enumerate all $n!$ permutations and compute $\gcd(1\cdot p_1, \dots, n \cdot p_n)$ for each. This is correct in principle because it directly implements the problem statement, but it is hopelessly slow. Even for $n=10$, this requires 3.6 million permutations to check, which multiplied by $n$ operations per $\gcd$ computation is far above the allowed 1-second runtime.

The key insight is that for the $\gcd$ to exceed 1, all numbers must share a common factor. The smallest prime to consider is 2. If we can guarantee all products are even, the $\gcd$ is at least 2. This leads to a simple construction: assign the even numbers to positions that make their product even. By analysis, one can derive a recurrence that counts permutations where the first half of numbers occupy even indices and the second half occupy odd indices, adjusting for $n$ being even or odd. After some combinatorial work, this simplifies to $(n//2)!^2$ modulo $998244353$ for even $n$, and 0 for odd $n$.

The observation relies on the fact that odd positions multiplied by odd numbers give odd products. Therefore, for $n$ odd, at least one product remains odd, giving a $\gcd$ of 1. Only even $n$ allows a full arrangement where all products share a factor of 2.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!·n) | O(n) | Too slow |
| Optimal | O(n + t) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute factorials up to the maximum $n$ modulo $998244353$. This allows $O(1)$ factorial lookups and avoids recomputation for each test case.
2. Read the number of test cases $t$ and iterate through each $n$.
3. For each $n$, check if it is odd. If it is, output 0 because at least one product will be odd and the $\gcd$ will be 1.
4. If $n$ is even, compute the number of beautiful permutations as $(n//2)!^2 \mod 998244353$. This counts ways to assign the lower half of numbers to the odd positions and the upper half to even positions.
5. Print the result for each test case.

Why it works: The invariant is that we maintain the property that all products are even if and only if $n$ is even and numbers are distributed so that each product includes at least one even factor. By squaring the factorial of $n/2$, we account for all valid rearrangements separately for the two halves of the numbers. No other arrangements can produce a greater $\gcd$ because introducing an odd product would force the $\gcd$ down to 1.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
MAX_N = 1000

# Precompute factorials modulo MOD
fact = [1] * (MAX_N + 1)
for i in range(1, MAX_N + 1):
    fact[i] = fact[i-1] * i % MOD

t = int(input())
for _ in range(t):
    n = int(input())
    if n % 2 != 0:
        print(0)
    else:
        half = n // 2
        res = fact[half] * fact[half] % MOD
        print(res)
```

The code first precomputes factorials to avoid repeated computation. For each test case, we handle odd $n$ immediately by printing 0. For even $n$, we compute the product of factorials for each half of the permutation, squaring the factorial because the arrangement of the two halves is independent. Modulo $998244353$ ensures we do not overflow and matches the problem requirements.

## Worked Examples

Sample input `4`:

| n | n%2 | half | fact[half] | result |
| --- | --- | --- | --- | --- |
| 4 | 0 | 2 | 2 | 4 |

Explanation: `n=4` is even. Half is 2. `2! = 2`. Squaring gives 4. There are four beautiful permutations: [2,1,4,3], [2,3,4,1], [4,1,2,3], [4,3,2,1] (up to reordering each half).

Sample input `3`:

| n | n%2 | result |
| --- | --- | --- |
| 3 | 1 | 0 |

Explanation: `n=3` is odd. Any permutation has an odd product somewhere, giving gcd=1. Therefore 0 beautiful permutations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(MAX_N + t) | Precompute factorials once in O(MAX_N), each test case handled in O(1) |
| Space | O(MAX_N) | Store factorials up to 1000 |

Given the constraints, this is efficient. Precomputing factorials ensures constant-time computation per test case. Memory usage is minimal and fits easily within the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    MOD = 998244353
    MAX_N = 1000
    fact = [1] * (MAX_N + 1)
    for i in range(1, MAX_N + 1):
        fact[i] = fact[i-1] * i % MOD
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        if n % 2 != 0:
            out.append("0")
        else:
            half = n // 2
            res = fact[half] * fact[half] % MOD
            out.append(str(res))
    return "\n".join(out)

# Provided samples
assert run("7\n1\n2\n3\n4\n5\n6\n1000\n") == "0\n1\n0\n4\n0\n36\n665702330", "sample 1"

# Custom cases
assert run("2\n10\n11\n") == "14400\n0", "even vs odd n"
assert run("1\n2\n") == "1", "smallest even n"
assert run("1\n1000\n") == "665702330", "largest n"
assert run("1\n1\n") == "0", "smallest odd n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10 | 14400 | Correct counting for even n=10 |
| 11 | 0 | Correctly outputs 0 for odd n=11 |
| 2 | 1 | Minimal even n |
| 1000 | 665702330 | Performance and modular arithmetic correctness for max n |
| 1 | 0 | Minimal odd n |

## Edge Cases

For `n=1`, the algorithm immediately identifies `n%2==1` and outputs 0. This correctly handles the smallest input. For `n=2`, `n%2==0`, half=1, `1!*1! = 1` outputs 1, matching the single beautiful permutation `[2,1]`. For `n=1000`, the precomputed factorials allow us to compute `500!^2 % MOD` efficiently. The algorithm handles odd and even inputs distinctly, so no permutation of odd `n
