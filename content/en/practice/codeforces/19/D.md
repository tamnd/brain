---
title: "CF 19D - Points"
description: "We maintain a dynamic set of points on a 2D plane. Three operations are supported. add x y inserts a point. remove x y d"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 19
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 19"
rating: 2800
weight: 19
solve_time_s: 229
verified: true
draft: false
---

[CF 19D - Points](https://codeforces.com/problemset/problem/19/D)

**Rating:** 2800  
**Tags:** data structures  
**Solve time:** 3m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain a dynamic set of points on a 2D plane. Three operations are supported.

`add x y` inserts a point.

`remove x y` deletes an existing point.

`find x y` asks for the point with coordinates strictly larger than `(x, y)` in both dimensions, with a very specific tie-breaking rule.

Among all points satisfying:

- `px > x`
- `py > y`

we want the one with the smallest possible `px`. If several points share that same `px`, we choose the smallest `py`.

So the query is not asking for the globally smallest valid point. It first minimizes the x-coordinate, then minimizes the y-coordinate.

The number of operations reaches `2 * 10^5`, and coordinates go up to `10^9`. Large coordinates immediately suggest coordinate compression, because we cannot build arrays indexed directly by coordinate values.

The operation count is the more serious constraint. A naive scan over all points for every `find` query would take quadratic time in the worst case. With `2 * 10^5` operations, an `O(n)` query could easily produce around `4 * 10^10` comparisons, which is completely impossible within 2 seconds.

We need something close to logarithmic time per operation.

The tricky part is that the ordering rule is asymmetric. We do not simply need any point above and to the right. We specifically need the leftmost valid x-coordinate, and only after fixing that x-coordinate do we minimize y.

That structure is the key to the solution.

Consider this example:

```
add 2 100
add 3 1
find 1 50
```

The correct answer is `(2, 100)`.

A careless approach that globally minimizes y among valid points would return `(3, 1)`, which is wrong because x has higher priority.

Another subtle case is strict inequality.

```
add 5 5
find 5 4
```

The answer is `-1`.

Even though `y > 4`, the x-coordinate is not strictly larger than `5`.

Duplicate x-coordinates also matter.

```
add 7 10
add 7 3
find 5 4
```

The answer is `(7, 10)`.

The point `(7, 3)` fails because `3` is not greater than `4`. We cannot just store the minimum y for each x-coordinate. We need to know whether some y larger than the query exists.

Dynamic deletion creates another common failure mode.

```
add 4 8
remove 4 8
find 1 1
```

The answer is `-1`.

Any cached structure must correctly remove contributions when points disappear.

## Approaches

The brute-force solution is straightforward. Maintain all current points in a set. For each `find x y`, iterate through every point and keep the best candidate according to the problem ordering.

This works because the query definition is explicit. We simply test every point satisfying:

```
px > x and py > y
```

and keep the lexicographically smallest `(px, py)`.

Insertion and deletion are easy with a hash set, but queries become expensive. In the worst case we may have `2 * 10^5` active points and `2 * 10^5` queries, producing roughly `4 * 10^10` checks.

The bottleneck is searching for the smallest valid x-coordinate efficiently.

The important observation is that for every x-coordinate, we only care about the largest y currently present at that x.

Suppose we are checking whether some x-coordinate can answer a query `(qx, qy)`.

If the maximum y at that x is not larger than `qy`, then no point at that x works.

If the maximum y is larger than `qy`, then at least one valid point exists there.

That turns the problem into:

- find the smallest x-coordinate greater than `qx`
- whose maximum y is greater than `qy`

Once that x is found, we only need the smallest y at that x that exceeds `qy`.

This is exactly the kind of condition a segment tree handles well.

We compress all x-coordinates appearing in the input. For every compressed x-index, we maintain:

- a sorted set of y-values currently present at that x
- the maximum y-value at that x

The segment tree stores these maxima.

Now a query becomes:

- search the segment tree for the leftmost position after `qx`
- whose stored maximum y exceeds `qy`

After locating that x-coordinate, binary search inside its y-set for the smallest y greater than `qy`.

Each operation becomes logarithmic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) worst case | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all operations first and collect every x-coordinate that appears.

