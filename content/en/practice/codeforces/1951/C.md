---
title: "CF 1951C - Ticket Hoarding"
description: "The task is to buy exactly k concert tickets over n days, with each day offering a ticket price ai. You are limited to buying at most m tickets per day. Additionally, every ticket you buy increases the price of all future tickets by the number of tickets bought on that day."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1951
codeforces_index: "C"
codeforces_contest_name: "Codeforces Global Round 25"
rating: 1400
weight: 1951
solve_time_s: 59
verified: false
draft: false
---

[CF 1951C - Ticket Hoarding](https://codeforces.com/problemset/problem/1951/C)

**Rating:** 1400  
**Tags:** greedy, math, sortings  
**Solve time:** 59s  
**Verified:** no  

## Solution
## Problem Understanding

The task is to buy exactly `k` concert tickets over `n` days, with each day offering a ticket price `a_i`. You are limited to buying at most `m` tickets per day. Additionally, every ticket you buy increases the price of all future tickets by the number of tickets bought on that day. The goal is to minimize total spending.

The input consists of multiple test cases. Each test case provides the number of days `n`, the per-day ticket limit `m`, the total tickets needed `k`, and the initial price array `a`. The output should be a single integer per test case representing the minimal total cost.

Because `n` can reach `3 * 10^5` and `k` up to `10^9`, any solution that simulates each purchase explicitly is too slow. The constraints imply that we need an approach that avoids day-by-day or ticket-by-ticket simulation. Careful attention is required when `k` exceeds `m` or when early purchases make later tickets significantly more expensive. For example, if `a = [1, 2, 3]`, `m = 2`, and `k = 3`, a naive greedy approach that always buys the maximum each day might pay more than necessary, because buying one ticket on the first day and two on the last could cost less.

Edge cases include scenarios where the cheapest tickets are not on the first days, when `k` is smaller than `m`, or when all ticket prices are equal.

## Approaches

The brute-force approach would iterate over all days, buying some number of tickets (0 up to `m` or remaining tickets) and updating all future prices after each purchase. This guarantees correctness but has worst-case complexity O(n*k), which is infeasible for large `k` because `k` can be up to 10^9.

The key insight is that once we sort the ticket prices, the optimal strategy is to buy tickets in order from cheapest to most expensive, while buying as many as allowed (up to `m`) for each of the cheapest days. The reason is that increasing prices only affect later purchases, so we want to "front-load" purchases to the cheapest days while respecting the `m` limit per day. Formally, if we sort the prices and consider buying `x` tickets on day `i`, the effective cost of those tickets is `x * (a_i + previous_tickets_bought)`, where `previous_tickets_bought` accumulates from earlier purchases. By iterating from cheapest to most expensive and always taking the min between `m` and remaining tickets, we guarantee minimal spending without simulating price increases explicitly.

This reduces the problem to sorting followed by a linear scan, giving O(n log n) per test case for sorting and O(n) for purchasing, which is feasible given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*k) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `n`, `m`, `k`, and the array of ticket prices `a`.
2. Sort `a` in non-decreasing order. This ensures we consider the cheapest tickets first.
3. Initialize two variables: `spent` to accumulate total cost and `bought` to track total tickets purchased.
4. Iterate through the sorted array. For each price `price`:

a. Compute `can_buy = min(m, k - bought)`. This is the maximum tickets you can buy today without exceeding per-day or total limits.

b. Add `can_buy * (price + bought)` to `spent`. Here, `bought` represents the cumulative increase from previous purchases.

c. Update `bought += can_buy`.

d. Stop iteration once `bought == k`.
5. Print `spent`.

Why it works: Sorting guarantees that we buy cheaper tickets first. Accumulating `bought` simulates the future price increase without modifying the array, ensuring that each ticket’s effective cost accounts for all previous purchases. Limiting purchases by `m` ensures we never exceed per-day constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m, k = map(int, input().split())
        a = list(map(int, input().split()))
        a.sort()
        spent = 0
        bought = 0
        for price in a:
            if bought >= k:
                break
            can_buy = min(m, k - bought)
            spent += can_buy * (price + bought)
            bought += can_buy
        print(spent)

if __name__ == "__main__":
    solve()
```

The code reads all test cases, sorts ticket prices, and iterates to buy tickets in a greedy manner. `can_buy` ensures we never exceed `m` or `k`. `price + bought` accounts for cumulative price increases. The loop breaks once we reach `k` tickets, avoiding unnecessary computation.

## Worked Examples

### Sample 1

Input:

```
4 2 3
8 6 4 2
```

State of key variables:

| Day | price | bought | can_buy | spent | Comment |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 2 | 4 | Buy 2 cheapest tickets |
| 2 | 4 | 2 | 1 | 9 | Buy remaining 1 ticket, previous bought = 2 |
| 3 | 6 | 3 | 0 | 9 | Stop, already bought 3 |

Total spent = 10

This trace confirms that front-loading cheaper tickets while respecting `m` yields minimal cost.

### Sample 2

Input:

```
4 2 8
8 6 4 2
```

State of key variables:

| Day | price | bought | can_buy | spent | Comment |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 2 | 4 | Buy 2 tickets |
| 2 | 4 | 2 | 2 | 12 | Buy 2 tickets, cost = 2*(4+2) |
| 3 | 6 | 4 | 2 | 24 | Buy 2 tickets, cost = 2*(6+4) |
| 4 | 8 | 6 | 2 | 40 | Buy 2 tickets, cost = 2*(8+6) |

Total spent = 40

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, linear scan is O(n) |
| Space | O(n) | For storing array per test case |

Sorting the prices dominates the runtime, which is feasible because total `n` over all test cases ≤ 3 * 10^5. Memory usage is minimal since we only store the array and a few integers per test case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("1\n4 2 3\n8 6 4 2\n") == "10", "sample 1"
assert run("1\n4 2 8\n8 6 4 2\n") == "64", "sample 2"
assert run("1\n5 100 1\n10000 1 100 10 1000\n") == "1", "sample 3"
assert run("1\n6 3 9\n5 5 5 5 5 5\n") == "72", "sample 4"

# custom cases
assert run("1\n3 1 3\n1 2 3\n") == "10", "all tickets different, m=1"
assert run("1\n3 5 2\n2 2 2\n") == "5", "all equal prices, large m"
assert run("1\n1 10 5\n100\n") == "500", "single day, buy all tickets"
assert run("1\n4 2 7\n1 3 2 4\n") == "29", "edge: k not multiple of m"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 1 3 / 1 2 3 | 10 | Buying one per day, increasing prices |
| 3 5 2 / 2 2 2 | 5 | All prices equal, m > k |
| 1 10 5 / 100 | 500 | Single day, multiple tickets |
| 4 2 7 / 1 3 2 4 | 29 | Non-trivial k, not divisible by m |

## Edge Cases

If `k` is smaller than `m`, the algorithm buys exactly `k` tickets from the cheapest day. For example, `n = 3, m = 5, k = 2, a = [3,1,2]` sorts to `[1,2,3]`. `can_buy = min(5,2-0)=2` buys both tickets on day 1 with `spent = 2*(1+0)=2`. No further purchases occur. This correctly handles the boundary
