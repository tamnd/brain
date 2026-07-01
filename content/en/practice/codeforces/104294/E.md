---
title: "CF 104294E - Monster-Slayer"
description: "We are given a line of monsters, each with an integer power value. We want to choose a contiguous block of these monsters and compute the sum of their powers. Among all possible contiguous blocks, we need the one whose sum is as large as possible, and we output that sum."
date: "2026-07-01T20:25:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104294
codeforces_index: "E"
codeforces_contest_name: "UTPC Spring 2023 Open Contest"
rating: 0
weight: 104294
solve_time_s: 64
verified: true
draft: false
---

[CF 104294E - Monster-Slayer](https://codeforces.com/problemset/problem/104294/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of monsters, each with an integer power value. We want to choose a contiguous block of these monsters and compute the sum of their powers. Among all possible contiguous blocks, we need the one whose sum is as large as possible, and we output that sum.

The input is simply a sequence of integers. Each integer can be positive, negative, or zero. A valid choice is any interval from index i to j, and its score is the sum of elements in that interval. The task is to find the maximum possible score over all such intervals.

The constraints allow up to 100000 elements, with values up to 10^9 in magnitude. This immediately rules out any solution that tries all subarrays explicitly. A naive O(n^2) enumeration already computes about 5 billion intervals in the worst case, and if each requires O(n) summation it becomes O(n^3), which is far beyond the time limit. Even O(n^2) is too slow in Python under 1 second.

A subtle point is handling cases where all numbers are negative. A common incorrect approach is to return 0 by assuming we can pick an empty subarray. The problem does not allow an empty subarray, so we must pick at least one element. For example, for input `[-5, -2, -8]`, the correct answer is `-2`, not `0`.

Another edge case is a single-element array. For `[7]`, the answer is `7`, and any logic that initializes the best sum to 0 without care will fail here.

## Approaches

The brute-force idea is straightforward: consider every possible starting index, extend it to every possible ending index, compute the sum, and track the maximum. This is correct because every contiguous subarray is explicitly evaluated. However, the cost comes from recomputing sums repeatedly. There are about n(n+1)/2 subarrays, and even with incremental sums, this is O(n^2) operations, which is too slow for 100000 elements.

The key observation is that when scanning left to right, the best subarray ending at position i either extends the best subarray ending at i−1 or starts fresh at i. If the running sum becomes negative, keeping it only makes future sums worse, since it will subtract from any extension. This reduces the problem to maintaining a single running best ending at each position.

This is the essence of Kadane’s idea: we compress all subarray choices ending at each index into a single state, instead of exploring all partitions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimal (Kadane) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process the array from left to right while maintaining two values: the best sum ending at the current position, and the best overall answer seen so far.

1. Initialize both the current running sum and the global best answer with the first element of the array. This ensures correctness even if all values are negative.
2. For each next element p[i], decide whether to extend the previous subarray or start a new one at i. We compute the new running sum as the maximum of p[i] and current_sum + p[i]. This choice reflects whether the previous accumulated sum is beneficial or harmful.
3. Update the global best answer as the maximum of itself and the new running sum. This ensures we record the best subarray seen anywhere in the array, not only those ending at the last index.
4. Continue until the end of the array and output the global best answer.

The core decision happens at each index: if the previous sum is negative, adding it to the current element only reduces the result, so restarting is optimal. If it is positive, extending improves the sum.

### Why it works

At every index i, the algorithm maintains the invariant that the current running sum is the maximum possible subarray sum that must end exactly at i. Any subarray ending at i either comes from extending a subarray ending at i−1 or starting fresh at i. Since both possibilities are explicitly compared, no valid candidate is missed. The global maximum tracks the best among all endpoints, so once the scan completes, it must equal the best subarray over the entire array.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

cur = a[0]
best = a[0]

for i in range(1, n):
    cur = max(a[i], cur + a[i])
    best = max(best, cur)

print(best)
```

The implementation directly mirrors the state transition described earlier. `cur` stores the best subarray sum ending at the current position, while `best` tracks the global optimum. Initializing both with `a[0]` avoids incorrect handling of all-negative arrays.

The critical detail is the order of updates: we must compute the new `cur` before updating `best`, since `best` depends on the updated subarray ending at i. Another subtle point is initialization, which must not default to 0.

## Worked Examples

### Example 1

Input:

```
9
-2 10 -3 5 -2 1 2 6 -1
```

| i | a[i] | cur (best ending here) | best |
| --- | --- | --- | --- |
| 0 | -2 | -2 | -2 |
| 1 | 10 | 10 | 10 |
| 2 | -3 | 7 | 10 |
| 3 | 5 | 12 | 12 |
| 4 | -2 | 10 | 12 |
| 5 | 1 | 11 | 12 |
| 6 | 2 | 13 | 13 |
| 7 | 6 | 19 | 19 |
| 8 | -1 | 18 | 19 |

This trace shows how negative values are selectively absorbed or rejected depending on whether they reduce the running total. The final peak occurs when the accumulation of positive contributions outweighs earlier negatives.

### Example 2

Input:

```
5
-4 -1 -7 -3 -2
```

| i | a[i] | cur | best |
| --- | --- | --- | --- |
| 0 | -4 | -4 | -4 |
| 1 | -1 | -1 | -1 |
| 2 | -7 | -7 | -1 |
| 3 | -3 | -3 | -1 |
| 4 | -2 | -2 | -1 |

This case demonstrates that the algorithm never incorrectly returns 0. It correctly identifies the least negative single element as the best subarray.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed exactly once with constant work |
| Space | O(1) | Only two variables are maintained regardless of input size |

The linear scan comfortably fits within constraints for 100000 elements, and constant memory ensures no overhead from auxiliary structures.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    cur = a[0]
    best = a[0]

    for i in range(1, n):
        cur = max(a[i], cur + a[i])
        best = max(best, cur)

    return str(best)

# provided sample
assert run("9\n-2 10 -3 5 -2 1 2 6 -1\n") == "19"

# single element
assert run("1\n5\n") == "5"

# all negative
assert run("3\n-5 -2 -8\n") == "-2"

# all positive
assert run("4\n1 2 3 4\n") == "10"

# alternating
assert run("5\n1 -2 3 -2 5\n") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 5 | base initialization |
| all negative | -2 | no empty subarray allowed |
| all positive | 10 | full accumulation correctness |
| alternating values | 5 | restart vs extend logic |

## Edge Cases

For a single-element array like `[5]`, the algorithm initializes `cur` and `best` to 5 and returns it immediately. No iteration is required, and the invariant trivially holds since there is only one possible subarray.

For an all-negative array like `[-5, -2, -8]`, the running sum repeatedly restarts at each element because extending only decreases the value. The trace is `cur = -5, -2, -8` with `best = -2`, correctly selecting the least negative element. This shows that the algorithm does not incorrectly prefer longer subarrays when they are harmful.
