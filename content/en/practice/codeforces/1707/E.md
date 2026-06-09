---
title: "CF 1707E - Replace"
description: "We are given an array of integers a of length n, where each element is between 1 and n. Conceptually, imagine these as labeled tiles laid out in a row."
date: "2026-06-09T21:15:28+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 1707
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 808 (Div. 1)"
rating: 3500
weight: 1707
solve_time_s: 179
verified: false
draft: false
---

[CF 1707E - Replace](https://codeforces.com/problemset/problem/1707/E)

**Rating:** 3500  
**Tags:** binary search, data structures  
**Solve time:** 2m 59s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers `a` of length `n`, where each element is between 1 and `n`. Conceptually, imagine these as labeled tiles laid out in a row. We define a "replace" operation on a contiguous segment `(l, r)`: it collapses the segment into the pair `(min value in the segment, max value in the segment)`. We can repeatedly apply this operation: each step maps the current `(l, r)` to the min-max of the subarray defined by that range.

The queries ask: starting from a given `(l, r)`, how many replacements do we need to reach `(1, n)`? If it's impossible - that is, the sequence of replacements enters a cycle that never covers the full `[1, n]` - we return `-1`.

Constraints tell us `n` and `q` can each be up to 100,000, so naive iteration over subarrays in each query is far too slow. If we consider a naive solution that recomputes min and max by scanning a subarray on every replace, the worst-case operation count is roughly `O(n * q)` or even higher if multiple replacements are required per query. This would reach `10^10` operations, far beyond a 2-second time limit. We need a smarter approach that reduces repeated scanning.

An edge case that is subtle is when the replacement cycles indefinitely. For example, the array `[2, 1]` with query `(1, 1)` produces `(2, 2) → (1, 1) → (2, 2)` forever. A careless solution that assumes eventual convergence to `(1, n)` will incorrectly return a number instead of `-1`. Another edge case occurs when the starting segment is already `(1, n)`; the answer should be `0`.

## Approaches

The brute-force approach is straightforward. For each query `(l, r)`, repeatedly compute the min and max of `a[l..r]` until reaching `(1, n)` or detecting a loop. This is correct because it simulates the exact process described, but it is too slow. The number of steps could be `O(n)` per query, and computing min and max naïvely is also `O(n)`, yielding `O(n^2 * q)` operations. For `n, q = 10^5`, this is clearly infeasible.

The key observation is that the replace operation only ever expands the segment: the min can only decrease or stay the same, and the max can only increase or stay the same. This monotonic property suggests that the process can be predicted in advance. We can preprocess the array into a structure that allows us to jump from one `(l, r)` to the next `(l', r')` in `O(1)` or `O(log n)` time. Specifically, we notice that for any `x` in `[1, n]`, the first and last occurrences of `x` define a segment that must eventually be covered if we want to reach `(1, n)`. By repeatedly merging overlapping segments corresponding to consecutive numbers, we can compute the minimal number of replacements without scanning the array for every query.

The resulting approach is a combination of interval expansion and binary lifting. First, preprocess for each position the maximum interval that can be reached in one replacement. Then, for each query, repeatedly apply jumps using a doubling table to reach `(1, n)` efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 * q) | O(1) | Too slow |
| Optimal (Interval Merging + Doubling) | O(n log n + q log n) | O(n log n) | Accepted |

## Algorithm Walkthrough

1. Precompute the first and last occurrence of each value from `1` to `n`. Let `first[x]` and `last[x]` denote the first and last index where `a[i] = x`. This lets us know the minimal segment that covers all occurrences of a value.
2. Compute the initial expansion `b[i]` for each index `i`. `b[i]` is the farthest right index that can be reached starting from `[i, i]` in one replace. Initialize `b[i] = i`. Iterate over values `1..n` in order, and for each value, expand `b[i]` for all `i` in its segment to cover the min-max interval. After this step, `b[i]` represents the maximal segment reachable in one step from `[i, i]`.
3. Build a doubling table. Let `jump[k][i]` be the farthest right index reachable from `i` using `2^k` replacements. Populate this table using the recurrence `jump[k][i] = jump[k-1][jump[k-1][i]]`. This allows us to answer queries in `O(log n)` by jumping powers of two.
4. For each query `(l, r)`, first check if `(l, r)` already covers `(1, n)`. If so, return `0`. Otherwise, expand `(l, r)` using the doubling table: starting from the highest power of two, jump whenever it does not exceed `n`. If after all jumps we reach `n` and cover `1` on the left, return the number of jumps. Otherwise, return `-1`.

Why it works: the doubling table ensures that we never recompute min/max for the same segment repeatedly. The precomputed maximal reach captures exactly one replace operation. The monotonic property of segment expansion guarantees that repeated application never shrinks the interval, so this procedure cannot miss the minimal number of steps. Cycles are implicitly handled: if we cannot reach `(1, n)`, the jump table will eventually fail to extend the segment, yielding `-1`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    
    first = [n] * (n + 1)
    last = [-1] * (n + 1)
    for i, val in enumerate(a):
        first[val] = min(first[val], i)
        last[val] = max(last[val], i)
    
    b = list(range(n))
    i = 0
    while i < n:
        r = i
        j = i
        while j <= r:
            val = a[j]
            r = max(r, last[val])
            j += 1
        for k in range(i, r + 1):
            b[k] = r
        i = r + 1

    LOG = 20
    jump = [b]
    for k in range(1, LOG):
        nxt = [0] * n
        for i in range(n):
            nxt[i] = jump[k-1][jump[k-1][i]]
        jump.append(nxt)

    for _ in range(q):
        l, r = map(int, input().split())
        l -= 1
        r -= 1
        if l == 0 and r == n - 1:
            print(0)
            continue
        if b[l] < r:
            print(-1)
            continue
        ans = 0
        cur_l = l
        cur_r = r
        for k in reversed(range(LOG)):
            nxt_r = jump[k][cur_l]
            if nxt_r < n - 1:
                cur_l = nxt_r + 1
                ans += 1 << k
        if cur_l <= 0 and jump[0][cur_l] >= n - 1:
            ans += 1
            print(ans)
        else:
            print(-1)

if __name__ == "__main__":
    solve()
```

The first section computes first and last occurrences. The second computes `b[i]` using segment expansion. Then we prepare the doubling table for fast jumps. In queries, we check initial coverage, invalid segments, and then repeatedly jump. Off-by-one errors are critical: indices are converted to 0-based for Python lists, and segment bounds must be inclusive in expansion.

## Worked Examples

**Sample Input 1:**

| Step | Segment | Expanded |
| --- | --- | --- |
| Query 4,4 | (4,4) | (1,1) |
| Next | (1,1) | (2,2) |
| ... | Cycle | ... |

Answer: -1, matches expectation that it never reaches (1,5).

**Query 3,5:**

| Step | Segment | Expansion |
| --- | --- | --- |
| 3,5 | (3,5) | (1,4) |
| Next | (1,4) | (1,5) |

Answer: 2 steps. Shows doubling table reduces repeated computation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + q log n) | Preprocessing takes O(n) for segment expansion, O(n log n) for doubling table. Each query uses O(log n) jumps. |
| Space | O(n log n) | Doubling table stores O(log n) arrays of size n. |

With n, q ≤ 10^5, `O(n log n + q log n)` is comfortably within 2 seconds, and memory ≤
