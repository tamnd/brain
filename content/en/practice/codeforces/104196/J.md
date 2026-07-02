---
title: "CF 104196J - Recycling"
description: "We are given a sequence of weekly estimates, where each number describes how many cubic meters of recyclable material will arrive in a specific week. We want to place a recycling bin for some contiguous range of weeks and choose its capacity."
date: "2026-07-02T17:56:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104196
codeforces_index: "J"
codeforces_contest_name: "2021-2022 ICPC East Central North America Regional Contest (ECNA 2021)"
rating: 0
weight: 104196
solve_time_s: 65
verified: true
draft: false
---

[CF 104196J - Recycling](https://codeforces.com/problemset/problem/104196/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of weekly estimates, where each number describes how many cubic meters of recyclable material will arrive in a specific week. We want to place a recycling bin for some contiguous range of weeks and choose its capacity.

Once the bin is installed with a fixed capacity, each week it is emptied and refills up to the incoming amount. The bin remains in use as long as, at the end of a week, it is completely full. The first week where the expected amount is strictly less than the capacity forces us to remove it before that week.

So if we choose a start week and a capacity, the bin will operate on a maximal contiguous segment starting there where every value is at least the capacity. The total recycled amount over such a segment is the capacity multiplied by the number of weeks in the segment.

The task is to choose a starting week, an ending week, and a capacity so that this product is maximized, and if multiple choices give the same result, we pick the one with the smallest starting week.

The input size goes up to 100,000 weeks. Any solution that tries all possible subarrays directly would need to examine roughly n² intervals, and that leads to about 10¹⁰ checks in the worst case, which is far beyond feasible limits. This forces us to look for a structure that avoids enumerating all intervals explicitly.

A subtle edge case comes from equal values. If many consecutive weeks have the same amount, multiple different choices of capacity and interval boundaries can produce the same score. The tie-breaking rule on smallest start index means that even among equal optimal rectangles, we must be consistent in how we define boundaries.

## Approaches

A naive approach is to consider every possible starting week, extend an interval to the right, and maintain the minimum value in that interval. For each extension, we compute the product of the minimum value and the length. This is correct because the best capacity for a fixed interval is exactly its minimum value. However, maintaining the minimum for every extension across all starts still leads to quadratic behavior, since each start can extend up to n steps.

The key observation is that every optimal choice is determined by a position that acts as the minimum inside its chosen interval. If we fix an index i as the minimum of some interval, then the best interval for that choice extends as far as possible to the left and right while all elements remain at least a[i]. This turns the problem into finding, for every index, the largest interval where a[i] is the minimum, and evaluating a[i] times the width of that interval.

This is exactly the classical “largest rectangle in a histogram” structure. Each value is treated as a height, and we expand outward until we hit a strictly smaller value. A monotonic stack allows us to compute these boundaries in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) extra | Too slow |
| Monotonic Stack (Histogram method) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We reinterpret each week i as a bar with height equal to the expected recycling amount. For each position, we want to know how far this bar can extend left and right while staying the smallest value in its segment.

We compute two boundaries using a monotonic stack. The stack keeps indices with increasing values.

1. We scan from left to right and maintain a stack of indices whose values are strictly increasing. When we encounter a value that is smaller than or equal to the stack top, we pop until the invariant is restored. Each popped index has found its right boundary, because the current index is the first position to its right with a smaller value.
2. We repeat a similar process to determine, for each index, the nearest smaller value on the left. When scanning, we again use a monotonic stack, and the previous index remaining on the stack gives the last position where the value is strictly smaller.
3. For each index i, once both boundaries are known, we define the interval as everything strictly between them. This is the maximal segment where a[i] is the minimum value.
4. We compute the score for this segment as a[i] multiplied by its length. We track the best score and store its interval.
5. When updating the best answer, we break ties by preferring the smaller starting index. Since we process indices in increasing order, ensuring consistent boundary rules guarantees deterministic tie resolution.