We need coordinate compression because x-values can be as large as `10^9`, but there are at most `2 * 10^5` distinct coordinates.
2. Sort and deduplicate the x-coordinates.

Each original x-coordinate receives a compressed index between `0` and `m - 1`.
3. For every compressed x-index, maintain a sorted container of y-values currently active at that x.

We need two operations on this structure:

- insert/delete y
- find the smallest y strictly larger than a query value
4. Build a segment tree where each node stores the maximum y currently present in its interval.

If an x-coordinate has no active points, its value becomes `-1`.
5. For an `add x y` operation:

- insert `y` into the sorted structure for x
- update the segment tree leaf with the new maximum y at that x

The segment tree always reflects the largest y available for each x-coordinate.
6. For a `remove x y` operation:

- erase `y` from the structure for x
- recompute the maximum y at that x
- update the segment tree

If no points remain at that x-coordinate, the stored maximum becomes `-1`.
7. For a `find x y` operation:

- locate the first compressed x-index strictly larger than `x`
- query the segment tree for the leftmost index whose stored maximum y exceeds `y`

The search works because if a segment maximum is not greater than `y`, then no x-coordinate inside that segment can answer the query.
8. If no such x-coordinate exists, output `-1`.
9. Otherwise, inside the y-container for that x-coordinate, binary search for the smallest y strictly larger than the query value.

This gives the required tie-breaking behavior:

- smallest valid x first
- smallest valid y within that x

### Why it works

The segment tree invariant is:

```
tree[node] = maximum y among all active points in that interval of x-coordinates
```

During a query, if a segment maximum is at most `qy`, then every point in that segment fails the condition `py > qy`. Skipping that entire segment is always safe.

The search always descends into the left child first. Because of that, the first valid leaf found corresponds to the smallest x-coordinate satisfying the query.

Once the x-coordinate is fixed, selecting the smallest y greater than `qy` from that x-coordinate exactly matches the required ordering rule.

Since insertions and deletions always refresh the corresponding maximum y, the invariant remains true after every update.

## Python Solution

```python
import sys
from bisect import bisect_right, insort
from collections import defaultdict

input = sys.stdin.readline

class SegmentTree:
    def __init__(self, n):
        self.n = n
        self.tree = [-1] * (4 * n)

    def update(self, node, l, r, idx, val):
        if l == r:
            self.tree[node] = val
            return

        mid = (l + r) // 2

        if idx <= mid:
            self.update(node * 2, l, mid, idx, val)
        else:
            self.update(node * 2 + 1, mid + 1, r, idx, val)

        self.tree[node] = max(
            self.tree[node * 2],
            self.tree[node * 2 + 1]
        )

    def query(self, node, l, r, ql, y):
        if r < ql or self.tree[node] <= y:
            return -1

        if l == r:
            return l

        mid = (l + r) // 2

        left = self.query(node * 2, l, mid, ql, y)
        if left != -1:
            return left

        return self.query(node * 2 + 1, mid + 1, r, ql, y)

def solve():
    n = int(input())

    ops = []
    xs = []

    for _ in range(n):
        t, x, y = input().split()
        x = int(x)
        y = int(y)

        ops.append((t, x, y))
        xs.append(x)

    comp = sorted(set(xs))
    xid = {x: i for i, x in enumerate(comp)}

    m = len(comp)

    ys = defaultdict(list)

    seg = SegmentTree(m)

    out = []

    for t, x, y in ops:
        idx = xid[x]

        if t == "add":
            insort(ys[idx], y)
            seg.update(1, 0, m - 1, idx, ys[idx][-1])

        elif t == "remove":
            pos = bisect_right(ys[idx], y) - 1
            ys[idx].pop(pos)

            new_max = ys[idx][-1] if ys[idx] else -1
            seg.update(1, 0, m - 1, idx, new_max)

        else:
            start = bisect_right(comp, x)

            if start >= m:
                out.append("-1")
                continue

            res = seg.query(1, 0, m - 1, start, y)

            if res == -1:
                out.append("-1")
                continue

            pos = bisect_right(ys[res], y)
            ans_y = ys[res][pos]

            out.append(f"{comp[res]} {ans_y}")

    sys.stdout.write("\n".join(out))

solve()
```

