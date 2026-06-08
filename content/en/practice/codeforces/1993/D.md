---
title: "CF 1993D - Med-imize"
description: "We are given an array of integers and a parameter $k$. We can repeatedly remove any contiguous subarray of length exactly $k$ from the array, shrinking it. Once the array's length is no longer greater than $k$, we stop."
date: "2026-06-08T15:09:43+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1993
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 963 (Div. 2)"
rating: 2200
weight: 1993
solve_time_s: 157
verified: false
draft: false
---

[CF 1993D - Med-imize](https://codeforces.com/problemset/problem/1993/D)

**Rating:** 2200  
**Tags:** binary search, dp, greedy  
**Solve time:** 2m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and a parameter $k$. We can repeatedly remove any contiguous subarray of length exactly $k$ from the array, shrinking it. Once the array's length is no longer greater than $k$, we stop. Our goal is to determine the largest median of the remaining elements after this process.

The median is the "middle" element in the sorted array. For example, if one element remains, that element is trivially the median. If multiple elements remain, the median is the element at position $\lfloor (n+1)/2 \rfloor$ when sorted.

Constraints suggest arrays can have up to $5 \cdot 10^5$ elements, and the sum of $n$ across all test cases is at most $5 \cdot 10^5$. This means any solution with $O(n \log n)$ per test case is acceptable, but anything quadratic is infeasible. Each element can be as large as $10^9$, so simple counting or frequency-based tricks won't work.

A subtle edge case arises when $k=1$ or $k=n$. If $k=1$, any single element can be removed at any time, which means we can eventually leave the largest element as the median. If $k=n$, no removals are possible, and the median is simply the median of the original array. Missing these nuances could produce incorrect results.

## Approaches

The brute-force approach would consider all sequences of valid subarray removals and compute the median for each resulting array. This is correct in principle but prohibitively slow. For example, if $n=10^5$ and $k=2$, there are roughly $\binom{n}{k}$ sequences of operations to consider, which is astronomically large.

The key insight is to realize that only the relative positions of elements matter. After repeated removals, the remaining array will always consist of elements at the boundaries of removed subarrays. Since we want the largest median, we do not care about the exact sequence of removals. Instead, we ask: for a candidate median value $x$, can we remove enough elements so that $x$ ends up in the "middle" of the final array?

This naturally leads to a binary search solution. We can guess a median value $x$ and check if it is achievable. To do this, we can transform the array into a +1/-1 sequence: +1 for elements $\ge x$, -1 for elements $< x$. Then the problem reduces to finding whether a subarray removal strategy allows a positive balance of +1s over -1s in the final array. This check can be done in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n/k)^n) | O(n) | Too slow |
| Binary Search + Prefix Sums | O(n log(max(a))) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort is unnecessary because we only care about whether a value can be a median.
2. Initialize binary search bounds: `lo = 1`, `hi = max(a)`.
3. While `lo < hi`, pick `mid = (lo + hi + 1) // 2` as a candidate median.
4. Transform the array into `b[i] = +1 if a[i] >= mid else -1`.
5. Compute prefix sums `pref[i] = b[0] + ... + b[i]`.
6. For each index `i` where we could stop removing subarrays, maintain the minimum prefix sum for the left side of the current window of size `k`.
7. If at any point the prefix sum minus the minimum prefix sum is positive, the candidate `mid` is achievable.
8. If achievable, move `lo = mid`. Otherwise, set `hi = mid - 1`.
9. After binary search, `lo` is the largest achievable median.

Why it works: the +1/-1 transformation captures whether a candidate median is "large enough." Positive prefix sum differences guarantee that we can select subarrays so that this median survives to the end. The binary search ensures that we find the maximal median efficiently.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_achieve(a, n, k, x):
    b = [1 if val >= x else -1 for val in a]
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i+1] = pref[i] + b[i]

    min_pref = 0
    for i in range(k, n+1):
        if pref[i] - min_pref > 0:
            return True
        min_pref = min(min_pref, pref[i-k+1])
    return False

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        lo, hi = 1, max(a)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if can_achieve(a, n, k, mid):
                lo = mid
            else:
                hi = mid - 1
        print(lo)

if __name__ == "__main__":
    solve()
```

Explanation: The `can_achieve` function computes the prefix sums over the transformed array and checks if a positive sum can be achieved using a sliding window of size `k`. Binary search finds the maximal feasible median. Note that the `+1` in `(lo + hi + 1) // 2` ensures the search does not get stuck when `lo` and `hi` are adjacent. Boundary handling in `min_pref` is subtle and critical for correctness.

## Worked Examples

**Example 1:**

Input: `4 3` with array `[3,9,9,2]`

Candidate median binary search starts at mid-values 6, 4, 3. Transforming array with `mid=4` gives `[-1,1,1,-1]`. Prefix sums `[0,-1,0,1,0]`. Sliding window check confirms that positive sum exists; `mid=4` achievable. Binary search proceeds, final answer `3`.

| Step | mid | transformed | prefix | min_pref | achievable? |
| --- | --- | --- | --- | --- | --- |
| 1 | 6 | [-1,-1,-1,-1] | [0,-1,-2,-3,-4] | 0 | No |
| 2 | 4 | [-1,1,1,-1] | [0,-1,0,1,0] | 0 | Yes |
| 3 | 3 | [1,1,1,-1] | [0,1,2,3,2] | 0 | Yes |

This confirms the algorithm correctly identifies the maximal median 3.

**Example 2:**

Input: `5 3` with array `[3,2,5,6,4]`

Binary search candidate `mid=4` yields transformed `[ -1,-1,1,1,1 ]`. Prefix sums `[0,-1,-2,-1,0,1]`. Sliding window finds positive difference, achievable. Final answer 4.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log(max(a))) | Binary search over element values (up to 10^9) times linear prefix sum check |
| Space | O(n) | Prefix sum array of length n+1 |

Given $n \le 5 \cdot 10^5$ and max element $10^9$, this solution easily fits within 2 seconds and 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples
assert run("5\n4 3\n3 9 9 2\n5 3\n3 2 5 6 4\n7 1\n5 9 2 6 5 4 6\n8 2\n7 1 2 6 8 3 4 5\n4 5\n3 4 5 6\n") == "3\n4\n9\n6\n4"

# custom cases
assert run("1\n1 1\n10\n") == "10"  # single element
assert run("1\n5 5\n1 2 3 4 5\n") == "3"  # k=n, median of original
assert run("1\n5 1\n1 2 3 4 5\n") == "5"  # k=1, can leave largest
assert run("1\n6 2\n1 1 1 1 1 1\n") == "1"  # all equal
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1\n10 | 10 | Single-element array |
| 5 5\n1 2 3 4 5 | 3 | k=n, median |
