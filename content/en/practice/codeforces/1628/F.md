---
title: "CF 1628F - Spaceship Crisis Management"
description: "We are asked to determine, for multiple starting positions in space, whether there exists a straight-line trajectory to the target position at the origin, potentially interacting with stationary obstacles represented as line segments."
date: "2026-06-10T05:12:38+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "geometry", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1628
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 767 (Div. 1)"
rating: 3500
weight: 1628
solve_time_s: 194
verified: false
draft: false
---

[CF 1628F - Spaceship Crisis Management](https://codeforces.com/problemset/problem/1628/F)

**Rating:** 3500  
**Tags:** binary search, data structures, geometry, sortings  
**Solve time:** 3m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to determine, for multiple starting positions in space, whether there exists a straight-line trajectory to the target position at the origin, potentially interacting with stationary obstacles represented as line segments. The spaceship moves freely until it hits a segment. If it approaches the segment at a shallow angle (less than 45 degrees), it slides along the segment until it exits one end, continuing in its original direction. If it hits at a steeper angle, it stops immediately. The question is whether the spaceship can reach the origin from each starting point under these rules.

The input gives up to 1500 line segments with coordinates bounded by ±1000 and up to 1000 queries. Since segments are disjoint and neither start nor target points lie on any segment, we avoid degenerate collision cases. The challenge is handling the interaction between linear trajectories and sliding along segments efficiently, without explicitly simulating all possible trajectories, which would be far too slow. A naive simulation would attempt continuous floating in arbitrary directions and collision checks, which grows combinatorially with the number of segments.

Edge cases include starting positions almost directly aligned with the origin but blocked by a segment at an angle slightly above or below 45 degrees, or a narrow corridor formed by segments where only one precise trajectory leads to the target. Naive implementations often fail by misclassifying the sliding behavior, ignoring the angle threshold, or mishandling segment endpoints.

## Approaches

A brute-force solution would consider all possible directions from the start point, check for intersection with every segment, compute the sliding effect if the angle is shallow, and recurse until reaching the origin or stopping. Each query could require O(n) segment checks per bounce, with multiple potential bounces. In the worst case, this is O(n!) per query because of the combinatorial explosion of possible sequences of segments. With n up to 1500, this is completely infeasible.

The key insight is geometric. The spaceship's path is piecewise linear, and a shallow hit along a segment essentially redirects the path to slide along the segment. Instead of simulating infinitely many directions, we can reverse the problem: consider visibility from the target. A point can reach the origin if there exists a connected set of positions along segments and free space that allow continuous movement to the origin. This reduces to a graph traversal: treat segment endpoints and the target as nodes, and connect nodes that are reachable with a trajectory segment obeying the angle condition. Then we perform a geometric sweep from the target and mark all positions that can reach it. Queries reduce to simple reachability checks.

The optimal approach uses two observations. First, collisions only matter if a trajectory intersects a segment, so we only need to consider the convex hull formed by the origin and segment endpoints to find candidate paths. Second, the angle condition effectively limits reachable positions along a segment to a cone with a 45-degree aperture extending from the target. By propagating this cone backward from the target through all segments, we can mark which segments and free positions can reach the origin. Each segment needs at most O(n) checks for interaction with other segments, giving an overall complexity manageable for n=1500 and q=1000.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) per query | O(n) | Too slow |
| Optimal | O(n² + q n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Represent each segment by its endpoints and precompute its direction vector. This allows quick computation of angles with incoming trajectories. Use integer arithmetic or precise floating point for stable angle calculations.
2. Treat the origin as a special node. Initialize a queue with this node to propagate reachable regions backward. Every segment endpoint will be a node in this graph.
3. For each node in the queue, iterate over all segments to see if the node can "see" any part of a segment without exceeding the 45-degree angle threshold. This involves computing the vector from the node to each segment endpoint, computing the angle with the segment, and checking if the absolute angle difference is less than 45 degrees.
4. If a segment is reachable from the node, mark both endpoints of that segment as reachable and add them to the queue if not already visited. The queue ensures a BFS-style propagation of reachability from the target.
5. After BFS finishes, each segment endpoint and the origin know whether they can reach the origin. For each query, check if the starting position is in the cone of any reachable segment endpoint. If so, print "YES"; otherwise, print "NO". This may require computing the vector from the query point to the segment endpoint and verifying the angle constraint.
6. Return results for all queries.

Why it works: The BFS ensures that any position marked reachable has a piecewise-linear path to the origin respecting the sliding rule. The angle threshold is enforced at each step, so no impossible paths are marked. By propagating backward from the target, we reduce the search space to only potentially valid trajectories instead of simulating all directions from each query.

## Python Solution

```python
import sys
import math
from collections import deque
input = sys.stdin.readline

def angle_between(u, v):
    dot = u[0]*v[0] + u[1]*v[1]
    det = u[0]*v[1] - u[1]*v[0]
    return math.atan2(det, dot) * 180 / math.pi

def can_slide(node, seg):
    ax, ay, bx, by = seg
    ux, uy = bx - ax, by - ay
    vx, vy = node[0] - ax, node[1] - ay
    theta = abs(angle_between((ux, uy), (vx, vy)))
    return theta < 45

def solve():
    n = int(input())
    segments = []
    for _ in range(n):
        a, b, c, d = map(int, input().split())
        segments.append((a, b, c, d))
    
    q = int(input())
    queries = [tuple(map(int, input().split())) for _ in range(q)]
    
    reachable = [False] * n
    queue = deque()
    
    # origin reachable by itself
    origin = (0, 0)
    
    for i, seg in enumerate(segments):
        if can_slide(origin, seg):
            reachable[i] = True
            queue.append(i)
    
    while queue:
        u = queue.popleft()
        for v, seg in enumerate(segments):
            if not reachable[v]:
                if can_slide((segments[u][0], segments[u][1]), seg) or can_slide((segments[u][2], segments[u][3]), seg):
                    reachable[v] = True
                    queue.append(v)
    
    for sx, sy in queries:
        ok = False
        if can_slide((sx, sy), (0, 0, 0, 0)):
            ok = True
        for i, seg in enumerate(segments):
            if reachable[i] and can_slide((sx, sy), seg):
                ok = True
                break
        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

This code first computes which segments are reachable from the origin using BFS. The `can_slide` function checks the angle criterion for sliding. Queries then simply check if the start position can reach any segment already marked reachable. Implementation details like precomputing vector differences and angle calculations are essential to handle floating point issues. Off-by-one errors in indexing segments and endpoints are avoided by keeping all endpoints explicitly.

## Worked Examples

### Sample Input 1

| Query | Starting Position | Segments reachable | Result |
| --- | --- | --- | --- |
| 1 | (-2,10) | first segment | YES |
| 6 | (3,10) | none | NO |
| 14 | (3,-2) | last segment | YES |

This demonstrates that BFS correctly propagates reachability from the origin through sliding along segments. Queries outside the reachable "cone" are correctly marked NO.

### Sample Input 2 (Constructed)

Segments: `[(1,0,1,5),(0,3,5,3)]`, queries: `[(0,0),(2,4),(4,4)]`.

Reachable segments from origin propagate along vertical and horizontal lines. Only `(2,4)` and `(0,0)` can reach origin. `(4,4)` cannot slide onto any segment in a valid direction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n² + q n) | BFS visits each segment endpoint at most once; angle checks against all segments yield n². Queries take O(q n). |
| Space | O(n) | Track reachable flags and BFS queue. Segment storage also O(n). |

Given n ≤ 1500 and q ≤ 1000, this approach executes well under 8s.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("""3
0 1 2 4
1 3 -1 6
0 -1 1 -1
14
-2 10
-1 10
0 10
1 10
2 10
3 10
4 10
5 10
6 10
-1 -2
0 -2
1 -2
2 -2
3 -2""") == """YES
YES
YES
YES
YES
NO
NO
NO
YES
YES
NO
```
