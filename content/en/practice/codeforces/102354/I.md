---
title: "CF 102354I - From Modular to Rational"
description: "For every test case, the judge has chosen a rational number [ x=frac pq, qquad 1le p,qle 10^9. ] We cannot ask for (x) directly. Instead, for a prime (m10^9), we ask for the residue (y) satisfying [ yequiv p q^{-1}pmod m. ] Equivalently, [ pequiv yqpmod m."
date: "2026-08-15T17:45:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102354
codeforces_index: "I"
codeforces_contest_name: "2018-2019 Summer Petrozavodsk Camp, Oleksandr Kulkov Contest 2"
rating: 0
weight: 102354
solve_time_s: 182
verified: false
draft: false
---

[CF 102354I - From Modular to Rational](https://codeforces.com/problemset/problem/102354/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 2s  
**Verified:** no  

## Solution
## Problem Understanding

For every test case, the judge has chosen a rational number

[
x=\frac pq,
\qquad 1\le p,q\le 10^9.
]

We cannot ask for (x) directly. Instead, for a prime (m>10^9), we ask for the residue (y) satisfying

[
y\equiv p q^{-1}\pmod m.
]

Equivalently,

[
p\equiv yq\pmod m.
]

The goal is to recover any valid pair (p,q) describing the same rational number. The pair does not have to be the exact pair originally chosen, because (1/2), (2/4), and (500000004/1000000008) represent the same rational number, and the protocol accepts any pair within the bounds representing that value. The official sample explicitly demonstrates this with (1/2) being answered as (2/4).

The limit of (10) queries is generous enough for a number theoretic reconstruction, but far too small for trying many moduli or searching through possible denominators. Since there can be (10^5) test cases, even an (O(10^9)) operation algorithm per case would mean (10^{14}) operations in the worst case. The intended solution uses only two queries per test case and then performs a logarithmic number of Euclidean algorithm steps.

The most useful way to think about the problem is that a modular answer gives us a linear congruence between the unknown numerator and denominator. One modulus around (10^9) is not large enough to make that congruence unique, but the product of two allowed primes can be around (10^{24}). That is much larger than (2\cdot10^{18}), which is the scale needed to distinguish two different fractions whose numerators and denominators are bounded by (10^9).

There are three edge cases that easily lead to incorrect solutions.

First, one modulus is not enough. Take (m=1000000007) and suppose the response is (500000004). The fraction (1/2) produces this residue because (2\cdot500000004\equiv1\pmod m). But the integer fraction (500000004/1) produces exactly the same residue. Both numerator and denominator satisfy the bounds, so a solution using only this modulus cannot know which rational number was chosen. Two moduli remove this ambiguity.

Second, the hidden pair does not have to be reduced. For example, the hidden representation (1000000000/1000000000) is simply the rational number (1). A reconstruction algorithm that insists on recovering the exact original numerator and denominator would be solving a problem the judge does not ask for. The correct answer can be (1/1).

Third, the recovered pair from rational reconstruction should be expected to be reduced. Suppose the hidden value is (2/4). The modular equations describe the rational value (1/2), and the Euclidean reconstruction naturally finds (1/2), not (2/4). This is valid because both pairs represent the same value.

## Approaches

A direct approach would query one prime (m), then try every possible denominator (q) from (1) through (10^9). For each (q), we calculate

[
p=(yq\bmod m)
]

and check whether (1\le p\le10^9). The true denominator must pass this test, so the method is correct if we accept any valid pair.

The problem is the (10^9) possible denominators. With (10^5) test cases, the worst case reaches (10^{14}) modular multiplications and reductions. Even one test case is already too large for a six second limit.

The key observation is that two modular answers can be combined into one answer modulo the product of the two primes. This is exactly the Chinese Remainder Theorem. After combining the residues, we know an integer (r) such that

[
r\equiv pq^{-1}\pmod M,
]

where

[
M=m_1m_2.
]

Equivalently,

[
p\equiv rq\pmod M.
]

The two fixed primes

[
m_1=999999999989,\qquad
m_2=1000000000039
]

are both valid primes in the required range. They are listed as consecutive primes around (10^{12}) in standard prime tables. Their product is roughly (10^{24}), so

[
M>2\cdot10^{18}.
]

Now suppose two different bounded fractions (p_1/q_1) and (p_2/q_2) produced the same residue. Then

[
p_1q_2\equiv p_2q_1\pmod M,
]

so (M) divides

[
p_1q_2-p_2q_1.
]

But each numerator and denominator is at most (10^9), so

[
|p_1q_2-p_2q_1|\le2\cdot10^{18}<M.
]

The only multiple of (M) in that interval is zero. Hence

[
p_1q_2=p_2q_1,
]

which means the two fractions are equal.

So after CRT, the problem becomes a standard rational reconstruction problem. Rational reconstruction is closely connected to the extended Euclidean algorithm and continued fractions.

The extended Euclidean algorithm produces remainders of the form

[
r_i=s_iM+t_ir.
]

Thus every intermediate pair satisfies

[
r_i\equiv t_ir\pmod M.
]

When the remainder first becomes at most (10^9), the large modulus condition guarantees that the corresponding coefficient (t_i) is also within the required bound and gives the desired numerator and denominator. This is the classical Euclidean algorithm approach to rational reconstruction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(10^9)) per test case | (O(1)) | Too slow |
| Optimal | (O(\log M)) arithmetic steps per test case | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Ask for the residue modulo (m_1=999999999989), then ask for the residue modulo (m_2=1000000000039). Both numbers are primes and lie strictly between (10^9) and (10^{12}), so both queries are legal. Using primes this large makes their product vastly exceed the (10^{18}) cross-product bound.
2. Combine the two residues with the Chinese Remainder Theorem. Let the answers be (y_1) and (y_2). Write

