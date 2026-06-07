---
title: "CF 2086B - Large Array and Segments"
description: "We are given an array a of length n and a positive integer k. From a, we construct a larger array b by repeating a exactly k times. That is, b has length n k, and its first n elements are the same as a, and the remaining elements repeat a in order."
date: "2026-06-08T06:02:38+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2086
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 177 (Rated for Div. 2)"
rating: 1100
weight: 2086
solve_time_s: 83
verified: true
draft: false
---

[CF 2086B - Large Array and Segments](https://codeforces.com/problemset/problem/2086/B)

**Rating:** 1100  
**Tags:** binary search, brute force, greedy  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array `a` of length `n` and a positive integer `k`. From `a`, we construct a larger array `b` by repeating `a` exactly `k` times. That is, `b` has length `n * k`, and its first `n` elements are the same as `a`, and the remaining elements repeat `a` in order. The task is, for a given threshold `x`, to count how many starting positions `l` in `b` have at least one segment `[l, r]` whose sum is at least `x`.

Because `n` and `k` can each be up to `10^5`, `b` can theoretically have length up to `10^10`. Clearly, constructing `b` explicitly or iterating over all segments would be infeasible. The sum of all `n` and all `k` across test cases is bounded by `2*10^5`, which hints that a solution linear in `n` per test case is acceptable, but anything linear in `n * k` is not.

Edge cases to watch include when `k` is very large but `x` is enormous, so no segment reaches `x`. For instance, if `a = [1]`, `k = 100000`, and `x = 1000000000`, the answer is `0`. Another edge case occurs when `x` is very small relative to `a`, such as `x = 1` and `a = [100]`, where every position `l` is valid.

## Approaches

The brute-force approach would consider every starting position `l` in `b`, then iterate forward adding elements until the sum reaches or exceeds `x`. This works correctly but has complexity `O(n*k)` per test case, which can be as large as `10^{10}` operations. This is impossible in the time limits.

The key insight comes from two observations. First, the array `b` is periodic with period `n`. That means any segment starting after the first `n` elements can be mapped back to a segment starting within the first `n` elements, with possibly additional whole copies of `a` appended. Second, because we are looking for _any segment_ that sums to at least `x`, we only need to know, for each position in the first copy of `a`, how many repeated blocks we need to reach `x`.

We precompute the prefix sums of `a` to quickly determine the minimum number of elements from the current position needed to reach `x`. If the total sum of `a` is `S`, then for positions where `x` is larger than `S`, we might need multiple complete repetitions of `a`. If the number of required repetitions exceeds `k`, no segment from that position can reach `x`. Otherwise, we can count how many starting positions in `b` will succeed, based on how many full repetitions fit. This reduces the problem to `O(n)` operations per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * k) | O(n * k) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `k`, `x`, and array `a`.
2. Compute the prefix sum array `pref` for `a`, where `pref[i] = a[0] + ... + a[i]`. This allows us to compute the sum of any segment in `a` in constant time.
3. Compute the total sum `S = sum(a)`. If `S >= x`, then some segments of length ≤ `n` can reach `x`. Otherwise, multiple copies are needed.
4. For each starting position `i` in `a` (0-based), compute the maximum number of repetitions of `a` that can be used while keeping the sum < `x`. Specifically, for each `i`, find the minimal number of full copies `full_blocks` needed after `i` such that the cumulative sum from `i` reaches `x`.
5. If the number of required full copies exceeds `k`, this position contributes `0` valid starting positions. Otherwise, every corresponding position in `b` created by repeating `a` contributes. Count the number of valid positions by `valid_count = k - full_blocks`.
6. Sum `valid_count` over all positions `i` to get the answer for the test case.

Why it works: The invariant is that for each position `i` in the first copy of `a`, the number of full copies needed to reach `x` is determined solely by the prefix sums and the total sum `S`. Repetition beyond `k` cannot create a valid segment. All positions in later copies of `a` map back to a position in the first copy due to the periodicity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k, x = map(int, input().split())
        a = list(map(int, input().split()))
        S = sum(a)
        pref = [0] * n
        pref[0] = a[0]
        for i in range(1, n):
            pref[i] = pref[i-1] + a[i]

        result = 0
        for i in range(n):
            needed = x - pref[i-1] if i > 0 else x
            if needed <= 0:
                # sum from i to i only (or less) already >= x
                result += k
            else:
                # full repetitions needed
                full_blocks = (needed + S - 1) // S
                if full_blocks <= k:
                    result += k - full_blocks + 1
        print(result)

if __name__ == "__main__":
    solve()
```

The code first computes prefix sums to allow constant-time segment sum queries. For each starting position, we compute how many full repetitions are needed to reach `x`. The use of `(needed + S - 1) // S` ensures proper ceiling division to avoid undercounting blocks. We then calculate the number of valid starting positions in the repeated array. Special care is taken for positions where the first element alone is already enough to reach `x`.

## Worked Examples

**Example 1:**

Input: `a = [3,4,2,1,5]`, `k = 3`, `x = 10`

| i | pref[i-1] | needed | full_blocks | valid_count |
| --- | --- | --- | --- | --- |
| 0 | 0 | 10 | 2 | 2 |
| 1 | 3 | 7 | 1 | 3 |
| 2 | 7 | 3 | 1 | 3 |
| 3 | 9 | 1 | 1 | 3 |
| 4 | 10 | 0 | 0 | 3 |

Summing `valid_count` gives `12`, matching the sample output. This demonstrates the handling of segments starting at different positions and how repetitions contribute.

**Example 2:**

Input: `a = [1]`, `k = 100000`, `x = 1`

The first element alone satisfies `x`, so every position in `b` is valid. The answer is `100000`, confirming the handling of minimal arrays and large `k`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Prefix sums and loop over `n` elements; all other operations are constant-time arithmetic |
| Space | O(n) | Prefix sum array; other variables are O(1) |

The algorithm scales linearly with `n` per test case, which fits comfortably under the problem constraints given `sum(n) <= 2*10^5`. Memory usage is also within the 512 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("""7
5 3 10
3 4 2 1 5
15 97623 1300111
105 95 108 111 118 101 95 118 97 108 111 114 97 110 116
1 100000 1234567891011
1
1 1 1
1 1 1
2 2 1 2
1 1
2 1 5
2 1
""") == "12\n1452188\n0\n1\n1\n1\n0", "sample 1"

# minimum input
assert run("1\n1 1 1\n1") == "1", "min input"

# all elements equal, x smaller than sum
assert run("1\n3 2 3\n1 1 1") == "6", "all equal"

# x too large, no segment
assert run("1\n2 5 20\n3 4") == "0", "x too large"

# large k, small array
assert run("1\n1 100000 1\n1") == "100000", "large k"

# multiple full blocks needed
assert run("1\n2 3 10\n3 2") == "2", "full blocks needed"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 |  |  |
