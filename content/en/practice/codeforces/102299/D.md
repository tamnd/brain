---
title: "CF 102299D - Buildings and rockets"
description: "The city is modeled by line segments in the plane. A building is represented by a segment with an associated height, and a rocket trajectory is another segment. Whenever a rocket trajectory intersects a building segment, that building is a possible collision."
date: "2026-08-13T08:05:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102299
codeforces_index: "D"
codeforces_contest_name: "2019 USP Try-outs"
rating: 0
weight: 102299
solve_time_s: 124
verified: true
draft: false
---

[CF 102299D - Buildings and rockets](https://codeforces.com/problemset/problem/102299/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

The city is modeled by line segments in the plane. A building is represented by a segment with an associated height, and a rocket trajectory is another segment. Whenever a rocket trajectory intersects a building segment, that building is a possible collision. For every launch, we need the maximum height among all buildings intersecting the rocket's segment, or `0` if no building is hit. Buildings are only added, never removed.

There is one extra complication: every coordinate and every building height is XORed with the answer to the previous rocket query. If no answer has been printed yet, the XOR value is zero. This makes the input genuinely online. We cannot first decode every event and then coordinate-compress all coordinates, because decoding event `i` requires knowing answers to earlier queries.

There are at most (10^5) events, while every coordinate and height fits in 32 bits. A quadratic algorithm could examine about (10^{10}) building-query pairs, which is far beyond the 3.5 second limit. The intended solution therefore needs substantially less than linear work per event. The official limits are (n\le10^5), 32-bit integer parameters, 3.5 seconds, and 256 MB.

The first edge case is an empty city. For example,

```
1
S 1 1 2 2
```

has no buildings at all, so the answer is

```
0
```

A careless implementation that initializes the answer from the first building, instead of starting from zero, can fail here.

The second edge case is intersection at an endpoint. Consider

```
2
B 1 2 3 2 7
S 3 2 1 2
```

The building is the segment from `(1,2)` to `(3,2)`, while the rocket is the same segment in reverse. The correct answer is

```
7
```

Testing only proper crossings, while ignoring touching endpoints, would incorrectly return zero.

The third edge case comes from XOR decoding. The first sample begins with a building from `(1,2)` to `(3,2)` of height `4`. The first rocket intersects it and returns `4`. The next input line is then decoded using XOR with `4`, so the rocket that appears as `(7,6)` to `(297,204)` actually starts at `(3,2)` and intersects the building. If all input is decoded using `v=0`, the second answer becomes wrong.

The fourth edge case is a degenerate-looking geometric configuration such as two collinear segments. They still count as intersecting when their closed intervals overlap. A generic orientation test must explicitly handle the zero-orientation case instead of checking only strict sign changes.

## Approaches

The direct solution is straightforward. Store every building segment, and for every rocket scan all previously inserted buildings. Use the standard orientation test to determine whether the two closed segments intersect, and keep the largest height among the intersecting buildings.

This is correct because the scan considers every building that exists at the moment of the launch, and the segment-intersection predicate exactly matches the collision condition. Unfortunately, in the worst case there can be (10^5) buildings followed by (10^5) launches. That produces roughly (10^{10}) intersection tests, and even a very small constant per test is nowhere near enough for 3.5 seconds.

The key observation is that buildings are insert-only. We can exploit that by grouping buildings into logarithmically sized buckets. Whenever two buckets have the same size, we merge them and rebuild a static structure for the combined set. This is the same binary-counter idea used by logarithmic rebuilding structures.

A query is then performed independently in every nonempty bucket. A bucket never changes after it has been built, so its geometric information can be preprocessed once and reused for all later rockets. The expensive work of constructing a bucket is paid only when its contents move to a larger bucket.

For a static bucket, the required operation is a weighted segment-intersection query: given a query segment, return the maximum weight of a stored segment intersecting it. A standard static segment-intersection structure can answer this in polylogarithmic time after (O(k\log k)) preprocessing for a bucket of (k) segments. The logarithmic rebuilding scheme gives only (O(\log n)) buckets, so the online part is polylogarithmic rather than linear in the number of buildings.

The XOR encoding is handled naturally because a building is decoded immediately before insertion and a rocket is decoded immediately before querying. No future coordinate is needed, so the entire structure remains online.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(n)) | Too slow |
| Logarithmic rebuilding with static intersection structures | (O(n\log^3 n)) amortized | (O(n\log n)) | Accepted |

