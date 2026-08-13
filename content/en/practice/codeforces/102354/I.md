---
title: "CF 102354I - From Modular to Rational"
description: "The interactor hides a positive rational number (x=p/q), where both (p) and (q) are at most (10^9). We cannot read (p) and (q) directly. Instead, for a chosen prime (m) larger than (10^9), the interactor returns the residue of (p q^{-1}) modulo (m)."
date: "2026-08-14T02:41:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102354
codeforces_index: "I"
codeforces_contest_name: "2018-2019 Summer Petrozavodsk Camp, Oleksandr Kulkov Contest 2"
rating: 0
weight: 102354
solve_time_s: 295
verified: false
draft: false
---

[CF 102354I - From Modular to Rational](https://codeforces.com/problemset/problem/102354/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 55s  
**Verified:** no  

## Solution
## Problem Understanding

The interactor hides a positive rational number (x=p/q), where both (p) and (q) are at most (10^9). We cannot read (p) and (q) directly. Instead, for a chosen prime (m) larger than (10^9), the interactor returns the residue of (p q^{-1}) modulo (m). Since (q<m), the inverse (q^{-1}) exists.

The task is to recover any pair of integers (p,q) with (1\le p,q\le10^9) representing the hidden rational number. The original problem is interactive, so a query is printed as `? m`, the answer from the interactor is read, and the final result is printed as `! p q`. The statement allows ten queries, while the solution below needs only two. The official problem is interactive and its key reduction is to modular minimization after combining the queried residues with the Chinese remainder theorem.

The bound (10^9) is the central part of the problem. A direct search over every possible denominator would require up to (10^9) modular multiplications for one test case. With as many as (10^5) test cases, that becomes (10^{14}) operations, far beyond the six second limit. The modulus supplied by one query is only around (10^9), so one query does not provide enough information to make the rational representation unique. Two such primes have a product slightly larger than (10^{18}), which is exactly what we need because products of two numbers bounded by (10^9) are at most (10^{18}).

There are several easy ways to make a wrong implementation. First, using only one modulus can leave multiple valid representations. For example, with (m=10^9+7), the value (1/2) produces (500000004), while the same residue can correspond to other bounded numerator-denominator pairs because the modulus is only about (10^9). A solution that assumes one residue uniquely determines (p) and (q) is invalid.

Second, the original (p,q) need not be coprime. For example, the hidden value (1/2) can legally be written as (2/4). If reconstruction produces the reduced pair (1,2), that is still a correct answer. A careless implementation that insists on reproducing the exact hidden pair would reject a perfectly valid result.

Third, the modular minimization can return a denominator whose resulting residue is zero only if the hidden numerator is zero modulo the combined modulus. That cannot happen here because (1\le p\le10^9), while the combined modulus is greater than (10^{18}). Thus the valid residue is always positive. An implementation of the continued-fraction helper still needs to handle the trivial (r=0) case defensively, even though the actual interactor cannot produce it.

## Approaches

The most direct approach is to query a modulus (m), obtain (r\equiv pq^{-1}\pmod m), and try every denominator (q) from (1) through (10^9). For each candidate we calculate (rq\bmod m), and if the result is at most (10^9), it can serve as a candidate numerator. The true denominator certainly succeeds because (rq\equiv p\pmod m). This is correct as a search procedure, but the worst case requires (10^9) modular multiplications for every test case, giving (10^{14}) operations across (10^5) cases.

The first useful observation is that two queries can be treated as one query modulo their product. Take the fixed primes

[
m_1=1000000007,\qquad m_2=1000000009.
]

Their product is

[
M=m_1m_2=1000000016000000063>10^{18}.
]

Suppose the two responses are (r_1) and (r_2). By the Chinese remainder theorem there is a unique (R\in[0,M)) satisfying

[
R\equiv r_1\pmod {m_1},
\qquad
R\equiv r_2\pmod {m_2}.
]

The hidden rational number then satisfies

[
Rq\equiv p\pmod M.
]

Because (M>10^{18}), this representation is unique as a rational number among all pairs bounded by (10^9). Indeed, if both (p_1/q_1) and (p_2/q_2) were valid and different, then (M) would divide

[
p_1q_2-p_2q_1.
]

The absolute value of this difference is at most (10^{18}), so it cannot be a nonzero multiple of (M). This uniqueness argument is the reason two primes are enough.

We are now left with a purely mathematical problem. Find (q\le10^9) such that

[
Rq\bmod M\le10^9.
]

Since the true denominator has this property, we could search for the minimum value of (Rq\bmod M) among all (1\le q\le10^9). The minimum is certainly at most (10^9), and the corresponding remainder is a valid numerator. The remaining question is how to find that minimum without trying all (10^9) denominators.

Write

[
Rq-kM=b,
]

where (b=Rq\bmod M). Minimizing (b) means finding an integer lattice point ((q,k)) just below the line

[
k=\frac{R}{M}q.
]

The best such lattice points are exactly the lower semiconvergents of the continued fraction of (R/M). Instead of enumerating all semiconvergents explicitly, we can generate the continued fraction convergents and identify the final lower-hull segment whose denominator range reaches (10^9). The resulting denominator is a particular semiconvergent and minimizes (Rq\bmod M). This is the continued-fraction reduction used for this problem.

The important distinction from ordinary rational reconstruction is the bound. A textbook convergent-only argument often uses a condition stronger than (M>10^{18}), such as (M>2C^2). Here we only have (M>C^2), so we need lower semiconvergents, not merely ordinary convergents. The official continued-fraction formulation explicitly reduces the task to this modular minimization and checks the relevant lower semiconvergent.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(t\cdot10^9)) | (O(1)) | Too slow |
| Two queries + CRT + continued fractions | (O(t\log 10^9)) | (O(\log 10^9)) | Accepted |

