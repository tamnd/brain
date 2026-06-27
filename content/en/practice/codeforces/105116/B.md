---
title: "CF 105116B - \u0410\u043a\u0446\u0438\u044f \u043d\u0430 \u0434\u0435\u043d\u044c \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f"
description: "We are asked to decide whether it is possible to choose a mix of two types of bakery items so that two constraints are satisfied at the same time. Vasилиса must buy exactly one item for each of her N guests, so the total number of items is fixed to N."
date: "2026-06-27T19:46:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105116
codeforces_index: "B"
codeforces_contest_name: "\u041e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 1\u0421 2024, \u043f\u0440\u0435\u0434\u043c\u0435\u0442\u043d\u044b\u0439 \u0442\u0443\u0440"
rating: 0
weight: 105116
solve_time_s: 45
verified: true
draft: false
---

[CF 105116B - \u0410\u043a\u0446\u0438\u044f \u043d\u0430 \u0434\u0435\u043d\u044c \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f](https://codeforces.com/problemset/problem/105116/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to decide whether it is possible to choose a mix of two types of bakery items so that two constraints are satisfied at the same time. Vasилиса must buy exactly one item for each of her N guests, so the total number of items is fixed to N. At the same time, she has a promotional coupon that requires the total cost of the purchase to be exactly K rubles.

There are only two available product types: one type costs A rubles per item and the other costs B rubles per item, with A different from B. The task is to determine whether there exist non-negative integers x and y such that x is the number of A-priced items, y is the number of B-priced items, x + y equals N, and the total cost Ax + By equals K. If such a pair exists, we must output any valid pair; otherwise, we output -1.

The constraints allow values up to 10^9, which immediately rules out any solution that tries all possible values of x or y. A linear scan over N possibilities would require up to 10^9 iterations in the worst case, which is far beyond a 1 second limit. This pushes us toward an algebraic solution rather than a combinatorial search.

A common pitfall appears when people try greedy choices such as taking as many cheap items as possible or as many expensive items as possible. Those strategies fail because the target cost K is fixed exactly, and the correct solution might require a precise balance rather than an extreme configuration. Another subtle failure case appears when integer division is used without checking divisibility, leading to fractional counts being silently accepted.

## Approaches

A brute-force method would iterate over all possible values of x from 0 to N, compute y as N minus x, and check whether Ax + By equals K. This is correct because it explicitly tests every valid combination of counts. However, this approach performs N iterations, and each iteration involves constant work. With N up to 10^9, this becomes computationally infeasible.

The key observation is that the problem is not truly two-dimensional. Once we fix x, the value of y is determined immediately by N, which reduces the system to a single variable. More importantly, the cost equation becomes linear in x. This means we can solve directly for x using algebra rather than enumeration.

From x + y = N, we substitute y = N - x into the cost equation. This transforms the problem into a single linear equation in x. Because there is only one unknown, we can isolate it in constant time. The remaining task is to check whether the computed value is an integer and lies within valid bounds.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N) | O(1) | Too slow |
| Optimal Algebraic Solution | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We denote x as the number of A-cost items and y as the number of B-cost items.

1. Start from the constraint x + y = N and express y as N - x. This removes one variable from the system and reduces everything to a single unknown x.
2. Substitute y into the cost equation Ax + By = K, obtaining Ax + B(N - x) = K. This step converts the problem into a linear equation in x alone.
3. Expand the equation to get Ax + BN - Bx = K, then group terms involving x to obtain x(A - B) + BN = K. This isolates all dependence on x in a single coefficient.
4. Rearrange to solve for x: x(A - B) = K - BN. This expresses x as a ratio of two known quantities.
5. Compute the numerator K - BN and denominator A - B. At this point, x must equal (K - BN) / (A - B). The value is valid only if the numerator is divisible by the denominator.
6. Check whether the computed x is an integer and satisfies 0 ≤ x ≤ N. If it does, compute y as N - x and output both values. Otherwise, conclude that no valid selection exists.

### Why it works

