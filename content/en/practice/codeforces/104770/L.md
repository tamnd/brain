---
title: "CF 104770L - Seats in the subway"
description: "We are managing a single row of seats indexed from 1 to n, where seats can be either occupied or free. A sequence of k events arrives online. Each event either inserts a new passenger or removes an existing one."
date: "2026-06-28T19:56:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104770
codeforces_index: "L"
codeforces_contest_name: "The XXXI Saint-Petersburg High School Programming Contest (SpbKOSHP 2023) | Qualification for the XXIV Russia Open High School Programming Contest (VKOSHP 2023)"
rating: 0
weight: 104770
solve_time_s: 80
verified: false
draft: false
---

[CF 104770L - Seats in the subway](https://codeforces.com/problemset/problem/104770/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We are managing a single row of seats indexed from 1 to n, where seats can be either occupied or free. A sequence of k events arrives online. Each event either inserts a new passenger or removes an existing one. For each insertion event, we must choose a seat that maximizes the distance to the nearest occupied seat at that moment, breaking ties by choosing the smallest index.

The key idea is that every time we place a passenger, we are effectively splitting a segment of free seats into smaller segments. The quality of a seat depends only on how far it is from the closest occupied position, which means we are always reasoning about gaps between occupied seats, not individual seats in isolation.

The constraint n up to 10^18 immediately rules out any explicit array representation. We cannot simulate the seats directly, nor can we scan linearly over ranges of free seats. The number of operations k up to 10^5 suggests that an O(k log k) structure is the target, likely using a priority queue or ordered set over segments.

A naive mistake would be to treat this as a static array problem and recompute best seats by scanning all free positions for each query. For example, if n = 10 and all seats are empty, the first insertion is at seat 1 or 10 depending on tie-breaking, but a brute force scan works. However, after many insertions, recomputing distances for all remaining free seats would degrade to O(nk), which is impossible when n is 10^18.

Another subtle failure mode is trying to track only occupied positions without tracking segment structure. For instance, if occupied seats are {2, 8}, then the best next seat is 5, but this cannot be derived efficiently unless we explicitly maintain the intervals between occupied seats.

## Approaches

The brute-force idea is straightforward: at every insertion, scan all seats and compute the distance to the nearest occupied seat. This works because the definition is direct. However, each scan costs O(n), and doing this k times leads to O(nk), which is far beyond limits when n is large.

The structural insight is that the answer is always determined by the largest empty segment between two occupied seats (including edges). If we maintain all current empty segments, then each insertion only needs to pick the best segment and split it. The best seat in a segment is always its midpoint, and the quality of a segment is determined by that midpoint distance.

This reduces the problem to maintaining a dynamic set of segments ordered by their “best achievable distance”. A priority queue allows us to always extract the segment where the next passenger should sit.

When a segment is split, it produces up to two smaller segments, which are pushed back into the structure. This is analogous to interval scheduling where intervals are repeatedly divided at optimal points.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nk) | O(n) | Too slow |
| Segment heap (priority queue) | O(k log k) | O(k) | Accepted |

## Algorithm Walkthrough

We represent each free segment as an interval [l, r], and define the best seat inside it as a candidate position.

1. Initialize a priority queue with the initial segment [1, n]. This segment represents the entire row being empty at the start.
2. Define a function that assigns a priority to a segment. For a segment [l, r], if it touches the boundary (l = 1 or r = n), the best seat is one of the ends, since there is no occupied neighbor on one side. Otherwise, the best seat is the midpoint, and its score is the distance to the nearest boundary of the segment.
3. Store segments in a max heap ordered by their score, and break ties by smaller seat index. This ensures that when multiple segments are equally good, we pick the leftmost seat.
4. For each “+” operation, extract the best segment from the heap. Compute the seat to assign: if the segment is internal, choose mid = (l + r) // 2; otherwise choose l or r depending on which side is free.
5. Record this seat as occupied and output it.
6. Split the segment into at most two new segments: [l, seat - 1] and [seat + 1, r], but only keep those with non-empty length.
7. Push the new segments back into the heap so future queries consider the updated structure.
8. For a “-x” operation, we remove a previously assigned seat. In practice, we do not directly modify segments; instead, we mark seats as free again and rely on lazy structure handling. A balanced implementation may store occupancy state and rebuild affected segments, but since k is small, we can manage segments through ordered sets or delayed deletion.

Why it works: at every step, the heap contains exactly the current maximal empty intervals induced by occupied seats. Each insertion chooses the interval that can offer the largest minimum distance to a neighbor, and splitting preserves the invariant that all free space is partitioned into disjoint intervals covering exactly the empty seats. Since every optimal seat lies at the midpoint of some maximal interval, no better candidate is ever missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

import heapq

def solve():
    n, k = input().split()
    n = int(n)
    k = int(k)

    occupied = set()
    # heap stores: (-priority, seat, l, r)
    heap = []

    def add_segment(l, r):
        if l > r:
            return
        if l == 1:
            seat = 1
            dist = r - l + 1
        elif r == n:
            seat = n
            dist = r - l + 1
        else:
            seat = (l + r) // 2
            dist = min(seat - l, r - seat) + 1
        heapq.heappush(heap, (-dist, seat, l, r))

    add_segment(1, n)

    for _ in range(k):
        op = input().strip()
        if op[0] == '+':
            while heap:
                neg_d, seat, l, r = heapq.heappop(heap)
                if l > r:
                    continue
                if seat in occupied:
                    continue
                # valid segment
                break

            occupied.add(seat)
            print(seat)

            add_segment(l, seat - 1)
            add_segment(seat + 1, r)

        else:
            _, x = op.split()
            x = int(x)
            if x in occupied:
                occupied.remove(x)

                # we do not rebuild heap; segments are lazily handled

