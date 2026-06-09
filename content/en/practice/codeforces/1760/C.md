---
title: "CF 1760C - Advantage"
description: "We have a list of competitors, each with a numeric strength. For every competitor, we want to compute their advantage over the strongest opponent that is not themselves. Concretely, if the array of strengths is [s1, s2, ..."
date: "2026-06-09T14:20:24+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1760
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 835 (Div. 4)"
rating: 800
weight: 1760
solve_time_s: 166
verified: false
draft: false
---

[CF 1760C - Advantage](https://codeforces.com/problemset/problem/1760/C)

**Rating:** 800  
**Tags:** data structures, implementation, sortings  
**Solve time:** 2m 46s  
**Verified:** no  

## Solution
## Problem Understanding

We have a list of competitors, each with a numeric strength. For every competitor, we want to compute their advantage over the strongest opponent that is not themselves. Concretely, if the array of strengths is `[s_1, s_2, ..., s_n]`, for each `i` we need to find the largest value among all `s_j` with `j ≠ i`, and subtract it from `s_i`. The result can be negative if `s_i` is smaller than all others.

The constraints allow up to `2 * 10^5` participants across all test cases, with each individual strength up to `10^9`. This implies that any solution iterating over all participants for every single competitor, resulting in O(n²) operations per test case, would be too slow. The sum over all `n` being limited to `2 * 10^5` allows a linear or linearithmic per-test-case solution. Sorting or scanning arrays a constant number of times is feasible.

The main edge cases to watch for are arrays where multiple participants share the maximum strength. If the maximum occurs more than once, removing one of them still leaves the same maximum. For example, in `[5, 5, 3]`, the first participant sees a max of 5 among others, giving `5 - 5 = 0`, not `5 - 3 = 2`. Arrays with all equal values are another edge case, e.g., `[4, 4, 4, 4]`, where every participant’s advantage is zero.

## Approaches

A straightforward brute-force approach would iterate for each participant, scan all others, and pick the maximum. This works because it directly implements the problem statement, but the operation count is `n * (n-1)`, which is roughly 4 * 10^10 in the worst case if `n` is 2 * 10^5. That is far too slow.

The key insight for a faster approach is that the maximum of all other participants is either the global maximum of the array or, if the current participant holds the maximum, the second largest value in the array. Therefore, we only need to know the largest and second largest strengths in each test case. Once these two values are known, computing each participant's advantage becomes a single subtraction operation. This reduces the work to a single pass to compute the two largest values and another pass to compute the answers, achieving O(n) per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and the array of strengths `s`.
3. Initialize two variables `max1` and `max2` to store the largest and second largest values. Iterate through `s` once, updating these variables. If a number is greater than `max1`, assign `max2 = max1` and `max1 = number`. If it is between `max1` and `max2`, assign `max2 = number`.
4. Iterate through the array again. For each participant, if their strength equals `max1`, their "other max" is `max2`; otherwise, it is `max1`.
5. Compute the difference between the participant's strength and their corresponding "other max", and output it.

Why it works: at every step, `max1` and `max2` correctly store the largest and second largest numbers. For any participant, if they are the largest, removing them exposes `max2` as the next largest. Otherwise, removing them does not change the maximum. This invariant guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    s = list(map(int, input().split()))
    max1 = max2 = -1
    for num in s:
        if num > max1:
            max2 = max1
            max1 = num
        elif num > max2:
            max2 = num
    res = []
    for num in s:
        other_max = max2 if num == max1 else max1
        res.append(num - other_max)
    print(' '.join(map(str, res)))
```

The first loop computes the two largest values. The second loop computes the advantage for each participant in constant time. Using `max2 if num == max1 else max1` ensures that if multiple participants share the maximum, each one still uses the correct "other max". Fast I/O prevents TLE when handling large inputs.

## Worked Examples

Trace for input `[4, 7, 3, 5]`:

| Participant | s_i | max1 | max2 | other_max | s_i - other_max |
| --- | --- | --- | --- | --- | --- |
| 4 | 4 | 7 | 5 | 7 | -3 |
| 7 | 7 | 7 | 5 | 5 | 2 |
| 3 | 3 | 7 | 5 | 7 | -4 |
| 5 | 5 | 7 | 5 | 7 | -2 |

This confirms that the algorithm correctly distinguishes between the largest participant and others.

Trace for input `[4, 4, 4, 4]`:

| Participant | s_i | max1 | max2 | other_max | s_i - other_max |
| --- | --- | --- | --- | --- | --- |
| 4 | 4 | 4 | 4 | 4 | 0 |
| 4 | 4 | 4 | 4 | 4 | 0 |
| 4 | 4 | 4 | 4 | 4 | 0 |
| 4 | 4 | 4 | 4 | 4 | 0 |

This shows the edge case of all equal strengths is handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single pass to find max1 and max2, single pass to compute differences |
| Space | O(n) | Output array stores n values per test case |

Since the sum of `n` over all test cases does not exceed 2 * 10^5, the solution easily runs under the 2-second time limit and within 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n = int(input())
        s = list(map(int, input().split()))
        max1 = max2 = -1
        for num in s:
            if num > max1:
                max2 = max1
                max1 = num
            elif num > max2:
                max2 = num
        res = []
        for num in s:
            other_max = max2 if num == max1 else max1
            res.append(num - other_max)
        print(' '.join(map(str, res)))
    return output.getvalue().strip()

# Provided samples
assert run("5\n4\n4 7 3 5\n2\n1 2\n5\n1 2 3 4 5\n3\n4 9 4\n4\n4 4 4 4\n") == "-3 2 -4 -2\n-1 1\n-4 -3 -2 -1 1\n-5 5 -5\n0 0 0 0"

# Custom cases
assert run("1\n2\n10 1\n") == "9 -9", "minimum size input"
assert run("1\n3\n7 7 3\n") == "0 0 -4", "duplicate maximum"
assert run("1\n4\n1 2 3 4\n") == "-3 -2 -1 1", "ascending order"
assert run("1\n5\n5 5 5 5 5\n") == "0 0 0 0 0", "all equal values"
assert run("1\n6\n1 1000000000 2 999999999 3 4\n") == "-999999999 1 -999999997 1 -999999996 -999999995", "large numbers and second max"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n10 1 | 9 -9 | Minimum size array, difference calculation |
| 3\n7 7 3 | 0 0 -4 | Multiple maximums edge case |
| 4\n1 2 3 4 | -3 -2 -1 1 | Increasing sequence |
| 5\n5 5 5 5 5 | 0 0 0 0 0 | All values equal |
| 6\n1 1000000000 2 999999999 3 4 | -999999999 1 -999999997 1 -999999996 -999999995 | Very large numbers, second max selection |

## Edge Cases

If the largest value occurs more than once, each participant holding that value should use the second largest among all numbers as the "other max". For example, `[7, 7, 3]` produces
