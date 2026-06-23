---
title: "CF 105457C - Schedules"
description: "We are given a list of class schedules, each represented by a start time and an end time on a single circular day that has m discrete hours."
date: "2026-06-23T17:46:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105457
codeforces_index: "C"
codeforces_contest_name: "XXIII Spain Olympiad in Informatics, Online Qualifier 1"
rating: 0
weight: 105457
solve_time_s: 71
verified: true
draft: false
---

[CF 105457C - Schedules](https://codeforces.com/problemset/problem/105457/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of class schedules, each represented by a start time and an end time on a single circular day that has `m` discrete hours. Each class occupies a half-open interval from its start hour to its end hour, and the task is to select as many classes as possible such that no two selected classes overlap in time.

Time is linear from `0` to `m`, so although the interpretation is “hours in a day”, there is no wraparound. The only constraint is that chosen intervals must be pairwise disjoint, and touching at endpoints is allowed since a class ending at time `t` does not overlap with one starting at `t`.

The input may contain multiple independent test cases, each with up to `5 · 10^5` intervals in the hardest version. That scale immediately rules out any solution that compares pairs of intervals or explores subsets. A quadratic or even `O(n log n)` per-test-case solution is still fine, but anything worse than `O(n log n)` overall would fail due to repeated sorting dominating runtime.

A subtle edge case appears when multiple intervals share the same start or end time. For example, consider `m = 2` with intervals `[0, 2]`, `[0, 1]`, `[1, 2]`. The optimal answer is `2`, but a naive strategy that always picks the earliest starting interval might choose `[0, 2]` and block everything else. Another pitfall arises when intervals are nested: `[0, 10]`, `[1, 2]`, `[2, 3]`, where the correct answer is 2, not 1.

These cases show that local greedy decisions based on start time alone are insufficient.

## Approaches

A brute-force approach would try all subsets of intervals and check whether a chosen subset has no overlaps, tracking the maximum size. Checking validity of one subset costs `O(n)` if done naively by sorting or scanning, and there are `2^n` subsets, making this infeasible even for `n = 30`. Another slightly better idea is backtracking with pruning, but worst-case behavior still degenerates into exponential time because intervals can be arranged to avoid early pruning.

The key observation is that the problem has optimal substructure and a greedy choice property if we sort intervals by finishing time. Once we commit to taking the interval that ends earliest among available choices, we maximize remaining free space for future intervals. Any alternative choice that ends later can only restrict or delay future selections without increasing the number of intervals we can fit.

This transforms the problem into a classic interval scheduling maximization problem. Sorting by end time ensures that every step makes the locally optimal choice that leaves maximum flexibility.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Optimal (Greedy) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read all intervals and store them as pairs `(a, b)`. These represent fixed time blocks that must be chosen without overlap.
2. Sort all intervals by their ending time `b`. The reason for this ordering is that choosing earlier-finishing intervals preserves the most future availability.
3. Initialize a variable `current_time = 0`, which tracks the earliest time we are free to schedule the next interval.
4. Iterate through intervals in sorted order.
5. For each interval `(a, b)`, if `a >= current_time`, select it and set `current_time = b`. This ensures we never overlap and always commit to the earliest finishing compatible interval.
6. Count how many intervals we selected and output this value.

### Why it works

At every step, we maintain the invariant that `current_time` is the end of the last chosen interval, and all chosen intervals are disjoint and finish as early as possible given the sorting order. When we consider an interval that ends earliest among all remaining candidates, any alternative interval that overlaps it but ends later can only reduce future scheduling space without increasing the number of compatible intervals. This exchange argument guarantees that replacing any optimal solution’s first differing choice with the greedy choice does not reduce the total number of intervals, so repeated application yields an optimal solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    it = iter(sys.stdin.read().strip().split())
    out = []
    
    while True:
        try:
            n = int(next(it))
        except StopIteration:
            break
        m = int(next(it))  # unused, but part of format
        
        intervals = []
        for _ in range(n):
            a = int(next(it))
            b = int(next(it))
            intervals.append((b, a))  # sort by end time
        
        intervals.sort()
        
        current = 0
        ans = 0
        
        for b, a in intervals:
            if a >= current:
                ans += 1
                current = b
        
        out.append(str(ans))
    
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation reads all input at once to avoid overhead from repeated I/O calls, which matters given the total size can reach several hundred thousand intervals.

Intervals are stored as `(end, start)` specifically to allow Python’s default tuple sort to order them by end time first without extra comparator logic. This is both simpler and faster than custom sorting keys in tight loops.

The greedy sweep maintains `current`, representing the end of the last selected interval. The condition `a >= current` enforces non-overlap while still allowing back-to-back scheduling, which is consistent with the problem’s definition.

## Worked Examples

### Example 1

Input:

```
3 2
0 1
0 2
1 2
```

Sorted by end time: `(0,1)`, `(1,2)`, `(2,0)`

| Step | Interval (a,b) | current | Action | ans |
| --- | --- | --- | --- | --- |
| 1 | (0,1) | 0 | take | 1 |
| 2 | (1,2) | 1 | take | 2 |
| 3 | (0,2) | 2 | skip | 2 |

The trace shows that selecting early-finishing intervals preserves the ability to take later compatible ones.

### Example 2

Input:

```
4 8
0 1
1 2
3 7
4 7
```

Sorted: `(0,1)`, `(1,2)`, `(3,7)`, `(4,7)`

| Step | Interval (a,b) | current | Action | ans |
| --- | --- | --- | --- | --- |
| 1 | (0,1) | 0 | take | 1 |
| 2 | (1,2) | 1 | take | 2 |
| 3 | (3,7) | 2 | take | 3 |
| 4 | (4,7) | 7 | skip | 3 |

This demonstrates that even when intervals overlap partially, sorting by end time ensures we always keep the schedule as flexible as possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) per test case | Sorting dominates, greedy scan is linear |
| Space | O(n) | Storing intervals |

