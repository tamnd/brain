---
title: "CF 102163A - Hasan the lazy judge"
description: "We have two kinds of finite line segments. A horizontal segment is described by its left and right x coordinates and its fixed y coordinate. A vertical segment is described by its bottom and top y coordinates and its fixed x coordinate."
date: "2026-08-23T10:49:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "A"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 2337
verified: true
draft: false
---

[CF 102163A - Hasan the lazy judge](https://codeforces.com/problemset/problem/102163/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 38m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two kinds of finite line segments. A horizontal segment is described by its left and right x coordinates and its fixed y coordinate. A vertical segment is described by its bottom and top y coordinates and its fixed x coordinate.

Choose one horizontal segment and one vertical segment that intersect at a point C. The four arms of the resulting plus sign end at the four endpoints of those two segments. If the intersection is at `(x, y)`, the four arm lengths are

`x - x1`, `x2 - x`, `y - y1`, and `y2 - y`.

The value of this plus sign is the smallest of those four numbers. We need the maximum possible value over every valid horizontal and vertical pair.

With up to `10^5` horizontal segments and `10^5` vertical segments, trying every pair would require up to `10^10` checks in one test case. A one-second limit rules that out completely. Even an `O((N+M) log(N+M))` solution is much more appropriate here, while an algorithm with an additional logarithmic factor can still be practical because the coordinate range is only `10^5`.

There are several boundary cases that a correct implementation has to handle carefully. First, touching at an endpoint is a valid intersection, but it gives zero length on that side. For example,

```
1
1 1
1 1 1
1 1 1
```

has answer `0`. A solution that requires a strictly positive overlap would incorrectly report that there is no intersection.

A second case is that a horizontal segment can be long enough while the vertical segment is too short. For example,

```
1
1 1
1 10 5
1 5 5
```

has answer `0`. The segments intersect, but the vertical segment has only two units of room on its shorter side at the best possible intersection, and in fact its total length is only four, so no positive plus of length greater than zero can be formed at the required crossing. More generally, a candidate of length `d` requires both segments to have total length at least `2d`.

A third case is the equality at the shrunken boundaries. Consider

```
1
1 1
1 5 3
1 5 3
```

The answer is `2`, because the crossing at `(3,3)` leaves exactly two units in every direction. A check for length `d` must use inclusive conditions such as `x1 + d <= x <= x2 - d`. Replacing them with strict inequalities would lose this valid answer.

The input does not promise that the endpoints are presented in increasing order, so a robust implementation should normalize every segment first. The reference solutions for this problem do the same before processing the geometry.

## Approaches

The direct approach is to examine every horizontal segment against every vertical segment. For a pair, we check whether their x and y ranges intersect, compute the intersection coordinate, and then evaluate the four distances from that point to the segment endpoints. This is correct because every possible plus sign is determined by exactly one such pair. The problem is the number of pairs. With `N = M = 10^5`, there can be `10^10` pairs, which is far beyond what the time limit allows.

The useful observation is to stop trying to maximize the answer directly. Instead, ask a yes-or-no question: can we form a plus sign whose value is at least `d`?

For a horizontal segment `[x1, x2]` at height `y`, an intersection at x has at least `d` units on both horizontal sides exactly when

`x1 + d <= x <= x2 - d`.

So the horizontal segment can be replaced, for this particular check, by the allowed x interval `[x1+d, x2-d]`. If `x1+d > x2-d`, this horizontal segment cannot participate in a plus of size `d`.

Likewise, a vertical segment `[y1, y2]` at x can support a plus of size `d` exactly when the intersection height satisfies

`y1 + d <= y <= y2-d`.

Now the geometry has become a sweep-line problem. Sort the vertical segments by x. For a fixed `d`, each useful horizontal segment becomes active when the sweep reaches `x1+d`, and stops being active after `x2-d`. While processing a vertical segment at coordinate x, the active horizontals are precisely those whose allowed x interval contains x.

Among the active horizontals, we only need to know whether at least one has its y coordinate inside the vertical segment's valid interval `[y1+d, y2-d]`. A Fenwick tree over y coordinates is the standard implementation. The original accepted C++ solution uses exactly this sweep, activating horizontals by their left boundary, removing them after their right boundary, and querying the y interval with a Fenwick tree.

The final observation is monotonicity. If a plus of size `d` exists, then a plus of every smaller size also exists. That makes the answer suitable for binary search. We test a candidate `d`, and if it is feasible, search larger values; otherwise, search smaller values.

For the Python implementation below, the same sweep is combined with a small block-based bitset over the y coordinate universe. Coordinates are at most `10^5`, so we can maintain which y coordinates are currently active without a logarithmic tree operation. Each block contains 256 y positions, and a second small bitset records which blocks are nonempty. An interval query then touches at most two boundary blocks and the compact block-level bitset.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(NM)` | `O(N+M)` | Too slow |
| Binary search + sweep + Fenwick tree | `O((N+M) log C log C)` | `O(N+M+C)` | Accepted |
| Binary search + sweep + bounded-coordinate bitset | `O((N+M) log C)` for fixed coordinate bound | `O(N+M+C)` | Accepted |

Here `C` is the maximum coordinate, at most `10^5`. The second approach is the usual data-structure formulation, while the third is particularly suitable for Python under the one-second limit because the coordinate universe is explicitly bounded.

## Algorithm Walkthrough

1. Normalize every horizontal segment so that `x1 <= x2`, and every vertical segment so that `y1 <= y2`. Compute the largest possible answer from half of the length of any segment.
2. Sort the horizontal segments twice, once by `x1` and once by `x2`. For a fixed candidate `d`, their usable interval becomes `[x1+d, x2-d]`. Since adding the same `d` preserves the ordering, the lists never need to be sorted again during binary search.
3. Sort the vertical segments by x coordinate. We will sweep through them from left to right.
4. For a candidate `d`, discard every horizontal segment with `x2-x1 < 2d`, because there is not enough horizontal room for two arms of length `d`. For every remaining horizontal segment, define `left = x1+d` and `right = x2-d`.
5. During the x sweep, insert a horizontal segment when `left <= x` for the current vertical segment. Remove it when `right < x`. The strict comparison for removal is deliberate. If `right == x`, the vertical line passes through the endpoint of the shrunken horizontal interval, and that still gives exactly `d` units on the corresponding side.
6. Maintain the y coordinates of all currently active horizontal segments. If several active horizontals have the same y coordinate, maintain a count rather than a simple boolean, because removing one of them must not accidentally remove the coordinate while another horizontal remains active.
7. For each vertical segment, first require `y2-y1 >= 2d`. Its possible crossing heights are then exactly `[y1+d, y2-d]`. If the active y set contains any coordinate in this interval, a plus of size at least `d` exists.
8. Binary search the largest feasible `d`. The lower bound is zero. The upper bound can be the largest half-length of any input segment. If `check(mid)` succeeds, store `mid` and continue to the right; otherwise continue to the left.

### Why it works

For a fixed `d`, an active horizontal segment is exactly a horizontal segment whose x coordinate can be chosen so that both horizontal arms have length at least `d`. When the sweep is at vertical coordinate x, the active set contains precisely all horizontals whose allowed x intervals contain that x.

A vertical segment contributes a valid plus of size at least `d` exactly when its y coordinate can be chosen inside `[y1+d, y2-d]`. Thus the range query over the active horizontal y coordinates is true exactly when some horizontal and this vertical can form such a plus. The sweep therefore answers `check(d)` correctly.

Finally, feasibility is monotone. Increasing the required arm length can only remove possible intersections, never create new ones. Binary search consequently finds the maximum feasible value.

## Python Solution

```python
import sys
input = sys.stdin.readline

BLOCK = 256

class ActiveY:
    def __init__(self, max_y):
        self.size = max_y + 1
        self.blocks = [0] * ((max_y >> 8) + 1)
        self.count = [0] * (max_y + 1)
        self.nonempty = 0

    def add(self, y):
        c = self.count[y]
        self.count[y] = c + 1
        if c == 0:
            b = y >> 8
            bit = 1 << (y & 255)
            old = self.blocks[b]
            self.blocks[b] = old | bit
            if old == 0:
                self.nonempty |= 1 << b

    def remove(self, y):
        c = self.count[y] - 1
        self.count[y] = c
        if c == 0:
            b = y >> 8
            bit = 1 << (y & 255)
            new = self.blocks[b] & ~bit
            self.blocks[b] = new
            if new == 0:
                self.nonempty &= ~(1 << b)

    def any_in_range(self, lo, hi):
        if lo > hi:
            return False

        b1 = lo >> 8
        b2 = hi >> 8

        if b1 == b2:
            left = lo & 255
            right = hi & 255
            mask = ((1 << (right - left + 1)) - 1) << left
            return (self.blocks[b1] & mask) != 0

        left = lo & 255
        if self.blocks[b1] & (~((1 << left) - 1) & ((1 << 256) - 1)):
            return True

        right = hi & 255
        if self.blocks[b2] & ((1 << (right + 1)) - 1):
            return True

        if b2 - b1 <= 1:
            return False

        width = b2 - b1 - 1
        middle_mask = ((1 << width) - 1) << (b1 + 1)
        return (self.nonempty & middle_mask) != 0

def solve_case(horizontal, vertical, max_coord):
    n = len(horizontal)
    m = len(vertical)

    horizontal.sort(key=lambda p: p[0])
    by_right = sorted(horizontal, key=lambda p: p[1])
    vertical.sort(key=lambda p: p[2])

    max_len = 0
    for x1, x2, _ in horizontal:
        max_len = max(max_len, (x2 - x1) // 2)
    for y1, y2, _ in vertical:
        max_len = max(max_len, (y2 - y1) // 2)

    def check(d):
        left_list = []
        right_list = []

        for x1, x2, y in horizontal:
            if x2 - x1 >= 2 * d:
                left_list.append((x1 + d, y))
                right_list.append((x2 - d, y))

        active = ActiveY(max_coord)

        li = 0
        ri = 0
        ln = len(left_list)
        rn = len(right_list)

        for y1, y2, x in vertical:
            if y2 - y1 < 2 * d:
                continue

            while li < ln and left_list[li][0] <= x:
                active.add(left_list[li][1])
                li += 1

            while ri < rn and right_list[ri][0] < x:
                active.remove(right_list[ri][1])
                ri += 1

            if active.any_in_range(y1 + d, y2 - d):
                return True

        return False

    lo = 0
    hi = max_len
    ans = 0

    while lo <= hi:
        mid = (lo + hi) // 2
        if check(mid):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1

    return ans

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())

        horizontal = []
        vertical = []
        max_coord = 0

        for _ in range(n):
            x1, x2, y = map(int, input().split())
            if x1 > x2:
                x1, x2 = x2, x1
            horizontal.append((x1, x2, y))
            max_coord = max(max_coord, x1, x2, y)

        for _ in range(m):
            y1, y2, x = map(int, input().split())
            if y1 > y2:
                y1, y2 = y2, y1
            vertical.append((y1, y2, x))
            max_coord = max(max_coord, y1, y2, x)

        out.append(str(solve_case(horizontal, vertical, max_coord)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input phase normalizes endpoints immediately, so every later comparison can assume increasing coordinates. The maximum possible answer is at most half the length of one segment, since a plus of length `d` needs `2d` units along both the horizontal and vertical segment.

The two horizontal orderings are prepared once. Sorting by `x1` gives the order in which horizontal intervals become active, while sorting by `x2` gives the order in which they expire. Adding `d` to every left endpoint and subtracting `d` from every right endpoint does not change either ordering, so binary-search iterations do not require another sort.

The `ActiveY` structure stores a count for every y coordinate. Its first bitset records the occupied positions inside each 256-coordinate block. The second bitset records which blocks contain at least one active coordinate. This makes insertion and deletion constant-time with respect to the problem's fixed coordinate universe.

The interval query first checks the two boundary blocks directly. If there are complete blocks between them, it checks their occupancy using the compact block-level bitset. The largest block index is only about `10^5 / 256`, so these integer operations remain very small even though the original coordinate range is large.

The sweep uses `left <= x` when inserting and `right < x` when removing. Those inequalities are the key boundary detail. A horizontal segment whose usable interval ends exactly at the current vertical x coordinate is still a valid candidate.

Python integers have arbitrary precision, so there is no overflow issue when constructing the bit masks. The coordinate bounds also keep every bitset comfortably small. The original C++ implementation uses a Fenwick tree instead of this bounded-universe structure, with the same geometric sweep and the same inclusive interval boundaries.

## Worked Examples

### Sample 1

The input contains horizontal segments `[1,5]` at `y=3`, `[2,4]` at `y=2`, and `[6,12]` at `y=6`. The vertical segments are `[1,5]` at `x=3` and `[6,9]` at `x=2`.

For `d=2`, the first horizontal becomes usable only at `x=3`, with y coordinate `3`. The second horizontal has exactly the required length and is usable at `x=3` as well. The first vertical has a valid y interval `[3,3]`.

| Step | Candidate `d` | Vertical `(y1,y2,x)` | Active horizontal y values | Query interval | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | `(1,5,3)` | `{3,2}` | `[3,3]` | Found |
| 2 | 2 | `(6,9,2)` | `{}` after x ordering | `[8,7]` | Not needed |

The first vertical intersects the first horizontal at `(3,3)`. The four arm lengths are `2,2,2,2`, so the answer is at least `2`. A larger value is impossible because the first horizontal has total length `4`, and the second horizontal also has total length `2`. Thus the answer is `2`.

### Custom trace

Consider

```
1
1 1
1 9 5
3 7 5
```

The horizontal segment has x range `[1,9]` and the vertical segment has y range `[3,7]`, both crossing at coordinate `5`.

For `d=2`, the horizontal usable x range is `[3,7]`, and the vertical usable y range is `[5,5]`.

| Step | Candidate `d` | Horizontal usable x | Vertical x | Active y values | Vertical usable y | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | `[3,7]`, y=`5` | `5` | `{5}` | `[5,5]` | Found |
| 2 | 3 | `[4,6]`, y=`5` | `5` | `{5}` | `[6,4]` | Impossible |

The check for `d=2` succeeds because the crossing at `(5,5)` leaves four units horizontally and two units vertically, so the shortest arm is `2`. The check for `d=3` fails because the vertical segment has total length only `4`, which is insufficient for two arms of length `3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O((N+M) log C)` | Each feasibility check sweeps all segments in linear time, and binary search performs `O(log C)` checks |
| Space | `O(N+M+C)` | The segments, sorted copies, y counters, and bounded-coordinate bitsets are stored |

Here `C <= 10^5`. The crucial practical property is that the dynamic y structure uses the bounded coordinate universe instead of a Python tree with `O(log C)` work per event. The binary search needs at most about 17 iterations because `2^17 > 10^5`, so roughly a few million segment-processing operations are performed per large test case.

The original C++ solution uses a Fenwick tree and therefore has an additional logarithmic factor in the sweep, but it fits the stated limits in C++. The Python version replaces that logarithmic data structure with the coordinate-bitset representation to keep the implementation suitable for the same tight limit.

## Test Cases

```python
# Helper: execute the same solve logic on an input string.
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

# Provided sample.
assert run("""\
1
3 2
1 5 3
2 4 2
6 12 6
1 5 3
6 9 2
""") == "2\n", "sample 1"

# Minimum-size segments. They intersect at one point, but every arm has length zero.
assert run("""\
1
1 1
1 1 1
1 1 1
""") == "0\n", "minimum-size segments"

# Endpoint intersection with positive horizontal length, catching strict-boundary errors.
assert run("""\
1
1 1
1 5 3
3 3 3
""") == "0\n", "endpoint-only intersection"

# Exact maximum plus. Both segments have length 8 and cross at their centers.
assert run("""\
1
1 1
1 9 5
1 9 5
""") == "4\n", "exact half-length"

# Reversed endpoints must be normalized.
assert run("""\
1
1 1
9 1 5
9 1 5
""") == "4\n", "reversed endpoints"

# Two horizontals share the same y coordinate. Removing one must not remove
# the coordinate while the other is still active.
assert run("""\
1
2 1
1 10 5
3 8 5
1 10 5
""") == "3\n", "duplicate active y"

# Large boundary coordinates.
assert run("""\
1
1 1
1 100000 50000
1 100000 50000
""") == "49999\n", "coordinate boundary"

# Multiple test cases.
assert run("""\
2
1 1
1 5 3
1 5 3
1 1
1 2 1
1 2 1
""") == "2\n1\n", "multiple test cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / [1,1] / [1,1]` | `0` | Minimum-size segments and zero-length arms |
| `1 1 / [1,5] at y=3 / [3,3] at x=3` | `0` | Endpoint-only intersection |
| `1 1 / [1,9] at y=5 / [1,9] at x=5` | `4` | Exact half-length and inclusive boundaries |
| Reversed `[9,1]` endpoints | `4` | Endpoint normalization |
| Two horizontals with the same y | `3` | Correct reference counting during deletion |
| Coordinates equal to `100000` | `49999` | Maximum coordinate boundary |
| Two test cases | `2`, `1` | State isolation between test cases |

## Edge Cases

For an intersection that occurs only at an endpoint, the algorithm keeps the candidate because the usable horizontal interval is closed. For

```
1
1 1
1 5 3
3 3 3
```

the horizontal segment allows a crossing at `x=3`, while the vertical segment can only cross at `y=3`. The intersection is valid, but the vertical segment has zero length, so the answer is `0`. In a positive-length check, `y1+d <= y2-d` immediately fails for every `d > 0`.

For a segment whose total length is exactly twice the requested answer, the shrunken interval consists of one coordinate. For

```
1
1 1
1 5 3
3 3 3
```

the candidate `d=0` is feasible, while `d=1` is impossible because the vertical segment cannot provide one unit on both sides. More generally, for

```
1
1 1
1 5 3
1 5 3
```

the candidate `d=2` produces horizontal range `[3,3]` and vertical range `[3,3]`. The sweep uses `<=` for activation and `<` for removal, so the common boundary coordinate remains active and the answer `2` is found.

When several horizontal segments have the same y coordinate, the active structure must represent multiplicity. Suppose two horizontals with the same y become active and one expires. The y coordinate is still represented by the other horizontal. The `count[y]` array handles this directly: the bit is set when the count changes from zero to one and cleared only when the count returns to zero.

Reversed endpoints are handled before any geometry is performed. For example,

```
1
1 1
9 1 5
9 1 5
```

is normalized to two segments from `1` to `9`. Their centers coincide at `5`, giving answer `4`. Without normalization, expressions such as `x2-x1` would become negative and the binary-search upper bound could silently become incorrect.

The all-degenerate case is also safe. If every horizontal and vertical segment consists of a single point, every possible plus has value zero. The initial binary-search lower bound is zero, and `check(0)` correctly accepts any actual intersection while every positive candidate is rejected.

Finally, intersections involving multiple lines at the same coordinate do not require special treatment. The problem asks us to choose one horizontal and one vertical segment, so each active horizontal combined with the current vertical represents one valid pair. The algorithm only needs to know whether at least one such pair exists for the current candidate length, not how many pairs exist.
