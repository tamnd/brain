---
title: "CF 102460M - DivModulo"
description: "We need to compute a special remainder of a binomial coefficient. Given (M), (N), and (D), with (0 le N le M), consider [ C(M,N)=frac{M!}{N!(M-N)!}. ] The DivModulo operation does not simply take this number modulo (D)."
date: "2026-08-08T10:26:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102460
codeforces_index: "M"
codeforces_contest_name: "2019-2020 ICPC Asia Taipei-Hsinchu Regional Contest"
rating: 0
weight: 102460
solve_time_s: 524
verified: true
draft: false
---

[CF 102460M - DivModulo](https://codeforces.com/problemset/problem/102460/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to compute a special remainder of a binomial coefficient. Given (M), (N), and (D), with (0 \le N \le M), consider

[
C(M,N)=\frac{M!}{N!(M-N)!}.
]

The DivModulo operation does not simply take this number modulo (D). Instead, we repeatedly remove a complete factor of (D) while possible. If

[
C(M,N)=X D^h
]

where (D\nmid X), the required answer is (X\bmod D).

This distinction matters whenever the binomial coefficient is divisible by (D). For example, (C(5,2)=10=2\cdot5), so ordinary modulo gives (0), while DivModulo gives (2).

The input size makes direct factorial computation impossible. (M) can reach (4\cdot10^{18}), so even an (O(M)) algorithm would require around (4\cdot10^{18}) iterations. Exact factorials are also far too large to construct. The useful size is instead (D), which is at most (1.6\cdot10^7). This strongly suggests an algorithm whose expensive preprocessing depends on (D), while the huge values (M) and (N) are handled through logarithmic recurrences.

There are several edge cases that expose incorrect approaches.

For input `5 2 5`, the binomial coefficient is (10). Ordinary modular arithmetic gives (10\bmod5=0), but one factor of (5) must first be removed, so the correct answer is (2).

For input `6 2 6`, the binomial coefficient is (15). Neither (6) nor (6^2) divides (15), so the answer is (15\bmod6=3). A careless implementation that removes prime factors of (D) independently would remove a factor (2) or (3) even though the DivModulo operation only removes complete factors of (6).

For input `1 0 2`, the binomial coefficient is (1), because (0!=1). There is no factor of (2) to remove, so the answer is (1). An implementation that assumes (N>0) or treats an empty factorial incorrectly can fail here.

For input `6 3 6`, the binomial coefficient is (20). Since (6\nmid20), nothing is removed and the answer is (20\bmod6=2). This is a useful boundary case because the prime valuations of (20) are different: there are two factors of (2), but no factor of (3).

## Approaches

The brute-force approach is straightforward. We could compute the factorials, form the binomial coefficient, repeatedly divide by (D), and finally take the remainder. A less extreme version could generate the binomial coefficient multiplicatively, but it still needs (\Theta(M)) arithmetic steps in the worst case. At (M=4\cdot10^{18}), that means roughly four quintillion iterations before considering the cost of the enormous integers being manipulated. Pascal's triangle is even less practical. The brute-force method is correct because it follows the definition directly, but the input bounds make it unusable.

The key observation is that removing complete factors of (D) is a valuation problem. Factor (D) as

[
D=\prod_{i=1}^s p_i^{a_i},
]

where the (p_i) are distinct primes.

Let

[
e_i=v_{p_i}(C(M,N)).
]

A complete copy of (D) consumes (a_i) copies of (p_i) for every (i). Hence the number of complete copies of (D) contained in the binomial coefficient is

[
K=\min_i\left\lfloor\frac{e_i}{a_i}\right\rfloor.
]

The required integer is consequently

[
R=\frac{C(M,N)}{D^K}.
]

We cannot calculate (C(M,N)) itself, but we only need (R) modulo (D). Since the prime powers (p_i^{a_i}) are pairwise coprime, we can calculate (R) separately modulo every prime power and combine the results with the Chinese Remainder Theorem.

Fix one prime power

[
q=p^a.
]

Suppose the binomial coefficient has (p)-adic valuation (e=v_p(C(M,N))). After removing (D^K), its remaining (p)-adic exponent is

[
k=e-aK.
]

Write the binomial coefficient as

[
C(M,N)=p^e U,
]

where (U) is not divisible by (p). Then

p^k U\left(\frac{D}{q}\right)^{-K}.
]

Modulo (q), the denominator is invertible because (D/q) contains no factor (p). Thus the remaining task is to calculate the (p)-free part (U) of the binomial coefficient modulo (q).

For a factorial, define

[
F_p(n)=\frac{n!}{p^{v_p(n!)}}.
]

