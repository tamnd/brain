---
title: "CF 484E - Sign on Fence"
description: "We have a fence represented by an array of heights. A rectangular sign must be placed on top of some consecutive panels. The sign has a fixed width w, so it must cover exactly w consecutive fence panels."
date: "2026-06-07T17:25:15+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 484
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 276 (Div. 1)"
rating: 2500
weight: 484
solve_time_s: 199
verified: true
draft: false
---

[CF 484E - Sign on Fence](https://codeforces.com/problemset/problem/484/E)

**Rating:** 2500  
**Tags:** binary search, constructive algorithms, data structures  
**Solve time:** 3m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a fence represented by an array of heights. A rectangular sign must be placed on top of some consecutive panels. The sign has a fixed width `w`, so it must cover exactly `w` consecutive fence panels. Its height cannot exceed the shortest panel among those covered, otherwise part of the sign would stick out above the fence.

For a query `(l, r, w)`, we may choose any consecutive block of exactly `w` panels entirely contained inside the interval `[l, r]`. If we place the sign on a block `[x, x+w-1]`, the maximum possible sign height equals

$$\min(h_x,h_{x+1},\ldots,h_{x+w-1}).$$

Among all valid placements inside `[l,r]`, we want the largest such value.

Equivalently, each query asks:

$$\max_{x \in [l,r-w+1]}
\min(h_x,\ldots,h_{x+w-1}).$$

The fence contains up to $10^5$ panels and there are up to $10^5$ queries. Any algorithm that scans the query interval directly is hopeless. Even an $O((r-l+1)\log n)$ solution per query could require around $10^{10}$ operations in the worst case.

The constraints suggest that all queries must be processed together. A complexity around $O((n+m)\log^2 n)$ or $O((n+m)\log n)$ is appropriate.

A subtle aspect is that the answer is not the minimum height over the whole interval. We are free to choose where the width-`w` sign is placed.

Consider:

```
heights = [5,1,5]
query = (1,3,1)
```

The answer is `5`, because width `1` allows choosing either endpoint. A solution that simply takes the minimum over `[1,3]` would incorrectly return `1`.

Another common mistake is forgetting that the sign width is fixed.

```
heights = [4,4,1,4]
query = (1,4,3)
```

The valid windows are `[4,4,1]` and `[4,1,4]`, both having minimum `1`. The answer is `1`, even though there exists a shorter window with minimum `4`.

A third edge case occurs when the whole interval must be used.

```
heights = [7,3,5]
query = (1,3,3)
```

Only one placement exists, so the answer is the interval minimum, namely `3`.

The optimal solution must correctly handle all of these situations.

## Approaches

The most direct solution evaluates every possible placement of the sign. For a query `(l,r,w)`, we examine all starting positions from `l` to `r-w+1`. For each width-`w` window we compute its minimum height and take the maximum.

This is correct because it explicitly checks every legal sign placement.

The problem is the running time. A query interval may contain $O(n)$ candidate windows. Even if a range minimum structure gives each window minimum in $O(1)$, a single query still costs $O(n)$. With $10^5$ queries, the worst case becomes $10^{10}$ operations.

The key observation is to stop thinking about answers directly and instead ask a decision question:

For a height threshold $H$, does there exist a width-`w` block inside `[l,r]` whose every panel has height at least $H$?

If we mark every position with height at least $H$ as active, the question becomes:

Is there a consecutive active segment inside `[l,r]` of length at least `w`?

This transforms the original optimization problem into a monotone decision problem. If height $H$ works, every smaller height also works. That monotonicity suggests binary search.

However, binary searching independently for every query would still be too expensive. The standard trick is parallel binary search.

For a fixed threshold $H$, we activate all positions with height at least $H$. Then we need a data structure that can answer:

Inside interval `[l,r]`, what is the maximum length of a consecutive active segment?

This can be maintained with a segment tree storing:

- longest active prefix
- longest active suffix
- longest active segment
- interval length

As heights are activated in descending order, updates are point assignments.

Parallel binary search groups together all queries currently testing the same height rank. During one sweep of the heights, we activate panels and evaluate all those queries. Each query needs only $O(\log n)$ segment tree work per binary-search round.

The resulting complexity becomes $O((n+m)\log^2 n)$, which fits comfortably.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(mn)$ | $O(1)$ | Too slow |
| Optimal | $O((n+m)\log^2 n)$ | $O(n+m)$ | Accepted |

## Algorithm Walkthrough

First compress the candidate answers. The answer to every query must equal one of the fence heights, because increasing the sign height only changes feasibility when passing a panel height.

Let the distinct heights be sorted in descending order.

### 1. Initialize a binary search range for every query

For each query maintain indices `low` and `high` into the sorted distinct heights.

Initially every height is possible, so:

`low = 0`

`high = number_of_distinct_heights - 1`

### 2. Repeatedly perform one round of parallel binary search

For every unresolved query compute

$$mid = \frac{low+high}{2}.$$

Group queries by their current midpoint.

All queries in the same group are asking whether a particular height threshold is feasible.

### 3. Sweep heights from largest to smallest

Sort fence positions by height descending.

Process midpoint groups in descending threshold order.

Whenever the current threshold decreases, activate all fence positions whose height is at least that threshold.

The active set exactly represents panels that can support a sign of that height.

### 4. Maintain active segments in a segment tree

Each leaf corresponds to one panel.

An inactive panel stores:

- prefix = 0
- suffix = 0
- best = 0

An active panel stores:

- prefix = 1
- suffix = 1
- best = 1

When combining two children:

$$prefix =
\begin{cases}
left.length + right.prefix & \text{if left is completely active}\\
left.prefix & \text{otherwise}
\end{cases}$$

The suffix is computed symmetrically.

The best segment is the maximum of:

- left.best
- right.best
- left.suffix + right.prefix

### 5. Answer feasibility queries

For query `(l,r,w)` obtain the segment tree information on `[l,r]`.

The field `best` equals the longest consecutive active run inside that interval.

The threshold is feasible exactly when

$$best \ge w.$$

If feasible, move the binary search toward larger heights.

Otherwise move it toward smaller heights.

### 6. Continue until all searches finish

After about `log(number_of_distinct_heights)` rounds, every query converges to one height value.

### 7. Output the corresponding height

The final binary-search position identifies the largest feasible threshold, which is exactly the answer.

### Why it works

Fix a threshold $H$. A width-`w` sign of height at least $H$ exists inside `[l,r]` if and only if there are `w` consecutive panels in that interval whose heights are all at least $H$.

After activating exactly those panels with height at least $H$, such a sign exists if and only if the interval contains an active run of length at least `w`.

The segment tree computes the longest active run in every queried interval, so the feasibility test is correct.

Feasibility is monotone. If a threshold $H$ is feasible, every smaller threshold is also feasible because activating more panels cannot destroy an existing valid run. Binary search therefore finds the largest feasible threshold. Parallel binary search evaluates many such searches simultaneously while reusing the same activation sweep. Hence every reported value is exactly the maximum achievable sign height.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, n):
        self.n = n
        self.pref = [0] * (4 * n)
        self.suff = [0] * (4 * n)
        self.best = [0] * (4 * n)
        self.length = [0] * (4 * n)
        self._build(1, 0, n - 1)

    def _build(self, v, tl, tr):
        self.length[v] = tr - tl + 1
        if tl == tr:
            return
        tm = (tl + tr) // 2
        self._build(v * 2, tl, tm)
        self._build(v * 2 + 1, tm + 1, tr)

    def _pull(self, v):
        lc = v * 2
        rc = lc + 1

        self.pref[v] = self.pref[lc]
        if self.pref[lc] == self.length[lc]:
            self.pref[v] += self.pref[rc]

        self.suff[v] = self.suff[rc]
        if self.suff[rc] == self.length[rc]:
            self.suff[v] += self.suff[lc]

        self.best[v] = max(
            self.best[lc],
            self.best[rc],
            self.suff[lc] + self.pref[rc]
        )

    def update(self, v, tl, tr, pos):
        if tl == tr:
            self.pref[v] = 1
            self.suff[v] = 1
            self.best[v] = 1
            return

        tm = (tl + tr) // 2
        if pos <= tm:
            self.update(v * 2, tl, tm, pos)
        else:
            self.update(v * 2 + 1, tm + 1, tr, pos)

        self._pull(v)

    def query(self, v, tl, tr, l, r):
        if l == tl and r == tr:
            return (
                self.pref[v],
                self.suff[v],
                self.best[v],
                self.length[v]
            )

        tm = (tl + tr) // 2

        if r <= tm:
            return self.query(v * 2, tl, tm, l, r)

        if l > tm:
            return self.query(v * 2 + 1, tm + 1, tr, l, r)

        left = self.query(v * 2, tl, tm, l, tm)
        right = self.query(v * 2 + 1, tm + 1, tr, tm + 1, r)

        lp, ls, lb, ll = left
        rp, rs, rb, rl = right

        pref = lp
        if lp == ll:
            pref += rp

        suff = rs
        if rs == rl:
            suff += ls

        best = max(lb, rb, ls + rp)

        return (pref, suff, best, ll + rl)