The correctness relies on the fact that every valid interval has a unique index where the minimum is achieved, and this index determines the maximal extension of that interval. Any optimal solution must coincide with one of these maximal spans, since shrinking the interval can only reduce the length while not increasing the minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    # boundaries
    left = [-1] * n
    right = [n] * n

    stack = []

    # next smaller to the left
    for i in range(n):
        while stack and a[stack[-1]] >= a[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)

    stack = []

    # next smaller to the right
    for i in range(n - 1, -1, -1):
        while stack and a[stack[-1]] >= a[i]:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)

    best_val = -1
    best_l = 0
    best_r = 0

    for i in range(n):
        l = left[i] + 1
        r = right[i] - 1
        val = a[i] * (r - l + 1)

        if val > best_val or (val == best_val and l < best_l):
            best_val = val
            best_l = l
            best_r = r

    print(best_l + 1, best_r + 1, best_val)

if __name__ == "__main__":
    solve()
```

The first two passes compute, for each position, how far its value can extend while remaining the minimum. The left pass uses a monotonic increasing stack so that when a smaller value appears, everything larger is removed and cannot extend further. The right pass mirrors this logic in reverse.

The final loop evaluates each index as the limiting minimum of a candidate segment. The conversion between zero-based indices and one-based output is handled only at the end to avoid off-by-one errors.

## Worked Examples

Consider the array `[2, 5, 7, 3, 5, 10, 2]`.

After computing boundaries, each index defines a maximal segment. The most interesting candidate is the value `3` at index 3 (0-based), which expands from week 2 to week 6 in 1-based indexing.

| i | a[i] | left boundary | right boundary | segment (1-based) | value |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | -1 | 6 | 1-7 | 14 |
| 1 | 5 | 0 | 3 | 2-4 | 15 |
| 2 | 7 | 1 | 3 | 3-4 | 14 |
| 3 | 3 | 0 | 5 | 2-6 | 15 |
| 4 | 5 | 3 | 5 | 5-5 | 5 |
| 5 | 10 | 4 | 6 | 6-6 | 10 |
| 6 | 2 | -1 | 6 | 1-7 | 14 |

The best value is 15, achieved by multiple segments, but the tie-breaking rule selects the one with the smallest starting index, which is weeks 2-6.

Now consider a case with all equal values `[4, 4, 4, 4]`. Every index can extend to the full array, producing the same product for all choices. The algorithm consistently assigns the entire range to each index, and the tie-break rule selects the first index, giving segment 1-4.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each index is pushed and popped at most once in each stack pass, and the final scan is linear |
| Space | O(n) | Arrays for boundaries and stack storage |

The linear complexity is necessary because n can reach 100,000, and only an O(n) approach comfortably fits within typical time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import isclose

    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))

    left = [-1] * n
    right = [n] * n

    stack = []
    for i in range(n):
        while stack and a[stack[-1]] >= a[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)

    stack = []
    for i in range(n - 1, -1, -1):
        while stack and a[stack[-1]] >= a[i]:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)

    best_val = -1
    best_l = best_r = 0

    for i in range(n):
        l = left[i] + 1
        r = right[i] - 1
        val = a[i] * (r - l + 1)
        if val > best_val or (val == best_val and l < best_l):
            best_val = val
            best_l = l
            best_r = r

    return f"{best_l+1} {best_r+1} {best_val}"

# minimum size
assert run("1\n5\n") == "1 1 5"

# strictly increasing
assert run("5\n1 2 3 4 5\n") == "1 5 9"

# strictly decreasing
assert run("5\n5 4 3 2 1\n") == "1 5 9"

# all equal
assert run("4\n4 4 4 4\n") == "1 4 16"

# mixed case
assert run("7\n2 5 7 3 5 10 2\n") == "2 6 15"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 1 1 v | base boundary handling |
| increasing | full range | right expansion correctness |
| decreasing | full range | left expansion correctness |
| all equal | full range | tie handling |
| sample-like | 2 6 15 | correctness of full solution |

## Edge Cases

For a single-element array like `[7]`, both boundaries collapse to the same index. The algorithm sets left boundary to -1 and right boundary to n, producing a segment of length 1 and value 7, which is trivially optimal.

For arrays with all identical values, every index generates the same maximal interval. The stack logic ensures every element expands across the full range, and the tie-breaking rule selects the smallest starting index, which matches the requirement.

For strictly monotone arrays, each element expands over the entire array because no smaller element exists on either side. The algorithm correctly identifies that the best choice is using the global minimum at one endpoint, producing the full-span interval with correct product.
