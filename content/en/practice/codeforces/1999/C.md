---
title: "CF 1999C - Showering"
description: "We are given a day of length m minutes and a set of non-overlapping tasks, each occupying a continuous interval of time."
date: "2026-06-08T14:20:25+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1999
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 964 (Div. 4)"
rating: 800
weight: 1999
solve_time_s: 139
verified: true
draft: false
---

[CF 1999C - Showering](https://codeforces.com/problemset/problem/1999/C)

**Rating:** 800  
**Tags:** greedy, implementation  
**Solve time:** 2m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a day of length `m` minutes and a set of non-overlapping tasks, each occupying a continuous interval of time. Alex wants to shower for `s` minutes, and we need to determine whether there exists at least one contiguous block of time of length `s` that does not intersect any of the scheduled tasks. The input consists of multiple test cases, each with its own list of tasks and parameters `n`, `s`, and `m`. The output is a simple "YES" if such a block exists and "NO" otherwise.

The constraints allow up to `2 * 10^5` tasks across all test cases, and each day can be up to `10^9` minutes long. Because of this, any solution iterating over every minute of the day would be far too slow. We need an approach that works linearly in the number of tasks for each test case.

An edge case to consider is when a free block exists either at the very start of the day before the first task or at the end after the last task. For example, if `s = 3`, `m = 10`, and the only task is `(5, 7)`, the interval `(0, 5)` is long enough for a shower, and so is `(7, 10)`. A careless implementation that only checks gaps between consecutive tasks may miss these start and end intervals. Another subtle case is when `s` exactly equals a gap length; off-by-one errors often appear here, so the inequality must be `>= s`.

## Approaches

A brute-force approach would consider every minute of the day and check whether a block of length `s` is free. For each starting minute `t`, we would verify if `[t, t+s)` overlaps any task interval. This is correct logically but can require up to `10^9` checks in the worst case, which is far beyond feasible limits.

The key observation is that tasks are non-overlapping and sorted by start time. Therefore, it suffices to only check the gaps between consecutive tasks, as well as the start of the day before the first task and the end of the day after the last task. Each gap is defined by the end of one task and the start of the next. If any gap is at least `s` minutes long, Alex can shower. This reduces the problem to a linear scan over `n` intervals, making the complexity `O(n)` per test case. This approach is simple, fast, and handles all edge cases naturally.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m * n) | O(n) | Too slow |
| Optimal | O(n) | O(1) per test case | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`. For each test case, read `n`, `s`, and `m`.
2. Read all `n` tasks and store them as pairs `(l_i, r_i)`.
3. Check the interval before the first task. If the first task starts at `l_1`, and `l_1 >= s`, output "YES".
4. Iterate through consecutive tasks. For tasks `i` and `i+1`, calculate the gap `l_{i+1} - r_i`. If this gap is `>= s`, output "YES".
5. Check the interval after the last task. If the last task ends at `r_n`, and `m - r_n >= s`, output "YES".
6. If none of these checks succeeded, output "NO".

Why it works: The tasks are non-overlapping and sorted. All possible locations for a shower are either before the first task, between two tasks, or after the last task. By checking each of these intervals for length `>= s`, we cover all possibilities without missing any valid window.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_shower(n, s, m, tasks):
    if tasks[0][0] >= s:
        return True
    for i in range(n - 1):
        if tasks[i+1][0] - tasks[i][1] >= s:
            return True
    if m - tasks[-1][1] >= s:
        return True
    return False

t = int(input())
for _ in range(t):
    n, s, m = map(int, input().split())
    tasks = [tuple(map(int, input().split())) for _ in range(n)]
    print("YES" if can_shower(n, s, m, tasks) else "NO")
```

The function `can_shower` handles the core logic. We check the start-of-day gap first, then the gaps between tasks, and finally the end-of-day gap. This order ensures we return "YES" at the first possible interval, avoiding unnecessary computations. Using tuples and direct arithmetic keeps the solution simple and efficient. We avoid off-by-one errors by carefully using `>= s`.

## Worked Examples

Sample input:

```
3 3 10
3 5
6 8
9 10
```

| Step | Interval checked | Gap length | Result |
| --- | --- | --- | --- |
| Before first task | 0-3 | 3 | YES |

We see the first task starts at 3 and `3 >= s`, so Alex can shower immediately. No further checks needed.

Second input:

```
3 3 10
1 2
3 5
6 8
```

| Step | Interval checked | Gap length | Result |
| --- | --- | --- | --- |
| Before first task | 0-1 | 1 | NO |
| Between tasks 1 & 2 | 3-2 | -1 | NO |
| Between tasks 2 & 3 | 6-5 | 1 | NO |
| After last task | 8-10 | 2 | NO |

Here, all gaps are shorter than 3 minutes, so output is NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We scan tasks once and compute gaps between consecutive tasks. |
| Space | O(n) per test case | We store task intervals as a list of tuples. |

With the sum of `n` across all test cases ≤ 2*10^5, this is well within the 2-second time limit. Memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # solution
    t = int(input())
    for _ in range(t):
        n, s, m = map(int, input().split())
        tasks = [tuple(map(int, input().split())) for _ in range(n)]
        if tasks[0][0] >= s:
            print("YES")
            continue
        for i in range(n - 1):
            if tasks[i+1][0] - tasks[i][1] >= s:
                print("YES")
                break
        else:
            if m - tasks[-1][1] >= s:
                print("YES")
            else:
                print("NO")
    return output.getvalue().strip()

# provided samples
assert run("4\n3 3 10\n3 5\n6 8\n9 10\n3 3 10\n1 2\n3 5\n6 7\n3 3 10\n1 2\n3 5\n6 8\n3 4 10\n1 2\n6 7\n8 9\n") == "YES\nYES\nNO\nYES"

# custom tests
assert run("1\n1 5 10\n0 4\n") == "YES", "start-of-day gap"
assert run("1\n2 2 5\n0 2\n3 5\n") == "NO", "no valid gaps"
assert run("1\n3 1 10\n0 1\n2 3\n4 5\n") == "YES", "tiny gaps suffice"
assert run("1\n2 3 6\n0 2\n3 4\n") == "NO", "end-of-day insufficient"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 task at start | YES | Correctly handles gap before first task |
| Two tasks with full coverage | NO | Correctly detects no free interval |
| Multiple tiny gaps | YES | Correctly handles minimal gaps sufficient for shower |
| End-of-day gap too short | NO | Correctly evaluates gap after last task |

## Edge Cases

If the first task starts at exactly `s`, the algorithm will return "YES" immediately because the interval `[0, l_1)` has length `l_1 >= s`. If the only gap occurs after the last task, the final check `m - r_n >= s` captures it. Negative or zero-length gaps cannot occur due to the input guarantee that `l_i > r_{i-1}`, but we still use `>= s` to avoid off-by-one errors. This guarantees correctness even at boundaries.
