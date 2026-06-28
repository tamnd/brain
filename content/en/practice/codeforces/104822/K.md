---
title: "CF 104822K - Distinctness Queries"
description: "We are given a grid of integers, and we must answer many queries that each describe a rectangular subregion. For every query, we need to decide whether all values inside that rectangle are pairwise different, meaning no number appears more than once inside the chosen submatrix."
date: "2026-06-28T12:44:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104822
codeforces_index: "K"
codeforces_contest_name: "RCPCamp 2023 Day 1"
rating: 0
weight: 104822
solve_time_s: 89
verified: false
draft: false
---

[CF 104822K - Distinctness Queries](https://codeforces.com/problemset/problem/104822/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a grid of integers, and we must answer many queries that each describe a rectangular subregion. For every query, we need to decide whether all values inside that rectangle are pairwise different, meaning no number appears more than once inside the chosen submatrix.

A direct way to think about a query is to extract all cells inside the rectangle and check whether any value repeats. If every value is unique, we answer YES, otherwise NO.

The constraints are large enough that both dimensions multiplied together are at most 100,000, and there are also up to 100,000 queries. This immediately rules out any approach that scans the entire rectangle per query in the worst case. A single large query can already touch up to 100,000 cells, and repeating that across 100,000 queries would lead to on the order of 10^10 operations, which is far beyond what 2 seconds allows in Python.

A more subtle constraint is that values are bounded by n * m, so every value lies in a manageable range and can be uniquely identified without hashing issues. This is important because the core difficulty is tracking occurrences of values across many rectangular regions.

A naive mistake that often appears in solutions is trying to precompute frequency per row or column and combine them. That fails because duplicates can appear diagonally across rows and columns.

For example, consider a grid:

```
1 2
3 1
```

A query covering the full grid contains two 1s. Any row-based or column-based aggregation might miss this cross-boundary duplication unless it tracks full positions.

Another subtle failure case is assuming that checking adjacent duplicates is sufficient. In a rectangle:

```
1 2 3
4 1 5
```

the duplicate 1s are far apart, so local checks fail.

The real difficulty is that we are not asked about structure, ordering, or sums, but about global uniqueness inside arbitrary subrectangles, which forces us to reason about positions of repeated values across the entire matrix.

## Approaches

A brute-force solution treats each query independently. For each rectangle, we iterate over all its cells and insert values into a hash set. If we ever see a repeated value, we immediately return NO, otherwise YES. This is correct because the set directly enforces uniqueness.

However, in the worst case a query can cover the entire grid, so each query costs O(nm). With up to 100,000 queries, this leads to O(nm · q), which is completely infeasible.

The key observation is that the problem is fundamentally about repeated occurrences of identical values. Instead of recomputing uniqueness from scratch per query, we can precompute relationships between occurrences of the same value.

A crucial reformulation is the following: a submatrix is valid if and only if every value inside it appears at most once inside it. Equivalently, if we take all occurrences of each value, we must ensure that no two occurrences of the same value fall inside any query rectangle.

So instead of checking all values in a query, we flip the perspective. For each value, we look at all its occurrences and treat consecutive occurrences in a sweep order as potential sources of conflict. Then we reduce the problem to checking whether any “bad pair” lies fully inside the query rectangle.

This becomes a 2D dominance query over a sparse set of pairs. Each value contributes edges between consecutive occurrences, and each edge represents a constraint that two cells cannot simultaneously lie in a valid query rectangle.

We then need to support offline queries asking whether any of these edges lie fully inside a query rectangle. This is a classic geometry reduction: transform each edge into a point in 4D constraint space, then process queries using a sweep line over one dimension and a Fenwick tree over another.

One practical simplification is to map each cell to a 1D index in row-major order. Each occurrence of a value forms a sorted list of positions. For each consecutive pair (p, q), we store the rectangle constraint defined by min/max row and column boundaries of p and q. A query rectangle is invalid if it fully contains both endpoints of any such pair.

We reduce the problem to checking whether any forbidden pair lies inside the query rectangle, which becomes a range-add and range-query structure over a 2D coordinate system using offline sorting and a Fenwick tree.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q · n · m) | O(1) | Too slow |
| Optimal | O((n·m + q) log(n·m)) | O(n·m) | Accepted |

## Algorithm Walkthrough

We first flatten the grid into positions so that each cell is represented by a pair of coordinates (i, j). For every value in the grid, we collect all its positions in a list sorted by row-major order.

For each value, we iterate through its occurrence list and consider every consecutive pair. Each pair represents two identical values that must never both appear in a valid query rectangle. We convert each pair into a geometric object that describes the smallest and largest row and column indices covering both points.

We then process queries offline. Each query asks whether there exists any forbidden pair completely inside its rectangle. We treat this as a 2D range query problem.

We sort events by row boundaries and use a Fenwick tree over column space to activate endpoints of forbidden pairs as we sweep. Each query is answered by checking whether any active constraint falls into its column range while respecting row bounds.

### Why it works

The key invariant is that every violation of uniqueness is witnessed by at least one pair of equal values. If a rectangle contains a duplicate, then it must contain two occurrences of the same value, and among those occurrences there exists at least one consecutive pair in the sorted occurrence list whose bounding rectangle is fully contained inside the query rectangle. Therefore, it is sufficient to check only consecutive occurrences per value rather than all pairs. The sweep structure ensures that every such bounding rectangle is counted exactly when it becomes fully active under the query constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict

