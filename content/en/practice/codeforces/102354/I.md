---
title: "CF 102354I - From Modular to Rational"
description: "For every test case, the judge secretly chooses a positive rational number (x=p/q), where both (p) and (q) are at most (10^9). We cannot see (p) and (q) directly."
date: "2026-08-14T12:28:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102354
codeforces_index: "I"
codeforces_contest_name: "2018-2019 Summer Petrozavodsk Camp, Oleksandr Kulkov Contest 2"
rating: 0
weight: 102354
solve_time_s: 160
verified: false
draft: false
---

[CF 102354I - From Modular to Rational](https://codeforces.com/problemset/problem/102354/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 40s  
**Verified:** no  

## Solution
## Problem Understanding

For every test case, the judge secretly chooses a positive rational number (x=p/q), where both (p) and (q) are at most (10^9). We cannot see (p) and (q) directly. Instead, we can choose a large prime (m), ask for the value of (p q^{-1}\pmod m), and use the returned residue to recover the rational number. The answer may use any positive numerator and denominator at most (10^9) representing the same rational value, so reducing the fraction is always allowed. The problem is interactive, meaning the program must print queries, flush them, read the judge's replies, and finally print the recovered fraction.

The upper bound (10^9) on both numerator and denominator is the key numerical constraint. It tells us that two different reduced fractions satisfying the bound can have cross products differing by at most (10^{18}). A modulus only slightly larger than (10^9) is not enough to distinguish them, so one query cannot in general provide enough information. The query limit of ten is generous enough to combine two moduli whose product is much larger than (10^{18}). The number of test cases can reach (10^5), so the local computation after each query must be logarithmic in the modulus rather than proportional to (10^9). Two queries and one extended Euclidean computation per test case are easily small enough.

There is another subtlety caused by the fact that the input fraction need not be reduced. Suppose the hidden value is (2/4). The correct mathematical value is (1/2), and returning `! 1 2` is valid. A reconstruction algorithm that searches only for the exact hidden pair (2,4) would be solving a stronger problem than necessary and can produce the wrong answer when it insists on recovering the original representation.

A second edge case is (p=q=10^9). The fraction is exactly (1), so the correct response can be `! 1 1`, not necessarily `! 1000000000 1000000000`. A careless algorithm that treats the given bounds as requiring the original numerator and denominator would unnecessarily distinguish representations of the same rational number.

A third edge case occurs when the modular residue is very large. For example, for (x=1/2) and an odd prime (m), the returned residue is ((m+1)/2), which is close to (m/2), far above (10^9). Trying to interpret the returned value itself as the numerator therefore fails. The numerator and denominator have to be reconstructed from the congruence (p\equiv rq\pmod M), rather than read directly from the residue.

## Approaches

A direct approach is to query one modulus and try every possible denominator (q) from (1) through (10^9). For each (q), the congruence determines a candidate numerator as (p=rq\bmod m). If that value lies between (1) and (10^9), we have found a valid representation. This works because the hidden pair is guaranteed to be among those candidates, but the worst case requires (10^9) modular multiplications for one test case. Across (10^5) test cases that becomes (10^{14}) iterations, which is completely impractical.

The key observation is that several modular answers can be combined. Ask two different primes (m_1,m_2), then use the Chinese Remainder Theorem to turn the two answers into a single residue (r) modulo

[
M=m_1m_2.
]

We can choose the two primes so that (M>2\cdot 10^{18}). The values

[
m_1=999999999989,\qquad m_2=1000000000039
]

are both prime and satisfy the required query range. Their product is about (10^{24}), comfortably above the required bound.

Now the problem becomes a standard rational reconstruction problem. We know

[
r\equiv pq^{-1}\pmod M,
]

or equivalently,

[
rq\equiv p\pmod M.
]

The reduced hidden fraction has (1\le p,q\le10^9). If two different reduced fractions (p_1/q_1) and (p_2/q_2) produced the same residue, then

[
p_1q_2-p_2q_1\equiv0\pmod M.
]

The absolute value of the left side is at most (2\cdot10^{18}), while (M) is larger than that. Hence the difference must actually be zero, so the fractions are identical. This is precisely the uniqueness condition behind rational reconstruction, which can be performed using the extended Euclidean algorithm.

The Euclidean algorithm gives a sequence of identities

[
R_i=A_iM+B_ir.
]

When the remainder (R_i) first becomes at most (10^9), the corresponding coefficient (B_i) is the denominator of the reconstructed fraction, up to a common sign. The modulus is deliberately much larger than (2N^2), with (N=10^9), so the desired numerator and denominator must appear at this point in the Euclidean sequence.

The brute-force and optimal approaches can be summarized as follows.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(10^9)) per test case | (O(1)) | Too slow |
| CRT + rational reconstruction | (O(\log M)) per test case | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Ask for the hidden residue modulo (m_1=999999999989). The number is prime and lies strictly between (10^9) and (10^{12}), so it is a legal query.
2. Ask for the residue modulo (m_2=1000000000039). Using two distinct primes gives two congruences describing the same rational number.
3. Combine the two answers with the Chinese Remainder Theorem. If the replies are (r_1) and (r_2), write

