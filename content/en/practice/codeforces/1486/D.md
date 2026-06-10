---
title: "CF 1486D - Max Median"
description: "We are asked to find the largest possible median among all contiguous subarrays of a given array with length at least $k$."
date: "2026-06-10T23:10:14+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 1486
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 703 (Div. 2)"
rating: 2100
weight: 1486
solve_time_s: 186
verified: false
draft: false
---

[CF 1486D - Max Median](https://codeforces.com/problemset/problem/1486/D)

**Rating:** 2100  
**Tags:** binary search, data structures, dp  
**Solve time:** 3m 6s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to find the largest possible median among all contiguous subarrays of a given array with length at least $k$. In other words, from the input array $a$ of length $n$, we must consider every segment of length $k$ or longer, compute the median of that segment, and return the maximum of these medians. The median of an array of size $m$ is the element at position $\lfloor (m + 1) / 2 \rfloor$ if the array is sorted.

The constraints indicate that $n$ can be as large as $2 \cdot 10^5$. A naive solution that examines all subarrays explicitly would require roughly $O(n^2)$ operations, which would be up to $4 \cdot 10^{10}$ operations in the worst case. This is far beyond the 2-second time limit, so we need an approach that is roughly linear or $O(n \log n)$ at most. The array elements are bounded by $1$ to $n$, which hints at the possibility of value-based processing rather than fully sorting subarrays repeatedly.

Non-obvious edge cases include subarrays where multiple elements are equal, or when the largest median occurs in a subarray longer than $k$. For example, for $n = 5$, $k = 3$, and $a = [1, 2, 2, 2, 1]$, the subarray $[2, 2, 2]$ has median 2, and longer subarrays like $[1, 2, 2, 2]$ also have median 2. Careless approaches that just pick medians from first k-length subarrays may miss the true maximum.

Another subtle case occurs when all elements are equal. Any subarray will have the same median, so the maximum median is trivially that element.

## Approaches

The brute-force method would be to iterate over all subarrays of length at least $k$, sort each subarray, and take the median. This approach is correct because it literally computes the medians of all subarrays, but the worst-case complexity is $O(n^3 \log n)$ if we account for all subarray sizes and sorting, which is infeasible for $n$ up to $2 \cdot 10^5$.

The key insight for an efficient solution is to recognize that we do not need the exact sorted order to know whether a candidate median $m$ is possible. For a subarray of length $l \ge k$ to have median at least $m$, more than half of its elements must be $\ge m$. This is equivalent to marking elements as +1 if $\ge m$ and -1 otherwise, then checking whether there exists a subarray of length at least $k$ whose cumulative sum is positive. This transforms the problem into a variant of the maximum subarray sum problem.

With this transformation, we can perform a binary search over candidate medians. Since the elements are bounded between 1 and $n$, there are at most $n$ distinct candidates. For each candidate median, we use prefix sums and a sliding window to efficiently check if a subarray of length at least $k$ exists with enough large elements to make the median at least that candidate. This gives an overall $O(n \log n)$ solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3 \log n)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Initialize a binary search on candidate median values between 1 and $n$. Each candidate $m$ represents the median we are testing.
2. For a given candidate $m$, transform the array $a$ into an array $b$ where $b[i] = 1$ if $a[i] \ge m$, and $-1$ otherwise. This allows us to track whether a subarray has enough large elements.
3. Compute prefix sums $s[i] = b[0] + b[1] + \dots + b[i-1]$. The prefix sum difference $s[r] - s[l]$ gives the net count of large elements minus small elements in the subarray $a[l..r-1]$.
4. To check if a subarray of length at least $k$ exists with median at least $m$, iterate over $r = k$ to $n$ and maintain the minimum prefix sum $min\_prefix = \min(s[0..r-k])$. If $s[r] - min\_prefix > 0$, then the subarray ending at $r-1$ has more +1s than -1s, so the median is at least $m$.
5. If such a subarray exists, the candidate median is feasible; otherwise it is not. Adjust the binary search bounds accordingly until the largest feasible median is found.

Why it works: The invariant maintained is that any subarray with more than half of its elements $\ge m$ corresponds to a positive difference in transformed prefix sums. Binary search ensures that the maximal $m$ is found, and the prefix sum check guarantees correctness for subarrays of length at least $k$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_median(n, k, a):
    low, high = 1, n
    ans = 1
    while low <= high:
        mid = (low + high) // 2
        b = [1 if x >= mid else -1 for x in a]
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i+1] = prefix[i] + b[i]
        min_prefix = 0
        found = False
        for r in range(k, n+1):
            min_prefix = min(min_prefix, prefix[r-k])
            if prefix[r] - min_prefix > 0:
                found = True
                break
        if found:
            ans = mid
            low = mid + 1
        else:
            high = mid - 1
    return ans

if __name__ == "__main__":
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    print(max_median(n, k, a))
```

The code first performs a binary search over possible median values. For each candidate, it transforms the array to +1/-1 values and computes prefix sums. A sliding window of size at least $k$ ensures we efficiently check whether a valid subarray exists. Updating `min_prefix` is subtle; it must always represent the minimum prefix sum from the start to `r-k` to capture all subarrays of length at least $k$.

## Worked Examples

Sample 1: $n = 5, k = 3, a = [1,2,3,2,1]$

| Candidate median | b array | prefix sums | min_prefix | Found? |
| --- | --- | --- | --- | --- |
| 3 | [-1,-1,1,-1,-1] | [0,-1,-2,-1,-2,-3] | 0, -1, -2 | True |
| 2 | [-1,1,1,1,-1] | [0,-1,0,1,2,1] | 0 | Found at r=4 |

This demonstrates that 2 is feasible while 3 is not.

Sample 2: $n=4, k=2, a=[3,1,4,2]$

| Candidate median | b array | prefix sums | min_prefix | Found? |
| --- | --- | --- | --- | --- |
| 3 | [1,-1,1,-1] | [0,1,0,1,0] | 0 | Found at r=3 |
| 4 | [-1,-1,1,-1] | [0,-1,-2,-1,-2] | 0 | No |

Maximum feasible median is 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Binary search over n candidate medians, each requiring O(n) prefix sum computation |
| Space | O(n) | Prefix sum array and transformed array |

With n up to $2 \cdot 10^5$, $O(n \log n) \approx 4 \cdot 10^6$ operations, which comfortably fits within 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    return str(max_median(n, k, a))

# Provided samples
assert run("5 3\n1 2 3 2 1\n") == "2", "sample 1"
assert run("4 2\n3 1 4 2\n") == "3", "sample 2"

# Custom cases
assert run("1 1\n7\n") == "7", "single element"
assert run("5 5\n2 2
```
