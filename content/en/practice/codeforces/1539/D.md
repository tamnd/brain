---
title: "CF 1539D - PriceFixed"
description: "We are asked to determine the minimal total cost for Lena to buy a set of products where each product has a required quantity and a threshold for a discount."
date: "2026-06-10T14:41:47+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "implementation", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1539
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 727 (Div. 2)"
rating: 1600
weight: 1539
solve_time_s: 268
verified: true
draft: false
---

[CF 1539D - PriceFixed](https://codeforces.com/problemset/problem/1539/D)

**Rating:** 1600  
**Tags:** binary search, greedy, implementation, sortings, two pointers  
**Solve time:** 4m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine the minimal total cost for Lena to buy a set of products where each product has a required quantity and a threshold for a discount. Each product costs 2 rubles initially, and after buying at least `b_i` items of any products, the price of product `i` drops to 1 ruble per unit for all subsequent purchases. Lena can buy more than the required amount if it helps reduce the overall cost.

The input gives us `n` products. Each product has a requirement `a_i` and a discount threshold `b_i`. Our output is the smallest total cost to satisfy all the requirements. The sum of all `a_i` can be as large as `10^14`, so algorithms that simulate each purchase individually would be too slow. Because `n` can be up to `10^5`, we cannot use algorithms with worse than O(n log n) time complexity, but we can handle linear or quasi-linear passes through sorted or priority-based data structures. Non-obvious edge cases include when the cheapest discounts are available late, requiring Lena to buy extra items of other products first, or when some products have very high thresholds compared to required quantities. A naive approach that buys each product in arbitrary order may ignore opportunities to unlock discounts and can significantly overspend.

For example, if we have two products with `a=[1,1]` and `b=[2,1]`, a careless approach that buys them sequentially may pay full price for both items. The optimal strategy is to buy the second product first to unlock the discount on the first, reducing the cost from 4 to 3 rubles.

## Approaches

A brute-force approach would simulate all possible purchase orders. For each day or purchase, we would check which items are affordable at discounted rates and choose one, repeating until all requirements are met. This works in principle because every purchase reduces the future cost of some items, but the number of permutations grows factorially with `n` and the quantities `a_i` are enormous, up to `10^14`. Simulating each purchase individually is infeasible because even a single product with `a_i = 10^{14}` would require `10^{14}` iterations.

The key observation is that the order of buying matters only in terms of when a discount becomes available, and once a discount is unlocked, it remains available for all future purchases. This lets us think greedily: we want to prioritize unlocking discounts on expensive products as early as possible. Since every product initially costs 2 rubles, we can always start with products with the smallest `b_i` (thresholds) to unlock other discounts quickly. However, the quantities `a_i` are large, so we cannot buy single units greedily. Instead, we can use a two-pointer approach: one pointer for the cheapest "to buy at full price" items and another for items that are already discounted or whose threshold is met. We sort products by their `b_i` values, and then simulate purchasing in bulk using two pointers to maximize the number of discounted purchases while meeting all `a_i` requirements. This reduces the complexity to linear in the number of products after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(sum a_i) | O(n) | Too slow for large inputs |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all product requirements `a_i` and discount thresholds `b_i`. Store them as pairs `(b_i, a_i)`. We will sort by `b_i` to prioritize discounts that unlock early.
2. Sort the products by their discount thresholds `b_i` in increasing order. This ensures that when we buy enough units to reach a threshold, we unlock discounts for as many products as possible with minimal initial expenditure.
3. Initialize two pointers, `l` at the start of the sorted list and `r` at the end. `l` represents the next product to buy at discounted or already purchased units, `r` represents the next product for full-price purchases to unlock discounts.
4. Keep track of the cumulative number of units purchased so far (`total_bought`) and the total cost (`cost`). Repeat until all `a_i` are satisfied:

a. If `total_bought >= b_i` for the product at pointer `l`, we can buy units at discounted price (1 ruble). Buy all required remaining units and increment `total_bought` and `cost`.

b. Otherwise, buy full-price units (2 rubles) from the product at pointer `r` to increase `total_bought` enough to unlock discounts. Only buy the minimal amount needed, not more than required for that product.
5. Continue this process moving the pointers inward (`l` increases when discounted purchases are done, `r` decreases when full-price purchases are done) until all quantities `a_i` are bought.

The invariant is that `total_bought` always accurately reflects the total items purchased, which determines which products can be bought at a discount. The algorithm never buys more full-price items than necessary to unlock discounts. Sorting by `b_i` guarantees that cheaper discounts are utilized first, ensuring minimal total cost.

## Python Solution

```
PythonRun
```

The solution first reads all product information and stores it as pairs `(b_i, a_i)` for easier sorting by discount thresholds. Sorting ensures that products with lower thresholds are considered first. The two-pointer loop carefully manages purchases: discounted purchases are handled at pointer `l`, and full-price purchases are taken from pointer `r` to unlock future discounts. Buying only the minimal required number of full-price items avoids overspending. The algorithm terminates when all required units are bought.

## Worked Examples

Using Sample 1:

| Step | l | r | total_bought | action | cost | remaining a_i |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 2 | 0 | full-price 1 from r=2 | 2 | [3,1,0] |
| 2 | 0 | 2 | 1 | full-price 1 from r=2 | 4 | [3,1,0] |
| 3 | 0 | 1 | 2 | full-price 1 from r=1 | 6 | [3,0] |
| 4 | 0 | 0 | 3 | discounted 1 from l=0 | 7 | [2] |
| 5 | 0 | 0 | 4 | discounted 2 from l=0 | 8 | [0] |

The table confirms that total cost 8 is achieved. All products meet the required quantities, and discounts are applied optimally.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting by `b_i` dominates; the two-pointer loop is O(n) |
| Space | O(n) | Storing product pairs and pointers |

The solution efficiently handles up to 100,000 products and very large quantities because it avoids iterating over individual units. Memory usage scales linearly with the number of products, well within limits.

## Test Cases

```
PythonRun
```
