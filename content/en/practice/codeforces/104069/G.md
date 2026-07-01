---
title: "CF 104069G - Grand Meeting"
description: "We are given a linear metro line with stations arranged in a fixed west to east order. Each station is connected to the next one, and moving between adjacent stations always takes exactly one minute."
date: "2026-07-02T03:00:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104069
codeforces_index: "G"
codeforces_contest_name: "VII MaratonUSP Freshman Contest"
rating: 0
weight: 104069
solve_time_s: 43
verified: true
draft: false
---

[CF 104069G - Grand Meeting](https://codeforces.com/problemset/problem/104069/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a linear metro line with stations arranged in a fixed west to east order. Each station is connected to the next one, and moving between adjacent stations always takes exactly one minute. Two people start at two different stations at the same time and both move along this line. The task is to determine the minimum time until they can be at the same station at the same moment.

The input gives the number of stations, followed by the ordered list of station names along the line. After that, we are given two station names indicating the starting positions of the two people. The output is a single integer: the earliest time at which they can occupy the same station if both start moving immediately and travel optimally along the line.

The key structure is that the graph is not a general graph but a simple path. Every station has at most two neighbors, and movement is deterministic in distance: the time between any two stations is just their index difference in the list.

The constraints are small, with at most 100 stations and station names of length up to 100. This immediately tells us that even a quadratic or naive approach over all pairs of stations would be trivial to run within limits. The real challenge is not performance but translating the meeting condition correctly into a shortest time expression.

A subtle point is that the two people do not need to meet by walking toward each other explicitly. They can move arbitrarily along the line, and the meeting time is the minimum over all possible meeting stations. A naive interpretation might incorrectly assume they must meet halfway or only consider one direction, which would miss the optimal meeting point.

Edge cases worth noting include when both start at the same station, where the answer is zero, and when the optimal meeting point is one of the starting positions, meaning one person waits in place while the other arrives.

## Approaches

The brute-force way to think about the problem is to consider every station as a potential meeting point. For each station, compute the time it takes for both people to reach it, which is just the absolute difference between indices in the station list. The meeting time for that station is the maximum of the two arrival times, since both must be there simultaneously. The answer is the minimum of this value over all stations.

This works because every valid meeting must happen at some station, and the time is fully determined by distances on a line. The issue is that if we implemented this without structure, we would repeatedly scan or recompute distances unnecessarily, but even that is fine given n is only 100.

The key simplification is recognizing that station names can be mapped directly to indices. Once we know the indices of the two starting stations, the problem reduces to minimizing max(|i - k|, |j - k|) over all k. On a line, this expression is minimized when k lies between i and j, and the optimal value becomes exactly half the distance between them, rounded up.

This gives a direct formula: the answer is (|i - j| + 1) // 2.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all meeting stations | O(n) | O(1) | Accepted |
| Index mapping + direct formula | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of stations and store the list in order. The order is crucial because it defines the metric structure of the graph.
2. Build a mapping from station name to its index in the list. This allows constant-time lookup of positions.
3. Retrieve the indices of the two starting stations. Let them be i and j.
4. Compute the absolute distance between them on the line. This distance represents the shortest time for one to reach the other if they move directly.
5. Return half of this distance rounded up, since both can move toward each other simultaneously and each minute reduces their separation by at most two total steps.

Why it works: on a path, any meeting point k induces arrival times |i - k| and |j - k|. The meeting time is the maximum of these two values. This function is minimized when k lies between i and j, because moving k toward the interval reduces the larger of the two distances. Once k is inside the segment, the best balance is achieved when both sides shrink symmetrically, which leads to splitting the total distance between i and j. Since movement is discrete in whole minutes, the result is the ceiling of half the distance.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
stations = []
pos = {}

for i in range(n):
    name = input().strip()
    stations.append(name)
    pos[name] = i

c, m = input().split()
i = pos[c]
j = pos[m]

dist = abs(i - j)
print((dist + 1) // 2)
```

The implementation relies entirely on converting station names into indices, which avoids any repeated scanning. The dictionary ensures O(1) access to positions. The final expression `(dist + 1) // 2` is a compact way of computing the ceiling of half the distance, which matches the optimal meeting time on a line.

A common mistake is attempting to simulate movement step by step, but that is unnecessary because the structure guarantees a closed-form solution. Another potential issue is forgetting that both move simultaneously, which is why the distance shrinks by up to two per minute, not one.

## Worked Examples

### Example 1

Input:

```
7
butanta
pinheiros
faria
fradique
oscar
paulista
luz
pinheiros oscar
```

Indices are:

pinheiros = 1, oscar = 4

| Step | i | j | dist | answer |
| --- | --- | --- | --- | --- |
| init | 1 | 4 | 3 | - |
| compute | 1 | 4 | 3 | 2 |

The meeting time is 2 because they can move toward each other, reducing their separation from 3 to 0 in two synchronized steps.

### Example 2

Input:

```
5
a
b
c
d
e
a e
```

Indices:

a = 0, e = 4

| Step | i | j | dist | answer |
| --- | --- | --- | --- | --- |
| init | 0 | 4 | 4 | - |
| compute | 0 | 4 | 4 | 2 |

This shows a symmetric case where both endpoints move inward and meet in the middle after 2 minutes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | building the position map requires scanning all stations once |
| Space | O(n) | dictionary stores one entry per station |

The constraints allow up to 100 stations, so even if we used a less direct approach, performance would not be an issue. The solution comfortably runs within limits due to its linear preprocessing and constant-time query.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input().strip())
    stations = []
    pos = {}

    for i in range(n):
        name = input().strip()
        stations.append(name)
        pos[name] = i

    c, m = input().split()
    i = pos[c]
    j = pos[m]

    dist = abs(i - j)
    return str((dist + 1) // 2)

# provided sample
assert run("""7
butanta
pinheiros
faria
fradique
oscar
paulista
luz
pinheiros oscar
""") == "2"

# same start
assert run("""3
a
b
c
a a
""") == "0"

# adjacent
assert run("""3
a
b
c
a b
""") == "1"

# symmetric far ends
assert run("""5
a
b
c
d
e
a e
""") == "2"

# middle meeting
assert run("""5
a
b
c
d
e
b d
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| a a | 0 | identical start case |
| a b | 1 | adjacent stations |
| a e | 2 | symmetric endpoints |
| b d | 1 | meeting inside segment |

## Edge Cases

When both people start at the same station, the index difference is zero, so the computed distance is zero and the formula returns zero. The algorithm correctly handles this without special casing.

For adjacent stations, such as indices 2 and 3, the distance is one, so `(1 + 1) // 2 = 1`. This matches the fact that they meet after one minute if they move toward each other.

For extreme endpoints, such as indices 0 and n-1, the meeting occurs in the center region. The formula automatically captures this without needing to explicitly search for a midpoint, since it is derived from minimizing the maximum of two linear distances over a path.
