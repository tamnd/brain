---
title: "CF 102471C - Dirichlet $k$-th root"
description: "We work with arrays indexed by positive integers, but multiplication of arrays is not ordinary elementwise multiplication. For two functions (f) and (g), their Dirichlet convolution at (n) is [ (fg)(n)=sum{dmid n}f(d)g(n/d)."
date: "2026-08-09T15:42:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102471
codeforces_index: "C"
codeforces_contest_name: "2019 ICPC Asia-East Continent Final"
rating: 0
weight: 102471
solve_time_s: 220
verified: true
draft: false
---

[CF 102471C - Dirichlet $k$-th root](https://codeforces.com/problemset/problem/102471/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We work with arrays indexed by positive integers, but multiplication of arrays is not ordinary elementwise multiplication. For two functions (f) and (g), their Dirichlet convolution at (n) is

[
(f*g)(n)=\sum_{d\mid n}f(d)g(n/d).
]

The input gives the first (n) values of a function (g), together with an exponent (k). We need to recover a function (f) satisfying

[
f^k=\underbrace{f_f_\cdots*f}_{k\text{ times}}=g,
]

with (f(1)=g(1)=1), and every calculation performed modulo (998244353). The official statement has (n\le 10^5) and a one-second time limit.

The output is the first (n) values of such an (f). Under the given constraints, a solution actually always exists and is unique. The apparent possibility of printing (-1) comes from the general wording of the problem, but here (k) is strictly smaller than the prime modulus, and the recurrence below has a nonzero denominator for every (n>1).

The bound (n\le10^5) rules out anything quadratic in (n). Even (O(n^2)) would require around (10^{10}) iterations. We need to exploit the fact that a Dirichlet convolution only pairs indices whose product is the target, so all relevant pairs can be enumerated in about (n\log n) time.

There are several edge cases that are easy to mishandle. First, (k=1) is completely valid. For example,

```
2 1
1 7
```

has the correct output

```
1 7
```

because (f^1=f=g). An implementation that assumes (k\ge2) would unnecessarily fail here.

Second, composite factorizations must be included. Consider

```
4 2
1 2 2 1
```

The correct output is

```
1 1 1 0
```

because

[
(f*f)(4)=f(1)f(4)+f(2)f(2)+f(4)f(1)=0+1+0=1.
]

A method that only considers the two factors (1) and (4) would miss the (2\cdot2) contribution.

Third, the quantity used in the recurrence must count prime factors with multiplicity. For example,

[
\Omega(4)=2,
]

not (1). Using the number of distinct prime factors would make the denominator for (n=4) incorrect and break the recurrence.

Finally, (k) can be very close to the modulus. For example,

```
2 998244352
1 1
```

has the answer

```
1 998244352
```

because (k=-1\pmod {998244353}), so (f(2)=1/k=-1\pmod {998244353}). We must perform all divisions as modular inverses rather than ordinary integer divisions.

## Approaches

A direct approach is to construct (f), repeatedly convolve it with itself, and compare the result with (g). One Dirichlet convolution can be computed by enumerating all pairs (ab=n). Across every (n\le N), the total number of such pairs is

[
\sum_{a=1}^{N}\left\lfloor\frac Na\right\rfloor
=O(N\log N).
]

Thus one convolution costs (O(n\log n)), but performing it (k-1) times costs (O(kn\log n)). In the worst case (k) is almost (10^9), so for (n=10^5) this is on the order of (10^{15}) arithmetic operations. The approach is correct, but the exponent makes it unusable.

The useful observation is that taking an ordinary derivative turns a power into a multiplication by (k):

[
(F^k)'=kF^{k-1}F'.
]

Dirichlet series give a similar algebraic representation for Dirichlet convolution. The difficulty is that differentiating (n^{-s}) introduces (-\ln n), which is not directly useful modulo (998244353).

We do not actually need the numerical properties of the logarithm. We only need the identity

[
\ln(ab)=\ln a+\ln b.
]

So we can replace (\ln n) by any completely additive function. The natural choice is

[
\Omega(n),
]

the number of prime factors of (n), counted with multiplicity. It satisfies

[
\Omega(ab)=\Omega(a)+\Omega(b).
]

Define an operator (T) on functions by

[
(Tf)(n)=\Omega(n)f(n).
]

The additive property of (\Omega) gives a Leibniz rule for Dirichlet convolution:

[
T(f_g)=Tf_g+f*Tg.
]

Consequently, for (G=F^k),

[
T(G)_F=kG_T(F).
]

Looking at the coefficient belonging to (n) gives an equation containing (f(n)) only once. All other terms use (f(d)) for (d<n). This turns the original root problem into a straightforward recurrence.

The remaining implementation detail is to evaluate all proper-divisor contributions efficiently. When (f(d)) becomes known, it contributes to every (n=d\cdot a) with (a\ge2). We can distribute that contribution immediately to an accumulator. The number of such pairs ((d,a)) is (O(n\log n)).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(kn\log n)) | (O(n)) | Too slow |
| Optimal | (O(n\log n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Compute (\Omega(i)) for every (1\le i\le n). We can do this with a linear sieve, because (\Omega(p)=1) and (\Omega(ip)=\Omega(i)+1).
2. Define the transformation

[
(Tf)(n)=\Omega(n)f(n).
]

Because (\Omega(ab)=\Omega(a)+\Omega(b)), this transformation obeys

[
T(f_g)=Tf_g+f*Tg.
]

This is the exact algebraic property that an ordinary derivative contributes in the usual power rule.

1. Since (g=f^k), applying (T) to both sides and using the power rule gives

[
T(g)_f=k,g_T(f).
]

Writing out the coefficient at (n),

k\sum_{d\mid n}g(d)f(n/d)\Omega(n/d).
]

1. Isolate the term containing (f(n)). In the right-hand side it occurs when (d=1), because (g(1)=f(1)=1). Since (\Omega(1)=0), there is no corresponding (f(n)) term on the left. Rearranging gives

\sum_{\substack{d\mid n\d<n}}
f(d)g(n/d)
\left(\Omega(n/d)-k\Omega(d)\right).
]

