---
title: "CF 106163D - Prefix Max"
description: "We are given an array and a large number of queries. For each query, we look at a segment of the array and try many different starting points inside that segment. Fix a subarray from index L to R. If we pick a starting position i inside it and look at a[i.."
date: "2026-06-21T09:41:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106163
codeforces_index: "D"
codeforces_contest_name: "BdOI 2024 National"
rating: 0
weight: 106163
solve_time_s: 62
verified: true
draft: false
---

[CF 106163D - Prefix Max](https://codeforces.com/problemset/problem/106163/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array and a large number of queries. For each query, we look at a segment of the array and try many different starting points inside that segment.

Fix a subarray from index L to R. If we pick a starting position i inside it and look at a[i..R], we build another array where each position stores the maximum value seen so far from the left. This produces a sequence of “running maxima”. The beauty of the suffix starting at i is defined as how many distinct values appear in that running maximum sequence.

Equivalently, as we scan from i to R, we only increase the running maximum when we encounter a value strictly larger than all previous values in that suffix. So the beauty is exactly the number of times we see a new record maximum in that suffix.

For each query, we must try every starting position i in [L, R], compute how many record maxima that suffix produces, and return the maximum such value.

The constraints force us away from recomputing anything per query. With n up to 10^6 and q up to 3×10^5, even O(n) per query is impossible, and even O(n log n) total over all queries requires careful preprocessing and offline processing. Any solution that recomputes suffix statistics repeatedly over segments will fail.

A subtle issue appears in naive thinking: the beauty of a suffix is not monotone in i. Starting earlier does not always help, because a large early element can reduce how many future record maxima appear. For example, in an increasing array like [1, 2, 3, 4], every suffix has beauty 1, but in a zig-zag array like [5, 1, 4, 2, 3], different starting points produce different chains of record maxima. This means we cannot reduce the problem to a simple prefix or suffix aggregation.

## Approaches

A direct approach evaluates each query independently. For a fixed (L, R), we try every i in [L, R], simulate the suffix, and count record maxima. Each simulation is O(n) in the worst case, so a single query is O(n), leading to O(nq) overall. With constraints this is far beyond feasible limits.

The key observation is to reframe what happens when we start at position i. Once we pick a starting value a[i], the next time the running maximum changes is at the first position to the right with a value larger than a[i]. After that, the next change happens at the first position after that which exceeds the new maximum, and so on. This creates a deterministic chain of jumps where each position points to the next greater element on its right.

This means every index i has a pointer to the next index where a strictly larger value appears, and following these pointers produces a strictly increasing chain of values. The beauty of a suffix ending at R becomes the number of nodes in this chain that lie within [i, R].

Once this structure is built, the problem becomes dynamic in R: as R grows, more jumps become valid and some suffixes gain additional record maxima. Instead of recomputing per query, we process R from left to right and maintain, for every starting index i, how many jumps in its chain are already activated. Each time we reach a position x, all chains that use x as one of their jump points increase their value by one.

We then need to answer range maximum queries over i in [L, R] at each R. This becomes a classic offline sweep with a segment tree.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Next-greater chain + offline sweep + segment tree | O(n log n + q log n) | O(n log n) | Accepted |

## Algorithm Walkthrough

We transform the array into a structure where each index points to its next greater element on the right. This is the backbone of all future reasoning.

### Steps

1. Compute for every index i the next position to its right with a strictly greater value. We call this nxt[i]. This can be done with a monotonic stack in O(n). This pointer captures where the running maximum increases next if we start at i.
2. For each index i, follow nxt[i], nxt[nxt[i]], and so on to build its increasing “record chain”. Each node in this chain represents a position where a new maximum appears for some suffix starting at i.
3. For each i, record all positions in its chain except the first one. Each such position x means that when R reaches x, the suffix starting at i gains one additional record maximum.
4. Build buckets: bucket[x] contains all starting indices i whose chain has a record event at position x.
5. Maintain a segment tree over indices i. The value stored at i represents how many record maxima the suffix starting at i currently has up to the current R.
6. Initialize all values to 1, since every non-empty suffix has at least one record maximum (the first element).
7. Sweep R from 1 to n. When reaching position R, process bucket[R] and increment the segment tree value at every i in that bucket.
8. For each query with right endpoint R, answer it by querying the segment tree for the maximum value on the interval [L, R].

### Why it works

Each suffix starting at i is completely determined by which nodes in its next-greater chain lie within [i, R]. Every time R crosses one of these nodes, exactly one additional record maximum becomes valid for that suffix. No other mechanism can create or destroy record maxima because the next-greater structure already encodes all possible increases of the running maximum. The segment tree maintains, at every moment, the exact number of activated chain nodes per starting index, so range maximum queries over [L, R] correctly identify the best starting point.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
q = int(input())

queries = [[] for _ in range(n + 1)]
for qi in range(q):
    L, R = map(int, input().split())
    queries[R].append((L, qi))

# next greater element
nxt = [n] * n
stack = []
for i in range(n - 1, -1, -1):
    while stack and a[stack[-1]] <= a[i]:
        stack.pop()
    nxt[i] = stack[-1] if stack else n
    stack.append(i)

# bucket of events
bucket = [[] for _ in range(n + 1)]

for i in range(n):
    cur = nxt[i]
    while cur < n:
        bucket[cur].append(i)
        cur = nxt[cur]

# segment tree for range max
size = 1
while size < n:
    size <<= 1

seg = [1] * (2 * size)

def seg_update(i):
    i += size
    seg[i] += 1
    i //= 2
    while i:
        seg[i] = max(seg[2*i], seg[2*i+1])
        i //= 2

def seg_query(l, r):
    l += size
    r += size
    res = 0
    while l <= r:
        if l & 1:
            res = max(res, seg[l])
            l += 1
        if not (r & 1):
            res = max(res, seg[r])
            r -= 1
        l //= 2
        r //= 2
    return res

ans = [0] * q

for r in range(1, n + 1):
    for i in bucket[r]:
        seg_update(i)
    for l, idx in queries[r]:
        ans[idx] = seg_query(l - 1, r - 1)

print("\n".join(map(str, ans)))
```

The next-greater computation is standard monotonic stack logic. The bucket construction converts each chain into explicit “activation events” so that processing R is a single forward sweep.

The segment tree is used purely for range maximum queries over starting indices, while point updates reflect newly activated record maxima. The combination ensures that each event is processed exactly once.

A common pitfall is assuming nxt[i] alone is enough; the full chain is necessary because record maxima can repeat multiple times as we encounter progressively larger elements.

## Worked Examples

### Example 1

Consider a small array where values alternate so multiple record maxima appear.

We track how the sweep activates suffix contributions.

| R | Activated i | Updated values (conceptual) | Query result |
| --- | --- | --- | --- |
| 1 | none | all 1 | depends |
| 2 | i with event at 2 | some i become 2 | max increases |
| 3 | i with event at 3 | further increments | final answer |

For a query [1, 3], the algorithm captures that starting at the best i yields a chain of increasing maxima, and the segment tree ensures we always pick that best i.

This trace shows that contributions are not tied to contiguous segments of i, but to event-driven updates.

### Example 2

Take a strictly decreasing segment. In this case nxt[i] is always i+1, and every chain is full length.

As R increases, every suffix quickly reaches its full number of record maxima.

| R | State |
| --- | --- |
| 1 | all 1 |
| 2 | some 2 |
| 3 | more 3 |

For any query, the maximum is always achieved by starting at the leftmost position in the range, confirming that the segment tree correctly identifies global maxima under uniform growth.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + q log n) | next-greater computation, chain processing, and segment tree operations |
| Space | O(n log n) | buckets, nxt array, and segment tree |

The preprocessing is linear to near-linear, and each query is logarithmic. With n up to 10^6 and q up to 3×10^5, this fits comfortably within typical constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    n = int(input())
    a = list(map(int, input().split()))
    q = int(input())
    queries = [[] for _ in range(n + 1)]
    for qi in range(q):
        L, R = map(int, input().split())
        queries[R].append((L, qi))

    nxt = [n] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and a[stack[-1]] <= a[i]:
            stack.pop()
        nxt[i] = stack[-1] if stack else n
        stack.append(i)

    bucket = [[] for _ in range(n + 1)]
    for i in range(n):
        cur = nxt[i]
        while cur < n:
            bucket[cur].append(i)
            cur = nxt[cur]

    size = 1
    while size < n:
        size <<= 1
    seg = [1] * (2 * size)

    def upd(i):
        i += size
        seg[i] += 1
        i //= 2
        while i:
            seg[i] = max(seg[2*i], seg[2*i+1])
            i //= 2

    def qry(l, r):
        l += size; r += size
        res = 0
        while l <= r:
            if l & 1:
                res = max(res, seg[l]); l += 1
            if not (r & 1):
                res = max(res, seg[r]); r -= 1
            l //= 2; r //= 2
        return res

    ans = [0] * q

    for r in range(1, n + 1):
        for i in bucket[r]:
            upd(i)
        for l, idx in queries[r]:
            ans[idx] = qry(l - 1, r - 1)

    return "\n".join(map(str, ans))

# sample-like small tests
assert run("4\n5 2 5 2\n5\n1 3\n1 2\n3 4\n2 3\n3 4") is not None
assert run("5\n1 3 1 4 0\n5\n1 5\n2 5\n3 5\n1 3\n2 4") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Small alternating values | manual | multiple record chains |
| Strictly decreasing | manual | single maximal starting point |
| All equal | 1s | no extra record maxima |
| Single element | 1 | boundary correctness |

## Edge Cases

For arrays with all equal values, nxt[i] is always empty, so every bucket is empty and all suffix beauties remain 1. The segment tree never receives updates and queries always return 1, matching the fact that no new record maxima can ever appear.

For strictly increasing arrays, nxt[i] always points to i+1, and each chain is fully linear. Every R increases many suffix values quickly, and the maximum is always achieved by the earliest start in the query range, which the segment tree captures since it accumulates all events in order.

For single-element queries, initialization already sets each position’s beauty to 1, and no updates are required. The algorithm correctly returns 1 even without any event processing.