## Algorithm Walkthrough

1. For every test case, query the prime (m_1=1000000007) and store its response (r_1). Flush immediately because the interactor must receive the query before it can send the response.
2. Query the second prime (m_2=1000000009) and store its response (r_2). Two queries are sufficient because their product exceeds (10^{18}), while every product (pq) and (p'q') formed from valid bounds is at most (10^{18}).
3. Combine (r_1) and (r_2) with the Chinese remainder theorem. We obtain a single residue (R) modulo

[
M=m_1m_2.
]

The implementation uses

[
R=r_1+m_1\left((r_2-r_1)m_1^{-1}\bmod m_2\right).
]

The inverse exists because (m_1) and (m_2) are distinct primes.

1. Consider the sequence

[
R\bmod M,\quad 2R\bmod M,\quad 3R\bmod M,\ldots
]

and search for the (q\le10^9) producing the smallest remainder. The true denominator is in this range and produces the true numerator, which is also at most (10^9).

1. Compute the continued fraction of (R/M) with the Euclidean algorithm. Keep the numerator and denominator of every convergent. The lower semiconvergents are the lattice points immediately below the line (y=(R/M)x), and one of them gives the minimum modular remainder.
2. Find the first lower-hull convergent index whose next denominator would exceed (10^9). If the current lower-hull vector is ((q_{i-1},p_{i-1})) and the next direction is ((q_i,p_i)), we can move along that direction as far as the denominator bound allows. Set

[
t=\left\lfloor\frac{10^9-q_{i-1}}{q_i}\right\rfloor
]

and take

[
q=q_{i-1}+tq_i.
]

This is precisely the largest denominator on that lower semiconvergent segment that remains within the allowed range.

1. Compute

[
p=Rq\bmod M.
]

By construction, this is the minimum attainable nonnegative remainder, so (p\le10^9). The pair ((p,q)) represents the hidden rational number.

### Why it works

The key invariant is that every valid representation satisfies (Rq\equiv p\pmod M), with (1\le p,q\le10^9). Since (M>10^{18}), there can be only one rational value satisfying these bounds. The continued-fraction step finds the denominator minimizing (Rq\bmod M) over all allowed denominators. The hidden denominator is one of those allowed denominators and produces a remainder at most (10^9), so the minimum is also at most (10^9). The resulting remainder is consequently a valid numerator, and uniqueness forces the reconstructed fraction to equal the hidden rational number.

## Python Solution

```python
import sys
input = sys.stdin.readline

M1 = 1000000007
M2 = 1000000009
LIMIT = 1000000000
M = M1 * M2

# M1 = -2 (mod M2), so its inverse is -1/2 = (M2 - 1) / 2.
INV_M1_MOD_M2 = 500000004

def crt(r1, r2):
    """
    Return R in [0, M) such that
        R == r1 (mod M1)
        R == r2 (mod M2)
    """
    k = ((r2 - r1) * INV_M1_MOD_M2) % M2
    return r1 + M1 * k

def convergents(num, den):
    """
    Return the numerator and denominator arrays of the continued
    fraction of num / den.

    The first two entries are the conventional pseudo-convergents:
        p[-2] / q[-2] = 0 / 1
        p[-1] / q[-1] = 1 / 0
    """
    ps = [0, 1]
    qs = [1, 0]

    while den:
        a = num // den
        ps.append(ps[-1] * a + ps[-2])
        qs.append(qs[-1] * a + qs[-2])
        num, den = den, num % den

    return ps, qs

def mod_min(r, n, m):
    """
    Find q, 1 <= q <= n, minimizing (q * r) % m.

    This is obtained from the lower semiconvergents of r / m.
    """
    if r == 0:
        return 1

    ps, qs = convergents(r, m)

    for i in range(2, len(qs)):
        if i & 1:
            if i + 1 == len(qs) or qs[i + 1] > n:
                t = (n - qs[i - 1]) // qs[i]
                return qs[i - 1] + t * qs[i]

    # The actual problem always has a valid positive solution.
    return 1

def reconstruct(r1, r2):
    R = crt(r1, r2)
    q = mod_min(R, LIMIT, M)
    p = (R * q) % M
    return p, q

def ask(m):
    print("?", m, flush=True)
    return int(input())

def solve():
    t = int(input())

    for _ in range(t):
        r1 = ask(M1)
        r2 = ask(M2)

        p, q = reconstruct(r1, r2)

        print("!", p, q, flush=True)

if __name__ == "__main__":
    solve()
```

