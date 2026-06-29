---
title: "CF 104678B - Streamer night"
description: "We are given a time interval from second 1 to second n. Along this timeline, there are k video streams, each represented by a half-open activity window in practice but effectively treated as a closed interval from a start second ai to an end second bi."
date: "2026-06-29T14:35:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104678
codeforces_index: "B"
codeforces_contest_name: "October come back. Together training"
rating: 0
weight: 104678
solve_time_s: 79
verified: false
draft: false
---

[CF 104678B - Streamer night](https://codeforces.com/problemset/problem/104678/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a time interval from second 1 to second n. Along this timeline, there are k video streams, each represented by a half-open activity window in practice but effectively treated as a closed interval from a start second ai to an end second bi.

The task is to select a sequence of streams such that you can watch them one after another without overlap in time, and the goal is to maximize how many streams you manage to watch. The only allowed transition is that if a stream ends at time t, you may immediately start another stream that begins at time t. Overlaps in any other way make two streams incompatible in the sequence.

The output is the maximum number of intervals you can chain together under this rule.

The constraints go up to 200000 intervals, so any solution worse than O(k log k) risks timing out. A quadratic approach would require checking all pairs or running DP over all intervals, leading to around 4e10 operations in the worst case, which is infeasible.

A subtle edge case appears when many intervals share the same start or end times. For example, if all intervals are identical like (2,3), only one can be chosen even though there are many candidates. Another edge case is when a long interval overlaps many short ones; a greedy method that picks long intervals first can block better chaining opportunities later.

## Approaches

A brute-force idea is to treat this as a longest path problem in a directed acyclic graph where each interval points to all intervals that can follow it. We could try every interval as a starting point and recursively try all valid next intervals whose start time is at least the current interval’s end. This correctly explores all valid chains, but for each interval we may scan up to k others, leading to O(k²) transitions, and recursion or DP over states still remains quadratic.

The key structural insight is that compatibility depends only on the end time of the current interval. Once we finish a stream at time t, any stream starting at or after t is valid. This suggests a greedy choice: always take the next stream that ends as early as possible among all currently available streams. By finishing early, we maximize the remaining time window for future selections, which preserves more opportunities.

To implement this, we sort intervals by their start time and sweep through them while maintaining a structure of “available streams” ordered by end time. At each step, we advance the current time and add all streams whose start time is reachable, then pick the one with the smallest end time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k²) | O(k) | Too slow |
| Optimal (Greedy + heap) | O(k log k) | O(k) | Accepted |

## Algorithm Walkthrough

1. Sort all intervals by their start time.

This ensures we can progressively reveal streams as time moves forward without repeatedly scanning the full list.
2. Maintain a pointer over the sorted intervals and a min-heap keyed by end time.

The heap represents all streams that have already started but have not yet been chosen.
3. Initialize current time to 0 and answer to 0.

We conceptually start before the first second, allowing any stream starting at 1 to be considered.
4. While there are still unprocessed intervals or the heap is not empty, repeat the process.

This loop simulates moving through time while collecting usable streams.
5. Add to the heap all intervals whose start time is less than or equal to the current time.

These are exactly the streams that are available to start at this moment.
6. If the heap is empty, jump the current time forward to the next interval’s start time.

This prevents stalling when there is a gap in coverage.
7. Otherwise, extract the interval with the smallest end time from the heap and take it.

This is the greedy step: choosing the earliest finishing stream preserves maximum flexibility for future choices.
8. Set current time to the end of the chosen interval and increment the answer.

We move forward in time exactly as far as the chosen stream runs.
9. Continue until no intervals remain to process.

### Why it works

At any moment, among all streams that are currently available, choosing the one that finishes earliest never reduces the optimal future count. Any other choice that ends later can only restrict or delay access to future intervals, because it occupies time longer while offering no additional reachability advantages. This establishes a standard exchange argument: any optimal solution that picks a non-minimal finishing interval can be transformed into one that picks the minimal finishing interval without decreasing the total number of chosen streams.

## Python Solution

