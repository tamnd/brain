---
title: "CF 102254H - High Hopes"
description: "For each message, we are given a base (n) and a modulus (m), with (1 le n < m le 10^6). We need to find an exponent (x) for which raising (n) to that exponent leaves remainder (1) after division by (m). If no such positive exponent exists, the required answer is (-1)."
date: "2026-08-17T21:13:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102254
codeforces_index: "H"
codeforces_contest_name: "IME++ Starters Try-outs 2019"
rating: 0
weight: 102254
solve_time_s: 141
verified: false
draft: false
---

[CF 102254H - High Hopes](https://codeforces.com/problemset/problem/102254/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 21s  
**Verified:** no  

## Solution
## Problem Understanding

For each message, we are given a base (n) and a modulus (m), with (1 \le n < m \le 10^6). We need to find an exponent (x) for which raising (n) to that exponent leaves remainder (1) after division by (m). If no such positive exponent exists, the required answer is (-1).

The key mathematical distinction is whether (n) is invertible modulo (m). If (\gcd(n,m)>1), every positive power of (n) remains divisible by some prime factor shared with (m), so it can never become congruent to (1). If (\gcd(n,m)=1), a suitable exponent always exists, because (n) belongs to the multiplicative group modulo (m).

There is a small inconsistency in the currently displayed statement: it says (0 \le x), while the second sample requires (-1) for (2^x \pmod 4). Since (2^0=1), the literal displayed condition would make (x=0) a solution for every query. The samples and the mathematical problem clearly intend a positive exponent. The solution below follows that intended interpretation, which is also the only interpretation consistent with Sample 2.

The bound (m\le 10^6) is the reason a number-theoretic preprocessing solution is possible. There can be (10^5) queries, so factoring every modulus by trial division up to (\sqrt m), followed by potentially expensive searches for the exponent, would be too costly in Python. We need to make factorization essentially logarithmic and keep the amount of modular arithmetic per query small. An (O(m\log\log m)) preprocessing pass followed by roughly logarithmic work per query is comfortably within the intended scale.

Several edge cases can fool a direct implementation. For example, with input `1 2`, the correct answer is `1`, because (2) is not the relevant modulus here: the query is (n=1,m=2), and (1^1\equiv1\pmod2). A search that starts from exponent (2) would miss the smallest valid exponent, although any valid exponent would still be accepted.

For input `2 4`, the correct answer is `-1`. Since (\gcd(2,4)=2), every positive power of (2) is even, while a number congruent to (1\pmod4) must be odd. A careless implementation that blindly applies Euler's theorem without first checking coprimality could incorrectly claim that an exponent exists.

For input `3 5`, the answer is `4`. Here (\varphi(5)=4), and (3^4\equiv1\pmod5), while (3,3^2,3^3) are not congruent to (1). This is also the sample and demonstrates that the required exponent is not necessarily (1).

## Approaches

The most direct approach is to try positive exponents one by one. Start with `value = n % m`, repeatedly multiply by (n) modulo (m), and stop when the value becomes (1). This is correct because the first time the running residue becomes (1), its exponent is exactly a solution.

The problem is the number of iterations. If a query has multiplicative order close to (10^6), the search needs nearly one million modular multiplications. With (10^5) queries, that can reach roughly (10^{11}) modular multiplications. That is far beyond what a one-second limit can support.

The observation that unlocks the faster solution is that, when (\gcd(n,m)=1), Euler's theorem gives

[
n^{\varphi(m)}\equiv1\pmod m.
]

So we already have a guaranteed candidate, (\varphi(m)). The remaining task is to remove unnecessary prime factors from this candidate.

Suppose the current candidate is (k), and a prime (p) divides (k). If

[
n^{k/p}\equiv1\pmod m,
]

then (k/p) is also a valid exponent, so the factor (p) was unnecessary and can be removed. We keep doing this for every prime factor of (\varphi(m)). The resulting value is exactly the multiplicative order of (n) modulo (m).

Because every valid order divides (\varphi(m)), the final answer is at most (\varphi(m)\le m\le10^6), so it also satisfies the exponent bound.

To make the factorization fast across (10^5) queries, we precompute the smallest prime factor, or SPF, for every integer up to (10^6). Each modulus can then be factored in (O(\log m)) divisions. Its Euler totient can be obtained directly from that factorization, and (\varphi(m)) can itself be factored using the same SPF array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(qm)) | (O(1)) | Too slow |
| Optimal | (O(M\log\log M + q\log M\log M)) | (O(M)) | Accepted |

Here (M=10^6). The second logarithmic factor accounts for the modular exponentiation performed while stripping prime factors from (\varphi(m)).

