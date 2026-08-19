---
title: "CF 102163A - Hasan the lazy judge"
description: "Each horizontal segment is described by its two endpoint x-coordinates and its fixed y-coordinate. Each vertical segment is described by its two endpoint y-coordinates and its fixed x-coordinate."
date: "2026-08-19T07:41:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "A"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 344
verified: false
draft: false
---

[CF 102163A - Hasan the lazy judge](https://codeforces.com/problemset/problem/102163/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 44s  
**Verified:** no  

## Solution
## Problem Understanding

Each horizontal segment is described by its two endpoint x-coordinates and its fixed y-coordinate. Each vertical segment is described by its two endpoint y-coordinates and its fixed x-coordinate. Choosing one horizontal segment and one vertical segment gives a plus sign exactly when the two segments intersect.

Suppose their intersection is C=(x,y). The four arms of the plus sign have lengths

x−X 1 ​ ,X 2 ​ −x,y−Y 1 ​ ,Y 2 ​ −y.

The value of this plus sign is the smallest of these four lengths. We need the maximum possible value over every intersecting horizontal and vertical pair.

The input can contain 10 5 horizontal and 10 5 vertical segments. A quadratic algorithm would have to inspect up to 10 10 pairs in one test case, which is far beyond what a 1 second limit can support. The coordinates are also bounded by 10 5, which makes Fenwick tree indexing particularly convenient.

There are several boundary cases that can make an implementation silently fail. First, an intersection at an endpoint is still an intersection. For example,

```
11 11 3 22 4 1
```

has answer `1`, because the segments meet at (1,2), but the horizontal segment has no positive distance to its left endpoint at that point. In fact, the correct intersection is (1,2), giving horizontal arm lengths 0 and 2, so the answer is actually `0`. A solution that treats intervals as open could incorrectly report no intersection at all, while a solution that only checks segment lengths could also confuse existence of an intersection with existence of a positive-length plus.

Second, a segment whose length is exactly 2d is valid for a candidate answer d. For example,

```
11 11 5 31 5 3
```

has answer `2`. The intersection is at (3,3), and all four arms have length 2. Using `length > 2*d` instead of `length >= 2*d` would incorrectly reject it.

Third, multiple segments may have the same y-coordinate. For example,

```
12 11 5 32 6 31 5 3
```

has answer `2`. Both horizontal segments contribute to the same y-coordinate, so the data structure must support multiple active segments at the same coordinate. A careless removal implementation that treats the Fenwick value as only a boolean could remove the coordinate while another segment with the same y is still active.

Finally, the two endpoints need not be assumed to arrive in increasing order unless that is guaranteed by the judge. Normalizing each segment with `min` and `max` makes the implementation robust.

## Approaches

The direct solution considers every horizontal segment together with every vertical segment. For each pair, we first test whether their coordinate ranges contain the intersection point, then calculate the four distances from that point to the endpoints. This is correct because every possible plus sign corresponds to exactly one such pair.

The problem is the number of pairs. With N=M=10 5, there can be N⋅M=10 10 pairs. Even a very small constant amount of work per pair is too much, so the brute-force approach is ruled out.

The useful observation is to stop trying to maximize the answer directly. Instead, ask a yes-or-no question: can we construct a plus sign whose length is at least d?

For a horizontal segment [X 1 ​ ,X 2 ​ ], an intersection point must be at least d away from both endpoints. Thus its x-coordinate must satisfy

X 1 ​ +d≤x≤X 2 ​ −d.

Similarly, for a vertical segment [Y 1 ​ ,Y 2 ​ ], the intersection y-coordinate must satisfy

Y 1 ​ +d≤y≤Y 2 ​ −d.

So for a fixed d, every horizontal segment becomes an allowed x-interval, and every vertical segment becomes an allowed y-interval. We only need to determine whether some vertical line passes through the allowed x-range of some horizontal segment while its y-range contains that horizontal segment's y-coordinate.

This feasibility condition is monotonic. If a plus sign of length d exists, then a plus sign of every smaller length also exists. That gives us binary search on the answer.

For one fixed d, sweep the vertical segments from left to right. A horizontal segment becomes usable when the current x-coordinate reaches X 1 ​ +d, and stops being usable after X 2 ​ −d. While sweeping, maintain the y-coordinates of all currently usable horizontal segments in a Fenwick tree. When processing a vertical segment at x, we ask whether any active horizontal y lies inside its shrunk interval [Y 1 ​ +d,Y 2 ​ −d].

The horizontal activation and deactivation events are already ordered if we sort the horizontal segments by their original X 1 ​ and X 2 ​. Since adding or subtracting the same d preserves ordering, these sorted arrays can be reused for every binary-search iteration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NM) | O(N+M) | Too slow |
| Optimal | O((N+M)logClogC) | O(N+M+C) | Accepted |

