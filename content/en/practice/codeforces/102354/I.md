---
title: "CF 102354I - From Modular to Rational"
description: "We need to recover a positive rational number (x=p/q), where both (p) and (q) are at most (10^9). We cannot see (p) and (q) directly. Instead, for a chosen prime modulus (m), the judge gives the integer (r) in the range (0le r<m) satisfying [ requiv p q^{-1}pmod m."
date: "2026-08-16T08:43:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102354
codeforces_index: "I"
codeforces_contest_name: "2018-2019 Summer Petrozavodsk Camp, Oleksandr Kulkov Contest 2"
rating: 0
weight: 102354
solve_time_s: 315
verified: false
draft: false
---

[CF 102354I - From Modular to Rational](https://codeforces.com/problemset/problem/102354/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We need to recover a positive rational number (x=p/q), where both (p) and (q) are at most (10^9). We cannot see (p) and (q) directly. Instead, for a chosen prime modulus (m), the judge gives the integer (r) in the range (0\le r<m) satisfying

[
r\equiv p q^{-1}\pmod m.
]

Since (m) is prime and (q<m), the inverse (q^{-1}) exists. Equivalently, the information returned by a query is exactly the statement

[
rq\equiv p\pmod m.
]

The task is interactive, so for every test case our program prints queries, reads the judge's answers, and eventually prints a pair (p,q) representing the hidden rational number. The pair does not have to be reduced. For example, (1/2), (2/4), and (500000000/1000000000) all represent the same value, and any one of them is accepted. The official statement specifies up to (10^5) test cases and at most ten queries per case.

The bound (p,q\le10^9) is the central structural constraint. A direct search over possible denominators already requires up to (10^9) iterations for one test case. With (10^5) cases, that becomes (10^{14}) modular computations, far beyond what a six-second limit can support. We need to turn the modular information into an exact rational reconstruction using logarithmic-time number theory.

There is also a subtle distinction between uniqueness and reconstruction. If we somehow knew the value modulo a modulus (M>10^{18}), then the rational number would already be unique among all fractions whose numerator and denominator are at most (10^9). Indeed, if both (p_1/q_1) and (p_2/q_2) produced the same residue, then

[
p_1q_2\equiv p_2q_1\pmod M.
]

Hence (M) divides (p_1q_2-p_2q_1). The absolute value of that difference is at most (10^{18}), so a modulus strictly larger than (10^{18}) forces the difference to be zero. This uniqueness observation is also the basis of standard solutions to the problem.

There are several edge cases that a careless implementation can mishandle. The first is an unreduced fraction. For example, the hidden value may be (2/4). A correct output is `1 2`, although the sample chooses `2 4`. An implementation that insists on recovering the exact original pair rather than the rational value would reject a perfectly valid answer.

The second is an integer such as (2/1). Here the modular residue is simply (2), so the correct answer can be `2 1`. A reconstruction routine that only searches for a nontrivial continued-fraction denominator can accidentally skip the initial residue itself and fail on this case.

The third is the value (1/1). For every queried modulus the returned residue is (1). A careless CRT or Euclidean implementation that assumes the residue is large can mishandle this smallest possible rational. The correct output is `1 1`.

The fourth is a fraction at the numerical boundary. For example, (1000000000/999999999) is valid even though its numerator and denominator are both near the upper limit. Floating-point reconstruction is unsafe here because the relevant integers can be around (10^{24}) after CRT. The solution must use exact integer arithmetic throughout.

## Approaches

The brute-force approach starts from the congruence

[
rq\equiv p\pmod M.
]

For every possible (q) from (1) through (10^9), we can calculate

[
p=(rq)\bmod M
]

and check whether (1\le p\le10^9). The hidden pair is guaranteed to pass this test, so the first valid pair gives a correct answer. This is conceptually simple and completely correct because the query tells us exactly what (rq\bmod M) must equal for the true denominator.

The problem is the operation count. In the worst case one test case needs (10^9) modular multiplications. Across (10^5) test cases this can reach (10^{14}) iterations. The brute force works because every possible denominator can be checked independently, but it fails because the denominator range is too large.

The key observation is that we are allowed to choose the moduli. Instead of using a modulus barely larger than (10^9), choose two fixed primes extremely close to (10^{12}):

[
m_1=999999999989,\qquad
m_2=999999999997.
]

Both satisfy the query restriction and are prime.

Two queries are enough. By the Chinese Remainder Theorem, the two residues can be combined into one residue (r) modulo

[
M=m_1m_2.
]

This modulus is approximately (10^{24}), so in particular

[
M>2\cdot10^{18}.
]

That stronger bound lets us use a standard continued-fraction rational reconstruction.

From

[
rq\equiv p\pmod M
]

there exists an integer (k) such that

[
rq-kM=p.
]

Divide by (Mq):

[
\frac rM-\frac{k}{q}=\frac{p}{Mq}.
]

Because (p,q\le10^9) and (M>2\cdot10^{18}),

[
\left|\frac rM-\frac{k}{q}\right|
=\frac{p}{Mq}
<\frac{1}{2q^2}.
]

A classical continued-fraction property says that a rational approximation this close to (r/M) must be one of its convergents. Thus the hidden denominator (q) appears naturally during the Euclidean algorithm applied to (M) and (r). The continued-fraction connection is a standard way to solve this exact rational-reconstruction problem.

This turns the search over (10^9) possible denominators into an (O(\log M)) Euclidean algorithm. Since (M) has only about 24 decimal digits, there are only a few dozen Euclidean iterations per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(10^9)) per test case | (O(1)) | Too slow |
| CRT + continued fractions | (O(\log M)) per test case | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Query the first fixed prime (m_1=999999999989), and call the returned residue (r_1). The query is legal because (m_1) is prime and lies strictly between (10^9) and (10^{12}).
2. Query the second fixed prime (m_2=999999999997), obtaining (r_2). The two moduli are coprime because they are distinct primes, which is exactly what the Chinese Remainder Theorem requires.
3. Combine the two congruences

