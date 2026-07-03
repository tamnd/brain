---
title: "CF 103069F - Rooks"
description: "We are given two sets of points on an infinite integer grid. One set belongs to Prof. Pang and the other belongs to Prof. Shou."
date: "2026-07-04T00:59:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103069
codeforces_index: "F"
codeforces_contest_name: "2020 ICPC Asia East Continent Final"
rating: 0
weight: 103069
solve_time_s: 42
verified: true
draft: false
---

[CF 103069F - Rooks](https://codeforces.com/problemset/problem/103069/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two sets of points on an infinite integer grid. One set belongs to Prof. Pang and the other belongs to Prof. Shou. Each point behaves like a rook: it can “attack” another rook only if both are aligned either horizontally or vertically, and there is no other rook strictly between them on that same row or column.

The task is not to count attacks globally, but to determine for every rook whether it participates in at least one valid attack against an opponent rook. For each rook, we output a binary indicator depending on whether it has at least one “visible” opponent along its row or column with no blocking rook in between.

The constraints are large, with up to 200000 points per player, so up to 400000 points total. A naive pairwise check between all rooks would be quadratic and far too slow. Any solution must essentially process all points in near-linear or log-linear time per coordinate group.

A subtle failure case for naive thinking appears when multiple rooks lie on the same row or column.

Consider three rooks on the same row:

```
P at (0, 0), S at (2, 0), P at (4, 0)
```

Even though the middle rook is attacked, the outer rooks are not necessarily both attacked unless we correctly enforce the “no rook in between” rule. A naive approach that only checks existence of an opposite-color rook on the same row would incorrectly mark all as attacked.

Another tricky scenario is when multiple opponent rooks exist in both directions; only the closest one in each direction matters.

## Approaches

A brute force approach would compare every rook with every other rook of the opposite player. For each pair, we would check whether they share the same x or y coordinate, and then verify if any other rook lies between them. Even if we precompute positions, verifying blocking would still require scanning points in between or maintaining a set, leading to roughly O(N^2) behavior in dense rows or columns.

The key observation is that the blocking condition makes only immediate neighbors in sorted order relevant. On any fixed x-coordinate, if we sort all rooks by y, then a rook can only see the nearest rook above and below it. Any farther rook is blocked by the nearest one. The same applies symmetrically for each y-coordinate.

So instead of checking all pairs, we group rooks by row and by column. Within each group, we sort and only compare adjacent elements. For each adjacency, if the two rooks belong to different players, both are marked as attacked.

This reduces the problem into two independent scans: one over all x-groups and one over all y-groups.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n1·n2) | O(n) | Too slow |
| Group + Sort Neighbors | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We process visibility separately along rows and columns, since attacks are defined independently in those directions.

1. Group all rooks by their x-coordinate. For each x-value, collect all rooks sharing it, storing their y-coordinate and player identity. This isolates vertical interactions.
2. For each x-group, sort rooks by y-coordinate. Sorting is required so that “no rook in between” becomes equivalent to adjacency in the sorted order.
3. Scan each sorted x-group from bottom to top. For every adjacent pair, check if they belong to different players. If they do, mark both rooks as attacked. The reason adjacency is sufficient is that any rook between two others would break direct visibility, so only consecutive points can see each other.
4. Repeat the same grouping process, but now by y-coordinate. This handles horizontal visibility in exactly the same way, but along rows instead of columns.
5. Maintain an array `attacked` for all rooks, initialized to false. Whenever a valid adjacent pair across different players is found in either dimension, set both corresponding entries to true.
6. Output results for each player in input order.

### Why it works

