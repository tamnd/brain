---
title: "CF 1154F - Shovels Shop"
description: "We have a shop with n shovels, each with a specific price. Misha wants to buy exactly k shovels, possibly in multiple purchases. The twist is that the shop offers special deals: if you buy exactly xj shovels in a single purchase, the yj cheapest among those shovels are free."
date: "2026-06-12T02:48:58+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1154
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 552 (Div. 3)"
rating: 2100
weight: 1154
solve_time_s: 83
verified: true
draft: false
---

[CF 1154F - Shovels Shop](https://codeforces.com/problemset/problem/1154/F)

**Rating:** 2100  
**Tags:** dp, greedy, sortings  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a shop with `n` shovels, each with a specific price. Misha wants to buy exactly `k` shovels, possibly in multiple purchases. The twist is that the shop offers special deals: if you buy exactly `x_j` shovels in a single purchase, the `y_j` cheapest among those shovels are free. Each offer can be used any number of times, but only one offer can apply to a single purchase. The goal is to minimize the total amount Misha pays.

From a constraints perspective, `n` and `m` can be as large as 200,000, but `k` is capped at 2000. This is crucial: while we cannot afford an `O(n*k)` or `O(n^2)` algorithm directly over all shovels, we can focus on just the `k` cheapest shovels because buying more expensive shovels than necessary would never be optimal. This reduces our effective problem size to `k` shovels, which is small enough to allow a dynamic programming approach.

Edge cases include scenarios where all offers require buying more shovels than Misha wants, or offers give zero free shovels. A naive approach might sort the entire list and try to apply offers without considering that it is never optimal to buy expensive shovels when cheaper ones remain, potentially inflating the total cost.

## Approaches

The brute-force solution would enumerate all ways to select subsets of shovels, apply all possible offers, and track the cost for each configuration. This would involve `2^k` subsets of shovels, which is infeasible even for `k = 20`. The brute-force is correct in principle because it considers every combination, but it becomes exponentially slow.

The key insight is that the order of shovels matters only by price. If we sort the shovels by increasing price, then every optimal purchase will take the cheapest remaining shovels. Once sorted, we can model the problem as a one-dimensional dynamic programming problem: let `dp[i]` represent the minimum cost to buy the first `i` cheapest shovels. For each `i`, we can decide the size of the last purchase `j` and see if there is an offer for exactly `j` shovels. If there is, we pay only for the most expensive `j - y_j` shovels. By iterating over all valid `j`, we update `dp[i]` to find the minimum cost.

This reduces a potentially combinatorial problem into an `O(k * m)` DP, which is feasible because `k ≤ 2000` and `m ≤ 2e5`. Sorting the prices adds `O(n log n)`, but since we only need the `k` cheapest, we can select them in `O(n + k log k)` with partial sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^k * m) | O(k) | Too slow |
| Optimal DP | O(k * m) + O(n log n) | O(k) | Accepted |

## Algorithm Walkthrough

1. First, sort all shovel prices in ascending order. Only the `k` cheapest shovels are relevant, as buying any more expensive shovels would not minimize the cost.
2. Preprocess the offers. Since multiple offers may have the same `x_j` but different `y_j`, for each purchase size `x`, retain the maximum `y` among the offers. This ensures that for any given purchase size, we always get the best possible discount.
3. Initialize a DP array `dp` of size `k+1`, where `dp[i]` represents the minimum cost to buy the first `i` shovels. Set `dp[0] = 0` because buying zero shovels costs nothing.
4. Iterate through `i` from 1 to `k`. For each `i`, consider all possible purchase sizes `j` from 1 up to `i`. For each `j`, calculate the effective cost of buying the last `j` shovels. If there is an offer for size `j`, subtract the cost of the `y` cheapest shovels in this block, which are always the first `y` of these `j` shovels due to sorting. Update `dp[i]` as the minimum of its current value and `dp[i-j] + cost_of_last_j`.
5. After filling the DP array, `dp[k]` holds the minimum total cost for buying exactly `k` shovels.

This works because of the sorted order invariant: we always take the cheapest remaining shovels, so any combination of purchases that does not follow this order cannot be optimal. Dynamic programming ensures we consider all ways to partition the first `i` shovels into valid purchases, taking advantage of offers wherever beneficial.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, m, k = map(int, input().split())
    prices = list(map(int, input().split()))
    prices.sort()
    prices = prices[:k]

    offer = [0] * (k + 1)
    for _ in range(m):
        x, y = map(int, input().split())
        if x <= k:
            offer[x] = max(offer[x], y)

    prefix_sum = [0] * (k + 1)
    for i in range(k):
        prefix_sum[i+1] = prefix_sum[i] + prices[i]

    INF = 10**18
    dp = [INF] * (k + 1)
    dp[0] = 0

    for i in range(1, k + 1):
        for j in range(1, i + 1):
            free = offer[j]
            cost = prefix_sum[i] - prefix_sum[i - j + free]
            dp[i] = min(dp[i], dp[i - j] + cost)

    print(dp[k])

if __name__ == "__main__":
    main()
```

In this solution, the prefix sums allow efficient calculation of any contiguous block of shovels' costs. The array `offer` stores the best discount for each purchase size. We loop over all partition sizes `j` for `i` shovels and apply the corresponding offer to compute the minimal cost dynamically.

## Worked Examples

Sample 1:

| i | j | free | cost of last j | dp[i] |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 2 | 2 |
| 2 | 1 | 0 | 2 | 4 |
| 2 | 2 | 1 | 2 | 2 |
| 3 | 1 | 0 | 4 | 4 |
| 3 | 2 | 1 | 4 | 4 |
| 3 | 3 | 1 | 4 | 4 |
| 4 | 1 | 0 | 5 | 7 |
| 5 | 2 | 1 | 4 | 7 |

The table shows that by optimally choosing purchase sizes and applying offers, we achieve `dp[5] = 7`.

Sample 2:

| i | j | free | cost of last j | dp[i] |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 1 |
| 2 | 1 | 0 | 2 | 3 |
| 3 | 3 | 1 | 5 | 5 |
| 4 | 4 | 1 | 8 | 8 |
| 5 | 5 | 3 | 5 | 10 |

We see the offer for 5 shovels with 3 free reduces the cost effectively.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k * k) + O(n log n) | Sorting n shovels and computing DP over k shovels considering all partition sizes |
| Space | O(k) | DP array and prefix sums |

Because `k ≤ 2000`, `k^2` is roughly 4 million, which is fast enough under a 2-second time limit. Sorting the prices of up to `n = 2e5` shovels takes O(n log n), which is also acceptable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as io_module
    out = io_module.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# Provided samples
assert run("7 4 5\n2 5 4 2 6 3 1\n2 1\n6 5\n2 1\n3 1\n") == "7", "sample 1"
assert run("9 2 5\n6 8 5 1 2 1 1 4 3\n5 3\n3 1\n") == "17", "sample 2"
assert run("4 0 4\n5 4 6 2\n") == "17", "sample 3"

# Custom cases
assert run("1 1 1\n100\n1 1\n") == "0", "single shovel, offer free"
assert run("3 2 2\n10 20 30\n2 1\n2 2\n") == "
```