[
r=r_1+m_1k.
]

We choose (k) so that (r\equiv r_2\pmod {m_2}). Thus

[
k\equiv(r_2-r_1)m_1^{-1}\pmod {m_2}.
]

The resulting (r) is the unique residue modulo (M=m_1m_2) satisfying both queries.

1. Run the extended Euclidean algorithm on (M) and (r), while tracking the coefficient of (r). Initially the two relevant pairs are

[
(M,0),\qquad(r,1).
]

Every Euclidean transition preserves an identity of the form

[
R=AM+Br.
]

1. Stop at the first Euclidean remainder (R) with (R\le10^9). The rational reconstruction theorem says that, because (M>2\cdot10^{18}), this remainder and its coefficient of (r) give the unique reduced numerator and denominator within the required bounds.
2. Make the coefficient positive if necessary by changing both signs. In the valid positive reconstruction for this problem the final pair is positive, but normalizing the sign makes the implementation robust.
3. Print the reconstructed numerator and denominator as the final answer. The reconstructed fraction is the same rational value as the hidden fraction, even when the judge originally chose a non-reduced representation.

The invariant throughout the Euclidean phase is that every current remainder (R) has a known representation (R=AM+Br). Since (r\equiv pq^{-1}\pmod M), multiplying the latter congruence by (q) gives (rq\equiv p\pmod M). Thus the hidden pair itself is one of the small solutions represented in this Euclidean lattice. The bound (M>2N^2) makes that small reduced solution unique, so when Euclid reaches the first sufficiently small remainder, it cannot be a different valid fraction.

## Python Solution

The original task is interactive, so the program below is the actual interactive solution. The sample shown in the statement is an interaction transcript rather than ordinary input, so it cannot be executed as a conventional stdin-to-stdout batch test.

```python
import sys
input = sys.stdin.readline

P1 = 999999999989
P2 = 1000000000039
N = 10**9

def extended_gcd(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

    return old_r, old_s, old_t

def crt(r1, r2):
    # r = r1 + P1 * k
    # P1 * k == r2 - r1 (mod P2)
    _, inv, _ = extended_gcd(P1, P2)
    inv %= P2

    k = ((r2 - r1) % P2) * inv % P2
    return r1 + P1 * k

def rational_reconstruct(r, mod):
    # Euclidean sequence:
    # remainder = A * mod + B * r
    old_r, cur_r = mod, r
    old_b, cur_b = 0, 1

    while cur_r > N:
        q = old_r // cur_r

        old_r, cur_r = cur_r, old_r - q * cur_r
        old_b, cur_b = cur_b, old_b - q * cur_b

    numerator = cur_r
    denominator = cur_b

    if denominator < 0:
        numerator = -numerator
        denominator = -denominator

    return numerator, denominator

def ask(m):
    print("?", m, flush=True)
    ans = int(input())

    if ans == -1:
        sys.exit(0)

    return ans

def main():
    t = int(input())

    for _ in range(t):
        r1 = ask(P1)
        r2 = ask(P2)

        r = crt(r1, r2)
        mod = P1 * P2

        p, q = rational_reconstruct(r, mod)

        print("!", p, q, flush=True)

if __name__ == "__main__":
    main()
```

The constants are fixed before processing any test case. Both are valid primes in the permitted interval, so there is no need to spend queries or computation searching for primes. Their product is larger than (2\cdot10^{18}), which is the only size condition needed by rational reconstruction.