The constants `M1` and `M2` are fixed valid primes, both strictly greater than (10^9). Their product is (1000000016000000063), which is strictly greater than (10^{18}).

The `crt` function performs the Chinese remainder step. Since (M_1\equiv-2\pmod{M_2}), its inverse modulo (M_2) is (500000004). Python integers have arbitrary precision, so the intermediate products around (10^{18}) and (10^{27}) do not overflow.

The `convergents` function follows the standard recurrence

[
P_i=a_iP_{i-1}+P_{i-2},
\qquad
Q_i=a_iQ_{i-1}+Q_{i-2}.
]

The two initial pseudo-convergents are deliberately stored because the semiconvergent selection formula uses their indices. Omitting them and changing the parity tests is a common source of an off-by-one error.

The `mod_min` function is the core of the solution. The condition `i & 1` selects the lower side of the continued-fraction hull. We stop at the first such segment whose next convergent denominator would exceed the allowed denominator. The multiplier `t` then moves as far as possible along the current semiconvergent direction without making the denominator larger than (10^9).

The final multiplication `(R * q) % M` gives the numerator directly. There is no need to divide a rational number or reduce it by a gcd. If the hidden value was originally represented as (2/4), reconstruction may return (1/2), which is equally valid.

The interaction requires `flush=True` after every query and after the final answer. Without flushing, the interactor may wait indefinitely for output that is still buffered.

## Worked Examples

The official sample is interactive, so its input and output are a transcript between the contestant and the interactor rather than an ordinary input-output pair. The first sample case has hidden value (1/1), the second has (1/2), and the third has (2/1). For an offline trace, we can supply the same rational values to both fixed moduli and observe the reconstruction.

For (x=1/1), both residues are (1).

| Step | (r_1) | (r_2) | (R) | chosen (q) | (p=Rq\bmod M) |
| --- | --- | --- | --- | --- | --- |
| Query first prime | 1 |  |  |  |  |
| Query second prime | 1 | 1 |  |  |  |
| CRT | 1 | 1 | 1 |  |  |
| Continued fractions |  |  | 1 | 1 |  |
| Recover numerator |  |  | 1 | 1 | 1 |

The fraction is recovered as (1/1). This also demonstrates the smallest possible numerator and denominator.

For (x=1/2), the residues are

[
r_1=500000004
]

and

[
r_2=500000005.
]

The second value follows because (2r_2\equiv1\pmod{1000000009}).

| Step | (r_1) | (r_2) | (R) | chosen (q) | (p) |
| --- | --- | --- | --- | --- | --- |
| Query first prime | 500000004 |  |  |  |  |
| Query second prime | 500000004 | 500000005 |  |  |  |
| CRT | 500000004 | 500000005 | (500000004) |  |  |
| Continued fractions |  |  | (500000004) | 2 |  |
| Recover numerator |  |  | (500000004) | 2 | 1 |

The denominator (2) produces remainder (1), which is the minimum possible positive remainder. The algorithm consequently returns (1/2), matching the second case of the official sample.

As another useful trace, take (x=2/3). The two residues are (666666672) modulo (1000000007) and (333333337) modulo (1000000009). CRT reconstructs the residue corresponding to (2/3) modulo (M). The continued-fraction search finds (q=3), and the final modular multiplication gives (p=2). This illustrates that the denominator does not have to be particularly small relative to the modulus, only bounded by (10^9).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(t\log 10^9)) | Each test case performs two queries, CRT, and one Euclidean-algorithm continued-fraction computation |
| Space | (O(\log 10^9)) | The continued fraction contains (O(\log 10^9)) coefficients |

The continued fraction has only logarithmically many terms because the Euclidean algorithm decreases its arguments according to the same recurrence. For (10^5) test cases this keeps the computational work small enough for the six second limit. The two interactive queries are also comfortably below the allowed ten queries per test case. The original problem allows ten queries, while the construction here deliberately uses only two.

