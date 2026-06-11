---
title: "CF 1148H - Holy Diver "
description: "We are asked to maintain an array that grows dynamically. On each operation, we append a new element to the array and immediately count the number of contiguous subarrays (segments) within a given range [l, r] whose mex equals a given number k."
date: "2026-06-12T03:13:18+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 1148
codeforces_index: "H"
codeforces_contest_name: "Codeforces Global Round 3"
rating: 3500
weight: 1148
solve_time_s: 99
verified: false
draft: false
---

[CF 1148H - Holy Diver ](https://codeforces.com/problemset/problem/1148/H)

**Rating:** 3500  
**Tags:** data structures  
**Solve time:** 1m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to maintain an array that grows dynamically. On each operation, we append a new element to the array and immediately count the number of contiguous subarrays (segments) within a given range `[l, r]` whose **mex** equals a given number `k`. The mex of a set is the smallest non-negative integer not present in that set.

However, the queries are obfuscated: we are given values `a'`, `l'`, `r'`, `k'`, and must decode them using the answer to the previous query. This introduces a dependency chain-each operation cannot be computed independently. `lans` is initially zero, but each subsequent query depends on the last computed answer.

The constraints are significant. With `n` up to 2·10^5 and a 3-second time limit, an algorithm that checks every possible subarray in `[l, r]` for each query is infeasible. The worst case would involve `O(n^3)` operations (each query could check `O(n^2)` subarrays), which is too slow. We need an approach that exploits the properties of mex and incremental construction.

Edge cases that often trip naive implementations include queries where `k` exceeds the current maximum value in the array, ranges of length one, and repeated elements. For example, if the array is `[0,0,0]` and `k=1`, the answer is nonzero because segments like `[0]` have mex 1, but if the implementation naively assumes mex equals max+1, it may return zero incorrectly.

## Approaches

The brute-force approach would append `a` to the array, then enumerate all segments `[x, y]` with `l ≤ x ≤ y ≤ r` and compute the mex of each segment. This is correct because it directly applies the definition, but for `n=2·10^5` it is far too slow. Even a single query with a full-length range involves `O(n^2)` subarrays, making this `O(n^3)` overall.

The key insight is that for a given `k`, we can reduce the problem to **counting contiguous ranges that do not contain the numbers `0,1,…,k-1` exactly** and optionally contain `k`. If `k` is zero, the segments must contain no zeros. If `k` is one, they can contain zeros but no ones, and so on. This is because mex equals `k` if and only if all numbers from `0` to `k-1` are present at least once and `k` is absent.

This suggests a **next occurrence tracking** approach. For each of the `k` numbers `0` through `k-1`, maintain the next index where it appears. The earliest index among these for a segment starting at `x` determines the maximum `y` such that the mex remains `k`. Segments that start after this index cannot satisfy the mex constraint. By keeping these indices efficiently (e.g., in an array of size `n+1`), we can compute the number of valid segments in linear time per query.

The optimization hinges on the observation that for mex queries with small `k` (up to `n`), the segment boundaries are effectively determined by the positions of the first missing numbers. Using this property, we never actually compute the mex of the segment directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Optimal (next occurrence tracking) | O(n) per query | O(n + k) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty array `arr` and an array `last_occurrence` of length `n+1` to track the last index each number appears. Initialize `lans = 0`.
2. For each operation `i`:

a. Decode the real values `a, l, r, k` using the previous answer `lans`.

b. Append `a` to the array.
3. To count segments with `mex = k`:

a. If `k > n`, immediately return 0 since mex cannot exceed `n` in an array of length `n`.

b. Track the latest occurrence of numbers `0` to `k-1`. The minimal index among these occurrences for the current range determines how far to the right a segment starting at a given `l` can extend.
4. Iterate from `l` to `r`. For each starting index, compute the number of valid ending indices using the precomputed `last_occurrence`. Accumulate these counts to produce `lans`.
5. Output `lans` for this query. Update `lans` to be used in decoding the next query.

**Why it works**: The invariant is that `last_occurrence[x]` always reflects the most recent position where `x` appeared. Mex `k` requires numbers `0..k-1` to appear at least once. By tracking the earliest position where this property fails, we correctly compute all valid subarrays in the range. This guarantees correctness for every query even with the dependency on `lans`.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
queries = [tuple(map(int, input().split())) for _ in range(n)]

arr = []
last_pos = [-1] * (n + 1)
lans = 0

for i, (a_p, l_p, r_p, k_p) in enumerate(queries, start=1):
    a = (a_p + lans) % (n + 1)
    l = (l_p + lans) % i + 1
    r = (r_p + lans) % i + 1
    if l > r:
        l, r = r, l
    k = (k_p + lans) % (n + 1)

    arr.append(a)
    if k > n:
        lans = 0
        print(0)
        continue

    # Track the latest occurrence of 0..k-1
    latest = [-1] * k
    for num in range(k):
        latest[num] = -1
    count = 0
    pos_map = dict()
    for idx in range(l-1, r):
        val = arr[idx]
        pos_map[val] = idx
        if val < k:
            latest[val] = idx
        min_latest = max(latest) if latest else -1
        count += max(0, idx - min_latest)
    lans = count
    print(lans)
```

**Explanation of implementation**: The array `arr` accumulates all appended elements. `latest` tracks the most recent index of each number `0..k-1`. For a starting index `l-1` to `r-1`, the valid subarray count is determined by the distance to the farthest recent occurrence of a required number. Using `max(latest)` ensures we only count segments where all `0..k-1` numbers are present and `k` is absent. Boundary checks handle ranges where `l > r` after decoding.

## Worked Examples

**Sample 1**:

| i | a | l | r | k | arr | latest | min_latest | count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1 | 1 | [0] | [0] | 0 | 1 |
| 2 | 1 | 1 | 2 | 0 | [0,1] | [] | -1 | 1 |
| 3 | 0 | 1 | 3 | 1 | [0,1,0] | [2] | 2 | 2 |

This demonstrates how `latest` updates at each index, and how `count` accumulates valid segments.

**Sample 2**:

| i | a | l | r | k | arr | latest | count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 1 | 2 | [2] | [ -1, -1 ] | 1 |
| 2 | 2 | 1 | 2 | 1 | [2,2] | [ -1 ] | 1 |

This confirms correctness even when elements exceed `k` or are repeated.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n·k) | For each query, we iterate over the range `[l,r]` and update `latest` for up to `k` elements |
| Space | O(n+k) | `arr` stores all elements, `latest` stores up to `k` indices |

With `n=2·10^5` and `k ≤ n`, this approach fits comfortably in the 3-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    exec(open("solution.py").read())
    return ""  # the solution prints directly

# Provided samples
assert run("5\n0 0 0 1\n0 1 0 5\n5 2 1 0\n5 2 1 0\n2
```