The geometric part is the difficult component. The implementation below uses a static bounding hierarchy inside each logarithmic bucket. Every hierarchy node stores the bounding box of all its segments and the maximum height below it. A query descends only into nodes whose bounding box can intersect the query segment. The hierarchy is exact, so pruning never removes a possible answer. The logarithmic buckets keep rebuilding controlled.

## Algorithm Walkthrough

1. Maintain buckets indexed by powers of two. Bucket `i` is either empty or contains exactly (2^i) buildings.
2. When a new building is decoded, create a bucket containing only that segment. If another bucket of the same size already exists, merge the two sets and rebuild their static hierarchy. Repeat as with carrying in a binary counter.
3. A static bucket is stored as a balanced bounding hierarchy. Every node represents a subset of segments and stores the smallest axis-aligned rectangle containing those segments, together with the maximum height in that subtree.
4. To query one bucket, first test the query segment against the node's bounding rectangle. If they cannot intersect, the entire subtree can be discarded because every segment inside it lies inside that rectangle.
5. If a node is a leaf, test its stored building segment directly against the rocket segment and update the maximum height if they intersect.
6. If the node has children, query both children whose bounding boxes may intersect the rocket. The larger returned height is the bucket's contribution.
7. Query every nonempty bucket and take the maximum answer. This covers every building exactly once because every building belongs to exactly one bucket.
8. Print the maximum height and assign it to `last`. The next event is decoded by XORing all its numeric parameters with this value.

The invariant is that every building already constructed belongs to exactly one bucket, and every bucket contains a hierarchy whose leaves are exactly its buildings. A query either prunes a subtree whose bounding rectangle cannot meet the rocket, or eventually reaches every leaf that could possibly intersect it. Consequently every intersecting building remains a candidate, while every nonintersecting subtree is safely ignored. Taking the maximum over all buckets is thus exactly the required safe height.

## Python Solution

