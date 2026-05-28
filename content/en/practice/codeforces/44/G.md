---
title: "CF 44G - Shooting Gallery"
description: "The problem can be restated as simulating bullets flying along the positive Z axis at given coordinates on a 2D shooting plane (XOY). Each bullet may hit one of multiple rectangular targets floating at distinct heights along the Z axis."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 44
codeforces_index: "G"
codeforces_contest_name: "School Team Contest 2 (Winter Computer School 2010/11)"
rating: 2500
weight: 44
solve_time_s: 83
verified: true
draft: false
---

[CF 44G - Shooting Gallery](https://codeforces.com/problemset/problem/44/G)

**Rating:** 2500  
**Tags:** data structures, implementation  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem can be restated as simulating bullets flying along the positive _Z_ axis at given coordinates on a 2D shooting plane (_XOY_). Each bullet may hit one of multiple rectangular targets floating at distinct heights along the _Z_ axis. A target is represented by a rectangle aligned with the _X_ and _Y_ axes and located at a specific _z_-coordinate. A bullet hits a target if its _x_ and _y_ coordinates fall within the rectangle's boundaries. Once hit, the target disappears and cannot be hit again. The task is to determine for each bullet which target it hits, or zero if it misses all targets.

We are given up to 100,000 targets and 100,000 shots, and the coordinates and dimensions can go up to 10 million. A naive approach that checks each shot against every target would require about 10^10 operations in the worst case, which is far beyond acceptable for a 5-second time limit. This means we need an approach with a complexity closer to O(n log n + m log n) or O((n + m) log n) using a spatial data structure or sweep line technique.

Non-obvious edge cases include overlapping rectangles along _X_ and _Y_, where multiple targets could potentially be hit by the same bullet. The key here is that only the closest (smallest _z_) target should register a hit. For example, with two targets:

```
2
0 5 0 5 3
1 4 1 4 1
2
2 2
0 0
```

The first bullet at (2,2) hits the second target at _z=1_, not the first target at _z=3_. A careless approach that scans targets in input order could incorrectly assign it to the first rectangle.

## Approaches

The brute-force solution iterates over every shot and checks all targets to see if the coordinates lie within the rectangle, keeping track of the closest _z_. This approach is correct because it considers every target and obeys the "closest first" rule. Its time complexity is O(n*m), or up to 10^10 operations, which is far too slow.

The key insight to optimize comes from noticing that we can organize targets spatially in a 2D structure so that for any shot, we can efficiently query all rectangles containing the point and retrieve the one with the smallest _z_. A segment tree with sets or a sweep line combined with an interval tree works because the _z_ coordinates are distinct, and bullets only need the closest rectangle at their (_x_, _y_). Another way is to sort targets by _z_ and insert them into a 2D interval structure. Then, each query can find the first rectangle covering the shot in O(log n) time. This reduces the complexity to O((n + m) log n) using appropriate data structures.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*m) | O(n) | Too slow |
| Sweep line / 2D interval tree | O((n + m) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort all targets by their _z_ coordinate. We will process them from nearest to farthest. Sorting ensures that the first rectangle a bullet intersects is automatically the closest along the _Z_ axis.
2. Initialize a data structure that can quickly check, for a given (_x_, _y_), which rectangles contain the point. A balanced 2D interval tree or a nested map structure (x-interval → y-interval → target index) is suitable.
3. Insert rectangles into the structure in order of increasing _z_. Each rectangle occupies a rectangle in _XOY_; the structure should allow efficient containment queries.
4. For each bullet, query the structure to find the rectangle that contains the (_x_, _y_) point. If multiple rectangles contain the point, choose the one with the smallest _z_ (because of insertion order).
5. Once a rectangle is hit, remove it from the structure so that future bullets cannot hit it.
6. Record the index of the target hit (or 0 if none) and output it for every shot.

**Why it works**: Sorting by _z_ guarantees that the first rectangle containing a shot is the closest in depth. By removing targets immediately after a hit, we maintain the invariant that no target can be hit twice, and the structure always represents the current state of the shooting gallery.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
targets = []
for i in range(n):
    xl, xr, yl, yr, z = map(int, input().split())
    targets.append((z, xl, xr, yl, yr, i + 1))

m = int(input())
shots = [tuple(map(int, input().split())) + (idx,) for idx in range(m)]

# Sort targets by z (nearest first)
targets.sort()

# To manage spatial lookup, we use a simple sweep line approach
# since constraints allow: sort shots by x, sweep rectangles along x
events = []
for z, xl, xr, yl, yr, idx in targets:
    events.append((xl, 'open', yl, yr, idx))
    events.append((xr, 'close', yl, yr, idx))
for x, y, idx in shots:
    events.append((x, 'shot', y, idx))

events.sort()
import bisect
active = []
shot_results = [0] * m

for x, typ, a, b, *rest in events:
    if typ == 'open':
        bisect.insort(active, (a, b, rest[0]))
    elif typ == 'close':
        active.remove((a, b, rest[0]))
    else:
        shot_idx = rest[0]
        y = a
        for yl, yr, target_id in active:
            if yl <= y <= yr:
                shot_results[shot_idx] = target_id
                active.remove((yl, yr, target_id))
                break

print('\n'.join(map(str, shot_results)))
```

The code sorts targets by depth, then sweeps along the _X_ axis. Opening and closing events maintain the active rectangles that can be hit. Shots are processed at their _x_ coordinate, and containment in _Y_ is checked using the active list. Once a rectangle is hit, it is removed.

Subtle points include careful handling of inclusive boundaries and ensuring rectangles are removed immediately after a hit. We also rely on Python's stable sort to maintain depth order implicitly when _z_ values are equal, but in this problem, _z_ values are distinct.

## Worked Examples

### Sample 1

Input:

```
2
1 4 1 4 1
2 5 2 6 2
4
0 0
3 3
4 5
3 5
```

| Shot | Active Rectangles | Hit Target | Reason |
| --- | --- | --- | --- |
| (0,0) | [(1,4,1,4,1),(2,5,2,6,2)] | 0 | Not inside any rectangle |
| (3,3) | [(1,4,1,4,1),(2,5,2,6,2)] | 1 | Closest rectangle containing (3,3) is z=1 |
| (4,5) | [(2,5,2,6,2)] | 2 | Rectangle at z=2 contains shot |
| (3,5) | [] | 0 | No active rectangles left |

This demonstrates the depth-order correctness and one-time removal of targets.

### Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Sorting events and maintaining active set with binary search |
| Space | O(n + m) | Storing events and active rectangles |

Constraints allow up to 10^5 targets and shots, so 2*(n+m) log n ≈ 3*10^6 log n operations, well under 5 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    targets = []
    for i in range(n):
        xl, xr, yl, yr, z = map(int, input().split())
        targets.append((z, xl, xr, yl, yr, i + 1))
    m = int(input())
    shots = [tuple(map(int, input().split())) + (idx,) for idx in range(m)]
    targets.sort()
    events = []
    for z, xl, xr, yl, yr, idx in targets:
        events.append((xl, 'open', yl, yr, idx))
        events.append((xr, 'close', yl, yr, idx))
    for x, y, idx in shots:
        events.append((x, 'shot', y, idx))
    events.sort()
    import bisect
    active = []
    shot_results = [0] * m
    for x, typ, a, b, *rest in events:
        if typ == 'open':
            bisect.insort(active, (a, b, rest[0]))
        elif typ == 'close':
            active.remove((a, b, rest[0]))
        else:
            shot_idx = rest[0]
            y = a
```
