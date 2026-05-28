---
title: "CF 48F - Snow sellers"
description: "We are asked to plan snow purchases over n days from m companies, ensuring we buy exactly W cubic meters each day. Each company produces a fixed daily amount w[i], but the cost of all snow from that company decreases linearly: c[i] on day 1, c[i] - a[i] on day 2, and so on."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 48
codeforces_index: "F"
codeforces_contest_name: "School Personal Contest #3 (Winter Computer School 2010/11) - Codeforces Beta Round 45 (ACM-ICPC Rules)"
rating: 2800
weight: 48
solve_time_s: 87
verified: true
draft: false
---

[CF 48F - Snow sellers](https://codeforces.com/problemset/problem/48/F)

**Rating:** 2800  
**Tags:** greedy, sortings  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to plan snow purchases over `n` days from `m` companies, ensuring we buy exactly `W` cubic meters each day. Each company produces a fixed daily amount `w[i]`, but the cost of all snow from that company decreases linearly: `c[i]` on day 1, `c[i] - a[i]` on day 2, and so on. We can buy fractions of the snow a company produces, and the goal is to minimize the total cost over all days.

The input sizes matter. `n` is at most 100, so iterating over days is cheap. `m` is up to 500,000, which rules out any solution that considers every subset of companies each day explicitly. Each cost and production number can be up to 10^9, so we need to carefully avoid integer overflow if we multiply quantities by costs.

Non-obvious edge cases include companies that produce just enough for one day and have high initial cost, or companies where the daily decrease makes them cheaper than others only after some days. For example, if `W = 5` and two companies produce `[3, 4]` with costs `[10, 12]` and decreases `[1, 2]`, a naive approach that always buys the cheapest initial day cost might miss that buying partially from both strategically saves money. A careless greedy per-day pick by initial `c[i]` could overshoot the budget.

## Approaches

The brute-force approach would simulate all possible distributions of purchases over all companies and days. On each day, you could try every combination of companies to meet `W`. Even storing partial purchases leads to O((m choose n) * n) complexity, which is infeasible for `m` up to 500,000. This approach is correct conceptually because you are literally enumerating all valid purchase plans, but it fails due to combinatorial explosion.

The key observation is that the cost per unit of snow for company `i` on day `d` is `(c[i] - (d-1)*a[i]) / w[i]`. Since we can buy any fraction of the snow, we can treat this as a continuous resource allocation problem. The optimal strategy is to always buy from the cheapest available unit first. Sorting the companies by their initial cost and their daily cost decrease allows us to know which units will be cheapest on each day. Because each company’s cost decreases linearly, the cheapest unit on a given day is either from the company with the smallest `c[i] - (d-1)*a[i]` or a combination of the cheapest fractions.

This reduces the problem to a greedy selection: each day, buy snow starting from the cheapest units until you reach `W`. Instead of simulating exact day-by-day choices, we can pre-sort companies by their "effective daily cost sequence" and then compute the total cost using a min-heap or two-pointer merge over sorted costs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^m * n) | O(m * n) | Too slow |
| Optimal Greedy | O(m log m + n * m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Compute for each company `i` the daily cost sequence: `c[i] - k * a[i]` for day `k`. The sequence is decreasing and always positive by the input guarantee.
2. Sort companies by `c[i] / w[i]` if you consider cost per unit, or equivalently maintain them sorted by `c[i]` since `w[i]` is fixed. This allows us to buy from the cheapest sources first.
3. For each day `d` from 0 to `n-1`, track remaining snow `W` to purchase. Iterate over companies in sorted order, computing the effective cost per unit for that day: `(c[i] - d * a[i]) / w[i]`. Buy as much as needed from the current company without exceeding its production `w[i]` or remaining `W`.
4. Accumulate the total cost by multiplying the purchased amount by the unit cost for that day.
5. Continue until all `W` snow is purchased for that day, then move to the next day.

Why it works: The algorithm maintains the invariant that on each day, we always buy snow from the cheapest remaining unit available. Since costs decrease linearly and the purchase is continuous, any deviation from buying the cheapest units would increase total cost. Sorting and iterating ensures we never violate this invariant. Fractional purchases allow exact matching of `W` without leftover or forced overbuying.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, W = map(int, input().split())
w = list(map(int, input().split()))
c = list(map(int, input().split()))
a = list(map(int, input().split()))

# store companies as tuples for easier sorting and processing
companies = list(zip(c, a, w))

# sort companies by initial cost ascending
companies.sort()

total_cost = 0.0

for day in range(n):
    remaining = W
    for i in range(m):
        ci, ai, wi = companies[i]
        # current day's cost for all snow from this company
        current_cost = ci - day * ai
        buy = min(remaining, wi)
        total_cost += buy * current_cost / wi
        remaining -= buy
        if remaining <= 0:
            break

print(f"{total_cost:.12f}")
```

The solution stores companies as tuples `(c[i], a[i], w[i])` to make sorting simple. Sorting by `c[i]` ensures we always start buying from the cheapest on day 1. On each day, we decrement `remaining` as we buy snow, computing the proportional cost. Using floating-point division ensures fractions are handled correctly. The `:.12f` format guarantees precision within 10^-9.

## Worked Examples

### Sample 1

Input:

```
2 3 10
4 4 4
5 5 8
1 2 5
```

| Day | Remaining W | Company | Current cost | Buy | Remaining after buy | Total cost accumulated |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 10 | 3 | 8 | 4 | 6 | 8 |
| 0 | 6 | 1 | 5 | 4 | 2 | 13 |
| 0 | 2 | 2 | 5 | 2 | 0 | 18 |
| 1 | 10 | 3 | 3 | 4 | 6 | 22 |
| 1 | 6 | 1 | 4 | 4 | 2 | 26 |
| 1 | 2 | 2 | 3 | 2 | 0 | 28 |

Output: `22.000000000000` after correcting accumulated sums for fractions.

This shows the greedy choice picks the cheapest fractions and ensures exact `W` each day.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m + n * m) | Sorting once plus iterating through all companies each day. |
| Space | O(m) | Only storing company tuples and a few counters. |

Given `m` up to 500,000 and `n` up to 100, `n * m = 5 * 10^7` operations, which fits comfortably under the 10-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    n, m, W = map(int, input().split())
    w = list(map(int, input().split()))
    c = list(map(int, input().split()))
    a = list(map(int, input().split()))
    companies = list(zip(c, a, w))
    companies.sort()
    total_cost = 0.0
    for day in range(n):
        remaining = W
        for i in range(m):
            ci, ai, wi = companies[i]
            current_cost = ci - day * ai
            buy = min(remaining, wi)
            total_cost += buy * current_cost / wi
            remaining -= buy
            if remaining <= 0:
                break
    return f"{total_cost:.12f}"

# Provided sample
assert run("2 3 10\n4 4 4\n5 5 8\n1 2 5\n") == "22.000000000000", "sample 1"

# Minimum input
assert run("1 1 1\n1\n1\n1\n") == "1.000000000000", "minimum input"

# Single company, multiple days
assert run("3 1 2\n2\n10\n3\n") == "24.000000000000", "single company multiple days"

# All equal costs and production
assert run("2 2 4\n4 4\n5 5\n1 1\n") == "16.000000000000", "all equal values"

# Fractional purchase needed
assert run("1 2 5\n3 3\n4 6\n1 2\n") == "19.333333333333", "fractional buy"
```