The `ask` function prints the query and immediately flushes stdout. Flushing is mandatory in an interactive problem because the judge cannot answer a query it has not received. A reply of `-1` conventionally means that the interaction has failed, so the program terminates immediately rather than sending more output.

The `crt` function follows the direct two-modulus CRT formula. The extended Euclidean algorithm gives the inverse of (P_1) modulo (P_2), and the multiplication is reduced modulo (P_2) before constructing the final residue. Python integers have arbitrary precision, which is useful because (P_1P_2) is around (10^{24}), far beyond signed 64-bit range.

The `rational_reconstruct` function tracks only the coefficient of the queried residue. There is no need to retain the coefficient of the modulus. When `cur_r` first becomes at most (10^9), the corresponding coefficient gives the denominator and the remainder gives the numerator. The stopping condition uses `>` rather than `>=`, because a remainder equal to (10^9) is already a valid numerator and must be accepted.

The algorithm never divides by the original denominator modulo the combined modulus. The denominator is at most (10^9), while both queried primes are greater than (10^9), so it is automatically invertible modulo each prime. This is what makes the modular representation of the rational number well defined.

## Worked Examples

The statement's sample uses one modulus and demonstrates three hidden values, (1), (1/2), and (2). Our implementation asks two larger primes instead, but the reconstruction phase behaves in exactly the same way.

For the first sample value (x=1), both replies are (1).

| Step | (r_1) | (r_2) | CRT residue (r) | Euclidean remainder | Coefficient of (r) | Result |
| --- | --- | --- | --- | --- | --- | --- |
| Query 1 | 1 |  |  |  |  |  |
| Query 2 | 1 | 1 |  |  |  |  |
| CRT | 1 | 1 | 1 |  |  |  |
| Reconstruction |  |  | 1 | 1 | 1 | (1/1) |

The Euclidean algorithm reaches (1) immediately, and the corresponding coefficient is (1). The output `! 1 1` represents the same value as the hidden number.

For the second sample value (x=1/2), the inverse of (2) modulo an odd prime (m) is ((m+1)/2). Thus the two replies are (499999999995) and (500000000020).

| Step | (r_1) | (r_2) | CRT residue (r) | Euclidean remainder | Coefficient of (r) | Result |
| --- | --- | --- | --- | --- | --- | --- |
| Query 1 | 499999999995 |  |  |  |  |  |
| Query 2 | 499999999995 | 500000000020 |  |  |  |  |
| CRT | 499999999995 | 500000000020 | ((M+1)/2) |  |  |  |
| Euclid 1 |  |  |  | ((M-1)/2) | (-1) |  |
| Euclid 2 |  |  |  | 1 | 2 | (1/2) |

The large modular residue is not mistaken for a large numerator. Euclid converts the modular information into the small pair (1,2), which demonstrates why rational reconstruction is the correct abstraction.

As a second custom example, consider the hidden representation (10^9/10^9). Its value is (1), so every query returns the residue (1), exactly as in the first trace. Rational reconstruction returns (1/1).

| Step | Hidden representation | (r_1) | (r_2) | Reconstructed numerator | Reconstructed denominator |
| --- | --- | --- | --- | --- | --- |
| Queries | (1000000000/1000000000) | 1 | 1 |  |  |
| CRT | (1) | 1 | 1 |  |  |
| Reconstruction | (1) |  |  | 1 | 1 |

This trace exercises the maximum allowed numerator and denominator while also confirming that the answer is allowed to be reduced.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(\log M)) per test case | CRT uses a constant number of extended Euclidean operations, and rational reconstruction performs one Euclidean algorithm |
| Space | (O(1)) | Only a constant number of integers are stored |

With (M\approx10^{24}), the Euclidean algorithm needs only a few dozen integer divisions per test case. Even for (10^5) test cases, the number of arithmetic steps is tiny compared with the (10^{14}) iterations required by denominator enumeration. Python's arbitrary-precision integers also handle the (10^{24})-scale CRT modulus directly, so there is no overflow issue.

## Test Cases

Because this is interactive, the literal sample input cannot be fed to the solution as a normal string. The following offline harness tests the deterministic reconstruction core by simulating the judge's two modular replies from a known fraction. The three fractions from the provided sample are included as the first test.

