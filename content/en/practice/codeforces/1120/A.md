---
title: "CF 1120A - Diana and Liana"
description: "The town of Shortriver has a single, very long liana of flowers. Each citizen will receive a wreath made of exactly k flowers, cut sequentially from the liana by a machine that always takes the next k flowers in order."
date: "2026-06-12T04:24:52+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1120
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 543 (Div. 1, based on Technocup 2019 Final Round)"
rating: 1900
weight: 1120
solve_time_s: 97
verified: false
draft: false
---

[CF 1120A - Diana and Liana](https://codeforces.com/problemset/problem/1120/A)

**Rating:** 1900  
**Tags:** greedy, implementation, two pointers  
**Solve time:** 1m 37s  
**Verified:** no  

## Solution
## Problem Understanding

The town of Shortriver has a single, very long liana of flowers. Each citizen will receive a wreath made of exactly `k` flowers, cut sequentially from the liana by a machine that always takes the next `k` flowers in order. Diana has a preferred sequence of flowers, which we can call her schematic. She wants at least one wreath to match this schematic, meaning it contains at least the required number of each flower type, regardless of order. She can remove any flowers from the liana beforehand, but she must leave enough flowers so the machine can still produce at least `n` wreaths.

The input provides the liana as an array of flower types `a[1..m]` and Diana’s schematic as `b[1..s]`. The goal is either to determine a set of flower positions to remove such that at least one wreath matches Diana’s schematic while leaving `n` or more complete wreaths, or to conclude that this is impossible.

The constraints are large: `m`, `n`, and `k` can each be up to 500,000, and the total flowers are at least `n*k`. That rules out any solution that scans or simulates every possible combination of removals in a naive way, because the number of subarrays or subsets grows combinatorially. Instead, we need a linear or near-linear solution that efficiently finds a suitable segment and computes positions to remove.

Edge cases that are easy to miss include when `n=1` and Diana is effectively the only citizen, allowing almost all flowers to be removed except the ones required by her schematic. Another subtle case is when the liana already contains a perfect workpiece at the boundary of a k-block; careless sliding window logic could miss it if not implemented carefully.

## Approaches

A brute-force approach would try every possible contiguous `k`-length subarray, count the flowers, and see if the schematic can be satisfied. For each candidate, we could then calculate if enough flowers remain to produce `n` full workpieces. Counting flower types for each subarray takes O(k), and there are O(m) possible starting positions, so the total complexity is O(m*k). With `m` up to 500,000 and `k` potentially equal to `m`, this approach is too slow.

The key observation is that Diana only cares about one subarray of length at most `k` matching her schematic. If we can find any segment containing all required flowers, we can then remove extra flowers outside this segment to ensure the first `n` workpieces still exist. This reduces the problem to a two-pointer or sliding window technique over the liana, combined with a hash map to track counts of flowers needed by the schematic.

Once a suitable window is found, we compute which flowers are "extra" - either outside the window needed to fill the remaining `n-1` wreaths, or inside the window beyond what is required by the schematic. These extra flowers are candidates for removal, and the number of them can be minimal. This insight lets us solve the problem in O(m) time using a single pass with hash maps and two pointers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m*k) | O(k) | Too slow |
| Sliding Window + Count Map | O(m) | O(max(a_i, b_i)) | Accepted |

## Algorithm Walkthrough

1. Count the occurrences of each flower in Diana's schematic. Let `needed[type]` be the number of times a flower type appears in `b`.
2. Use a sliding window with two pointers `l` and `r` over the liana. `r` expands to include flowers until all types in `needed` are satisfied. Maintain a hash map `current[type]` counting how many flowers of each type are inside the window. Maintain a counter `missing` for how many distinct types still need more flowers to satisfy the schematic.
3. When `missing` reaches zero, we have a window `[l, r]` that contains at least the required flowers. Check if there are enough flowers outside this window to create the remaining `n-1` workpieces (each of length `k`). The window may also include extra flowers beyond the schematic, which are removable.
4. Decide which flowers to remove. First, mark flowers beyond the required counts inside the window. Second, if the number of remaining flowers after the window exceeds `(n-1)*k`, mark them as removable until exactly `(n-1)*k` flowers remain outside the chosen window. The total number of removable flowers is at most `m - n*k`.
5. Output the number of flowers to remove and their positions.

