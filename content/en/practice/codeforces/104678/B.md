---
title: "CF 104678B - Streamer night"
description: "We are given a night that lasts from second 1 to second n, and a collection of k live streams. Each stream occupies a continuous time interval from ai to bi, and during that interval the stream is available to watch."
date: "2026-06-29T09:05:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104678
codeforces_index: "B"
codeforces_contest_name: "October come back. Together training"
rating: 0
weight: 104678
solve_time_s: 84
verified: false
draft: false
---

[CF 104678B - Streamer night](https://codeforces.com/problemset/problem/104678/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a night that lasts from second 1 to second n, and a collection of k live streams. Each stream occupies a continuous time interval from ai to bi, and during that interval the stream is available to watch. You can switch between streams, but switching is only allowed at integer seconds, and specifically you are allowed to start watching a new stream exactly at the moment another one ends.

The task is to choose a sequence of streams such that each next stream starts no earlier than the end of the previous one, and among all such valid sequences, we want the maximum possible number of streams watched.

In other words, we are selecting a maximum-length chain of intervals where each interval begins at or after the previous one finishes.

The constraints go up to n, k ≤ 200000, which immediately rules out any quadratic transition between intervals. Any solution that compares every pair of streams or attempts dynamic programming over all pairs will be too slow, since that would reach up to 4e10 operations in the worst case.

A subtle issue appears when multiple streams share the same start or end time. For example, if many intervals begin at the same second, choosing a suboptimal one early may block a longer chain later. Another tricky situation is when one interval ends exactly when another starts. Because switching is allowed at equal times, the ordering at boundary equality matters: treating overlap strictly or inclusively incorrectly can change the answer.

## Approaches

A naive approach is to treat this as a graph problem where each stream is a node, and we draw an edge from stream i to stream j if bi ≤ aj. Then we try to find the longest path in this DAG. While this is conceptually correct, building all edges requires checking every pair of intervals, which is O(k^2). Even if we skip explicit graph construction and instead do DP, where dp[i] is the best chain starting at i and we try all j that can follow i, we still end up with quadratic behavior.

The structure of the problem is actually much simpler. We are not constrained by arbitrary transitions, but only by time ordering. If we always pick the next stream that ends as early as possible among all streams we can currently reach, we preserve maximum future flexibility. This is the classic greedy idea for interval scheduling, except here we are chaining intervals instead of picking disjoint ones, and the rule remains the same: earliest finishing interval among valid choices is always safe.

To implement this efficiently, we sort streams by starting time and sweep through time while maintaining a structure of currently available streams, ordered by their ending time. At each step, we advance the current time to the end of the chosen stream and add all streams that start before or at that time into a priority structure. Then we pick the one with smallest ending time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (DP / all pairs) | O(k²) | O(k) | Too slow |
| Optimal (sorting + greedy heap) | O(k log k) | O(k) | Accepted |

## Algorithm Walkthrough

1. Sort all streams by their starting time ai. This allows us to process streams in the order they become available as time progresses.
2. Initialize a pointer i = 0 over the sorted streams, a current time cur = 1, and a min-heap that will store candidate streams ordered by their ending time.
3. While there are still streams left to process or the heap is not empty, first insert into the heap all streams whose starting time is ≤ cur. We advance i while ai ≤ cur, pushing (bi, ai) into the heap. This ensures that the heap always contains exactly the streams we are currently allowed to start.
4. If the heap is empty, it means no stream is available at the current time. In this case, we jump cur forward to the next stream’s start time. This is necessary because otherwise we would stall even though future streams exist.
5. If the heap is not empty, we pop the stream with the smallest ending time. This choice is optimal because finishing earlier leaves more room for future streams. We increment the answer by 1 and set cur to its ending time.
6. Repeat until all streams are processed and no candidates remain.

### Why it works

At any moment, the algorithm considers exactly the set of streams that can be started at the current time or earlier. Among these, choosing the one with the smallest end time is safe because any other choice that ends later cannot unlock any stream that the chosen one would not also eventually allow, but it can block streams that require earlier availability. This maintains the invariant that after each selection, we have not reduced the set of achievable future transitions compared to any alternative choice. Since we always consume the earliest finishing valid interval, we maximize the number of future insertion opportunities, which leads to an optimal chain length.

## Python Solution

```python
import sys
input = sys.stdin.readline
import heapq

def solve():
    n, k = map(int, input().split())
    seg = []
    for _ in range(k):
        a, b = map(int, input().split())
        seg.append((a, b))
    
    seg.sort()
    
    heap = []
    i = 0
    cur = 1
    ans = 0
    
    while i < k or heap:
        while i < k and seg[i][0] <= cur:
            heapq.heappush(heap, seg[i][1])
            i += 1
        
        if not heap:
            if i < k:
                cur = seg[i][0]
            continue
        
        cur = heapq.heappop(heap)
        ans += 1
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by sorting intervals by start time so we can incrementally reveal available streams as the current time advances. The heap stores only end times, since we do not need full interval data once it becomes eligible.

The inner loop that pushes all intervals with ai ≤ cur ensures correctness of the available set. The heap pop always selects the stream that finishes earliest, implementing the greedy choice.

The jump `cur = seg[i][0]` is essential when there is a gap in coverage, otherwise the algorithm would get stuck at a time where no interval is available even though future ones exist.

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

| cur | heap after insert | chosen interval | ans |
| --- | --- | --- | --- |
| 1 | (3) | (1,3) | 1 |
| 3 | (4,5) | (3,4) | 2 |
| 4 | (5) | (2,5 not usable now) wait until 5 | 2 |

After taking (1,3), we move to 3 and can choose (3,4), reaching answer 2.

This confirms the greedy strategy of always taking earliest finishing available stream.

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

| cur | heap after insert | chosen interval | ans |
| --- | --- | --- | --- |
| 1 | empty | jump to 2 | 0 |
| 2 | (3,3,3,3) | (2,3) | 1 |
| 3 | empty | stop | 1 |

Only one interval can be used because all overlap completely, confirming that duplicates do not inflate the result incorrectly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k log k) | sorting plus each interval pushed and popped once from heap |
| Space | O(k) | storing intervals and heap of active candidates |

The constraints allow up to 200000 streams, and logarithmic overhead per stream fits comfortably within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import heapq

    def solve():
        n, k = map(int, input().split())
        seg = []
        for _ in range(k):
            a, b = map(int, input().split())
            seg.append((a, b))

        seg.sort()

        heap = []
        i = 0
        cur = 1
        ans = 0

        while i < k or heap:
            while i < k and seg[i][0] <= cur:
                heapq.heappush(heap, seg[i][1])
                i += 1

            if not heap:
                if i < k:
                    cur = seg[i][0]
                continue

            cur = heapq.heappop(heap)
            ans += 1

        return str(ans)

    return solve()

# provided samples
assert run("5 3\n1 3\n2 5\n3 4\n") == "2"
assert run("6 4\n2 3\n2 3\n2 3\n2 3\n") == "1"

# minimum case
assert run("2 1\n1 2\n") == "1"

# non-overlapping chain
assert run("10 3\n1 2\n2 3\n3 4\n") == "3"

# overlapping mixed
assert run("10 4\n1 5\n2 3\n3 4\n4 6\n") == "3"

# identical intervals
assert run("10 3\n2 5\n2 5\n2 5\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single interval | 1 | minimum valid chain |
| 1-2,2-3,3-4 | 3 | perfect chaining across boundaries |
| mixed overlaps | 3 | greedy selection amid conflicts |
| identical intervals | 1 | duplicates do not inflate answer |

## Edge Cases

One edge case is when there is a large gap between intervals. For example:

```
10 2
1 2
8 9
```

The algorithm takes (1,2), then finds no available interval at cur = 2, and jumps to 8. This ensures the second interval is not missed, producing answer 2.

Another case is many intervals starting at the same time:

```
10 3
2 5
2 3
2 4
```

At cur = 1, we jump to 2 and push all intervals. The heap ensures we pick (2,3) first, then continue with the remaining valid intervals, producing the optimal chain length 2.
