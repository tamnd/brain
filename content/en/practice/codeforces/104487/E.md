---
title: "CF 104487E - Interesting Ratios"
description: "Each test case describes a download process that completes in exactly n equal steps, from 0 to n. At some intermediate point x, where 1 ≤ x ≤ n - 1, the download is at x/n completion and (n - x)/n remaining."
date: "2026-06-30T12:38:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104487
codeforces_index: "E"
codeforces_contest_name: "Tishreen + SVU CPC 2023"
rating: 0
weight: 104487
solve_time_s: 68
verified: true
draft: false
---

[CF 104487E - Interesting Ratios](https://codeforces.com/problemset/problem/104487/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case describes a download process that completes in exactly `n` equal steps, from `0` to `n`. At some intermediate point `x`, where `1 ≤ x ≤ n - 1`, the download is at `x/n` completion and `(n - x)/n` remaining. We are asked to look at the ratio of completed part to remaining part, that is `x : (n - x)`, reduce it, and keep only the integer value of this ratio when it becomes a whole number.

For a fixed position `x`, the ratio is integer exactly when `x / (n - x)` is an integer. Each such valid `x` contributes its reduced ratio value to a sum. The task is to compute this sum for every `n`.

The constraints allow up to `10^5` test cases and each `n` can be as large as `10^6`. This immediately rules out checking every `x` from `1` to `n - 1` for every query, since that would lead to about `10^11` operations in the worst case. Even a logarithmic per-step approach over all positions would still be too slow unless heavily preprocessed.

A subtle edge case appears when `n` is prime. Then only trivial divisors exist, and we must ensure the logic does not accidentally count invalid positions. For example, when `n = 5`, the valid positions must be derived carefully rather than assuming many internal ratios exist. A naive simulation might try all `x` and miss the structure that only specific algebraic conditions matter.

## Approaches

A brute-force approach iterates over every position `x` from `1` to `n - 1`, computes the ratio `x / (n - x)`, checks whether it is an integer, and if so adds it to the answer. This is correct because it directly follows the definition. However, it requires `O(n)` work per test case, leading to `O(nT)` overall, which is far beyond feasible limits when both `n` and `T` are large.

The key simplification comes from rewriting the condition for integrality. The ratio `x / (n - x)` is an integer `k` if and only if `x = k(n - x)`. Rearranging gives `x(1 + k) = kn`, so `x = kn / (k + 1)`. For this to be valid, `(k + 1)` must divide `kn`. Since `k` and `k + 1` are coprime, this forces `(k + 1)` to divide `n`.

This transforms the problem from iterating over positions `x` to iterating over divisors of `n`. Each divisor directly corresponds to exactly one valid ratio value, making the solution dependent only on number-theoretic functions of `n`, not its linear range.

From this, the answer reduces to a simple expression involving divisor sums and counts, allowing full preprocessing for all values up to `10^6`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nT) | O(1) | Too slow |
| Divisor-based precomputation | O(N log N + T) | O(N) | Accepted |

## Algorithm Walkthrough

We transform the problem into divisor arithmetic and precompute everything once for all `n` up to the maximum limit.

1. Precompute the sum of divisors `sigma(n)` for every `n` up to `10^6`. This is done using a sieve-style approach where each integer contributes to all of its multiples. This is necessary because every valid ratio depends on divisor structure rather than individual positions.
2. Precompute the number of divisors `tau(n)` for every `n` using the same sieve accumulation. Each time we add one contribution per divisor occurrence.
3. For each test case, read `n` and compute the answer using the identity `answer = sigma(n) - tau(n)`.
4. Output the result immediately for each query.

The reason step 3 is valid comes from mapping each valid ratio to a divisor `d` of `n` where `d ≥ 2`, and each such divisor contributes exactly `(d - 1)` to the sum.

### Why it works

