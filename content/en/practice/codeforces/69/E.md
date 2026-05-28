---
title: "CF 69E - Subsegments"
description: "We are given an array of integers and a fixed window size k. For each contiguous subarray (segment) of length k, we need to find the largest element that appears exactly once within that segment. If no element appears exactly once, we output \"Nothing\"."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 69
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 63 (Div. 2)"
rating: 1800
weight: 69
solve_time_s: 82
verified: true
draft: false
---

[CF 69E - Subsegments](https://codeforces.com/problemset/problem/69/E)

**Rating:** 1800  
**Tags:** data structures, implementation  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and a fixed window size `k`. For each contiguous subarray (segment) of length `k`, we need to find the largest element that appears exactly once within that segment. If no element appears exactly once, we output "Nothing".

The input starts with the array size `n` and the segment length `k`, followed by `n` integers. The output is `n-k+1` lines, each corresponding to one segment.

The constraints are significant: `n` can be up to 100,000, which rules out any solution that does more than roughly `O(n log n)` or `O(n)` work per test case if we want to stay under 1 second. A naive approach that checks all elements in each segment for uniqueness would be `O(n*k)`, which can reach 10 billion operations in the worst case and will time out.

A non-obvious edge case occurs when a segment has all elements duplicated. For example, if the segment is `[2, 2, 2]`, there is no element that appears exactly once. A careless implementation might try to return the maximum anyway and produce `2` instead of "Nothing". Another edge case is when the array has negative numbers or large values; the algorithm must correctly compare them without assuming positivity.

## Approaches

The brute-force solution iterates over every segment of length `k`. For each segment, we count the frequency of each number and then pick the maximum among numbers with frequency exactly one. This works because it guarantees correct results by direct inspection, but the complexity is `O(n*k)` - for `n=10^5` and `k=10^5`, that is too slow.

The key observation for a faster approach is that we can maintain a sliding window of size `k` and update frequencies as we move from one segment to the next. Instead of recomputing frequencies from scratch for every segment, we decrement the count of the element leaving the window and increment the count of the element entering the window. This reduces the work per step to essentially `O(log k)` if we maintain the set of candidates in a data structure that allows extracting the maximum quickly, like a balanced BST or a `SortedSet`.

In this problem, we use a `SortedSet` of elements that appear exactly once in the current window. Whenever a number’s frequency changes from one to two, we remove it from the set; when it drops from two to one, we add it. The maximum of this set is exactly the number we need to output. If the set is empty, we print "Nothing".

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*k) | O(k) | Too slow |
| Sliding Window with Frequency Map + SortedSet | O(n log k) | O(k) | Accepted |

## Algorithm Walkthrough

1. Initialize a frequency dictionary to count occurrences of elements in the current window. Initialize a `SortedSet` (or equivalent) to keep all elements with frequency exactly one.
2. Populate the frequency map and set for the first window of length `k`. For each element, increment its count; if the count becomes one, add it to the set; if it becomes two, remove it.
3. Output the maximum of the set for the first window. If the set is empty, print "Nothing".
4. Slide the window one element at a time. For each step, remove the frequency of the element leaving the window: if its frequency drops from two to one, add it back to the set; if it drops from one to zero, remove it. Then increment the frequency of the new element entering the window: if it becomes one, add it; if it becomes two, remove it.
5. After updating the set for the new window, output the maximum element or "Nothing" if the set is empty. Repeat until all windows are processed.

Why it works: At every step, the set contains all numbers that occur exactly once in the current window. By updating incrementally, we never miss elements or include duplicates, so the maximum of the set is guaranteed to satisfy the problem requirement. The sliding window guarantees we only spend `O(log k)` time per step if using a balanced structure, keeping the algorithm efficient.

## Python Solution

```python
import sys
input = sys.stdin.readline
from sortedcontainers import SortedSet
from collections import defaultdict

n, k = map(int, input().split())
a = [int(input()) for _ in range(n)]

freq = defaultdict(int)
unique = SortedSet()

# initialize first window
for i in range(k):
    freq[a[i]] += 1
for i in range(k):
    if freq[a[i]] == 1:
        unique.add(a[i])
    elif freq[a[i]] == 2:
        unique.discard(a[i])

# output for the first window
print(unique[-1] if unique else "Nothing")

# slide the window
for i in range(k, n):
    left = a[i - k]
    freq[left] -= 1
    if freq[left] == 1:
        unique.add(left)
    elif freq[left] == 0:
        unique.discard(left)

    right = a[i]
    freq[right] += 1
    if freq[right] == 1:
        unique.add(right)
    elif freq[right] == 2:
        unique.discard(right)

    print(unique[-1] if unique else "Nothing")
```

The solution starts by building a frequency map for the first window and a `SortedSet` of elements that appear exactly once. When sliding the window, we carefully update counts and adjust the set accordingly. The order of operations matters: decrement first, increment second, because the window changes from left to right.

## Worked Examples

**Sample 1:**

Input:

```
5 3
1
2
2
3
3
```

| Window | freq | unique | Output |
| --- | --- | --- | --- |
| [1,2,2] | {1:1,2:2} | {1} | 1 |
| [2,2,3] | {2:2,3:1} | {3} | 3 |
| [2,3,3] | {2:1,3:2} | {2} | 2 |

This demonstrates correct handling of duplicates and proper updates when elements enter and leave the window.

**Custom Input:**

Input:

```
6 2
4
4
5
6
5
7
```

| Window | freq | unique | Output |
| --- | --- | --- | --- |
| [4,4] | {4:2} | {} | Nothing |
| [4,5] | {4:1,5:1} | {4,5} | 5 |
| [5,6] | {5:1,6:1} | {5,6} | 6 |
| [6,5] | {6:1,5:1} | {5,6} | 6 |
| [5,7] | {5:1,7:1} | {5,7} | 7 |

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log k) | Sliding window updates involve `SortedSet` operations per element, which are log(size of window) |
| Space | O(k) | Frequency map and `SortedSet` store at most `k` elements |

The solution easily fits within the 1-second time limit for `n=10^5` and uses under 256 MB memory.

## Test Cases

```python
import sys, io
from contextlib import redirect_stdout

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    f = io.StringIO()
    with redirect_stdout(f):
        # insert solution code here
        import sys
        input = sys.stdin.readline
        from sortedcontainers import SortedSet
        from collections import defaultdict

        n, k = map(int, input().split())
        a = [int(input()) for _ in range(n)]

        freq = defaultdict(int)
        unique = SortedSet()

        for i in range(k):
            freq[a[i]] += 1
        for i in range(k):
            if freq[a[i]] == 1:
                unique.add(a[i])
            elif freq[a[i]] == 2:
                unique.discard(a[i])
        print(unique[-1] if unique else "Nothing")

        for i in range(k, n):
            left = a[i - k]
            freq[left] -= 1
            if freq[left] == 1:
                unique.add(left)
            elif freq[left] == 0:
                unique.discard(left)

            right = a[i]
            freq[right] += 1
            if freq[right] == 1:
                unique.add(right)
            elif freq[right] == 2:
                unique.discard(right)

            print(unique[-1] if unique else "Nothing")
    return f.getvalue().strip()

# provided sample
assert run("5 3\n1\n2\n2\n3\n3\n") == "1\n3\n2"

# custom cases
assert run("2 1\n1\n1\n") == "1\n1", "single element windows"
assert run("3 3\n2\n2\n2\n") == "Nothing", "all duplicates"
assert run("4
```
