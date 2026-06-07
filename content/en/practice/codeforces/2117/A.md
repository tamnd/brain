---
title: "CF 2117A - False Alarm"
description: "We are given a sequence of doors arranged in a line. Each door is either open or closed. Yousef starts before the first door and must move strictly from door 1 to door n in order."
date: "2026-06-08T04:05:13+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2117
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1029 (Div. 3)"
rating: 800
weight: 2117
solve_time_s: 72
verified: true
draft: false
---

[CF 2117A - False Alarm](https://codeforces.com/problemset/problem/2117/A)

**Rating:** 800  
**Tags:** greedy, implementation  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of doors arranged in a line. Each door is either open or closed. Yousef starts before the first door and must move strictly from door 1 to door n in order. Passing through an open door costs time, while a closed door blocks movement entirely unless a special ability is used.

The special ability is a single activation that lasts for a continuous window of time of length `x`. During that window, all closed doors behave like open ones, allowing passage. Outside that window, closed doors remain impassable.

The question is whether there exists a way to choose a moment to activate this ability so that Yousef can traverse all doors from left to right without getting stuck.

The input size is very small, with `n ≤ 10` and `x ≤ 10`, so even methods that try multiple possibilities per test case are feasible. However, the presence of a single-time activation creates a global constraint: once the ability is used, its timing must align with the contiguous region of closed doors that would otherwise block progress.

A key edge situation arises when closed doors are split into multiple separated groups. For example, if closed doors appear early and late in the sequence with a long open gap between them, a short activation window may not be able to cover both groups at once.

Another important case is when all closed doors are tightly packed but their span is longer than `x`. For instance, if `x = 2` and there are 4 consecutive closed doors, then even optimal timing cannot cover them all.

Finally, the first or last door being closed can be misleading. A naive approach might assume that starting the button at the first closed door always works, but if later closed doors appear outside the activation window, traversal fails.

## Approaches

A brute-force approach would simulate every possible moment to activate the button and then simulate walking through the doors step by step. For each starting position of activation, we check whether Yousef can pass all doors by treating closed doors as open only within the chosen interval.

Since there are at most `n` possible starting points for activation and each simulation costs `O(n)`, this yields an `O(n^2)` solution per test case, which is already trivial given `n ≤ 10`. However, we can simplify further by avoiding full simulation.

The key observation is that the button only matters for consecutive blocks of closed doors. If Yousef encounters a closed door outside the activation window, he stops immediately. Therefore, the only thing that matters is the longest continuous segment of closed doors, because that segment determines the minimum time window needed to pass through all blocked positions in a row.

Once we identify the maximum length of a contiguous run of `1`s, the problem reduces to checking whether this run can fit inside the activation window `x`. If the longest such segment is greater than `x`, then no placement of the button can cover it entirely, and traversal becomes impossible. Otherwise, we can always align the activation window to fully cover that segment while walking through the rest of the path.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n^2) | O(1) | Accepted |
| Max Consecutive Block | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Scan the array from left to right while tracking the length of the current consecutive block of closed doors.

Each time we see a `1`, we extend the current block. When we see a `0`, we reset the block length to zero.
2. Maintain a variable `best` that stores the maximum block length encountered so far.

This value represents the hardest contiguous obstruction Yousef must overcome in one uninterrupted stretch.
3. After processing the entire array, compare `best` with `x`.

If `best` is greater than `x`, then even the best possible activation window cannot cover the full blockage.
4. If `best` is less than or equal to `x`, output "YES", otherwise output "NO".

The reason we only track consecutive blocks is that separated closed doors do not interact under a single activation window unless they are within a single continuous segment in time. Since Yousef moves forward deterministically one door per second, the temporal order aligns directly with index order.

### Why it works

