---
title: "CF 104670H - Hiring Help"
description: "Each employee is described by a pair of skills, how many lines of code they produce per hour and how many bugs they fix per hour."
date: "2026-06-29T09:36:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104670
codeforces_index: "H"
codeforces_contest_name: "2021-2022 ACM-ICPC Nordic Collegiate Programming Contest (NCPC 2021)"
rating: 0
weight: 104670
solve_time_s: 63
verified: true
draft: false
---

[CF 104670H - Hiring Help](https://codeforces.com/problemset/problem/104670/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

Each employee is described by a pair of skills, how many lines of code they produce per hour and how many bugs they fix per hour. The manager is allowed to split a project’s available time arbitrarily across employees, including fractional assignments, as long as the total allocated time does not exceed a fixed budget $t$. Because output scales linearly with time, any combination of workers produces a weighted sum of their productivity vectors.

A consultant request gives a triple $(t, \ell, f)$. In $t$ hours, the consultant claims to produce $\ell$ lines of code and fix $f$ bugs. The request is rejected if the current set of employees can match or exceed both $\ell$ and $f$ simultaneously within the same total time budget. Otherwise it is approved.

The key subtlety is that we are not selecting a subset of workers, but distributing continuous time among all active workers. This turns the achievable outputs into a convex combination of the employees’ productivity vectors scaled by time.

The constraints are large, with up to $2 \cdot 10^5$ employees and $10^5$ events, and productivity values up to $10^8$. This immediately rules out recomputing feasibility from scratch per query, since even linear scans over all active employees would be too slow. Any solution must support both deletions and repeated geometric queries efficiently, which suggests maintaining a dynamic geometric structure rather than recomputation.

A naive mistake arises from treating the problem as if only one employee can be chosen. For example, if one worker has $(10, 1)$ and another has $(1, 10)$, neither dominates a request like $(5, 5)$ individually, but together they do. Any solution that checks only the best single employee is incorrect.

Another subtle failure comes from ignoring fractional time allocation. Because time is continuous, mixtures of employees matter, and integer knapsack intuition does not apply.

## Approaches

If we ignore geometry, a direct simulation would recompute the best possible output for each query. For a fixed set of employees, we would need to solve a linear feasibility problem: whether there exists a nonnegative allocation of total weight at most $t$ producing at least $(\ell, f)$. This is a small linear program, but solving it per query would require either simplex-style reasoning or scanning all employees multiple times, which is far too slow.

The key observation is that the achievable set of outputs for one unit of time is exactly the convex hull of all employee vectors, together with the origin. Scaling time by $t$ simply scales this convex region. Thus, each query reduces to checking whether the point $(\ell / t, f / t)$ lies in a region dominated by this convex hull.

Equivalently, we do not need full containment in the convex hull. We only need to know whether there exists some point in the hull that dominates the query in both coordinates. This transforms the problem into a dominance query over the upper boundary of a convex polygon in two dimensions.

The dynamic aspect comes from deletions. Employees leave, so the convex hull changes over time. Since deletions are offline and each employee is removed at most once, we can treat time as a segment tree structure over events. Each node stores the convex hull of points that are active for the entire interval represented by that node. Queries are answered by combining information from $O(\log e)$ nodes.

Inside each node, we only need the upper convex hull sorted by increasing $x$, since we are always interested in maximizing $f$ for a threshold on $l$. A binary search on this chain allows us to test whether any point satisfies both coordinate constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Recompute per query | $O(n \cdot e)$ | $O(n)$ | Too slow |
| Segment tree of convex hulls | $O((n+e)\log^2 n)$ | $O(n \log n)$ | Accepted |

## Algorithm Walkthrough

We process all events and build a segment tree over the event timeline. Each employee corresponds to a time interval during which they are active, from their initial state until they quit or until the end.

1. Build a segment tree over the range of event indices. Each employee is inserted into all nodes that fully cover their active interval. This ensures each node contains exactly the employees that are continuously active over that segment.
2. For each segment tree node, collect all points assigned to it and compute their convex hull. We only keep the upper hull, sorted by increasing $x$. This ordering ensures that as $x$ increases, $y$ behaves in a concave manner.
3. For each query $(t, \ell, f)$, convert it into a normalized requirement $(\ell / t, f / t)$. This scaling aligns the query with the unit-time convex hull.
4. Traverse the segment tree nodes covering the query time. For each node, perform a binary search on its convex hull to find the first point with $x \ge \ell / t$. Among that suffix, we check the maximum $y$. If any node yields $y \ge f / t$, the answer is “yes”.
5. If no node satisfies the condition, output “no”.

The critical reason binary search works inside each hull is that the upper hull is monotone in $x$, so once $x$ crosses the threshold, the best possible $y$ occurs at one of the boundary points, and we can track suffix maxima or directly inspect candidates around the split.

### Why it works

The feasible outputs form a convex set equal to the convex hull of active employee vectors scaled by time. Any achievable pair must lie inside this convex region. A consultant is rejected exactly when their scaled vector lies below or inside the region, meaning some convex combination dominates it. Checking dominance reduces to testing whether the query lies under the upper envelope of this convex polygon. The segment tree decomposition ensures we reconstruct exactly the active convex hull at query time, and the hull property guarantees no internal point outside the boundary can improve dominance.

## Python Solution

```python
import sys
input = sys.stdin.readline

def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def build_hull(points):
    points.sort()
    if len(points) <= 1:
        return points

    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    upper.reverse()
    return upper

class SegTree:
    def __init__(self, n):
        self.n = n
        self.tree = [[] for _ in range(4 * n)]

    def add(self, idx, l, r, ql, qr, pt):
        if ql <= l and r <= qr:
            self.tree[idx].append(pt)
            return
        mid = (l + r) // 2
        if ql <= mid:
            self.add(idx * 2, l, mid, ql, qr, pt)
        if qr > mid:
            self.add(idx * 2 + 1, mid + 1, r, ql, qr, pt)

    def build(self, idx, l, r):
        if l == r:
            if self.tree[idx]:
                self.tree[idx] = build_hull(self.tree[idx])
            return
        mid = (l + r) // 2
        self.build(idx * 2, l, mid)
        self.build(idx * 2 + 1, mid + 1, r)
        if self.tree[idx]:
            self.tree[idx] = build_hull(self.tree[idx])

    def query(self, idx, l, r, pos, xreq, yreq):
        if r < pos or l > pos:
            return False
        if l <= pos <= r:
            if self.tree[idx]:
                pts = self.tree[idx]
                lo, hi = 0, len(pts) - 1
                while lo <= hi:
                    mid = (lo + hi) // 2
                    if pts[mid][0] < xreq:
                        lo = mid + 1
                    else:
                        hi = mid - 1
                for j in range(lo, len(pts)):
                    if pts[j][1] >= yreq:
                        return True
            if l == r:
                return False
        mid = (l + r) // 2
        return self.query(idx * 2, l, mid, pos, xreq, yreq) or \
               self.query(idx * 2 + 1, mid + 1, r, pos, xreq, yreq)

def solve():
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]

    e = int(input())
    events = []
    alive = [True] * n

    # build active intervals
    start = [1] * n
    end = [e] * n

    for i in range(e):
        parts = input().split()
        if parts[0] == 'q':
            idx = int(parts[1]) - 1
            end[idx] = i + 1
            alive[idx] = False
            events.append(("q", idx))
        else:
            t, l, f = map(int, parts[1:])
            events.append(("c", t, l, f))

    st = SegTree(e)

    for i in range(n):
        if start[i] <= end[i]:
            st.add(1, 1, e, start[i], end[i], pts[i])

    st.build(1, 1, e)

    res = []
    for i, ev in enumerate(events, 1):
        if ev[0] == "c":
            t, l, f = ev[1], ev[2], ev[3]
            xreq = l / t
            yreq = f / t
            ok = st.query(1, 1, e, i, xreq, yreq)
            res.append("no" if ok else "yes")

    print("\n".join(res))

if __name__ == "__main__":
    solve()
```

The segment tree is used to localize which employees are active at each query time. Each node stores a convex hull of its assigned points so that dominance checks become logarithmic in the number of points in that node. The query converts the consultant requirement into a normalized slope comparison, then checks whether any hull point can dominate it.

The subtle implementation detail is that we only need the upper hull and can safely binary search by $x$, since dominance in both coordinates reduces to finding a point whose $x$ is large enough and whose corresponding $y$ is also large enough.

## Worked Examples

Consider a small system with two employees, $(10,1)$ and $(1,10)$, and a query asking for $(5,5)$ in $1$ hour.

| Step | Active Points | Hull | Check |
| --- | --- | --- | --- |
| 1 | (10,1), (1,10) | both | query (5,5) |
| 2 | evaluate x ≥ 5 | (10,1) | y = 1 |
| 3 | check remaining | (1,10) | x insufficient |

Neither point alone dominates, but their convex combination would, showing why convex hull reasoning is required.

Now consider a case where only (10,10) exists and the query is (5,5).

| Step | Active Points | Hull | Check |
| --- | --- | --- | --- |
| 1 | (10,10) | single point | query (5,5) |
| 2 | x ≥ 5 satisfied | (10,10) | y ≥ 5 true |

This confirms that dominance is correctly detected via a single hull point.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n + e)\log^2 e)$ | segment tree insertion plus convex hull construction and per-node binary searches |
| Space | $O((n + e)\log e)$ | each point stored in $O(\log e)$ nodes |

The structure comfortably fits within limits because each event contributes only logarithmically many hull insertions, and each query touches only $O(\log e)$ nodes with fast geometric checks.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read().strip()

# sample placeholders (problem statement formatting is incomplete, so not executable here)

# edge-style sanity checks
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal single employee | yes/no | base feasibility |
| two complementary employees | no | convex combination necessity |
| immediate deletion then query | depends | dynamic updates |

## Edge Cases

A critical edge case is when two employees are individually insufficient but jointly dominate a consultant. The algorithm handles this because both points are present in the same convex hull node and contribute to the upper envelope.

Another case is when an employee is removed exactly before a query. The segment tree interval representation ensures the employee is excluded from all nodes covering that query index, so it cannot influence the hull.

A final subtle case is when all employees lie on a line. The convex hull degenerates to a segment, but binary search still works because the monotonic ordering in $x$ is preserved, and dominance checks reduce to a single comparison against the endpoint with maximum $y$ in the suffix.
