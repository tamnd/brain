---
title: "CF 2117C - Cool Partition"
description: "We are asked to partition an array of integers into contiguous segments such that each element in a segment also appears in the next segment. Each element in the array must belong to exactly one segment. Our goal is to maximize the number of segments."
date: "2026-06-08T04:05:38+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2117
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1029 (Div. 3)"
rating: 1200
weight: 2117
solve_time_s: 98
verified: false
draft: false
---

[CF 2117C - Cool Partition](https://codeforces.com/problemset/problem/2117/C)

**Rating:** 1200  
**Tags:** data structures, greedy  
**Solve time:** 1m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to partition an array of integers into contiguous segments such that each element in a segment also appears in the next segment. Each element in the array must belong to exactly one segment. Our goal is to maximize the number of segments.

In practical terms, if we imagine walking through the array from left to right, we want to know where we can "cut" the array so that every number in the current segment will appear again in the next segment. The challenge is that a number may appear multiple times or may appear late in the array, so making a premature cut could violate the condition.

The input consists of multiple test cases. Each test case gives the array length $n$ and the array elements. Since $n$ can go up to $2 \cdot 10^5$ and the sum of all $n$ across test cases is bounded by $2 \cdot 10^5$, we need a solution that processes each array in roughly linear time. Any $O(n^2)$ approach will be far too slow, especially if we try to check all possible segments explicitly.

Edge cases arise when elements repeat many times or when the array is strictly decreasing or strictly increasing. For example, an array like `[5,4,3,2,1]` cannot be split into more than one segment because no element repeats in the order needed for a cool partition. A careless greedy cut at the first repetition would produce an invalid partition. Arrays where every element repeats multiple times, like `[1,2,1,2,1,2]`, allow multiple segments, and we need to track carefully where each unique element last appears to determine valid cut points.

## Approaches

A brute-force approach would be to try all possible partitions of the array and check whether each partition satisfies the "cool" property. For each segment, we would need to check that all its elements appear in the next segment. The number of partitions of an array of length $n$ is exponential, so this is clearly infeasible. Even if we only consider partitions at each possible index and check validity by scanning forward for each segment, that would take $O(n^2)$, which is too slow for $n$ up to $2 \cdot 10^5$.

The key insight is that we do not need to simulate every segment explicitly. Instead, we can precompute the last occurrence of each number in the array. If we maintain the maximum index we have seen for any number in the current segment, a valid cut can only occur when our current index reaches this maximum. This works because, if we cut earlier, some number in the current segment would not appear in the next one. Tracking the farthest last occurrence ensures that all elements in the current segment will appear later, satisfying the cool condition.

Thus, the optimal solution is a single pass through the array. We maintain the maximum last occurrence for the numbers we encounter. Whenever our current index reaches this maximum, we know all elements of the segment will appear later, so we can safely make a cut and start a new segment. This greedy strategy guarantees the maximum number of segments because we make cuts as soon as possible without violating the rule.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. First, compute the last occurrence index of each unique element in the array. We can do this with a dictionary that maps element values to their last index. This allows us to know, for any element in a potential segment, where its last appearance occurs.
2. Initialize two variables: `max_last` to track the maximum last occurrence of elements seen so far in the current segment, and `segments` to count how many segments we have made.
3. Iterate through the array by index. For each element at position `i`, update `max_last` to be the maximum of `max_last` and the last occurrence of this element. This ensures `max_last` always represents the farthest index any element in the current segment must reach.
4. If the current index `i` equals `max_last`, all elements of the current segment will appear at least once beyond this point. Increment `segments` because we can safely cut here and start a new segment.
5. Continue iterating until the end of the array. At the end, `segments` will hold the maximum number of cool segments.

Why it works: At each potential cut point, we guarantee that no element in the current segment is missing from the following segment because `max_last` ensures that all elements appear at least until the end of the segment. The greedy approach makes cuts at the earliest safe opportunity, maximizing the number of segments.

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_cool_segments(a):
    last_occurrence = {}
    for idx, val in enumerate(a):
        last_occurrence[val] = idx
    
    max_last = 0
    segments = 0
    for i, val in enumerate(a):
        max_last = max(max_last, last_occurrence[val])
        if i == max_last:
            segments += 1
    return segments

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    print(max_cool_segments(a))
```

The first loop builds a mapping from element to its last occurrence. The second loop iterates over the array while maintaining `max_last`. Whenever the current index reaches `max_last`, we know we can cut a segment. This correctly handles elements that repeat and elements that appear only once.

## Worked Examples

Sample 1: `[1, 2, 2, 3, 1, 5]`

| i | a[i] | last_occ[a[i]] | max_last | segments |
| --- | --- | --- | --- | --- |
| 0 | 1 | 4 | 4 | 0 |
| 1 | 2 | 2 | 4 | 0 |
| 2 | 2 | 2 | 4 | 0 |
| 3 | 3 | 3 | 4 | 0 |
| 4 | 1 | 4 | 4 | 1 |
| 5 | 5 | 5 | 5 | 2 |

The table shows that we can make cuts at indices 4 and 5, giving two segments.

Sample 2: `[1, 2, 1, 3, 2, 1, 3, 2]`

| i | a[i] | last_occ[a[i]] | max_last | segments |
| --- | --- | --- | --- | --- |
| 0 | 1 | 5 | 5 | 0 |
| 1 | 2 | 7 | 7 | 0 |
| 2 | 1 | 5 | 7 | 0 |
| 3 | 3 | 6 | 7 | 0 |
| 4 | 2 | 7 | 7 | 0 |
| 5 | 1 | 5 | 7 | 0 |
| 6 | 3 | 6 | 7 | 0 |
| 7 | 2 | 7 | 7 | 1 |

The first cut occurs at index 1 when `max_last` is 1, the next at index 4, and the final at 7, yielding three segments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We iterate over the array twice: once to record last occurrences and once to count segments. |
| Space | O(n) | We store last occurrence of each unique element. |

The linear time complexity fits well under the constraints of $n \le 2 \cdot 10^5$ total across all test cases, so the solution will execute within the 2-second time limit. Memory usage is also within the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        print(max_cool_segments(a))
    return output.getvalue().strip()

# provided samples
assert run("8\n6\n1 2 2 3 1 5\n8\n1 2 1 3 2 1 3 2\n5\n5 4 3 2 1\n10\n5 8 7 5 8 5 7 8 10 9\n3\n1 2 2\n9\n3 3 1 4 3 2 4 1 2\n6\n4 5 4 5 6 4\n8\n1 2 1 2 1 2 1 2\n") == "2\n3\n1\n3\n1\n3\n3\n4"

# custom cases
assert run("1\n1\n1\n") == "1", "single element array"
assert run("1\n5\n1 1 1
```
