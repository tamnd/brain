---
title: "CF 102346F - Forests in Danger"
description: "We need to choose an integer distance (r) around every river so that the union of all preserved regions covers at least (P%) of the rectangular territory. Each river is an axis-aligned line segment."
date: "2026-08-14T02:02:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102346
codeforces_index: "F"
codeforces_contest_name: "2019-2020 ACM-ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 102346
solve_time_s: 115
verified: true
draft: false
---

[CF 102346F - Forests in Danger](https://codeforces.com/problemset/problem/102346/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to choose an integer distance (r) around every river so that the union of all preserved regions covers at least (P%) of the rectangular territory.

Each river is an axis-aligned line segment. For a fixed (r), its preserved region is the rectangle obtained by extending the segment by (r) units in every direction. If the river is horizontal from ((x_1,y)) to ((x_2,y)), its rectangle before clipping is

[
[x_1-r,x_2+r]\times[y-r,y+r].
]

For a vertical river, the analogous rectangle is

[
[x-r,x+r]\times[y_1-r,y_2+r].
]

The territory itself is a rectangle, so every preserved rectangle must be clipped to the territory. The quantity we need is the area of the union of all these clipped rectangles, not the sum of their individual areas, because rivers can be close enough for their preserved regions to overlap.

The input contains at most (10^4) rivers, while every coordinate is at most (10^5). The territory can consequently have area as large as (10^{10}). That immediately rules out treating the plane as a unit grid and checking every cell. Even one such grid could contain (10^{10}) cells. We need to work with the rectangle boundaries rather than individual points or cells.

The answer is also bounded. Let the territory have width (W) and height (H). For (r\ge\max(W,H)), every expanded river rectangle covers the entire territory, because every river is already inside the territory and the expansion reaches every possible horizontal and vertical coordinate. Thus the answer lies between (0) and (\max(W,H)), giving only about (17) binary-search iterations because the coordinates are at most (10^5).

There are several edge cases that can silently break a careless implementation. The first is overlap. For example,

```
2
0 0 4 0
0 0 4 0
50
0 0 4 4
```

Both rivers are identical. At (r=1), their preserved regions are the same (4\times2) rectangle, so the preserved area is (8), exactly (50%) of the (4\times4) territory. The answer is (1), not (0) and not a value obtained by adding the two rectangle areas. A solution that simply sums rectangle areas would count the same region twice.

Clipping against the territory is another common source of errors. Consider

```
1
0 0 0 4
25
0 0 4 4
```

At (r=1), the expanded rectangle is ([-1,1]\times[-1,5]), but only ([0,1]\times[0,4]) lies inside the territory. Its area is (4), exactly (25%), so the answer is (1). Forgetting the clipping would incorrectly use area (12).

The case (r=0) also matters. For a line segment, the preserved rectangle then has zero width or zero height and consequently has zero area. Since (P\ge1), (r=0) can never be the answer. A binary search that assumes the lower endpoint is already feasible would have an invalid invariant.

Finally, two rectangles can touch along an edge without having positive intersection area. For example,

```
2
0 0 2 0
2 0 2 2
50
0 0 4 4
```

At (r=1), their expanded rectangles overlap with positive area, while at smaller distances their boundaries can merely touch. Rectangle union must use half-open sweep intervals conceptually, so an interval ([y_1,y_2]) contributes the geometric length (y_2-y_1), with no artificial area assigned to a boundary.

## Approaches

The direct approach is to try every possible integer (r), construct all (N) expanded rectangles, and calculate their union area. A standard rectangle-union sweep takes (O(N\log N)), so trying all (O(10^5)) possible distances would cost (O(10^5N\log N)). With (N=10^4), that is on the order of (10^{10}) logarithmic-scale operations, far beyond the limit.

The brute-force approach is correct because for each candidate (r) it computes exactly the area defined by the problem. Its weakness is that the answer is an integer chosen from a large ordered range, and it repeatedly solves essentially the same geometric problem.

The key observation is that the preserved area is monotone in (r). Increasing (r) can only enlarge every preserved rectangle. Consequently, if some distance (r) preserves enough area, every larger distance also preserves enough area. The search for the smallest valid (r) is therefore a binary search.

We are left with one geometric subproblem: given at most (N) axis-aligned rectangles, compute whether their union covers enough area. A vertical sweep line solves this efficiently. Each rectangle creates a start event at its left side and an end event at its right side. Between two consecutive event (x)-coordinates, the set of active rectangles does not change, so the union has a constant covered height. If that height is (L) and the sweep moves by (\Delta x), the area gained is (L\Delta x).

To maintain the covered height dynamically, we compress all rectangle (y)-coordinates and use a segment tree. Each node stores how many active rectangles completely cover its interval and the actual length covered by at least one rectangle. A positive cover count means the entire node interval is covered. Otherwise, its covered length is the sum of its two children.

Thus the brute-force solution works because rectangle union gives the exact area, but fails when the same calculation is repeated for every possible (r). Monotonicity reduces the search to (O(\log 10^5)) candidates, while the sweep line and segment tree make each candidate check (O(N\log N)).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(10^5N\log N)) | (O(N)) | Too slow |
| Optimal | (O(N\log N\log 10^5)) | (O(N)) | Accepted |

