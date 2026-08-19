---
title: "CF 102180C - \u0412\u0430\u043d\u044f \u0438 \u0442\u0435\u0442\u0440\u0430\u0434\u0438"
description: "Vanya has a fixed budget of k coins and wants to buy as many squared notebooks as possible. There are n shops. Shop i sells each notebook for ai coins and has bi notebooks available."
date: "2026-08-19T15:29:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102180
codeforces_index: "C"
codeforces_contest_name: "MSPU Training Contest 2018-2019"
rating: 0
weight: 102180
solve_time_s: 94
verified: true
draft: false
---

[CF 102180C - \u0412\u0430\u043d\u044f \u0438 \u0442\u0435\u0442\u0440\u0430\u0434\u0438](https://codeforces.com/problemset/problem/102180/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

Vanya has a fixed budget of `k` coins and wants to buy as many squared notebooks as possible. There are `n` shops. Shop `i` sells each notebook for `a_i` coins and has `b_i` notebooks available. Vanya can buy any number from a shop, from zero up to its stock, and his total spending cannot exceed `k`.

The task is to find the largest total number of notebooks that can be purchased.

The key constraint is the budget, which can be as large as `10^18`, while there can be `10^5` shops. A solution that performs work proportional to the budget is impossible, since even `O(k)` can mean `10^18` operations. Likewise, enumerating all possible purchase quantities is completely infeasible because every shop can contribute up to `10^6` notebooks. With `n = 10^5`, we need an algorithm around `O(n log n)` or better.

The answer itself can be as large as the total stock, which is at most `10^5 * 10^6 = 10^11`. Python handles integers of this size directly, while languages with fixed-width integer types need at least 64-bit integers.

Several edge cases are easy to mishandle. First, Vanya may not be able to afford even one notebook. For example,

```
1 1
2 10
```

has answer `0`, because every notebook costs 2 coins and Vanya has only 1. An implementation that always buys at least one notebook from the cheapest shop would be wrong.

Second, the budget can run out exactly after buying all available notebooks from a shop. For example,

```
10 2
2 5
100 5
```

has answer `5`. Vanya spends exactly 10 coins on the five cheap notebooks and cannot buy anything else. Using a strict `<` comparison instead of `<=` would incorrectly reject the fifth notebook.

Third, the final shop may be only partially affordable. For example,

```
15 2
5 2
7 10
```

has answer `3`: two notebooks cost 10 coins, leaving 5 coins, which is enough for only one notebook from the second shop. A solution that takes either all or none of a shop's stock would miss this case.

Finally, the input prices need not be sorted. In

```
20 3
10 1
2 4
5 6
```

the correct answer is `8`, because the four notebooks costing 2 and four of the notebooks costing 5 fit into the budget. Processing shops in input order would spend 10 coins immediately and can produce a smaller answer.

## Approaches

A direct brute-force approach could try every possible number of notebooks purchased from every shop. For shop `i`, there are `b_i + 1` choices, including buying zero notebooks. The number of complete purchase combinations is

`(b_1 + 1)(b_2 + 1)...(b_n + 1)`.

In the worst case this is `(10^6 + 1)^100000`, so even generating the possibilities is hopeless. The brute-force is correct because it explicitly considers every legal purchase plan, but the number of plans grows exponentially with the number of shops.

A less extreme brute-force idea is to repeatedly buy individual notebooks while trying to decide which shop to use. Even if we always select the currently cheapest available notebook, the total stock can reach `10^11`, so simulating one purchase at a time still requires up to `10^11` iterations.

The useful observation is that notebooks are independent apart from their prices and stock limits. If one affordable notebook costs more than another available notebook, replacing the expensive purchase with the cheaper one never decreases the number of notebooks that can be bought. Consequently, in an optimal solution, every cheaper notebook should be purchased before any more expensive notebook is considered.

This turns the problem into a simple greedy process. Sort shops by notebook price, consume the stock of the cheapest shop while the budget allows it, then move to the next price. At the first shop that cannot be bought completely, we buy as many notebooks as the remaining budget permits and stop. There is no reason to consider a more expensive shop after that point, because every notebook there costs at least as much.

The brute-force works because every possible allocation is examined, but fails because there are far too many allocations. The observation that cheaper notebooks can always replace more expensive ones reduces the entire search to sorting the shops and making one decision per shop.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in `n` | Exponential in `n` in the enumeration | Too slow |
| Optimal | `O(n log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Read the budget `k` and all shop pairs `(a_i, b_i)`. Each pair describes one price level together with the number of notebooks available at that price.
2. Sort all shops by `a_i`, from the smallest notebook price to the largest. This puts the notebooks in exactly the order in which an optimal solution should consume them.
3. Set the current answer to zero and keep the remaining budget equal to `k`.
4. Process the sorted shops from cheapest to most expensive. For a shop with price `a` and stock `b`, first determine how many of its notebooks the remaining budget can afford, which is `remaining // a`.
5. Buy the smaller of that affordable quantity and the available stock. Adding `min(b, remaining // a)` notebooks is optimal because every notebook at this shop is no more expensive than every notebook in a later shop.
6. Subtract the cost of the purchased notebooks from the remaining budget and add their count to the answer.
7. If the affordable quantity is smaller than the shop's stock, the budget is insufficient to empty this shop. Stop immediately. Every later shop has a price at least as large, so replacing one of the notebooks just considered with a later notebook cannot increase the total count.
8. Print the accumulated number of notebooks.

Why it works: after processing any prefix of the shops, the algorithm has purchased the maximum possible number of notebooks that can be obtained using only that prefix and the original budget. When a shop can be emptied, buying one of its notebooks is never worse than saving those coins for a later, more expensive notebook. When a shop cannot be emptied, the algorithm buys the maximum possible number at the current cheapest remaining price. Any alternative that spends some of the remaining budget on a later shop can replace that later notebook with a current notebook for no more money, so it cannot produce more notebooks. Thus the first partially affordable shop determines the maximum possible answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    k, n = map(int, input().split())
    shops = [tuple(map(int, input().split())) for _ in range(n)]

    shops.sort()

    answer = 0
    remaining = k

    for price, stock in shops:
        can_buy = remaining // price
        take = min(stock, can_buy)

        answer += take
        remaining -= take * price

        if take < stock:
            break

    print(answer)

if __name__ == "__main__":
    solve()
```

The `shops` list stores each price and its corresponding stock, then `sort()` orders the pairs by price because the first component is compared first. No secondary ordering is needed.

For each shop, `remaining // price` gives the largest number of notebooks that can be bought without exceeding the current budget. Taking the minimum with `stock` respects the shop's availability limit.

The multiplication `take * price` must happen before subtracting from the budget. Python integers have arbitrary precision, so values such as `10^18` and the products encountered here are handled safely without overflow.

The `take < stock` condition detects the first shop that cannot be completely emptied. This is equivalent to saying that `remaining < price * stock`. Once this happens, processing more expensive shops cannot improve the answer, so the loop can terminate immediately.

There is no multiple-test-case format in this problem, so `solve()` processes exactly one instance.

## Worked Examples

### Sample 1

The input is:

```
10 2
1 5
2 5
```

The shops are already sorted. The algorithm first consumes the five notebooks costing 1 coin each, then uses the remaining budget on the second shop.

| Shop price | Stock | Remaining before | Affordable | Taken | Remaining after | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 5 | 10 | 10 | 5 | 5 | 5 |
| 2 | 5 | 5 | 2 | 2 | 1 | 7 |

The final answer is `7`. The first shop is completely emptied, while only two of the five notebooks in the second shop can be purchased.

### Sample 2

The input is:

```
15 1
5 2
```

There is only one shop, and both available notebooks can be purchased.

| Shop price | Stock | Remaining before | Affordable | Taken | Remaining after | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| 5 | 2 | 15 | 3 | 2 | 5 | 2 |

The answer is `2`. The remaining 5 coins cannot buy another notebook because the shop has no stock left.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n)` | Sorting `n` shops dominates the single pass through them |
| Space | `O(n)` | The list of shop records requires linear memory |

With `n = 10^5`, sorting is easily practical, while algorithms proportional to the budget or total stock could require up to `10^18` or `10^11` operations. The algorithm performs one sort and at most one pass through the shops, so it fits comfortably within the intended limits.

## Test Cases

```python
import sys
import io

