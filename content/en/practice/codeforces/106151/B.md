---
title: "CF 106151B - foodbreak"
description: "We are given a day that starts at time 0 and ends at time T. Inside this interval, there are N scheduled presentations, each occupying a half-open segment [si, ei), meaning it starts at si and ends just before ei. These presentations may overlap or be disjoint."
date: "2026-06-19T19:22:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106151
codeforces_index: "B"
codeforces_contest_name: "2025 ICPC Greek Collegiate Programming Contest (GRCPC 2025)"
rating: 0
weight: 106151
solve_time_s: 47
verified: true
draft: false
---

[CF 106151B - foodbreak](https://codeforces.com/problemset/problem/106151/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a day that starts at time 0 and ends at time T. Inside this interval, there are N scheduled presentations, each occupying a half-open segment [si, ei), meaning it starts at si and ends just before ei. These presentations may overlap or be disjoint.

Between these scheduled segments, there are free periods where no presentation is running. The task is to find the longest continuous free period inside [0, T) that is not covered by any presentation.

The key detail is that “gap” means a maximal contiguous interval with no overlap from any presentation. So even if multiple small free intervals exist, we only care about the largest one after considering all overlaps and merging occupied time correctly.

The constraints N up to 100000 and T up to 10^9 immediately rule out any approach that checks every unit of time. Even scanning the timeline or doing a per-time simulation would be far too slow. Any correct solution must reduce the problem to sorting and linear processing over intervals.

A common failure case appears when intervals overlap and are not merged. For example, if we have [5, 10] and [8, 12], the free space between them is not between 10 and 8, since the intervals overlap and effectively form a continuous blocked region [5, 12). A naive gap computation that compares consecutive input intervals without normalization would incorrectly count internal overlaps as free space.

Another edge case is when no presentations exist. Then the whole interval [0, T) is a single gap of length T. A naive solution that assumes at least one interval would fail here.

Finally, presentations may not be sorted by start time, so relying on input order without sorting can produce incorrect gap calculations.

## Approaches

The brute-force idea is to reconstruct the entire timeline and mark all occupied regions, then scan for free segments. One way is to sort events per unit time or simulate each interval start and end, but since T can be as large as 10^9, any discretization over time is impossible. Even if we tried to iterate over all possible integer times, that would be 10^9 operations, which is far beyond limits.

A more structured brute-force approach is to sort intervals and then, for each interval, repeatedly merge it into a growing occupied set. Once we have a union of all occupied intervals, we can scan between them to compute gaps. The naive version still might recompute overlaps inefficiently if implemented with repeated scanning, potentially leading to O(N^2) behavior.

The key observation is that all we really need is the union of intervals. Once intervals are sorted by start time, merging them greedily in one pass produces disjoint occupied segments. After that, gaps are simply differences between consecutive merged segments, plus the boundaries at 0 and T.

The structure that enables this is that interval union on a line is fully determined by sorting endpoints and sweeping once. No further global reasoning is needed beyond maintaining the current merged segment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(T + N^2) or O(T) | O(T) | Too slow |
| Optimal (sort + merge) | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Sort all presentations by their start time. This ensures we process intervals in chronological order, so overlaps become easy to detect.
2. Initialize a variable current_end to 0, representing the end of the last merged occupied segment.
3. Initialize best_gap to 0, which will track the maximum free time found so far.
4. Iterate through each interval [s, e] in sorted order.
5. If s is greater than current_end, then there is a free gap between current_end and s. Update best_gap with s - current_end. This is valid because all previous intervals end no later than current_end, so nothing blocks this region.
6. Update current_end to be max(current_end, e). This merges overlapping intervals into a single occupied segment.
7. After processing all intervals, there may still be free time between current_end and T. Update best_gap with T - current_end.

Why it works is that after sorting, we maintain an invariant that current_end always represents the farthest point covered by the union of all processed intervals. Any time we encounter a start time beyond this point, we have fully discovered a maximal free segment. Since every interval is processed once in order and merged greedily, no occupied region is missed and no gap is double-counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, T = map(int, input().split())
    intervals = []

    for _ in range(n):
        s, e = map(int, input().split())
        intervals.append((s, e))

    intervals.sort()

    current_end = 0
    best_gap = 0

    for s, e in intervals:
        if s > current_end:
            best_gap = max(best_gap, s - current_end)
        current_end = max(current_end, e)

    best_gap = max(best_gap, T - current_end)

    print(best_gap)

if __name__ == "__main__":
    solve()
```

The code begins by reading all intervals and sorting them so that overlaps become contiguous in processing order. The variable current_end tracks the farthest time covered by merged presentations so far. Whenever we see a new interval starting after current_end, we immediately measure the free space between them. Updating current_end with max ensures overlapping or touching intervals are merged correctly instead of being treated as separate blocks. The final update against T captures the tail gap after the last presentation.

A subtle point is using a strict comparison s > current_end rather than s >= current_end. Using s >= current_end is also correct in this problem because touching intervals like [1,2) and [2,3) do not create a gap. However, using s > current_end makes the intention explicit that only strictly uncovered time contributes to gaps.

## Worked Examples

### Example 1

Input:

4 60

5 10

50 55

25 30

15 20

Sorted intervals become:

[5,10], [15,20], [25,30], [50,55]

| Interval | current_end before | Gap detected | current_end after | best_gap |
| --- | --- | --- | --- | --- |
| [5,10] | 0 | 5 | 10 | 5 |
| [15,20] | 10 | 5 | 20 | 5 |
| [25,30] | 20 | 5 | 30 | 5 |
| [50,55] | 30 | 20 | 55 | 20 |

After loop, final gap is 60 - 55 = 5, so answer is 20.

This trace shows how the algorithm accumulates gaps only between merged occupied segments, not between raw input intervals.

### Example 2

Input:

3 10

2 3

3 5

6 8

Sorted intervals:

[2,3], [3,5], [6,8]

| Interval | current_end before | Gap detected | current_end after | best_gap |
| --- | --- | --- | --- | --- |
| [2,3] | 0 | 2 | 3 | 2 |
| [3,5] | 3 | 0 | 5 | 2 |
| [6,8] | 5 | 1 | 8 | 2 |

Final gap is 10 - 8 = 2, answer is 2.

This example highlights that touching intervals do not create gaps and that merging prevents false internal gaps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Sorting dominates, single linear sweep afterwards |
| Space | O(N) | Storage for intervals |

The solution fits easily within constraints since N is up to 100000, and sorting plus one pass is well within time limits in 1 second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()

    def solve():
        n, T = map(int, sys.stdin.readline().split())
        intervals = []
        for _ in range(n):
            s, e = map(int, sys.stdin.readline().split())
            intervals.append((s, e))

        intervals.sort()
        current_end = 0
        best_gap = 0

        for s, e in intervals:
            if s > current_end:
                best_gap = max(best_gap, s - current_end)
            current_end = max(current_end, e)

        best_gap = max(best_gap, T - current_end)
        print(best_gap)

    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("""4 60
5 10
50 55
25 30
15 20
""") == "20"

# no presentations
assert run("""0 10
""") == "10"

# fully covered
assert run("""2 5
0 3
3 5
""") == "0"

# overlapping intervals
assert run("""3 10
1 5
2 6
7 9
""") == "1"

# disjoint with boundary gaps
assert run("""2 10
2 3
8 9
""") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty schedule | 10 | full-day gap handling |
| full coverage | 0 | no-gap case |
| overlapping merge | 1 | correct union merging |
| boundary gaps | 5 | prefix/suffix gap correctness |

## Edge Cases

One important edge case is when there are no intervals at all. The algorithm never enters the loop, current_end remains 0, and the final answer becomes T - 0, correctly producing the full-day gap.

Another case is complete coverage where merged intervals extend to T. For input like [0,3] and [3,5], current_end becomes 5, and the final gap is T - current_end = 0, correctly reflecting no free time.

A subtle case is overlapping chains where intervals are not directly overlapping pairwise but still form one large block. For example [1,4], [3,6], [5,10]. The sweep ensures current_end grows monotonically to 10, preventing any false gap between intermediate endpoints.
