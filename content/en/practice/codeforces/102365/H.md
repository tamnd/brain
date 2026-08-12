---
title: "CF 102365H - Ancient Wisdom"
description: "Let David's age be (d), Aram's age be (a), and let the given integer be (C). The conversation tells us that cubing David's age and multiplying by (C) produces exactly Aram's age squared: [ C d^3 = a^2. ] Both ages are positive integers."
date: "2026-08-12T23:56:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102365
codeforces_index: "H"
codeforces_contest_name: "UBC Programming Contest 2019 (UBCPC 2019)"
rating: 0
weight: 102365
solve_time_s: 85
verified: true
draft: false
---

[CF 102365H - Ancient Wisdom](https://codeforces.com/problemset/problem/102365/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

Let David's age be (d), Aram's age be (a), and let the given integer be (C). The conversation tells us that cubing David's age and multiplying by (C) produces exactly Aram's age squared:

[
C d^3 = a^2.
]

Both ages are positive integers. We need the smallest possible value of (d) for the given (C).

The key difficulty is that (C) can be as large as (2^{63}-1), roughly (9.2\cdot10^{18}). A direct search over possible ages is impossible, and even ordinary trial division up to (\sqrt C) can require about (2^{31}) divisions in the worst case. The one second limit rules out anything remotely close to a billion iterations, so the factorization itself has to be substantially faster than trial division.

The equation is controlled entirely by prime exponents. Suppose

[
C=\prod p_i^{e_i}
]

and

[
d=\prod p_i^{f_i}.
]

Then the exponent of (p_i) in (Cd^3) is

[
e_i+3f_i.
]

For (Cd^3) to be a perfect square, every such exponent must be even. Since (3) is odd, this means

[
e_i+f_i\equiv0\pmod2,
]

so (f_i) must have the same parity as (e_i). The smallest possible choice is consequently (f_i=1) when (e_i) is odd and (f_i=0) when (e_i) is even.

Thus the answer is the product of exactly those prime factors of (C) whose exponents are odd. This is the squarefree kernel of (C).

Several edge cases are easy to mishandle. For input `1`, the factorization has no prime factors with odd exponent, so the answer is `1`. A brute-force implementation that starts searching from age `2` would incorrectly reject the valid minimum.

For input `8`, we have (8=2^3). The exponent of (2) is odd, so the answer is `2`. Indeed,

[
8\cdot2^3=64=8^2.
]

An implementation that simply takes the distinct prime factors would also happen to return `2` here, but that idea fails on input `12`. Since (12=2^2\cdot3), only the exponent of (3) is odd, so the answer is `3`. Using all distinct prime factors would incorrectly produce `6`.

A second subtle case is a large prime. If (C) itself is prime, its only exponent is (1), so the answer is (C). An implementation based on trial division up to (\sqrt C) can spend billions of iterations proving that such a number is prime.

## Approaches

The most direct approach is to try David's ages starting from (1), compute (Cd^3), and check whether the result is a perfect square. This is correct because the first successful (d) is exactly the minimum age. However, there is no useful small upper bound on the answer. In particular, when (C) is a large prime, the answer itself is approximately (9\cdot10^{18}), so searching through candidate ages is hopeless.

We can instead reason about prime exponents. For every prime (p), the exponent in (Cd^3) has to be even. If (p) appears an odd number of times in (C), we need one copy of (p) in (d). If (p) appears an even number of times, we need no copy. Adding more copies only makes (d) larger and cannot help minimize it.

The problem has therefore been reduced to finding the parity of the exponent of every prime dividing (C). Factoring (C) by trial division would still be too slow because (C) can approach (2^{63}). The appropriate tool for arbitrary 64-bit integers is deterministic Miller-Rabin primality testing combined with Pollard-Rho factorization.

Miller-Rabin lets us quickly recognize prime factors, while Pollard-Rho finds a nontrivial factor of a composite number without scanning every possible divisor. For 64-bit inputs, a fixed set of Miller-Rabin bases makes the primality test deterministic. After recursively factoring (C), we count the occurrences of each prime and multiply the ones occurring an odd number of times.

The brute-force method works because every possible age can be tested directly, but it fails because the answer can itself be enormous. The exponent observation reduces the mathematical problem to factorization, and Pollard-Rho reduces that factorization to a practical amount of work for a 63-bit integer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over ages | (O(d)) | (O(1)) | Too slow |
| Trial division | (O(\sqrt C)) | (O(1)) | Too slow for (C\approx2^{63}) |
| Miller-Rabin + Pollard-Rho | Expected sub-(\sqrt C), practical for 63-bit integers | (O(\log C)) recursion | Accepted |

## Algorithm Walkthrough

1. Read (C). If (C=1), immediately return `1`, because (1\cdot1^3=1^2).
2. Use deterministic Miller-Rabin to determine whether a number is prime. For values below (2^{64}), the bases (2,325,9375,28178,450775,9780504,1795265022) are sufficient for a deterministic test.
3. Use Pollard-Rho to find a nontrivial divisor of every composite number. If the current number is prime, store it. Otherwise, split it into the divisor returned by Pollard-Rho and the corresponding quotient, then factor both recursively.
4. Count how many times every prime occurs in the factorization of (C). The parity is all that matters. For example, if the factorization contains (2^4), the four copies of (2) cancel from the requirement because the exponent is already even. If it contains (7^3), one copy of (7) must be included in David's age.
5. Multiply every prime whose exponent is odd. Call this product (d). This is the smallest possible David age because every prime with odd exponent in (C) must occur at least once in (d), while primes with even exponent do not need to occur at all.
6. Print (d).

### Why it works

Consider any prime (p), with exponent (e) in (C) and exponent (f) in David's age. Its exponent in (Cd^3) is (e+3f). Since a perfect square has only even prime exponents, we need (e+3f) to be even. Because (3) is odd, this is equivalent to (e+f) being even. Hence (f) must have the same parity as (e).

When (e) is even, the smallest valid (f) is (0). When (e) is odd, the smallest valid (f) is (1). These choices are independent for every prime, so their product is the globally smallest possible age. The factorization phase finds exactly these exponents, and the final multiplication constructs precisely that minimum.

## Python Solution

```python
import sys
import random
import math

input = sys.stdin.readline

def is_prime(n):
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

    bases = (
        2,
        325,
        9375,
        28178,
        450775,
        9780504,
        1795265022,
    )

    for a in bases:
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
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n

                g = math.gcd(q, n)
                k += m

            r <<= 1

        if g == n:
            while True:
                ys = (ys * ys + c) % n
                g = math.gcd(abs(x - ys), n)
                if g > 1:
                    break

        if g != n:
            return g

def factor(n, result):
    if n == 1:
        return

    if is_prime(n):
        result.append(n)
        return

    d = pollard_rho(n)
    factor(d, result)
    factor(n // d, result)

def solve():
    c = int(input())

    if c == 1:
        print(1)
        return

    factors = []
    factor(c, factors)
    factors.sort()

    answer = 1
    i = 0

    while i < len(factors):
        j = i + 1
        while j < len(factors) and factors[j] == factors[i]:
            j += 1

        if (j - i) & 1:
            answer *= factors[i]

        i = j

    print(answer)

if __name__ == "__main__":
    solve()
```

The `is_prime` function first removes a collection of tiny prime cases. This makes common small factors cheap to process and also avoids unnecessary Miller-Rabin work.

The remaining primality test writes (n-1) as (d2^s) with (d) odd. Each Miller-Rabin base checks whether the number behaves like a prime under modular exponentiation. The seven fixed bases used here are a deterministic set for all integers below (2^{64}), which covers the entire input range.

The `pollard_rho` function searches for a factor using the pseudorandom recurrence

[
x_{i+1}=x_i^2+c\pmod n.
]

The gcd of differences between two sequences can reveal a factor of (n). The implementation uses Brent's batching variant, which reduces the number of expensive gcd calls compared with a straightforward Pollard-Rho loop.

The recursive `factor` function has a simple stopping condition. A prime is appended immediately. A composite number is split into two smaller numbers and both are factored recursively. Since every recursive branch decreases the number being factored, the recursion terminates.

After sorting the factors, equal primes form contiguous groups. The code counts each group and multiplies the prime into the answer exactly when its count is odd. Sorting is convenient here because it avoids maintaining a separate dictionary and makes the parity calculation straightforward.

Python integers have arbitrary precision, so there is no overflow when computing the final answer or intermediate modular products. The modular multiplications inside Pollard-Rho are also safe because Python automatically expands integer storage.

## Worked Examples

The original statement as provided does not contain concrete sample input and output values, so the following traces use two small inputs that exercise different exponent patterns.

For (C=12), the factorization is (2^2\cdot3). The exponent of (2) is even, while the exponent of (3) is odd.

| Stage | Factors found | Current prime | Count | Answer |
| --- | --- | --- | --- | --- |
| Start | none | none | none | 1 |
| Factorization | 2, 2, 3 | none | none | 1 |
| Group 2 | 2, 2, 3 | 2 | 2 | 1 |
| Group 3 | 2, 2, 3 | 3 | 1 | 3 |
| Finish | 2, 2, 3 | none | none | 3 |

The resulting age is `3`. Checking the original equation gives (12\cdot3^3=324=18^2). The trace demonstrates why using distinct prime factors would be incorrect, since the repeated factor (2^2) contributes nothing to the answer.

For (C=72), we have

[
72=2^3\cdot3^2.
]

Only the exponent of (2) is odd.

| Stage | Factors found | Current prime | Count | Answer |
| --- | --- | --- | --- | --- |
| Start | none | none | none | 1 |
| Factorization | 2, 2, 2, 3, 3 | none | none | 1 |
| Group 2 | 2, 2, 2, 3, 3 | 2 | 3 | 2 |
| Group 3 | 2, 2, 2, 3, 3 | 3 | 2 | 2 |
| Finish | 2, 2, 2, 3, 3 | none | none | 2 |

The answer is `2`, because (72\cdot2^3=576=24^2). The trace confirms that an odd exponent contributes exactly one copy of its prime, regardless of whether that exponent is (1), (3), (5), or larger.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | Expected sub-(\sqrt C), practical for 63-bit integers | Miller-Rabin performs a constant number of modular exponentiations, while Pollard-Rho finds factors using a randomized sequence |
| Space | (O(\log C)) | The factorization recursion has logarithmic depth, and there are at most (O(\log C)) prime factors counted with multiplicity |

The crucial difference from trial division is that the algorithm never scans all integers up to (\sqrt C). Since (C<2^{63}), deterministic Miller-Rabin handles primality reliably, and Pollard-Rho is designed precisely for factoring integers of this size. The memory usage is tiny compared with the 1024 MB limit.

## Test Cases

The statement does not provide actual sample values, so the test suite below uses the same two constructed examples from the worked traces plus boundary and large-value cases.

```python
# helper: run solution on input string, return output string
import sys
import io
import random
import math

def is_prime(n):
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

    bases = (
        2,
        325,
        9375,
        28178,
        450775,
        9780504,
        1795265022,
    )

    for a in bases:
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

                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n

                g = math.gcd(q, n)
                k += m

            r <<= 1

        if g == n:
            while True:
                ys = (ys * ys + c) % n
                g = math.gcd(abs(x - ys), n)
                if g > 1:
                    break

        if g != n:
            return g

def factor(n, result):
    if n == 1:
        return

    if is_prime(n):
        result.append(n)
        return

    d = pollard_rho(n)
    factor(d, result)
    factor(n // d, result)

def solve_value(c):
    if c == 1:
        return 1

    factors = []
    factor(c, factors)
    factors.sort()

    answer = 1
    i = 0

    while i < len(factors):
        j = i + 1
        while j < len(factors) and factors[j] == factors[i]:
            j += 1

        if (j - i) & 1:
            answer *= factors[i]

        i = j

    return answer

def run(inp: str) -> str:
    return str(solve_value(int(inp.strip()))) + "\n"

# constructed samples
assert run("12") == "3\n", "sample-like case 1"
assert run("72") == "2\n", "sample-like case 2"

# minimum input
assert run("1") == "1\n", "C = 1"

# all prime exponents even
assert run("36") == "1\n", "36 = 2^2 * 3^2"

# all distinct prime exponents are odd
assert run("30") == "30\n", "30 = 2 * 3 * 5"

# boundary near 2^63
assert run("9223372036854775807") == "188232082384791343\n", "2^63 - 1"

# large power with an even exponent
assert run("4611686018427387904") == "1\n", "2^62"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Smallest possible input and empty odd-exponent factor set |
| `36` | `1` | Every prime exponent is even |
| `30` | `30` | Several different primes all have odd exponents |
| `9223372036854775807` | `188232082384791343` | Large 63-bit boundary value and nontrivial factorization |
| `4611686018427387904` | `1` | Very large power with an even prime exponent |

## Edge Cases

For (C=1), the input is `1`. There are no prime factors at all, so the product of primes with odd exponent is the empty product, which is `1`. The algorithm handles this before calling Pollard-Rho and prints `1`.

For (C=12), the factorization is (2^2\cdot3). The factorization phase produces `2, 2, 3`. The group containing two copies of `2` has even size, so `2` is excluded. The group containing one copy of `3` has odd size, so `3` is included. The output is `3`.

For (C=8), the factorization is (2^3). The single group has odd size, so the answer becomes `2`. The resulting equation is (8\cdot2^3=64=8^2). This catches the common mistake of treating the answer as something based on the numerical size of (C) rather than the parity of its prime exponents.

For the large boundary input `9223372036854775807`, which is (2^{63}-1), the factorization is

[
7^2\cdot73\cdot127\cdot337\cdot92737\cdot649657.
]

The exponent of `7` is even, while every other displayed exponent is odd. The algorithm consequently removes the factor (7^2) and returns

[
73\cdot127\cdot337\cdot92737\cdot649657
=188232082384791343.
]

This case demonstrates why trial division is unsuitable. Even though the final answer is obtained from a relatively small amount of factorization information, proving the factors by scanning every divisor up to (\sqrt C) would require roughly (3\cdot10^9) candidate divisions, far beyond the intended time budget.
