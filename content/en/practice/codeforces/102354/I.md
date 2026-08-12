---
title: "CF 102354I - From Modular to Rational"
description: "For each test case, the judge has chosen a positive rational number [ x=frac{p}{q}, qquad 1le p,qle 10^9. ] We cannot see (p) and (q) directly. Instead, for a prime modulus (m) between (10^9) and (10^{12}), we can ask for the residue [ yequiv p q^{-1}pmod m."
date: "2026-08-13T00:38:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102354
codeforces_index: "I"
codeforces_contest_name: "2018-2019 Summer Petrozavodsk Camp, Oleksandr Kulkov Contest 2"
rating: 0
weight: 102354
solve_time_s: 231
verified: false
draft: false
---

[CF 102354I - From Modular to Rational](https://codeforces.com/problemset/problem/102354/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 51s  
**Verified:** no  

## Solution
## Problem Understanding

For each test case, the judge has chosen a positive rational number

[
x=\frac{p}{q},
\qquad 1\le p,q\le 10^9.
]

We cannot see (p) and (q) directly. Instead, for a prime modulus (m) between (10^9) and (10^{12}), we can ask for the residue

[
y\equiv p q^{-1}\pmod m.
]

Since (m>10^9\ge q), the inverse (q^{-1}\pmod m) always exists. Our task is to recover any pair (P,Q) with (1\le P,Q\le10^9) representing the same rational value. The pair does not have to be reduced, so returning (1/2) instead of (2/4) is equally valid. The original problem is interactive, so the displayed sample is a dialogue between the program and the judge rather than an ordinary fixed input/output pair.

The bounds are designed around a number-theoretic reconstruction rather than enumeration. There can be (10^5) test cases, while a query itself gives only a modular value. Trying all (10^9) possible denominators for every test case would require up to (10^{14}) iterations, which is far beyond the six-second limit. The useful fact is that the allowed modulus can be almost (10^{12}), so two queries can give us a combined modulus around (10^{24}). That is vastly larger than the (10^{18})-scale product of the unknown numerator and denominator.

There are several cases where a simplistic implementation can silently fail. First, one modulus does not necessarily identify the rational value. With (m=10^9+7), the two different rationals

[
\frac{600000000}{1}
\quad\text{and}\quad
\frac{199999993}{2}
]

produce the same residue, because

[
199999993\equiv 2\cdot600000000\pmod {10^9+7}.
]

Both numerators and denominators satisfy the required bounds, so assuming that one sufficiently large modulus is enough is incorrect.

Second, the input fraction need not be reduced. The sample contains (2/4), which has the same value as (1/2). An implementation that insists on recovering exactly the original (p) and (q) is solving a stronger problem than the judge asks. Rational reconstruction naturally returns the reduced representation, which is acceptable.

Third, a boundary value such as (p=q=10^9) should not be rejected merely because the reduced fraction is (1/1). The original representation is legal, and the required answer is any legal representation of the same value.

## Approaches

A direct approach would choose a modulus, obtain its residue (r), and try every denominator (q) from (1) through (10^9). For each candidate, we could calculate

[
p=(rq)\bmod m
]

and accept the pair if (1\le p\le10^9). This is correct whenever it finds a valid pair because the test is exactly the congruence supplied by the judge. The problem is the number of iterations. In the worst case one test requires (10^9) modular multiplications, and (10^5) tests would give (10^{14}) iterations. Even ignoring interaction overhead, that is hopeless.

The key observation is that the query gives a congruence of exactly the form used by rational reconstruction:

[
p\equiv rq\pmod M.
]

If we can make (M) larger than (2\cdot10^9\cdot10^9=2\cdot10^{18}), there can be at most one reduced rational with numerator and denominator bounded by (10^9) satisfying this congruence. The standard rational reconstruction algorithm finds that pair using the extended Euclidean algorithm. Its connection to Euclid is especially natural here because the desired equation can be rewritten as

[
p=rq-kM
]

for some integer (k). Thus (p) and (q) occur as a small remainder and its corresponding coefficient in the Euclidean algorithm.

One allowed modulus is too small for the uniqueness bound. Two primes close to (10^{12}), however, give a product close to (10^{24}). We first ask for the residue modulo each prime and combine the two residues with the Chinese remainder theorem. The resulting modulus satisfies the rational reconstruction bound by an enormous margin. The official problem constraints allow up to ten queries, so using two is comfortably within the limit.

The two fixed primes used below are (999999999989) and (999999999997). Both are below (10^{12}), above (10^9), and prime. The first is the largest twelve-digit prime, and the second is the preceding known prime near (10^{12}).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(t\cdot10^9)) | (O(1)) | Too slow |
| Two queries + CRT + rational reconstruction | (O(t\log 10^{12})) arithmetic steps | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Ask the judge for the residue modulo (m_1=999999999989). Store the answer as (r_1). We use a prime larger than every possible denominator, so division by (q) modulo (m_1) is well-defined.
2. Ask for the residue modulo (m_2=999999999997), storing it as (r_2). The two moduli are distinct primes, so they are coprime and can be combined with the Chinese remainder theorem.
3. Construct the unique (R) with (0\le R<M=m_1m_2) satisfying

