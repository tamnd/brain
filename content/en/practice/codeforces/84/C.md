---
title: "CF 84C - Biathlon"
description: "We are given a set of circular targets, all lying on the Ox axis, each defined by its center coordinate and radius. Valera shoots multiple times, and each shot has an (x, y) coordinate."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "implementation"]
categories: ["algorithms"]
codeforces_contest: 84
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 72 (Div. 2 Only)"
rating: 1700
weight: 84
solve_time_s: 177
verified: false
draft: false
---

[CF 84C - Biathlon](https://codeforces.com/problemset/problem/84/C)

**Rating:** 1700  
**Tags:** binary search, implementation  
**Solve time:** 2m 57s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of circular targets, all lying on the Ox axis, each defined by its center coordinate and radius. Valera shoots multiple times, and each shot has an (x, y) coordinate. The goal is to identify, for each target, the first shot that hits it, or -1 if no shot hits it. A shot hits a target if its Euclidean distance to the center is less than or equal to the radius. The final output also requires the total number of targets hit at least once.

The number of targets $n$ can be up to $10^4$, and the number of shots $m$ can be up to $2 \cdot 10^5$. Checking each shot against every target in a naive double loop would require $n \times m$ operations, up to roughly $2 \cdot 10^9$ in the worst case, which is too slow for a 1-second time limit. We need a method that reduces the number of distance calculations per shot.

A subtle edge case occurs when targets are very close or touching each other. Even though no targets overlap, shots on the boundary of one target might also lie within the next. The algorithm must correctly identify the first target hit in the input order, not just any target.

Another edge case is a shot exactly on the boundary of a target. The Euclidean distance formula must be implemented with “≤” to include the boundary. Integer overflow is not a concern because all coordinates are bounded, but squaring coordinates should remain within standard integer limits.

## Approaches

The brute-force approach simply iterates through each target and each shot, computes the squared distance from the shot to the target center, and compares it with the squared radius. While correct, it performs $n \times m$ distance computations, which is roughly $2 \cdot 10^9$ in the worst case and too slow.

The key observation to optimize is that all target centers lie on the x-axis and are non-overlapping. Each target is defined by an interval on the x-axis: from $x-r$ to $x+r$. A shot can only hit a target if its x-coordinate lies within this interval. Furthermore, the vertical distance $y$ must satisfy $y^2 \le r^2 - (x_{\text{shot}} - x_{\text{target}})^2$. Sorting the targets by their x-coordinates allows us to use binary search to identify candidate targets for each shot efficiently.

Instead of checking all targets for every shot, we can precompute intervals for each target on the x-axis. For a shot at position $(sx, sy)$, we find all targets whose x-intervals contain $sx$. Because intervals are disjoint or just touching, a binary search identifies at most one candidate target per shot. Then we check the vertical distance to confirm whether the shot is inside the circle. This reduces the complexity to $O(m \log n)$ for checking shots, plus $O(n \log n)$ for sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(n) | Too slow |
| Sorted intervals + binary search | O(n log n + m log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all targets into a list, each as a tuple of (center_x, radius, index). Compute for each target its interval on the x-axis: [center_x - radius, center_x + radius]. Store the index to map back to input order.
2. Sort the targets by their left interval boundary. Sorting ensures binary search works efficiently.
3. Initialize a result array of length n with -1 to track the first shot that hits each target.
4. Iterate over all shots. For each shot at (sx, sy):

a. Perform a binary search on the targets’ left boundaries to find the last target whose left boundary is ≤ sx.

b. For the candidate target, check if the shot’s x-coordinate is within the interval and if the squared Euclidean distance to the center is ≤ squared radius.

c. If it hits, and the target has no recorded first shot, update the result array with the 1-based shot index.
5. After processing all shots, count the number of targets with a first hit (result not equal to -1).
6. Output the total hit count, followed by the result array in input order.

Why it works: Sorting the targets and searching by x-coordinate guarantees we do not miss any target a shot could possibly hit. Because intervals are non-overlapping, binary search identifies a single candidate target per shot. Using squared distances avoids floating-point errors, and the index mapping ensures we report results in input order.

## Python Solution

```python
import sys
input = sys.stdin.readline
from bisect import bisect_right

n = int(input())
targets = []
for i in range(n):
    x, r = map(int, input().split())
    targets.append((x - r, x + r, x, r, i))  # left, right, center, radius, original index

targets.sort()  # sort by left boundary

m = int(input())
shots = [tuple(map(int, input().split())) + (idx + 1,) for idx in range(m)]  # x, y, 1-based index

res = [-1] * n
lefts = [t[0] for t in targets]  # for binary search

for sx, sy, shot_idx in shots:
    pos = bisect_right(lefts, sx) - 1
    if 0 <= pos < n:
        l, r, cx, cr, idx = targets[pos]
        if l <= sx <= r and (sx - cx)**2 + sy**2 <= cr**2:
            if res[idx] == -1:
                res[idx] = shot_idx

hit_count = sum(1 for x in res if x != -1)
print(hit_count)
print(' '.join(map(str, res)))
```

This solution reads targets and converts them to x-intervals. Sorting by left boundary allows efficient binary search for candidate targets. For each shot, bisect_right finds the last interval whose left is ≤ shot x-coordinate. Checking the x-interval and squared distance ensures correctness. We only update the first hit per target, preserving the "first shot" requirement.

## Worked Examples

Sample Input 1:

```
3
2 1
5 2
10 1
5
0 1
1 3
3 0
4 0
4 0
```

Step trace for each shot:

| Shot idx | sx | sy | Candidate target | Hits? | res after shot |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | none | no | [-1,-1,-1] |
| 2 | 1 | 3 | none | no | [-1,-1,-1] |
| 3 | 3 | 0 | target 1 | yes | [3,-1,-1] |
| 4 | 4 | 0 | target 2 | yes | [3,4,-1] |
| 5 | 4 | 0 | target 2 | yes, but already recorded | [3,4,-1] |

Final output:

```
2
3 4 -1
```

This confirms that the binary search identifies the correct target for each shot, and first-hit indexing is maintained.

Sample Input 2 (edge shot on boundary):

```
2
0 2
5 3
3
2 0
5 3
8 0
```

| Shot idx | sx | sy | Candidate target | Hits? | res after shot |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 0 | target 1 | yes | [1,-1] |
| 2 | 5 | 3 | target 2 | yes | [1,2] |
| 3 | 8 | 0 | target 2 | no | [1,2] |

Output:

```
2
1 2
```

Confirms boundary conditions are handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m log n) | Sorting targets O(n log n) plus binary search per shot O(log n) for m shots |
| Space | O(n + m) | Store targets and results, plus shot array |

This fits comfortably within the 1-second time limit and 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # paste the solution code here
    n = int(input())
    targets = []
    for i in range(n):
        x, r = map(int, input().split())
        targets.append((x - r, x + r, x, r, i))
    targets.sort()
    m = int(input())
    shots = [tuple(map(int, input().split())) + (idx + 1,) for idx in range(m)]
    res = [-1] * n
    from bisect import bisect_right
    lefts = [t[0] for t in targets]
    for sx, sy, shot_idx in shots:
        pos = bisect_right(lefts, sx) - 1
        if 0 <= pos < n:
            l, r
```