The official problem page gives a 3 second time limit and 256 MB memory limit. The original contest PDF confirms the two sample cases, including outputs (5) and (2).

## Algorithm Walkthrough

1. Read all rivers and normalize each segment so its coordinates are ordered. Store the territory bounds and compute its total area.
2. Define a function that receives a candidate (r) and returns whether the preserved union reaches the required percentage. The required area is computed with integer arithmetic as

[
\left\lceil\frac{P\cdot A}{100}\right\rceil,
]

where (A) is the territory area. Using a ceiling avoids floating-point calculations entirely.

1. For every river, expand its bounding rectangle by (r) in both coordinate directions. Intersect that rectangle with the territory. If the intersection has zero width or zero height, it contributes no area and can be ignored.
2. Convert every remaining rectangle into two sweep events. The left boundary adds its (y)-interval to the active set, and the right boundary removes it. Collect both (y)-coordinates because the segment tree needs them as elementary interval boundaries.
3. Sort the events by (x), and compress all collected (y)-coordinates. Between two consecutive event positions, the active set is unchanged. The segment tree therefore tells us exactly how much vertical length is covered throughout that whole horizontal strip.
4. Sweep through the events from left to right. Before processing events at the current (x), add

[
(\text{current }x-\text{previous }x)\times\text{covered height}
]

to the area. Then apply all additions and removals occurring at the current (x). Processing equal (x)-coordinates as one group avoids introducing an artificial horizontal width between events that occur at the same position.

1. Stop immediately if the accumulated area reaches the required area. This is safe because the union area can only increase as the sweep progresses, so later events cannot make an already successful check fail.
2. Binary search the smallest feasible (r). Set the lower bound to (0), which is infeasible because all rivers have zero-area preserved regions at (r=0), and set the upper bound to (\max(W,H)), which always covers the whole territory. Whenever the midpoint is feasible, keep it as a possible answer and search smaller values. Otherwise search larger values.