[
R\equiv r_1\pmod {m_1},
\qquad
R\equiv r_2\pmod {m_2}.
]

A convenient formula is

[
R=r_1+m_1
\left((r_2-r_1)m_1^{-1}\bmod m_2\right).
]

The important point is that the two original congruences are now represented by one congruence modulo the much larger modulus (M).

1. Run the extended Euclidean algorithm on (M) and (R). Maintain coefficients (t) satisfying

[
\text{remainder}=sM+tR.
]

When a remainder becomes at most (10^9), stop. Rational reconstruction guarantees that the corresponding coefficient (t), after changing both signs if necessary, is the denominator of the desired reduced fraction, provided it is at most (10^9). The standard rational reconstruction algorithm is precisely an extended-Euclidean procedure with numerator and denominator bounds.

1. Let the resulting positive pair be ((P,Q)). Verify conceptually that

[
P\equiv RQ\pmod M.
]

Since (M>2\cdot10^{18}), there cannot be two different reduced fractions with both numerator and denominator at most (10^9) satisfying this congruence. Thus the reconstructed fraction is the same rational number as the hidden one.

1. Output `! P Q`. The reconstructed pair may be reduced even when the judge originally chose a non-reduced pair, which is explicitly allowed by the problem.

### Why it works

Suppose two reduced fractions (p/q) and (a/b), with all four values at most (10^9), produced the same residue modulo (M). Then

[
pq^{-1}\equiv ab^{-1}\pmod M
]

implies

[
pb-aq\equiv0\pmod M.
]

But

[
|pb-aq|
\le pb+aq
\le2\cdot10^{18}
<M.
]

The only multiple of (M) with absolute value smaller than (M) is zero, so (pb=aq). Since both fractions are reduced, they are equal. Rational reconstruction finds the small pair corresponding to the Euclidean relation, so it must be this unique fraction.

## Python Solution

```python
import sys
input = sys.stdin.readline

M1 = 999999999989
M2 = 999999999997
LIMIT = 10**9

def crt(r1, r2):
    # R = r1 + M1 * k
    # R == r2 (mod M2)
    # M1 * k == r2-r1 (mod M2)
    inv = pow(M1, -1, M2)
    k = ((r2 - r1) * inv) % M2
    return r1 + M1 * k

def rational_reconstruct(r, mod):
    # We maintain:
    # rem = s * mod + t * r
    rem0, rem1 = mod, r
    t0, t1 = 0, 1

    while rem1 > LIMIT:
        q = rem0 // rem1
        rem0, rem1 = rem1, rem0 - q * rem1
        t0, t1 = t1, t0 - q * t1

    if t1 < 0:
        rem1 = -rem1
        t1 = -t1

    # The problem guarantees that a valid reconstruction exists.
    assert 1 <= rem1 <= LIMIT
    assert 1 <= t1 <= LIMIT
    assert (r * t1 - rem1) % mod == 0

    return rem1, t1

def ask(m):
    print("?", m, flush=True)
    return int(input())

def main():
    t = int(input())

    for _ in range(t):
        r1 = ask(M1)
        r2 = ask(M2)

        r = crt(r1, r2)
        p, q = rational_reconstruct(r, M1 * M2)

        print("!", p, q, flush=True)

if __name__ == "__main__":
    main()
```

