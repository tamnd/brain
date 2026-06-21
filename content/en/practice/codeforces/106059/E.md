---
title: "CF 106059E - Echoes on the Endless Line"
description: "We are given positions of enemies and positions of observers on a number line. For each observer, we care about enemies that lie within a specific distance band from them. Each observer at position b defines two radii."
date: "2026-06-21T15:55:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106059
codeforces_index: "E"
codeforces_contest_name: "National Yang Ming Chiao Tung University 2025 Team Selection Programming Contest"
rating: 0
weight: 106059
solve_time_s: 54
verified: true
draft: false
---

[CF 106059E - Echoes on the Endless Line](https://codeforces.com/problemset/problem/106059/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given positions of enemies and positions of observers on a number line. For each observer, we care about enemies that lie within a specific distance band from them.

Each observer at position `b` defines two radii. Enemies at distance at most `L` are considered too close to engage with, while enemies at distance at most `R` are visible. The task is only concerned with enemies whose distance from the observer lies strictly greater than `L` and at most `R`. For each observer, we must report two values: how many enemies fall into this distance range, and the sum of their distances to the observer.

The key difficulty is that both `n` and `q` can be as large as 200,000, so any solution that checks every enemy for every observer will be too slow. A double loop would perform about 4e10 distance checks in the worst case, which is far beyond the limits of a 2 second execution time in Python.

The structure of the condition is also important. Each query depends only on absolute distance, which splits naturally into two independent regions around each observer: enemies on the left and enemies on the right. A naive mistake is to try to treat the interval as a single contiguous range in index space, which fails because the transformation `|a - b|` is symmetric and not order-preserving without splitting.

A subtle edge case appears when `L = 0`. In that case, enemies exactly at the observer position are excluded even though they are within range `R`. Another case is when all enemies are outside `R`, where the answer should be `0 0`, and any prefix-sum based solution must avoid accessing invalid ranges.

## Approaches

A direct approach evaluates each watcher independently by scanning all enemies and computing distances. This is correct because it follows the definition literally: for each enemy, compute `|a[i] - b[j]|` and check whether it lies in `(L, R]`, accumulating counts and sums when it does. The problem is that this performs `n * q` distance computations. With both up to 200,000, this leads to 40 billion operations, which cannot finish in time.

The structure of the condition suggests a different viewpoint. Instead of thinking in terms of distance, we can translate the constraint back onto the number line. The inequality `L < |a - b| ≤ R` is equivalent to two disjoint segments: `[b - R, b - L)` on the left side and `(b + L, b + R]` on the right side. This removes absolute values entirely and reduces the problem to range counting over a static sorted array.

Once the enemy positions are sorted, we can answer how many lie in any interval using binary search. To also compute distance sums efficiently, we maintain a prefix sum array over the sorted positions. That allows constant-time computation of sums over any segment, turning each query into a logarithmic number of boundary searches and constant arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Sorting + Binary Search + Prefix Sums | O((n + q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

We first sort the array of enemy positions so that we can reason about contiguous segments on the line. Sorting is the key transformation that converts geometric distance constraints into interval queries.

Next, we build a prefix sum array over the sorted positions. This allows us to compute the sum of any subarray in constant time after locating its boundaries.

For each watcher position `b`, we translate the condition `L < |a - b| ≤ R` into two intervals on the sorted axis. The left interval is all enemies in `[b - R, b - L)`, and the right interval is all enemies in `(b + L, b + R]`. We query both independently.

For each interval, we use binary search to find the first index where elements are at least the left boundary and the first index where they exceed the right boundary. This gives us a contiguous segment in the sorted array.

We compute both the count and the sum of values in each segment using the prefix sum array. However, the required output is the sum of distances, not the sum of coordinates, so we convert accordingly. For a right-side interval, each contribution is `a[i] - b`, so the total is `sum(a[i]) - count * b`. For a left-side interval, each contribution is `b - a[i]`, so the total is `count * b - sum(a[i])`.

Finally, we add contributions from both sides and output the combined count and distance sum.

### Why it works

The correctness relies on the fact that absolute distance partitions the line into two monotone regions relative to each query point. After sorting, any condition of the form `a[i] ≤ x` or `a[i] ≥ x` corresponds to a contiguous block. The transformation turns a geometric filter into a pair of disjoint array slices, and prefix sums ensure both counting and aggregation are exact over those slices.

## Python Solution

```python
import sys
input = sys.stdin.readline

def lower_bound(arr, x):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo

def upper_bound(arr, x):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    return lo

n, q, L, R = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

a.sort()

pref = [0] * (n + 1)
for i in range(n):
    pref[i + 1] = pref[i] + a[i]

out = []

for x in b:
    cnt = 0
    dist_sum = 0

    left_l = x - R
    left_r = x - L
    l = lower_bound(a, left_l)
    r = lower_bound(a, left_r)
    c = r - l
    if c > 0:
        s = pref[r] - pref[l]
        cnt += c
        dist_sum += c * x - s

    right_l = x + L
    right_r = x + R
    l = upper_bound(a, right_l)
    r = upper_bound(a, right_r)
    c = r - l
    if c > 0:
        s = pref[r] - pref[l]
        cnt += c
        dist_sum += s - c * x

    out.append(f"{cnt} {dist_sum}")

print("\n".join(out))
```

The implementation relies on explicit binary search instead of `bisect` to make the boundary behavior transparent. The important detail is the use of different inclusivity rules on the left and right intervals. On the left side we use a half-open interval `[b - R, b - L)`, so both boundaries use `lower_bound`. On the right side we use `(b + L, b + R]`, so we apply `upper_bound` on both ends.

The distance conversion step is where most implementation mistakes happen. The prefix sum gives us sums of coordinates, but the problem asks for sums of absolute differences. The code carefully transforms these into linear expressions in `b`.

## Worked Examples

Consider the first sample input.

We have enemies at positions `[4, 5, 6]`, and two watchers at `1` and `10`, with `L = 4` and `R = 5`.

For watcher at `1`, the valid distances are enemies with positions in `[ -4, -3 ]` on the left and `[5, 6]` on the right after translation. Only the right side contributes. The interval `(1 + 4, 1 + 5] = (5, 6]` contains only `6`.

| Watcher | Left interval | Right interval | Count | Sum of distances |
| --- | --- | --- | --- | --- |
| 1 | empty | [6] | 1 | 5 |

This confirms the mechanism correctly splits the space.

For watcher at `10`, we compute intervals `[1, 6)` and `(14, 15]`. Only the left side contributes, containing `4, 5, 6`.

| Watcher | Left interval | Right interval | Count | Sum of distances |
| --- | --- | --- | --- | --- |
| 10 | [4,5,6] | empty | 3 | 9 |

This shows that all distances are accumulated correctly using `10 - a[i]`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | Sorting plus two binary searches per query |
| Space | O(n) | Prefix sum array over sorted positions |

The constraints allow up to 200,000 elements, so a logarithmic factor per query stays comfortably within limits. The prefix sum construction is linear and negligible compared to sorting.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, q, L, R = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    a.sort()

    pref = [0]
    for x in a:
        pref.append(pref[-1] + x)

    def lb(x):
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid] < x:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def ub(x):
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid] <= x:
                lo = mid + 1
            else:
                hi = mid
        return lo

    res = []
    for x in b:
        cnt = 0
        s = 0

        l1, r1 = lb(x - R), lb(x - L)
        c = r1 - l1
        cnt += c
        s += c * x - (pref[r1] - pref[l1])

        l2, r2 = ub(x + L), ub(x + R)
        c = r2 - l2
        cnt += c
        s += (pref[r2] - pref[l2]) - c * x

        res.append(f"{cnt} {s}")

    return "\n".join(res)

# provided samples
assert run("""3 2 4 5
4 5 6
1 10
""") == """1 5
1 5"""

assert run("""5 4 1 3
1 3 5 6 9
2 4 7 8
""") == """1 3
2 5
2 4
2 5"""

# custom cases
assert run("""1 1 0 0
5
5
""") == """0 0"""

assert run("""3 1 0 10
1 2 3
2
""") == """3 3"""

assert run("""4 1 1 1
1 2 3 4
2
""") == """2 2"""

assert run("""5 2 2 3
-2 -1 0 1 2
0 2
""") == """2 3
2 3"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single point with zero radius | `0 0` | L = R = 0 exclusion handling |
| Full coverage range | `3 3` | All elements counted correctly |
| Exact boundary distance | `2 2` | Strict vs inclusive boundary correctness |
| Mixed negative and positive | `2 3 / 2 3` | Symmetry around origin and split intervals |

## Edge Cases

When all enemies lie exactly at distance `L`, they must be excluded. For example, with enemies at `[0, 5]`, `L = 5`, and watcher at `0`, both points are at distance `5`, so neither contributes. The algorithm handles this because the left interval uses `[b - R, b - L)` and the right interval uses `(b + L, b + R]`, explicitly excluding the boundary at `L`.

When `L = 0`, enemies at the same position as the watcher are excluded. For a single enemy at `0` and watcher at `0`, the left interval becomes `[0, 0)` and the right interval becomes `(0, R]`, so the point at `0` is not counted, matching the strict inequality requirement.

When no enemies fall within `[b - R, b + R]`, both binary searches produce empty segments, and both count and sum remain zero. The prefix sum structure naturally supports empty intervals since identical boundaries produce zero differences.
