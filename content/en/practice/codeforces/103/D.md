---
title: "CF 103D - Time to Raid Cowavans"
description: "We have an array of cow weights. For every query (a, b), we repeatedly take positions a, a + b, a + 2b, ... until the index exceeds n, and we must output the sum of all visited values."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "sortings"]
categories: ["algorithms"]
codeforces_contest: 103
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 80 (Div. 1 Only)"
rating: 2100
weight: 103
solve_time_s: 108
verified: false
draft: false
---

[CF 103D - Time to Raid Cowavans](https://codeforces.com/problemset/problem/103/D)

**Rating:** 2100  
**Tags:** brute force, data structures, sortings  
**Solve time:** 1m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We have an array of cow weights. For every query `(a, b)`, we repeatedly take positions

`a, a + b, a + 2b, ...`

until the index exceeds `n`, and we must output the sum of all visited values.

If the array is

`[1, 2, 3, 4, 5]`

and the query is `(2, 2)`, we take positions `2, 4`, so the answer is `2 + 4 = 6`.

The important part is the scale. Both the number of cows and the number of queries can reach `3 * 10^5`. A direct simulation for every query can become extremely expensive.

Suppose we process one query by repeatedly jumping by `b`. The number of visited elements is roughly `n / b`.

If `b = 1`, one query touches all `n` elements. With `3 * 10^5` queries, that becomes about

$3 \cdot 10^5 \times 3 \cdot 10^5 = 9 \cdot 10^{10}$

operations, far beyond the limit.

The structure of the queries matters. Small jump sizes produce long sequences, while large jump sizes produce short sequences. This asymmetry is the key observation behind the accepted solution.

There are also several edge cases that are easy to mishandle.

Consider this input:

```
5
1 2 3 4 5
1
5 3
```

The correct answer is:

```
5
```

After taking position `5`, the next position would be `8`, which is outside the array. A careless loop condition like `while pos < n` instead of `<= n` would skip the last valid element.

Another subtle case appears when `b = 1`.

```
4
10 20 30 40
1
2 1
```

The correct answer is:

```
90
```

because we take `20 + 30 + 40`.

This is the worst-case query length. Any solution that recomputes these sums repeatedly will time out.

A different issue appears with indexing. The problem uses 1-based positions, but Python lists are 0-based.

```
3
5 6 7
1
1 2
```

The correct answer is:

```
12
```

because we take positions `1` and `3`, giving `5 + 7`.

If we forget to convert indices properly, we may accidentally sum `6` instead.

Finally, the sums can become large. Each value can be up to `10^9`, and we may add up to `3 * 10^5` elements. The result can exceed 32-bit integer range, so the implementation must use 64-bit arithmetic. Python handles this automatically.

## Approaches

The brute-force approach follows the query definition directly.

For a query `(a, b)`, start at position `a`, repeatedly add the current element to the answer, then move to `a + b`, `a + 2b`, and so on until leaving the array.

This works because the query itself explicitly describes an arithmetic progression of indices.

The cost of one query is proportional to the number of visited positions, roughly `n / b`.

When `b` is large, this is actually very fast. For example, if `b = 1000`, only about `300` positions are visited even when `n = 3 * 10^5`.

The problem comes from small values of `b`.

If many queries have `b = 1`, every query scans almost the entire array. In the worst case, the total complexity becomes

$O(p \cdot n)$

which is too slow.

The key observation is that there are only a small number of distinct small jump sizes.

If we choose a threshold `B ≈ sqrt(n)`, then:

For queries with `b > B`, brute force is cheap because each query visits at most `n / B` elements.

For queries with `b <= B`, we can precompute all answers.

This works because the number of small `b` values is limited.

For a fixed jump size `b`, define:

$dp[i] = w_i + dp[i+b]$

where `dp[i]` represents the answer for query `(i, b)`.

We compute this backwards from `n` down to `1`. Once built, every query with this `b` can be answered in constant time.

The total preprocessing cost is manageable because we only do this for about `sqrt(n)` different jump sizes.

The final complexity becomes roughly:

$O(n\sqrt{n} + p\sqrt{n})$

which easily fits within the limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(p · n) worst case | O(1) | Too slow |
| Optimal | O(n√n + p√n) | O(n√n) | Accepted |

## Algorithm Walkthrough

1. Read the array of cow weights using 1-based indexing.

Using 1-based indexing keeps the query logic identical to the statement and avoids repeated index conversions.
2. Choose a threshold value `B = int(sqrt(n)) + 1`.

Queries with jump size larger than `B` are short enough to process directly. Queries with smaller jump sizes are worth preprocessing.
3. Create a DP table where `dp[b][i]` stores the answer for query `(i, b)` for all `b <= B`.
4. For every small jump size `b` from `1` to `B`, compute the table backwards.

The recurrence is:

if `i + b <= n`, otherwise:

the recurrence:
