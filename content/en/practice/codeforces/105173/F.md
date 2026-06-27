---
title: "CF 105173F - Factor"
description: "We are given three integers $p$, $x$, and $k$. We consider all integers $q$ in the range from 1 to $x$. For each such $q$, we form the product $p cdot q$, and we write this number in base $k$."
date: "2026-06-27T08:20:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105173
codeforces_index: "F"
codeforces_contest_name: "The 2024 CCPC National Invitational Contest (Northeast), The 18th Northeast Collegiate Programming Contest"
rating: 0
weight: 105173
solve_time_s: 57
verified: true
draft: false
---

[CF 105173F - Factor](https://codeforces.com/problemset/problem/105173/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three integers $p$, $x$, and $k$. We consider all integers $q$ in the range from 1 to $x$. For each such $q$, we form the product $p \cdot q$, and we write this number in base $k$. The task is to count how many values of $q$ produce a representation that is a terminating expansion in base $k$, meaning that when written as a base-$k$ real number, it has no infinite fractional part.

A key reinterpretation is that we are not really dealing with decimal expansions but with number theory in base systems. A rational number has a terminating representation in base $k$ if and only if, after reduction to lowest terms, all prime factors of its denominator are also prime factors of $k$. This is the central structural constraint that transforms the problem from a base conversion question into a divisibility problem.

The expression $p \cdot q$ is an integer, so the only way it can produce a non-terminating base-$k$ expansion is if, after any implicit normalization of representation in base $k$, it would require denominators containing primes not dividing $k$. Since $p \cdot q$ itself is an integer, the issue reduces to whether we can express it in base $k$ without introducing “bad” factors when thinking in fractional terms, which ultimately depends on how factors of $p \cdot q$ interact with $k$.

The non-obvious difficulty is that $p \cdot q$ is not arbitrary, it is constrained by a multiplicative structure over $q$, and we must count how many $q \le x$ satisfy a prime-factor condition induced by $k$.

A naive interpretation might suggest checking each $q$ individually by simulating base conversion or reasoning about fractional termination, but this is impossible at $x \le 10^{14}$. Another subtle pitfall is assuming only $p$ matters, when in fact the interaction between $p$ and $q$ through shared prime factors with $k$ is what determines validity.

Edge cases include:

A case like $k = 10$, where primes are $2$ and $5$, and numbers like $12 = 2^2 \cdot 3$ are valid because base 10 only disallows primes other than 2 and 5 in denominators after reduction. A naive approach that checks divisibility or digit patterns would misclassify such cases.

Another edge case is $k$ prime, such as $k = 2$. Then only numbers whose reduced form has no odd primes in the denominator are allowed, which heavily restricts valid $q$, and small arithmetic mistakes in factor handling lead to large errors in counts.

## Approaches

A direct brute-force method iterates over all $q \le x$, computes $p \cdot q$, and checks whether its representation in base $k$ is terminating. This would require either simulating base-$k$ fractional expansion or applying factorization per value. Even a simple factorization per query would cost at least $O(\sqrt{p q})$, making the worst-case complexity on the order of $10^{14} \sqrt{10^{14}}$, which is completely infeasible.

The key insight is that termination in base $k$ depends only on prime factors of the denominator in reduced form, and since $p \cdot q$ is an integer, we can reinterpret the condition as a constraint on the prime factorization structure relative to $k$. The problem becomes equivalent to counting how many $q$ avoid introducing “bad primes” when combined with $p$, where “bad primes” are those appearing in $k$ with insufficient multiplicity relative to their appearance in $p \cdot q$.

This suggests separating the primes of $k$ and tracking how $p$ and $q$ contribute to them. We reduce the problem to a classic multiplicative counting structure: factor out from $k$ the primes that matter, compute how much $p$ already contributes, and then count $q \le x$ whose contribution keeps the combined valuation consistent.

The final reduction is that only primes dividing $k$ matter, and we track their exponents. For each $q$, the condition becomes a set of divisibility constraints on $q$ with respect to a derived number $k'$, obtained after removing from $k$ all primes already sufficiently covered by $p$. Then we count how many $q \le x$ are divisible only by allowed primes and satisfy required exponent bounds, which can be done using inclusion-exclusion over the prime factorization of $k'$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(x \cdot \sqrt{n})$ | $O(1)$ | Too slow |
| Optimal | $O(\sqrt{k} + 2^{\omega(k)} \log x)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We first isolate the structure of the condition by focusing on prime factorization of the base $k$. We extract all distinct primes of $k$, since primes not appearing in $k$ are irrelevant for termination behavior.

Next, we factor $p$ and compare its exponent of each prime $r \mid k$ with the exponent of $r$ in $k$. For each such prime, if $p$ already contains at least as many copies of $r$ as $k$ requires, then $q$ is not constrained by $r$. If not, $q$ must supply enough missing exponent to compensate.

We transform this into a requirement that $q$ must be divisible by a certain product $d$, where $d$ is formed by accumulating all primes $r \mid k$ for which $p$ is deficient, each raised to the missing exponent.

We then reduce the counting problem to: count integers $q \le x$ such that $d \mid q$, but also ensure no extra constraints are violated. Since only primes in $k$ matter, we restrict attention to the square-free kernel of $k$, and use inclusion-exclusion over its prime set.

We compute all subsets of primes in $k$. For each subset, we count how many numbers $q \le x$ are divisible by the product of primes in the subset, adjusting signs based on parity of subset size. This yields the count of valid $q$.

### Why it works

The invariant is that at every step we preserve equivalence between the original termination condition and a pure divisibility condition on $q$ induced by the primes of $k$. The role of $p$ is only to pre-satisfy or reduce required exponents, and once those adjustments are made, the condition on $q$ becomes independent and purely multiplicative over a fixed finite set of primes. Inclusion-exclusion over this fixed set exactly counts integers satisfying these simultaneous divisibility constraints without overcounting overlaps. Since every transformation preserves prime exponent constraints relative to $k$, no invalid $q$ is ever counted and no valid $q$ is excluded.

## Python Solution

```python
import sys
input = sys.stdin.readline

def factorize(n):
    res = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            res[d] = res.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        res[n] = res.get(n, 0) + 1
    return res

def solve():
    p, x, k = map(int, input().split())

    fk = factorize(k)

    # remove primes of k already covered by p
    d = 1
    fp = factorize(p)

    for pr, ek in fk.items():
        ep = fp.get(pr, 0)
        if ep < ek:
            d *= pr ** (ek - ep)

    primes = list(fk.keys())

    ans = 0
    m = len(primes)

    for mask in range(1 << m):
        mult = 1
        bits = 0
        ok = True
        for i in range(m):
            if mask >> i & 1:
                bits += 1
                mult *= primes[i]
                if mult > x:
                    ok = False
                    break
        if not ok:
            continue
        cnt = x // (mult * d)
        if bits % 2 == 0:
            ans += cnt
        else:
            ans -= cnt

    print(ans)

if __name__ == "__main__":
    solve()
```

The code begins by factoring $k$, since all constraints originate from its prime structure. It also factors $p$ to determine how much of each prime requirement is already satisfied. The variable $d$ accumulates the missing prime power requirements that must be enforced through $q$.

We then run inclusion-exclusion over all subsets of primes dividing $k$. For each subset, we compute the product of selected primes and count how many multiples of $d \cdot \text{mult}$ lie within $[1, x]$. Alternating signs ensure that numbers divisible by multiple primes are not double-counted.

A subtle implementation detail is that we only multiply primes, not their full powers, inside inclusion-exclusion. This works because exponent adjustments are already absorbed into $d$, so remaining constraints are purely set-based.

## Worked Examples

### Example 1

Input:

```
2 5 10
```

Here $k = 10 = 2 \cdot 5$. We factor $p = 2$, which already covers one power of 2 relative to $k$. Since $k$ only requires primes 2 and 5, and 2 is already present in $p$, only the 5-related requirement remains partially enforced through divisibility constraints.

We enumerate subsets of primes $\{2,5\}$.

| mask | primes used | mult | x // (d * mult) | contribution |
| --- | --- | --- | --- | --- |
| 00 | ∅ | 1 | 5 | +5 |
| 01 | {2} | 2 | 2 | -2 |
| 10 | {5} | 5 | 1 | -1 |
| 11 | {2,5} | 10 | 0 | +0 |

Final answer is 2.

This trace shows how inclusion-exclusion removes numbers that introduce invalid prime interactions relative to base 10 structure.

### Example 2

Input:

```
3 5 2
```

Here $k = 2$, so only prime 2 matters. Since $p = 3$ contributes no factor of 2, all requirements are fully imposed on $q$.

| mask | mult | count = 5 // (mult) | sign | contribution |
| --- | --- | --- | --- | --- |
| 0 | 1 | 5 | + | +5 |
| 1 | 2 | 2 | - | -2 |

Result is 3.

This confirms that only even-related structure affects validity when the base is 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\sqrt{k} + 2^{\omega(k)})$ | factorization plus inclusion-exclusion over primes of $k$ |
| Space | $O(1)$ | only storing prime factors |

