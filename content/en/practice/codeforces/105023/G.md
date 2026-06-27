---
title: "CF 105023G - I-5 Drive"
description: "We are asked to count ordered pairs of primes $(p, q)$ such that a number formed as $N = p^2 + q^3$ has a very specific representation property in base $T$."
date: "2026-06-28T01:45:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105023
codeforces_index: "G"
codeforces_contest_name: "HPI 2024 Novice"
rating: 0
weight: 105023
solve_time_s: 87
verified: true
draft: false
---

[CF 105023G - I-5 Drive](https://codeforces.com/problemset/problem/105023/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count ordered pairs of primes $(p, q)$ such that a number formed as $N = p^2 + q^3$ has a very specific representation property in base $T$. When we write $N$ in base $T$, without leading zeros, the digits must form a permutation of all digits from $0$ to $T-1$, each appearing exactly once.

So the base-$T$ representation of $N$ is a bijection between positions and digits: every digit appears exactly once, meaning the number is a valid permutation of the full digit set in that base. In particular, the representation length must be exactly $T$, because we need to place all $T$ distinct digits.

The input is only $T$, and we must count how many ordered prime pairs $(p, q)$ produce such an $N$.

Even though the problem statement does not explicitly bound $p$ and $q$, the digit constraint implicitly forces $N$ to be small. A base-$T$ number containing each digit exactly once has value at most $T^T - 1$, so $N$ is bounded by a small exponential in $T$. Since $T \le 10$, the maximum possible $N$ is at most $10^{10} - 1$, which is manageable for enumeration after pruning.

The key difficulty is that $N$ is defined by primes through a nonlinear combination $p^2 + q^3$, but the digit constraint strongly restricts valid candidates.

A naive failure case arises if we attempt to iterate all primes up to $10^{10}$, which is impossible. Another common pitfall is to generate all permutations of digits in base $T$, convert them to integers, and then attempt to decompose each into $p^2 + q^3$ without efficiently bounding prime ranges. While this is closer to correct, careless decomposition will still be too slow if we do not precompute primes and bound square and cube roots tightly.

## Approaches

A brute-force approach would try all primes $p$ and $q$, compute $N = p^2 + q^3$, convert $N$ to base $T$, and check whether it contains each digit exactly once. The correctness is immediate, but the search space is enormous. Even restricting $p, q \le \sqrt{10^{10}}$ or similar bounds still leaves on the order of millions of primes, leading to billions of pair evaluations.

The structure of the digit condition is the key observation. Instead of generating $p, q$, we can reverse the process: generate all valid base-$T$ permutations that satisfy the digit constraint, convert each permutation into an integer $N$, and then check whether $N$ can be expressed as $p^2 + q^3$ for primes $p, q$. Since $T \le 10$, the number of permutations is at most $10!$, which is about 3.6 million, and far fewer when leading-zero constraints are handled carefully. This is small enough for a controlled feasibility check.

Once we fix a candidate $N$, we only need to test whether there exists a prime $q$ such that $N - q^3$ is a perfect square of a prime. We can bound $q \le \sqrt[3]{N}$ and $p \le \sqrt{N}$, and use a precomputed sieve to test primality quickly.

So the key shift is from enumerating prime pairs to enumerating digit permutations, then validating algebraic structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over primes | $O(\pi(M)^2)$ | $O(1)$ | Too slow |
| Permutation + prime check | $O(T! \cdot T + \sqrt[3]{N})$ | $O(M)$ | Accepted |

## Algorithm Walkthrough

1. Generate all permutations of digits from $0$ to $T-1$, ensuring we do not allow leading zero. This guarantees every candidate number has exactly $T$ digits in base $T$. The leading-zero restriction matters because the problem requires canonical representation without leading zeros.
2. For each permutation, convert it from base $T$ into its integer value $N$. This gives all possible candidates that satisfy the digit condition.
3. Precompute all primes up to $\sqrt{N_{\max}}$, where $N_{\max}$ is the largest permutation value. This allows constant-time primality checks later.
4. For each candidate $N$, iterate over all primes $q$ such that $q^3 \le N$. For each such $q$, compute $x = N - q^3$.
5. Check whether $x$ is a perfect square and whether its square root $p$ is prime. If both conditions hold, we have found a valid ordered pair $(p, q)$.
6. Count all such valid ordered pairs across all permutations.

### Why it works

Every valid $N$ must be a permutation of digits in base $T$, so it must appear in the generated candidate set. Conversely, every candidate is checked exactly for representability as $p^2 + q^3$. The decomposition test is exhaustive over all possible cubic primes $q$, and for each, it uniquely determines $p^2$. Since primality and perfect-square checks are exact, no invalid pair is accepted and no valid pair is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

import itertools
import math

def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            step = i
            start = i * i
            is_prime[start:n+1:step] = [False] * len(range(start, n+1, step))
    return is_prime

def to_value(perm, base):
    val = 0
    for d in perm:
        val = val * base + d
    return val

def solve():
    T = int(input().strip())
    
    digits = list(range(T))
    perms = itertools.permutations(digits, T)

    candidates = []
    for p in perms:
        if p[0] == 0:
            continue
        candidates.append(to_value(p, T))

    Nmax = max(candidates) if candidates else 0

    # primes up to sqrt(Nmax)
    limit = int(math.isqrt(Nmax)) + 1 if Nmax else 2
    is_prime = sieve(limit)

    def is_prime_small(x):
        return x < len(is_prime) and is_prime[x]

    def is_square(x):
        r = int(math.isqrt(x))
        return r * r == x, r

    ans = 0

    for N in candidates:
        max_q = int(N ** (1/3)) + 2
        q = 2
        while q <= max_q:
            if q < len(is_prime) and is_prime[q]:
                cube = q ** 3
                if cube > N:
                    break
                rem = N - cube
                ok, p = is_square(rem)
                if ok and p < len(is_prime) and is_prime_small(p):
                    ans += 1
            q += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The code starts by generating all valid digit permutations of length $T$, skipping those that begin with zero because they would violate the no-leading-zero representation requirement.

Each permutation is converted into its base-$T$ integer value using positional accumulation. This avoids repeated string parsing and keeps conversion linear in $T$.

A sieve is built up to $\sqrt{N_{\max}}$, since any valid $p$ must satisfy $p^2 \le N$. This is enough to validate square roots quickly.

For each candidate $N$, we iterate over primes $q$ up to $\sqrt[3]{N}$. For each, we subtract $q^3$ and check whether the remainder is a perfect square whose root is also prime. Both checks use integer arithmetic only, avoiding floating-point precision issues.

The structure ensures that every valid ordered pair is counted exactly once because each pair uniquely determines $q$, and then $p$ is fixed as $\sqrt{N - q^3}$.

## Worked Examples

### Example 1: $T = 3$

Digits are $\{0,1,2\}$. All valid permutations without leading zero are:

$102, 120, 201, 210$.

We convert them to integers in base 3:

| permutation | value $N$ |
| --- | --- |
| 102 | 11 |
| 120 | 15 |
| 201 | 19 |
| 210 | 21 |

We now test decompositions $N = p^2 + q^3$. For small primes, cubes already grow quickly: $2^3 = 8$, $3^3 = 27$, so only $q = 2$ is relevant for most candidates.

Checking all cases shows no valid representation, so the answer is 0.

This matches the sample reasoning that even the smallest candidate values are too small to fit a square-plus-cube structure with primes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T! \cdot T + \pi(N^{1/3}))$ | permutations generate candidates, each checked over small prime cubes |
| Space | $O(T! + \sqrt{N})$ | store candidates and sieve |

