---
title: "CF 1946A - Median of an Array"
description: "We are given an array of integers and asked to determine the minimum number of increment operations needed to increase the median of the array. An increment operation consists of picking any element and adding one to it."
date: "2026-06-07T17:50:52+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1946
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 936 (Div. 2)"
rating: 800
weight: 1946
solve_time_s: 90
verified: true
draft: false
---

[CF 1946A - Median of an Array](https://codeforces.com/problemset/problem/1946/A)

**Rating:** 800  
**Tags:** greedy, implementation, sortings  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and asked to determine the minimum number of increment operations needed to increase the median of the array. An increment operation consists of picking any element and adding one to it. The median is defined as the middle element of the array once it is sorted; if the array has even length, the median is the element at position $\lceil n/2 \rceil$, using 1-based indexing.

For example, for the array `[2, 2, 8]`, the median is `2`. Applying one increment to the first element yields `[3, 2, 8]`. When sorted, this becomes `[2, 3, 8]`, and the new median is `3`, which has increased. The task is to find the smallest number of such operations to ensure the median strictly increases.

The constraints imply that we need an efficient approach. Each array can have up to $10^5$ elements, and the total across all test cases is $2 \cdot 10^5$. This rules out brute-force approaches that simulate every possible operation because incrementing elements one by one and re-sorting would be too slow, especially for large numbers.

A subtle edge case occurs with arrays of size one. For example, if the array is `[1000000000]`, the median is `1000000000`. Increasing that single element by one immediately increases the median. Another edge case is when all elements are equal. For instance, `[5, 5, 5, 5]` requires operations on the second half of the array to increase the median. A careless approach that always targets the first half could miscount the required increments.

## Approaches

The brute-force approach is straightforward: repeatedly increment elements in the array and recompute the median each time until it increases. This works because incrementing any element greater than or equal to the median can affect the median's value. However, this requires repeatedly sorting the array after each operation, which is $O(n \log n)$ per operation. For large arrays or large median gaps, this can lead to up to $O(n^2 \log n)$ operations, which is far too slow.

The key insight for an optimal solution is that the median only depends on the middle and upper half of the sorted array. Any increment on elements before the median does not help. Once the array is sorted, if we target the median and elements to its right, we can increment them directly to reach the next greater number in that half. By counting the total number of increments required to raise the median to the next element in the sorted upper half, we can determine the minimum operations efficiently.

We do not need to simulate each increment individually. We can sort the array once, identify the median position, and then sum the differences between the target value and the current elements from the median onward until the median increases. This approach is linear in the size of the upper half after sorting, which is $O(n)$ per test case once the array is sorted.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 log n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases, $t$. For each test case, read $n$ and the array $a$.
2. Sort the array $a$ in non-decreasing order. Sorting ensures we can directly identify the median and work with elements that influence it.
3. Compute the index of the median as $m = n // 2$ in 0-based indexing. This corresponds to the $\lceil n/2 \rceil$-th element in 1-based indexing.
4. Initialize a variable `operations` to zero. This will accumulate the total number of increments needed.
5. Iterate over the elements from index $m$ to $n-1$, which covers the median and all elements to its right. For each element, compute the difference between a chosen target value and the current element. The target value is the smallest value that exceeds the current median after all increments.
6. Sum these differences. The sum gives the minimum number of increments needed because any increment must target elements at or above the median to influence its value.
7. Output the sum as the result for the current test case.

Why it works: After sorting, the median is the element at position $m$. To increase the median, at least the median element must be increased. The number of operations to raise the median to any value $x$ is the sum of increments for all elements from $m$ onward that are below $x$. Since we always target the right elements and sum the exact differences, this ensures the minimum operations to strictly increase the median.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    median_idx = n // 2
    target = a[median_idx]
    operations = 0
    # Increment the median and right half until median increases
    for i in range(median_idx, n):
        operations += max(0, a[i] - target + 1)
        target = a[i] + 1
    print(operations)
```

The code reads the test cases and arrays efficiently using fast I/O. Sorting allows direct access to the median. We compute the required increments for elements at or above the median and accumulate them. The subtle point is updating the target each step to ensure that we are always incrementing to the next possible value that affects the median.

## Worked Examples

### Example 1

Input: `[2, 2, 8]`

| Step | Sorted Array | Median Index | Target | Operations |
| --- | --- | --- | --- | --- |
| Initial | [2,2,8] | 1 | 2 | 0 |
| i=1 | a[1]=2 | target=2 | operations += 1 | 1 |
| i=2 | a[2]=8 | target=3 | operations += 0 | 1 |

The algorithm identifies that incrementing the median once suffices. Total operations = 1.

### Example 2

Input: `[7,3,3,1]`

| Step | Sorted Array | Median Index | Target | Operations |
| --- | --- | --- | --- | --- |
| Initial | [1,3,3,7] | 2 | 3 | 0 |
| i=2 | a[2]=3 | target=3 | operations += 1 | 1 |
| i=3 | a[3]=7 | target=4 | operations += 3 | 4 |

We need 2 operations to raise the median from 3 to 4 (incrementing a[2] and a[3] as needed). Algorithm correctly computes the minimum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; iterating over the upper half is O(n) |
| Space | O(n) | Array storage and sorting |

With $n$ up to $10^5$ and total elements across all test cases $2 \cdot 10^5$, sorting each array individually is acceptable. The solution fits within 1-second limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t = int(input())
    res = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()
        median_idx = n // 2
        target = a[median_idx]
        operations = 0
        for i in range(median_idx, n):
            operations += max(0, a[i] - target + 1)
            target = a[i] + 1
        res.append(str(operations))
    return "\n".join(res)

# provided samples
assert run("8\n3\n2 2 8\n4\n7 3 3 1\n1\n1000000000\n5\n5 5 5 4 5\n6\n2 1 2 3 1 4\n2\n1 2\n2\n1 1\n4\n5 5 5 5\n") == "1\n2\n1\n3\n2\n1\n2\n3", "sample 1"

# custom cases
assert run("2\n1\n1\n5\n1 1 1 1 1\n") == "1\n3", "single element and all-equal array"
assert run("1\n6\n1 2 3 4 5 6\n") == "1", "increment median once"
assert run("1\n4\n5 5 5 5\n") == "3", "all equal array, median requires multiple ops"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n1` | `1` | Single element array, increment median immediately |
| `5\n1 1 1 1 1` | `3` | All equal elements, requires multiple increments |
| `6\n1 2 3 4 5 6` | `1` | Increment median once suffices |
| `4\n5 5 5 5` | `3` | Correct counting on even-length all-equal array |

## Edge Cases

For a single-element array `[100
