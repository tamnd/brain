---
title: "CF 102299F - Forbechenko v Rodvsky"
description: "We are given two positive integers (A) and (B), representing the fraction (A/B). We may choose any integer base (beta ge 2), and we want the smallest base in which this fraction has a finite representation after the radix point."
date: "2026-08-13T08:11:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102299
codeforces_index: "F"
codeforces_contest_name: "2019 USP Try-outs"
rating: 0
weight: 102299
solve_time_s: 73
verified: true
draft: false
---

[CF 102299F - Forbechenko v Rodvsky](https://codeforces.com/problemset/problem/102299/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two positive integers (A) and (B), representing the fraction (A/B). We may choose any integer base (\beta \ge 2), and we want the smallest base in which this fraction has a finite representation after the radix point. For example, (1/3) repeats forever in base 10, but it is exactly (0.1_3), so the answer for (A=1,B=3) is (3). The original problem has (1 \le A,B \le 10^{18}), a one-second time limit, and a 256 MB memory limit.

The first useful step is to reduce the fraction. Let (g=\gcd(A,B)), (a=A/g), and (b=B/g). Only the reduced denominator (b) matters. In base (\beta), a rational number has a finite fractional representation exactly when its reduced denominator divides some power of (\beta). If (b) has prime factorization

[
b=p_1^{e_1}p_2^{e_2}\cdots p_k^{e_k},
]

then (b\mid\beta^t) for some (t) precisely when every (p_i) divides (\beta). The exponents (e_i) do not matter, because once (p_i\mid\beta), arbitrarily high powers of (p_i) divide sufficiently large powers of (\beta).

Consequently, the smallest possible base is

[
\beta=p_1p_2\cdots p_k,
]

the product of the distinct prime factors of the reduced denominator. If the denominator becomes (1), the fraction is an integer and is finite in every base, so the answer is (2).

The large bound of (10^{18}) is the real difficulty. Iterating through all possible bases can require (10^{18}) candidates when the reduced denominator itself is a large prime. Even ordinary trial division of the denominator up to its square root can require about (10^9) divisions, which is far beyond what a one-second solution can afford. The factorization has to use a sublinear integer-factorization algorithm.

Several edge cases are easy to mishandle. For input `1 1`, the reduced denominator is (1), so the correct output is `2`. A solution that always returns the product of discovered prime factors can accidentally return (1), which is not a valid base.

For input `2 4`, the fraction reduces to (1/2), so the answer is `2`. A solution that factors (B) before reducing the fraction would still happen to work here, but the distinction becomes meaningful for inputs such as `6 15`: the reduced fraction is (2/5), so the answer is `5`, not the product of the factors of the unreduced denominator combined with irrelevant factors from the numerator.

For input `1 12`, the denominator is (2^2\cdot3). The answer is `6`, not `12`. The exponent of a prime does not need to appear in the base. A careless solution that constructs the entire denominator rather than its radical would produce the wrong answer.

For input `1 3`, the answer is `3`. This catches implementations that only check familiar bases such as (2, 10), or that confuse finite decimal representation with finite representation in some arbitrary base.

## Approaches

A direct approach is to try bases in increasing order. For each candidate (\beta), reduce the current denominator by every factor that also divides (\beta). If the denominator can eventually be reduced to (1), the fraction has a finite representation in that base. This is correct because the process is checking exactly whether every prime factor of the denominator occurs in the candidate base.

The problem is the number of candidates. Consider (A=1) and (B=p), where (p) is a large prime close to (10^{18}). Every base from (2) through (p-1) fails, while (p) succeeds. That means the brute force can perform roughly (10^{18}) candidate checks. Even if each check took only a few machine operations, this is completely infeasible.

A more mathematical naive solution is to factor the reduced denominator by trying every integer from (2) through (\sqrt b). This is much better than trying bases, but for (b) near (10^{18}), the loop still reaches about (10^9) iterations. A one-second limit rules this out as well.

The key observation is that we do not need the full prime factorization with exponents. We only need the distinct prime factors. However, finding those distinct factors for an arbitrary 64-bit integer is still an integer-factorization problem. The appropriate tool here is Pollard's Rho factorization combined with deterministic Miller-Rabin primality testing.

Miller-Rabin quickly tells us whether a remaining number is prime. If it is composite, Pollard's Rho finds a nontrivial factor much faster than trial division. We recursively factor both pieces and multiply each distinct prime exactly once.

The brute force works because a base is valid exactly when it contains every prime factor of the denominator. It fails because discovering the first valid base may require checking essentially the whole (10^{18}) range. The observation that only the distinct prime factors matter lets us replace the search over bases with one factorization of a single 64-bit integer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(B\log B)) in the worst case | (O(1)) | Too slow |
| Trial Division | (O(\sqrt B)) divisions | (O(1)) | Too slow |
| Pollard Rho + Miller-Rabin | Expected roughly (O(B^{1/4})) factorization work for hard semiprimes | (O(\log B)) recursion | Accepted |

## Algorithm Walkthrough