This value is always coprime to (p), so it has an inverse modulo (q). The binomial's (p)-free part is

[
U\equiv
F_p(M)F_p(N)^{-1}F_p(M-N)^{-1}\pmod q.
]

The crucial recurrence comes from separating the multiples of (p) inside (n!). Every multiple of (p) can have one factor (p) removed, leaving exactly the (p)-free part of the corresponding number after division by (p). Therefore,

F_p\left(\left\lfloor\frac np\right\rfloor\right)
\prod_{\substack{1\le i\le n\p\nmid i}}i
\pmod q.
]

The remaining product is periodic in blocks of length (q=p^a). If

[
G(x)=\prod_{\substack{1\le i\le x\p\nmid i}}i\pmod q,
]

then

G(q-1)^{\lfloor n/q\rfloor}G(n\bmod q)
\pmod q.
]

We can precompute (G(x)) for every (0\le x<q) in (O(q)) time. Every subsequent factorial calculation repeatedly replaces (n) by (\lfloor n/p\rfloor), so only (O(\log_p M)) levels are needed.

The brute-force method works because it evaluates the factorial definition literally, but fails because (M) is enormous. The observation that only the (p)-adic valuations and (p)-free parts matter lets us replace an astronomical factorial computation with (O(D)) preprocessing and logarithmically many reductions of (M) and (N).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(M)) or worse | (O(M)) or worse | Too slow |
| Optimal | (O(D+\omega(D)\log^2 M)) | (O(\max p_i^{a_i})) | Accepted |

Here (\omega(D)) is the number of distinct prime factors of (D). The (D) term comes from the prime-power prefix tables. The logarithmic term accounts for the repeated division by (p) and modular exponentiation.

## Algorithm Walkthrough

1. Factor (D) into distinct prime powers (q_i=p_i^{a_i}). Trial division is sufficient because (D\le1.6\cdot10^7), so checking divisors only up to (\sqrt D) takes at most about (4000) trial values.
2. For every prime (p_i), calculate

[
e_i=v_{p_i}(M!)-v_{p_i}(N!)-v_{p_i}((M-N)!).
]

The valuation of a factorial is given by Legendre's formula,

[
v_p(n!)=\left\lfloor\frac np\right\rfloor+
\left\lfloor\frac n{p^2}\right\rfloor+
\left\lfloor\frac n{p^3}\right\rfloor+\cdots.
]

Only (O(\log_p M)) terms are nonzero.

1. Compute

[
K=\min_i\left\lfloor\frac{e_i}{a_i}\right\rfloor.
]

This is exactly the number of complete copies of (D) that can be removed from the binomial coefficient. The minimum is necessary because one copy of (D) simultaneously consumes (a_i) copies of every prime (p_i).

1. Process each prime power (q=p^a) independently. Build a prefix array

[
G(x)=\prod_{\substack{1\le i\le x\p\nmid i}}i\bmod q.
]

Only numbers not divisible by (p) are multiplied into the prefix. Every value in this table is coprime to (p), which later makes modular inverses valid.

1. Implement a factorial-unit function (F_p(n)). At each iteration, multiply the contribution from the current block,

[
G(q-1)^{\lfloor n/q\rfloor}G(n\bmod q),
]

then replace (n) by (\lfloor n/p\rfloor). The loop terminates after (O(\log_p M)) iterations.

1. Use the three factorial-unit values to obtain the (p)-free part of the binomial coefficient,

[
U=
F_p(M)F_p(N)^{-1}F_p(M-N)^{-1}\pmod q.
]

All three factorial units are coprime to (q), so the inverses exist.

1. Let

[
k=e-aK.
]

The desired DivModulo value still contains (p^k) after all complete (D) factors have been removed. Thus its residue modulo (q) is

[
r=
U,p^k
\left(\frac Dq\right)^{-K}
\bmod q.
]

The inverse of (D/q) exists modulo (q), because (q) contains the entire (p)-power of (D).

1. Combine all congruences (R\equiv r_i\pmod{q_i}) using the Chinese Remainder Theorem. The prime powers are pairwise coprime and their product is (D), so there is exactly one answer modulo (D).

Why it works: for every prime (p_i), the algorithm separates the binomial coefficient into its exact (p_i)-power and a part coprime to (p_i). The valuation calculation determines exactly how many complete copies of (D) can be removed globally. After removing those copies, the remaining exponent of each prime is known, and the remaining (p)-free part is computed by the factorial recurrence. Consequently the residue modulo every prime-power component of (D) is exact. The Chinese Remainder Theorem then reconstructs the unique integer modulo (D), which is precisely the DivModulo result.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def factorize(n):
    factors = []
    e = 0
    while n % 2 == 0:
        n //= 2
        e += 1
    if e:
        factors.append((2, e))

    p = 3
    while p * p <= n:
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            factors.append((p, e))
        p += 2

    if n > 1:
        factors.append((n, 1))
    return factors

