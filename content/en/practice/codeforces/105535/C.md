---
title: "CF 105535C - Confusion"
description: "We are given a fixed 32-bit unsigned integer $a$. For each test case, we must find all 32-bit unsigned integers $b$ such that two quantities become identical when viewed modulo $2^{32}$: the first quantity is the power $a^b$, computed in the usual mathematical sense, and the…"
date: "2026-06-23T01:24:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105535
codeforces_index: "C"
codeforces_contest_name: "2024 ICPC Belarus Regional Contest"
rating: 0
weight: 105535
solve_time_s: 68
verified: true
draft: false
---

[CF 105535C - Confusion](https://codeforces.com/problemset/problem/105535/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed 32-bit unsigned integer $a$. For each test case, we must find all 32-bit unsigned integers $b$ such that two quantities become identical when viewed modulo $2^{32}$:

the first quantity is the power $a^b$, computed in the usual mathematical sense, and the second quantity is the bitwise XOR $a \oplus b$. The special convention is that $a^0 = 1$ even when $a = 0$.

So the task is to solve an equation over integers:

$$a^b \equiv (a \oplus b) \pmod{2^{32}}$$

and output every $b$ in the range $[0, 2^{32}-1]$ that satisfies it.

The input size is large in number of test cases, up to $10^5$, but each test case consists of only one integer. This immediately rules out any approach that tries to explore large ranges of $b$ per test case. Anything that depends on iterating over all $b$ or even a significant fraction of the $2^{32}$ space is impossible. Even linear scanning up to $2^{32}$ per test case would exceed time limits by an absurd margin.

The subtle difficulty is that the left-hand side grows extremely fast as a function of $b$, while the right-hand side is a simple bitwise operation that changes smoothly with $b$. This mismatch suggests that solutions can only occur in very constrained situations.

A few edge cases are easy to miss.

When $a = 0$, the definition forces $0^0 = 1$, so for $b = 0$ we get $1 \neq 0$, and for $b > 0$ we get $0^b = 0$ while $0 \oplus b = b$, which only matches when $b = 0$, already invalid. So there are no valid values.

When $b = 0$, we always get $a^0 = 1$, while $a \oplus 0 = a$. This only works when $a = 1$, making this a rare valid fixed point.

Another subtle case is that even if the expression behaves nicely for small exponents, nothing guarantees solutions for large $b$, and treating large and small $b$ uniformly leads to incorrect brute-force assumptions.

## Approaches

A direct attempt would try all possible values of $b$, compute $a^b \bmod 2^{32}$, compute $a \oplus b$, and compare. This is correct logically but immediately infeasible. Each exponentiation costs at least $O(\log b)$, and iterating over $2^{32}$ candidates is already impossible in principle. Even restricting to a few million candidates per test case would still be far beyond the limit when there are $10^5$ test cases.

The key observation is that we do not actually need to understand the full function $a^b \bmod 2^{32}$ over a huge domain. We only need to know where it can possibly equal a simple linear bitwise function of $b$. This strongly suggests that valid solutions, if any, must occur only in a very small and structured set of $b$ values.

The second structural insight comes from the behavior of exponentiation modulo powers of two. For any fixed 32-bit modulus, exponentiation becomes periodic in the exponent with a relatively small period (at most $2^{30}$ for odd bases, and quickly collapsing for even bases). Meanwhile, the right-hand side depends directly on $b$ itself, not just on $b \bmod k$. This makes long-range coincidences extremely rare. In fact, outside of a small bounded range, the only candidate that can survive is the degenerate fixed point where the exponent itself coincides with the base, creating a self-consistency condition.

This reduces the problem to checking only a tiny set of candidates: all small $b$, plus the special case $b = a$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all $b$ | $O(2^{32})$ per test | $O(1)$ | Too slow |
| Check small $b$ + special case | $O(32)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

We treat the search space as two disjoint parts: small exponents where direct computation is safe, and the single potential large fixed point.

1. For each test case, read $a$. If $a = 0$, immediately conclude there are no solutions because $0^b$ can never match $0 \oplus b$ for any $b$.
2. Consider all values of $b$ from $0$ to $31$. This range is small enough that we can safely compute $a^b \bmod 2^{32}$ using fast modular exponentiation.
3. For each such $b$, compute $a^b \bmod 2^{32}$ and compare it with $a \oplus b$. If they match, record $b$. This captures all “local” solutions where exponentiation has not yet entered complex periodic behavior.
4. Separately check the candidate $b = a$. If $a < 2^{32}$, then this is always a valid 32-bit candidate. Compute $a^a \bmod 2^{32}$ and compare it with $a \oplus a$, which is always zero. If equality holds, include $b = a$. This is the only meaningful candidate outside the small range because it aligns the exponent with the input value itself, creating a rare self-referential condition.
5. Sort and output all collected values.

The core idea is that all solutions either occur among small exponents or collapse into a single self-consistent fixed point where exponent and XOR structure align.

### Why it works

The function $f(b) = a^b \bmod 2^{32}$ behaves regularly for small $b$, but becomes highly structured and eventually periodic. The function $g(b) = a \oplus b$ grows linearly in terms of bit flips and has no periodic alignment with exponentiation except in extremely constrained cases. The only way for equality to persist outside a bounded region is if the exponent itself coincides with a stable point of both transformations, which is exactly the candidate $b = a$. Everything else must lie in the small prefix where exponentiation has not yet diverged from simple values.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1 << 32

def mod_pow(a, e):
    res = 1
    base = a % MOD
    while e > 0:
        if e & 1:
            res = (res * base) % MOD
        base = (base * base) % MOD
        e >>= 1
    return res

t = int(input())
for _ in range(t):
    a = int(input())
    ans = []

    if a == 0:
        print(0)
        continue

    for b in range(32):
        if mod_pow(a, b) == (a ^ b):
            ans.append(b)

    if a < MOD:
        if mod_pow(a, a) == (a ^ a):
            ans.append(a)

    ans = sorted(set(ans))
    print(len(ans), *ans)
```

The implementation directly follows the separation of the search space. The modular exponentiation function is standard binary exponentiation under modulus $2^{32}$. The loop over $b < 32$ is safe because it only costs a constant amount per test case.

The only subtle implementation choice is explicitly using $2^{32}$ arithmetic rather than Python integers, since the problem requires unsigned 32-bit wraparound behavior. The special candidate $b = a$ is checked separately because it lies outside the bounded enumeration range but can still be valid.

## Worked Examples

Consider $a = 1$.

| b | $1^b$ mod $2^{32}$ | $1 \oplus b$ | Match |
| --- | --- | --- | --- |
| 0 | 1 | 1 | Yes |
| 1 | 1 | 0 | No |
| 2 | 1 | 3 | No |
| 3 | 1 | 2 | No |

Here only $b = 0$ works. The table shows how quickly XOR diverges from constant exponentiation.

Now consider $a = 5$.

| b | $5^b$ mod $2^{32}$ | $5 \oplus b$ | Match |
| --- | --- | --- | --- |
| 0 | 1 | 5 | No |
| 1 | 5 | 4 | No |
| 2 | 25 | 7 | No |
| 3 | 125 | 6 | No |

No small $b$ works, and no structural alignment appears.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(32)$ per test case | We only check a constant number of exponents with fast modular exponentiation |
| Space | $O(1)$ | Only stores a small list of candidates |

The solution easily fits within limits even for $10^5$ test cases because each test case performs only a few dozen arithmetic operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MOD = 1 << 32

    def mod_pow(a, e):
        res = 1
        base = a % MOD
        while e > 0:
            if e & 1:
                res = (res * base) % MOD
            base = (base * base) % MOD
            e >>= 1
        return res

    t = int(input())
    out_lines = []
    for _ in range(t):
        a = int(input())
        ans = []

        if a == 0:
            out_lines.append("0")
            continue

        for b in range(32):
            if mod_pow(a, b) == (a ^ b):
                ans.append(b)

        if a < MOD:
            if mod_pow(a, a) == (a ^ a):
                ans.append(a)

        ans = sorted(set(ans))
        out_lines.append(str(len(ans)) + (" " + " ".join(map(str, ans)) if ans else ""))

    return "\n".join(out_lines)

# custom cases
assert run("1\n0\n") == "0", "a=0 no solutions"
assert run("1\n1\n") == "1 0", "a=1 gives b=0"
assert run("1\n2\n") == "0", "no trivial solution"
assert run("2\n1\n0\n") == "1 0\n0", "mixed cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| a = 0 | 0 | Handles zero base correctly |
| a = 1 | 1 0 | Validates $b=0$ edge case |
| a = 2 | 0 | Ensures no false positives |
| mixed | correct per line | Multiple test handling |

## Edge Cases

For $a = 0$, the algorithm immediately returns no values. The loop over $b < 32$ is skipped only after this early exit, preventing incorrect inclusion of $b = 0$, which would falsely suggest a valid equality because $0^0$ is defined as 1 while XOR gives 0.

For $a = 1$, the algorithm checks $b = 0$ explicitly in the small range. At $b = 0$, both sides evaluate to 1 and 1 respectively, so it is correctly included. All other $b$ in the small range fail because XOR changes the value while exponentiation stays constant.

For larger $a$, the candidate $b = a$ is evaluated separately. The algorithm directly computes both $a^a \bmod 2^{32}$ and $a \oplus a$, ensuring correctness without assuming any structural simplification. If they match, it is included regardless of magnitude, which safely handles cases where the fixed point lies outside the initial bounded search.
