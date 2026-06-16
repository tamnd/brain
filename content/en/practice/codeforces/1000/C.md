---
title: "CF 1000C - Covered Points Count"
description: "We are given a collection of segments on a very large number line. Each segment covers every integer point between its endpoints, including both ends. Different segments may overlap in arbitrary ways: they can be disjoint, nested, identical, or partially intersecting."
date: "2026-06-16T23:47:25+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1000
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 46 (Rated for Div. 2)"
rating: 1700
weight: 1000
solve_time_s: 74
verified: true
draft: false
---

[CF 1000C - Covered Points Count](https://codeforces.com/problemset/problem/1000/C)

**Rating:** 1700  
**Tags:** data structures, implementation, sortings  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of segments on a very large number line. Each segment covers every integer point between its endpoints, including both ends. Different segments may overlap in arbitrary ways: they can be disjoint, nested, identical, or partially intersecting.

The task is not to find the coverage at a single point, but to understand the global distribution of coverage. For every possible value of k, we need to compute how many integer positions are covered by exactly k segments.

In other words, if we imagine sweeping along the number line and, at every integer coordinate, counting how many segments currently cover it, we want to know how many coordinates produce count 1, how many produce count 2, and so on up to n.

The constraints are what force the design choice. With up to 200,000 segments and endpoints as large as 10^18, we cannot afford to inspect every integer point explicitly. Any approach that iterates over coordinates is immediately infeasible because the coordinate space is effectively unbounded at this scale. We need to reason in terms of changes in coverage rather than individual points.

A common failure mode comes from trying to simulate coverage per point or per unit interval without compressing coordinates. For example, with segments [0, 3], [1, 3], [3, 8], a naive sweep over every integer would work on this tiny input but would be impossible if intervals stretch to 10^18. Another subtle mistake is treating intervals as half-open inconsistently. Since endpoints are inclusive, the coverage changes exactly at l and at r + 1, not at r.

## Approaches

A brute-force idea is straightforward: for each integer coordinate that lies inside at least one segment, count how many segments cover it, then increment a frequency array indexed by that count. Conceptually, for each segment we mark all points it covers and maintain a global counter per point.

This works logically but breaks immediately on performance. A single segment can span up to 10^18 integers, so even one interval may require impossible work. Even if we try to restrict ourselves only to observed endpoints, we still face the issue that coverage is constant only between event points, not necessarily at them.

The key observation is that the coverage count only changes at segment boundaries. Between two consecutive “event positions” on the number line, the number of active segments is constant. So instead of thinking about every integer point, we compress the problem into intervals where coverage does not change.

This leads to a sweep line idea: we convert each segment into two events, one that increases coverage at l, and one that decreases coverage after r. Sorting these events allows us to process the line in increasing order and maintain the current active segment count. Whenever we move from one event position to the next, the segment count remains fixed across the entire gap, so we can add the length of that gap to the answer for that count.

This reduces the problem from per-point counting to per-interval aggregation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(total covered points) | O(1) to O(n) | Too slow |
| Sweep Line | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We transform each segment into two boundary events, one increasing coverage and one decreasing coverage after the segment ends. We then sort these events by position.

We maintain a running variable `active` representing how many segments currently cover the sweep position. We also iterate through the sorted event positions in order.

1. Convert each segment [l, r] into two events: at l we add +1, and at r + 1 we add -1. This encoding ensures correctness for inclusive intervals because the segment contributes through r, and stops contributing starting at r + 1.
2. Sort all events by their coordinate. Sorting is necessary because we need to process coverage changes in left-to-right order.
3. Initialize `active = 0` and an empty result array `ans` of size n + 1.
4. Iterate through the sorted events while tracking the previous coordinate `prev`. For each distinct coordinate `x`, we first consider the segment from `prev` to `x - 1`. During this entire region, the number of active segments is constant, so every integer point in this range contributes to `ans[active]`.
5. After accounting for the gap, apply all updates at coordinate `x`, adjusting `active` accordingly.
6. Move `prev` to `x` and continue.
7. After processing all events, no further gaps remain.

The key correctness point is that we only assign counts over stable regions where no event occurs, ensuring that each integer point is counted exactly once, and exactly with its true coverage value.

### Why it works

The sweep line maintains the invariant that between two consecutive event coordinates, no segment starts or ends. Therefore the set of active segments is constant throughout that interval. Since every integer point belongs to exactly one such interval, and we account for its full length using that constant value, each point contributes exactly once to the correct frequency bucket. The endpoint shifting by +1 ensures inclusivity is handled without double counting at boundaries.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    events = []
    
    for _ in range(n):
        l, r = map(int, input().split())
        events.append((l, 1))
        events.append((r + 1, -1))
    
    events.sort()
    
    ans = [0] * (n + 1)
    
    active = 0
    prev = None
    
    i = 0
    m = len(events)
    
    while i < m:
        x = events[i][0]
        
        if prev is not None and prev < x:
            length = x - prev
            ans[active] += length
        
        delta = 0
        while i < m and events[i][0] == x:
            delta += events[i][1]
            i += 1
        
        active += delta
        prev = x
    
    print(*ans[1:])

if __name__ == "__main__":
    solve()
```

The solution encodes segment endpoints into difference-array style events. The critical detail is using r + 1 for the decrement event, which aligns inclusive coverage with half-open interval processing. Sorting groups all changes at the same coordinate, and we aggregate them before moving forward so that intermediate states at the same position do not incorrectly affect the active count.

The gap handling `length = x - prev` is where coverage is actually accumulated. This is the only place where integer points are “counted”, and it correctly counts all integers from prev up to x - 1.

## Worked Examples

### Example 1

Input:

```
3
0 3
1 3
3 8
```

We build events:

(0, +1), (4, -1), (1, +1), (4, -1), (3, +1), (9, -1)

Sorted:

(0, +1), (1, +1), (3, +1), (4, -2), (9, -1)

| Step | x | prev | active before | segment length | contribution | active after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | - | 0 | - | - | 1 |
| 2 | 1 | 0 | 1 | 1 | ans[1] += 1 | 2 |
| 3 | 3 | 1 | 2 | 2 | ans[2] += 2 | 3 |
| 4 | 4 | 3 | 3 | 1 | ans[3] += 1 | 1 |
| 5 | 9 | 4 | 1 | 5 | ans[1] += 5 | 0 |

Final ans:

k=1 → 6, k=2 → 2, k=3 → 1

This trace shows that coverage is never computed per integer explicitly. Instead, each stable region between event coordinates is compressed into a single contribution weighted by its length.

### Example 2

Input:

```
3
0 0
2 2
4 4
```

Events:

(0, +1), (1, -1), (2, +1), (3, -1), (4, +1), (5, -1)

| Step | x | prev | active | length | contribution |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | - | 0 | - | - |
| 2 | 1 | 0 | 1 | 1 | ans[1]+=1 |
| 3 | 2 | 1 | 0 | 1 | ans[0]+=1 (ignored later) |
| 4 | 3 | 2 | 1 | 1 | ans[1]+=1 |
| 5 | 4 | 3 | 0 | 1 | ans[0]+=1 |
| 6 | 5 | 4 | 1 | 1 | ans[1]+=1 |

After ignoring k=0, result is:

k=1 → 3, k>=2 → 0

This highlights how isolated points behave as unit-length intervals between consecutive integers.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting 2n events dominates |
| Space | O(n) | event list and frequency array |

The algorithm scales cleanly to 200,000 segments because all operations reduce to sorting and linear scanning. No dependence on coordinate magnitude remains, which is essential given the 10^18 endpoint range.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    events = []
    for _ in range(n):
        l, r = map(int, input().split())
        events.append((l, 1))
        events.append((r + 1, -1))
    events.sort()

    ans = [0] * (n + 1)
    active = 0
    prev = None
    i = 0

    while i < len(events):
        x = events[i][0]
        if prev is not None and prev < x:
            ans[active] += x - prev
        delta = 0
        while i < len(events) and events[i][0] == x:
            delta += events[i][1]
            i += 1
        active += delta
        prev = x

    return " ".join(map(str, ans[1:]))

# provided sample
assert run("""3
0 3
1 3
3 8
""") == "6 2 1"

# single point segments
assert run("""3
5 5
10 10
15 15
""") == "3 0 0"

# fully overlapping
assert run("""3
1 5
1 5
1 5
""") == "0 0 5"

# nested segments
assert run("""3
1 10
2 9
3 8
""") == "0 2 6"

# disjoint large gaps
assert run("""2
0 0
100 100
""") == "2 0"

# all identical segments, large overlap
assert run("""4
0 1
0 1
0 1
0 1
""") == "0 0 2 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single points | 3 0 0 | degenerate segments |
| full overlap | 0 0 5 | maximum overlap counting |
| nested | 0 2 6 | varying coverage depth |
| disjoint | 2 0 | gaps and independent regions |
| identical | 0 0 2 0 | repeated identical intervals |

## Edge Cases

One important edge case is when segments degenerate into single points. For input:

```
1
5 5
```

The events become (5, +1) and (6, -1). The algorithm treats the interval [5, 5] as a unit-length contribution between 5 and 6. The active count becomes 1 exactly on that interval, so ans[1] increases by 1, matching the fact that exactly one integer point is covered.

Another edge case occurs when multiple events share the same coordinate. For example:

```
2
1 3
3 5
```

At coordinate 3, one segment ends while another starts. Because we aggregate all deltas at each coordinate before moving forward, the transition is handled atomically. The active count used for the interval [1, 3] is correct, and the next interval starts with the updated active count without any intermediate corruption.
