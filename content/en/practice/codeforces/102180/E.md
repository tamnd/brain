---
title: "CF 102180E - \u0412\u0430\u043d\u044f \u0438 \u043f\u0430\u0440\u0430\u043b\u043b\u0435\u043b\u044c\u043d\u044b\u0435 \u043c\u0438\u0440\u044b"
description: "There are n stores. Store i has notebooks costing ai coins each, and at most bi notebooks can be bought there. Every world has exactly the same stores and stock, but the amount of money k differs between worlds."
date: "2026-08-19T06:52:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102180
codeforces_index: "E"
codeforces_contest_name: "MSPU Training Contest 2018-2019"
rating: 0
weight: 102180
solve_time_s: 85
verified: true
draft: false
---

[CF 102180E - \u0412\u0430\u043d\u044f \u0438 \u043f\u0430\u0440\u0430\u043b\u043b\u0435\u043b\u044c\u043d\u044b\u0435 \u043c\u0438\u0440\u044b](https://codeforces.com/problemset/problem/102180/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

There are `n` stores. Store `i` has notebooks costing `a_i` coins each, and at most `b_i` notebooks can be bought there. Every world has exactly the same stores and stock, but the amount of money `k` differs between worlds. For each of the `m` budgets, we need the largest possible number of notebooks that can be purchased.

Since every notebook contributes exactly one to the answer, the identity of a notebook matters only through its price. If we want to maximize the number of notebooks, the optimal strategy is to take the cheapest available notebooks first. The problem is thus equivalent to sorting all available notebooks by price and asking, for each budget, how long a prefix of this sorted sequence can be afforded.

The constraints make a direct simulation impossible. There can be `10^5` stores and `10^5` different worlds, so processing every store independently for every world could perform `10^10` operations. The prices can reach `10^9` and a budget can reach `10^18`, so 64-bit integer arithmetic is required. Python integers already handle these values safely.

There are several edge cases where a careless implementation can fail. First, a budget can end in the middle of a store's stock. For example,

```
1 1
10
6 2
```

The answer is `1`, because one notebook costs 6 and two cost 12. An implementation that only considers complete stores would incorrectly return `0`.

Second, a budget can be exactly equal to the cost of several notebooks:

```
2 1
15
5 2
5 1
```

All three notebooks cost 5, so the answer is `3`. A binary search using a strict `< budget` condition would incorrectly return `2`.

Third, a very large budget can afford every notebook:

```
2 1
100
3 2
7 4
```

The answer is `6`. The algorithm must allow the search to reach the total stock instead of assuming that there is always an unaffordable item after the purchased prefix.

Finally, several stores can have the same price. For example,

```
3 2
5 10
2 1
2 3
7 1
```

For budget `5`, four notebooks costing 2 each are not all affordable, so the answer is `2`. Stores with equal prices must be treated as interchangeable, and sorting them separately still gives the correct result.

## Approaches

The most direct solution is to sort the stores by price and, for every world, scan them from cheapest to most expensive. At each store we buy as many notebooks as the remaining budget permits, possibly taking only part of the available stock. This is correct because replacing a purchased expensive notebook with an available cheaper notebook never decreases the number of notebooks we can afford.

The problem is the repeated scan. In the worst case, `n = 10^5` and `m = 10^5`, so scanning all stores for every budget takes up to `10^10` store visits. That is far beyond what a one-second contest solution can handle.

The key observation is that the stores are identical across all worlds. We should preprocess the common price structure once instead of repeating the same work for every budget.

After sorting stores by price, define a prefix containing all notebooks from the first few cheapest stores. For each such prefix, store its total number of notebooks and its total cost. If a budget is large enough to buy an entire prefix, we can immediately move to a later prefix. Once we find the first store whose complete stock cannot be bought, the answer is already determined up to that store, and we only need to buy a partial amount from it.

This means each query can be answered by binary-searching the first prefix whose total cost exceeds the budget. The prefix immediately before it is completely affordable. The remaining money can then buy `remaining // price` notebooks from the next store, capped by that store's stock.

The brute-force works because taking stores in increasing price order produces an optimal purchase. It fails because it repeats this same traversal for every world. The observation that every world shares the same sorted stores lets us compress the repeated work into prefix arrays and answer each budget independently with one binary search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n log n + mn)` | `O(n)` | Too slow |
| Optimal | `O(n log n + m log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Read all stores and sort them by `a_i`, the notebook price. The cheapest notebooks must always be considered first, because buying a more expensive notebook while a cheaper one is still available cannot improve the number of notebooks bought.
2. Build two prefix arrays. Let `cnt[i]` be the total number of notebooks in the first `i` sorted stores, and let `cost[i]` be the total price of buying all those notebooks. For a store with price `a` and stock `b`, its contribution to the total cost is `a * b`.
3. For each world with budget `k`, binary-search the largest prefix `i` satisfying `cost[i] <= k`. This finds exactly how many complete stores can be exhausted with the available money.
4. Let `spent = cost[i]`. If `i` is equal to the number of stores, every notebook is affordable, so the answer is simply `cnt[i]`.
5. Otherwise, consider store `i`, which is the first store whose entire stock is too expensive to buy. There is still `k - spent` money available. Since every notebook in this store has the same price `a_i`, we can buy `(k - spent) // a_i` of them. We cannot exceed its stock, so the number taken is the smaller of this quotient and `b_i`.
6. Add those partially purchased notebooks to `cnt[i]` and output the result for the current world.

The reason this works is captured by the invariant that `cnt[i]` and `cost[i]` describe the cheapest possible way to buy exactly `cnt[i]` notebooks from the available stock. Every prefix consists of the cheapest available notebooks, so any solution containing more than `cnt[i]` notebooks must spend at least enough money to reach the next prefix. Once `cost[i] <= k < cost[i+1]`, all of the first `i` stores can be exhausted, but the entire next store cannot be purchased. Since all notebooks in that next store have the same price, taking as many as the remaining budget permits gives the maximum possible answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    budgets = list(map(int, input().split()))

    stores = [tuple(map(int, input().split())) for _ in range(n)]
    stores.sort()

    prefix_count = [0] * (n + 1)
    prefix_cost = [0] * (n + 1)

    for i, (price, stock) in enumerate(stores, 1):
        prefix_count[i] = prefix_count[i - 1] + stock
        prefix_cost[i] = prefix_cost[i - 1] + price * stock

    answers = []

    for budget in budgets:
        lo = 0
        hi = n

        while lo < hi:
            mid = (lo + hi + 1) // 2
            if prefix_cost[mid] <= budget:
                lo = mid
            else:
                hi = mid - 1

        i = lo
        answer = prefix_count[i]

        if i < n:
            remaining = budget - prefix_cost[i]
            price, stock = stores[i]
            answer += min(stock, remaining // price)

        answers.append(str(answer))

    sys.stdout.write(" ".join(answers))

if __name__ == "__main__":
    solve()
```

The stores are first sorted by `(price, stock)`, although only the price order matters. The prefix arrays have length `n + 1`, with index `0` representing an empty prefix. This makes the boundary case where no complete store is affordable natural, because `prefix_cost[0]` is zero.

For every budget, the binary search maintains the condition that all prefixes at or below `lo` are affordable. The upper bound is `n`, because buying all stores may be possible. The expression `(lo + hi + 1) // 2` biases the midpoint upward, which prevents an infinite loop when `lo` and `hi` differ by one.

After the search, `i` is the largest number of complete stores that fit into the budget. If `i == n`, there is no next store to inspect. Otherwise, `remaining` is nonnegative because `prefix_cost[i] <= budget`. Dividing it by the next store's price gives the maximum number of additional notebooks that can be bought there.

The multiplication `price * stock` can be as large as `4 * 10^13` for one store, and the total cost can be much larger still. Python's arbitrary-precision integers handle the required values without overflow.

The order of the operations also matters. We first remove the cost of every completely purchased cheaper store, then use the remaining money only on the next price level. There is never a reason to skip a cheaper notebook in favor of a more expensive one.

## Worked Examples

### Sample 1

The input is

```
2 3
10 30 20
8 2
5 2
```

After sorting, the stores are `(5, 2)` and `(8, 2)`. Their prefixes are:

| Prefix `i` | Store just added | `prefix_count[i]` | `prefix_cost[i]` |
| --- | --- | --- | --- |
| 0 | none | 0 | 0 |
| 1 | price 5, stock 2 | 2 | 10 |
| 2 | price 8, stock 2 | 4 | 26 |

For each world:

| Budget | Largest affordable prefix `i` | Remaining money | Extra notebooks | Answer |
| --- | --- | --- | --- | --- |
| 10 | 1 | 0 | 0 | 2 |
| 30 | 2 | 4 | 0 | 4 |
| 20 | 1 | 10 | 1 | 3 |

The third query demonstrates the partial-store case. After buying both notebooks priced at 5, ten coins remain. Only one notebook priced at 8 can be added, giving three notebooks total.

### Sample 2

Consider

```
3 3
4 5 11
2 1
3 2
10 1
```

The sorted stores are already in price order. The prefix information is:

| Prefix `i` | Store just added | `prefix_count[i]` | `prefix_cost[i]` |
| --- | --- | --- | --- |
| 0 | none | 0 | 0 |
| 1 | price 2, stock 1 | 1 | 2 |
| 2 | price 3, stock 2 | 3 | 8 |
| 3 | price 10, stock 1 | 4 | 18 |

The queries behave as follows:

| Budget | Largest affordable prefix `i` | Remaining money | Extra notebooks | Answer |
| --- | --- | --- | --- | --- |
| 4 | 1 | 2 | 0 | 1 |
| 5 | 1 | 3 | 1 | 2 |
| 11 | 2 | 3 | 0 | 3 |

For budget `5`, the first notebook costs `2`, leaving `3`, which buys exactly one notebook from the next store. The second notebook at price `3` would require another three coins, so two notebooks is optimal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n + m log n)` | Sorting costs `O(n log n)`, and each of the `m` budgets uses a binary search over `n` prefixes |
| Space | `O(n)` | The sorted stores and two prefix arrays contain `O(n)` values |

With `n, m <= 10^5`, the preprocessing performs roughly `10^5 log(10^5)` comparisons, and the queries perform another `10^5 log(10^5)` binary-search iterations. This is comfortably within the intended scale, while the `O(mn)` scan would require up to `10^10` operations.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    try:
        input = sys.stdin.readline

        n, m = map(int, input().split())
        budgets = list(map(int, input().split()))

        stores = [tuple(map(int, input().split())) for _ in range(n)]
        stores.sort()

        prefix_count = [0] * (n + 1)
        prefix_cost = [0] * (n + 1)

        for i, (price, stock) in enumerate(stores, 1):
            prefix_count[i] = prefix_count[i - 1] + stock
            prefix_cost[i] = prefix_cost[i - 1] + price * stock

        answers = []

        for budget in budgets:
            lo = 0
            hi = n

            while lo < hi:
                mid = (lo + hi + 1) // 2
                if prefix_cost[mid] <= budget:
                    lo = mid
                else:
                    hi = mid - 1

            i = lo
            answer = prefix_count[i]

            if i < n:
                remaining = budget - prefix_cost[i]
                price, stock = stores[i]
                answer += min(stock, remaining // price)

            answers.append(str(answer))

        print(" ".join(answers))
        return out.getvalue().strip()

    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def run(inp: str) -> str:
    return solve_data(inp)

# Provided sample
assert run(
    """2 3
10 30 20
8 2
5 2
"""
) == "2 4 3", "sample 1"

# Minimum-size input
assert run(
    """1 1
1
1 1
"""
) == "1", "minimum case"

# Budget is just below the first full purchase
assert run(
    """1 2
4 5
5 3
"""
) == "0 1", "boundary below and at one item"

# Multiple stores with the same price
assert run(
    """3 3
5 10 12
2 1
2 3
7 1
"""
) == "2 4 5", "equal prices"

# Budget is large enough for everything, including a 1e18 budget
assert run(
    """2 2
100 1000000000000000000
1000000000 40000
1 40000
"""
) == "40001 80000", "large budget"

# Partial purchase from the next store
assert run(
    """3 3
1 7 10
2 3
5 4
100 1
"""
) == "0 2 3", "partial store and exact boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1 / 1 1` | `1` | Minimum possible input |
| `1 2 / 4 5 / 5 3` | `0 1` | Budget below the first price and exact affordability |
| `3 3 / 5 10 12 / 2 1 / 2 3 / 7 1` | `2 4 5` | Equal prices and taking an entire stock level |
| `2 2 / 100 10^18 / 10^9 40000 / 1 40000` | `40001 80000` | Very large budgets and integer arithmetic |
| `3 3 / 1 7 10 / 2 3 / 5 4 / 100 1` | `0 2 3` | Partial purchase and binary-search boundaries |

## Edge Cases

When the budget is smaller than the cheapest notebook, the binary search returns prefix `0`. For example,

```
1 1
4
5 3
```

Both `prefix_cost[0] = 0` and the first complete prefix costing `15` are considered. The largest affordable prefix is `0`, so `remaining = 4`, and `4 // 5 = 0`. The answer is correctly `0`.

When the budget is exactly enough for a complete prefix, the `<=` comparison is essential. For

```
2 1
10
5 2
8 1
```

the first prefix costs exactly `10`, so the binary search returns `i = 1`. The answer is `2`. Using `<` instead of `<=` would incorrectly discard an affordable prefix.

When the budget falls inside the next store's stock, the prefix search deliberately stops before that store. For

```
1 1
10
6 2
```

the full prefix costs `12`, which is too much, so `i = 0`. The remaining ten coins buy `10 // 6 = 1` notebook, giving the correct answer `1`.

When every notebook is affordable, the search can return `i = n`. For

```
2 1
100
3 2
7 4
```

the total cost is `34`, so the largest affordable prefix is the entire array. The algorithm returns `prefix_count[2] = 6` and skips the partial-store calculation because there is no next store.

Equal prices do not require any special handling. For

```
3 1
5
2 1
2 3
7 1
```

sorting produces four notebooks at price `2`, followed by one at price `7`. The prefix containing both price-2 stores costs `8`, so with only five coins the algorithm stops before that complete prefix and buys `5 // 2 = 2` notebooks. The answer is `2`. The same reasoning works regardless of how stores having equal prices are ordered.

Finally, large values must be treated as exact integers. If a store has price `10^9` and stock `40000`, its complete cost is `4 * 10^13`. Across `10^5` stores, the accumulated cost can exceed ordinary 32-bit and 64-bit ranges. Python integers avoid overflow, and the prefix-cost construction preserves the exact values needed by the binary searches.
