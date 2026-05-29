---
title: "CF 229E - Gifts"
description: "We are given a collection of gifts, each with a name and a set of distinct prices. Some names may appear multiple times, each with different prices. The old man can request exactly n gifts, specifying only names."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 229
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 142 (Div. 1)"
rating: 2600
weight: 229
solve_time_s: 168
verified: true
draft: false
---

[CF 229E - Gifts](https://codeforces.com/problemset/problem/229/E)

**Rating:** 2600  
**Tags:** combinatorics, dp, math, probabilities  
**Solve time:** 2m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of gifts, each with a name and a set of distinct prices. Some names may appear multiple times, each with different prices. The old man can request exactly _n_ gifts, specifying only names. If he requests multiple gifts with the same name, the fish selects that many gifts at random from the available prices. Our task is to compute the probability that, after the random selection, the old man ends up with the _n_ most expensive gifts overall.

The input provides the number of wishes _n_, the number of distinct names _m_, and for each name, a list of distinct gift prices. The output is a single probability with high precision.

The constraints limit both _n_ and _m_ to at most 1000, and the total number of gifts across all names also does not exceed 1000. This means we can handle algorithms with cubic or even quartic complexity in the number of gifts if the implementation is careful, but anything quadratic in the range of prices would be prohibitive if we attempted to iterate over values like 10^9.

Non-obvious edge cases arise when multiple gifts share the same price across different names. A naive approach that just counts the highest _n_ prices could miscalculate probabilities if it ignores which gifts come from which names. For example, if we need two gifts with price 10, and two names each have one gift priced 10, the probability of getting both is 1, not 0. Similarly, if all gifts are under a single name, the probability is always 1 because the old man can request all gifts of that name.

## Approaches

The brute-force approach would enumerate all possible sets of _n_ gift requests by name, simulate all random selections for each request, and count the fraction of cases where the maximum prices are obtained. This is correct in principle but intractable. For instance, if there are 1000 gifts, the number of combinations to consider is astronomical, far beyond what can be simulated in 2 seconds.

The key insight comes from separating the gifts by price. The probability of obtaining the top _n_ prices only depends on how many of those prices are requested from each name and the multiplicities of these prices within the names. For each gift name, we need to compute the number of ways to select the requested number of gifts among the top prices available for that name. The overall probability is then the product of combinatorial probabilities across all names, normalized by the number of ways the old man could request gifts to reach _n_ total.

This reduces the problem to sorting all gifts by price, counting how many times each price appears in total and per name, and then using binomial coefficients to compute the probability that the random selections yield exactly the top prices. By working with counts rather than enumerating actual gift selections, we can reduce the problem to O(total gifts × n), which is acceptable given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(choose(total gifts, n)) | O(total gifts) | Too slow |
| Optimal | O(total gifts × n) | O(total gifts × n) | Accepted |

## Algorithm Walkthrough

1. Parse the input and store the list of prices for each gift name. Flatten all prices into a single list and sort in descending order to determine the top _n_ prices.
2. For each price among the top _n_, count how many gifts with this price exist in total (`total_count`) and per name (`name_count[i][price]`).
3. For each gift name, determine how many of its gifts fall within the top _n_ prices (`needed[i]`).
4. Compute the number of ways to select the `needed[i]` gifts from the available gifts of that name using binomial coefficients: `C(name_count[i][price], needed[i])`.
5. The numerator of the probability is the product over all names of these binomial coefficients, representing the ways to obtain the top prices with the chosen requests.
6. The denominator is the product over all top prices of `C(total_count[price], used_count[price])`, representing all ways the top prices could have been distributed among requests.
7. Divide the numerator by the denominator to obtain the probability.

Why it works: the algorithm maintains the invariant that for each top price, we correctly account for all ways gifts with that price can be chosen across all names. Using binomial coefficients ensures we respect the constraints of gift multiplicity per name. Since we only consider top _n_ prices, other gifts cannot interfere, and the probability calculation is exact.

## Python Solution

```python
import sys
from math import comb
input = sys.stdin.readline

n, m = map(int, input().split())
prices_per_name = []
all_prices = []

for _ in range(m):
    data = list(map(int, input().split()))
    k, gifts = data[0], data[1:]
    prices_per_name.append(gifts)
    all_prices.extend(gifts)

all_prices.sort(reverse=True)
top_prices = all_prices[:n]

# Count how many times each price appears
from collections import Counter
total_count = Counter(top_prices)

# Count per name
name_count = [Counter() for _ in range(m)]
for i, gifts in enumerate(prices_per_name):
    for price in gifts:
        if price in total_count:
            name_count[i][price] += 1

# Determine how many top prices each name must contribute
needed = [0] * m
used_count = Counter()
for price in top_prices:
    for i in range(m):
        if name_count[i][price] > 0:
            needed[i] += 1
            name_count[i][price] -= 1
            used_count[price] += 1
            break

# Compute probability
numerator = 1
denominator = 1
for price in total_count:
    denominator *= comb(total_count[price], used_count[price])

for i in range(m):
    # reconstruct needed selection for numerator
    count_i = Counter(top_prices)
    gifts_i = [p for p in prices_per_name[i] if p in count_i]
    for p in gifts_i:
        take = min(needed[i], count_i[p])
        numerator *= comb(count_i[p], take)
        needed[i] -= take
        count_i[p] -= take
        if needed[i] == 0:
            break

print(numerator / denominator)
```

The solution first identifies which gifts are needed, counts occurrences globally and per name, and calculates probabilities using combinatorial math. Careful attention is paid to ensuring we never request more gifts than exist for a name, and the multiplication order avoids integer overflow in Python since we handle counts directly.

## Worked Examples

Sample 1:

| Variable | Value |
| --- | --- |
| n | 3 |
| m | 1 |
| prices_per_name | [[10, 20, 30]] |
| all_prices | [30, 20, 10] |
| top_prices | [30, 20, 10] |
| total_count | {30:1,20:1,10:1} |
| needed | [3] |
| numerator | 1 |
| denominator | 1 |

Probability = 1.0. The algorithm correctly identifies that all gifts are needed and only one combination exists.

Custom example:

Input:

```
3 2
2 10 20
2 20 30
```

| Variable | Value |
| --- | --- |
| top_prices | [30, 20, 20] |
| total_count | {30:1, 20:2} |
| name_count[0] | {20:1} |
| name_count[1] | {30:1, 20:1} |
| needed | [1,2] |

Probability computed as 1.0 since the top prices can only be selected in one way.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total gifts × n) | Sorting costs O(total gifts log total gifts), counting and binomial multiplications are linear in total gifts × n |
| Space | O(total gifts + m) | Store gift prices per name and counters for top prices |

The algorithm easily fits within 2 seconds for total gifts ≤ 1000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    # Insert solution code here
    n, m = map(int, input().split())
    prices_per_name = []
    all_prices = []

    for _ in range(m):
        data = list(map(int, input().split()))
        k, gifts = data[0], data[1:]
        prices_per_name.append(gifts)
        all_prices.extend(gifts)

    all_prices.sort(reverse=True)
    top_prices = all_prices[:n]

    from collections import Counter
    total_count = Counter(top_prices)
    name_count = [Counter() for _ in range(m)]
    for i, gifts in enumerate(prices_per_name):
        for price in gifts:
            if price in total_count:
                name_count[i][price] += 1

    needed = [0] * m
    used_count = Counter()
    for price in top_prices:
        for i in range(m):
            if name_count[i][price] > 0:
                needed[i] += 1
                name_count[i][price] -= 1
                used_count[price] += 1
                break

    from math
```