Hence

[
\boxed{
f(n)=
\frac{
\displaystyle
\sum_{\substack{d\mid n\d<n}}
f(d)g(n/d)
\left(\Omega(n/d)-k\Omega(d)\right)
}{
k\Omega(n)
}
}.
]

For every (n>1), (\Omega(n)\ge1). Also (1\le k<998244353), so (k\not\equiv0\pmod{998244353}). The denominator is consequently invertible.

1. Set (f(1)=1). Maintain an accumulator `acc[m]` containing the numerator of the recurrence for (f(m)).

When (f(d)) has been computed, consider every (a\ge2) with (d a\le n). The pair

[
(d,a)
]

contributes to (m=da) by

[
f(d)g(a)
\left(\Omega(a)-k\Omega(d)\right).
]

So we add exactly this value to `acc[d*a]`.

1. Process (d=1,2,\ldots,n) in increasing order. For (d=1), (f(1)=1) is already known, and its updates create the term (g(n)\Omega(n)) in every accumulator. For (d>1), all proper divisors of (d) have already been processed, so `acc[d]` is complete and we can calculate

[
f(d)=
\text{acc}[d],(k\Omega(d))^{-1}\pmod p.
]

Then immediately distribute the newly known (f(d)) to all of its multiples.

1. Compute modular inverses for (k) and the small possible values of (\Omega(n)). Since (n\le10^5), (\Omega(n)\le16), so only a tiny inverse table is needed.

### Why it works

The central invariant is that before computing (f(n)), `acc[n]` contains exactly

[
\sum_{\substack{d\mid n\d<n}}
f(d)g(n/d)
\left(\Omega(n/d)-k\Omega(d)\right).
]

Every term has been added when its smaller factor (d) was processed, and no term involving (f(n)) is added because we only multiply by (a\ge2).

