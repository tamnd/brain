---
title: "CF 104760C - \u0414\u043e\u0440\u043e\u0433\u0430"
description: "We are given a collection of intervals placed along a number line. Each interval represents a lamp that illuminates a segment of a road, from its starting coordinate to its ending coordinate."
date: "2026-06-28T22:00:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104760
codeforces_index: "C"
codeforces_contest_name: "2023-2024 ICPC NERC (NEERC), Kyrgyzstan Qualification Contest"
rating: 0
weight: 104760
solve_time_s: 58
verified: true
draft: false
---

[CF 104760C - \u0414\u043e\u0440\u043e\u0433\u0430](https://codeforces.com/problemset/problem/104760/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of intervals placed along a number line. Each interval represents a lamp that illuminates a segment of a road, from its starting coordinate to its ending coordinate. Multiple lamps may overlap, and parts of the road may be covered by several intervals or by none at all.

The task is to determine the total length of the road that is illuminated by at least one lamp. In other words, we need to compute the length of the union of all given intervals.

The constraints allow up to 10,000 intervals, with coordinates ranging from negative to positive one billion. This size immediately rules out any approach that tries to inspect the road point by point. A naive discretization over the coordinate range would require iterating over up to 2 billion positions, which is far beyond feasible limits. Even storing every possible coordinate explicitly is impossible in both time and memory.

A more subtle issue arises with overlap handling. For example, if intervals are nested or heavily overlapping, simply summing their lengths will overcount shared regions. Consider intervals `[0, 10]` and `[5, 15]`. Summing lengths gives 10 + 10 = 20, but the correct union is `[0, 15]`, which has length 15. Any correct solution must explicitly avoid double counting overlapping segments.

Edge cases that commonly break naive implementations include completely disjoint intervals, fully nested intervals, and intervals that only touch at endpoints. For instance, `[0, 5]` and `[5, 10]` should contribute a total length of 10 if endpoints are considered continuous coverage, which is the standard interpretation in this problem. A naive “merge only if overlap is strict” implementation may incorrectly treat touching intervals as separate.

## Approaches

A brute-force interpretation would be to simulate coverage on a fine-grained number line. One could imagine marking every integer point covered by any interval and then counting how many are marked. While conceptually simple, this fails immediately because coordinates span from -10^9 to 10^9. Even if we compress coordinates, doing per-point marking or scanning remains too slow because each interval might be very large.

Another brute idea is to compare every pair of intervals and merge overlaps repeatedly until stability. This leads to an O(N^2) process in the worst case, since each merge step can require scanning and updating many intervals, and repeated passes may be needed.

The key observation is that we do not actually need to know point-level coverage. We only need to know where coverage changes from “uncovered” to “covered” and vice versa. Once intervals are sorted by starting coordinate, overlaps become structured: when we process intervals in order, we only need to maintain the farthest right endpoint seen so far. Any new interval either extends the current covered region or starts a new disjoint region.

This reduces the problem to a classic sweep over sorted intervals, maintaining a current active segment and accumulating its contribution whenever a gap appears.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force marking | O(R) where R is coordinate range | O(R) | Impossible |
| Pairwise merging | O(N^2) | O(N) | Too slow |
| Sorting + sweep | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Read all intervals and sort them by their starting coordinate. Sorting ensures that when we move left to right, we never revisit earlier uncovered gaps incorrectly.
2. Initialize a running segment using the first interval. This segment represents the current union of overlapping intervals we are building.
3. Iterate through the remaining intervals one by one in sorted order.
4. For each interval, compare its start with the current segment’s end. If the start is less than or equal to the current end, the intervals overlap or touch, so we extend the current segment’s end to the maximum of both ends. This preserves continuity of coverage without double counting.
5. If the start is greater than the current end, there is a gap between the current covered segment and the new interval. In this case, add the length of the current segment to the answer, then start a new segment from the current interval.
6. After processing all intervals, add the final active segment to the answer.

The key idea is that we only finalize a segment when we are certain no future interval can extend it, which happens exactly when we detect a gap.

### Why it works

At every step, the algorithm maintains an invariant: the current segment represents exactly the union of all intervals processed so far that intersect each other or form a connected chain through overlaps. Because intervals are processed in increasing order of start, any future interval can only extend this segment or begin strictly after it. Therefore, when we encounter a new interval starting after the current end, the current segment is fully determined and cannot be affected by any future data, so its length can safely be added to the final result.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    intervals = []
    for _ in range(n):
        a, b = map(int, input().split())
        intervals.append((a, b))

    intervals.sort()

    cur_l, cur_r = intervals[0]
    total = 0

    for l, r in intervals[1:]:
        if l <= cur_r:
            if r > cur_r:
                cur_r = r
        else:
            total += cur_r - cur_l
            cur_l, cur_r = l, r

    total += cur_r - cur_l
    print(total)

if __name__ == "__main__":
    solve()
```

The code begins by reading all intervals and sorting them, which is essential for ensuring that overlaps appear consecutively. The variables `cur_l` and `cur_r` track the currently active merged segment. When a new interval overlaps, only the right boundary may expand, which is why we take the maximum. When a gap is found, the current segment length is finalized and added to `total`, and we restart the segment.

A subtle detail is that we never add partial contributions during overlap processing. This avoids double counting entirely, since each segment is accounted for exactly once when it is closed.

## Worked Examples

### Example 1

Input:

```
5
30 40
5 8
3 22
40 42
0 10
```

Sorted intervals:

`(0,10), (3,22), (5,8), (30,40), (40,42)`

| Step | Interval | Current segment | Action | Total |
| --- | --- | --- | --- | --- |
| 1 | (0,10) | (0,10) | initialize | 0 |
| 2 | (3,22) | (0,22) | extend | 0 |
| 3 | (5,8) | (0,22) | no change | 0 |
| 4 | (30,40) | finalize (0,22) | add 22 | 22 |
| 5 | (30,40) | (30,40) | start new | 22 |
| 6 | (40,42) | (30,42) | extend | 22 |
| end | - | finalize (30,42) | add 12 | 34 |

This trace shows how overlapping intervals collapse into a single continuous segment, while disjoint parts are accumulated separately.

### Example 2

Input:

```
3
1 3
2 5
6 8
```

Sorted intervals: `(1,3), (2,5), (6,8)`

| Step | Interval | Current segment | Action | Total |
| --- | --- | --- | --- | --- |
| 1 | (1,3) | (1,3) | initialize | 0 |
| 2 | (2,5) | (1,5) | extend | 0 |
| 3 | (6,8) | finalize (1,5) | add 4 | 4 |
| end | - | finalize (6,8) | add 2 | 6 |

This example highlights the gap detection logic that triggers segment finalization.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Sorting dominates; single linear sweep afterward |
| Space | O(N) | Storage of intervals |

The constraints allow up to 10,000 intervals, so sorting and a linear scan are easily fast enough. The algorithm avoids any dependence on coordinate magnitude, which is crucial given the large range.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    intervals = []
    for _ in range(n):
        a, b = map(int, input().split())
        intervals.append((a, b))

    intervals.sort()

    cur_l, cur_r = intervals[0]
    total = 0

    for l, r in intervals[1:]:
        if l <= cur_r:
            if r > cur_r:
                cur_r = r
        else:
            total += cur_r - cur_l
            cur_l, cur_r = l, r

    total += cur_r - cur_l
    return str(total).strip()

# provided sample
assert run("""5
30 40
5 8
3 22
40 42
0 10
""") == "34"

# disjoint intervals
assert run("""2
0 1
3 4
""") == "2"

# fully nested intervals
assert run("""3
0 10
2 5
3 7
""") == "10"

# touching intervals
assert run("""3
0 5
5 10
10 15
""") == "15"

# single interval
assert run("""1
-5 5
""") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| disjoint intervals | 2 | gap handling |
| nested intervals | 10 | non-overcounting |
| touching intervals | 15 | endpoint merging |
| single interval | 10 | base case |

## Edge Cases

For disjoint intervals such as `[0,1]` and `[3,4]`, the algorithm processes the first interval, then detects `3 > 1` and finalizes the first segment before starting a new one. This ensures no artificial merging occurs across gaps.

For nested intervals like `[0,10]`, `[2,5]`, `[3,7]`, the running end only ever increases to 10, and no premature closure happens because all starts are within the current range. The invariant that `cur_r` is the maximum right endpoint of all overlapping intervals guarantees correctness.

For touching intervals such as `[0,5]` and `[5,10]`, the condition `l <= cur_r` treats them as connected, so they merge into `[0,10]`. This avoids undercounting due to boundary separation conventions in continuous coverage problems.
