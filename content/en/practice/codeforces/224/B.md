---
title: "CF 224B - Array"
description: "We are given an array of integers and a number k. The task is to find a contiguous subarray, or segment, such that it contains exactly k distinct integers."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 224
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 138 (Div. 2)"
rating: 1500
weight: 224
solve_time_s: 62
verified: true
draft: false
---

[CF 224B - Array](https://codeforces.com/problemset/problem/224/B)

**Rating:** 1500  
**Tags:** bitmasks, implementation, two pointers  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and a number _k_. The task is to find a contiguous subarray, or segment, such that it contains exactly _k_ distinct integers. Among all segments that satisfy this condition, we are asked to find one that is **minimal by inclusion**, meaning we cannot remove elements from the start or end of the segment without violating the requirement of having exactly _k_ distinct integers. If no such segment exists, we should return `-1 -1`.

The array can have up to 10^5 elements, and each element value can also be as large as 10^5. Because _n_ is 10^5 and the time limit is 2 seconds, any solution that checks all possible subarrays explicitly would take O(n^2) time, which is too slow. This forces us to consider linear or near-linear approaches. Edge cases include arrays with all elements identical, arrays where _k_ is larger than the number of distinct elements, and arrays where the minimal segment occurs at the boundaries.

For example, if the array is `[1, 2, 2, 3]` and _k_ = 2, the segment `[1, 2]` is valid and minimal because `[1, 2]` contains exactly two distinct numbers, and any shorter subsegment would have fewer than 2 distinct numbers. If _k_ = 4, the output should be `-1 -1` because the array contains only 3 distinct numbers.

## Approaches

The brute-force approach would consider every possible segment `[l, r]` in the array, count distinct elements in that segment, and check if it equals _k_. Counting distinct elements can be done with a set. This approach is correct in principle, but checking all O(n^2) segments and computing the set of distinct elements in each could take up to O(n^3) in the worst case if we rebuild the set each time. Even if we use a running set, the total work remains O(n^2) for all segments, which is too slow for n = 10^5.

The key observation is that we can maintain a **sliding window** that grows or shrinks while keeping track of the count of distinct elements. If we use a frequency dictionary to track how many times each number occurs in the current window, we can efficiently add elements to the right and remove elements from the left, updating the count of distinct numbers in O(1) per operation. This allows us to find a valid segment in **O(n)** time, because each element is added and removed at most once.

The insight that makes the sliding window possible is that the problem of counting distinct elements over subarrays has a **monotonic property**: expanding the window to the right can only increase the number of distinct elements, and shrinking it from the left can only decrease the number of distinct elements. This property guarantees that we can move two pointers without missing any minimal-by-inclusion segment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Sliding Window / Two Pointers | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize two pointers `l` and `r` at 0, representing the current segment `[l, r)`. Initialize a dictionary `count` to track the frequency of each number in the current segment, and a variable `distinct` to track the number of distinct elements.
2. Move the right pointer `r` forward in a loop until the number of distinct elements in `[l, r]` reaches or exceeds _k_. For each element `a[r]`, increment its frequency in `count`. If this element appears for the first time, increment `distinct`.
3. Once `distinct` equals _k_, check if this segment `[l, r]` is minimal by inclusion. While the leftmost element `a[l]` has frequency greater than 1, decrement its frequency and move `l` to the right. This ensures no unnecessary elements remain at the start of the segment.
4. If `distinct` equals *k` after shrinking, record this segment as a valid answer. We can return immediately because any further valid segment found later would not be smaller in inclusion; we only need **one** minimal-by-inclusion segment.
5. If the loop ends and `distinct` never reaches _k_, output `-1 -1`.

### Why it works

The invariant is that the sliding window `[l, r)` always contains at most _k_ distinct numbers. Moving the right pointer expands the window, potentially increasing `distinct`. Shrinking from the left ensures minimal inclusion. Every element enters and exits the window at most once, guaranteeing O(n) complexity, and the frequency dictionary ensures we maintain an accurate distinct count efficiently.

## Python Solution

```python
import sys
input = sys.stdin.readline

def find_segment(n, k, a):
    count = {}
    distinct = 0
    l = 0
    for r in range(n):
        if a[r] not in count:
            count[a[r]] = 0
        count[a[r]] += 1
        if count[a[r]] == 1:
            distinct += 1
        
        while distinct > k:
            count[a[l]] -= 1
            if count[a[l]] == 0:
                distinct -= 1
            l += 1
        
        if distinct == k:
            # shrink from left to make it minimal by inclusion
            while count[a[l]] > 1:
                count[a[l]] -= 1
                l += 1
            return l + 1, r + 1  # converting to 1-based index
    return -1, -1

def main():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    l, r = find_segment(n, k, a)
    print(l, r)

if __name__ == "__main__":
    main()
```

The code maintains a frequency dictionary `count` to track elements in the current window. Each addition or removal updates the distinct count. Shrinking the left pointer ensures the segment is minimal by inclusion. The one subtle point is converting indices to 1-based for output, which is why `l + 1` and `r + 1` are returned.

## Worked Examples

### Sample 1

Input: `[1, 2, 2, 3]`, k = 2

| l | r | distinct | count | action |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | {1:1} | add 1 |
| 0 | 1 | 2 | {1:1,2:1} | add 2, distinct == k |
| 0 | 1 | 2 | {1:1,2:1} | shrink left? 1 count=1 |
| 0 | 1 | 2 | {1:1,2:1} | minimal segment found |

Output: `1 2`

This trace confirms that the algorithm correctly finds the minimal-by-inclusion segment starting at index 1 and ending at index 2.

### Sample 2

Input: `[1, 1, 1, 1]`, k = 2

| l | r | distinct | count | action |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | {1:1} | add 1 |
| 0 | 1 | 1 | {1:2} | add 1 |
| 0 | 2 | 1 | {1:3} | add 1 |
| 0 | 3 | 1 | {1:4} | add 1 |

distinct never reaches k. Output: `-1 -1`.

This demonstrates handling the case where there are fewer distinct elements than k.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is added and removed at most once from the window, total O(n) operations |
| Space | O(n) | The count dictionary can contain up to n distinct elements in the worst case |

The solution comfortably fits within the 2-second limit and 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    
    def find_segment(n, k, a):
        count = {}
        distinct = 0
        l = 0
        for r in range(n):
            if a[r] not in count:
                count[a[r]] = 0
            count[a[r]] += 1
            if count[a[r]] == 1:
                distinct += 1
            while distinct > k:
                count[a[l]] -= 1
                if count[a[l]] == 0:
                    distinct -= 1
                l += 1
            if distinct == k:
                while count[a[l]] > 1:
                    count[a[l]] -= 1
                    l += 1
                return f"{l+1} {r+1}"
        return "-1 -1"
    
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    return find_segment(n, k, a)

# provided samples
assert run("4 2\n
```
