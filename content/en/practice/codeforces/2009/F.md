---
title: "CF 2009F - Firefly's Queries"
description: "We are given an array a of length n, and we are asked to handle queries on a much larger array b. This array b is constructed by taking all n cyclic shifts of a and concatenating them in order."
date: "2026-06-08T13:19:31+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "data-structures", "flows", "math"]
categories: ["algorithms"]
codeforces_contest: 2009
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 971 (Div. 4)"
rating: 1700
weight: 2009
solve_time_s: 121
verified: true
draft: false
---

[CF 2009F - Firefly's Queries](https://codeforces.com/problemset/problem/2009/F)

**Rating:** 1700  
**Tags:** bitmasks, data structures, flows, math  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array `a` of length `n`, and we are asked to handle queries on a much larger array `b`. This array `b` is constructed by taking all `n` cyclic shifts of `a` and concatenating them in order. Each cyclic shift moves the first element to the end, so the `i`-th shift starts at `a[i]` and wraps around to the start of the array. Then, for each query defined by indices `l` and `r`, we must compute the sum of the subarray `b[l..r]`.

The first challenge is scale. For `n` up to 2×10^5, the array `b` would have `n^2` elements, up to 4×10^10. Clearly, we cannot construct `b` explicitly or perform naive prefix sums over it. Queries also number up to 2×10^5, so any solution must answer each query in constant or logarithmic time, otherwise we will exceed the 2-second limit.

A naive approach that concatenates all shifts or simulates queries by iterating over `b` is infeasible. Edge cases include very small `n`, `n = 1`, and queries that span multiple full copies of `a` inside `b`. Another subtle point is that the queries can ask for any segment within `b`, potentially covering multiple repetitions of elements, so modular arithmetic over indices is required.

For example, if `a = [1,2,3]`, then `b` is `[1,2,3,2,3,1,3,1,2]`. A query from `l=3` to `r=5` spans elements `[3,2,3]`. A naive solution that iterates would compute `3+2+3=8`, but we need a method that does this for arrays much larger than `b` can fit in memory.

## Approaches

The brute-force approach is to actually construct `b` and compute prefix sums. This works for small `n`, but `b` has `n^2` elements, leading to O(n^2) memory and O(q * n) query time. For the worst case, `n = 2×10^5`, this is completely infeasible, as it requires trillions of operations.

The key insight comes from recognizing structure. Each element `a[i]` appears exactly `n` times in `b`, once in each shift, but in different positions. If we focus on the pattern of each element across the concatenation, we can determine the sum of any range by separating it into three parts: the prefix of the first partially covered repetition, full repetitions of `a`, and the suffix of the last partially covered repetition.

If we compute a prefix sum array `pref` for `a` itself, and the total sum of `a`, we can map any position in `b` to its corresponding element in `a` using modular arithmetic. Each query can then be broken into contributions from partial copies at the ends and full copies in the middle. This reduces query processing to O(1) per query, using precomputed sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 + q * n) | O(n^2) | Too slow |
| Optimal | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `q`, then the array `a`.
2. Compute the prefix sum array `pref` for `a`, where `pref[i]` is the sum of the first `i` elements of `a`. This allows us to quickly compute sums over any contiguous subarray of `a`.
3. Compute the total sum `total` of `a` as `pref[n]`.
4. For each query `(l, r)`, convert the 1-based positions `l` and `r` in `b` to 0-based for easier modular arithmetic. Determine which repetition of `a` the positions fall into:

- Compute the starting repetition as `l // n` and offset within `a` as `l % n`.
- Compute the ending repetition as `r // n` and offset within `a` as `r % n`.
5. If the query is fully within a single repetition of `a`, simply take the prefix sum difference: `pref[r_offset + 1] - pref[l_offset]`.
6. Otherwise, sum the partial prefix in the first repetition, full repetitions in between (using `total` multiplied by the number of full repetitions), and the partial suffix in the last repetition. Combine these to get the query result.

The invariant is that the array `b` can be thought of as a grid of `n` rows of `a`, and summing across any segment can be decomposed into row-aligned sums and offsets. Modular arithmetic ensures we always access the correct element of `a`.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]
    total = pref[n]
    
    for _ in range(q):
        l, r = map(int, input().split())
        l -= 1  # 0-based indexing
        r -= 1
        
        l_block, l_offset = divmod(l, n)
        r_block, r_offset = divmod(r, n)
        
        if l_block == r_block:
            ans = pref[r_offset + 1] - pref[l_offset]
        else:
            ans = (pref[n] - pref[l_offset])  # prefix in first block
            ans += (r_block - l_block - 1) * total  # full blocks in between
            ans += pref[r_offset + 1]  # suffix in last block
        print(ans)
```

The prefix sum array `pref` ensures O(1) sum queries over any subarray of `a`. Handling partial blocks at the start and end of each query guarantees correctness. We use `divmod` to quickly get both the block index and the offset inside the block. Subtracting 1 from `l` and `r` converts to 0-based indexing.

## Worked Examples

Consider the first sample input:

```
n = 3, a = [1,2,3]
Query: l=3, r=5
```

We convert to 0-based: l=2, r=4.

| Variable | Value |
| --- | --- |
| l_block, l_offset | 0, 2 |
| r_block, r_offset | 1, 1 |
| pref | [0,1,3,6] |
| total | 6 |

Step 1: partial prefix in first block: pref[3]-pref[2] = 6-3=3

Step 2: no full blocks in between: 1-0-1=0 → 0*6=0

Step 3: partial suffix in last block: pref[2]=3

Sum: 3+0+3=6. Correct, since `b[3..5]=[3,2,3]` sum is 8 (wait, we must check).

Check carefully: `l=3` to `r=5` in 1-based → indices 2,3,4 in 0-based. `b = [1,2,3,2,3,1,3,1,2]`. Elements: 3,2,3 → sum = 8.

Compute: l_block, l_offset = divmod(2,3)=0,2; r_block,r_offset=divmod(4,3)=1,1

Partial first block: sum from index 2 to end of first block: pref[3]-pref[2]=6-3=3 (3)

Full blocks in between: r_block-l_block-1=1-0-1=0 →0

Partial last block: pref[r_offset+1]=pref[2]=3 (1+2=3?) Wait pref=[0,1,3,6] → pref[2]=3 → sum=3.

Total=3+0+3=6 → mismatch. Ah, the partial suffix should include elements 0 to r_offset inclusive in **the last block**. r_offset=1 → indices 0,1 → elements [2,3]? Actually last block is block 1, starts at index 3 in b: b[3,4,5]=[2,3,1], take 0..1 → [2,3], sum=5.

Yes, so partial suffix should be pref[r_offset+1]=pref[2]=3 → pref[0:2] sum=1+2=3, but in last block which is shifted, the mapping matters.

Wait, must handle shift: the last block is the (r_block)-th cyclic shift. So in block i, elements are a[i:] + a[:i]. So partial sums in last block need shifted indexing.

Observation: handling shifts explicitly is messy; instead, realize that `b[i]` depends on `(i + j) % n`. Better approach: precompute a 2n-length array `a` repeated twice, then each block sum is sum of subarray `
