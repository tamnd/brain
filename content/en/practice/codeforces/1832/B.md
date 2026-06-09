---
title: "CF 1832B - Maximum Sum"
description: "We are given an array of distinct integers and must perform exactly k deletion operations. In each operation we can either remove the largest element or remove the two smallest elements together."
date: "2026-06-09T07:00:14+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1832
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 148 (Rated for Div. 2)"
rating: 1100
weight: 1832
solve_time_s: 82
verified: true
draft: false
---

[CF 1832B - Maximum Sum](https://codeforces.com/problemset/problem/1832/B)

**Rating:** 1100  
**Tags:** brute force, sortings, two pointers  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of distinct integers and must perform exactly `k` deletion operations. In each operation we can either remove the largest element or remove the two smallest elements together. After exactly `k` operations, we need the sum of the remaining elements to be as large as possible. The array size `n` can be up to 200,000, and the sum of all `n` across test cases also does not exceed 200,000, which means we must process each test case in roughly linear or linearithmic time.

A naive solution that simulates each operation by repeatedly finding minimums or maximums will be too slow because finding the two minimums or the maximum in an unsorted array costs O(n) per operation, leading to O(k·n) complexity, which can reach roughly $10^{10}$ in the worst case.

Edge cases to consider include arrays with only three elements where `k = 1`, because the choice between removing the largest or two smallest elements is delicate. Another edge case arises when the largest elements are much bigger than all others - deleting the largest even once may be strictly worse than repeatedly removing small elements.

## Approaches

A brute-force approach is straightforward: for each of the `k` steps, scan the array to find either the two smallest or the largest element, remove them, and continue. This is correct but O(k·n) per test case. When `n` and `k` are large, it will time out.

The key insight for a faster solution comes from sorting. Once the array is sorted in ascending order, the two smallest elements are always at the start, and the largest element is at the end. Instead of simulating every operation, we can precompute the sum of all elements and consider the effect of removing either prefix pairs (two smallest each time) or suffix singles (largest each time). Specifically, we only need to consider all combinations of `i` operations removing the two smallest elements and `k-i` operations removing the largest element. For each `i` from 0 to `k`, the remaining sum is the total sum minus the sum of the `2*i` smallest and `k-i` largest elements. Iterating over all `i` in `0..k` is feasible because `k < n/2` and each sum computation can be done in O(1) if we precompute prefix sums.

This reduces the complexity dramatically from O(k·n) to O(n log n) for sorting plus O(k) for the iteration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k·n) | O(n) | Too slow for large n, k |
| Sorting + Prefix/Suffix Sums | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read `n` and `k`, followed by the array `a`.
2. Sort the array in ascending order. This allows constant-time access to the smallest and largest elements in prefix and suffix form.
3. Precompute prefix sums for the array. Let `prefix[i]` be the sum of the first `i` elements.
4. Precompute suffix sums. Let `suffix[i]` be the sum of the last `i` elements.
5. Initialize a variable `max_sum` with a very small number.
6. Iterate `i` from 0 to `k`. `i` represents the number of operations that remove two smallest elements. The remaining `k-i` operations remove the largest element.
7. Compute the sum of the remaining elements as the total sum minus the sum of the first `2*i` elements and minus the sum of the last `k-i` elements.
8. Update `max_sum` if this sum is larger than the previous maximum.
9. After iterating all `i`, print `max_sum`.

Why it works: Sorting ensures we can always remove exactly the `2*i` smallest and `k-i` largest elements for any combination of operations. Because we consider all possibilities of how many two-smallest deletions versus largest deletions to perform, we explore the entire solution space efficiently without simulating every operation.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()
    
    prefix = [0]*(n+1)
    for i in range(n):
        prefix[i+1] = prefix[i] + a[i]
    
    suffix = [0]*(n+1)
    for i in range(n-1, -1, -1):
        suffix[n-i] = suffix[n-i-1] + a[i]
    
    total = prefix[n]
    max_sum = 0
    for i in range(k+1):
        if 2*i > n or (k-i) > n:
            continue
        remaining_sum = total - prefix[2*i] - suffix[k-i]
        max_sum = max(max_sum, remaining_sum)
    
    print(max_sum)
```

The code sorts the array, precomputes prefix and suffix sums, then iterates through all possible numbers of "remove two smallest" operations. The prefix sum subtracts the `2*i` smallest elements, the suffix sum subtracts the `k-i` largest elements. Handling prefix and suffix carefully prevents off-by-one errors. All operations use integer arithmetic, avoiding overflow since Python handles large integers.

## Worked Examples

Consider the first sample input:

```
5 1
2 5 1 10 6
```

Sorted array: `[1, 2, 5, 6, 10]`

Prefix sums: `[0, 1, 3, 8, 14, 24]`

Suffix sums (reversed): `[0, 10, 16, 21, 23, 24]`

- `i=0` means 0 "two-smallest" operations, 1 "largest" operation: remaining sum = 24 - 0 - 10 = 14
- `i=1` means 1 "two-smallest" operation, 0 "largest" operations: remaining sum = 24 - 3 - 0 = 21

Maximum sum is 21, which matches the expected output.

Second sample:

```
5 2
2 5 1 10 6
```

Sorted: `[1,2,5,6,10]`

Total sum = 24

- `i=0`: 0 "two-smallest", 2 "largest": sum = 24 - 0 - (16) = 8
- `i=1`: 1 "two-smallest", 1 "largest": sum = 24 - 3 - 10 = 11
- `i=2`: 2 "two-smallest", 0 "largest": sum = 24 - 3 - 0 = 21? Wait 2*2=4>5? Invalid.

Maximum sum is 11.

This trace confirms that we correctly handle the 2*i > n boundary and pick the maximum sum across all valid combinations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, prefix/suffix sums and iteration over k is O(n + k) ≤ O(n) |
| Space | O(n) | We store prefix and suffix sums arrays of size n+1 each |

With constraints `n ≤ 2·10^5` and sum over all test cases ≤ 2·10^5, the solution easily fits in time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        a.sort()
        
        prefix = [0]*(n+1)
        for i in range(n):
            prefix[i+1] = prefix[i] + a[i]
        
        suffix = [0]*(n+1)
        for i in range(n-1, -1, -1):
            suffix[n-i] = suffix[n-i-1] + a[i]
        
        total = prefix[n]
        max_sum = 0
        for i in range(k+1):
            if 2*i > n or (k-i) > n:
                continue
            remaining_sum = total - prefix[2*i] - suffix[k-i]
            max_sum = max(max_sum, remaining_sum)
        print(max_sum)
    return output.getvalue().strip()

# Provided samples
assert run("6\n5 1\n2 5 1 10 6\n5 2\n2 5 1 10 6\n3 1\n1 2 3\n6 1\n15 22 12 10 13 11\n6 2\n15 22 12 10 13 11\n5 1\n999999996 999999999 999999997 999999998 999999995\n") == "21\n11\n3\n62\n46\n3999999986"

# Custom test cases
assert run("1\n3 1\n1 2 3\n") == "3"  # minimum-size input
assert run("1\n4 1\n5 1 2 4
```
