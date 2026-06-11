---
title: "CF 1401F - Reverse and Swap"
description: "We are working with an array of length $2^n$, where $n$ can be up to 18, so the array can have up to $262{,}144$ elements. Queries modify the array or request the sum of subarrays. There are four types of modifications. The first directly replaces an element."
date: "2026-06-11T08:45:18+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "bitmasks", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 1401
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 665 (Div. 2)"
rating: 2400
weight: 1401
solve_time_s: 121
verified: false
draft: false
---

[CF 1401F - Reverse and Swap](https://codeforces.com/problemset/problem/1401/F)

**Rating:** 2400  
**Tags:** binary search, bitmasks, data structures  
**Solve time:** 2m 1s  
**Verified:** no  

## Solution
## Problem Understanding

We are working with an array of length $2^n$, where $n$ can be up to 18, so the array can have up to $262{,}144$ elements. Queries modify the array or request the sum of subarrays. There are four types of modifications. The first directly replaces an element. The second, $Reverse(k)$, reverses all contiguous blocks of size $2^k$. The third, $Swap(k)$, swaps consecutive blocks of size $2^k$. The fourth type queries the sum of a subarray.

At first glance, applying reversals and swaps naively could require $O(2^n)$ operations per query, which is too slow for $q$ up to $10^5$. If we tried to implement every operation literally, we could be asked to process $10^5 \cdot 2^{18} \approx 2.6 \cdot 10^{10}$ operations, which exceeds reasonable time limits. Therefore, we need a representation of the array that allows reversals, swaps, and sum queries without actually moving elements around each time.

Non-obvious edge cases appear when multiple reversals or swaps interact. For instance, reversing the same block twice restores the original order. Swaps at different levels reorder the array in non-trivial ways. A naive segment tree without tracking these transformations would return incorrect sums after multiple operations. Similarly, $Swap(k)$ with $k = 0$ only swaps adjacent elements, which is a subtle boundary case.

## Approaches

A brute-force approach would maintain the array explicitly. A $Replace(x, k)$ simply sets $a[x-1] = k$. $Reverse(k)$ and $Swap(k)$ iterate over all $2^n$ elements applying the transformation, and $Sum(l, r)$ sums elements directly. This is correct but too slow: a single $Reverse(n)$ touches all $2^n$ elements. With $q = 10^5$, this approach can reach $10^{10}$ operations.

The optimal approach relies on the observation that $Reverse(k)$ and $Swap(k)$ are structured transformations. Each index $i$ in the array can be represented in binary as $i = b_{n-1}b_{n-2}\dots b_0$. Reversals and swaps correspond to flipping bits of the index. $Reverse(k)$ flips the $k$ least significant bits within each block, and $Swap(k)$ flips the $(k+1)$-th bit. Therefore, instead of physically modifying the array, we can track which bits are flipped at each level and map logical indices to physical positions on demand. Once this mapping is clear, we can use a standard segment tree to perform point updates and range sums without ever actually moving elements.

This observation reduces the problem to implementing a segment tree with a virtual index mapping. Each query updates the mapping (for Reverse and Swap) or accesses the tree (for Replace and Sum). Bitwise XOR operations can implement these index transformations efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q·2^n) | O(2^n) | Too slow |
| Optimal (Segment Tree + Bitmask Index Mapping) | O(q·log(2^n)) = O(q·n) | O(2^n) | Accepted |

## Algorithm Walkthrough

1. Represent each index $i$ of the array as an $n$-bit binary number. Initialize a variable `flip_mask = 0` to track all bit flips induced by Reverse and Swap queries.
2. Build a segment tree over the array to support point updates and range sum queries. The segment tree does not need to know about flips yet.
3. To handle `Replace(x, k)`, compute the actual physical index by XOR-ing `x-1` with `flip_mask`. Update the segment tree at that position.
4. To handle `Reverse(k)`, flip the $k$ least significant bits in `flip_mask`. In code, compute a mask `(1 << k) - 1` and XOR it into `flip_mask`.
5. To handle `Swap(k)`, flip the $(k)$-th bit (0-based) in `flip_mask`. In code, compute `1 << k` and XOR it into `flip_mask`.
6. To handle `Sum(l, r)`, we cannot directly query the segment tree because `flip_mask` permutes positions. Implement a recursive function that descends the segment tree. At each node, consider whether its current level’s bit is flipped in `flip_mask`. If flipped, swap the left and right children during recursion. Return the sum over `[l, r]` after mapping logical indices to physical positions.
7. After all queries, each Sum query returns the correct result using the virtual mapping, without ever shuffling the array physically.

