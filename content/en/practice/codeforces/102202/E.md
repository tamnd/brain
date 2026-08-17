---
title: "CF 102202E - Water Knows the Answer"
description: "We have (N) rectangular boxes. Each box can be placed in either orientation, and all boxes must form one contiguous row on the ground. Rain falls vertically, so water can remain only in a region that is horizontally enclosed by boxes."
date: "2026-08-18T01:12:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102202
codeforces_index: "E"
codeforces_contest_name: "2019 KAIST RUN Spring Contest"
rating: 0
weight: 102202
solve_time_s: 397
verified: false
draft: false
---

[CF 102202E - Water Knows the Answer](https://codeforces.com/problemset/problem/102202/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We have (N) rectangular boxes. Each box can be placed in either orientation, and all boxes must form one contiguous row on the ground. Rain falls vertically, so water can remain only in a region that is horizontally enclosed by boxes.

The useful way to think about one possible water level (H) is to decide which boxes form the two walls of the container and which boxes sit inside it. Let

[
L_i=\max(w_i,h_i),\qquad S_i=\min(w_i,h_i).
]

For a box used inside the container, the best orientation is to put its longer side horizontally and its shorter side vertically. If (S_i<H), that box then contributes

[
L_i(H-S_i)
]

to the stored area. If (S_i\ge H), it contributes nothing.

A box can instead be used as a wall. To reach level (H), its vertical side must be at least (H), so this is possible exactly when (L_i\ge H). In that role we rotate it, putting its longer side vertically. Consequently, for a fixed (H), we need two distinct boxes with (L_i\ge H) to be the two walls. Among all such boxes, we should choose the two whose ordinary contributions (L_i(H-S_i)) are smallest, because those are the two contributions we lose by turning the boxes into walls. This fixed-height formulation is the central reduction used by the solution.

The constraints rule out anything quadratic in (N). With (N) as large as (250000), even (O(N^2)) would mean about (6.25\times10^{10}) pair operations. The side lengths are at most (10^6), which gives us a useful bounded coordinate range, but iterating over every height and every box would still require up to (10^6\cdot250000=2.5\times10^{11}) evaluations. We need roughly (O(N\log N)).

There are several edge cases that a direct implementation can mishandle. First, there may be fewer than two boxes capable of reaching a chosen level. For example,

```
3
1 3
1 2
1 1
```

has only one box with (L_i\ge3), so level (3) cannot hold any water at all. A routine that simply computes contributions without checking for two walls could report a positive value.

Second, a box whose shorter side is exactly the water level contributes zero, not a negative amount. For

```
3
1 2
1 2
1 1
```

the correct answer is (1). The two (1\times2) boxes can be rotated into vertical walls of height (2), while the (1\times1) box holds one unit of water. Using (H-S_i) without clamping at zero would incorrectly introduce negative contributions.

Third, rotation matters in both roles. Consider

```
3
2 5
2 5
100 1
```

The two (2\times5) boxes become vertical walls of height (5), while the (100\times1) box lies horizontally inside them. The answer is (100(5-1)=400). Treating the original input width as permanently horizontal would miss this arrangement.

Finally, equal dimensions cause no special geometric complication. For

```
3
2 2
2 2
2 2
```

every possible arrangement has zero stored water, so the answer is (0). The implementation must allow equal (L_i) and (S_i) without relying on strict inequalities between them.

## Approaches

The most literal brute force enumerates every permutation of the boxes, every choice of rotation, and then evaluates the resulting arrangement. That takes (N!,2^N) arrangements, with an (O(N)) scan for each arrangement, giving (O(N!,2^N N)). At (N=250000), this is far beyond consideration.

A more useful naive approach is to use the fixed-height observation. For every possible integer (H), scan all boxes, compute (L_i\max(0,H-S_i)), identify the two boxes with (L_i\ge H) having the smallest contributions, and subtract them. There are at most (10^6) possible heights, so this takes (O(10^6N)), or (2.5\times10^{11}) box evaluations in the worst case.

The brute force works because, once (H) and the two walls are known, every remaining box can be handled independently. The problem is that repeatedly finding the two smallest values is expensive. The key observation is that every box contributes a linear function of (H):

[
f_i(H)=L_iH-L_iS_i.
]

We only need the two smallest active functions, where a box becomes eligible as a wall when (H\le L_i). This is exactly the type of dynamic minimum-of-lines query handled by a Li Chao tree. The original solution uses a Li Chao tree modified so that every node keeps its two best lines rather than only its single best line.

There is one more optimization. The fixed-height answer does not have to be checked at all (10^6) heights. Between two consecutive values appearing among the (S_i) and (L_i), the set of contributing boxes and the set of possible walls are unchanged. The total contribution is affine in (H), while the sum of the two smallest affine functions is concave. Their difference is consequently convex, and a convex function reaches its maximum on an interval at an endpoint. Thus it is enough to check the distinct values among all (S_i) and (L_i).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N!2^N N)) | (O(N)) | Too slow |
| Fixed height, scan all boxes | (O(10^6N)) | (O(N)) | Too slow |
| Optimal | (O(N\log N)) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. For every box, compute (L_i=\max(w_i,h_i)) and (S_i=\min(w_i,h_i)). Think of (L_i) as the dimension that can be used either as the horizontal width of an interior box or as the vertical height of a wall. Its contribution as an interior box at level (H) is

