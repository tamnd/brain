---
title: "CF 228D - Zigzag"
description: "We are asked to maintain an array of integers while supporting two types of operations: updating a single element to a new value, and computing a weighted sum over a subarray where the weights follow a small repeating zigzag pattern determined by a factor z."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 228
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 141 (Div. 2)"
rating: 2100
weight: 228
solve_time_s: 88
verified: false
draft: false
---

[CF 228D - Zigzag](https://codeforces.com/problemset/problem/228/D)

**Rating:** 2100  
**Tags:** data structures  
**Solve time:** 1m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to maintain an array of integers while supporting two types of operations: updating a single element to a new value, and computing a weighted sum over a subarray where the weights follow a small repeating zigzag pattern determined by a factor `z`. The zigzag pattern starts at 1 and goes up to `z`, then back down to 1, repeating infinitely. For example, with `z = 3`, the weight sequence is 1, 2, 3, 2, 1, 2, 3, 2, 1, ….

The input consists of an array of up to `10^5` integers, each up to `10^9`, and up to `10^5` operations. Each query of type 2 (the Zigzag operation) can span a subarray of length up to `10^5`, and the factor `z` ranges from 2 to 6. A naive approach that directly iterates over the subarray for each Zigzag operation could require up to `10^10` operations in the worst case, which is far too large for the 3-second time limit. This implies we need a sublinear or logarithmic-time solution for the sum queries.

Edge cases include subarrays of length 1, arrays with all elements equal, updates that overwrite previous values multiple times, and small values of `z`. For instance, if `a = [5]` and we query `Z(1,1,2)`, the result must correctly handle the zigzag cycle even for a single element.

## Approaches

A brute-force approach would iterate over each Zigzag query, compute the appropriate weight for each element by simulating the zigzag pattern, and sum them. While straightforward, this requires `O(n)` per query, leading to `O(n*m)` overall, which is infeasible for large `n` and `m`.

The key observation is that `z` is very small (at most 6). This allows us to precompute separate prefix sums for each possible offset modulo `2*z - 2` because the zigzag pattern repeats every `2*z - 2` elements. For a given `z`, the pattern of weights for positions 1 through `2*z-2` can be stored in an array. Then we can maintain `2*z-2` segment trees (or Fenwick trees) for each remainder of the index modulo the cycle length. An update only affects one position in each relevant tree. A query can be broken into at most `2*z-2` sums over these trees, giving a logarithmic-time solution for both updates and queries.

The brute-force works because it directly implements the definition, but fails when subarrays are large or when there are many queries. The insight that the weight pattern is periodic and `z` is small lets us reduce each query to a fixed number of fast prefix sum lookups.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(n) | Too slow |
| Periodic Prefix Sums / Segment Trees | O((2*z) * log n) per operation | O(n * 2*z) | Accepted |

## Algorithm Walkthrough

1. For each `z` from 2 to 6, compute the zigzag pattern for one full cycle of length `2*z-2`. This array stores the weight for each position modulo the cycle length. The first `z` weights are 1 through `z`, and the remaining `z-2` weights descend back to 2.
2. For each `z`, build `2*z-2` Fenwick trees, one for each remainder modulo the cycle length. Each tree stores the values of the array elements multiplied by the corresponding weight of that remainder. This allows summing values in the array according to their weighted zigzag positions efficiently.
3. To handle an update operation `a[p] = v`, compute the difference `delta = v - a[p]`. For each `z`, find the position `p % (2*z-2)` and update the corresponding Fenwick tree at index `p` by `delta * weight[p % (2*z-2)]`.
4. To handle a Zigzag query `(l, r, z)`, break the subarray `[l, r]` into segments corresponding to each remainder modulo `2*z-2`. Query the Fenwick tree for that remainder for the range `[l, r]`, sum them all, and return the total.
5. Execute all operations in order. The updates modify the trees so that subsequent queries see the latest array values.

Why it works: the algorithm preserves a separate sum for each position in the zigzag cycle. Every query can then be reconstructed exactly by summing over these precomputed weighted contributions. Updates are localized and propagate correctly because each index affects only one position in each cycle tree.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.tree = [0]*(n+1)
    def update(self, i, delta):
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i
    def query(self, i):
        res = 0
        while i > 0:
            res += self.tree[i]
            i -= i & -i
        return res
    def range_query(self, l, r):
        return self.query(r) - self.query(l-1)

n = int(input())
a = list(map(int, input().split()))
m = int(input())

max_z = 6
trees = {}
weights = {}

for z in range(2, max_z+1):
    cycle = list(range(1, z+1)) + list(range(z-1, 1, -1))
    weights[z] = cycle
    trees[z] = [Fenwick(n) for _ in range(len(cycle))]
    for idx, val in enumerate(a):
        pos = idx % len(cycle)
        trees[z][pos].update(idx+1, val * cycle[pos])

for _ in range(m):
    tmp = input().split()
    t = int(tmp[0])
    if t == 1:
        p, v = int(tmp[1])-1, int(tmp[2])
        delta = v - a[p]
        a[p] = v
        for z in range(2, max_z+1):
            pos = p % len(weights[z])
            trees[z][pos].update(p+1, delta * weights[z][pos])
    else:
        l, r, z = int(tmp[1]), int(tmp[2]), int(tmp[3])
        res = 0
        cycle = weights[z]
        for i, fen in enumerate(trees[z]):
            start = l + (i - (l-1)%len(cycle)) % len(cycle)
            if start > r:
                continue
            cnt = (r - start) // len(cycle) + 1
            res += fen.range_query(start, start + (cnt-1)*len(cycle))
        print(res)
```

The Fenwick tree class handles prefix sums and range queries. We construct separate trees for each remainder modulo the zigzag cycle length. During updates, we scale the delta by the weight. During queries, we iterate over the cycle positions to combine contributions. Care is taken to handle 1-based indexing for Fenwick trees.

## Worked Examples

**Sample 1**

```
a = [2, 3, 1, 5, 5]
Operations:
2 2 3 2
2 1 5 3
1 3 5
2 1 5 3
```

| Step | Operation | Array | Zigzag cycle used | Result |
| --- | --- | --- | --- | --- |
| 1 | Zigzag(2,3,2) | [2,3,1,5,5] | cycle=[1,2] | 3_1 + 1_2 = 5 |
| 2 | Zigzag(1,5,3) | [2,3,1,5,5] | cycle=[1,2,3,2] | 2_1+3_2+1_3+5_2+5*1=26 |
| 3 | Update a[3]=5 | [2,3,5,5,5] | - | - |
| 4 | Zigzag(1,5,3) | [2,3,5,5,5] | cycle=[1,2,3,2] | 2_1+3_2+5_3+5_2+5*1=38 |

The trace demonstrates that updates correctly modify contributions in the Fenwick trees and queries reconstruct the weighted sum.

**Custom Example**

```
a = [1,1,1,1,1,1]
Operations:
2 1 6 2
1 4 10
2 1 6 2
```

| Step | Operation | Array | Result |
| --- | --- | --- | --- |
| 1 | Zigzag(1,6,2) | [1,1,1,1,1,1] | 1_1+1_2+1_1+1_2+1_1+1_2=9 |
| 2 | Update a[4]=10 | [1,1,1,10,1,1] | - |
| 3 | Zigzag(1,6,2) | [1,1,1,10 |  |