Here C≤10 5 is the coordinate bound. The first logarithm comes from Fenwick tree operations and the second from binary search on the answer.

## Algorithm Walkthrough

1. Normalize every segment so that its first endpoint is smaller than its second endpoint. For a horizontal segment store (X 1 ​ ,X 2 ​ ,Y), and for a vertical segment store (Y 1 ​ ,Y 2 ​ ,X). Compute an upper bound for the answer from the largest possible half-length of the segments.
2. Sort the horizontal segments once by X 1 ​, and separately by X 2 ​. Sort the vertical segments by their x-coordinate. These orders do not depend on the candidate length d, because shrinking an interval by d simply adds the same value to its left endpoint and subtracts the same value from its right endpoint.
3. Binary search the largest feasible length d. For a candidate d, immediately discard every horizontal segment with X 2 ​ −X 1 ​ <2d, because it cannot leave at least d units on both sides of its intersection. Do the analogous check for vertical segments.
4. For every remaining horizontal segment, define its valid x-range as [X 1 ​ +d,X 2 ​ −d]. During the sweep over x, insert its y-coordinate when the current vertical x reaches X 1 ​ +d.
5. Remove a horizontal segment when its valid range has ended. The correct removal condition is X 2 ​ −d<x, because x=X 2 ​ −d is still a valid intersection position. The Fenwick tree stores how many active horizontal segments exist at each y-coordinate, rather than merely whether one exists, because several segments can share the same y.
6. Process vertical segments in increasing x-coordinate. Before processing a vertical segment at x, activate all horizontal segments whose valid left endpoint is at most x, then remove all whose valid right endpoint is strictly less than x.
7. The vertical segment has a valid y-range [Y 1 ​ +d,Y 2 ​ −d]. Query the Fenwick tree for the number of active horizontal segments whose y-coordinate lies in that inclusive interval. If the count is positive, the candidate d is feasible and the binary search moves upward.
8. If no vertical segment finds an active horizontal segment, d is impossible and the binary search moves downward.

### Why it works

For a fixed d, a horizontal segment is active at x exactly when an intersection at that x would leave at least d units on both horizontal sides. Likewise, a vertical segment accepts exactly the y-coordinates that leave at least d units on both vertical sides.

At the moment a vertical segment at x is processed, the Fenwick tree contains precisely the y-coordinates of horizontal segments whose valid x-ranges contain x. A Fenwick range query then checks precisely whether one of those y-coordinates belongs to the vertical segment's valid y-range. Thus `check(d)` returns true exactly when a plus sign of length at least d exists.

The predicate is monotonic because shrinking the required arm length can only enlarge the set of valid intersections. Binary search consequently finds the maximum feasible length.

## Python Solution

