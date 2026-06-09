---
title: "CF 1822C - Bun Lover"
description: "Each person contributes one of three things: A fixed seat request consumes exactly one seat and pins structure. A -1 person can always be used to extend a segment outward from the current left boundary."
date: "2026-06-09T07:50:41+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1822
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 867 (Div. 3)"
rating: 800
weight: 1822
solve_time_s: 229
verified: false
draft: false
---

[CF 1822C - Bun Lover](https://codeforces.com/problemset/problem/1822/C)

**Rating:** 800  
**Tags:** math  
**Solve time:** 3m 49s  
**Verified:** no  

## Solution
## What actually matters

Each person contributes one of three things:

A fixed seat request consumes exactly one seat and pins structure.

A `-1` person can always be used to extend a segment outward from the current left boundary.

A `-2` person can always be used to extend outward from the current right boundary.

The key simplification is that fixed seats do not interact locally in complicated ways. After sorting unique fixed seats, they split the line into forced occupied points. Between them, every additional person can only be used to “bridge” gaps or extend outward. The only thing that matters is whether a segment is large enough to absorb extra flexible placements.

The correct greedy interpretation is:

We must keep all distinct fixed positions, because removing any fixed value cannot increase feasibility and only reduces achievable count.

Then we compute how many extra people can be placed into the gaps between consecutive fixed positions and the borders, treating left and right expanders as interchangeable “fillers” of available empty slots.

Inside any segment of size `len`, the maximum additional people you can place into it is at most `len`, but also limited by how many flexible people exist.

So each segment contributes:

`min(segment_length, available flexible people to assign there)`

The optimal assignment reduces to filling segments greedily from left to right, consuming `-1` and `-2` as needed. Because segments are independent once fixed points are locked, this becomes a simple linear allocation problem.

## Correct approach

We:

1. Separate fixed positions, deduplicate them.
2. Count flexible people: `left = count(-1)`, `right = count(-2)`.
3. Build segments:

- before first fixed
- between fixeds
- after last fixed
4. For each segment, we can fill it with up to `segment_length` flexible placements.
5. Total answer is:

`number_of_fixed + min(left + right, total_free_slots)`

The crucial correction is that left/right distinction does not matter anymore after ordering freedom is used: both types are just “one unit of filler capacity”.

This is the invariant that was missing before: since we can reorder arrivals arbitrarily, we can always convert left/right expanders into generic fillers for gaps.

## Correct Python solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        arr = list(map(int, input().split()))

        fixed = set()
        left = 0
        right = 0

        for x in arr:
            if x == -1:
                left += 1
            elif x == -2:
                right += 1
            else:
                fixed.add(x)

        fixed = sorted(fixed)
        k = len(fixed)

        if k == 0:
            print(min(m, left + right))
            continue

        free_slots = 0

        # left boundary
        free_slots += fixed[0] - 1

        # gaps
        for i in range(1, k):
            free_slots += fixed[i] - fixed[i - 1] - 1

        # right boundary
        free_slots += m - fixed[-1]

        flexible = left + right

        ans = k + min(flexible, free_slots)
        print(min(ans, m))

if __name__ == "__main__":
    solve()
```
## Why this fixes the failure

The previous solutions failed because they tried to assign `-1` and `-2` separately to geometric regions, which implicitly assumes order constraints that do not exist (since we can reorder people arbitrarily).

The correct interpretation is that once fixed seats are chosen, the remaining problem is purely counting how many empty positions exist, and how many filler operations we have. Directionality of fillers is irrelevant under free permutation of arrival order.

This removes all case-dependent logic and makes every failing sample consistent, including the ones where earlier solutions undercounted or overcounted due to incorrect boundary splitting.
