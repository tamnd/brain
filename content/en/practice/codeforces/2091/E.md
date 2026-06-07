---
title: "CF 2091E - Interesting Ratio"
description: "We are asked to count pairs of integers $(a, b)$ where $1 le a < b le n$ such that the ratio $F(a, b) = frac{text{lcm}(a, b)}{gcd(a, b)}$ is a prime number."
date: "2026-06-08T05:47:01+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math", "number-theory", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2091
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1013 (Div. 3)"
rating: 1300
weight: 2091
solve_time_s: 72
verified: true
draft: false
---

[CF 2091E - Interesting Ratio](https://codeforces.com/problemset/problem/2091/E)

**Rating:** 1300  
**Tags:** brute force, math, number theory, two pointers  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count pairs of integers $(a, b)$ where $1 \le a < b \le n$ such that the ratio $F(a, b) = \frac{\text{lcm}(a, b)}{\gcd(a, b)}$ is a prime number. The input consists of multiple test cases, each specifying a maximum number $n$, and for each test case we need to output the number of pairs satisfying this condition.

The main insight is that $F(a, b) = \frac{\text{lcm}(a, b)}{\gcd(a, b)} = \frac{a \cdot b / \gcd(a, b)}{\gcd(a, b)} = \frac{a \cdot b}{\gcd(a, b)^2}$. So $F(a, b)$ is always an integer, and we need it to be prime. Since primes are greater than 1, $F(a, b) \ge 2$.

The constraints are significant. $n$ can be as large as $10^7$, and the sum of all $n$ across test cases does not exceed $10^7$. A naive approach that checks all $O(n^2)$ pairs for each test case would require up to $10^{14}$ operations in the worst case, which is far beyond feasible. This indicates we need a solution close to linear time or slightly superlinear with respect to $n$.

Edge cases that can break a careless approach include small $n$ like $n = 2$, where only one pair exists $(1, 2)$, or cases where $a$ is 1, since $F(1, p) = p$ for any prime $p$. Another tricky case is when $b$ is a multiple of $a$; $F(a, b)$ simplifies to $\frac{b}{a}$, so we can generate all interesting ratios by considering multiples of a base integer.

## Approaches

The brute-force approach enumerates all pairs $(a, b)$ with $1 \le a < b \le n$, computes $\gcd(a, b)$, calculates $F(a, b)$, and checks whether it is prime. While this is correct in principle, for $n \sim 10^7$ this approach requires $O(n^2 \log n)$ time because computing $\gcd$ and checking primes are not constant time. This is clearly too slow.

The key observation is to express $b$ as $b = a \cdot k$, where $k > 1$ is an integer. Then $\gcd(a, b) = a$ and $\text{lcm}(a, b) = a \cdot k$, so $F(a, b) = \frac{a \cdot k}{a} / a = k$. Therefore, $F(a, b)$ is prime exactly when $b = a \cdot p$ for some prime $p$. The problem reduces to counting all multiples of each integer $a$ by a prime $p$ such that the product does not exceed $n$.

We can precompute primes up to $n$ using a sieve and then for each $a$ iterate over all primes $p$ with $a \cdot p \le n$. This reduces the complexity to roughly $O(n \log \log n)$ for the sieve plus $O(n \log n)$ for generating pairs, which is feasible given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² log n) | O(1) | Too slow |
| Prime multiples | O(n log log n + n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute all primes up to the maximum $n$ across all test cases using the Sieve of Eratosthenes. This gives us a fast way to check primes and enumerate them.
2. Initialize an array `counts` where `counts[i]` will store the number of interesting ratios for a given $i$.
3. For each integer $a$ from 1 to $n$, iterate over primes $p$ such that $a \cdot p \le n$. Each valid product $b = a \cdot p$ forms a valid pair $(a, b)$, so increment `counts[a * p]`.
4. To handle multiple test cases efficiently, accumulate counts for all integers up to `max_n` and store prefix sums if needed.
5. For each test case with given $n$, sum the contributions from all valid pairs up to $n$ and print the result.

Why it works: By factorizing $b$ as a multiple of $a$, we ensure $\gcd(a, b) = a$, so $F(a, b) = b / a$. This guarantees integer results and allows direct checking for primality. The sieve ensures that all prime factors are considered, and iterating over multiples ensures that all valid pairs are counted exactly once. The constraints $1 \le a < b \le n$ are maintained naturally.

## Python Solution

```python
import sys
input = sys.stdin.readline

# sieve of Eratosthenes
def sieve(max_n):
    is_prime = [True] * (max_n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(max_n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, max_n + 1, i):
                is_prime[j] = False
    primes = [i for i, val in enumerate(is_prime) if val]
    return primes, is_prime

def solve():
    t = int(input())
    ns = [int(input()) for _ in range(t)]
    max_n = max(ns)
    primes, _ = sieve(max_n)
    
    # precompute number of interesting ratios
    counts = [0] * (max_n + 1)
    for p in primes:
        for a in range(1, max_n // p + 1):
            counts[a * p] += 1
    
    # prefix sums
    for i in range(1, max_n + 1):
        counts[i] += counts[i - 1]
    
    for n in ns:
        print(counts[n])

if __name__ == "__main__":
    solve()
```

The sieve generates all primes efficiently. We iterate over each prime and then over all multiples that do not exceed `max_n`. Using a prefix sum array allows us to answer each test case in constant time. Careful attention is paid to boundaries: the loop `a in range(1, max_n // p + 1)` ensures we do not exceed the maximum allowed $b$.

## Worked Examples

Sample input `n = 5`:

| a | primes p | a * p <= 5 | counts[a*p] after this prime |
| --- | --- | --- | --- |
| 1 | 2,3,5 | 2,3,5 | counts[2]=1, counts[3]=1, counts[5]=1 |
| 2 | 2 | 4 | counts[4]=1 |
| 3 | 2 | 6 > 5 | skip |
| 4 | 2 | 8 > 5 | skip |
| 5 | 2 | 10 > 5 | skip |

Prefix sum yields total `counts[5] = 4`.

This confirms the algorithm counts pairs `(1,2)`, `(1,3)`, `(1,5)`, `(2,4)` correctly.

Sample input `n = 10`:

| a | p | a*p <= 10 | pairs counted |
| --- | --- | --- | --- |
| 1 | 2,3,5,7 | 2,3,5,7 | 4 |
| 2 | 2,3,5 | 4,6,10 | 3 more |
| 3 | 2,3 | 6,9 | 2 more |
| 4 | 2 | 8 | 1 more |
| 5 | 2 | 10 | already counted in 2*5? counts separately |
| 6..10 | only products >10 | skipped |  |

Total count = 11, matches expected output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log log n + n log n) | sieve + iterating over primes and multiples |
| Space | O(n) | storing counts and sieve arrays |

This fits comfortably under the 2-second time limit for `n ≤ 10^7` and memory limit of 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples
assert run("4\n5\n10\n34\n10007\n") == "4\n11\n49\n24317"

# minimum-size input
assert run("1\n2\n") == "1"

# maximum-size input (just check it runs)
assert run("1\n10000000\n
```
