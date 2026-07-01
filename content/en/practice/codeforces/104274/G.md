---
title: "CF 104274G - \u0420\u0443\u0434\u043e\u043b\u044c\u0444 \u0438 \u0444\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u0431\u0443\u043a\u0435\u0442\u0430"
description: "We are given a row of flowers, each flower having a type represented by an integer. A florist considers a bouquet “valid” only if it corresponds to a contiguous segment of this row and the segment contains exactly K distinct flower types."
date: "2026-07-01T21:19:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104274
codeforces_index: "G"
codeforces_contest_name: "2023 VIII \u0418\u043d\u0442\u0435\u043b\u043b\u0435\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u041f\u0424\u041e"
rating: 0
weight: 104274
solve_time_s: 66
verified: true
draft: false
---

[CF 104274G - \u0420\u0443\u0434\u043e\u043b\u044c\u0444 \u0438 \u0444\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u0431\u0443\u043a\u0435\u0442\u0430](https://codeforces.com/problemset/problem/104274/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of flowers, each flower having a type represented by an integer. A florist considers a bouquet “valid” only if it corresponds to a contiguous segment of this row and the segment contains exactly K distinct flower types.

The task is to count how many contiguous subarrays have precisely K distinct values.

The input size goes up to 300,000 elements. Any solution that tries to examine all subarrays directly would require roughly N squared checks in the worst case, which is on the order of 10^10 operations and is not feasible within typical time limits. This immediately rules out any approach that recomputes distinct counts independently for every interval.

A subtle point in this problem is that “exactly K distinct” is much harder than “at most K distinct.” Counting subarrays with at most K distinct values behaves nicely under sliding window techniques, while exact K requires a reduction trick.

A typical failure case comes from trying to expand both ends independently without maintaining a consistent window structure. For example, if all elements are distinct and K = 2, a naive expansion might double count or miss valid segments depending on how duplicates are handled. The issue is not correctness of individual checks but inconsistent accounting of overlapping subarrays.

## Approaches

The brute-force idea is straightforward. We iterate over every left endpoint, then extend the right endpoint while tracking a frequency map of elements inside the current segment. For each extension, we count how many distinct values exist and increment the answer if it equals K. This works logically because it enumerates all possible subarrays exactly once.

The problem appears when we analyze complexity. Maintaining a frequency map is O(1) amortized per insertion, but there are O(N^2) subarrays, so the total work becomes O(N^2), which is far too slow for N up to 3 × 10^5.

The key insight is to convert the problem from “exactly K” into a difference of two “at most K” counts. If we can efficiently count subarrays with at most K distinct values, then the number of subarrays with exactly K distinct values is the difference between those with at most K and those with at most K − 1. This works because every subarray with at most K contributes to the total, and subtracting those with at most K − 1 removes all cases with fewer than K distinct values, leaving exactly K.

The “at most K distinct” problem is well-suited for a sliding window. We maintain a window [l, r] and ensure the number of distinct elements does not exceed K by moving the left pointer whenever necessary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N^2) | O(N) | Too slow |
| Optimal | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

We reduce the problem to computing atMost(K) − atMost(K − 1).

### Steps

1. Define a function atMost(K) that counts subarrays containing at most K distinct values. We will compute it using a sliding window.
2. Maintain a frequency map of elements inside the current window and a counter distinct that tracks how many values currently have nonzero frequency.
3. Initialize two pointers, l and r at 0, and an answer variable ans = 0.
4. Expand r from left to right over the array. For each new element A[r], increase its frequency. If this element appears for the first time in the window, increment distinct.
5. If distinct becomes greater than K, shrink the window from the left by moving l forward and decreasing frequencies until distinct is again at most K. When a frequency becomes zero, decrement distinct.
6. Once the window satisfies the constraint, all subarrays ending at r and starting anywhere from l to r are valid. Add (r − l + 1) to ans.
7. Repeat steps 4 to 6 until r reaches the end.
8. The final answer is atMost(K) − atMost(K − 1).

### Why it works

At every position r, the algorithm maintains the smallest left boundary l such that the window [l, r] contains at most K distinct values. Any subarray ending at r that starts earlier than l would introduce at least K + 1 distinct values, because extending left only adds elements and cannot reduce distinct count.

This creates a monotonic structure: for each r, all valid starts form a continuous segment. Counting them as r − l + 1 ensures each valid subarray is counted exactly once, and no invalid subarray is included. The subtraction step then isolates exactly K distinct values without overlap issues.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict

