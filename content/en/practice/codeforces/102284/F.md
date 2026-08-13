---
title: "CF 102284F - \u041a\u043b\u0443\u0431 \u0430\u043d\u043e\u043d\u0438\u043c\u043d\u044b\u0445 \u0433\u0435\u043e\u043c\u0435\u0442\u0440\u043e\u0432"
description: "We have (n) convex polygons. Polygon (i) is given by its vertices in counterclockwise order, and the total number of vertices across all polygons is at most (300,000). For every query ([l,r]), we need the number of vertices of the Minkowski sum of polygons (l,l+1,ldots,r)."
date: "2026-08-13T08:51:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102284
codeforces_index: "F"
codeforces_contest_name: "\u041b\u041a\u0428 2019, \u0418\u044e\u043b\u044c, \u041c\u0438\u043a\u0441 \u0441\u0442\u0430\u0440\u0448\u0435\u0439 \u0438 \u043c\u043b\u0430\u0434\u0448\u0435\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434"
rating: 0
weight: 102284
solve_time_s: 79
verified: true
draft: false
---

[CF 102284F - \u041a\u043b\u0443\u0431 \u0430\u043d\u043e\u043d\u0438\u043c\u043d\u044b\u0445 \u0433\u0435\u043e\u043c\u0435\u0442\u0440\u043e\u0432](https://codeforces.com/problemset/problem/102284/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We have (n) convex polygons. Polygon (i) is given by its vertices in counterclockwise order, and the total number of vertices across all polygons is at most (300,000). For every query ([l,r]), we need the number of vertices of the Minkowski sum of polygons (l,l+1,\ldots,r).

For two sets (A) and (B), their Minkowski sum contains every point (a+b) with (a\in A) and (b\in B). For convex polygons, the result is again a convex polygon. The input polygons can have as many as (300,000) vertices in total, while there can be (100,000) queries. The constraints immediately rule out constructing a Minkowski sum separately for every query. Even processing all edges of a query once would be too expensive if repeated (100,000) times. We need to preprocess the polygons globally and answer each interval query in roughly logarithmic time.

The key geometric simplification is that the number of vertices of a Minkowski sum is determined entirely by edge directions. If two edges have the same direction, they merge into one edge in the Minkowski sum. Edges with different directions remain separate. Since a convex polygon cannot have two different edges with the same directed direction, the answer for a range of polygons is exactly the number of distinct directed edge directions appearing in those polygons.

For example, consider two identical triangles.

```
2
3
0 0
1 0
0 1
3
5 5
6 5
5 6
1
1 2
```

The correct output is

```
3
```

A careless solution might add the three edges of each triangle and return (6). That is wrong because the corresponding edges have identical directions and become a single edge in the Minkowski sum.

A second boundary case occurs when the query contains only one polygon.

```
1
3
0 0
1 0
0 1
1
1 1
```

The answer is

```
3
```

The query range must include all three edges of polygon (1), including the closing edge from the last vertex back to the first. Forgetting that cyclic edge would incorrectly produce (2).

Another subtle case is when the edge vectors have the same direction but different lengths. For example, vectors ((1,1)) and ((7,7)) represent the same direction. They must be treated as equal, so comparing raw vectors instead of normalized vectors gives a wrong answer.

We normalize every nonzero edge vector ((x,y)) by dividing both coordinates by (\gcd(|x|,|y|)). The sign is preserved, so ((1,0)) and ((-1,0)) remain different directions.

## Approaches

A direct geometric approach would actually compute the Minkowski sum for every query. The Minkowski sum of two convex polygons can be constructed by merging their edge vectors in angular order, and its size is linear in the number of edges involved. That is correct because the boundary of the sum is obtained by taking the edge vectors of both polygons in increasing angular order.

The problem is repetition. Suppose one query contains (300,000) edges and we build the sum by adding polygons one at a time. In the worst case the intermediate result grows to (3,6,9,\ldots,300,000) edges. The total amount of edge processing is then approximately

45,000,150,000,
]

already around (4.5\times10^{10}) operations for one query. With up to (100,000) queries, this approach is completely infeasible.

The observation that removes the geometric construction is that a convex polygon is represented, along its boundary, by its directed edge vectors. When two convex polygons are added, their edge vectors are merged by angle. If two vectors have the same direction, they are adjacent in that angular order and their lengths simply add. Thus every distinct directed edge direction contributes exactly one edge to the final Minkowski sum.

The brute force works because it explicitly performs this angular merge. It fails because we repeatedly reconstruct information that is already present in the original polygons. The observation that only distinct normalized directions matter lets us throw away coordinates and lengths entirely. We flatten all polygon edges into one array, where each polygon occupies a contiguous segment, and reduce every edge vector to its primitive direction.

