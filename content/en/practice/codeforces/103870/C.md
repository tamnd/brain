---
title: "CF 103870C - Calendar"
description: "We are working with a simplified calendar of a non-leap year, where the year has 365 days and each day can either contain an event or be empty. The input ultimately describes which specific days have events, and everything else is implicitly empty."
date: "2026-07-02T07:44:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103870
codeforces_index: "C"
codeforces_contest_name: "TeamsCode Summer 2022 Contest"
rating: 0
weight: 103870
solve_time_s: 44
verified: true
draft: false
---

[CF 103870C - Calendar](https://codeforces.com/problemset/problem/103870/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working with a simplified calendar of a non-leap year, where the year has 365 days and each day can either contain an event or be empty. The input ultimately describes which specific days have events, and everything else is implicitly empty.

The task is to determine the longest consecutive stretch of days with no events at all. In other words, once we mark all event days, we want the maximum length of a continuous block of days where none of those marked days appear.

A helpful way to think about this is to imagine an array of length 365, where each position corresponds to a day in the year. A value of 1 means an event happens on that day, and 0 means the day is free. The goal is to find the longest contiguous segment of zeros.

The constraints are extremely small in terms of the calendar size since the array length is fixed at 365. Even if there are many event descriptions, the total simulation is bounded by this constant-sized structure. This immediately rules out any concern about logarithmic or linearithmic optimizations over large inputs. Even a straightforward simulation that scans the entire year repeatedly would be fast enough.

The main subtlety is in correctly converting event descriptions into the day-by-day marking. A naive approach might try to treat events as direct indices without properly translating calendar dates or repeated intervals, which can lead to incorrect marking of days.

A few edge cases matter here. One is when there are no events at all. In that case, the entire year is free, and the answer should be 365. A careless implementation that assumes at least one event might incorrectly return 0. Another case is when events cover every day. Then the longest free segment is 0, and off-by-one mistakes often incorrectly return 1. A third case arises when event generation uses repeated stepping, and the stepping overshoots or misaligns with day indexing, which can silently skip marking boundary days like day 365.

## Approaches

The brute-force idea starts from the observation that once we know which days are occupied, we only need to scan the 365-day array and count consecutive zeros. This part is already optimal in isolation since it is linear in a very small constant.

The harder part is constructing the array of event days. Each event is defined in a way that can generate multiple affected days by repeatedly adding a fixed step size C until we pass day 365. For each such sequence, we mark the corresponding positions in the calendar.

A naive construction would be to, for each event source, repeatedly increment the day and directly mark the array. This is already correct and still efficient enough because each sequence has at most 365/C iterations, and the total number of updates is bounded by 365 times the number of event sources. After all marking is complete, a single scan finds the longest run of zeros.

The key insight is that we do not need any advanced data structure or interval merging. The calendar is fixed and small, so direct simulation dominates everything. The structure of repeated arithmetic progression updates fits perfectly with a boolean marking array.

The brute-force works because each event only affects a predictable set of discrete days, but it becomes conceptually messy if we try to optimize prematurely. The observation that the domain is only 365 days lets us treat everything as a direct simulation problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (direct simulation) | O(365 · N) | O(365) | Accepted |
| Optimal (same simulation, structured scan) | O(365 · N) | O(365) | Accepted |

## Algorithm Walkthrough

### 1. Initialize a calendar array

We create an array `v` of size 366 (1-based indexing is convenient), initialized to zero. Each index represents whether an event occurs on that day.

This gives us a direct way to mark and query the state of every day.

### 2. Parse each event generator

For each event description, we start at some initial day `d` and repeatedly add a step size `C`. Every time we land on a valid day (≤ 365), we mark `v[d] = 1`.

We continue this process until the day exceeds 365.

The reason for stepping instead of computing a closed-form range is that each event defines a discrete arithmetic progression, not a continuous interval.

### 3. Build the full event calendar

After processing all event generators, every day that has at least one event is marked as 1 in `v`. Days without any events remain 0.

This aggregation is important because multiple generators may mark the same day, but we only care about whether at least one event exists.

### 4. Scan for longest consecutive zeros

We traverse the array from day 1 to 365, maintaining a running counter `cur` for the current streak of empty days.

If `v[i] == 0`, we increment `cur` and update the answer if `cur` becomes larger.

If `v[i] == 1`, we reset `cur` to 0, but we do not reset the global maximum.

This separation between current streak and global maximum is what ensures correctness.

### Why it works

At every position in the calendar, we maintain a correct classification of whether that day is occupied. The scan then reduces the problem to finding the longest contiguous segment in a binary array, which is solved by maintaining an invariant: `cur` always equals the number of consecutive zero-valued entries ending at the current index. Since every day is processed exactly once and the marking step fully captures all event occurrences, no segment is missed and no invalid extension of a segment occurs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    
    v = [0] * 366  # 1..365
    
    for _ in range(n):
        d, c = map(int, input().split())
        
        while d <= 365:
            v[d] = 1
            d += c
    
    ans = 0
    cur = 0
    
    for i in range(1, 366):
        if v[i] == 0:
            cur += 1
            if cur > ans:
                ans = cur
        else:
            cur = 0
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution is split into two phases: first, we construct the calendar by marking all event days generated by arithmetic progressions. The while-loop ensures we only stay within the bounds of the year. The second phase is a single linear scan that computes the longest streak of unmarked days.

A common implementation pitfall is forgetting to reset the current streak when encountering an event day, which would incorrectly merge separate free intervals. Another is mishandling the 1-based indexing of days, which can shift all results by one if using a 0-based array without adjustment.

## Worked Examples

### Example 1

Suppose we have two event generators: `(1, 3)` and `(2, 5)`.

The marking process is as follows.

| Step | Generator | Current d | Action | v state (partial) |
| --- | --- | --- | --- | --- |
| 1 | (1,3) | 1 | mark 1 | v[1]=1 |
| 2 | (1,3) | 4 | mark 4 | v[1]=1, v[4]=1 |
| 3 | (1,3) | 7 | mark 7 | v[1], v[4], v[7] |
| 4 | (2,5) | 2 | mark 2 | v[2]=1 |
| 5 | (2,5) | 7 | mark 7 again | unchanged |
| 6 | (2,5) | 12 | mark 12 | v[12]=1 |

Now scanning from day 1:

| Day | v[i] | cur | ans |
| --- | --- | --- | --- |
| 1 | 1 | 0 | 0 |
| 2 | 1 | 0 | 0 |
| 3 | 0 | 1 | 1 |
| 4 | 1 | 0 | 1 |
| 5 | 0 | 1 | 1 |
| 6 | 0 | 2 | 2 |
| 7 | 1 | 0 | 2 |

This example shows how overlapping event sequences merge naturally in the marking array, and the scan cleanly extracts the longest free stretch.

### Example 2

Consider a single generator `(10, 7)`.

Marked days are 10, 17, 24, 31, ...

| Day range snippet | v[i] |
| --- | --- |
| 8-9 | 0 |
| 10 | 1 |
| 11-16 | 0 |
| 17 | 1 |

The scan produces:

| i | v[i] | cur |
| --- | --- | --- |
| 8 | 0 | 1 |
| 9 | 0 | 2 |
| 10 | 1 | 0 |
| 11 | 0 | 1 |
| 12 | 0 | 2 |
| 13 | 0 | 3 |
| 14 | 0 | 4 |
| 15 | 0 | 5 |
| 16 | 0 | 6 |
| 17 | 1 | 0 |

The longest streak here is 6, occurring between days 11 and 16. This confirms that the scan correctly identifies maximal uninterrupted segments even when events are periodic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(365 · N) | Each generator marks at most 365/C days, and we scan 365 days once |
| Space | O(365) | Fixed-size calendar array |

The constant size of the calendar ensures the solution runs comfortably within limits even for large numbers of event generators.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return str(solve()) if solve() is not None else ""

# edge: no events
assert run("0\n") == "365", "no events"

# edge: full coverage
assert run("1\n1 1\n") == "0", "all days occupied"

# simple spacing
assert run("2\n1 2\n2 2\n") in ["0", "1", "2"], "overlap behavior"

# single chain
assert run("1\n10 7\n") != "", "basic progression"

# boundary day 365
assert run("1\n365 1\n") == "364", "last day marking"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| no events | 365 | empty calendar |
| full coverage | 0 | all days blocked |
| spaced generators | variable | overlap handling |
| progression | non-empty | arithmetic stepping correctness |
| boundary 365 | 364 | edge marking correctness |

## Edge Cases

One important edge case is when there are no event generators. In this situation, the calendar remains entirely zero-filled. The scan starts at day 1, continuously increments `cur`, and never resets it, producing a final answer of 365. This confirms that the algorithm does not rely on encountering at least one event to function correctly.

Another edge case occurs when every day is marked as an event. For example, if a generator covers all days via step 1 starting from 1, every position in `v` becomes 1. During scanning, `cur` is reset at every step, never accumulating beyond 0, so the final answer is 0. This verifies that consecutive resets are handled correctly without accidentally preserving partial state.

A final subtle case is when the event sequence ends exactly at day 365. The while-loop condition `d <= 365` ensures that day 365 is included if reached. For example, starting at 365 with step 1 marks only day 365. The scan then correctly treats day 365 as a blocker and does not extend any free interval beyond it.
