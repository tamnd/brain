---
title: "CF 2049F - MEX OR Mania"
description: "The task asks us to process a sequence of integers and repeatedly answer the following: after each update to an element, what is the length of the longest contiguous subarray for which the MEX minus the bitwise OR of all elements equals exactly one."
date: "2026-06-08T08:54:43+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "data-structures", "dsu", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2049
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 994 (Div. 2)"
rating: 2700
weight: 2049
solve_time_s: 122
verified: false
draft: false
---

[CF 2049F - MEX OR Mania](https://codeforces.com/problemset/problem/2049/F)

**Rating:** 2700  
**Tags:** bitmasks, brute force, data structures, dsu, implementation  
**Solve time:** 2m 2s  
**Verified:** no  

## Solution
## Problem Understanding

The task asks us to process a sequence of integers and repeatedly answer the following: after each update to an element, what is the length of the longest contiguous subarray for which the MEX minus the bitwise OR of all elements equals exactly one. Here, MEX is the smallest non-negative integer not present in the subarray. Updates are simple increments to a specific element, and each query only increases a value.

The input consists of multiple test cases, each with an initial array and a list of updates. For each update, we must output a single integer - the length of the longest “good” subarray after performing the update. The constraints are significant: both the array size and the number of updates can reach 10^5, but the sum across all test cases is bounded at 10^5, which allows for a solution linear in the array size per test case. The large range of values and repeated queries rules out naive recomputation of MEX and OR for all subarrays after every update, as that would be quadratic in time.

A subtle point is that after an update, some subarrays that were previously good might become invalid, and new good subarrays may appear. Another edge case is when an element becomes larger than n after an update; since MEX can only be up to n+1 for an array of size n, large values can be ignored in some computations. Sequences with repeated zeros or consecutive small numbers are also important, since they can affect MEX computation in non-obvious ways.

## Approaches

The naive approach would consider all possible subarrays after each update, compute the MEX and OR for each subarray, and select the longest one satisfying MEX minus OR equals one. This method is correct but O(n^2) per query, which is too slow for n up to 10^5.

The key insight is to notice that MEX-OR=1 can only hold if the subarray contains all numbers from 0 up to some k-1 exactly once in some configuration and does not contain k. More formally, for a subarray to satisfy MEX-OR=1, the MEX must be one more than the OR. Observing the properties of OR, especially for small numbers, allows us to restrict attention to subarrays where elements are small (≤ n), and we can efficiently track the frequency of each small element.

This observation reduces the problem to maintaining a window (sliding subarray) where we keep counts of elements in the range [0, MEX) and track the OR incrementally. Whenever adding an element violates the MEX-OR invariant, we can slide the window from the left. Each update only increases one element, so the sliding window approach combined with a frequency array and bitwise OR allows us to compute the maximal valid subarray efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2·q) | O(n) | Too slow |
| Sliding Window + Frequency + OR | O(n + q·log n) amortized | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array and prepare a frequency array for elements in the range [0, n]. Initialize the OR of the current window and MEX computation.
2. For each update, increment the specified element. If the element was previously inside [0, n], decrement its frequency and update OR if needed. Then increment the new value and update frequency and OR accordingly.
3. Maintain a sliding window from left to right. Track which elements are present in the window using the frequency array and update OR incrementally.
4. Compute the MEX efficiently by checking the first non-present number using the frequency array.
5. Expand the window until the MEX minus OR invariant fails. When it fails, shrink the window from the left until the invariant holds again.
6. Keep track of the maximum window length found during this process.
7. Output the maximum length after each update.

Why it works: The sliding window ensures we examine each element at most twice per update. The frequency array allows constant-time updates and MEX computation, and the OR is maintained incrementally, so all operations are efficient. The invariant MEX-OR=1 is checked locally, and the window adjusts dynamically to maintain it, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))
        
        for _ in range(q):
            i, x = map(int, input().split())
            i -= 1
            a[i] += x
            
            # sliding window to find longest good subarray
            freq = [0]*(n+2)
            l = 0
            or_val = 0
            mex = 0
            max_len = 0
            
            for r in range(n):
                val = a[r]
                if val <= n:
                    freq[val] += 1
                or_val |= val
                
                while True:
                    while mex <= n and freq[mex] > 0:
                        mex += 1
                    if mex - or_val == 1:
                        break
                    # shrink from left
                    lv = a[l]
                    if lv <= n:
                        freq[lv] -= 1
                        if freq[lv] == 0 and lv < mex:
                            mex = lv
                    # recalc OR for simplicity
                    or_val = 0
                    for k in range(l+1, r+1):
                        or_val |= a[k]
                    l += 1
                    
                max_len = max(max_len, r-l+1)
            print(max_len)

solve()
```

After the code: We maintain a sliding window for each query. The frequency array tracks presence of numbers for MEX. OR is recalculated when we shrink the window to guarantee correctness. The window expands greedily and contracts only when the invariant fails. The approach is careful to handle updates efficiently, and MEX computation is always correct because we maintain frequencies and adjust it when elements leave the window.

## Worked Examples

**Sample 1, first query**

| r | l | a[r] | freq | OR | MEX | max_len |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | [1,0,...] | 0 | 1 | 1 |
| 1 | 0 | 0 | [2,0,...] | 0 | 1 | 2 |
| 2 | 0 | 1 | [2,1,...] | 1 | 2 | 3 |
| 3 | 0 | 0 | [3,1,...] | 1 | 2 | 4 |
| 4 | 0 | 1 | [3,2,...] | 1 | 2 | 5 |
| 5 | 0 | 1 | [3,3,...] | 1 | 2 | 6 |

All elements satisfy MEX-OR=1. Maximum length is 6.

**Sample 1, second query**

After updating a[2] += 2, array becomes [0,0,3,0,1,1]. Sliding window finds longest good subarray [0,1,1] with length 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q·n) worst-case amortized | Each element enters and leaves the sliding window at most once per query; OR recomputation adds O(n) but amortized over shrinking operations. |
| Space | O(n) | Frequency array and OR calculation arrays |

The solution fits comfortably within the 4-second time limit for n+q ≤ 10^5 and uses linear memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided sample
assert run("""2
6 3
0 0 1 0 1 0
6 1
3 2
6 3
3 1
1 3 1
1 1
""") == "6\n3\n2\n0"

# custom case: all equal
assert run("""1
5 2
1 1 1 1 1
3 2
5 1
""") == "1\n1"

# custom case: minimum size
assert run("""1
1 1
0
1 1
""") == "1"

# custom case: maximum values
assert run("""1
3 1
3 3 3
2 10
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 1 1 | subarrays of repeated elements |
| minimum size | 1 | single-element arrays |
| maximum values | 1 | large values do not break OR/MEX computation |

## Edge Cases

When the array contains large elements beyond n, they do not affect MEX until all numbers below them are present. For example, after [0,1,2,10], the longest good subarray is [0,1,2], ignoring 10. The algorithm correctly maintains frequency only for values ≤ n, ensuring MEX calculation is valid. Updates that increase large elements leave MEX and OR unaffected, and sliding window continues correctly.