## Algorithm Walkthrough

1. Precompute the smallest prime factor `spf[v]` for every (2\le v\le10^6). The SPF array lets us factor any query modulus and any totient in logarithmic time.
2. For each query ((n,m)), compute (\gcd(n,m)). If it is greater than (1), output `-1`. A positive power of (n) remains divisible by every common prime divisor of (n) and (m), so it cannot be congruent to (1) modulo (m).
3. Factor (m) using `spf`. If

[
m=p_1^{a_1}p_2^{a_2}\cdots p_k^{a_k},
]

compute

m\prod_{i=1}^{k}\left(1-\frac1{p_i}\right).
]

Only distinct prime factors are used in this formula.

1. Set `order = phi(m)`. Euler's theorem guarantees that (n^{order}\equiv1\pmod m), because the gcd check established that (n) and (m) are coprime.
2. Factor `order` into its distinct prime factors. For every such prime (p), repeatedly test whether

[
n^{order/p}\equiv1\pmod m.
]

If the test succeeds, divide `order` by (p) and test again. If it fails, keep that factor.

1. Output the resulting `order`. It is the smallest positive exponent producing residue (1), so it is a valid answer and is automatically at most (10^6).

### Why it works

Maintain the invariant that `order` is always a positive exponent satisfying (n^{order}\equiv1\pmod m). Initially this is true by Euler's theorem. When a prime factor (p) is removed, we do so only after verifying that (n^{order/p}\equiv1\pmod m), so the invariant remains true. When the test fails, removing another (p) would destroy the property.

At the end, no prime factor of `order` can be removed while preserving the congruence. Since the multiplicative order of (n) modulo (m) divides every exponent producing (1), and in particular divides the initial value (\varphi(m)), repeatedly removing every removable prime factor leaves exactly that smallest positive exponent.

If (\gcd(n,m)>1), no positive solution exists, so the early `-1` result is also correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAX_M = 10**6

