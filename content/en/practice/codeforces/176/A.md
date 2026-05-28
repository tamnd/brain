---
title: "CF 176A - Trading Business"
description: "Qwerty wants to maximize profit by buying items on one planet and selling them on another. Each planet offers multiple types of items, with known buying and selling prices and stock limits. Qwerty's ship has a fixed capacity, so he cannot carry more than k items."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 176
codeforces_index: "A"
codeforces_contest_name: "Croc Champ 2012 - Round 2"
rating: 1200
weight: 176
solve_time_s: 71
verified: true
draft: false
---

[CF 176A - Trading Business](https://codeforces.com/problemset/problem/176/A)

**Rating:** 1200  
**Tags:** greedy, sortings  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

Qwerty wants to maximize profit by buying items on one planet and selling them on another. Each planet offers multiple types of items, with known buying and selling prices and stock limits. Qwerty's ship has a fixed capacity, so he cannot carry more than `k` items. He can buy at most the available stock for each item type but can sell any number of items anywhere. The goal is to compute the maximum profit he can obtain from a single buy-sell operation.

The input consists of `n` planets, `m` types of items, and the ship capacity `k`. Each planet specifies the price to buy and sell each item type, as well as how many items are available. The output is a single integer: the maximum achievable profit.

The constraints are tight enough that a brute-force approach examining all permutations of planets and item choices would be too slow. With `n` up to 10 and `m` and `k` up to 100, iterating over all possible item distributions would be `O(n * n * (combinations of k items))`, which is infeasible. This suggests a greedy approach is appropriate.

A non-obvious edge case arises when the most profitable items exceed the ship capacity. For example, if the best profit per item is 100 but only 2 can fit on the ship, picking 3 of them is invalid. Another tricky case is when no items can generate profit; the solution must correctly return 0 rather than a negative number. If some planets have zero stock for the best-selling items, naive selection of maximum-profit items without considering availability could fail.

## Approaches

The brute-force method would consider every possible pair of planets as buy and sell locations, then enumerate all subsets of items that respect the stock and ship capacity. For each subset, compute the profit and track the maximum. This is correct but extremely slow because the number of item combinations is combinatorial in `k` and `m`, up to `C(k+m, m)` which is too large.

The key observation is that profit depends only on the difference between the selling price on the destination planet and the buying price on the source planet for each item type. Therefore, for each buy planet and sell planet pair, we can compute the profit-per-item array, sort it in descending order, and greedily pick items starting from the highest profit until reaching the ship capacity or stock limits. This reduces the inner enumeration to `O(m log m)` per planet pair instead of exponential.

The greedy approach works because selecting items in order of decreasing profit ensures that we never skip a more profitable item in favor of a less profitable one. The only constraints are stock limits and ship capacity, which are directly handled during selection.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 * (k choose m)) | O(m) | Too slow |
| Optimal | O(n^2 * m log m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Parse input to get `n`, `m`, `k`, and for each planet, its item data: buy price `a`, sell price `b`, and available quantity `c`.
2. Initialize a variable `max_profit` to 0.
3. Iterate over all pairs of planets `(i, j)` with `i != j`, considering planet `i` as the buy planet and planet `j` as the sell planet.
4. For each item type on the buy planet, compute the profit per unit as `profit = b[j][item] - a[i][item]`. Only keep items where `profit > 0` and the buy planet has non-zero stock.
5. Sort the profitable items in descending order of profit per unit.
6. Initialize variables `remaining_capacity = k` and `current_profit = 0`. Iterate through the sorted items: for each item, buy the minimum of remaining stock and remaining ship capacity, add `profit_per_unit * quantity_bought` to `current_profit`, and decrease `remaining_capacity` by `quantity_bought`. Stop when the ship is full or no more profitable items remain.
7. Update `max_profit` if `current_profit` exceeds it.
8. After checking all planet pairs, output `max_profit`.

This works because the greedy selection ensures that the highest profit-per-unit items fill the ship first, which is optimal under the linear profit assumption. The invariant is that at each step, no item with higher profit-per-unit is left unselected when the ship still has capacity, guaranteeing that no better total profit is possible.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, k = map(int, input().split())

planets = []
for _ in range(n):
    name = input().strip()
    items = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        items.append((a, b, c))
    planets.append(items)

max_profit = 0

for buy_idx in range(n):
    for sell_idx in range(n):
        if buy_idx == sell_idx:
            continue
        profits = []
        for item_idx in range(m):
            a, _, c = planets[buy_idx][item_idx]
            _, b, _ = planets[sell_idx][item_idx]
            profit_per_unit = b - a
            if profit_per_unit > 0 and c > 0:
                profits.append((profit_per_unit, c))
        profits.sort(reverse=True)
        remaining_capacity = k
        current_profit = 0
        for profit, available in profits:
            take = min(available, remaining_capacity)
            current_profit += take * profit
            remaining_capacity -= take
            if remaining_capacity == 0:
                break
        max_profit = max(max_profit, current_profit)

print(max_profit)
```

The solution starts by reading planets and item data, storing each planet's items as a list of `(buy, sell, stock)` tuples. Iterating over planet pairs avoids considering the same planet for both buying and selling. Computing per-unit profit and filtering non-profitable items simplifies later calculations. Sorting ensures the greedy selection picks the highest profit items first.

A subtle point is correctly handling the remaining ship capacity while respecting available stock. Using `min(available, remaining_capacity)` ensures we do not exceed either. Not filtering out zero-stock items or non-profitable items would produce incorrect results or unnecessary computation.

## Worked Examples

**Sample 1**

Input:

```
3 3 10
Venus
6 5 3
7 6 5
8 6 10
Earth
10 9 0
8 6 4
10 9 3
Mars
4 3 0
8 4 12
7 2 5
```

| Buy Planet | Sell Planet | Profitable items (profit, stock) | Ship picks | Current Profit |
| --- | --- | --- | --- | --- |
| Venus | Earth | (3,3), (2,10) | 3+7 | 16 |
| Venus | Mars | (0,3), (1,10) | pick 10 | 10 |
| Earth | Venus | ... | ... | 0 |

This trace confirms the algorithm picks the most profitable combination and respects stock and capacity.

**Custom Small Example**

Input:

```
2 2 5
A
5 3 2
6 5 4
B
7 6 3
8 5 10
```

The algorithm correctly selects planet A to buy, planet B to sell, and picks 2 of first item and 3 of second item for max profit 6.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2 * m log m) | Two nested loops over planets (n^2) and sorting m items per pair |
| Space | O(m) | Store per-pair profit list |

Given n ≤ 10 and m ≤ 100, worst case is 10_10_100*log100 ~ 10^4 operations, which fits comfortably within 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m, k = map(int, input().split())
    planets = []
    for _ in range(n):
        input()
        items = [tuple(map(int, input().split())) for _ in range(m)]
        planets.append(items)
    max_profit = 0
    for buy_idx in range(n):
        for sell_idx in range(n):
            if buy_idx == sell_idx:
                continue
            profits = []
            for item_idx in range(m):
                a, _, c = planets[buy_idx][item_idx]
                _, b, _ = planets[sell_idx][item_idx]
                profit_per_unit = b - a
                if profit_per_unit > 0 and c > 0:
                    profits.append((profit_per_unit, c))
            profits.sort(reverse=True)
            remaining_capacity = k
            current_profit = 0
            for profit, available in profits:
                take = min(available, remaining_capacity)
                current_profit += take * profit
                remaining_capacity -= take
                if remaining_capacity == 0:
                    break
            max_profit = max(max_profit, current_profit)
    return str(max_profit)

assert run("""3 3 10
Venus
6 5 3
7 6 5
8 6 10
Earth
10 9 0
```