def solve():
    n = int(input())
    h = list(map(int, input().split()))

    m = int(input())

    queries = []
    for _ in range(m):
        l, r, w = map(int, input().split())
        queries.append((l - 1, r - 1, w))

    vals = sorted(set(h), reverse=True)
    k = len(vals)

    low = [0] * m
    high = [k - 1] * m

    positions = sorted(
        [(h[i], i) for i in range(n)],
        reverse=True
    )

    while True:
        buckets = [[] for _ in range(k)]
        active = False

        for i in range(m):
            if low[i] < high[i]:
                active = True
                mid = (low[i] + high[i]) // 2
                buckets[mid].append(i)

        if not active:
            break

        seg = SegTree(n)

        ptr = 0

        for mid in range(k):
            threshold = vals[mid]

            while ptr < n and positions[ptr][0] >= threshold:
                seg.update(1, 0, n - 1, positions[ptr][1])
                ptr += 1

            for qi in buckets[mid]:
                l, r, w = queries[qi]
                best = seg.query(1, 0, n - 1, l, r)[2]

                if best >= w:
                    high[qi] = mid
                else:
                    low[qi] = mid + 1

    ans = [str(vals[low[i]]) for i in range(m)]
    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The segment tree stores exactly the information needed to merge consecutive active runs. The `best` value is the longest active segment inside a node's interval. The prefix and suffix lengths allow runs crossing the midpoint to be reconstructed.