def build_spf(limit):
    spf = list(range(limit + 1))
    if limit >= 1:
        spf[1] = 1

    for i in range(2, int(limit ** 0.5) + 1):
        if spf[i] == i:
            start = i * i
            for j in range(start, limit + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf

spf = build_spf(MAX_M)

def factor_distinct(x):
    """Return the distinct prime factors of x."""
    factors = []
    while x > 1:
        p = spf[x]
        factors.append(p)
        while x % p == 0:
            x //= p
    return factors

def phi_from_factorization(m):
    phi = m
    x = m

    while x > 1:
        p = spf[x]
        phi -= phi // p
        while x % p == 0:
            x //= p

    return phi

def multiplicative_order(n, m):
    if m == 1:
        return 1

    if __import__("math").gcd(n, m) != 1:
        return -1

    order = phi_from_factorization(m)

    for p in factor_distinct(order):
        while order % p == 0:
            candidate = order // p
            if pow(n, candidate, m) == 1:
                order = candidate
            else:
                break

    return order

def solve():
    q = int(input())
    out = []

    for _ in range(q):
        n, m = map(int, input().split())
        out.append(str(multiplicative_order(n, m)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The SPF construction is done once before processing queries. For every composite number, `spf[x]` stores one of its prime divisors, and repeatedly dividing by that divisor exposes the complete factorization without trial division.

`phi_from_factorization` starts with (\varphi(m)=m). For every distinct prime (p\mid m), it applies the transformation `phi -= phi // p`, which is exactly the integer form of multiplying by (1-1/p). The inner loop then removes all copies of (p), so each distinct prime is processed once.

The gcd check comes before Euler's theorem. Euler's theorem requires coprimality, and skipping this check is the most significant correctness error in this solution. For `n = 2, m = 4`, for example, there is no positive exponent that works.

The order reduction uses Python's built-in `pow(n, exponent, m)`. This computes modular exponentiation directly without constructing the enormous integer (n^{exponent}). Python's arbitrary-precision integers also mean there is no overflow issue, but the three-argument `pow` is still essential because ordinary exponentiation would be vastly slower and use enormous intermediate values.

The `while` loop around each prime factor is necessary. A prime can occur several times in (\varphi(m)), and more than one copy may be removable. For example, if the current candidate contains (p^3), one successful division does not prove that the remaining (p^2) copies are necessary.

The implementation returns `1` when (n=1), since (1^1\equiv1\pmod m). The intended problem asks for a positive exponent, so this is the smallest valid answer.

## Worked Examples

For Sample 1, the query is (n=3,m=5).

| n | m | gcd | phi(m) | Current order | Test | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 5 | 1 | 4 | 4 | (3^{4/2}\bmod5=3^2\bmod5=4) | Keep factor 2 |
| 3 | 5 | 1 | 4 | 4 | No more distinct factors | Output 4 |

The initial candidate is (\varphi(5)=4). Its only prime factor is (2), but exponent (2) does not produce residue (1). Hence the factor cannot be removed and the answer remains (4). Indeed, (3^4=81\equiv1\pmod5).

For Sample 2, the query is (n=2,m=4).

| n | m | gcd | Action | Output |
| --- | --- | --- | --- | --- |
| 2 | 4 | 2 | gcd is greater than 1, so no positive order exists | -1 |

The algorithm stops before computing a totient-based order. Every positive power of (2) is even, so none can be congruent to (1\pmod4). This is exactly the non-coprime case that Euler's theorem cannot handle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(M\log\log M + q\log M\log M)) | SPF preprocessing costs (O(M\log\log M)); each query factors numbers in (O(\log M)) and performs logarithmically many modular exponentiations |
| Space | (O(M)) | The SPF array contains (10^6+1) integers |

With (M=10^6), the preprocessing is a one-time cost, while (q\le10^5) keeps the per-query work manageable. The algorithm avoids the potentially (10^{11}) modular multiplications of brute force and uses only a small number of modular exponentiation calls per query. The memory usage is also safely below 256 MB for the SPF array and the query output.

## Test Cases

```python
# helper: run the core solution on input string, return output string
import io
import math

def run(inp: str) -> str:
    data = inp.strip().split()
    it = iter(data)
    q = int(next(it))
    ans = []

    for _ in range(q):
        n = int(next(it))
        m = int(next(it))
        ans.append(str(multiplicative_order(n, m)))

    return "\n".join(ans)

# provided sample 1
assert run("""\
1
3 5
""") == "4", "sample 1"

# provided sample 2
assert run("""\
1
2 4
""") == "-1", "sample 2"

# Minimum-size modulus, n = 1
assert run("""\
1
1 2
""") == "1", "minimum-size valid query"

# Boundary case with n = m - 1. Since n == -1 (mod m), order is 2.
assert run("""\
1
999999 1000000
""") == "2", "maximum modulus boundary"

# Repeated identical queries, including a non-coprime case.
assert run("""\
4
5 8
5 8
6 9
6 9
""") == "2\n2\n-1\n-1", "repeated queries"

# Several small orders, including order 1 and order 2.
assert run("""\
4
1 7
2 7
3 7
6 7
""") == "1\n3\n6\n2", "small multiplicative orders"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 2` | `1` | Minimum valid values and the order-1 case |
| `1 / 999999 1000000` | `2` | Maximum modulus and the (n\equiv-1\pmod m) boundary |
| `4 / 5 8 / 5 8 / 6 9 / 6 9` | `2 / 2 / -1 / -1` | Repeated queries and non-coprime rejection |
| `4 / 1 7 / 2 7 / 3 7 / 6 7` | `1 / 3 / 6 / 2` | Different exact multiplicative orders and factor reduction |

## Edge Cases

The first edge case is the smallest modulus, `1 2`. The gcd is (1), and (\varphi(2)=1). The candidate order is already (1), so there is nothing to reduce. The algorithm outputs `1`, and indeed (1^1\equiv1\pmod2).

The second edge case is the non-coprime query `2 4`. The gcd is (2), so the algorithm immediately returns `-1`. No modular exponentiation is needed. This prevents the incorrect application of Euler's theorem to a value that is not invertible modulo (4).

The third edge case is `999999 1000000`. Since (999999\equiv-1\pmod{1000000}), the exponent (2) is sufficient. The totient of (1000000) is (400000), so the algorithm starts with (400000) and repeatedly removes prime factors whenever the corresponding smaller exponent still produces (1). Eventually it reaches `2`. The final congruence is ((-1)^2\equiv1\pmod{1000000}).

The fourth edge case is `1 7`. Here every positive power of (1) is (1), so the multiplicative order is exactly `1`. The algorithm starts with (\varphi(7)=6), tests the prime factors of (6), and repeatedly reduces the candidate until it reaches `1`. The final result is valid and exposes why the reduction loop must allow a candidate to fall all the way to one.

The fifth edge case concerns the statement's displayed lower bound `0 <= x`. If that wording were interpreted literally, every query would have answer `0`, because (n^0=1) for every positive (n). That would make Sample 2 incorrect. The algorithm intentionally follows the positive-exponent interpretation implied by the sample and by the multiplicative-order formulation. This distinction should be checked before submitting against any judge version where the statement may have been modified.
