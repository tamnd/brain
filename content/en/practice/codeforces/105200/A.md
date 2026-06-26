---
title: "CF 105200A - Array Issue"
description: "We are given an array of integers, and the task is to evaluate a classic “maximum subarray” quantity repeatedly as we extend the array from left to right."
date: "2026-06-27T02:52:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105200
codeforces_index: "A"
codeforces_contest_name: "IME++ Starters Try-outs 2024"
rating: 0
weight: 105200
solve_time_s: 55
verified: true
draft: false
---

[CF 105200A - Array Issue](https://codeforces.com/problemset/problem/105200/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and the task is to evaluate a classic “maximum subarray” quantity repeatedly as we extend the array from left to right. At every prefix of the array, we want to know the best possible sum of any contiguous subarray that lies entirely inside that prefix. The output is the sequence of these best values, one for each prefix.

Another way to read the task is that we simulate revealing the array one element at a time. After seeing the first element, we compute the maximum subarray sum of that single element. After seeing the first two elements, we recompute the maximum subarray sum over both. This continues until the full array is processed.

The key constraint implication is that a straightforward recomputation for each prefix would be too slow. If the array length is up to typical competitive programming limits like 100000, then recomputing a full Kadane scan for each prefix leads to O(n²) behavior, which is far beyond acceptable. We need to maintain incremental state so that each new element updates the answer in constant time.

A common edge case is when all numbers are negative. For example, if the array is [-5, -2, -8], then the answer for each prefix is the largest single element seen so far, not zero. A naive Kadane implementation that resets negatives to zero would incorrectly output zeros, which are not valid subarray sums if empty subarrays are disallowed.

Another subtle case is when the best subarray for a prefix ends exactly at the current position. For instance, in [3, -10, 4], the prefix answers evolve as 3, 3, 4. Any approach that only tracks global best without properly maintaining a “best ending here” state will fail on transitions where restarting at the current element is better than extending.

## Approaches

The brute-force approach recomputes the maximum subarray sum for every prefix independently. For each prefix ending at index i, we scan all subarrays ending at or before i and compute their sums. A direct implementation tries all pairs (l, r) with r ≤ i, leading to O(n²) work per prefix, and O(n³) overall if implemented naively via summation. Even with prefix sums reducing range sum queries to O(1), we still have O(n²) subarrays per prefix, making it infeasible.

The reason this is wasteful is that adjacent prefixes share almost all structure. When moving from prefix i to prefix i+1, we are only adding one new element, but brute force recomputes everything from scratch instead of updating previous results.

The key observation is that Kadane’s algorithm already maintains exactly the two pieces of information needed for this process: the best subarray sum ending at the current position, and the best subarray sum seen so far. The first value can be updated in O(1) by deciding whether to extend the previous subarray or start fresh at the current element. The second value is simply the maximum over time.

By maintaining these two states as we iterate, we naturally produce the answer for every prefix without recomputation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) or O(n³) | O(1) | Too slow |
| Optimal Kadane per prefix | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize two variables, one to track the best subarray sum ending at the current index and one to track the best answer seen so far. The first must start from the first element because an empty subarray is not allowed.
2. Iterate through the array from left to right, processing one element at a time. At each step, we decide whether to extend the previous subarray or start a new one at the current element.
3. Update the “best ending here” value as the maximum between the current element alone and the previous best ending plus the current element. This choice reflects whether continuity helps or hurts.
4. Update the global best value as the maximum between its current value and the newly computed “best ending here”.
5. Output the global best after each iteration, since at that point it represents the maximum subarray sum of the current prefix.

### Why it works

The algorithm maintains a precise invariant: after processing index i, the variable tracking “best ending here” equals the maximum sum of any subarray that must end exactly at i, and the global best equals the maximum sum of any subarray fully contained in the prefix [0, i]. Any subarray ending at i either extends a subarray ending at i-1 or starts fresh at i, so the transition captures all possibilities. Since every subarray has a unique ending position, every candidate subarray is considered exactly once as it becomes the “ending here” state, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = input().strip().split()
    if not data:
        return
    n = int(data[0])
    arr = list(map(int, data[1:]))

    # In case input is split across lines
    if len(arr) < n:
        while len(arr) < n:
            arr.extend(map(int, input().split()))

    best_ending = arr[0]
    best_global = arr[0]

    out = [str(best_global)]

    for i in range(1, n):
        x = arr[i]

        best_ending = max(x, best_ending + x)
        best_global = max(best_global, best_ending)

        out.append(str(best_global))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution starts by reading the full array carefully, including the case where the first line might not contain all elements. This is a common competitive programming pitfall when inputs are space or newline mixed.

The variable `best_ending` corresponds to the best subarray sum that must end at the current position. The update `max(x, best_ending + x)` directly encodes the decision of restarting or extending. The variable `best_global` tracks the best seen across all prefixes so far, and is appended after each update to produce the required output sequence.

A subtle detail is initialization. Both variables start at the first element, not zero, because subarrays must contain at least one element.

## Worked Examples

Consider the array [3, -2, 5].

| i | value | best_ending | best_global | output |
| --- | --- | --- | --- | --- |
| 0 | 3 | 3 | 3 | 3 |
| 1 | -2 | max(-2, 3 + -2 = 1) = 1 | 3 | 3 |
| 2 | 5 | max(5, 1 + 5 = 6) = 6 | 6 | 3 3 6 |

This trace shows how a negative value does not reset everything, but only reduces the ending sum if extension is still beneficial. The global answer remains stable until a better subarray appears.

Now consider [-1, -2, -3].

| i | value | best_ending | best_global | output |
| --- | --- | --- | --- | --- |
| 0 | -1 | -1 | -1 | -1 |
| 1 | -2 | max(-2, -1 + -2 = -3) = -2 | -1 | -1 |
| 2 | -3 | max(-3, -2 + -3 = -5) = -3 | -1 | -1 |

This confirms that the algorithm correctly avoids zero initialization and preserves the largest negative element.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once with constant-time transitions |
| Space | O(1) | Only two running variables are maintained |

The linear time complexity is essential for handling large arrays, since any quadratic recomputation over prefixes would exceed typical limits by several orders of magnitude. The constant space usage ensures memory stability even at maximum input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from main import solve
    return solve()

# Since solve() prints directly, we adapt testing by capturing stdout
import contextlib

def run(inp: str) -> str:
    import sys, io
    backup_in = sys.stdin
    backup_out = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = backup_in
        sys.stdout = backup_out

# sample-like cases
assert run("3\n3 -2 5\n") == "3\n3\n6", "basic mixed case"
assert run("3\n-1 -2 -3\n") == "-1\n-1\n-1", "all negative"

# custom cases
assert run("1\n5\n") == "5", "single element"
assert run("5\n1 2 3 4 5\n") == "1\n3\n6\n10\n15", "increasing array"
assert run("4\n-1 5 -1 5\n") == "-1\n5\n5\n9", "alternating gains"
assert run("6\n2 -1 2 -1 2 -1\n") == "2\n2\n3\n3\n4\n4", "repeated interruptions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 5 | base initialization |
| increasing array | cumulative growth | positive-only behavior |
| alternating gains | stable max propagation | prefix stability |
| repeated interruptions | restart vs extend logic | Kadane transitions |

## Edge Cases

For an input like [-5, -1, -3], the algorithm initializes with -5. After the second element, it evaluates best_ending = max(-1, -5 + -1 = -6) = -1, and best_global remains -1. After the third element, best_ending = max(-3, -1 + -3 = -4) = -3, and best_global stays -1. The output correctly remains the best prefix value at each step, never incorrectly introducing zero.

For an input like [4, -10, 6], the algorithm first sets best_ending = 4, best_global = 4. At index 1, best_ending becomes max(-10, -6) = -6, but best_global remains 4. At index 2, best_ending becomes max(6, 0) = 6, updating best_global to 6. This demonstrates how the restart at the third element is correctly captured through the local transition rule rather than any global recomputation.