Every valid ratio corresponds to a value `k` such that `x / (n - x) = k`. This forces `x = kn / (k + 1)`, which is integral only when `(k + 1)` divides `n`. Writing `d = k + 1`, each divisor `d ≥ 2` produces exactly one valid position and contributes `d - 1` to the sum. Summing over all such divisors is equivalent to `sum_{d|n, d≥2}(d - 1)`, which simplifies algebraically to `sigma(n) - tau(n)`.

The algorithm is correct because it replaces a position-based condition with an exact bijection between valid ratios and divisors of `n`.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXN = 10**6

sigma = [0] * (MAXN + 1)
tau = [0] * (MAXN + 1)

for i in range(1, MAXN + 1):
    for j in range(i, MAXN + 1, i):
        sigma[j] += i
        tau[j] += 1

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        out.append(str(sigma[n] - tau[n]))
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The preprocessing loops build divisor sums and counts in a classic sieve manner. For every `i`, it contributes to all multiples `j`, accumulating both its value into `sigma[j]` and one count into `tau[j]`.

The query step is constant time per test case. The subtraction `sigma[n] - tau[n]` directly implements the derived formula, avoiding any recomputation during queries.

## Worked Examples

### Example 1

Consider `n = 6`.

Valid ratios come from divisors of 6 greater than 1, which are 2, 3, and 6.

| divisor d | ratio contribution (d - 1) |
| --- | --- |
| 2 | 1 |
| 3 | 2 |
| 6 | 5 |

Total sum is `1 + 2 + 5 = 8`.

This matches `sigma(6) = 1 + 2 + 3 + 6 = 12` and `tau(6) = 4`, so `12 - 4 = 8`.

### Example 2

Consider `n = 10`.

Divisors greater than 1 are 2, 5, 10.

| divisor d | contribution |
| --- | --- |
| 2 | 1 |
| 5 | 4 |
| 10 | 9 |

Total is `14`.

Again, `sigma(10) = 18`, `tau(10) = 4`, so `18 - 4 = 14`.

These traces show that each divisor contributes independently, and no interaction between positions exists once the transformation is applied.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N + T) | sieve-like accumulation over all divisors plus constant-time queries |
| Space | O(N) | arrays for divisor sums and counts |

The preprocessing cost is acceptable for `N = 10^6`, and each query is answered in constant time, making the solution comfortably fit within both time and memory limits.

## Test Cases

```python
import sys, io

MAXN = 10**6
sigma = [0] * (MAXN + 1)
tau = [0] * (MAXN + 1)

for i in range(1, MAXN + 1):
    for j in range(i, MAXN + 1, i):
        sigma[j] += i
        tau[j] += 1

def solve_case(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    t = int(input())
    res = []
    for _ in range(t):
        n = int(input())
        res.append(str(sigma[n] - tau[n]))
    return "\n".join(res)

# custom small cases
assert solve_case("1\n1\n") == "0"
assert solve_case("1\n2\n") == "1"
assert solve_case("1\n6\n") == "8"
assert solve_case("1\n10\n") == "14"

# multiple tests
assert solve_case("3\n6\n10\n12\n") == "\n".join([
    str(sigma[6]-tau[6]),
    str(sigma[10]-tau[10]),
    str(sigma[12]-tau[12])
])
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n = 1 | 0 | no valid intermediate progress |
| n = 2 | 1 | smallest non-trivial case |
| n = 6 | 8 | composite with multiple divisors |
| n = 10,12 | computed | multiple queries consistency |

## Edge Cases

For `n = 1`, there are no intermediate positions at all, so the sum must be zero. The formula gives `sigma(1) - tau(1) = 1 - 1 = 0`, matching the definition without special handling.

For prime `n`, such as `n = 5`, only divisor-based contributions exist. The divisors are `1` and `5`, so only `5` contributes, giving `(5 - 1) = 4`. The formula gives `sigma(5) - tau(5) = (1 + 5) - 2 = 4`, confirming correctness even when no internal structure exists in the interval.

For highly composite numbers like `n = 12`, many divisors contribute independently. The algorithm handles this naturally because each divisor contributes exactly once during preprocessing, ensuring no overcounting or missing contributions.