```python
import sys
import io
from math import gcd

P1 = 999999999989
P2 = 1000000000039
N = 10**9

def extended_gcd(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

    return old_r, old_s, old_t

def crt(r1, r2):
    _, inv, _ = extended_gcd(P1, P2)
    inv %= P2
    k = ((r2 - r1) % P2) * inv % P2
    return r1 + P1 * k

def rational_reconstruct(r, mod):
    old_r, cur_r = mod, r
    old_b, cur_b = 0, 1

    while cur_r > N:
        q = old_r // cur_r
        old_r, cur_r = cur_r, old_r - q * cur_r
        old_b, cur_b = cur_b, old_b - q * cur_b

    p, q = cur_r, cur_b

    if q < 0:
        p = -p
        q = -q

    return p, q

def solve_fraction(p, q):
    # Simulate the two interactive replies.
    r1 = (p * pow(q, -1, P1)) % P1
    r2 = (p * pow(q, -1, P2)) % P2

    r = crt(r1, r2)
    return rational_reconstruct(r, P1 * P2)

def run(inp: str) -> str:
    out = []

    for line in inp.strip().splitlines():
        if not line.strip():
            continue

        p, q = map(int, line.split())
        a, b = solve_fraction(p, q)
        out.append(f"{a} {b}")

    return "\n".join(out) + "\n"

# Provided sample values: 1, 1/2, and 2.
assert run("""\
1 1
1 2
2 1
""") == """\
1 1
1 2
2 1
""", "provided sample values"

# Non-reduced representation. The correct rational value is 1/2.
assert run("""\
2 4
""") == """\
1 2
""", "non-reduced fraction"

# Minimum-size fraction.
assert run("""\
1 1
""") == """\
1 1
""", "minimum-size values"

# Maximum-size numerator and denominator. The value is exactly 1.
assert run("""\
1000000000 1000000000
""") == """\
1 1
""", "maximum-size equal values"

# Boundary numerator and denominator.
assert run("""\
1000000000 999999999
""") == """\
1000000000 999999999
""", "values at the upper bound")

# A fraction whose reduced denominator is large.
assert run("""\
999999999 1000000000
""") == """\
999999999 1000000000
""", "large reduced denominator")

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1`, `1 2`, `2 1` | `1 1`, `1 2`, `2 1` | Values represented in the provided interactive sample |
| `2 4` | `1 2` | Non-reduced input representation |
| `1 1` | `1 1` | Minimum allowed values |
| `1000000000 1000000000` | `1 1` | Maximum values and reduction |
| `1000000000 999999999` | `1000000000 999999999` | Upper-bound numerator |
| `999999999 1000000000` | `999999999 1000000000` | Large reduced denominator |

## Edge Cases

For the non-reduced case, consider the exact input `2 4` in the offline harness. Both primes see the same modular value as (1/2), because

[
2\cdot4^{-1}\equiv1\cdot2^{-1}\pmod m.
]

CRT combines the two observations into the residue of (1/2), and rational reconstruction returns `1 2`. This is correct because the required output is the rational value, not the original encoding.

For the maximum-equal case, consider `1000000000 1000000000`. Both modular replies are (1), so CRT gives (r=1). The first Euclidean remainder already satisfies the (10^9) bound, with coefficient (1), giving `1 1`. A solution that attempted to preserve the hidden representation would unnecessarily return the unreduced pair, but the judge accepts any valid representation of the value.

For (x=1/2), the modular replies are around (5\cdot10^{11}), even though both numerator and denominator are at most (10^9). The Euclidean sequence eventually reaches remainder (1) with coefficient (2). This catches the common mistake of assuming the returned modular value itself must be the numerator.

For the upper-bound fraction `1000000000 999999999`, the numerator is exactly at the allowed limit. The combined modulus is still much larger than every relevant cross product, so the rational reconstruction theorem applies without needing any special treatment for equality at the bound. The algorithm returns the same reduced pair, confirming that the stopping condition must accept a remainder equal to (10^9), not only one strictly smaller than it.

The essential idea is to spend two of the ten available queries to manufacture a modulus around (10^{24}), then stop thinking about the interaction and solve a purely arithmetic problem. CRT gives one congruence modulo a sufficiently large modulus, and the extended Euclidean algorithm turns that congruence back into the unique small rational number.