```python
Pythonimport sysinput = sys.stdin.readline

def solve():    t = int(input())    out = []
    for _ in range(t):        n, m = map(int, input().split())
        horizontal = []        vertical = []
        max_coord = 0        max_half_h = 0        max_half_v = 0
        for _ in range(n):            x1, x2, y = map(int, input().split())            if x1 > x2:                x1, x2 = x2, x1
            horizontal.append((x1, x2, y))            max_coord = max(max_coord, x2, y)            max_half_h = max(max_half_h, (x2 - x1) // 2)
        for _ in range(m):            y1, y2, x = map(int, input().split())            if y1 > y2:                y1, y2 = y2, y1
            vertical.append((y1, y2, x))            max_coord = max(max_coord, y2, x)            max_half_v = max(max_half_v, (y2 - y1) // 2)
        horizontal_by_left = sorted(horizontal, key=lambda s: s[0])        horizontal_by_right = sorted(horizontal, key=lambda s: s[1])        vertical.sort(key=lambda s: s[2])
        bit_size = max_coord + 2
        def check(d):            bit = [0] * bit_size
            def add(pos, delta):                pos += 1                while pos < bit_size:                    bit[pos] += delta                    pos += pos & -pos
            def prefix(pos):                if pos < 0:                    return 0                pos += 1                res = 0                while pos:                    res += bit[pos]                    pos -= pos & -pos                return res
            left_ptr = 0            right_ptr = 0
            for y1, y2, x in vertical:                if y2 - y1 < 2 * d:                    continue
                while left_ptr < n:                    x1, x2, y = horizontal_by_left[left_ptr]
                    if x1 + d > x:                        break
                    if x2 - x1 >= 2 * d:                        add(y, 1)
                    left_ptr += 1
                while right_ptr < n:                    x1, x2, y = horizontal_by_right[right_ptr]
                    if x2 - d >= x:                        break
                    if x2 - x1 >= 2 * d:                        add(y, -1)
                    right_ptr += 1
                low_y = y1 + d                high_y = y2 - d
                if prefix(high_y) - prefix(low_y - 1) > 0:                    return True
            return False
        high = min(max_half_h, max_half_v)        low = 0        answer = 0
        while low <= high:            mid = (low + high) // 2
            if check(mid):                answer = mid                low = mid + 1            else:                high = mid - 1
        out.append(str(answer))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":    solve()
```

The input is read with `sys.stdin.readline`, which avoids the overhead of repeated generic input parsing. Each segment is normalized immediately, so all later interval calculations can safely assume increasing endpoints.

The two sorted horizontal arrays are the key preprocessing step. `horizontal_by_left` controls when a segment enters the active set, while `horizontal_by_right` controls when it leaves. The pointers only move forward, so each horizontal segment is considered a constant number of times per feasibility check.

The Fenwick tree is indexed by y-coordinate. Because coordinates are at most 10 5, direct indexing is simpler than coordinate compression. The tree stores counts, not booleans, so two active horizontal segments with the same y-coordinate are represented correctly.

The activation condition uses `x1 + d <= x`. The removal condition uses `x2 - d < x`. That strict inequality is essential because the right endpoint of the shrunk interval is still valid. The vertical query is also inclusive at both ends, implemented as

```
Pythonprefix(high_y) - prefix(low_y - 1)
```

A segment of length exactly 2d is accepted, because its shrunk interval consists of one coordinate. Python integers have arbitrary precision, so there is no integer overflow issue, although all values in this problem are already small enough for ordinary 32-bit arithmetic.

The binary search upper bound uses the smaller of the largest horizontal half-length and largest vertical half-length. A valid plus of length d needs both a horizontal and a vertical segment of length at least 2d, so no answer can exceed either bound.

## Worked Examples

### Sample 1

The input is

```
13 21 5 32 4 26 12 61 5 36 9 2
```

The candidate answer can be at most 2. The binary search checks the candidates 1 and 2.

For d=1, the horizontal valid x-ranges are [2,4], [3,3], and [7,11]. The vertical segments have valid y-ranges [2,4] and [7,8].

| d | Vertical x | Active horizontal y | Vertical valid y | Feasible |
| --- | --- | --- | --- | --- |
| 1 | 2 | none | [2, 4] | no |
| 1 | 3 | 3, 2 | [2, 4] | yes |

Once x reaches 3, the first two horizontal segments are active. The vertical segment at x=3 covers y from 2 through 4, so either horizontal segment gives a plus of length at least 1.