def at_most(k, a):
    if k <= 0:
        return 0
    freq = defaultdict(int)
    l = 0
    distinct = 0
    res = 0

    for r in range(len(a)):
        if freq[a[r]] == 0:
            distinct += 1
        freq[a[r]] += 1

        while distinct > k:
            freq[a[l]] -= 1
            if freq[a[l]] == 0:
                distinct -= 1
            l += 1

        res += r - l + 1

    return res

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    print(at_most(k, a) - at_most(k - 1, a))

if __name__ == "__main__":
    solve()
```

The implementation revolves around the helper function at_most. The frequency dictionary tracks element counts inside the current window, while distinct ensures we know when the constraint is violated. The while loop is the critical part that restores validity whenever the window grows too diverse.

The subtraction in solve directly implements the transformation from exact K to at most K counts. The edge case k = 0 is handled by returning zero early, since no non-empty subarray can have zero distinct elements.

## Worked Examples

### Sample 1

Input:

```
8 2
1 2 1 2 1 3 1 2
```

We compute atMost(2) and atMost(1).

For atMost(2), the window expands smoothly except when the third distinct value appears. The contributions accumulate as valid ranges per right endpoint.

| r | A[r] | l | distinct | window | added |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | [1] | 1 |
| 1 | 2 | 0 | 2 | [1,2] | 2 |
| 2 | 1 | 0 | 2 | [1,2,1] | 3 |
| 3 | 2 | 0 | 2 | [1,2,1,2] | 4 |
| 4 | 1 | 0 | 2 | [1,2,1,2,1] | 5 |
| 5 | 3 | 1 | 2 | [2,1,3] | 3 |
| 6 | 1 | 1 | 2 | [2,1,3,1] | 4 |
| 7 | 2 | 1 | 2 | [2,1,3,1,2] | 5 |

This yields atMost(2) = 27.

For atMost(1), only uniform segments contribute. The final result of subtraction gives 14.

This trace shows how the left pointer jumps when the third distinct element appears, compressing the window while preserving validity.

### Sample 2

Input:

```
8 3
1 2 1 2 1 3 1 2
```

Here the array never exceeds 3 distinct values in most prefixes, so atMost(3) behaves like full accumulation.

The subtraction removes all subarrays with 0, 1, or 2 distinct values, leaving exactly those with 3 distinct values.

The equality of outputs in both samples confirms that the structure of distinct-value transitions, not raw frequency of specific numbers, governs the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each pointer l and r moves at most N times total in each atMost call |
| Space | O(N) | Frequency map stores counts of active elements in window |

The solution runs two linear passes over the array, so the total complexity remains linear in N, which fits comfortably within limits for N up to 3 × 10^5.

## Test Cases

```python
import sys, io
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def at_most(k, a):
        if k <= 0:
            return 0
        freq = defaultdict(int)
        l = 0
        distinct = 0
        res = 0
        for r in range(len(a)):
            if freq[a[r]] == 0:
                distinct += 1
            freq[a[r]] += 1
            while distinct > k:
                freq[a[l]] -= 1
                if freq[a[l]] == 0:
                    distinct -= 1
                l += 1
            res += r - l + 1
        return res

    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    return str(at_most(k, a) - at_most(k - 1, a))

# provided samples
assert run("8 2\n1 2 1 2 1 3 1 2\n") == "14"
assert run("8 3\n1 2 1 2 1 3 1 2\n") == "14"

# minimum size
assert run("1 1\n5\n") == "1"

# impossible case
assert run("5 2\n1 1 1 1 1\n") == "0"

# all distinct
assert run("5 3\n1 2 3 4 5\n") == "3"

# boundary
assert run("6 2\n1 2 3 1 2 3\n") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | minimal valid window |
| all equal, k=2 | 0 | no way to reach k distinct |
| all distinct, k=3 | checks sliding behavior | multiple expansions and contractions |
| alternating pattern | verifies transitions | window stability |

## Edge Cases

One edge case is when K equals 1. In this case, every subarray consisting of identical elements is valid. The atMost transformation still works because atMost(1) counts all uniform segments, and atMost(0) correctly returns zero since no subarray can have zero distinct values.

Another edge case occurs when K is larger than the number of distinct values in the array. Here atMost(K) counts all subarrays, while atMost(K − 1) already equals atMost(K), producing zero. The sliding window never triggers a full reset because the distinct counter never exceeds K, so the entire array is treated as a single valid region whenever possible.

A final subtle case is when frequent alternations cause repeated shrinking of the left pointer. Even in patterns like 1,2,1,2,1,2, the window oscillates but each index is still processed at most once per pointer movement, preserving linear complexity while maintaining correct counting of overlapping valid segments.
