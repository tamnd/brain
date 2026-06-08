---
title: "CF 2051B - Journey"
description: "Monocarp is going on a multi-day hike and has a repeating pattern of distances for each day: he walks a kilometers on the first day, b on the second, c on the third, then repeats that cycle indefinitely."
date: "2026-06-08T08:39:49+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "math"]
categories: ["algorithms"]
codeforces_contest: 2051
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 995 (Div. 3)"
rating: 800
weight: 2051
solve_time_s: 91
verified: true
draft: false
---

[CF 2051B - Journey](https://codeforces.com/problemset/problem/2051/B)

**Rating:** 800  
**Tags:** binary search, math  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

Monocarp is going on a multi-day hike and has a repeating pattern of distances for each day: he walks `a` kilometers on the first day, `b` on the second, `c` on the third, then repeats that cycle indefinitely. Given a target total distance `n`, we are asked to determine the exact day on which Monocarp reaches or exceeds `n` kilometers cumulatively. Each test case gives four integers: the target distance `n` and the distances for the three-day cycle `a`, `b`, `c`. The output is simply the day number when Monocarp completes his journey.

The constraints allow up to 10,000 test cases, each with `n` up to 1 billion and daily distances up to 1 million. This means that a naive approach that simulates every day one by one could perform up to 1 billion operations for a single test case, which is far too slow. Any approach must account for the repeating pattern and the potential for very large `n` without iterating through every day individually.

Edge cases arise when the journey completes within the first cycle, especially on the first day itself. For example, if `n = 6` and the first-day distance `a = 6`, Monocarp finishes immediately. Another edge case is when `n` is very large, forcing many complete cycles before the final partial cycle contributes to reaching `n`. A careless implementation might attempt to iterate day by day and either time out or incorrectly handle off-by-one counting at the end of a partial cycle.

## Approaches

A brute-force solution would simulate the journey day by day, maintaining a running total of distance, and stop once the total reaches or exceeds `n`. While this is correct, the worst case occurs when `n = 10^9` and the daily distances are small (for example, `a = b = c = 1`). The algorithm would need roughly 1 billion iterations, which is infeasible within 1 second.

The key observation is that the distances repeat in a cycle of three days. The sum of a full cycle is `cycle_sum = a + b + c`. If we can calculate how many complete cycles are needed before reaching `n`, we can jump in multiples of three days rather than iterating day by day. After completing full cycles, we only need to check at most three more days to reach `n`. This reduces the problem from potentially billions of iterations to at most a few simple arithmetic operations per test case.

The brute-force approach is conceptually simple but slow, while the optimized approach leverages the periodicity of the sequence to reduce computations dramatically. We can combine simple math with conditional checks for the partial cycle at the end.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow for large n |
| Cycle Jump | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read input values `n`, `a`, `b`, `c` for a single test case. These represent the target distance and the three-day walking distances.
2. Compute the sum of one full three-day cycle: `cycle_sum = a + b + c`. This represents the total distance Monocarp walks in three days.
3. Compute the number of complete three-day cycles that can fit before exceeding `n`: `full_cycles = (n - 1) // cycle_sum`. The `-1` ensures we correctly account for the final day if the exact total lands on the cycle boundary. Multiply `full_cycles` by 3 to get `days = full_cycles * 3`. This is the day count after all full cycles.
4. Calculate the cumulative distance after the full cycles: `distance_so_far = full_cycles * cycle_sum`.
5. Iterate over the next days in the cycle (up to three days: `a`, `b`, `c`), adding each day's distance to `distance_so_far`. After each addition, check if `distance_so_far >= n`. The first day that satisfies this condition is the answer. Increment `days` with each additional day.
6. Output `days` as the day Monocarp reaches at least `n` kilometers.

Why it works: By leveraging the periodicity of the walking distances, we can jump over entire three-day cycles that do not individually require day-by-day simulation. The partial cycle is small, only up to three days, so iterating through it is negligible. The invariant is that after accounting for full cycles, `distance_so_far` is always less than `n`, and the first day in the next partial cycle that pushes the total above `n` is guaranteed to be the correct completion day.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, a, b, c = map(int, input().split())
    cycle_sum = a + b + c
    
    # number of full cycles
    full_cycles = (n - 1) // cycle_sum
    days = full_cycles * 3
    distance_so_far = full_cycles * cycle_sum
    
    for d in [a, b, c]:
        if distance_so_far >= n:
            break
        distance_so_far += d
        days += 1
    
    print(days)
```

The code first reads the number of test cases. For each test case, it computes the sum of the three-day cycle and the number of complete cycles to jump. It then adds days from the next partial cycle, checking after each addition if the total distance reaches `n`. The iteration over `[a, b, c]` ensures we never exceed three extra checks.

## Worked Examples

**Example 1:** `n = 12, a = 1, b = 5, c = 3`

| Step | days | distance_so_far | Action |
| --- | --- | --- | --- |
| full_cycles | 1*3=3 | 9 | after 1 full cycle of 9 km |
| day 4 | 4 | 9+1=10 | check distance < n |
| day 5 | 5 | 10+5=15 | distance >= n → stop |

The algorithm returns 5, matching the expected result.

**Example 2:** `n = 6, a = 6, b = 7, c = 4`

| Step | days | distance_so_far | Action |
| --- | --- | --- | --- |
| full_cycles | 0 | 0 | (n-1)//cycle_sum = 0 |
| day 1 | 1 | 0+6=6 | distance >= n → stop |

The algorithm returns 1, correct for a single-day completion.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only arithmetic and at most three additional day checks |
| Space | O(1) | No extra structures, only integers |

With up to 10,000 test cases, the total operations remain very small, comfortably within the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n, a, b, c = map(int, input().split())
        cycle_sum = a + b + c
        full_cycles = (n - 1) // cycle_sum
        days = full_cycles * 3
        distance_so_far = full_cycles * cycle_sum
        for d in [a, b, c]:
            if distance_so_far >= n:
                break
            distance_so_far += d
            days += 1
        output.append(str(days))
    return "\n".join(output)

# Provided samples
assert run("4\n12 1 5 3\n6 6 7 4\n16 3 4 1\n1000000000 1 1 1\n") == "5\n1\n6\n1000000000", "sample tests"

# Custom tests
assert run("1\n1 1 1 1\n") == "1", "minimum n"
assert run("1\n3 1 1 1\n") == "3", "exact 1 cycle"
assert run("1\n10 2 2 2\n") == "5", "partial cycle after full cycles"
assert run("1\n7 3 2 2\n") == "3", "finishes within first cycle"
assert run("1\n1000000 1000000 1000000 1000000\n") == "1", "large single step"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 | 1 | Minimum n completes on first day |
| 3 1 1 1 | 3 | Exact completion at end of first cycle |
| 10 2 2 2 | 5 | Partial cycle after full cycles |
| 7 3 2 2 | 3 | Completion within first cycle |
| 1000000 1000000 1000000 1000000 | 1 | Large value finishes immediately |

## Edge Cases

When `n` is smaller than the first day, such as `n=1` and `a=1, b=1, c=1`, `full_cycles = 0`, and the first iteration over `[a, b, c]` immediately satisfies `distance_so_far