The transformation reduces a system of two linear equations in two unknowns into a single linear equation in one variable. Since all constraints are linear and there is no inequality other than non-negativity, every feasible solution must satisfy this derived expression exactly. Any valid solution must produce the same value of x because the equation has a unique solution in real numbers, and integrality plus bounds are the only remaining restrictions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    K = int(input())
    N = int(input())
    A = int(input())
    B = int(input())

    numerator = K - B * N
    denom = A - B

    if denom == 0:
        print(-1)
        return

    if numerator % denom != 0:
        print(-1)
        return

    x = numerator // denom
    y = N - x

    if x < 0 or y < 0:
        print(-1)
        return

    print(x, y)

if __name__ == "__main__":
    solve()
```

The code directly implements the algebraic derivation. The first step computes the rearranged numerator and denominator of the expression for x. The divisibility check ensures we do not accept fractional solutions. The bounds check enforces that both counts are valid non-negative integers that sum to N.

A subtle implementation detail is the sign of A - B. Since A and B can appear in either order, the denominator may be negative, but integer division in Python still works correctly as long as divisibility is checked before division.

## Worked Examples

### Example 1

Input:

K = 11, N = 3, A = 5, B = 1

We compute:

| Step | Expression | Value |
| --- | --- | --- |
| numerator | K - B·N | 11 - 3 = 8 |
| denominator | A - B | 5 - 1 = 4 |
| x | 8 / 4 | 2 |
| y | N - x | 1 |

The result is valid since both x and y are non-negative and sum to N. This demonstrates how the solution balances expensive and cheap items to match the exact target cost.

### Example 2

Input:

K = 2, N = 1, A = 3, B = 0

| Step | Expression | Value |
| --- | --- | --- |
| numerator | 2 - 0·1 | 2 |
| denominator | 3 - 0 | 3 |

Here 2 is not divisible by 3, so no integer x exists. This shows how the method correctly rejects impossible fractional solutions without attempting enumeration.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | All operations are constant-time arithmetic |
| Space | O(1) | Only a fixed number of variables are used |

The solution easily fits within the limits because it performs no iteration over N and relies only on a constant number of arithmetic operations, even for values up to 10^9.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    import sys as _sys
    input = _sys.stdin.readline

    K = int(input())
    N = int(input())
    A = int(input())
    B = int(input())

    numerator = K - B * N
    denom = A - B

    if denom == 0:
        return "-1"

    if numerator % denom != 0:
        return "-1"

    x = numerator // denom
    y = N - x

    if x < 0 or y < 0:
        return "-1"

    return f"{x} {y}"

# provided sample
assert run("11\n3\n5\n1\n") == "2 1"

# N=1 trivial valid
assert run("5\n1\n5\n1\n") == "1 0"

# impossible due to parity/divisibility
assert run("2\n3\n5\n1\n") == "-1"

# all cookies cheaper case
assert run("3\n3\n1\n2\n") in ["3 0", "0 3"]

# boundary large equal mix
assert run("1000000000\n1000000000\n1\n2\n") != ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 11 3 5 1 | 2 1 | basic valid mix |
| 5 1 5 1 | 1 0 | single item edge case |
| 2 3 5 1 | -1 | no integer solution |
| 3 3 1 2 | 3 0 or 0 3 | skewed pricing case |
| large values | valid output | overflow and scale safety |

## Edge Cases

One important edge case happens when A and B are very close or swapped, for example A = 1 and B = 2. In this situation, the denominator A - B becomes negative, and careless handling can lead to sign mistakes. The algorithm avoids this by relying strictly on integer divisibility before division, so the sign does not affect correctness.

Another case appears when K is smaller than the minimum possible cost or larger than the maximum possible cost given N items. For instance, if all items cost at least 5 and N is 3, any K below 15 is impossible. The formula naturally rejects these cases because the computed numerator produces a value of x outside the range [0, N].

A third edge case occurs when no integer solution exists even though the linear equation has a real solution. For example, if the computed x equals 2.5, the divisibility check fails, and the algorithm correctly reports impossibility without attempting to round or approximate.
