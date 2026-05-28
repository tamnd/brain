---
title: "CF 91E - Igloo Skyscraper"
description: "Each walrus builds a skyscraper whose height changes linearly over time. Walrus i starts with height a[i] and gains b[i] floors every minute, so at time t its height equals: $$hi(t) = ai + bi cdot t$$ For every query [l, r, t], we must find an index inside that interval whose…"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "geometry"]
categories: ["algorithms"]
codeforces_contest: 91
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 75 (Div. 1 Only)"
rating: 2500
weight: 91
solve_time_s: 164
verified: true
draft: false
---

[CF 91E - Igloo Skyscraper](https://codeforces.com/problemset/problem/91/E)

**Rating:** 2500  
**Tags:** data structures, geometry  
**Solve time:** 2m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

Each walrus builds a skyscraper whose height changes linearly over time. Walrus `i` starts with height `a[i]` and gains `b[i]` floors every minute, so at time `t` its height equals:

$$h_i(t) = a_i + b_i \cdot t$$

For every query `[l, r, t]`, we must find an index inside that interval whose skyscraper is tallest at time `t`.

The straightforward interpretation is: among all lines

$$y = a_i + b_i t$$

restricted to indices in `[l, r]`, return the one with maximum value at `t`.

The constraints immediately rule out anything quadratic. With `n, q ≤ 10^5`, even an `O(n)` scan per query would require roughly `10^{10}` operations in the worst case. We need something close to `O(log^2 n)` or `O(\sqrt n)` per query.

The most dangerous part of this problem is that the maximum changes over time. A walrus that is best at small `t` may become worse later because another walrus has a larger slope.

Consider this example:

```
2 2
100 1
1 100
1 2 0
1 2 2
```

At time `0`, walrus `1` wins with height `100`.

At time `2`, walrus `2` wins with height `201`.

A structure that stores only the current maximum or compares walruses by a fixed ordering fails immediately.

Another subtle case is ties.

```
2 1
5 3
5 3
1 2 10
```

Both walruses have the same height forever. Any answer is valid. A careless convex hull implementation that removes equal lines incorrectly may accidentally delete all candidates or keep the wrong one.

One more trap is handling lines with identical slopes.

```
3 1
1 5
10 5
7 5
1 3 100
```

All slopes are equal, so the walrus with largest intercept always dominates the others. If equal slopes are not processed carefully during hull construction, binary search on intersections becomes invalid because parallel lines never intersect.

The geometry viewpoint is the key observation. Each walrus corresponds to a line, and each query asks for the maximum line at one x-coordinate over a subarray of indices.

## Approaches

The brute-force solution evaluates every walrus inside `[l, r]`.

For one query we compute:

$$a_i + b_i \cdot t$$

for all `i` in the interval and return the index with maximum value.

This is correct because it directly implements the definition of the problem. The issue is cost. A query may inspect `O(n)` walruses, so the total complexity becomes `O(nq)`. With both values equal to `10^5`, this reaches `10^{10}` evaluations, far beyond the limit.

The crucial observation is that every walrus defines a line in the plane. A query asks for the upper envelope at coordinate `t`.

If we had all lines globally, we could build a convex hull trick structure. The difficulty is the interval restriction `[l, r]`.

This suggests combining two ideas:

First, use a segment tree over indices. Every node stores all lines belonging to that segment.

Second, inside each node, build a convex hull for maximum queries.

Then a query interval `[l, r]` decomposes into `O(log n)` segment tree nodes. For each node we query its hull at time `t`, and the best among those answers is the global maximum.

Why does this work well here? Because every walrus belongs to only `O(log n)` segment tree nodes. The total number of stored lines becomes `O(n log n)`, which is manageable.

Inside a node, we sort lines by slope and construct the upper hull. Since queries only ask for a single x-coordinate, we can binary search on intersection points to find the best line in `O(log n)` time.

The final complexity becomes `O(log^2 n)` per query, fast enough for `10^5` operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Optimal | O(n log n + q log² n) | O(n log n) | Accepted |

## Algorithm Walkthrough

1. Represent every walrus as a line.

For walrus `i`, define:

$$f_i(t) = a_i + b_i t$$

We also store index `i` because queries must return the walrus number, not only the height.
2. Build a segment tree over walrus indices.

Each node corresponds to some interval of indices. The node stores all lines whose walruses belong to that interval.
3. For every node, sort lines by slope.

If two lines have the same slope, only the one with larger intercept matters because it dominates the other for every `t`.
4. Construct the upper convex hull for the node.

While inserting lines in slope order, remove useless lines from the back.

Suppose we already have lines `A` and `B`, and want to insert `C`. If the intersection of `A` and `B` occurs to the right of the intersection of `B` and `C`, then `B` is never optimal and can be removed.
5. Store the hull as an ordered list of lines.

Since slopes are sorted, the optimal line for increasing `t` also moves monotonically along the hull.
6. Process a query `[l, r, t]`.

Decompose the interval into `O(log n)` segment tree nodes.
7. Query each node hull independently.

For a fixed `t`, binary search on the hull to find the line with maximum value at `t`.
8. Compare all candidate answers.

Evaluate every returned line at time `t` and keep the best walrus index.

### Why it works

Every walrus line appears in every segment tree node whose interval contains its index. When querying `[l, r]`, the segment tree decomposition covers exactly the walruses in that interval and nothing else.

Inside one node, the convex hull stores precisely the lines that can become maximum for some time value. Any removed line is dominated by others for all possible `t`, so removing it cannot change answers.

Binary search works because along the upper hull, the optimal line changes monotonically as `t` increases. The intersections between consecutive hull lines are ordered, which is exactly the property maintained during hull construction.

Combining all queried nodes guarantees we consider every walrus in `[l, r]`, and taking the maximum among their best candidates gives the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**30

class Line:
    __slots__ = ("m", "b", "idx")

    def __init__(self, m, b, idx):
        self.m = m
        self.b = b
        self.idx = idx

    def value(self, x):
        return self.m * x + self.b

def bad(l1, l2, l3):
    return (l3.b - l1.b) * (l1.m - l2.m) <= (l2.b - l1.b) * (l1.m - l3.m)

class Hull:
    __slots__ = ("lines",)

    def __init__(self, arr):
        arr.sort(key=lambda x: (x.m, x.b))

        filtered = []
        for line in arr:
            if filtered and filtered[-1].m == line.m:
                if filtered[-1].b < line.b:
                    filtered[-1] = line
            else:
                filtered.append(line)

        hull = []
        for line in filtered:
            while len(hull) >= 2 and bad(hull[-2], hull[-1], line):
                hull.pop()
            hull.append(line)

        self.lines = hull

    def query(self, x):
        lines = self.lines

        lo, hi = 0, len(lines) - 1

        while lo < hi:
            mid = (lo + hi) // 2

            if lines[mid].value(x) <= lines[mid + 1].value(x):
                lo = mid + 1
            else:
                hi = mid

        best = lines[lo]
        return best.value(x), best.idx

class SegmentTree:
    def __init__(self, a, b):
        self.n = len(a)
        self.tree = [[] for _ in range(4 * self.n)]

        self.build(1, 0, self.n - 1, a, b)

    def build(self, node, l, r, a, b):
        if l == r:
            self.tree[node] = Hull([Line(b[l], a[l], l + 1)])
            return

        mid = (l + r) // 2

        self.build(node * 2, l, mid, a, b)
        self.build(node * 2 + 1, mid + 1, r, a, b)

        merged = []

        merged.extend(self.tree[node * 2].lines)
        merged.extend(self.tree[node * 2 + 1].lines)

        self.tree[node] = Hull(merged)

    def query(self, node, l, r, ql, qr, t):
        if ql <= l and r <= qr:
            return self.tree[node].query(t)

        mid = (l + r) // 2

        best_val = -INF
        best_idx = -1

        if ql <= mid:
            val, idx = self.query(node * 2, l, mid, ql, qr, t)
            if val > best_val:
                best_val = val
                best_idx = idx

        if qr > mid:
            val, idx = self.query(node * 2 + 1, mid + 1, r, ql, qr, t)
            if val > best_val:
                best_val = val
                best_idx = idx

        return best_val, best_idx

def solve():
    n, q = map(int, input().split())

    a = [0] * n
    b = [0] * n

    for i in range(n):
        a[i], b[i] = map(int, input().split())

    seg = SegmentTree(a, b)

    ans = []

    for _ in range(q):
        l, r, t = map(int, input().split())

        _, idx = seg.query(1, 0, n - 1, l - 1, r - 1, t)

        ans.append(str(idx))

    sys.stdout.write("\n".join(ans))

solve()
```

The `Line` class stores slope, intercept, and original walrus index. The expression is written as `m * x + b`, where `m = b[i]` and `b = a[i]`.

The `bad` function implements the convex hull removal condition using cross multiplication. Using integer arithmetic avoids floating point precision problems.

Hull construction first sorts by slope. If two lines have identical slopes, only the larger intercept survives because the smaller one can never win.

The binary search inside `Hull.query` relies on the fact that values along the upper hull form a unimodal sequence at fixed `x`. Comparing adjacent lines is enough to determine which side contains the optimum.

The segment tree stores a hull at every node. Building merges the hull lines from both children and rebuilds the hull for the parent.

One subtle implementation detail is indexing. The tree works internally with `0`-based indices, but the answer must use original `1`-based walrus numbers, so the line stores `l + 1`.

Another important detail is that query comparison uses only `>` instead of `>=`. The problem allows any valid answer in ties, so either choice works.

## Worked Examples

### Sample 1

Input:

```
5 4
4 1
3 5
6 2
3 5
6 5
1 5 2
1 3 5
1 1 0
1 5 0
```

The walrus lines are:

| Walrus | Formula |
| --- | --- |
| 1 | 4 + t |
| 2 | 3 + 5t |
| 3 | 6 + 2t |
| 4 | 3 + 5t |
| 5 | 6 + 5t |

Query `[1, 5, 2]`.

| Walrus | Height at t=2 |
| --- | --- |
| 1 | 6 |
| 2 | 13 |
| 3 | 10 |
| 4 | 13 |
| 5 | 16 |

The answer is walrus `5`.

Query `[1, 3, 5]`.

| Walrus | Height at t=5 |
| --- | --- |
| 1 | 9 |
| 2 | 28 |
| 3 | 16 |

The answer is walrus `2`.

This example shows how larger slopes eventually dominate even if their starting heights are smaller.

### Custom Example

```
3 2
100 1
1 100
50 2
1 3 0
1 3 10
```

At time `0`:

| Walrus | Height |
| --- | --- |
| 1 | 100 |
| 2 | 1 |
| 3 | 50 |

Answer: `1`

At time `10`:

| Walrus | Height |
| --- | --- |
| 1 | 110 |
| 2 | 1001 |
| 3 | 70 |

Answer: `2`

This trace demonstrates why static ordering is impossible. The maximum changes over time because slopes matter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + q log² n) | Each query touches O(log n) nodes and performs O(log n) hull searches |
| Space | O(n log n) | Every line appears in O(log n) segment tree nodes |

With `10^5` walruses and queries, roughly a few million operations are performed, which fits comfortably within the limits in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

INF = 10**30

class Line:
    __slots__ = ("m", "b", "idx")

    def __init__(self, m, b, idx):
        self.m = m
        self.b = b
        self.idx = idx

    def value(self, x):
        return self.m * x + self.b

def bad(l1, l2, l3):
    return (l3.b - l1.b) * (l1.m - l2.m) <= (l2.b - l1.b) * (l1.m - l3.m)

class Hull:
    def __init__(self, arr):
        arr.sort(key=lambda x: (x.m, x.b))

        filtered = []
        for line in arr:
            if filtered and filtered[-1].m == line.m:
                if filtered[-1].b < line.b:
                    filtered[-1] = line
            else:
                filtered.append(line)

        hull = []
        for line in filtered:
            while len(hull) >= 2 and bad(hull[-2], hull[-1], line):
                hull.pop()
            hull.append(line)

        self.lines = hull

    def query(self, x):
        lines = self.lines

        lo, hi = 0, len(lines) - 1

        while lo < hi:
            mid = (lo + hi) // 2

            if lines[mid].value(x) <= lines[mid + 1].value(x):
                lo = mid + 1
            else:
                hi = mid

        best = lines[lo]
        return best.value(x), best.idx

class SegmentTree:
    def __init__(self, a, b):
        self.n = len(a)
        self.tree = [[] for _ in range(4 * self.n)]

        self.build(1, 0, self.n - 1, a, b)

    def build(self, node, l, r, a, b):
        if l == r:
            self.tree[node] = Hull([Line(b[l], a[l], l + 1)])
            return

        mid = (l + r) // 2

        self.build(node * 2, l, mid, a, b)
        self.build(node * 2 + 1, mid + 1, r, a, b)

        merged = []
        merged.extend(self.tree[node * 2].lines)
        merged.extend(self.tree[node * 2 + 1].lines)

        self.tree[node] = Hull(merged)

    def query(self, node, l, r, ql, qr, t):
        if ql <= l and r <= qr:
            return self.tree[node].query(t)

        mid = (l + r) // 2

        best_val = -INF
        best_idx = -1

        if ql <= mid:
            val, idx = self.query(node * 2, l, mid, ql, qr, t)
            if val > best_val:
                best_val = val
                best_idx = idx

        if qr > mid:
            val, idx = self.query(node * 2 + 1, mid + 1, r, ql, qr, t)
            if val > best_val:
                best_val = val
                best_idx = idx

        return best_val, best_idx

def solve():
    input = sys.stdin.readline

    n, q = map(int, input().split())

    a = []
    b = []

    for _ in range(n):
        x, y = map(int, input().split())
        a.append(x)
        b.append(y)

    seg = SegmentTree(a, b)

    out = []

    for _ in range(q):
        l, r, t = map(int, input().split())

        _, idx = seg.query(1, 0, n - 1, l - 1, r - 1, t)

        out.append(str(idx))

    return "\n".join(out)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run(
"""5 4
4 1
3 5
6 2
3 5
6 5
1 5 2
1 3 5
1 1 0
1 5 0
"""
) == "5\n2\n1\n5"

# minimum size
assert run(
"""1 1
7 3
1 1 10
"""
) == "1"

# equal slopes
assert run(
"""3 1
1 5
10 5
7 5
1 3 100
"""
) == "2"

# changing maximum over time
assert run(
"""2 2
100 1
1 100
1 2 0
1 2 10
"""
) == "1\n2"

# single-element range inside larger array
assert run(
"""4 2
1 1
2 2
3 3
4 4
2 2 100
4 4 0
"""
) == "2\n4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single walrus | Always itself | Minimum constraints |
| Equal slopes | Largest intercept wins | Parallel line handling |
| Changing maximum | Different answers over time | Correct hull transitions |
| Single-element interval | Exact index returned | Segment tree boundaries |

## Edge Cases

Consider identical slopes again:

```
3 1
1 5
10 5
7 5
1 3 100
```

All lines are parallel. During hull construction, only the line with intercept `10` survives because:

$$10 + 5t > 7 + 5t$$

and

$$10 + 5t > 1 + 5t$$

for every `t`.

The query correctly returns walrus `2`.

Now consider ties:

```
2 1
5 3
5 3
1 2 10
```

Both lines are identical. The hull may keep either one. At time `10`, both evaluate to `35`, so either index is valid according to the statement.

Finally, consider a dominance switch:

```
2 2
100 1
1 100
1 2 0
1 2 2
```

At `t = 0`:

| Walrus | Height |
| --- | --- |
| 1 | 100 |
| 2 | 1 |

At `t = 2`:

| Walrus | Height |
| --- | --- |
| 1 | 102 |
| 2 | 201 |

The convex hull stores both lines because each is optimal on some interval of `t`. Binary search over the hull transitions from walrus `1` to walrus `2` exactly after their intersection point.
