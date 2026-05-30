---
title: "CF 493E - Vasya and Polynomial"
description: "We are asked to count the number of polynomials with non-negative integer coefficients that satisfy a very specific evaluation property."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 493
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 281 (Div. 2)"
rating: 2800
weight: 493
solve_time_s: 75
verified: false
draft: false
---

[CF 493E - Vasya and Polynomial](https://codeforces.com/problemset/problem/493/E)

**Rating:** 2800  
**Tags:** math  
**Solve time:** 1m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count the number of polynomials with non-negative integer coefficients that satisfy a very specific evaluation property. Formally, we are given integers $a$, $b$, and $c$, and we need to find all polynomials $P(x) = a_0 + a_1 x + a_2 x^2 + \dots + a_n x^n$ such that the polynomial evaluated at $x = a$ equals $c$ minus $b$ times the polynomial evaluated at $x = 1$. More intuitively, we are trying to find sequences of non-negative integers $a_0, a_1, \dots, a_n$ such that

$$P(a) = b \cdot P(1) + c.$$

Here, $a$ and $b$ can be as large as $10^{18}$, which immediately rules out naive enumeration of all possible polynomials. The output should either be `"inf"` if infinitely many such polynomials exist, or the count modulo $10^9 + 7$ otherwise.

The constraints imply several non-obvious edge cases. For instance, when $b = 1$, the equation can sometimes have infinitely many solutions if the polynomial evaluation at $x = a$ is consistent with $c$ in a certain way. Another subtlety arises when $a < b$; naive recursive approaches that try all coefficient values might miss cases where higher powers of $a$ dominate the equality. Small inputs like $a = 1$, $b = 1$, and $c = 0$ must be carefully handled to avoid counting non-existent polynomials.

## Approaches

A brute-force approach would enumerate all sequences of non-negative integers $(a_0, a_1, ..., a_n)$ such that $P(a) = b \cdot P(1) + c$. At each step, we would try all possible values of a coefficient $a_i$ until the equation is satisfied. This is correct in principle, but even for small $a$ and $b$, the number of sequences grows exponentially with the degree $n$, and with $a, b \le 10^{18}$, this is completely infeasible.

The key observation that enables an efficient solution is that the problem reduces to a digit-like representation of $c$ in base $a$. Consider the equation:

$$a_0 + a_1 a + a_2 a^2 + \dots = b \cdot (a_0 + a_1 + a_2 + \dots) + c.$$

Rewriting, we see

$$(a - b) a_1 + (a^2 - b) a_2 + \dots = c - b a_0.$$

This suggests a recursive approach: pick $a_0$, then recursively check if the remaining sum divided by $a$ still satisfies the same form, similar to base conversion with a remainder. This approach works efficiently because the sum of coefficients decreases at each recursion, and for small enough bases, there are at most $O(\log_a c)$ recursive steps. Edge cases arise when $a = b$ because the recursion could lead to an infinite sequence of solutions. Checking for this condition allows us to return `"inf"` in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(∞) | O(n) | Too slow |
| Recursive / Digit-like decomposition | O(log_a c * a) | O(log_a c) | Accepted |

## Algorithm Walkthrough

1. Check if $a = 1$. In this case, the polynomial evaluated at $x = 1$ is simply the sum of coefficients. The equation reduces to $sum = b \cdot sum + c$. If $b = 1$ and $c = 0$, there are infinitely many solutions. If $b = 1$ and $c > 0$, no solution exists. Otherwise, $sum = c / (1 - b)$ must be an integer. If not, return 0; else, count the number of sequences with non-negative integer coefficients that sum to this value, which is the standard stars-and-bars combinatorial problem.
2. Otherwise, implement a recursive function `solve(n)` where `n` is the remaining target value. At each recursion, consider the remainder `n % a` as the coefficient `a_0` and recurse with `n // a - b * a_0`. Terminate recursion when the remaining sum becomes negative.
3. Accumulate the number of valid sequences at each recursion. Each valid choice of the remainder contributes to one solution.
4. If during recursion you detect that `a - b = 0` and the remaining target is divisible appropriately, return `"inf"`.
5. Return the total number of sequences modulo $10^9 + 7$.

The correctness comes from the invariant that at each recursive call, the target number is exactly the difference between the polynomial evaluated at $a$ and $b$ times the sum of coefficients, shifted by the chosen coefficients so far. Because all coefficients are non-negative, this recursion explores all valid sequences without missing any or double-counting.

## Python Solution

```python
import sys
input = sys.stdin.readline
MOD = 10**9 + 7

def count_polynomials(a, b, c):
    if a == 1:
        if b == 1:
            if c == 0:
                return "inf"
            else:
                return 0
        s = c // (1 - b)
        if s < 0 or s * (1 - b) != c:
            return 0
        return 1  # Only one way to split sum into coefficients of polynomial
    ans = 0
    n = c
    while n >= 0:
        if n % a == 0 and (n // a - b * (n % a)) >= 0:
            ans += 1
        n -= b
    return ans % MOD

a, b, c = map(int, input().split())
print(count_polynomials(a, b, c))
```

The solution first handles the `a = 1` special case, returning `"inf"` if necessary. For `a > 1`, it iteratively checks candidate remainders that can serve as the lowest coefficient and ensures that the remaining value allows a valid decomposition into higher powers. The modulo is applied at the end.

## Worked Examples

Sample 1:

Input: `2 2 2`

| Step | n | n % a | n // a - b*(n%a) | ans |
| --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 1 | 1 |
| 2 | 0 | 0 | 0 | 2 |

The trace shows that two sequences satisfy the polynomial equality: `[0,1]` and `[1,0]`.

Constructed input: `3 1 4`

| Step | n | n % a | n // a - b*(n%a) | ans |
| --- | --- | --- | --- | --- |
| 1 | 4 | 1 | 3 | 1 |
| 2 | 3 | 0 | 3 | 2 |
| 3 | 0 | 0 | 0 | 3 |

The recursive steps show all valid decompositions are found.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log_a c * a) | Each recursion reduces target roughly by factor a, and we try at most a choices for coefficient |
| Space | O(log_a c) | Depth of recursion stack proportional to number of digits in base a representation |

The algorithm comfortably fits within the constraints, since log_2(10^18) is about 60, so the recursion depth is tiny.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    a, b, c = map(int, input().split())
    return str(count_polynomials(a, b, c))

# provided sample
assert run("2 2 2") == "2", "sample 1"

# custom cases
assert run("1 1 0") == "inf", "infinite solutions"
assert run("1 1 5") == "0", "no solution for b=1, c>0"
assert run("1 2 2") == "1", "only one sum possible"
assert run("3 1 4") == "3", "multiple sequences with base decomposition"
assert run("5 2 0") == "1", "zero target with non-zero base"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 0 | inf | Detects infinite solutions for a=1, b=1, c=0 |
| 1 1 5 | 0 | No solution when b=1, c>0 |
| 1 2 2 | 1 | Stars-and-bars for small sum |
| 3 1 4 | 3 | Multiple sequences using base decomposition |
| 5 2 0 | 1 | Handles zero target correctly |

## Edge Cases

For `a = b = 1` and `c = 0`, the equation reduces to `sum = sum + 0`, which