[
r=y_1+m_1k.
]

We need

[
y_1+m_1k\equiv y_2\pmod {m_2},
]

so

[
k\equiv(y_2-y_1)m_1^{-1}\pmod {m_2}.
]

Choosing the least nonnegative (k) gives the unique residue (r) modulo

[
M=m_1m_2.
]

The CRT step turns two small modular equations into one equation with a modulus around (10^{24}).

1. Run the extended Euclidean algorithm on (M) and (r), while also tracking the coefficient of (r). Initialize

[
R_0=M,\quad R_1=r,
]

and

[
T_0=0,\quad T_1=1.
]

The invariant is

[
R_i=S_iM+T_ir.
]

Consequently,

[
R_i\equiv T_ir\pmod M.
]

The coefficient (T_i) is the candidate denominator corresponding to the candidate numerator (R_i).

1. Repeatedly perform the usual Euclidean division

[
R_{i-1}=a_iR_i+R_{i+1},
]

and update

[
T_{i+1}=T_{i-1}-a_iT_i.
]

Stop when the current remainder becomes at most (10^9). The remainder is decreasing exactly as in the ordinary Euclidean algorithm, so only (O(\log M)) iterations are needed.

1. Normalize the signs so that the denominator is positive. For the positive rational hidden by the judge, the successful reconstruction has positive numerator and denominator.
2. Output the resulting numerator and denominator. If the hidden pair was not reduced, the Euclidean algorithm gives the reduced representation of the same rational number, which is still a valid answer.

### Why it works

The central invariant is

[
R_i=S_iM+T_ir,
]

so every Euclidean state represents a rational candidate (R_i/T_i) whose modular value is (r). The actual reduced hidden fraction (p/q) satisfies

[
p\equiv rq\pmod M.
]

Because (M>2\cdot10^{18}), two different rational values with numerator and denominator at most (10^9) cannot satisfy the same congruence. Classical rational reconstruction says that the first Euclidean remainder crossing the (10^9) bound is precisely the bounded solution.

The uniqueness argument is particularly simple. If two candidates existed, their cross product would be a multiple of (M), but its absolute value would be at most (2\cdot10^{18}), strictly smaller than (M). Hence the cross product must be zero, so both candidates represent the same rational number.

## Python Solution

```python
import sys
input = sys.stdin.readline

M1 = 999999999989
M2 = 1000000000039
LIMIT = 10**9

def crt(a1, a2):
    # x = a1 (mod M1)
    # x = a2 (mod M2)
    inv = pow(M1, -1, M2)
    k = ((a2 - a1) * inv) % M2
    return a1 + M1 * k

def reconstruct(r, mod):
    # Extended Euclidean algorithm.
    #
    # rem = s * mod + t * r
    # so rem == t * r (mod mod).
    old_rem, rem = mod, r
    old_t, t = 0, 1

    while rem > LIMIT:
        q = old_rem // rem

        old_rem, rem = rem, old_rem - q * rem
        old_t, t = t, old_t - q * t

    numerator = rem
    denominator = t

    if denominator < 0:
        numerator = -numerator
        denominator = -denominator

    # The original fraction may not have been reduced.
    # The Euclidean reconstruction is normally already reduced,
    # but reducing here also makes the returned representation explicit.
    g = __import__("math").gcd(numerator, denominator)
    numerator //= g
    denominator //= g

    return numerator, denominator

def ask(m):
    print("?", m, flush=True)
    return int(input())

def main():
    t = int(input())

    for _ in range(t):
        y1 = ask(M1)
        y2 = ask(M2)

        r = crt(y1, y2)
        p, q = reconstruct(r, M1 * M2)

        print("!", p, q, flush=True)

if __name__ == "__main__":
    main()
```