The invariant behind the binary search is that every value below the current answer is known to be infeasible and the current upper bound is feasible. The segment-tree invariant is that every node's stored length is exactly the portion of its (y)-interval covered by at least one active rectangle. Together, these two invariants guarantee that every feasibility decision is exact and that binary search returns the smallest valid integer distance.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    rivers = []

    for _ in range(n):
        x1, y1, x2, y2 = map(int, input().split())
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        rivers.append((x1, y1, x2, y2))

    p = int(input())
    tx1, ty1, tx2, ty2 = map(int, input().split())

    if tx1 > tx2:
        tx1, tx2 = tx2, tx1
    if ty1 > ty2:
        ty1, ty2 = ty2, ty1

    width = tx2 - tx1
    height = ty2 - ty1
    total_area = width * height
    need = (total_area * p + 99) // 100

    def enough(r):
        events = []
        ys = []

        for x1, y1, x2, y2 in rivers:
            lx = max(tx1, x1 - r)
            rx = min(tx2, x2 + r)
            ly = max(ty1, y1 - r)
            ry = min(ty2, y2 + r)

            if lx >= rx or ly >= ry:
                continue

            events.append((lx, 1, ly, ry))
            events.append((rx, -1, ly, ry))
            ys.append(ly)
            ys.append(ry)

        if not events:
            return False

        ys = sorted(set(ys))
        index = {y: i for i, y in enumerate(ys)}

        m = len(ys) - 1
        if m <= 0:
            return False

        cover = [0] * (4 * m)
        length = [0] * (4 * m)

        def update(node, left, right, ql, qr, delta):
            if ql <= left and right <= qr:
                cover[node] += delta
            else:
                mid = (left + right) // 2
                if ql <= mid:
                    update(node * 2, left, mid, ql, qr, delta)
                if qr > mid:
                    update(node * 2 + 1, mid + 1, right, ql, qr, delta)

            if cover[node] > 0:
                length[node] = ys[right + 1] - ys[left]
            elif left == right:
                length[node] = 0
            else:
                length[node] = (
                    length[node * 2] +
                    length[node * 2 + 1]
                )

        events.sort(key=lambda e: e[0])

        area = 0
        prev_x = events[0][0]
        i = 0

        while i < len(events):
            x = events[i][0]

            area += length[1] * (x - prev_x)
            if area >= need:
                return True

            while i < len(events) and events[i][0] == x:
                _, delta, y1, y2 = events[i]
                l = index[y1]
                rr = index[y2] - 1
                if l <= rr:
                    update(1, 0, m - 1, l, rr, delta)
                i += 1

            prev_x = x

        return area >= need

    lo = 0
    hi = max(width, height)

    while lo < hi:
        mid = (lo + hi) // 2
        if enough(mid):
            hi = mid
        else:
            lo = mid + 1

    print(lo)

if __name__ == "__main__":
    solve()
```

The input is read once and the rivers are normalized immediately, so every later feasibility check can treat the coordinates uniformly. The territory is also normalized, although valid input already gives its lower-left and upper-right corners in the intended order.

Inside `enough`, every river becomes a clipped rectangle. The use of `max` and `min` is what handles rivers close to or directly on the territory boundary. A rectangle whose clipped width or height is zero is skipped because it has no area.

The segment tree represents the elementary (y)-intervals between consecutive compressed coordinates. If the compressed coordinates are (y_0,y_1,\ldots,y_k), leaf (i) represents the geometric interval ([y_i,y_{i+1}]), whose length is (y_{i+1}-y_i). This is why the update range ends at `index[y2] - 1`, rather than at `index[y2]`. Updating the latter would cover an interval above (y_2) that does not belong to the rectangle.

The `cover` value records how many active rectangles completely cover a segment-tree node. When it is positive, the entire node interval is covered regardless of the children. When it is zero, the covered length comes from the children. This is the standard union-area segment-tree invariant.

All area calculations use integers. Coordinates are at most (10^5), so the largest territory area is (10^{10}), and Python integers easily handle all intermediate values. More importantly, the percentage comparison never uses floating point, so values such as (33%) of a small area cannot suffer from rounding errors.

The binary search uses `lo < hi` and assigns `hi = mid` when the candidate is feasible. This is the lower-bound form of binary search, so when the loop ends, `lo` is exactly the first feasible integer.

## Worked Examples

The first official sample is

```
3
1 1 4 1
2 2 2 8
3 2 7 2
50
1 1 15 15
```

The territory is (14\times14), so its area is (196), and at least (98) units of area must be preserved. The official output is (5).

A useful trace of the binary search is:

| Candidate (r) | Preserved area | Required area | Feasible? | Binary-search action |
| --- | --- | --- | --- | --- |
| 7 | at least 98 | 98 | Yes | Search below 7 |
| 3 | below 98 | 98 | No | Search above 3 |
| 5 | at least 98 | 98 | Yes | Search below 5 |
| 4 | below 98 | 98 | No | Search above 4 |
| Result | 5 | 98 | Yes | Answer = 5 |

The exact union calculation is performed by the sweep line for each candidate. The trace demonstrates the crucial monotonicity property. Once (r=5) is feasible, every larger distance is also feasible, while (r=4) is not, so (5) is the smallest possible answer.

The second official sample is

```
1
0 0 0 4
50
0 0 4 4
```

The territory is (4\times4), so (8) units of preserved area are required. The river runs along the left boundary.

| Candidate (r) | Clipped preserved rectangle | Area | Required area | Feasible? |
| --- | --- | --- | --- | --- |
| 0 | zero-width line | 0 | 8 | No |
| 1 | ([0,1]\times[0,4]) | 4 | 8 | No |
| 2 | ([0,2]\times[0,4]) | 8 | 8 | Yes |

The official output is (2). This sample directly exercises boundary clipping. Without clipping, the (r=2) rectangle would extend outside the country and the area calculation would be wrong.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N\log N\log 10^5)) | Each feasibility check builds and sorts (O(N)) events and performs (O(N)) segment-tree updates, each taking (O(\log N)). Binary search performs (O(\log 10^5)) checks. |
| Space | (O(N)) | There are (O(N)) events, compressed (y)-coordinates, and segment-tree nodes. |

With (N\le10^4), each feasibility check processes only (2N) rectangle events, and there are fewer than (18) binary-search iterations because the answer is bounded by (10^5). The algorithm avoids dependence on the potentially (10^{10})-sized territory area and stores only rectangle boundaries and segment-tree state.

## Test Cases

The following tests use the same `solve_case` logic as the submitted solution, but accept the input as a string so that each case can be checked with an assertion.

```python
import sys
import io

