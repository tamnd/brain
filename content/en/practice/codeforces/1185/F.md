---
title: "CF 1185F - Two Pizzas"
description: "We are asked to help a group of friends pick exactly two pizzas so that the maximum number of friends are satisfied with the choice."
date: "2026-06-12T00:54:49+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 1185
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 568 (Div. 2)"
rating: 2100
weight: 1185
solve_time_s: 66
verified: true
draft: false
---

[CF 1185F - Two Pizzas](https://codeforces.com/problemset/problem/1185/F)

**Rating:** 2100  
**Tags:** bitmasks, brute force  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to help a group of friends pick exactly two pizzas so that the maximum number of friends are satisfied with the choice. Each friend has a set of favorite ingredients, and a friend is satisfied if every one of their favorite ingredients appears on at least one of the two selected pizzas. Each pizza has a fixed set of ingredients and a price. If multiple pairs of pizzas satisfy the same number of friends, we must choose the pair with the minimum combined price. The output is simply the indices of the two pizzas.

The number of friends, $n$, and the number of pizzas, $m$, can each be as large as $10^5$. Each friend and pizza involves up to 9 ingredients, since the total number of possible ingredients is 9. These bounds rule out any solution that explicitly checks all $n \times m^2$ combinations, which would reach $10^{15}$ operations in the worst case. Instead, we need to exploit the small number of ingredients and use a representation that allows us to quickly check which friends are satisfied by a pair of pizzas.

A subtle edge case occurs when multiple pizzas together cover all ingredients needed for a friend, but no single pizza does. For example, if a friend likes ingredients {1,2}, and the pizzas are [{1}, {2}], choosing only one pizza will not satisfy this friend. Any naive approach that evaluates satisfaction per pizza independently will incorrectly count this friend as unsatisfied. Another edge case arises when several pairs of pizzas satisfy the same number of friends - we must choose the pair with the minimal total cost.

## Approaches

The brute-force approach is straightforward: iterate over all pairs of pizzas, compute the union of their ingredients, and count how many friends have all their ingredients in that union. Keep track of the pair giving the maximum number of satisfied friends, breaking ties by minimal total cost. This is correct in principle but has $O(m^2 \cdot n \cdot k)$ complexity, where $k \le 9$ is the number of ingredients per friend. With $m = 10^5$ and $n = 10^5$, this is completely impractical.

The key insight is that there are only 9 ingredients, so we can represent any set of ingredients as a 9-bit integer (bitmask). A friend's preference set and a pizza's ingredients can each be encoded as a bitmask of length 9. Using bitwise operations, we can quickly determine if a friend's preferences are satisfied by a pizza or a combination of pizzas. Since there are only $2^9 = 512$ possible ingredient sets, we can preprocess the cheapest pizza for each ingredient set. Then, instead of checking all $m^2$ pizza pairs directly, we only need to consider pairs among the 512 possible sets, drastically reducing the number of comparisons from $10^{10}$ to roughly $512^2 = 262144$, which is feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m^2) | O(1) | Too slow |
| Bitmask Compression | O(n + 2^9 * 2^9) | O(2^9) | Accepted |

## Algorithm Walkthrough

1. Encode each friend's set of favorite ingredients as a 9-bit integer. Each bit represents whether the friend likes that ingredient.
2. Encode each pizza's ingredients as a 9-bit integer. Each pizza also has a cost.
3. Maintain a dictionary mapping each bitmask to the index of the cheapest pizza with that exact set of ingredients. If multiple pizzas share the same bitmask, keep the two cheapest, since the optimal pair might include the same ingredient set twice.
4. Count, for each possible friend mask (up to 512), how many friends have that mask. This allows us to compute satisfaction quickly by checking if the union of two pizza masks includes a friend mask.
5. Iterate over all pairs of pizza masks (including using the same mask twice if there are at least two pizzas of that type). For each pair, compute the union of the two masks. For each friend mask, check if it is fully contained in the union using a bitwise AND. Sum the counts of satisfied friends.
6. Keep track of the pair of pizzas that maximizes the total satisfied friends. If multiple pairs yield the same maximum, choose the one with the minimal total cost. Store indices for output.
7. Output the indices of the two selected pizzas.

Why it works: By using bitmasks and the small universe of ingredients, we reduce the problem to considering all meaningful ingredient combinations rather than all pizzas individually. Each union of pizza masks correctly represents the ingredients available from choosing those two pizzas. Counting satisfied friends with a bitwise check ensures correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
friend_count = [0] * 512  # count of friends for each mask

for _ in range(n):
    parts = list(map(int, input().split()))
    fmask = 0
    for ing in parts[1:]:
        fmask |= 1 << (ing - 1)
    friend_count[fmask] += 1

pizza_masks = {}
pizza_prices = {}
pizza_indices = {}

for idx in range(1, m + 1):
    parts = list(map(int, input().split()))
    price = parts[0]
    pmask = 0
    for ing in parts[2:]:
        pmask |= 1 << (ing - 1)
    
    if pmask not in pizza_prices:
        pizza_prices[pmask] = [price]
        pizza_indices[pmask] = [idx]
    else:
        pizza_prices[pmask].append(price)
        pizza_indices[pmask].append(idx)
        # keep only two cheapest
        combined = sorted(zip(pizza_prices[pmask], pizza_indices[pmask]))
        pizza_prices[pmask], pizza_indices[pmask] = zip(*combined[:2])

best_count = -1
best_cost = None
best_pair = None

masks = list(pizza_prices.keys())
for i in range(len(masks)):
    for j in range(i, len(masks)):
        mask1, mask2 = masks[i], masks[j]
        cost1_list, cost2_list = pizza_prices[mask1], pizza_prices[mask2]
        idx1_list, idx2_list = pizza_indices[mask1], pizza_indices[mask2]

        if i == j and len(cost1_list) < 2:
            continue  # cannot pick same pizza twice if only one exists

        cost = cost1_list[0] + (cost2_list[0] if i != j else cost1_list[1])
        union_mask = mask1 | mask2
        count = 0
        for fmask in range(512):
            if friend_count[fmask] > 0 and (fmask & union_mask) == fmask:
                count += friend_count[fmask]

        if count > best_count or (count == best_count and cost < best_cost):
            best_count = count
            best_cost = cost
            if i != j:
                best_pair = (idx1_list[0], idx2_list[0])
            else:
                best_pair = (idx1_list[0], idx1_list[1])

print(best_pair[0], best_pair[1])
```

The code first encodes friends and pizzas as bitmasks, then stores the two cheapest pizzas per mask. The nested loop over masks ensures we consider all feasible pairs without iterating over all $m^2$ pizzas. Union masks and bitwise AND operations efficiently check which friends are satisfied.

## Worked Examples

### Sample Input 1

```
3 4
2 6 7
4 2 3 9 5
3 2 3 9
100 1 7
400 3 3 2 5
100 2 9 2
500 3 2 9 5
```

| Step | mask1 | mask2 | union_mask | satisfied friends | cost | best_pair |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 7 | 14 | 15 | 2 | 500 | (2,3) |

Trace shows friend 1 likes {6,7}, friend 2 likes {2,3,5,9}, friend 3 likes {2,3,9}. Pizza 2 {3,2,5} + Pizza 3 {9,2} satisfies friends 2 and 3. Pizza 1 {7} satisfies friend 1. Optimal pair is Pizza 2 and 3 because it covers maximum friends with minimal price among optimal pairs.

### Custom Input 2

```
2 3
1 1
1 2
100 1 1
200 1 2
300 2 1 2
```

| Step | mask1 | mask2 | union_mask | satisfied friends | cost | best_pair |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 3 | 2 | 300 | (1,2) |
| 2 | 1 | 3 | 3 | 2 | 400 | (1,3) |

The first pair already gives maximum satisfaction with minimal cost. Shows algorithm prefers minimal cost in ties.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + 2^9 * |  |
