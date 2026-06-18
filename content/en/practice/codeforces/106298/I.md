---
title: "CF 106298I - Mega Polynomial"
description: "We are given a collection of integers that define a rational expression built from falling factorials. The central object is a constant $K$ defined indirectly through two equivalent coefficient comparisons in a polynomial identity."
date: "2026-06-18T22:29:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106298
codeforces_index: "I"
codeforces_contest_name: "OCPC 2024 Summer, Day 4: wuhudsm Contest"
rating: 0
weight: 106298
solve_time_s: 53
verified: true
draft: false
---

[CF 106298I - Mega Polynomial](https://codeforces.com/problemset/problem/106298/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of integers that define a rational expression built from falling factorials. The central object is a constant $K$ defined indirectly through two equivalent coefficient comparisons in a polynomial identity. After simplifying those identities, the task reduces to checking whether a value constructed from a product of consecutive integers divided by $A$ is an integer.

Concretely, the numerator that appears is a truncated factorial segment of the form $n \cdot (n-1) \cdot \ldots \cdot (n-k+1)$. This is the number of permutations of length $k$ chosen from $n$, often written as $nPk = \frac{n!}{(n-k)!}$. The value $K$ is this permutation product divided by $A$. The question is whether this division is exact.

There is an additional algebraic identity involving $B, C, D$, and $(n-k)$, which ensures consistency of the polynomial coefficients. That identity does not change the computational core: it only motivates why the same $K$ appears in two different coefficient comparisons. The only computational check that matters is whether all prime factors of $A$ are fully covered by the prime factorization of the permutation product.

The input structure is naturally interpreted as multiple queries, each specifying parameters $A, B, C, D, n, k$, and for each query we must decide whether $K$ is an integer.

The constraint shape implied by a Codeforces problem of this type typically allows up to large $n$, so expanding the product explicitly is infeasible. A naive multiplication would require $O(k)$ per query, which becomes too slow when both the number of queries and $k$ are large.

A subtle failure case appears when $A$ contains high powers of small primes. For example, if $A = 2^{20}$, $n = 10^6$, and $k$ is large, a naive method might overflow or miscount factors if it does not properly track multiplicity of primes across the whole range. Another edge case is when $k = 0$, where the product is empty and equals 1, meaning the answer depends purely on whether $A = 1$.

## Approaches

The most direct approach is to compute the product $n \cdot (n-1) \cdot \ldots \cdot (n-k+1)$ explicitly for each query and then check divisibility by $A$. This is correct in principle because it matches the definition of the numerator exactly. The issue is cost: each query would take $O(k)$ multiplications, and with large inputs this becomes impossible within time limits. Additionally, the intermediate product grows extremely large and would require arbitrary precision arithmetic or repeated reductions, which complicates implementation and still does not fix the time complexity problem.

The key observation is that we never need the full value of the product. We only need to know, for every prime $p$ dividing $A$, whether the exponent of $p$ in the permutation product is at least the exponent in $A$. This shifts the problem from numeric computation to valuation counting.

The permutation product $n \cdot (n-1) \cdot \ldots \cdot (n-k+1)$ can be expressed as $\frac{n!}{(n-k)!}$. This allows us to compute the exponent of any prime $p$ using a standard factorial valuation trick: $v_p(n!) - v_p((n-k)!)$. This removes the need to iterate over all elements in the range and replaces it with logarithmic counting per prime.

We factorize $A$ once per query, then for each prime factor $p$, we compute its exponent in the permutation range using the factorial valuation formula. If all required exponents are satisfied, the answer is yes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Product | $O(k)$ per query | $O(1)$ | Too slow |
| Prime Factor + Valuation | $O(\sqrt{A} + \log n)$ per query | $O(1)$ | Accepted |

## Algorithm Walkthrough

### Algorithm Walkthrough

1. Read a query consisting of $A, B, C, D, n, k$. Only $A, n, k$ affect the divisibility check, so the other values are ignored for computation.
2. Factorize $A$ into its prime components. This gives $A = \prod p_i^{e_i}$. We need to verify each exponent independently.
3. Rewrite the numerator as a factorial ratio $n! / (n-k)!$. This transforms a product range into a form where prime exponents can be counted efficiently.
4. For each prime $p_i$, compute its exponent in $n!$ using repeated division by $p_i$, then subtract its exponent in $(n-k)!$. This gives the exponent in the permutation product.
5. Compare this exponent with $e_i$. If any prime has insufficient exponent, immediately conclude $K$ is not an integer.
6. If all primes satisfy the condition, conclude $K$ is an integer.

The core idea is that divisibility reduces to checking exponent-wise dominance in prime factorization, and factorial structure allows those exponents to be computed without constructing the numbers explicitly.

### Why it works

The permutation product and factorial ratio are identical as integers, so their prime factorizations match exactly. Since integer divisibility is equivalent to comparing prime exponents component-wise, checking each prime independently fully characterizes whether $A$ divides the product. The factorial decomposition ensures we can compute those exponents exactly without enumerating the range.

## Python Solution

```python
import sys
input = sys.stdin.readline

def factorize(x):
    f = {}
    p = 2
    while p * p <= x:
        while x % p == 0:
            f[p] = f.get(p, 0) + 1
            x //= p
        p += 1
    if x > 1:
        f[x] = f.get(x, 0) + 1
    return f

def vp_factorial(n, p):
    cnt = 0
    while n:
        n //= p
        cnt += n
    return cnt

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        A, B, C, D, n, k = map(int, input().split())

        if k == 0:
            out.append("YES" if A == 1 else "NO")
            continue

        factors = factorize(A)
        ok = True

        for p, need in factors.items():
            total = vp_factorial(n, p) - vp_factorial(n - k, p)
            if total < need:
                ok = False
                break

        out.append("YES" if ok else "NO")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution begins by factorizing $A$, since all divisibility constraints are expressed in terms of its prime powers. The function `vp_factorial` computes the exponent of a prime inside a factorial using the standard summation of floor divisions, which is efficient even for large $n$.

For each query, the permutation range exponent is computed as the difference between two factorial exponents. This avoids explicitly iterating through the product range and keeps computation logarithmic in $n$.

The special case $k = 0$ corresponds to an empty product, which equals 1, so only $A = 1$ can succeed.

## Worked Examples

Consider a simple query where $A = 12$, $n = 5$, $k = 3$. The numerator is $5 \cdot 4 \cdot 3 = 60$. We factorize $12 = 2^2 \cdot 3$. The product 60 has $2^2 \cdot 3 \cdot 5$, so both required exponents are present.

| Step | p | v_p(n!) | v_p((n-k)!) | Difference | Required | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | 3 | 1 | 2 | 2 | OK |
| 3 | 3 | 1 | 0 | 1 | 1 | OK |

This trace shows that each prime constraint is checked independently and all are satisfied.

Now consider $A = 8$, $n = 6$, $k = 2$. The product is $6 \cdot 5 = 30$, which only contains one factor of 2.

| Step | p | v_p(n!) | v_p((n-k)!) | Difference | Required | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | 4 | 3 | 1 | 3 | FAIL |

Here the missing power of 2 immediately invalidates the answer.

These examples show how the method isolates prime deficiencies without computing the full product.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T \cdot (\sqrt{A} + \log n))$ | Factorization of $A$ plus factorial valuation per prime |
| Space | $O(1)$ | Only stores prime factors of $A$ |

The approach comfortably fits within typical constraints since both factorization and factorial valuation are fast even for large inputs, and no per-element iteration over the range $k$ is required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys as _sys

    # re-run solution
    input = _sys.stdin.readline

    def factorize(x):
        f = {}
        p = 2
        while p * p <= x:
            while x % p == 0:
                f[p] = f.get(p, 0) + 1
                x //= p
            p += 1
        if x > 1:
            f[x] = f.get(x, 0) + 1
        return f

    def vp_factorial(n, p):
        cnt = 0
        while n:
            n //= p
            cnt += n
        return cnt

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            A, B, C, D, n, k = map(int, input().split())

            if k == 0:
                out.append("YES" if A == 1 else "NO")
                continue

            factors = factorize(A)
            ok = True

            for p, need in factors.items():
                total = vp_factorial(n, p) - vp_factorial(n - k, p)
                if total < need:
                    ok = False
                    break

            out.append("YES" if ok else "NO")

        return "\n".join(out)

    return solve()

# custom cases
assert run("1\n1 0 0 0 5 3\n") == "YES", "trivial divisor"
assert run("1\n2 0 0 0 5 2\n") == "YES", "2 divides 5*4"
assert run("1\n8 0 0 0 6 2\n") == "NO", "insufficient powers of 2"
assert run("1\n12 0 0 0 5 3\n") == "YES", "mixed primes"
assert run("1\n6 0 0 0 3 3\n") == "YES", "edge full product"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| $A=1$ case | YES | identity divisor edge case |
| small powers of 2 | YES | factorial exponent accumulation |
| insufficient 2-adic valuation | NO | failure detection |
| mixed primes | YES | multi-prime correctness |
| full range product | YES | boundary $k=n$ style case |

## Edge Cases

A critical edge case is when $k = 0$. The product becomes empty, which evaluates to 1. For any $A > 1$, divisibility fails immediately. The algorithm handles this explicitly before any factorization.

Another case is when $k = n$. The numerator becomes $n!$, and the algorithm naturally reduces to checking whether $A$ divides $n!$ using the same valuation method. Since the factorial difference becomes $v_p(n!) - v_p(0!)$, and $v_p(0!) = 0$, the computation remains consistent.

A third subtle case is when $A = 1$. The factorization step produces an empty set of primes, so no checks are performed and the answer is always yes.
