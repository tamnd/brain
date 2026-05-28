---
title: "CF 41B - Martian Dollar"
description: "We are asked to maximize the amount of money Vasya can have at the end of n days if he starts with a given sum of bourle"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 41
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 40 (Div. 2)"
rating: 1400
weight: 41
solve_time_s: 68
verified: true
draft: false
---

[CF 41B - Martian Dollar](https://codeforces.com/problemset/problem/41/B)

**Rating:** 1400  
**Tags:** brute force  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to maximize the amount of money Vasya can have at the end of _n_ days if he starts with a given sum of bourles and can buy and later sell Martian dollars. Each day has a price for dollars, and Vasya can only perform one buy-sell operation, purchasing an integer number of dollars and selling them later at the full integer price on a subsequent day.

The input gives the number of days, the initial money in bourles, and a list of daily dollar prices. The output is the maximum amount of bourles Vasya can have after possibly buying and selling once.

The constraints are small: both the number of days and the initial money are at most 2000, which allows algorithms that scale quadratically, because 2000² operations is only about four million, which fits comfortably in a 2-second time limit. The main challenge is not efficiency but correctly modeling the integer buy/sell behavior.

A few edge cases are non-obvious. For example, if dollar prices never increase, the optimal strategy is to never buy, so the maximum money is the initial amount. If the initial money is smaller than all dollar prices, Vasya cannot buy any dollars, and again the maximum money is unchanged. A careless solution that assumes he always buys at the first day will produce the wrong answer here.

## Approaches

The most straightforward approach is brute-force. For every day, consider buying dollars on that day. For each potential buy day, simulate selling on every later day. Compute the number of dollars Vasya can buy (integer division of his current bourles by the price), multiply by the selling price, and add any leftover bourles to compute the final total. Keep track of the maximum across all buy/sell pairs.

This method is correct because it enumerates all possible buy/sell decisions. The operation count is roughly $O(n^2)$ because for each of the n days we might consider buying, we check all later days as potential sell days. With n ≤ 2000, this is at most four million operations, which is acceptable.

The key insight that lets us simplify slightly is that the maximum selling price after a given day is what matters. Instead of checking all later days for each buy day, we can precompute the maximum price from day _i_ onward. Then the profit for buying on day _i_ is simply `(max_price_after_i - price[i]) * dollars_can_buy`. This reduces redundant comparisons and simplifies reasoning, though asymptotically it remains O(n²) because computing dollars and leftover bourles still involves integer arithmetic per day.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Optimized Max-Tracking | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of days `n` and initial money `b`, then read the array of daily prices `a`.
2. Initialize a variable `max_money` with the initial money, representing the scenario where Vasya does not buy any dollars.
3. Iterate over each day `i` as a potential buy day. Compute the number of dollars Vasya can buy as `b // a[i]`. If he cannot buy any dollars, skip to the next day.
4. For each buy day `i`, iterate over each later day `j > i` as a potential sell day. Compute the final money if Vasya sells on day `j` as `dollars_bought * a[j] + leftover_bourles`. Update `max_money` if this total is larger.
5. After checking all possible buy/sell pairs, print `max_money`.

Why it works: At each iteration, we consider all feasible buy and sell days, and the computation respects integer dollar purchases and leftover bourles. Since every valid scenario is enumerated, the maximum across all iterations is guaranteed to be the true maximum. Skipping days where no dollars can be purchased ensures correctness for edge cases where initial money is too small.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, b = map(int, input().split())
a = list(map(int, input().split()))

max_money = b

for i in range(n):
    dollars = b // a[i]
    leftover = b % a[i]
    if dollars == 0:
        continue
    for j in range(i + 1, n):
        total = dollars * a[j] + leftover
        if total > max_money:
            max_money = total

print(max_money)
```

This solution first reads input efficiently using `sys.stdin.readline`. We maintain `max_money` to account for the possibility of not buying at all. For each potential buy day, integer division gives the number of dollars Vasya can purchase, and the modulo operation gives leftover bourles. We skip iterations where no dollars can be bought. Nested loops consider all possible sell days, updating the maximum money seen. Using integer arithmetic carefully ensures no floating point errors.

## Worked Examples

**Sample 1**

Input:

```
2 4
3 7
```

| Buy Day i | Dollars | Leftover | Sell Day j | Total Money | max_money |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 1*7 + 1 = 8 | 8 |

Explanation: Vasya can buy 1 dollar at 3 bourles, leaving 1 bourle. Selling on day 1 at 7 yields 8, which is the optimal.

**Custom Example**

Input:

```
3 5
5 4 3
```

| Buy Day i | Dollars | Leftover | Sell Day j | Total Money | max_money |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 1*4 + 0 = 4 | 5 |
| 0 | 1 | 0 | 2 | 1*3 + 0 = 3 | 5 |
| 1 | 1 | 1 | 2 | 1*3 + 1 = 4 | 5 |

Explanation: Prices decrease daily. Buying any day leads to less than the initial 5 bourles. Optimal is to do nothing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Each buy day checks all later sell days; n ≤ 2000 so ~4e6 operations |
| Space | O(n) | Array of prices, constant extra variables |

Given the constraints, this solution is fast enough. Memory usage is small, well under the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, b = map(int, input().split())
    a = list(map(int, input().split()))
    max_money = b
    for i in range(n):
        dollars = b // a[i]
        leftover = b % a[i]
        if dollars == 0:
            continue
        for j in range(i + 1, n):
            total = dollars * a[j] + leftover
            if total > max_money:
                max_money = total
    return str(max_money)

# provided sample
assert run("2 4\n3 7\n") == "8", "sample 1"

# minimum-size input
assert run("1 1\n1\n") == "1", "min input"

# prices decreasing
assert run("3 5\n5 4 3\n") == "5", "no profit"

# all-equal prices
assert run("4 10\n2 2 2 2\n") == "10", "no profit all same"

# buy on first day, sell on last
assert run("3 10\n2 5 6\n") == "30", "first to last"

# initial money too small
assert run("3 1\n2 3 4\n") == "1", "cannot buy"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 \n 1 | 1 | Minimum input |
| 3 5 \n 5 4 3 | 5 | Prices decreasing, no buy |
| 4 10 \n 2 2 2 2 | 10 | All prices equal, buying unnecessary |
| 3 10 \n 2 5 6 | 30 | Buy first day, sell last day maximizes profit |
| 3 1 \n 2 3 4 | 1 | Initial money too small to buy |

## Edge Cases

If initial money is smaller than all prices, Vasya cannot buy any dollars. For example, `b = 1` and prices `[2,3,4]`. The algorithm computes `dollars = b // a[i]` as 0 for each day, skips all iterations, and leaves `max_money = b = 1`.

If prices decrease monotonically, buying early results in lower money than initial, so skipping buying yields the maximum. The trace confirms that the algorithm correctly compares total money to `max_money` at each step and never chooses a worse option.

If prices remain constant, any buy-sell cycle is equivalent to keeping the initial money, and the