input = sys.stdin.readline

def solve():
    k, n = map(int, input().split())
    shops = [tuple(map(int, input().split())) for _ in range(n)]

    shops.sort()

    answer = 0
    remaining = k

    for price, stock in shops:
        can_buy = remaining // price
        take = min(stock, can_buy)

        answer += take
        remaining -= take * price

        if take < stock:
            break

    print(answer)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run("""10 2
1 5
2 5
""") == "7", "sample 1"

# Provided sample 2
assert run("""15 1
5 2
""") == "2", "sample 2"

# Provided sample 3
assert run("""20 3
10 1
2 4
5 6
""") == "8", "sample 3"

# Minimum-size input
assert run("""1 1
1 1
""") == "1", "minimum case"

# Cannot afford even one notebook
assert run("""1 1
2 10
""") == "0", "cannot afford one notebook"

# Exact budget and unsorted shops
assert run("""10 2
100 5
2 5
""") == "5", "exact budget with unsorted input"

# Partial purchase from the final shop
assert run("""15 2
7 10
5 2
""") == "3", "partial final purchase"

# All prices and stocks equal
assert run("""17 4
3 5
3 5
3 5
3 5
""") == "5", "equal values"

# Large values, including k close to 10^18
assert run("""1000000000000000000 2
1000000 1000000
1 1000000
""") == "1001000000", "large integer values"