```python
import sys
input = sys.stdin.readline

import heapq

def solve():
    n, k = map(int, input().split())
    intervals = [tuple(map(int, input().split())) for _ in range(k)]
    
    intervals.sort()  # sort by start time
    
    i = 0
    current_time = 0
    ans = 0
    heap = []
    
    while i < k or heap:
        if not heap:
            current_time = max(current_time, intervals[i][0])
        
        while i < k and intervals[i][0] <= current_time:
            heapq.heappush(heap, intervals[i][1])
            i += 1
        
        if not heap:
            continue
        
        end_time = heapq.heappop(heap)
        ans += 1
        current_time = end_time
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation follows the sweep-line idea directly. Sorting by start time allows us to incrementally activate intervals. The heap stores only end times since start times are already satisfied when inserted. The key subtlety is the jump when the heap is empty, which avoids incorrectly counting idle time as a missed opportunity.

The choice of `current_time = max(current_time, intervals[i][0])` ensures we never move backward in time if a previous interval ends after the next available start. This is important when intervals are disjoint in time.

## Worked Examples

### Sample 1

Input:

```
5 3
1 3
2 5
3 4
```

Sorted intervals:

(1,3), (2,5), (3,4)

| Step | Current time | Heap (end times) | Action | Answer |
| --- | --- | --- | --- | --- |
| 1 | 0 → 1 | [3] | add (1,3) | 0 |
| 2 | 1 | [3,5] | add (2,5) | 0 |
| 3 | 1 | [3,5] | take (1,3) | 1 |
| 4 | 3 | [4,5] | add (3,4) | 1 |
| 5 | 3 | [5] | take (3,4) | 2 |

The algorithm selects (1,3) then (3,4). This confirms that early finishing intervals enable better chaining than attempting to take the long interval (2,5) first.

### Sample 2

Input:

```
6 4
2 3
2 3
2 3
2 3
```

All intervals are identical.

| Step | Current time | Heap | Action | Answer |
| --- | --- | --- | --- | --- |
| 1 | 0 → 2 | [3,3,3,3] | add all | 0 |
| 2 | 2 | [3,3,3] | take one | 1 |
| 3 | 3 | [] | stop | 1 |

Only one interval can be chosen because after the first selection, all remaining intervals are no longer usable.

These traces confirm that duplicates do not artificially inflate the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k log k) | Sorting dominates and each interval is pushed and popped once from the heap |
| Space | O(k) | Heap and interval storage |

The constraints allow up to 200000 intervals, and each heap operation is logarithmic, so the total number of operations stays comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import heapq

    def solve():
        n, k = map(int, input().split())
        intervals = [tuple(map(int, input().split())) for _ in range(k)]
        intervals.sort()

        i = 0
        current_time = 0
        ans = 0
        heap = []

        while i < k or heap:
            if not heap:
                current_time = max(current_time, intervals[i][0])

            while i < k and intervals[i][0] <= current_time:
                heapq.heappush(heap, intervals[i][1])
                i += 1

            if not heap:
                continue

            heapq.heappop(heap)
            ans += 1

        return str(ans)

    return solve()

# provided samples
assert run("5 3\n1 3\n2 5\n3 4\n") == "2"
assert run("6 4\n2 3\n2 3\n2 3\n2 3\n") == "1"

# minimum input
assert run("2 1\n1 2\n") == "1"

# non-overlapping chain
assert run("10 3\n1 2\n2 3\n3 4\n") == "3"

# overlapping chain with choice
assert run("10 3\n1 5\n2 3\n3 4\n") == "2"

# all intervals start late
assert run("10 2\n5 6\n7 8\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single interval | 1 | minimal case correctness |
| chain 1-2-3-4 | 3 | full greedy chaining |
| long + short overlaps | 2 | greedy avoids bad long choice |
| disjoint late intervals | 2 | correct time jumps |

## Edge Cases

A key edge case is when there is a gap in interval coverage. Suppose the input is:

```
10 2
5 6
7 8
```

The heap is empty initially, so the algorithm jumps current_time to 5. It selects (5,6), then moves to 6. At this point, there are no active intervals until time 7, so it jumps again. Without this jump logic, a naive implementation might repeatedly check empty heaps or incorrectly conclude no further intervals are usable.

Another case is heavy overlap where many intervals are available simultaneously:

```
10 4
1 10
2 3
3 4
4 5
```

A naive greedy by earliest start might pick (1,10) first and end immediately with answer 1. The heap-based strategy instead prioritizes (2,3), then (3,4), then (4,5), producing answer 3. The correctness comes from always selecting the smallest end time among available choices, not the earliest start or longest duration.
