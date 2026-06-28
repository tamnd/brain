---
title: "CF 104840G - \u0412\u043e\u0437\u0432\u0440\u0430\u0449\u0435\u043d\u0438\u0435 \u0417\u043b\u043e\u0433\u043e \u041c\u043e\u0440\u0442\u0438"
description: "We are given a collection of segments on the number line. Each segment represents a range of “realities” that must be searched as a single item."
date: "2026-06-28T11:38:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104840
codeforces_index: "G"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2023-2024, \u0422\u0440\u0435\u0442\u044c\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 104840
solve_time_s: 53
verified: true
draft: false
---

[CF 104840G - \u0412\u043e\u0437\u0432\u0440\u0430\u0449\u0435\u043d\u0438\u0435 \u0417\u043b\u043e\u0433\u043e \u041c\u043e\u0440\u0442\u0438](https://codeforces.com/problemset/problem/104840/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of segments on the number line. Each segment represents a range of “realities” that must be searched as a single item. The operation we perform is grouping these segments: a group contains several segments, and processing one group means we handle all segments inside it together.

Inside a single group, no two segments are allowed to intersect. Intersection here means they share at least one point in common, so two segments are incompatible if one starts before the other ends.

The task is to split all segments into the smallest possible number of such groups and also output the composition of each group.

The input size reaches two hundred thousand segments, and each endpoint can be as large as one billion. This immediately rules out any approach that tries to compare all pairs of segments, since that would be quadratic and far beyond the time limit. Even maintaining an explicit compatibility matrix is impossible.

A subtle point is that the segments are closed intervals. That matters for adjacency cases like `[1, 3]` and `[3, 5]`, which do intersect at the point 3 and therefore cannot belong to the same group. This forces the strict condition for compatibility to be `r < l`.

A naive mistake is to assume that touching endpoints are safe to combine. For example:

Input:

```
3
1 3
3 5
6 7
```

A careless grouping might put the first and second segments together, but they intersect at 3, so this violates the rule. The correct solution must treat that boundary as conflicting.

Another common pitfall is to greedily pack segments into the first available group without a global ordering strategy. Without sorting by start time, the grouping can become order-dependent and produce more groups than necessary.

## Approaches

A brute-force idea is to build groups one by one. We repeatedly pick an unassigned segment, start a new group, and then scan all remaining segments to add any that do not intersect with any already inside the group. Each addition requires checking compatibility against all current members of the group.

This works logically because it explicitly enforces the non-intersection constraint. The problem is performance. In the worst case, if segments are heavily overlapping, each group might only take one segment, and each attempt to fill a group scans almost all remaining segments. This leads to quadratic behavior on the order of n squared, which is far beyond acceptable for 200,000 elements.

The key observation is that this is a classic interval coloring problem. The minimum number of groups needed equals the maximum number of overlapping intervals at any point. Instead of constructing groups greedily in an arbitrary order, we process segments sorted by their starting points and maintain a structure of currently active groups, each represented by the last end point assigned to it.

At any moment, a group is eligible for reuse if its last segment ends strictly before the current segment begins. So we want to quickly find a group with the smallest ending time that still satisfies this condition. A min-heap over group end times gives exactly this functionality.

Each segment is assigned to an existing compatible group if possible, otherwise a new group is created. This ensures optimal reuse of groups and guarantees minimal count.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort all segments by their left endpoint. This ensures we always process intervals in the order they begin, which is essential for maintaining a consistent notion of “currently open” groups.
2. Maintain a min-heap where each element represents a group, keyed by the right endpoint of the last segment placed into that group. Each heap entry also stores the group identifier.
3. Iterate over segments in sorted order. For each segment `[l, r]`, inspect the heap.
4. If the heap is not empty and the smallest ending group has end `< l`, pop it and assign the current segment to that group. We choose the smallest end because it frees up earliest, maximizing future reuse opportunities.
5. Otherwise, no existing group can accept this segment, so we create a new group and assign the segment to it.
6. After assignment, push the updated group back into the heap with the current segment’s end time.
7. Store group membership lists so we can output them at the end.

### Why it works

At any moment, the heap stores all active groups ordered by when they stop being usable. Assigning a segment to the group with the smallest ending time is safe because if any group can accommodate the segment, that one is the most constrained; if it cannot, no other group can either. This greedy choice preserves all future possibilities and avoids creating unnecessary groups.

The invariant is that after processing each segment, every group in the heap represents a valid non-overlapping chain of segments, and any segment assigned later is compatible with all segments already in its group. Since we always reuse a compatible group when possible, we never increase the group count unless forced by overlap structure. This matches the definition of interval partitioning optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    segs = []
    for i in range(n):
        l, r = map(int, input().split())
        segs.append((l, r, i + 1))

    segs.sort()

    import heapq
    heap = []
    groups = []
    
    for l, r, idx in segs:
        if heap and heap[0][0] < l:
            end, gid = heapq.heappop(heap)
        else:
            gid = len(groups)
            groups.append([])

        groups[gid].append(idx)
        heapq.heappush(heap, (r, gid))

    print(len(groups))
    for g in groups:
        print(len(g))
        print(*g)

if __name__ == "__main__":
    solve()
```

The solution begins by sorting intervals by their left endpoint, which ensures we always extend groups in chronological order. The heap stores pairs of `(end_time, group_id)` so that we can efficiently find the group that becomes free earliest.

The condition `heap[0][0] < l` is the critical detail. It enforces strict non-intersection: if a group ends at time `r`, it can only accept a new interval starting at `l` when `r < l`.

When we pop from the heap, we are committing to reuse that group. If no group is valid, we allocate a new one, which corresponds to increasing the chromatic number of the interval graph.

## Worked Examples

### Example 1

Input:

```
4
1 5
2 3
4 7
8 9
```

Sorted segments remain:

```
(1,5), (2,3), (4,7), (8,9)
```

We track group assignment:

| Segment | Heap before | Action | Groups formed |
| --- | --- | --- | --- |
| (1,5) | empty | new group 0 | [1] |
| (2,3) | (5,0) | new group 1 | [1], [2] |
| (4,7) | (3,1), (5,0) | reuse group 1 | [1], [2,3] |
| (8,9) | (5,0), (7,1) | reuse group 0 | [1,4], [2,3] |

Final groups are `[1,4]` and `[2,3]`, so two groups are sufficient.

This demonstrates how reuse depends on the earliest finishing group, not on arrival order.

### Example 2

Input:

```
3
1 2
2 3
3 4
```

All intervals overlap via endpoints, so none can share a group.

| Segment | Heap before | Action | Groups formed |
| --- | --- | --- | --- |
| (1,2) | empty | new group 0 | [1] |
| (2,3) | (2,0) | new group 1 | [1], [2] |
| (3,4) | (2,0), (3,1) | new group 2 | [1], [2], [3] |

This confirms that endpoint touching forces maximum separation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, heap operations are logarithmic per interval |
| Space | O(n) | Storage for segments, heap, and group assignments |

The constraints allow up to 200,000 intervals, so an n log n approach comfortably fits within time limits. The heap ensures that each interval is inserted and removed at most once, keeping overhead minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    segs = []
    for i in range(n):
        l, r = map(int, input().split())
        segs.append((l, r, i + 1))

    segs.sort()
    import heapq

    heap = []
    groups = []

    for l, r, idx in segs:
        if heap and heap[0][0] < l:
            end, gid = heapq.heappop(heap)
        else:
            gid = len(groups)
            groups.append([])

        groups[gid].append(idx)
        heapq.heappush(heap, (r, gid))

    out = []
    out.append(str(len(groups)))
    for g in groups:
        out.append(str(len(g)))
        out.append(" ".join(map(str, g)))
    return "\n".join(out)

# minimum size
assert run("1\n1 10\n") == "1\n1\n1"

# all overlap
assert run("3\n1 5\n2 6\n3 7\n") == "3\n1\n1\n1\n2\n1\n3"

# chain overlap via endpoints
assert run("3\n1 2\n2 3\n3 4\n") == "3\n1\n1\n1\n2\n1\n3"

# disjoint intervals
assert run("3\n1 2\n5 6\n9 10\n") == "1\n3\n1 2 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single interval | 1 group | base case |
| fully overlapping | n groups | worst-case overlap |
| endpoint chain | n groups | strict intersection rule |
| disjoint | 1 group | full reuse |

## Edge Cases

A key edge case is when intervals only touch at endpoints. For instance, `[1,2]` and `[2,3]` cannot be grouped together because they intersect at 2. The heap condition `end < l` enforces this strictly, preventing invalid reuse.

Another edge case is when intervals arrive in reverse order. Sorting by left endpoint ensures correctness regardless of input order, since grouping depends only on structure, not sequence.

Finally, when many intervals start at the same point, the algorithm rapidly creates multiple groups. The heap still ensures each new interval is placed optimally among existing chains, and the number of groups matches the maximum simultaneous overlap at that point.
