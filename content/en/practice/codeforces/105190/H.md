---
title: "CF 105190H - How Ali Sees Black"
description: "Let dp[n] be the minimum number of operations needed for the initial set {1,2,...,n}. Suppose the first operation chooses x. The element x disappears immediately. Every value smaller than x stays unchanged, while every value larger than x is reduced by x."
date: "2026-06-27T04:20:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105190
codeforces_index: "H"
codeforces_contest_name: "Al-Baath Collegiate Programming Contest 2024"
rating: 0
weight: 105190
solve_time_s: 36
verified: true
draft: false
---

[CF 105190H - How Ali Sees Black](https://codeforces.com/problemset/problem/105190/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
Let `dp[n]` be the minimum number of operations needed for the initial set `{1,2,...,n}`.

Suppose the first operation chooses `x`.

The element `x` disappears immediately. Every value smaller than `x` stays unchanged, while every value larger than `x` is reduced by `x`. After removing zero, the remaining values are exactly the union of

`{1,2,...,x-1}` and `{1,2,...,n-x}`.

The two parts are completely independent. Since duplicate values never make the problem harder, the remaining work is determined only by the larger of these two ranges. The larger size is

`max(x-1, n-x)`.

Hence

`dp[n] = 1 + min(max(dp[x-1], dp[n-x]))`.

The best choice is always to split the range as evenly as possible, so

`max(x-1, n-x) = floor(n/2)`,

giving the much simpler recurrence

`dp[0] = 0`

`dp[n] = dp[n//2] + 1`.

For `n ≤ 100`, a tiny DP is enough.

```python
import sys
input = sys.stdin.readline

n = int(input())

dp = [0] * (n + 1)
for i in range(1, n + 1):
    dp[i] = dp[i // 2] + 1

print(dp[n])
```

This recurrence is equivalent to the closed form

`dp[n] = floor(log2(n)) + 1` for `n ≥ 1`. Thus, for example, `n = 47` gives `5 + 1 = 6`, matching the sample.