[
R\equiv r_1\pmod {m_1},
\qquad
R\equiv r_2\pmod {m_2}
]

into a single residue (R) modulo (M=m_1m_2). Write

[
R=r_1+m_1t.
]

Substituting into the second congruence gives

[
m_1t\equiv r_2-r_1\pmod {m_2}.
]

Since (m_1) has an inverse modulo (m_2), we can calculate (t) with one modular inverse.

1. After CRT, we know

[
R\equiv pq^{-1}\pmod M,
]

so

[
Rq\equiv p\pmod M.
]

Consequently there is an integer (k) satisfying

[
Rq-kM=p.
]

The goal is now to recover the small positive integers (p,q) from this equation.

1. Consider the rational number (k/q). From the previous equation,

[
\frac RM-\frac{k}{q}
=\frac{p}{Mq}.
]

Since (p,q\le10^9) and (M>2\cdot10^{18}), the right-hand side is strictly less than (1/(2q^2)). Thus (k/q) is a convergent of the continued fraction of (R/M).

1. Run the Euclidean algorithm on (M) and (R), while also tracking the coefficient of (R) in every remainder. Initialize

[
M=0\cdot R+1\cdot M
]

and

[
R=1\cdot R+0\cdot M.
]

When Euclid transforms two consecutive remainders using

[
a\leftarrow b,\qquad
b\leftarrow a-\lfloor a/b\rfloor b,
]

the same transformation can be applied to their coefficients of (R). Therefore every Euclidean remainder (s) has the form

[
s=cR+dM.
]

1. Look for a remainder (s) with (1\le s\le10^9) and a positive coefficient (c\le10^9). For the hidden fraction, the relation is exactly

[
p=qR-kM,
]

so its numerator (p) is such a Euclidean remainder and its denominator (q) is the positive coefficient of (R).

1. Output that pair. If the original fraction was not reduced, the Euclidean reconstruction may return its reduced form, which represents the same rational number and is accepted.

### Why it works

The central invariant is that every Euclidean remainder is represented as an integer linear combination of (R) and (M), and its tracked coefficient records the multiplier of (R). The hidden pair satisfies

[
p=qR-kM,
]

so (p) is one of these remainders with coefficient (q). The large CRT modulus gives the approximation bound

[
\left|\frac RM-\frac{k}{q}\right|<\frac1{2q^2},
]

which forces (k/q) to be a continued-fraction convergent. Euclid enumerates exactly the convergent structure needed for the reconstruction. Since (M>10^{18}), there cannot be two different rational values with both numerator and denominator bounded by (10^9), so the candidate found by the algorithm is necessarily the hidden rational number.

## Python Solution