[
g_i(H)=\max(0,L_i(H-S_i)).
]

1. Fix a water level (H). A box can be one of the two outer walls exactly when (L_i\ge H). Every other box can be placed between those walls. The maximum area for this (H) is the sum of all (g_i(H)), minus the two smallest (g_i(H)) among boxes satisfying (L_i\ge H).
2. Observe that before applying the maximum with zero, every contribution is the line

[
f_i(H)=L_iH-L_iS_i.
]

We process (H) from large to small. When we reach (H=L_i), box (i) becomes eligible to be a wall and its line is inserted into the Li Chao tree. Since we never increase (H) again, an inserted line remains eligible for every later query.

1. Maintain a Li Chao tree over the candidate height coordinates. A normal Li Chao node stores the line that is minimum at its midpoint. Here we store the two smallest distinct lines at the midpoint. During insertion, the better line becomes the first line, the next best becomes the second line, and only the displaced candidate has to continue recursively into one child.
2. For a query at height (H), walk from the root toward the leaf representing (H). At every visited node, both stored lines are candidates for the two smallest values. Merge those values into two running minima. This gives the smallest and second-smallest raw values of (f_i(H)) among all currently inserted wall candidates.
3. Separately compute the sum of all nonnegative contributions. Sort the boxes by (S_i), and build prefix sums of (L_i) and (L_iS_i). For a height (H), all boxes with (S_i<H) contribute, so if their total (L_i) is (A) and their total (L_iS_i) is (B), the total is

[
AH-B.
]

The values with (S_i=H) contribute zero, so using either strict or non-strict inclusion at that boundary gives the same result.

1. Subtract the two smallest nonnegative wall contributions obtained from the Li Chao tree. If fewer than two wall candidates exist, that height cannot contain water and is skipped.
2. Check every distinct value among all (L_i) and (S_i), keeping the largest resulting area. These are sufficient because between consecutive event heights the active sets are fixed and the resulting objective is convex, so an interior height cannot be better than both endpoints.

Why it works: for any fixed (H), every box that is not one of the two walls can be oriented independently to contribute exactly (g_i(H)). The only boxes that must be sacrificed are the two walls, so choosing the two smallest eligible contributions is optimal. The Li Chao tree maintains precisely those two minima. The prefix sums give the contribution of every box before the two walls are removed. Finally, every interval without an (S_i) or (L_i) event has a fixed set of participating lines, and its objective is convex, so checking its endpoints covers its maximum. Thus the best value examined by the algorithm equals the globally optimal water area.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

INF = 10**30

