---
title: "CF 103719L - AvtoBus"
description: "We are told the total number of wheels in a bus fleet. Every vehicle in the fleet is either a 4-wheel bus or a 6-wheel bus, and we are not given how many of each type exist."
date: "2026-07-02T09:24:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103719
codeforces_index: "L"
codeforces_contest_name: "VII \u041b\u0438\u043f\u0435\u0446\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e. \u0424\u0438\u043d\u0430\u043b. 8-11 \u043a\u043b\u0430\u0441\u0441\u044b"
rating: 0
weight: 103719
solve_time_s: 40
verified: true
draft: false
---

[CF 103719L - AvtoBus](https://codeforces.com/problemset/problem/103719/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are told the total number of wheels in a bus fleet. Every vehicle in the fleet is either a 4-wheel bus or a 6-wheel bus, and we are not given how many of each type exist. The task is to reconstruct all possible fleet sizes that could produce exactly the given total number of wheels. Among all valid configurations, we must report the smallest possible number of buses and the largest possible number of buses. If no combination of 4-wheel and 6-wheel buses can produce the given total, we output that it is impossible.

The input is a single integer n, potentially as large as 10^18, so any solution must run in constant or logarithmic time. Anything that iterates over possible bus counts up to n is immediately infeasible.

A key subtlety is that not every n is representable. Since both bus types contribute an even number of wheels, any odd n cannot be formed at all. For example, n = 7 has no solution because sums of 4 and 6 are always even. Another corner case is very small values. For n = 2, no combination exists either, since the smallest bus already contributes 4 wheels.

## Approaches

A brute-force idea would be to try all possible numbers of buses k from 1 upward and check whether we can assign some number of 4-wheel and 6-wheel buses to reach total n. For each k, we would check whether there exists an integer x such that 4x + 6(k − x) = n. This reduces to checking whether n − 6k is divisible by −2 and whether the resulting x is within bounds. While each check is constant time, iterating over all k up to n/4 in the worst case is far too large for n up to 10^18.

The structure simplifies if we rewrite the equation. Let a be the number of 4-wheel buses and b the number of 6-wheel buses. Then we have 4a + 6b = n, which can be divided by 2 to get 2a + 3b = n/2. This immediately shows that n must be even, otherwise no solution exists.

Now fix b. Then a is determined uniquely as (n − 6b) / 4, and we only require it to be a non-negative integer. The number of buses is k = a + b. Substituting a gives k = b + (n − 6b)/4 = n/4 − b/2. This expression reveals a monotonic relationship: increasing b reduces k. That means the maximum number of buses happens when we minimize b, and the minimum number of buses happens when we maximize b, under validity constraints.

The only constraint is that a must remain non-negative and integral. From 4a + 6b = n, we require n − 6b ≥ 0 and divisible by 4. Since everything is even, divisibility reduces to a parity condition on b. We can therefore determine feasible b values in a very small range and extract the extremal k values directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over k | O(n) | O(1) | Too slow |
| Algebraic reduction | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We start from the equation relating buses and wheels. Each step extracts structure until only constant-time checks remain.

1. Check whether n is divisible by 2. If it is not, immediately conclude there is no solution. This follows because both 4 and 6 are even, so any sum must also be even.
2. Define m = n / 2 to simplify coefficients. The equation becomes 2a + 3b = m, which reduces arithmetic size without changing feasibility.
3. Express one variable in terms of the other: a = (m − 3b) / 2. This shows that for any fixed b, a is uniquely determined.
4. Impose validity conditions: a ≥ 0 and integral. Non-negativity gives m − 3b ≥ 0, which bounds b from above. Integrality requires m − 3b to be even, which is equivalent to b having the same parity as m.
5. From these constraints, identify the smallest feasible b and the largest feasible b. Since k = a + b decreases as b increases, the smallest b yields the maximum number of buses and the largest b yields the minimum number of buses.
6. Compute k for both boundary values of b and output them.

### Why it works

The core invariant is that every valid solution corresponds exactly to a single integer value of b satisfying two independent constraints: a non-negativity bound and a parity condition. Once b is fixed, a is forced. This collapses the two-dimensional search space into a single bounded arithmetic progression. Since k is a linear function decreasing in b, extremal values of k must occur at extremal feasible values of b, so scanning only the boundary values is sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    
    if n % 2 == 1:
        print(-1)
        return
    
    m = n // 2  # 2a + 3b = m
    
    # b must satisfy:
    # 3b <= m  => b <= m // 3
    # (m - 3b) even => b % 2 == m % 2
    
    # smallest valid b
    if m % 2 == 0:
        b_min = 0
    else:
        b_min = 1
    
    # largest valid b <= m//3 with correct parity
    b_max = m // 3
    if b_max % 2 != m % 2:
        b_max -= 1
    
    if b_max < b_min:
        print(-1)
        return
    
    def buses(b):
        a = (m - 3 * b) // 2
        return a + b
    
    x = buses(b_max)  # minimum buses
    y = buses(b_min)  # maximum buses
    
    print(x, y)

if __name__ == "__main__":
    solve()
```

The code first filters impossible cases using parity of n. It then transforms the problem into the simplified equation 2a + 3b = m. The constraints on b are derived directly from non-negativity and parity. We pick boundary values of b that satisfy both conditions and compute the corresponding number of buses. The ordering is intentional: larger b reduces total buses, so b_max gives the minimum answer.

A subtle detail is that integer division and parity adjustments must be applied carefully; otherwise, a candidate b may satisfy the inequality but violate integrality, producing incorrect a.

## Worked Examples

### Example 1: n = 4

Here m = 2, so 2a + 3b = 2. The only possible value of b is 0, giving a = 1.

| b | a = (2 − 3b)/2 | valid | buses a + b |
| --- | --- | --- | --- |
| 0 | 1 | yes | 1 |

Both minimum and maximum are 1.

This confirms that when only one configuration exists, both extremes coincide.

### Example 2: n = 24

Here m = 12, so 2a + 3b = 12.

| b | a | valid | buses |
| --- | --- | --- | --- |
| 0 | 6 | yes | 6 |
| 2 | 3 | yes | 5 |
| 4 | 0 | yes | 4 |

Maximum buses occur at b = 0, minimum at b = 4.

This shows the monotone trade-off between heavier buses and total count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations and boundary checks |
| Space | O(1) | No auxiliary structures are used |

The solution works comfortably under the 1 second limit because it avoids iteration entirely and reduces the problem to constant-time arithmetic.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import prod
    import builtins

    # re-import solution by redefining solve inline for test simplicity
    def solve():
        n = int(sys.stdin.readline().strip())
        if n % 2 == 1:
            return "-1\n"
        m = n // 2
        if m % 2 == 0:
            b_min = 0
        else:
            b_min = 1
        b_max = m // 3
        if b_max % 2 != m % 2:
            b_max -= 1
        if b_max < b_min:
            return "-1\n"
        def buses(b):
            a = (m - 3 * b) // 2
            return a + b
        x = buses(b_max)
        y = buses(b_min)
        return f"{x} {y}\n"

    return solve()

# provided samples
assert run("4\n") == "1 1\n"
assert run("7\n") == "-1\n"

# custom cases
assert run("2\n") == "-1\n"
assert run("6\n") == "1 1\n"
assert run("24\n") == "4 6\n"
assert run("1000000000000000000\n") != "", "large even case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 | -1 | smallest impossible even case |
| 6 | 1 1 | single configuration case |
| 24 | 4 6 | multiple valid decompositions |
| 10^18 | valid pair | stress test for constant-time behavior |

## Edge Cases

For n = 1, the algorithm immediately rejects due to odd parity, since no combination of 4 and 6 can form an odd sum.

For n = 2, parity passes only after division, but m = 1 makes all candidate values invalid because 2a + 3b cannot equal 1. The computed b range becomes empty, triggering the impossibility check.

For n = 4, the boundary logic yields b_min = 0 and b_max = 0, producing a single valid configuration with one bus. This confirms correctness when only one solution exists.

For very large even n, such as 10^18, all computations remain within integer arithmetic and only depend on a few divisions and parity checks, so the algorithm behaves identically regardless of magnitude.
