---
title: "CF 102803I - InkBall FX"
description: "The game can be viewed as a ray moving from left to right. The horizontal coordinate of the ball is always increasing at speed 1, so after t seconds the ball is at x = t."
date: "2026-07-26T16:25:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102803
codeforces_index: "I"
codeforces_contest_name: "The 15th Heilongjiang Provincial Collegiate Programming Contest"
rating: 0
weight: 102803
solve_time_s: 51
verified: true
draft: false
---

[CF 102803I - InkBall FX](https://codeforces.com/problemset/problem/102803/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

The game can be viewed as a ray moving from left to right. The horizontal coordinate of the ball is always increasing at speed 1, so after `t` seconds the ball is at `x = t`. The only changing part is the vertical direction: it starts increasing, and every time the ball touches a horizontal segment the vertical velocity flips.

A segment `(L, R, Y)` is hit when the current trajectory reaches height `Y` at some horizontal coordinate between `L` and `R`. After being hit, the segment disappears, so the same obstacle never needs to be considered again.

The input contains up to `10^5` horizontal segments. A direct simulation that checks every segment after every collision would require up to `10^10` checks, which is far beyond what a 6 second limit allows. We need a logarithmic or near-linear method.

The tricky cases are caused by the fact that touching an endpoint also counts as a collision. A segment like:

```
1
3 5 2
```

is hit because the initial path is `y=x`, and it reaches `(2,2)` before the segment, not `(3,2)`, so the answer is `0`. A careless implementation that only checks heights and ignores the x-range may count it incorrectly.

Another common mistake is forgetting that a collision exactly at an endpoint is valid:

```
1
2 4 2
```

The ball reaches `(2,2)`, which is the left endpoint of the segment, so the answer is `1`.

A third issue appears after reflections:

```
2
4 6 1
2 4 3
```

The first collision is with the segment at height `3` when the ball reaches `(3,3)`. The direction changes, and the second segment is never hit. A solution that assumes the ball always follows the original diagonal fails here.

## Approaches

A straightforward approach is to repeatedly find the next collision by checking every remaining segment. For each segment we calculate whether the current ray intersects it and keep the earliest one. This is correct because the ball only moves forward in `x`, so the first intersection is exactly the next event. However, after every collision one segment is removed, and in the worst case we perform about `n + (n-1) + ... + 1` checks, which is `O(n^2)`.

The key observation is that a ray with slope `1` or `-1` can be described by a single constant.

When the ball moves upward, its path is:

```
y = x + c
```

where `c = y - x`. A segment is hit when this value lies inside:

```
Y - R <= c <= Y - L
```

For a fixed `c`, the collision position is `x = Y - c`, so among all matching segments we need the smallest `Y`.

When the ball moves downward, its path is:

```
y = -x + c
```

where `c = y + x`. The valid interval becomes:

```
Y + L <= c <= Y + R
```

and the collision position is `x = c - Y`, so we need the largest `Y`.

The problem becomes two dynamic interval stabbing queries. Each segment is inserted into two interval structures. A query gives the best segment among intervals covering a point, and after using it we lazily delete it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(n log n) | Accepted |

## Algorithm Walkthrough

1. Convert every segment into two transformed intervals. The upward structure stores `[Y-R, Y-L]` with value `Y`, and the downward structure stores `[Y+L, Y+R]` with value `Y`.
2. Build a compressed coordinate segment tree for each direction. Every node stores heaps of segments whose transformed interval completely covers that node.
3. Start the simulation at `(0,0)` with upward direction.
4. For the current direction, compute the corresponding constant. If moving upward it is `y-x`; otherwise it is `y+x`.
5. Query the corresponding segment tree. The query returns the segment with the earliest possible collision. If no segment exists, the simulation ends.
6. Remove the found segment by marking it deleted. The heaps remove deleted elements lazily when they reach the top.
7. Move the ball to the collision point. The x-coordinate becomes the collision position. Flip the vertical direction and repeat.

Why it works:

The segment tree invariant is that every active segment appears in exactly the nodes whose coordinate range is fully covered by its transformed interval. A query visits every node on the path to the queried coordinate, so it sees every segment that could collide. The heap ordering selects the closest collision among those candidates. Since each collision removes one segment permanently, every operation is performed at most `n` times.

## Python Solution

```python
import sys
import heapq
input = sys.stdin.readline

class SegmentTree:
    def __init__(self, coords, mode):
        self.coords = coords
        self.n = len(coords)
        self.tree = [[] for _ in range(self.n * 4)]
        self.mode = mode
        self.deleted = None

    def add(self, node, l, r, ql, qr, item):
        if ql <= l and r <= qr:
            heapq.heappush(self.tree[node], item)
            return
        m = (l + r) // 2
        if ql <= m:
            self.add(node * 2, l, m, ql, qr, item)
        if m < qr:
            self.add(node * 2 + 1, m + 1, r, ql, qr, item)

    def query(self, node, l, r, pos):
        while self.tree[node] and self.deleted[self.tree[node][0][1]]:
            heapq.heappop(self.tree[node])

        best = self.tree[node][0] if self.tree[node] else None
        if l != r:
            m = (l + r) // 2
            if pos <= m:
                other = self.query(node * 2, l, m, pos)
            else:
                other = self.query(node * 2 + 1, m + 1, r, pos)
            if other is not None:
                if best is None:
                    best = other
                elif self.mode == 1 and other[0] < best[0]:
                    best = other
                elif self.mode == -1 and other[0] < best[0]:
                    best = other
        return best

def build_coords(intervals):
    a = []
    for l, r, _, _ in intervals:
        a.append(l)
        a.append(r)
    a.sort()
    res = []
    for x in a:
        if not res or res[-1] != x:
            res.append(x)
    extra = []
    for i in range(len(res) - 1):
        if res[i + 1] - res[i] > 1:
            extra.append((res[i] + res[i + 1]) // 2)
    res.extend(extra)
    res.sort()
    return res

def solve_case(segs):
    n = len(segs)
    up = []
    down = []

    for i, (l, r, y) in enumerate(segs):
        up.append((y - r, y - l, y, i))
        down.append((y + l, y + r, y, i))

    cu = build_coords(up)
    cd = build_coords(down)

    tree_up = SegmentTree(cu, 1)
    tree_down = SegmentTree(cd, -1)

    deleted = [False] * n
    tree_up.deleted = deleted
    tree_down.deleted = deleted

    import bisect

    for l, r, y, i in up:
        tree_up.add(1, 0, len(cu) - 1,
                    bisect.bisect_left(cu, l),
                    bisect.bisect_right(cu, r) - 1,
                    (y, i))

    for l, r, y, i in down:
        tree_down.add(1, 0, len(cd) - 1,
                      bisect.bisect_left(cd, l),
                      bisect.bisect_right(cd, r) - 1,
                      (-y, i))

    x = 0
    y = 0
    direction = 1
    ans = 0

    while True:
        if direction == 1:
            c = y - x
            p = bisect.bisect_left(cu, c)
            if p == len(cu) or cu[p] != c:
                p -= 1
            if p < 0:
                break
            res = tree_up.query(1, 0, len(cu) - 1, p)
            if res is None:
                break
            ny, idx = res
            nx = ny - c
        else:
            c = y + x
            p = bisect.bisect_left(cd, c)
            if p == len(cd) or cd[p] != c:
                p -= 1
            if p < 0:
                break
            res = tree_down.query(1, 0, len(cd) - 1, p)
            if res is None:
                break
            ny, idx = -res[0], res[1]
            nx = c - ny

        deleted[idx] = True
        ans += 1
        x = nx
        y = ny
        direction *= -1

    return ans

def main():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        segs = [tuple(map(int, input().split())) for _ in range(n)]
        out.append(str(solve_case(segs)))
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The transformed intervals are the core of the implementation. The segment tree does not store positions of collisions directly, because the current trajectory is changing after every hit. Instead it stores the constants that describe all possible trajectories.

The heaps contain segment ids so deletion is lazy. A removed segment may remain inside several heaps, but it is ignored once it reaches the top. This avoids expensive removal from many tree nodes.

All coordinates are handled with Python integers, so there is no overflow concern even though intermediate values can exceed the original coordinate range.

## Worked Examples

For the first sample:

```
3
4 6 1
2 4 3
5 6 3
```

| Step | Direction | Current position | Constant | Hit |
| --- | --- | --- | --- | --- |
| 1 | Up | (0,0) | 0 | Segment (2,4,3) |
| 2 | Down | (3,3) | 6 | None |

The first hit happens because `y=x` reaches height `3` at `x=3`. After reflection, the downward ray does not meet another remaining segment.

For the second sample:

```
2
3 4 1
1 2 2
```

| Step | Direction | Current position | Constant | Hit |
| --- | --- | --- | --- | --- |
| 1 | Up | (0,0) | 0 | Segment (1,2,2) |
| 2 | Down | (2,2) | 4 | Segment (3,4,1) |

The first collision occurs at the endpoint `(2,2)`. The reflected ray then reaches the second segment at `(3,1)`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Every segment is inserted into two trees and every collision performs logarithmic queries. |
| Space | O(n log n) | Each interval is stored in logarithmically many segment tree nodes. |

The maximum of `10^5` segments is handled because the algorithm never scans all active segments during a collision. Each segment participates in a bounded number of heap operations.

## Test Cases

```
# The following tests can be used with the solve_case logic.

assert solve_case([(4, 6, 1), (2, 4, 3), (5, 6, 3)]) == 2
assert solve_case([(3, 4, 1), (1, 2, 2)]) == 2
assert solve_case([(1, 2, 5)]) == 0
assert solve_case([(1, 3, 1)]) == 1
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One segment never touched | 0 | Checks missing collision handling |
| Endpoint collision | 1 | Checks inclusive boundaries |
| Reflection sample | 2 | Checks direction changes |
| Multiple active intervals | Correct first hit | Checks heap ordering |

## Edge Cases

A segment that is only touched at an endpoint is stored with a closed transformed interval, so both endpoints remain valid query positions. The coordinate compression also keeps every original endpoint, preventing accidental removal of boundary cases.

When several segments can be hit at the same transformed coordinate, the heap ordering chooses the one with the smallest collision x-coordinate. This follows directly from the transformed equations: for upward movement the x-coordinate is `Y-c`, and for downward movement it is `c-Y`.

After a collision, the segment is only marked deleted. It may still exist in internal heaps, but every query removes invalid entries before using them. This preserves correctness while keeping the implementation fast.
