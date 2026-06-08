---
title: "CF 1978B - New Bakery"
description: "In this problem, Bob is trying to maximize his profit from selling buns with a special promotion. He has n buns to sell, a usual price a for each bun, and a promotional parameter b."
date: "2026-06-08T17:10:27+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "math", "ternary-search"]
categories: ["algorithms"]
codeforces_contest: 1978
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 953 (Div. 2)"
rating: 800
weight: 1978
solve_time_s: 127
verified: true
draft: false
---

[CF 1978B - New Bakery](https://codeforces.com/problemset/problem/1978/B)

**Rating:** 800  
**Tags:** binary search, greedy, math, ternary search  
**Solve time:** 2m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

In this problem, Bob is trying to maximize his profit from selling buns with a special promotion. He has `n` buns to sell, a usual price `a` for each bun, and a promotional parameter `b`. The promotion allows him to choose an integer `k` and sell the first `k` buns at prices decreasing from `b` down to `b - k + 1`. The remaining buns, if any, are sold at the usual price `a`. The task is to determine the maximum total profit Bob can obtain by choosing the optimal `k`.

The input consists of multiple test cases. Each test case gives `n`, `a`, and `b`. The output is the maximum profit for each case. Since `n`, `a`, and `b` can be as large as `10^9` and there are up to `10^4` test cases, any solution that iterates over individual buns is too slow. We need a constant-time formula per test case to stay within the time limit.

A subtle edge case arises when `b` is very small or very large relative to `a` and `n`. For example, if `b <= a`, selling any buns at the promotional price will not increase profit. Conversely, if `b` is huge, it may be optimal to sell as many buns as allowed by the promotion. The naive solution that tries all values of `k` will time out, so a direct computation is necessary.

## Approaches

The naive approach iterates `k` from 0 to `min(n, b)`, computes the sum of the first `k` decreasing prices, adds `(n - k) * a`, and keeps track of the maximum. This is correct but requires up to `10^9` operations per test case in the worst case, which is infeasible.

The optimal approach comes from the observation that the total profit function in terms of `k` is quadratic and concave. The profit for `k` buns sold at the promotional price is `sum_{i=1}^k (b - i + 1) = k * b - k*(k-1)/2`. The remaining buns give `(n - k) * a`. Combining these, the total profit function is `profit(k) = k*b - k*(k-1)/2 + (n - k)*a`. This is a concave quadratic function in `k`, so the maximum occurs at the boundary or at the vertex. The vertex is at `k = b - a`, but `k` is limited to `[0, min(n, b)]`. Therefore, the optimal `k` is `max(0, min(b - a, min(n, b)))`.

This reduces the problem to a single computation per test case without loops. The arithmetic formula can be directly evaluated in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (iterate k) | O(n) | O(1) | Too slow |
| Direct computation formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n`, `a`, and `b`.
3. Compute the candidate number of promotional buns `k` as `b - a`. This comes from differentiating the quadratic profit function; it is the unconstrained optimum.
4. Clamp `k` to the feasible range `[0, min(n, b)]` using `max(0, min(k, min(n, b)))`.
5. Compute the profit from the first `k` buns as the sum of decreasing prices: `k * b - k * (k - 1) // 2`.
6. Compute the profit from the remaining `n - k` buns at price `a`: `(n - k) * a`.
7. Add the two components to get total profit.
8. Print the total profit.

Why it works: The profit function in terms of `k` is a concave quadratic, so the maximum occurs either at the vertex or at the boundaries. Clamping `k` ensures we respect the number of buns and the promotion limit. Computing the sum via a formula avoids loops and ensures O(1) computation per test case.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    results = []

    for _ in range(t):
        n, a, b = map(int, input().split())
        k = b - a
        k = max(0, min(k, n, b))
        profit = k * b - k * (k - 1) // 2 + (n - k) * a
        results.append(str(profit))

    sys.stdout.write("\n".join(results) + "\n")

solve()
```

### Explanation

The code reads all test cases efficiently using `sys.stdin.readline`. For each case, it computes the optimal number of promotional buns using the derived formula. Clamping ensures that `k` respects all constraints. The sum of the first `k` decreasing prices is computed using the arithmetic series formula. The remaining buns are multiplied by the usual price. Results are collected and printed at the end for efficiency.

## Worked Examples

| Test Case | n | a | b | k | Profit Calculation | Total Profit |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 4 | 4 | 5 | 1 | 1_5 - 0 + 3_4 = 5 + 12 | 17 |
| 2 | 5 | 5 | 9 | 4 | 4_9 - 6 + 1_5 = 36 - 6 + 5 | 35 |
| 3 | 10 | 10 | 5 | 0 | 0 + 10*10 | 100 |

The tables show that for each input, computing `k` as `b - a` and clamping it yields the maximum profit, and the arithmetic sum correctly computes the total.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a few arithmetic operations per test case |
| Space | O(t) | Storing output strings for all test cases |

The solution comfortably fits within the constraints of up to 10^4 test cases and 1s time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("7\n4 4 5\n5 5 9\n10 10 5\n5 5 11\n1000000000 1000000000 1000000000\n1000000000 1000000000 1\n1000 1 1000\n") == \
       "17\n35\n100\n45\n1000000000000000000\n1000000000000000000\n500500", "sample 1"

# Custom tests
assert run("1\n1 5 5\n") == "5", "single bun edge"
assert run("1\n10 1 10\n") == "55", "all buns promotional"
assert run("1\n10 10 1\n") == "100", "promotion worse than normal"
assert run("1\n1000000000 1 1000000000\n") == "500000000500000000", "large numbers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5 5 | 5 | Single bun edge |
| 10 1 10 | 55 | Selling all buns under promotion |
| 10 10 1 | 100 | Promotion worse than normal price |
| 1e9 1 1e9 | 500000000500000000 | Large number arithmetic correctness |

## Edge Cases

When `b <= a`, the computed `k` becomes negative. Clamping to zero ensures that no buns are sold under the promotion, which is optimal. For example, `n=10, a=10, b=5` results in `k = max(0, min(-5, 10, 5)) = 0`. Profit is `10*10 = 100`, matching the expected result. Similarly, when `b` exceeds `n`, clamping ensures `k <= n` to avoid exceeding the number of buns. This guarantees correctness for all boundary conditions.