The solution begins with coordinate compression because x-values are sparse and extremely large. Every x-coordinate appearing anywhere in the input receives a compact index.

For every compressed x-index, `ys[idx]` stores all active y-values in sorted order. The sorted order matters because queries need the smallest y strictly greater than a threshold. Python's `bisect_right` gives that position directly.

The segment tree stores only one number per x-coordinate, the maximum active y. That single value is enough to determine whether some point at that x can satisfy a query.

The recursive query function is the heart of the solution. It skips segments whose maximum y is too small, and always explores the left child first. That guarantees the first valid leaf corresponds to the smallest valid x-coordinate.

Deletion is easy to get wrong. After removing a y-value, we must recompute the maximum y at that x-coordinate. If the container becomes empty, we store `-1` so future queries correctly ignore that position.

The query uses strict inequalities everywhere. That is why `bisect_right` is used both for x and y searches. Using `bisect_left` would incorrectly allow equal coordinates.

## Worked Examples

### Example 1

Input:

```
7
add 1 1
add 3 4
find 0 0
remove 1 1
find 0 0
add 1 1
find 0 0
```

### Trace

| Step | Operation | Active Points | Segment Maxima | Answer |
| --- | --- | --- | --- | --- |
| 1 | add 1 1 | {(1,1)} | x=1→1, x=3→-1 |  |
| 2 | add 3 4 | {(1,1),(3,4)} | x=1→1, x=3→4 |  |
| 3 | find 0 0 | unchanged | unchanged | 1 1 |
| 4 | remove 1 1 | {(3,4)} | x=1→-1, x=3→4 |  |
| 5 | find 0 0 | unchanged | unchanged | 3 4 |
| 6 | add 1 1 | {(1,1),(3,4)} | x=1→1, x=3→4 |  |
| 7 | find 0 0 | unchanged | unchanged | 1 1 |

The trace shows why the query searches for the smallest valid x-coordinate first. Even though `(3,4)` always satisfies the condition, `(1,1)` is preferred whenever it exists because its x-coordinate is smaller.

### Example 2

Input:

```
8
add 5 2
add 5 10
add 7 3
find 4 5
find 5 1
remove 5 10
find 4 5
find 6 2
```

### Trace

| Step | Operation | Active Points | Max at x=5 | Max at x=7 | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | add 5 2 | {(5,2)} | 2 | -1 |  |
| 2 | add 5 10 | {(5,2),(5,10)} | 10 | -1 |  |
| 3 | add 7 3 | {(5,2),(5,10),(7,3)} | 10 | 3 |  |
| 4 | find 4 5 | unchanged | 10 | 3 | 5 10 |
| 5 | find 5 1 | unchanged | 10 | 3 | 7 3 |
| 6 | remove 5 10 | {(5,2),(7,3)} | 2 | 3 |  |
| 7 | find 4 5 | unchanged | 2 | 3 | -1 |
| 8 | find 6 2 | unchanged | 2 | 3 | 7 3 |

This example demonstrates why storing the maximum y for each x-coordinate is sufficient. Before deletion, x=5 remains viable because its maximum y is 10. After deleting `(5,10)`, the maximum becomes 2, which no longer satisfies `y > 5`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each update and query performs logarithmic segment tree and binary search operations |
| Space | O(n) | Coordinate compression, segment tree, and stored points all scale linearly |

