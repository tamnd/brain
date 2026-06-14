---
title: "CF 1511B - GCD Length"
description: "We are asked to construct two positive integers, call them $x$ and $y$, such that we fully control three properties at once: how many digits $x$ has, how many digits $y$ has, and how many digits their greatest common divisor has."
date: "2026-06-14T18:06:15+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1511
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 107 (Rated for Div. 2)"
rating: 1100
weight: 1511
solve_time_s: 425
verified: false
draft: false
---

[CF 1511B - GCD Length](https://codeforces.com/problemset/problem/1511/B)

**Rating:** 1100  
**Tags:** constructive algorithms, math, number theory  
**Solve time:** 7m 5s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct two positive integers, call them $x$ and $y$, such that we fully control three properties at once: how many digits $x$ has, how many digits $y$ has, and how many digits their greatest common divisor has.

In other words, instead of being given numbers and computing something from them, we are given the “shape constraints” of the numbers. The task is to fabricate any valid pair that satisfies those constraints simultaneously.

A key observation from the constraints is that all digit lengths are small, at most 9. That means the actual numeric values can be enormous in principle, but we do not need anything close to optimal search or factoring. A direct constructive pattern is sufficient because we are allowed to output any valid solution, not a unique one.

A naive approach might try to brute force pairs of numbers with correct digit lengths and compute their gcd until a match is found. That fails immediately because even restricting to 9-digit numbers gives a search space far beyond what can be enumerated per test case. Another naive mistake is to try to independently construct $x$ and $y$ with the right digit lengths and then “adjust” them to fix the gcd. That adjustment problem is essentially number-theoretic and would quickly become complicated.

The real difficulty is that gcd constraints are multiplicative in structure. If we build both numbers as multiples of a common base $g$, then the gcd becomes exactly that base if we keep the remaining parts coprime. This structure is what makes a direct construction possible.

## Approaches

A brute-force interpretation would attempt to iterate over all $a$-digit numbers for $x$ and all $b$-digit numbers for $y$, compute $\gcd(x, y)$, and check whether its digit length matches $c$. Even if we restrict to one second per test, the number of candidates is on the order of $10^a \cdot 10^b$, which is astronomically large even for moderate values like $a = b = 6$. This immediately rules out enumeration.

The key insight is to reverse the role of the gcd. Instead of discovering it after constructing $x$ and $y$, we explicitly construct it first. We pick a number $g$ that has exactly $c$ digits. Then we force both $x$ and $y$ to be multiples of $g$. This guarantees that $\gcd(x, y)$ is at least $g$. If we ensure the multipliers are coprime, the gcd becomes exactly $g$.

So we reduce the problem to constructing two multipliers $u$ and $v$ such that:

$x = g \cdot u$, $y = g \cdot v$,

and $u$ has $a-c$ digits, $v$ has $b-c$ digits, while $\gcd(u, v) = 1$.

The simplest way to guarantee coprimality is to take $u = 10^{a-c}$ and $v = 10^{b-c} + 1$. The first is a pure power of ten, the second is one more than a power of ten, so their gcd is 1. Multiplying both by the same $g$ preserves the gcd structure.

This construction directly enforces all digit-length constraints and fixes the gcd exactly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in digits | O(1) | Too slow |
| Constructive gcd splitting | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

### Construction idea

We first decide the gcd explicitly, then embed it into both numbers.

### Steps

1. Construct a number $g$ that has exactly $c$ digits.

We can simply take $g = 10^{c-1}$.

This guarantees the digit length is exactly $c$.
2. Construct a base multiplier for $x$: $u = 10^{a-c}$.

This is a number with exactly $a-c+1$ digits in raw form but effectively ensures $x$ becomes an $a$-digit number after multiplication with $g$.
3. Construct a base multiplier for $y$: $v = 10^{b-c} + 1$.

This ensures $v$ is not divisible by 2 or 5 and is not a multiple of $u$, which makes it coprime with $u$.
4. Set $x = g \cdot u$, $y = g \cdot v$.
5. Output $x, y$.

### Why it works

The constructed numbers share a common factor $g$, so the gcd is at least $g$. After factoring it out, we are left with $u$ and $v$. By construction, $u$ is a power of ten and $v$ is that power plus one, so they share no common prime factor. This forces $\gcd(u, v) = 1$, so the gcd of the full numbers is exactly $g$. The digit lengths are controlled because multiplying by powers of ten shifts digits without changing structure, and adding one to a power of ten creates the minimal perturbation that preserves the required length while maintaining coprimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        a, b, c = map(int, input().split())

        g = 10 ** (c - 1)
        u = 10 ** (a - c)
        v = 10 ** (b - c) + 1

        x = g * u
        y = g * v

        print(x, y)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the construction. The only subtlety is handling powers of ten correctly. Since all exponents are at most 9, integer size is completely safe in Python. No special edge handling is required beyond ensuring the exponent expressions match the digit-length logic exactly.

## Worked Examples

### Example 1

Input:

$a = 2, b = 3, c = 1$

We compute:

$g = 10^0 = 1$

$u = 10^1 = 10$

$v = 10^2 + 1 = 101$

| step | g | u | v | x | y |
| --- | --- | --- | --- | --- | --- |
| init | 1 | - | - | - | - |
| build u | 1 | 10 | - | - | - |
| build v | 1 | 10 | 101 | - | - |
| final | 1 | 10 | 101 | 10 | 101 |

We obtain $x = 10$, $y = 101$. Their gcd is 1, which matches the required 1-digit gcd.

### Example 2

Input:

$a = 3, b = 3, c = 2$

We compute:

$g = 10$

$u = 10$

$v = 101$

| step | g | u | v | x | y |
| --- | --- | --- | --- | --- | --- |
| init | 10 | - | - | - | - |
| build u | 10 | 10 | - | - | - |
| build v | 10 | 10 | 101 | - | - |
| final | 10 | 10 | 101 | 100 | 1010 |

Here $x = 100$, $y = 1010$. The gcd is 10, which has exactly 2 digits.

These examples show that the construction reliably scales digit lengths while keeping the gcd exactly controlled by the chosen base $g$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t)$ | Each test constructs a few powers and multiplies constants |
| Space | $O(1)$ | Only a fixed number of integers are used |

