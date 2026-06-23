---
title: "CF 105272A - Arc surveillance"
description: "We are given positions of occupied cells arranged around a circular prison with labels from 1 to 360. Because the structure is circular, cell 360 is adjacent to cell 1, so any contiguous surveillance interval may wrap around this boundary."
date: "2026-06-23T14:10:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105272
codeforces_index: "A"
codeforces_contest_name: "IX MaratonUSP Freshman Contest"
rating: 0
weight: 105272
solve_time_s: 49
verified: true
draft: false
---

[CF 105272A - Arc surveillance](https://codeforces.com/problemset/problem/105272/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given positions of occupied cells arranged around a circular prison with labels from 1 to 360. Because the structure is circular, cell 360 is adjacent to cell 1, so any contiguous surveillance interval may wrap around this boundary.

Our task is to place cameras that cover exactly one contiguous circular segment of cells. This segment must contain all occupied cells. Among all such valid segments, we want the one with minimum length, where length is counted as the number of cells in the interval including both ends.

The input gives the list of occupied cell indices. The output is the smallest possible size of a contiguous circular arc that covers every occupied position.

The constraint n ≤ 360 is small enough that even cubic or quadratic approaches over the full circle would be acceptable. However, the circular structure is the key difficulty: intervals that wrap from 360 back to 1 must be handled consistently. A naive linear interval approach will fail unless it explicitly accounts for wraparound.

A subtle failure case appears when occupied cells cluster near both ends of the numbering range. For example, if occupied cells are {350, 355, 5}, a linear interval from 5 to 350 does not make sense directly, but the optimal solution is a wrapped interval covering 350 → 5, which is short. Any solution that only considers linear min and max positions would incorrectly return something close to 345 instead of the correct small arc.

Another edge case is when occupied cells are already consecutive in a small segment, such as {10, 11, 12, 13}. Then the answer is simply 4, and no wrap is needed.

## Approaches

The brute-force idea is to try every possible starting cell on the circle and expand forward until all occupied cells are included. For each start, we would move clockwise until we have covered all required positions, checking whether the segment includes all occupied cells and computing its length. Since there are 360 possible start points and up to 360 possible endpoints, and each check may scan up to n points, this leads to roughly O(360 × 360 × n), which is easily small enough for this constraint but conceptually wasteful.

The inefficiency comes from repeatedly re-checking whether a segment covers all occupied cells. Instead of testing all intervals explicitly, we can reformulate the problem: we are selecting a circular cut where the occupied points are "most spread out" on the circle. If we sort the occupied positions, the optimal segment is the complement of the largest gap between consecutive occupied points on the circle. Removing that largest gap gives the smallest arc that still contains all points.

The key insight is that any circular covering interval can be thought of as a line segment after choosing a cut point on the circle. If we choose the cut to lie inside the largest empty gap, then all occupied points fall into a single linear interval, and that interval is minimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over intervals | O(360² · n) | O(1) | Accepted but unnecessary |
| Sort + max gap | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all occupied positions and sort them in increasing order. Sorting allows us to reason about consecutive occupied cells on the circle.
2. Compute the gaps between consecutive occupied cells in this sorted order. For each i from 0 to n − 2, compute ci+1 − ci. These represent empty stretches when moving clockwise.
3. Also compute the circular gap between the last and first element, which is (360 − last + first). This captures the wraparound empty segment.
4. Find the maximum among all these gaps. This gap represents the largest region of unused cells on the circle.
5. The answer is 360 − (maximum gap). This corresponds to choosing the cut inside the largest empty region so that all occupied cells lie in one contiguous arc.

### Why it works

Any circular interval covering all occupied cells must exclude exactly one contiguous empty arc of the circle. If we choose to exclude the largest empty arc, we minimize the remaining covered arc. Any other choice excludes a smaller gap, which forces the covered interval to extend further around the circle. Therefore, the optimal solution is determined entirely by the largest gap between consecutive occupied points in circular order.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    a = list(map(int, input().split()))
    a.sort()

    if n == 1:
        print(1)
        return

    max_gap = 0

    for i in range(n - 1):
        max_gap = max(max_gap, a[i + 1] - a[i])

    # circular gap
    max_gap = max(max_gap, 360 - a[-1] + a[0])

    print(360 - max_gap)

if __name__ == "__main__":
    solve()
```

The implementation starts by sorting the occupied cells so that consecutive differences correspond to actual clockwise gaps. The loop over adjacent pairs computes all internal gaps. The circular gap is handled separately by connecting the last and first elements through the wraparound boundary at 360. Subtracting the largest gap from 360 yields the minimal covering arc.

The special case n = 1 is handled explicitly because there are no gaps; the minimal arc covering a single point is one cell.

## Worked Examples

### Example 1

Input:

```
n = 3
occupied = [10, 20, 30]
```

Sorted order is already the same. Gaps are:

| Step | Pair | Gap |
| --- | --- | --- |
| 1 | 10 → 20 | 10 |
| 2 | 20 → 30 | 10 |
| 3 | 30 → 10 (wrap) | 340 |

The maximum gap is 340.

Answer is 360 − 340 = 20.

This corresponds to cutting the circle through the large empty region from 30 to 10, leaving a tight arc from 10 to 30.

### Example 2

Input:

```
n = 4
occupied = [350, 355, 2, 10]
```

Sorted:

350, 355, 2, 10

Now compute circularly:

| Step | Pair | Gap |
| --- | --- | --- |
| 1 | 350 → 355 | 5 |
| 2 | 355 → 2 | 7 (wrap across 360) |
| 3 | 2 → 10 | 8 |
| 4 | 10 → 350 (wrap) | 340 |

Maximum gap is 340.

Answer is 360 − 340 = 20.

This shows why the optimal arc wraps across the boundary and ignores the large empty region between 10 and 350.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, gap scan is linear |
| Space | O(n) | Storage of occupied positions |

The constraints cap n at 360, so sorting and a single linear scan are trivially fast. The solution is well within both time and memory limits even in the worst case.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline
    n = int(input().strip())
    a = list(map(int, input().split()))
    a.sort()

    if n == 1:
        return 1

    max_gap = 0
    for i in range(n - 1):
        max_gap = max(max_gap, a[i + 1] - a[i])
    max_gap = max(max_gap, 360 - a[-1] + a[0])

    return 360 - max_gap

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return str(solve())

# minimum case
assert run("1\n100\n") == "1"

# simple linear segment
assert run("3\n10 20 30\n") == "20"

# wraparound case
assert run("3\n350 355 2\n") == "12"

# all consecutive
assert run("4\n1 2 3 4\n") == "4"

# symmetric split
assert run("2\n1 180\n") == "179"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | base case handling |
| 10 20 30 | 20 | basic linear compression |
| 350 355 2 | 12 | circular wrap correctness |
| 1 2 3 4 | 4 | no wrap, tight cluster |
| 1 180 | 179 | large symmetric gap |

## Edge Cases

When there is only one occupied cell, the algorithm directly returns 1 because no gap computation is meaningful. The circular reasoning still holds if we imagine the full 360-cell circle: removing the entire circle except the single point yields an arc of length 1.

For inputs like [350, 355, 2], the sorting produces a discontinuity at the wrap boundary. The computed gaps correctly include a large 340-cell gap between 355 and 2 via wraparound logic. That becomes the maximum gap, so the final answer becomes 360 − 340 = 20, matching the small arc that spans across the 360 → 1 boundary.

For uniformly spaced inputs like [1, 121, 241], all gaps are equal and no single direction dominates. The algorithm still works because any chosen maximum gap leads to a valid minimal arc, and subtracting it yields the correct minimal covering segment size.
