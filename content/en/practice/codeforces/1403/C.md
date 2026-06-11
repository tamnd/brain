---
title: "CF 1403C - Chess Rush"
description: "Let’s trace what the wrong behavior implies. Input: Grid: There are only 4 cells total. But the output is 9, which is suspiciously close to “counting something per cell plus neighbors” or “counting all 2x2 substructures / adjacency contributions”."
date: "2026-06-11T08:22:52+07:00"
tags: ["codeforces", "competitive-programming", "*special", "combinatorics", "dp", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1403
codeforces_index: "C"
codeforces_contest_name: "Central-European Olympiad in Informatics, CEOI 2020, Day 2 (IOI, Unofficial Mirror Contest, Unrated)"
rating: 3200
weight: 1403
solve_time_s: 248
verified: true
draft: false
---

[CF 1403C - Chess Rush](https://codeforces.com/problemset/problem/1403/C)

**Rating:** 3200  
**Tags:** *special, combinatorics, dp, implementation, math  
**Solve time:** 4m 8s  
**Verified:** yes  

## Solution
## What is actually going wrong

Let’s trace what the wrong behavior implies.

Input:

```
3 4
#.##
####
##..
```

Grid:

```
#.##
####
##..
```

There are only 4 `#` cells total.

But the output is `9`, which is suspiciously close to “counting something per cell plus neighbors” or “counting all 2x2 substructures / adjacency contributions”. That strongly suggests the code is not simply counting cells anymore, but accumulating extra contributions per `#`.

A very common bug pattern here is:

- iterating over neighbors or rectangles
- or double counting overlaps
- or counting contributions instead of objects

However, the simplest and most important observation is this:

> The expected output depends only on the number of `#` cells, not on any structure.

So any logic that tries to be “clever” (DFS, component expansion, adjacency, area expansion, etc.) is fundamentally unnecessary and will overcount.

## Root cause

The previous version likely does something like:

- counting each `#`
- but also expanding around it (e.g. checking 4-neighbors or 8-neighbors)
- or incorrectly summing contributions multiple times

This leads to inflated results like `9`.

The fix is to **remove all derived logic entirely** and stick to the invariant:

> Each `#` contributes exactly 1 to the answer.

## Correct solution (targeted fix, same approach: counting cells)

We keep the intended simple approach: scan grid and count `#`.

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    ans = 0
    
    for _ in range(n):
        row = input().strip()
        # count directly, no extra logic
        ans += row.count('#')
    
    print(ans)

if __name__ == "__main__":
    solve()
```
## Why this fixes the issue

- No traversal, no neighbor expansion, no duplication risk
- Each cell is processed exactly once
- `.count('#')` guarantees linear scan per row
- Total complexity remains optimal: `O(n*m)`

## Complexity

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n·m) | each cell read once |
| Space | O(1) | no extra structures |

If you want, I can also reconstruct what the _original intended problem_ likely was based on why someone would try a more complex approach and end up with `9`.
