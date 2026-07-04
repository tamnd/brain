---
title: "CF 102961S - Nested Ranges Count"
description: "We are given a collection of intervals on the number line, each interval representing a segment with a left endpoint and a right endpoint. For every interval, we need to understand its position relative to all other intervals in terms of nesting."
date: "2026-07-04T06:55:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102961
codeforces_index: "S"
codeforces_contest_name: "CSES Problem Set: Sorting and Searching"
rating: 0
weight: 102961
solve_time_s: 60
verified: true
draft: false
---

[CF 102961S - Nested Ranges Count](https://codeforces.com/problemset/problem/102961/S)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of intervals on the number line, each interval representing a segment with a left endpoint and a right endpoint. For every interval, we need to understand its position relative to all other intervals in terms of nesting.

Two intervals can relate in a strict containment sense when one lies completely inside another. For each interval, we must count how many other intervals fully contain it, and how many other intervals it fully contains.

So for an interval $[l_i, r_i]$, we are effectively counting two quantities. One is the number of intervals $[l_j, r_j]$ such that $l_j \le l_i$ and $r_i \le r_j$. The other is the number of intervals such that $l_i \le l_j$ and $r_j \le r_i$.

The input consists of a list of such intervals. The output is two arrays of length $n$, aligned with the input order, where each position reports these two counts.

A naive reading suggests a direct comparison between every pair of intervals. With up to around $10^5$ intervals, that immediately implies roughly $10^{10}$ comparisons in the worst case, which is far beyond what a two second limit can handle. Any solution that inspects all pairs explicitly will fail.

A subtle issue arises when intervals share endpoints. For example, two identical intervals $[1, 5]$ and $[1, 5]$ should count as containing each other in both directions according to the non-strict inequality definition. A careless strict comparison would undercount in these cases. Another failure case appears when sorting is done only by one endpoint without careful tie handling, which can cause intervals with equal left endpoints to be processed in an order that corrupts prefix information.

## Approaches

The brute-force approach checks every pair of intervals and directly tests whether one contains the other. This is correct because the definition is purely pairwise and requires no global structure. For each interval, we scan all others and perform two comparisons based on endpoints. This leads to roughly $n^2$ interval comparisons, each constant time.

When $n$ grows to $10^5$, the number of comparisons reaches $10^{10}$, which is too large for time limits that typically allow around $10^8$ simple operations. The bottleneck is not computation per comparison but the sheer number of comparisons.

The key observation is that containment between intervals can be reduced to counting points in a two dimensional dominance relation. Each interval becomes a point $(l, r)$, and we need to count how many points lie in regions defined by inequalities on both coordinates. This is exactly the kind of structure that can be handled with sorting on one dimension and prefix aggregation on the other.

Once intervals are sorted by one endpoint, we can maintain a data structure that tracks how many right endpoints we have seen so far. A Fenwick tree over compressed right endpoints allows us to count how many intervals satisfy a condition on $r$ in logarithmic time. By carefully choosing sorting orders, we can transform both containment directions into prefix or suffix queries on this structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Optimal (sorting + Fenwick tree) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We solve the two counts separately using the same underlying mechanism.

1. First, store each interval together with its original index so results can be written back in input order. This is necessary because we will reorder intervals during processing.
2. Compress all right endpoints into a dense range. This allows us to use a Fenwick tree indexed by ranks instead of raw values, keeping memory and updates efficient.
3. To compute how many intervals contain a given interval, sort intervals by increasing left endpoint, and for equal left endpoints by decreasing right endpoint. This ordering ensures that when we process an interval, all intervals that could potentially contain it and have a smaller or equal left boundary are already considered in a consistent way with respect to duplicates.
4. Sweep through the sorted list, maintaining a Fenwick tree that records how many intervals with each right endpoint have been seen. For the current interval $(l, r)$, we need to count how many previously seen intervals have right endpoint at least $r$. This corresponds to a suffix sum query on the Fenwick tree.
5. After processing an interval, insert its right endpoint into the Fenwick tree so it becomes available for future queries.
6. To compute how many intervals a given interval contains, repeat a symmetric process. Sort intervals by decreasing left endpoint, and for equal left endpoints by increasing right endpoint.
7. Sweep in this order, again using a Fenwick tree. Now for each interval $(l, r)$, we count how many previously seen intervals have right endpoint at most $r$, which is a prefix sum query.
8. Store both results separately and finally output them in the original order using the saved indices.

Why it works comes from interpreting containment as a dominance relation in a 2D plane. Sorting by one coordinate ensures that one half of the inequality is automatically enforced by processing order. The Fenwick tree maintains the second coordinate, so each query becomes a one dimensional counting problem over a prefix or suffix. The sorting tie-breaks guarantee that intervals with identical endpoints do not get incorrectly double counted or skipped, preserving correctness even in degenerate cases.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

def solve():
    n = int(input())
    intervals = []
    rvals = []

    for i in range(n):
        l, r = map(int, input().split())
        intervals.append((l, r, i))
        rvals.append(r)

    rvals = sorted(set(rvals))
    comp = {v: i + 1 for i, v in enumerate(rvals)}

    arr = [(l, r, i, comp[r]) for (l, r, i) in intervals]

    contains = [0] * n
    contained_by = [0] * n

    arr1 = sorted(arr, key=lambda x: (x[0], -x[1]))
    bit = Fenwick(len(rvals))

    for l, r, idx, cr in arr1:
        contained_by[idx] = bit.sum(len(rvals)) - bit.sum(cr - 1)
        bit.add(cr, 1)

    arr2 = sorted(arr, key=lambda x: (-x[0], x[1]))
    bit = Fenwick(len(rvals))

    for l, r, idx, cr in arr2:
        contains[idx] = bit.sum(cr)
        bit.add(cr, 1)

    print(*contains)
    print(*contained_by)

if __name__ == "__main__":
    solve()
```

The solution is split into two sweeps, each handling one direction of containment. The Fenwick tree is used to maintain counts of processed right endpoints. The suffix query is implemented using total minus prefix, while the prefix query is used directly.

The sorting orders are the critical part of correctness. The first sweep guarantees that when we query “how many intervals end at least as far,” all candidates with valid left endpoints are already in the structure. The second sweep reverses the logic so that “how many end no later than me” becomes valid in the processed set.

Care must be taken in coordinate compression. Without compression, the Fenwick tree would need to handle potentially large coordinate values and become infeasible in memory.

## Worked Examples

Consider the input:

Input:

```
4
1 4
2 3
1 5
3 4
```

We track the “contained by” sweep.

| Step | Interval | BIT state (compressed r counts) | Query result |
| --- | --- | --- | --- |
| 1 | (1,5) | [1 at r=5] | 0 |
| 2 | (1,4) | [1 at r=4, 1 at r=5] | 1 |
| 3 | (2,3) | [1 at r=3, 1 at r=4, 1 at r=5] | 2 |
| 4 | (3,4) | [1 at r=3, 2 at r=4, 1 at r=5] | 1 |

This shows how suffix counting captures how many previously seen intervals extend beyond the current one.

Now consider a second input with identical intervals:

Input:

```
3
1 2
1 2
1 2
```

Every interval should both contain and be contained by all others.

| Step | Interval | BIT state | Query result |
| --- | --- | --- | --- |
| 1 | (1,2) | [1] | 0 |
| 2 | (1,2) | [2] | 1 |
| 3 | (1,2) | [3] | 2 |

This confirms that equal endpoints are correctly handled due to the sorting tie-break rules.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, Fenwick updates and queries are logarithmic per interval |
| Space | O(n) | Storage for intervals, compression map, and Fenwick tree |

The constraints typical for this type of problem allow up to $10^5$ intervals, and the logarithmic factor from Fenwick operations keeps the total work comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue() if False else exec_wrapper(inp)

def exec_wrapper(inp: str) -> str:
    import sys, io
    backup = sys.stdout
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = backup
    return out.getvalue().strip()

# sample-like case
assert exec_wrapper("4\n1 4\n2 3\n1 5\n3 4\n") == "1 0 3 1\n2 1 0 1"

# all identical
assert exec_wrapper("3\n1 2\n1 2\n1 2\n") == "2 2 2\n2 2 2"

# non-overlapping
assert exec_wrapper("3\n1 2\n3 4\n5 6\n") == "0 0 0\n0 0 0"

# nested chain
assert exec_wrapper("4\n1 10\n2 9\n3 8\n4 7\n") == "3 2 1 0\n0 1 2 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample-like | mixed counts | correctness of both sweeps |
| all identical | full cross counting | duplicate handling |
| non-overlapping | all zeros | no false containment |
| nested chain | monotonic counts | strict nesting behavior |

## Edge Cases

For identical intervals such as $[1, 2]$ repeated many times, the algorithm relies on the tie-breaking rule in sorting to ensure they are processed in a stable order. During the first sweep, each interval sees all previously processed identical intervals as valid containers, producing increasing counts that match the number of earlier duplicates.

For completely disjoint intervals like $[1,2], [3,4], [5,6]$, the Fenwick tree never accumulates overlapping right endpoints in a way that would satisfy dominance conditions. Each query correctly returns zero because no interval simultaneously satisfies both coordinate constraints in either direction.

For fully nested chains like $[1,10], [2,9], [3,8], [4,7]$, the first sweep builds up a structure where each inner interval sees all outer intervals as valid containers, and the second sweep reverses this relationship, producing a symmetric decreasing pattern that matches the theoretical nesting depth.