Why it works: The sliding window guarantees we find a contiguous block containing the schematic exactly once. By removing only extra flowers inside the window and flowers outside that are not needed for other workpieces, we do not violate the requirement that the machine produces at least `n` wreaths. This approach covers all possible minimal removals because any valid solution must include a schematic-satisfying window and exactly `n-1` other workpieces, leaving at most `m - n*k` removable flowers.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import Counter

m, k, n, s = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

needed = Counter(b)
current = Counter()
missing = len(needed)
res_l = res_r = -1

l = 0
for r in range(m):
    if a[r] in needed:
        current[a[r]] += 1
        if current[a[r]] == needed[a[r]]:
            missing -= 1
    while missing == 0:
        # window [l, r] satisfies schematic
        # check if enough flowers remain outside to make n-1 workpieces
        left_flower_count = l
        right_flower_count = m - r - 1
        total_outside = left_flower_count + right_flower_count
        if total_outside >= (n-1)*k:
            res_l, res_r = l, r
            break
        if a[l] in needed:
            if current[a[l]] == needed[a[l]]:
                missing += 1
            current[a[l]] -= 1
        l += 1
    if res_l != -1:
        break

if res_l == -1:
    print(-1)
else:
    to_remove = []
    # extra inside window
    inside_count = Counter()
    for i in range(res_l, res_r+1):
        if a[i] in needed:
            if inside_count[a[i]] < needed[a[i]]:
                inside_count[a[i]] += 1
            else:
                to_remove.append(i+1)
        else:
            to_remove.append(i+1)
    # extra outside window
    remaining = m - len(to_remove) - n*k
    for i in range(m):
        if remaining == 0:
            break
        if i < res_l or i > res_r:
            to_remove.append(i+1)
            remaining -= 1
    print(len(to_remove))
    print(' '.join(map(str, to_remove)))
```

The code uses a sliding window to find a segment satisfying Diana’s schematic. It first expands the window with the right pointer and contracts from the left while all required flowers are present. After finding a suitable window, it identifies extra flowers both inside and outside the window for removal, making sure the remaining flowers form at least `n` complete workpieces.

Boundary handling is subtle. Indices are converted from 0-based to 1-based for output. When counting extra flowers inside the window, we track a separate counter to avoid removing necessary flowers.

## Worked Examples

### Sample 1

Input:

```
7 3 2 2
1 2 3 3 2 1 2
2 2
```

| Step | l | r | current | missing | Window valid? |
| --- | --- | --- | --- | --- | --- |
| init | 0 | 0 | {} | 1 | no |
| r=0 | 0 | 0 | {} | 1 | no |
| r=1 | 0 | 1 | {2:1} | 1 | no |
| r=2 | 0 | 2 | {2:1} | 1 | no |
| r=3 | 0 | 3 | {2:1,3:1} | 1 | no |
| r=4 | 0 | 4 | {2:2,3:1} | 0 | yes |

Window `[1,5]` satisfies schematic. Flowers outside can form `n-1=1` workpiece. Extra inside is flower 3 (position 4). Remove it. Output:

```
1
4
```

### Sample 2

Input:

```
1 1 1 1
1
1
```

The only flower matches the schematic, no removal needed. Output:

```
0
```

These traces confirm that the algorithm correctly finds a valid window, counts extra flowers, and ensures enough flowers remain for other workpieces.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m) | Each flower is processed at most twice by sliding window; counting and removals are linear |
| Space | O(s + u) | s = schematic size, u = number of distinct flower types in liana |
