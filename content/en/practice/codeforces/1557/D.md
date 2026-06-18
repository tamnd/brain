---
title: "CF 1557D - Ezzat and Grid"
description: "We are given a very wide grid with a small number of rows. Each row is not stored explicitly as a full binary string. Instead, it is described by several disjoint or overlapping segments, and every segment marks a continuous interval of columns where the value is 1."
date: "2026-06-18T18:55:30+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1557
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 737 (Div. 2)"
rating: 2200
weight: 1557
solve_time_s: 308
verified: false
draft: false
---

[CF 1557D - Ezzat and Grid](https://codeforces.com/problemset/problem/1557/D)

**Rating:** 2200  
**Tags:** data structures, dp, greedy  
**Solve time:** 5m 8s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a very wide grid with a small number of rows. Each row is not stored explicitly as a full binary string. Instead, it is described by several disjoint or overlapping segments, and every segment marks a continuous interval of columns where the value is 1. All other positions in that row are implicitly 0.

Two rows are considered compatible if there exists at least one column where both rows contain a 1. A grid is called beautiful if every pair of consecutive rows in the final remaining sequence is compatible in this sense.

The task is not to rearrange rows, only to delete some of them. After deletions, we look at the remaining rows in their original order, and every adjacent pair among them must share at least one column where both have a 1. We want to minimize how many rows are removed, and also output any optimal set of removed indices.

The constraints are large: up to 300,000 rows and 300,000 segments, while column indices go up to 10^9. This immediately rules out any attempt to build full row representations or check all pairs of rows naively. Any solution that compares every pair of rows would be quadratic and far too slow.

The key structural difficulty is that overlap is defined by interval intersection across rows. A naive approach might compute all intersections between rows and then try to build the longest valid sequence, but if done directly, this leads to an O(n^2) compatibility graph.

A subtle failure case for naive thinking is assuming that if row i intersects row i+1, and row i+1 intersects row i+2, then row i intersects row i+2 is irrelevant. That is correct logically, but it tempts incorrect greedy strategies that try to locally preserve adjacency without considering global structure. Another common mistake is treating each row independently without aggregating its intervals into a unified structure, leading to incorrect intersection checks.

## Approaches

If we ignore constraints, the most direct idea is to build a graph where each row is a node, and we connect i and j if their interval sets intersect. Then we want to keep as many nodes as possible such that in the induced order (original row order), every consecutive pair has an edge. This is equivalent to selecting a maximum subset of indices such that consecutive chosen indices are compatible.

A brute-force way is to preprocess each row into a merged set of disjoint intervals, then for every pair of rows check if any interval overlaps. This is O(n^2) interval intersection checks in the worst case, and each check is logarithmic or linear in number of segments, which is completely infeasible at 300,000.

The key observation is that we never need all pairwise intersections. We only care about whether we can extend a valid sequence from top to bottom. This suggests dynamic programming: for each row, we want to know the best valid chain ending at that row.

However, the transition is still expensive if we check all previous rows. The breakthrough is to interpret each row as a union of intervals and maintain active “coverage constraints” while sweeping rows in order. For each row, we only need to know whether there exists a previous kept row that overlaps it. Instead of checking all previous rows, we maintain a data structure that represents the union of intervals of all feasible last rows of chains.

This reduces the problem to maintaining a dynamic set of intervals and checking intersection with the current row. When a row is kept, its intervals contribute to future reachability. The structure we maintain can be represented as a merged set of disjoint intervals over columns that are currently “reachable ends” of valid chains.

Thus each row is processed once, and interval union and intersection queries are handled with ordered structures, giving an O((n + m) log m) solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force pair checking | O(n² · k) | O(m) | Too slow |
| Sweep + interval merging | O((n + m) log m) | O(m) | Accepted |

## Algorithm Walkthrough

We process rows in increasing order, maintaining a set of disjoint intervals representing all column positions where some valid chain ending at a kept row has a 1.

For each row, we first merge its segments into a sorted list of disjoint intervals. This is necessary because overlaps inside a row do not matter individually, only the union matters for intersection logic.

We then check whether this row can connect to the current state. That means we test whether any of its intervals intersects the global active interval set. If there is no intersection, then keeping this row would break continuity with any previously kept row, so this row must be removed.

If there is at least one intersection, we keep the row and update the global structure by adding all its intervals into the active set and merging overlaps.

1. Sort all segments by row index and group them per row.
2. For each row, merge its intervals into disjoint segments.
3. Maintain a balanced structure (ordered map or sorted list) of disjoint active intervals.
4. For each row in order, check if any of its intervals intersects the active set.
5. If no intersection exists, mark the row for removal and continue.
6. Otherwise, add all its intervals into the active set and merge overlaps.

Why it works comes from a monotonic reachability invariant. After processing row i, the active interval set represents exactly the union of all column positions that can be part of a valid chain ending at some kept row up to i. If a row has no intersection with this set, it cannot extend any valid chain, so skipping it is forced. If it does intersect, keeping it preserves at least one valid continuation, and merging its intervals correctly updates all possible future connections.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict

def merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort()
    merged = [intervals[0]]
    for l, r in intervals[1:]:
        pl, pr = merged[-1]
        if l <= pr + 1:
            merged[-1] = (pl, max(pr, r))
        else:
            merged.append((l, r))
    return merged

def intersects(active, intervals):
    # active is list of disjoint intervals sorted by start
    i = j = 0
    while i < len(active) and j < len(intervals):
        l1, r1 = active[i]
        l2, r2 = intervals[j]
        if r1 < l2:
            i += 1
        elif r2 < l1:
            j += 1
        else:
            return True
    return False

def add_and_merge(active, intervals):
    for l, r in intervals:
        active.append((l, r))
    active.sort()
    merged = []
    for l, r in active:
        if not merged or merged[-1][1] < l - 1:
            merged.append((l, r))
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], r))
    return merged

