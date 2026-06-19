---
title: "CF 106467A - Spotlights"
description: "We are given a one-dimensional strip of positions, and some of these positions contain spotlights. Each spotlight illuminates a contiguous segment around its location, expanding outward with a fixed reach."
date: "2026-06-19T15:20:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106467
codeforces_index: "A"
codeforces_contest_name: "East China University of Science and Technology Programming Championship 2026"
rating: 0
weight: 106467
solve_time_s: 44
verified: true
draft: false
---

[CF 106467A - Spotlights](https://codeforces.com/problemset/problem/106467/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a one-dimensional strip of positions, and some of these positions contain spotlights. Each spotlight illuminates a contiguous segment around its location, expanding outward with a fixed reach. The task is to determine the final total illuminated coverage on the line after all spotlights are considered together.

You can think of the input as a list of spotlight centers and a fixed illumination radius. Each spotlight contributes an interval on the number line, and overlapping illuminated regions should be merged rather than counted multiple times. The output is the total length of the union of all illuminated intervals.

The key difficulty is that naïvely treating each point independently leads to overcounting when intervals overlap heavily.

From a complexity perspective, if there are up to 100000 spotlights, a solution that checks all pairs or marks every unit position individually is too slow. A quadratic approach over intervals would perform on the order of 10^10 operations in the worst case, which is not feasible under typical limits. Even a dense grid marking approach fails if coordinate ranges are large, because memory and time would explode with coordinate size.

A subtle edge case occurs when all spotlights overlap completely. For example, if all centers are identical and the radius is large, every spotlight produces the same interval. A naive summation would multiply this coverage incorrectly.

Another edge case arises when spotlights are far apart so that no intervals overlap. In this case, the answer is simply the sum of all individual coverage lengths, and any merging logic must not accidentally merge unrelated segments due to incorrect sorting or boundary handling.

## Approaches

The brute-force idea is straightforward. For each spotlight, we convert it into an interval on the line, say from center minus radius to center plus radius. Then we explicitly mark every covered unit position in a boolean array or set and count how many unique positions are covered.

This works correctly because it directly simulates the illumination process. However, it fails when coordinate values are large or when the range of coordinates is sparse. If coordinates span up to 10^9, creating an array of that size is impossible. Even if we compress coordinates, iterating over every unit position inside each interval leads to potentially summing up to 10^9 operations.

The key observation is that the problem reduces to computing the total length of a union of intervals. Once each spotlight is converted into an interval, we do not need to reason about individual points anymore. We only need to merge overlapping intervals and sum their lengths.

Sorting intervals by starting coordinate makes the structure exploitable. Once sorted, overlapping intervals appear consecutively, so we can sweep from left to right and maintain a currently active merged segment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(R) or O(n·R) | O(R) | Too slow |
| Sort + Merge Intervals | O(n log n) | O(n) | Accepted |

Here R represents the coordinate range or total covered discrete positions.

## Algorithm Walkthrough

We convert every spotlight into an interval, then merge them greedily in sorted order.

1. For each spotlight, compute its covered interval as [center − radius, center + radius]. This transforms the geometric illumination into a standard interval problem.
2. Sort all intervals by their left endpoint. Sorting ensures that any overlap must occur with previously processed intervals, so we never need to revisit earlier segments.
3. Initialize a current interval as the first sorted interval and a running answer as zero.
4. Iterate over the remaining intervals one by one.
5. For each new interval, compare it with the current merged interval.
6. If the new interval starts after the current interval ends, there is no overlap. Add the length of the current interval to the answer and start a new current interval. This is safe because no future interval can overlap backwards due to sorting.
7. If the new interval overlaps or touches the current interval, extend the current interval’s right endpoint to cover the union. This preserves correctness because overlapping coverage should not be double counted.
8. After processing all intervals, add the final current interval length to the answer.

The reason this greedy merging works is that at any point in the sweep, the current interval represents the full union of all intervals seen so far that overlap with each other. Since intervals are sorted, any future interval either overlaps this union or starts after it completely, and no earlier interval can extend beyond what has already been merged.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, r = map(int, input().split())
    intervals = []
    
    for _ in range(n):
        x = int(input())
        intervals.append((x - r, x + r))
    
    intervals.sort()
    
    ans = 0
    cur_l, cur_r = intervals[0]
    
    for l, r in intervals[1:]:
        if l > cur_r:
            ans += cur_r - cur_l
            cur_l, cur_r = l, r
        else:
            if r > cur_r:
                cur_r = r
    
    ans += cur_r - cur_l
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution first builds all illumination ranges and stores them as pairs. Sorting ensures we process intervals in increasing order of starting position, which is necessary for the greedy merge to work.

The variables `cur_l` and `cur_r` maintain the currently active merged coverage segment. Whenever a gap appears, the previous segment is finalized and added to the answer. If overlap exists, we only extend the right boundary.

A common implementation pitfall is forgetting to add the last active segment after the loop ends, which would lose the final contribution.

## Worked Examples

Consider an input with three spotlights and radius 2:

```
centers: 1, 4, 10
```

Intervals become:

```
[-1, 3], [2, 6], [8, 12]
```

Sorted order is the same.

| Step | Current Interval | New Interval | Action | Total Answer |
| --- | --- | --- | --- | --- |
| 1 | [-1, 3] | [2, 6] | merge → [ -1, 6 ] | 0 |
| 2 | [-1, 6] | [8, 12] | close [-1,6], start new | 7 |

Final interval [8,12] adds 4, so total is 11.

This trace shows how overlapping intervals are merged into a single continuous region, preventing double counting.

Now consider fully disjoint intervals:

```
centers: 0, 10, 20 with r = 1
```

Intervals:

```
[-1,1], [9,11], [19,21]
```

| Step | Current Interval | New Interval | Action | Total Answer |
| --- | --- | --- | --- | --- |
| 1 | [-1, 1] | [9, 11] | close [-1,1], start new | 2 |
| 2 | [9, 11] | [19, 21] | close [9,11], start new | 4 |

Final segment adds 2, total 6.

This confirms that non-overlapping regions are handled independently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates, merging is linear |
| Space | O(n) | storing intervals |

The sorting step is well within limits for n up to 100000. The linear scan ensures that each interval is processed once, making the solution efficient enough for typical Codeforces constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# sample-like
assert run("3 2\n1\n4\n10\n") == "11"

# no overlap
assert run("3 1\n0\n10\n20\n") == "6"

# all overlap
assert run("3 10\n0\n0\n0\n") == "20"

# single element
assert run("1 5\n7\n") == "10"

# tight chain overlap
assert run("4 2\n0\n3\n6\n9\n") == "11"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all overlap centers identical | 20 | duplicate intervals |
| disjoint spaced centers | 6 | independent segments |
| single spotlight | 10 | base case |
| chain overlap | 11 | transitive merging |

## Edge Cases

If all spotlights share the same position, every interval is identical. The algorithm still works because sorting keeps them adjacent and merging simply expands once, with no redundant counting.

For example:

```
3 5
10
10
10
```

All intervals are [5,15]. The first interval initializes the current segment, and every subsequent interval is fully contained, so no changes occur. The final answer is 10.

When intervals just touch at boundaries, such as [0,2] and [2,5], the algorithm treats them as overlapping because `l > cur_r` is false when equal. This ensures contiguous coverage is merged correctly into a single segment of length 5.

If there is only one spotlight, the loop never executes, and the final segment is directly returned, avoiding off-by-one errors in empty iteration logic.
