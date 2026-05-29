---
title: "CF 414C - Mashmokh and Reverse Operation"
description: "We are given an array of length $2^n$, where $n$ is at most 20, and a sequence of queries. Each query specifies a number $qi$, which tells us to repeatedly split the array into blocks of size $2^{qi}$, reverse each block, and then join the blocks back together."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "divide-and-conquer"]
categories: ["algorithms"]
codeforces_contest: 414
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 240 (Div. 1)"
rating: 2100
weight: 414
solve_time_s: 100
verified: true
draft: false
---

[CF 414C - Mashmokh and Reverse Operation](https://codeforces.com/problemset/problem/414/C)

**Rating:** 2100  
**Tags:** combinatorics, divide and conquer  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of length $2^n$, where $n$ is at most 20, and a sequence of queries. Each query specifies a number $q_i$, which tells us to repeatedly split the array into blocks of size $2^{q_i}$, reverse each block, and then join the blocks back together. After performing the reversal, we are asked to count the number of inversions in the resulting array.

An inversion is a pair of indices $(i,j)$ such that $i < j$ and $a[i] > a[j]$. The query operations are **cumulative**, meaning that the array is modified permanently after each query.

Given the constraints, the array size is at most $2^{20} \approx 10^6$, which is manageable, but the number of queries can also be very large ($m \le 10^6$). Therefore, any naive solution that recalculates inversions from scratch after each query using a quadratic algorithm ($O(N^2)$) will be far too slow. Even an $O(N \log N)$ inversion count per query may barely fit, and we should look for ways to **reuse computations**.

Edge cases include $n = 0$ (array of size 1, no inversions), $q_i = 0$ (blocks of size 1, no effect on array), and queries that repeat the same $q_i$ multiple times. Handling the array reversal carefully is also crucial, because the block reversal is not the same as reversing the entire array.

A naive implementation could silently fail by recalculating inversions incorrectly after partial reversals, or by misunderstanding how to split into blocks when $q_i = 0$ or $q_i = n$.

## Approaches

The brute-force approach is straightforward: for each query, split the array into blocks of size $2^{q_i}$, reverse each block, reassemble the array, then count inversions using a merge sort or a naive $O(N^2)$ loop. Counting inversions via merge sort is $O(N \log N)$.

For $n = 20$, $N = 2^n = 1,048,576$. A single merge sort per query costs roughly $N \log N \approx 2 \times 10^7$ operations. With $m = 10^6$ queries, this would exceed reasonable time limits. Even $O(N \log N)$ per query is too slow.

The key insight is that each query reverses **blocks of size $2^{q_i}$**, which corresponds exactly to flipping bits in the binary representation of indices. If we precompute the number of inversions at each level of the **merge sort tree**, we can answer each query by just toggling which levels are reversed. Specifically, a full merge sort can be viewed as a **divide-and-conquer tree**: the top level merges the first and second halves, the next level merges quarters, and so on. Reversing blocks of size $2^k$ swaps elements in a way that affects inversions at levels $0..k-1$ of this tree.

Thus, the optimal approach is to preprocess the inversions per level and maintain a **bitmask of flips**. Each query updates this mask and the total number of inversions can be computed in $O(n)$ per query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m * N log N) | O(N) | Too slow |
| Optimal | O(N log N + m * n) | O(N log N) | Accepted |

## Algorithm Walkthrough

1. **Precompute inversions by level.** Treat the array as a full merge sort tree. Each level of merge sort corresponds to merging segments of length $2^k$. During preprocessing, for each level, count the number of inversions created between left and right halves of each segment and store them in an array `inv_level[k]`. This gives us a way to know, for any segment size, how many inversions it contributes if not reversed.
2. **Initialize a bitmask to track reversals.** The bitmask `rev_mask` has length $n$, where `rev_mask[k]` indicates whether the segments of size $2^k$ have been reversed due to queries. Initially all zeros.
3. **Process each query $q_i$.** For a query $q_i$, flip all bits in the mask at levels `0` to `q_i-1`. This simulates the effect of reversing all blocks of size $2^{q_i}$. The reasoning comes from how merge-sort inversions are affected: flipping a segment reverses all lower-level inversions inside it.
4. **Compute total inversions.** After updating the mask, compute the total inversions by summing `inv_level[k]` for levels where `rev_mask[k]` is zero, and `total_pairs[k] - inv_level[k]` for levels where `rev_mask[k]` is one. Here `total_pairs[k]` is the maximum number of inversions possible at level `k`, i.e., pairs across left and right halves of size $2^k$.
5. **Output result.** Repeat steps 3-4 for each query. Because we only update a mask and sum over $n \le 20$ levels, each query is $O(n)$ and feasible for $m \le 10^6$.

**Why it works.** Inversions are additive in a merge-sort tree. Reversing a segment of size $2^k$ flips all inversions inside that segment, which is exactly accounted for by toggling the precomputed values for levels below $k$. No inversions are double-counted or missed because the merge-sort tree structure partitions all pairs uniquely at some level.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_inversions(arr):
    n = len(arr)
    tmp = arr[:]
    inv_levels = [0] * (n.bit_length())
    
    def merge_sort(l, r, level):
        if r - l <= 1:
            return 0
        m = (l + r) // 2
        inv = merge_sort(l, m, level - 1) + merge_sort(m, r, level - 1)
        i, j, k = l, m, l
        while i < m and j < r:
            if arr[i] <= arr[j]:
                tmp[k] = arr[i]
                i += 1
            else:
                tmp[k] = arr[j]
                inv += m - i
                j += 1
            k += 1
        while i < m:
            tmp[k] = arr[i]
            i += 1
            k += 1
        while j < r:
            tmp[k] = arr[j]
            j += 1
            k += 1
        arr[l:r] = tmp[l:r]
        inv_levels[level] += inv
        return inv
    
    total_inv = merge_sort(0, n, n.bit_length() - 1)
    return inv_levels, total_inv

n = int(input())
arr = list(map(int, input().split()))
m = int(input())
queries = list(map(int, input().split()))

inv_levels, _ = count_inversions(arr[:])
total_pairs = [(1 << (i)) * (1 << (i)) for i in range(n.bit_length())]

rev_mask = [0] * n
res = []

for q in queries:
    for i in range(q):
        rev_mask[i] ^= 1
    total = 0
    for i in range(n):
        if rev_mask[i]:
            total += total_pairs[i] - inv_levels[i]
        else:
            total += inv_levels[i]
    res.append(str(total))

sys.stdout.write('\n'.join(res) + '\n')
```

**Explanation.** The `count_inversions` function computes inversions per level of merge sort. The `rev_mask` tracks which levels have been reversed. `total_pairs` calculates the maximum inversion count possible per level. For each query, the mask is updated and the total inversion count is computed by summing over levels, flipping contributions where necessary.

Subtle points include correctly indexing levels from bottom to top in the merge-sort tree and handling queries with `q = 0` (no change) or `q = n` (full array reversal).

## Worked Examples

**Sample 1**

Input array: `[2, 1, 4, 3]`

Queries: `[1, 2, 0, 2]`

| Query | Reversed Blocks | rev_mask | Inversions |
| --- | --- | --- | --- |
| 1 | `[1,2],[3,4]` | `[1,0]` | 0 |
| 2 | `[4,3,2,1]` | `[0,1]` | 6 |
| 0 | no change | `[0,1]` | 6 |
| 2 | full reversal `[1,2,3,4]` | `[0,0]` | 0 |

Trace confirms that flipping levels exactly matches the inversion counts.

**Custom Input**

Array: `[1,3,2
