---
title: "CF 1101C - Division and Union"
description: "We are given several independent test cases. Each test case provides a collection of closed segments on a number line. The task is to assign every segment to one of two groups such that no segment in one group overlaps with any segment in the other group."
date: "2026-06-13T07:21:10+07:00"
tags: ["codeforces", "competitive-programming", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1101
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 58 (Rated for Div. 2)"
rating: 1500
weight: 1101
solve_time_s: 417
verified: false
draft: false
---

[CF 1101C - Division and Union](https://codeforces.com/problemset/problem/1101/C)

**Rating:** 1500  
**Tags:** sortings  
**Solve time:** 6m 57s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent test cases. Each test case provides a collection of closed segments on a number line. The task is to assign every segment to one of two groups such that no segment in one group overlaps with any segment in the other group. Overlap here means the intersection of two segments is non-empty, including touching at a single point.

Another way to view the requirement is that if we pick any segment from group 1 and any segment from group 2, those two segments must be completely disjoint on the line.

We must decide whether such a bipartition of segments exists, and if it does, output one valid assignment.

The constraints are tight enough that any solution that compares all pairs of segments per test case would fail. In the worst case, a single test contains 100000 segments, and there are up to 50000 test cases. A quadratic check inside each test would imply about 10^10 comparisons in total, which is far beyond a 2 second limit. This immediately rules out pairwise checking or any approach that repeatedly scans the full set for each segment.

A subtle corner case appears when all segments are connected through overlaps, even indirectly. For example, if segment A overlaps B, and B overlaps C, even if A does not overlap C, all three effectively form a connected structure. In that case, separating them into two groups without cross intersections becomes impossible if both groups must be non-empty. This situation corresponds to the entire set forming a single connected component under overlap.

Another edge case appears when segments are already cleanly separable by a “gap”. For example, if all segments lie in [1, 10] or [20, 30] with no overlap between the two clusters, then a valid partition exists naturally. The challenge is detecting whether such a split exists and constructing it efficiently.

## Approaches

The naive idea is to treat each segment as a node in a graph and connect two nodes if their segments intersect. Then the condition becomes: we must assign two colors to nodes such that no edge connects different colors. However, this is not a standard bipartite condition, because we are not required to avoid same-color edges, we are required to avoid cross-color edges. That flips the logic: instead of separating adjacent nodes, we must ensure that every connected component is entirely inside one group.

So the naive solution would first build the full intersection graph by checking every pair of segments. If two segments overlap, we union them into a component. Then we try to assign components to two groups. But if there is only one component, we cannot split it into two non-empty groups, so the answer is impossible. If there are at least two components, we can assign each entire component to group 1 or group 2, ensuring both groups are non-empty.

The issue is constructing the intersection structure. Checking all pairs costs O(n^2). Even if we optimize slightly, it remains too slow.

The key observation is that intersection connectivity on segments is captured by sorting. If we sort segments by left endpoint and sweep, we can merge any overlapping chain into a single interval component. Whenever a segment starts after the current maximum right endpoint, we know a new component begins.

Thus, instead of building a graph, we only need to merge intervals into connected components using a single pass after sorting. Once components are identified, the problem reduces to checking whether there is more than one component.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (pairwise overlap graph) | O(n^2) | O(n^2) | Too slow |
| Optimal (sort + sweep merging) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read all segments and keep their original indices. We need indices because output must match input order, not sorted order.
2. Sort segments by their left endpoint. Sorting is essential because it allows us to detect overlaps using a single scan instead of pairwise comparisons.
3. Initialize a current component interval using the first segment. Also maintain a component id counter.
4. Traverse segments from left to right. For each segment, compare its left endpoint with the current component’s maximum right endpoint.
5. If the current segment starts before or at the current maximum right endpoint, it overlaps with the current component, so we merge it by extending the maximum right endpoint if needed.
6. If it starts after the current maximum right endpoint, this means it does not intersect anything in the current component. We finalize the previous component and start a new one.
7. After all segments are processed, we have a partition of segments into connected components where each component is a maximal chain of overlapping segments.
8. If there is only one component, output -1 because any split would force at least one overlap across groups.
9. Otherwise, assign group 1 to all segments in the first component and group 2 to all remaining components.

### Why it works

Two segments are in the same component exactly when there exists a chain of pairwise intersecting segments connecting them. Any segment in one component overlaps (directly or indirectly) with every other segment in that component, so placing them in different groups would force a cross-group intersection. Conversely, segments in different components are separated by a gap in the sorted sweep, meaning no segment in one component can overlap any segment in another. This guarantees that assigning whole components to groups produces a valid solution, and that a solution exists if and only if there are at least two components.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        segs = []
        for i in range(n):
            l, r = map(int, input().split())
            segs.append((l, r, i))

        segs.sort()

        comp = [0] * n
        cid = 0

        cur_l, cur_r, idx = segs[0]

        comp[idx] = cid

        for l, r, i in segs[1:]:
            if l <= cur_r:
                if r > cur_r:
                    cur_r = r
                comp[i] = cid
            else:
                cid += 1
                cur_r = r
                comp[i] = cid

        if cid == 0:
            out.append("-1")
            continue

        ans = [0] * n
        for i in range(n):
            ans[i] = 1 if comp[i] == 0 else 2

        out.append(" ".join(map(str, ans)))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation relies on sorting by left endpoint so that overlap detection reduces to a simple comparison with the running maximum right endpoint. The variable `cur_r` is the key state: it tracks the furthest reach of the current connected component. When a segment lies inside this reach, it is absorbed into the same component. When it lies outside, we start a new component.

A common pitfall is forgetting to preserve original indices. Since sorting rearranges segments, we must store assignments back into the original order. Another subtle issue is that merging only requires tracking the maximum right endpoint; tracking the left boundary is unnecessary because overlaps are determined entirely by whether the next segment starts before the current reach ends.

## Worked Examples

### Example 1

Input:

```
3
2
5 5
2 3
```

Sorted segments become:

(2,3, idx1), (5,5, idx0)

| Step | Segment | cur_r | Component | Action |
| --- | --- | --- | --- | --- |
| 1 | (2,3) | 3 | 0 | start component 0 |
| 2 | (5,5) | 3 → 5 | 1 | new component |

Output assignment becomes:

component 0 → group 1, component 1 → group 2

So output is `2 1`.

This confirms that non-overlapping segments are separated cleanly into different components.

### Example 2

Input:

```
3
3
3 5
2 3
2 3
```

Sorted:

(2,3), (2,3), (3,5)

| Step | Segment | cur_r | Component | Action |
| --- | --- | --- | --- | --- |
| 1 | (2,3) | 3 | 0 | start |
| 2 | (2,3) | 3 | 0 | merge |
| 3 | (3,5) | 5 | 0 | merge |

Only one component is formed.

Since all segments are connected through overlaps, any split would force one group to be empty or introduce cross-group overlap. Output is `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, sweep is linear |
| Space | O(n) | storing segments and component labels |

The total number of segments across all test cases is at most 100000, so the sorting-based approach comfortably fits within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        segs = []
        for i in range(n):
            l, r = map(int, input().split())
            segs.append((l, r, i))

        segs.sort()

        comp = [0] * n
        cid = 0

        cur_r = segs[0][1]
        comp[segs[0][2]] = 0

        for l, r, i in segs[1:]:
            if l <= cur_r:
                cur_r = max(cur_r, r)
                comp[i] = cid
            else:
                cid += 1
                cur_r = r
                comp[i] = cid

        if cid == 0:
            out.append("-1")
        else:
            ans = [1 if comp[i] == 0 else 2 for i in range(n)]
            out.append(" ".join(map(str, ans)))

    return "\n".join(out)

# provided samples
assert run("""3
2
5 5
2 3
3
3 5
2 3
2 3
3
3 3
4 4
5 5
""") == """2 1
-1
1 1 2"""

# minimum size
assert run("""1
2
1 1
2 2
""") in ["1 2", "2 1"]

# all overlapping
assert run("""1
3
1 5
2 6
3 7
""") == "-1"

# already separated
assert run("""1
3
1 2
10 11
20 21
""").count(" ") == 2
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 disjoint segments | any valid split | basic separability |
| fully overlapping chain | -1 | single component detection |
| three separated blocks | valid 1/2 split | multiple components correctness |

## Edge Cases

A fully connected chain of overlapping segments, such as `[1, 5], [2, 6], [3, 7]`, produces a single merged component during the sweep because the running maximum right endpoint never drops. The algorithm assigns all segments to component 0 and correctly outputs `-1`.

A fully disjoint set like `[1,2], [5,6], [10,11]` creates three components because each new segment starts after the previous `cur_r`. The sweep resets correctly at each gap, producing multiple components and enabling a valid two-group split.

Touching segments such as `[1,3]` and `[3,5]` are treated as overlapping because `l <= cur_r`. This ensures they remain in the same component, which is required since they share a point and cannot be separated across groups.
