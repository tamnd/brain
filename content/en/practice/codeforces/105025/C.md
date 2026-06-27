---
title: "CF 105025C - \u0421\u043e\u043b\u043d\u0435\u0447\u043d\u0430\u044f \u043f\u0430\u043d\u0435\u043b\u044c"
description: "We are given a sequence of heights representing consecutive segments of a roof. Each segment has a fixed height, and we want to place a solar panel on a contiguous interval of these segments."
date: "2026-06-28T01:39:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105025
codeforces_index: "C"
codeforces_contest_name: "\u041e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b \u00ab\u041c\u0430\u0448\u0438\u043d\u0430 \u0422\u044c\u044e\u0440\u0438\u043d\u0433\u0430\u00bb \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 105025
solve_time_s: 50
verified: true
draft: false
---

[CF 105025C - \u0421\u043e\u043b\u043d\u0435\u0447\u043d\u0430\u044f \u043f\u0430\u043d\u0435\u043b\u044c](https://codeforces.com/problemset/problem/105025/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of heights representing consecutive segments of a roof. Each segment has a fixed height, and we want to place a solar panel on a contiguous interval of these segments. The only constraint is that within the chosen interval, the heights must be monotonic, either entirely non-decreasing or entirely non-increasing.

The task is to find the longest such contiguous interval and output its endpoints.

The input size can be as large as one million elements. That immediately rules out any approach that inspects all subarrays explicitly. A quadratic scan over all pairs of endpoints would require on the order of 10^12 operations, which is far beyond the time limit. Even cubic or nested scanning approaches are clearly impossible.

A linear or near-linear scan is required, meaning we should expect a solution that processes the array in a single pass while maintaining some local structure of monotonicity.

A subtle edge case arises when the best segment spans long stretches with equal values. For example, an array like 5 5 5 5 5 is valid both as non-decreasing and non-increasing, so the entire array must be returned. Any solution that treats equal elements inconsistently in slope changes risks breaking this case.

Another edge case is when the array is strictly alternating, such as 1 3 2 4 3 5. The longest monotonic segment may then be only length 2, and the solution must correctly reset at every change in direction.

## Approaches

The brute-force idea is straightforward: try every pair of endpoints l and r, check whether the segment is non-decreasing or non-increasing, and track the maximum length. For each segment, verifying monotonicity takes O(n) time, and there are O(n^2) segments, giving O(n^3) overall. Even if we optimize checking using prefix comparisons, we still end up at O(n^2), which is too slow for n up to 10^6.

The key observation is that monotonicity is a local property. Once a direction is established, it continues until it breaks. This means the array can be decomposed into maximal monotone runs, and the answer must be one of these runs or a combination of two runs that share a turning point.

More precisely, if we look at each position as a potential "turning point", we can expand left and right while maintaining either non-decreasing or non-increasing condition. Instead of recomputing from scratch for each l, we can reuse information from neighbors and maintain running segments.

This leads to a linear scan solution where we track two types of monotonic segments dynamically: increasing and decreasing. We extend them as long as possible and reset when the condition breaks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) to O(n^3) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain two running lengths as we traverse the array: the current length of a non-decreasing segment ending at position i, and the current length of a non-increasing segment ending at position i. We also track the best segment seen so far.

1. Initialize both increasing and decreasing lengths to 1 at the first element. At this point, any single element is trivially valid.
2. Iterate through the array from left to right starting at index 1.
3. If the current height is greater than or equal to the previous one, we can extend the non-decreasing segment. Otherwise, we reset it to length 1 because monotonicity is broken.
4. If the current height is less than or equal to the previous one, we can extend the non-increasing segment. Otherwise, we reset it to length 1.
5. After updating both states, compare the current best ending at i with the global best answer. If either monotone direction produces a longer segment, update the stored best endpoints accordingly.
6. Continue until the end of the array, always maintaining correct segment boundaries by remembering where each run started.

The key detail is that we must track not only lengths but also the starting index of each current run, because the answer requires endpoints, not just length.

### Why it works

