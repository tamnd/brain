---
title: "CF 102412A - The One Polynomial Man"
description: "We have a prime modulus (p), a subset (S) of residues modulo (p), and another subset (V). For every ordered pair ((a,b)) with both values in (S), we evaluate [ F(a,b)= frac{(2a+3b)^2+5a^2}{(3a+b)^2} + frac{(2a+5b)^2+3b^2}{(3a+2b)^2} pmod p."
date: "2026-08-11T08:27:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102412
codeforces_index: "A"
codeforces_contest_name: "MEX Foundation Contest (supported by AIM Tech)"
rating: 0
weight: 102412
solve_time_s: 500
verified: true
draft: false
---

[CF 102412A - The One Polynomial Man](https://codeforces.com/problemset/problem/102412/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a prime modulus (p), a subset (S) of residues modulo (p), and another subset (V). For every ordered pair ((a,b)) with both values in (S), we evaluate

[
F(a,b)=
\frac{(2a+3b)^2+5a^2}{(3a+b)^2}
+
\frac{(2a+5b)^2+3b^2}{(3a+2b)^2}
\pmod p.
]

The pair is counted exactly when every denominator that appears is nonzero and (F(a,b)) belongs to (V). The product in the original formulation is just a compact way of saying that at least one factor (F(a,b)-z) is zero for some (z\in V).

The prime (p) can be as large as (10^6), while (S) and (V) can each contain all (p) residues. A direct scan over all ordered pairs can consequently perform about (p^2), or up to (10^{12}), pair checks. A four-second limit rules that out completely. The useful target is roughly (O(p\log p)), which is the scale of an FFT or NTT over an array of size proportional to (p). The original contest solution uses precisely this reduction.

There are three edge cases that deserve separate treatment.

First, the pair ((0,0)) must never be counted. For example,

```
2
1
0
1
0
```

has only the pair ((0,0)), but both denominators are zero, so the answer is `0`. A careless implementation that substitutes (a/b) without first removing zero values has no valid ratio for this pair and can accidentally treat it as a special ratio.

Second, pairs with exactly one zero have perfectly valid denominators and must not be discarded. For (a=0,b\ne0), the expression is (16). For (a\ne0,b=0), it is (13/9). For example,

```
7
2
0 1
2
2 3
```

contains the pair ((0,1)), whose value is (16\equiv2\pmod7), and the pair ((1,0)), whose value is (13/9\equiv3\pmod7). The pair ((1,1)) has value (0), which is not in (V), and ((0,0)) is invalid. The correct output is `2`. An implementation that simply removes zero from (S) loses these two valid ordered pairs.

Third, even for nonzero (a,b), a ratio can make a denominator vanish. For example, with (p=7), (3a+b=0) means (a/b=2), while (3a+2b=0) means (a/b=4). Thus for

```
7
2
1 2
1
0
```

the ratios (1) and (1) from the pairs ((1,1)) and ((2,2)) are valid and give value (0), while the pairs ((1,2)) and ((2,1)) have ratio (4) and (2), respectively, so a denominator is zero. The correct output is `2`. Simply evaluating the rational expression after modular inversion without checking its denominators can produce an unrelated value.

## Approaches

The brute-force solution is straightforward. For every (a\in S) and every (b\in S), check the two denominators, compute the two modular fractions, obtain (F(a,b)), and test whether that value belongs to (V). This is correct because every ordered pair is examined exactly once. The problem is the (p^2) pair count. At (p=10^6), there can be (10^{12}) pairs, before even accounting for modular inverses or membership checks. That is far beyond what the time limit permits.

The structure that saves us is homogeneity. Every numerator and denominator in the expression has degree two in (a,b). Consequently, when (a\ne0) and (b\ne0), multiplying both variables by the same nonzero value does not change the result. The value depends only on the ratio

[
t=\frac{a}{b}\pmod p.
]

This observation reduces the algebraic part from all (p^2) pairs to only (p-1) possible nonzero ratios. The intended solution first evaluates the expression for every such ratio and records which ratios produce a value belonging to (V).

We can then forget the complicated rational function. The remaining problem is to count pairs (a,b\in S) satisfying

[
a b^{-1}\in L,
]

where (L) is the set of accepted ratios.

A normal convolution handles addition, not multiplication. The multiplicative group of nonzero residues modulo a prime is cyclic, however. Choose a primitive root (g). Every nonzero residue can be written uniquely as (g^x), where (0\le x<p-1). If (a=g^x) and (b=g^y), then

[
\frac ab=g^{x-y}.
]

The multiplicative ratio has become a difference of exponents. We can count these differences with a cyclic convolution. One convenient formulation convolves the indicator of (S) with the indicator of (L). At exponent (x), the convolution counts choices of (y) and (r) with (y+r=x), exactly corresponding to (r=x-y), hence to (a/b). This is the central transformation described by the standard solution.

Since the convolution coefficients are at most (p), we can use the NTT modulus (998244353) without ambiguity. The largest convolution coefficient is at most (10^6), much smaller than the NTT modulus. We use an NTT length that is the next power of two above (2(p-1)-1), which is at most (2^{21}).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(p^2\log p)) with direct modular inversion | (O(p)) | Too slow |
| Ratio reduction + NTT | (O(p\log p)) | (O(p)) | Accepted |

