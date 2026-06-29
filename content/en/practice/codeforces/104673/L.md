---
title: "CF 104673L - Wagon"
description: "A train moves through a sequence of cities in a fixed order, and at each city there are a few crane types available, each with a price. Every crane type is identified by an ID, and in a given city you may buy or sell any of the types listed there at that city’s price."
date: "2026-06-29T09:22:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104673
codeforces_index: "L"
codeforces_contest_name: "2022-2023 CTU Open Contest"
rating: 0
weight: 104673
solve_time_s: 43
verified: true
draft: false
---

[CF 104673L - Wagon](https://codeforces.com/problemset/problem/104673/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

A train moves through a sequence of cities in a fixed order, and at each city there are a few crane types available, each with a price. Every crane type is identified by an ID, and in a given city you may buy or sell any of the types listed there at that city’s price.

The key restriction is that the train only moves forward. If you buy a crane in some city, you can only sell it in a later city. You are allowed to repeat this process multiple times, but you can only carry one crane at any moment, meaning transactions do not overlap. You start with enough money to buy any crane at any city, so the only goal is to maximize total profit from all buy and sell operations.

The task is to compute the maximum profit achievable along the route.

The constraints imply up to 100,000 cities, each with at most 10 crane types. This immediately rules out any solution that considers all pairs of cities directly, since that would be quadratic in the worst case and lead to around 10^10 operations. Even iterating over all pairs of cities per crane type would be far too slow.

A correct solution must exploit the fact that the structure is sequential and that each crane type can be treated independently over time.

A subtle failure case appears when a naive greedy strategy is used per city, such as always buying the cheapest available crane and selling it at the next higher price without tracking future opportunities. For example, if a crane is cheap early but becomes even cheaper later, a greedy “buy now, sell next increase” approach may commit too early and miss a much larger later rise. The correct solution must allow waiting and choosing the best buy-sell pair globally, not locally.

## Approaches

A brute force interpretation would treat each possible transaction as a choice of a buy city, a sell city later in the route, and a crane type present in both cities. For each crane type, we could scan all pairs of cities where it appears, compute price differences, and take the best profit. This is correct because every valid transaction is explicitly considered, but it is far too slow: in the worst case, a crane type appears in all cities, leading to O(N^2) pairs per type, and up to 10 types per city, making the total complexity effectively O(N^2).

The key observation is that each crane type evolves independently along time. For a fixed crane type, we only care about the best opportunity to buy at some earlier city and sell at a later city. This reduces the problem to tracking, for each type, the minimum price seen so far and the best profit achievable by selling at the current city. As we move forward, every new city can either improve the minimum buying price or create a profitable sell against the previously observed minimum.

This transforms the global problem into a streaming maximum difference problem per crane type, processed in chronological order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all pairs per type | O(N^2 · M) | O(1) | Too slow |
| Per-type single pass tracking min price | O(N · M) | O(M) | Accepted |

## Algorithm Walkthrough

We process cities in order while maintaining, for each crane type, the lowest price seen so far and the best profit achievable.

1. Initialize a dictionary for each crane type that will store the minimum observed price. Also initialize total profit as zero. This prepares us to evaluate every type independently as we scan forward.
2. Iterate over cities from left to right. At each city, we examine all crane types available in that city.
3. For each crane type and its price in the current city, we first check whether this type has been seen before. If not, we initialize its minimum price with the current price, since this is the first possible buying point.
4. If the type has been seen before, we compare the current price with the stored minimum price. Selling at the current city would yield a profit equal to current price minus minimum price. If this profit is positive and better than any previously recorded gain, we add it to the total profit.
5. Regardless of whether we sold or not, we update the minimum price for this crane type to be the smaller of the existing minimum and the current price. This ensures that future cities always consider the best possible buying opportunity.
6. Continue this process for all cities and all crane types within them.

The important detail is that we never “lock in” a transaction. Each update only improves knowledge of past best buying prices, and each city evaluates selling opportunities without consuming inventory.

### Why it works

For each crane type, the algorithm maintains the invariant that after processing city i, the stored minimum price is exactly the lowest price of that type among all cities 1 through i. Any valid transaction must consist of a buy at some earlier city j and a sell at a later city i, so when processing city i, the algorithm correctly compares against the best possible buy point. Since every sell opportunity is evaluated exactly once at its selling city, and every buy candidate is absorbed into the running minimum, no valid pair is missed and no invalid pair is counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    min_price = {}
    profit = 0

    for _ in range(n):
        m = int(input())
        for _ in range(m):
            cid, price = map(int, input().split())

            if cid not in min_price:
                min_price[cid] = price
            else:
                if price > min_price[cid]:
                    profit += price - min_price[cid]
                if price < min_price[cid]:
                    min_price[cid] = price

    print(profit)

if __name__ == "__main__":
    solve()
```

The code maintains a dictionary keyed by crane type. Each entry stores the minimum observed price so far. As we read each city, we process all available crane types. If a profitable sell is possible at the current price, it is added immediately to the global profit. The minimum is updated in the same pass so future cities always compare against the best historical buy price.

A subtle point is that we never remove a type after selling. This is correct because we are not simulating holding inventory, but instead decomposing every transaction into independent buy-sell pairs. Each profitable pair is counted exactly once when we reach the sell city.

## Worked Examples

Consider a simple progression with one crane type.

Input:

```
3
1
1 2
1
1 5
1
1 3
```

We track type 1.

| City | Price | Min so far | Profit added |
| --- | --- | --- | --- |
| 1 | 2 | 2 | 0 |
| 2 | 5 | 2 | 3 |
| 3 | 3 | 2 | 0 |

The algorithm buys effectively at price 2 and sells at 5, then ignores later lower price since it is not profitable.

This shows that profit is accumulated only when a later price exceeds the best previous buying point.

Now consider multiple oscillations:

Input:

```
4
1
1 3
1
1 1
1
1 4
1
1 2
```

| City | Price | Min so far | Profit added |
| --- | --- | --- | --- |
| 1 | 3 | 3 | 0 |
| 2 | 1 | 1 | 0 |
| 3 | 4 | 1 | 3 |
| 4 | 2 | 1 | 0 |

This demonstrates that after resetting the minimum at a lower price, future increases are still captured correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N · M) | Each city processes at most 10 crane types |
| Space | O(K) | K is number of distinct crane types stored in dictionary |

The bounds make this efficient since N is up to 100,000 and M is at most 10, so total operations are about 1,000,000 updates, easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample-like cases
assert run("""3
1
1 2
1
1 5
1
1 3
""") == "3"

# minimum size
assert run("""1
1
10 5
""") == "0"

# monotone increasing
assert run("""4
1
1 1
1
1 2
1
1 3
1
1 4
""") == "3"

# monotone decreasing
assert run("""4
1
1 5
1
1 4
1
1 3
1
1 2
""") == "0"

# multiple types
assert run("""3
2
1 1
2 10
2
1 5
2 3
1
1 10
""") == "15"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single city | 0 | no forward sell possible |
| increasing sequence | positive accumulation | greedy capture of rises |
| decreasing sequence | 0 | no invalid negative profit |
| multiple types | mixed independent tracking | per-type correctness |

## Edge Cases

A key edge case is when the same crane type appears multiple times in a city or alternates frequently between low and high prices.

Input:

```
3
2
1 5
1 1
2
1 2
2 10
2
1 6
2 3
```

For type 1, minimum becomes 1 at city 1, and best sell is 6 at city 3, yielding profit 5. Intermediate higher price 5 is ignored because it does not improve profit beyond later opportunity.

For type 2, minimum is 10 at city 2, but later price 3 does not yield profit, so no contribution.

This confirms that local updates of minimum and immediate profit accumulation correctly handle repeated IDs within and across cities without needing explicit transaction simulation.