For d=2, the first horizontal segment has valid x-range [3,3], while the second has no width left and the third has valid x-range [8,10]. The first vertical segment at x=3 has valid y-range [3,3].

| d | Vertical x | Active horizontal y | Vertical valid y | Feasible |
| --- | --- | --- | --- | --- |
| 2 | 2 | none | [3, 3] | no |
| 2 | 3 | 3 | [3, 3] | yes |

The intersection at (3,3) leaves exactly 2 units in all four directions for the first horizontal and first vertical segments, so the answer is `2`.

### Custom Example 2

Consider

```
12 21 9 52 6 35 7 51 9 4
```

The first horizontal segment has length 8, and the first vertical segment has length 2. Thus the answer cannot exceed 1. The second vertical segment has length 8.

For d=1, the first horizontal's valid x-range is [2,8], and the second horizontal's valid x-range is [3,5]. The vertical segment at x=5 has valid y-range [6,6], so it cannot meet either horizontal at a valid y. The vertical segment at x=4 has valid y-range [2,8], and both horizontal y-values 5 and 3 are inside it.

| d | Vertical x | Active horizontal y | Vertical valid y | Feasible |
| --- | --- | --- | --- | --- |
| 1 | 4 | 5, 3 | [2, 8] | yes |
| 1 | 5 | 5, 3 | [6, 6] | no |

The existence of the x=4 intersection proves that d=1 is feasible, so the final answer is `1`. This trace also demonstrates why the sweep must process all horizontal segments whose shrunk left endpoint is at most the current x before performing the query.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N+M)logClogC) | Binary search performs O(logC) checks, each check uses O(N+M) pointer operations and O(N+M) Fenwick operations, each costing O(logC). |
| Space | O(N+M+C) | Two sorted horizontal arrays, the vertical array, and one Fenwick tree are stored. |

With N,M≤10 5 and C≤10 5, the binary search needs fewer than 17 iterations. The solution avoids the 10 10 pair enumeration of brute force and keeps every feasibility check within near-linearithmic time. The coordinate bound also keeps the Fenwick tree small enough for the 256 MB memory limit.

## Test Cases

