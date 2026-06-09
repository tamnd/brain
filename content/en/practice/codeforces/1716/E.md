---
title: "CF 1716E - Swap and Maximum Block"
description: "The array contains exactly $2^n$ elements. Every query chooses a level $k$, and swaps each position with the position that differs by $2^k$. The swaps are done simultaneously in disjoint pairs, so every block of size $2^{k+1}$ has its left half exchanged with its right half."
date: "2026-06-09T19:52:49+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "data-structures", "dfs-and-similar", "divide-and-conquer", "dp"]
categories: ["algorithms"]
codeforces_contest: 1716
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 133 (Rated for Div. 2)"
rating: 2500
weight: 1716
solve_time_s: 138
verified: true
draft: false
---

[CF 1716E - Swap and Maximum Block](https://codeforces.com/problemset/problem/1716/E)

**Rating:** 2500  
**Tags:** bitmasks, data structures, dfs and similar, divide and conquer, dp  
**Solve time:** 2m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

The array contains exactly $2^n$ elements. Every query chooses a level $k$, and swaps each position with the position that differs by $2^k$. The swaps are done simultaneously in disjoint pairs, so every block of size $2^{k+1}$ has its left half exchanged with its right half.

After applying the swap, we need the maximum sum among all contiguous subarrays, where the empty subarray is allowed and contributes zero.

The array itself changes permanently, so queries accumulate. We are not repeatedly applying the same operation to the original array, we are changing the current arrangement.

The size of the array is at most $2^{18}=262144$, which is moderate. A single Kadane pass is cheap, but there can be $2\cdot10^5$ queries. Rebuilding the array and recomputing the answer after every query would require roughly

$$2\cdot10^5 \times 2^{18}\approx 5\cdot10^{10}$$

operations, which is far beyond the limit.

The swap operation itself is deceptive. A query with $k=0$ swaps adjacent elements. Repeating it twice restores the original order. More generally, each level acts independently and can be viewed as flipping one bit in every index. The sequence of queries only determines which levels have been flipped an odd number of times.

Several situations easily lead to mistakes.

Suppose

```
n = 1
a = [-5, -7]
```

After the only possible query, the array becomes

```
[-7, -5]
```

The correct answer is 0 because the empty subarray is allowed. A careless implementation of Kadane that insists on choosing at least one element would output -5.

Another pitfall is forgetting that operations accumulate. For

```
n = 2
a = [1,2,3,4]
queries: 0,0
```

The first query gives

```
[2,1,4,3]
```

The second query restores

```
[1,2,3,4]
```

The answers are 10 and 10. Reapplying each query to the original array would accidentally produce the same first state twice.

The most subtle issue is understanding what a level swap does inside larger blocks. For

```
[1,2,3,4,5,6,7,8]
```

with $k=1$, every block of length four changes

```
[1,2,3,4] → [3,4,1,2]
[5,6,7,8] → [7,8,5,6]
```

The operation does not globally shift the array. It only exchanges halves inside blocks of size $2^{k+1}$.

## Approaches

The straightforward method is to maintain the current array explicitly. For each query we perform all required swaps, then run Kadane's algorithm to obtain the maximum subarray sum. This is correct because Kadane computes exactly the desired quantity.

Unfortunately, a query may touch all $2^n$ elements, and Kadane also scans the entire array. With $2\cdot10^5$ queries and $2^{18}$ elements, the total work becomes about $10^{11}$, which is hopeless.

The key observation is that every swap exchanges two halves of some segment. This is exactly the same structure as a segment tree. When a node represents a segment, its answer depends only on four numbers:

The total sum.

The maximum prefix sum.

The maximum suffix sum.

The maximum subarray sum.

These are the usual values used for maximum subarray queries.

Normally, the left child always comes before the right child. Here, a level flip may reverse their order inside every node of that height. Since each node has only two possible orientations, we can precompute both versions.

For every node we store two states.

State 0 means the children are concatenated in the normal order.

State 1 means the children are concatenated in reversed order.

When combining children, the reversed order simply swaps their roles. Because each node only has two possibilities, preprocessing remains linear.

A query toggles one level. All nodes of that height change orientation simultaneously. Instead of touching them individually, we maintain a bitmask describing which levels are flipped. Using that mask, we know which state should be used at the root. The root's maximum subarray value is the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(q2^n)$ | $O(2^n)$ | Too slow |
| Optimal | $O(2^n+q)$ | $O(2^n)$ | Accepted |

## Algorithm Walkthrough

1. Build a complete binary tree over the array.

Every node corresponds to a segment whose length is a power of two.
2. For a leaf, both orientations are identical.

The total sum equals the element itself. Prefix, suffix, and maximum subarray are all the element value if positive, otherwise zero because the empty subarray is allowed.
3. For an internal node, compute two versions.

Version 0 concatenates left child followed by right child.

Version 1 concatenates right child followed by left child.
4. To merge two segments $A$ and $B$, use the standard formulas.

Total sum is $A.sum+B.sum$.

Maximum prefix is the better of $A.pref$ and $A.sum+B.pref$.

Maximum suffix is the better of $B.suff$ and $B.sum+A.suff$.

Maximum subarray is the maximum among the best segment inside $A$, the best segment inside $B$, and a segment crossing the boundary, whose value is $A.suff+B.pref$.
5. Maintain a mask describing which levels have been flipped an odd number of times.

A query with value $k$ toggles bit $k$.
6. During preprocessing, number levels from the bottom.

For a node at height $h$, its orientation depends only on bit $h-1$ of the current mask.
7. The root has two precomputed states.

After updating the mask, select the root state corresponding to the highest bit pattern and output its maximum subarray value.

### Why it works

Each query independently swaps the two halves of every segment whose size is $2^{k+1}$. A node at that height experiences exactly one local reversal, while deeper or higher nodes are unaffected. Thus every node's ordering depends only on the parity of flips on its own level.

Because a node has only two possible orders, storing both possibilities completely describes every future arrangement. The merge formulas are exactly the same as those used in segment trees for maximum subarray sum, so the values computed for each orientation are correct. Since the root represents the whole array, its maximum subarray value equals the answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Node:
    __slots__ = ("sm", "pref", "suff", "best")

    def __init__(self, sm=0, pref=0, suff=0, best=0):
        self.sm = sm
        self.pref = pref
        self.suff = suff
        self.best = best

def merge(a, b):
    res = Node()
    res.sm = a.sm + b.sm
    res.pref = max(a.pref, a.sm + b.pref)
    res.suff = max(b.suff, b.sm + a.suff)
    res.best = max(a.best, b.best, a.suff + b.pref)
    return res

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    m = 1 << n

    dp = [[None, None] for _ in range(2 * m)]

    for i, x in enumerate(a):
        val = max(0, x)
        node = Node(x, val, val, val)
        dp[m + i][0] = node
        dp[m + i][1] = node

    for v in range(m - 1, 0, -1):
        left = v << 1
        right = left | 1

        dp[v][0] = merge(dp[left][0], dp[right][0])
        dp[v][1] = merge(dp[right][1], dp[left][1])

    orient = [0] * (n + 1)

    q = int(input())
    out = []

    for _ in range(q):
        k = int(input())
        level = k + 1
        orient[level] ^= 1

        cur = 1
        for h in range(n, 0, -1):
            bit = orient[h]
            cur = (cur << 1) | bit

        out.append(str(dp[cur][0].best))

    sys.stdout.write("\n".join(out))

solve()
```

Leaves store zero for negative prefix, suffix, and maximum values because the empty subarray is allowed.

The merge routine is the standard maximum-subarray merge. Only four numbers are required.

Each internal node stores two orientations. In one orientation the left child precedes the right child, and in the other orientation their order is reversed.

The orientation array keeps the parity of flips on every level. Since applying the same query twice cancels itself, only parity matters.

The implementation carefully distinguishes the segment-tree height from the query value. Query $k$ affects segments of length $2^{k+1}$, which corresponds to level $k+1$ when counting upward from the leaves.

## Worked Examples

### Example 1

Input

```
3
-3
```
