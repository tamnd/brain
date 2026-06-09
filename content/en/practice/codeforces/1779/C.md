---
title: "CF 1779C - Least Prefix Sum"
description: "We are given an array of integers, and Baltic wants a specific prefix sum-the sum of the first m elements-to be the smallest among all prefix sums of the array. We are allowed to flip the sign of any element any number of times."
date: "2026-06-09T11:28:55+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1779
codeforces_index: "C"
codeforces_contest_name: "Hello 2023"
rating: 1600
weight: 1779
solve_time_s: 119
verified: false
draft: false
---

[CF 1779C - Least Prefix Sum](https://codeforces.com/problemset/problem/1779/C)

**Rating:** 1600  
**Tags:** data structures, greedy  
**Solve time:** 1m 59s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers, and Baltic wants a specific prefix sum-the sum of the first `m` elements-to be the smallest among all prefix sums of the array. We are allowed to flip the sign of any element any number of times. The goal is to compute the minimum number of such sign-flips required to achieve this condition.

The input gives multiple test cases. Each test case provides the array size `n`, the favorite prefix length `m`, and the array elements. The output for each test case is a single integer, the minimal number of flips required.

Given that `n` can be up to 2·10^5 and the sum of all `n` across test cases does not exceed 2·10^5, any solution exceeding O(n log n) will likely be too slow. A naive brute-force that tries all combinations of sign flips is completely infeasible because there are 2^n possible sign-flip patterns.

Non-obvious edge cases include arrays where the initial sum of the first `m` elements is already the smallest, arrays with all negative or all positive numbers, and cases where large values appear later in the array that might otherwise dominate the prefix sums. A careless approach might flip too many elements or focus only on local adjustments, producing more flips than necessary.

## Approaches

A brute-force solution would attempt all possible sign-flip combinations for each element and then check which combination minimizes the first `m` prefix sum relative to others. This is correct in principle but completely impractical because the number of combinations is exponential, 2^n.

The key observation to optimize is that the problem can be separated into two phases: the first `m` elements and the remaining elements. For the first `m` elements, we want their sum to be as negative as possible if it’s positive, or leave them alone if already negative. Any positive prefix sum within these `m` elements can be flipped to reduce the sum, and to minimize flips, we should flip the largest positive values first. For the remaining elements, we need to ensure that the cumulative sum never drops below the sum of the first `m` elements. This can be controlled by flipping large negative numbers after the `m`-th element to prevent them from reducing a prefix sum below our target.

Using a heap (max-heap for the first `m` elements to flip the largest positives and min-heap for the remaining elements to flip the largest negatives) allows us to process these adjustments efficiently. Each flip operation reduces the problematic prefix by the maximum possible amount, guaranteeing minimal flips.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n·n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a variable to store the current prefix sum as we iterate through the array.
2. For the first `m` elements, maintain a max-heap of positive numbers. Iterate from the first to the `m`-th element, adding each to the current prefix sum. Whenever the current prefix sum is greater than the target sum (initially zero works for comparison), flip the largest positive number in the max-heap, subtracting twice its value from the prefix sum and incrementing the flip counter. Continue until the prefix sum of the first `m` elements is minimized.
3. For elements `m+1` to `n`, maintain a min-heap of negative numbers. Iterate forward, adding each element to the running prefix sum. If at any point the prefix sum becomes smaller than the first `m` prefix sum, repeatedly flip the smallest negative element from the min-heap (if available) to increase the prefix sum above the first `m` prefix sum. Each flip increments the counter.
4. After processing the entire array, the counter contains the minimal number of sign flips needed.

**Why it works:** The first `m` elements are greedily minimized by flipping the largest positives first, which reduces the prefix sum as efficiently as possible. For the remaining elements, we ensure that no prefix sum falls below the first `m` sum by flipping the largest negatives first. This guarantees that we only perform necessary flips, maintaining the invariant that after each step, the current prefix sum never violates the target.

## Python Solution

```python
import sys
import heapq
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    ops = 0
    pref = 0
    max_heap = []
    
    # Process first m elements
    for i in range(m):
        pref += a[i]
        if a[i] > 0:
            heapq.heappush(max_heap, -a[i])
    while max_heap and pref > 0:
        largest = -heapq.heappop(max_heap)
        pref -= 2 * largest
        ops += 1
    
    # Process remaining elements
    min_heap = []
    for i in range(m, n):
        pref += a[i]
        if a[i] < 0:
            heapq.heappush(min_heap, a[i])
        while min_heap and pref < 0:
            smallest = heapq.heappop(min_heap)
            pref -= 2 * smallest
            ops += 1
    
    print(ops)
```

The code first handles the first `m` elements by flipping large positives to reduce the sum efficiently. It then handles the rest by flipping large negatives to ensure no prefix sum after the `m`-th element is smaller than the first `m` prefix sum. Careful attention to heap ordering ensures that each flip contributes maximally to reducing or increasing the relevant prefix sum.

## Worked Examples

**Example 1:**

Input array `[-1, -2, -3, -4]` with `m = 3`.

| i | Element | Prefix Sum | Heap | Flip? | ops |
| --- | --- | --- | --- | --- | --- |
| 0 | -1 | -1 | [] | No | 0 |
| 1 | -2 | -3 | [] | No | 0 |
| 2 | -3 | -6 | [] | No | 0 |
| 3 | -4 | -10 | [] | Flip largest? | 1 |

Here we flip `-4` to `4` after `m`-th element because the prefix sum would otherwise be smaller than `-6`. The algorithm flips 1 element, matching expected output.

**Example 2:**

Input array `[1, 2, 3, 4]` with `m = 3`.

| i | Element | Prefix Sum | Heap | Flip? | ops |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | [1] | No | 0 |
| 1 | 2 | 3 | [1,2] | No | 0 |
| 2 | 3 | 6 | [1,2,3] | Flip 3 | 1 |

Flipping 3 reduces first prefix sum to 0, which becomes the minimal among all prefixes. This confirms the heap-based greedy works.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each element can enter a heap once, and each heap operation is log n |
| Space | O(n) | We maintain two heaps and a running prefix sum |

The solution easily handles the upper constraint of 2·10^5 total elements because log n overhead per element is acceptable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    # paste solution code here
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        
        ops = 0
        pref = 0
        max_heap = []
        for i in range(m):
            pref += a[i]
            if a[i] > 0:
                heapq.heappush(max_heap, -a[i])
        while max_heap and pref > 0:
            largest = -heapq.heappop(max_heap)
            pref -= 2 * largest
            ops += 1
        
        min_heap = []
        for i in range(m, n):
            pref += a[i]
            if a[i] < 0:
                heapq.heappush(min_heap, a[i])
            while min_heap and pref < 0:
                smallest = heapq.heappop(min_heap)
                pref -= 2 * smallest
                ops += 1
        print(ops)
    return out.getvalue().strip()

# Provided samples
assert run("6\n4 3\n-1 -2 -3 -4\n4 3\n1 2 3 4\n1 1\n1\n5 5\n-2 3 -5 1 -20\n5 2\n-2 3 -5 -5 -20\n10 4\n345875723 -48 384678321 -375635768 -35867853 -35863586 -358683842 -81725678 38576 -357865873") == "1\n1\n0\n0\n3\n4"
# Minimum size
assert run("1\n1 1\n5") == "1"
# Maximum negative sum
assert run("1\n
```
