---
title: "CF 441A - Valera and Antique Items"
description: "Valera wants to buy exactly one antique item from a set of sellers. Each seller offers multiple items with a current auction price. Valera can only secure a deal if he offers strictly more than the current price of an item, and he has a fixed budget v."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 441
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 252 (Div. 2)"
rating: 1000
weight: 441
solve_time_s: 81
verified: true
draft: false
---

[CF 441A - Valera and Antique Items](https://codeforces.com/problemset/problem/441/A)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

Valera wants to buy exactly one antique item from a set of sellers. Each seller offers multiple items with a current auction price. Valera can only secure a deal if he offers strictly more than the current price of an item, and he has a fixed budget `v`. The goal is to find all sellers from whom he can successfully buy at least one item.

The input provides the number of sellers `n` and Valera's budget `v`. For each seller, we receive the number of items they have and a list of their current prices. The output must state how many sellers Valera can deal with, followed by their 1-based indices in ascending order.

The constraints are small: `n` and the number of items per seller `k_i` are at most 50. Prices and Valera's budget are up to 10^6. This implies that a straightforward search across all items for each seller is feasible because the total number of price checks in the worst case is 50 × 50 = 2500, which is trivial for modern CPUs in under a second.

A subtle edge case is when all items from a seller are priced higher than Valera's budget. A naive approach that assumes any seller with items can be chosen would incorrectly include them. Another edge case is when multiple items are cheaper than `v`; only one successful outbid is sufficient per seller, but a careless implementation might count multiple times.

## Approaches

The brute-force approach is also essentially the optimal one due to small input sizes. We can iterate over each seller, then over each of their items, checking whether the price is less than Valera's budget. The first item that satisfies this condition confirms that Valera can deal with this seller, and we can move on to the next seller. This is correct because the problem only requires that at least one item per seller is affordable, and the exact item chosen does not matter. In the worst case, we perform `n * k_i` comparisons, which is at most 2500 for the largest input.

The observation that allows this problem to be solved efficiently is that we do not need to track all items below `v` for each seller; we only need to detect the existence of one. This avoids unnecessary computation and makes the solution straightforward and efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force / Optimal | O(n * max k_i) = O(2500) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `v` from input.
2. Initialize an empty list `deal_sellers` to store indices of sellers with whom Valera can make a deal.
3. For each seller `i` from 1 to `n`:

1. Read the number of items `k_i` and their prices.
2. Check each item's price sequentially.
3. If an item's price is strictly less than `v`, append `i` to `deal_sellers` and break the loop for this seller.
4. Print the number of sellers in `deal_sellers`.
5. Print the indices of these sellers in ascending order.

Why it works: the invariant is that whenever a seller is added to `deal_sellers`, Valera can afford at least one item from that seller. Iterating through each item guarantees that no seller is missed, and breaking early avoids redundant checks.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, v = map(int, input().split())
deal_sellers = []

for i in range(1, n + 1):
    data = list(map(int, input().split()))
    k_i, prices = data[0], data[1:]
    for price in prices:
        if price < v:
            deal_sellers.append(i)
            break

print(len(deal_sellers))
print(' '.join(map(str, deal_sellers)))
```

The code reads the number of sellers and Valera's budget. For each seller, it reads their items and checks if at least one is affordable. Once an affordable item is found, it records the seller's index and moves on. The output prints the total number of sellers and their indices, matching the required format.

## Worked Examples

Sample 1:

Input:

```
3 50000
1 40000
2 20000 60000
3 10000 70000 190000
```

| seller | prices | item < v? | deal_sellers |
| --- | --- | --- | --- |
| 1 | 40000 | yes | [1] |
| 2 | 20000, 60000 | yes (20000) | [1, 2] |
| 3 | 10000, 70000, 190000 | yes (10000) | [1, 2, 3] |

Output:

```
3
1 2 3
```

This trace confirms that the algorithm correctly identifies the first item that Valera can afford per seller.

Sample 2:

Input:

```
2 10000
2 20000 30000
1 15000
```

| seller | prices | item < v? | deal_sellers |
| --- | --- | --- | --- |
| 1 | 20000, 30000 | no | [] |
| 2 | 15000 | no | [] |

Output:

```
0
```

This confirms the algorithm correctly handles the case when no deals are possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * max k_i) | We check each item for each seller until we find an affordable one. |
| Space | O(n) | We store indices of sellers Valera can deal with. |

Given n ≤ 50 and k_i ≤ 50, the total operations are under 2500, which easily fits within 1 second. Memory usage is negligible compared to the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, v = map(int, input().split())
    deal_sellers = []
    for i in range(1, n + 1):
        data = list(map(int, input().split()))
        k_i, prices = data[0], data[1:]
        for price in prices:
            if price < v:
                deal_sellers.append(i)
                break
    out = f"{len(deal_sellers)}\n{' '.join(map(str, deal_sellers))}"
    return out

# Provided samples
assert run("3 50000\n1 40000\n2 20000 60000\n3 10000 70000 190000\n") == "3\n1 2 3", "sample 1"
assert run("2 10000\n2 20000 30000\n1 15000\n") == "0\n", "sample 2"

# Custom cases
assert run("1 5000\n1 4999\n") == "1\n1", "minimum-size input"
assert run("2 1000000\n50 " + " ".join(str(x) for x in range(1000000, 1000050)) + "\n50 " + " ".join(str(x) for x in range(500000, 500050)) + "\n") == "1\n2", "max-size inputs"
assert run("3 10000\n2 10000 10000\n2 9999 10001\n2 10001 10002\n") == "1\n2", "all-equal prices and boundary check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5000\n1 4999 | 1\n1 | Minimum-size input |
| 2 sellers with max-size items | 1\n2 | Handling largest possible input sizes |
| Equal and boundary prices | 1\n2 | Correct handling of exact budget boundary and duplicates |

## Edge Cases

If all items from a seller are more expensive than Valera's budget, the algorithm never appends that seller. For example, with input:

```
2 10000
1 15000
2 12000 13000
```

The trace:

| seller | prices | item < v? | deal_sellers |
| --- | --- | --- | --- |
| 1 | 15000 | no | [] |
| 2 | 12000, 13000 | no | [] |

Output:

```
0
```

This confirms that sellers with unaffordable items are correctly excluded. The algorithm checks each item and breaks only when a valid item is found, preventing false positives.
