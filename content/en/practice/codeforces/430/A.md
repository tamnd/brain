---
title: "CF 430A - Points and Segments (easy)"
description: "We are asked to color a set of points on a number line using two colors, red and blue, so that for each given segment, the number of red and blue points inside that segment differ by at most one."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "sortings"]
categories: ["algorithms"]
codeforces_contest: 430
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 245 (Div. 2)"
rating: 1600
weight: 430
solve_time_s: 94
verified: false
draft: false
---

[CF 430A - Points and Segments (easy)](https://codeforces.com/problemset/problem/430/A)

**Rating:** 1600  
**Tags:** constructive algorithms, sortings  
**Solve time:** 1m 34s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to color a set of points on a number line using two colors, red and blue, so that for each given segment, the number of red and blue points inside that segment differ by at most one. In other words, every segment should be nearly balanced, with either exactly the same number of points of each color or one color exceeding the other by one. The input provides the coordinates of the points and the endpoints of each segment. The output must assign a color to each point, encoded as 0 for red and 1 for blue.

The constraints are quite small: there are at most 100 points and 100 segments, and coordinates range from 0 to 100. This allows algorithms with quadratic complexity in n or m, as $100^2 = 10,000$ operations are trivial for a 1-second time limit. The small coordinate range also suggests we might leverage coordinate compression or even an array indexed by position if needed.

A subtle edge case arises when two segments overlap in such a way that one point belongs to multiple segments. If we attempt a naive alternating pattern without considering segment overlap, we might create a situation where a point’s color choice causes one of the overlapping segments to violate the balance condition. For instance, with points `[1, 2, 3]` and segments `[1, 2]` and `[2, 3]`, coloring all points red seems fine for the first segment but violates the balance for the second. Recognizing this pattern is key to constructing a correct solution.

## Approaches

The brute-force approach would consider every possible coloring of points. With n points, there are $2^n$ colorings, which quickly becomes infeasible even for n = 20. Checking each coloring against all segments is straightforward, but the total operation count grows exponentially, making brute-force impractical for n = 100.

The key observation is that the segments are independent if you consider only adjacent points between segment boundaries. For any segment [l, r], as long as the points within the segment are colored in an alternating pattern along the x-axis, the balance condition |red - blue| ≤ 1 is automatically satisfied. This works because the points are distinct and sorted along the OX axis. It does not matter what color a point outside the segment has because segments only count the points they contain. Sorting points by x-coordinate and then coloring them alternately guarantees that every segment with consecutive points satisfies the balance requirement.

This insight reduces the problem to a simple greedy strategy: sort the points by their x-coordinate and assign colors alternately, starting with red. There is no need to backtrack or handle conflicts explicitly because the alternation ensures all possible segments are balanced. This approach is linear in the number of points, plus a sorting cost.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * m) | O(n) | Too slow |
| Alternating Colors by Sorted X | O(n log n + n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read n, m, the points, and the segment endpoints.
2. Pair each point with its original index because sorting will reorder them.
3. Sort the points by their x-coordinate.
4. Initialize a color array of size n.
5. Assign colors alternately along the sorted points, starting with red (0). For example, the first point is 0, the second is 1, the third is 0, and so on.
6. Restore the original order using the saved indices and print the color array.

Why it works: By coloring points in alternating order along the x-axis, any contiguous subset of points (which forms a segment) will have a color difference of at most one. This satisfies the problem’s balance condition for all segments. Sorting ensures that we treat points in left-to-right order, and alternating ensures the balance invariant.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
points = list(map(int, input().split()))
segments = [tuple(map(int, input().split())) for _ in range(m)]

# keep original indices
indexed_points = list(enumerate(points))
indexed_points.sort(key=lambda x: x[1])

colors = [0] * n
for i, (idx, _) in enumerate(indexed_points):
    colors[idx] = i % 2

print(' '.join(map(str, colors)))
```

The solution starts by reading the input and preserving the original indices of points. Sorting ensures that we alternate colors correctly along the number line. Assigning `i % 2` guarantees alternation, and finally, printing respects the original point order. Sorting by x-coordinate is crucial because segments may contain arbitrary consecutive points, and only consecutive coloring preserves balance.

## Worked Examples

**Sample 1**:

Input points: `[3, 7, 14]`

Segments: `[1,5], [6,10], [11,15]`

| Sorted index | Original idx | Point | Assigned color |
| --- | --- | --- | --- |
| 0 | 0 | 3 | 0 |
| 1 | 1 | 7 | 1 |
| 2 | 2 | 14 | 0 |

Segment [1,5] contains `[3]` → one red, zero blue → difference = 1 

Segment [6,10] contains `[7]` → one blue, zero red → difference = 1 

Segment [11,15] contains `[14]` → one red, zero blue → difference = 1 

All segments satisfy the requirement.

**Custom Sample 2**:

Points: `[2, 4, 5, 8]`

Segments: `[2,5], [4,8]`

| Sorted index | Original idx | Point | Assigned color |
| --- | --- | --- | --- |
| 0 | 0 | 2 | 0 |
| 1 | 1 | 4 | 1 |
| 2 | 2 | 5 | 0 |
| 3 | 3 | 8 | 1 |

Segment [2,5] contains `[2,4,5]` → colors `[0,1,0]` → red=2, blue=1 → difference =1 

Segment [4,8] contains `[4,5,8]` → colors `[1,0,1]` → red=1, blue=2 → difference=1 

The alternating pattern preserves the invariant across overlapping segments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m) | Sorting the points is O(n log n), segment processing is implicit |
| Space | O(n + m) | Store colors and indexed points, plus segments |

The solution easily fits within the limits: 100 points and 100 segments yield trivial computation times and memory usage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    points = list(map(int, input().split()))
    segments = [tuple(map(int, input().split())) for _ in range(m)]
    indexed_points = list(enumerate(points))
    indexed_points.sort(key=lambda x: x[1])
    colors = [0] * n
    for i, (idx, _) in enumerate(indexed_points):
        colors[idx] = i % 2
    return ' '.join(map(str, colors))

# Provided sample
assert run("3 3\n3 7 14\n1 5\n6 10\n11 15\n") in ["0 1 0", "0 0 0", "1 0 1"], "sample 1"

# Minimum input
assert run("1 1\n0\n0 0\n") == "0", "single point"

# Maximum input with alternating pattern
assert run("4 2\n1 2 3 4\n1 2\n3 4\n") in ["0 1 0 1", "1 0 1 0"], "overlapping segments"

# All points at same value (edge case)
assert run("3 1\n5 5 5\n5 5\n") in ["0 1 0", "1 0 1"], "single-point segment repeated"

# Non-overlapping segments
assert run("5 2\n1 3 5 7 9\n0 2\n6 8\n") in ["0 1 0 1 0", "1 0 1 0 1"], "non-overlapping segments"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1\n0\n0 0` | `0` | Single point case |
| `4 2\n1 2 3 4\n1 2\n3 4` | `0 1 0 1` | Alternating pattern across multiple segments |
| `3 1\n5 5 5\n5 5` | `0 1 0` | Points at same coordinate with single-point segment |
| `5 2\n1 3 5 7 9\n0 2\n6 8` | `0 1 0 1 0` | Non-overlapping segments |

## Edge Cases

When points coincide with segment boundaries or when segments overlap, the alternation strategy still guarantees that any segment will contain either equal numbers of red and blue points or differ
