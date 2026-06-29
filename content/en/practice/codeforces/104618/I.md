---
title: "CF 104618I - Magic Sprinkles"
description: "We are given a set of points in the plane, each representing a sprinkle placed somewhere above the x-axis, since all y-coordinates are strictly positive. Each sprinkle has a color, either red or blue."
date: "2026-06-29T17:31:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104618
codeforces_index: "I"
codeforces_contest_name: "UTPC Contest 09-22-23 Div. 1"
rating: 0
weight: 104618
solve_time_s: 74
verified: false
draft: false
---

[CF 104618I - Magic Sprinkles](https://codeforces.com/problemset/problem/104618/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of points in the plane, each representing a sprinkle placed somewhere above the x-axis, since all y-coordinates are strictly positive. Each sprinkle has a color, either red or blue. Bob stands fixed at the origin and chooses a geometric region shaped like a circular sector with vertex at the origin. This region is unbounded in radius but restricted to an angular interval, so geometrically it corresponds to choosing two rays from the origin and taking all points between them in counterclockwise order.

A sprinkle is collected if it lies inside or on the boundary of this sector. Bob wants to choose one such sector that contains no blue points at all, while maximizing the number of red points inside it.

The input size can reach 200,000 points, so any approach that examines all pairs of points or all angular intervals explicitly will fail. A quadratic solution would require roughly 40 billion pair considerations in the worst case, which is far beyond what 2 seconds allows. This immediately suggests that the problem must reduce to a one-dimensional structure, most likely involving angular sorting around the origin.

A subtle issue comes from geometry on a circle. Even though all points lie in the upper half-plane, angles wrap around at the negative x-axis. Any solution must carefully handle the circular ordering of points by angle.

Another edge case appears when blue points lie between red clusters in angular order. A naive approach that simply takes a maximal consecutive block of red points in angular sorting is wrong because it may include blue points inside the interval or miss that the optimal sector can start and end at arbitrary points.

A third pitfall is treating the sector as a linear interval without handling the wrap-around case. The optimal sector may cross the positive x-axis direction, meaning angular intervals may need duplication to simulate circular continuity.

## Approaches

A brute-force idea is to consider every possible pair of points as the boundaries of the sector. For each ordered pair of points, we imagine a sector starting at the first angle and ending at the second angle in counterclockwise order, and then count how many red points lie inside while ensuring no blue points are included. This requires checking all points for each pair, leading to O(N^3) time complexity, or O(N^2) if counting is optimized with preprocessing but still too large for 200,000 points.

The key observation is that the only meaningful sector boundaries occur at angles defined by the given points. If we fix one boundary and rotate the other, the condition “no blue points inside” becomes a sliding window constraint over sorted angular order. This transforms the problem into finding the longest valid angular interval that contains no blue points and maximizes red points.

Once all points are converted into polar angles, we can sort them and duplicate the array to handle wrap-around. Then the problem becomes selecting a contiguous segment in this doubled circular array such that it contains no blue points and the number of red points is maximized. A two-pointer sweep maintains a window where no blue point is present; whenever a blue point enters the window, we move the left pointer forward until the constraint is restored.

Within each valid window, we track how many red points are included and take the maximum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over sector pairs | O(N^3) | O(N) | Too slow |
| Sort + two pointers on angles | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Convert each point (x, y) into a polar angle using atan2(y, x).

This ensures correct angular ordering around the origin, respecting quadrant structure.
2. Pair each angle with its color and sort the list by angle.

Sorting linearizes the circular geometry into a sequence.
3. Duplicate the sorted array by appending (angle + 2π, color) for each element.

This allows wrap-around intervals to be represented as normal subarrays.
4. Initialize two pointers l and r at the start of the doubled array and maintain a window.

The window represents the current candidate angular sector.
5. Expand r step by step, adding points into the window.

Each time we include a point, we update counts of red and blue points.
6. If a blue point appears in the window, move l forward until no blue remains.

This restores the validity condition that the sector must contain zero blue points.
7. Whenever the window is valid, compute the number of red points inside and update the answer.

The best sector must correspond to some maximal valid window boundary pair.
8. Ensure that the window length never exceeds N, since a valid sector cannot include more than a full rotation of unique points.

### Why it works

After sorting by angle, every valid sector corresponds to some contiguous interval on the circle. Duplicating the array converts circular intervals into linear ones without losing any candidate sector. The two-pointer process maintains the invariant that the current window contains no blue points, and any time a blue point enters, the left boundary is advanced just enough to remove it. This guarantees that every maximal valid angular interval is considered exactly once as the right pointer expands, so the maximum number of red points among all valid blue-free sectors is captured.

## Python Solution

```python
import sys
input = sys.stdin.readline

import math

def main():
    n = int(input())
    colors = input().strip()
    
    pts = []
    for i in range(n):
        x, y = map(int, input().split())
        ang = math.atan2(y, x)
        pts.append((ang, colors[i]))
    
    pts.sort()
    
    arr = pts + [(ang + 2 * math.pi, col) for ang, col in pts]
    
    l = 0
    red = 0
    blue = 0
    ans = 0
    
    for r in range(len(arr)):
        if arr[r][1] == 'r':
            red += 1
        else:
            blue += 1
        
        while blue > 0:
            if arr[l][1] == 'r':
                red -= 1
            else:
                blue -= 1
            l += 1
        
        ans = max(ans, red)
        
        if r - l + 1 > n:
            if arr[l][1] == 'r':
                red -= 1
            else:
                blue -= 1
            l += 1
    
    print(ans)

if __name__ == "__main__":
    main()
```

The implementation directly follows the angular sweep construction. The atan2 conversion is critical because it preserves correct ordering across all quadrants. Sorting ensures that any valid sector becomes a contiguous interval in angular space.

The duplication step is what enables wrap-around handling. Without it, a se
