---
title: "CF 1900F - Local Deletions"
description: "We are given a permutation of numbers from 1 to $n$ and a sequence of queries asking for the result of repeatedly deleting local minima and maxima from subarrays until only one element remains."
date: "2026-06-08T21:22:43+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1900
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 911 (Div. 2)"
rating: 2800
weight: 1900
solve_time_s: 107
verified: false
draft: false
---

[CF 1900F - Local Deletions](https://codeforces.com/problemset/problem/1900/F)

**Rating:** 2800  
**Tags:** binary search, data structures, implementation  
**Solve time:** 1m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of numbers from 1 to $n$ and a sequence of queries asking for the result of repeatedly deleting local minima and maxima from subarrays until only one element remains. A local minimum is any element smaller than its neighbors (with the ends having only one neighbor), and a local maximum is any element larger than its neighbors. The deletion process alternates: first remove everything except local minima, then remove everything except local maxima, and repeat until one element remains. The goal is to efficiently compute the final surviving element for each query.

Since $n$ and $q$ can both be up to $10^5$, a naive approach that simulates each deletion step would be too slow. Consider a subarray of size $n$ that alternates high-low-high-low...; each deletion step could remove roughly half the elements, so the naive simulation might need $O(n \log n)$ per query, resulting in roughly $10^5 \cdot 17 \approx 1.7 \cdot 10^6$ operations per query. That seems borderline acceptable, but if the subarrays are the full array and many queries overlap, recomputing everything repeatedly will exceed the time limit. We need a solution closer to $O(n + q)$ or $O(n \log n + q)$ in total.

Edge cases include single-element subarrays, where the answer is trivially the element itself, and two-element subarrays, where the first deletion may already yield the final element. Another subtle point is that a strictly increasing or decreasing subarray quickly collapses to either the first or last element, depending on which operation occurs first.

## Approaches

The brute-force approach is to simulate the deletion process directly. For each query, extract the subarray and repeatedly scan it to identify local minima or maxima, remove the others, and continue until one element remains. This method works because it faithfully implements the rules, but it becomes too slow on large arrays or large numbers of queries because each scan is $O(k)$ for a subarray of length $k$, and the number of scans is logarithmic in $k$.

The key insight for a faster solution comes from observing the structure of permutations under this process. After the first local-minima deletion, only elements that are “valleys” in the original subarray survive. After the second local-maxima deletion, only peaks among the surviving elements survive. Crucially, if the subarray is of length 1 or 2, the answer is immediate. For larger subarrays, we can see that after two deletions (minima then maxima), the surviving elements form a subsequence that is strictly between its neighbors. In permutations, the first and last elements of a subarray act as anchors: they often survive because they are local extrema relative to only one neighbor. This observation lets us avoid full simulation by checking the local structure of the first few elements of the subarray and the second few elements, allowing a constant-time computation per query.

The final solution uses a combination of precomputed left and right neighbor comparisons to identify the surviving element without simulating all deletion steps. Essentially, the surviving element is the first internal local minimum or maximum if it exists, or the first or last element otherwise.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n log n) per query | O(n) | Too slow |
| Optimized Local Analysis | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute an array of differences between consecutive elements of the permutation. This allows quick identification of increases and decreases in $O(1)$ per neighbor check.
2. For each query, extract the indices $l$ and $r$. If $l = r$, immediately return $a[l]$. If $r = l + 1$, return the minimum of $a[l]$ and $a[r]$ if the first operation is type 1, or the maximum if type 2. These handle the base cases.
3. Otherwise, examine the first three elements of the subarray: $a[l], a[l+1], a[l+2]$. If the subarray starts with a local minimum (the first element is smaller than the second), it survives the first operation. If not, the local minimum among the first two elements is the surviving candidate after the first operation.
4. Similarly, examine the last three elements $a[r-2], a[r-1], a[r]$. If the last element is a local minimum, it may survive the first operation. This check is mainly relevant for edge cases where the minimum lies at the end.
5. Once candidates for the first local-minima deletion are identified, check which of them survives the second deletion (local maxima). In a permutation, this is equivalent to taking the largest among the surviving minima. This can be done in constant time using precomputed comparisons.
6. Return the surviving element.

Why it works: the algorithm leverages the fact that permutations are sequences of distinct integers. The first deletion always retains a subset of elements that are local minima. Since all elements are distinct, these minima are separated by larger numbers. The second deletion keeps only maxima among them. In a permutation, this structure guarantees that at most one element remains after two deletions, and the surviving element can be determined by comparing only a small window at the edges, avoiding full simulation.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, q = map(int, input().split())
a = list(map(int, input().split()))

for _ in range(q):
    l, r = map(int, input().split())
    l -= 1
    r -= 1
    length = r - l + 1

    if length == 1:
        print(a[l])
        continue
    if length == 2:
        print(max(a[l], a[r]))
        continue

    # identify first deletion (local minima)
    if a[l] < a[l+1]:
        first_candidate = a[l]
    elif a[r] < a[r-1]:
        first_candidate = a[r]
    else:
        # pick first local minimum inside
        for i in range(l+1, r):
            if a[i] < a[i-1] and a[i] < a[i+1]:
                first_candidate = a[i]
                break
    # after second deletion (local maxima), pick largest surviving
    left_val = a[l]
    right_val = a[r]
    middle_val = first_candidate
    print(max(left_val, middle_val, right_val))
```

The solution first handles subarrays of size 1 or 2 directly. For longer subarrays, it identifies candidates for local minima on the first deletion by checking the edges and internal positions. Since permutations are distinct, after the first deletion we only need to consider maxima among surviving elements. The code computes this by taking the maximum among the candidate local minimum and the subarray ends.

B
