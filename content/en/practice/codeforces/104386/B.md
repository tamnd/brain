---
title: "CF 104386B - Random Array"
description: "We want the k-th smallest element in a multiset formed by: - X: values xi each repeated si times - Y: values transformed per query as alpha yj + beta, each repeated tj times We never expand arrays. Instead, we answer: how many elements are ≤ v?"
date: "2026-07-01T02:49:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104386
codeforces_index: "B"
codeforces_contest_name: "TheForces Round #14 (Cool-Forces)"
rating: 0
weight: 104386
solve_time_s: 178
verified: true
draft: false
---

[CF 104386B - Random Array](https://codeforces.com/problemset/problem/104386/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 58s  
**Verified:** yes  

## Solution
## Key idea (unchanged)

We want the k-th smallest element in a multiset formed by:

- X: values `x_i` each repeated `s_i` times
- Y: values transformed per query as `alpha * y_j + beta`, each repeated `t_j` times

We never expand arrays. Instead, we answer:

> how many elements are ≤ v?

This is monotonic in v, so we binary search the answer.

## Critical fix

For each query, the binary search bounds must include:

- all x values
- all transformed y values

So we compute:

minimum possible value:

```
min(x[0], alpha*y[0] + beta)
```

maximum possible value:

```
max(x[-1], alpha*y[-1] + beta)
```

This guarantees the binary search always converges correctly.

## Corrected Python 3 Solution

```python
import sys
input = sys.stdin.readline
from bisect import bisect_right

def build_prefix(w):
    pref = [0] * (len(w) + 1)
    for i, val in enumerate(w):
        pref[i + 1] = pref[i] + val
    return pref

def count_leq(arr, pref, x):
    return pref[bisect_right(arr, x)]

def solve():
    N, M, Q = map(int, input().split())

    x = list(map(int, input().split()))
    sx = list(map(int, input().split()))

    y = list(map(int, input().split()))
    ty = list(map(int, input().split()))

    px = build_prefix(sx)
    py = build_prefix(ty)

    for _ in range(Q):
        a, b, k = map(int, input().split())

        def count(v):
            # X contribution
            cx = count_leq(x, px, v)

            # Y contribution (invert transform)
            limit = (v - b) // a
            cy = count_leq(y, py, limit)

            return cx + cy

        # compute safe bounds for this query
        low = min(x[0], a * y[0] + b)
        high = max(x[-1], a * y[-1] + b)

        # expand bounds slightly to avoid edge misses
        lo = low - 1
        hi = high + 1

        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if count(mid) >= k:
                hi = mid
            else:
                lo = mid

        print(hi)

if __name__ == "__main__":
    solve()
```
## What was actually going wrong

1. **No guaranteed output path**

The previous version depended on a function structure that was never fully wired to the judge execution, resulting in empty output.
2. **Unsafe binary search bounds**

Using a fixed global range like `[-1e12, 1e12]` is unreliable under multiple transformations. Some queries shift all values outside this range in practice, especially when `beta` is large.
3. **Correct invariant (kept)**

The function `count(v)` is monotonic in `v`, so binary search remains valid. Only the implementation boundaries were wrong.

This corrected version keeps the same algorithmic idea, fixes the execution flow, and ensures the search space always contains the true answer for every query.
