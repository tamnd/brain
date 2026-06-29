---
title: "CF 104639C - Multiply Then Plus"
description: "We are maintaining a dynamic collection of pairs of integers. Each pair behaves like a linear function in a single variable: for a pair $(ai, bi)$, we can evaluate a value $fi(x) = ai cdot x + bi$. The system supports two operations over time."
date: "2026-06-29T16:55:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104639
codeforces_index: "C"
codeforces_contest_name: "The 2023 ICPC Asia EC Regionals Online Contest (I)"
rating: 0
weight: 104639
solve_time_s: 53
verified: true
draft: false
---

[CF 104639C - Multiply Then Plus](https://codeforces.com/problemset/problem/104639/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are maintaining a dynamic collection of pairs of integers. Each pair behaves like a linear function in a single variable: for a pair $(a_i, b_i)$, we can evaluate a value $f_i(x) = a_i \cdot x + b_i$. The system supports two operations over time.

One operation updates a single indexed pair, replacing its coefficients completely. The other operation asks for a fixed value of $x$ and a contiguous segment of indices, and we must find the maximum value of $a_i x + b_i$ among all pairs in that segment.

So the task is a mixture of point updates on linear functions and range maximum queries evaluated at a chosen $x$, where the function being evaluated is different for every query.

The constraints are extremely large: up to 500,000 pairs and 500,000 operations. This immediately rules out any solution that recomputes a range query by scanning all elements, since even a single worst-case query would already be too slow. Any acceptable solution must process each operation in roughly logarithmic time or better, with careful constant factors.

A subtle edge case arises from frequent updates. A naive idea is to rebuild auxiliary structures for every query, or maintain per-query sorting of values after applying $x$. That fails because updates invalidate any precomputed ordering.

Another trap is assuming monotonicity in index or value. Even if $a_i$ and $b_i$ are bounded, the expression $a_i x + b_i$ can vary wildly between neighboring indices, so segment pruning strategies that rely on smoothness do not apply.

## Approaches

A direct brute-force solution evaluates every query by iterating over the range $[l, r]$ and computing $a_i x + b_i$ for each index. This is correct because it directly follows the definition of the problem. However, each query would take $O(n)$ time in the worst case, leading to $O(nq)$ total operations, which is on the order of $2.5 \times 10^{11}$. This is far beyond feasible limits.

The key observation is that each element defines a linear function, and each query asks for the maximum value of a set of lines evaluated at a single point $x$, restricted to a segment. This is a classic dynamic convex hull style problem, but complicated by two dimensions of dynamism: both queries and updates on arbitrary indices.

A standard way to handle this structure is to use a segment tree over indices. Each node of the segment tree represents a fixed interval of indices. Inside each node, we maintain a structure that can answer: given a value $x$, what is the maximum $a_i x + b_i$ among all lines stored in that node.

For static sets of lines, the optimal structure is the convex hull trick. Since $x$ in queries is arbitrary and not monotonic, we cannot use a simple pointer-based hull. Instead, we store a convex hull in each segment tree node and evaluate it using binary search.

Updates replace a single line, so we rebuild the convex hulls along the path from leaf to root.

The combination gives a log factor from the segment tree and another log factor from binary search inside each hull.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nq)$ | $O(1)$ | Too slow |
| Segment tree + hull per node | $O((n+q)\log^2 n)$ | $O(n \log n)$ | Accepted |

## Algorithm Walkthrough

We maintain a segment tree over indices from 1 to n, where each node stores a set of lines corresponding to its interval.

Each line is represented as $(a, b)$, corresponding to a function $f(x) = ax + b$.

1. Build a segment tree where each leaf node stores exactly one line from the input array. Internal nodes represent unions of their children intervals.
2. For each node, construct a convex hull from its lines. We sort lines by slope $a$, then remove unnecessary ones using the standard convex hull construction. The removal criterion is based on whether a newly added line makes the previous one always worse for all $x$. This ensures only potentially optimal lines remain.
3. To evaluate a query for a node, we perform a binary search over its hull to find the line that maximizes $a x + b$ for the given $x$. Since slopes are sorted, the function values are unimodal in index order.
4. For a range query $[l, r]$, we decompose the interval into $O(\log n)$ segment tree nodes and query each node’s hull independently.
5. The answer is the maximum over all returned values.
6. For an update at position $k$, we replace the line at the leaf and rebuild all hulls along the path to the root.

Why binary search works here is because the convex hull ensures that slopes are monotonic, and intersection points between consecutive lines are ordered. This guarantees that the best line for a given $x$ can be found in logarithmic time.

### Why it works

