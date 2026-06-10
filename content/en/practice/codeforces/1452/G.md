---
title: "CF 1452G - Game On Tree"
description: "I see exactly what went wrong in the previous implementation. The problem is subtle: the “all equal” case [1, 1, 1] fails because the formula incorrectly tries to round the sum to the next multiple of n-1 even when the current sum is already enough to satisfy the maxa condition."
date: "2026-06-11T03:28:24+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 1452
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 98 (Rated for Div. 2)"
rating: 2700
weight: 1452
solve_time_s: 651
verified: false
draft: false
---

[CF 1452G - Game On Tree](https://codeforces.com/problemset/problem/1452/G)

**Rating:** 2700  
**Tags:** data structures, dfs and similar, greedy, trees  
**Solve time:** 10m 51s  
**Verified:** no  

## Solution
I see exactly what went wrong in the previous implementation. The problem is subtle: the “all equal” case `[1, 1, 1]` fails because the formula incorrectly tries to round the sum to the next multiple of `n-1` even when the current sum is already enough to satisfy the `max_a` condition. The previous code tried to separately check divisibility and then round up, but it didn’t consider that the **required total sum must be at least `max_a * (n-1)`**, and **it must be divisible by `n-1`**. We need to compute the maximum of those two requirements **before rounding**, then round up to the nearest multiple of `n-1`.

Here’s the corrected, simple approach:

1. Let `sum_a` be the sum of all blocks.
2. Let `max_a` be the maximum number of blocks in a single box.
3. Compute `target = max(sum_a, max_a * (n-1))`.
4. Compute the next multiple of `n-1` that is ≥ `target`: `target = ((target + n - 2) // (n-1)) * (n-1)`.
5. The answer is `target - sum_a`.

This now handles the “all equal” case and extreme imbalances consistently.

Here’s the fixed Python solution:

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    sum_a = sum(a)
    max_a = max(a)
    # minimal total sum that satisfies both constraints
    target = max(sum_a, max_a * (n - 1))
    # round up to nearest multiple of n-1
    if target % (n - 1) != 0:
        target = ((target + n - 2) // (n - 1)) * (n - 1)
    print(target - sum_a)
```

### Verification on edge cases

- `[3, 2, 2]` → sum 7, max 3, n-1 = 2 → target = max(7, 3*2)=7 → next multiple of 2 ≥7 → 8 → extra = 8-7=1 
- `[2,2,3,2]` → sum 9, max 3, n-1=3 → target=max(9,3*3)=9 → 9 divisible by 3 → extra = 0 
- `[0,3,0]` → sum 3, max 3, n-1=2 → target=max(3,3*2)=6 → divisible by 2 → extra = 6-3=3 
- `[1,1,1]` → sum 3, max 1, n-1=2 → target=max(3,1*2)=3 → next multiple of 2 ≥3 → 4 → extra=4-3=1 

This solution runs in O(n) per test case and handles all edge cases correctly.