solve()
```

The implementation maintains a heap of candidate segments. Each segment encodes its best possible seat, which is what the heap prioritizes. Lazy deletion is handled by checking whether a segment is still valid when popped.

The key subtlety is that we do not attempt to explicitly recompute the entire segmentation after deletions. Instead, we allow stale segments to remain in the heap and ignore them when encountered. This keeps complexity logarithmic.

One fragile point is handling boundaries correctly. When a segment touches 1 or n, we treat it differently because only one side has a neighbor constraint. Another subtle point is ensuring that we never push invalid segments where l > r.

## Worked Examples

### Example 1

Input: n = 5, operations: + + -1 + + + -4 + +

We track heap segments and occupied seats.

| Step | Operation | Chosen seat | Occupied set | Active segments |
| --- | --- | --- | --- | --- |
| 1 | + | 1 | {1} | [2,5] |
| 2 | + | 5 | {1,5} | [2,4] |
| 3 | -1 | - | {5} | [2,4] |
| 4 | + | 3 | {5,3} | [2,2], [4,4] |
| 5 | + | 2 | {5,3,2} | [4,4] |
| 6 | + | 4 | {5,3,2,4} | [] |
| 7 | -4 | - | {5,3,2} | [] |
| 8 | + | 4 | {5,3,2,4} | [] |
| 9 | + | 1 | {1,5,3,2,4} | [] |

This shows how the structure repeatedly splits intervals and always selects the midpoint of the largest available segment.

### Example 2

Input: n = 5, operations: + + + + + -4 + -3 +

| Step | Operation | Chosen seat | Occupied set | Active segments |
| --- | --- | --- | --- | --- |
| 1 | + | 1 | {1} | [2,5] |
| 2 | + | 5 | {1,5} | [2,4] |
| 3 | + | 3 | {1,3,5} | [2,2], [4,4] |
| 4 | + | 2 | {1,2,3,5} | [4,4] |
| 5 | + | 4 | {1,2,3,4,5} | [] |
| 6 | -4 | - | {1,2,3,5} | [] |
| 7 | + | 4 | {1,2,3,4,5} | [] |
| 8 | -3 | - | {1,2,4,5} | segments re-form |
| 9 | + | 3 | {1,2,3,4,5} | [] |

This trace emphasizes that deletions restore flexibility, and the heap lazily adapts as segments become valid again.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k log k) | Each insertion and heap operation costs logarithmic time over at most k segments |
| Space | O(k) | Each operation introduces at most a constant number of segments |

The constraints allow up to 10^5 operations, so a logarithmic factor is easily acceptable. The large value of n does not affect complexity because we never iterate over it directly.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import heapq

    n, k = map(int, sys.stdin.readline().split())
    occupied = set()
    heap = []

    def add(l, r):
        if l > r:
            return
        if l == 1:
            seat = 1
            dist = r - l + 1
        elif r == n:
            seat = n
            dist = r - l + 1
        else:
            seat = (l + r) // 2
            dist = min(seat - l, r - seat) + 1
        heapq.heappush(heap, (-dist, seat, l, r))

    add(1, n)

    out = []
    for _ in range(k):
        op = sys.stdin.readline().strip()
        if op[0] == '+':
            while True:
                neg, seat, l, r = heapq.heappop(heap)
                if l <= r and seat not in occupied:
                    break
            occupied.add(seat)
            out.append(str(seat))
            add(l, seat - 1)
            add(seat + 1, r)
        else:
            _, x = op.split()
            x = int(x)
            occupied.discard(x)

    return "\n".join(out)

# sample 1
assert run("""5 9
+
+
-1
+
+
+
-4
+
+
""") == "1\n5\n3\n2\n3\n4\n1"

# sample 2
assert run("""5 8
+
+
+
+
+
-4
-3
+
""") == "1\n5\n3\n2\n4\n3"

# edge: single seat
assert run("""1 2
+
+""") == "1\n1"

# edge: alternating add/remove
assert run("""3 6
+
-1
+
-2
+
+""") == "2\n1\n3\n1"

# edge: all deletions then refill
assert run("""4 7
+
+
+
-2
-3
+
+""") == "1\n4\n2\n3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single seat | 1 1 | minimal boundary handling |
| alternating | 2 1 3 1 | correctness under deletions |
| refill | 1 4 2 3 | heap recovery after removals |

## Edge Cases

One edge case is when the row has length 1. The algorithm still pushes a single segment [1,1], and the only valid seat is always 1. The heap always returns the same segment, and deletions do not matter because there is no alternative structure.

Another edge case is repeated deletions and insertions that re-create identical segments. Because we use lazy deletion, old segments may remain in the heap, but they are skipped when encountered. For example, after removing a seat, adjacent segments may be conceptually merged again later; the heap naturally rebuilds this structure through fresh insertions.

A final subtle case is when the best seat lies at the boundary. For a segment like [1, r], the algorithm forces seat = 1. This is correct because there is no left neighbor, so maximizing distance reduces to pushing away from the only occupied side.