The binary search is performed over distinct heights rather than over the full range up to $10^9$. This reduces the search depth to about `log2(n)`.

A common implementation mistake is getting the binary-search direction backward. The height array `vals` is sorted in descending order. Smaller indices correspond to larger heights. When a threshold is feasible we keep searching toward larger heights, which means moving the upper bound to `mid`.

Another subtle point is rebuilding the segment tree every parallel-binary-search round. Each round represents a fresh sweep over thresholds, so the active set must be reconstructed from scratch.

## Worked Examples

### Example 1

Input:

```
5
1 2 2 3 3
1
2 5 3
```

Distinct heights are `[3,2,1]`.

| Mid Height | Active Positions | Query Interval | Longest Active Run | Feasible |
| --- | --- | --- | --- | --- |
| 2 | 2,3,4,5 | [2,5] | 4 | Yes |
| 3 | 4,5 | [2,5] | 2 | No |

Binary search first verifies that height `2` works. It then tests height `3`, which fails because there are only two consecutive panels of height at least `3`. The answer is `2`.

This demonstrates the monotonicity property. Once `3` fails, every larger threshold must also fail.

### Example 2

Input:

```
4
5 1 5 5
1
1 4 2
```

Distinct heights are `[5,1]`.

| Mid Height | Active Positions | Query Interval | Longest Active Run | Feasible |
| --- | --- | --- | --- | --- |
| 5 | 1,3,4 | [1,4] | 2 | Yes |

The active run `[3,4]` has length `2`, so a width-2 sign can be placed with height `5`.

This example shows why we need the longest consecutive run rather than simply counting active panels. There are three active panels, but only two are adjacent.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n+m)\log^2 n)$ | About $\log n$ parallel binary search rounds, each performing $O(n+m)$ segment-tree operations |
| Space | $O(n+m)$ | Segment tree, queries, binary-search state |

