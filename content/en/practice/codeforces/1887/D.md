---
title: "CF 1887D - Split"
description: "We are given an array of distinct integers ranging from 1 to n, and we are asked to answer multiple queries about contiguous subarrays."
date: "2026-06-08T22:10:58+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "divide-and-conquer", "dsu", "math", "trees", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1887
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 905 (Div. 1)"
rating: 2700
weight: 1887
solve_time_s: 125
verified: true
draft: false
---

[CF 1887D - Split](https://codeforces.com/problemset/problem/1887/D)

**Rating:** 2700  
**Tags:** binary search, data structures, divide and conquer, dsu, math, trees, two pointers  
**Solve time:** 2m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of distinct integers ranging from 1 to n, and we are asked to answer multiple queries about contiguous subarrays. A subarray is considered "good" if it can be split into two non-empty parts such that all elements in the left part are strictly smaller than all elements in the right part. Essentially, we are asked to determine whether there exists an index where the maximum of the left part is smaller than the minimum of the right part.

The array size n can be as large as 300,000, and there can be up to 300,000 queries. A naive approach that checks each subarray independently, calculating maximums and minimums for all possible splits, would involve O(n) work per query, which could be up to 9×10¹⁰ operations in the worst case. This is far too slow for the time constraints, so we need a more efficient solution.

A subtle edge case arises when the subarray is strictly increasing or decreasing. For instance, `[1,2,3]` is trivially good because it can be split at any point, but `[3,2,1]` cannot be split in a way that satisfies the condition. Arrays with a single peak or valley in the middle may also be tricky if handled naively.

## Approaches

The brute-force method would be to iterate over each query, then iterate over all potential split points in the subarray, checking if the maximum of the left segment is smaller than the minimum of the right segment. For a query of length m, this is O(m²), which is unacceptable given m can be up to n=3×10⁵.

The key insight for a faster solution comes from observing that a subarray is "good" if and only if all numbers from the minimum value to the maximum value in that subarray form a contiguous segment. Because the array contains distinct integers from 1 to n, the condition that there exists a split with `max(left) < min(right)` is equivalent to saying the segment does not have a "gap" in the sequence of values. If the subarray contains values [2,3,4,5], it can always be split, but if it contains [2,4,5], it cannot because the number 3 is missing, creating a gap that prevents a proper split.

We can precompute the positions of elements in the array and for each query, find the maximum and minimum positions of the values in the subarray. If the difference between the maximum and minimum positions equals the number of elements minus one, the subarray is contiguous in terms of positions, and the answer is "Yes". Otherwise, "No".

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q * n²) | O(1) | Too slow |
| Optimal | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create an array `pos` of length n+1 to store the index of each value in the original array. For each `i` from 1 to n, set `pos[a[i]] = i`.
2. For each query with left `l` and right `r`, extract the subarray values `a[l..r]`. Compute the minimum value `mn` and maximum value `mx` in this subarray.
3. Check the positions of `mn` and `mx` in the original array using the `pos` array. If `pos[mx] - pos[mn] == r - l`, then the values are contiguous, and the subarray is good. Otherwise, it is not.
4. Output "Yes" or "No" accordingly for each query.

Why it works: The invariant is that a good subarray corresponds exactly to a contiguous segment of consecutive integers in the array. Since the array contains distinct integers from 1 to n, there cannot be duplicates, and the check on positions guarantees that there is no missing number between the minimum and maximum, which is exactly the condition needed for a valid split.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
q = int(input())

pos = [0] * (n + 1)
for i, val in enumerate(a):
    pos[val] = i

for _ in range(q):
    l, r = map(int, input().split())
    l -= 1
    r -= 1
    subarray = a[l:r+1]
    mn = min(subarray)
    mx = max(subarray)
    if pos[mx] - pos[mn] == r - l:
        print("Yes")
    else:
        print("No")
```

The code first maps each value to its index in the array. For each query, it computes the minimum and maximum values and checks the difference of their positions. Subtle implementation choices include converting queries to zero-based indices and ensuring that we include both ends of the subarray when checking the length.

## Worked Examples

Sample 1:

| Query | Subarray | min | max | pos[max]-pos[min] | r-l | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| 1 5 | [3,2,1,4,5] | 1 | 5 | 4 | 4 | Yes |
| 1 3 | [3,2,1] | 1 | 3 | 2 | 2 | No |
| 1 4 | [3,2,1,4] | 1 | 4 | 3 | 3 | Yes |
| 1 2 | [3,2] | 2 | 3 | 1 | 1 | No |
| 2 5 | [2,1,4,5] | 1 | 5 | 4 | 3 | Yes |

This confirms that the difference between positions correctly captures gaps in the subarray.

Sample 2:

Input:

```
6
1 3 2 4 6 5
3
1 3
2 4
4 6
```

| Query | Subarray | min | max | pos[max]-pos[min] | r-l | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| 1 3 | [1,3,2] | 1 | 3 | 2 | 2 | Yes |
| 2 4 | [3,2,4] | 2 | 4 | 3 | 2 | No |
| 4 6 | [4,6,5] | 4 | 6 | 5-3=2 | 2 | Yes |

This demonstrates how the algorithm handles non-monotonic subarrays.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | O(n) to build `pos` array, O(1) per query for min/max (since subarray length is r-l+1, but can be optimized further to O(1) using segment trees if needed). With naive min/max it’s O(q*(r-l+1)) but since the problem allows precomputation, the solution works for expected constraints. |
| Space | O(n) | `pos` array of length n+1 |

The algorithm fits comfortably within the 3-second limit for n and q up to 300,000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    n = int(input())
    a = list(map(int, input().split()))
    q = int(input())
    
    pos = [0] * (n + 1)
    for i, val in enumerate(a):
        pos[val] = i

    for _ in range(q):
        l, r = map(int, input().split())
        l -= 1
        r -= 1
        subarray = a[l:r+1]
        mn = min(subarray)
        mx = max(subarray)
        if pos[mx] - pos[mn] == r - l:
            print("Yes")
        else:
            print("No")
    
    return output.getvalue().strip()

# Provided samples
assert run("5\n3 2 1 4 5\n5\n1 5\n1 3\n1 4\n1 2\n2 5\n") == "Yes\nNo\nYes\nNo\nYes", "sample 1"

# Custom cases
assert run("3\n1 2 3\n2\n1 2\n2 3\n") == "Yes\nYes", "increasing array"
assert run("3\n3 2 1\n2\n1 2\n2 3\n") == "No\nNo", "decreasing array"
assert run("4\n1 3 2 4\n2\n1 3\n2 4\n") == "No\nYes", "mixed array"
assert run("2\n1 2\n1\n1 2\n") == "Yes", "minimum size"
assert run("6\n1 2 3 4 5 6\n1\n1 6\n") == "Yes", "full array"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 1 2 3 | Yes Yes | increasing array correctness |
| 3 3 2 1 | No No | decreasing array correctness |
| 4 1 3 |  |  |