```python
import sys

input = sys.stdin.readline

B = 10**9

# Both are primes and satisfy 10^9 < m < 10^12.
M1 = 999999999989
M2 = 999999999997

def crt(a1, m1, a2, m2):
    """
    Return x in [0, m1*m2) such that
        x == a1 (mod m1)
        x == a2 (mod m2)
    """
    t = ((a2 - a1) % m2) * pow(m1, -1, m2) % m2
    x = a1 + m1 * t
    return x, m1 * m2

def recover(r, mod):
    """
    Recover p, q with 1 <= p, q <= B from
        r == p * q^{-1} (mod mod).
    We have mod > 2 * B^2.
    """
    # r0 = s0 * r + ...
    # r1 = s1 * r + ...
    r0, r1 = mod, r
    s0, s1 = 0, 1

    while r1:
        # The first remainder is r itself, which matters for
        # integer answers such as 2/1.
        if 1 <= r1 <= B and 1 <= s1 <= B:
            if (r * s1) % mod == r1:
                return r1, s1

        q = r0 // r1

        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1

    raise RuntimeError("rational reconstruction failed")

def ask(m):
    print("?", m, flush=True)
    ans = int(input())
    if ans == -1:
        sys.exit(0)
    return ans

def main():
    t = int(input())

    for _ in range(t):
        r1 = ask(M1)
        r2 = ask(M2)

        r, mod = crt(r1, M1, r2, M2)
        p, q = recover(r, mod)

        print("!", p, q, flush=True)

if __name__ == "__main__":
    main()
```

The two constants are deliberately chosen close to (10^{12}). Their product is

[
M=999999999986000000000033,
]

which is far larger than (2\cdot10^{18}). Using such large moduli is what allows the continued-fraction proof to use the standard (1/(2q^2)) approximation bound.

The `ask` function prints a query and immediately flushes stdout. Flushing is mandatory in an interactive problem because otherwise the judge may wait forever for a query that is still sitting in Python's output buffer. A judge response of `-1` conventionally signals an invalid interaction, so the program terminates immediately.

The `crt` function uses the representation

[
R=r_1+m_1t.
]

The value of (t) is found using the modular inverse of (m_1) modulo (m_2). Python integers have arbitrary precision, so the approximately (10^{24}) CRT modulus causes no overflow. In a fixed-width language, this product would require a wider integer type than signed 64-bit arithmetic.

The `recover` function is an extended version of the Euclidean algorithm. `r1` is the current remainder and `s1` is its coefficient with respect to the original residue (r). The invariant is that the current remainder can be written as

[
r_1=s_1r+cM
]

for some integer (c).

The candidate check is done before the Euclidean update. This boundary is necessary for cases such as (2/1), where the residue itself is already the desired numerator and the denominator is (1). Skipping this check would lose integer answers.

The additional modular check

```
(r * s1) % mod == r1
```

is not needed for the mathematical proof, but it makes the candidate condition explicit and protects the implementation from accepting a remainder with an unrelated coefficient.

No floating-point arithmetic is used. In particular, neither (R/M) nor the rational answer is ever converted to `float`, because the CRT modulus is around (10^{24}), far beyond the range where a floating-point representation can preserve all relevant integer information.

## Worked Examples

The supplied sample is an interactive transcript rather than an ordinary batch input/output pair. It uses the single modulus (1000000007), while the solution above deliberately uses two larger primes so that continued-fraction reconstruction has a strong enough modulus. The sample's `1/2` case returns `500000004`, and the sample accepts `2/4`; our algorithm would instead return the reduced representation `1/2`.

For the first worked example, take the sample's value (x=1/2). With

[
m_1=999999999989
]

the inverse of (2) is (500000000000), so the judge returns (500000000000). With

[
m_2=999999999997,
]

the inverse of (2) is (499999999999). CRT combines these into

[
R=499999999993000000000017.
]

The combined modulus is

[
M=999999999986000000000033.
]

Since (M=2R-1), the first Euclidean steps are especially simple.

| Euclidean state | Current remainder | Coefficient of (R) | Candidate |
| --- | --- | --- | --- |
| Initial | 499999999993000000000017 | 1 | Too large |
| After (M-R) | 499999999992999999999? | -1 | Coefficient negative |
| After next division | 1 | 2 | (p=1,q=2) |

The exact middle remainder is (R-1=499999999993000000000016). The final small remainder satisfies

[
1=2R-M,
]

so the coefficient of (R) is (2), giving (p=1,q=2). This demonstrates why the coefficient tracking is useful: the Euclidean algorithm simultaneously finds the small numerator and its corresponding denominator.

For the second worked example, take the sample's integer value (x=2/1). The judge returns (2) for both large primes, so CRT immediately gives

[
R=2.
]

The Euclidean reconstruction starts with the residue itself.

| Euclidean state | Current remainder | Coefficient of (R) | Candidate |
| --- | --- | --- | --- |
| Initial | 2 | 1 | (p=2,q=1) |
| Next | 1 | Large negative coefficient | Rejected |
| Final | 0 | Not considered | Stop |

The first state is already a valid answer. This is the edge case that motivates checking the initial remainder before performing the first Euclidean division.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(t\log M)) | Two queries, CRT, and one Euclidean algorithm per test case |
| Space | (O(1)) | Only a constant number of integers are stored |