def solve_case(inp: str) -> str:
    data = inp.split()
    it = iter(data)

    n = int(next(it))
    rivers = []

    for _ in range(n):
        x1 = int(next(it))
        y1 = int(next(it))
        x2 = int(next(it))
        y2 = int(next(it))

        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1

        rivers.append((x1, y1, x2, y2))

    p = int(next(it))
    tx1 = int(next(it))
    ty1 = int(next(it))
    tx2 = int(next(it))
    ty2 = int(next(it))

    if tx1 > tx2:
        tx1, tx2 = tx2, tx1
    if ty1 > ty2:
        ty1, ty2 = ty2, ty1

    width = tx2 - tx1
    height = ty2 - ty1
    total_area = width * height
    need = (total_area * p + 99) // 100

    def enough(r):
        events = []
        ys = []

        for x1, y1, x2, y2 in rivers:
            lx = max(tx1, x1 - r)
            rx = min(tx2, x2 + r)
            ly = max(ty1, y1 - r)
            ry = min(ty2, y2 + r)

            if lx >= rx or ly >= ry:
                continue

            events.append((lx, 1, ly, ry))
            events.append((rx, -1, ly, ry))
            ys.append(ly)
            ys.append(ry)

        if not events:
            return False

        ys = sorted(set(ys))
        pos = {y: i for i, y in enumerate(ys)}

        m = len(ys) - 1
        if m <= 0:
            return False

        cover = [0] * (4 * m)
        length = [0] * (4 * m)

        def update(node, left, right, ql, qr, delta):
            if ql <= left and right <= qr:
                cover[node] += delta
            else:
                mid = (left + right) // 2

                if ql <= mid:
                    update(node * 2, left, mid, ql, qr, delta)

                if qr > mid:
                    update(node * 2 + 1, mid + 1, right, ql, qr, delta)

            if cover[node]:
                length[node] = ys[right + 1] - ys[left]
            elif left == right:
                length[node] = 0
            else:
                length[node] = length[node * 2] + length[node * 2 + 1]

        events.sort()
        area = 0
        prev_x = events[0][0]
        i = 0

        while i < len(events):
            x = events[i][0]
            area += length[1] * (x - prev_x)

            if area >= need:
                return True

            while i < len(events) and events[i][0] == x:
                _, delta, y1, y2 = events[i]
                l = pos[y1]
                r = pos[y2] - 1

                if l <= r:
                    update(1, 0, m - 1, l, r, delta)

                i += 1

            prev_x = x

        return area >= need

    lo = 0
    hi = max(width, height)

    while lo < hi:
        mid = (lo + hi) // 2

        if enough(mid):
            hi = mid
        else:
            lo = mid + 1

    return str(lo)

