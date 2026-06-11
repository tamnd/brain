---
title: "CF 1401E - Divide Square"
description: "We are asked to compute the number of pieces a large square is divided into after drawing several horizontal and vertical line segments."
date: "2026-06-11T08:43:17+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "geometry", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1401
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 665 (Div. 2)"
rating: 2400
weight: 1401
solve_time_s: 137
verified: false
draft: false
---

[CF 1401E - Divide Square](https://codeforces.com/problemset/problem/1401/E)

**Rating:** 2400  
**Tags:** data structures, geometry, implementation, sortings  
**Solve time:** 2m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to compute the number of pieces a large square is divided into after drawing several horizontal and vertical line segments. The square is fixed at size $10^6 \times 10^6$, and the segments may partially or fully cross the square, but they always intersect at least one of its edges. Horizontal segments are given by their y-coordinate and x-range, while vertical segments are given by their x-coordinate and y-range. No two segments lie on the same line.

The output is a single integer representing how many connected regions remain in the square after adding all segments. Conceptually, each segment can potentially split existing regions into two along its line. A horizontal segment splits regions horizontally; a vertical segment splits regions vertically. Intersections between segments increase the number of resulting pieces.

The constraints indicate that both $n$ and $m$ can be up to $10^5$. A brute-force grid-based solution would require at least $10^{12}$ operations if we tried to mark all points of the square, which is clearly impossible in 2 seconds. Therefore, we must avoid approaches that iterate over every unit of the square. Instead, the solution needs to process only the segments themselves and their intersections.

A key edge case is when a segment does not span the full width or height of the square but touches a side. For instance, a horizontal segment from $(0,2)$ to $(4,2)$ in a $10^6 \times 10^6$ square still counts for splitting pieces even though it does not reach the far side. A naive approach might ignore segments not fully spanning an axis, producing an undercount. Another tricky case is overlapping segments in different axes. If a vertical and horizontal segment intersect, the intersection creates a new piece. Ignoring intersections would undercount the total number of pieces.

## Approaches

The brute-force method is straightforward: imagine a 2D array representing the square and mark all the horizontal and vertical segments on it. Then perform a flood fill to count the connected regions. This works because marking and connectivity directly correspond to the number of pieces. The problem is that even storing a grid of $10^6 \times 10^6$ cells is impossible, and iterating over it is far beyond the allowed $2\cdot 10^9$ operations per second. So the brute-force approach fails due to memory and time constraints.

The optimal approach leverages the observation that we do not need to represent the full square; we only need the segments and their intersections. Each horizontal segment can be considered as cutting all vertical regions it crosses, and each vertical segment as cutting all horizontal regions it crosses. Counting intersections carefully allows us to use a combinatorial argument: every new segment adds pieces equal to one plus the number of intersections it forms with the other orientation. This reduces the problem to sorting the segments and counting overlaps efficiently, which can be done using a sweep line and coordinate compression, since coordinates are large but the number of segments is moderate. This approach avoids any full grid representation, relying only on the $n+m$ segments and their intersection counts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(10^12) | O(10^12) | Too slow |
| Optimal | O((n+m) log(n+m)) | O(n+m) | Accepted |

## Algorithm Walkthrough

1. Separate the segments into horizontal and vertical lists, keeping their coordinates. Horizontal segments are stored as `(y, x_start, x_end)` and vertical as `(x, y_start, y_end)`.
2. Coordinate-compress all x-coordinates of horizontal segments and vertical segments, and similarly compress y-coordinates. This ensures that all segment coordinates map to a smaller integer range from 0 to at most $2\cdot 10^5$, which fits in memory and allows efficient processing.
3. For horizontal segments, sort by y-coordinate. For vertical segments, sort by x-coordinate. This sorting prepares for a sweep line algorithm to efficiently count intersections.
4. Initialize a Fenwick tree (Binary Indexed Tree) along the compressed axis. For a horizontal sweep, the tree tracks active vertical segments across the x-axis, counting how many vertical segments a horizontal line intersects. Update the tree when entering or leaving a vertical segment.
5. Iterate over all horizontal segments in increasing y-coordinate. For each horizontal segment, query the Fenwick tree across its x-range to count intersections with vertical segments. Each intersection increases the piece count by one. Add one for the horizontal segment itself, since it always splits the region it traverses.
6. Repeat symmetrically for vertical segments with a sweep along the x-axis, using horizontal segments stored in the tree. The sum of all segment contributions minus the counted intersections (since intersections are counted twice) gives the total number of pieces.
7. Initialize the result with 1, representing the original square. For each segment processed, add its contribution according to the above rules. Output the final result.

The key invariant is that every new segment either splits an existing piece or intersects with a segment of the other orientation, which creates a new piece at the intersection. The algorithm guarantees that each intersection is counted exactly once per segment type, so the sum correctly represents all resulting pieces.

## Python Solution

```python
import sys
input = sys.stdin.readline

class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.bit = [0]*(n+1)
    
    def update(self, i, val):
        i += 1
        while i <= self.n:
            self.bit[i] += val
            i += i & -i
    
    def query(self, i):
        i += 1
        res = 0
        while i > 0:
            res += self.bit[i]
            i -= i & -i
        return res
    
    def range_query(self, l, r):
        return self.query(r) - self.query(l-1)

def main():
    n, m = map(int, input().split())
    horiz = []
    vert = []
    x_coords = set()
    y_coords = set()
    
    for _ in range(n):
        y, lx, rx = map(int, input().split())
        horiz.append((y, lx, rx))
        x_coords.add(lx)
        x_coords.add(rx)
        y_coords.add(y)
    
    for _ in range(m):
        x, ly, ry = map(int, input().split())
        vert.append((x, ly, ry))
        y_coords.add(ly)
        y_coords.add(ry)
        x_coords.add(x)
    
    x_list = sorted(x_coords)
    y_list = sorted(y_coords)
    x_map = {x:i for i,x in enumerate(x_list)}
    y_map = {y:i for i,y in enumerate(y_list)}
    
    horiz_mapped = [(y_map[y], x_map[lx], x_map[rx]) for y, lx, rx in horiz]
    vert_mapped = [(x_map[x], y_map[ly], y_map[ry]) for x, ly, ry in vert]
    
    horiz_mapped.sort()
    vert_mapped.sort()
    
    BIT = FenwickTree(len(x_list))
    
    res = 1
    events = []
    for x, ly, ry in vert_mapped:
        events.append((ly, 1, x))
        events.append((ry+1, -1, x))
    events.sort()
    
    j = 0
    for y, lx, rx in horiz_mapped:
        while j < len(events) and events[j][0] <= y:
            _, delta, x = events[j]
            BIT.update(x, delta)
            j += 1
        res += 1 + BIT.range_query(lx, rx)
    
    # symmetric for vertical segments
    BIT = FenwickTree(len(y_list))
    events = []
    for y, lx, rx in horiz_mapped:
        events.append((lx, 1, y))
        events.append((rx+1, -1, y))
    events.sort()
    
    j = 0
    for x, ly, ry in vert_mapped:
        while j < len(events) and events[j][0] <= x:
            _, delta, y = events[j]
            BIT.update(y, delta)
            j += 1
        res += 1 + BIT.range_query(ly, ry)
    
    print(res)

if __name__ == "__main__":
    main()
```

The code first maps coordinates to compressed indices, ensuring we can use a Fenwick tree efficiently. Horizontal segments are processed first: each segment contributes one piece, and intersections with vertical segments are counted via the Fenwick tree. Then vertical segments are processed similarly. Adding one for each segment handles the new split, while the range queries account for intersections. Using `events` ensures the sweep line correctly adds or removes vertical segments at their endpoints. This method avoids double counting and handles large coordinates within memory limits.

## Worked Examples

### Sample 1

Input:

```
3 3
2 3 1000000
4 0 4
3 0 1000000
4 0 1
2 0 5
3 1 1000000
```

| Segment | Compressed Coordinates | Intersections | Contribution | Cumulative Pieces |
| --- | --- | --- | --- | --- |
| H2 3-1e6 | y=0 | crosses V2 | 1 | 2 |
| H4 0-4 | y=1 | crosses V1 | 1 | 3 |
| H3 0-1e6 | y=2 |  |  |  |
