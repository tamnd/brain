---
title: "CF 1473D - Program"
description: "We are given a program that manipulates a single integer variable x, starting from 0. Each instruction either increments or decrements x by 1."
date: "2026-06-11T00:23:39+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1473
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 102 (Rated for Div. 2)"
rating: 1700
weight: 1473
solve_time_s: 106
verified: true
draft: false
---

[CF 1473D - Program](https://codeforces.com/problemset/problem/1473/D)

**Rating:** 1700  
**Tags:** data structures, dp, implementation, strings  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a program that manipulates a single integer variable `x`, starting from `0`. Each instruction either increments or decrements `x` by `1`. Then, we are asked a series of queries: for each query, ignore a contiguous subsequence of instructions and determine how many distinct values `x` takes when executing the remaining instructions in order. The output for a query is simply the count of distinct values `x` achieves.

The constraints are significant. Each program can have up to 200,000 instructions, and there can be up to 200,000 queries. Across all test cases, the sum of instructions and queries is also capped at 200,000. This immediately rules out any solution that simulates the program from scratch for every query, because that could take on the order of $O(n \cdot m)$ operations, which can be $4 \cdot 10^{10}$ in the worst case. We need a solution that preprocesses information so that each query can be answered in constant or logarithmic time.

An important subtlety is that ignoring a subsequence can shift all subsequent values by a fixed offset. For example, consider a program "+-+-" and a query ignoring instructions 2 through 3. The resulting sequence is "+-" from instructions 1 and 4, but the relative min and max of `x` change based on the cumulative effect of the ignored instructions. Careless solutions that just recompute the sequence naively will overcount or undercount distinct values. Similarly, queries that remove the first or last instructions must correctly handle boundary conditions where the program might become empty.

## Approaches

The naive approach is straightforward: for each query, construct a new program sequence by skipping the instructions from `l` to `r`, simulate `x` step by step, record all values, and return the count of distinct values. This works correctly for small inputs, but it is extremely inefficient. If `n` and `m` are each $2 \cdot 10^5$, this could require $O(n \cdot m) = 4 \cdot 10^{10}$ operations, which is far beyond the 2-second limit.

The key insight is that we can preprocess prefix and suffix information about the program. If we know, for each position, the minimum and maximum `x` value reached up to that point (prefix) and from that point to the end (suffix), we can answer any query by combining the prefix before the ignored segment and the suffix after it. The ignored segment contributes a net change `delta`, which is the sum of increments and decrements in that segment. The values in the suffix shift by this `delta` when concatenated after the prefix. We do not need to simulate the entire program; it suffices to track the minimum and maximum `x` in both prefix and suffix and adjust them based on the net change of the ignored segment.

This reduces the per-query computation to constant time after linear preprocessing. The preprocessing computes prefix min/max and suffix min/max arrays in $O(n)$. Each query uses these arrays to compute the effective min and max across the remaining instructions and outputs the number of distinct values as `max_val - min_val + 1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(n) | Too slow |
| Optimal | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert the program string into an array `a` where `a[i] = 1` for '+' and `a[i] = -1` for '-'. This allows numerical operations instead of string processing.
2. Construct prefix sums `pref[i]` such that `pref[i]` is the value of `x` after executing the first `i` instructions. Initialize `pref[0] = 0`.
3. Compute prefix minimum `pref_min[i]` and prefix maximum `pref_max[i]` arrays. `pref_min[i]` is the smallest value `x` reaches from the beginning to instruction `i`. `pref_max[i]` is the largest.
4. Similarly, construct suffix information. Let `suff[i]` represent the cumulative sum from instruction `i` to the end. Then compute `suff_min[i]` and `suff_max[i]`, representing minimum and maximum values of `x` in that suffix relative to its starting point, which is initially `0`.
5. For each query `[l, r]`, split the program into two parts: prefix `1..l-1` and suffix `r+1..n`. The ignored segment contributes a net delta of `pref[r] - pref[l-1]`.
6. Adjust the suffix's min and max values by the net change in `x` due to the prefix (`pref[l-1]`). The minimum value of `x` over the remaining instructions is `min(pref_min[l-1], pref[l-1] + suff_min[r+1])`, and the maximum is `max(pref_max[l-1], pref[l-1] + suff_max[r+1])`.
7. The answer for the query is `max_val - min_val + 1`.

Why it works: The invariant is that any contiguous subsequence's removal simply shifts all later values by the net effect of the removed segment. By storing the min and max values for all prefixes and suffixes, we can reconstruct the extremal values without simulating every step. Combining the two extremal values after shifting yields the complete set of distinct values because each increment/decrement changes `x` by exactly 1.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        s = input().strip()
        a = [1 if c == '+' else -1 for c in s]

        # prefix sums and min/max
        pref = [0] * (n + 1)
        pref_min = [0] * (n + 1)
        pref_max = [0] * (n + 1)
        for i in range(1, n + 1):
            pref[i] = pref[i - 1] + a[i - 1]
            pref_min[i] = min(pref_min[i - 1], pref[i])
            pref_max[i] = max(pref_max[i - 1], pref[i])

        # suffix min/max
        suff_min = [0] * (n + 2)
        suff_max = [0] * (n + 2)
        suff_sum = 0
        for i in range(n, 0, -1):
            suff_sum += a[i - 1]
            suff_min[i] = min(0, suff_min[i + 1] + a[i - 1])
            suff_max[i] = max(0, suff_max[i + 1] + a[i - 1])

        res = []
        for _ in range(m):
            l, r = map(int, input().split())
            # prefix before ignored segment
            pre_min = pref_min[l - 1]
            pre_max = pref_max[l - 1]
            # suffix after ignored segment, shifted by pref[l-1]
            suf_min = pref[l - 1] + suff_min[r + 1]
            suf_max = pref[l - 1] + suff_max[r + 1]
            total_min = min(pre_min, suf_min)
            total_max = max(pre_max, suf_max)
            res.append(str(total_max - total_min + 1))
        print('\n'.join(res))

if __name__ == "__main__":
    solve()
```

The code first converts the string into numerical increments and decrements. Prefix sums and their min/max values track the extremal values up to each instruction. The suffix min/max arrays are calculated in reverse, accumulating relative min/max values from the end. For each query, we merge the prefix and suffix values, adjusting the suffix values by the prefix sum before the ignored segment. The final answer is the range of distinct `x` values.

## Worked Examples

Sample input:

```
8 4
-+--+--+
1 8
2 8
2 5
1 1
```

| Step | pref | pref_min | pref_max | suff_min | suff_max | Query | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Initial | 0 | 0 | 0 | 0 | 0 | - | - |
| 1 | -1 | -1 | 0 | ... | ... | 1-8 | 1 |
| 2 | -1+1=0 | -1 | 1 | ... | ... | 2-8 | 2 |
| 3 | ... | ... | ... | ... | ... | 2-5 | 4 |
| 4 | ... | ... | ... | ... | ... | 1-1 | 4 |

This trace shows the min and max before and after ignored segments, demonstrating how the algorithm computes the range efficiently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each array is built in O(n) and each query answered in O(1) |
| Space | O(n) | Prefix and suffix arrays require O(n) space each |

With n and m up to 2e5, O(n + m) operations comfortably fit within a 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str)
```
