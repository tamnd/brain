---
title: "CF 106347B - \u0426\u0432\u0435\u0442\u043e\u0447\u043d\u044b\u0439 \u043c\u0430\u0433\u0430\u0437\u0438\u043d"
description: "We have a flower shop with n different flower types. A valid bouquet needs exactly one flower of every type, so making one bouquet consumes one flower from each category. The shop already owns a[i] flowers of type i."
date: "2026-06-25T08:04:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106347
codeforces_index: "B"
codeforces_contest_name: "\u0412\u044b\u0441\u0448\u0430\u044f \u043f\u0440\u043e\u0431\u0430 - 2024. \u0417\u0430\u043a\u043b\u044e\u0447\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f"
rating: 0
weight: 106347
solve_time_s: 29
verified: false
draft: false
---

[CF 106347B - \u0426\u0432\u0435\u0442\u043e\u0447\u043d\u044b\u0439 \u043c\u0430\u0433\u0430\u0437\u0438\u043d](https://codeforces.com/problemset/problem/106347/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 29s  
**Verified:** no  

## Solution
## Problem Understanding

We have a flower shop with `n` different flower types. A valid bouquet needs exactly one flower of every type, so making one bouquet consumes one flower from each category. The shop already owns `a[i]` flowers of type `i`. If some type runs out, Petya can buy additional flowers of that type from a base, paying one ruble for each purchased flower.

For every query value `x`, we need to determine the largest number of complete bouquets Petya can make if he is allowed to spend at most `x` rubles on extra flowers.

The main difficulty is that the queries are independent. We cannot simulate buying flowers separately for every query because both the number of flower types and the number of queries can reach `100000`. Any solution doing work proportional to `n * q` would require up to `10^10` operations, which is far beyond what a typical 1 second limit allows. We need to preprocess the flower information once and answer each query quickly.

The initial amount of every flower type can be very large, up to `10^9`, so storing every possible bouquet count or simulating individual flowers is impossible. The algorithm must work with ranges and arithmetic formulas instead.

Several edge cases are easy to miss.

Consider a single flower type:

```
Input:
1 3
5
0 1 10
```

The correct output is:

```
5 6 15
```

With one type of flower, every single flower is already a complete bouquet. A solution that assumes a bouquet always needs multiple types or forgets this case may return incorrect values.

Another important case is when the shop initially has uneven amounts:

```
Input:
2 3
1 0
1 2 5
```

The answers are:

```
1 1 3
```

With one ruble, Petya buys one flower of the second type and makes one bouquet. With two rubles, he still cannot make two bouquets because the first type is missing one additional flower for the second bouquet. A careless approach that only sums the available flowers may think two rubles are enough.

A third case is when one flower type limits the number of bouquets:

```
Input:
3 1
100 100 0
10
```

The answer is:

```
10
```

Even though two types have many flowers, the third type requires all purchases. The number of bouquets depends on balancing all types, not on the total flower count.

## Approaches

A straightforward approach is to test each possible bouquet count. Suppose we want to know whether `k` bouquets are possible. Type `i` requires `k` flowers, but the shop already owns `a[i]`, so the missing amount is:

```
max(0, k - a[i])
```

The total money required is the sum of these missing amounts over all types. If the value is at most `x`, then `k` bouquets can be made.

This check is correct because every missing flower has exactly the same price, and the only thing that matters is how many flowers are missing from each type.

The problem is the number of checks. The answer can be as large as `sum(a[i]) + x`, which can reach around `10^14`. Even if we use binary search for every query, each query would need about 50 checks, and each check would scan all `n` flower types. The complexity becomes:

```
O(q * n * log(answer))
```

which is far too slow for `n, q = 100000`.

The key observation is that the cost of producing `k` bouquets has a very simple shape.

For a fixed `k`, every type with `a[i] >= k` contributes zero cost. Every type with `a[i] < k` contributes exactly `k - a[i]`. If we sort the existing flower counts, then as `k` grows, the set of types that require buying flowers changes only when `k` passes one of the existing values.

After sorting:

```
b[0] <= b[1] <= ... <= b[n-1]
```

for a target bouquet count `k`, suppose exactly `t` types have `b[i] < k`. The required money is:

```
t * k - (b[0] + b[1] + ... + b[t-1])
```

The difficult part is not checking one value of `k`, but answering many queries. We need to understand the inverse problem: for a given budget `x`, what is the largest `k` where the cost is at most `x`?

Because the cost function only increases as `k` increases, we can binary search the answer. The sorted array and prefix sums let us calculate the cost of any candidate `k` quickly.

For a candidate `k`, we find how many flower types have fewer than `k` flowers using binary search. Then we use the prefix sum of those types to calculate the exact amount of money needed.

The brute-force method works because every candidate bouquet count can be verified independently. The observation that the verification function is monotonic lets us search over the answer instead of trying every possible number.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * q * log(answer)) | O(1) | Too slow |
| Optimal | O((n + q) * log(n) * log(answer)) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the existing flower counts and build prefix sums.

The sorted order lets us quickly find all flower types that have fewer than a chosen number of flowers. The prefix sums allow the total missing cost to be computed without iterating through those types.

1. For each query budget `x`, binary search the maximum possible number of bouquets.

The answer space is monotonic. If `k` bouquets can be made with `x` rubles, then any smaller number of bouquets can also be made with the same budget.

1. For every binary search midpoint `mid`, calculate the required money for `mid` bouquets.

Find the first position where the sorted flower count is at least `mid`. Let this position be `pos`. The first `pos` types need extra flowers, and their total cost is:

```
pos * mid - prefix[pos]
```

The remaining types already have enough flowers for `mid` bouquets.

1. If the calculated cost is at most `x`, move the binary search upward.

This means `mid` bouquets are achievable, so there may be a larger answer.

1. Otherwise, move the binary search downward.

The budget is insufficient for `mid` bouquets, so every larger number is impossible as well.

Why it works:

The function `cost(k)`, which represents the minimum money needed to make `k` bouquets, is nondecreasing. Increasing `k` can never reduce the number of missing flowers. Binary search relies exactly on this property. For every tested value, the prefix sums compute the true minimum purchase cost, so the search only discards impossible ranges and keeps all possible answers. When the search finishes, the largest feasible `k` is the required answer.
