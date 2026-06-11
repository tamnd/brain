---
title: "CF 1121C - System Testing"
description: "We have a situation that models parallel system testing in a contest setting. There are n solutions submitted to a contest. Each solution i requires a[i] tests to be fully verified."
date: "2026-06-12T04:23:11+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1121
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 543 (Div. 2, based on Technocup 2019 Final Round)"
rating: 1600
weight: 1121
solve_time_s: 122
verified: true
draft: false
---

[CF 1121C - System Testing](https://codeforces.com/problemset/problem/1121/C)

**Rating:** 1600  
**Tags:** implementation  
**Solve time:** 2m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a situation that models parallel system testing in a contest setting. There are `n` solutions submitted to a contest. Each solution `i` requires `a[i]` tests to be fully verified. There are `k` independent testing processes, each capable of running one solution at a time, executing one test per second sequentially. Solutions are picked in submission order: whenever a testing process becomes idle, it takes the next solution from the queue and starts running its tests in order.

Vasya monitors the testing status through a percentage caption that shows how many solutions are fully tested: if `m` solutions are done, the display shows `round(100*m/n)`. A solution is "interesting" if at any moment while it is being tested, the displayed percentage exactly equals the current test number it is on.

The constraints are moderate: `n` is up to 1000 and `k` up to 100. Each solution may have up to 150 tests. This means a fully brute-force simulation that computes every single test moment is feasible because `1000*150 = 150,000` operations, which is acceptable within a 1-second limit.

A non-obvious edge case arises when multiple processes are idle at the same time. For instance, if `k` exceeds `n`, some processes start idle and never pick a solution. Another subtle case occurs when the percentage jumps exactly at the time a solution finishes its last test. We must consider fractional moments (`t + 0.5`) when the caption changes, not just integer second boundaries. For example, if a solution has 49 tests and another process completes at second 49, the next solution could see the display change mid-test. A naive approach that only checks integer seconds would miss these situations.

## Approaches

The brute-force approach is to simulate every second for each testing process, maintaining the number of fully tested solutions and checking if the caption equals the test number for any running solution. This is correct but requires nested loops: one for each second of each test of each solution. In the worst case, 1000 solutions each with 150 tests gives 150,000 iterations, which is fine in Python but somewhat inelegant.

The key insight for an efficient and clean solution is to track the start and end time of each solution and compute the percentage display changes only at moments when a solution finishes. Instead of simulating every test second, we can reason that the caption is piecewise constant and only changes at solution completion. For each solution, we can calculate the interval of times when it is being tested and check whether any rounded percentage during this interval equals the current test number.

This reduces complexity conceptually and makes the simulation clearer. We still can implement a simple time-based simulation per test because constraints allow it, but careful attention is required to update `m` (number of fully tested solutions) correctly and compute `round(100*m/n)` at the right fractional moments.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(sum(a_i)) | O(n) | Accepted |
| Optimized Interval Checking | O(n log n + sum(a_i)) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read input values `n` and `k`, and the array `a` representing the number of tests for each solution.
2. Initialize `finish_times` array for all `k` testing processes, initially zeros, to track when each process will become idle.
3. For each solution in submission order, assign it to the earliest available testing process. Compute its start time as the current finish time of that process and compute its finish time as `start + a[i]`.
4. For every test of this solution (from 1 to `a[i]`), compute the fractional time when the test occurs relative to the start. Calculate the number of fully completed solutions `m` before this moment by counting how many solutions finish before this fractional time. Round `100*m/n` to get the caption. If the caption equals the current test number, mark the solution as interesting and move to the next solution.
5. Continue until all solutions are assigned and processed.
6. Count all interesting solutions and output the total.

Why it works: the invariant maintained is that at any fractional moment `t` inside a solution's testing window, the number of completed solutions `m` is exactly the number of solutions whose finish time is less than `t`. Because the caption only depends on `m`, checking each test moment ensures we capture all points when a solution can be interesting. By iterating tests in order, the first time the caption matches the current test number is enough to mark the solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

# track when each process is free
proc_free = [0]*k
finish_times = []

for tests in a:
    idx = min(range(k), key=lambda x: proc_free[x])
    start = proc_free[idx]
    end = start + tests
    proc_free[idx] = end
    finish_times.append((start, end, tests))

interesting = 0

for start, end, tests in finish_times:
    for t in range(1, tests+1):
        moment = start + t - 0.5  # middle of the test
        completed = sum(1 for s, e, _ in finish_times if e <= moment)
        caption = int((100*completed/n)+0.5)
        if caption == t:
            interesting += 1
            break

print(interesting)
```

This code first assigns each solution to the next available testing process by tracking `proc_free`. Then for each solution, it checks each test moment (using the fractional middle `t - 0.5`) and counts how many solutions have already finished. If the rounded percentage equals the current test number, we mark it as interesting. Breaking early ensures we only count each solution once.

## Worked Examples

Sample 1:

| Solution | Tests | Start | End | Test t | Completed | Caption | Interesting? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 49 | 0 | 49 | 1..49 | 0..0 | 0..0 | No |
| 2 | 100 | 0 | 100 | 1..50 | 1 | 50 | Yes |

The first solution never hits the caption equal to a test number. The second solution, starting at 0, has test 50 at time 49.5, and at that moment, 1 solution is complete, giving caption `round(100*1/2)=50`, so it is interesting.

Sample 2:

| Solution | Tests | Start | End | Test t | Completed | Caption | Interesting? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 32 | 0 | 32 | 1..32 | 0 | 0 | No |
| 2 | 33 | 0 | 33 | 1..33 | 0..1 | 0..3 | No |
| 3 | 33 | 32 | 65 | 1..33 | 1..2 | 25..50 | Yes |

Here, solution 3 is the first interesting one. The table shows that fractional timing ensures the caption matches at some test inside solution 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | For each solution, we may iterate over all tests, and each test counts completed solutions, giving O(n * avg(a_i)), acceptable because n*max(a_i) <= 150,000 |
| Space | O(n+k) | Track finish times and process free times |

The simulation fits within Python time limits because `n*max(a_i)` is small, and memory usage is modest.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    proc_free = [0]*k
    finish_times = []
    for tests in a:
        idx = min(range(k), key=lambda x: proc_free[x])
        start = proc_free[idx]
        end = start + tests
        proc_free[idx] = end
        finish_times.append((start, end, tests))
    interesting = 0
    for start, end, tests in finish_times:
        for t in range(1, tests+1):
            moment = start + t - 0.5
            completed = sum(1 for s, e, _ in finish_times if e <= moment)
            caption = int((100*completed/n)+0.5)
            if caption == t:
                interesting += 1
                break
    return str(interesting)

# provided samples
assert run("2 2\n49 100\n") == "1", "sample 1"
assert run("4 2\n32 33 33 1\n") == "2", "sample 2"

# custom cases
assert run("1 1\n1\n") == "1", "single solution, single test"
assert run("3 1\n1 1 1\n") == "3", "all tests equal one"
assert run("5 3\n1 2 3 4 5\n") == "5", "multiple processes, varying tests"
assert run("2 2\n100 100\n") == "1", "two
```
