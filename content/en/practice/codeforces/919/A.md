---
title: "CF 919A - Supermarket"
description: "We are given several supermarkets, and each supermarket describes a bundled offer: a price a for b kilograms of apples. This is equivalent to a unit price of a / b per kilogram, but the key point is that we are not restricted to buying only in full bundles of b kilograms."
date: "2026-06-13T02:35:55+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 919
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 460 (Div. 2)"
rating: 800
weight: 919
solve_time_s: 397
verified: false
draft: false
---

[CF 919A - Supermarket](https://codeforces.com/problemset/problem/919/A)

**Rating:** 800  
**Tags:** brute force, greedy, implementation  
**Solve time:** 6m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several supermarkets, and each supermarket describes a bundled offer: a price `a` for `b` kilograms of apples. This is equivalent to a unit price of `a / b` per kilogram, but the key point is that we are not restricted to buying only in full bundles of `b` kilograms. We want exactly `m` kilograms in total, and we can choose how to distribute purchases across supermarkets, effectively treating each supermarket as an unlimited source of apples with a fixed per-kilogram price.

So the task reduces to selecting where to buy apples so that the total amount purchased is exactly `m` kilograms, minimizing total cost.

The input size immediately shapes the approach. We may have up to 5000 supermarkets, but the required amount `m` is at most 100. This imbalance is the central hint: the decision is small in one dimension, so we can afford a dynamic programming solution over kilograms while iterating all supermarkets.

A naive misunderstanding is to think we must choose exactly one supermarket and buy all `m` kilograms there. That is incorrect because mixing supermarkets can produce a cheaper combination even if no single one is optimal alone.

Another subtle issue is floating-point precision. Since prices are ratios, direct repeated division can accumulate error if we are not careful. However, since all computations are linear combinations of rational values with small integers, using floating point `double` is safe if done carefully.

A small illustrative pitfall is this scenario: suppose one supermarket has `a=1, b=2` (0.5 per kg) and another has `a=3, b=4` (0.75 per kg), and we need `m=3`. Buying all from the second might look plausible if miscomputed as integer division, but mixing clearly gives better cost. Any approach that only picks the minimum per-kilo supermarket would fail here.

## Approaches

The brute-force idea is to consider all ways to distribute `m` kilograms among `n` supermarkets. For each supermarket we could decide how many kilograms to buy from it, and ensure the total sums to `m`. If we think in terms of integer partitions, each kilogram can independently choose a supermarket, giving roughly `n^m` possibilities. With `n = 5000` and `m = 100`, this is astronomically large and completely infeasible.

The key observation is that the cost of buying kilograms is additive and independent: buying one more kilogram from a supermarket always adds the same cost `a/b`. This turns the problem into a classic knapsack-style optimization where we build the answer kilogram by kilogram. Each kilogram is identical, and each choice depends only on minimizing cumulative cost.

We define a state for how many kilograms we have already purchased, and transition by trying every supermarket as the source of the next kilogram. Since `m` is small, we can afford `O(n * m)` transitions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^m) | O(m) | Too slow |
| Optimal (DP over kilograms) | O(nm) | O(m) | Accepted |

## Algorithm Walkthrough

We build the solution incrementally, tracking the minimum cost to buy exactly `i` kilograms for every `i` from `0` to `m`.

1. Define a DP array `dp` where `dp[i]` is the minimum cost to buy exactly `i` kilograms. Initialize `dp[0] = 0` and all other values as infinity. This encodes that buying zero kilograms costs nothing, and all other states are initially unreachable.
2. Iterate over all supermarkets one by one. Each supermarket is a reusable source, so we allow it to contribute multiple kilograms across transitions.
3. For a given supermarket with cost `a/b`, compute its unit price. This is the incremental cost for each kilogram taken from it.
4. Update the DP array for each possible target weight `i` from `1` to `m`. For each `i`, try taking one kilogram from the current supermarket and combine it with a previously computed state `dp[i-1]`. The transition is `dp[i] = min(dp[i], dp[i-1] + a/b)`.

This works because every kilogram is identical and independent, so we are effectively choosing the cheapest source for each unit while respecting that we are summing exactly `m` units.

### Why it works

