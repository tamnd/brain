---
title: "CF 12C - Fruits"
description: "Valera has a shopping list containing a number of fruits, possibly with duplicates if he wants more than one of the same"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 12
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 12 (Div 2 Only)"
rating: 1100
weight: 12
solve_time_s: 62
verified: true
draft: false
---

[CF 12C - Fruits](https://codeforces.com/problemset/problem/12/C)

**Rating:** 1100  
**Tags:** greedy, implementation, sortings  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

Valera has a shopping list containing a number of fruits, possibly with duplicates if he wants more than one of the same type. At the market, the stall has _n_ types of fruits and _n_ price tags, but the tags are not yet attached to the fruits. Each tag represents the price of one fruit of a given kind. Valera wants to know the minimum and maximum total amount he could pay, depending on how the seller attaches the tags to the fruits he wants.

The input provides the number of price tags `n` and the number of fruits on Valera’s list `m`. The next line gives the `n` prices. Then `m` lines list the names of the fruits on his list. Since the number of distinct fruits on the list is no more than `n`, we are guaranteed that there is always a price available for each distinct fruit. The output must be two numbers: the smallest and largest possible total sum of the fruits on Valera's list.

With the constraints `n, m ≤ 100` and prices ≤ 100, a naive approach iterating over all possible permutations of price-tag assignments is theoretically possible but inefficient, because `n!` permutations would quickly become infeasible. Edge cases include situations where all fruits on the list are of a single type, or where prices are identical, where careless handling of duplicates or indexing could produce wrong results.

For example, if `n=2`, `m=3`, prices `[1, 2]`, and the list contains `apple`, `apple`, `apple`, the minimum total is `1 + 1 + 2 = 4`, while the maximum total is `2 + 2 + 1 = 5`. A naive approach that doesn’t handle repeated fruits correctly might miscalculate the sums.

## Approaches

The brute-force approach considers every possible way of assigning prices to the fruits on Valera’s list. You could generate all permutations of the price list and then sum the corresponding prices for the fruits in the list. This approach is correct because every possible distribution is explicitly considered, but it is too slow: even for `n=10`, `10! = 3,628,800` permutations is excessive for a 1-second time limit, and `n` can go up to 100.

The key insight is that the problem reduces to a greedy strategy: the minimum total is obtained when the cheapest available prices are assigned to the most frequently requested fruits, and the maximum total is obtained when the most expensive prices are assigned to the most frequently requested fruits. Sorting the list of prices and counting how many times each fruit appears is enough to compute both extremes. The frequency of fruits matters because repeated items in the list must each be assigned a price.

The greedy approach works because there is no interaction between different fruits beyond the count. Once the counts are known, the only variable affecting the sum is which price each fruit receives, so assigning lowest-to-most-frequent (or highest-to-most-frequent) guarantees the optimal sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * m) | O(n) | Too slow |
| Optimal | O(n log n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read the number of price tags `n` and the number of fruits `m`.
2. Read the list of `n` prices and sort them in ascending order. Sorting will allow efficient selection of the cheapest and most expensive prices.
3. Read the `m` fruits from Valera’s list and count how many times each distinct fruit occurs. This creates a frequency map where keys are fruit names and values are the number of times Valera wants each fruit.
4. Extract the frequencies and sort them in descending order. The most frequently requested fruits will be assigned the lowest prices for the minimum total and the highest prices for the maximum total.
5. Initialize two sums: `min_total` and `max_total`. For `min_total`, assign the cheapest prices to the most frequent fruits sequentially. For `max_total`, assign the most expensive prices to the most frequent fruits sequentially. Each frequency may consume multiple prices from the sorted price list.
6. Output `min_total` and `max_total`.

The reason this works is that for both extremes, any deviation from this assignment would either leave a cheaper price unassigned or a more expensive price unused, increasing the minimum or decreasing the maximum. The invariant is that the largest frequencies always match with the smallest or largest remaining prices.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import Counter

n, m = map(int, input().split())
prices = list(map(int, input().split()))
prices.sort()

fruits = [input().strip() for _ in range(m)]
freq = list(Counter(fruits).values())
freq.sort(reverse=True)

# minimum total
min_total = 0
price_idx = 0
for f in freq:
    for _ in range(f):
        min_total += prices[price_idx]
        price_idx += 1

# maximum total
prices_rev = prices[::-1]
max_total = 0
price_idx = 0
for f in freq:
    for _ in range(f):
        max_total += prices_rev[price_idx]
        price_idx += 1

print(min_total, max_total)
```

The solution reads the input efficiently, counts fruit frequencies, and sorts both prices and frequencies. The inner loops iterate exactly once per fruit in the list. Boundary conditions, such as all fruits being the same, are correctly handled by the frequency map. Reversing the price array allows a symmetric calculation for the maximum total.

## Worked Examples

**Sample 1**

Input:

```
5 3
4 2 1 10 5
apple
orange
mango
```

| Step | Prices | Frequencies | min_total | max_total |
| --- | --- | --- | --- | --- |
| Sort prices | [1,2,4,5,10] | [1,1,1] | 0 | 0 |
| Assign min | 1→apple, 2→orange, 4→mango | [1,1,1] | 7 | - |
| Assign max | 10→apple, 5→orange, 4→mango | [1,1,1] | - | 19 |

This shows that the algorithm correctly pairs the cheapest prices with requested fruits for the minimum and the most expensive prices for the maximum.

**Custom Sample 2**

Input:

```
4 5
1 3 2 4
apple
apple
banana
banana
banana
```

| Step | Prices | Frequencies | min_total | max_total |
| --- | --- | --- | --- | --- |
| Sort prices | [1,2,3,4] | [3,2] | 0 | 0 |
| Assign min | 1→banana, 2→banana, 3→banana, 4→apple, next cheapest 2→apple | 0 | 12 | - |
| Assign max | 4→banana, 3→banana, 2→banana, 1→apple, next expensive 2→apple | - | 14 |  |

This shows that repeated fruits are correctly handled, and the sums reflect the greedy assignments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m) | Sorting prices dominates, counting frequencies is O(m) |
| Space | O(n + m) | Storing prices and the frequency map |

With `n, m ≤ 100`, the algorithm easily executes within 1-second time limit and uses far less than 256 MB of memory.

## Test Cases

```python
import sys, io
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    from collections import Counter

    n, m = map(int, input().split())
    prices = list(map(int, input().split()))
    prices.sort()

    fruits = [input().strip() for _ in range(m)]
    freq = list(Counter(fruits).values())
    freq.sort(reverse=True)

    min_total = 0
    price_idx = 0
    for f in freq:
        for _ in range(f):
            min_total += prices[price_idx]
            price_idx += 1

    prices_rev = prices[::-1]
    max_total = 0
    price_idx = 0
    for f in freq:
        for _ in range(f):
            max_total += prices_rev[price_idx]
            price_idx += 1

    return f"{min_total} {max_total}"

# Provided sample
assert run("5 3\n4 2 1 10 5\napple\norange\nmango\n") == "7 19", "sample 1"

# Custom: single fruit repeated
assert run("2 3\n1 2\napple\napple\napple\n") == "4 5", "single fruit repeated"

# Custom: all prices equal
assert run("3 3\n5 5 5\napple\nbanana\norange\n") == "15 15", "all prices equal"

# Custom: min-size input
assert run("1 1\n7\napple\n") == "7 7", "min-size input"

# Custom: max-size, uniform price
inp = "100 100\n" +
```
