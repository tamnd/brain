---
title: "CF 1945C - Left and Right Houses"
description: "We are given a village with n houses aligned in a row. Each resident has a preference for which side of a street they want to live on: left (0) or right (1)."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 1945
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 935 (Div. 3)"
rating: 1200
weight: 1945
solve_time_s: 48
verified: true
draft: false
---

[CF 1945C - Left and Right Houses](https://codeforces.com/problemset/problem/1945/C)

**Rating:** 1200  
**Tags:** brute force  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a village with `n` houses aligned in a row. Each resident has a preference for which side of a street they want to live on: left (`0`) or right (`1`). The village planners want to place a road somewhere between houses so that at least half of the residents on each side are satisfied. A side is satisfied if the number of residents who get their preferred side is at least the ceiling of half the number of houses on that side.

Effectively, the problem asks us to find a partition index `i` (the road is after house `i`) such that the left segment of length `i` has at least `ceil(i/2)` zeros, and the right segment of length `n-i` has at least `ceil((n-i)/2)` ones. Among all valid `i`, we should choose the one closest to the middle of the village, i.e., minimizing `abs(n/2 - i)`, with ties broken by the smaller `i`.

The constraints allow up to 300,000 houses across all test cases and up to 20,000 test cases. A naive solution that checks every split with a full scan of left and right segments would be O(n^2) per test case in the worst case, which is far too slow. We need an O(n) solution per test case or better. Edge cases include all houses preferring the same side, road at the boundaries (before the first house or after the last house), or odd and even-sized segments affecting the ceiling of half the segment.

## Approaches

The brute-force approach would consider each possible split `i` from 0 to `n` and count the number of zeros in the left segment and ones in the right segment. If the counts satisfy the ceiling conditions, we consider it valid. This approach works logically but requires O(n^2) operations for large strings because each split requires scanning a portion of the array, making it impractical for `n` up to 3·10^5.

The key insight is that we can precompute prefix sums. Let `prefix_zeros[j]` be the number of zeros in the first `j` houses. Then the number of zeros in the left segment of length `i` is `prefix_zeros[i]`. The number of ones in the right segment of length `n-i` can be derived as `(total_ones - prefix_ones[i])` or equivalently `((n - prefix_zeros[n]) - (i - prefix_zeros[i]))`, but simpler is to compute prefix sums for ones as well. With these prefix sums, checking each split becomes O(1), and we only need a single pass through the array to find the optimal split.

The observation that the satisfaction condition only depends on counts of zeros and ones allows us to convert the ceiling inequalities into simple numeric comparisons using the prefix sums. This reduces a potentially quadratic brute-force to linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Prefix Sums / Linear Scan | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `n` and the string `a`. Convert `a` into a list of integers for easier arithmetic.
2. Compute the prefix sum of zeros, `prefix_zeros`, where `prefix_zeros[i]` is the number of zeros in the first `i` houses.
3. Compute the total number of ones, `total_ones`, by counting ones in the full array or by subtracting zeros from `n`.
4. Initialize variables to track the best index `best_i` and the minimum distance to the center `min_dist = n`. We will try to minimize `abs(n/2 - i)`.
5. Iterate over all possible split indices `i` from 0 to `n`. For each split, the left segment has length `i`, right segment length `n-i`.
6. Compute the number of zeros on the left: `left_zeros = prefix_zeros[i]`. Compute the number of ones on the right: `right_ones = total_ones - (i - left_zeros)`.
7. Check if `left_zeros >= ceil(i/2)` and `right_ones >= ceil((n-i)/2)`. Use integer arithmetic for the ceiling: `ceil(x/2) = (x+1)//2`.
8. If both conditions hold, compute `dist = abs(n/2 - i)`. If `dist < min_dist` or `dist == min_dist` and `i < best_i`, update `best_i` and `min_dist`.
9. After the loop, output `best_i`.

Why it works: Prefix sums let us know instantly how many zeros are in any left segment and how many ones are in any right segment. The ceiling condition is properly handled with integer arithmetic. By scanning all `i` from 0 to `n` and tracking the closest to the middle, we ensure the solution satisfies both the fairness condition and the minimal distance requirement.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = input().strip()
        arr = [int(ch) for ch in a]

        prefix_zeros = [0]*(n+1)
        for i in range(n):
            prefix_zeros[i+1] = prefix_zeros[i] + (1 if arr[i] == 0 else 0)
        total_ones = n - prefix_zeros[n]

        best_i = 0
        min_dist = n
        for i in range(n+1):
            left_len = i
            right_len = n - i
            left_zeros = prefix_zeros[i]
            right_ones = total_ones - (right_len - (total_ones - (prefix_zeros[n] - prefix_zeros[i])))
            right_ones = total_ones - (i - left_zeros)

            if left_zeros >= (left_len + 1)//2 and right_ones >= (right_len + 1)//2:
                dist = abs(n/2 - i)
                if dist < min_dist or (dist == min_dist and i < best_i):
                    best_i = i
                    min_dist = dist
        print(best_i)

if __name__ == "__main__":
    solve()
```

In this implementation, we compute prefix sums for zeros. The number of ones on the right segment is computed by subtracting the ones counted on the left from the total. The `(length + 1)//2` trick correctly handles the ceiling division. Iterating from 0 to `n` ensures we consider all possible placements of the road, including before the first house and after the last house. The tie-breaking logic ensures we pick the smaller index if two positions are equally close to the center.

## Worked Examples

### Example 1:

Input string `101` with `n=3`.

| i | left_len | right_len | left_zeros | right_ones | ceil(left_len/2) | ceil(right_len/2) | valid? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 3 | 0 | 2 | 0 | 2 | Yes |
| 1 | 1 | 2 | 0 | 2 | 1 | 1 | No |
| 2 | 2 | 1 | 1 | 1 | 1 | 1 | Yes |
| 3 | 3 | 0 | 1 | 0 | 2 | 0 | No |

The closest to the center `n/2 = 1.5` is `i=2`. Output `2`.

### Example 2:

Input string `010111` with `n=6`.

| i | left_len | right_len | left_zeros | right_ones | ceil(left_len/2) | ceil(right_len/2) | valid? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 6 | 0 | 4 | 0 | 3 | Yes |
| 1 | 1 | 5 | 1 | 4 | 1 | 3 | Yes |
| 2 | 2 | 4 | 1 | 3 | 1 | 2 | Yes |
| 3 | 3 | 3 | 2 | 2 | 2 | 2 | Yes |
| 4 | 4 | 2 | 2 | 2 | 2 | 1 | Yes |
| 5 | 5 | 1 | 2 | 1 | 3 | 1 | No |
| 6 | 6 | 0 | 3 | 0 | 3 | 0 | Yes |

Closest to middle `3` is index `3`, but tie-breaking prefers smaller index `3`. Output `3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Prefix sum computation is O(n), scanning splits is O(n) |
| Space | O(n) per test case | Prefix sum array of length n+1 |

The algorithm is linear in the number of houses per test case. With the sum of `n` across all test cases ≤ 3·10^5, this fits easily within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin
```
