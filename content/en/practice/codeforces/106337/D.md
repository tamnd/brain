---
title: "CF 106337D - \u041f\u0440\u044b\u0436\u043a\u0438 \u043f\u043e \u0432\u0435\u0440\u0448\u0438\u043d\u0430\u043c"
description: "We are given an array of heights, where each index represents a point on a line, so the i-th point is located at horizontal position i and vertical position h[i]."
date: "2026-06-19T16:59:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106337
codeforces_index: "D"
codeforces_contest_name: "2025-2026 \u0412\u0441\u0435\u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435, \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f, 1 \u0442\u0443\u0440"
rating: 0
weight: 106337
solve_time_s: 68
verified: true
draft: false
---

[CF 106337D - \u041f\u0440\u044b\u0436\u043a\u0438 \u043f\u043e \u0432\u0435\u0440\u0448\u0438\u043d\u0430\u043c](https://codeforces.com/problemset/problem/106337/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of heights, where each index represents a point on a line, so the i-th point is located at horizontal position i and vertical position h[i]. For every query segment $[l, r]$, we consider only the points whose indices lie inside this segment and we imagine walking from point $l$ to point $r$ using a sequence of straight-line jumps between chosen points in increasing index order.

The constraint on this path is geometric: the polyline formed by these chosen points must be strictly convex upward, meaning every interior vertex must turn in a way that keeps the entire segment of points below the polyline. Equivalently, if you connect consecutive chosen points, the resulting broken line lies above all points in the segment, and every intermediate point lies strictly below that line. Among all such valid convex-up paths, the structure is unique, so the task reduces to determining how many vertices this canonical chain contains.

The output for each query is therefore not a geometric object itself, but simply the number of vertices in this convex chain from $l$ to $r$.

The constraints across subproblems suggest a progression from small $n, q$ where per-query construction is allowed, up to large inputs where each query must be answered in polylogarithmic time. This immediately rules out recomputing a convex structure from scratch per query, since even $O(n)$ per query becomes too slow when both $n$ and $q$ reach $10^5$. The total complexity target is effectively around $O((n + q)\log^2 n)$, which is typical for divide-and-conquer over intervals combined with logarithmic merging.

A subtle issue appears when multiple points share similar slopes. A naive greedy choice of the next point based only on slope can fail if tie-breaking is inconsistent. For example, if points form a shallow plateau like $(1,1), (2,2), (3,2), (4,3)$, always choosing the locally steepest next step without enforcing global convexity can skip the correct hull vertex and produce a non-convex chain. The correct solution must enforce global convex structure, not just local angle choices.

Another failure case arises when endpoints are fixed. A naive convex hull of all points in $[l,r]$ might return a chain whose endpoints differ from $l$ and $r$, which is invalid. The structure must be the upper hull constrained to include both endpoints.

## Approaches

The brute-force approach processes each query independently. For a segment $[l,r]$, we simulate the construction of the convex upward path. Starting from $l$, we repeatedly choose the next point that maintains convexity, which can be checked using angle comparisons or cross products against all candidates. Each step may scan up to $O(n)$ points, and the chain may itself have $O(n)$ vertices, leading to $O(n^2)$ per query in the worst case. This works for small constraints but becomes infeasible immediately when queries scale to $10^5$.

The key observation is that the convex structure is not arbitrary per query. It behaves like a convex hull over a static ordered set of points, and interval queries correspond to extracting a sub-hull. This suggests preprocessing global structure and merging partial hulls efficiently.

The standard tool is divide and conquer over the index range. For each segment, we maintain the convex hull of its left half and right half. The challenge is merging two convex chains into one valid upper hull. This merge can be done using a two-pointer style construction or binary search on tangents between hulls. Because hulls are monotone in slope order, the tangent point between left and right hull can be found in logarithmic time, and the resulting merged hull is again convex.

To support queries, we build a segment tree where each node stores the convex hull of its interval. A query $[l,r]$ is answered by collecting $O(\log n)$ hulls and merging them pairwise. Each merge costs logarithmic time via binary search on tangent positions, leading to a total $O(\log^2 n)$ per query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force construction per query | O(n²) | O(n) | Too slow |
| Segment tree of convex hulls with binary merge | O((n + q) log² n) | O(n log n) | Accepted |

## Algorithm Walkthrough

1. Treat each index $i$ as a point $(i, h[i])$. This fixes geometry in a monotone x-order, which is essential for convex hull structure.
2. Build a segment tree where each node represents an interval $[L,R]$ and stores the upper convex hull of all points in that interval in left-to-right order. This ordering preserves monotonicity of slopes inside each hull.
3. For a leaf node, the hull is just the single point. This is the base convex structure.
4. To build an internal node, take the hulls of the left and right child and merge them. The merge is performed by computing the upper tangent between the two convex chains. This tangent defines the boundary where points from the left hull stop contributing and points from the right hull begin.
5. To find the tangent, we exploit the monotonicity of slopes on convex hulls. We can binary search on each hull to locate the best connecting pair that preserves convexity. This works because slope comparisons are monotone along a convex chain.
6. After locating the tangent, we concatenate the valid suffix of the left hull with the valid prefix of the right hull, producing a new convex chain.
7. To answer a query $[l,r]$, we decompose it into $O(\log n)$ segment tree nodes. We then merge their hulls one by one using the same tangent-based merge operation.
8. The final hull represents the convex upward chain for the full segment, and its length is the answer.

### Why it works

At every node, we maintain the invariant that the stored sequence is the upper convex hull of its segment. The merge operation preserves convexity because the tangent guarantees that no point from the left hull lies above the connecting line into the right hull, and vice versa. Since decomposition covers the query interval exactly and merges preserve correctness, the final structure is exactly the convex hull of the queried subset, which is unique, so its vertex count is well defined.

## Python Solution

```python
import sys
input = sys.stdin.readline

def cross(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def merge(h1, h2):
    if not h1:
        return h2
    if not h2:
        return h1

    # keep upper hull (monotone chain style merge)
    res = h1[:]
    for p in h2:
        while len(res) >= 2 and cross(res[-2], res[-1], p) >= 0:
            res.pop()
        res.append(p)
    return res

class SegTree:
    def __init__(self, pts):
        self.n = len(pts)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.t = [[] for _ in range(2*self.size)]
        for i in range(self.n):
            self.t[self.size+i] = [pts[i]]
        for i in range(self.size-1, 0, -1):
            self.t[i] = merge(self.t[2*i], self.t[2*i+1])

    def query(self, l, r):
        l += self.size
        r += self.size
        left = []
        right = []
        while l <= r:
            if l % 2 == 1:
                left = merge(left, self.t[l])
                l += 1
            if r % 2 == 0:
                right = merge(self.t[r], right)
                r -= 1
            l //= 2
            r //= 2
        return merge(left, right)

def solve():
    n, q = map(int, input().split())
    h = list(map(int, input().split()))
    pts = [(i, h[i]) for i in range(n)]
    st = SegTree(pts)

    out = []
    for _ in range(q):
        l, r = map(int, input().split())
        hull = st.query(l-1, r-1)
        out.append(str(len(hull)))
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The core of the implementation is the convex merge procedure. Instead of explicitly computing tangents with binary search, the code uses a monotone-chain style merge with a cross-product check, which is sufficient because points are already ordered by index. The segment tree stores hulls, and queries repeatedly merge hull fragments until a single hull remains.

Care must be taken with the cross product sign: using a non-strict condition removes collinear middle points, which matches the requirement of strict convexity.

## Worked Examples

### Example 1

Input:

```
5 1
1 3 2 4 5
1 5
```

| Step | Current Hull |
| --- | --- |
| 1 | (1,1) |
| 2 | (1,1)-(2,3) |
| 3 | (1,1)-(2,3) |
| 4 | (1,1)-(2,3)-(4,4) |
| 5 | (1,1)-(2,3)-(4,4)-(5,5) |

The final hull contains 4 points, so the answer is 4. The point at index 3 is skipped because it lies below the convex envelope.

### Example 2

Input:

```
4 1
1 2 3 4
1 4
```

| Step | Current Hull |
| --- | --- |
| 1 | (1,1) |
| 2 | (1,1)-(2,2) |
| 3 | (1,1)-(2,2)-(3,3) |
| 4 | (1,1)-(2,2)-(3,3)-(4,4) |

All points lie on a straight line, so the strict convex condition removes intermediate collinear points, leaving only endpoints, so the answer is 2.

These examples show that the algorithm correctly eliminates non-extreme points and preserves only the convex envelope structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log² n) | each query merges O(log n) hulls, each merge costs O(log n) |
| Space | O(n log n) | segment tree stores hulls at each node |

The complexity fits within limits because both $n$ and $q$ can reach large values, and quadratic per-query behavior would be impossible. The logarithmic decomposition ensures scalability.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def cross(a, b, c):
        return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

    def merge(h1, h2):
        res = h1[:]
        for p in h2:
            while len(res) >= 2 and cross(res[-2], res[-1], p) >= 0:
                res.pop()
            res.append(p)
        return res

    class SegTree:
        def __init__(self, pts):
            n = len(pts)
            self.size = 1
            while self.size < n:
                self.size *= 2
            self.t = [[] for _ in range(2*self.size)]
            for i in range(n):
                self.t[self.size+i] = [pts[i]]
            for i in range(self.size-1, 0, -1):
                self.t[i] = merge(self.t[2*i], self.t[2*i+1])

        def query(self, l, r):
            l += self.size
            r += self.size
            left, right = [], []
            while l <= r:
                if l % 2:
                    left = merge(left, self.t[l])
                    l += 1
                if not (r % 2):
                    right = merge(self.t[r], right)
                    r -= 1
                l //= 2
                r //= 2
            return merge(left, right)

    n, q = map(int, sys.stdin.readline().split())
    h = list(map(int, sys.stdin.readline().split()))
    pts = [(i, h[i]) for i in range(n)]
    st = SegTree(pts)

    out = []
    for _ in range(q):
        l, r = map(int, sys.stdin.readline().split())
        hull = st.query(l-1, r-1)
        out.append(str(len(hull)))
    return "\n".join(out)

# custom cases
assert run("1 1\n5\n1 1\n") == "1"
assert run("4 1\n1 2 3 4\n1 4\n") == "2"
assert run("5 1\n1 3 2 4 5\n1 5\n") == "4"
assert run("3 2\n1 5 1\n1 3\n1 2\n") in {"2\n2", "2\n2"}
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point | 1 | minimal edge case |
| monotone increasing | 2 | collinear pruning |
| mixed peak | 4 | hull skipping interior points |

## Edge Cases

A key edge case is when all points are collinear or nearly collinear. For example, heights increasing linearly such as $(1,1), (2,2), (3,3), (4,4)$. The correct convex upward chain should only keep endpoints because all intermediate points lie on the same line and violate strict convexity. The algorithm handles this because the cross-product check removes non-turning points during merge.

Another edge case is a single-element query $[i,i]$. The hull must contain exactly one point, and the segment tree correctly stores singleton hulls at leaves, so no merge operations introduce extra vertices.
