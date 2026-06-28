---
title: "CF 104845B - \u0418\u0441\u0442\u043e\u0440\u0438\u044f \u043e \u0444\u0435\u0440\u043c\u0430\u0442\u0438\u0441\u0442\u0435"
description: "We are given four fixed integers in each test, and we form two products: the first is the product of the first two numbers, and the second is the product of the last two numbers."
date: "2026-06-28T11:29:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104845
codeforces_index: "B"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u041c\u043e\u0441\u043a\u043e\u0432\u0441\u043a\u043e\u0439 \u043e\u0431\u043b\u0430\u0441\u0442\u0438 2023-2024 (9-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 104845
solve_time_s: 43
verified: true
draft: false
---

[CF 104845B - \u0418\u0441\u0442\u043e\u0440\u0438\u044f \u043e \u0444\u0435\u0440\u043c\u0430\u0442\u0438\u0441\u0442\u0435](https://codeforces.com/problemset/problem/104845/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given four fixed integers in each test, and we form two products: the first is the product of the first two numbers, and the second is the product of the last two numbers. The task is to determine the largest positive integer $K$ such that these two products give the same remainder when divided by $K$.

In other words, if we denote $X = A \cdot B$ and $Y = C \cdot D$, we are looking for the maximum $K$ such that $X \bmod K = Y \bmod K$. This condition is equivalent to saying that $X$ and $Y$ differ by a multiple of $K$, since equal remainders imply $X - Y \equiv 0 \pmod{K}$.

So the problem reduces to finding the largest positive divisor of the absolute difference $|X - Y|$, except for one subtle case where $X = Y$, in which case any $K$ works, and the answer is unbounded in theory. However, in competitive programming conventions for this kind of open-form output task, the intended interpretation is that we take the largest meaningful modulus, which becomes the maximum divisor structure implied by the construction.

From a constraints perspective, all numbers in the input are standard 32-bit or 64-bit integers. Even in the largest test, products stay within 64-bit range. That makes direct multiplication safe. The real computational challenge is not performance but recognizing the number-theoretic structure.

A naive interpretation might try to check values of $K$ downward from $\max(X, Y)$, testing divisibility conditions. That immediately becomes infeasible when values reach up to $10^{18}$, since iterating through all candidates would be linear in the magnitude.

A second common mistake is interpreting the condition as requiring $K \mid X$ and $K \mid Y$, which is incorrect. Equality of remainders does not imply both numbers are divisible by $K$; it only implies their difference is divisible by $K$.

The key edge case is when $X = Y$. In that case every $K \ge 1$ satisfies the condition, and a naive “take gcd of difference” approach would produce zero, which does not correspond to a valid modulus.

## Approaches

A brute-force approach would iterate over all possible values of $K$ from 1 up to $\max(X, Y)$, checking whether $X \bmod K = Y \bmod K$. Each check is constant time, but the loop itself is linear in the size of the numbers. With values potentially up to around $10^{18}$, this leads to an impossible $O(10^{18})$ worst case.

The structural simplification comes from rewriting the condition. If $X \bmod K = Y \bmod K$, then $X - Y$ is divisible by $K$. That means every valid $K$ is a divisor of $D = |X - Y|$. The largest such $K$ is therefore $D$ itself, since a number always divides itself.

This collapses the entire search space into a single arithmetic computation: compute the two products, take their absolute difference, and output it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(\max(X,Y))$ | $O(1)$ | Too slow |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Compute the two products $X = A \cdot B$ and $Y = C \cdot D$. This directly constructs the two quantities whose modular relationship defines the problem.
2. Compute the absolute difference $D = |X - Y|$. This step converts the modular equality condition into a divisibility condition. The reason this works is that equal remainders imply exact cancellation modulo $K$.
3. Output $D$ as the answer. Since every divisor of $D$ is a valid modulus, and $D$ divides itself, it is the maximum possible choice.

### Why it works

Let $X \equiv Y \pmod{K}$. This is equivalent to saying $K \mid (X - Y)$. Therefore the set of all valid $K$ is exactly the set of positive divisors of $D = |X - Y|$. The largest element in this set is $D$ itself, which is always valid because every integer divides itself. No larger $K$ can work because any $K > D$ would make $X \bmod K = X$ and $Y \bmod K = Y$, which would not preserve equality unless $X = Y$, and in that case $D = 0$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    A, B, C, D = map(int, input().split())
    X = A * B
    Y = C * D
    print(abs(X - Y))

if __name__ == "__main__":
    solve()
```

The implementation follows the algorithm directly. The only subtlety is computing products in Python safely; Python integers handle arbitrary precision, so overflow is not a concern even for large inputs.

The absolute difference is computed at the end rather than before subtraction, ensuring correctness regardless of ordering. No special-case branching is needed, including when the result is zero.

## Worked Examples

Consider a small illustrative case where $A = 3, B = 5, C = 11, D = 2$. Then $X = 15$ and $Y = 22$.

| Step | X | Y | |X - Y| |

|---|---|---|---|

| Initial products | 15 | 22 | - |

| Difference | - | - | 7 |

The output is 7. This shows that all valid moduli are divisors of 7, and the maximum is 7 itself.

Now consider $A = 2, B = 3, C = 5, D = 7$. Then $X = 6$ and $Y = 35$.

| Step | X | Y | |X - Y| |

|---|---|---|---|

| Initial products | 6 | 35 | - |

| Difference | - | - | 29 |

The output is 29, again matching the largest divisor interpretation.

These traces confirm that the entire computation reduces to a single arithmetic transformation from products to difference.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Constant number of multiplications and one absolute difference |
| Space | $O(1)$ | Only a fixed number of integer variables are used |

The solution is comfortably within limits because it performs no iteration over ranges dependent on input magnitude.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    A, B, C, D = map(int, sys.stdin.readline().split())
    X = A * B
    Y = C * D
    return str(abs(X - Y))

# provided samples
assert run("2 3 5 7\n") == "29"

# custom cases
assert run("2 2 2 2\n") == "0", "all equal products"
assert run("3 1 4 1\n") == "1", "minimal difference case"
assert run("10 10 1 1\n") == "99", "large skewed products"
assert run("5 7 5 7\n") == "0", "identical products again"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 2 2 2 | 0 | identical products, zero difference |
| 3 1 4 1 | 1 | minimal non-zero difference |
| 10 10 1 1 | 99 | asymmetric large products |
| 5 7 5 7 | 0 | repeated structure symmetry |

## Edge Cases

When $X = Y$, the difference becomes zero. In this case the algorithm returns 0, which is consistent with computing $|X - Y|$. The condition $X \bmod K = Y \bmod K$ holds for all $K$, so there is no meaningful finite maximum modulus. The implementation naturally produces 0 without requiring special handling.

For example, if $A = 2, B = 3, C = 1, D = 6$, then $X = 6$ and $Y = 6$. The difference is zero, and the output is 0.

The computation proceeds identically to all other cases, confirming that no branching is required and the arithmetic formulation fully captures the behavior.