## Algorithm Walkthrough

1. Read (p), (S), and (V), and build constant-time membership arrays for both sets. We also separate zero from the nonzero elements of (S), because the ratio (a/b) exists only when both values are nonzero.
2. Handle pairs with exactly one zero. If (0\in S), every nonzero (x\in S) creates two ordered pairs, ((0,x)) and ((x,0)). The first has value (16), while the second has value (13/9). Add the corresponding counts whenever those values belong to (V). The pair ((0,0)) is always invalid.
3. Find a primitive root (g) modulo (p). Factor (p-1), then test candidates (g) until (g^{(p-1)/q}\ne1\pmod p) for every distinct prime factor (q) of (p-1). This guarantees that the powers of (g) enumerate every nonzero residue exactly once.
4. Build a discrete-logarithm array. Starting with (x=1), repeatedly multiply by (g). At exponent (e), record that the current residue has logarithm (e). After (p-1) iterations, every nonzero residue has a known exponent.
5. Precompute modular inverses of all nonzero residues using the standard linear recurrence

p-\left\lfloor\frac pi\right\rfloor
\operatorname{inv}[p\bmod i]\pmod p.
]

This avoids performing a separate (O(\log p)) exponentiation for every ratio.

1. Enumerate every nonzero ratio (t). The denominators are

[
(3t+1)^2
\quad\text{and}\quad
(3t+2)^2.
]

If either (3t+1) or (3t+2) is zero modulo (p), skip this ratio because the original expression explicitly forbids division by zero.

1. For every remaining (t), substitute (a=t,b=1). The resulting value is

[
G(t)=
\frac{(2t+3)^2+5t^2}{(3t+1)^2}
+
\frac{(2t+5)^2+3}{(3t+2)^2}.
]

If (G(t)\in V), mark the discrete logarithm of (t) in the second convolution array.

1. Build the first convolution array from (S). If (x\in S) and (x\ne0), put a one at index (\log_g x). Build the second array from the accepted ratios, putting a one at index (\log_g t).
2. Compute their ordinary convolution with NTT. If the exponent arrays contain (y) and (r), a coefficient at (y+r) counts a pair satisfying

[
\log_g(a)+\log_g(t)=\log_g(a),
]

after interpreting the first exponent as the exponent of (b). More directly, for a desired numerator exponent (x), the equality (y+r=x) is exactly (r=x-y), which means (t=g^{x-y}=a/b).

1. Fold the second half of the convolution back by (p-1). Exponents live modulo (p-1), so coefficient (k+(p-1)) represents the same multiplicative-group exponent as coefficient (k).
2. For every nonzero (a\in S), add the cyclic-convolution coefficient at (\log_g a). That coefficient counts exactly the choices of (b\in S) for which (a/b) is an accepted ratio. Add the zero-case contribution from step 2 to obtain the final answer.

### Why it works

For every nonzero pair ((a,b)), write (a=g^x) and (b=g^y). The expression is homogeneous of degree zero, so its value depends only on (a/b=g^{x-y}). The ratio preprocessing marks exactly those exponents (r=x-y) for which the expression is defined and belongs to (V). The cyclic convolution counts exactly the pairs of exponents satisfying (x=y+r), which is equivalent to (r=x-y). Thus every valid nonzero ordered pair contributes once, and no invalid pair contributes. The separately handled zero cases cover every pair for which the ratio representation is unavailable.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