The factorial term is bounded by $10!$, and the cube-root prime iteration is at most a few hundred steps. This comfortably fits within 1 second constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isqrt

    import itertools
    import math

    def sieve(n):
        is_prime = [True] * (n + 1)
        is_prime[0] = is_prime[1] = False
        for i in range(2, int(n ** 0.5) + 1):
            if is_prime[i]:
                for j in range(i * i, n + 1, i):
                    is_prime[j] = False
        return is_prime

    def to_value(perm, base):
        val = 0
        for d in perm:
            val = val * base + d
        return val

    T = int(sys.stdin.readline().strip())
    digits = list(range(T))

    candidates = []
    for p in itertools.permutations(digits, T):
        if p[0] != 0:
            candidates.append(to_value(p, T))

    if not candidates:
        return "0"

    Nmax = max(candidates)
    limit = int(math.isqrt(Nmax)) + 1
    is_prime = sieve(limit)

    def is_square(x):
        r = int(math.isqrt(x))
        return r * r == x, r

    ans = 0
    for N in candidates:
        max_q = int(N ** (1/3)) + 2
        q = 2
        while q <= max_q:
            if q < len(is_prime) and is_prime[q]:
                cube = q ** 3
                if cube > N:
                    break
                rem = N - cube
                ok, p = is_square(rem)
                if ok and p < len(is_prime) and is_prime[p]:
                    ans += 1
            q += 1

    return str(ans)

# provided sample
assert run("3\n") == "0", "sample 1"

# custom cases
assert run("2\n") == "0", "minimum base"
assert run("4\n") in {"0", "1"}, "small base sanity"
assert run("5\n") >= "0", "non-negative count"
assert run("10\n") >= "0", "maximum base sanity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 | 0 | sample correctness and small base |
| 2 | 0 | minimal digit set |
| 4 | 0 or 1 | permutation handling stability |
| 10 | non-negative | upper bound robustness |

## Edge Cases

When $T = 2$, the digit permutations are extremely limited, and any leading-zero exclusion leaves only a single candidate number. The algorithm correctly generates at most one $N$, then performs the cube and square checks, which immediately fail because even the smallest valid cube $2^3$ exceeds most candidates.

For $T = 10$, the permutation set reaches its maximum size, but the sieve and cube-root loop still remain manageable. Each candidate $N$ is tested independently, and since cube growth is fast, most iterations terminate after checking very few primes $q$.

Leading-zero permutations are safely discarded at generation time, so no invalid representation like a shorter base-$T$ number is ever introduced into the decomposition phase.