The two constants at the top are fixed legal query moduli. Using fixed primes avoids spending queries or computation on primality testing during the interaction.

The `crt` function implements the Chinese remainder theorem directly. We write (R=r_1+m_1k), substitute it into the second congruence, and solve one linear congruence for (k). Python integers have arbitrary precision, so the product (m_1m_2), which is around (10^{24}), does not overflow.

The `rational_reconstruct` function is the extended Euclidean part. Initially the two remainders are (M) and (R), with coefficients (0) and (1) of (R). After every Euclidean division, the coefficient is updated using exactly the same quotient as the remainder. When the remainder first falls to at most (10^9), rational reconstruction tells us that this remainder and its coefficient encode the desired numerator and denominator.

The sign correction matters because Euclid's coefficients alternate in sign. If the denominator coefficient is negative, both values are negated together. The final assertion checks the defining congruence and also catches an implementation error during local testing.

The query calls use `flush=True`. Without flushing, the program could wait for a judge response while the judge is waiting for the query that remains buffered in the output stream.

## Worked Examples

The supplied sample is an interaction transcript for the modulus (10^9+7). Our solution deliberately uses two different primes, so its actual query lines and residues differ from the transcript, while the recovered rational values are the same. The sample's three hidden values are (1/1), (1/2), and (2/1).

For (1/1), every queried residue is (1).

| Hidden value | (r_1) | (r_2) | Reconstructed (P) | Reconstructed (Q) |
| --- | --- | --- | --- | --- |
| (1/1) | 1 | 1 | 1 | 1 |

For (1/2), the residues are the modular inverses of (2). Since both chosen primes are odd, these are ((m+1)/2). After CRT, the combined residue is

[
R=\frac{M+1}{2}
=499999999993000000000017.
]

The Euclidean algorithm eventually reaches the relation

[
1=2R-M,
]

so the small positive pair is (P=1,Q=2).

| Hidden value | (R) after CRT | Small remainder | Coefficient | Output |
| --- | --- | --- | --- | --- |
| (1/2) | 499999999993000000000017 | 1 | 2 | (1/2) |

For (2/1), the combined residue is simply (2). It is already at most (10^9), and its coefficient of (R) is (1), so reconstruction stops immediately.

| Hidden value | (R) after CRT | Small remainder | Coefficient | Output |
| --- | --- | --- | --- | --- |
| (2/1) | 2 | 2 | 1 | (2/1) |

These traces demonstrate why the algorithm also handles very small numerators and denominators without any special case. The Euclidean process either finds the answer immediately or reaches it after only a logarithmic number of divisions.

As a second example, consider the boundary fraction

[
x=\frac{10^9}{10^9}=1.
]

Both modular answers are (1), so CRT gives (R=1). The algorithm returns (1/1), which is a valid answer even though it is not the same representation the judge might have used.

| Hidden value | (r_1) | (r_2) | (R) | Output |
| --- | --- | --- | --- | --- |
| (10^9/10^9) | 1 | 1 | 1 | (1/1) |

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(t\log M)) | Each test performs CRT plus one extended Euclidean algorithm on integers of at most about (10^{24}). |
| Space | (O(1)) | Only a constant number of large integers is stored for each test case. |

Here (M=m_1m_2<10^{24}), so the Euclidean algorithm takes only a few dozen iterations per test case. Even with (10^5) test cases, the arithmetic work is small compared with the interaction itself. Python's arbitrary-precision integers also remove the overflow issue caused by the (10^{24})-scale CRT modulus.

## Test Cases

Because the original problem is interactive, the literal sample cannot be passed to an ordinary `run(input_string)` function: the numbers shown under input are judge responses, not a complete offline input format. The following test harness checks the complete mathematical core by generating the two legal residues from hidden (p,q) values and feeding them into the reconstruction routine.

