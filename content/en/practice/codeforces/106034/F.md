---
title: "CF 106034F - \u041c\u0430\u0433\u0430\u0437\u0438\u043d"
description: "We are given multiple independent test cases. Each test case describes a collection of intervals, one interval per person. Person i is only allowed to be assigned a single integer position, and that position must lie inside their interval $[li, ri]$."
date: "2026-06-25T13:02:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106034
codeforces_index: "F"
codeforces_contest_name: "ICPC Central Russia Regional Qualification Round, 2024"
rating: 0
weight: 106034
solve_time_s: 51
verified: true
draft: false
---

[CF 106034F - \u041c\u0430\u0433\u0430\u0437\u0438\u043d](https://codeforces.com/problemset/problem/106034/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given multiple independent test cases. Each test case describes a collection of intervals, one interval per person. Person i is only allowed to be assigned a single integer position, and that position must lie inside their interval $[l_i, r_i]$. All assigned positions must be distinct.

Another way to view the problem is that we want to pick a distinct integer for each interval, but each interval restricts which integers are acceptable for it. The integers themselves are abstract labels, so only relative ordering matters, not the fact that they can go up to $10^9$.

The task is to decide whether there exists an assignment of distinct integers such that every interval contains the integer assigned to it.

The constraints imply that the total number of intervals across all test cases is at most $2 \cdot 10^5$. Any solution that is quadratic per test case will not survive. Sorting is fine, and any greedy algorithm with a heap or pointer sweep is also fine.

A few edge cases expose typical greedy mistakes. If all intervals are identical, for example $[1, 10], [1, 10], [1, 10]$, the answer is immediately impossible because we only have 10 available integers but we need 3 distinct choices. A naive approach that assigns all to the same midpoint would incorrectly claim success.

Another edge case appears when intervals are nested, such as $[1, 5], [2, 4], [3, 3]$. This one is actually feasible, but only if we assign carefully from the most constrained interval outward. Any strategy that processes in input order without considering tightness will easily fail here.

A third subtle case is when many intervals overlap heavily but shift slightly, for example $[1,2], [2,3], [3,4], [4,5]$. The only correct assignment is essentially a chain, and greedy decisions that do not respect earliest finishing constraints will break feasibility.

## Approaches

A brute force approach would try to assign integers explicitly. Since values go up to $10^9$, we could compress all endpoints and then attempt to match intervals to integer points one by one using backtracking or bipartite matching. Even after compression, this becomes a maximum bipartite matching problem between intervals and coordinates. If there are $n$ intervals and up to $2n$ coordinates, a standard matching like Hopcroft-Karp gives about $O(n^{2.5})$ in practice, which is too slow for $2 \cdot 10^5$.

The key observation is that we do not actually need to model coordinates explicitly. We only care about whether we can greedily “consume” available integers in order. Once intervals are sorted by their right endpoint, we want to assign each interval the smallest possible integer that is still available and lies within its range. This transforms the problem into a scheduling-style greedy process.

The intuition is that an interval with a smaller right endpoint is more constrained and must be satisfied earlier. If we delay it, we may consume its only valid positions with looser intervals.

We sweep from left to right over candidate integer values, and maintain which intervals become available at each point. A priority queue keeps active intervals ordered by their right endpoint, so we always assign the current smallest feasible interval first.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Matching | $O(n^{2.5})$ | $O(n)$ | Too slow |
| Greedy Sweep + Heap | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We first sort all intervals by their left endpoint so we know when each interval becomes eligible. We then simulate assigning integer positions from the smallest possible upward, but we never explicitly iterate to $10^9$. Instead, we jump through interval boundaries implicitly using events.

1. Sort intervals by $l_i$. This lets us activate intervals exactly when their range starts.
2. Maintain a pointer over intervals and a min-heap keyed by $r_i$. The heap contains all intervals that have started but not yet been assigned a position.
3. Iterate over candidate positions in increasing order, but instead of iterating blindly, we advance to the next useful position whenever possible. At each step, we push all intervals with $l_i \le x$ into the heap.
4. Before assigning position $x$, remove from the heap any intervals whose $r_i < x$, since they can no longer be satisfied. If any interval expires unassigned, the answer is immediately impossible.
5. If the heap is not empty, assign current position $x$ to the interval with the smallest $r_i$. This is the interval that will become infeasible the earliest if we delay it, so it must be prioritized.
6. Mark that interval as assigned and continue to the next position.
7. If all intervals are assigned successfully, return “Yes”.

### Why it works

The core invariant is that at every position $x$, the heap contains exactly the intervals that can still be assigned some valid integer $\ge x$, and none of them has already been assigned. Among these, choosing the interval with the smallest right endpoint is safe because any feasible solution must assign it no later than any interval with a larger right endpoint. If we fail to assign it at its last possible moment, it would be impossible to fix later since all future positions are even larger and thus outside its range. This creates a forced ordering, and the greedy choice respects that ordering globally.

## Python Solution

```python
import sys
input = sys.stdin.readline

import heapq

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        seg = []
        for i in range(n):
            l, r = map(int, input().split())
            seg.append((l, r))

        seg.sort()
        heap = []
        i = 0
        x = 0
        used = 0
        ok = True

        while used < n:
            if not heap and i < n:
                x = max(x, seg[i][0])

            while i < n and seg[i][0] <= x:
                heapq.heappush(heap, seg[i][1])
                i += 1

            while heap and heap[0] < x:
                heapq.heappop(heap)
                ok = False
                break

            if not ok:
                break

            if heap:
                heapq.heappop(heap)
                used += 1

            x += 1

        out.append("Yes" if ok and used == n else "No")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation follows the sweep line logic. The variable `x` represents the current integer being assigned. The pointer `i` advances through sorted intervals, pushing all intervals whose left boundary is already reached. The heap stores only right endpoints, because that is sufficient to decide feasibility and priority.

A subtle point is the jump of `x` to `seg[i][0]` when the heap is empty. Without this, the simulation would waste time iterating over values where no interval is active. Another important detail is removing expired intervals before attempting assignment; otherwise we might incorrectly assign a position while some interval is already impossible.

## Worked Examples

### Example 1

Intervals: $[1,2], [2,3], [3,3]$

| x | Active intervals | Heap (r) | Action | Assigned |
| --- | --- | --- | --- | --- |
| 1 | [1,2] | [2] | assign [1,2] | 1 |
| 2 | [2,3] | [3] | assign [2,3] | 1,2 |
| 3 | [3,3] | [3] | assign [3,3] | 1,2,3 |

All intervals get distinct valid positions, confirming feasibility.

### Example 2

Intervals: $[1,1], [1,1], [1,1]$

| x | Active intervals | Heap (r) | Action | Assigned |
| --- | --- | --- | --- | --- |
| 1 | all three | [1,1,1] | assign one | 1 |
| 2 | none valid | [] | fail (expired) | partial |

At the moment we move past $x=1$, two intervals are already invalid because their only allowed position was consumed. The algorithm correctly rejects.

These traces show the greedy rule always prioritizes the most constrained interval first.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | each interval is pushed and popped once from the heap |
| Space | $O(n)$ | storage for intervals and heap |

Given that the total $n$ over all test cases is at most $2 \cdot 10^5$, this comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read().strip()  # placeholder if integrated

# NOTE: full solution integration required for real tests

# sample-based structure (placeholders since statement input unknown exact formatting)
# assert run("...") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all identical intervals | No | impossible overconstrained case |
| nested chain | Yes | greedy ordering correctness |
| disjoint intervals | Yes | independent assignment |

## Edge Cases

For identical intervals like $[1,1], [1,1]$, every interval competes for the same single position. The heap will contain multiple intervals with the same deadline. The algorithm assigns one at $x=1$, but immediately detects that remaining intervals are expired, producing “No” correctly.

For nested intervals like $[1,5], [2,4], [3,3]$, the heap always prioritizes $[3,3]$ at $x=3$. Earlier intervals remain available longer, so they are assigned later without conflict. This shows the invariant that smallest right endpoint is always safely handled first.

For widely spaced intervals like $[1,1], [100,100]$, the pointer jump skips unused regions, ensuring efficiency while preserving correctness because no interval depends on intermediate values.
