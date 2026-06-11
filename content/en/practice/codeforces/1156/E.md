---
title: "CF 1156E - Special Segments of Permutation"
description: "We are given a permutation of the numbers from 1 to n. For every subarray [l, r], we look at its maximum value. The subarray is called special when the sum of the two endpoint values equals that maximum: $$pl + pr = max(pl,dots,pr)$$ The task is to count how many subarrays…"
date: "2026-06-12T02:39:17+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer", "dsu", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1156
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 64 (Rated for Div. 2)"
rating: 2200
weight: 1156
solve_time_s: 101
verified: true
draft: false
---

[CF 1156E - Special Segments of Permutation](https://codeforces.com/problemset/problem/1156/E)

**Rating:** 2200  
**Tags:** data structures, divide and conquer, dsu, two pointers  
**Solve time:** 1m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of the numbers from `1` to `n`. For every subarray `[l, r]`, we look at its maximum value. The subarray is called special when the sum of the two endpoint values equals that maximum:

$$p_l + p_r = \max(p_l,\dots,p_r)$$

The task is to count how many subarrays satisfy this condition.

The array is a permutation, which is the crucial property. Every value appears exactly once. The maximum element of any segment is uniquely determined and appears at exactly one position.

The constraint `n ≤ 2 · 10^5` immediately rules out any algorithm that examines all subarrays. There are about

$$\frac{n(n+1)}2 \approx 2 \cdot 10^{10}$$

subarrays in the worst case, far beyond what can be processed in two seconds. Even an `O(n²)` solution would perform around `4 · 10^10` operations.

The permutation property suggests that values can be used as identifiers and that position lookups can be performed efficiently. Any accepted solution will need something close to `O(n log n)`.

A subtle point is that the maximum element may lie anywhere inside the segment, not necessarily at one of the endpoints.

Consider:

```
3 4 1
```

The segment `[1,3]` is special because

$$3 + 1 = 4$$

and `4` is the maximum of the segment, even though it is in the middle.

Another easy mistake is to count pairs of values instead of pairs of positions.

Example:

```
2 1 4 3
```

The values `1` and `3` sum to `4`, but the segment containing their positions is `[2,4]`, whose maximum is still `4`, so this pair contributes. The condition depends on both values and the positions enclosing them.

A third pitfall is double counting. Suppose a segment's maximum is `M`. Since the array is a permutation, there is only one position containing `M`, and every valid segment is naturally associated with that unique maximum position. A correct solution must count each segment exactly once through its maximum.

## Approaches

The most direct approach is to enumerate every subarray. For each pair `(l,r)` we compute the maximum value on that segment and check whether the endpoint sum equals that maximum.

The condition itself is easy to verify, but there are `Θ(n²)` segments. Even if range maximum queries were answered in `O(1)`, we would still perform about twenty billion checks when `n = 200000`. This is hopelessly slow.

The key observation is that every special segment has a unique maximum element. Let the maximum value of a special segment be `x`, located at position `m`.

Because

$$p_l + p_r = x,$$

the endpoints must be two values whose sum is exactly `x`.

Now look at all segments whose maximum is `x`. Since `x` is the maximum, every element inside that segment must be smaller than `x`. This means the segment must stay inside the maximal interval around position `m` that contains only values smaller than `x`.

This naturally leads to divide and conquer on the position of the maximum element.

Suppose we recursively process an interval `[L,R]`. Let `m` be the position of the maximum value in that interval.

Any special segment whose maximum is `p[m]` must have one endpoint on the left of `m` and the other on the right of `m` (possibly one endpoint equals `m`). For every value `a` on one side, we need a value

$$b = p[m] - a$$

on the other side.

Since the array is a permutation, every value appears at exactly one position. If we know the position of every value, we can check in `O(1)` whether the complementary value exists on the opposite side.

To keep the complexity low, we always iterate through the smaller side of the maximum and search complements on the larger side. This is the classic divide-and-conquer counting trick that yields

$$O(n \log n)$$

overall.

The recursion structure is identical to the Cartesian tree of the permutation. Each level charges work proportional to the smaller side, and every element participates in only `O(log n)` such scans.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal Divide and Conquer | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

### Preprocessing

Store `pos[v]`, the position of value `v` in the permutation.

Also build a structure that can return the position of the maximum value inside any interval. A segment tree works well.

### Recursive solve(L, R)

1. If `L >= R`, return.
2. Find the position `m` of the maximum value in `[L,R]`.
3. Let `mx = p[m]`.
4. Compare the sizes of the left side `[L,m-1]` and right side `[m+1,R]`.
5. Iterate through the smaller side.
6. For each value `a` encountered, compute

$$b = mx - a.$$

1. If `b` is outside the range `1..n`, skip it.
2. Look up the position of `b` using `pos[b]`.
3. Check whether that position lies on the opposite side of `m` but still inside `[L,R]`.
4. If it does, we have found exactly one special segment whose maximum is `mx`, so add one to the answer.
5. Recursively process `[L,m-1]`.
6. Recursively process `[m+1,R]`.

### Why it works

Fix any special segment. Let its maximum value be `mx` at position `m`.

When recursion reaches the smallest interval containing that segment and whose maximum is `mx`, the segment's endpoints lie on opposite sides of `m` or one endpoint equals `m`. Their values satisfy

$$a+b=mx.$$

During the scan of the smaller side, one endpoint value is examined. The algorithm computes the complementary value `mx-a` and checks whether its position lies on the other side. The segment is counted once.

No segment can be counted twice because every segment has a unique maximum value and thus belongs to exactly one recursion node. Conversely, every counted pair corresponds to endpoints whose enclosing segment has maximum `mx`, so every count is valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def sol
```
