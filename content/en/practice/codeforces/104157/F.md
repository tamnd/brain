---
title: "CF 104157F - Toilet Orders"
description: "We are given two large integers per test case, representing available counts of two complementary parts. From these counts, Thomas effectively produces a number of complete pairs equal to the greatest common divisor of the two values."
date: "2026-07-02T01:15:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104157
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 01-27-23 Div. 2 (Beginner)"
rating: 0
weight: 104157
solve_time_s: 79
verified: false
draft: false
---

[CF 104157F - Toilet Orders](https://codeforces.com/problemset/problem/104157/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two large integers per test case, representing available counts of two complementary parts. From these counts, Thomas effectively produces a number of complete pairs equal to the greatest common divisor of the two values. That gcd value, call it $g$, is the only quantity we actually care about, because it represents how many full items can be formed consistently from both supplies.

For each test case, once $g$ is determined, the task is not to output $g$ itself, but to express it in prime factor form. We need all distinct primes dividing $g$, sorted increasingly, and for each such prime we must output how many times it appears in the factorization.

The constraints are small in number of test cases, but the values themselves are large up to $10^{12}$. That immediately rules out any approach that repeatedly enumerates candidates up to $g$ or performs trial division up to $g$. Even a naive factorization up to $10^{12}$ per test case would be too slow if repeated worst case 100 times.

The main computational structure is therefore clear: we need to compute gcd efficiently, and then factor a number up to $10^{12}$ efficiently.

A few edge cases matter. If $b$ and $l$ are coprime, then $g = 1$, and we must print only the terminating marker for that test case with no primes before it. If $g$ is prime, we must output exactly one line containing that prime with multiplicity 1. A common mistake is forgetting that multiplicity refers to exponent in the factorization of $g$, not of the original inputs.

## Approaches

The naive approach computes $g = \gcd(b, l)$, then factorizes it by checking all integers from 2 up to $\sqrt{g}$ and dividing repeatedly. This is correct because every composite number has at least one prime factor at most its square root. However, in the worst case $g \approx 10^{12}$, so $\sqrt{g} \approx 10^6$. Doing up to a million trial divisions per test case and repeating this for up to 100 cases gives roughly $10^8$ operations, and each division step is not trivial in Python. This is close to the boundary and risks TLE.

The key improvement comes from noticing that factorization only needs primes, not all integers. We can precompute all primes up to $10^6$ once using a sieve, then factor each $g$ by dividing only by these primes. Since any composite number up to $10^{12}$ has at least one prime factor ≤ $10^6$, this is sufficient. After removing small primes, if the remaining value is greater than 1, it is itself a prime.

This reduces each test case from $O(\sqrt{g})$ checks to roughly $O(\pi(\sqrt{g}))$, which is about 78,000 primes, but in practice much less due to early reduction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Trial Division | $O(T \sqrt{g})$ | $O(1)$ | Too slow |
| Sieve + Prime Factorization | $O(\sqrt{N} + T \cdot \pi(\sqrt{g}))$ | $O(\sqrt{N})$ | Accepted |

## Algorithm Walkthrough

### 1. Precompute primes up to $10^6$

We build a sieve of Eratosthenes. This gives us all primes needed to factor any number up to $10^{12}$, since any composite number in that range must have a prime factor at most $10^6$.

### 2. Process each test case

For each pair $(b, l)$, compute $g = \gcd(b, l)$. This step is fast, $O(\log \min(b,l))$, and dominates nothing.

### 3. Factor $g$ using precomputed primes

We iterate through primes in increasing order. For each prime $p$, we divide $g$ as long as $p \mid g$, counting how many times this happens.

Each successful division shrinks $g$, so later checks become cheaper. This is why we stop early when $p^2 > g$.

### 4. Handle leftover value

If after processing all primes up to $\sqrt{g}$, the remaining $g > 1$, then it is prime and contributes one final factor with exponent 1.

### 5. Output formatting

We print each prime factor and its exponent in increasing order. After finishing a test case, we print a single line containing 0.

### Why it works

The correctness rests on the uniqueness of prime factorization and the fact that every composite number has a prime divisor not exceeding its square root. The sieve guarantees we test all possible primes in order, so every factor is fully extracted exactly once. Since each division removes all occurrences of a prime before moving on, multiplicities are counted precisely, and ordering is preserved by iterating primes in increasing order.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

MAX = 10**6

is_prime = [True] * (MAX + 1)
is_prime[0] = is_prime[1] = False
primes = []

for i in range(2, MAX + 1):
    if is_prime[i]:
        primes.append(i)
        for j in range(i * i, MAX + 1, i):
            is_prime[j] = False

def factorize(n):
    res = []
    for p in primes:
        if p * p > n:
            break
        if n % p == 0:
            cnt = 0
            while n % p == 0:
                n //= p
                cnt += 1
            res.append((p, cnt))
    if n > 1:
        res.append((n, 1))
    return res

t = int(input())
out = []

for _ in range(t):
    b, l = map(int, input().split())
    g = math.gcd(b, l)

    if g == 1:
        out.append("0")
        continue

    factors = factorize(g)
    for p, c in factors:
        out.append(f"{p} {c}")
    out.append("0")

sys.stdout.write("\n".join(out))
```

The sieve is built once at the start and reused across all test cases. The factorization routine carefully stops once $p^2 > n$, which prevents unnecessary iterations once the remaining number is already prime.

The gcd computation ensures we only ever factor a single reduced number per test case, not two large inputs.

The output is accumulated in a list to avoid repeated I/O overhead inside loops, which is important in Python under tight time limits.

## Worked Examples

### Sample 1

Input:

```
360 240
```

We first compute $g = \gcd(360, 240) = 120$.

| Step | Prime $p$ | Current $g$ | Action | Output so far |
| --- | --- | --- | --- | --- |
| 1 | 2 | 120 → 15 | divides 2 three times | (2, 3) |
| 2 | 3 | 15 → 5 | divides once | (3, 1) |
| 3 | 5 | 5 → 1 | divides once | (5, 1) |

Final output:

```
2 3
3 1
5 1
0
```

This confirms correct extraction of all prime multiplicities in increasing order.

### Sample 2

Input:

```
83 24
15 25
```

First pair: $\gcd(83, 24) = 1$

| Step | g | Action | Output |
| --- | --- | --- | --- |
| 1 | 1 | immediate stop | 0 |

Second pair: $\gcd(15, 25) = 5$

| Step | Prime $p$ | Current $g$ | Action | Output |
| --- | --- | --- | --- | --- |
| 1 | 5 | 5 → 1 | divides once | (5, 1) |

Final output:

```
0
5 1
0
```

The first case verifies correct handling of $g = 1$, while the second confirms correct handling of a prime gcd.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\sqrt{N} + T \cdot \pi(\sqrt{g}))$ | sieve up to $10^6$, then trial division by primes only |
| Space | $O(\sqrt{N})$ | sieve and prime list storage |

The sieve cost is paid once and reused across all test cases. Each factorization works on a number up to $10^{12}$, but is reduced quickly through division. With at most 100 test cases, this comfortably fits within limits.

## Test Cases

```python
import sys, io, math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    MAX = 10**6
    is_prime = [True] * (MAX + 1)
    is_prime[0] = is_prime[1] = False
    primes = []
    for i in range(2, MAX + 1):
        if is_prime[i]:
            primes.append(i)
            for j in range(i * i, MAX + 1, i):
                is_prime[j] = False

    def factorize(n):
        res = []
        for p in primes:
            if p * p > n:
                break
            if n % p == 0:
                cnt = 0
                while n % p == 0:
                    n //= p
                    cnt += 1
                res.append((p, cnt))
        if n > 1:
            res.append((n, 1))
        return res

    t = int(input())
    out = []
    for _ in range(t):
        b, l = map(int, input().split())
        g = math.gcd(b, l)
        if g == 1:
            out.append("0")
        else:
            for p, c in factorize(g):
                out.append(f"{p} {c}")
            out.append("0")
    return "\n".join(out) + "\n"

# provided samples
assert run("1\n360 240\n") == "2 3\n3 1\n5 1\n0\n", "sample 1"
assert run("2\n83 24\n15 25\n") == "0\n5 1\n0\n", "sample 2"

# custom cases
assert run("1\n2 2\n") == "2 1\n0\n", "minimum prime power"
assert run("1\n49 49\n") == "7 2\n0\n", "perfect square gcd"
assert run("1\n1000000000000 999999999999\n")[-2:] == "0\n", "large coprime-ish"
assert run("3\n6 9\n10 25\n17 19\n") == "3 1\n0\n5 2\n0\n0\n", "mixed cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 2 | 2 1 0 | smallest non-trivial gcd |
| 49 49 | 7 2 0 | repeated prime exponent handling |
| large pair | ends with 0 | large-number stability |
| mixed cases | multiple patterns | batch correctness |

## Edge Cases

One important edge case is when the gcd is 1. For example, input `83 24` produces $g = 1$. The factorization loop is skipped entirely, and the only required output is a single `0`. The algorithm handles this naturally because the factorization function returns an empty list and the caller directly appends the terminator.

Another edge case is when the gcd is a prime power, such as `49 49`, where $g = 49 = 7^2$. The loop detects divisibility by 7, counts two divisions, and appends `(7, 2)`. Since the reduced value becomes 1, no leftover is appended, preventing duplicate output.

A final subtle case is when the gcd is itself a large prime greater than $10^6$, for example `1000000000039 1000000000039`. In that case no sieve prime divides it, so the loop finishes and the leftover `n > 1` is appended as a single prime factor with exponent 1. This ensures correctness even beyond the sieve range.
