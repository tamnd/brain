---
title: "CF 104930E - Up Down Matching"
description: "We are given several independent test cases. In each test case, a line of people stands in a fixed order, where each person is either from Uptown or Downside."
date: "2026-06-28T07:42:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104930
codeforces_index: "E"
codeforces_contest_name: "UTPC Contest 01-26-24 Div. 2 (Beginner)"
rating: 0
weight: 104930
solve_time_s: 64
verified: false
draft: false
---

[CF 104930E - Up Down Matching](https://codeforces.com/problemset/problem/104930/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent test cases. In each test case, a line of people stands in a fixed order, where each person is either from Uptown or Downside. We are allowed to choose one contiguous segment of this line, and we want that segment to be “balanced”, meaning it contains exactly the same number of Uptownites and Downsiders. Among all such balanced segments, we need the maximum possible length.

The key task per test case is therefore not to find any balanced segment, but to find the longest substring where the counts of `U` and `D` are equal.

The constraints are tight enough that any approach that checks all substrings directly is infeasible. With total length up to 200,000 across test cases, a quadratic scan per test case would lead to on the order of 10^10 operations in the worst case, which is far beyond a 2 second limit in Python.

A few edge cases matter structurally:

A string consisting entirely of one character, for example `UUUUU`, has no valid segment of positive length, so the answer must be 0. A naive approach that assumes at least one valid pair exists would incorrectly return at least 2.

A full alternating string like `UDUDUD` should return the full length, since every prefix can potentially be balanced at some point, but only after tracking cumulative balance correctly.

A case like `UUDDUD` can have multiple valid segments of different lengths, and we must ensure we are not just taking the first balanced prefix.

## Approaches

The brute-force idea is straightforward: try every possible segment `[l, r]`, count how many `U` and `D` appear, and check whether they match. If they do, update the answer with `r - l + 1`. This is correct because it explicitly evaluates all candidates.

The issue is performance. For each starting index `l`, we scan all `r > l` and recompute counts, or even if we maintain running counts, we still examine O(n^2) segments per test case. With up to 2·10^5 total length, this becomes too slow.

The key observation is that we do not actually care about the raw counts of `U` and `D`, but only their difference. If we map `U` to +1 and `D` to -1, then a segment is balanced exactly when its sum is zero. This converts the problem into finding the longest subarray with sum zero.

This is a classic prefix sum structure. If we define `prefix[i]` as the sum up to index `i`, then a segment `[l, r]` has sum zero if and only if `prefix[r] == prefix[l-1]`. So the problem becomes finding two equal prefix values with maximum distance between their indices.

We can solve this by storing the earliest position where each prefix sum value appears. When we see the same prefix sum again, we compute the distance from its first occurrence and update the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Prefix sum + hashmap | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Convert the string into a running balance by treating `U` as +1 and `D` as -1. We maintain a variable `pref` starting at 0. This transforms the problem into detecting equal prefix sums.
2. Initialize a dictionary `first_pos` mapping prefix sum values to the earliest index where they appear. We set `first_pos[0] = 0` before processing, because a zero sum before starting allows subarrays starting at index 1.
3. Iterate through the string from left to right, updating `pref` at each position. After processing position `i`, `pref` represents the balance of the prefix ending at `i`.
4. If `pref` has been seen before, compute the segment length `i - first_pos[pref]` and update the answer if this is larger. This works because equal prefix sums imply a zero-sum segment between their indices.
5. If `pref` has not been seen before, store `first_pos[pref] = i`. We store only the first occurrence to maximize later distances, since a later occurrence would only shorten possible segments.
6. After processing the full string, the answer is the maximum balanced segment length found.

### Why it works

The prefix sum transformation encodes the entire problem into equality comparisons. Every balanced segment corresponds exactly to two indices with the same prefix sum value. By tracking the earliest occurrence of each prefix sum, we ensure that whenever we revisit that sum, we are forming the longest possible segment ending at the current index with zero net balance. This guarantees that every valid segment is considered exactly once, and the longest among them is captured.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input().strip())
        s = input().strip()

        first_pos = {0: 0}
        pref = 0
        ans = 0

        for i, ch in enumerate(s, start=1):
            if ch == 'U':
                pref += 1
            else:
                pref -= 1

            if pref in first_pos:
                ans = max(ans, i - first_pos[pref])
            else:
                first_pos[pref] = i

        print(ans)