The constraints allow up to `5 · 10^5` intervals, so a single global `O(n log n)` pass is efficient. The memory footprint is linear and well within limits since we store only pairs of integers.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import deque
    
    input = sys.stdin.readline
    
    data = inp.strip().split()
    it = iter(data)
    out = []
    
    while True:
        try:
            n = int(next(it))
        except StopIteration:
            break
        m = int(next(it))
        intervals = []
        for _ in range(n):
            a = int(next(it))
            b = int(next(it))
            intervals.append((b, a))
        intervals.sort()
        
        cur = 0
        ans = 0
        for b, a in intervals:
            if a >= cur:
                ans += 1
                cur = b
        
        out.append(str(ans))
    
    return "\n".join(out)

# provided samples
assert run("""3 2
0 1
0 2
1 2
2 2
0 1
0 2
4 8
0 1
1 2
3 7
4 7
""") == "2\n1\n3"

# minimum size
assert run("1 10\n0 5\n") == "1"

# all overlapping
assert run("3 10\n0 10\n1 9\n2 8\n") == "1"

# disjoint chain
assert run("3 10\n0 2\n2 4\n4 6\n") == "3"

# identical end times
assert run("3 10\n0 5\n1 5\n2 5\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single interval | 1 | minimal case |
| nested intervals | 1 | dominance of large interval |
| chain intervals | 3 | boundary equality handling |
| identical ends | 1 | correct tie-breaking |

## Edge Cases

A first corner case is when intervals are fully nested. Consider input:

```
3 10
0 10
1 9
2 8
```

The algorithm sorts by end time and selects `(2,8)` first? No, it actually selects `(8,2)` as the earliest end, then rejects the others since they all start before the chosen interval ends. The final answer is `1`, which matches optimal behavior because only one interval can be chosen without overlap in this configuration.

Another edge case is a tight chain of back-to-back intervals:

```
3 10
0 2
2 4
4 6
```

Here each interval starts exactly when the previous ends. The greedy condition `a >= current` allows all of them to be selected. The algorithm processes them in order of increasing end time, updates `current` step by step, and outputs `3`, which is optimal.

A third case involves identical end times:

```
3 10
0 5
1 5
2 5
```

After sorting, all intervals share the same end. The greedy process picks the first one it encounters whose start is valid, then rejects the rest because `current` becomes `5`. The result is `1`, which is correct since all intervals overlap in their entire duration up to time 5.