1. Compute (g=\gcd(A,B)) and replace (B) by (B/g). This gives the denominator of the fraction in lowest terms, which is the only part relevant to whether the representation terminates.
2. If the reduced denominator is (1), print `2`. The fraction is an integer, so it has a finite representation in every base, and (2) is the smallest allowed base.
3. Factor the reduced denominator using Miller-Rabin and Pollard's Rho. Miller-Rabin handles prime numbers immediately, while Pollard's Rho supplies a proper divisor whenever the current number is composite.
4. Collect the distinct prime factors. If a factor appears repeatedly, such as (2^5), store (2) only once. The base only needs to contain the prime itself, not its full exponent.
5. Multiply all distinct prime factors together and print the result. This product is divisible by every prime factor of the reduced denominator, and no smaller positive integer can be divisible by all of them simultaneously.

### Why it works

Let the reduced fraction be (a/b). A finite base-(\beta) fractional representation with (k) digits has the form (x/\beta^k) for some integer (x), so (a/b=x/\beta^k), which implies (b\mid\beta^k). Conversely, if (b\mid\beta^k), then (a/b) can be written with denominator (\beta^k), giving a finite representation. Thus the problem is exactly to find the smallest (\beta) whose prime factors include every prime factor of (b). The product of those distinct primes is the smallest such integer, so the algorithm's result is optimal.

## Python Solution

```python
import sys
import math
import random

input = sys.stdin.readline

# Deterministic for every 64-bit integer.
MR_BASES = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)

def is_prime(n: int) -> bool:
    if n < 2:
        return False

    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small_primes:
        if n % p == 0:
            return n == p

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    for a in MR_BASES:
        if a % n == 0:
            continue

        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False

    return True

def pollard_rho(n: int) -> int:
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3

    while True:
        y = random.randrange(1, n - 1)
        c = random.randrange(1, n - 1)
        m = 128

        g = 1
        r = 1
        q = 1

        while g == 1:
            x = y

            for _ in range(r):
                y = (y * y + c) % n

            k = 0
            while k < r and g == 1:
                ys = y
                limit = min(m, r - k)

                for _ in range(limit):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n

                g = math.gcd(q, n)
                k += limit

            r <<= 1

        if g == n:
            while True:
                ys = (ys * ys + c) % n
                g = math.gcd(abs(x - ys), n)
                if g > 1:
                    break

        if g != n:
            return g

def factor(n: int, factors: list[int]) -> None:
    if n == 1:
        return

    if is_prime(n):
        factors.append(n)
        return

    d = pollard_rho(n)
    factor(d, factors)
    factor(n // d, factors)

def solve() -> None:
    A, B = map(int, input().split())

    B //= math.gcd(A, B)

    if B == 1:
        print(2)
        return

    factors = []
    factor(B, factors)

    answer = 1
    for p in set(factors):
        answer *= p

    print(answer)

if __name__ == "__main__":
    solve()
```

The first part of the implementation reduces the fraction with `math.gcd`, matching the first algorithm step. Dividing only the denominator is sufficient because we do not need the reduced numerator for the rest of the calculation.

`is_prime` uses the deterministic Miller-Rabin base set that is sufficient for all integers below (2^{64}), which includes the entire input range. Python's arbitrary-precision integers also make the modular multiplication safe without any special 128-bit handling.

`pollard_rho` uses the Brent-style batched variant of Pollard's Rho. The sequence is generated by (f(x)=x^2+c\pmod n). When two generated values become equal modulo an unknown prime factor, their difference has a nontrivial gcd with (n). Computing the gcd after a batch of differences reduces the number of relatively expensive gcd operations.

The variable `q` stores a product of several absolute differences modulo (n). If any one of those differences contains a factor of (n), the gcd of the whole product with (n) can reveal it. If the batch accidentally gives the full number (n), the code falls back to checking the differences one at a time.

The recursive `factor` function stops immediately for primes. Otherwise it splits the number using Pollard's Rho and recursively processes both factors. Repeated factors are allowed in the temporary list because the final `set` removes their multiplicity.

The final multiplication deliberately happens after deduplication. For example, if the denominator is (72=2^3\cdot3^2), the factor list may contain several copies of `2` and `3`, but the answer must be (2\cdot3=6), not (72).

There is no integer-overflow issue in Python. In a C++ implementation, the modular multiplication inside Pollard's Rho needs a 128-bit intermediate type for this input range.

## Worked Examples

For Sample 1, the input is `1 3`. The denominator is already reduced, and `3` is prime.

| Step | Reduced denominator | Prime factors found | Answer |
| --- | --- | --- | --- |
| Reduce fraction | 3 | none | 1 |
| Test primality | 3 | 3 | 1 |
| Build radical | 3 | {3} | 3 |

The answer is `3`. In base (3), the fraction is exactly (0.1_3), so the representation terminates.

For Sample 2, the input is `3 4`. The denominator is (4=2^2).