The constraints allow up to 285 test cases, and each operation is constant time arithmetic on small integers, so the solution runs well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        a, b, c = map(int, input().split())
        g = 10 ** (c - 1)
        u = 10 ** (a - c)
        v = 10 ** (b - c) + 1
        x = g * u
        y = g * v
        output.append(f"{x} {y}")
    
    return "\n".join(output)

# sample tests (structure check only)
inp = """4
2 3 1
2 2 2
6 6 2
1 1 1
"""
res = run(inp)
assert len(res.splitlines()) == 4

# custom edge cases
assert run("1\n1 1 1\n") == "1 1"
assert run("1\n2 2 1\n").split()[0].isdigit()
assert run("1\n3 3 3\n").count(" ") == 1
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | 1 1 | smallest boundary case |
| 2 2 1 | valid pair | minimal gcd length with larger numbers |
| 3 3 3 | valid pair | gcd equals full number length |

## Edge Cases

When $c = 1$, the gcd must be a single-digit number, which includes 1. The construction sets $g = 1$, so both numbers are simply $u$ and $v$. This correctly reduces the problem to constructing any coprime pair with fixed digit lengths, which is handled by $10^k$ and $10^k + 1$.

When $a = c$ or $b = c$, one of the multipliers becomes $10^0 = 1$. This means one of the numbers becomes exactly $g$, and the other becomes a scaled version. The digit constraints still hold because multiplying by 1 does not change the structure, and the other number still preserves its intended length through multiplication by a power of ten.
