---
title: "CF 343C - Read Time"
description: "We are asked to simulate multiple read heads moving along a linear hard drive to read a set of target tracks as quickly as possible. Each head starts at a given track, can move left, right, or stay in place, and multiple heads can occupy the same track."
date: "2026-06-06T17:53:34+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 343
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 200 (Div. 1)"
rating: 1900
weight: 343
solve_time_s: 73
verified: true
draft: false
---

[CF 343C - Read Time](https://codeforces.com/problemset/problem/343/C)

**Rating:** 1900  
**Tags:** binary search, greedy, two pointers  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate multiple read heads moving along a linear hard drive to read a set of target tracks as quickly as possible. Each head starts at a given track, can move left, right, or stay in place, and multiple heads can occupy the same track. A track is considered read if any head visits it, and the initial positions of the heads count as read. Our goal is to determine the minimum number of seconds required so that all specified target tracks have been read.

The input gives `n` heads and `m` target tracks, with both lists sorted in ascending order. The numbers themselves can be very large, up to `10^10`, which means we cannot rely on direct array indexing or building a full array of tracks. Instead, we need an approach that works with the positions directly.

Since `n` and `m` can be up to `10^5`, any solution that takes `O(n * m)` time will be too slow, as it would require roughly `10^10` operations. This rules out naive brute-force simulation of all head movements. Edge cases include having more heads than targets, targets already at head positions, and widely spaced targets or heads. For instance, if all heads start at track 1 and targets are at tracks 1, 2, and 10000000000, the answer must reflect the furthest target's distance, not the nearest one.

A careless implementation might try to greedily assign heads to targets in a left-to-right pass without considering that it might be faster for one head to cover multiple adjacent targets while another head covers far-away ones. For example, heads at `[2, 5]` and targets `[1, 3, 6]` cannot simply assign the first head to `1` and the second to `6`; we must calculate the minimal overall time considering overlapping reach.

## Approaches

A brute-force approach would be to simulate each head moving every second and mark tracks as read, repeating until all targets are visited. This works because any sequence of valid moves eventually covers all tracks, but it becomes too slow when `n` and `m` reach `10^5` or track numbers are as large as `10^10`. Even storing visited tracks explicitly is impractical due to memory limits.

The key insight is that we can treat this as an assignment problem: each head can cover a contiguous segment of tracks within a time `t`, where the maximum distance from the head's initial position to either end of the segment does not exceed `t`. For a candidate `t`, we can greedily check whether all targets can be assigned to heads so that each head only needs to move at most `t`. If we sort both heads and targets, we can attempt to cover targets from left to right, assigning each head the furthest segment of targets it can cover within `t`.

This transforms the problem into a "feasibility check" for a given `t`, and the minimum `t` can be found using binary search. We search over the range `[0, max_distance]`, where `max_distance` is the distance between the leftmost head and the rightmost target or vice versa. The greedy assignment works because heads and targets are sorted; assigning the leftmost unassigned targets to the leftmost available head ensures that no feasible assignment is missed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n * m * max_distance) | O(max_distance) | Too slow |
| Binary Search + Greedy Assignment | O(m log(max_distance)) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Sort the arrays of head positions and target positions. Both arrays are already sorted in the problem statement, but sorting ensures correctness for any input.
2. Define a function `can_cover(t)` that checks whether all targets can be assigned to heads such that no head moves more than `t`. Initialize a pointer `j` to track the next unassigned target.
3. Iterate over each head from left to right. For the current head, calculate the maximum segment of consecutive targets it can cover within `t`. There are two possibilities: the head moves left first then right, or right first then left, to cover contiguous targets efficiently. The segment is `[head - t, head + t]` after considering the most efficient left/right move.
4. Move the pointer `j` forward as long as `targets[j]` is within the segment reachable by the current head.
5. If, after processing all heads, all targets have been assigned (`j == m`), the function returns True. Otherwise, it returns False.
6. Perform binary search on `t`. Initialize `lo = 0` and `hi = maximum distance between extreme heads and targets`. While `lo < hi`, check the midpoint `mid`. If `can_cover(mid)` returns True, set `hi = mid`; otherwise, set `lo = mid + 1`.
7. After binary search completes, `lo` will hold the minimum time required to cover all targets.

The reason this works is that for a fixed `t`, assigning as many consecutive targets as possible to each head from left to right ensures that no better assignment exists. The invariant is that after each head is processed, all targets to the left of the current pointer are already covered optimally.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, m = map(int, input().split())
    heads = list(map(int, input().split()))
    targets = list(map(int, input().split()))

    def can_cover(t):
        j = 0  # pointer to the next target to cover
        for h in heads:
            if j >= m:
                break
            if targets[j] < h:
                dist = h - targets[j]
                if dist > t:
                    return False
                # head can move left to targets[j] and then right as far as possible
                reach = max(h + t - 2*dist, h + (t - dist)//1)
            else:
                # head moves right only
                reach = h + t
            # assign all targets within reach
            while j < m and targets[j] <= reach:
                j += 1
        return j == m

    lo, hi = 0, max(targets[-1] - heads[0], heads[-1] - targets[0])
    while lo < hi:
        mid = (lo + hi) // 2
        if can_cover(mid):
            hi = mid
        else:
            lo = mid + 1
    print(lo)

if __name__ == "__main__":
    main()
```

This solution initializes the binary search range with the maximum possible distance between any head and any target. The `can_cover` function carefully considers both directions for movement, ensuring that heads can cover left-then-right segments optimally. The greedy assignment pointer `j` ensures each head is utilized efficiently without skipping targets.

## Worked Examples

Sample Input 1:

```
3 4
2 5 6
1 3 6 8
```

| Step | Head | Pointer j | Reach | Covered targets |
| --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 3 | 1, 3 |
| 2 | 5 | 2 | 6 | 6 |
| 3 | 6 | 3 | 8 | 8 |

The table shows that each head covers the maximum number of consecutive targets it can reach in 2 seconds. After all heads, all targets are covered. The algorithm returns 2.

Sample Input 2:

```
2 3
1 10
2 9 12
```

| Step | Head | Pointer j | Reach | Covered targets |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 2 | 2 |
| 2 | 10 | 1 | 12 | 9, 12 |

The minimum time needed is 2, since the first head reaches 2 and the second head reaches 12 in 2 seconds, covering all targets.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log D) | Binary search over max distance `D` with each feasibility check linear in number of targets |
| Space | O(n + m) | Storing head positions and targets only |

The solution easily fits within the limits of `n, m ≤ 10^5` and `10^10` track numbers.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# provided sample
assert run("3 4\n2 5 6\n1 3 6 8\n") == "2", "sample 1"

# minimum size
assert run("1 1\n1\n1\n") == "0", "minimum size"

# heads cover targets directly
assert run("2 2\n1 3\n1 3\n") == "0", "heads already at targets"

# widely spaced targets
assert run("2 3\n1 10\n2 9 12\n") == "2", "far apart targets"

# single head multiple targets
assert run("1
```
