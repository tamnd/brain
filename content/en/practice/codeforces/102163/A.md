---
title: "CF 102163A - Hasan the lazy judge"
description: "We have a collection of horizontal line segments and vertical line segments on an integer coordinate plane. A horizontal segment is described by its two x endpoints and its fixed y coordinate. A vertical segment is described by its two y endpoints and its fixed x coordinate."
date: "2026-08-21T18:48:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "A"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 2814
verified: false
draft: false
---

[CF 102163A - Hasan the lazy judge](https://codeforces.com/problemset/problem/102163/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 46m 54s  
**Verified:** no  

## Solution
# Problem Understanding

We have a collection of horizontal line segments and vertical line segments on an integer coordinate plane. A horizontal segment is described by its two x endpoints and its fixed y coordinate. A vertical segment is described by its two y endpoints and its fixed x coordinate.

Choosing one horizontal segment and one vertical segment gives a plus sign only when they intersect. At their intersection point, the horizontal segment contributes a left arm and a right arm, while the vertical segment contributes a downward arm and an upward arm. The value of this plus sign is the shortest of these four arm lengths.

For a horizontal segment `[x1, x2]` at height `y`, intersected at x, the horizontal contribution is

`min(x - x1, x2 - x)`.

For a vertical segment `[y1, y2]` at coordinate x, intersected at height y, the vertical contribution is

`min(y - y1, y2 - y)`.

The answer is the maximum possible value of the minimum of all four quantities over every valid intersection.

With up to `10^5` horizontal and `10^5` vertical segments, checking every pair requires up to `10^10` intersections. A quadratic approach is far beyond what a one-second limit can handle. The coordinates are also bounded by `10^5`, which makes logarithmic data structures over the coordinate range practical.

There are several boundary cases that can easily break a careless implementation. First, an intersection may happen exactly at an endpoint. For example,

```

```

The two segments intersect at `(1, 2)`, so the shortest arm has length `0`, and the answer is `0`. An implementation using strict inequalities instead of inclusive intersection conditions could incorrectly report that there is no intersection.

A second issue is that a segment may be too short to support a requested answer. For example,

```

```

The segments intersect at `(2, 2)`, but the horizontal segment has length only `1`, so no plus sign of length `1` is possible. The answer is `0`. During a feasibility check for length `1`, the horizontal segment must be discarded because it needs total length at least `2`.

A third boundary case is reversed endpoints. Although the statement describes starting and ending coordinates, a robust implementation should not depend on their order. For example,

```

```

After normalizing both segments, they intersect at `(3, 3)` and the answer is `2`.

# Approaches

The direct approach considers every horizontal segment together with every vertical segment. For each pair, we test whether their x and y coordinates fall inside the corresponding intervals. If they intersect, we calculate the four arm lengths and update the answer. This is correct because every possible plus sign is determined by exactly one horizontal and one vertical segment, so examining every pair cannot miss an optimum.

The problem is the number of pairs. With `N = M = 10^5`, there can be `N * M = 10^10` pairs. Even a constant-time check for each pair is much too slow, so we need to avoid enumerating intersections.

The key observation is that the answer can be tested instead of constructed directly. Suppose we ask whether a plus sign of length at least `d` exists. For a horizontal segment `[x1, x2]`, the intersection x-coordinate must then satisfy

`x1 + d <= x <= x2 - d`.

Thus the horizontal segment can participate only through its reduced interval `[x1 + d, x2 - d]`, and it is usable only when `x2 - x1 >= 2d`.

Similarly, a vertical segment `[y1, y2]` can participate only when

`y1 + d <= y <= y2 - d`.

So the problem for a fixed `d` becomes finding a horizontal segment whose reduced x-interval contains the x-coordinate of some usable vertical segment, while the horizontal segment's y-coordinate lies inside that vertical segment's reduced y-interval.

This can be handled by sweeping from left to right. Sort vertical segments by x. As we reach a vertical segment at x, every horizontal segment whose reduced left endpoint is at most x becomes active. A horizontal segment remains active until its reduced right endpoint becomes smaller than x.

The only remaining question is how to ask whether an active horizontal segment has its y-coordinate inside the vertical segment's reduced y-interval. Since each active horizontal contributes one point at its y-coordinate, a Fenwick tree can maintain how many active horizontals exist at every y. A range sum then tells us whether at least one active horizontal lies in the required y interval.

The predicate is monotone. If a plus sign of length `d` exists, then a plus sign of every smaller length also exists. We can consequently binary search for the maximum feasible `d`.

The brute-force works because every candidate is explicitly examined, but fails because there are too many pairs. The observation that a fixed answer reduces every segment independently lets us turn the two-dimensional intersection problem into a one-dimensional sweep with a Fenwick tree.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(NM)` | `O(N + M)` | Too slow |
| Optimal | `O((N + M) log C log C)` | `O(N + M + C)` | Accepted |

Here `C <= 10^5` is the coordinate limit. One logarithm comes from the binary search over the answer and the other from Fenwick tree operations.

# Algorithm Walkthrough

1. Normalize every segment so that its first endpoint is no greater than its second endpoint. Store the horizontal segments as `(x1, x2, y)` and the vertical segments as `(y1, y2, x)`.
2. Sort the horizontal segments once by `x1`, sort them once by `x2`, and sort the vertical segments once by `x`. These orders remain valid for every binary-search value because adding or subtracting the same `d` does not change the ordering.
3. Binary search the answer `d`. For a candidate `d`, a horizontal segment is usable only if `x2 - x1 >= 2d`. Its possible intersection x-coordinates form `[x1 + d, x2 - d]`. A vertical segment is usable only if `y2 - y1 >= 2d`, with possible intersection y-coordinates `[y1 + d, y2 - d]`.
4. Sweep through usable vertical segments in increasing x order. Maintain a Fenwick tree indexed by y. When the current vertical segment has coordinate x, add every horizontal segment whose `x1 + d <= x`. Such a horizontal segment has enough room on its left side to give an arm of length at least `d`.
5. Remove every horizontal segment whose `x2 - d < x`. Such a segment can no longer provide a right arm of length `d` at the current x. The strict `<` is essential because equality means the right arm has exactly length `d`, which is valid.
6. Query the Fenwick tree over `[y1 + d, y2 - d]`. A positive range sum means that some active horizontal segment has its y-coordinate in the valid vertical range. That horizontal and the current vertical segment form a plus sign whose four arms are all at least `d`, so the check succeeds.
7. If the check succeeds, move the binary-search lower bound upward. Otherwise, move the upper bound downward. The largest successful value is the answer.

### Why it works

For a fixed `d`, a horizontal segment is represented in the sweep exactly while its x-coordinate can be chosen so that both horizontal arms have length at least `d`. Thus an active horizontal segment is equivalent to the condition `x1 + d <= x <= x2 - d`.

At a vertical segment with coordinate x, the Fenwick tree contains exactly the y-coordinates of all horizontal segments satisfying that horizontal condition. Querying `[y1 + d, y2 - d]` additionally enforces both vertical-arm conditions. Hence the query succeeds exactly when there exists an intersection whose four arms are all at least `d`.

The feasibility predicate is monotone, because reducing `d` only relaxes the required distances. Binary search consequently finds the largest feasible length.

# Python Solution

```
Python
```

The input phase normalizes endpoints first. This avoids having every later operation handle both possible orientations.

The three sorted arrays are the core of the sweep. Sorting by `x1` lets the algorithm add horizontals in the exact order in which they become eligible. Sorting by `x2` lets it remove them when their right endpoint becomes too close to the current x-coordinate. The vertical array is sorted by x because the sweep itself moves from left to right.

For a candidate `d`, the condition `x1 + d <= x` determines insertion. The condition `x2 - d < x` determines removal. The second comparison is strict because `x2 - d == x` gives a right arm of exactly `d`, which must remain valid.

The Fenwick tree stores counts rather than booleans. Multiple horizontal segments can have the same y-coordinate, so removing one segment must not accidentally remove another. A count handles coincident y-values naturally.

The range query uses

`prefix(high_y) - prefix(low_y - 1)`,

which is the standard inclusive Fenwick range sum. This also handles the case where the valid y interval contains exactly one coordinate.

Python integers do not overflow, so all coordinate arithmetic is safe. The largest relevant coordinate is only `10^5`, while the binary-search multiplication `2 * d` is also tiny.

# Worked Examples

## Sample 1

The input contains horizontal segments

```

```

and vertical segments

```

```

The following trace shows the decisive feasibility checks.

| `d` | Usable horizontal ranges | Usable vertical ranges | Result |
| --- | --- | --- | --- |
| `3` | `[1,5]` becomes `[4,2]`, `[2,4]` becomes `[]`, `[6,12]` becomes `[9,9]` | First vertical becomes `[]`, second becomes `[]` | False |
| `1` | `[1,5]` -> `[2,4]`, `[2,4]` -> `[3,3]`, `[6,12]` -> `[7,11]` | `[1,5]` -> `[2,4]`, `[6,9]` -> `[7,8]` | True |
| `2` | `[1,5]` -> `[3,3]`, `[2,4]` -> `[4,2]`, `[6,12]` -> `[8,10]` | `[1,5]` -> `[3,3]`, `[6,9]` -> `[8,7]` | True |

For `d = 2`, the horizontal segment `[1,5]` can be used only at x-coordinate `3`. The vertical segment `[1,5]` at x-coordinate `3` can be used only at y-coordinate `3`. Their intersection is `(3,3)`, and all four arms have length at least `2`. A larger value is impossible, so the answer is `2`.

## Constructed Example 2

Consider

```

```

For `d = 2`, the reduced horizontal intervals are `[3,5]` at y=4 and `[5,3]` for the second horizontal, so only the first horizontal remains usable. The reduced vertical intervals are `[4,6]` at x=5 and `[3,4]` at x=3.

| Vertical | x | Active horizontal y-values | Required y-range | Result |
| --- | --- | --- | --- | --- |
| `[1,6]` at x=3 | 3 | none | `[3,4]` | no |
| `[2,8]` at x=5 | 5 | `{4}` | `[4,6]` | yes |

The second vertical intersects the first horizontal at `(5,4)`. Its four arm lengths are `4`, `2`, `2`, and `4`, so the plus sign has length `2`.

This example demonstrates why the Fenwick tree needs to maintain the currently active horizontals rather than simply checking whether the segments intersect somewhere. The required intersection must leave at least `d` units on every side.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O((N + M) log C log C)` | Binary search performs `O(log C)` checks, and every check performs `O(N + M)` Fenwick operations, each taking `O(log C)` |
| Space | `O(N + M + C)` | Three sorted segment collections and one Fenwick tree over the coordinate range |

With `C <= 10^5`, the binary search needs at most about 17 iterations. Each segment enters and leaves the Fenwick structure at most once during a check, while each vertical segment causes a constant number of Fenwick prefix queries. The resulting complexity is logarithmic in the coordinate range on top of a linear scan of the segments, which is suitable for the given limits.

# Test Cases

```
Python
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | `2` | Normal intersection and binary search |
| One horizontal and one vertical touching at an endpoint | `0` | Inclusive boundaries and zero-length arms |
| `[1,5]` crossing `[1,5]` centrally | `2` | Exact maximum where every arm has length `2` |
| Reversed endpoints | `2` | Endpoint normalization |
| Segments with geometric intersections but no positive plus | `0` | Rejecting insufficient arm lengths |
| `100000` full-length horizontals and verticals | `49999` | Maximum input size and performance |

# Edge Cases

The endpoint-intersection case

```

```

is handled by `d = 0`. The horizontal becomes active when `x1 + 0 <= x`, so it is active at x=`1`. Its right boundary is not removed until `x2 < x`. At the vertical's x-coordinate `1`, the Fenwick query covers y=`2`, so the intersection is found and the binary search keeps `0` as the answer. A strict removal condition is what preserves an endpoint intersection.

The insufficient-length case

```

```

illustrates the `x2 - x1 >= 2d` condition. For `d = 1`, the horizontal has length `1`, which is less than `2`, so it is never inserted into the Fenwick tree. Although the two segments intersect, no four arms of length `1` can exist. The check fails and the answer remains `0`.

The reversed-endpoint case

```

```

is normalized to horizontal `[1,5]` and vertical `[1,5]`. At `d = 2`, both reduced intervals collapse to coordinate `3`, producing the intersection `(3,3)`. The answer is `2`. Without normalization, comparisons such as `x1 + d <= x` would be meaningless for the reversed representation.

Finally, multiple horizontal segments may share the same y-coordinate. The Fenwick tree stores a count at each coordinate rather than a boolean state. If two active segments both lie at y=`7`, inserting them produces count `2`, and removing one produces count `1`. The remaining segment is still represented correctly, so overlapping coordinates do not corrupt the sweep.