At every position i, any valid monotonic subarray ending at i must be either part of the maximal non-decreasing run ending at i or the maximal non-increasing run ending at i. These runs are uniquely determined by local comparisons and cannot be extended further without violating monotonicity. Since every valid solution is contained in one of these maximal runs, checking all runs implicitly covers all candidates. The algorithm never misses a candidate because every valid interval is exactly a suffix of one of these maintained monotone segments.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n_and_rest = input().split()
    if not n_and_rest:
        return
    n = int(n_and_rest[0])
    h = list(map(int, input().split()))
    
    if n == 1:
        print(1, 1)
        return

    best_len = 1
    best_l = 1
    best_r = 1

    inc_start = 0
    dec_start = 0
    inc_len = 1
    dec_len = 1

    for i in range(1, n):
        if h[i] >= h[i - 1]:
            inc_len += 1
        else:
            inc_len = 1
            inc_start = i

        if h[i] <= h[i - 1]:
            dec_len += 1
        else:
            dec_len = 1
            dec_start = i

        if inc_len > best_len:
            best_len = inc_len
            best_l = inc_start + 1
            best_r = i + 1

        if dec_len > best_len:
            best_len = dec_len
            best_l = dec_start + 1
            best_r = i + 1

    print(best_l, best_r)

if __name__ == "__main__":
    solve()
```

The implementation keeps two independent sliding windows. The increasing window expands when the next element is not smaller, otherwise it resets and starts at the current index. The decreasing window behaves symmetrically.

The critical implementation detail is that when a reset happens, the start index is set to the current position, not the previous one. This ensures correctness for strict reversals like 1 3 2, where the segment must restart at 3 and 2 respectively.

We also maintain best indices in 1-based form, converting from 0-based indexing only at output time.

## Worked Examples

### Example 1

Input:

```
5
2 9 4 3 5
```

We track both monotone directions.

| i | h[i] | inc_len | inc_start | dec_len | dec_start | best |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 2 | 1 | 0 | 1 | 0 | (1,1) |
| 1 | 9 | 2 | 0 | 1 | 1 | (1,2) |
| 2 | 4 | 1 | 2 | 2 | 1 | (2,3) |
| 3 | 3 | 1 | 3 | 3 | 1 | (2,4) |
| 4 | 5 | 2 | 3 | 1 | 4 | (2,4) |

The decreasing segment from index 2 to 4 is the longest valid one, giving 4 2 in 1-based indexing.

This trace shows how resets correctly restart segments and how a global maximum can come from any direction.

### Example 2

Input:

```
4
1 2 3 4
```

| i | h[i] | inc_len | inc_start | dec_len | dec_start | best |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 0 | 1 | 0 | (1,1) |
| 1 | 2 | 2 | 0 | 1 | 1 | (1,2) |
| 2 | 3 | 3 | 0 | 1 | 2 | (1,3) |
| 3 | 4 | 4 | 0 | 1 | 3 | (1,4) |

The increasing segment covers the whole array.

This confirms that the algorithm correctly handles fully monotone sequences without unnecessary resets.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once with constant work |
| Space | O(1) | Only a few counters and indices are maintained |

The linear scan is sufficient for n up to 10^6 because each iteration performs only a constant number of comparisons and assignments, well within typical time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()  # placeholder if solve prints directly

# Since solve() prints, redefine properly
def run(inp: str) -> str:
    import sys, io
    backup = sys.stdin
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    sys.stdin = backup
    return out.getvalue().strip()

# provided sample
assert run("5\n2 9 4 3 5\n") == "2 4"

# all increasing
assert run("4\n1 2 3 4\n") == "1 4"

# all decreasing
assert run("4\n4 3 2 1\n") == "1 4"

# all equal
assert run("5\n7 7 7 7 7\n") == "1 5"

# single element
assert run("1\n10\n") == "1 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 2 9 4 3 5 | 2 4 | mixed monotone runs |
| 1 2 3 4 | 1 4 | full increasing case |
| 4 4 3 2 1 | 1 4 | full decreasing case |
| 5 7 7 7 7 7 | 1 5 | equal elements handling |
| 1 10 | 1 1 | minimum size |

## Edge Cases

For the constant array case like 7 7 7 7 7, both monotone conditions always hold. The algorithm keeps extending both inc_len and dec_len continuously, never triggering a reset. The best segment is updated at the final index to cover the entire range, producing 1 5 correctly.

For a sharp zigzag such as 1 3 2 4, the increasing segment resets at 2 and 4, while the decreasing segment resets at 3. The longest valid run is 1 3 or 3 4 depending on direction, and the algorithm correctly identifies length 2 segments as optimal.

For strictly monotone decreasing input like 5 4 3 2, the decreasing counter grows at every step without interruption. The increasing counter resets at every step but never affects the final answer, since the decreasing run dominates.