NTT_MOD = 998244353
NTT_ROOT = 3

def factorize(n):
    factors = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors.append(n)
    return factors

def primitive_root(p):
    if p == 2:
        return 1

    factors = factorize(p - 1)
    for g in range(2, p):
        ok = True
        for q in factors:
            if pow(g, (p - 1) // q, p) == 1:
                ok = False
                break
        if ok:
            return g
    return -1

def ntt(a, invert, rev):
    n = len(a)

    for i in range(n):
        j = rev[i]
        if i < j:
            a[i], a[j] = a[j], a[i]

    length = 2
    while length <= n:
        wlen = pow(
            NTT_ROOT,
            (NTT_MOD - 1) // length,
            NTT_MOD
        )
        if invert:
            wlen = pow(wlen, NTT_MOD - 2, NTT_MOD)

        half = length >> 1

        for start in range(0, n, length):
            w = 1
            end = start + half
            j = start

            while j < end:
                u = a[j]
                v = a[j + half] * w % NTT_MOD

                x = u + v
                if x >= NTT_MOD:
                    x -= NTT_MOD

                y = u - v
                if y < 0:
                    y += NTT_MOD

                a[j] = x
                a[j + half] = y

                w = w * wlen % NTT_MOD
                j += 1

        length <<= 1

    if invert:
        inv_n = pow(n, NTT_MOD - 2, NTT_MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % NTT_MOD

def convolution(a, b):
    need = len(a) + len(b) - 1
    n = 1
    while n < need:
        n <<= 1

    fa = a + [0] * (n - len(a))
    fb = b + [0] * (n - len(b))

    rev = array('I', [0]) * n
    half = n >> 1
    for i in range(1, n):
        rev[i] = (rev[i >> 1] >> 1) | ((i & 1) * half)

    ntt(fa, False, rev)
    ntt(fb, False, rev)

    for i in range(n):
        fa[i] = fa[i] * fb[i] % NTT_MOD

    del fb

    ntt(fa, True, rev)
    return fa[:need]

def solve():
    p = int(input())

    n = int(input())
    s = list(map(int, input().split())) if n else []

    m = int(input())
    v = list(map(int, input().split())) if m else []

    in_s = bytearray(p)
    for x in s:
        in_s[x] = 1

    in_v = bytearray(p)
    for x in v:
        in_v[x] = 1

    ans = 0

    has_zero = in_s[0]

    # Handle (0, b), b != 0.
    # The value is 16.
    if has_zero and in_v[16 % p]:
        ans += n - 1

    # Handle (a, 0), a != 0.
    # The value is 13 / 9.
    # If 9 == 0 mod p, the denominator is zero and no such pair is valid.
    if has_zero and 9 % p != 0:
        value = 13 * pow(9, p - 2, p) % p
        if in_v[value]:
            ans += n - 1

    nonzero_count = n - (1 if has_zero else 0)

    if nonzero_count == 0 or m == 0:
        print(ans)
        return

    q = p - 1

    # Find a primitive root and construct discrete logarithms.
    g = primitive_root(p)

    log = array('i', [-1]) * p
    cur = 1
    for e in range(q):
        log[cur] = e
        cur = cur * g % p

    # Linear-time modular inverses.
    inv = array('I', [0]) * p
    if p > 1:
        inv[1] = 1
        for i in range(2, p):
            inv[i] = (
                p - (p // i) * inv[p % i] % p
            )

    # A[x] = 1 iff g^x is in S.
    a_poly = [0] * q
    for x in range(1, p):
        if in_s[x]:
            a_poly[log[x]] = 1

    # B[r] = 1 iff g^r is an accepted ratio.
    b_poly = [0] * q

    for t in range(1, p):
        d1 = (3 * t + 1) % p
        d2 = (3 * t + 2) % p

        if d1 == 0 or d2 == 0:
            continue

        u = (2 * t + 3) % p
        w = (2 * t + 5) % p

        num1 = (u * u + 5 * t * t) % p
        num2 = (w * w + 3) % p

        inv_d1 = inv[d1]
        inv_d2 = inv[d2]

        term1 = num1 * inv_d1 % p * inv_d1 % p
        term2 = num2 * inv_d2 % p * inv_d2 % p
        value = (term1 + term2) % p

        if in_v[value]:
            b_poly[log[t]] = 1

    c = convolution(a_poly, b_poly)

    # Convert ordinary convolution into cyclic convolution modulo p - 1.
    for i in range(q, len(c)):
        c[i - q] += c[i]

    # For a = g^x, c[x] counts b = g^y with
    # x = y + log(a / b).
    for x in range(1, p):
        if in_s[x]:
            ans += c[log[x]]

    print(ans)

if __name__ == "__main__":
    solve()
```

The input is read with `input = sys.stdin.readline`, as required. The membership sets use `bytearray`, which keeps the per-residue storage small even when (p=10^6).

The zero handling happens before any discrete logarithms are used. The value for ((0,b)) is (16), while the value for ((a,0)) is (13/9). The check `9 % p != 0` is necessary because (p=3) makes the denominator of the second fraction zero when (b=0).

The inverse table avoids doing two modular exponentiations for each of the (p-1) ratios. Once `inv[d1]` and `inv[d2]` are known, the squared denominators are inverted by multiplying the inverse twice. The ratio loop also checks the unsquared linear denominator first, which is exactly equivalent to checking whether the original squared denominator is zero.

The convolution arrays use exponent indices from `0` through `p-2`. The first array represents the nonzero elements of (S), while the second represents accepted ratios. Since the group order is (p-1), exponents wrap around. The ordinary convolution contains sums from `0` through `2(p-2)`, so the second part is folded back by `p-1`.

The NTT modulus (998244353) is large enough that the exact integer convolution coefficients cannot wrap modulo the NTT modulus. A coefficient counts a collection of pairs of residues, so it is at most (p\le10^6).

The Python implementation uses the same algorithm as the accepted C++ approach, but the original 4 second contest limit was designed around highly optimized compiled NTT code. A pure Python NTT of size (2^{21}) has substantial interpreter overhead, so for the original Codeforces time limit, C++ is the practical implementation language. The mathematics and integer arithmetic in the Python version are exact.

## Worked Examples

### Sample 1

The input is

```
7
4
0 4 5 6
2
2 3
```

The nonzero elements are (4,5,6). The zero cases contribute two pairs because (16\equiv2\pmod7), so each nonzero element creates a valid pair ((0,b)). The value (13/9\equiv3\pmod7) also belongs to (V), giving the same number of valid pairs in the opposite direction.

For the nonzero part, the accepted ratio set contains the ratios whose rational value is either (2) or (3). After converting the relevant residues to primitive-root exponents, the convolution counts the valid nonzero ordered pairs.

A compact trace is:

| Stage | State | Contribution |
| --- | --- | --- |
| Input | (S={0,4,5,6}), (V={2,3}) | 0 |
| Zero cases | (F(0,b)=2), (F(a,0)=3) | 6 |
| Nonzero ratios | Check (t=1,\ldots,6), excluding denominator-zero ratios | 2 |
| Final | All valid ordered pairs | 8 |

The final output is

```
8
```

The trace demonstrates why zero values cannot simply be removed. They account for most of the answer in this sample.

### Sample 2

The input is

```
19
10
0 3 4 5 8 9 13 14 15 18
10
2 3 5 9 10 11 12 13 14 15
```

There are nine nonzero elements in (S). The algorithm first handles the two possible orientations involving zero. It then evaluates the rational expression for every nonzero ratio modulo (19), skipping ratios (t) satisfying (3t+1=0) or (3t+2=0).

The resulting ratio set is converted to exponents of a primitive root. The convolution then counts how many ordered pairs of exponents differ by each accepted ratio.

| Stage | Key state | Running answer |
| --- | --- | --- |
| Input | ( | S | =10, | V | =10) | 0 |
| Zero cases | (9) nonzero candidates in each direction | partial |
| Ratio scan | (18) nonzero ratios, with invalid denominator ratios skipped | partial |
| NTT | Convolution over exponents modulo (18) | partial |
| Final sum | Add (c[\log_g a]) for each nonzero (a\in S) | 42 |

The final output is

```
42
```

The important part of this example is that the convolution counts ordered pairs. There is no division by two, because ((a,b)) and ((b,a)) correspond to opposite exponent differences and are distinct ordered pairs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(p\log p)) | Primitive-root preprocessing, ratio evaluation, and NTT convolution are all within this bound |
| Space | (O(p)) | Membership arrays, logarithms, inverse table, and NTT buffers are linear in (p) |

The largest instance has (p=10^6). The ratio scan is linear, while the convolution uses an NTT of size at most (2^{21}), giving the intended (O(p\log p)) complexity. This is the correct asymptotic scale for the original 4 second and 256 MiB limits. The original accepted approach likewise uses an NTT with a linear-size set of residues and reports the same (O(p\log p)) idea.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Sample 1
assert run(
    """7
4
0 4 5 6
2
2 3
"""
) == "8\n", "sample 1"

# Sample 2
assert run(
    """19
10
0 3 4 5 8 9 13 14 15 18
10
2 3 5 9 10 11 12 13 14 15
"""
) == "42\n", "sample 2"

# Minimum-size input.
# Only (0, 0) exists, and its denominators are zero.
assert run(
    """2
1
0
1
0
"""
) == "0\n", "minimum size and invalid zero pair"

# All-equal nonzero values.
# For p = 7 and a = b = 1, the expression is 0.
assert run(
    """7
1
1
1
0
"""
) == "1\n", "all-equal nonzero values"

# Boundary denominator cases.
# For p = 7, ratios 2 and 4 make one denominator zero.
# S = {1, 2}, V = {0}; only (1,1) and (2,2) are valid.
assert run(
    """7
2
1 2
1
0
"""
) == "2\n", "denominator-zero ratios"

# Maximum-size style case.
# S and V contain every residue modulo 101.
# Every pair with valid denominators is accepted.
# The two invalid denominator lines contain 101 pairs each,
# and intersect only at (0,0), so 101^2 - (2*101 - 1) = 10000.
p = 101
all_values = " ".join(map(str, range(p)))
assert run(
    f"""{p}
{p}
{all_values}
{p}
{all_values}
"""
) == "10000\n", "full sets and large input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `p=2, S={0}, V={0}` | `0` | Minimum-size input and ((0,0)) denominator failure |
| `p=7, S={1}, V={0}` | `1` | All-equal nonzero values and the ratio (a/b=1) |
| `p=7, S={1,2}, V={0}` | `2` | Denominator-zero ratios (2) and (4) |
| `p=101, S=V=\{0,\ldots,100\}` | `10000` | Large set sizes and complete residue coverage |

## Edge Cases

For the ((0,0)) case, take

```
2
1
0
1
0
```

The algorithm sees that zero belongs to (S), but there are no nonzero elements, so the zero-case contribution is zero. It immediately finishes without constructing a meaningful ratio convolution. This is correct because both original denominators are zero.

For a pair ((0,b)) with (b\ne0), the first fraction becomes

[
\frac{9b^2}{b^2}=9,
]

and the second becomes

[
\frac{28b^2}{(2b)^2}=7,
]

so the total is (16). With (p=7), this is (2). The algorithm adds one such pair for every nonzero (b\in S) when (2\in V).

For a pair ((a,0)) with (a\ne0), the first fraction is (1), while the second is (4/9), giving (13/9). The algorithm checks that (9\ne0\pmod p) before using this value. This check matters at (p=3), where the denominator would be zero.

For a denominator-zero ratio, suppose (p=7) and (t=a/b=2). Then

[
3t+1=7\equiv0\pmod7.
]

The algorithm rejects this ratio before calculating an inverse. Likewise (t=4) gives (3t+2=14\equiv0\pmod7). This exactly matches the original division rule rather than treating a rational expression with an undefined denominator as some modular value.

For the all-residues case with (p=101), (S=V=\mathbb F_{101}). Every pair whose denominators are nonzero has some value in (V), so only denominator failures are excluded. Each equation (3a+b=0) and (3a+2b=0) describes (101) pairs, and they intersect only at ((0,0)). Thus there are (2\cdot101-1=201) invalid pairs, leaving

[
101^2-201=10000.
]

The convolution handles all nonzero pairs, while the explicit zero treatment handles the remaining valid pairs without ever assigning a discrete logarithm to zero.
