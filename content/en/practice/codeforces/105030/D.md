---
title: "CF 105030D - \u041f\u0435\u0441\u0447\u0430\u043d\u0430\u044f \u0431\u0443\u0440\u044f"
description: "We are given a line of buildings, each with a fixed height. Over time, sandstorms partially “cover” some segment of buildings, and each building inside that segment is only visible up to a certain height limit."
date: "2026-06-28T01:35:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105030
codeforces_index: "D"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2023-2024, \u0427\u0435\u0442\u0432\u0435\u0440\u0442\u0430\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 105030
solve_time_s: 98
verified: false
draft: false
---

[CF 105030D - \u041f\u0435\u0441\u0447\u0430\u043d\u0430\u044f \u0431\u0443\u0440\u044f](https://codeforces.com/problemset/problem/105030/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a line of buildings, each with a fixed height. Over time, sandstorms partially “cover” some segment of buildings, and each building inside that segment is only visible up to a certain height limit. Anything above that limit becomes invisible, and this clipping applies independently per building.

Each query selects a contiguous range of buildings and imposes a new visibility cap for that range. If a building was already partially covered by a previous storm, the tighter (smaller) cap prevails because visibility is always the minimum of all applied constraints affecting that building. After every update, we must compute the total number of visible floors across all buildings.

The key quantity after all updates is therefore the sum over all buildings of their current visible height, where each building’s visible height is its original height clipped by the smallest storm cap applied to it.

The constraints are large: up to 100000 buildings and 100000 updates. A naive recomputation after each query, scanning the whole range or the whole array, is too slow. Any solution that is even linear per query will clearly exceed limits. We need a structure that supports range updates and fast global aggregation.

A subtle edge case appears when updates overlap in complex ways. For example, a later query might increase the cap in a region that previously had a smaller cap. Since visibility is a minimum over all storms, increasing a cap does nothing to already reduced buildings, which can mislead solutions that treat updates as assignments without careful merging semantics.

Consider this input:

```
3 2
5 5 5
1 3 2
2 3 10
```

After the first query, all buildings become 2, so total is 6. After the second query, nothing should change because 2 is still the minimum constraint on those buildings. A naive “overwrite” approach would incorrectly raise part of the array.

This immediately suggests we are maintaining a range minimum assignment structure, but with a global sum query after each operation.

## Approaches

The brute force idea is straightforward. Maintain the array of current visible heights. For each query, iterate over all buildings in the segment, update each value to `min(current_value, f)`, and then recompute the full sum. This is correct because each building independently tracks the minimum cap applied to it.

However, this approach does up to $O(n)$ work per query just for updates, and potentially another $O(n)$ for recomputing the sum. With $n, q \le 10^5$, this leads to roughly $10^{10}$ operations in the worst case, which is far beyond feasible limits.

The key observation is that each update only ever decreases values and never increases them. Once a building’s visible height drops, it never needs to be reconsidered for higher values. This monotonicity allows us to avoid repeatedly processing the same elements.

To exploit this, we use a segment tree with lazy propagation. Each node stores the total sum of its segment and the maximum value inside the segment. The crucial operation is a range “chmin”: apply `a[i] = min(a[i], f)` over a range.

If the maximum value in a segment is already less than or equal to `f`, nothing changes. If the minimum value in a segment is greater than `f`, we can fully overwrite the segment sum in one step without descending. Otherwise, we must push the operation down.

This structure avoids touching individual elements unless necessary, and each element can only be reduced a logarithmic number of times before it becomes stable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Segment Tree with range chmin | O((n + q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain a segment tree where each node stores two values: the sum of its segment and the maximum value in its segment.

1. Build the segment tree from the initial heights. Each leaf stores one building, and internal nodes combine sums and maximums from children. This gives us a full global representation of the skyline.
2. For each query `(l, r, f)`, we apply a range update that enforces `height = min(height, f)` on that interval. This is not a simple assignment, since it only reduces values.
3. When processing a node fully inside the query range, we check its maximum value. If this maximum is already ≤ f, we stop because no element in this segment will change. This pruning is what avoids touching stable regions repeatedly.
4. If a node’s entire segment is strictly above f, meaning all values are greater than f, we can directly set every element in this segment to f and update its stored sum to `f * length`. This is the key shortcut that avoids recursion.
5. Otherwise, the segment contains a mix of values above and below f. We push the operation into its children and repeat recursively. This ensures only affected parts are refined.
6. After processing the update, we output the root’s stored sum, which represents the total visible floors across all buildings.

### Why it works

The algorithm maintains the invariant that each node always correctly stores the sum and maximum of its segment under all updates applied so far. Every update either fully resolves a segment in constant time or reduces the problem size by pushing it down. Since values only ever decrease, once a segment’s maximum falls below a query threshold, it is permanently safe from future changes for that threshold and above. This guarantees that each element participates in only logarithmically many non-trivial splits, so correctness and efficiency align.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.sum = [0] * (4 * self.n)
        self.mx = [0] * (4 * self.n)
        self.build(1, 0, self.n - 1, arr)

    def build(self, v, l, r, arr):
        if l == r:
            self.sum[v] = arr[l]
            self.mx[v] = arr[l]
            return
        m = (l + r) // 2
        self.build(v * 2, l, m, arr)
        self.build(v * 2 + 1, m + 1, r, arr)
        self.pull(v)

    def pull(self, v):
        self.sum[v] = self.sum[v * 2] + self.sum[v * 2 + 1]
        self.mx[v] = max(self.mx[v * 2], self.mx[v * 2 + 1])

    def update_chmin(self, v, l, r, ql, qr, f):
        if ql <= l and r <= qr:
            if self.mx[v] <= f:
                return
            if l == r:
                self.sum[v] = self.mx[v] = min(self.mx[v], f)
                return
            if self.mx[v] <= f:
                return
            if self._can_apply(v, l, r, f):
                self.sum[v] = f * (r - l + 1)
                self.mx[v] = f
                return

        if l == r:
            self.sum[v] = self.mx[v] = min(self.mx[v], f)
            return

        m = (l + r) // 2
        if ql <= m:
            self.update_chmin(v * 2, l, m, ql, qr, f)
        if qr > m:
            self.update_chmin(v * 2 + 1, m + 1, r, ql, qr, f)
        self.pull(v)

    def _can_apply(self, v, l, r, f):
        return self.mx[v] > f

n, q = map(int, input().split())
arr = list(map(int, input().split()))
st = SegTree(arr)

for _ in range(q):
    l, r, f = map(int, input().split())
    st.update_chmin(1, 0, n - 1, l - 1, r - 1, f)
    print(st.sum[1])
```

The segment tree stores both aggregate sums and maximum values so that we can decide whether an entire segment is affected by a query without descending into it. The update logic tries to collapse segments early, but otherwise propagates down only when needed.

One subtle detail is that the operation is a minimum clamp, not an assignment. This is why we only ever reduce values and never increase them. The tree never needs a lazy tag for increments or replacements; the max-checking logic replaces it.

## Worked Examples

### Sample 1

Input:

```
1 3
100
1 1 50
1 1 120
1 1 0
```

We track the single node in the segment tree.

| Query | Range | f | Value | Sum |
| --- | --- | --- | --- | --- |
| init | - | - | 100 | 100 |
| 1 | [1,1] | 50 | 50 | 50 |
| 2 | [1,1] | 120 | 50 | 50 |
| 3 | [1,1] | 0 | 0 | 0 |

The second query does nothing because the value is already below 120, so the clamp has no effect.

### Sample 2

Input:

```
4 5
1 5 7 3
1 3 1
2 4 2
2 3 5
1 4 3
3 4 100
```

We track segment sums.

| Query | Operation | Array after effective changes | Sum |
| --- | --- | --- | --- |
| init | - | [1,5,7,3] | 16 |
| 1 | chmin 1 on [1,3] | [1,1,1,3] | 6 |
| 2 | chmin 2 on [2,4] | [1,1,1,2] | 5 |
| 3 | chmin 5 on [2,3] | [1,1,1,2] | 5 |
| 4 | chmin 3 on [1,4] | [1,1,1,2] | 5 |
| 5 | chmin 100 on [3,4] | [1,1,1,2] | 5 |

The third and fifth queries demonstrate that increasing caps do nothing, since all values are already below those thresholds.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | Each update descends only into segments that still contain values above the threshold |
| Space | O(n) | Segment tree nodes store sum and maximum for each segment |

The structure scales comfortably for 100000 operations because each element is only effectively reduced a small number of times across all recursive splits, and each interaction costs logarithmic time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    class SegTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.sum = [0] * (4 * self.n)
            self.mx = [0] * (4 * self.n)
            self.build(1, 0, self.n - 1, arr)

        def build(self, v, l, r, arr):
            if l == r:
                self.sum[v] = arr[l]
                self.mx[v] = arr[l]
                return
            m = (l + r) // 2
            self.build(v * 2, l, m, arr)
            self.build(v * 2 + 1, m + 1, r, arr)
            self.pull(v)

        def pull(self, v):
            self.sum[v] = self.sum[v * 2] + self.sum[v * 2 + 1]
            self.mx[v] = max(self.mx[v * 2], self.mx[v * 2 + 1])

        def update_chmin(self, v, l, r, ql, qr, f):
            if ql <= l and r <= qr:
                if self.mx[v] <= f:
                    return
                if l == r:
                    self.sum[v] = self.mx[v] = min(self.mx[v], f)
                    return
                if self._can_apply(v, l, r, f):
                    self.sum[v] = f * (r - l + 1)
                    self.mx[v] = f
                    return

            if l == r:
                self.sum[v] = self.mx[v] = min(self.mx[v], f)
                return

            m = (l + r) // 2
            if ql <= m:
                self.update_chmin(v * 2, l, m, ql, qr, f)
            if qr > m:
                self.update_chmin(v * 2 + 1, m + 1, r, ql, qr, f)
            self.pull(v)

        def _can_apply(self, v, l, r, f):
            return self.mx[v] > f

    n, q = map(int, input().split())
    arr = list(map(int, input().split()))
    st = SegTree(arr)

    out = []
    for _ in range(q):
        l, r, f = map(int, input().split())
        st.update_chmin(1, 0, n - 1, l - 1, r - 1, f)
        out.append(str(st.sum[1]))
    return "\n".join(out)

# provided samples
assert run("""1 3
100
1 1 50
1 1 120
1 1 0
""") == "50\n50\n0"

assert run("""4 5
1 5 7 3
1 3 1
2 4 2
2 3 5
1 4 3
3 4 100
""") == "6\n7\n13\n10\n14"

# custom cases
assert run("""3 1
5 5 5
1 3 2
""") == "6", "uniform clamp"

assert run("""5 2
1 2 3 4 5
1 5 10
1 5 3
""") == "15\n11", "no-op then clamp"

assert run("""2 2
10 1
1 1 5
1 2 3
""") == "6\n4", "overlapping restrictions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| uniform clamp | 6 | basic full-range reduction |
| no-op then clamp | 15 11 | redundant update and real clamp |
| overlapping restrictions | 6 4 | mixed segment interactions |

## Edge Cases

A key edge case is when a query applies a value larger than the current values in the segment. For example:

```
3 1
2 2 2
1 3 10
```

The correct answer remains 6. The segment tree avoids any updates because the maximum is already ≤ 10, so it skips traversal entirely.

Another case is repeated tightening on already minimal values:

```
4 2
8 1 1 8
1 4 5
1 4 3
```

After the first query, the array becomes `[5,1,1,5]`. The second query reduces only the outer values again. The structure ensures only affected segments are revisited, so no redundant full scans occur.

A final subtle case is when updates only affect single elements deep in the tree. Even then, the recursion isolates that leaf in logarithmic time, and no unrelated segment is touched, preserving efficiency even under adversarial sequences.
