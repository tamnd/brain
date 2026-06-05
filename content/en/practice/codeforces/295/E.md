---
title: "CF 295E - Yaroslav and Points"
description: "We have a set of points on the number line. Each point has an identity, so when an update says \"move point p by d\", only that specific point changes position. There are two operations."
date: "2026-06-05T17:48:14+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 295
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 179 (Div. 1)"
rating: 2500
weight: 295
solve_time_s: 139
verified: true
draft: false
---

[CF 295E - Yaroslav and Points](https://codeforces.com/problemset/problem/295/E)

**Rating:** 2500  
**Tags:** data structures  
**Solve time:** 2m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a set of points on the number line. Each point has an identity, so when an update says "move point `p` by `d`", only that specific point changes position.

There are two operations.

The first operation removes one point from its current coordinate and inserts it at a new coordinate. The statement guarantees that coordinates remain distinct after every update.

The second operation looks at all points whose coordinates lie inside a given interval `[l, r]`. Among those points, we must compute the sum of distances over every unordered pair.

If the selected coordinates are

$$y_1 < y_2 < \dots < y_k,$$

the query asks for

$$\sum_{1 \le i < j \le k}(y_j-y_i).$$

The constraints are the real challenge. Both the number of points and the number of queries can reach $10^5$. A solution that scans all points for every query would require roughly $10^{10}$ operations in the worst case, which is completely infeasible.

The coordinates themselves are large, up to $10^9$ in absolute value, and updates keep changing them. We cannot build a direct array indexed by coordinate.

A subtle case appears when the interval contains zero or one point. There are no pairs, so the answer must be zero.

For example:

```
Points: 5

Query: [0, 10]
```

Only one point is selected, so the answer is:

```
0
```

Another easy mistake is forgetting that updates move a specific point, not a coordinate value.

```
Points: 1 10
Update: move point 1 by +20
```

The resulting coordinates are:

```
21 10
```

not

```
1 30
```

A third source of bugs is handling query boundaries. If a point lies exactly at `l` or exactly at `r`, it must be included.

```
Points: 0 5 10
Query: [0, 10]
```

All three points participate.

The answer is:

```
(5-0) + (10-0) + (10-5) = 20
```

Using strict inequalities would incorrectly discard boundary points.

## Approaches

The most direct solution is to process each query independently. For a type 2 query, collect all points whose coordinates lie in `[l, r]`, sort them, and compute the pairwise distance sum.

This is correct because the definition is exactly the sum over all selected pairs.

Unfortunately, it is far too slow. A single query may contain $10^5$ points. Computing answers this way costs $O(n \log n)$ per query, leading to roughly $10^{10}$ operations overall.

The key observation is that the answer for a set of ordered coordinates can be merged from smaller pieces.

Suppose we split a coordinate range into a left half and a right half. Every coordinate in the left half is smaller than every coordinate in the right half.

For two groups:

$$L=\{x\},\qquad R=\{y\},$$

the cross contribution is

$$\sum (y-x).$$

Expanding this expression gives

$$|L|\cdot \sum R - |R|\cdot \sum L.$$

This depends only on the number of points and the sum of coordinates in each half.

That suggests a segment tree. For every node we store:

$$cnt = \text{number of active points}$$

$$sum = \text{sum of their coordinates}$$

$$ans = \text{sum of pairwise distances inside this segment}$$

When merging two children:

$$cnt = cnt_L + cnt_R$$

$$sum = sum_L + sum_R$$

$$ans = ans_L + ans_R + cnt_L \cdot sum_R - cnt_R \cdot sum_L$$

The last term is exactly the contribution of pairs whose endpoints lie in different children.

Updates become point deletions and insertions. Queries become ordinary segment tree range queries.

The coordinates are large and dynamic, so we compress all coordinates that can ever appear. Since every update value is known in advance, we can simulate the sequence offline and collect every coordinate that will ever exist.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(mn \log n)$ | $O(n)$ | Too slow |
| Optimal Segment Tree + Coordinate Compression | $O((n+m)\log(n+m))$ | $O(n+m)$ | Accepted |

## Algorithm Walkthrough

1. Read the initial coordinates.
2. Scan all queries once before processing them.
3. Simulate the coordinate changes of every point and collect every coordinate that ever appears.
4. Sort and deduplicate those coordinates. This becomes the coordinate compression array.
5. Build a segment tree over the compressed coordinates.
6. Insert every initial point into the tree. A leaf stores:

$$cnt=1,\quad sum=\text{coordinate},\quad ans=0.$$
7. For a type 1 update:

1. Remove the old coordinate of the point.
2. Compute the new coordinate.
3. Insert the new coordinate.
4. Update the stored position of that point.
8. For a type 2 query:

1. Find the first compressed coordinate not smaller than `l`.
2. Find the last compressed coordinate not greater than `r`.
3. Query that segment tree range.
4. Output the returned `ans`.
9. During every merge, compute:

$$cross = cnt_L \cdot sum_R - cnt_R \cdot sum_L$$

and set

$$ans = ans_L + ans_R + cross.$$

The reason this works is that every coordinate in the left child is smaller than every coordinate in the right child.

### Why it works

Each segment tree node stores the exact information needed to reconstruct the pairwise distance sum inside its interval.

The stored value `ans` already contains all pairs completely inside the left child and all pairs completely inside the right child. The only missing pairs are those with one endpoint in each child.

Because coordinates are ordered by the segment tree, every cross pair contributes `right - left`. Summing over all such pairs yields

$$cnt_L \cdot sum_R - cnt_R \cdot sum_L.$$

Thus every pair is counted exactly once during the merge. By induction on segment tree nodes, every query returns the correct sum of distances among all selected points.

## Python Solution

```python
import sys
from bisect import bisect_left, bisect_right

input = sys.stdin.readline

class SegTree:
    def __init__(self, coords):
        self.coords = coords
        self.n = len(coords)
        size = 4 * self.n + 5

        self.cnt = [0] * size
        self.sm = [0] * size
        self.ans = [0] * size

    def pull(self, p):
        lc = p * 2
        rc = lc + 1

        cnt_l = self.cnt[lc]
        cnt_r = self.cnt[rc]

        sum_l = self.sm[lc]
        sum_r = self.sm[rc]

        self.cnt[p] = cnt_l + cnt_r
        self.sm[p] = sum_l + sum_r

        cross = cnt_l * sum_r - cnt_r * sum_l
        self.ans[p] = self.ans[lc] + self.ans[rc] + cross

    def update(self, p, l, r, idx, delta):
        if l == r:
            self.cnt[p] += delta
            self.sm[p] += self.coords[idx] * delta
            self.ans[p] = 0
            return

        mid = (l + r) >> 1
        if idx <= mid:
            self.update(p * 2, l, mid, idx, delta)
        else:
            self.update(p * 2 + 1, mid + 1, r, idx, delta)

        self.pull(p)

    def query(self, p, l, r, ql, qr):
        if ql <= l and r <= qr:
            return (self.cnt[p], self.sm[p], self.ans[p])

        mid = (l + r) >> 1

        if qr <= mid:
            return self.query(p * 2, l, mid, ql, qr)

        if ql > mid:
            return self.query(p * 2 + 1, mid + 1, r, ql, qr)

        left = self.query(p * 2, l, mid, ql, qr)
        right = self.query(p * 2 + 1, mid + 1, r, ql, qr)

        cnt_l, sum_l, ans_l = left
        cnt_r, sum_r, ans_r = right

        cross = cnt_l * sum_r - cnt_r * sum_l

        return (
            cnt_l + cnt_r,
            sum_l + sum_r,
            ans_l + ans_r + cross
        )

def solve():
    n = int(input())
    x = list(map(int, input().split()))

    m = int(input())

    queries = []
    coords = x[:]

    cur = x[:]

    for _ in range(m):
        q = list(map(int, input().split()))
        queries.append(q)

        if q[0] == 1:
            p, d = q[1], q[2]
            cur[p - 1] += d
            coords.append(cur[p - 1])

    coords = sorted(set(coords))
    pos = {v: i for i, v in enumerate(coords)}

    seg = SegTree(coords)

    current = x[:]

    for v in current:
        seg.update(1, 0, seg.n - 1, pos[v], 1)

    out = []

    for q in queries:
        if q[0] == 1:
            p, d = q[1], q[2]
            p -= 1

            old = current[p]
            new = old + d

            seg.update(1, 0, seg.n - 1, pos[old], -1)
            seg.update(1, 0, seg.n - 1, pos[new], 1)

            current[p] = new

        else:
            lq, rq = q[1], q[2]

            L = bisect_left(coords, lq)
            R = bisect_right(coords, rq) - 1

            if L > R:
                out.append("0")
                continue

            _, _, ans = seg.query(1, 0, seg.n - 1, L, R)
            out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first pass over the queries performs coordinate compression. Every coordinate that can ever appear is collected before the segment tree is built.

Each leaf corresponds to one compressed coordinate value. Since coordinates are always distinct, a leaf contains either zero or one active point, but the implementation naturally works even if larger counts were allowed.

The merge formula is the heart of the solution. The segment tree never explicitly enumerates pairs. Instead, it keeps enough aggregate information to reconstruct the total contribution of all cross pairs in constant time.

The range query returns a triple `(count, sum, answer)`. When two partial results are merged during query processing, exactly the same merge formula is used as in the tree itself.

All arithmetic must use 64-bit integers. In Python this is automatic.

## Worked Examples

### Example 1

```
Points: 0 5 10
Query: [0,10]
```

| Segment | Count | Sum | Pair Distance Sum |
| --- | --- | --- | --- |
| {0} | 1 | 0 | 0 |
| {5} | 1 | 5 | 0 |
| Merge | 2 | 5 | 5 |
| {10} | 1 | 10 | 0 |
| Final Merge | 3 | 15 | 20 |

The final answer is:

$$(5-0)+(10-0)+(10-5)=20.$$

The table shows how the cross contribution recreates the distances without enumerating pairs.

### Example 2

```
Points: 1 4 8
Update: point 2 += 3
Query: [0,10]
```

After the update the coordinates become:

```
1 7 8
```

| Active Coordinates | Count | Sum | Answer |
| --- | --- | --- | --- |
| {1} | 1 | 1 | 0 |
| {7} | 1 | 7 | 0 |
| Merge | 2 | 8 | 6 |
| {8} | 1 | 8 | 0 |
| Final Merge | 3 | 16 | 14 |

The answer is:

$$(7-1)+(8-1)+(8-7)=14.$$

This trace demonstrates that updates only require removing one coordinate and inserting another.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n+m)\log(n+m))$ | Each update and query performs a constant number of segment tree operations |
| Space | $O(n+m)$ | Coordinate compression and segment tree storage |

The compressed coordinate count is at most the initial coordinates plus one new coordinate per update, which is $O(n+m)$. With $10^5$ points and $10^5$ queries, the logarithmic factor is small enough to fit comfortably within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    from bisect import bisect_left, bisect_right

    input_data = io.StringIO(inp)
    input = input_data.readline

    # paste solve() body here and return output
    return ""

# minimum size
# one point, one query
# answer must be 0

# assert run("1\n5\n1\n2 0 10\n") == "0"

# interval contains no points
# assert run("2\n0 10\n1\n2 20 30\n") == "0"

# boundary inclusion
# assert run("3\n0 5 10\n1\n2 0 10\n") == "20"

# update then query
# assert run(
# "3\n1 4 8\n2\n1 2 3\n2 0 10\n"
# ) == "14"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single point | 0 | No pairs exist |
| Empty interval | 0 | Correct range handling |
| Points exactly on boundaries | 20 | Inclusive endpoints |
| Update then query | 14 | Removal and insertion logic |

## Edge Cases

Consider a query interval that contains no points:

```
Points: 0 10
Query: [20,30]
```

The binary searches produce an empty compressed range. The algorithm immediately returns `0`. No segment tree query is performed.

Consider an interval containing exactly one point:

```
Points: 5
Query: [0,10]
```

The queried segment returns `cnt = 1` and `ans = 0`. Since there are no pairs, the result is correct.

Consider boundary coordinates:

```
Points: 0 5 10
Query: [0,10]
```

`bisect_left` and `bisect_right` include both endpoints. All three points are selected and the answer becomes `20`.

Consider a point moving across many other coordinates:

```
Points: 1 100
Update: point 1 += 200
```

The old coordinate is removed from its leaf and the new coordinate is inserted into another leaf. The segment tree remains ordered by coordinate value, so future cross-contribution calculations continue to be valid. The correctness argument never depends on how far a point moves.