The two constants at the top are fixed legal primes, so there is no primality testing during the interaction. The product of these primes is around (10^{24}), comfortably above the required (2\cdot10^{18}) threshold.

The `crt` function implements the equation

[
r=y_1+m_1k.
]

The second congruence determines (k), and `pow(M1, -1, M2)` computes the modular inverse. Python's three-argument `pow` supports a negative exponent for modular inverses in Python 3.8 and later.

The `reconstruct` function stores only the remainder and its coefficient of (r). The coefficient of the modulus is unnecessary after the invariant has been established, which keeps the implementation small.

The loop condition is `rem > LIMIT`, not `rem >= LIMIT`. A remainder equal to (10^9) is already legal and must be accepted. This is an easy boundary condition to get wrong.

Python integers are arbitrary precision, so the CRT product around (10^{24}) does not overflow. A C++ implementation using signed 64-bit integers would also have to avoid storing this product in a signed `long long`, because (10^{24}) is far beyond its range. Python does not have this issue.

The final gcd reduction handles the fact that the original pair (p,q) need not be coprime. For example, the hidden value (2/4) is reconstructed as (1/2), which is a valid answer.

Every query is flushed immediately. Without `flush=True`, an interactive solution can wait indefinitely because the judge may not receive a query that remains in the output buffer.

## Worked Examples

The provided sample uses one query per test case and demonstrates the interaction protocol. For (m=1000000007), the response (500000004) corresponds to (1/2), while the judge accepts the answer (2/4). The optimal solution described here asks two larger primes instead, because a single modulus does not provide enough information.

For a first reconstruction trace, consider the same rational value (x=1/2), using the two primes from the solution. The residues are

[
y_1=\frac{m_1+1}{2}=499999999995
]

and

[
y_2=\frac{m_2+1}{2}=500000000020.
]

The CRT result is the residue of (1/2) modulo (M=m_1m_2), namely

[
r=\frac{M+1}{2}.
]

| Euclidean state | Remainder | Coefficient of (r) | Meaning |
| --- | --- | --- | --- |
| Initial | (M) | (0) | (M=1\cdot M+0\cdot r) |
| Initial | ((M+1)/2) | (1) | (r=0\cdot M+1\cdot r) |
| After (q=1) | ((M-1)/2) | (-1) | (R=-M+r) |
| After (q=1) | (1) | (2) | (1=2r-M) |

The last row has remainder (1) and coefficient (2), so the reconstructed fraction is (1/2). The invariant directly verifies the modular relation because (2r\equiv1\pmod M).

For the second trace, use (x=2/3). Since (M\equiv2\pmod3), the residue of (2/3) modulo (M) is

[
r=\frac{M+2}{3}.
]

The Euclidean sequence becomes particularly short.

| Euclidean state | Remainder | Coefficient of (r) | Meaning |
| --- | --- | --- | --- |
| Initial | (M) | (0) | (M=1\cdot M+0\cdot r) |
| Initial | ((M+2)/3) | (1) | (r=0\cdot M+1\cdot r) |
| After (q=2) | ((M-4)/3) | (-2) | (R=M-2r) |
| After (q=1) | (2) | (3) | (2=3r-M) |

The first remainder below (10^9) is (2), with coefficient (3). Hence the result is (2/3). This demonstrates why tracking the Euclidean coefficient is enough, and why we do not need to search over possible denominators.

The official sample also includes the cases (1/1), (1/2), and (2/1), and specifically points out that a non-reduced answer such as (2/4) is valid for (1/2).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(t\log M)) arithmetic steps | Two CRT operations and one extended Euclidean algorithm per test case |
| Space | (O(1)) | Only a constant number of integers is stored |