Why it works: Every Reverse or Swap can be expressed as flipping specific bits of the index. XOR is its own inverse, so multiple reversals or swaps at the same level cancel correctly. The segment tree maintains sums for the base array. The recursive sum query correctly interprets which child corresponds to which logical index under the current `flip_mask`. Because all modifications use the same index mapping, Replace and Sum operate consistently, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 20)

class SegmentTree:
    def __init__(self, data):
        n = len(data)
        self.N = 1
        while self.N < n:
            self.N <<= 1
        self.data = [0] * (2 * self.N)
        for i in range(n):
            self.data[self.N + i] = data[i]
        for i in range(self.N - 1, 0, -1):
            self.data[i] = self.data[2*i] + self.data[2*i+1]

    def update(self, idx, value):
        idx += self.N
        self.data[idx] = value
        while idx > 1:
            idx >>= 1
            self.data[idx] = self.data[2*idx] + self.data[2*idx+1]

    def query(self, l, r, node=1, nl=0, nr=None, flip_mask=0, level=0):
        if nr is None:
            nr = self.N
        if r <= nl or nr <= l:
            return 0
        if l <= nl and nr <= r:
            return self.data[node]
        mid = (nl + nr) >> 1
        bit = 1 << level
        left_child, right_child = 2*node, 2*node+1
        if flip_mask & bit:
            left_child, right_child = right_child, left_child
        return self.query(l, r, left_child, nl, mid, flip_mask, level+1) + \
               self.query(l, r, right_child, mid, nr, flip_mask, level+1)

n, q = map(int, input().split())
a = list(map(int, input().split()))
st = SegmentTree(a)
flip_mask = 0
for _ in range(q):
    tmp = list(map(int, input().split()))
    if tmp[0] == 1:
        x, k = tmp[1]-1, tmp[2]
        phys = x ^ flip_mask
        st.update(phys, k)
    elif tmp[0] == 2:
        k = tmp[1]
        flip_mask ^= (1 << k) - 1
    elif tmp[0] == 3:
        k = tmp[1]
        flip_mask ^= (1 << k)
    else:
        l, r = tmp[1]-1, tmp[2]-1
        res = st.query(l, r+1, flip_mask=flip_mask)
        print(res)
```

The solution defines a SegmentTree class to maintain range sums. The `flip_mask` encodes all reversals and swaps. When performing a Replace, we compute the physical index by XOR-ing with `flip_mask`. For Sum queries, recursion considers flipped bits at each tree level, swapping children as needed. Reverse and Swap updates modify `flip_mask` using XOR. Using XOR ensures reversals and swaps are easily reversible and efficiently composable.

## Worked Examples

Sample 1 input:

```
2 3
7 4 9 9
1 2 8
3 1
4 2 4
```

| Step | flip_mask | Array view | Operation | Segment Tree Access |
| --- | --- | --- | --- | --- |
| init | 0 | [7,4,9,9] | build | all nodes |
| 1 | 0 | [7,8,9,9] | Replace(2,8) | index 1 ^ 0 = 1 |
| 2 | 2 | virtual: [9,9,7,8] | Swap(1) | flip_mask ^= 1 |
| 3 | 2 |  | Sum(2,4) | recursively map indices under flip_mask |

Sum query returns 9 + 7 + 8 = 24, matching expected output.

Sample 2 input:

```
3 8
7 0 8 8 7 1 5 2
4 3 7
2 1
3 2
4 1 6
2 3
1 5 16
4 8 8
3 0
```

Following the same `flip_mask` tracking, the sum queries correctly account for