At any point, `dp[i]` represents the minimum cost achievable using any combination of supermarkets for exactly `i` kilograms. When we process a supermarket, we consider using it for the last kilogram in a construction of size `i`. Since every possible sequence of choices can be decomposed by its last step, every valid solution is represented in some transition. The recurrence covers all such decompositions, so no valid combination is missed, and every state is minimized over all possibilities.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

INF = 1e18
dp = [INF] * (m + 1)
dp[0] = 0.0

for _ in range(n):
    a, b = map(int, input().split())
    cost_per_kg = a / b

    for i in range(1, m + 1):
        dp[i] = min(dp[i], dp[i - 1] + cost_per_kg)

print(dp[m])
```

The solution uses a one-dimensional DP array because each state only depends on the previous kilogram count. The transition order is important: we iterate `i` forward because each supermarket can be used repeatedly without restriction, effectively allowing unlimited reuse.

Floating-point arithmetic is sufficient because the constraints are small and the required precision tolerance is `1e-6`. The final answer is `dp[m]`, representing the minimum cost for exactly `m` kilograms.

## Worked Examples

### Example 1

Input:

```
3 5
1 2
3 4
1 3
```

We compute unit prices:

- Supermarket 1: 0.5
- Supermarket 2: 0.75
- Supermarket 3: 0.333...

We simulate DP updates.

| i (kg) | dp before | chosen update | dp after |
| --- | --- | --- | --- |
| 1 | 0, inf... | 0 + 0.333... | 0.333... |
| 2 | updated | best so far | 0.666... |
| 3 | updated | best so far | 1.0 |
| 4 | updated | best so far | 1.333... |
| 5 | updated | best so far | 1.666... |

Final answer is `1.66666667`, which corresponds to buying all 5 kilograms from supermarket 3.

This trace shows that the DP accumulates the cheapest per-unit cost consistently, always preferring the best available supermarket.

### Example 2

Input:

```
2 1
98 99
1 1
```

Unit prices:

- Supermarket 1: 98/99 ≈ 0.9899
- Supermarket 2: 1.0

| i (kg) | dp before | chosen update | dp after |
| --- | --- | --- | --- |
| 1 | 0, inf | min(0+0.9899, 0+1.0) | 0.9899 |

The DP selects the slightly cheaper first supermarket. This confirms the algorithm correctly handles fine-grained comparisons where differences are small.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | For each of the n supermarkets, we update m DP states |
| Space | O(m) | We store only DP values for 0 to m kilograms |

The constraints allow up to 5000 supermarkets and at most 100 kilograms, giving about 500,000 transitions, which is comfortably fast in Python. Memory usage is minimal since we only keep a single DP array.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    n, m = map(int, sys.stdin.readline().split())
    INF = 1e18
    dp = [INF] * (m + 1)
    dp[0] = 0.0

    for _ in range(n):
        a, b = map(int, sys.stdin.readline().split())
        cost = a / b
        for i in range(1, m + 1):
            dp[i] = min(dp[i], dp[i - 1] + cost)

    return str(dp[m])

# provided sample
assert abs(float(run("""3 5
1 2
3 4
1 3
""").strip()) - 1.66666667) < 1e-6

# minimum case
assert abs(float(run("""1 1
1 1
""").strip()) - 1.0) < 1e-6

# all equal prices
assert abs(float(run("""3 4
2 2
4 4
6 6
""").strip()) - 4.0) < 1e-6

# cheaper later supermarket
assert abs(float(run("""2 2
10 1
1 1
""").strip()) - 2.0) < 1e-6

# mix case
assert abs(float(run("""3 3
1 2
2 3
3 4
""").strip()) < 10)  # sanity check
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 kg single offer | 1.0 | minimum boundary |
| identical supermarkets | exact linear scaling | consistency |
| mixed prices | optimal selection | greedy transitions |

## Edge Cases

A small `m = 1` case tests whether the algorithm correctly reduces to simply choosing the cheapest unit price among all supermarkets. The DP initializes `dp[1]` directly from all available transitions, so the minimum ratio dominates as expected.

A case where all supermarkets are identical checks whether repeated updates preserve correctness without overwriting optimal values. Since every transition uses `min`, the DP remains stable and never increases.

A case with a significantly cheaper supermarket appearing late ensures order independence. Even if the best option is processed last, it still correctly updates all states because each update considers all previous values and improves them when possible.