Here (M=m_1m_2) is about (10^{24}), so its bit length is only about (80). The Euclidean algorithm therefore takes only a few dozen iterations per test case. Across (10^5) cases this remains practical, while the brute-force approach would require up to (10^{14}) denominator checks.

The interaction itself uses exactly two queries per test case, well below the limit of ten.

## Test Cases

Because the original task is interactive, its sample input is not an ordinary complete input file. The lines shown as input are responses from the hidden judge, so an offline `run()` function cannot replay the sample literally. The useful way to unit-test the submitted logic is to test the pure reconstruction routine by generating the two modular responses from known rational values.

```python
import sys
import io
from math import gcd

M1 = 999999999989
M2 = 1000000000039
LIMIT = 10**9

def crt(a1, a2):
    inv = pow(M1, -1, M2)
    k = ((a2 - a1) * inv) % M2
    return a1 + M1 * k

def reconstruct(r, mod):
    old_rem, rem = mod, r
    old_t, t = 0, 1

    while rem > LIMIT:
        q = old_rem // rem
        old_rem, rem = rem, old_rem - q * rem
        old_t, t = t, old_t - q * t

    if t < 0:
        rem = -rem
        t = -t

    g = gcd(rem, t)
    return rem // g, t // g

def modular_image(p, q, m):
    return (p * pow(q, -1, m)) % m

def run(inp: str) -> str:
    # Offline test harness.
    # Each line contains the hidden p and q.
    out = []

    for line in inp.strip().splitlines():
        if not line.strip():
            continue

        p, q = map(int, line.split())

        y1 = modular_image(p, q, M1)
        y2 = modular_image(p, q, M2)

        r = crt(y1, y2)
        a, b = reconstruct(r, M1 * M2)

        out.append(f"{a} {b}")

    return "\n".join(out)

# Values represented by the provided interactive sample.
assert run("1 1\n1 2\n2 1\n") == (
    "1 1\n"
    "1 2\n"
    "2 1"
), "provided sample values"

# Minimum-size numerator and denominator.
assert run("1 1\n") == "1 1", "minimum-size values"

# Maximum allowed numerator and denominator, both equal.
# The rational value is 1, so 1/1 is the canonical answer.
assert run("1000000000 1000000000\n") == "1 1", "maximum equal values"

# Numerator and denominator are both close to the upper boundary
# and are coprime.
assert run("999999999 1000000000\n") == "999999999 1000000000", (
    "upper-bound coprime fraction"
)

# Small denominator and maximum numerator.
assert run("1000000000 1\n") == "1000000000 1", (
    "maximum numerator with denominator 1"
)

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1`, `1 2`, `2 1` | `1 1`, `1 2`, `2 1` | Values represented in the provided sample |
| `1 1` | `1 1` | Minimum-size boundary |
| `1000000000 1000000000` | `1 1` | Non-reduced representation and maximum equal values |
| `999999999 1000000000` | `999999999 1000000000` | Both bounds simultaneously, with a reduced fraction |
| `1000000000 1` | `1000000000 1` | Maximum numerator and denominator boundary behavior |

## Edge Cases

The one-modulus collision is the most fundamental failure mode. With (m=1000000007), the response (500000004) is produced by (1/2), because

[
2\cdot500000004=1000000008\equiv1\pmod m.
]

The same response is also produced by (500000004/1). A solution using only this modulus has no mathematical way to distinguish the two values. The optimal solution asks a second independent prime, combines the answers into a modulus above (10^{18}), and makes such a collision impossible.

The non-reduced representation is another subtle case. For the input value (1000000000/1000000000), both original numbers are at their maximum allowed size, but the rational number itself is (1). The modular response is (1) for every queried prime. Rational reconstruction returns (1/1), and the answer is accepted because the protocol asks for a representation of the rational value, not recovery of the exact hidden pair.

For a value such as (2/4), the same modular observations are generated as for (1/2). The Euclidean reconstruction finds the reduced pair (1/2). Dividing both components by their gcd does not change the represented rational value, so the result remains valid.

Finally, a remainder exactly equal to (10^9) must be accepted. The reconstruction loop uses `rem > LIMIT`, not `rem >= LIMIT`. Treating equality as too large would skip a legal numerator and could move the Euclidean process past the correct reconstruction.

The complete idea is thus quite compact: two large prime queries give one enormous modulus through CRT, and the enormous modulus turns modular rational recovery into a standard bounded rational reconstruction problem solved by extended Euclid. The original problem and independent editorials describe the same CRT and Euclidean reconstruction viewpoint.