With at most `2 * 10^5` operations, `O(n log n)` easily fits within the limits. The segment tree performs around `log₂(2 * 10^5) ≈ 18` recursive levels per operation, which is very manageable in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from bisect import bisect_right, insort
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    input = sys.stdin.readline

    class SegmentTree:
        def __init__(self, n):
            self.n = n
            self.tree = [-1] * (4 * n)

        def update(self, node, l, r, idx, val):
            if l == r:
                self.tree[node] = val
                return

            mid = (l + r) // 2

            if idx <= mid:
                self.update(node * 2, l, mid, idx, val)
            else:
                self.update(node * 2 + 1, mid + 1, r, idx, val)

            self.tree[node] = max(
                self.tree[node * 2],
                self.tree[node * 2 + 1]
            )

        def query(self, node, l, r, ql, y):
            if r < ql or self.tree[node] <= y:
                return -1

            if l == r:
                return l

            mid = (l + r) // 2

            left = self.query(node * 2, l, mid, ql, y)
            if left != -1:
                return left

            return self.query(node * 2 + 1, mid + 1, r, ql, y)

    n = int(input())

    ops = []
    xs = []

    for _ in range(n):
        t, x, y = input().split()
        x = int(x)
        y = int(y)

        ops.append((t, x, y))
        xs.append(x)

    comp = sorted(set(xs))
    xid = {x: i for i, x in enumerate(comp)}

    ys = defaultdict(list)

    seg = SegmentTree(len(comp))

    ans = []

    for t, x, y in ops:
        idx = xid[x]

        if t == "add":
            insort(ys[idx], y)
            seg.update(1, 0, len(comp) - 1, idx, ys[idx][-1])

        elif t == "remove":
            pos = bisect_right(ys[idx], y) - 1
            ys[idx].pop(pos)

            val = ys[idx][-1] if ys[idx] else -1
            seg.update(1, 0, len(comp) - 1, idx, val)

        else:
            start = bisect_right(comp, x)

            if start >= len(comp):
                ans.append("-1")
                continue

            res = seg.query(1, 0, len(comp) - 1, start, y)

            if res == -1:
                ans.append("-1")
                continue

            pos = bisect_right(ys[res], y)
            ans.append(f"{comp[res]} {ys[res][pos]}")

    return "\n".join(ans)

# provided sample
assert run(
"""7
add 1 1
add 3 4
find 0 0
remove 1 1
find 0 0
add 1 1
find 0 0
"""
) == "1 1\n3 4\n1 1"

# minimum case
assert run(
"""1
find 0 0
"""
) == "-1"

# strict inequality check
assert run(
"""3
add 5 5
find 5 4
find 4 5
"""
) == "-1\n-1"

# multiple points with same x
assert run(
"""5
add 7 3
add 7 10
find 5 4
find 5 9
find 5 10
"""
) == "7 10\n7 10\n-1"

# deletion updates maximum correctly
assert run(
"""6
add 2 1
add 2 100
remove 2 100
find 1 50
find 1 0
find 0 0
"""
) == "-1\n2 1\n2 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single `find` on empty set | `-1` | Empty structure handling |
| Queries with equal coordinates | `-1` | Strict inequality correctness |
| Multiple y-values at same x | Proper y selection | Correct tie-breaking inside one x |
| Deleting the largest y | Updated maxima | Segment tree maintenance correctness |

## Edge Cases

Consider strict inequality again:

```
3
add 5 5
find 5 4
find 4 5
```

For `find 5 4`, the search begins strictly after x=5. No larger x exists, so the answer is `-1`.

For `find 4 5`, x=5 is valid, but y=5 is not strictly larger than 5. The segment tree stores maximum y=5, which is not greater than the query threshold, so the query correctly rejects the segment.

Now consider duplicate x-values:

```
4
add 7 3
add 7 10
find 5 4
find 5 9
```

The segment tree stores maximum y=10 for x=7.

For `find 5 4`, the query discovers that x=7 is viable because 10 > 4. Inside the sorted y-list `[3, 10]`, binary search returns 10 as the smallest y greater than 4.

For `find 5 9`, the same logic returns 10 again.

Deletion correctness is another subtle point:

```
5
add 2 1
add 2 100
remove 2 100
find 1 50
find 1 0
```

Initially the segment tree stores maximum y=100 at x=2.

After deleting `(2,100)`, the maximum becomes 1. The update propagates upward through the tree.

For `find 1 50`, the segment tree now rejects x=2 because its maximum y is no longer greater than 50, so the answer becomes `-1`.

For `find 1 0`, the point `(2,1)` still satisfies the query and is returned correctly.