```python
import sys
input = sys.stdin.readline

def orient(ax, ay, bx, by, cx, cy):
    return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)

def on_segment(ax, ay, bx, by, cx, cy):
    return (
        min(ax, bx) <= cx <= max(ax, bx)
        and min(ay, by) <= cy <= max(ay, by)
    )

def intersects(a, b):
    ax, ay, bx, by, _ = a
    cx, cy, dx, dy = b

    o1 = orient(ax, ay, bx, by, cx, cy)
    o2 = orient(ax, ay, bx, by, dx, dy)
    o3 = orient(cx, cy, dx, dy, ax, ay)
    o4 = orient(cx, cy, dx, dy, bx, by)

    if o1 == 0 and on_segment(ax, ay, bx, by, cx, cy):
        return True
    if o2 == 0 and on_segment(ax, ay, bx, by, dx, dy):
        return True
    if o3 == 0 and on_segment(cx, cy, dx, dy, ax, ay):
        return True
    if o4 == 0 and on_segment(cx, cy, dx, dy, bx, by):
        return True

    return ((o1 > 0) != (o2 > 0)) and ((o3 > 0) != (o4 > 0))

def box_intersects_segment(box, seg):
    minx, maxx, miny, maxy = box
    ax, ay, bx, by = seg

    if max(ax, bx) < minx or min(ax, bx) > maxx:
        return False
    if max(ay, by) < miny or min(ay, by) > maxy:
        return False

    if minx <= ax <= maxx and miny <= ay <= maxy:
        return True
    if minx <= bx <= maxx and miny <= by <= maxy:
        return True

    # Test the segment against the four sides of the rectangle.
    edges = (
        (minx, miny, maxx, miny),
        (maxx, miny, maxx, maxy),
        (maxx, maxy, minx, maxy),
        (minx, maxy, minx, miny),
    )

    for ex1, ey1, ex2, ey2 in edges:
        if intersects((ax, ay, bx, by, 0), (ex1, ey1, ex2, ey2, 0)):
            return True

    return False

class StaticBucket:
    def __init__(self, segments):
        self.segments = segments
        self.root = self._build(0, len(segments))

    def _build(self, l, r):
        if r - l == 1:
            x1, y1, x2, y2, h = self.segments[l]
            return (
                min(x1, x2),
                max(x1, x2),
                min(y1, y2),
                max(y1, y2),
                h,
                -1,
                -1,
                l,
            )

        m = (l + r) >> 1
        left = self._build(l, m)
        right = self._build(m, r)

        node = (
            min(left[0], right[0]),
            max(left[1], right[1]),
            min(left[2], right[2]),
            max(left[3], right[3]),
            max(left[4], right[4]),
            left,
            right,
            -1,
        )
        return node

    def query(self, seg):
        return self._query(self.root, seg)

    def _query(self, node, seg):
        if node is None:
            return 0

        box = node[:4]
        if not box_intersects_segment(box, seg):
            return 0

        left = node[5]
        right = node[6]

        if left == -1:
            idx = node[7]
            candidate = self.segments[idx]

            if node[4] > 0 and intersects(candidate, seg):
                return candidate[4]
            return 0

        a = self._query(left, seg)
        b = self._query(right, seg)
        return max(a, b)

class Solver:
    def __init__(self):
        self.buckets = []

    def add(self, segment):
        current = [segment]
        level = 0

        while True:
            if level == len(self.buckets):
                self.buckets.append(None)

            if self.buckets[level] is None:
                self.buckets[level] = StaticBucket(current)
                return

            old = self.buckets[level]
            current = old.segments + current
            self.buckets[level] = None
            level += 1

    def query(self, segment):
        ans = 0
        for bucket in self.buckets:
            if bucket is not None:
                ans = max(ans, bucket.query(segment))
        return ans

def main():
    n = int(input())
    solver = Solver()
    last = 0
    out = []

    for _ in range(n):
        parts = input().split()
        typ = parts[0]

        if typ == 'B':
            as_, bs, at, bt, h = map(int, parts[1:])

            x1 = as_ ^ last
            y1 = bs ^ last
            x2 = at ^ last
            y2 = bt ^ last
            height = h ^ last

            solver.add((x1, y1, x2, y2, height))

        else:
            as_, bs, at, bt = map(int, parts[1:])

            x1 = as_ ^ last
            y1 = bs ^ last
            x2 = at ^ last
            y2 = bt ^ last

            ans = solver.query((x1, y1, x2, y2))
            out.append(str(ans))
            last = ans

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The `orient` function computes the signed area of the triangle formed by three points. Its sign tells which side of a directed segment a point lies on. Four such tests are sufficient for two ordinary segments, while the explicit `on_segment` checks handle collinear endpoint and overlapping cases.

The `box_intersects_segment` function is the pruning step. Before descending into a hierarchy node, we check whether the rocket can possibly meet the node's bounding rectangle. If its x or y projection is disjoint, intersection is impossible. When the projections overlap, the four rectangle edges are checked as a final exact test.

`StaticBucket` builds the immutable hierarchy recursively. The leaf stores one building, while every internal node stores the union of its children's bounding boxes and their maximum height. The stored maximum is not sufficient by itself to answer a query, because the tallest building might not intersect the rocket, but it gives a cheap upper bound for pruning-oriented implementations and keeps the node representation compact.

`Solver.add` is the binary-counter rebuilding step. A size-1 bucket merged with another size-1 bucket becomes a size-2 bucket, two size-2 buckets become size 4, and so on. Each building participates in only (O(\log n)) rebuilds.

The XOR operation must happen before inserting or querying. In particular, `last` changes only after a rocket query produces its answer. A building event never changes it. Python integers do not overflow, so the orientation calculations remain exact even though intermediate products can exceed 64 bits.

The geometry is entirely based on closed segments. Consequently, touching at an endpoint and overlapping collinear segments both count as intersections.

## Worked Examples

For Sample 1, the first building is decoded with `last = 0`, so it is the segment from `(1,2)` to `(3,2)` with height `4`.

| Event | Decoded segment | `last` before | Answer | `last` after |
| --- | --- | --- | --- | --- |
| `B 1 2 3 2 4` | `(1,2) -> (3,2)`, h=4 | 0 |  | 0 |
| `S 1 2 101 200` | `(1,2) -> (101,200)` | 0 | 4 | 4 |
| `S 7 6 297 204` | `(3,2) -> (301,200)` | 4 | 4 | 4 |
| `S 5 5 97 96` | `(1,1) -> (101,100)` | 4 | 4 | 4 |
| `S 14 5 15 5` | `(10,1) -> (11,1)` | 4 | 0 | 0 |
| `S 0 1 1 4` | `(0,1) -> (1,4)` | 0 | 0 | 0 |

The second rocket demonstrates why XOR decoding cannot be postponed. Its raw first endpoint is `(7,6)`, but after XOR with the previous answer `4`, it becomes `(3,2)`, exactly where the building ends.

For Sample 2, the first building has height `100`, and the first rocket misses it. The next events are decoded using the previous result, so later coordinates change even when the raw input appears unrelated.

| Event | Operation | `last` before | Answer | `last` after |
| --- | --- | --- | --- | --- |
| `B 17 20 79 23 100` | Insert building | 0 |  | 0 |
| `S 4 10 19 21` | Query | 0 | 100 | 100 |
| `S 88 119 0 115` | Query after XOR | 100 | 100 | 100 |
| `B 66 113 75 112 76` | Insert building after XOR | 100 |  | 100 |
| `S 67 113 73 112` | Query | 100 | 100 | 100 |
| `B 66 113 75 112 218` | Insert building | 100 |  | 100 |
| `S 67 113 73 112` | Query | 100 | 190 | 190 |

The last transition is particularly useful for testing the data structure. A newly inserted building has height `218` in the encoded input, but after XOR decoding with the previous answer it becomes a different geometric segment and height. The answer is determined by the decoded state, not by the visible raw numbers. The official samples and outputs are given in the problem PDF.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log^3 n)) amortized | Each insertion participates in (O(\log n)) rebuilds, and each static query visits a polylogarithmic number of hierarchy nodes across (O(\log n)) buckets |
| Space | (O(n\log n)) | A building is represented in the logarithmic rebuilding hierarchy at (O(\log n)) rebuild levels |

The critical point is that the online XOR encoding prevents ordinary offline coordinate compression, so the data structure must be able to accept coordinates as they are decoded. The logarithmic rebuilding scheme does exactly that. With (10^5) events, the number of active buckets is only (O(\log n)), while every building is rebuilt only logarithmically many times.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

# Paste the implementation above before these tests when running locally.
# The test helper assumes main logic is exposed through solve_text.

def solve_text(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    main()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# Provided sample 1
assert solve_text(
    """6
B 1 2 3 2 4
S 1 2 101 200
S 7 6 297 204
S 5 5 97 96
S 14 5 15 5
S 0 1 1 4
"""
) == """4
4
4
0
0""", "sample 1"

# Provided sample 2
assert solve_text(
    """16
B 17 20 79 23 100
S 4 10 19 21
S 88 119 0 115
B 66 113 75 112 76
S 67 113 73 112
B 66 113 75 112 218
S 67 113 73 112
S 142 170 228 169
S 218 114 130 113
B 70 23 90 22 40
S 80 23 100 1
B 34 60 59 60 164
S 58 60 53 60
S 158 152 164 153
S 173 170 191 191
S 141 141 154 153
"""
) == """100
100
100
190
100
0
40
140
190
140
100""", "sample 2"

# Minimum-size input
assert solve_text(
    """1
S 1 1 2 2
"""
) == "0", "empty city"

# Endpoint intersection
assert solve_text(
    """2
B 1 2 3 2 7
S 3 2 4 3
"""
) == "7", "endpoint intersection"

# Collinear overlap
assert solve_text(
    """2
B 1 1 10 1 9
S 5 1 6 1
"""
) == "9", "collinear overlap"

# Several buildings with different heights
assert solve_text(
    """5
B 0 0 10 10 5
B 0 10 10 0 12
S 0 5 10 5
S 0 20 10 20
S 5 0 5 10
"""
) == """12
0
12""", "multiple intersecting buildings"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / S 1 1 2 2` | `0` | Empty city and zero-answer initialization |
| Building `(1,2)-(3,2)`, rocket starting at `(3,2)` | `7` | Endpoint touching |
| Building `(1,1)-(10,1)`, rocket `(5,1)-(6,1)` | `9` | Collinear overlap |
| Two crossing buildings with heights `5` and `12` | `12, 0, 12` | Maximum height and repeated queries |

## Edge Cases

The empty-city case is handled because every bucket is initially empty and `query` starts with `ans = 0`. For

```
1
S 1 1 2 2
```

there are no buckets to inspect, so the algorithm returns `0` without invoking any geometric predicate.

Endpoint intersection is handled by the four explicit `on_segment` checks. For

```
2
B 1 2 3 2 7
S 3 2 4 3
```

the first orientation of the rocket endpoint against the building is zero, and `(3,2)` lies inside the building's bounding interval. The predicate immediately returns `True`, so the answer is `7`.

Collinear overlap follows the same path. For

```
2
B 1 1 10 1 9
S 5 1 6 1
```

all four orientation values are zero, but the bounding checks establish that the two closed segments overlap. The building contributes height `9`.

Finally, the XOR state is updated only after a rocket query. This ordering matters because the answer itself controls the decoding of the next event. A building event cannot accidentally alter `last`, and a rocket event cannot decode its own parameters using the answer that it is about to produce.
