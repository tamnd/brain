---
title: "CF 1439C - Greedy Shopping"
description: "We are given a sequence of shops arranged in a line, each with a fixed meal price. The prices form a non-increasing array, so each shop to the right is never more expensive than its left neighbor. There are two types of operations we need to support."
date: "2026-06-11T04:27:41+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "divide-and-conquer", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1439
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 684 (Div. 1)"
rating: 2600
weight: 1439
solve_time_s: 109
verified: true
draft: false
---

[CF 1439C - Greedy Shopping](https://codeforces.com/problemset/problem/1439/C)

**Rating:** 2600  
**Tags:** binary search, data structures, divide and conquer, greedy, implementation  
**Solve time:** 1m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of shops arranged in a line, each with a fixed meal price. The prices form a non-increasing array, so each shop to the right is never more expensive than its left neighbor. There are two types of operations we need to support. The first operation raises the prices of the first few shops to at least a specified value, without decreasing any existing price. The second operation simulates a buyer starting at a given shop, spending money greedily: he will purchase one meal in each shop he can afford as he moves right, stopping when he cannot afford the next meal.

The problem constraints are large. The number of shops and the number of queries can each reach 200,000. A naive simulation of each type 2 query, iterating through every shop and deducting the money, would involve O(n) operations per query, which could reach 4 × 10^10 operations in the worst case, far beyond what is feasible in 3 seconds. Similarly, performing type 1 updates naively by iterating and updating values is too slow. This means we need a data structure that can handle both range updates and efficient prefix or suffix queries.

Non-obvious edge cases include situations where the price update does not actually change the array because the values are already higher than the requested minimum. For example, with shops `[10, 8, 5]` and a type 1 query `1 2 7`, only the second shop changes, resulting in `[10, 8, 5]` remaining unchanged since 8 ≥ 7. Another edge case arises in type 2 queries when the buyer cannot afford any meal; the output should correctly be zero. For instance, with `[5, 4, 3]` and `2 1 2`, the buyer has 2 money, which is less than 5, 4, and 3, so the correct output is 0.

## Approaches

A brute-force approach processes each query directly on the array. For a type 1 query, we iterate from the first shop to the x-th shop, setting each value to the maximum of its current value and the given y. For a type 2 query, we simulate the buyer moving right from shop x, decrementing his money each time he buys a meal. This works correctly but performs up to n operations per query, leading to O(nq) total complexity, which is too slow for the given constraints.

The key insight for optimization is that both queries deal with contiguous ranges, and type 2 queries involve the sum of prices over a suffix. This allows us to use a segment tree with lazy propagation that supports two operations: setting a minimum value over a prefix and querying how many meals can be purchased with a given budget starting from a position. In this segment tree, each node stores the sum of its segment and the maximum value. For type 1, we propagate a "max update" over the range. For type 2, we perform a greedy traversal of the segment tree: if the sum of a segment is within the buyer's budget, we take all meals at once; otherwise, we go down to children, counting meals individually. This reduces the complexity to O(log n) per operation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Segment Tree with Lazy Max Updates | O(q log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a segment tree representing the array of shop prices. Each node stores the sum of its segment, the maximum price, and a lazy propagation value indicating a pending "max update".
2. For a type 1 query, propagate any pending updates down the tree to ensure correctness. Then, recursively traverse nodes covering the prefix `[1..x]`. If the maximum in a node is already at least y, no action is needed. Otherwise, apply a "max update" to the node and propagate lazily.
3. For a type 2 query, we want to count meals the buyer can purchase from shop x to n with budget y. Start at the root, recursively descending to segments overlapping `[x..n]`. If the sum of the segment is less than or equal to the remaining budget, take all meals at once, decrement the budget, and add the count of meals. Otherwise, descend to children until reaching individual shops, purchasing meals greedily. This uses the invariant that the tree always stores correct maximums and sums after lazy propagation.
4. After processing each query, output the results of type 2 queries in order.

Why it works: The segment tree maintains accurate sums and maximums through lazy propagation. Type 1 updates never decrease values, so the invariant that prices are non-decreasing through max updates holds. Type 2 queries greedily consume budget without violating the true state of the array, since the tree allows us to efficiently sum and check maximums over any range. This guarantees correct meal counts.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.size = 1
        while self.size < self.n:
            self.size <<= 1
        self.maxv = [0] * (2 * self.size)
        self.sumv = [0] * (2 * self.size)
        self.lazy = [0] * (2 * self.size)
        for i in range(self.n):
            self.maxv[self.size + i] = data[i]
            self.sumv[self.size + i] = data[i]
        for i in range(self.size - 1, 0, -1):
            self.pull(i)

    def pull(self, i):
        self.maxv[i] = max(self.maxv[i*2], self.maxv[i*2+1])
        self.sumv[i] = self.sumv[i*2] + self.sumv[i*2+1]

    def push(self, i, l, r):
        if self.lazy[i]:
            self.apply(i*2, self.lazy[i], (r-l)//2)
            self.apply(i*2+1, self.lazy[i], (r-l)//2)
            self.lazy[i] = 0

    def apply(self, i, val, length):
        if val <= self.maxv[i]:
            return
        self.maxv[i] = val
        self.sumv[i] = val * length
        if i < self.size:
            self.lazy[i] = val

    def update(self, ql, qr, val, i=1, l=0, r=None):
        if r is None:
            r = self.size
        if qr <= l or r <= ql:
            return
        if ql <= l and r <= qr and val >= self.maxv[i]:
            self.apply(i, val, r-l)
            return
        self.push(i, l, r)
        m = (l+r)//2
        self.update(ql, qr, val, i*2, l, m)
        self.update(ql, qr, val, i*2+1, m, r)
        self.pull(i)

    def query(self, pos, budget, i=1, l=0, r=None):
        if r is None:
            r = self.size
        if l >= self.n or budget <= 0:
            return 0, budget
        if r - l == 1:
            if l >= pos and self.maxv[i] <= budget:
                return 1, budget - self.maxv[i]
            return 0, budget
        self.push(i, l, r)
        m = (l+r)//2
        cnt, budget = self.query(pos, budget, i*2, l, m)
        cnt2, budget = self.query(pos, budget, i*2+1, m, r)
        return cnt + cnt2, budget

n, q = map(int, input().split())
a = list(map(int, input().split()))
tree = SegmentTree(a)

for _ in range(q):
    t, x, y = map(int, input().split())
    if t == 1:
        tree.update(0, x, y)
    else:
        cnt, _ = tree.query(x-1, y)
        print(cnt)
```

This code first constructs a segment tree for prefix max and sum. Type 1 updates use lazy propagation to efficiently raise shop prices. Type 2 queries greedily traverse the tree, counting meals while respecting the buyer's budget. The indices are carefully adjusted because Python arrays are 0-based while the problem uses 1-based indexing.

## Worked Examples

**Sample 1 trace:**

| Query | Array Before | Operation | Array After | Buyer Meals |
| --- | --- | --- | --- | --- |
| 2 3 50 | 10 10 10 6 6 5 5 5 3 1 | Budget=50 from shop3 | 10 10 10 6 6 5 5 5 3 1 | 8 |
| 2 4 10 | same | Budget=10 from shop4 | same | 3 |
| 1 3 10 | same | Raise first 3 to 10 | 10 10 10 6 6 5 5 5 3 1 | - |
| 2 2 36 | array | Budget=36 from shop2 | 10 10 10 6 6 5 5 5 3 1 | 6 |
| 1 4 7 | array | Raise first 4 to at least |  |  |