With $n,m \le 10^5$, $\log n$ is roughly 17. The resulting operation count is well within the 4-second limit and comfortably fits inside the memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    class SegTree:
        def __init__(self, n):
            self.n = n
            self.pref = [0] * (4 * n)
            self.suff = [0] * (4 * n)
            self.best = [0] * (4 * n)
            self.length = [0] * (4 * n)
            self.build(1, 0, n - 1)

        def build(self, v, l, r):
            self.length[v] = r - l + 1
            if l == r:
                return
            m = (l + r) // 2
            self.build(v * 2, l, m)
            self.build(v * 2 + 1, m + 1, r)

        def pull(self, v):
            lc = v * 2
            rc = lc + 1

            self.pref[v] = self.pref[lc]
            if self.pref[lc] == self.length[lc]:
                self.pref[v] += self.pref[rc]

            self.suff[v] = self.suff[rc]
            if self.suff[rc] == self.length[rc]:
                self.suff[v] += self.suff[lc]

            self.best[v] = max(
                self.best[lc],
                self.best[rc],
                self.suff[lc] + self.pref[rc]
            )

        def update(self, v, l, r, pos):
            if l == r:
                self.pref[v] = self.suff[v] = self.best[v] = 1
                return
            m = (l + r) // 2
            if pos <= m:
                self.update(v * 2, l, m, pos)
            else:
                self.update(v * 2 + 1, m + 1, r, pos)
            self.pull(v)

        def query(self, v, l, r, ql, qr):
            if ql == l and qr == r:
                return (self.pref[v], self.suff[v], self.best[v], self.length[v])

            m = (l + r) // 2

            if qr <= m:
                return self.query(v * 2, l, m, ql, qr)
            if ql > m:
                return self.query(v * 2 + 1, m + 1, r, ql, qr)

            A = self.query(v * 2, l, m, ql, m)
            B = self.query(v * 2 + 1, m + 1, r, m + 1, qr)

            ap, asf, ab, al = A
            bp, bsf, bb, bl = B

            pref = ap + bp if ap == al else ap
            suff = bsf + asf if bsf == bl else bsf
            best = max(ab, bb, asf + bp)

            return (pref, suff, best, al + bl)

    out = []

    n = int(input())
    h = list(map(int, input().split()))
    m = int(input())

    qs = [tuple(map(int, input().split())) for _ in range(m)]

    vals = sorted(set(h), reverse=True)
    k = len(vals)

    lo = [0] * m
    hi = [k - 1] * m

    pos = sorted([(h[i], i) for i in range(n)], reverse=True)

    while True:
        buckets = [[] for _ in range(k)]
        alive = False

        for i in range(m):
            if lo[i] < hi[i]:
                alive = True
                md = (lo[i] + hi[i]) // 2
                buckets[md].append(i)

        if not alive:
            break

        seg = SegTree(n)
        ptr = 0

        for md in range(k):
            thr = vals[md]

            while ptr < n and pos[ptr][0] >= thr:
                seg.update(1, 0, n - 1, pos[ptr][1])
                ptr += 1

            for qi in buckets[md]:
                l, r, w = qs[qi]
                best = seg.query(1, 0, n - 1, l - 1, r - 1)[2]

                if best >= w:
                    hi[qi] = md
                else:
                    lo[qi] = md + 1

    return "\n".join(str(vals[lo[i]]) for i in range(m))

# provided sample
assert run(
"""5
1 2 2 3 3
3
2 5 3
2 5 2
1 5 5
"""
) == "2\n3\n1"

# minimum size
assert run(
"""1
7
1
1 1 1
"""
) == "7"

# all equal
assert run(
"""4
5 5 5 5
2
1 4 2
2 3 1
"""
) == "5\n5"

# width equals interval length
assert run(
"""3
7 3 5
1
1 3 3
"""
) == "3"

# separated tall panels
assert run(
"""4
5 1 5 5
1
1 4 2
"""
) == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single panel | 7 | Smallest legal instance |
| All heights equal | 5, 5 | Uniform-height behavior |
| Width equals interval length | 3 | Only one possible placement |
| `5 1 5 5` with width 2 | 5 | Consecutive run logic rather than counting active panels |

## Edge Cases

Consider:

```
3
5 1 5
1
1 3 1
```

The answer is `5`. During threshold `5`, positions 1 and 3 are active. The longest active run inside `[1,3]` is `1`, which already satisfies width `1`. Binary search correctly returns `5`. A solution using the interval minimum would incorrectly return `1`.

Consider:

```
4
4 4 1 4
1
1 4 3
```

For threshold `4`, active runs have lengths `2` and `1`. The longest run is only `2`, smaller than the required width `3`, so the threshold fails. For threshold `1`, all positions become active and the longest run becomes `4`, so the answer is `1`. The algorithm correctly enforces the fixed-width requirement.

Consider:

```
3
7 3 5
1
1 3 3
```

At threshold `5`, the active positions are `{1,3}` and the longest run is `1`, so feasibility fails. At threshold `3`, every position is active and the longest run becomes `3`, exactly matching the required width. The answer is `3`, which is the minimum height of the entire interval.