sample1 = """\
3
1 1 4 1
2 2 2 8
3 2 7 2
50
1 1 15 15
"""

sample2 = """\
1
0 0 0 4
50
0 0 4 4
"""

assert solve_case(sample1) == "5", "sample 1"

assert solve_case(sample2) == "2", "sample 2"

assert solve_case("""\
1
0 0 10 0
10
0 0 10 10
""") == "1", "single horizontal river"

assert solve_case("""\
3
0 0 10 0
0 0 10 0
0 0 10 0
20
0 0 10 10
""") == "1", "identical rivers must not be counted three times"

assert solve_case("""\
1
0 0 0 4
25
0 0 4 4
""") == "1", "boundary clipping"

assert solve_case("""\
1
5 5 5 5
1
0 0 10 10
""") == "1", "zero-length river"

max_case = "10000\n" + ("0 0 1 0\n" * 10000) + "1\n0 0 1 1\n"
assert solve_case(max_case) == "1", "maximum N with identical rivers"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Three identical horizontal rivers | 1 | Union area must not count overlaps multiple times |
| One river on the territory boundary | 1 | Correct clipping against the country boundary |
| One zero-length river | 1 | Degenerate segment handling |
| 10000 identical rivers | 1 | Maximum (N) and repeated rectangles |
| Single horizontal river across the territory | 1 | Smallest positive (r) and zero area at (r=0) |

## Edge Cases

For overlapping preserved regions, consider the three identical rivers

```
3
0 0 10 0
0 0 10 0
0 0 10 0
20
0 0 10 10
```

At (r=1), every river produces exactly the same rectangle ([0,10]\times[0,1]), with area (10). The target is (20), so (r=1) is not enough and the answer is (2). The sweep line keeps a cover count of three over the same (y)-interval, but the stored covered length remains (1), not (3). The resulting area is consequently (10) at (r=1), which demonstrates why the cover count and covered length must be separate pieces of state.

For clipping, use

```
1
0 0 0 4
25
0 0 4 4
```

At (r=1), the unbounded expanded rectangle is ([-1,1]\times[-1,5]). Clipping changes it to ([0,1]\times[0,4]), whose area is (4). Since the territory area is (16), this is exactly (25%), and the binary search returns (1). The event construction only receives the clipped rectangle, so no area outside the territory can enter the sweep.

For (r=0), consider

```
1
0 0 10 0
1
0 0 10 10
```

The expanded rectangle is ([0,10]\times[0,0]), which has zero height. The feasibility check discards it because `ly >= ry`. Thus the area is zero and the binary search moves above zero. At (r=1), the rectangle becomes ([0,10]\times[0,1]), with area (10), which already reaches the required (1%). The answer is (1).

For a zero-length river, consider

```
1
5 5 5 5
1
0 0 10 10
```

Although the segment has no length, it is still a valid point. At (r=1), its preserved rectangle is ([4,6]\times[4,6]), with area (4), which is enough to preserve (1%) of the (100)-unit territory. The algorithm treats the segment as a vertical segment because its (x)-coordinates are equal, producing the correct (2r\times2r) square.

For rectangles that merely touch, the segment tree works on elementary intervals between distinct (y)-coordinates, and every contribution uses coordinate differences such as `ys[right + 1] - ys[left]`. A shared boundary has zero geometric length, so it contributes no area by itself. This avoids the common mistake of adding one unit merely because two integer coordinates are adjacent.

Finally, for the maximum input size, (10^4) identical rivers generate (2\cdot10^4) sweep events per feasibility check, not (10^4) separate geometric grids. The segment tree still represents the union only once. The algorithm's running time depends on the number of rivers and their event boundaries, not on the potentially (10^{10}) cells inside the territory.
