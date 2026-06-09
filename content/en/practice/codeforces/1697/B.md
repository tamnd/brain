---
title: "CF 1697B - Promo"
description: "We have a store with n items, each with a specific price. The store runs a promotion where, if a customer buys at least x items, the y cheapest among those items are free. For each query (x, y), we want to determine the maximum total value of items a customer can get for free."
date: "2026-06-09T22:25:36+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1697
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 130 (Rated for Div. 2)"
rating: 900
weight: 1697
solve_time_s: 126
verified: true
draft: false
---

[CF 1697B - Promo](https://codeforces.com/problemset/problem/1697/B)

**Rating:** 900  
**Tags:** greedy, sortings  
**Solve time:** 2m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a store with `n` items, each with a specific price. The store runs a promotion where, if a customer buys at least `x` items, the `y` cheapest among those items are free. For each query `(x, y)`, we want to determine the maximum total value of items a customer can get for free.

The input gives the item prices as an array `p` of size `n` and then `q` independent queries. Each query specifies the promotion parameters `(x, y)`, and the output is a single integer for each query: the maximum sum of the cheapest `y` items among any selection of `x` items.

The main constraints are that `n` and `q` can be up to 200,000, and item prices can go up to one million. A naive approach that iterates over all subsets of size `x` is impossible since the number of subsets grows combinatorially. Even iterating over all possible `x`-item selections explicitly would exceed `10^10` operations in the worst case. We need a solution that works in near-linear time with respect to `n`, ideally `O(n log n)` plus `O(1)` per query.

Non-obvious edge cases include when all items have the same price, when `x` equals `n` forcing the customer to buy everything, or when `y` equals `x` so every selected item is free. For example, if the prices are `[5, 5, 5]` and the query is `(3, 3)`, the free value is `15`. A careless approach that always tries to pick the globally cheapest items might miscompute the sum for other `x` values.

## Approaches

The brute-force approach would be to generate all possible subsets of size `x` for a query, sort each subset, take the `y` cheapest items, and sum their prices. This works logically but is prohibitively expensive. Even for moderate `n = 20`, there are over 100,000 subsets to consider, and `n = 2 * 10^5` is completely intractable.

The key observation is that to maximize the value of the `y` free items, we want to select the `x` most expensive items possible, because the `y` cheapest among them will still be higher in value than cheaper items outside the selection. Sorting the full array in descending order allows us to pick the first `x` items quickly. Then, among those `x` items, the `y` cheapest can be summed using a prefix sum array. This reduces the problem to a single sorting operation plus simple arithmetic per query.

This greedy insight is correct because the free items are always taken from the selected `x`, so maximizing the total sum of the free items is equivalent to taking the most expensive `x` and summing their `y` cheapest.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n choose x * x log x) | O(x) per query | Too slow |
| Optimal | O(n log n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of items `n` and the number of queries `q`. Read the item prices into an array `p`.
2. Sort `p` in descending order. This ensures the first `x` elements of `p` for any query `(x, y)` are the most expensive selection.
3. Build a prefix sum array `prefix` where `prefix[i]` is the sum of the first `i` elements of `p`. This allows fast computation of sums over any contiguous segment.
4. For each query `(x, y)`, the `x` most expensive items are the first `x` elements of `p`. Among these, the `y` cheapest are the last `y` elements in this segment. Compute their sum as `prefix[x] - prefix[x-y]`.
5. Output the sum for each query.

Why it works: Sorting guarantees that any `x`-sized selection that maximizes the free items' sum is the first `x` elements. Prefix sums allow constant-time calculation of the `y` cheapest within that selection. The algorithm never selects a suboptimal set because moving any more expensive item outside the first `x` would reduce the sum of the free items.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, q = map(int, input().split())
p = list(map(int, input().split()))

p.sort(reverse=True)

# prefix[i] = sum of first i elements
prefix = [0] * (n + 1)
for i in range(n):
    prefix[i + 1] = prefix[i] + p[i]

for _ in range(q):
    x, y = map(int, input().split())
    # sum of y cheapest in first x items
    print(prefix[x] - prefix[x - y])
```

The code first sorts the prices in descending order to ensure we can always pick the most expensive `x` items. The prefix sum array allows us to compute sums of contiguous segments in constant time. The subtle point is the indexing in `prefix[x] - prefix[x - y]`: `prefix[x]` sums the first `x` items, and subtracting `prefix[x - y]` removes the sum of the more expensive `x-y` items, leaving only the `y` cheapest.

## Worked Examples

**Sample Input 1**

| Step | Sorted Prices | Prefix | x | y | Sum |
| --- | --- | --- | --- | --- | --- |
| Query 1 | [5,5,3,2,1] | [0,5,10,13,15,16] | 3 | 2 | 13-5=8 |
| Query 2 | [5,5,3,2,1] | same | 1 | 1 | 5-0=5 |
| Query 3 | [5,5,3,2,1] | same | 5 | 3 | 16-10=6 |

This demonstrates that sorting plus prefix sums allows us to pick the `x` items and sum the `y` cheapest in O(1) per query.

**Edge Case Example**

Prices `[1,1,1]`, query `(3,3)`. Sorted prices `[1,1,1]`, prefix `[0,1,2,3]`. Sum of last 3 of first 3 is `3-0=3`. This confirms the algorithm handles `y=x` correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + q) | Sorting takes O(n log n), each query is O(1) using prefix sums |
| Space | O(n) | Prefix array of size n+1 |

For the constraints `n, q ≤ 2 * 10^5`, sorting dominates and fits comfortably within 2 seconds. Memory usage is linear in `n`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())  # or paste solution here
    return output.getvalue().strip()

# Provided samples
assert run("5 3\n5 3 1 5 2\n3 2\n1 1\n5 3\n") == "8\n5\n6", "sample 1"

# Minimum size input
assert run("1 1\n10\n1 1\n") == "10", "min size"

# All equal values
assert run("4 2\n5 5 5 5\n2 1\n4 2\n") == "5\n10", "all equal"

# Maximum x
assert run("5 1\n1 2 3 4 5\n5 2\n") == "3", "x=n"

# Random large case
import random
n = 10
prices = " ".join(str(random.randint(1,10)) for _ in range(n))
assert run(f"{n} 1\n{prices}\n{n} 3\n")  # just ensure no crash
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "1 1\n10\n1 1" | "10" | Minimum-size input |
| "4 2\n5 5 5 5\n2 1\n4 2" | "5\n10" | All equal prices, multiple queries |
| "5 1\n1 2 3 4 5\n5 2" | "3" | x equals n |
| Random 10-item case | varies | Large random input, checks no crash |

## Edge Cases

If all prices are equal, the algorithm still correctly sums the `y` cheapest, since `prefix[x] - prefix[x-y]` works regardless of equality. For `y=x`, the sum of all first `x` items is computed correctly. If `y=1`, it still picks the last of the first `x` items after sorting, ensuring the minimum of that segment. This handles all subtle boundaries without special-casing.
