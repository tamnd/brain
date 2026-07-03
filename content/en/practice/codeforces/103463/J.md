---
title: "CF 103463J - Hsueh- owns large quantities of apples"
description: "We are modeling a deterministic transfer process that starts with a single pile of apples and moves through a line of m children. The first child receives all n apples."
date: "2026-07-03T06:58:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103463
codeforces_index: "J"
codeforces_contest_name: "The Hangzhou Normal U Qualification Trials for ZJPSC 2020"
rating: 0
weight: 103463
solve_time_s: 43
verified: true
draft: false
---

[CF 103463J - Hsueh- owns large quantities of apples](https://codeforces.com/problemset/problem/103463/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are modeling a deterministic transfer process that starts with a single pile of apples and moves through a line of m children. The first child receives all n apples. Each child performs the same operation: they consume exactly one apple, and then they attempt to partition the remaining apples into x equal piles. One of these piles is kept, while the other x − 1 piles are passed forward as the next child's input.

A key constraint is that at every step, the remaining number of apples after eating one must be divisible by x, and the final child’s remaining pile must be a positive integer. The task is to determine the smallest possible initial number of apples n that makes this entire process valid through all m children, and to output that minimum n modulo 998244353.

The structure is inherently sequential: each child transforms the input value into a smaller output value via a linear arithmetic condition involving subtraction by one and division by x. The output of one step becomes the input of the next, so the whole system is a recurrence that must remain valid for m transitions.

The constraints allow m up to 10^9 and x up to 10^9, while the number of test cases can reach 10^3. This immediately rules out any simulation across all children, since even O(m) per test case would be far too large. The solution must compress the effect of repeating the same transformation m times into a closed-form expression.

A subtle edge case arises when x = 2 or m is large: the recurrence grows very quickly, and intermediate values exceed standard bounds, so any approach relying on iterative multiplication without modular arithmetic or without a closed form will fail. Another subtlety is that divisibility must hold at every step, so not every arithmetic sequence is valid even if the final expression seems correct.

## Approaches

If we try to simulate directly, we start from some unknown n and repeatedly apply the transformation: subtract one, divide by x, and propagate forward. Running this forward is not possible because we do not know intermediate values unless we already know n.

Instead, we reverse the process. Suppose the i-th child receives some value a. After eating one apple, the remaining a − 1 must equal x times the value passed to the next child. That means a − 1 is always divisible by x, and the next state is (a − 1) / x. This defines a reverse recurrence: if we know the last valid value, we can reconstruct the previous ones.

Let the final child’s remaining pile be 1, since it must be a positive integer and we want the minimum starting value. Working backward m times expands the number according to a geometric construction: each reverse step multiplies by x and adds 1. Repeating this m times yields a closed form geometric series.

This leads to the expression n = 1 + x + x^2 + ... + x^{m}. This is a standard geometric sum, and can be rewritten as (x^{m+1} − 1) / (x − 1) for x ≠ 1. Since x ≥ 2, division is always valid in modular arithmetic because x − 1 is invertible modulo 998244353.

Thus the problem reduces to fast exponentiation and modular inverse computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(m) per test | O(1) | Too slow |
| Geometric Series + Fast Pow | O(log m) per test | O(1) | Accepted |

## Algorithm Walkthrough

### 1. Reformulate the process in reverse

We define the state after each child. If a child has value a, the previous state must satisfy a = x * b + 1 for some integer b. This inversion is forced by the requirement that after subtracting one, the remainder must split evenly into x piles.

### 2. Identify the minimal valid final state

The last child must end with a positive integer pile. To minimize the initial value, we set this final value to 1. Any larger choice would strictly increase all earlier reconstructed values.

### 3. Expand backward repeatedly

We apply the inverse transformation repeatedly:

a_{k-1} = x * a_k + 1

Starting from a_m = 1, we generate:

a_{m-1} = x + 1

a_{m-2} = x^2 + x + 1

and so on.

This pattern reveals that after k reverse steps, the value becomes a sum of powers of x.

### 4. Recognize the geometric structure

After m steps, the initial value is:

n = sum_{i=0 to m} x^i

This converts the sequential dependency into a closed form expression.

### 5. Compute efficiently under modulus

We compute x^{m+1} using fast exponentiation modulo 998244353. Then compute the modular inverse of x − 1 using Fermat’s theorem since the modulus is prime. Finally combine them into:

n = (x^{m+1} − 1) * inv(x − 1)

### Why it works

The reverse recurrence uniquely determines all previous states once the final state is fixed. Because each step is affine (a linear function plus constant), repeated composition yields a geometric progression. Every valid forward configuration corresponds to exactly one backward reconstruction, so choosing the minimal terminal value enforces the minimal initial value. The modular arithmetic preserves equality because all transformations are linear and the modulus is prime, ensuring inverses exist for x − 1.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modpow(a, e):
    res = 1
    while e:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

def solve():
    T = int(input())
    for _ in range(T):
        m, x = map(int, input().split())

        if x == 1:
            # degenerate case: sum of 1 repeated (m+1) times
            print((m + 1) % MOD)
            continue

        # geometric sum: (x^(m+1) - 1) / (x - 1)
        num = modpow(x, m + 1) - 1
        num %= MOD

        den_inv = modpow(x - 1, MOD - 2)
        ans = num * den_inv % MOD
        print(ans)

if __name__ == "__main__":
    solve()
```

The code directly implements the closed-form derivation. The fast exponentiation function computes powers in logarithmic time, which is necessary because m can be up to 10^9. The modular inverse uses Fermat’s theorem since 998244353 is prime.

A special case x = 1 is handled separately because the geometric formula degenerates; the sum becomes m + 1 since every term is 1.

## Worked Examples

Consider a small case m = 3, x = 2. The sequence is:

n = 1 + 2 + 4 + 8 = 15

We compute it via the formula.

| Step | Value |
| --- | --- |
| m+1 exponent | 4 |
| 2^4 | 16 |
| numerator | 15 |
| inverse of 1 | 1 |
| result | 15 |

This confirms the closed form matches direct expansion.

Now consider m = 2, x = 3:

n = 1 + 3 + 9 = 13

| Step | Value |
| --- | --- |
| m+1 exponent | 3 |
| 3^3 | 27 |
| numerator | 26 |
| inverse of 2 | 499122177 |
| result | 13 |

This trace shows that modular inversion correctly reconstructs the arithmetic sum even under modulus.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log m) per test | fast exponentiation for x^(m+1) and modular inverse |
| Space | O(1) | only a few integers are stored |

The solution comfortably handles up to 10^3 test cases since each runs in logarithmic time with respect to m, avoiding any dependence on the large linear parameter.

## Test Cases

```python
import sys, io

MOD = 998244353

def modpow(a, e):
    res = 1
    while e:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

def solve():
    input = sys.stdin.readline
    T = int(input())
    for _ in range(T):
        m, x = map(int, input().split())
        if x == 1:
            print((m + 1) % MOD)
            continue
        num = (modpow(x, m + 1) - 1) % MOD
        den = modpow(x - 1, MOD - 2)
        print(num * den % MOD)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    sys.stdin = old_stdin
    return out.getvalue().strip()

# sample-like checks
assert run("1\n3 2\n") == "15"
assert run("1\n2 3\n") == "13"

# edge cases
assert run("1\n0 5\n") == "1"
assert run("1\n5 1\n") == "6"
assert run("1\n1 2\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| m=3,x=2 | 15 | geometric expansion correctness |
| m=2,x=3 | 13 | modular inverse correctness |
| m=0,x=5 | 1 | empty chain behavior |
| m=5,x=1 | 6 | degenerate x=1 handling |
| m=1,x=2 | 3 | single transition correctness |

## Edge Cases

When x = 1, each step becomes a − 1 = 1 * next_value, so every step simply subtracts one. Starting from the last value 1, reversing m times gives n = m + 1. The implementation explicitly handles this case because the geometric formula would attempt division by zero modulo MOD.

When m = 0, there is effectively no transformation. The only valid value is n = 1, since the final child is also the first.

For x = 2 with large m, values grow exponentially, but the modular exponentiation prevents overflow. The recurrence is stable under modulo because all operations are linear and handled through exponentiation rather than iteration.
