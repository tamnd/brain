---
title: "CF 102860B - Triangles and a Circle"
description: "We are given several marked points on the circumference of a circle. The circle has circumference L, and every point is represented by its clockwise distance from a chosen starting point."
date: "2026-07-25T14:18:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102860
codeforces_index: "B"
codeforces_contest_name: "2020-2021 Saint-Petersburg Open High School Programming Contest (SpbKOSHP 20)"
rating: 0
weight: 102860
solve_time_s: 35
verified: true
draft: false
---

[CF 102860B - Triangles and a Circle](https://codeforces.com/problemset/problem/102860/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
# Problem Understanding

We are given several marked points on the circumference of a circle. The circle has circumference `L`, and every point is represented by its clockwise distance from a chosen starting point. We need to count how many different choices of three marked points form a triangle that contains the circle's center either strictly inside the triangle or exactly on one of its sides.

The important geometric fact is that the three vertices of a triangle inscribed in a circle fail to contain the center only when all three vertices fit inside some open semicircle. If the points are spread over more than half of the circle, the center must be inside the triangle. If two points are exactly opposite each other, the center lies on the triangle border, so those triangles must also be counted.

The input gives up to `300000` points. With that size, checking every triple is impossible because there are about `n^3 / 6` possible triangles. Even `O(n^2)` operations are too large when `n` is near the limit. The solution must process the points in sorted order and use a linear or near-linear scan.

The tricky cases come from the difference between an open and a closed semicircle. A triangle with vertices exactly half a circle apart is valid, because the center lies on its border. A solution that uses `<= L / 2` when searching for invalid triangles will remove these cases incorrectly.

For example:

```
3 10
0 5 6
```

The answer is:

```
1
```

The points at `0` and `5` are opposite ends of a diameter. The triangle has the center on the side connecting those two points. Treating the distance `5` as part of a bad semicircle would incorrectly count this triangle as invalid.

Another edge case is when all points are concentrated inside a small arc.

```
4 20
0 1 2 3
```

The answer is:

```
0
```

Every possible triangle fits inside an open semicircle, so none contains the center. A careless implementation that only checks adjacent points or only one direction around the circle can miss these cases.

# Approaches

The direct approach is to examine every possible triple of points. For each triple, we could compute whether the center is inside the triangle using geometry, or equivalently check whether the points fit into some semicircle. This is correct because every possible triangle is considered, but there are `C(n,3)` triples. With `n = 300000`, that is roughly `4.5 * 10^15` checks, which is far beyond any practical limit.

The key observation is that counting the triangles that contain the center directly is harder than counting the opposite group. A triangle is invalid exactly when all its vertices lie inside one open semicircle. After sorting the points around the circle, we can count those invalid triangles efficiently.

Fix the first point of such a semicircle. Suppose we stand at point `i` and look clockwise. If there are `k` later points strictly less than `L / 2` away, then every pair among those `k` points creates an invalid triangle with point `i`. This gives `k * (k - 1) / 2` invalid triangles starting from `i`.

The only remaining question is whether the same invalid triangle is counted more than once. For a triangle inside an open semicircle, the first point of that semicircle is unique. If the three points are `a < b < c` in circular order and `c - a < L / 2`, then starting from `b` would require wrapping around the circle, and that wrapped distance is greater than `L / 2`. So every invalid triangle is counted exactly once.

The answer is the total number of triangles minus the invalid ones.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

# Algorithm Walkthrough

1. Sort all point coordinates in clockwise order. Duplicate the sorted array by appending every coordinate plus `L`. The duplicate part represents going around the circle one extra time, which allows us to use normal two-pointer movement instead of manually handling wraparound cases.
2. For every original point `i`, move a right pointer until the distance from `i` reaches at least `L / 2`. The points between `i + 1` and `right - 1` are exactly the points that can join `i` inside an open semicircle.
3. If there are `k` such points, add `k * (k - 1) / 2` to the invalid triangle count. These are all pairs of points that combine with `i` to create a triangle that cannot contain the center.
4. Compute the total number of possible triangles, `n * (n - 1) * (n - 2) / 6`, and subtract the invalid count.

The invariant behind the two-pointer scan is that for every starting point `i`, the right pointer always marks the first position that is outside the allowed open semicircle. Because both pointers only move forward, every pair of points is considered in sorted order exactly once. The counting argument proves that every invalid triangle has one unique starting vertex, so the subtraction removes exactly the unwanted triangles.

# Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, L = map(int, input().split())
    x = list(map(int, input().split()))
    x.sort()

    a = x + [v + L for v in x]

    bad = 0
    r = 0

    for i in range(n):
        if r < i + 1:
            r = i + 1
        while r < i + n and a[r] - a[i] < L / 2:
            r += 1
        cnt = r - i - 1
        bad += cnt * (cnt - 1) // 2

    total = n * (n - 1) * (n - 2) // 6
    print(total - bad)

if __name__ == "__main__":
    solve()
```

The input is sorted first because the circular order is the only information needed for the semicircle test. The duplicated array allows every search to be written as a simple increasing interval.

The pointer `r` is never moved backwards. For each starting position, it finds the first point that is not strictly inside the semicircle. The strict comparison is necessary because points exactly `L / 2` apart create valid triangles with the center on the border.

The value `cnt` is the number of choices after `i` that can still fit into the same open semicircle. Choosing any two of them gives one invalid triangle, which is why the contribution is `cnt * (cnt - 1) // 2`.

Python integers do not overflow, so the large number of possible triangles is safe to compute directly.

# Worked Examples

For the first sample:

```
3 10
0 1 2
```

The sorted duplicated coordinates are:

`[0, 1, 2, 10, 11, 12]`

| i | Current point | Points inside open semicircle | Count | Added invalid triangles |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1, 2 | 2 | 1 |
| 1 | 1 | 2 | 1 | 0 |
| 2 | 2 | none | 0 | 0 |

The total number of triangles is `1`. The only triangle is invalid because all points are inside a semicircle shorter than half the circle, so the result is `1 - 1 = 0`.

For the second sample:

```
10 10
0 1 2 3 4 5 6 7 8 9
```

For each starting point, exactly four points lie in the following open semicircle.

| i | Current point | Number of following points within distance < 5 | Invalid contribution |
| --- | --- | --- | --- |
| 0 | 0 | 4 | 6 |
| 1 | 1 | 4 | 6 |
| 2 | 2 | 4 | 6 |
| 3 | 3 | 4 | 6 |
| 4 | 4 | 4 | 6 |
| 5 | 5 | 4 | 6 |
| 6 | 6 | 4 | 6 |
| 7 | 7 | 4 | 6 |
| 8 | 8 | 4 | 6 |
| 9 | 9 | 4 | 6 |

The invalid count is `60`. The total number of triangles is `120`, so the answer is `120 - 60 = 60`. The example also shows why diameter pairs must stay valid: opposite points are exactly at distance `5`, not included in the open semicircle.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, and the two-pointer scan is linear because each pointer moves only forward. |
| Space | O(n) | The duplicated coordinate array stores two copies of the points. |

The algorithm fits the constraint of `300000` points because the expensive part is only sorting. The counting phase performs a constant amount of work per point.

# Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

assert run("3 10\n0 1 2\n") == "0\n", "sample 1"
assert run("10 10\n0 1 2 3 4 5 6 7 8 9\n") == "60\n", "sample 2"

assert run("3 10\n0 5 6\n") == "1\n", "diameter edge case"
assert run("4 20\n0 1 2 3\n") == "0\n", "all points in one arc"
assert run("5 10\n0 2 4 6 8\n") == "5\n", "even spacing boundary case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 10 / 0 1 2` | `0` | Basic triangle completely inside a semicircle |
| `10 10 / 0 1 2 3 4 5 6 7 8 9` | `60` | Symmetric case with many diameter pairs |
| `3 10 / 0 5 6` | `1` | Correct handling of points exactly half a circle apart |
| `4 20 / 0 1 2 3` | `0` | All points concentrated in a small arc |
| `5 10 / 0 2 4 6 8` | `5` | Multiple boundary cases around the circle |

# Edge Cases

When two vertices are opposite each other, the triangle must be counted. For input:

```
3 10
0 5 6
```

the pointer search from `0` stops before `5` because the distance is exactly `L / 2`. The triangle is not marked invalid, and the total count remains `1`.

When all points are located close together, every triangle is invalid. For:

```
4 20
0 1 2 3
```

starting from `0` finds the other three points within distance `10`, producing three invalid triangles. The same happens for the other starting points where appropriate, and every possible triangle is removed exactly once.

The most common implementation mistake is using `<= L / 2` instead of `< L / 2`. The algorithm relies on open semicircles because closed semicircles include diameter cases where the center is on the triangle border and must be counted.
