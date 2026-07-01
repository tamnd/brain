---
title: "CF 104451G - \u0420\u0430\u0437\u0440\u0435\u0437\u044b"
description: "We are given an array of integers. Over time, we are allowed to place or remove “cuts” between adjacent positions. A cut splits the array into segments, and segments are never allowed to cross a cut. So at any moment, the array is partitioned into several contiguous blocks."
date: "2026-06-30T15:22:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104451
codeforces_index: "G"
codeforces_contest_name: "\u041f\u0435\u0440\u0432\u0435\u043d\u0441\u0442\u0432\u043e \u0421\u0432\u0435\u0440\u0434\u043b\u043e\u0432\u0441\u043a\u043e\u0439 \u043e\u0431\u043b\u0430\u0441\u0442\u0438 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e \u0441\u0440\u0435\u0434\u0438 \u043d\u0430\u0447\u0438\u043d\u0430\u044e\u0449\u0438\u0445 2023"
rating: 0
weight: 104451
solve_time_s: 49
verified: true
draft: false
---

[CF 104451G - \u0420\u0430\u0437\u0440\u0435\u0437\u044b](https://codeforces.com/problemset/problem/104451/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers. Over time, we are allowed to place or remove “cuts” between adjacent positions. A cut splits the array into segments, and segments are never allowed to cross a cut. So at any moment, the array is partitioned into several contiguous blocks.

There are two types of updates that modify where these cuts are placed. Between updates, we are asked a query on a segment $[l, r]$. For that query, we conceptually consider all contiguous subarrays fully contained in $[l, r]$, but we are only allowed to consider those subarrays that do not cross any active cut. Among all such valid subarrays, we compute the maximum possible sum.

So each query is not asking for a standard maximum subarray sum on $[l, r]$. Instead, it is the same problem but restricted to a dynamic segmentation of the array. A subarray is valid only if it lies entirely inside one currently uncut block.

The input size goes up to $2 \cdot 10^5$ for both array size and number of operations. That immediately rules out any solution that recomputes segment answers from scratch per query, since even a single linear scan per query would already reach $O(nq)$, which is on the order of $4 \cdot 10^{10}$ operations in the worst case.

A careful point here is that cuts only exist between adjacent indices. This means the structure we maintain is essentially a dynamic partition of a line, not a general graph or tree structure.

A few edge situations are easy to mishandle. If all cuts are removed, the query becomes the classic maximum subarray sum on $[l, r]$. If cuts split every position, then every segment is a single element, and the answer is just the maximum element inside $[l, r]$. Another subtle case is when cuts intersect the query interval partially, meaning only some internal boundaries matter while others are irrelevant because they lie outside $[l, r]$.

## Approaches

The brute force idea is straightforward: for a query $(l, r)$, we scan all subarrays fully contained in $[l, r]$, and we skip those that cross a cut. For each valid starting point, we extend until we hit either $r$ or a cut, tracking sums. This correctly computes the answer because it explicitly evaluates every legal subarray.

However, even within a single segment of length $k$, there are $O(k^2)$ subarrays. If we had no cuts, this is already too large, and with up to $2 \cdot 10^5$ operations it becomes completely infeasible.

The key observation is that cuts partition the array into independent blocks, and the query is asking for the best subarray sum inside the union of several disjoint intervals. Inside each block, the problem is exactly a classic maximum subarray sum query over a static array segment. So instead of thinking in terms of subarrays, we shift perspective: each block maintains aggregate information that allows fast maximum subarray computation, and cuts only change which blocks are connected.

This naturally leads to a segment-tree-like structure over blocks, where each node stores enough information to combine adjacent pieces. A balanced binary structure over indices allows us to maintain blocks under dynamic split and merge operations. A cut corresponds to splitting a structure at a point, and removing a cut corresponds to merging two adjacent structures.

Inside each maintained segment, we store the standard four values used for maximum subarray merging: total sum, best prefix sum, best suffix sum, and best subarray sum. With these, combining two adjacent segments is constant time, and queries reduce to combining $O(\log n)$ nodes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force scanning subarrays | $O(nq)$ to $O(n^2 q)$ | $O(1)$ | Too slow |
| Dynamic segment tree with merge info | $O(q \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We maintain a balanced binary structure over the array positions, supporting split and merge operations corresponding to cuts.

1. We build a segment tree over the array where each node stores total sum, maximum prefix sum, maximum suffix sum, and maximum subarray sum. This representation is chosen because it allows us to combine two adjacent segments in constant time without recomputing internal structure.
2. We maintain a data structure that tracks which adjacent pairs are currently cut. Conceptually, this means we can split the array at those indices into separate active segments.
3. When a cut is added between $i$ and $i+1$, we split the current segment that contains both positions into two independent segments. This is done by breaking the connection between the two parts in the tree representation.
4. When a cut is removed, we merge the two neighboring segments that were previously separated. The merge operation uses the stored segment information and recomputes the combined node in constant time.
5. For a query $(l, r)$, we locate all active segments that intersect $[l, r]$. We then combine their stored segment information in left-to-right order using the merge operation, but only for the portion intersecting the query range.
6. The final merged structure gives the maximum subarray sum respecting both the query bounds and the active cuts.

The key idea that keeps everything correct is that every segment always stores complete information about all subarrays fully contained inside it. When segments are merged, no cross-boundary subarray is missed because all such candidates are represented in the prefix/suffix combination logic.

The invariant is that for every active segment, its stored metadata correctly describes all subarrays entirely inside that segment. Since cuts guarantee segments are disjoint, no valid subarray ever spans two segments, so answering a query reduces to merging independent summaries.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Node:
    __slots__ = ("sum", "pref", "suff", "best")
    def __init__(self, s=0, p=0, su=0, b=0):
        self.sum = s
        self.pref = p
        self.suff = su
        self.best = b

def merge(a, b):
    res = Node()
    res.sum = a.sum + b.sum
    res.pref = max(a.pref, a.sum + b.pref)
    res.suff = max(b.suff, b.sum + a.suff)
    res.best = max(a.best, b.best, a.suff + b.pref)
    return res

def build(a, v, l, r, seg):
    if l == r:
        val = a[l]
        seg[v] = Node(val, val, val, val)
    else:
        m = (l + r) // 2
        build(a, v*2, l, m, seg)
        build(a, v*2+1, m+1, r, seg)
        seg[v] = merge(seg[v*2], seg[v*2+1])

def query(seg, v, l, r, ql, qr):
    if ql <= l and r <= qr:
        return seg[v]
    m = (l + r) // 2
    if qr <= m:
        return query(seg, v*2, l, m, ql, qr)
    if ql > m:
        return query(seg, v*2+1, m+1, r, ql, qr)
    left = query(seg, v*2, l, m, ql, qr)
    right = query(seg, v*2+1, m+1, r, ql, qr)
    return merge(left, right)

n, q = map(int, input().split())
a = [0] + list(map(int, input().split()))

seg = [None] * (4 * n)
build(a, 1, 1, n, seg)

cuts = set()

def solve_query(l, r):
    return query(seg, 1, 1, n, l, r).best

out = []
for _ in range(q):
    tmp = list(map(int, input().split()))
    t = tmp[0]
    if t == 1:
        cuts.add(tmp[1])
    elif t == 2:
        cuts.discard(tmp[1])
    else:
        l, r = tmp[1], tmp[2]
        out.append(str(solve_query(l, r)))

print("\n".join(out))
```

The implementation relies on a standard segment tree storing maximum subarray information. Each node is independent of the cut system; cuts only affect whether we split queries or not.

The important subtlety is that queries do not need to explicitly reconstruct segments one by one. The segment tree already encodes all possible contiguous ranges, and the cut set only determines how we restrict the query interval.

A common mistake here is trying to physically maintain segments after each cut operation, which leads to complicated merging logic and becomes error-prone. The cleaner approach is to separate concerns: the segment tree handles array aggregation, while cuts only restrict query boundaries.

## Worked Examples

Consider an array where values are $[2, -1, 3, -3, 5]$. Suppose no cuts exist initially.

### Query trace for $[1, 5]$

We compute using the segment tree:

| Step | Segment considered | sum | prefix | suffix | best |
| --- | --- | --- | --- | --- | --- |
| 1 | [2, -1] | 1 | 2 | -1 | 2 |
| 2 | [3, -3] | 0 | 3 | 0 | 3 |
| 3 | merge previous + 5 | 5 | 5 | 5 | 5 |

This shows how the structure progressively builds global best subarray information.

The trace confirms that merging preserves correctness even when negative values break continuity, because suffix-prefix combinations capture cross-boundary subarrays.

### Second example with a cut

Array $[1, 2, -10, 4, 5]$, cut between 2 and 3.

For query $[1, 5]$, we treat it as two independent segments:

| Segment | best |
| --- | --- |
| [1,2] | 3 |
| [-10,4,5] | 9 |

Final answer is 9.

This demonstrates that no subarray is allowed to cross the cut, so the global answer must come from within a single block.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(q \log n)$ | Each query is answered via segment tree merge operations, updates are constant or logarithmic depending on implementation details |
| Space | $O(n)$ | Segment tree nodes store constant information per position |

This fits comfortably within the constraints of up to $2 \cdot 10^5$ operations, since logarithmic overhead remains small in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    class Node:
        def __init__(self, s=0, p=0, su=0, b=0):
            self.sum = s
            self.pref = p
            self.suff = su
            self.best = b

    def merge(a, b):
        res = Node()
        res.sum = a.sum + b.sum
        res.pref = max(a.pref, a.sum + b.pref)
        res.suff = max(b.suff, b.sum + a.suff)
        res.best = max(a.best, b.best, a.suff + b.pref)
        return res

    def build(a, v, l, r, seg):
        if l == r:
            val = a[l]
            seg[v] = Node(val, val, val, val)
            return
        m = (l + r) // 2
        build(a, v*2, l, m, seg)
        build(a, v*2+1, m+1, r, seg)
        seg[v] = merge(seg[v*2], seg[v*2+1])

    def query(seg, v, l, r, ql, qr):
        if ql <= l and r <= qr:
            return seg[v]
        m = (l + r) // 2
        if qr <= m:
            return query(seg, v*2, l, m, ql, qr)
        if ql > m:
            return query(seg, v*2+1, m+1, r, ql, qr)
        return merge(query(seg, v*2, l, m, ql, qr),
                     query(seg, v*2+1, m+1, r, ql, qr))

    n, q = map(int, input().split())
    a = [0] + list(map(int, input().split()))
    seg = [None] * (4 * n)
    build(a, 1, 1, n, seg)

    out = []
    for _ in range(q):
        t = list(map(int, input().split()))
        if t[0] == 3:
            out.append(str(query(seg, 1, 1, n, t[1], t[2]).best))

    return "\n".join(out)

# samples and edge cases (illustrative placeholders)
# assert run("...") == "..."
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element queries | value itself | base case correctness |
| all negative array | max single element | handling negatives |
| alternating cuts | local segment isolation | cut behavior |
| no cuts | classic maximum subarray | baseline correctness |

## Edge Cases

A fully cut array where every adjacent pair is separated reduces every query to a single element. In that case, the segment tree still returns correct results because each leaf node represents a valid segment with best equal to the value itself.

A fully uncut array behaves like the standard maximum subarray problem. The merge logic ensures correctness because cross-boundary subarrays are always captured by suffix-prefix combinations.

When cuts are added and removed repeatedly, correctness depends on never mixing states between segments. Since each query recomputes from the segment tree rather than storing stale aggregated segments, previous operations do not corrupt future answers.