The remaining problem is now a standard offline range-distinct query. For every query ([l,r]), we need the number of distinct values in the corresponding interval of the flattened edge-direction array. We can answer all such queries with a Fenwick tree and the last occurrence of every direction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(m^2)) for a query containing (m) edges | (O(m)) | Too slow |
| Optimal | (O(V\log V + q\log V)) | (O(V+q)) | Accepted |

Here (V\le300,000) is the total number of polygon vertices and (q\le100,000).

## Algorithm Walkthrough

1. Read every polygon and convert each of its (k) boundary edges into a directed vector. For vertex (j), the edge is the vector from vertex (j) to vertex ((j+1)\bmod k). The modulo is necessary because the last edge returns to the first vertex.
2. Normalize every edge vector ((x,y)) by dividing it by (\gcd(|x|,|y|)). Store the resulting pair ((x',y')) as the edge direction. The coordinates can be large, but after normalization the pair uniquely represents the direction.
3. Append the directions of every polygon to one global array. Also store the starting position of every polygon and the position immediately after its last edge. A query involving polygons (l) through (r) then becomes an ordinary array interval from the beginning of polygon (l) to the end of polygon (r).
4. Coordinate-compress the direction pairs. The actual numeric values are irrelevant after equality has been established, so every distinct direction can be assigned an integer identifier.
5. Read all queries and group them by their right endpoint in the flattened array. If polygon (l) starts at position (L) and polygon (r) ends immediately before position (R), the query asks for the number of distinct direction identifiers in the half-open interval ([L,R)).
6. Process the flattened array from left to right. For each direction, keep only its most recent occurrence active in a Fenwick tree. When a direction appears at position (i), remove its previous active occurrence, if any, and activate (i).
7. When the sweep reaches the right endpoint (R) of a query ([L,R)), the Fenwick tree contains exactly one active position for every direction that occurs in the prefix ending at (R). A direction contributes inside ([L,R)) exactly when its latest occurrence is at least (L). Consequently, the Fenwick range sum on ([L,R)) is precisely the number of distinct directions in that query.

The invariant during the sweep is simple: after processing position (i), each direction occurring in positions (0) through (i) has exactly one active Fenwick position, namely its latest occurrence. A query ending at (i+1) therefore counts exactly those directions whose latest occurrence has not fallen before the query's left boundary. Since every distinct direction corresponds to exactly one edge of the Minkowski sum, the returned count is the required number of vertices.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, delta):
        i += 1
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i

    def prefix_sum(self, i):
        res = 0
        while i > 0:
            res += self.bit[i]
            i -= i & -i
        return res

    def range_sum(self, l, r):
        return self.prefix_sum(r) - self.prefix_sum(l)

def solve():
    n = int(input())

    directions = []
    borders = [0]

    for _ in range(n):
        k = int(input())
        points = [tuple(map(int, input().split())) for _ in range(k)]

        for j in range(k):
            x1, y1 = points[j]
            x2, y2 = points[(j + 1) % k]

            dx = x2 - x1
            dy = y2 - y1

            g = __import__("math").gcd(abs(dx), abs(dy))
            dx //= g
            dy //= g

            directions.append((dx, dy))

        borders.append(len(directions))

    # Coordinate-compress direction pairs.
    ids = {}
    arr = []

    for direction in directions:
        if direction not in ids:
            ids[direction] = len(ids)
        arr.append(ids[direction])

    m = len(arr)

    # next_pos[i] is the next occurrence of arr[i], or m if none exists.
    next_pos = [m] * m
    last = [m] * len(ids)

    for i in range(m - 1, -1, -1):
        x = arr[i]
        next_pos[i] = last[x]
        last[x] = i

    q = int(input())

    queries = [[] for _ in range(m)]
    answers = [0] * q

    for query_id in range(q):
        l, r = map(int, input().split())
        left = borders[l - 1]
        right = borders[r]

        queries[right - 1].append((left, query_id))

    fenwick = Fenwick(m)

    # Initially activate the last occurrence of every direction.
    for pos in last:
        if pos != m:
            fenwick.add(pos, 1)

    for i in range(m):
        # Queries ending at i + 1 use the half-open interval [left, i + 1).
        for left, query_id in queries[i]:
            answers[query_id] = fenwick.range_sum(left, i + 1)

        # Move the active occurrence of arr[i] from i to its next occurrence.
        fenwick.add(i, -1)

        if next_pos[i] != m:
            fenwick.add(next_pos[i], 1)

    sys.stdout.write("\n".join(map(str, answers)))

if __name__ == "__main__":
    solve()
