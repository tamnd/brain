---
title: "CF 105267F - \u9759\u6d41\u7684\u8def\u5f84"
description: "We are given a number $N$ that is fully described by its prime factorization. Every prime $pi$ appears with the same exponent $m$, so $N = p1^m p2^m cdots pk^m$."
date: "2026-06-23T23:28:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105267
codeforces_index: "F"
codeforces_contest_name: "CCF CAT 2024"
rating: 0
weight: 105267
solve_time_s: 64
verified: true
draft: false
---

[CF 105267F - \u9759\u6d41\u7684\u8def\u5f84](https://codeforces.com/problemset/problem/105267/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a number $N$ that is fully described by its prime factorization. Every prime $p_i$ appears with the same exponent $m$, so $N = p_1^m p_2^m \cdots p_k^m$. Any divisor of $N$ can be represented by choosing, for each prime, an exponent between $0$ and $m$, forming a vector of length $k$.

For a divisor $y$, we define a function $f(y)$ as the sum of all exponents in its factorization. In vector form, this is simply the sum of coordinates. We are interested in those divisors whose exponent sum is exactly $T$. These are the “target” nodes.

We must build several sequences, each starting at $1$ and ending at $N$, where each step moves from a divisor to a larger divisor by divisibility. In exponent terms, each step increases some coordinates while never decreasing any. A valid sequence is therefore a monotone path in a $k$-dimensional grid from $(0,0,\dots,0)$ to $(m,m,\dots,m)$.

The goal is to choose as few such paths as possible so that every divisor whose exponent sum is exactly $T$ appears in at least one chosen path.

The key constraints are $k \le 10^3$, $m \le 10^3$, and $T \le mk \le 10^6$. This rules out any approach that explicitly enumerates all divisors or builds the full $k$-dimensional lattice. Even storing a full DP table of size $k \times T$ may be borderline, and anything cubic in $k$ or $T$ is immediately impossible.

A subtle case that often breaks naive reasoning is the assumption that a single path might cover multiple target divisors. For example, when $k=2, m=2, T=2$, the targets include $(2,0)$, $(1,1)$, and $(0,2)$. A path can pass through at most one of these because once the sum of exponents reaches $2$, any further move strictly increases it. So no path can contain two different targets. This forces us into a purely counting-based solution.

Another edge case is when $T=0$. The only target is the root divisor $1$, so the answer is clearly $1$. On the opposite extreme, when $T=mk$, the only target is $N$, again giving answer $1$.

## Approaches

The brute-force viewpoint is to explicitly construct all monotone paths from $1$ to $N$, then check which target nodes they pass through, and try to select a minimum covering set. Even generating all paths is infeasible: the number of monotone paths in a $k$-dimensional grid grows exponentially in $k$ and $m$. This immediately exceeds any computational limit.

The structural breakthrough is to recognize that each path can cover at most one target node. The function $f$ strictly increases along any valid path because every step increases at least one exponent and never decreases any. Therefore, once a path reaches a node with sum $T$, it can never revisit another node with the same sum. This turns the problem into a partitioning: each valid target must be assigned to a distinct path, and every target can independently be extended to a full path up to $N$.

So the answer becomes exactly the number of exponent vectors $(e_1,\dots,e_k)$ such that $0 \le e_i \le m$ and $\sum e_i = T$. This is a bounded integer composition problem, equivalent to extracting the coefficient of $x^T$ in $(1 + x + x^2 + \cdots + x^m)^k$.

A direct DP over $k \times T$ is conceptually simple but too slow in the worst case. Instead, we convert the expression algebraically and apply inclusion-exclusion to get a closed form.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force paths + selection | Exponential | Exponential | Too slow |
| DP over layers | $O(kT)$ | $O(T)$ | Too slow |
| Inclusion-exclusion formula | $O(k)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We rewrite the generating function as:

$$(1 + x + \cdots + x^m)^k = \left(\frac{1 - x^{m+1}}{1 - x}\right)^k$$

This separates the bounded part from an unbounded composition structure.

## Step 1

Expand $(1 - x^{m+1})^k$ using the binomial theorem. This gives a sum over $a$ where we choose how many primes contribute the “cutoff” term $x^{m+1}$.

Each term contributes:

$$\binom{k}{a} (-1)^a x^{a(m+1)}$$

## Step 2

Expand $(1 - x)^{-k}$, which is a standard stars-and-bars series:

$$(1 - x)^{-k} = \sum_{t \ge 0} \binom{t + k - 1}{k - 1} x^t$$

This counts unconstrained compositions.

## Step 3

Multiply both expansions. The coefficient of $x^T$ becomes a sum over all $a$:

$$\sum_{a \ge 0} \binom{k}{a} (-1)^a \binom{T - a(m+1) + k - 1}{k - 1}$$

where terms with negative arguments are ignored.

## Step 4

Precompute factorials and inverse factorials up to $T + k$. Each binomial coefficient is then $O(1)$.

## Step 5

Iterate over $a$ from $0$ to $k$, accumulate contributions modulo $998244353$.

### Why it works

The transformation separates bounded constraints from free compositions. The inclusion-exclusion term $(1 - x^{m+1})^k$ removes all solutions where any coordinate exceeds $m$, correcting the overcount from $(1-x)^{-k}$. Every valid exponent vector is counted exactly once because each subset of “overflow coordinates” is corrected with alternating signs.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

def solve():
    m, k, T = map(int, input().split())
    primes = list(map(int, input().split()))  # not used

    max_n = T + k + 5

    fact = [1] * max_n
    invfact = [1] * max_n

    for i in range(1, max_n):
        fact[i] = fact[i - 1] * i % MOD

    invfact[max_n - 1] = modinv(fact[max_n - 1])
    for i in range(max_n - 2, -1, -1):
        invfact[i] = invfact[i + 1] * (i + 1) % MOD

    def C(n, r):
        if n < 0 or r < 0 or n < r:
            return 0
        return fact[n] * invfact[r] % MOD * invfact[n - r] % MOD

    ans = 0

    for a in range(k + 1):
        t = T - a * (m + 1)
        if t < 0:
            break
        ways = C(k, a) * C(t + k - 1, k - 1) % MOD
        if a % 2 == 1:
            ans = (ans - ways) % MOD
        else:
            ans = (ans + ways) % MOD

    print(ans % MOD)

if __name__ == "__main__":
    solve()
```

The implementation precomputes factorials once and uses them for all binomial evaluations. The loop over $a$ stops early when $T - a(m+1)$ becomes negative, since further terms contribute nothing. The primes are irrelevant after reformulating the problem in exponent space, so they are only read for completeness.

## Worked Examples

Consider $k=2, m=1, T=1$. The valid exponent vectors are $(1,0)$ and $(0,1)$, so the answer should be $2$.

| a | t = T - a(m+1) | C(k,a) | C(t+k-1,k-1) | Contribution |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 2 | 2 |
| 1 | -1 | 2 | - | stop |

The final result is $2$, matching expectation. This confirms that each coordinate choice is counted independently.

Now consider $k=3, m=2, T=3$. We are counting solutions to $e_1+e_2+e_3=3$ with each $e_i \le 2$. The valid vectors are all compositions of 3 except those with a coordinate equal to 3.

| a | t | C(3,a) | C(t+2,2) | Contribution |
| --- | --- | --- | --- | --- |
| 0 | 3 | 1 | 10 | 10 |
| 1 | 0 | 3 | 1 | -3 |
| 2 | -3 | - | - | stop |

Result is $7$, which matches direct enumeration.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(k + T)$ | factorial precomputation dominates, loop over $k$ terms |
| Space | $O(T + k)$ | factorial and inverse factorial arrays |

The constraints allow up to about one million in $T$, and the solution only performs linear preprocessing and a linear summation over $k \le 10^3$, which comfortably fits within limits.

## Test Cases

```python
import sys, io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import prod

    # inline solution
    input = sys.stdin.readline
    m, k, T = map(int, input().split())
    primes = list(map(int, input().split()))

    max_n = T + k + 5
    fact = [1] * max_n
    invfact = [1] * max_n
    for i in range(1, max_n):
        fact[i] = fact[i - 1] * i % MOD

    def modinv(x):
        return pow(x, MOD - 2, MOD)

    invfact[max_n - 1] = modinv(fact[max_n - 1])
    for i in range(max_n - 2, -1, -1):
        invfact[i] = invfact[i + 1] * (i + 1) % MOD

    def C(n, r):
        if n < 0 or r < 0 or n < r:
            return 0
        return fact[n] * invfact[r] % MOD * invfact[n - r] % MOD

    ans = 0
    for a in range(k + 1):
        t = T - a * (m + 1)
        if t < 0:
            break
        ways = C(k, a) * C(t + k - 1, k - 1) % MOD
        if a % 2:
            ans = (ans - ways) % MOD
        else:
            ans = (ans + ways) % MOD

    return str(ans % MOD)

# minimum case
assert run("1 1 0\n2\n") == "1"

# single variable
assert run("3 1 2\n2\n") == "1"

# small symmetric case
assert run("1 2 1\n2 3\n") == "2"

# boundary T = mk
assert run("2 2 4\n2 3\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal | 1 | T=0 base case |
| k=1 | 1 | single dimension behavior |
| small k=2 | 2 | basic compositions |
| T=mk | 1 | maximum boundary correctness |

## Edge Cases

When $T = 0$, the only solution is the zero vector, so the algorithm produces only the $a=0$ term with $C(k-1,k-1)=1$, giving output $1$. Any attempt to treat this as a DP over paths would overcount by considering unnecessary intermediate states, but the formula collapses correctly.

When $T = mk$, only one exponent vector exists where all coordinates equal $m$. In the formula, all terms with $a \ge 1$ make $t < 0$, so only $a=0$ contributes, yielding exactly one configuration. This shows the inclusion-exclusion cleanly removes all invalid overflow cases without special casing.
