---
title: "CF 104887H - Harana"
description: "Each position in the input represents a note in a song. At position i, there is an intended note si and Bob actually sings bi. If nothing else changed, the mismatch at position i is simply the absolute difference between these two values."
date: "2026-06-28T09:02:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104887
codeforces_index: "H"
codeforces_contest_name: "2023 Abakoda Long Contest"
rating: 0
weight: 104887
solve_time_s: 73
verified: true
draft: false
---

[CF 104887H - Harana](https://codeforces.com/problemset/problem/104887/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

Each position in the input represents a note in a song. At position `i`, there is an intended note `s_i` and Bob actually sings `b_i`. If nothing else changed, the mismatch at position `i` is simply the absolute difference between these two values.

Bob is allowed to shift the musical key, which means adding an integer constant to all notes in a contiguous segment. A key shift does not affect Bob’s singing; it shifts the song itself. After shifting, each position compares Bob’s fixed value `b_i` against a modified song value.

For a chosen split point `m`, the song is divided into two segments. The first segment uses one integer shift `k_1`, and the second segment uses another shift `k_2`. The goal is to choose both shifts so that the total absolute mismatch is minimized.

A key observation is that shifting a segment by `k` transforms each term into an expression of the form `|b_i - (s_i + k)|`, so the problem is really about choosing an integer `k` that best aligns a set of numbers.

The input size goes up to `2 × 10^5`, which immediately rules out any approach that tries all possible shifts or recomputes costs from scratch for every split. Even an `O(n^2)` solution that recomputes each segment independently would require on the order of `4 × 10^10` operations in the worst case, which is far beyond limits.

A subtle edge case appears when all differences cancel out in one segment but not in the other. For example, if `b_i - s_i` is constant in a segment, the optimal shift makes the cost zero for that segment, and any incorrect method that assumes per-index independence can miss this completely.

## Approaches

Start by rewriting the expression inside the absolute value. For a fixed segment and shift `k`, each term becomes

`|b_i - (s_i + k)| = |(b_i - s_i) - k|`.

Define `x_i = b_i - s_i`. Then each segment cost becomes minimizing

`sum |x_i - k|` over integer `k`.

This is a classic structure: we are choosing a single integer `k` that minimizes absolute deviation from a multiset of values. The optimal choice of `k` is a median of the segment, and the minimum cost is the sum of distances to that median.

So each split `m` requires computing two independent 1D problems: prefix `[1..m]` and suffix `[m+1..n]`. The total answer is the sum of their optimal absolute deviation costs.

The brute-force solution would, for each `m`, recompute the optimal `k_1` and `k_2` by sorting both halves and evaluating median costs. That gives `O(n)` work per split, leading to `O(n^2 log n)` overall, which is too slow.

The optimization comes from noticing that both prefix and suffix can be processed incrementally. As we extend a segment by one element, we can maintain its median and the sum of distances to it using two heaps and running sums. This reduces each segment cost computation to amortized `O(log n)` per insertion.

Suffix values are handled by processing the array in reverse.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (recompute each split) | O(n^2 log n) | O(n) | Too slow |
| Optimal (two heaps + prefix/suffix DP) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

Let `x_i = b_i - s_i`. We want prefix and suffix costs of optimal absolute deviation.

### 1. Convert the problem

Replace every pair `(s_i, b_i)` with `x_i = b_i - s_i`. From now on each segment cost is `min_k sum |x_i - k|`.

The shift value `k` disappears from the structure except as a median selector.

### 2. Build prefix costs online

We maintain a dynamic multiset of values with the ability to query:

the sum of absolute distances to the best integer `k`.

We store:

- a max heap for the lower half
- a min heap for the upper half
- sums of elements in each heap

The median is the top of the max heap.

As we insert each `x_i`, we rebalance heaps so that sizes differ by at most one, with the lower heap holding the extra element when odd.

The prefix cost at each position is computed from the current median.

### 3. Compute cost from median

If median is `m`, then:

Left side contributes `m * len(left) - sum(left)`.

Right side contributes `sum(right) - m * len(right)`.

Summing both gives total absolute deviation.

### 4. Build suffix costs

Repeat the same process on the reversed array to obtain suffix costs for every starting position.

### 5. Combine answers

For each split `m`, output:

`prefix_cost[m] + suffix_cost[m+1]`.

### Why it works

For any fixed segment, the function `sum |x_i - k|` is convex in `k` over integers. Its minimum is achieved at a median, and any deviation from the median increases the cost linearly according to how many points lie on each side. Maintaining a median split ensures that at every step we preserve the optimal structure of the segment, so the computed cost is always minimal for that prefix or suffix.

## Python Solution

```python
import sys
input = sys.stdin.readline
import heapq

INF = 10**30

def compute_costs(arr):
    low = []   # max heap via negatives
    high = []  # min heap
    sum_low = 0
    sum_high = 0

    def rebalance():
        nonlocal sum_low, sum_high
        if len(low) > len(high) + 1:
            x = -heapq.heappop(low)
            sum_low -= x
            heapq.heappush(high, x)
            sum_high += x
        elif len(high) > len(low):
            x = heapq.heappop(high)
            sum_high -= x
            heapq.heappush(low, -x)
            sum_low += x

    def add(x):
        nonlocal sum_low, sum_h
```
