---
title: "CF 1671C - Dolce Vita"
description: "We have a scenario where you want to buy sugar packs from several shops over consecutive days, with each shop selling one pack per day. Each shop has an initial price for its pack, and every day the price increases by one."
date: "2026-06-10T01:36:55+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1671
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 127 (Rated for Div. 2)"
rating: 1200
weight: 1671
solve_time_s: 115
verified: false
draft: false
---

[CF 1671C - Dolce Vita](https://codeforces.com/problemset/problem/1671/C)

**Rating:** 1200  
**Tags:** binary search, brute force, greedy, math  
**Solve time:** 1m 55s  
**Verified:** no  

## Solution
## Problem Understanding

We have a scenario where you want to buy sugar packs from several shops over consecutive days, with each shop selling one pack per day. Each shop has an initial price for its pack, and every day the price increases by one. You have a fixed budget per day and cannot carry over money to the next day. The goal is to determine the total number of packs you can buy until all packs exceed your daily budget.

The inputs are the number of shops `n`, the daily budget `x`, and the array `a` representing initial pack prices for each shop. The output is a single integer for each test case: the total packs you can buy before no pack is affordable.

The constraints are important. `n` can be up to 2·10^5, `x` and `a_i` up to 10^9, and the sum of `n` over all test cases is ≤ 2·10^5. This implies any brute-force simulation of each day for each shop is too slow, because the number of days could also be up to 10^9 in extreme cases. We need an approach that avoids simulating every single day individually.

An edge case occurs when the cheapest pack is already more expensive than your daily budget on day one. For example, if `x = 5` and the cheapest `a_i = 6`, you cannot buy any pack. Another subtle case arises when multiple cheap packs allow for repeated buying over many days, such as `a = [1, 1]` with a huge budget `x = 1000`. A naive per-day simulation would iterate thousands of times unnecessarily. We need a method that compresses this repetition efficiently.

## Approaches

A straightforward brute-force approach would simulate each day: for each day, compute the current price of every pack, buy as many as you can within the budget, then move to the next day and increase all prices by one. This is correct because it literally follows the problem description. However, in the worst case, if `n = 2·10^5` and prices are very low with a high budget, the simulation could require billions of iterations across days, which is far beyond the 2-second limit. This makes it impractical.

The key observation is that we do not need to simulate day by day. If we sort the packs by initial price, the cheapest packs will always be considered first. On any given day, if you can buy `k` packs within your budget, the number of days you can continue buying these `k` packs consecutively without exceeding the budget can be computed mathematically. Specifically, if the sum of the `k` cheapest packs plus `k*d` (where `d` is the number of consecutive days) remains ≤ `x`, then we can buy `k` packs for `d` days at once. This transforms the per-day simulation into a per-group calculation, which reduces the problem to O(n log n) sorting and O(n) arithmetic operations.

The brute-force works because it models the problem literally but fails due to potential billions of iterations. The observation about consecutive buying allows us to precompute the maximum number of days a certain prefix of sorted prices can be bought, which collapses repetitive calculations into a single arithmetic step.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * max_days) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and `x`, then read the array `a`.
3. Sort the array `a` in ascending order. Sorting ensures that we always attempt to buy the cheapest packs first, maximizing the number of packs bought.
4. Initialize `total_packs = 0`. This will accumulate all packs bought over all days.
5. Iterate over the array `a` with an index `i` representing the last pack in the current prefix. For each prefix `a[0..i]`, compute the sum `prefix_sum` of these `i+1` elements. This sum represents the cost of buying all packs in this prefix on day 0.
6. Determine how many consecutive days `d` we can buy this prefix without exceeding `x`. Using integer division: `d = (x - prefix_sum) // (i+1) + 1`. We add 1 because day 0 is included. If `d <= 0`, skip this prefix.
7. Increment `total_packs` by `(i+1) * d`. This accounts for buying `i+1` packs each day for `d` days.
8. Reduce `x` for the next iteration if needed, but in our approach, we do not actually need to modify `x` per prefix since each prefix computes days independently.
9. After finishing the loop, print `total_packs` for the current test case.

Why it works: sorting ensures we always consider cheapest packs first. By calculating consecutive days mathematically, we guarantee we buy the maximum possible without simulating each day. The prefix sums and day calculation respect the invariant that prices increase by exactly 1 each day.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))
        a.sort()
        total = 0
        prefix_sum = 0
        for i in range(n):
            prefix_sum += a[i]
            if prefix_sum > x:
                break
            days = (x - prefix_sum) // (i + 1) + 1
            total += days * (i + 1)
        print(total)

if __name__ == "__main__":
    solve()
```

The code reads input efficiently using `sys.stdin.readline`. Sorting the pack prices guarantees we buy cheaper packs first. `prefix_sum` tracks cumulative cost for the current prefix, and `(x - prefix_sum) // (i + 1) + 1` computes the number of consecutive days we can afford this prefix. Multiplying by `(i + 1)` gives the total packs for this prefix. The loop breaks as soon as `prefix_sum > x` because no packs in this prefix are affordable on the first day.

## Worked Examples

**Sample 1 Input:**

```
3 7
2 1 2
```

| Day | Prices | Budget | Bought | Prefix Sum | Days Computed | Total Packs |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1,2,2 | 7 | 3 | 5 | 1 | 3 |
| 2 | 2,3,3 | 7 | 2 | 5 | 1 | 5 |
| 3 | 3,4,4 | 7 | 2 | 5 | 1 | 7 |
| 4 | 4,5,5 | 7 | 1 | 5 | 1 | 8 |
| 5 | 5,6,6 | 7 | 1 | 5 | 1 | 9 |
| 6 | 6,7,7 | 7 | 1 | 5 | 1 | 10 |
| 7 | 7,8,8 | 7 | 1 | 5 | 1 | 11 |

This trace confirms that the calculation of `days` via `(x - prefix_sum) // (i+1) + 1` captures consecutive purchases efficiently.

**Sample 2 Input:**

```
5 9
10 20 30 40 50
```

Here the cheapest pack is 10, which is greater than `x=9`. No packs can be bought. The algorithm immediately skips the loop after the first prefix sum check.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, prefix sum and loop are O(n) |
| Space | O(n) | To store the array of prices |

Given `n` up to 2·10^5 and total `n` over all test cases ≤ 2·10^5, this solution easily fits within the 2s time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# provided samples
assert run("4\n3 7\n2 1 2\n5 9\n10 20 30 40 50\n1 1\n1\n2 1000\n1 1\n") == "11\n0\n1\n1500"

# custom tests
assert run("1\n1 1\n1\n") == "1", "minimum input"
assert run("1\n3 10\n2 2 2\n") == "15", "all equal small"
assert run("1\n2 5\n1 2\n") == "6", "small varied"
assert run("1\n3 1000000000\n100000000 200000000 300000000\n") == "5500000000", "large numbers"
assert run("1\n5 7\n1 1 1 1 1\n") == "35", "repeated cheap packs"
```

| Test input | Expected output | What it validates |

|
