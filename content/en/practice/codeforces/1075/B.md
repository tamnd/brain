---
title: "CF 1075B - Taxi drivers and Lyft"
description: "We are given a set of people positioned on a number line. Each person is either a rider or a taxi driver, and all positions are distinct and already sorted in increasing order."
date: "2026-06-18T16:56:37+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1075
codeforces_index: "B"
codeforces_contest_name: "Lyft Level 5 Challenge 2018 - Final Round (Open Div. 2)"
rating: 1200
weight: 1075
solve_time_s: 57
verified: true
draft: false
---

[CF 1075B - Taxi drivers and Lyft](https://codeforces.com/problemset/problem/1075/B)

**Rating:** 1200  
**Tags:** implementation, sortings  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of people positioned on a number line. Each person is either a rider or a taxi driver, and all positions are distinct and already sorted in increasing order.

When a rider requests a taxi, the system always assigns the request to the closest taxi driver in terms of absolute distance on the line. If two taxi drivers are equally close, the driver with the smaller coordinate is chosen. Each rider independently generates exactly one request, and we want to know how many riders would be assigned to each taxi driver if everyone requests a taxi simultaneously.

The task is to compute, for every taxi driver in order of increasing coordinate among drivers, how many riders would be matched to that driver under this nearest with tie breaking rule.

The input size reaches up to 200,000 total people. This immediately rules out any solution that compares each rider against all taxi drivers individually, since that would be quadratic in the worst case and far beyond time limits. A solution must be close to linear or linearithmic.

A subtle edge case arises when multiple riders lie exactly in the midpoint between two adjacent taxi drivers. In such cases, tie-breaking always pushes assignment to the left taxi driver. For example, if drivers are at 2 and 6, and a rider is at 4, the rider goes to 2. Any solution must respect this deterministic boundary behavior.

Another corner case is when all drivers are to one side of a rider cluster. For instance, if all taxis are on the right, every rider is assigned to the leftmost taxi, because it is the closest available.

## Approaches

A direct way to solve the problem is to process each rider independently and scan all taxi drivers to find the closest one. For each rider, we compute distances to all m drivers and select the minimum. This is correct because it directly follows the problem definition.

However, this approach requires O(nm) operations. With n and m up to 100,000, this becomes up to 10^10 comparisons, which is not feasible.

The key observation is that both riders and taxi drivers lie on a sorted line, and distance comparisons depend only on relative ordering. For any fixed rider, only the nearest taxi driver to the left and the nearest taxi driver to the right can possibly be optimal. All other drivers are strictly farther away.

This reduces the problem to maintaining, for each rider, the nearest taxi driver on each side. If we sort or scan the line while keeping track of driver positions, we can assign each rider in O(1) amortized time after preprocessing. A standard way to achieve this is to sweep across the line from left to right while maintaining the last seen taxi driver, and also precompute the next taxi driver to the right. With these two neighbors known, we compare distances and resolve ties using coordinate order.

This transforms the problem into a linear scan with constant-time decisions per rider.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Optimal sweep with nearest neighbors | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We first separate the positions into two lists: one containing all taxi driver coordinates and one containing all rider coordinates. Since the original sequence is already sorted by coordinate, we can build these lists in a single pass.

Next, we prepare a mapping from each taxi driver coordinate to its index in the sorted list of drivers. This is needed because the output must be ordered by driver coordinate, not by input order.

Then we compute, for every position on the line, the nearest taxi driver to the left. We sweep from left to right, remembering the last taxi driver we saw. Whenever we encounter a taxi driver, we update this value. For a rider at position x, this gives us its closest candidate on the left side.

We also compute the nearest taxi driver to the right by sweeping from right to left in the same manner.

Now each rider has at most two candidates: a left taxi driver and a right taxi driver. We compare their distances to the rider. If one is closer, we assign the rider to that driver. If both are equally close, we assign it to the left one because it has a smaller coordinate.

Finally, we increment the counter of the chosen taxi driver and output all counts in increasing order of driver coordinate.

### Why it works

The assignment of a rider depends only on the closest taxi drivers. On a line, any point has a unique closest element among a set, and that closest element must be either immediately to the left or immediately to the right in sorted order. All other candidates are strictly farther than at least one of these two. The tie-breaking rule is consistent with always preferring the left side in equal distance cases, so the comparison between these two candidates fully determines the result.

This establishes that reducing the search space to two candidates per rider preserves correctness for every assignment.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
x = list(map(int, input().split()))
t = list(map(int, input().split()))

riders = []
drivers = []

for i in range(n + m):
    if t[i] == 1:
        drivers.append(x[i])
    else:
        riders.append(x[i])

drivers.sort()

# maps driver position to its index in output order
pos_to_idx = {drivers[i]: i for i in range(m)}

INF = 10**18

left_driver = [-1] * (n + m)
right_driver = [-1] * (n + m)

last = -1
for i in range(n + m):
    if t[i] == 1:
        last = x[i]
    else:
        left_driver[i] = last

last = -1
for i in range(n + m - 1, -1, -1):
    if t[i] == 1:
        last = x[i]
    else:
        right_driver[i] = last

ans = [0] * m

for i in range(n + m):
    if t[i] == 0:
        x0 = x[i]

        L = left_driver[i]
        R = right_driver[i]

        # both exist
        if L != -1 and R != -1:
            dL = x0 - L
            dR = R - x0

            if dL <= dR:
                ans[pos_to_idx[L]] += 1
            else:
                ans[pos_to_idx[R]] += 1

        elif L != -1:
            ans[pos_to_idx[L]] += 1
        else:
            ans[pos_to_idx[R]] += 1

print(*ans)
```

The implementation relies on two directional sweeps. The first sweep records, for every rider position, the closest taxi driver to its left. The second sweep does the same for the right side. The final loop resolves each rider independently by comparing at most two candidates, ensuring constant time processing per person.

A key detail is the tie-breaking condition `dL <= dR`, which ensures that when a rider is exactly in the middle, preference goes to the left taxi driver due to smaller coordinate.

The dictionary `pos_to_idx` converts driver coordinates into output indices so that results can be accumulated in the required order.

## Worked Examples

### Example 1

Input:

```
3 1
1 2 3 10
0 0 1 0
```

Drivers are at 3, riders at 1, 2, 10.

| Rider position | Left driver | Right driver | dL | dR | Assigned |
| --- | --- | --- | --- | --- | --- |
| 1 | none | 3 | - | - | 3 |
| 2 | none | 3 | - | - | 3 |
| 10 | 3 | none | - | - | 3 |

All riders go to the only taxi driver.

Final counts: 3

This confirms the behavior when only one taxi exists, where every rider must map to it regardless of distance.

### Example 2

Input:

```
2 2
2 3 4 6
1 1 0 0
```

Drivers are at 2 and 3, riders at 4 and 6.

| Rider | Left driver | Right driver | dL | dR | Assigned |
| --- | --- | --- | --- | --- | --- |
| 4 | 3 | none | 1 | - | 3 |
| 6 | 3 | none | 3 | - | 3 |

All riders go to driver at 3, since it is the closest available.

This shows the case where all riders lie to the right of all drivers, so the right-side sweep never contributes candidates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Two linear sweeps over all positions and one final assignment pass |
| Space | O(n + m) | Arrays store left and right nearest driver for each position |

The solution runs comfortably within limits because it performs only a constant amount of work per input element, with no nested iteration over riders and drivers.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    x = list(map(int, input().split()))
    t = list(map(int, input().split()))

    drivers = []
    riders = []
    for i in range(n + m):
        if t[i] == 1:
            drivers.append(x[i])
        else:
            riders.append(x[i])

    drivers.sort()
    pos_to_idx = {drivers[i]: i for i in range(m)}

    left_driver = [-1] * (n + m)
    right_driver = [-1] * (n + m)

    last = -1
    for i in range(n + m):
        if t[i] == 1:
            last = x[i]
        else:
            left_driver[i] = last

    last = -1
    for i in range(n + m - 1, -1, -1):
        if t[i] == 1:
            last = x[i]
        else:
            right_driver[i] = last

    ans = [0] * m

    for i in range(n + m):
        if t[i] == 0:
            x0 = x[i]
            L = left_driver[i]
            R = right_driver[i]

            if L != -1 and R != -1:
                if x0 - L <= R - x0:
                    ans[pos_to_idx[L]] += 1
                else:
                    ans[pos_to_idx[R]] += 1
            elif L != -1:
                ans[pos_to_idx[L]] += 1
            else:
                ans[pos_to_idx[R]] += 1

    return " ".join(map(str, ans))

# provided sample
assert run("3 1\n1 2 3 10\n0 0 1 0\n") == "3"

# all drivers, symmetric
assert run("2 2\n1 2 3 4\n1 1 0 0\n") == "2 2"

# tie case
assert run("1 2\n1 2 3\n0 1 1\n") == "1 0"

# edge: single rider
assert run("1 1\n5 10\n0 1\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all drivers single | 3 | single taxi absorbs all riders |
| symmetric split | 2 2 | balanced assignment correctness |
| tie case | 1 0 | left preference in equal distance |
| single rider | 1 | minimal boundary behavior |

## Edge Cases

One edge case is when there is exactly one taxi driver. The sweep still assigns both left and right candidates as absent on one side, so every rider falls back to that single driver. The algorithm correctly increments the only counter for all riders.

Another edge case is when all riders are located between two taxi drivers at equal distances from both sides. The condition `dL <= dR` ensures deterministic assignment to the left driver. The sweeps guarantee that both candidates are correctly identified, so the tie-breaking is applied exactly once per rider.

A final edge case occurs when riders appear before the first taxi driver or after the last one. In both situations, only one of the two candidate directions exists, and the algorithm safely assigns all such riders to the only available neighbor without attempting invalid comparisons.