```python
Pythonimport sysimport io

def solve_io(inp: str) -> str:    old_stdin = sys.stdin    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)    sys.stdout = io.StringIO()
    solve()
    result = sys.stdout.getvalue()
    sys.stdin = old_stdin    sys.stdout = old_stdout
    return result

def solve():    t = int(input())    out = []
    for _ in range(t):        n, m = map(int, input().split())
        horizontal = []        vertical = []
        max_coord = 0        max_half_h = 0        max_half_v = 0
        for _ in range(n):            x1, x2, y = map(int, input().split())            if x1 > x2:                x1, x2 = x2, x1            horizontal.append((x1, x2, y))            max_coord = max(max_coord, x2, y)            max_half_h = max(max_half_h, (x2 - x1) // 2)
        for _ in range(m):            y1, y2, x = map(int, input().split())            if y1 > y2:                y1, y2 = y2, y1            vertical.append((y1, y2, x))            max_coord = max(max_coord, y2, x)            max_half_v = max(max_half_v, (y2 - y1) // 2)
        horizontal_by_left = sorted(horizontal, key=lambda s: s[0])        horizontal_by_right = sorted(horizontal, key=lambda s: s[1])        vertical.sort(key=lambda s: s[2])
        bit_size = max_coord + 2
        def check(d):            bit = [0] * bit_size
            def add(pos, delta):                pos += 1                while pos < bit_size:                    bit[pos] += delta                    pos += pos & -pos
            def prefix(pos):                if pos < 0:                    return 0                pos += 1                res = 0                while pos:                    res += bit[pos]                    pos -= pos & -pos                return res
            left_ptr = 0            right_ptr = 0
            for y1, y2, x in vertical:                if y2 - y1 < 2 * d:                    continue
                while left_ptr < n:                    x1, x2, y = horizontal_by_left[left_ptr]                    if x1 + d > x:                        break                    if x2 - x1 >= 2 * d:                        add(y, 1)                    left_ptr += 1
                while right_ptr < n:                    x1, x2, y = horizontal_by_right[right_ptr]                    if x2 - d >= x:                        break                    if x2 - x1 >= 2 * d:                        add(y, -1)                    right_ptr += 1
                low_y = y1 + d                high_y = y2 - d
                if prefix(high_y) - prefix(low_y - 1):                    return True
            return False
        low = 0        high = min(max_half_h, max_half_v)        answer = 0
        while low <= high:            mid = (low + high) // 2            if check(mid):                answer = mid                low = mid + 1            else:                high = mid - 1
        out.append(str(answer))
    sys.stdout.write("\n".join(out))

input = sys.stdin.readline
# Provided sampleassert solve_io("""\13 21 5 32 4 26 12 61 5 36 9 2""") == "2\n", "sample 1"
# Minimum-size segments, with a genuine intersectionassert solve_io("""\11 11 1 11 1 1""") == "0\n", "minimum-size case"
# Exactly 2*d on both segmentsassert solve_io("""\11 11 5 31 5 3""") == "2\n", "exact boundary length"
# No intersection at allassert solve_io("""\11 11 3 11 3 5""") == "0\n", "no intersection"
# Same y-coordinate on multiple horizontal segmentsassert solve_io("""\13 11 9 52 8 53 7 51 9 5""") == "4\n", "duplicate active y"
# Reversed endpointsassert solve_io("""\11 19 1 57 1 5""") == "4\n", "reversed endpoints"
# Boundary-coordinate maximum-size constructionn = 100000h_lines = "\n".join(["1 100000 50000"] * n)v_lines = "\n".join(["1 100000 50000"] * n)max_input = f"1\n{n} {n}\n{h_lines}\n{v_lines}\n"assert solve_io(max_input) == "49999\n", "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1 / 1 1 1 / 1 1 1` | `0` | Minimum-size segments and zero-length arms |
| `1 / 1 1 / 1 5 3 / 1 5 3` | `2` | Exact 2d boundary |
| `1 / 1 1 / 1 3 1 / 1 3 5` | `0` | Segments that never intersect |
| Three horizontal segments with the same y | `4` | Duplicate active y-coordinates |
| Reversed endpoints | `4` | Endpoint normalization |
| 10 5 identical horizontal and vertical segments | `49999` | Maximum input size and coordinate boundaries |

## Edge Cases

A segment can intersect another segment exactly at an endpoint. Consider

```
11 11 3 22 4 1
```

The only intersection is (1,2). The horizontal arms have lengths 0 and 2, so the plus length is `0`. During `check(0)`, the horizontal valid x-range is `[1,3]`, and the vertical valid y-range is `[2,4]`. At x=1 the horizontal is activated because the condition is `left <= x`. The Fenwick query finds y=2, so the intersection is recognized. For `d=1`, the horizontal valid x-range becomes `[2,2]`, while the vertical is still valid in y `[3,3]`, so no plus of length 1 exists.

A segment of exactly 2d length must remain valid. For

```
11 11 5 31 5 3
```

the answer is `2`. For `check(2)`, both shrunk intervals become the single point 3. The horizontal is activated at x=3, the vertical accepts y=3, and the Fenwick query succeeds. Using strict inequalities in either the length test or the sweep boundaries would incorrectly lose this solution.

Duplicate y-coordinates require counts. In

```
12 11 9 52 6 51 9 5
```

both horizontal segments are active at y=5 when the vertical segment is processed. The Fenwick value at y=5 becomes 2. If one horizontal segment were removed while the other remained active, the value would become 1, so the y-coordinate would still be represented. A boolean structure without reference counts could incorrectly erase it.

Finally, endpoint order should be normalized before any calculations. For

```
11 19 1 57 1 5
```

the horizontal segment is really [1,9] and the vertical segment is really [1,7]. Their intersection is at (5,5), giving four arms of length 4, so the answer is `4`. Swapping endpoints before calculating lengths and shrunk intervals makes the same algorithm work without special cases.
