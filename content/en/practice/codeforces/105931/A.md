---
title: "CF 105931A - \u041d\u043e\u0432\u044b\u0439 \u0443\u043d\u0438\u0432\u0435\u0440\u0441\u0438\u0442\u0435\u0442"
description: "The university is enrolling up to n students in total. Every student must fall into one of two categories. If a student pays tuition, they contribute a fixed amount a to the university. If a student receives a scholarship, their funding comes from a sponsor."
date: "2026-06-22T15:43:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105931
codeforces_index: "A"
codeforces_contest_name: "\u0412\u0441\u0435\u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0438\u043c. \u041c\u0441\u0442\u0438\u0441\u043b\u0430\u0432\u0430 \u041a\u0435\u043b\u0434\u044b\u0448\u0430 - 2024"
rating: 0
weight: 105931
solve_time_s: 65
verified: true
draft: false
---

[CF 105931A - \u041d\u043e\u0432\u044b\u0439 \u0443\u043d\u0438\u0432\u0435\u0440\u0441\u0438\u0442\u0435\u0442](https://codeforces.com/problemset/problem/105931/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

The university is enrolling up to `n` students in total. Every student must fall into one of two categories.

If a student pays tuition, they contribute a fixed amount `a` to the university.

If a student receives a scholarship, their funding comes from a sponsor. The sponsor supports at most `b` students, and the amount decreases linearly: the first scholarship gives `b`, the second gives `b - 1`, and so on until the k-th scholarship gives `b - k + 1`.

The university decides how many students `k` out of the total `n` will be scholarship recipients, with the restriction that `k` cannot exceed `b`. All remaining `n - k` students are paying students. The goal is to choose `k` so that the total money received, from tuition plus sponsorship, is maximized.

The output is this maximum achievable total revenue.

The constraints allow `n`, `a`, and `b` up to `10^9`. This immediately rules out any approach that tries every possible value of `k` and recomputes the result in linear time. Even iterating over all `k` is impossible because `k` itself can be up to `10^9`.

A direct simulation is also problematic because the scholarship part involves summing a decreasing arithmetic progression, which grows quadratically in `k`. Any naive per-student simulation would be too slow.

A subtle failure case appears when one tries greedy reasoning such as always taking as many scholarships as possible or always preferring paid students. For example, if `a` is small, scholarships might still be better for early values of `k` but worse later when the marginal scholarship drops below `a`. This creates a peak in the total profit rather than a monotone behavior, so local decisions fail.

## Approaches

A brute-force approach would try every possible number of scholarship students `k` from `0` to `min(n, b)`. For each choice, we compute revenue as `(n - k) * a` plus the sum of the arithmetic progression `b + (b - 1) + ... + (b - k + 1)`.

Computing each sum in O(k) would make the solution O(n^2) in the worst case, which is far too large. Even if we use the arithmetic series formula to compute each candidate in O(1), we still need to test up to `10^9` values of `k`, which is impossible.

The key observation is that the objective function is not arbitrary. The scholarship sum is quadratic in `k`, and the tuition part is linear in `k`. The total function becomes a concave quadratic function in `k`. That means it has a single peak, and once we move past it, the value only decreases.

This structure allows us to avoid searching the entire range. Instead of enumerating all values, we compute the position of the peak analytically and only check a constant number of nearby candidates, along with boundary values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(min(n, b)) or worse | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Express the total profit as a function of `k`, where `k` is the number of scholarship students. The remaining `n - k` students pay tuition, contributing `(n - k) * a`. The scholarship contribution is an arithmetic progression with `k` terms starting from `b`.
2. Rewrite the scholarship sum using a closed form formula. The sum becomes `k * (2b - k + 1) / 2`. This removes any need for iteration.
3. Combine both parts into a single expression depending only on `k`. After simplification, the problem reduces to maximizing a quadratic function in `k` over the integer range `[0, min(n, b)]`.
4. Identify that the function is concave because the coefficient of `k^2` is negative. This guarantees a single maximum point, so we only need to locate the peak rather than search exhaustively.
5. Compute the real-valued optimal point using the derivative idea, which gives `k* = (2b - 2a + 1) / 2`. This represents where marginal gain from scholarships balances the fixed tuition gain.
6. Since `k` must be an integer, consider the closest integers around `k*`. Also include boundary values `0` and `min(n, b)` because the optimum might lie outside the feasible interval or get clipped by constraints.
7. Evaluate the profit for each candidate `k` and take the maximum.

### Why it works

The profit function over `k` is a concave quadratic, meaning it decreases on both sides of a single peak. Any integer maximum must lie at either the floor or ceiling of the real optimum or at a boundary of the valid interval. By checking only those points, we guarantee capturing the global maximum without enumerating all possibilities.

## Python Solution

```python
import sys
input = sys.stdin.readline

def calc(n, a, b, k):
    # tuition part + scholarship part
    return (n - k) * a + k * (2 * b - k + 1) // 2

def solve():
    n = int(input())
    a = int(input())
    b = int(input())

    max_k = min(n, b)

    # continuous optimum
    k_star = (2 * b - 2 * a + 1) / 2

    candidates = set()

    for x in [0, max_k]:
        candidates.add(x)

    for x in [int(k_star), int(k_star) + 1]:
        candidates.add(x)

    best = 0
    for k in candidates:
        if 0 <= k <= max_k:
            best = max(best, calc(n, a, b, k))

    print(best)

if __name__ == "__main__":
    solve()
```

The function `calc` directly evaluates the profit formula without simulation. This is important because expanding the process student-by-student would be infeasible.

The candidate set includes both boundaries and the neighborhood around the analytical optimum. Casting `k_star` to integer and also checking the next value ensures we do not miss the discrete maximum due to flooring effects.

## Worked Examples

Consider a case where `n = 4`, `a = 4`, `b = 3`.

The feasible range for `k` is from `0` to `3`.

We compute values:

| k | tuition (4-k)*a | scholarship sum | total |
| --- | --- | --- | --- |
| 0 | 16 | 0 | 16 |
| 1 | 12 | 3 | 15 |
| 2 | 8 | 5 | 13 |
| 3 | 4 | 6 | 10 |

The maximum is at `k = 0`, meaning no scholarships are optimal because tuition is strong compared to diminishing scholarship values. This demonstrates that the function can decrease immediately from the start.

Now consider `n = 10`, `a = 2`, `b = 6`.

| k | tuition | scholarship | total |
| --- | --- | --- | --- |
| 0 | 20 | 0 | 20 |
| 1 | 18 | 6 | 24 |
| 2 | 16 | 11 | 27 |
| 3 | 14 | 15 | 29 |
| 4 | 12 | 18 | 30 |
| 5 | 10 | 20 | 30 |
| 6 | 8 | 21 | 29 |

The best value occurs around `k = 4 or 5`, showing a clear peak rather than monotonic growth or decay. This is exactly the shape expected from a concave quadratic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of candidate values are evaluated |
| Space | O(1) | No auxiliary structures beyond a few variables |

The solution is independent of the magnitude of `n`, `a`, and `b`, which makes it well within the limits even for `10^9`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import builtins

    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out
    try:
        solve()
    finally:
        sys.stdout = old_stdout
    return out.getvalue().strip()

# minimal case
assert run("1\n5\n10\n") == "10"

# no scholarships beneficial
assert run("5\n10\n3\n") == str(5 * 10)

# all scholarships beneficial
assert run("5\n1\n10\n") == str((5 - 5) * 1 + 5 * (2 * 10 - 5 + 1) // 2)

# balanced case
assert run("10\n2\n6\n") == "30"

# boundary n < b
assert run("3\n5\n10\n") == str((3 * (2 * 10 - 3 + 1) // 2))

# large equal values
assert run("1000000000\n1\n1\n") == str(1000000000)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5 10 | 10 | single student boundary |
| 5 10 3 | 50 | no scholarship is optimal |
| 5 1 10 | large scholarship preference | full scholarship dominance |
| 10 2 6 | 30 | interior maximum |
| 3 5 10 | scholarship cap smaller than n | boundary clipping |
| 1e9 1 1 | large-scale stability | overflow-safe formula |

## Edge Cases

One edge case is when `a` is so large that any scholarship reduces total profit immediately. For example, `n = 5`, `a = 10`, `b = 3`. The function at `k = 1` already decreases compared to `k = 0`. The algorithm still handles this correctly because `k = 0` is explicitly included among candidates, ensuring the maximum is not missed.

Another edge case occurs when `b` is smaller than `n`. For instance, `n = 10`, `b = 3`, `a = 1`. Even though there are many students, scholarships cannot exceed 3. The algorithm correctly clamps the search range to `min(n, b)`, so it never evaluates invalid values of `k`.

A final edge case is when the quadratic peak lies outside the feasible interval. For example, if the computed `k*` is negative, such as when `a` is very large compared to `b`, the valid maximum occurs at `k = 0`. Because the algorithm always checks boundary values, it correctly handles this situation without relying on the analytical peak.