| Step | Reduced denominator | Prime factors found | Answer |
| --- | --- | --- | --- |
| Reduce fraction | 4 | none | 1 |
| Factor 4 | 4 | 2, 2 | 1 |
| Remove duplicates | 4 | {2} | 1 |
| Build radical | 4 | {2} | 2 |

The answer is `2`. Although the denominator contains (2^2), the base only needs to contain the prime (2). Since (4\mid2^2), the fraction has a finite binary representation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | Expected (O(B^{1/4}\operatorname{polylog}B)) for difficult 64-bit composites | Pollard's Rho finds nontrivial factors substantially faster than trial division, while Miller-Rabin handles primes quickly |
| Space | (O(\log B)) | Recursive factorization depth is logarithmic, and only the factor list is stored |

With (B\le10^{18}), trial division could require around (10^9) iterations, whereas Pollard's Rho is designed for exactly this 64-bit factorization range. The algorithm also performs only a logarithmic amount of recursion and uses very little memory, so it fits the stated 256 MB memory limit and is suitable for the one-second target with an optimized implementation.

## Test Cases

```python
# This test harness contains the same algorithm as the submitted solution.
import sys
import io
import math
import random

MR_BASES = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)

def is_prime(n):
    if n < 2:
        return False

    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    for a in MR_BASES:
        if a % n == 0:
            continue

        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False

    return True

def pollard_rho(n):
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3

    while True:
        y = random.randrange(1, n - 1)
        c = random.randrange(1, n - 1)
        m = 128

        g = 1
        r = 1
        q = 1

        while g == 1:
            x = y

            for _ in range(r):
                y = (y * y + c) % n

            k = 0
            while k < r and g == 1:
                ys = y
                limit = min(m, r - k)

                for _ in range(limit):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n

                g = math.gcd(q, n)
                k += limit

            r <<= 1

        if g == n:
            while True:
                ys = (ys * ys + c) % n
                g = math.gcd(abs(x - ys), n)
                if g > 1:
                    break

        if g != n:
            return g

def factor(n, factors):
    if n == 1:
        return

    if is_prime(n):
        factors.append(n)
        return

    d = pollard_rho(n)
    factor(d, factors)
    factor(n // d, factors)

def solve_data(inp):
    A, B = map(int, inp.split())

    B //= math.gcd(A, B)

    if B == 1:
        return "2\n"

    factors = []
    factor(B, factors)

    ans = 1
    for p in set(factors):
        ans *= p

    return str(ans) + "\n"

def run(inp: str) -> str:
    return solve_data(inp)

# Provided samples
assert run("1 3\n") == "3\n", "sample 1"
assert run("3 4\n") == "2\n", "sample 2"

# Minimum-size input
assert run("1 1\n") == "2\n", "integer fraction"

# All factors have powers, so only distinct primes matter
assert run("1 12\n") == "6\n", "radical of 12"

# Numerator and denominator must be reduced first
assert run("6 15\n") == "5\n", "reduction by gcd"

# Maximum-size denominator from the stated range
assert run("1 1000000000000000000\n") == "10\n", "maximum-size denominator"

# Large all-equal values, again producing an integer
assert run("1000000000000000000 1000000000000000000\n") == "2\n", "large equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `2` | Minimum input and denominator equal to (1) |
| `1 12` | `6` | Repeated prime factors must not be multiplied repeatedly |
| `6 15` | `5` | Reduction by the gcd must happen before factorization |
| `1 1000000000000000000` | `10` | Maximum-size denominator and large composite factorization |
| `1000000000000000000 1000000000000000000` | `2` | Large equal numerator and denominator |

## Edge Cases

For `1 1`, the algorithm computes (g=1), leaving the denominator as (1). It immediately returns `2`. No factorization is attempted, because there are no prime factors to include in the base.

For `2 4`, the gcd is (2), so the reduced denominator becomes (2). Miller-Rabin recognizes it as prime, and the radical is (2). The output is `2`. This demonstrates why the factorization must use the reduced denominator rather than blindly using the original denominator.

For `6 15`, the gcd is (3), giving the reduced fraction (2/5). The only prime factor of the reduced denominator is (5), so the output is `5`. The factors of the numerator have no effect on the answer.

For `1 12`, the denominator factors as (2^2\cdot3). The algorithm may discover the factors as `2, 2, 3`, but `set(factors)` changes them to `{2,3}` before multiplication. The answer is `6`. A base of (6) works because (12\mid6^2).

For `1 3`, the denominator itself is a prime. Miller-Rabin identifies `3` immediately, so Pollard's Rho is unnecessary. The answer is `3`, which also shows why the smallest valid base is not restricted to a power of two or ten.

For `1 1000000000000000000`, the denominator is

[
10^{18}=2^{18}\cdot5^{18}.
]

Only the distinct primes (2) and (5) matter, so the answer is `10`. This case exercises both the large-integer arithmetic and the distinction between prime exponents and distinct prime factors.

For equal large values such as `1000000000000000000 1000000000000000000`, reduction produces denominator (1), so the algorithm returns `2` immediately. This avoids unnecessary factorization of a large integer and confirms that an integer fraction is valid in the smallest possible base.