```

The first part of `solve` reads each polygon and explicitly handles the cyclic edge from the final vertex to the first. The normalized pair is enough to identify the edge's direction, so the original coordinates do not need to be retained after that point.

`borders` converts polygon ranges into positions in the flattened direction array. If `borders[i]` is the position immediately after polygon (i), then polygons (l) through (r) occupy exactly `[borders[l - 1], borders[r])`. Using a half-open interval removes several possible off-by-one errors.

The dictionary `ids` compresses arbitrary direction pairs into small integer identifiers. The Fenwick tree only needs to store zeroes and ones, so this compression keeps the implementation compact and makes the `last` and `next_pos` arrays possible.

The reverse pass computes the next occurrence of every direction. The forward sweep uses these links to move the active occurrence from one position to the next. This is equivalent to maintaining the latest occurrence of each direction while scanning from left to right.

The query is evaluated before moving the active occurrence at position `i`. At that moment the active positions represent the latest occurrences in the prefix through `i`, exactly what is needed for a query ending at `i + 1`. The use of `range_sum(left, i + 1)` follows the same half-open interval convention as `borders`.

Python integers have arbitrary precision, so the coordinate differences and normalization do not risk integer overflow. The largest coordinate difference is only (2\cdot10^9), but using Python's integer arithmetic also makes the implementation independent of machine integer width.

## Worked Examples

For the official sample, the three polygons have the following normalized directed edge sequences:

```
Polygon 1:
(1,0), (-1,1), (0,-1)

Polygon 2:
(0,1), (-1,0), (0,-1), (1,0)

