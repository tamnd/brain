---
title: "CF 102899I - KK \u4e70\u80a1\u7968"
description: "We are given a sequence of stock prices over n days. On each day i, the stock has a known price p[i]. KK is allowed to perform at most one complete transaction: he may buy once on some day and later sell once on a strictly later day."
date: "2026-07-04T08:21:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102899
codeforces_index: "I"
codeforces_contest_name: "The 2nd Hangzhou Normal University Freshman Programming Contest"
rating: 0
weight: 102899
solve_time_s: 34
verified: true
draft: false
---

[CF 102899I - KK \u4e70\u80a1\u7968](https://codeforces.com/problemset/problem/102899/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of stock prices over n days. On each day i, the stock has a known price p[i]. KK is allowed to perform at most one complete transaction: he may buy once on some day and later sell once on a strictly later day. He starts with unlimited cash, so the goal is purely to maximize profit, defined as sell price minus buy price. If every possible transaction leads to non-positive profit, the answer is defined to be zero.

The structure is a single array scan problem where we are trying to pick two indices i < j that maximize p[j] − p[i].

The constraint n up to 100000 immediately rules out any O(n²) enumeration of all pairs. A quadratic solution would require about 10¹⁰ comparisons in the worst case, which is far beyond a 1-second limit in Python. This pushes us toward a linear or near-linear approach that processes the array in one pass or a small number of passes.

A subtle edge case appears when prices never increase. For example, if the sequence is 5 4 3 2, any buy-sell pair produces a negative result, but since KK is not forced to trade, the correct answer is 0. A naive approach that blindly takes the best difference might incorrectly return a negative number instead of clamping to zero.

Another edge case is when the best profit is achieved by buying at the global minimum that occurs late. For example, in 10 1 7 3 8 6, the best buy is at 1 and sell at 8, but the minimum might appear after a locally good sell if we are not careful about tracking history.

## Approaches

The brute-force idea is straightforward: try every possible pair of buy and sell days. For each i, we consider all j > i and compute p[j] − p[i], tracking the maximum. This is correct because it exhausts all valid transactions. However, for each of n starting points, we may scan up to n subsequent points, leading to roughly n(n−1)/2 operations, which is about 5×10⁹ when n is 100000. This cannot run within the time limit.

The key observation is that when we fix a selling day j, the best possible buy day is simply the day with the minimum price among all previous days. Instead of recomputing this minimum repeatedly, we maintain it while scanning from left to right. At every step, we know the cheapest price seen so far, and we compare the current price as a potential sell against that best possible buy.

This reduces the problem to a single pass where we continuously update two pieces of information: the minimum prefix value and the best profit obtained so far.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| One-pass tracking minimum | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a variable `min_price` with a very large value and `best_profit` as 0. The `min_price` represents the lowest stock price seen up to the current day, which is the best possible buying point so far.
2. Iterate through the price array from left to right.
3. For each price p[i], compute the profit if we sell on day i after buying at the cheapest earlier day, which is p[i] − min_price.
4. Update `best_profit` if this computed profit is larger than the current best.
5. Update `min_price` if p[i] is smaller than the current minimum, because future sales should consider this as a better buying option.
6. After processing all days, output `best_profit`.

The crucial point is the order inside the loop: we must compute profit using the previous minimum before potentially updating it with the current price. Otherwise, we would incorrectly allow buying and selling on the same day.

### Why it works

At every index i, `min_price` stores the minimum value of p[0..i−1]. This guarantees that when evaluating day i as a selling point, we consider all valid buy days strictly before i. Any optimal solution (i, j) must have j as the selling day, and our scan ensures that when we reach j, the best possible i has already been captured in `min_price`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    p = list(map(int, input().split()))
    
    min_price = p[0]
    best = 0
    
    for i in range(1, n):
        price = p[i]
        
        # sell today using best previous buy
        best = max(best, price - min_price)
        
        # update best buy candidate
        if price < min_price:
            min_price = price
    
    print(best)

if __name__ == "__main__":
    solve()
```

The solution uses a single pass through the array, maintaining a running minimum and the best profit. The initialization with p[0] is safe because the first possible transaction must involve at least one earlier day, and we only start computing profits from day 2 onward.

A common mistake is updating `min_price` before computing profit for the current day. That would allow using the same day as both buy and sell, which violates the problem constraint.

## Worked Examples

### Example 1: 1 7 3 8 6

We track the evolution day by day.

| Day | Price | Min so far | Profit today | Best profit |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | - | 0 |
| 2 | 7 | 1 | 6 | 6 |
| 3 | 3 | 1 | 2 | 6 |
| 4 | 8 | 1 | 7 | 7 |
| 5 | 6 | 1 | 5 | 7 |

The maximum profit occurs when buying at 1 and selling at 8, giving 7. The table shows how the minimum stabilizes early and all later improvements come from higher selling prices.

### Example 2: 3 2 8

| Day | Price | Min so far | Profit today | Best profit |
| --- | --- | --- | --- | --- |
| 1 | 3 | 3 | - | 0 |
| 2 | 2 | 2 | - | 0 |
| 3 | 8 | 2 | 6 | 6 |

This demonstrates the importance of updating the minimum before the final day contributes as a buy candidate. The best buy shifts to day 2 once we encounter the lower price.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each price is processed once with constant-time updates |
| Space | O(1) | Only two variables are maintained |

The linear scan fits comfortably within the constraint of 100000 elements. The operations are simple integer comparisons and updates, well within typical time limits for Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    p = list(map(int, input().split()))
    
    min_price = p[0]
    best = 0
    
    for i in range(1, n):
        best = max(best, p[i] - min_price)
        min_price = min(min_price, p[i])
    
    return str(best)

# provided samples
assert run("5\n1 7 3 8 6\n") == "7"
assert run("3\n3 2 8\n") == "6"

# custom cases
assert run("2\n5 4\n") == "0", "monotone decreasing"
assert run("2\n1 10\n") == "9", "simple increasing"
assert run("5\n5 5 5 5 5\n") == "0", "all equal"
assert run("6\n10 1 2 3 4 5\n") == "4", "min early then rising"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 4 | 0 | no profitable trade |
| 1 10 | 9 | basic profit computation |
| all equal | 0 | flat prices edge case |
| 10 1 2 3 4 5 | 4 | minimum shifts early |

## Edge Cases

For a strictly decreasing sequence like 5 4 3 2, the algorithm sets `min_price` to 5 initially. Every subsequent day produces a negative or zero profit, and `best` remains 0 throughout. The running minimum updates continuously but never helps create a positive difference, matching the required output.

For a sequence where the minimum occurs late, such as 8 7 6 1 10, the algorithm correctly avoids prematurely fixing an early minimum. When reaching 1, `min_price` becomes 1, and the final day 10 yields profit 9, which is correctly captured because the update of `min_price` happens after computing profit for each day.