if __name__ == "__main__":
    solve()
```

The core implementation choice is the 1-based indexing in the loop. This aligns naturally with the prefix definition where position 0 represents an empty prefix, allowing clean subtraction `i - first_pos[pref]` without off-by-one adjustments.

We also avoid updating `first_pos` after the first occurrence, which is essential. Overwriting it would destroy the possibility of forming maximal-length segments.

## Worked Examples

### Example 1

Input:

```
UDUD
```

We track prefix sums step by step:

| i | char | pref | first_pos | ans |
| --- | --- | --- | --- | --- |
| 0 | - | 0 | {0:0} | 0 |
| 1 | U | 1 | {0:0,1:1} | 0 |
| 2 | D | 0 | {0:0,1:1} | 2 |
| 3 | U | 1 | {0:0,1:1} | 2 |
| 4 | D | 0 | {0:0,1:1} | 4 |

The prefix sum returns to 0 at positions 2 and 4, giving segments `[1,2]` and `[1,4]`, with the full segment being valid.

This demonstrates how repeated prefix sums naturally capture multiple valid balanced segments, and the algorithm automatically keeps the longest.

### Example 2

Input:

```
UUDDUD
```

| i | char | pref | first_pos | ans |
| --- | --- | --- | --- | --- |
| 0 | - | 0 | {0:0} | 0 |
| 1 | U | 1 | {0:0,1:1} | 0 |
| 2 | U | 2 | {0:0,1:1,2:2} | 0 |
| 3 | D | 1 | {0:0,1:1,2:2} | 2 |
| 4 | D | 0 | {0:0,1:1,2:2} | 4 |
| 5 | U | 1 | {0:0,1:1,2:2} | 4 |
| 6 | D | 0 | {0:0,1:1,2:2} | 6 |

This shows multiple overlapping balanced segments, where only tracking first occurrences ensures we still capture the global maximum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once with O(1) dictionary operations |
| Space | O(n) | Prefix sum map stores at most n distinct values |

The total work across all test cases is linear in the total input size, which fits comfortably within the constraints of 2·10^5 characters.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        s = input().strip()

        first_pos = {0: 0}
        pref = 0
        ans = 0

        for i, ch in enumerate(s, start=1):
            pref += 1 if ch == 'U' else -1
            if pref in first_pos:
                ans = max(ans, i - first_pos[pref])
            else:
                first_pos[pref] = i

        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run("4\n4\nUDUD\n7\nUUUDDDD\n10\nDDUDDUDUUD\n2\nDD\n") == "4\n6\n8\n0"

# custom cases
assert run("1\n1\nU\n") == "0", "single element"
assert run("1\n6\nUUUUUU\n") == "0", "all same"
assert run("1\n6\nUDUDUD\n") == "6", "fully alternating"
assert run("1\n8\nUUDDUDUD\n") == "8", "multiple valid segments"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `U` | `0` | minimum length edge case |
| `UUUUUU` | `0` | no valid balanced segment |
| `UDUDUD` | `6` | full-length alternating balance |
| `UUDDUDUD` | `8` | overlapping valid subarrays |

## Edge Cases

A string with no `U` or no `D` is the most important degenerate case. For input `DDDD`, prefix sums only decrease, never repeat, so the dictionary never produces a match and the answer remains 0. The algorithm correctly avoids false positives because equality of prefix sums never occurs after the initial 0.

A case like `UDUDUD` repeatedly returns to previously seen prefix sums. Each return produces a candidate segment ending at the current index, and because only the earliest occurrence is stored, the longest segment ending at each position is always considered.

A case with mixed blocks like `UUDDUD` demonstrates that the optimal segment may start and end in the middle of the string, not necessarily aligned with block boundaries. The prefix sum equality handles this naturally without special casing.