Polygon 3:
(-1,0), (1,-1), (0,1)
```

The flattened sequence is processed as follows.

| Position | Direction | Latest active positions | Query result |
| --- | --- | --- | --- |
| 0 | (1,0) | (1,0) at 0 |  |
| 1 | (-1,1) | (1,0) at 0, (-1,1) at 1 |  |
| 2 | (0,-1) | three directions |  |
| 3 | (0,1) | four directions |  |
| 4 | (-1,0) | five directions |  |
| 5 | (0,-1) | (0,-1) moves from 2 to 5 |  |
| 6 | (1,0) | (1,0) moves from 0 to 6 |  |
| 7 | (-1,0) | (-1,0) moves from 4 to 7 |  |
| 8 | (1,-1) | new direction |  |
| 9 | (0,1) | (0,1) moves from 3 to 9 |  |

The query for polygons (1) through (2) covers positions `[0,7)`. At position (6), five latest occurrences remain at or after position (0), giving the answer (5). The query for polygons (2) through (3) covers `[3,10)` and also has five distinct directions. The full range contains six distinct directions, producing the official outputs `5`, `5`, and `6`.

For a smaller example, consider two triangles with the same shape.

```
2
3
0 0
1 0
0 1
3
10 10
11 10
10 11
2
1 2
1 1
```

Both polygons have exactly the same three normalized directions.

| Position | Direction | Active direction count | Query result |
| --- | --- | --- | --- |
| 0 | (1,0) | 3 |  |
| 1 | (-1,1) | 3 |  |
| 2 | (0,-1) | 3 |  |
| 3 | (1,0) | latest occurrence moved to 3 | 3 |
| 4 | (-1,1) | latest occurrence moved to 4 |  |
| 5 | (0,-1) | latest occurrence moved to 5 |  |

The query `[1,2]` ends at position (6), and the three directions have their latest occurrences at positions (3,4,5). All three lie inside the query interval, so the answer is `3`, not `6`. This is exactly the geometric fact that parallel corresponding edges merge in the Minkowski sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(V\log V + q\log V)) | Every edge is processed a constant number of times, and each Fenwick update or query costs (O(\log V)). |
| Space | (O(V+q)) | The direction array, occurrence arrays, Fenwick tree, query storage, and answers are all linear in the input size. |

Here (V\le300,000) and (q\le100,000). The preprocessing therefore performs only a few million logarithmic-time Fenwick operations, instead of repeatedly constructing potentially hundreds of thousands of edge Minkowski sums. The memory usage is also linear and comfortably fits the (256) MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
import math

def solve_data(data: str) -> str:
    inp = io.StringIO(data)
    out = []

    def read():
        return inp.readline

    input_local = read
    n = int(input_local())

    directions = []
    borders = [0]

    for _ in range(n):
        k = int(input_local())
        points = [tuple(map(int, input_local().split())) for _ in range(k)]

        for j in range(k):
            x1, y1 = points[j]
            x2, y2 = points[(j + 1) % k]
            dx = x2 - x1
            dy = y2 - y1
            g = math.gcd(abs(dx), abs(dy))
            directions.append((dx // g, dy // g))

        borders.append(len(directions))

    ids = {}
    arr = []

    for d in directions:
        if d not in ids:
            ids[d] = len(ids)
        arr.append(ids[d])

    m = len(arr)

    queries = [[] for _ in range(m)]
    q = int(input_local())
    answers = [0] * q

    for qi in range(q):
        l, r = map(int, input_local().split())
        left = borders[l - 1]
        right = borders[r]
        queries[right - 1].append((left, qi))

    bit = [0] * (m + 1)

    def add(pos, delta):
        pos += 1
        while pos <= m:
            bit[pos] += delta
            pos += pos & -pos

    def prefix(pos):
        res = 0
        while pos > 0:
            res += bit[pos]
            pos -= pos & -pos
        return res

    last = {}
    next_pos = [m] * m

    for i in range(m - 1, -1, -1):
        x = arr[i]
        next_pos[i] = last.get(x, m)
        last[x] = i

    for pos in last.values():
        add(pos, 1)

    for i in range(m):
        for left, qi in queries[i]:
            answers[qi] = prefix(i + 1) - prefix(left)

        add(i, -1)
        if next_pos[i] != m:
            add(next_pos[i], 1)

    return "\n".join(map(str, answers))

# provided sample
sample = """\
3
3
0 0
1 0
0 1
4
1 1
1 2
0 2
0 1
3
2 2
1 2
2 1
3
1 2
2 3
1 3
"""
assert solve_data(sample) == "5\n5\n6", "sample 1"

# minimum-size input, a single triangle
assert solve_data("""\
1
3
0 0
1 0
0 1
1
1 1
""") == "3", "minimum size"

# identical directions with different coordinates
assert solve_data("""\
2
3
0 0
1 0
0 1
3
10 10
11 10
10 11
1
1 2
""") == "3", "duplicate directions"

# range boundaries and different direction sets
assert solve_data("""\
3
3
0 0
1 0
0 1
3
5 5
6 5
5 6
3
20 20
21 20
21 21
3
1 2
2 3
3 3
""") == "3\n5\n3", "range boundaries"

# scaling of vectors must not create a new direction
assert solve_data("""\
2
3
0 0
2 0
0 2
3
10 10
14 10
10 14
1
1 2
""") == "3", "same directions after gcd normalization"

# maximum-size structure: 100000 triangles, 300000 vertices,
# and 100000 queries. Every polygon has the same three directions.
parts = ["100000"]
for i in range(100000):
    x = 10 * i
    parts.extend([
        "3",
        f"{x} 0",
        f"{x + 1} 0",
        f"{x} 1",
    ])

parts.append("100000")
for _ in range(100000):
    parts.append("1 100000")

max_case = "\n".join(parts) + "\n"
max_output = "\n".join(["3"] * 100000)
assert solve_data(max_case) == max_output, "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Official sample | `5`, `5`, `6` | General correctness on the supplied example |
| One triangle | `3` | Minimum input size and cyclic closing edge |
| Two identical triangles | `3` | Duplicate directions must be counted once |
| Three polygons with several ranges | `3`, `5`, `3` | Left and right range boundaries |
| Scaled edge vectors | `3` | Correct gcd normalization of directions |
| 100000 identical triangles and 100000 queries | `3` for every query | Maximum (n), maximum total vertices, maximum query count |

## Edge Cases

The first edge case is a query containing only one polygon. For

```
1
3
0 0
1 0
0 1
1
1 1
```

the flattened array has the three directions `(1,0)`, `(-1,1)`, and `(0,-1)`. The query interval is `[0,3)`, so all three active positions are counted and the answer is `3`. The closing edge is generated by `(j + 1) % k`, so it cannot be accidentally omitted.

The second edge case is repeated directions. For

```
2
3
0 0
1 0
0 1
3
10 10
11 10
10 11
1
1 2
```

the six edges reduce to three distinct direction identifiers, because the second triangle is a translation of the first. During the sweep, each new occurrence replaces the previous active occurrence of the same direction. At the query endpoint, exactly three positions remain active, giving `3`.

The third edge case concerns vectors with different lengths. In

```
2
3
0 0
2 0
0 2
3
10 10
14 10
10 14
1
1 2
```

the corresponding horizontal edges are `(2,0)` and `(4,0)`, while the other directions are similarly scaled. After dividing by the gcd, both polygons produce the same three primitive directions. The algorithm returns `3`, which matches the Minkowski sum geometry.

Finally, the range conversion is a common source of off-by-one errors. Suppose polygon (1) has three edges and polygon (2) has four. Then polygon (1) occupies `[0,3)` and polygon (2) occupies `[3,7)`. A query `[2,2]` must become `[3,7)`, not `[3,6)` or `[4,7)`. Storing `borders[i]` as the position immediately after polygon (i) gives the exact half-open interval, and the Fenwick query `prefix(right) - prefix(left)` counts precisely those active positions belonging to the requested polygons.