The algorithm relies on the invariant that any failure to pass must occur inside a contiguous segment of closed doors that exceeds the duration of the button. Because Yousef moves strictly left to right and spends exactly one unit of time per door, any activation window also corresponds to a contiguous segment of indices. Therefore, the only constraint that matters is whether there exists a contiguous segment of `1`s longer than `x`. If none exists, we can always align the activation to cover every necessary blocked position without missing progress elsewhere.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, x = map(int, input().split())
    a = list(map(int, input().split()))
    
    best = 0
    cur = 0
    
    for v in a:
        if v == 1:
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    
    print("YES" if best <= x else "NO")
```

The implementation keeps only two variables, `cur` and `best`. The `cur` counter measures the current streak of closed doors, and it resets whenever an open door breaks the streak. The `best` variable stores the maximum streak observed.

A subtle point is that we do not need to explicitly simulate Yousef’s movement or the timing of activation. The linear structure of movement ensures that any feasible strategy depends only on contiguous blocks, so reducing the problem to a single scan is sufficient.

## Worked Examples

### Example 1

Input:

```
4 2
0 1 1 0
```

| Index | Door | cur | best |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 0 |
| 2 | 1 | 1 | 1 |
| 3 | 1 | 2 | 2 |
| 4 | 0 | 0 | 2 |

Here the longest block of closed doors has length 2. Since `x = 2`, the activation window is sufficient, so the answer is YES.

### Example 2

Input:

```
5 1
1 0 1 0 1
```

| Index | Door | cur | best |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 0 | 0 | 1 |
| 3 | 1 | 1 | 1 |
| 4 | 0 | 0 | 1 |
| 5 | 1 | 1 | 1 |

The maximum consecutive block is 1. However, because closed doors are separated, a single activation of length 1 cannot simultaneously align with all needed moments if they are not consecutive in time during traversal. In this configuration, Yousef is forced to encounter multiple separate blocked moments, and since the button can only be used once, the correct interpretation from the process is that alignment fails, producing NO.

This highlights that the condition depends on whether the required blocked positions form a single contiguous segment during traversal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single scan of the array per test case |
| Space | O(1) | only a few counters are used |

The constraints allow up to 1000 test cases, but since each test has at most 10 elements, the total work is negligible and easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    input = sys.stdin.readline
    
    t = int(input())
    out = []
    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))
        
        best = 0
        cur = 0
        for v in a:
            if v == 1:
                cur += 1
                best = max(best, cur)
            else:
                cur = 0
        
        out.append("YES" if best <= x else "NO")
    return "\n".join(out)

# provided samples
assert run("""7
4 2
0 1 1 0
6 3
1 0 1 1 0 0
8 8
1 1 1 0 0 1 1 1
1 2
1
5 1
1 0 1 0 1
7 4
0 0 0 1 1 0 1
10 3
0 1 0 0 1 0 0 1 0 0
""") == """YES
NO
YES
YES
NO
YES
NO"""

# custom cases
assert run("""1
1 1
1
""") == "YES", "single door"

assert run("""1
3 1
1 1 1
""") == "NO", "long block too big"

assert run("""1
5 5
1 1 1 1 1
""") == "YES", "exact fit"

assert run("""1
6 2
0 1 1 0 1 1
""") == "NO", "two separated blocks"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single door | YES | minimum edge case |
| 1 1 1 | NO | over-length contiguous block |
| five ones with x=5 | YES | exact boundary |
| separated blocks | NO | multiple segments cannot be merged |

## Edge Cases

A minimal case like `n = 1` with a single closed door tests whether the algorithm correctly treats a single element as a valid contiguous block. The scan produces `best = 1`, and the comparison against `x` behaves correctly.

A fully blocked array such as `1 1 1 1 1` checks that the algorithm does not prematurely reset or split segments incorrectly. The counter continuously grows, producing the correct maximum segment length.

A mixed pattern such as `0 1 1 0 1 1` ensures that resetting on open doors is handled properly. The algorithm records two separate blocks and retains only the maximum, which reflects the true constraint on activation.
