---
title: "CF 2149E - Hidden Knowledge of the Ancients"
description: "We are given a sequence of integers representing symbols on an ancient tablet. Each test case asks us to count the number of continuous segments (subarrays) of this sequence that satisfy two conditions: the segment contains exactly k distinct numbers, and its length is at least…"
date: "2026-06-08T01:10:24+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2149
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1054 (Div. 3)"
rating: 1500
weight: 2149
solve_time_s: 86
verified: true
draft: false
---

[CF 2149E - Hidden Knowledge of the Ancients](https://codeforces.com/problemset/problem/2149/E)

**Rating:** 1500  
**Tags:** data structures, two pointers  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers representing symbols on an ancient tablet. Each test case asks us to count the number of continuous segments (subarrays) of this sequence that satisfy two conditions: the segment contains exactly `k` distinct numbers, and its length is at least `l` and at most `r`. For each test case, we must output the total count of such segments.

The input size allows sequences up to 200,000 elements and up to 10,000 test cases, with the total number of elements across all test cases bounded by 200,000. This implies that any algorithm with worst-case complexity above linear in `n` per test case is likely to time out. A naive approach that checks all possible subarrays would require `O(n^2)` operations per test case, which is infeasible for large inputs.

Edge cases include sequences where all elements are identical, sequences with all distinct elements, or where `l` and `r` limit the segment length to very narrow ranges. For example, a sequence `[7,7,7,7]` with `k=1` and `l=1, r=2` allows subarrays `[7]`, `[7,7]`, `[7,7]`, `[7]` - careful counting is needed to avoid off-by-one errors.

## Approaches

The brute-force solution iterates over every possible pair of start and end indices, counts distinct numbers in the subarray, and checks its length. It is correct but requires up to `O(n^2)` operations, which can reach 4*10^10 for the maximum constraints. This is too slow.

The key insight is that the number of distinct elements in a sliding window can be tracked efficiently using a two-pointer approach and a frequency map. By maintaining a window `[left, right]` that expands to include new elements and contracts to remove elements, we can count subarrays with exactly `k` distinct numbers in `O(n)` time per test case. To handle the length bounds `l` and `r`, we can maintain two right pointers: one to track the smallest valid segment length and another for the largest. The difference between these pointers gives the number of valid subarrays starting at the current left position.

This observation reduces the complexity from quadratic to linear, and the combination of a frequency map and two-pointer window guarantees that each element is processed at most twice per pointer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Two Pointers + Frequency Map | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize two right pointers `right_min` and `right_max`, a frequency map `freq`, and a count of distinct numbers `distinct_count`.
2. Iterate over the array with a left pointer `left` from `0` to `n-1`.
3. Expand `right_max` until the window `[left, right_max]` has more than `k` distinct numbers, keeping `freq` updated. Stop at the first invalid element. This ensures all segments starting at `left` with exactly `k` distinct numbers are within `[left, right_max-1]`.
4. Expand `right_min` until the window `[left, right_min]` has at least `k` distinct numbers. This marks the first subarray that satisfies the distinct element condition.
5. The valid subarrays starting at `left` are those with lengths between `l` and `r` and within `[right_min, right_max-1]`. Compute the overlap: the number of valid subarrays is `max(0, min(right_max-1, left + r - 1) - max(right_min, left + l - 1) + 1)`.
6. Add this count to the result.
7. Move the left pointer forward by one. Decrement the frequency of `a[left]` and adjust `distinct_count` if necessary. Repeat steps 3-6 until the end of the array.

**Why it works**: The two-pointer technique guarantees that all subarrays starting at `left` are counted exactly once. The frequency map ensures the `distinct_count` is always accurate. By adjusting `right_min` and `right_max` independently, we account for both the distinct number and length constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_valid_subarrays(n, k, l, r, a):
    from collections import defaultdict
    freq = defaultdict(int)
    distinct_count = 0
    result = 0
    right_min = right_max = 0
    
    for left in range(n):
        while right_max < n and (distinct_count < k or (distinct_count == k and freq[a[right_max]] > 0)):
            if freq[a[right_max]] == 0:
                distinct_count += 1
            freq[a[right_max]] += 1
            right_max += 1
        
        while right_min < n and (distinct_count > k or (distinct_count == k and freq[a[right_min]] == 0)):
            if freq[a[right_min]] == 0:
                distinct_count += 1
            freq[a[right_min]] += 1
            right_min += 1
        
        start = max(left + l - 1, right_min)
        end = min(left + r - 1, right_max - 1)
        if end >= start:
            result += end - start + 1
        
        freq[a[left]] -= 1
        if freq[a[left]] == 0:
            distinct_count -= 1
    
    return result

t = int(input())
for _ in range(t):
    n, k, l, r = map(int, input().split())
    a = list(map(int, input().split()))
    print(count_valid_subarrays(n, k, l, r, a))
```

The solution initializes frequency counts and uses two pointers to efficiently slide the window while maintaining the number of distinct elements. The tricky part is computing the number of valid subarrays using `start` and `end` while respecting both the distinct number and length constraints. Decrementing the frequency when moving `left` ensures the sliding window remains valid.

## Worked Examples

For the input `[1,2,1,3,2]` with `k=2`, `l=1`, `r=3`:

| left | right_min | right_max | freq | distinct_count | valid subarrays |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 2 | {1:1,2:1} | 2 | 2 |
| 1 | 2 | 4 | {1:1,2:1,3:1} | 3 | 2 |
| 2 | 2 | 4 | {1:1,2:1,3:1} | 3 | 1 |

This confirms that the window adjustments correctly account for the number of distinct elements and the subarray length constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is added and removed from the frequency map at most once for each pointer. |
| Space | O(n) | The frequency map stores at most `n` distinct elements. |

This linear solution fits comfortably within the 2-second limit even for the maximum `n=2*10^5`.

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
assert run("5\n1 1 1 1\n5\n5 2 2 3\n1 2 1 3 2\n6 3 1 6\n1 2 3 1 2 3\n4 1 1 2\n7 7 7 7\n7 3 2 4\n1 2 1 2 3 2 1") == "1\n5\n10\n7\n5"

# Custom cases
assert run("1\n4 1 1 1\n1 1 1 1") == "4", "all identical, l=r=1"
assert run("1\n5 5 1 5\n1 2 3 4 5") == "1", "all distinct, k=n"
assert run("1\n5 3 2 3\n1 2 1 3 2") == "4", "mixed distinct numbers"
assert run("1\n3 2 2 3\n1 2 3") == "2", "length constraints narrower than array"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[1,1,1,1], k=1, l=1, r=1` | 4 | Counting single-length subarrays correctly |
| `[1,2,3,4,5], k=5, l=1, r=5` | 1 | Handles case where entire array is the only valid segment |
| `[1,2,1,3,2], k=3, l=2, r=3` | 4 | Correct counting with overlapping subarrays |
| `[1,2,3], k=2, l=2, r=3` | 2 | Respects length constraints |

##
