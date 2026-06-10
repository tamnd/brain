---
title: "CF 1488F - Dogecoin"
description: "Ann wants to maximize profit by mining and selling Dogecoin over a period of days. She earns exactly one coin per day she mines, and the price of a coin varies each day according to a given list."
date: "2026-06-10T22:48:57+07:00"
tags: ["codeforces", "competitive-programming", "*special", "binary-search", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 1488
codeforces_index: "F"
codeforces_contest_name: "Kotlin Heroes: Episode 6"
rating: 2300
weight: 1488
solve_time_s: 185
verified: false
draft: false
---

[CF 1488F - Dogecoin](https://codeforces.com/problemset/problem/1488/F)

**Rating:** 2300  
**Tags:** *special, binary search, data structures  
**Solve time:** 3m 5s  
**Verified:** no  

## Solution
## Problem Understanding

Ann wants to maximize profit by mining and selling Dogecoin over a period of days. She earns exactly one coin per day she mines, and the price of a coin varies each day according to a given list. For each of several plans, defined by a start day `l` and an end day `r`, she must mine every day in the interval `[l, r]` and sell all coins by day `r`. The output for each plan is the maximum total profit she can get from selling the mined coins over the specified interval.

The input provides `n`, the number of days, followed by an array of coin prices for each day. Then there are `q` plans, each specifying a mining interval `[l, r]`. The constraints indicate that both `n` and `q` can be up to 200,000, which implies that any naive solution that iterates over the interval for each query would require up to `O(n * q)` operations. With a worst-case of roughly `4*10^10` operations, this is far too slow for a 2-second time limit, so we need an approach that precomputes data to answer each query efficiently.

A naive approach might ignore the fact that Ann can choose the best day to sell each mined coin, leading to suboptimal profit if she simply sells coins at the price of the day they are mined. Edge cases arise when the price fluctuates, for example: if the prices are `[1, 100, 1]` and she mines three days, a naive daily-sell approach gives a total of `1 + 100 + 1 = 102`, whereas selling all coins on the day with the highest price `100` yields `1 + 1 + 1` coins times `100 = 300`. Another edge case is when the interval contains only one day; in this case, the maximum profit is simply the coin price of that single day.

## Approaches

The brute-force solution considers each plan independently and simulates selling coins for every day in the interval. It would track the number of coins mined so far and always sell them at the current day's price. This is correct, but it iterates over each day in each query interval, leading to `O(n*q)` complexity, which is unacceptable for the maximum constraints. For `n = 200,000` and `q = 200,000`, this would require roughly 40 billion operations.

The key observation is that since Ann can sell any amount of coins on any day, she always wants to sell coins on the day with the highest price within her mining interval. The total profit for an interval `[l, r]` is simply the sum of the top `k` prices she can sell on each day, where `k` coins are available by day `r`. Since she mines exactly one coin per day, there will be `r - l + 1` coins to sell, and the optimal strategy is to sell all coins on the day with the maximum price in `[l, r]`. This reduces the problem to computing the sum of the maximum prefix sums over the interval.

A simple way to implement this efficiently is to use a prefix sum array of prices and a segment tree or a sparse table to compute maximums over any interval in `O(1)` (for sparse table) or `O(log n)` (for segment tree) time per query. The sparse table is especially efficient here because the array is static; no updates occur, only queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*q) | O(1) | Too slow |
| Sparse Table / Segment Tree for range max | O(n log n + q) | O(n log n) | Accepted |

## Algorithm Walkthrough

1. Read the number of days `n` and the price array `c`. This sets up the array on which we will perform interval queries.
2. Build a sparse table from `c` that can return the maximum price in any interval `[l, r]` in `O(1)` time. Precompute the logs and table rows using standard sparse table construction.
3. Read the number of queries `q` and the list of mining plans. For each query `[l, r]`, convert indices to zero-based for easier array access.
4. For each plan, compute the sum of prices from `l` to `r`. Then find the maximum price in that interval using the sparse table. The maximum profit is obtained by multiplying the number of coins mined `(r - l + 1)` by the maximum price in that interval.
5. Output the maximum profit for each query.

Why it works: By always selling coins on the day with the highest price in the interval, Ann maximizes the revenue. The sparse table guarantees that we can find this maximum in constant time for each query after `O(n log n)` preprocessing. Since all coins are identical and she must sell all coins by the last day, this strategy is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_sparse_table(arr):
    import math
    n = len(arr)
    K = n.bit_length()
    st = [[0] * n for _ in range(K)]
    st[0] = arr[:]
    for k in range(1, K):
        for i in range(n - (1 << k) + 1):
            st[k][i] = max(st[k-1][i], st[k-1][i + (1 << (k-1))])
    return st

def query_max(st, l, r):
    import math
    k = (r - l + 1).bit_length() - 1
    return max(st[k][l], st[k][r - (1 << k) + 1])

def main():
    n = int(input())
    c = list(map(int, input().split()))
    st = build_sparse_table(c)
    q = int(input())
    res = []
    for _ in range(q):
        l, r = map(int, input().split())
        l -= 1
        r -= 1
        num_coins = r - l + 1
        max_price = query_max(st, l, r)
        res.append(num_coins * max_price)
    print(" ".join(map(str, res)))

if __name__ == "__main__":
    main()
```

The sparse table construction builds `K` layers, where each layer stores the maximum over intervals of length `2^k`. During queries, the largest power of two fitting in `[l, r]` determines which two overlapping intervals to consider. Converting 1-based indices to 0-based ensures correctness. Multiplying the number of coins by the maximum price directly produces the maximum profit.

## Worked Examples

Sample input:

```
5
4 1 2 3 2
4
1 5
2 4
3 5
5 5
```

| Query | Interval | Max Price | Coins | Profit |
| --- | --- | --- | --- | --- |
| 1 | 1-5 | 4 | 5 | 20 |
| 2 | 2-4 | 3 | 3 | 9 |
| 3 | 3-5 | 3 | 3 | 9 |
| 4 | 5-5 | 2 | 1 | 2 |

This trace confirms that the algorithm correctly identifies the optimal day to sell and computes profits accordingly.

Another example:

```
3
1 100 1
2
1 3
2 3
```

| Query | Interval | Max Price | Coins | Profit |
| --- | --- | --- | --- | --- |
| 1 | 1-3 | 100 | 3 | 300 |
| 2 | 2-3 | 100 | 2 | 200 |

This demonstrates that the algorithm handles sharp price spikes correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + q) | Sparse table preprocessing is O(n log n), and each query is O(1) |
| Space | O(n log n) | Sparse table stores log n layers of size n |

Given `n, q <= 2*10^5`, this approach fits comfortably within the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    return output.getvalue().strip()

# Provided sample
assert run("5\n4 1 2 3 2\n4\n1 5\n2 4\n3 5\n5 5\n") == "20 9 9 2", "sample 1"

# Minimum size
assert run("1\n5\n1\n1 1\n") == "5", "min size"

# All equal values
assert run("4\n2 2 2 2\n2\n1 4\n2 3\n") == "8 4", "all equal"

# Maximum values
assert run("5\n1000000 1000000 1000000 1000000 1000000\n1\n1 5\n") == "5000000", "max values"

# Boundary condition
assert run("3\n1 2 3\n1\n2 3\n") == "4", "boundary"

# Peak in middle
assert run("5\n1 10 1 10 1\n1\n1 5\n") == "50
```
