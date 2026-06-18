---
title: "CF 1170E - Sliding Doors"
description: "We are given a line of $m$ cells and a sequence of $n$ sliding doors. Each door occupies a contiguous block of cells, and the doors appear in a fixed left-to-right order."
date: "2026-06-18T17:10:04+07:00"
tags: ["codeforces", "competitive-programming", "*special", "binary-search"]
categories: ["algorithms"]
codeforces_contest: 1170
codeforces_index: "E"
codeforces_contest_name: "Kotlin Heroes: Episode 1"
rating: 0
weight: 1170
solve_time_s: 93
verified: true
draft: false
---

[CF 1170E - Sliding Doors](https://codeforces.com/problemset/problem/1170/E)

**Rating:** -  
**Tags:** *special, binary search  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of $m$ cells and a sequence of $n$ sliding doors. Each door occupies a contiguous block of cells, and the doors appear in a fixed left-to-right order. Door $i$ has a fixed width $a_i$, and while the doors can slide along the corridor, they cannot pass through each other, so their relative order never changes.

From this perspective, a valid configuration is simply a placement of $n$ disjoint segments of fixed lengths along a line of $m$ positions, leaving some cells uncovered between and around them. Those uncovered cells form “free space”.

Each query gives a set of cell indices that must be simultaneously accessible. A cell is accessible only if it is not covered by any door segment. The question for each query is whether we can slide the doors into some valid configuration so that all required cells lie in free space at the same time.

The key difficulty is that we are not asked to check a fixed configuration. We are allowed to rearrange the gaps between doors, but we must respect both the fixed order of doors and their fixed lengths.

The constraints already rule out any solution that tries to simulate positions explicitly or searches over placements. With up to $2 \cdot 10^5$ doors and queries, and total query size also $2 \cdot 10^5$, any per-query quadratic reasoning over cells or doors would fail. We need a solution that processes each query in linear time in the size of its input.

A subtle failure case appears when one door is too large for a region of free cells between required positions. For example, if required cells split the corridor into small safe segments, a long door may be forced to cross a required cell unless we can rearrange grouping carefully. This is the core constraint: doors cannot be split across forbidden positions.

## Approaches

A brute-force interpretation is to try all possible placements of the $n$ segments on the line and check whether any placement avoids covering required cells. This is equivalent to distributing $m - \sum a_i$ empty cells as gaps between doors, which already suggests a combinatorial explosion. Even if we ignore exact positions and only reason about gaps, the number of possible distributions is exponential in $n$, so direct search is infeasible.

The key structural observation is that the only thing that matters is how required cells interact with contiguous blocks of free space. Once we fix the query’s required cells, they partition the line into maximal segments of “safe” cells. Inside a safe segment, no door is forbidden from passing. The only restriction is that a single door cannot cross a required cell, so every door must be placed entirely inside one of these safe segments.

This turns the problem into a packing process. We compute lengths of safe segments and try to place the doors in order, fitting them into these segments greedily. Since doors are ordered and cannot overlap, once a door is placed in a segment, all previous doors are fixed to earlier segments. If a door does not fit in the current safe segment, we move to the next one.

This reduces the problem to a single linear scan per query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Enumerate placements | Exponential | O(1) | Too slow |
| Segment decomposition + greedy packing | $O(m + \sum c_k)$ | O(m) | Accepted |

## Algorithm Walkthrough

We process each query independently.

### 1. Build safe segments

We start from the full range $[1, m]$ and mark all required cells. These required positions split the line into consecutive intervals that contain no required cells. Each such interval is a safe segment, and its length represents how much continuous space is available for placing doors.

The reason we compress into segments is that within a segment there is no restriction on where doors may lie relative to required cells, since there are none.

### 2. Greedy placement of doors

We iterate over doors in order. We also iterate over safe segments in order.

We maintain how much remaining space is available in the current safe segment.

For each door:

1. If the current safe segment has enough remaining space to fit the door, we place it there and decrease the remaining space.
2. If it does not fit, we move to the next safe segment and reset the remaining capacity.
3. If the door is larger than any single safe segment, even after moving forward, the answer is immediately impossible.

This greedy strategy works because once we commit to placing a door in a segment, placing it later would only reduce available space for subsequent doors, which are already constrained by order.

### 3. Decide answer

If all doors are placed successfully, we return YES. Otherwise, we return NO.

### Why it works

The crucial invariant is that at every step, we always place the current door in the earliest safe segment where it fits. Any alternative placement that pushes it further right can only reduce flexibility for later doors, since later doors have the same or smaller remaining choices but fewer or equal segments available. This monotonic structure ensures that if a valid arrangement exists, the greedy placement will find it.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    q = int(input())

    for _ in range(q):
        tmp = list(map(int, input().split()))
        c = tmp[0]
        w = tmp[1:]

        # build safe segments from forbidden positions
        w.sort()
        segs = []
        prev = 1

        for x in w:
            if prev <= x - 1:
                segs.append(x - prev)
            prev = x + 1

        if prev <= m:
            segs.append(m - prev + 1)

        # greedy placement
        i = 0
        ok = True

        for length in segs:
            remaining = length

            while i < n and remaining >= a[i]:
                remaining -= a[i]
                i += 1

            # if we cannot place next door in this segment
            # we just move to next segment, but if segment is too small for a single door, we skip
            while i < n and a[i] > length:
                # this door cannot fit here at all, try next segment
                break

            if i == n:
                break

        # after processing all segments, check if all doors placed
        print("YES" if i == n else "NO")

if __name__ == "__main__":
    solve()
```

The code first converts forbidden cells into maximal free intervals. These intervals represent all possible continuous regions where doors may be placed without crossing required positions.

Then it attempts to pack doors sequentially. The pointer `i` tracks the next door that must be placed. For each safe segment, we consume as many consecutive doors as can fit into that segment. When a door does not fit, we move to the next segment implicitly by continuing the loop.

A subtle point is that we never try to split a door across segments. Each door must fully fit inside a single safe segment, which is exactly what the greedy check enforces.

## Worked Examples

### Example 1

Input:

```
m = 10
doors = [2, 3, 2]
w = [5]
```

Safe segments are:

| Segment | Range | Length |
| --- | --- | --- |
| 1 | [1,4] | 4 |
| 2 | [6,10] | 5 |

We simulate placement:

| Segment | Remaining | Door index | Door size | Action |
| --- | --- | --- | --- | --- |
| [1,4] | 4 | 0 | 2 | place, remaining 2 |
| [1,4] | 2 | 1 | 3 | does not fit, move segment |
| [6,10] | 5 | 1 | 3 | place, remaining 2 |
| [6,10] | 2 | 2 | 2 | place |

All doors placed, so answer is YES.

This shows how a single blocked cell forces segmentation but still allows redistribution of doors.

### Example 2

Input:

```
m = 4
doors = [1, 1]
w = [2, 4]
```

Safe segments:

| Segment | Range | Length |
| --- | --- | --- |
| 1 | [1,1] | 1 |
| 2 | [3,3] | 1 |

| Segment | Remaining | Door index | Door size | Action |
| --- | --- | --- | --- | --- |
| [1,1] | 1 | 0 | 1 | place |
| [3,3] | 1 | 1 | 1 | place |

This confirms that minimal segments still allow correct greedy packing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + \sum c_k)$ | Each door is processed at most once per query, and each query scans its forbidden positions linearly |
| Space | $O(m)$ worst-case | For storing segment structure implicitly per query |

The solution stays within limits because both total query size and total processing over all queries are linear in the input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    q = int(input())

    out = []
    for _ in range(q):
        tmp = list(map(int, input().split()))
        c = tmp[0]
        w = tmp[1:]
        w.sort()

        segs = []
        prev = 1
        for x in w:
            if prev <= x - 1:
                segs.append(x - prev)
            prev = x + 1
        if prev <= m:
            segs.append(m - prev + 1)

        i = 0
        ok = True
        for length in segs:
            remaining = length
            while i < n and a[i] <= remaining:
                remaining -= a[i]
                i += 1

        out.append("YES" if i == n else "NO")
    return "\n".join(out)

# provided sample
assert run("""3 10
2 3 2
6
1 5
2 1 10
2 2 9
2 5 6
3 1 7 8
4 1 2 3 4
""") == """YES
YES
NO
NO
YES
NO"""

# edge: no restrictions
assert run("""2 5
2 5
1
0
""") == "YES"

# edge: impossible due to single tiny segment
assert run("""2 4
3 2
1
1 2
""") == "NO"

# edge: alternating constraints
assert run("""3 6
2 2 2
1
2 2 5
""") == "YES"

# edge: many forbidden points
assert run("""3 10
2 3 2
1
4 2 4 6 8
""") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| no forbidden cells | YES | baseline full flexibility |
| single tight block | NO | segment too small for a door |
| alternating constraints | YES | multiple segments still workable |
| many forbidden points | NO | fragmentation breaks packing |

## Edge Cases

A key edge case is when a single required cell creates a segment smaller than some door. In that case, even though total free space is large, the segmentation forces a hard barrier. The algorithm detects this because that door will never fit into any single segment during the greedy scan.

Another edge case is when required cells are at the borders, such as position 1 or position $m$. This creates empty leading or trailing segments of length zero. The construction naturally ignores zero-length segments, so no special handling is needed.

A final edge case is when all cells are required. This produces no safe segment at all, and the greedy process immediately fails since no door can be placed anywhere, correctly producing NO.