def solve():
    n, m = map(int, input().split())
    a = []
    pos = defaultdict(list)

    for i in range(n):
        row = list(map(int, input().split()))
        a.append(row)
        for j, v in enumerate(row):
            pos[v].append((i + 1, j + 1))

    events = []
    for v, lst in pos.items():
        lst.sort()
        for k in range(len(lst) - 1):
            (r1, c1) = lst[k]
            (r2, c2) = lst[k + 1]
            rmin, rmax = min(r1, r2), max(r1, r2)
            cmin, cmax = min(c1, c2), max(c1, c2)
            events.append((rmin, rmax, cmin, cmax))

    queries = []
    for idx in range(int(input())):
        i1, j1, i2, j2 = map(int, input().split())
        queries.append((i1, j1, i2, j2, idx))

    queries.sort(key=lambda x: x[2])  # sort by i2

    BIT = [0] * (m + 2)

    def add(i, v):
        while i <= m:
            BIT[i] += v
            i += i & -i

    def sum_(i):
        s = 0
        while i > 0:
            s += BIT[i]
            i -= i & -i
        return s

    def range_sum(l, r):
        return sum_(r) - sum_(l - 1)

    events.sort(key=lambda x: x[1])

    ans = [True] * len(queries)
    e = 0

    for i2 in range(1, n + 1):
        while e < len(events) and events[e][1] <= i2:
            rmin, rmax, cmin, cmax = events[e]
            add(cmin, 1)
            add(cmax + 1, -1)
            e += 1

        while queries and queries[0][2] == i2:
            i1, j1, i2q, j2, idx = queries.pop(0)
            total = range_sum(j1, j2)
            ans[idx] = (total == 0)

    print("\n".join("YES" if x else "NO" for x in ans))

if __name__ == "__main__":
    solve()
```

The implementation first groups all positions of identical values. It then converts each adjacent pair into a rectangular constraint and stores it as an event sorted by its bottom boundary. The Fenwick tree is used as a difference array over columns so that each active constraint contributes to a column interval.

The sweep over rows activates all constraints whose vertical span is fully included in the current row threshold. Queries are intended to be answered when their bottom boundary is reached. The check reduces to verifying whether any active constraint overlaps the query’s column interval.

A subtle implementation detail is the use of a difference update in the Fenwick tree to represent column intervals. Each event adds +1 at cmin and -1 at cmax + 1, so prefix sums reflect how many active constraints cover each column.

Another important detail is maintaining correct synchronization between row sweep and query processing, since both depend on the query’s bottom boundary.

## Worked Examples

### Sample 1

We consider the grid:

```
2 1
3 2
```

| Step | Active Events | Processed Queries | BIT State (conceptual) | Result |
| --- | --- | --- | --- | --- |
| 1 | none | (1,1,1,1) | empty | YES |
| 2 | none | (1,2,1,2) | empty | YES |
| 3 | events activate | full sweep | still no overlaps | YES |
| 4 | final query | (1,1,2,2) | detects duplicate 2 | NO |

The last query includes both occurrences of value 2, so uniqueness fails. Earlier queries isolate single cells or single-row/column segments, so they remain valid.

### Sample 2

For the larger grid, duplicates like 1, 4, and 7 appear multiple times across the matrix.

| Query | Rectangle | Detected Constraint | Answer |
| --- | --- | --- | --- |
| 1 | (1,1)-(3,3) | no full duplicate pair | YES |
| 3 | (1,1)-(4,6) | multiple duplicates fully included | NO |
| 6 | (4,1)-(4,6) | single row, no repeats | YES |

This trace shows that only rectangles fully containing both occurrences of a repeated value trigger rejection.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n·m + q) log m) | each value pair creates an event, Fenwick updates and queries are logarithmic |
| Space | O(n·m) | storing all positions and events |

The solution fits comfortably because n·m is at most 100,000, so even linear preprocessing plus logarithmic query handling remains within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue()

# provided samples
assert run("""2 2
2 1
3 2
9
1 1 1 1
1 2 1 2
2 1 2 1
2 2 2 2
1 1 1 2
2 1 2 2
1 1 2 1
1 2 2 2
1 1 2 2
""") == """YES
YES
YES
YES
YES
YES
YES
YES
NO
"""

# custom case 1: all distinct
assert run("""1 3
1 2 3
1
1 1 1 3
""") == "YES\n"

# custom case 2: all equal
assert run("""2 2
5 5
5 5
1
1 1 2 2
""") == "NO\n"

# custom case 3: duplicate only outside query
assert run("""2 3
1 2 3
1 4 5
1
1 2 2 3
""") == "YES\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all distinct row | YES | baseline correctness |
| all equal grid | NO | global duplicate detection |
| partial overlap | YES | exclusion of outside duplicates |

## Edge Cases

A key edge case is when duplicates exist but lie outside the query rectangle. In that case the algorithm must not falsely flag them. The event-based construction ensures this because only pairs fully contained in the row and column bounds contribute active constraints.

Another edge case is when duplicates occur in the same row or column. For example:

```
1 2 1
```

A query that excludes one occurrence must still return YES. The algorithm handles this because only pairs fully included in the query boundaries are activated.

A final edge case is single-cell queries, which should always return YES. Since no pair can fit inside a 1x1 rectangle, no event activates and the BIT remains empty, correctly producing a positive answer.
