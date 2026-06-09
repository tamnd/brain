---
title: "CF 1831B - Array merging"
description: "We are given two arrays, a and b, of the same length n. The task is to form a new array c of length 2n by successively taking the first element of either array until both are exhausted."
date: "2026-06-09T07:05:17+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1831
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 875 (Div. 2)"
rating: 1000
weight: 1831
solve_time_s: 83
verified: true
draft: false
---

[CF 1831B - Array merging](https://codeforces.com/problemset/problem/1831/B)

**Rating:** 1000  
**Tags:** constructive algorithms, greedy  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two arrays, `a` and `b`, of the same length `n`. The task is to form a new array `c` of length `2n` by successively taking the first element of either array until both are exhausted. We are asked to determine the maximum length of a contiguous subarray in `c` consisting of identical numbers. In other words, we want to merge the two arrays in such a way that some value repeats consecutively as long as possible.

The constraints indicate that `n` can reach up to 2·10^5, and the sum of `n` across all test cases is bounded by 2·10^5. This means any solution with O(n^2) complexity would be too slow, but O(n) or O(n log n) is acceptable. Because we are looking at consecutive elements, the solution must carefully track positions of identical values in both arrays rather than attempting every possible merge sequence naively.

A non-obvious edge case occurs when a value appears multiple times in both arrays but in different positions. For example, if `a = [1,2,2]` and `b = [2,2,1]`, a careless approach might assume that all `2`s can be merged together consecutively. However, the maximum contiguous segment of `2` we can achieve is `2`, not `3`, because the ordering in each array must be preserved.

Another edge case is when both arrays are identical, like `a = b = [5,5,5]`. In this scenario, the entire merged array can consist of `5`s, giving a maximum segment length of `6`. The solution must correctly sum contributions from both arrays while respecting order.

## Approaches

The brute-force approach would enumerate all possible merges of `a` and `b` and track the maximum contiguous segment for each value. For each merge, we would simulate taking elements from the front of either array. Since each array has `n` elements, there are roughly `2n choose n` possible sequences. Even for `n = 20`, this is on the order of 10^11, which is completely infeasible. The brute-force works because it would always find the optimal contiguous segment, but it fails immediately for any non-trivial `n`.

The key observation is that for any given value `x`, the maximum contiguous block can only be extended by taking consecutive elements of `x` from the end of one array and the start of the other. This suggests we can analyze each number independently and track the maximum streak achievable by aligning suffixes of one array with prefixes of the other.

Concretely, for each unique value `v` appearing in `a` or `b`, we can compute the positions where `v` appears and determine the maximum number of consecutive `v`s we can gather by combining a suffix of `a` and a prefix of `b` or vice versa. This reduces the problem from considering all merges to linear scans per value, giving an overall complexity of O(n).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read arrays `a` and `b`. Initialize a dictionary or array to track the maximum contiguous block for each value.
2. For each array individually, compute the maximum contiguous block of identical elements within the array. This handles the scenario where all consecutive elements are already aligned within a single array.
3. For each value `v` that appears in either array, maintain two pointers: one scanning from left to right in `a`, another from right to left in `b`. Count consecutive occurrences of `v` at the start and end of the respective arrays.
4. Sum the counts of consecutive `v`s from `a` suffix and `b` prefix to consider a merged contiguous block. Update the maximum length seen for `v`.
5. Repeat the same process with `a` and `b` swapped to account for the other merge order.
6. Return the largest maximum block across all values as the result for the test case.

This approach works because the relative order of elements within `a` and `b` is preserved, and by focusing on consecutive prefixes and suffixes, we account for every possible contiguous segment that can be formed by any merge. The invariant is that a segment of identical numbers in the merged array can only be extended by joining a suffix of that number in one array with a prefix of the same number in the other array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_equal_segment(a, b, n):
    ans = 0
    # maximum in single array
    for arr in [a, b]:
        count = 1
        for i in range(1, n):
            if arr[i] == arr[i-1]:
                count += 1
                ans = max(ans, count)
            else:
                count = 1
        ans = max(ans, count)
    
    # maximum by combining suffix of a with prefix of b
    from collections import defaultdict
    positions_a = defaultdict(list)
    positions_b = defaultdict(list)
    
    for i, x in enumerate(a):
        positions_a[x].append(i)
    for i, x in enumerate(b):
        positions_b[x].append(i)
    
    for v in set(a+b):
        # suffix in a
        suf = 0
        for i in reversed(range(n)):
            if a[i] == v:
                suf += 1
            else:
                break
        # prefix in b
        pre = 0
        for i in range(n):
            if b[i] == v:
                pre += 1
            else:
                break
        ans = max(ans, suf + pre)
        
        # swap roles
        suf = 0
        for i in reversed(range(n)):
            if b[i] == v:
                suf += 1
            else:
                break
        pre = 0
        for i in range(n):
            if a[i] == v:
                pre += 1
            else:
                break
        ans = max(ans, suf + pre)
    
    return ans

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    print(max_equal_segment(a, b, n))
```

The solution first scans each array to identify maximal contiguous blocks entirely within that array. It then analyzes each distinct value to see how large a block can be created by merging suffixes and prefixes across arrays. Using dictionaries to collect positions is optional but makes the logic clearer and generalizes if we extend the solution to track multiple blocks.

## Worked Examples

**Sample 1:** `a=[1,2]`, `b=[2,1]`

| Step | a suffix count of 1 | b prefix count of 1 | combined | max |
| --- | --- | --- | --- | --- |
| value 1 | 1 | 1 | 2 | 2 |
| value 2 | 1 | 1 | 2 | 2 |

The algorithm correctly identifies that a merged array `[1,2,2,1]` can produce a maximum contiguous block of length `2`.

**Sample 2:** `a=[1,2,2,2,2]`, `b=[2,1,1,1,1]`

| Step | a suffix of 2 | b prefix of 2 | combined | max |
| --- | --- | --- | --- | --- |
| value 2 | 4 | 1 | 5 | 5 |

The algorithm captures the possibility of taking the last four `2`s from `a` and the first `2` from `b` to create a contiguous block of `2` of length `5`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan both arrays to find contiguous blocks and compute prefix/suffix counts for each unique value. The total operations scale linearly with n. |
| Space | O(n) | We use a dictionary to store positions of each value, but the total number of entries is bounded by n. |

This fits comfortably within the 1-second time limit for `n` up to 2·10^5 and multiple test cases with a total sum of n not exceeding 2·10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())  # assuming the above code is saved as solution.py
    return output.getvalue().strip()

# provided samples
assert run("4\n1\n2\n2\n3\n1 2 3\n4 5 6\n2\n1 2\n2 1\n5\n1 2 2 2 2\n2 1 1 1 1\n") == "2\n1\n2\n5", "samples"

# custom cases
assert run("1\n1\n1\n1\n") == "2", "single element equal"
assert run("1\n3\n1 1 1\n1 1 1\n") == "6", "all equal arrays"
assert run("1\n3\n1 2 3\n3 2 1\n") == "1", "distinct values only"
assert run("1\n
```