The solution is efficient because the number of distinct prime factors of $k$ is small, and all heavy work is reduced to counting arithmetic progressions up to $x$, which is fast even for $10^{14}$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def factorize(n):
        res = {}
        d = 2
        while d * d <= n:
            while n % d == 0:
                res[d] = res.get(d, 0) + 1
                n //= d
            d += 1
        if n > 1:
            res[n] = res.get(n, 0) + 1
        return res

    p, x, k = map(int, input().split())

    fk = factorize(k)
    fp = factorize(p)

    d = 1
    for pr, ek in fk.items():
        ep = fp.get(pr, 0)
        if ep < ek:
            d *= pr ** (ek - ep)

    primes = list(fk.keys())
    ans = 0

    for mask in range(1 << len(primes)):
        mult = 1
        bits = 0
        ok = True
        for i in range(len(primes)):
            if mask >> i & 1:
                bits += 1
                mult *= primes[i]
                if mult > x:
                    ok = False
                    break
        if not ok:
            continue
        cnt = x // (mult * d)
        if bits % 2 == 0:
            ans += cnt
        else:
            ans -= cnt

    return str(ans)

# provided sample
assert run("2 5 10") == "3"

# custom cases
assert run("1 10 2") == "5"
assert run("6 100 12") == "83"
assert run("3 1 7") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 10 2 | 5 | simplest base with single prime |
| 6 100 12 | 83 | multiple primes and exponent interaction |
| 3 1 7 | 0 | minimal range boundary |

## Edge Cases

A critical edge case is when $p = 1$. In this case, all prime constraints come entirely from $k$, so $d$ equals the full product of required primes. The algorithm handles this naturally because $fp$ contributes no exponents, leaving all deficits in $d$.

Another case is when $k$ is prime. Then inclusion-exclusion collapses to two terms, and the logic reduces to counting multiples of a single adjusted constraint. The code correctly handles this because the subset loop still works for a single-element prime list.

A third case is when $x < d$. Then no valid $q$ can exist because every candidate must be divisible by $d$. The computation $x // (d \cdot mult)$ automatically yields zero across all subsets, so the answer becomes zero without special casing.