def vp_factorial(n, p):
    ans = 0
    while n:
        n //= p
        ans += n
    return ans

def build_prefix(p, q):
    # pref[x] = product of all 1 <= i <= x with p not dividing i, modulo q.
    pref = array('I', [0]) * q
    pref[0] = 1

    cur = 1
    for i in range(1, q):
        if i % p:
            cur = (cur * i) % q
        pref[i] = cur

    return pref

def factorial_unit(n, p, q, pref):
    # n! with every factor p removed, modulo q.
    block = pref[q - 1]
    res = 1

    while n:
        res = res * pow(block, n // q, q) % q
        res = res * pref[n % q] % q
        n //= p

    return res

def solve_case(M, N, D):
    factors = factorize(D)

    valuations = []
    K = 10**100

    for p, a in factors:
        e = (
            vp_factorial(M, p)
            - vp_factorial(N, p)
            - vp_factorial(M - N, p)
        )
        valuations.append(e)
        K = min(K, e // a)

    # CRT state: answer == x (mod mod)
    x = 0
    mod = 1

    for (p, a), e in zip(factors, valuations):
        q = p ** a

        pref = build_prefix(p, q)

        fm = factorial_unit(M, p, q, pref)
        fn = factorial_unit(N, p, q, pref)
        fr = factorial_unit(M - N, p, q, pref)

        unit = fm
        unit = unit * pow(fn, -1, q) % q
        unit = unit * pow(fr, -1, q) % q

        remaining_p = e - a * K

        residue = unit * pow(p, remaining_p, q) % q

        other = D // q
        residue = residue * pow(pow(other, K, q), -1, q) % q

        # Combine:
        # x + mod * t == residue (mod q)
        t = (residue - x) % q
        t = t * pow(mod, -1, q) % q

        x += mod * t
        mod *= q
        x %= mod

    return x

def solve():
    M, N, D = map(int, input().split())
    print(solve_case(M, N, D))

if __name__ == "__main__":
    solve()
```

The factorization routine uses trial division. Because (D) is at most (1.6\cdot10^7), the square root is below (4000), so a simple implementation is sufficient.

`vp_factorial` implements Legendre's formula. It never constructs a factorial and only performs repeated division by the relevant prime.

`build_prefix` stores the product of all integers up to each position that are not divisible by (p). The `array('I')` representation is deliberate. A Python list containing millions of Python integers would consume several hundred megabytes, while an unsigned integer array stores each entry in four bytes. Only one prime-power table is kept at a time.

`factorial_unit` implements the recurrence from the algorithm walkthrough. The recursion is written iteratively to avoid Python recursion overhead. At each level, the full blocks of length (q) contribute `pref[q - 1]`, while the incomplete block contributes `pref[n % q]`. Then `n` is divided by (p).

The three factorial units are combined using modular inverses. They are guaranteed to be coprime to (q), unlike the original factorials, which is exactly why the (p)-adic decomposition was needed.

The exponent `remaining_p = e - a * K` is never negative. By the definition of (K), we have (K\le e/a) for every prime-power component.

The factor `(D // q)^K` is inverted modulo `q`. This inverse always exists because (D/q) contains no factor (p). Computing the power before taking its inverse avoids ever trying to divide by a non-unit modulo (D).

Finally, the CRT update uses the equation

[
x+\text{mod}\cdot t\equiv r\pmod q.
]

Since `mod` and `q` are coprime, `pow(mod, -1, q)` exists. Python integers are arbitrary precision, so there is no overflow even though (M) reaches (4\cdot10^{18}).

## Worked Examples

### Sample 1

For `9 2 3`, we have

[
C(9,2)=36=4\cdot3^2.
]

There is only one prime-power component, (q=3).

| Step | (p) | (a) | (e=v_p(C)) | (K) | Remaining (p)-power | Residue |
| --- | --- | --- | --- | --- | --- | --- |
| Factorization | 3 | 1 | 2 | 2 | 0 |  |
| After removing (3^2) | 3 | 1 | 2 | 2 | (2-2=0) | 1 |

The (3)-free part of (36) is (4), and (4\bmod3=1). Since (36=4\cdot3^2), the answer is `1`. The trace also shows why ordinary modulo is insufficient: (36\bmod3=0), while DivModulo first removes both factors of (3).

### Sample 2

For `5 2 5`, we have

[
C(5,2)=10=2\cdot5.
]

Here (p=5), (a=1), and (e=1), so exactly one complete factor of (5) is removed.

| Step | (p) | (a) | (e=v_p(C)) | (K) | Remaining (p)-power | Final residue |
| --- | --- | --- | --- | --- | --- | --- |
| Factorization | 5 | 1 | 1 | 1 | 0 |  |
| Remove (5^1) | 5 | 1 | 1 | 1 | (1-1=0) | 2 |

The (5)-free part is (2), so the DivModulo result is `2`. A direct `10 % 5` would incorrectly produce zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(D+\omega(D)\log^2 M+\sqrt D)) | Prefix tables contain at most (D) entries in total, while factorial-unit evaluation and modular powers are logarithmic in (M). |
| Space | (O(\max_i p_i^{a_i})) | Only one prime-power prefix table is stored at a time. |

The sum of the distinct prime-power components of (D) is at most (D), so the total prefix preprocessing is (O(D)). With (D\le1.6\cdot10^7), this is the intended scale of the problem. The huge value of (M) only appears inside logarithmic computations, so the (4\cdot10^{18}) bound does not force iteration over the factorial itself.

The `array('I')` storage keeps the largest possible prefix table around the tens of megabytes rather than hundreds of megabytes of Python-object overhead, which is particularly relevant for the (D=1.6\cdot10^7) boundary.

## Test Cases

```
# This test block assumes the solution above is saved as solution.py
# and exposes solve_case(M, N, D).

from solution import solve_case

# Provided samples
assert solve_case(9, 2, 3) == 1, "sample 1"
assert solve_case(5, 2, 5) == 2, "sample 2"
assert solve_case(6, 3, 6) == 2, "sample 3"
assert solve_case(7654321, 1234567, 1050) == 210, "sample 4"

# Minimum-size input: C(1, 0) = 1
assert solve_case(1, 0, 2) == 1, "minimum input"

# N = M: C(M, M) = 1 even for enormous M
assert solve_case(4_000_000_000_000_000_000,
                 4_000_000_000_000_000_000,
                 16_000_000) == 1, "maximum M and D"

# D does not divide the binomial coefficient, even though
# D has several prime factors.
# C(6, 2) = 15, and 6 does not divide 15.
assert solve_case(6, 2, 6) == 3, "composite D without complete factor"

# Multiple complete D factors must all be removed.
# C(10, 5) = 252 = 7 * 6^2, so the answer is 7 mod 6 = 1.
assert solve_case(10, 5, 6) == 1, "multiple D factors"

# Dividing by D is required before taking the remainder.
# C(5, 2) = 10 = 2 * 5.
assert solve_case(5, 2, 5) == 2, "remove one complete D factor"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 2` | `1` | Minimum (M), (N=0), and (0!=1) |
| `4000000000000000000 4000000000000000000 16000000` | `1` | Maximum (M), maximum (D), and (C(M,M)=1) |
| `6 2 6` | `3` | Composite (D) where no complete factor of (D) exists |
| `10 5 6` | `1` | More than one complete factor of (D) must be removed |
| `5 2 5` | `2` | DivModulo differs from ordinary modulo |

## Edge Cases

For `5 2 5`, the algorithm finds (v_5(5!)=1), (v_5(2!)=0), and (v_5(3!)=0), giving (e=1). Since (D=5^1), we get (K=1). The remaining exponent is (e-K=0), so only the (5)-free binomial part remains. That part is (2), giving the correct answer `2`.

For `6 2 6`, factorization gives (D=2\cdot3). The binomial is (15), so its valuations are (v_2(15)=0) and (v_3(15)=1). The number of complete copies of (6) is

[
K=\min(0,1)=0.
]

Nothing is removed, and (15\bmod6=3). This demonstrates why the minimum across prime-power valuations is necessary. Removing prime factors independently would change the operation being computed.

For `6 3 6`, the binomial coefficient is (20=2^2\cdot5). Its (2)-valuation is (2), while its (3)-valuation is (0). Hence

[
K=\min(2,0)=0.
]

The algorithm leaves (20) unchanged and reconstructs (20\bmod6=2).

For `1 0 2`, both (0!) and (1!) have (p)-free part (1), and every factorial valuation is zero. Thus (K=0), the reconstructed residue is (1), and the answer is `1`.

For `10 5 6`, the binomial coefficient is (252=7\cdot6^2). The prime valuations are (v_2(252)=2) and (v_3(252)=2), so (K=2). After removing (6^2), the remaining value is (7), whose residue modulo (6) is `1`. The algorithm reaches the same result without ever constructing (252), and the same mechanism continues to work when the binomial coefficient has thousands or quintillions of digits.