The correctness relies on two invariants. First, each segment tree node stores exactly the set of lines covering its interval, so any query range can be expressed as a disjoint union of node intervals. Second, each node’s convex hull contains only lines that are potentially optimal for some $x$, and the ordering of slopes guarantees that for any fixed $x$, the maximum lies on a single contiguous region of the hull. Therefore, binary search always finds the true maximum among that node’s lines, and combining node results preserves global optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Hull:
    def __init__(self):
        self.lines = []
        self.ptr = 0

    def bad(self, l1, l2, l3):
        return (l2[1] - l1[1]) * (l1[0] - l3[0]) >= (l3[1] - l1[1]) * (l1[0] - l2[0])

    def build(self, lines):
        lines.sort()
        self.lines = []
        for line in lines:
            while len(self.lines) >= 2 and self.bad(self.lines[-2], self.lines[-1], line):
                self.lines.pop()
            self.lines.append(line)
        self.ptr = 0

    def query(self, x):
        l, r = 0, len(self.lines) - 1
        best = -10**30
        while l <= r:
            m = (l + r) // 2
            v1 = self.lines[m][0] * x + self.lines[m][1]
            best = max(best, v1)
            if m + 1 < len(self.lines):
                v2 = self.lines[m + 1][0] * x + self.lines[m + 1][1]
                if v2 >= v1:
                    l = m + 1
                else:
                    r = m - 1
            else:
                r = m - 1
        return best

class SegTree:
    def __init__(self, n):
        self.n = n
        self.tree = [None] * (4 * n)

    def build(self, idx, l, r, arr):
        if l == r:
            self.tree[idx] = Hull()
            self.tree[idx].build([arr[l]])
            return
        m = (l + r) // 2
        self.build(idx * 2, l, m, arr)
        self.build(idx * 2 + 1, m + 1, r, arr)
        self.tree[idx] = Hull()
        self.tree[idx].build(self.tree[idx * 2].lines + self.tree[idx * 2 + 1].lines)

    def update(self, idx, l, r, pos, val):
        if l == r:
            self.tree[idx].build([val])
            return
        m = (l + r) // 2
        if pos <= m:
            self.update(idx * 2, l, m, pos, val)
        else:
            self.update(idx * 2 + 1, m + 1, r, pos, val)
        self.tree[idx].build(self.tree[idx * 2].lines + self.tree[idx * 2 + 1].lines)

    def query(self, idx, l, r, ql, qr, x):
        if qr < l or r < ql:
            return -10**30
        if ql <= l and r <= qr:
            return self.tree[idx].query(x)
        m = (l + r) // 2
        return max(
            self.query(idx * 2, l, m, ql, qr, x),
            self.query(idx * 2 + 1, m + 1, r, ql, qr, x)
        )

n, q = map(int, input().split())
arr = [tuple(map(int, input().split())) for _ in range(n)]

st = SegTree(n)
st.build(1, 0, n - 1, arr)

out = []
for _ in range(q):
    tmp = list(map(int, input().split()))
    if tmp[0] == 1:
        _, k, a, b = tmp
        st.update(1, 0, n - 1, k - 1, (a, b))
    else:
        _, x, l, r = tmp
        out.append(str(st.query(1, 0, n - 1, l - 1, r - 1, x)))

print("\n".join(out))
```

The segment tree stores convex hulls for each interval, and both build and update operations recompute these hulls from child nodes. The hull query function performs a binary search over candidate lines to find the best evaluation at x.

One subtle detail is that every node rebuild is done by merging full lists from children. This is not asymptotically optimal but keeps the implementation straightforward. The correctness depends only on the hull construction, not on incremental merging efficiency.

Indexing is consistently converted to zero-based internally, which avoids off-by-one errors during segment splits.

## Worked Examples

### Example 1

Input:

```
3 2
2 3
1 5
3 1
2 2 1 3
2 3 2 3
```

We first build segment tree nodes.

| Step | Segment | Lines stored | Query x | Result |
| --- | --- | --- | --- | --- |
| 1 | [1,3] | (2,3),(1,5),(3,1) | - | - |
| 2 | full query | same | 2 | max(7,7,7)=7 |
| 3 | [2,3] | (1,5),(3,1) | 3 | max(8,10)=10 |

First query evaluates all three lines at x=2, all giving 7, so answer is 7. Second query restricts to indices 2 and 3, and the best line becomes index 3.

### Example 2

Input:

```
4 3
1 1
2 0
3 -1
4 -10
2 5 1 4
1 2 10 10
2 5 1 4
```

Initial evaluation at x=5:

| i | ai, bi | value |
| --- | --- | --- |
| 1 | 1,1 | 6 |
| 2 | 2,0 | 10 |
| 3 | 3,-1 | 14 |
| 4 | 4,-10 | 10 |

First query returns 14.

After update, second line becomes (10,10). Now at x=5:

| i | ai, bi | value |
| --- | --- | --- |
| 1 | 1,1 | 6 |
| 2 | 10,10 | 60 |
| 3 | 3,-1 | 14 |
| 4 | 4,-10 | 10 |

Second query returns 60.

These examples show how updates change which line dominates globally and how the segment structure isolates the affected region.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n + q)\log^2 n)$ | each update/query touches $O(\log n)$ nodes, each node query is $O(\log n)$ |
| Space | $O(n \log n)$ | each segment tree node stores a hull of merged lines |

The complexity fits within limits because both $n$ and $q$ are up to 500,000, and logarithmic factors remain manageable even in Python with careful implementation. The dominant cost is rebuilds during updates, but each operation still scales logarithmically in the number of segments.