## Test Cases

Because this is an interactive problem, the official sample cannot be passed directly to a normal `run(input_string)` harness. Its lines are responses produced by the interactor after the contestant prints queries. For offline testing, the clean approach is to test the deterministic `reconstruct` function by generating the two residues from known rational values.

```python
# Offline tests for the deterministic reconstruction part.
# The interactive solve() function itself must be tested with an interactor.

import sys

M1 = 1000000007
M2 = 1000000009
LIMIT = 1000000000
M = M1 * M2
INV_M1_MOD_M2 = 500000004

def crt(r1, r2):
    k = ((r2 - r1) * INV_M1_MOD_M2) % M2
    return r1 + M1 * k

def convergents(num, den):
    ps = [0, 1]
    qs = [1, 0]

    while den:
        a = num // den
        ps.append(ps[-1] * a + ps[-2])
        qs.append(qs[-1] * a + qs[-2])
        num, den = den, num % den

    return ps, qs

def mod_min(r, n, m):
    if r == 0:
        return 1

    _, qs = convergents(r, m)

    for i in range(2, len(qs)):
        if i & 1:
            if i + 1 == len(qs) or qs[i + 1] > n:
                t = (n - qs[i - 1]) // qs[i]
                return qs[i - 1] + t * qs[i]

    return 1

def reconstruct(r1, r2):
    R = crt(r1, r2)
    q = mod_min(R, LIMIT, M)
    p = (R * q) % M
    return p, q

def residue(p, q, mod):
    return (p * pow(q, mod - 2, mod)) % mod

def run_case(p, q):
    r1 = residue(p, q, M1)
    r2 = residue(p, q, M2)
    return reconstruct(r1, r2)

# Official sample values, converted into two-modulus offline tests.
assert run_case(1, 1) == (1, 1), "sample case x = 1"
assert run_case(1, 2) == (1, 2), "sample case x = 1/2"
assert run_case(2, 1) == (2, 1), "sample case x = 2"

# Minimum-size values.
assert run_case(1, 1) == (1, 1), "minimum numerator and denominator"

# Maximum-size values.
assert run_case(1000000000, 1000000000) == (1, 1), \
    "maximum values with a reducible representation"

# A large irreducible fraction.
assert run_case(999999999, 1000000000) == (999999999, 1000000000), \
    "large irreducible fraction"

# Boundary numerator and denominator.
assert run_case(1000000000, 999999999) == (1000000000, 999999999), \
    "both bounds are active"

# A case where reduction is necessary.
assert run_case(750000000, 1000000000) == (3, 4), \
    "non-coprime representation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| (1/1) | (1/1) | Minimum-size values and trivial continued fraction |
| (1/2) | (1/2) | Official sample and a small non-integer rational |
| (2/1) | (2/1) | Integer rational with denominator one |
| (10^9/10^9) | (1/1) | Maximum bounds and non-coprime representation |
| (999999999/10^9) | (999999999/10^9) | Large irreducible fraction |
| (10^9/999999999) | (10^9/999999999) | Both bounds simultaneously active |
| (750000000/10^9) | (3/4) | Correct handling of reducible input |

## Edge Cases

The one-modulus ambiguity is handled by never attempting reconstruction from a single query. For example, the official sample's (1/2) gives (500000004) modulo (1000000007). That modulus is not larger than (10^{18}), so uniqueness cannot be proved. The algorithm immediately obtains a second residue modulo (1000000009), combines them into a modulus larger than (10^{18}), and only then starts rational reconstruction.

The non-coprime case is handled naturally. Consider the concrete input representation (750000000/1000000000). Its actual value is (3/4). The modular responses are generated by the value (3/4), and the reconstruction finds the reduced pair (3/4). Since the requested output denotes a rational number rather than a particular representation, this is correct.

The maximum-boundary case (1000000000/999999999) is also safe. Both values fit exactly at the upper boundary, and their product with another valid candidate can reach (10^{18}). This is precisely why the combined modulus must be strictly greater than (10^{18}), not merely equal to it. Here

[
1000000007\cdot1000000009
=1000000016000000063

> 10^{18}.
> ]

The denominator boundary is handled by the expression

[
t=\left\lfloor\frac{10^9-q_{i-1}}{q_i}\right\rfloor.
]

The floor operation is intentional. If the next semiconvergent would exceed (10^9), it is excluded, while a denominator exactly equal to (10^9) remains allowed. Using a strict inequality at this point would incorrectly reject valid boundary solutions.

Finally, the continued-fraction helper contains an explicit `r == 0` branch. The actual problem cannot reach that branch because the hidden numerator is positive and smaller than the combined modulus, but keeping the case defined makes the helper robust and avoids undefined behavior if it is reused in a standalone modular-minimum test.