def solve():
    n = int(input())

    L = [0] * (n + 1)
    S = [0] * (n + 1)

    for i in range(1, n + 1):
        w, h = map(int, input().split())
        if w < h:
            w, h = h, w
        L[i] = w
        S[i] = h

    # Candidate heights are exactly the points where either
    # a contribution starts/ends or a box becomes a possible wall.
    events = sorted(set(L[1:] + S[1:]))

    # Sort boxes by wall threshold, descending.
    by_l = list(range(1, n + 1))
    by_l.sort(key=L.__getitem__, reverse=True)

    # Sort boxes by their smaller side for prefix sums.
    by_s = list(range(1, n + 1))
    by_s.sort(key=S.__getitem__)

    svals = [0] * n
    pref_l = [0] * (n + 1)
    pref_ls = [0] * (n + 1)

    for j, idx in enumerate(by_s):
        svals[j] = S[idx]
        pref_l[j + 1] = pref_l[j] + L[idx]
        pref_ls[j + 1] = pref_ls[j] + L[idx] * S[idx]

    # Dynamic Li Chao tree.
    # Each inserted line creates at most one new node.
    left = [0] * (n + 1)
    right = [0] * (n + 1)
    best = [0] * (n + 1)
    second = [0] * (n + 1)

    root = 0
    nodes = 0

    # We use the compressed event coordinates as the Li Chao domain.
    xs = events
    m = len(xs)

    def value(idx, x):
        if idx == 0:
            return INF
        return L[idx] * x - L[idx] * S[idx]

    def insert(line):
        nonlocal root, nodes

        if root == 0:
            nodes += 1
            root = nodes
            best[root] = line
            return

        node = root
        lo = 0
        hi = m - 1
        cur = line

        while True:
            mid = (lo + hi) >> 1
            xmid = xs[mid]

            a = best[node]
            b = second[node]

            if value(a, xmid) > value(cur, xmid):
                best[node], second[node], cur = cur, a, b
            elif value(b, xmid) > value(cur, xmid):
                second[node], cur = cur, b

            if cur == 0 or lo == hi:
                return

            # cur can improve on the current second-best line
            # only in a child where the two lines can change order.
            if value(second[node], xs[lo]) > value(cur, xs[lo]):
                nxt = left[node]
                if nxt == 0:
                    nodes += 1
                    nxt = nodes
                    left[node] = nxt
                    best[nxt] = cur
                    return
                node = nxt
                hi = mid
            elif value(second[node], xs[hi]) > value(cur, xs[hi]):
                nxt = right[node]
                if nxt == 0:
                    nodes += 1
                    nxt = nodes
                    right[node] = nxt
                    best[nxt] = cur
                    return
                node = nxt
                lo = mid + 1
            else:
                return

    def query(x):
        if root == 0:
            return INF, INF

        lo = 0
        hi = m - 1
        node = root
        first = INF
        second_best = INF

        while node:
            v = value(best[node], x)
            if v < first:
                second_best = first
                first = v
            elif v < second_best:
                second_best = v

            v = value(second[node], x)
            if v < first:
                second_best = first
                first = v
            elif v < second_best:
                second_best = v

            if lo == hi:
                break

            mid = (lo + hi) >> 1
            pos = bisect_left(xs, x, lo, hi + 1)

            if pos <= mid:
                node = left[node]
                hi = mid
            else:
                node = right[node]
                lo = mid + 1

        return first, second_best

    ans = 0
    p = 0

    for H in reversed(events):
        while p < n and L[by_l[p]] >= H:
            insert(by_l[p])
            p += 1

        # Boxes with S_i < H have positive possible contribution.
        k = bisect_left(svals, H)
        total = H * pref_l[k] - pref_ls[k]

        first, second_best = query(H)

        # Two distinct walls are mandatory.
        if second_best == INF:
            continue

        total -= max(first, 0)
        total -= max(second_best, 0)

        if total > ans:
            ans = total

    print(ans)

if __name__ == "__main__":
    solve()
```

The first part of the implementation normalizes every rectangle into (L_i) and (S_i). The input orientation no longer matters after this point, because the solution may rotate every box independently.

The two sorted orders serve different purposes. `by_l` controls when a box enters the Li Chao structure as a possible wall. `by_s` supports the prefix sums needed to evaluate the sum of all ordinary box contributions at a height.

The Li Chao implementation is slightly different from the textbook one. Each node stores `best[node]` and `second[node]`. When inserting a new line, the two best lines at the midpoint stay in the node, while the displaced candidate continues toward a child. Since one insertion can create at most one new node, at most (N) nodes are created, so the dynamic tree uses (O(N)) memory.

The line evaluation is always done with Python integers. The largest possible area is on the order of (N\cdot10^6\cdot10^6=2.5\times10^{17}), so fixed-width 32-bit arithmetic would overflow. Python integers avoid that issue automatically.

The query walks down the compressed coordinate tree. The `bisect_left` inside the query locates the side containing (x). Since the query coordinates themselves belong to `xs`, this is exact. The implementation keeps the two smallest values seen along the root-to-leaf path, which is enough because every line stored in a Li Chao node is a candidate for the queried point.

The subtraction uses `max(value, 0)` because (L_i(H-S_i)) is only a hypothetical contribution. A box with (S_i\ge H) contributes zero, not a negative amount. This is especially relevant because the Li Chao tree intentionally keeps raw affine functions rather than clamped functions.

## Worked Examples

### Sample 1

The three boxes become ((L,S)=(4,3),(6,2),(5,1)). The event heights are (1,2,3,4,5,6).

| (H) | Inserted wall candidates | Total potential area | Two smallest wall values | Candidate answer |
| --- | --- | --- | --- | --- |
| 6 | box 2 | 61 | fewer than two | 0 |
| 5 | boxes 2, 3 | 46 | 18, 20 | 8 |
| 4 | boxes 1, 2, 3 | 31 | 4, 12 | 15 |
| 3 | boxes 1, 2, 3 | 16 | 0, 6 | 10 |
| 2 | boxes 1, 2, 3 | 5 | 0, 0 | 5 |
| 1 | boxes 1, 2, 3 | 0 | 0, 0 | 0 |

At (H=4), the potential contributions are (4,12,15). The two boxes with contributions (4) and (12) become the walls, leaving the third box to store (15) units of water. Thus the answer is (15).

### Constructed example

Consider

```
3
1 3
1 3
1 1
```

The normalized boxes are ((3,1),(3,1),(1,1)). The only useful event heights are (1) and (3).

| (H) | Inserted wall candidates | Total potential area | Two smallest wall values | Candidate answer |
| --- | --- | --- | --- | --- |
| 3 | boxes 1, 2 | 14 | 6, 6 | 2 |
| 1 | boxes 1, 2 | 0 | 0, 0 | 0 |

At height (3), the two (1\times3) boxes are rotated into vertical walls of height (3). The (1\times1) box stays inside with its height (1), so it holds (3-1=2) units of water. The answer is (2).

These traces also show why the two smallest contributions have to be removed rather than simply choosing the two tallest boxes. At (H=3), the two long boxes are necessarily walls, and their hypothetical interior contributions are exactly the values removed by the Li Chao query.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N\log N)) | Two sorts plus (N) Li Chao insertions and (O(N)) height queries, each taking (O(\log N)) |
| Space | (O(N)) | Box arrays, sorting arrays, prefix sums, and at most (N) Li Chao nodes |

With (N=250000), (O(N\log N)) is appropriate for the three-second limit, while the (O(N)) memory usage is comfortably inside the 1024 MB limit. The bounded side length is used only to motivate the fixed-height formulation; the implementation compresses the relevant heights, so it does not need a million-element Li Chao tree.

## Test Cases

The following harness assumes the solution above is saved as `solution.py` and exposes the `solve()` function shown in the implementation.

```python
import sys
import io
import solution

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solution.input = sys.stdin.readline
        solution.solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run(
    """3
4 3
2 6
5 1
"""
) == "15", "sample 1"