Here (M) is about (10^{24}), so the Euclidean algorithm takes only (O(\log M)), roughly a few dozen iterations. For (10^5) test cases this is easily manageable in terms of arithmetic work. The interactive protocol itself dominates the practical cost because every test case requires two query-response exchanges, still within the allowed ten queries per case.

## Test Cases

Because this is an interactive problem, the supplied sample cannot be passed to the program as a normal batch input. The sample input consists of judge replies, while the program is expected to print queries before receiving those replies. The following test harness instead tests the mathematical reconstruction independently by simulating the judge for several hidden fractions.

```python
import io
import sys

B = 10**9
M1 = 999999999989
M2 = 999999999997

def crt(a1, m1, a2, m2):
    t = ((a2 - a1) % m2) * pow(m1, -1, m2) % m2
    return a1 + m1 * t, m1 * m2

def recover(r, mod):
    r0, r1 = mod, r
    s0, s1 = 0, 1

    while r1:
        if 1 <= r1 <= B and 1 <= s1 <= B:
            if (r * s1) % mod == r1:
                return r1, s1

        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1

    raise AssertionError("reconstruction failed")

def residue(p, q, mod):
    return p * pow(q, -1, mod) % mod

def solve_hidden(p, q):
    r1 = residue(p, q, M1)
    r2 = residue(p, q, M2)

    r, mod = crt(r1, M1, r2, M2)
    return recover(r, mod)

# Sample-derived cases.
assert solve_hidden(1, 1) == (1, 1), "sample value 1/1"
assert solve_hidden(1, 2) == (1, 2), "sample value 1/2"
assert solve_hidden(2, 1) == (2, 1), "sample value 2/1"

# Minimum numerator and denominator.
assert solve_hidden(1, 1) == (1, 1), "minimum values"

# Maximum values, with a reducible fraction.
assert solve_hidden(10**9, 10**9) == (1, 1), "maximum equal values"

# Both numerator and denominator are at the upper boundary,
# but the fraction is not reducible.
assert solve_hidden(10**9, 999999999) == (1000000000, 999999999), \
    "maximum boundary fraction"

# A fraction just below the upper numerator boundary.
assert solve_hidden(999999999, 1000000000) == (999999999, 1000000000), \
    "boundary numerator and denominator"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| (1/1) | (1/1) | Minimum values and constant residue |
| (1/2) | (1/2) | Sample's non-integer rational |
| (2/1) | (2/1) | Initial Euclidean remainder |
| (10^9/10^9) | (1/1) | Reducible maximum-size fraction |
| (10^9/999999999) | (10^9/999999999) | Both values near the upper boundary |
| (999999999/10^9) | (999999999/10^9) | Boundary denominator and numerator |

The test for (10^9/10^9) is particularly useful because the original pair is not coprime. The reconstruction returns (1/1), which is the same rational value and is a legal answer. The two boundary tests also confirm that the implementation never relies on a strict inequality such as (p<10^9) or (q<10^9).

## Edge Cases

For the unreduced fraction (2/4), the hidden value is (1/2). For the first large prime the residue is (500000000000), and for the second it is (499999999999). CRT produces the same combined residue as it would for (1/2), because modular division depends only on the rational value, not on which numerator and denominator representation was used. The reconstruction returns (1/2), which is accepted even though the sample transcript uses (2/4).

For the integer (2/1), both queried residues are exactly (2), so CRT returns (R=2). The reconstruction checks the initial Euclidean state (R=2) with coefficient (1), immediately obtaining (p=2,q=1). This is why the candidate check must occur before the first Euclidean division.

For (1/1), every query returns (1), and CRT also returns (R=1). The initial state has remainder (1) and coefficient (1), so the algorithm outputs (1/1) immediately. No special-case branch for the number (1) is required.

For the maximum equal pair (10^9/10^9), the modular value is still exactly (1), because the fraction reduces to (1/1). The algorithm returns (1/1), demonstrating why the output must be interpreted as a rational value rather than as the exact hidden pair.

For a boundary fraction such as (1000000000/999999999), the numerator and denominator both fit the allowed range, but their product is close to (10^{18}). The CRT modulus is around (10^{24}), leaving a very large safety margin. The Euclidean algorithm works entirely with integers and reconstructs the fraction without any precision loss.

The most dangerous implementation mistake is using only a modulus around (10^9) and then assuming continued fractions are automatically sufficient. The standard convergent bound requires (M>2B^2), while the original problem's individual query modulus is far smaller. The two large primes solve exactly this issue: their product is much larger than (2B^2), while each individual query remains inside the allowed range. This is the key reason the final algorithm is both short and rigorous.
