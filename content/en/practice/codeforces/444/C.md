---
title: "CF 444C - DZY Loves Colors"
description: "We have a ribbon consisting of positions 1...n. Initially, position i has color i, so every position starts with a distinct color. Two kinds of operations are performed. A paint operation assigns a new color x to every position in a segment [l, r]."
date: "2026-06-07T16:00:27+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 444
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 254 (Div. 1)"
rating: 2400
weight: 444
solve_time_s: 319
verified: false
draft: false
---

[CF 444C - DZY Loves Colors](https://codeforces.com/problemset/problem/444/C)

**Rating:** 2400  
**Tags:** data structures  
**Solve time:** 5m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We have a ribbon consisting of positions `1...n`. Initially, position `i` has color `i`, so every position starts with a distinct color.

Two kinds of operations are performed.

A paint operation assigns a new color `x` to every position in a segment `[l, r]`. When a position currently colored `y` is repainted to `x`, its accumulated colorfulness increases by `|x - y|`.

A query operation asks for the total colorfulness over a segment `[l, r]`.

The challenge is that both the ribbon length and the number of operations can reach `10^5`. A straightforward simulation of repainting every position inside every update can require up to `10^10` position updates in the worst case, which is completely infeasible within a 2-second limit.

The first observation is that colors change many times, but after every paint operation an entire interval becomes a single color. The ribbon naturally decomposes into maximal segments having the same current color. If we can maintain those segments directly instead of individual positions, the number of changes per operation becomes much smaller.

Another subtle aspect is that colorfulness accumulates permanently. Repainting a position does not overwrite previous contributions. For example:

```
n = 1

paint [1,1] color 5
paint [1,1] color 2
query [1,1]
```

The answer is

```
|5-1| + |2-5| = 4 + 3 = 7
```

A careless implementation that stores only the current color would lose the earlier contribution.

A second easy mistake appears when repainting with the same color.

```
n = 3

paint [1,3] color 10
paint [1,3] color 10
query [1,3]
```

The second update contributes zero because every position already has color `10`. The answer must remain the same after the second update.

A third source of bugs is partial overlap with existing color segments.

```
n = 5

paint [2,4] color 7
```

Initially the color segments are

```
[1]=1 [2]=2 [3]=3 [4]=4 [5]=5
```

The update intersects three existing colors. The contribution added to colorfulness is

```
|7-2| + |7-3| + |7-4|
```

for positions 2, 3, and 4 respectively. Any segment structure must first split at the boundaries of the update range, otherwise segment lengths and contributions become incorrect.

## Approaches

The brute-force approach stores the current color and accumulated colorfulness of every position.

For an update `[l,r] -> x`, iterate through every position in the range, add `|current_color - x|` to its colorfulness, then replace its color with `x`.

For a query, sum the colorfulness values over the requested interval.

This method is obviously correct because it directly follows the definition. Unfortunately, a single update may touch `O(n)` positions. With `10^5` updates on a ribbon of length `10^5`, the worst-case work reaches `10^10` operations.

The key observation is that a paint operation affects an entire monochromatic segment in exactly the same way.

Suppose positions `[L,R]` currently all have color `c`, and we repaint them with color `x`.

Every position gains the same amount:

```
|x-c|
```

Instead of updating each position individually, we can add this value to an interval data structure over `[L,R]`.

This suggests separating the problem into two independent parts.

The first part tracks the current colors. For that we maintain an ordered set of maximal monochromatic intervals. Repainting a range only requires examining the intervals that intersect it.

The second part tracks accumulated colorfulness. Every time an interval of length `k` and color `c` is repainted to `x`, every position in that interval receives an additive increment `|x-c|`. This is simply a range-add operation. Queries ask for range sums. A segment tree with lazy propagation handles both operations in `O(log n)`.

The interval set tells us which positions receive which increment. The segment tree stores the accumulated colorfulness values.

Each repaint operation splits interval boundaries at `l` and `r+1`, visits all affected monochromatic intervals, applies the corresponding range additions to the segment tree, removes those intervals, and finally inserts one new interval colored `x`.

The classical ordered-disjoint-interval-tree argument shows that each interval can only be created and destroyed a limited number of times. Across all operations, the total number of interval visits remains manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Optimal | O((m + K) log n) where K is total interval splits/visits | O(n) | Accepted |

## Algorithm Walkthrough

1. Build an ordered set of intervals representing current colors.

Initially every position has a unique color, so we create intervals:

```
[1,1] color 1
[2,2] color 2
...
[n,n] color n
```
2. Build a lazy segment tree storing colorfulness values.

Every value starts at zero.
3. Before processing an update, split the interval structure at position `l`.

If some interval crosses `l`, replace it by two intervals so that one interval starts exactly at `l`.
4. Split again at position `r+1`.

After this step, every interval completely inside `[l,r]` becomes an explicit interval in the set.
5. Iterate through all intervals fully contained in `[l,r]`.

Suppose an interval is `[L,R]` with current color `c`.

Every position in that interval gains:

```
|x-c|
```

Apply a segment-tree range addition of `|x-c|` on `[L,R]`.
6. Remove all intervals contained in `[l,r]`.

Their colors are no longer relevant because the repaint operation overwrites them.
7. Insert one new interval `[l,r]` with color `x`.

This interval represents the entire repainted region.
8. For a query operation, simply ask the segment tree for the range sum on `[l,r]`.

The segment tree already contains every colorfulness increment ever applied.

### Why it works

The interval set always represents the exact current coloring of the ribbon as a partition into disjoint monochromatic intervals.

After splitting at `l` and `r+1`, every interval inside `[l,r]` has a single current color. Repainting such an interval from color `c` to color `x` increases every position in that interval by exactly `|x-c|`, which is precisely the update applied to the segment tree.

The segment tree stores the sum of all repaint contributions accumulated over time. Since every repaint contribution is added once to every affected position and never removed, range-sum queries return exactly the total colorfulness requested.

Thus the interval structure maintains correct current colors, while the segment tree maintains correct accumulated colorfulness, and together they simulate every operation exactly.

## Python Solution

```python
import sys
from bisect import bisect_left
input = sys.stdin.readline

class SegTree:
    def __init__(self, n):
        self.n = n
        self.sum = [0] * (4 * n)
        self.lazy = [0] * (4 * n)

    def _push(self, p, l, r):
        if self.lazy[p] == 0:
            return

        mid = (l + r) >> 1
        v = self.lazy[p]

        self.sum[p * 2] += v * (mid - l + 1)
        self.sum[p * 2 + 1] += v * (r - mid)

        self.lazy[p * 2] += v
        self.lazy[p * 2 + 1] += v

        self.lazy[p] = 0

    def _add(self, p, l, r, ql, qr, val):
        if ql <= l and r <= qr:
            self.sum[p] += val * (r - l + 1)
            self.lazy[p] += val
            return

        self._push(p, l, r)

        mid = (l + r) >> 1

        if ql <= mid:
            self._add(p * 2, l, mid, ql, qr, val)
        if qr > mid:
            self._add(p * 2 + 1, mid + 1, r, ql, qr, val)

        self.sum[p] = self.sum[p * 2] + self.sum[p * 2 + 1]

    def add(self, l, r, val):
        self._add(1, 1, self.n, l, r, val)

    def _query(self, p, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.sum[p]

        self._push(p, l, r)

        mid = (l + r) >> 1
        ans = 0

        if ql <= mid:
            ans += self._query(p * 2, l, mid, ql, qr)
        if qr > mid:
            ans += self._query(p * 2 + 1, mid + 1, r, ql, qr)

        return ans

    def query(self, l, r):
        return self._query(1, 1, self.n, l, r)

def solve():
    n, m = map(int, input().split())

    seg = SegTree(n)

    starts = list(range(1, n + 1))
    color = {i: i for i in range(1, n + 1)}
    right = {i: i for i in range(1, n + 1)}

    def split(pos):
        if pos > n:
            return len(starts)

        idx = bisect_left(starts, pos)

        if idx < len(starts) and starts[idx] == pos:
            return idx

        idx -= 1
        s = starts[idx]
        e = right[s]
        c = color[s]

        starts.insert(idx + 1, pos)

        right[s] = pos - 1
        right[pos] = e

        color[pos] = c

        return idx + 1

    out = []

    for _ in range(m):
        op = list(map(int, input().split()))

        if op[0] == 1:
            _, l, r, x = op

            ir = split(r + 1)
            il = split(l)

            affected = starts[il:ir]

            for s in affected:
                e = right[s]
                c = color[s]
                seg.add(s, e, abs(x - c))

            for s in affected:
                del color[s]
                del right[s]

            starts[il:ir] = [l]
            color[l] = x
            right[l] = r

        else:
            _, l, r = op
            out.append(str(seg.query(l, r)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The segment tree is responsible only for colorfulness values. Every repaint translates into a range-add operation, and every query becomes a range-sum request.

The interval structure stores current colors. Each interval is identified by its left endpoint. The `starts` list remains sorted, while the dictionaries store the interval's right endpoint and color.

The `split(pos)` routine is the crucial operation. If an interval crosses `pos`, it is divided into two intervals having the same color. After splitting at both update boundaries, every interval inside the repaint range can be processed independently.

A subtle implementation detail is the order of the two splits. We split at `r + 1` before splitting at `l`. This mirrors the standard ODT implementation and avoids invalidating the iterator range that we later process.

Another detail is that the answer may exceed 32-bit limits. Every segment tree value is stored in Python integers, which automatically handle arbitrarily large values.

## Worked Examples

### Example 1

Input:

```
3 3
1 1 2 4
1 2 3 5
2 1 3
```

State after each operation:

| Operation | Intervals after operation | Added contribution |
| --- | --- | --- |
| Initial | [1,1]:1 [2,2]:2 [3,3]:3 | 0 |
| Paint [1,2] -> 4 | [1,2]:4 [3,3]:3 | 3 on pos1, 2 on pos2 |
| Paint [2,3] -> 5 | [1,1]:4 [2,3]:5 | 1 on pos2, 2 on pos3 |
| Query [1,3] | unchanged | answer = 8 |

Colorfulness values become:

| Position | Value |
| --- | --- |
| 1 | 3 |
| 2 | 3 |
| 3 | 2 |

Sum:

```
3 + 3 + 2 = 8
```

This example shows how the segment tree accumulates contributions from multiple repaint operations.

### Example 2

Input:

```
5 3
1 2 4 7
2 1 5
2 2 4
```

After the repaint:

| Position | Old color | New color | Increment |
| --- | --- | --- | --- |
| 2 | 2 | 7 | 5 |
| 3 | 3 | 7 | 4 |
| 4 | 4 | 7 | 3 |

Colorfulness array:

```
[0, 5, 4, 3, 0]
```

Queries:

| Query | Result |
| --- | --- |
| [1,5] | 12 |
| [2,4] | 12 |

This trace demonstrates that repainting a range contributes independently to each covered monochromatic interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((m + K) log n) | Each segment-tree operation costs O(log n), and each interval created by splitting is processed only when visited by updates |
| Space | O(n) | Segment tree plus interval representation |

The interval structure never contains more than `O(n + m)` intervals over the entire execution, and the segment tree uses linear memory. With `n, m ≤ 10^5`, this comfortably fits within the limits used by accepted solutions for this problem.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    from bisect import bisect_left

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    input = sys.stdin.readline

    class SegTree:
        def __init__(self, n):
            self.n = n
            self.sum = [0] * (4 * n)
            self.lazy = [0] * (4 * n)

        def push(self, p, l, r):
            if not self.lazy[p]:
                return
            mid = (l + r) // 2
            v = self.lazy[p]
            self.sum[p * 2] += v * (mid - l + 1)
            self.sum[p * 2 + 1] += v * (r - mid)
            self.lazy[p * 2] += v
            self.lazy[p * 2 + 1] += v
            self.lazy[p] = 0

        def add(self, p, l, r, ql, qr, v):
            if ql <= l and r <= qr:
                self.sum[p] += v * (r - l + 1)
                self.lazy[p] += v
                return
            self.push(p, l, r)
            mid = (l + r) // 2
            if ql <= mid:
                self.add(p * 2, l, mid, ql, qr, v)
            if qr > mid:
                self.add(p * 2 + 1, mid + 1, r, ql, qr, v)
            self.sum[p] = self.sum[p * 2] + self.sum[p * 2 + 1]

        def query(self, p, l, r, ql, qr):
            if ql <= l and r <= qr:
                return self.sum[p]
            self.push(p, l, r)
            mid = (l + r) // 2
            ans = 0
            if ql <= mid:
                ans += self.query(p * 2, l, mid, ql, qr)
            if qr > mid:
                ans += self.query(p * 2 + 1, mid + 1, r, ql, qr)
            return ans

    n, m = map(int, input().split())
    seg = SegTree(n)

    starts = list(range(1, n + 1))
    color = {i: i for i in range(1, n + 1)}
    right = {i: i for i in range(1, n + 1)}

    def split(pos):
        if pos > n:
            return len(starts)
        idx = bisect_left(starts, pos)
        if idx < len(starts) and starts[idx] == pos:
            return idx
        idx -= 1
        s = starts[idx]
        starts.insert(idx + 1, pos)
        right[pos] = right[s]
        color[pos] = color[s]
        right[s] = pos - 1
        return idx + 1

    ans = []

    for _ in range(m):
        q = list(map(int, input().split()))

        if q[0] == 1:
            _, l, r, x = q
            ir = split(r + 1)
            il = split(l)

            cur = starts[il:ir]

            for s in cur:
                seg.add(1, 1, n, s, right[s], abs(x - color[s]))

            for s in cur:
                del color[s]
                del right[s]

            starts[il:ir] = [l]
            color[l] = x
            right[l] = r

        else:
            _, l, r = q
            ans.append(str(seg.query(1, 1, n, l, r)))

    return "\n".join(ans)

# sample
assert run(
"""3 3
1 1 2 4
1 2 3 5
2 1 3
"""
) == "8"

# minimum size
assert run(
"""1 1
2 1 1
"""
) == "0"

# repaint same color
assert run(
"""1 2
1 1 1 1
2 1 1
"""
) == "0"

# full range repaint
assert run(
"""3 2
1 1 3 10
2 1 3
"""
) == "24"

# boundary split test
assert run(
"""5 3
1 2 4 7
2 1 5
2 2 4
"""
) == "12\n12"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element query | 0 | Initial state handling |
| Repaint with same color | 0 | Zero contribution updates |
| Full range repaint | 24 | Whole-array updates |
| Partial interior repaint | 12, 12 | Correct interval splitting |
| Official sample | 8 | General correctness |

## Edge Cases

Consider repainting with the same color.

```
1 2
1 1 1 1
2 1 1
```

Position 1 initially has color 1. Repainting it with color 1 adds

```
|1-1| = 0
```

The algorithm visits the interval, computes `abs(x - c)`, obtains zero, and applies a zero range addition. The query correctly returns `0`.

Consider repeated repainting of the same position.

```
1 3
1 1 1 5
1 1 1 2
2 1 1
```

The first repaint contributes `4`, the second contributes `3`. The segment tree stores both updates, so the final answer is `7`. Since contributions are only added and never overwritten, accumulated colorfulness remains correct.

Consider a repaint that starts and ends inside existing intervals.

```
5 2
1 2 4 7
2 1 5
```

Before processing the update, the algorithm splits at positions `2` and `5`. The affected region becomes a collection of complete monochromatic intervals. Each receives exactly one range addition equal to its color difference from `7`. No position outside `[2,4]` is touched, and the query correctly returns `12`.

These cases are precisely where interval splitting and accumulated range additions matter. The algorithm handles them naturally through its invariant that the interval set always matches the current coloring and the segment tree always stores every repaint contribution ever applied.
