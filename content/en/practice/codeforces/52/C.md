---
title: "CF 52C - Circular RMQ"
description: "We have an array arranged in a circle. Every operation works on a segment between two indices, but the segment may wrap around the end of the array."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 52
codeforces_index: "C"
codeforces_contest_name: "Codeforces Testing Round 1"
rating: 2200
weight: 52
solve_time_s: 138
verified: true
draft: false
---
[CF 52C - Circular RMQ](https://codeforces.com/problemset/problem/52/C)

**Rating:** 2200  
**Tags:** data structures  
**Solve time:** 2m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array arranged in a circle. Every operation works on a segment between two indices, but the segment may wrap around the end of the array.

There are two operations.

The first operation adds a value to every element in a range.

The second operation asks for the minimum value inside a range.

If the left endpoint is less than or equal to the right endpoint, the segment is the normal contiguous interval. If the left endpoint is larger, the segment wraps around. For example, in an array of size 5, the range `[3,1]` means indices `3,4,0,1`.

The input gives the initial array, followed by up to 200000 operations. For every query operation, we must print the minimum value in the requested circular segment.

The constraints immediately rule out any linear-time processing per operation. With `n = 200000` and `m = 200000`, a brute-force solution could touch roughly `4 * 10^10` elements in the worst case, which is far beyond what fits in 2 seconds. Even `O(sqrt n)` per operation would be uncomfortable in Python at this scale. We need something close to logarithmic time for both updates and queries.

The operations are also mixed. Updates modify ranges, and queries ask for range minimums. This combination is exactly the setting where lazy propagation becomes necessary. A structure that supports only point updates or only static queries is not enough.

The circular nature creates several edge cases that are easy to mishandle.

Consider this input:

```
5
1 2 3 4 5
1
3 1
```

The query does not mean an empty range. It means indices `3,4,0,1`, so the answer is `1`. A careless implementation that assumes `l <= r` would either crash or return the wrong result.

Negative updates also matter:

```
3
5 5 5
2
0 2 -10
0 2
```

After the update, the array becomes `[-5,-5,-5]`, so the answer is `-5`. Any implementation using unsigned integers or incorrect initialization for minimum values would fail here.

Another subtle case appears when the range covers the entire array through wrapping:

```
4
10 20 30 40
2
2 1 -5
0 3
```

The update `[2,1]` affects every index because the wrapped segment is `2,3,0,1`. The final array becomes `[5,15,25,35]`, so the minimum is `5`. Splitting circular ranges incorrectly can leave gaps.

## Approaches

The most direct solution is to simulate every operation literally.

For an update, iterate through all indices in the segment and add the value. For a query, iterate through all indices in the segment and compute the minimum.

This works because the operations are simple and the circular interval can be handled by wrapping indices manually. The problem is performance. In the worst case, every operation may touch all `n` elements. With both `n` and `m` equal to `200000`, we get roughly:

```
200000 * 200000 = 4 * 10^10
```

operations. That is several hundred times too slow.

The key observation is that both operations are range-based.

We do not need to update every element immediately. If a whole segment receives `+v`, we can store that information lazily and only push it deeper when necessary. At the same time, if every node stores the minimum value of its segment, then range minimum queries become natural.

This leads directly to a segment tree with lazy propagation.

The circular interval is the only extra complication. A wrapped segment `[l,r]` with `l > r` can be split into two normal intervals:

```
[l, n-1]
[0, r]
```

Once we reduce every circular range into at most two ordinary ranges, the rest becomes standard segment tree processing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Optimal | O(m log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a segment tree over the array.

Each node stores the minimum value inside its segment. The root stores the minimum of the entire array.
2. Add a lazy array alongside the tree.

`lazy[node]` stores a pending increment that still needs to be propagated to children. This lets us delay updates instead of immediately touching every element.
3. For a range update, recursively process the segment tree.

If the current node lies completely inside the update range, add the increment directly to `tree[node]` and record it in `lazy[node]`.

We do not descend further because every element in that segment changes by the same amount.
4. If a node is only partially covered, push its pending lazy value downward before continuing.

This keeps child values correct before recursion continues deeper.
5. After updating children, recompute the current node as:

```
tree[node] = min(left child, right child)
```

This preserves the invariant that every node stores the minimum of its segment.
6. For a range minimum query, recursively traverse the relevant nodes.

If the current segment lies completely inside the query range, return its stored minimum immediately.
7. If the segment only partially overlaps, push lazy values first and combine results from both children using `min`.
8. Handle circular intervals by splitting them.

If `l <= r`, process normally.

If `l > r`, process:

```
[l, n-1]
[0, r]
```

For queries, take the minimum of the two parts.

For updates, apply the increment to both parts.

### Why it works

The segment tree always maintains one invariant:

```
tree[node] = minimum value inside that segment,
including all applied and pending updates.
```

Lazy propagation preserves correctness because every delayed increment is recorded before any future query or deeper recursion needs that information. When a node is fully covered by an update, increasing its stored minimum by `v` is valid because every element in that segment changes uniformly by `v`.

Splitting wrapped intervals into two ordinary intervals is also correct because the circular segment is exactly the union of those two disjoint ranges.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**18

class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self.build(1, 0, self.n - 1, arr)

    def build(self, node, l, r, arr):
        if l == r:
            self.tree[node] = arr[l]
            return

        mid = (l + r) // 2

        self.build(node * 2, l, mid, arr)
        self.build(node * 2 + 1, mid + 1, r, arr)

        self.tree[node] = min(
            self.tree[node * 2],
            self.tree[node * 2 + 1]
        )

    def push(self, node):
        if self.lazy[node] != 0:
            val = self.lazy[node]

            left = node * 2
            right = node * 2 + 1

            self.tree[left] += val
            self.tree[right] += val

            self.lazy[left] += val
            self.lazy[right] += val

            self.lazy[node] = 0

    def update(self, node, l, r, ql, qr, val):
        if ql <= l and r <= qr:
            self.tree[node] += val
            self.lazy[node] += val
            return

        self.push(node)

        mid = (l + r) // 2

        if ql <= mid:
            self.update(node * 2, l, mid, ql, qr, val)

        if qr > mid:
            self.update(node * 2 + 1, mid + 1, r, ql, qr, val)

        self.tree[node] = min(
            self.tree[node * 2],
            self.tree[node * 2 + 1]
        )

    def query(self, node, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.tree[node]

        self.push(node)

        mid = (l + r) // 2
        ans = INF

        if ql <= mid:
            ans = min(ans, self.query(node * 2, l, mid, ql, qr))

        if qr > mid:
            ans = min(ans, self.query(node * 2 + 1, mid + 1, r, ql, qr))

        return ans

def solve():
    n = int(input())
    arr = list(map(int, input().split()))

    seg = SegmentTree(arr)

    m = int(input())

    out = []

    for _ in range(m):
        parts = list(map(int, input().split()))

        if len(parts) == 2:
            l, r = parts

            if l <= r:
                ans = seg.query(1, 0, n - 1, l, r)
            else:
                ans = min(
                    seg.query(1, 0, n - 1, l, n - 1),
                    seg.query(1, 0, n - 1, 0, r)
                )

            out.append(str(ans))

        else:
            l, r, v = parts

            if l <= r:
                seg.update(1, 0, n - 1, l, r, v)
            else:
                seg.update(1, 0, n - 1, l, n - 1, v)
                seg.update(1, 0, n - 1, 0, r, v)

    sys.stdout.write("\n".join(out))

solve()
```

The segment tree stores minimum values for segments. The build phase recursively combines child minimums upward.

The `lazy` array is the critical optimization. When an update completely covers a segment, we modify the node directly and postpone propagation. This avoids descending into every leaf.

The `push` function transfers pending updates to children before deeper recursion. Forgetting this step is the most common bug in lazy propagation. Queries would otherwise read stale child values.

The query function initializes the answer with a very large value because minimum queries need a neutral element. Using `0` here would break cases where all values are positive.

Circular intervals are handled outside the segment tree logic. This keeps the tree implementation clean and focused only on ordinary intervals.

The recursion boundaries are inclusive on both ends. That choice must stay consistent everywhere, especially around:

```
mid = (l + r) // 2
```

with child segments:

```
[l, mid]
[mid + 1, r]
```

Mixing inclusive and half-open conventions is a common source of off-by-one errors.

## Worked Examples

### Example 1

Input:

```
4
1 2 3 4
4
3 0
3 0 -1
0 1
2 1
```

Initial array:

```
[1, 2, 3, 4]
```

| Operation | Affected Range | Array After Operation | Query Result |
| --- | --- | --- | --- |
| `3 0` | indices `3,0` | `[1,2,3,4]` | `1` |
| `3 0 -1` | indices `3,0` | `[0,2,3,3]` | - |
| `0 1` | indices `0,1` | `[0,2,3,3]` | `0` |
| `2 1` | indices `2,3,0,1` | `[0,2,3,3]` | `0` |

The first query demonstrates wrapped querying. The update also wraps and correctly modifies both ends of the array. The final query covers the entire array through wrapping.

### Example 2

Input:

```
5
10 20 30 40 50
5
1 3
4 1 -15
0 4
2 2 -100
0 4
```

Initial array:

```
[10,20,30,40,50]
```

| Operation | Affected Range | Array After Operation | Query Result |
| --- | --- | --- | --- |
| `1 3` | indices `1,2,3` | `[10,20,30,40,50]` | `20` |
| `4 1 -15` | indices `4,0,1` | `[-5,5,30,40,35]` | - |
| `0 4` | full array | `[-5,5,30,40,35]` | `-5` |
| `2 2 -100` | index `2` | `[-5,5,-70,40,35]` | - |
| `0 4` | full array | `[-5,5,-70,40,35]` | `-70` |

This trace shows both wrapped updates and point updates. The segment tree handles both using the same recursive machinery.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log n) | Each update and query touches at most logarithmically many segment tree nodes |
| Space | O(n) | Segment tree and lazy arrays require linear storage |

With `n` and `m` both up to `200000`, logarithmic operations are fast enough. A segment tree with lazy propagation comfortably fits within the time limit and memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    input_data = io.StringIO(inp)
    output_data = io.StringIO()

    input = input_data.readline

    INF = 10**18

    class SegmentTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.tree = [0] * (4 * self.n)
            self.lazy = [0] * (4 * self.n)
            self.build(1, 0, self.n - 1, arr)

        def build(self, node, l, r, arr):
            if l == r:
                self.tree[node] = arr[l]
                return

            mid = (l + r) // 2

            self.build(node * 2, l, mid, arr)
            self.build(node * 2 + 1, mid + 1, r, arr)

            self.tree[node] = min(
                self.tree[node * 2],
                self.tree[node * 2 + 1]
            )

        def push(self, node):
            if self.lazy[node]:
                val = self.lazy[node]

                self.tree[node * 2] += val
                self.tree[node * 2 + 1] += val

                self.lazy[node * 2] += val
                self.lazy[node * 2 + 1] += val

                self.lazy[node] = 0

        def update(self, node, l, r, ql, qr, val):
            if ql <= l and r <= qr:
                self.tree[node] += val
                self.lazy[node] += val
                return

            self.push(node)

            mid = (l + r) // 2

            if ql <= mid:
                self.update(node * 2, l, mid, ql, qr, val)

            if qr > mid:
                self.update(node * 2 + 1, mid + 1, r, ql, qr, val)

            self.tree[node] = min(
                self.tree[node * 2],
                self.tree[node * 2 + 1]
            )

        def query(self, node, l, r, ql, qr):
            if ql <= l and r <= qr:
                return self.tree[node]

            self.push(node)

            mid = (l + r) // 2
            ans = INF

            if ql <= mid:
                ans = min(ans, self.query(node * 2, l, mid, ql, qr))

            if qr > mid:
                ans = min(ans, self.query(node * 2 + 1, mid + 1, r, ql, qr))

            return ans

    n = int(input())
    arr = list(map(int, input().split()))

    seg = SegmentTree(arr)

    m = int(input())

    out = []

    for _ in range(m):
        parts = list(map(int, input().split()))

        if len(parts) == 2:
            l, r = parts

            if l <= r:
                ans = seg.query(1, 0, n - 1, l, r)
            else:
                ans = min(
                    seg.query(1, 0, n - 1, l, n - 1),
                    seg.query(1, 0, n - 1, 0, r)
                )

            out.append(str(ans))

        else:
            l, r, v = parts

            if l <= r:
                seg.update(1, 0, n - 1, l, r, v)
            else:
                seg.update(1, 0, n - 1, l, n - 1, v)
                seg.update(1, 0, n - 1, 0, r, v)

    return "\n".join(out)

# provided samples
assert run(
"""4
1 2 3 4
4
3 0
3 0 -1
0 1
2 1
"""
) == "1\n0\n0", "sample 1"

# minimum size
assert run(
"""1
5
3
0 0
0 0 -3
0 0
"""
) == "5\n2", "single element"

# all equal values
assert run(
"""5
7 7 7 7 7
4
0 4
1 3 5
0 4
4 1
"""
) == "7\n7\n7", "all equal values"

# wrap-around update covering all elements
assert run(
"""4
10 20 30 40
2
2 1 -5
0 3
"""
) == "5", "full circular coverage"

# negative updates and queries
assert run(
"""3
5 5 5
3
0 2 -10
0 2
1 1
"""
) == "-5\n-5", "negative values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single-element array | `5`, then `2` | Correct handling of smallest possible tree |
| All equal values | Always `7` | Updates do not accidentally affect unrelated segments |
| Wrapped full-array update | `5` | Circular splitting logic |
| Negative updates | `-5` | Proper minimum handling with negative numbers |

## Edge Cases

A wrapped query must not be treated as empty.

Input:

```
5
1 2 3 4 5
1
3 1
```

The algorithm splits `[3,1]` into:

```
[3,4]
[0,1]
```

The first query returns `4`, the second returns `1`, and the final answer is:

```
min(4,1) = 1
```

This correctly matches the circular interpretation.

Negative updates must propagate correctly through lazy values.

Input:

```
3
5 5 5
2
0 2 -10
0 2
```

The update fully covers the root segment, so the root minimum immediately becomes `-5`, and `lazy[root]` stores `-10`.

The later query reads the already-correct minimum from the root without needing to visit every leaf. The output is:

```
-5
```

A wrapped update may cover the entire array.

Input:

```
4
10 20 30 40
2
2 1 -5
0 3
```

The update splits into:

```
[2,3]
[0,1]
```

Together, these cover every index exactly once.

The array becomes:

```
[5,15,25,35]
```

The final minimum query returns `5`.

This case confirms that splitting wrapped ranges preserves correctness even when the wrapped interval spans the whole array.
