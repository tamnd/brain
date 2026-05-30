---
title: "CF 1955D - Inaccurate Subsequence Search"
description: "We are asked to count subsegments of length m in an array a that are “good” relative to another array b of length m. A subsegment is considered good if, after rearranging its elements, at least k of them match elements from b."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1955
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 938 (Div. 3)"
rating: 1400
weight: 1955
solve_time_s: 46
verified: true
draft: false
---

[CF 1955D - Inaccurate Subsequence Search](https://codeforces.com/problemset/problem/1955/D)

**Rating:** 1400  
**Tags:** data structures, two pointers  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count subsegments of length `m` in an array `a` that are “good” relative to another array `b` of length `m`. A subsegment is considered good if, after rearranging its elements, at least `k` of them match elements from `b`. In practice, this means we are checking whether the multiset intersection of the subsegment and `b` contains at least `k` elements.

The input provides multiple test cases, each with arrays `a` and `b`, and integers `n`, `m`, `k`. The total size of all `a` arrays across test cases does not exceed `2 * 10^5`, and similarly for `b`. This bounds the total number of operations we can perform efficiently. Any solution that iterates over every subsegment and compares it to `b` element by element in `O(n * m)` time will be too slow, because in the worst case this could reach `2 * 10^5 * 2 * 10^5 = 4 * 10^10` operations.

Edge cases include subsegments where elements repeat, `k = m` (requiring a full match), `k = 1` (requiring minimal match), and `a` or `b` containing repeated numbers. A naive approach might count distinct elements incorrectly or fail when multiple duplicates are involved. For example, if `a = [1,1,1]` and `b = [1,2,3]` with `k = 2`, the algorithm must not incorrectly count this segment as good since only one `1` in `b` can match the segment.

## Approaches

A brute-force approach would iterate over every subsegment of length `m` in `a`, and for each, compute the multiset intersection with `b`. Counting the matches requires iterating over all elements of the subsegment and comparing with `b`. This works correctly because it directly implements the definition, but it has `O(n * m)` complexity per test case and fails for large `n` and `m`.

The key insight is that we can maintain a sliding window of length `m` over `a` and track how many elements match those in `b` using a frequency map. Initially, we count the occurrences of each number in `b` in a dictionary. Then, as we slide the window across `a`, we maintain another dictionary for counts of elements in the current window that appear in `b`. When an element enters the window, we increment the match count if it is present in `b` and hasn't been fully matched yet. When an element leaves the window, we decrement the match count if it was previously contributing to the intersection. This reduces the complexity to `O(n)` per test case using `O(m)` extra space for frequency tracking.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(m) | Too slow |
| Sliding Window + Frequency Map | O(n) | O(m) | Accepted |

## Algorithm Walkthrough

1. Construct a frequency dictionary for array `b`. Each key is a number, and the value is how many times it appears. This lets us efficiently check if an element in a subsegment can match `b`.
2. Initialize a sliding window over the first `m` elements of `a`. Maintain a count of how many elements in the window match elements in `b` without exceeding their required frequency. For each element entering the window, increment a match counter if the element exists in `b` and hasn't yet reached the maximum count from `b`.
3. Check if the match counter for the current window is at least `k`. If so, increment the answer.
4. Slide the window forward one element at a time. For each shift, remove the element that leaves the window and add the element that enters. Update the match counter according to the frequency dictionary. When removing, decrement the counter if the element was contributing to the match; when adding, increment it if it now contributes.
5. Repeat until the end of the array. The answer will be the total number of windows where the match counter is at least `k`.

Why it works: At each step, the match counter exactly reflects the number of elements in the current window that can correspond to elements in `b` without exceeding their frequency. Sliding the window updates this count efficiently, preserving correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import Counter

def solve():
    t = int(input())
    for _ in range(t):
        n, m, k = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        b_count = Counter(b)
        window_count = Counter()
        matches = 0
        result = 0

        # Initialize first window
        for i in range(m):
            x = a[i]
            if x in b_count:
                if window_count[x] < b_count[x]:
                    matches += 1
                window_count[x] += 1
        if matches >= k:
            result += 1

        # Slide the window
        for i in range(m, n):
            out_elem = a[i - m]
            in_elem = a[i]

            if out_elem in b_count:
                if window_count[out_elem] <= b_count[out_elem]:
                    matches -= 1
                window_count[out_elem] -= 1

            if in_elem in b_count:
                if window_count[in_elem] < b_count[in_elem]:
                    matches += 1
                window_count[in_elem] += 1

            if matches >= k:
                result += 1

        print(result)

if __name__ == "__main__":
    solve()
```

This solution begins by counting frequencies in `b`, then slides a window over `a`, updating the matches and checking the good subsegment condition at each step. The subtle parts are ensuring that incrementing and decrementing `matches` respects the maximum occurrences allowed by `b_count`, which handles repeated numbers correctly. Edge boundaries are managed by careful indexing with `i - m` for the element leaving the window.

## Worked Examples

### Sample 1 Trace

Input:

```
7 4 2
4 1 2 3 4 5 6
1 2 3 4
```

| Window Index | Window | Matches | Result |
| --- | --- | --- | --- |
| 0-3 | [4,1,2,3] | 4 | 1 |
| 1-4 | [1,2,3,4] | 4 | 2 |
| 2-5 | [2,3,4,5] | 3 | 3 |
| 3-6 | [3,4,5,6] | 2 | 4 |

This trace confirms that the algorithm correctly counts matches for each window and updates the result whenever matches >= k.

### Sample 2 Trace

Input:

```
7 4 3
4 1 2 3 4 5 6
1 2 3 4
```

| Window Index | Window | Matches | Result |
| --- | --- | --- | --- |
| 0-3 | [4,1,2,3] | 4 | 1 |
| 1-4 | [1,2,3,4] | 4 | 2 |
| 2-5 | [2,3,4,5] | 3 | 3 |
| 3-6 | [3,4,5,6] | 2 | 3 |

This trace shows that windows with fewer than 3 matches are ignored.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element enters and leaves the window exactly once. |
| Space | O(m) | The counters store frequencies of elements from `b` and the current window. |

Given that the sum of all `n` across test cases is <= 2 * 10^5, this solution fits within the 2-second limit and 256 MB memory limit.

## Test Cases

```python
import sys, io
from collections import Counter

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# Provided samples
assert run("5\n7 4 2\n4 1 2 3 4 5 6\n1 2 3 4\n7 4 3\n4 1 2 3 4 5 6\n1 2 3 4\n7 4 4\n4 1 2 3 4 5 6\n1 2 3 4\n11 5 3\n9 9 2 2 10 9 7 6 3 6 3\n6 9 7 8 10\n4 1 1\n4 1 5 6\n6\n") == "4\n3\n2\n4\n1"

# Custom cases
assert run("1\n3 3 3\n1 1 1\n1 1 1\n") == "1", "all equal"
assert run("1\n5 2 1\n1 2 3 4 5\n5 6\n") == "2", "minimal k=1"
assert run("1\n6 3 2\n1 2 2
```
