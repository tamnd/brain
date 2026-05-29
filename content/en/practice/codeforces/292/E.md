---
title: "CF 292E - Copying Data"
description: "We have two arrays, a and b, both of length n. Queries arrive online. One type of query copies a contiguous segment from a into a segment of b. If the query is (x, y, k), then: The second type asks for the current value at a single position in b."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 292
codeforces_index: "E"
codeforces_contest_name: "Croc Champ 2013 - Round 1"
rating: 1900
weight: 292
solve_time_s: 116
verified: true
draft: false
---

[CF 292E - Copying Data](https://codeforces.com/problemset/problem/292/E)

**Rating:** 1900  
**Tags:** data structures  
**Solve time:** 1m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two arrays, `a` and `b`, both of length `n`. Queries arrive online.

One type of query copies a contiguous segment from `a` into a segment of `b`. If the query is `(x, y, k)`, then:

```
b[y + i] = a[x + i]    for 0 <= i < k
```

The second type asks for the current value at a single position in `b`.

The tricky part is that copy operations overlap and overwrite previous copies. A position in `b` may still contain its original value, or it may currently mirror some position in `a` because of the most recent copy covering it.

The constraints completely rule out simulating every copy directly. Both `n` and `m` are up to `10^5`. A single copy operation can affect `O(n)` elements, so a naive solution may perform around `10^10` assignments in the worst case, which is far beyond what fits in 2 seconds.

The structure of the operations is what matters here. We never modify array `a`. Every update says that an interval of `b` now corresponds to an interval of `a` with a fixed offset. Queries only ask for one position at a time. That means we do not actually need to materialize the copied values immediately. We only need enough information to answer, for any position `p` in `b`, whether it currently points into `a`, and if so, which index.

There are several edge cases that easily break careless implementations.

Suppose we copy a large segment and later overwrite only part of it.

Input:

```
a = [10, 20, 30, 40]
b = [1, 2, 3, 4]

copy a[1..4] -> b[1..4]
copy a[2..2] -> b[2..2]
```

The final `b` should behave like:

```
[10, 20, 30, 40]
```

A buggy interval structure that does not properly split segments may accidentally erase information for positions `1`, `3`, and `4`.

Another subtle case is querying a position that was never touched by any copy operation.

Input:

```
a = [5]
b = [7]

query b[1]
```

The answer is `7`, not `5`. If we initialize every position as mapped into `a`, we silently produce wrong answers.

Overlapping updates also matter.

Input:

```
a = [1, 2, 3, 4, 5]
b = [9, 9, 9, 9, 9]

copy a[1..3] -> b[2..4]
copy a[3..5] -> b[1..3]
```

The final logical contents of `b` become:

```
[3, 4, 5, 3, 9]
```

The second update overwrites only part of the first one. If we only store whole operations without respecting recency on subranges, queries return stale data.

## Approaches

The most direct solution is to execute each copy literally. For every update `(x, y, k)`, we loop through all `k` positions and assign:

```
b[y + i] = a[x + i]
```

Then query operations become trivial because `b` always contains the real values.

This works logically because each operation exactly matches the statement. The problem is the cost. A single update may touch `10^5` elements, and there may be `10^5` updates, leading to roughly `10^10` writes. That is far too slow.

The key observation is that copied values always come from `a`, which never changes. After an update, a position in `b` does not need a stored value, it only needs a description of where its value comes from.

If we copy:

```
a[x..x+k-1] -> b[y..y+k-1]
```

then every position `p` in that interval satisfies:

```
b[p] = a[x + (p - y)]
```

The relationship between `p` and its source index in `a` is just a fixed offset.

This turns the problem into interval assignment. For a segment of `b`, we store metadata describing which segment of `a` it currently mirrors. Point queries then recover the corresponding index in `a`.

A segment tree with lazy propagation fits perfectly here. Each update assigns metadata to an interval. Each query walks down to one position and retrieves the latest assignment affecting it.

Instead of storing actual copied values, each node stores the starting index in `a` corresponding to the left boundary of that node's interval. From that information, any position inside the segment can compute its mapped source index.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Optimal | O(m log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a segment tree over the positions of array `b`.

Each node represents an interval of `b`. Initially, all nodes store `-1`, meaning that this interval still uses original values from `b`.
2. Process a copy query `(x, y, k)` as a range assignment on interval `[y, y+k-1]`.

We store enough information to reconstruct the source position in `a`.

If a node interval starts at `l`, then position `l` in `b` corresponds to position:

```
x + (l - y)
```

in `a`.

We store this starting source index in the node.
3. Use lazy propagation during updates.

If an update fully covers a node interval, we overwrite that node directly without descending further.

This matters because updates overlap heavily, and repeatedly touching every leaf would destroy performance.
4. For a query at position `p`, walk from the root toward the leaf containing `p`.

Whenever we encounter pending lazy information, we push it to children so that deeper intervals inherit the correct mapping.
5. Once we reach the leaf for `p`, there are two possibilities.

If the leaf still stores `-1`, the position was never overwritten, so answer `b[p]`.

Otherwise, the stored value tells us which index of `a` corresponds to this position, so answer that element from `a`.

### Why it works

The invariant is:

```
For every segment tree node, if it stores a mapping value,
then every position in that interval currently maps to a
contiguous segment of a with the correct relative offsets.
```

Whenever a copy operation fully covers an interval, we overwrite the node with the newest mapping, exactly matching the semantics of the operation. Lazy propagation guarantees that later partial updates correctly split intervals and preserve unaffected regions.

A query follows the unique path from root to leaf. Any pending assignments affecting that position are pushed downward in order, so the leaf finally contains the most recent copy operation covering that index, or `-1` if no copy ever affected it.

Because every update precisely mirrors the overwrite rules from the problem, the retrieved value is always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegmentTree:
    def __init__(self, n):
        self.n = n
        self.lazy = [-1] * (4 * n)

    def push(self, node, l, r):
        if self.lazy[node] == -1 or l == r:
            return

        mid = (l + r) // 2
        left = node * 2
        right = node * 2 + 1

        start = self.lazy[node]

        self.lazy[left] = start

        right_start = start + (mid + 1 - l)
        self.lazy[right] = right_start

        self.lazy[node] = -1

    def update(self, node, l, r, ql, qr, start):
        if ql <= l and r <= qr:
            self.lazy[node] = start + (l - ql)
            return

        self.push(node, l, r)

        mid = (l + r) // 2

        if ql <= mid:
            self.update(node * 2, l, mid, ql, qr, start)

        if qr > mid:
            self.update(node * 2 + 1, mid + 1, r, ql, qr, start)

    def query(self, node, l, r, pos):
        if l == r:
            return self.lazy[node]

        self.push(node, l, r)

        mid = (l + r) // 2

        if pos <= mid:
            return self.query(node * 2, l, mid, pos)
        else:
            return self.query(node * 2 + 1, mid + 1, r, pos)

def solve():
    n, m = map(int, input().split())

    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    seg = SegmentTree(n)

    out = []

    for _ in range(m):
        q = list(map(int, input().split()))

        if q[0] == 1:
            _, x, y, k = q

            x -= 1
            y -= 1

            seg.update(
                1,
                0,
                n - 1,
                y,
                y + k - 1,
                x
            )

        else:
            _, pos = q
            pos -= 1

            src = seg.query(1, 0, n - 1, pos)

            if src == -1:
                out.append(str(b[pos]))
            else:
                out.append(str(a[src]))

    print("\n".join(out))

solve()
```

The segment tree stores lazy assignment values only. There is no separate tree array because we never need aggregated information such as sums or minimums. Every operation is interval assignment plus point query.

The most delicate part is the meaning of the stored value. If a node interval starts at `l` and stores `s`, then position `l` in `b` corresponds to `a[s]`. Every next position shifts by the same amount.

The `push` function is where many off-by-one mistakes happen. Suppose a parent interval `[l, r]` maps to `a[start...]`. The left child `[l, mid]` starts at the same source index, but the right child `[mid+1, r]` must skip exactly the length of the left interval:

```
right_start = start + (mid + 1 - l)
```

Without this adjustment, right-side queries return shifted values.

Updates use:

```
start + (l - ql)
```

because a fully covered node may begin after the left edge of the update range. Its source index in `a` must shift accordingly.

Queries descend to a single leaf. After all pending lazy values are pushed, the leaf contains either:

```
-1
```

meaning untouched original data from `b`, or the exact source index inside `a`.

## Worked Examples

### Example 1

Input:

```
a = [1, 2, 0, -1, 3]
b = [3, 1, 5, -2, 0]
```

Operations:

```
copy a[3..5] -> b[3..5]
query b[5]
query b[4]
```

State trace:

| Step | Operation | Stored Mapping on b | Query Result |
| --- | --- | --- | --- |
| 1 | Initial | none | - |
| 2 | copy a[3..5] -> b[3..5] | b[3]=a[3], b[4]=a[4], b[5]=a[5] | - |
| 3 | query b[5] | same | 3 |
| 4 | query b[4] | same | -1 |

This demonstrates how the tree stores relationships instead of values. Position `5` in `b` maps to position `5` in `a`, so the answer is `3`.

### Example 2

Input:

```
a = [10, 20, 30, 40, 50]
b = [1, 1, 1, 1, 1]
```

Operations:

```
copy a[1..3] -> b[2..4]
copy a[4..5] -> b[3..4]
query b[2]
query b[3]
query b[4]
```

Trace:

| Step | Operation | Logical b State |
| --- | --- | --- |
| 1 | Initial | [1,1,1,1,1] |
| 2 | copy a[1..3] -> b[2..4] | [1,10,20,30,1] |
| 3 | copy a[4..5] -> b[3..4] | [1,10,40,50,1] |
| 4 | query b[2] | 10 |
| 5 | query b[3] | 40 |
| 6 | query b[4] | 50 |

This trace shows how newer updates overwrite only overlapping regions while preserving unaffected positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log n) | Each update and query touches at most one path per tree level |
| Space | O(n) | Segment tree lazy array |

With `n, m <= 10^5`, the solution performs roughly a few million operations total, which comfortably fits within the time limit. The memory usage is also small since the tree stores only one integer per node.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    class SegmentTree:
        def __init__(self, n):
            self.lazy = [-1] * (4 * n)

        def push(self, node, l, r):
            if self.lazy[node] == -1 or l == r:
                return

            mid = (l + r) // 2

            start = self.lazy[node]

            self.lazy[node * 2] = start
            self.lazy[node * 2 + 1] = start + (mid + 1 - l)

            self.lazy[node] = -1

        def update(self, node, l, r, ql, qr, start):
            if ql <= l and r <= qr:
                self.lazy[node] = start + (l - ql)
                return

            self.push(node, l, r)

            mid = (l + r) // 2

            if ql <= mid:
                self.update(node * 2, l, mid, ql, qr, start)

            if qr > mid:
                self.update(node * 2 + 1, mid + 1, r, ql, qr, start)

        def query(self, node, l, r, pos):
            if l == r:
                return self.lazy[node]

            self.push(node, l, r)

            mid = (l + r) // 2

            if pos <= mid:
                return self.query(node * 2, l, mid, pos)

            return self.query(node * 2 + 1, mid + 1, r, pos)

    n, m = map(int, input().split())

    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    seg = SegmentTree(n)

    out = []

    for _ in range(m):
        q = list(map(int, input().split()))

        if q[0] == 1:
            _, x, y, k = q

            x -= 1
            y -= 1

            seg.update(1, 0, n - 1, y, y + k - 1, x)

        else:
            pos = q[1] - 1

            src = seg.query(1, 0, n - 1, pos)

            if src == -1:
                out.append(str(b[pos]))
            else:
                out.append(str(a[src]))

    return "\n".join(out)

# provided sample
assert run(
"""5 10
1 2 0 -1 3
3 1 5 -2 0
2 5
1 3 3 3
2 5
2 4
2 1
1 2 1 4
2 1
2 4
1 4 2 1
2 2
"""
) == \
"""0
3
-1
3
2
3
-1"""

# minimum size
assert run(
"""1 2
5
7
2 1
2 1
"""
) == \
"""7
7"""

# full overwrite
assert run(
"""4 3
1 2 3 4
9 9 9 9
1 1 1 4
2 3
"""
) == \
"""3"""

# overlapping updates
assert run(
"""5 5
10 20 30 40 50
1 1 1 1 1
1 1 2 3
1 4 3 2
2 2
2 3
2 4
"""
) == \
"""10
40
50"""

# untouched positions
assert run(
"""3 2
5 6 7
8 9 10
1 1 1 1
2 3
"""
) == \
"""10"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum size | Original value preserved | Correct handling of smallest arrays |
| Full overwrite | Copied value returned | Entire interval assignment |
| Overlapping updates | Newer copy overrides older one | Lazy propagation correctness |
| Untouched positions | Original `b` value survives | Correct `-1` handling |

## Edge Cases

Consider a partial overwrite after a larger copy.

Input:

```
5 3
1 2 3 4 5
9 9 9 9 9
1 1 1 5
1 3 3 1
2 3
```

After the first operation:

```
b = [1,2,3,4,5]
```

After the second operation:

```
b = [1,2,3,4,5]
```

Position `3` is overwritten again, but with the same value. The tree still has to correctly split intervals and update only one leaf range. The query returns `3`.

Now consider querying an untouched position.

Input:

```
3 1
5 6 7
8 9 10
2 2
```

No update ever touched `b[2]`. The query descends to a leaf whose mapping value remains `-1`, so the algorithm returns the original `b[2] = 9`.

Finally, consider overlapping updates.

Input:

```
5 4
1 2 3 4 5
0 0 0 0 0
1 1 2 3
1 4 3 2
2 3
2 4
```

The first update creates:

```
b = [0,1,2,3,0]
```

The second update overwrites positions `3` and `4`:

```
b = [0,1,4,5,0]
```

When querying position `3`, the descent encounters the newer assignment first because lazy propagation pushes the latest overwrite into the relevant subtree. The answer becomes `4`, not the stale earlier value `2`.
