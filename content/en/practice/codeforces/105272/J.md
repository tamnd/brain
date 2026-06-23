---
title: "CF 105272J - Jupiter's Dinner"
description: "We are given a sequence of requests arranged in a line, where each position corresponds to a person who ordered a specific type of dish. Alongside this, there is a constraint: a waiter has only k “arms”, and each arm can carry arbitrarily many dishes but only of one dish type."
date: "2026-06-23T14:03:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105272
codeforces_index: "J"
codeforces_contest_name: "IX MaratonUSP Freshman Contest"
rating: 0
weight: 105272
solve_time_s: 48
verified: true
draft: false
---

[CF 105272J - Jupiter's Dinner](https://codeforces.com/problemset/problem/105272/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of requests arranged in a line, where each position corresponds to a person who ordered a specific type of dish. Alongside this, there is a constraint: a waiter has only k “arms”, and each arm can carry arbitrarily many dishes but only of one dish type. This means that if an interval of customers contains at most k distinct dish types, the waiter can serve all of them in one trip.

The task is to find a contiguous segment of the array that contains at most k distinct values, and among all such segments, we want one with maximum possible length. We must output both the length and the indices of one optimal segment.

The array length and k can be as large as 200000, so any quadratic or near-quadratic approach will fail. A solution must process the array in linear or near-linear time, typically O(n) or O(n log n). This strongly suggests a sliding window or two-pointer technique with frequency tracking.

A naive approach would try all subarrays and count distinct elements in each. That leads to O(n²) subarrays, and even with optimized counting it becomes too slow because maintaining distinct counts still costs O(1) amortized but the number of subarrays is too large.

A more subtle failure case for naive reasoning appears when the array has many repeated blocks. For example, if all elements are distinct and k is small, most intervals are invalid, but we would still waste time checking them. Conversely, if k is large, many intervals are valid, and brute force again explodes.

The core difficulty is not checking validity, but efficiently maintaining the set of distinct elements while moving across all candidate intervals.

## Approaches

The brute-force idea is straightforward: pick every left endpoint l, extend r from l to n, and track how many distinct values are in the current segment. Each time we extend r, we update a frequency table. If the number of distinct elements is at most k, we update the best answer. This is correct because it explores all possible intervals.

However, the number of intervals is O(n²). Even though updating frequency when expanding r is O(1), we still perform about n(n+1)/2 expansions, which is far too large for n up to 200000.

The key observation is that the constraint “at most k distinct values” is monotonic with respect to shrinking and expanding intervals. If an interval is valid, expanding it may break validity, and if it is invalid, shrinking it may restore validity. This structure is exactly what allows a two-pointer sliding window approach.

Instead of recomputing from scratch for each l, we maintain a window [l, r] and ensure it always satisfies the constraint. We move r forward greedily, and whenever the constraint is violated, we move l forward until it becomes valid again. Each index enters and leaves the window at most once, giving linear complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Two Pointers | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain a frequency map of values inside the current window and a counter tracking how many distinct values are currently present. We also maintain two pointers l and r defining the current segment, and variables tracking the best segment seen so far.

1. Initialize l = 0, best_length = 0, and an empty frequency structure. The current distinct count is 0 because the window is empty.
2. Expand r from left to right. For each new element a[r], increment its frequency. If this value was not previously in the window, increment the distinct counter. This step grows the window greedily.
3. After inserting a[r], if the number of distinct values exceeds k, we must restore validity. We do this by moving l forward. For each step, we decrement frequency of a[l]. If it becomes zero, we reduce the distinct counter. We continue until the window again has at most k distinct values.
4. Once the window is valid, we compare its length (r - l + 1) with the best length found so far. If it is larger, we update the best answer and store the current l and r.
5. Continue until r reaches the end of the array.

Why this works: at every r, we find the longest valid segment ending at r. Any shorter segment ending at r is contained inside it, so it cannot improve the answer beyond what we already consider. The sliding adjustment ensures that l is always minimal such that the constraint holds, so the window is always the maximal valid window for that r.

The invariant is that at the start of each iteration for r, the window [l, r-1] contains at most k distinct values, and after processing r and adjusting l, the window [l, r] is the smallest left boundary that keeps at most k distinct values. This ensures no valid segment is skipped and every candidate maximal segment is examined exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    freq = {}
    distinct = 0

    l = 0
    best_len = 0
    best_l = 0
    best_r = 0

    for r in range(n):
        x = a[r]
        if x not in freq or freq[x] == 0:
            freq[x] = 1
            distinct += 1
        else:
            freq[x] += 1

        while distinct > k:
            y = a[l]
            freq[y] -= 1
            if freq[y] == 0:
                distinct -= 1
            l += 1

        if r - l + 1 > best_len:
            best_len = r - l + 1
            best_l = l
            best_r = r

    print(best_len)
    print(best_l + 1, best_r + 1)

if __name__ == "__main__":
    solve()
```

The frequency dictionary tracks how many times each dish type appears inside the current window. The distinct counter avoids repeatedly scanning the dictionary keys. The inner loop ensures the window always satisfies the k-distinct constraint after each extension of r.

Indexing is carefully handled by storing best_l and best_r in zero-based form and converting to one-based output at the end.

## Worked Examples

### Example 1

Input:

```
5 2
1 2 3 2 1
```

We track the sliding window:

| r | a[r] | l | window | distinct | action | best |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | [1] | 1 | valid | [1,1] |
| 1 | 2 | 0 | [1,2] | 2 | valid | [1,2] |
| 2 | 3 | 0→1 | [2,3] | 2 | shrink | [1,2] |
| 3 | 2 | 1 | [2,3,2] | 2 | valid | [2,4] |
| 4 | 1 | 1→2 | [3,2,1] | 3→2 | shrink | [2,4] |

The best segment is [2,4], which matches the optimal window when r = 3.

This trace shows how the left pointer moves only when the constraint is violated, preserving maximal valid windows.

### Example 2

Input:

```
8 3
4 1 2 3 3 2 1 4
```

| r | a[r] | l | window | distinct | action | best |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 4 | 0 | [4] | 1 | valid | [1,1] |
| 1 | 1 | 0 | [4,1] | 2 | valid | [1,2] |
| 2 | 2 | 0 | [4,1,2] | 3 | valid | [1,3] |
| 3 | 3 | 0 | [4,1,2,3] | 4→3 | shrink to l=1 | [2,4] |
| 4 | 3 | 1 | [1,2,3,3] | 3 | valid | [2,5] |
| 5 | 2 | 1 | [1,2,3,3,2] | 3 | valid | [2,6] |
| 6 | 1 | 1 | [1,2,3,3,2,1] | 3 | valid | [2,7] |
| 7 | 4 | 1→2 | [2,3,3,2,1,4] | 4→3 | shrink | [2,7] |

The best segment becomes [2,7], illustrating that the algorithm captures long stable stretches once the window is reduced to satisfy k.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | each index enters and leaves the window at most once |
| Space | O(n) | frequency map stores counts of active elements |

The linear behavior is sufficient for n up to 200000, and the memory usage fits comfortably within typical limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    freq = {}
    distinct = 0
    l = 0

    best_len = 0
    best_l = best_r = 0

    for r in range(n):
        x = a[r]
        freq[x] = freq.get(x, 0) + 1
        if freq[x] == 1:
            distinct += 1

        while distinct > k:
            y = a[l]
            freq[y] -= 1
            if freq[y] == 0:
                distinct -= 1
            l += 1

        if r - l + 1 > best_len:
            best_len = r - l + 1
            best_l, best_r = l, r

    return f"{best_len}\n{best_l+1} {best_r+1}\n"

# provided samples
assert run("5 2\n1 2 3 2 1\n") == "3\n2 4\n"
assert run("8 3\n4 1 2 3 3 2 1 4\n") == "6\n2 7\n"

# custom cases
assert run("1 1\n7\n") == "1\n1 1\n"
assert run("5 5\n1 2 3 4 5\n") == "5\n1 5\n"
assert run("5 1\n1 1 1 1 1\n") == "5\n1 5\n"
assert run("6 2\n1 1 2 2 3 3\n") == "4\n1 4\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | full range | minimum size correctness |
| k large | whole array | trivial validity |
| k = 1 | all equal | strict constraint handling |
| alternating groups | partial window | shrink correctness |

## Edge Cases

A minimal case with n = 1 tests whether the algorithm initializes best answers correctly without entering the shrinking loop. The window starts valid and should immediately be recorded.

A case where k ≥ number of distinct values tests whether the algorithm avoids unnecessary shrinking. The window should expand fully without any contraction, confirming correctness of the “only shrink when needed” logic.

A case where k = 1 and all elements differ tests aggressive shrinking behavior. The window should always collapse to a single element, ensuring the frequency map correctly resets counts and the distinct counter is decremented precisely when a value leaves the window completely.