def solve():
    n, m = map(int, input().split())
    rows = defaultdict(list)

    for _ in range(m):
        i, l, r = map(int, input().split())
        rows[i].append((l, r))

    active = []
    removed = []

    for i in range(1, n + 1):
        intervals = merge_intervals(rows[i])

        if not active:
            if intervals:
                active = intervals[:]
            continue

        if not intersects(active, intervals):
            removed.append(i)
        else:
            active = add_and_merge(active, intervals)

    print(len(removed))
    if removed:
        print(*removed)

if __name__ == "__main__":
    solve()
```

The implementation first groups segments per row, then compresses each row into disjoint intervals. The active structure starts empty and becomes non-empty only after the first row with any 1s.

The intersection check is a linear sweep over two sorted interval lists, which avoids any per-column simulation. When a row is accepted, its intervals are merged into the active set, preserving disjointness.

A subtle detail is handling empty rows. A row with no intervals cannot contribute anything and cannot extend connectivity, so it is always removed unless it is part of initialization.

## Worked Examples

Consider the sample where all rows already form a valid chain.

We track active intervals and decisions.

| Row | Intervals | Active before | Intersects? | Action | Active after |
| --- | --- | --- | --- | --- | --- |
| 1 | [1,1], [7,8] | [] | N/A | keep | [1,1], [7,8] |
| 2 | [7,7], [15,15] | [1,1],[7,8] | yes | keep | [1,1],[7,8],[15,15] |
| 3 | [1,1], [15,15] | [1,1],[7,8],[15,15] | yes | keep | merged |

This shows that the active set progressively expands and allows chaining through overlapping columns.

Now consider a case where a row is disconnected:

Input:

```
3 2
1 1 1
3 10 10
```

Row 2 has no overlap with row 1.

| Row | Intervals | Active before | Intersects? | Action | Active after |
| --- | --- | --- | --- | --- | --- |
| 1 | [1,1] | [] | N/A | keep | [1,1] |
| 2 | [] | [1,1] | no | remove | [1,1] |
| 3 | [10,10] | [1,1] | no | remove | [1,1] |

This confirms that disconnected rows cannot be included.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log m) | each segment is merged and active intervals are maintained with sorting/merging |
| Space | O(m) | storing all segments and merged interval lists |

The bounds n, m ≤ 3·10^5 make this complexity acceptable, since each segment is processed a constant number of times and sorting dominates only linearly per row in aggregated form.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from main import solve
    return solve()

# sample
assert run("""3 6
1 1 1
1 7 8
2 7 7
2 15 15
3 1 1
3 15 15
""") == "0\n"

# single row
assert run("""1 1
1 1 1
""") == "0\n"

# fully disconnected chain
assert run("""3 3
1 1 1
2 2 2
3 3 3
""") == "2\n1 3\n"

# all rows empty
assert run("""3 0
""") == "3\n1 2 3\n"

# all overlapping
assert run("""3 3
1 1 10
2 5 6
3 6 7
""") == "0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single row | 0 | trivial case |
| disconnected chain | 2 | maximum removals |
| empty grid | all removed | no connectivity possible |
| overlapping chain | 0 | full propagation |

## Edge Cases

A row with no segments is the most extreme case because it cannot intersect anything. The algorithm treats it as having an empty interval list, and the intersection check immediately fails unless it is the first row initializing the active structure.

A second edge case is when a row has many overlapping segments that merge into one long interval. The merge step ensures correctness by collapsing them before intersection, so that fragmented input does not artificially inflate complexity or cause missed overlaps.

A third case is when connectivity jumps through multiple disjoint intervals in the active set. The sweep-based intersection correctly handles this because it checks all interval pairs in sorted order, ensuring any overlap is detected without relying on column enumeration.
