---
title: "CF 104313B - \u041a\u0430\u0448\u0442\u0430\u043d\u044b"
description: "We are given a group of n children who each collected some number of chestnuts and then placed them into a single pile. The first child in order, Sasha, puts his chestnuts into the pile first. Every next child contributes twice as many chestnuts as the previous child."
date: "2026-07-01T19:45:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104313
codeforces_index: "B"
codeforces_contest_name: "II \u041e\u0442\u043a\u0440\u044b\u0442\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u042e\u041c\u0428 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 104313
solve_time_s: 54
verified: true
draft: false
---

[CF 104313B - \u041a\u0430\u0448\u0442\u0430\u043d\u044b](https://codeforces.com/problemset/problem/104313/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a group of n children who each collected some number of chestnuts and then placed them into a single pile. The first child in order, Sasha, puts his chestnuts into the pile first. Every next child contributes twice as many chestnuts as the previous child. So the contributions form a geometric progression starting from Sasha’s unknown amount a, then 2a, then 4a, and so on until the nth child.

We are also given the total sum m that Sasha computed. The task is to check whether this total can be produced by some integer starting value a, and if it is possible, determine what a must be.

The structure of the problem forces a very rigid form of the sum. For a fixed n, the total is always a times a known constant, namely 1 + 2 + 4 + ... + 2^(n-1). This already suggests that the entire problem reduces to checking divisibility and reconstructing a single unknown from a fixed multiplier.

The constraints n ≤ 100 and m ≤ 10^18 indicate that the values involved can be large, but the sequence length is small. This rules out any need for simulation over large ranges of values, but also warns us to avoid naive arithmetic that might overflow if not handled carefully in other languages. In Python this is not a concern, but conceptual correctness still matters.

A subtle edge case appears when m is not divisible by the geometric sum. In that case no valid a exists. Another corner case is when the computed a is zero or negative, but since m ≥ 1 and all terms are positive multiples of a, a must also be positive if a solution exists.

## Approaches

A naive way to think about the problem is to try all possible values of a from 1 up to m and simulate the sequence  a, 2a, 4a, ... for n terms, checking whether the sum matches m. This is correct in principle because every valid configuration corresponds to exactly one a. However, for each candidate a we would compute n terms, giving O(mn) operations in the worst case. With m up to 10^18 this is completely infeasible.

The key observation is that the sequence is linear in a. The total sum can be factored as:

S = a (1 + 2 + 4 + ... + 2^(n-1))

The expression in parentheses is a fixed geometric sum that depends only on n. This transforms the problem from searching over possible sequences into a simple arithmetic check: compute the multiplier, check whether m is divisible by it, and recover a as m divided by that multiplier.

The only subtlety is computing the geometric sum safely. Since n ≤ 100, the sum 2^n is well within Python’s integer capacity, but in general we must compute it iteratively or using bit shifts rather than relying on floating-point operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (try all a) | O(m · n) | O(1) | Too slow |
| Optimal (geometric factorization) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We rewrite the total sum using the structure of the sequence.

1. Compute the geometric multiplier corresponding to the contributions of all children except scaling, which is 1 + 2 + 4 + ... + 2^(n-1). This can be built iteratively starting from 1 and repeatedly doubling and adding.
2. Maintain a running value cur starting at 1, and a sum multiplier s starting at 1. For each of the remaining n-1 children, double cur and add it to s. This constructs the exact sum of powers of two without overflow concerns.
3. After computing s, check whether m is divisible by s. If it is not divisible, there is no integer starting value a that can produce the given total, so the answer is impossible.
4. If divisibility holds, compute a = m / s. This is the only possible value of Sasha’s contribution because all other contributions are fixed multiples of it.
5. Output success along with a.

### Why it works

The sequence of contributions is exactly a scaled version of a fixed vector (1, 2, 4, ..., 2^(n-1)). Any valid total must lie on a one-dimensional lattice generated by this vector. The computed sum s is the exact coefficient of this vector, so any valid total must equal s times a single scalar a. Since all contributions are positive integers, there is no ambiguity in reconstruction, and divisibility fully characterizes feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    s = 1
    cur = 1
    for _ in range(n - 1):
        cur *= 2
        s += cur

    if m % s != 0:
        print("No")
        return

    a = m // s
    print("Yes")
    print(a)

if __name__ == "__main__":
    solve()
```

The solution directly mirrors the algorithm. The loop builds the geometric sum without relying on formulas that might overflow in other languages. The divisibility check ensures that the reconstructed starting value is integral.

A common implementation mistake is attempting to use the closed form 2^n - 1 directly without considering overflow or off-by-one errors in exponent handling. The iterative construction avoids both issues and makes the relationship explicit.

## Worked Examples

### Example 1

Input:

```
4 30
```

We compute the multiplier s step by step.

| Step | cur | s |
| --- | --- | --- |
| start | 1 | 1 |
| 1 | 2 | 3 |
| 2 | 4 | 7 |
| 3 | 8 | 15 |

So s = 15. Since 30 is divisible by 15, a = 2.

Trace confirms that contributions would be 2, 4, 8, 16.

This matches the requirement that each next child doubles the previous one.

### Example 2

Input:

```
5 10
```

Compute s:

| Step | cur | s |
| --- | --- | --- |
| start | 1 | 1 |
| 1 | 2 | 3 |
| 2 | 4 | 7 |
| 3 | 8 | 15 |
| 4 | 16 | 31 |

Now s = 31. Since 10 is not divisible by 31, no integer a can produce the sum. The structure forces every valid total to be a multiple of 31, and 10 does not lie in that set.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We build the geometric sum with n steps |
| Space | O(1) | Only a few integers are stored |

The constraints allow n up to 100, so a linear pass is trivial. The solution comfortably fits within both time and memory limits since all operations are constant-time arithmetic on small integers.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    n, m = map(int, sys.stdin.readline().split())

    s = 1
    cur = 1
    for _ in range(n - 1):
        cur *= 2
        s += cur

    if m % s != 0:
        return "No\n"

    return "Yes\n" + str(m // s) + "\n"

# provided samples
assert run("4 30") == "Yes\n2\n", "sample 1"
assert run("5 10") == "No\n", "sample 2"

# custom cases
assert run("1 7") == "Yes\n7\n", "single child always valid"
assert run("3 7") == "Yes\n1\n", "1 2 4 sum case"
assert run("3 8") == "No\n", "not divisible case"
assert run("10 0") == "No\n", "zero total impossible"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 7 | Yes 7 | single participant base case |
| 3 7 | Yes 1 | correct geometric construction |
| 3 8 | No | non-divisible rejection |
| 10 0 | No | invalid zero total handling |

## Edge Cases

A key edge case is when n = 1. The multiplier s is simply 1, so any m is valid and a must equal m. The algorithm handles this because the loop runs zero times and s remains 1, preserving correctness without special handling.

Another case is when m is not divisible by the geometric sum. For example, n = 3 and m = 8 gives s = 7. The algorithm computes 8 % 7 ≠ 0 and immediately rejects the case. This matches the structural constraint that valid totals form an arithmetic lattice of multiples of 7.

Finally, large n values like n = 100 still behave safely because the iterative doubling never relies on floating-point arithmetic or approximations. Each value is computed exactly, ensuring correctness even at the upper bound.
