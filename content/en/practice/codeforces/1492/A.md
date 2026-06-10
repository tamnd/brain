---
title: "CF 1492A - Three swimmers"
description: "We have three swimmers who repeatedly swim across a pool and return, each at their own fixed period. The first swimmer takes a minutes to complete a round trip, the second b minutes, and the third c minutes."
date: "2026-06-10T22:20:25+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1492
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 704 (Div. 2)"
rating: 800
weight: 1492
solve_time_s: 114
verified: true
draft: false
---

[CF 1492A - Three swimmers](https://codeforces.com/problemset/problem/1492/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We have three swimmers who repeatedly swim across a pool and return, each at their own fixed period. The first swimmer takes `a` minutes to complete a round trip, the second `b` minutes, and the third `c` minutes. You arrive at the pool `p` minutes after the start, and the goal is to determine how many minutes you must wait until at least one swimmer reaches the left side of the pool again.

The input gives multiple independent test cases. For each, we are given four integers `p`, `a`, `b`, and `c`. Each of these values can be as large as 10^18, which means any brute-force simulation that iterates over each swimmer's return times would be infeasible. We need a method that works directly with these large numbers.

The non-obvious edge cases arise when you arrive exactly at the same moment a swimmer is at the left side, or when the wait time is longer than some of the swimmer periods. For example, if `p = 10` and `a = 2, b = 5, c = 10`, you arrive exactly at a time when the third swimmer is there, so the wait time should be `0`. A careless solution that only checks future multiples without considering equality would incorrectly report a positive wait.

## Approaches

A brute-force approach would be to generate all return times for each swimmer up to the moment `p` and beyond, then scan forward to find the first time greater than or equal to `p`. This is correct in principle, but it quickly becomes impractical because `p` can be 10^18 and the periods `a, b, c` can also be very large. Iterating over millions or billions of steps is too slow.

The key observation is that each swimmer’s return times form an arithmetic sequence starting at zero with a step equal to their period. To find the next return time that is no less than `p`, we can compute it mathematically instead of iterating. For a swimmer with period `x`, the next return time after `p` is the smallest multiple of `x` greater than or equal to `p`. If `p` is divisible by `x`, the next return is `p` itself. Otherwise, it is `(p // x + 1) * x`. Once we have the next return time for each swimmer, the wait time is the minimum of `(next_return_time - p)` across all three swimmers.

This reduces the problem from iterating through potentially enormous sequences to a constant-time arithmetic calculation for each swimmer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(p / min(a, b, c)) | O(1) | Too slow |
| Arithmetic Calculation | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read the integers `p`, `a`, `b`, and `c`.
3. For each swimmer period `x` in `[a, b, c]`, compute the next time the swimmer is at the left side that is no earlier than `p`. If `p` is divisible by `x`, the next time is `p`. Otherwise, compute `next_time = ((p // x) + 1) * x`.
4. Compute the wait time for each swimmer as `next_time - p`.
5. The answer for the test case is the minimum wait time across the three swimmers.
6. Print the result for each test case.

Why it works: The arithmetic guarantees we find the first multiple of each swimmer's period that is not less than `p`. Subtracting `p` gives the exact wait time. Taking the minimum over all swimmers ensures we find the earliest one to arrive. Since arithmetic with integers up to 10^18 is supported, no approximations are needed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def next_arrival(p, x):
    if p % x == 0:
        return p
    return ((p // x) + 1) * x

t = int(input())
for _ in range(t):
    p, a, b, c = map(int, input().split())
    wait_times = [next_arrival(p, a) - p,
                  next_arrival(p, b) - p,
                  next_arrival(p, c) - p]
    print(min(wait_times))
```

The function `next_arrival` handles the computation of the next multiple cleanly, avoiding off-by-one errors when `p` is exactly divisible by a swimmer’s period. The main loop reads input efficiently using `sys.stdin.readline` and performs all calculations in integer arithmetic, ensuring correctness for very large values.

## Worked Examples

For the first sample input `9 5 4 8`, the computation proceeds as follows:

| Swimmer | Period `x` | Next multiple ≥ 9 | Wait time |
| --- | --- | --- | --- |
| a | 5 | 10 | 1 |
| b | 4 | 12 | 3 |
| c | 8 | 16 | 7 |

The minimum wait time is `1`.

For the second sample `2 6 10 9`:

| Swimmer | Period `x` | Next multiple ≥ 2 | Wait time |
| --- | --- | --- | --- |
| a | 6 | 6 | 4 |
| b | 10 | 10 | 8 |
| c | 9 | 9 | 7 |

The minimum wait time is `4`.

These traces confirm the algorithm computes the correct next arrival times and correctly selects the minimal wait.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case involves three arithmetic calculations and a minimum. |
| Space | O(1) | Only a constant number of variables are used per test case. |

With `t` up to 1000, this solution easily runs within the 1-second limit even with values up to 10^18.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())  # assuming solution above saved in solution.py
    return output.getvalue().strip()

# provided samples
assert run("4\n9 5 4 8\n2 6 10 9\n10 2 5 10\n10 9 9 9\n") == "1\n4\n0\n8", "sample 1"

# custom cases
assert run("1\n1 1 1 1\n") == "0", "all swimmers arrive immediately"
assert run("1\n10 3 7 11\n") == "1", "general case with different periods"
assert run("1\n1000000000000000000 1 2 3\n") == "0", "p divisible by smallest period"
assert run("1\n5 10 10 10\n") == "5", "all periods larger than p"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 | 0 | Arriving exactly at start time, all swimmers present |
| 10 3 7 11 | 1 | General case with different periods |
| 10^18 1 2 3 | 0 | Handling very large `p` with immediate swimmer arrival |
| 5 10 10 10 | 5 | All swimmer periods greater than arrival time |

## Edge Cases

If you arrive exactly when a swimmer is at the left side, `p % x == 0` ensures the wait time is zero. For example, with input `p=10` and `a=2`, `b=5`, `c=10`, the computation for the third swimmer gives `next_time = 10`, and `next_time - p = 0`. The minimum over all swimmers correctly outputs `0`.

When all periods are larger than `p`, such as `p=5` and `a=b=c=10`, the calculation yields `next_time = 10` for all, and the wait time is `5`, correctly reflecting that you must wait until the first swimmer returns.

This method consistently handles all combinations of arrival times relative to swimmers’ periods.
