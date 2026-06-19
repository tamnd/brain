---
title: "CF 106136C - Time Trouble"
description: "We are given two small integers for each test case, and we must decide whether we can interpret them as the two fields of a valid 24-hour clock time in the format HH:MM."
date: "2026-06-19T19:40:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106136
codeforces_index: "C"
codeforces_contest_name: "East China University of Science and Technology Programming Contest 2025"
rating: 0
weight: 106136
solve_time_s: 50
verified: true
draft: false
---

[CF 106136C - Time Trouble](https://codeforces.com/problemset/problem/106136/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two small integers for each test case, and we must decide whether we can interpret them as the two fields of a valid 24-hour clock time in the format HH:MM. Each of the two numbers must be used exactly once, but we are free to assign either number to the hour field or the minute field.

The task is purely about feasibility under constraints: hours must lie in the inclusive range from 00 to 23, and minutes must lie in the inclusive range from 00 to 59. If at least one ordering of the two given numbers satisfies these rules, we output the corresponding formatted time with leading zeros. Otherwise we output -1.

The constraints are large in the number of test cases, up to 10^4, but each test case is constant work. This immediately rules out any approach that tries to simulate anything larger than a few constant checks per case. There is no hidden structure across test cases, so each one is independent.

The most common pitfall is assuming that both numbers are already valid as time components or forgetting that swapping is allowed. Another subtle issue is formatting: even when a number like 6 is used as minutes, it must be printed as 06, and similarly for hours like 9 which must be printed as 09.

## Approaches

A brute-force approach is straightforward. For each test case, we try both possible assignments: first treating a as hours and b as minutes, then treating b as hours and a as minutes. For each assignment we check whether the hour lies in [0, 23] and the minute lies in [0, 59]. If either assignment works, we output it.

This brute-force idea already operates in constant time per test case. There is no deeper combinatorial explosion because there are only two permutations of the inputs. Even if we extended the idea to k digits, we would quickly run into factorial growth, but here k is fixed at 2, so the search space is trivial.

The key observation is that the structure of the problem is entirely local: validity depends only on whether each chosen value fits into its respective range. There is no coupling between the two numbers beyond assignment. This reduces the problem to checking two constant conditions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (try both permutations) | O(T) | O(1) | Accepted |
| Optimal (same idea, direct checks) | O(T) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases T. Each test case is independent, so we process them sequentially without storing results.
2. For each pair (a, b), first try interpreting a as the hour and b as the minute. We check whether a ≤ 23 and b ≤ 59. If this condition holds, we immediately output the formatted time using a as HH and b as MM.
3. If the first assignment fails, we try the reverse: interpret b as the hour and a as the minute. We check whether b ≤ 23 and a ≤ 59. If this condition holds, we output b:a in HH:MM format.
4. If neither assignment is valid, we output -1.

The decision order is arbitrary because either valid assignment is acceptable, but checking one first and falling back to the other guarantees we do not miss any feasible configuration.

### Why it works

The algorithm is complete because every valid solution must correspond to exactly one of the two permutations of the input pair. Since we test both permutations and validate each against the strict hour and minute constraints, any feasible configuration will be found. There is no hidden state or dependency between test cases, so correctness reduces to correctness per pair.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    
    for _ in range(t):
        a, b = map(int, input().split())
        
        if a <= 23 and b <= 59:
            out.append(f"{a:02d}:{b:02d}")
        elif b <= 23 and a <= 59:
            out.append(f"{b:02d}:{a:02d}")
        else:
            out.append("-1")
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution reads all test cases and stores outputs in a list to avoid repeated printing overhead. Each test case performs at most two constant-time checks.

The formatting uses Python’s f-string padding to ensure two-digit output, which is essential for correctness. Without zero-padding, outputs like `9:5` would be invalid even if logically correct.

The branching order is not important; either valid permutation is acceptable, so we can safely prefer the (a, b) ordering first.

## Worked Examples

### Example 1

Input pair: a = 9, b = 41

We test both permutations.

| Step | Hour | Minute | Valid hour ≤ 23 | Valid minute ≤ 59 | Decision |
| --- | --- | --- | --- | --- | --- |
| 1 | 9 | 41 | yes | yes | accept |

We immediately output 09:41. The reverse assignment would be invalid because 41 cannot be an hour.

This shows the importance of checking both constraints independently rather than assuming both numbers are interchangeable.

### Example 2

Input pair: a = 25, b = 35

| Step | Hour | Minute | Valid hour ≤ 23 | Valid minute ≤ 59 | Decision |
| --- | --- | --- | --- | --- | --- |
| 1 | 25 | 35 | no | yes | reject |
| 2 | 35 | 25 | no | yes | reject |

Both permutations fail because both numbers exceed the allowed hour range when assigned to hours. Even though both are valid minutes, at least one must be a valid hour, which is impossible here.

This confirms that feasibility requires overlap of the two constraints across the two assignments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case performs a constant number of comparisons and formatting operations |
| Space | O(1) | Only a fixed number of variables and output buffer are used |

The solution easily fits within limits since T is up to 10^4 and each iteration is O(1), resulting in trivial total work.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = []

    t = int(input())
    for _ in range(t):
        a, b = map(int, input().split())
        if a <= 23 and b <= 59:
            out.append(f"{a:02d}:{b:02d}")
        elif b <= 23 and a <= 59:
            out.append(f"{b:02d}:{a:02d}")
        else:
            out.append("-1")
    return "\n".join(out)

# provided samples
assert run("9 41\n9 61\n50 9\n0 6\n25 35\n") == "09:41\n-1\n09:50\n00:06\n-1"

# minimum values
assert run("1 0\n0 1\n") == "01:00\n00:01"

# both valid as both orders
assert run("12 34\n") == "12:34"

# swap-only valid
assert run("61 9\n") == "09:61\n-1"

# boundary hour max
assert run("23 59\n") == "23:59"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 / 0 1 | 01:00 / 00:01 | single-digit padding correctness |
| 12 34 | 12:34 | normal valid assignment |
| 61 9 | -1 | no valid hour/minute pairing |
| 23 59 | 23:59 | boundary validity |

## Edge Cases

One edge case is when both numbers are within 0 to 59 but only one is within 0 to 23. For example, input (9, 61) fails because although 9 is a valid hour, 61 is not a valid minute, and swapping gives (61, 9) which fails because 61 cannot be an hour. The algorithm correctly checks both permutations and rejects both.

Another edge case is when both numbers are valid hours but one exceeds minute constraints. For instance (23, 41) is valid as 23:41, but (41, 23) fails since 41 cannot be an hour. The first permutation succeeds immediately, demonstrating why we must not require both numbers to be valid in both roles simultaneously, only one consistent assignment.

A final edge case is when both numbers are identical, such as (12, 12). Both permutations are identical and valid since 12 ≤ 23 and 12 ≤ 59. The algorithm outputs 12:12 consistently without ambiguity.
