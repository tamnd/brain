---
title: "CF 104349B - Least SigDig"
description: "We are given a sequence of independent test cases. Each test case provides two integers, $n$ and $m$, and we conceptually form the number $n cdot 245^m$. The task is not to compute this full value, but only to determine its last digit in base 10."
date: "2026-07-01T18:14:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104349
codeforces_index: "B"
codeforces_contest_name: "TheForces Round #13 (Boombastic-Forces)"
rating: 0
weight: 104349
solve_time_s: 89
verified: false
draft: false
---

[CF 104349B - Least SigDig](https://codeforces.com/problemset/problem/104349/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of independent test cases. Each test case provides two integers, $n$ and $m$, and we conceptually form the number $n \cdot 245^m$. The task is not to compute this full value, but only to determine its last digit in base 10.

So the real output question is about the units digit of a product where one factor is a fixed base $n$, and the other factor is a large power of 245. Since only the last digit is requested, all higher place values are irrelevant and can be ignored entirely.

The constraints are large: both $n$ and $m$ can go up to $10^9$, and there are up to $10^3$ test cases. Any approach that attempts to compute $245^m$ directly, even with fast exponentiation, is unnecessary because the exponent itself is large but the quantity we care about is extremely small in structure, only one digit.

The key implication of the constraints is that the solution must reduce everything to modular arithmetic on the last digit only. Any attempt to handle full integers or even full powers will be wasteful and unnecessary.

A subtle edge case appears when $n = 0$. In this case the product is always zero regardless of $m$, so the answer is always 0. Another important edge case is when $m = 0$. Then $245^0 = 1$, so the answer is simply the last digit of $n$. These cases are easy to overlook if one focuses only on the exponent.

## Approaches

A brute-force idea would be to compute $245^m$ explicitly and multiply by $n$, then extract the last digit. Even if we switch to exponentiation by squaring, we are still working with large integers unnecessarily. In Python this might survive small inputs, but for $m$ up to $10^9$, the intermediate values grow quickly unless aggressively reduced, and the multiplication step becomes meaningless overhead since only the last digit is needed.

The key observation is that last digits behave cyclically under multiplication. Since we only care about the last digit of the final product, we can reduce both $n$ and $245$ modulo 10 immediately. This transforms the problem into computing:

$$(n \bmod 10) \cdot (5^m \bmod 10)$$

because 245 ends in 5.

Now the structure becomes very simple. Any power of 5 has a stable last digit: once we multiply 5 by itself even once, the result always ends in 5. So for all $m \ge 1$, $5^m$ ends in 5, while $5^0 = 1$.

This reduces the entire problem to a constant-time per test case decision.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(m)$ or worse per test | $O(1)$ | Too slow |
| Optimal | $O(1)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

We reduce the problem to last-digit arithmetic and handle the exponent behavior of 5 explicitly.

1. Read $n$ and $m$ for each test case. Only their last digits matter, so we immediately compute $n \% 10$.
2. Handle the special case $n = 0$. If the first factor is zero, the product is always zero, so we can output 0 without further computation.
3. Check whether $m = 0$. If so, the expression becomes $n \cdot 1$, so the answer is simply $n \% 10$.
4. If $m \ge 1$, replace $245^m$ with its last digit behavior. Since 245 ends in 5 and $5^m$ ends in 5 for all positive $m$, the second factor contributes a fixed last digit of 5.
5. Multiply the last digit of $n$ with 5 and output the last digit of that product.

The key idea is that exponentiation collapses into a constant pattern once we reduce to last digits.

### Why it works

The correctness comes from the fact that the last digit of a product depends only on the last digits of its factors. Formally, if $a \equiv a' \pmod{10}$ and $b \equiv b' \pmod{10}$, then $ab \equiv a'b' \pmod{10}$. This allows us to replace $n$ with $n \% 10$ and $245^m$ with $(5^m \% 10)$ without affecting the final answer.

The second property is that powers of 5 stabilize modulo 10: for all $m \ge 1$, $5^m \equiv 5 \pmod{10}$. This removes the need for any exponentiation logic. The algorithm is therefore guaranteed to produce the same last digit as the original expression.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())

        if n == 0:
            print(0)
            continue

        last_n = n % 10

        if m == 0:
            print(last_n)
        else:
            print((last_n * 5) % 10)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the reduction to last-digit arithmetic. The only branching logic is separating the $m = 0$ case from $m \ge 1$, because exponentiation identity differs there. The multiplication by 5 is safe to perform directly because we only care about the final digit.

The most common mistake is attempting to compute $245^m$ using exponentiation without reducing modulo 10 early. That is unnecessary work and obscures the simple periodic behavior of the last digit.

## Worked Examples

Consider two representative cases.

First input: $n = 31, m = 1$

We track only last digits.

| Step | n % 10 | m | 5^m mod 10 | result |
| --- | --- | --- | --- | --- |
| init | 1 | 1 | - | - |
| compute | 1 | 1 | 5 | 1 × 5 = 5 |

The output is 5, matching the fact that $31 \cdot 245$ ends in 5.

Second input: $n = 12, m = 2$

| Step | n % 10 | m | 5^m mod 10 | result |
| --- | --- | --- | --- | --- |
| init | 2 | 2 | - | - |
| compute | 2 | 2 | 5 | 2 × 5 = 10 → 0 |

The output is 0, showing how multiplication with 5 forces a zero last digit when the other factor is even.

These examples confirm that the exponent has no effect beyond determining whether we use 1 (when $m=0$) or 5 (when $m>0$).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t)$ | Each test case requires only constant-time arithmetic and branching |
| Space | $O(1)$ | No additional storage beyond variables |

The solution is well within limits since even for $10^3$ test cases, we perform only a few integer operations per case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose  # harmless import
    input = sys.stdin.readline

    def solve():
        t = int(input())
        for _ in range(t):
            n, m = map(int, input().split())

            if n == 0:
                print(0)
                continue

            last_n = n % 10

            if m == 0:
                print(last_n)
            else:
                print((last_n * 5) % 10)

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout
    return out

# provided samples
assert run("3\n1 1\n2 2\n12 2\n") == "5\n0\n0"

# minimum input
assert run("1\n0 0\n") == "0"

# m = 0 case
assert run("1\n987 0\n") == "7"

# large n, m > 0
assert run("1\n999999999 1000000000\n") == "5"

# even n with m > 0 leading to zero
assert run("1\n20 5\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 | 0 | zero edge case |
| 987 0 | 7 | identity power case |
| 999999999 1000000000 | 5 | large exponent stability |
| 20 5 | 0 | even digit × 5 behavior |

## Edge Cases

For $n = 0, m = 0$, the algorithm immediately returns 0 due to the zero check, matching $0 \cdot 1 = 0$.

For $n = 987, m = 0$, we bypass the power logic and return $987 \% 10 = 7$, correctly handling the identity exponent.

For $n = 20, m = 5$, we take last digit 0 and multiply by 5, producing 0. Even though the exponent is large, the reduction makes the result immediate and stable.

For very large $m$, such as $10^9$, the algorithm does not attempt exponentiation. It relies on the fact that any positive power of 5 has last digit 5, so the computation remains constant time regardless of magnitude.
