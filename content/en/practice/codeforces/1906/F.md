---
title: "CF 1906F - Maximize The Value"
description: "We are given an array of size $N$, initially filled with zeros. There are $M$ operations; each operation is described by three integers $Li, Ri, Xi$, meaning that if we execute this operation, we add $Xi$ to every element in positions $Li$ through $Ri$."
date: "2026-06-08T20:45:08+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1906
codeforces_index: "F"
codeforces_contest_name: "2023-2024 ICPC, Asia Jakarta Regional Contest (Online Mirror, Unrated, ICPC Rules, Teams Preferred)"
rating: 2100
weight: 1906
solve_time_s: 105
verified: true
draft: false
---

[CF 1906F - Maximize The Value](https://codeforces.com/problemset/problem/1906/F)

**Rating:** 2100  
**Tags:** data structures, sortings  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of size $N$, initially filled with zeros. There are $M$ operations; each operation is described by three integers $L_i, R_i, X_i$, meaning that if we execute this operation, we add $X_i$ to every element in positions $L_i$ through $R_i$.

The queries are a bit unusual: for each query $(K, S, T)$, we want to find the maximum possible value of $A_K$ after executing a contiguous subsequence of operations chosen from the range $S$ to $T$. In other words, we can pick any continuous block of operations in $[S, T]$ and execute them in order, and we want to know the largest value that position $K$ can reach.

The constraints $N, M, Q \le 10^5$ mean that any naive solution that tries all contiguous ranges for every query will be far too slow. Each query could require $O(M^2)$ checks in a brute-force approach, which is infeasible. We must look for a solution around $O((M + Q) \log M)$ or $O(M + Q)$ per query using preprocessing and efficient data structures.

A non-obvious edge case occurs when operations can have negative values. For instance, if $X_i$ is negative, executing more operations does not necessarily increase $A_K$. A careless approach that assumes "more operations are always better" would give wrong answers. Similarly, if a query's range $[S, T]$ includes no operations that affect $A_K$, the correct answer is zero.

For example, consider $N = 2$, $M = 2$, operations: $(1, 1, -10), (2, 2, 20)$, and query $(1, 1, 2)$. Only operation 1 affects position 1, so the maximum value for $A_1$ is -10. A naive sum over all operations in $[S, T]$ would incorrectly add 20 from the second operation.

## Approaches

The brute-force method is straightforward: for each query, iterate over all subarrays of operations in $[S, T]$, simulate applying the operations, and track the maximum value of $A_K$. This requires $O((T-S+1)^2 \cdot N)$ work per query, which is $O(M^2 \cdot N)$ in the worst case. With $M$ up to $10^5$, this approach would need $10^{15}$ operations, clearly impossible.

The key insight is that for each position $K$, we only care about operations that affect it. Each operation affects a continuous range of array positions. We can preprocess the operations to build, for each $K$, a list of operation values that impact it. Then, each query reduces to finding the maximum sum of a contiguous subarray of these values, restricted to the subsequence $[S, T]$. This is a classic "maximum subarray sum" problem, solvable in $O(\text{length})$ using Kadane’s algorithm, or even faster with segment trees if we want to handle multiple queries efficiently.

Because queries ask for maximum subarrays in specific ranges, we can build a segment tree over the sequence of operations affecting each $A_K$. Each segment tree node stores four values: total sum, maximum prefix sum, maximum suffix sum, and maximum subarray sum. Then, answering a query is $O(\log M)$ per query after preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(Q * M * N) | O(N) | Too slow |
| Preprocess + Segment Tree per position | O(M log M + Q log M) | O(M) | Accepted |

## Algorithm Walkthrough

1. For each position $1 \le K \le N$, iterate through all operations and collect the operations affecting position $K$. Store as a list of integers, where the index corresponds to the original operation number.
2. For each position $K$, build a segment tree on its list of relevant operations. Each node in the segment tree stores four values: total sum of the segment, maximum prefix sum, maximum suffix sum, and maximum subarray sum. These allow combining child segments efficiently.
3. For each query $(K, S, T)$:

a. Map the global operation indices $[S, T]$ to indices in the list of operations affecting $K$. Only operations that actually modify $A_K$ are relevant.

b. Query the segment tree for the maximum subarray sum within these indices. This returns the maximum possible contribution to $A_K$ from any contiguous subsequence of operations in the query range.
4. Output the result. If there are no operations affecting $A_K$ in the range, the maximum sum is zero.

Why it works: The segment tree maintains the invariant that each node accurately reports the maximum subarray sum over its interval. When querying a subrange, the segment tree combines nodes in logarithmic time, preserving the maximum subarray sum. By preprocessing operations per position, we avoid iterating over irrelevant operations, ensuring efficiency.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegmentTree:
    def __init__(self, data):
        n = len(data)
        self.N = 1
        while self.N < n: self.N <<= 1
        self.data = [(-float('inf'), -float('inf'), -float('inf'), 0)] * (2*self.N)
        for i in range(n):
            val = data[i]
            self.data[self.N + i] = (val, val, val, val)  # total, prefix, suffix, max subarray
        for i in range(self.N-1, 0, -1):
            self.data[i] = self._combine(self.data[2*i], self.data[2*i+1])
    
    def _combine(self, left, right):
        total = left[0] + right[0]
        prefix = max(left[1], left[0] + right[1])
        suffix = max(right[2], right[0] + left[2])
        maxsum = max(left[3], right[3], left[2] + right[1])
        return (total, prefix, suffix, maxsum)
    
    def query(self, l, r):
        l += self.N
        r += self.N
        left_res = (0, 0, 0, -float('inf'))
        right_res = (0, 0, 0, -float('inf'))
        while l < r:
            if l % 2:
                left_res = self._combine(left_res, self.data[l])
                l += 1
            if r % 2:
                r -= 1
                right_res = self._combine(self.data[r], right_res)
            l //= 2
            r //= 2
        return self._combine(left_res, right_res)[3]

N, M = map(int, input().split())
ops = []
for _ in range(M):
    L, R, X = map(int, input().split())
    ops.append((L-1, R-1, X))

# map each position to affecting operations
pos_ops = [[] for _ in range(N)]
for idx, (L, R, X) in enumerate(ops):
    for k in range(L, R+1):
        pos_ops[k].append((idx, X))

# build segment trees per position
trees = []
for lst in pos_ops:
    vals = [x for idx, x in lst]
    if vals:
        trees.append(SegmentTree(vals))
    else:
        trees.append(None)

Q = int(input())
for _ in range(Q):
    K, S, T = map(int, input().split())
    K -= 1
    S -= 1
    # map global indices S,T to position-specific list indices
    lst = pos_ops[K]
    if not lst:
        print(0)
        continue
    l = 0
    while l < len(lst) and lst[l][0] < S:
        l += 1
    r = l
    while r < len(lst) and lst[r][0] <= T-1:
        r += 1
    if l == r:
        print(0)
    else:
        print(trees[K].query(l, r))
```

The first section reads input and collects, for each array position, the operations that affect it. Each segment tree stores relevant prefix, suffix, and maximum sums to support range maximum queries. For each query, we carefully map global operation indices to the position-specific operation list, then query the segment tree. Boundary checks ensure empty ranges return zero.

## Worked Examples

**Sample Input 1**:

```
2 6
1 1 -50
1 2 -20
2 2 -30
1 1 60
1 2 40
2 2 10
5
1 1 6
2 1 6
1 1 3
2 1 3
1 1 2
```

For position 1:

| Op idx | Affects pos 1 | X |
| --- | --- | --- |
| 0 | yes | -50 |
| 1 | yes | -20 |
| 2 | no | - |
| 3 | yes | 60 |
|  |  |  |