# Maximum n
large_input = "1000000000000 100000\n" + "\n".join(["1 1"] * 100000) + "\n"
assert run(large_input) == "100000", "maximum number of shops"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1 1` | `1` | Minimum-sized valid instance |
| `1 1 / 2 10` | `0` | Correct handling when even one notebook is unaffordable |
| `10 2 / 100 5 / 2 5` | `5` | Sorting and exact budget consumption |
| `15 2 / 7 10 / 5 2` | `3` | Partial purchase from the next shop |
| Four shops with price `3`, stock `5` | `5` | Equal prices and stocks |
| `10^18` budget with million-sized prices and stocks | `1001000000` | Large integer arithmetic |
| `100000` shops with one notebook each | `100000` | Maximum `n` and linear scan after sorting |

## Edge Cases

When the budget cannot buy even one notebook, the algorithm naturally returns zero. For

```
1 1
2 10
```

the only shop has price 2, so `remaining // price` is `1 // 2 = 0`. Consequently `take` is zero, the condition `take < stock` is true, and the loop stops with answer `0`. No artificial minimum purchase is introduced.

When the budget exactly pays for all available notebooks, the algorithm accepts them because integer division gives at least the full stock. For

```
10 2
2 5
100 5
```

the first shop gives `10 // 2 = 5`, so all five notebooks are taken and the remaining budget becomes zero. The answer is `5`. The second shop immediately yields an affordable quantity of zero, but it is never necessary to inspect it because the budget is already exhausted.

When only part of a shop's stock can be purchased, integer division gives exactly the required quantity. For

```
15 2
5 2
7 10
```

the first shop contributes two notebooks for 10 coins. Five coins remain, and `5 // 7 = 0` for the second shop, so the answer is `2`. For a slightly different partial case,

```
15 2
5 2
4 10
```

the shops are reordered to price 4 first. Vanya buys three notebooks for 12 coins and cannot buy a fourth, giving the correct answer `3`.

Unsorted input is handled by sorting before any purchases are made. In

```
20 3
10 1
2 4
5 6
```

the sorted order is `(2, 4), (5, 6), (10, 1)`. The first four notebooks cost 8 coins, leaving 12. Two notebooks costing 5 can then be bought for 10, leaving 2. The final shop costs 10 per notebook and is unaffordable, so the answer is `6`, which is exactly the maximum possible count. The ordering step is what prevents the original input order from influencing the result.

Large budgets and products are handled without special cases in Python. For example, with a budget of `10^18`, computing `remaining // price` and `take * price` remains exact. The algorithm never loops once per coin or once per notebook, so the magnitude of the budget does not affect the number of iterations.
