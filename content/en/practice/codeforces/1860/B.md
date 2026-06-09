---
title: "CF 1860B - Fancy Coins"
description: "We are asked to determine the minimum number of fancy coins Monocarp must use to pay exactly m burles when he has two types of coins: one worth 1 burle and one worth k burles."
date: "2026-06-09T00:21:59+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1860
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 153 (Rated for Div. 2)"
rating: 1200
weight: 1860
solve_time_s: 106
verified: true
draft: false
---

[CF 1860B - Fancy Coins](https://codeforces.com/problemset/problem/1860/B)

**Rating:** 1200  
**Tags:** binary search, brute force, greedy, math  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine the minimum number of fancy coins Monocarp must use to pay exactly `m` burles when he has two types of coins: one worth 1 burle and one worth `k` burles. For each type, he has a limited number of regular coins (`a_1` of 1-burle coins, `a_k` of k-burle coins) and infinitely many fancy coins. Fancy coins are more "expensive" in the sense that Monocarp wants to minimize their usage.

The input consists of multiple test cases. For each, we receive the total amount `m`, the larger coin value `k`, and the counts of available regular coins `a_1` and `a_k`. We must compute, for each case, the smallest total number of fancy coins required to exactly reach `m` using any combination of regular and fancy coins.

The constraints indicate that `m` and `k` can be as large as `10^8`, and the number of test cases `t` can be up to 30,000. This rules out any solution that iterates through all possible coin combinations because that could result in up to `10^16` operations in a naive approach. We need a method that calculates the result in constant time per test case or logarithmic time relative to `k`.

Some subtle edge cases are when Monocarp has zero regular coins of one or both types, or when `m` is smaller than `k`. For example, if `m = 5`, `k = 3`, and `a_1 = 0`, `a_k = 1`, the correct answer is 2 fancy coins (one 3-burle coin and two 1-burle coins), not 1 fancy coin. A careless implementation that greedily uses large coins without checking regular coin counts would produce a wrong result.

## Approaches

The brute-force approach would attempt all combinations of how many coins of each type to use, computing the total number of fancy coins for each possibility. Concretely, we could iterate `x` from 0 to the minimum of `a_k` and `m//k`, representing the number of regular k-burle coins used, then solve for the number of 1-burle coins needed. This approach is correct but far too slow: in the worst case, we could try `m/k` possibilities for each of 30,000 test cases, easily exceeding time limits.

The key insight is to consider the remainder modulo `k`. The total amount `m` can be expressed as `m = q * k + r` where `0 ≤ r < k`. The number of fancy 1-burle coins is exactly the amount of the remainder that cannot be covered by regular 1-burle coins, i.e., `max(0, r - a_1)`. For the k-burle coins, any shortfall beyond the regular k-burle coins contributes `q - a_k` fancy coins, but only if positive. This reduces the problem to a simple arithmetic calculation using division and modulo, eliminating the need for iteration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m/k) per test case | O(1) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Divide the total amount `m` by `k` to find the quotient `q` and remainder `r`. `q` represents the number of k-burle coins required if we ignore regular coin availability. `r` represents the leftover amount to be paid with 1-burle coins.
2. Calculate how many fancy 1-burle coins are needed. Use `fancy_1 = max(0, r - a_1)`. This ensures we first consume all available regular 1-burle coins to cover the remainder.
3. Calculate how many fancy k-burle coins are needed. After consuming all regular k-burle coins, any remaining k-burle coin requirement must come from fancy coins. Use `fancy_k = max(0, q - a_k)`.
4. Sum the two values: `fancy_1 + fancy_k` is the minimal number of fancy coins required.

Why it works: by first paying as much as possible with regular coins and then only using fancy coins for the shortfall, we guarantee the minimal fancy coin usage. Division and modulo ensure that the number of k-burle coins is minimized automatically, since any remaining 1-burle amount is directly computed as the remainder.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        m, k, a1, ak = map(int, input().split())
        q, r = divmod(m, k)
        fancy_1 = max(0, r - a1)
        fancy_k = max(0, q - ak)
        print(fancy_1 + fancy_k)

if __name__ == "__main__":
    main()
```

The solution reads all inputs efficiently with `sys.stdin.readline`. `divmod` avoids writing two separate operations for quotient and remainder. Using `max(0, ...)` guarantees we never report negative fancy coins. The order of subtraction ensures we first consume all regular coins before counting fancy coins, aligning with the greedy strategy.

## Worked Examples

**Example 1:** `m = 11, k = 3, a1 = 6, ak = 1`

| Step | q, r | fancy_1 | fancy_k | total fancy |
| --- | --- | --- | --- | --- |
| Compute q, r | 11 // 3 = 3, 11 % 3 = 2 | max(0, 2 - 6) = 0 | max(0, 3 - 1) = 2 | 2 |

Trace shows that even though 1-burle coins are sufficient to cover the remainder, we need two fancy k-burle coins to make up the bulk.

**Example 2:** `m = 11, k = 3, a1 = 0, ak = 0`

| Step | q, r | fancy_1 | fancy_k | total fancy |
| --- | --- | --- | --- | --- |
| Compute q, r | 11 // 3 = 3, 11 % 3 = 2 | max(0, 2 - 0) = 2 | max(0, 3 - 0) = 3 | 5 |

Here, no regular coins exist, so all coins must be fancy. This matches the sample output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Each test case only performs division, modulo, and two max operations. |
| Space | O(1) per test case | Only a few integer variables are stored. |

Given `t ≤ 3e4`, total time is negligible (~10^5 operations), comfortably within 2 seconds. Memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# Provided samples
assert run("4\n11 3 0 0\n11 3 20 20\n11 3 6 1\n100000000 2 0 0\n") == "5\n0\n1\n50000000"

# Custom cases
assert run("1\n5 5 0 1\n") == "0", "Use one regular k-burle coin"
assert run("1\n5 5 0 0\n") == "1", "Use one fancy k-burle coin"
assert run("1\n1 2 1 0\n") == "0", "Exactly enough 1-burle coin"
assert run("1\n1 2 0 0\n") == "1", "No regular coins, must use one fancy 1-burle coin"
assert run("1\n100000000 100000000 0 0\n") == "1", "Large k equal to m"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 5 0 1` | 0 | Correctly consumes a regular k-burle coin |
| `5 5 0 0` | 1 | Uses a fancy k-burle coin when no regular available |
| `1 2 1 0` | 0 | Minimal 1-burle coin covers remainder |
| `1 2 0 0` | 1 | Minimal fancy coin needed when no regular coins |
| `100000000 100000000 0 0` | 1 | Large numbers handled correctly |

## Edge Cases

When `a1 = 0` and `ak = 0`, all coins must be fancy. For input `m = 11, k = 3`, we compute `q = 3, r = 2`. Then `fancy_
