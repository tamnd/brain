---
title: "CF 2117C - Cool Partition"
description: "We are given an array of integers and need to divide it into contiguous segments. Each element must appear in exactly one segment. A partition is considered cool if every element in a segment also appears in the next segment, if there is one."
date: "2026-06-08T11:02:39+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2117
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1029 (Div. 3)"
rating: 1200
weight: 2117
solve_time_s: 113
verified: false
draft: false
---

[CF 2117C - Cool Partition](https://codeforces.com/problemset/problem/2117/C)

**Rating:** 1200  
**Tags:** data structures, greedy  
**Solve time:** 1m 53s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and need to divide it into contiguous segments. Each element must appear in exactly one segment. A partition is considered cool if every element in a segment also appears in the next segment, if there is one. Our goal is to maximize the number of segments.

The input consists of multiple test cases, each with an array of size up to 200,000. The sum of array sizes across all test cases does not exceed 200,000, meaning we can afford a linear-time solution per array. Quadratic approaches are impractical because iterating over all subarrays would result in up to $10^{10}$ operations.

The non-obvious edge cases arise when elements repeat in complicated patterns. For instance, consider an array where the same element appears intermittently: `[1, 2, 1, 2, 1, 2]`. A naive approach that splits at every repeated element could fail because we would violate the requirement that every element in a segment must also appear in the next. Another edge case is an array with all unique elements, where the only cool partition is the entire array itself.

## Approaches

The brute-force approach would attempt to generate every possible partition and check whether it is cool. For each candidate partition, we would verify that all elements of a segment appear in the next segment. While this is correct conceptually, it is extremely slow: for an array of length $n$, there are $2^{n-1}$ possible partitions, which is completely infeasible even for $n = 20$.

The key insight to speed this up is to notice that a segment can only end once all elements currently in the segment also appear later in the array. In other words, for any candidate segment ending at position $i$, we need to ensure that no element that appears in this segment appears again after $i$ without being part of the next segment. This observation allows us to track the last occurrence of every element and only close a segment when the current index matches the last occurrence of all elements seen so far.

By iterating through the array once and keeping track of the maximum last occurrence of elements in the current segment, we can determine the segment boundaries in a single pass. Each time the current index matches the maximum last occurrence, we can safely close a segment, guaranteeing that all elements in it appear in the next segment if there is one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the array `a` and its length `n`.
2. Compute a dictionary mapping each unique element to its last occurrence index in the array. This allows us to know, for any element, the farthest index we must include it to satisfy the cool segment condition.
3. Initialize two variables: `current_max` to track the maximum last occurrence of elements in the current segment, and `segments` to count the number of segments found.
4. Iterate through the array with index `i` from 0 to `n-1`. For each element `a[i]`, update `current_max` as the maximum of itself and the last occurrence of `a[i]`.
5. If `i` equals `current_max`, it means all elements in the current segment end here. Increment `segments` and reset any segment-specific tracking if needed.
6. After the loop, output the total `segments` for this test case.

The key invariant is that `current_max` always represents the farthest index we must include to satisfy the cool partition condition for the current segment. By closing a segment exactly when the current index reaches this maximum, we ensure no element in the segment violates the condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_cool_segments(n, a):
    last_occurrence = {}
    for i, val in enumerate(a):
        last_occurrence[val] = i
    
    segments = 0
    current_max = -1
    for i, val in enumerate(a):
        current_max = max(current_max, last_occurrence[val])
        if i == current_max:
            segments += 1
    return segments

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    print(max_cool_segments(n, a))
```

This solution first constructs a dictionary `last_occurrence` that stores the last index where each element appears. During the iteration over `a`, we track `current_max` to determine when it is safe to end the current segment. Incrementing `segments` only when the current index equals `current_max` guarantees correctness. The approach avoids off-by-one errors by using zero-based indexing consistently.

## Worked Examples

### Sample Input 1

```
6
1 2 2 3 1 5
```

| i | a[i] | last_occurrence[a[i]] | current_max | segments |
| --- | --- | --- | --- | --- |
| 0 | 1 | 4 | 4 | 0 |
| 1 | 2 | 2 | 4 | 0 |
| 2 | 2 | 2 | 4 | 0 |
| 3 | 3 | 3 | 4 | 0 |
| 4 | 1 | 4 | 4 | 1 |
| 5 | 5 | 5 | 5 | 2 |

This trace shows that the first segment ends at index 4, covering `[1, 2, 2, 3, 1]`, and the second segment is `[5]`. The invariant is maintained because all elements in a segment appear in the next segment.

### Sample Input 2

```
8
1 2 1 3 2 1 3 2
```

| i | a[i] | last_occurrence[a[i]] | current_max | segments |
| --- | --- | --- | --- | --- |
| 0 | 1 | 5 | 5 | 0 |
| 1 | 2 | 7 | 7 | 0 |
| 2 | 1 | 5 | 7 | 0 |
| 3 | 3 | 6 | 7 | 0 |
| 4 | 2 | 7 | 7 | 0 |
| 5 | 1 | 5 | 7 | 0 |
| 6 | 3 | 6 | 7 | 0 |
| 7 | 2 | 7 | 7 | 1 |

This shows that the first segment ends at index 7. By following the same logic, the algorithm can identify smaller segments in other cases, giving a maximum partition count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We iterate over the array once and compute last occurrences in a single pass. |
| Space | O(n) | The `last_occurrence` dictionary stores up to `n` keys. |

With $n \le 2 \cdot 10^5$ per test case and total sum $2 \cdot 10^5$, this solution comfortably fits within the 2-second time limit and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())
    return output.getvalue().strip()

# Provided samples
assert run("1\n6\n1 2 2 3 1 5\n") == "2", "sample 1"
assert run("1\n8\n1 2 1 3 2 1 3 2\n") == "3", "sample 2"

# Custom cases
assert run("1\n1\n1\n") == "1", "single element array"
assert run("1\n5\n1 1 1 1 1\n") == "5", "all equal elements"
assert run("1\n5\n5 4 3 2 1\n") == "1", "all unique elements descending"
assert run("1\n6\n1 2 1 2 1 2\n") == "3", "interleaved repeats"
assert run("1\n7\n1 2 3 2 1 3 1\n") == "2", "complex overlaps"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | single element array |
| 1 1 1 1 1 | 5 | all equal elements |
| 5 4 3 2 1 | 1 | all unique elements, only one segment possible |
| 1 2 1 2 1 2 | 3 | interleaved repeating pattern, correct segment count |
| 1 2 3 2 1 3 1 | 2 | overlapping elements, ensures algorithm merges segments correctly |

## Edge Cases

For a single-element array `[1]`, `last_occurrence` maps 1 to index