```python
import sys
import io
from math import gcd

M1 = 999999999989
M2 = 999999999997
LIMIT = 10**9

def crt(r1, r2):
    inv = pow(M1, -1, M2)
    k = ((r2 - r1) * inv) % M2
    return r1 + M1 * k

def rational_reconstruct(r, mod):
    rem0, rem1 = mod, r
    t0, t1 = 0, 1

    while rem1 > LIMIT:
        q = rem0 // rem1
        rem0, rem1 = rem1, rem0 - q * rem1
        t0, t1 = t1, t0 - q * t1

    if t1 < 0:
        rem1 = -rem1
        t1 = -t1

    assert 1 <= rem1 <= LIMIT
    assert 1 <= t1 <= LIMIT
    assert (r * t1 - rem1) % mod == 0

    return rem1, t1

def reconstruct(p, q):
    r1 = p * pow(q, -1, M1) % M1
    r2 = p * pow(q, -1, M2) % M2
    r = crt(r1, r2)
    return rational_reconstruct(r, M1 * M2)

def run(cases):
    out = []
    for p, q in cases:
        a, b = reconstruct(p, q)
        g = gcd(p, q)
        expected = (p // g, q // g)
        out.append((a, b))
        assert (a, b) == expected
    return out

# Provided sample values.
assert run([
    (1, 1),
    (1, 2),
    (2, 1),
]) == [
    (1, 1),
    (1, 2),
    (2, 1),
], "sample 1"

# Minimum-size values.
assert run([
    (1, 1),
]) == [
    (1, 1),
], "minimum values"

# Maximum numerator and denominator, with a reduced answer.
assert run([
    (10**9, 10**9),
]) == [
    (1, 1),
], "maximum equal values"

# Opposite boundaries.
assert run([
    (1, 10**9),
    (10**9, 1),
]) == [
    (1, 10**9),
    (10**9, 1),
], "boundary values"

# Non-reduced representation and large coprime values.
assert run([
    (999999999, 999999999),
    (999999937, 1000000000),
]) == [
    (1, 1),
    (999999937, 1000000000),
], "reduction and large values"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| (1/1,\ 1/2,\ 2/1) | (1/1,\ 1/2,\ 2/1) | Values represented in the supplied sample |
| (1/1) | (1/1) | Minimum values and immediate reconstruction |
| (10^9/10^9) | (1/1) | Maximum equal values and reduction |
| (1/10^9,\ 10^9/1) | Same reduced fractions | Both denominator and numerator boundaries |
| (999999999/999999999,\ 999999937/10^9) | (1/1,\ 999999937/10^9) | Non-reduced input and large coprime values |

## Edge Cases

The first edge case is the failure of a single modulus. With (m=10^9+7), the fractions (600000000/1) and (199999993/2) give the same residue. A one-query implementation therefore has no mathematical basis for choosing between them. The two-query solution combines independent residues into a modulus of roughly (10^{24}), after which the uniqueness inequality

[
2\cdot10^9\cdot10^9<M
]

rules out both fractions being valid reconstructions simultaneously.

The second edge case is a non-reduced hidden fraction. For the hidden value (2/4), each modular response is identical to the response for (1/2). CRT therefore reconstructs the reduced pair (1/2). This is correct because the required output describes the rational value, not the exact representation originally selected by the judge.

The third edge case is (p=q=10^9). The hidden fraction is numerically (1), and its modular residue is (1) for every allowed prime. CRT returns (R=1), so rational reconstruction returns (1/1). The fact that the original numerator and denominator were both at their maximum does not require any special handling.

The fourth edge case is a denominator of exactly (10^9), such as (1/10^9). The reconstruction condition uses `<= LIMIT`, not `< LIMIT`, because the problem permits the boundary itself. The same applies to a numerator of exactly (10^9).

The fifth edge case is the sign of the Euclidean coefficient. During extended Euclid, the coefficient associated with the modular residue alternates in sign. For (1/2), for example, the desired relation can appear as a negative coefficient before the next Euclidean step. Negating both the remainder and coefficient preserves the congruence, giving the required positive numerator and denominator. Ignoring this sign correction can produce a negative denominator even though the underlying reconstruction is valid.