The transformation (T(f)(n)=\Omega(n)f(n)) satisfies the Leibniz rule because (\Omega) is completely additive. Thus every valid root satisfies the recurrence. Conversely, our recurrence constructs values satisfying that recurrence. Suppose (H=f^k). Both (H) and the given (g) satisfy the same transformed convolution equation. Their difference has value zero at (1), and at every (n>1) its coefficient is multiplied by the nonzero value (k\Omega(n)), while all other terms involve smaller indices. Induction on (n) forces (H(n)=g(n)) for every (n\le N). Hence the constructed (f) is a correct (k)-th Dirichlet root.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    n, k = map(int, input().split())
    g = [0] + list(map(int, input().split()))

    # Linear sieve for Omega(n), the number of prime factors
    # counted with multiplicity.
    lp = [0] * (n + 1)
    omega = [0] * (n + 1)
    primes = []

    for i in range(2, n + 1):
        if lp[i] == 0:
            lp[i] = i
            primes.append(i)
            omega[i] = 1

        for p in primes:
            x = i * p
            if x > n or p > lp[i]:
                break
            lp[x] = p
            omega[x] = omega[i] + 1

    # Modular inverse of k.
    inv_k = pow(k, MOD - 2, MOD)

    # Omega(n) <= 16 for n <= 1e5, but 20 is a convenient safe bound.
    inv_omega = [0] * 21
    for x in range(1, 21):
        inv_omega[x] = pow(x, MOD - 2, MOD)

    f = [0] * (n + 1)
    acc = [0] * (n + 1)

    f[1] = 1

    for d in range(1, n + 1):
        if d > 1:
            f[d] = (acc[d] % MOD) * inv_k % MOD
            f[d] = f[d] * inv_omega[omega[d]] % MOD

        fd = f[d]
        od = omega[d]

        # Every a >= 2 gives m = d * a > d.
        # This contribution is part of the recurrence for f[m].
        for a in range(2, n // d + 1):
            m = d * a
            acc[m] += fd * g[a] * (omega[a] - k * od)

    print(*f[1:])

if __name__ == "__main__":
    solve()
```

The input is stored with a dummy zero at index zero, so mathematical index (i) and Python index (i) coincide. This avoids repeated `i - 1` conversions.

The linear sieve computes `omega[i]` using the smallest prime factor representation. When (i) is multiplied by a prime (p), one additional prime factor is introduced, so `omega[i * p] = omega[i] + 1`.

The accumulator is deliberately not reduced modulo `MOD` inside the innermost loop. Each `acc[m]` receives only one term for each proper divisor of (m), so it contains only (O(\tau(m))) terms. Python's arbitrary-precision integers can handle these values comfortably for (n\le10^5), while avoiding a costly modulo operation on every divisor pair.

At the beginning of the iteration for `d`, every proper divisor of `d` has already propagated its contribution to `acc[d]`. This is why the increasing order of `d` is essential. After calculating `f[d]`, we immediately propagate it to larger indices, which preserves the invariant needed by later iterations.

The expression

```
omega[a] - k * od
```

is intentionally allowed to be negative. The final modular reduction of `acc[d]` handles negative accumulated values correctly.

There is no integer-overflow problem in Python. In a language with fixed-width integers, the products should be stored in a sufficiently wide integer type before taking the modulus.

The code also does not explicitly test for `-1`. Under these constraints the denominator (k\Omega(n)) is always nonzero modulo the prime modulus, so the recurrence always produces a valid root.

## Worked Examples

### Sample 1

The input is

```
5 2
1 8 4 26 6
```

We have

[
\Omega(2)=1,\quad
\Omega(3)=1,\quad
\Omega(4)=2,\quad
\Omega(5)=1.
]

The accumulator starts by processing (d=1). Since (f(1)=1), it contributes (g(a)\Omega(a)) to every (a).

| (d) | (f(d)) | Updated index | Contribution | `acc` after update |
| --- | --- | --- | --- | --- |
| 1 | 1 | 2 | (8\cdot1=8) | `acc[2]=8` |
| 1 | 1 | 3 | (4\cdot1=4) | `acc[3]=4` |
| 1 | 1 | 4 | (26\cdot2=52) | `acc[4]=52` |
| 1 | 1 | 5 | (6\cdot1=6) | `acc[5]=6` |
| 2 | 4 | 4 | (4\cdot8(1-2)=-32) | `acc[4]=20` |

Now the values are obtained from

[
f(n)=\frac{\text{acc}[n]}{2\Omega(n)}.
]

| (n) | (\Omega(n)) | `acc[n]` | Denominator | (f(n)) |
| --- | --- | --- | --- | --- |
| 1 | 0 |  |  | 1 |
| 2 | 1 | 8 | 2 | 4 |
| 3 | 1 | 4 | 2 | 2 |
| 4 | 2 | 20 | 4 | 5 |
| 5 | 1 | 6 | 2 | 3 |

The resulting root is

```
1 4 2 5 3
```

The interesting part is (n=4). The direct (1\cdot4) contribution gives (52), but the factorization (2\cdot2) contributes (-32) to the recurrence, leaving (20). This is exactly what is needed to recover (f(4)=5).

### Constructed Example

Take

```
5 2
1 4 6 14 14
```

The intended root is

```
1 2 3 5 7
```

because

[
(f*f)(2)=2f(2)=4,
]

[
(f*f)(3)=2f(3)=6,
]

[
(f*f)(4)=2f(4)+f(2)^2=10+4=14,
]

and

[
(f*f)(5)=2f(5)=14.
]

The recurrence proceeds as follows.

| (d) | (f(d)) | New `acc` contribution | Relevant `acc` |
| --- | --- | --- | --- |
| 1 | 1 | (g(a)\Omega(a)) | `acc[2]=4`, `acc[3]=6`, `acc[4]=28`, `acc[5]=14` |
| 2 | 2 | (2\cdot4(1-2)=-8) to index 4 | `acc[4]=20` |
| 3 | 3 | no multiple (3a\le5) with (a\ge2) | unchanged |
| 4 | 5 | no multiple within range | unchanged |
| 5 | 7 | no multiple within range | unchanged |

The final divisions are

[
f(2)=4/2=2,
]

[
f(3)=6/2=3,
]

[
f(4)=20/4=5,
]

[
f(5)=14/2=7.
]

This trace demonstrates the invariant that `acc[n]` contains exactly the proper-divisor part of the recurrence before (f(n)) is computed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log n)) | Every pair ((d,a)) with (da\le n) and (a\ge2) is processed once, giving (\sum_{d=1}^n O(n/d)=O(n\log n)). The linear sieve is (O(n)). |
| Space | (O(n)) | The arrays `g`, `f`, `acc`, `omega`, and the sieve arrays all have length (O(n)). |

For (n=10^5), the number of divisor-pair updates is only on the order of (n\log n), around a million rather than the (10^{10}) operations of a quadratic algorithm. The memory consumption is linear and comfortably below 256 MB. The original contest limits are one second and 256 MB.

## Test Cases

The following test harness uses the same algorithm as the submitted solution. The maximum-size case deliberately uses (k=1), making the expected answer easy to verify without embedding a 100,000-element literal.

```python
import sys
import io

MOD = 998244353

def solve_instance(inp: str) -> str:
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    k = next(it)
    g = [0] + [next(it) for _ in range(n)]

    lp = [0] * (n + 1)
    omega = [0] * (n + 1)
    primes = []

    for i in range(2, n + 1):
        if lp[i] == 0:
            lp[i] = i
            primes.append(i)
            omega[i] = 1

        for p in primes:
            x = i * p
            if x > n or p > lp[i]:
                break
            lp[x] = p
            omega[x] = omega[i] + 1

    inv_k = pow(k, MOD - 2, MOD)

    inv_omega = [0] * 21
    for x in range(1, 21):
        inv_omega[x] = pow(x, MOD - 2, MOD)

    f = [0] * (n + 1)
    acc = [0] * (n + 1)
    f[1] = 1

    for d in range(1, n + 1):
        if d > 1:
            f[d] = acc[d] % MOD
            f[d] = f[d] * inv_k % MOD
            f[d] = f[d] * inv_omega[omega[d]] % MOD

        fd = f[d]
        od = omega[d]

        for a in range(2, n // d + 1):
            m = d * a
            acc[m] += fd * g[a] * (omega[a] - k * od)

    return " ".join(map(str, f[1:]))

def run(inp: str) -> str:
    return solve_instance(inp)

# Provided sample
assert run(
    "5 2\n"
    "1 8 4 26 6\n"
) == "1 4 2 5 3", "sample 1"

# k = 1, so f must equal g.
assert run(
    "2 1\n"
    "1 7\n"
) == "1 7", "minimum size and k=1"

# Composite contribution 2 * 2 is required.
assert run(
    "4 2\n"
    "1 2 2 1\n"
) == "1 1 1 0", "composite factorization"

# k = MOD - 1, so 1 / k = -1 modulo MOD.
assert run(
    "2 998244352\n"
    "1 1\n"
) == "1 998244352", "large k boundary"

# All values of the root are 1. For k = 2, g(n) is the divisor count.
assert run(
    "5 2\n"
    "1 2 2 3 2\n"
) == "1 1 1 1 1", "all-equal root"

# Maximum n, with k = 1 and all values equal to 1.
n = 100000
inp = f"{n} 1\n" + " ".join(["1"] * n) + "\n"
expected = " ".join(["1"] * n)
assert run(inp) == expected, "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 2 / 1 8 4 26 6` | `1 4 2 5 3` | Provided sample and composite divisor contribution |
| `2 1 / 1 7` | `1 7` | Minimum size and (k=1) |
| `4 2 / 1 2 2 1` | `1 1 1 0` | The (2\cdot2) factorization and (\Omega(4)=2) |
| `2 998244352 / 1 1` | `1 998244352` | (k) at its maximum allowed value |
| `5 2 / 1 2 2 3 2` | `1 1 1 1 1` | Equal root values and divisor multiplicities |
| (n=100000,\ k=1), all ones | 100001 ones | Maximum input size and boundary performance |

## Edge Cases

For (k=1), the recurrence still works without modification. With

```
2 1
1 7
```

we have (\Omega(2)=1), and the accumulator for (2) is (7). The denominator is (1\cdot1), so (f(2)=7). Thus the output is `1 7`, exactly as required.

For a composite number with repeated prime factors, (\Omega) must count multiplicity. In

```
4 2
1 2 2 1
```

the root is `1 1 1 0`. At (n=4), the proper divisor (d=2) contributes

[
f(2)g(2)(\Omega(2)-2\Omega(2))
=1\cdot2(1-2)=-2.
]

The initial (d=1) contribution is (g(4)\Omega(4)=1\cdot2=2), so `acc[4]=0` and consequently (f(4)=0). Using the number of distinct prime factors would incorrectly use (\Omega(4)=1) and produce the wrong denominator.

For the largest allowed exponent,

```
2 998244352
1 1
```

we have (k\equiv-1\pmod{998244353}). The recurrence gives

[
f(2)=1/(-1)=-1\pmod{998244353},
]

so the output is `1 998244352`. This demonstrates why modular inversion is required even when the input exponent is represented as an ordinary positive integer.

For (n=1), there would be no recurrence because (\Omega(1)=0), which would make the denominator meaningless. The problem starts at (n=2), and we explicitly set (f(1)=1) before processing any other index. This also supplies the identity element needed by every later Dirichlet convolution.

The possibility of a zero value in (g) causes no special case. For example, the root in

```
4 2
1 2 2 1
```

has (f(4)=0), and the recurrence handles it exactly like every other value. The algorithm never divides by (g(n)), so zero entries of (g) are harmless.

The apparent (-1) output case also requires no special handling for the given constraints. Since (k) is nonzero modulo the prime (998244353), and (\Omega(n)) is a positive integer strictly smaller than that prime for (n\le10^5), every denominator (k\Omega(n)) is invertible. The recurrence consequently determines a root for every valid input.
