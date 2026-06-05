---
title: "CF 280D - k-Maximum Subsequence Sum"
description: "We maintain an array that changes over time. There are two kinds of operations. One operation updates a single position. The other asks for the maximum total sum obtainable by selecting at most k pairwise disjoint subarrays inside a given interval [l, r]."
date: "2026-06-05T08:49:07+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "flows", "graphs", "implementation"]
categories: ["algorithms"]
codeforces_contest: 280
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 172 (Div. 1)"
rating: 2800
weight: 280
solve_time_s: 147
verified: true
draft: false
---

[CF 280D - k-Maximum Subsequence Sum](https://codeforces.com/problemset/problem/280/D)

**Rating:** 2800  
**Tags:** data structures, flows, graphs, implementation  
**Solve time:** 2m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain an array that changes over time.

There are two kinds of operations. One operation updates a single position. The other asks for the maximum total sum obtainable by selecting at most `k` pairwise disjoint subarrays inside a given interval `[l, r]`.

The phrase "at most `k`" is crucial. We are never forced to take a negative contribution. If every possible subarray has negative sum, the correct answer is `0`, obtained by selecting no segments at all.

The array length reaches `10^5`, and there are up to `10^5` operations. Query intervals can cover almost the entire array. A solution that scans the interval for every query is impossible. Even `O(n)` per operation would require around `10^10` work in the worst case.

A second important observation is that `k ≤ 20`. The interval may be huge, but the number of segments we are allowed to choose is very small. That asymmetry is the key to the solution.

Several edge cases make the problem trickier than a standard maximum subarray query.

Consider:

```
[-5, -2, -7]
k = 3
```

The answer is `0`, not `-2`. A solution that always chooses exactly `k` segments would fail.

Consider:

```
[9, -8, 9, -1, -1, -1, 9, -8, 9]
k = 2
```

Taking the two individually best positive blocks gives `9 + 9 = 18`, but the optimal answer is `25`, obtained by joining through some negative values. Local choices do not work.

Consider:

```
[10, -100, 10]
k = 1
```

The answer is `10`, not `20`. When only one segment is allowed, the two positive values cannot be taken independently.

Updates create another challenge. Precomputing answers for every interval is impossible because a single modification may affect many intervals.

The final solution must support both interval optimization and point updates efficiently.

## Approaches

The most direct approach is dynamic programming on every query interval.

Suppose a query asks about `[l, r]`. We could run the classical DP for selecting at most `k` disjoint subarrays inside that interval. For an interval of length `m`, this requires roughly `O(mk)` time.

The DP is correct because it explicitly tracks how many segments have been opened and closed. Unfortunately, in the worst case `m = 10^5` and there are up to `10^4` such queries. Even with `k ≤ 20`, this becomes roughly

```
10^4 × 10^5 × 20 = 2 × 10^10
```

operations.

We need a way to answer interval queries without scanning the interval.

The key observation comes from a well-known reduction between maximum disjoint-subarray problems and min-cost/max-cost flow.

Imagine every array element as an edge whose profit equals its value. Selecting a subarray corresponds to sending one unit of flow through a consecutive block of those profit edges. Restricting ourselves to at most `k` subarrays becomes a capacity constraint of `k`.

For a fixed interval, the answer becomes the maximum cost of sending at most `k` units of flow.

This still sounds expensive until we exploit two facts.

First, `k` is tiny, at most `20`.

Second, the graph corresponding to an interval is extremely structured. Every augmenting path corresponds exactly to a maximum-sum subarray in the current residual network.

The residual-network operations can be implemented using a segment tree that supports:

1. Maximum subarray sum queries.
2. Point updates.
3. Negating an entire chosen subarray.

After finding the current best subarray, we augment one unit of flow. In the residual graph this is equivalent to reversing the sign of every element inside that chosen segment. Then we search again.

This is exactly the classic successive-shortest-path interpretation of maximum-cost flow.

A segment tree storing maximum-subarray information can find the best segment in `O(log n)`. Negating a whole segment is handled with lazy propagation. Since at most `k ≤ 20` augmentations are needed, each query costs only `O(k log n)`.

Updates are ordinary point modifications in the same segment tree.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP per query | O((r-l+1)k) | O(r-l+1) | Too slow |
| Segment tree + flow interpretation | O(k log n) per query, O(log n) update | O(n) | Accepted |

## Algorithm Walkthrough

The accepted solution uses the classical segment-tree representation of a maximum-subarray structure together with the flow reduction.

Each segment tree node stores enough information to answer maximum-subarray queries and also enough information to support sign reversals.

For every segment we maintain:

- Total sum.
- Best prefix sum.
- Best suffix sum.
- Best subarray sum.

We also maintain the corresponding minimum versions because negation swaps maxima and minima.

### 1. Build the segment tree

For a leaf containing value `x`, both maximum and minimum structures are known immediately.

Internal nodes are merged using the standard maximum-subarray formulas.

### 2. Handle a point update

When `a[i]` becomes `val`, update the corresponding leaf and recompute all ancestors.

The segment tree remains consistent after `O(log n)` work.

### 3. Start answering a query `(l,r,k)`

The flow interpretation says we repeatedly send one more unit of flow while the best augmenting path has positive cost.

Initially the residual network is represented by the current array values.

### 4. Find the maximum-sum subarray inside `[l,r]`

Using the segment tree, obtain the maximum-subarray information for the interval.

This gives both the value of the best segment and its endpoints.

### 5. Stop if the value is non-positive

The problem allows selecting fewer than `k` segments.

Once the best available segment has value `≤ 0`, every remaining augmenting path is non-profitable, so the answer cannot increase.

### 6. Add the segment value to the answer

This corresponds to sending one more unit of flow.

### 7. Negate the chosen segment

In the residual graph, using a segment introduces reverse edges with opposite cost.

The segment-tree implementation realizes exactly the same effect by multiplying every element of that chosen subarray by `-1`.

Lazy propagation makes this operation `O(log n)`.

### 8. Repeat up to `k` times

Each iteration finds the next best augmenting path in the residual graph.

### 9. Restore all modified segments

The query must not permanently change the array.

Every segment negated during the query is negated once more at the end, restoring the original state.

### Why it works

The flow reduction converts the problem of choosing up to `k` disjoint subarrays into a maximum-cost flow problem with unit augmentations.

In the residual network, the maximum-cost augmenting path corresponds exactly to the current maximum-sum subarray. Augmenting one unit of flow reverses the costs along that path, which is represented by negating the chosen segment.

Successive augmentations in a maximum-cost flow algorithm always produce an optimal flow. Since each augmentation is implemented exactly by the segment-tree operations above, the sequence of selected segments is identical to the sequence produced by the flow algorithm.

Stopping when the best available profit becomes non-positive is correct because additional augmentations cannot increase total cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10 ** 18

class Node:
    __slots__ = (
        "sum",
        "mx",
        "mxl",
        "mxr",
        "mn",
        "mnl",
        "mnr",
        "mx_pos",
        "mxl_pos",
        "mxr_pos",
        "mn_pos",
        "mnl_pos",
        "mnr_pos",
    )

    def __init__(self):
        self.sum = 0

        self.mx = self.mxl = self.mxr = -INF
        self.mn = self.mnl = self.mnr = INF

        self.mx_pos = (0, 0)
        self.mxl_pos = (0, 0)
        self.mxr_pos = (0, 0)

        self.mn_pos = (0, 0)
        self.mnl_pos = (0, 0)
        self.mnr_pos = (0, 0)

def merge(a, b):
    res = Node()

    res.sum = a.sum + b.sum

    if a.mxl >= a.sum + b.mxl:
        res.mxl = a.mxl
        res.mxl_pos = a.mxl_pos
    else:
        res.mxl = a.sum + b.mxl
        res.mxl_pos = (a.mxl_pos[0], b.mxl_pos[1])

    if b.mxr >= b.sum + a.mxr:
        res.mxr = b.mxr
        res.mxr_pos = b.mxr_pos
    else:
        res.mxr = b.sum + a.mxr
        res.mxr_pos = (a.mxr_pos[0], b.mxr_pos[1])

    res.mx = a.mx
    res.mx_pos = a.mx_pos

    if b.mx > res.mx:
        res.mx = b.mx
        res.mx_pos = b.mx_pos

    cross = a.mxr + b.mxl
    if cross > res.mx:
        res.mx = cross
        res.mx_pos = (a.mxr_pos[0], b.mxl_pos[1])

    if a.mnl <= a.sum + b.mnl:
        res.mnl = a.mnl
        res.mnl_pos = a.mnl_pos
    else:
        res.mnl = a.sum + b.mnl
        res.mnl_pos = (a.mnl_pos[0], b.mnl_pos[1])

    if b.mnr <= b.sum + a.mnr:
        res.mnr = b.mnr
        res.mnr_pos = b.mnr_pos
    else:
        res.mnr = b.sum + a.mnr
        res.mnr_pos = (a.mnr_pos[0], b.mnr_pos[1])

    res.mn = a.mn
    res.mn_pos = a.mn_pos

    if b.mn < res.mn:
        res.mn = b.mn
        res.mn_pos = b.mn_pos

    cross = a.mnr + b.mnl
    if cross < res.mn:
        res.mn = cross
        res.mn_pos = (a.mnr_pos[0], b.mnl_pos[1])

    return res

class SegTree:
    def __init__(self, arr):
        self.n = len(arr) - 1
        self.t = [Node() for _ in range(self.n * 4 + 5)]
        self.lazy = [False] * (self.n * 4 + 5)
        self.build(1, 1, self.n, arr)

    def apply(self, p):
        node = self.t[p]

        node.sum = -node.sum

        node.mx, node.mn = -node.mn, -node.mx
        node.mxl, node.mnl = -node.mnl, -node.mxl
        node.mxr, node.mnr = -node.mnr, -node.mxr

        node.mx_pos, node.mn_pos = node.mn_pos, node.mx_pos
        node.mxl_pos, node.mnl_pos = node.mnl_pos, node.mxl_pos
        node.mxr_pos, node.mnr_pos = node.mnr_pos, node.mxr_pos

        self.lazy[p] ^= True

    def push(self, p):
        if self.lazy[p]:
            self.apply(p << 1)
            self.apply(p << 1 | 1)
            self.lazy[p] = False

    def build(self, p, l, r, arr):
        if l == r:
            x = arr[l]
            node = self.t[p]

            node.sum = x

            node.mx = node.mxl = node.mxr = x
            node.mn = node.mnl = node.mnr = x

            node.mx_pos = node.mxl_pos = node.mxr_pos = (l, l)
            node.mn_pos = node.mnl_pos = node.mnr_pos = (l, l)
            return

        m = (l + r) >> 1
        self.build(p << 1, l, m, arr)
        self.build(p << 1 | 1, m + 1, r, arr)

        self.t[p] = merge(self.t[p << 1], self.t[p << 1 | 1])

    def update_point(self, p, l, r, idx, val):
        if l == r:
            node = self.t[p]

            node.sum = val

            node.mx = node.mxl = node.mxr = val
            node.mn = node.mnl = node.mnr = val

            node.mx_pos = node.mxl_pos = node.mxr_pos = (l, l)
            node.mn_pos = node.mnl_pos = node.mnr_pos = (l, l)
            return

        self.push(p)

        m = (l + r) >> 1
        if idx <= m:
            self.update_point(p << 1, l, m, idx, val)
        else:
            self.update_point(p << 1 | 1, m + 1, r, idx, val)

        self.t[p] = merge(self.t[p << 1], self.t[p << 1 | 1])

    def update_range(self, p, l, r, ql, qr):
        if ql <= l and r <= qr:
            self.apply(p)
            return

        self.push(p)

        m = (l + r) >> 1

        if ql <= m:
            self.update_range(p << 1, l, m, ql, qr)
        if qr > m:
            self.update_range(p << 1 | 1, m + 1, r, ql, qr)

        self.t[p] = merge(self.t[p << 1], self.t[p << 1 | 1])

    def query(self, p, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.t[p]

        self.push(p)

        m = (l + r) >> 1

        if qr <= m:
            return self.query(p << 1, l, m, ql, qr)
        if ql > m:
            return self.query(p << 1 | 1, m + 1, r, ql, qr)

        left = self.query(p << 1, l, m, ql, qr)
        right = self.query(p << 1 | 1, m + 1, r, ql, qr)

        return merge(left, right)

def solve():
    n = int(input())
    arr = [0] + list(map(int, input().split()))

    seg = SegTree(arr)

    m = int(input())
    ans = []

    for _ in range(m):
        q = list(map(int, input().split()))

        if q[0] == 0:
            _, idx, val = q
            seg.update_point(1, 1, n, idx, val)
        else:
            _, l, r, k = q

            changed = []
            cur = 0

            for _ in range(k):
                node = seg.query(1, 1, n, l, r)

                if node.mx <= 0:
                    break

                cur += node.mx

                x, y = node.mx_pos
                changed.append((x, y))

                seg.update_range(1, 1, n, x, y)

            for x, y in changed:
                seg.update_range(1, 1, n, x, y)

            ans.append(str(cur))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The segment tree stores both maximum-subarray and minimum-subarray information. The minimum version is necessary because negating a segment turns maxima into minima and vice versa. Without storing both, lazy sign reversal would become impossible.

The `apply()` function is the most subtle part. Negation changes every sum's sign. A maximum subarray after negation corresponds exactly to the negative of the previous minimum subarray. The code swaps the maximum and minimum structures while negating their values.

During a query we repeatedly extract the best subarray, add its contribution, negate it, and continue. Every negated interval is remembered. After finishing, all those intervals are negated again so the global array returns to its original state.

The implementation uses 1-based indexing throughout because interval endpoints are stored directly inside tree nodes. This avoids many off-by-one mistakes.

## Worked Examples

### Example 1

Input:

```
9 -8 9 -1 -1 -1 9 -8 9
k = 2
```

| Iteration | Best segment | Segment sum | Running answer |
| --- | --- | --- | --- |
| 1 | [1,7] | 16 | 16 |
| 2 | [9,9] | 9 | 25 |

The answer becomes `25`.

This example shows why greedily taking the visibly positive blocks is insufficient. The optimal first segment deliberately includes several negative values because that creates a larger total contribution.

### Example 2

Input:

```
-5 -2 -7
k = 3
```

| Iteration | Best segment sum | Action |
| --- | --- | --- |
| 1 | -2 | Stop |

The answer is `0`.

This demonstrates the "at most `k`" condition. The algorithm stops as soon as the best available segment is non-positive.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) update, O(k log n) query | Each augmentation requires one interval query and one range negation |
| Space | O(n) | Segment tree and lazy arrays |

Since `k ≤ 20`, every query performs only a small constant number of segment-tree operations. With `n, m ≤ 10^5`, this easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    old_stdout = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = old_stdout
    return out.getvalue().strip()

# provided sample
assert run(
"""9
9 -8 9 -1 -1 -1 9 -8 9
3
1 1 9 1
1 1 9 2
1 4 6 3
"""
) == "17\n25\n0", "sample"

# minimum size
assert run(
"""1
5
1
1 1 1 1
"""
) == "5"

# all negative
assert run(
"""3
-1 -2 -3
1
1 1 3 5
"""
) == "0"

# update then query
assert run(
"""3
1 2 3
2
0 2 -10
1 1 3 2
"""
) == "4"

# off-by-one interval
assert run(
"""5
1 2 3 4 5
1
1 5 5 1
"""
) == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single positive element | 5 | Minimum array size |
| All negative values | 0 | Choosing zero segments |
| Update before query | 4 | Point-update correctness |
| Interval `[5,5]` | 5 | Boundary handling |
| Official sample | 17,25,0 | Core functionality |

## Edge Cases

Consider:

```
3
-5 -2 -7
1
1 1 3 3
```

The maximum-subarray query returns `-2`. Since this value is non-positive, the augmentation loop terminates immediately. No segment is chosen and the output becomes `0`. This matches the requirement that selecting zero segments is allowed.

Consider:

```
3
10 -100 10
1
1 1 3 1
```

The best subarray is either the first or third element, with value `10`. Because only one augmentation is permitted, the algorithm stops after selecting one segment. It never combines both positive values through the large negative gap.

Consider:

```
5
1 2 3 4 5
2
0 5 -10
1 4 5 1
```

After the update, the interval `[4,5]` becomes `[4,-10]`. The segment tree recomputes all affected ancestors. The subsequent query returns `4`, obtained from the single-element segment `[4,4]`. This confirms that updates propagate correctly through the maximum-subarray structure.

Consider:

```
5
5 -1 5 -1 5
1
1 1 5 10
```

Although `k=10`, only a finite number of profitable augmentations exist. After the positive contributions are exhausted, the best residual segment becomes non-positive and the algorithm stops early. The answer is still optimal because additional segments would not increase the total sum.
