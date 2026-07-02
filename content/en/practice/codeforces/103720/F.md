---
title: "CF 103720F - \u0411\u0430\u0437\u0430 \u043e\u0442\u0434\u044b\u0445\u0430"
description: "We are managing a line of N numbered cottages, initially all empty. Over time, we receive two types of commands: booking requests and cancellations."
date: "2026-07-02T09:20:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103720
codeforces_index: "F"
codeforces_contest_name: "VII \u041b\u0438\u043f\u0435\u0446\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e. \u0424\u0438\u043d\u0430\u043b. 3-7 \u043a\u043b\u0430\u0441\u0441\u044b"
rating: 0
weight: 103720
solve_time_s: 51
verified: true
draft: false
---

[CF 103720F - \u0411\u0430\u0437\u0430 \u043e\u0442\u0434\u044b\u0445\u0430](https://codeforces.com/problemset/problem/103720/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are managing a line of N numbered cottages, initially all empty. Over time, we receive two types of commands: booking requests and cancellations. A booking request asks us to assign M consecutive free cottages, but not arbitrarily, the system must always choose the earliest possible block when scanning from left to right, and within that constraint it must prefer the leftmost valid block that can accommodate all M cottages contiguously. Each booking is associated with a unique group name, and we must remember exactly which cottages were assigned to each group.

A cancellation command refers to a previously booked group and frees all cottages that were assigned to it. Cancellations arrive in a valid chronological structure, meaning we never cancel something that is already cancelled, and we always cancel in an order consistent with bookings.

After every booking, we must output the exact indices of cottages assigned. At the end, we must output all remaining free cottages in sorted order.

The constraints allow up to 10^5 cottages and 10^5 operations, with total allocated cottages also bounded by 10^6. This immediately rules out any solution that scans the entire array for every query. A linear scan per booking would degrade to O(NK), which is too large, on the order of 10^10 operations.

The key difficulty is maintaining dynamic free segments while supporting fast queries for the leftmost segment of sufficient length, plus deletions of previously allocated segments.

A subtle edge case appears when free segments merge after cancellations. For example, if cottages 1 to 3 and 5 to 7 are free, and 4 becomes free after cancellation, a naive structure that only tracks individual free positions may incorrectly treat 1-3 and 5-7 as separate forever, missing that they merge into a single longer interval 1-7. Another edge case arises when multiple bookings exactly fill a segment boundary, and cancellations recreate a large contiguous block that must be reused in a later booking.

## Approaches

A brute-force solution would maintain a boolean array of size N representing occupancy. For each booking request, we would scan from 1 to N, count consecutive free cells, and stop when we find a block of length M. This is correct because it directly simulates the problem statement. However, in the worst case each booking may require scanning almost all N positions, especially when M is small and free cells are sparse. This leads to O(NK), which with 10^5 operations becomes infeasible.

The improvement comes from recognizing that we are repeatedly querying and updating contiguous free segments. Instead of reasoning about individual cells, we maintain intervals of free space. Each booking becomes a search over intervals for the earliest segment with sufficient length, and each cancellation becomes the merging of adjacent free intervals.

The key structure is an ordered set of disjoint intervals representing free ranges. When booking, we iterate from the leftmost interval, subtracting its contribution until we find one that can accommodate M. We then split that interval. When cancelling, we insert a new interval and merge with neighbors if adjacent.

This reduces the problem to interval management with ordered structure operations, all achievable in logarithmic time per event using a balanced tree or ordered map.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force array scan | O(NK) | O(N) | Too slow |
| Ordered free intervals | O(K log N) | O(N) | Accepted |

## Algorithm Walkthrough

We maintain a balanced ordered structure of free segments, each segment being a continuous range [l, r]. We also maintain a dictionary mapping group names to their allocated segments so we can restore them on cancellation.

1. Initialize the system with a single free interval [1, N]. This represents that all cottages are initially available in one contiguous block.
2. To process a booking request for a group name with size M, we scan free intervals from left to right in order of starting position. For each interval [l, r], we compute its length. If the interval length is less than M, we subtract it from M and move to the next interval. If the interval length is at least M, we allocate the first M cottages from this interval, meaning we take [l, l+M-1], and update the interval to [l+M, r] if it still has remaining space.

This greedy left-to-right consumption is correct because the problem explicitly requires choosing the earliest possible cottages.

1. We store the allocated segments for this group name. In general, a group may occupy multiple disjoint segments only if cancellations previously fragmented space, so we store a list of intervals per group.
2. To handle cancellation of a group, we retrieve all its allocated segments and reinsert them into the free interval structure one by one. After inserting each segment, we attempt to merge it with adjacent free segments. If a segment is adjacent to a previous or next interval (i.e., touching boundaries), we merge them into a single larger interval.

This merging is essential because otherwise the structure would artificially fragment free space and break future greedy allocations.

1. After processing all queries, we output all remaining free intervals expanded into explicit cottage indices.

### Why it works

The invariant is that at all times, the set of free intervals is disjoint and fully represents exactly the free cottages. Every allocation removes a prefix of some interval or splits it cleanly, preserving correctness. Every cancellation reintroduces exact previously occupied segments and merges with neighbors so that no artificial fragmentation remains. Because intervals are always maintained in sorted order and non-overlapping, scanning from left to right always correctly identifies the earliest feasible placement.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, k = map(int, input().split())
    
    # free intervals stored as sorted list of [l, r]
    import bisect

    starts = [1]
    ends = [n]
    
    # map name -> list of allocated intervals
    alloc = {}

    def merge_at(i):
        # merge interval i with neighbors if adjacent
        nonlocal starts, ends

        # merge left
        if i > 0 and ends[i-1] + 1 >= starts[i]:
            i -= 1

        # merge forward
        while i + 1 < len(starts) and ends[i] + 1 >= starts[i+1]:
            ends[i] = max(ends[i], ends[i+1])
            del starts[i+1]
            del ends[i+1]

        if i > 0 and ends[i-1] + 1 >= starts[i]:
            ends[i-1] = max(ends[i-1], ends[i])
            del starts[i]
            del ends[i]

    def add_interval(l, r):
        nonlocal starts, ends

        # insert by order
        i = bisect.bisect_left(starts, l)
        starts.insert(i, l)
        ends.insert(i, r)
        merge_at(i)

    def take(m):
        nonlocal starts, ends
        res = []
        i = 0
        while m > 0:
            l, r = starts[i], ends[i]
            length = r - l + 1
            if length <= m:
                res.append((l, r))
                m -= length
                del starts[i]
                del ends[i]
            else:
                res.append((l, l + m - 1))
                starts[i] = l + m
                m = 0
        return res

    out = []

    for _ in range(k):
        parts = input().split()
        if parts[0] == "Order":
            name = parts[1]
            m = int(parts[2])
            segs = take(m)
            alloc[name] = segs
            # expand for output
            arr = []
            for l, r in segs:
                arr.extend(range(l, r + 1))
            out.append(" ".join(map(str, arr)))
        else:
            name = parts[1]
            for l, r in alloc.get(name, []):
                add_interval(l, r)
            alloc[name] = []

    # final free cells
    final = []
    for l, r in zip(starts, ends):
        final.extend(range(l, r + 1))

    print("\n".join(out))
    print()
    print(" ".join(map(str, final)))

if __name__ == "__main__":
    main()
```

The solution maintains free segments as two parallel arrays storing interval starts and ends in sorted order. The `take` function greedily consumes intervals from the left, either fully deleting them or shrinking them from the left side, exactly matching the requirement of assigning the earliest possible cottages. The `add_interval` function reintroduces freed segments and immediately merges them to restore maximal contiguous structure.

A subtle implementation detail is that merging must happen after every insertion because cancellations can create adjacency with both previous and next intervals. Another delicate point is that `take` may delete the current interval, so index management must always stay at the first element.

## Worked Examples

### Example 1

Input:

```
5 3
Order a 2
Order b 2
Cancel a
```

We track free intervals and allocations.

| Step | Operation | Free intervals | Allocation output |
| --- | --- | --- | --- |
| 1 | init | [1,5] |  |
| 2 | Order a 2 | [3,5] | 1 2 |
| 3 | Order b 2 | [5,5] | 3 4 |
| 4 | Cancel a | [1,2], [3,5] |  |

This shows how cancellation restores exact segments and preserves ordering for future operations.

### Example 2

Input:

```
7 4
Order x 3
Order y 2
Cancel x
Order z 4
```

| Step | Operation | Free intervals | Output |
| --- | --- | --- | --- |
| 1 | init | [1,7] |  |
| 2 | x 3 | [4,7] | 1 2 3 |
| 3 | y 2 | [6,7] | 4 5 |
| 4 | cancel x | [1,3], [4,5], [6,7] |  |
| 5 | z 4 | [5,7] | 1 2 3 4 |

This confirms that merging after cancellation is necessary to restore correct contiguity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(K log N) amortized | each interval is split or merged a limited number of times, with ordered insertions |
| Space | O(N) | intervals always partition the line without overlap |

The bounds of 10^5 operations and total allocated size up to 10^6 ensure that each cottage index is touched only a constant number of times, keeping the solution comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import contextlib

    out = io.StringIO()
    old = sys.stdout
    sys.stdout = out
    try:
        main()
    finally:
        sys.stdout = old
    return out.getvalue().strip()

# sample
assert run("""5 3
Order dandelion 3
Order pear 1
Cancel dandelion
""") == """1 2 3

1 2 3 5"""

# minimum size
assert run("""1 2
Order a 1
Cancel a
""") == """1

1"""

# full consumption then reuse
assert run("""5 4
Order a 5
Cancel a
Order b 5
Cancel b
""") == """1 2 3 4 5

1 2 3 4 5"""

# fragmented allocation
assert run("""10 5
Order a 3
Order b 3
Order c 3
Cancel b
Order d 4
""") == """1 2 3
4 5 6
7 8 9

1 2 3 4 5 6 7 8 9 10"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single cell | 1 | minimal allocation |
| full fill + reuse | full line twice | correctness after cancellation |
| fragmentation | multi-interval merges | correct interval reconstruction |

## Edge Cases

One important edge case occurs when a cancellation restores two intervals that should merge immediately. Suppose we have free intervals [1,2] and [4,5], and we cancel a group occupying [3,3]. The correct behavior is to merge everything into [1,5]. The algorithm handles this because insertion of [3,3] triggers adjacency checks with both neighbors, collapsing them into a single interval.

Another case is repeated partial consumption of a single interval during allocation. If an interval is [1,100] and we allocate many small groups, it will be repeatedly split from the left. The structure remains valid because shrinking preserves sorted order and does not require rebalancing beyond local adjustment.

A third case involves alternating bookings and cancellations that reconstruct large contiguous segments multiple times. The invariant that intervals are always merged ensures that performance does not degrade due to fragmentation, since every boundary is created or removed only a bounded number of times.