# Minimum-size input, and a water level exactly equal to the two wall heights.
assert run(
    """3
1 3
1 3
1 1
"""
) == "2", "minimum size and exact wall height"

# All boxes are identical, so no arrangement can trap water.
assert run(
    """3
2 2
2 2
2 2
"""
) == "0", "all equal values"

# The long dimension must be used horizontally for the interior box.
assert run(
    """3
2 5
2 5
100 1
"""
) == "400", "rotation choice"

# Water appears exactly at H = S + 1, catching strict-boundary mistakes.
assert run(
    """3
1 2
1 2
1 1
"""
) == "1", "off-by-one at the water level"

# Maximum N, with the smallest possible dimensions.
# There is no possible water, but the test exercises the full input size.
max_n = 250000
max_case = str(max_n) + "\n" + ("1 1\n" * max_n)
assert run(max_case) == "0", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / 1 3 / 1 3 / 1 1` | 2 | Minimum (N), two valid walls, exact boundary height |
| `3 / 2 2 / 2 2 / 2 2` | 0 | All-equal dimensions |
| `3 / 2 5 / 2 5 / 100 1` | 400 | Correct use of rotation for walls and interior boxes |
| `3 / 1 2 / 1 2 / 1 1` | 1 | Off-by-one behavior when (H=S_i+1) |
| 250000 copies of `1 1` | 0 | Maximum input size and performance |

## Edge Cases

For the case with only one possible wall at a high level,

```
3
1 3
1 2
1 1
```

consider (H=3). Only the first box has (L_i\ge3), so the Li Chao query can return only one finite wall candidate. The implementation detects that the second minimum is `INF` and skips this height. At (H=2), two boxes become possible walls, but the first box contributes zero as a wall and the remaining configuration still gives no positive trapped area. The final answer is (0).

For the exact-boundary case,

```
3
1 2
1 2
1 1
```

at (H=2), the two (1\times2) boxes are inserted as walls. The (1\times1) box contributes (1(2-1)=1). The two wall candidates have raw contribution zero, so subtracting them leaves (1). The answer is exactly (1), showing why the contribution must be clamped at zero and why a box with (S_i=H) must not be treated as producing negative water.

For the rotation-sensitive case,

```
3
2 5
2 5
100 1
```

the normalized dimensions are ((5,2),(5,2),(100,1)). At (H=5), the first two boxes can be rotated so that their (5)-sides are vertical, giving two walls. The third box uses its (100)-side horizontally and its (1)-side vertically, contributing (100(5-1)=400). The Li Chao query removes the two wall candidates, and the computed answer is (400).

For equal dimensions,

```
3
2 2
2 2
2 2
```

every normalized box is ((2,2)). At (H=2), all contributions are zero. Above (2), there are no boxes with (L_i\ge H), so there cannot be two walls. Below (2), no box has a positive amount of space above it. The algorithm consequently returns (0).

The maximum-size case consists of (250000) boxes of size (1\times1). Every box has (L_i=S_i=1), so every candidate water contribution is zero and the answer is (0). The implementation still processes all boxes through the sorting and Li Chao machinery, exercising the intended (O(N\log N)) behavior without relying on small input sizes.
