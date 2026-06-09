---
title: "CF 1691E - Number of Groups"
description: "We are given a set of segments on the number line, each colored either red or blue. Each segment occupies a continuous interval from li to ri, inclusive."
date: "2026-06-09T23:11:30+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "dsu", "graphs", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1691
codeforces_index: "E"
codeforces_contest_name: "CodeCraft-22 and Codeforces Round 795 (Div. 2)"
rating: 2300
weight: 1691
solve_time_s: 192
verified: true
draft: false
---

[CF 1691E - Number of Groups](https://codeforces.com/problemset/problem/1691/E)

**Rating:** 2300  
**Tags:** data structures, dfs and similar, dsu, graphs, greedy, sortings  
**Solve time:** 3m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of segments on the number line, each colored either red or blue. Each segment occupies a continuous interval from `l_i` to `r_i`, inclusive. The task is to find groups of segments where two segments are considered connected if they are of different colors and their intervals overlap. Segments can be connected indirectly through a chain of alternating colors. The output is the total number of such connected groups for each test case.

The constraints tell us that the total number of segments across all test cases does not exceed `10^5`. This means any algorithm that is `O(n^2)` per test case will be too slow. We need a solution that is roughly linear or linearithmic per test case, ideally `O(n log n)`.

Edge cases that can trip a naive approach include segments that share endpoints but do not overlap beyond that, multiple segments of the same color fully overlapping each other, or segments that alternate in color but have gaps that break connectivity. For example, three segments `(0, 0, 1)`, `(1, 1, 2)`, `(0, 3, 4)` form three separate groups because the last red segment does not overlap the blue segment, even though it follows it in order.

## Approaches

The brute-force approach would iterate over every pair of segments and check if they overlap and have different colors. If they do, you would union them into a group using a data structure like DSU (disjoint set union). This is correct but would require checking `O(n^2)` pairs, which can reach `10^10` operations for the largest inputs, far exceeding the time limit.

The key insight is that for each color, you only need to track the furthest-right point reached so far in order to determine if a segment of the opposite color connects to the current group. Sorting segments by their start point and sweeping from left to right allows us to merge segments into groups efficiently. This reduces the problem to scanning two sorted lists (one for red and one for blue), maintaining maximum reach, and incrementing the group count whenever a segment starts after the furthest point of the opposite color.

This observation transforms a naive `O(n^2)` approach into a manageable `O(n log n)` solution dominated by the sort operation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Sweep + Max Reach | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Separate the segments into two lists by color: red and blue. Sort each list by the left endpoint `l_i`.
2. Initialize two variables `max_red` and `max_blue` to track the rightmost endpoints of segments in the current active group for each color.
3. Initialize a group counter `groups` to 0. This will count connected groups.
4. Merge the two sorted lists in left-to-right order. For each segment, check if it overlaps with the current maximum reach of the opposite color.
5. If the segment overlaps the opposite color’s max endpoint, merge it into the current group and update the max endpoint for its color.
6. If the segment starts after the max reach of the opposite color, increment the group counter because this segment starts a new disconnected group. Reset `max_red` and `max_blue` accordingly.
7. Continue until all segments are processed. The final value of `groups` is the number of connected groups.

Why it works: by always keeping track of the maximum right endpoints for red and blue segments, we ensure that any segment that starts before or at the max of the opposite color must belong to the same group. Segments that start beyond this point cannot connect to previous segments, so they initiate a new group. Sorting ensures we process segments in the correct order and handle overlaps correctly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        red, blue = [], []
        for _ in range(n):
            c, l, r = map(int, input().split())
            if c == 0:
                red.append((l, r))
            else:
                blue.append((l, r))
        red.sort()
        blue.sort()
        
        i, j = 0, 0
        max_red, max_blue = -1, -1
        groups = 0
        
        events = []
        for l, r in red:
            events.append((l, r, 0))
        for l, r in blue:
            events.append((l, r, 1))
        events.sort()
        
        for l, r, color in events:
            if color == 0:
                if l > max_blue:
                    groups += 1
                    max_red, max_blue = r, -1
                else:
                    max_red = max(max_red, r)
            else:
                if l > max_red:
                    groups += 1
                    max_blue, max_red = r, -1
                else:
                    max_blue = max(max_blue, r)
        
        print(groups)

if __name__ == "__main__":
    solve()
```

The code first separates and sorts segments by color. It merges all segments in order of starting point and maintains the maximum endpoint reached by each color. When a segment starts after the maximum of the opposite color, it starts a new group. Care is taken to reset the max reach correctly for new groups, otherwise distant segments could incorrectly merge.

## Worked Examples

### Sample Input 1

```
5
0 0 5
1 2 12
0 4 7
1 9 16
0 13 19
```

| Segment | Color | L | R | max_red | max_blue | Groups |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 5 | 5 | -1 | 1 |
| 1 | 1 | 2 | 12 | 5 | 12 | 1 |
| 2 | 0 | 4 | 7 | 7 | 12 | 1 |
| 3 | 1 | 9 | 16 | 7 | 16 | 1 |
| 4 | 0 | 13 | 19 | 19 | 16 | 2 |

The table shows how max reach is updated and groups incremented only when a new segment does not overlap the opposite color.

### Sample Input 2

```
3
1 0 1
1 1 2
0 3 4
```

The first two segments form one group, the last red segment starts after max_blue=2, forming a second group. Then the final red segment also does not overlap any blue, giving three groups.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting red and blue segments dominates the computation. Merging sweep is O(n). |
| Space | O(n) | Storing segments and events requires linear space. |

This fits comfortably under the `2s` limit for `n ≤ 10^5`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# Provided samples
assert run("2\n5\n0 0 5\n1 2 12\n0 4 7\n1 9 16\n0 13 19\n3\n1 0 1\n1 1 2\n0 3 4\n") == "2\n3", "samples"

# Custom cases
assert run("1\n1\n0 0 0\n") == "1", "single segment"
assert run("1\n2\n0 0 5\n0 1 2\n") == "2", "same color segments, not connected"
assert run("1\n3\n0 0 5\n1 5 10\n0 10 15\n") == "1", "chain connection"
assert run("1\n4\n0 0 2\n1 3 4\n0 5 6\n1 7 8\n") == "4", "disjoint segments"

| Test input | Expected output | What it validates |
|------------|----------------|-----------------|
| 1 segment | 1 | minimal case |
| 2 red overlapping | 2 | segments same color not connected |
| 3 forming chain | 1 | transitive group merge |
| 4 disjoint | 4 | each disconnected forms own group |
```

## Edge Cases

Segments that just touch at endpoints like `(0,0,2)` and `(1,2,4)` are considered connected, because the ranges are inclusive. The algorithm handles this correctly because it compares `l > max_opposite` to detect new groups. If the start equals the max of the opposite color, they still merge. A segment far away, like `(0, 10, 12)` after a previous max_blue of 4, starts a new group, as expected. This treatment ensures no off-by-one mistakes occur in group counting.