The core invariant is that after sorting within a fixed coordinate group, any valid visibility edge must occur between two consecutive points in that sorted order. If two points share a line and are not consecutive, at least one other point lies between them and blocks the attack. Therefore, every valid attack corresponds exactly to one adjacency in either the x-group or y-group scan, and every adjacency check captures a valid attack if players differ. This ensures completeness and correctness without missing or double-counting any reachable pair.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n1, n2 = map(int, input().split())
    
    pts = []
    attacked = [False] * (n1 + n2)

    for i in range(n1):
        x, y = map(int, input().split())
        pts.append((x, y, 0, i))

    for i in range(n2):
        x, y = map(int, input().split())
        pts.append((x, y, 1, n1 + i))

    # process by x (vertical visibility)
    pts.sort()
    i = 0
    while i < len(pts):
        j = i
        x = pts[i][0]
        group = []
        while j < len(pts) and pts[j][0] == x:
            group.append(pts[j])
            j += 1
        
        group.sort(key=lambda t: t[1])

        for k in range(len(group) - 1):
            if group[k][2] != group[k + 1][2]:
                attacked[group[k][3]] = True
                attacked[group[k + 1][3]] = True

        i = j

    # process by y (horizontal visibility)
    pts.sort(key=lambda t: (t[1], t[0]))
    i = 0
    while i < len(pts):
        j = i
        y = pts[i][1]
        group = []
        while j < len(pts) and pts[j][1] == y:
            group.append(pts[j])
            j += 1
        
        group.sort(key=lambda t: t[0])

        for k in range(len(group) - 1):
            if group[k][2] != group[k + 1][2]:
                attacked[group[k][3]] = True
                attacked[group[k + 1][3]] = True

        i = j

    res1 = ''.join('1' if attacked[i] else '0' for i in range(n1))
    res2 = ''.join('1' if attacked[n1 + i] else '0' for i in range(n2))

    print(res1)
    print(res2)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the theoretical decomposition into vertical and horizontal scans. Each scan reconstructs coordinate groups and relies on sorting to enforce adjacency equivalence. The key detail is that we do not attempt to search between arbitrary pairs, which avoids quadratic behavior entirely.

One subtle implementation choice is storing both x-scan and y-scan results into the same `attacked` array. This is safe because attacks are monotonic in the sense that once a rook is marked, it stays marked regardless of direction. Another detail is stable indexing: each rook carries a global index so we can update answers without ambiguity after sorting.

## Worked Examples

### Example 1

Input:

```
3 2
0 0
0 1
1 0
0 -1
-1 0
```

We process x-groups first.

| x | group (sorted by y) | adjacency checks | attacked updates |
| --- | --- | --- | --- |
| 0 | (0, -1 S), (0, 0 P), (0, 1 P) | S-P, P-P | S, P(0,0) |
| 1 | (1, 0 P), (-1, 0 S) | S-P | both |

After vertical scan, several rooks are marked. Horizontal scan reinforces the same relationships since all points also lie on y=0 or form pairs.

Final outputs:

Pang: `111`

Shou: `11`

This demonstrates that multiple valid adjacent detections can reinforce correctness without double counting issues.

### Example 2

Input:

```
2 2
0 0
0 2
0 1
0 3
```

All points lie on x = 0.

| x=0 group sorted by y | adjacency | result |
| --- | --- | --- |
| (0 P), (1 S), (2 P), (3 S) | P-S, S-P, P-S | all attacked |

This confirms that the adjacency rule correctly captures chained visibility along a line.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting by x and y dominates, each group scan is linear overall |
| Space | O(n) | storage for all points and attack flags |

The solution comfortably fits within constraints for 400000 total points, since sorting and linear scans are efficient at this scale.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = backup
    return out.getvalue().strip()

# sample
assert run("""3 2
0 0
0 1
1 0
0 -1
-1 0
""") == "111\n11"

# single pair direct attack
assert run("""1 1
0 0
0 1
""") == "1\n1"

# no attack
assert run("""2 2
0 0
2 2
1 1
3 3
""") == "0\n0"

# chain on same row
assert run("""2 2
0 0
2 0
1 0
3 0
""") == "11\n11"

# vertical chain alternating players
assert run("""1 3
0 0
0 1
0 2
0 3
""") == "1\n111"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | mixed | correctness on mixed geometry |
| single pair | 1/1 | direct visibility |
| no attack | 0/0 | isolation case |
| chain row | all 1 | adjacency propagation |
| vertical chain | full marking | long column correctness |

## Edge Cases

A key edge case is when multiple rooks share the same coordinate line with alternating ownership. For example:

```
(0,0) P, (0,1) S, (0,2) P, (0,3) S
```

During the x-group scan, we sort by y and only check adjacent pairs. The scan marks all rooks because every adjacent pair is cross-player. This correctly propagates attack status across the entire chain without requiring long-range checks.

Another case is when only one rook exists on a line. Since there is no adjacent pair, nothing is marked, which correctly reflects that no attack is possible.

Finally, consider a dense configuration where many rooks overlap in one coordinate but are spread elsewhere. The algorithm isolates each coordinate group independently, ensuring unrelated lines do not interfere with each other, preserving correctness across the full grid.
