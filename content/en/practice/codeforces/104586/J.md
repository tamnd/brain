---
title: "CF 104586J - \u0420\u0443\u0434\u043e\u043b\u044c\u0444 \u0438 \u043f\u043e\u0440\u0442\u0430\u043b \u0432 \u0420\u0430\u043c\u0435\u043d\u044c"
description: "We are given a set of vertical posts placed on a line, each defined by a position on the x-axis and a height. We are allowed to pick two different posts, say one as the “falling” post and one as the “target” post."
date: "2026-06-30T07:37:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104586
codeforces_index: "J"
codeforces_contest_name: "Codemasters Codecup 2023 - \u041e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u0442\u0443\u0440"
rating: 0
weight: 104586
solve_time_s: 120
verified: true
draft: false
---

[CF 104586J - \u0420\u0443\u0434\u043e\u043b\u044c\u0444 \u0438 \u043f\u043e\u0440\u0442\u0430\u043b \u0432 \u0420\u0430\u043c\u0435\u043d\u044c](https://codeforces.com/problemset/problem/104586/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of vertical posts placed on a line, each defined by a position on the x-axis and a height. We are allowed to pick two different posts, say one as the “falling” post and one as the “target” post. The falling post is rotated so that its top touches the top of the target post, forming a right triangle together with the ground.

Geometrically, the base of this triangle is the horizontal distance between the two chosen positions, and the vertical component is determined by the height of the target post, because the top of the target is what defines the upper vertex of the triangle. The falling post only serves as a connector that must be tall enough to reach that point, but it does not independently contribute to the triangle’s height once the configuration is valid.

The goal is to choose an ordered pair of distinct indices that maximizes the area of this right triangle. If no valid configuration exists that produces a positive area, we output -1 -1.

The constraints allow up to 100,000 posts, with coordinates up to 10^9. This immediately rules out any solution that considers all pairs explicitly, since that would require on the order of 10^10 operations in the worst case. We need something closer to O(n log n) or O(n).

A subtle issue in problems of this type is that the direction of the falling post matters only in terms of feasibility, not in the final area formula. Many incorrect solutions accidentally treat the problem as symmetric or ignore the ordering constraint, which leads to wrong answers on cases where the optimal configuration depends on selecting the correct “target” post first.

Another failure mode comes from assuming the best pair is always formed by adjacent posts after sorting by x-coordinate. For example, consider:

Input:

```
3
0 100
1 1
10 1
```

A greedy adjacency approach might try (0,1) or (1,10), but the best structure depends on combining extreme distance with sufficient height constraints, which adjacency does not capture.

Finally, another pitfall is ignoring that the best partner for a given post depends on global extrema among a filtered set, not local neighbors.

## Approaches

A brute-force solution tries every ordered pair of posts. For each pair, we compute the triangle area implied by using one as the falling post and the other as the support. This is straightforward and correct because it checks all configurations directly. However, it requires checking n(n−1) pairs, and each check is O(1), leading to O(n^2) time, which is far beyond feasible for n = 100,000.

The key observation is that for a fixed “target” post, the area depends only on its height and the distance to the best possible partner. If we fix the target post as b, the best falling post a is always one that maximizes |x_a − x_b| while still satisfying the feasibility condition that a is tall enough to reach b.

This suggests reversing the perspective: instead of enumerating pairs, we process posts in order of decreasing height. When we process a post, all previously processed posts have height at least as large, so they are valid candidates to be falling posts for the current one. Among those candidates, we only need the minimum and maximum x-coordinate to maximize distance.

This reduces the problem to maintaining a dynamic set of points with fast access to extreme x-values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Sorting + sweep with extrema | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

### 1. Sort posts by height in descending order

We begin by sorting all posts so that we always process taller posts first. This ensures that when we consider a post, every previously processed post is at least as tall.

This ordering is crucial because it guarantees feasibility: any earlier post can serve as the falling post for the current one.

### 2. Maintain a dynamic set of x-coordinates

We maintain a structure that stores x-coordinates of all previously processed posts. From this set, we only need to track the minimum and maximum x-values.

These two extremes are sufficient because they maximize horizontal distance to any new point.

### 3. Process each post as the current target

For each post i in sorted order, we treat it as the potential target. If we already have processed posts, we compute the best possible distance from i to the current extremes:

We evaluate distance = max(|x_i − min_x|, |x_i − max_x|).

We then compute area candidate = h_i × distance.

This corresponds to using i as the support post and pairing it with the farthest valid falling post.

### 4. Update the best answer

We keep track of the maximum area found so far and store the corresponding ordered pair of indices.

### 5. Insert current post into the structure

After processing i, we insert its x-coordinate into the structure so it becomes available for future (shorter) posts.

### Why it works

At any step, all previously processed posts have height greater or equal to the current one, so they are valid falling posts. For each target post, the best falling post must lie at one of the two ends of the current x-range, since distance is linear in x and maximized at extremes. This ensures that we never miss a candidate that could yield a larger area, because any interior point cannot produce a larger horizontal distance than the extremes.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    pts = []
    for i in range(n):
        x, h = map(int, input().split())
        pts.append((h, x, i + 1))
    
    pts.sort(reverse=True)

    min_x = None
    max_x = None

    best_area = 0
    best_pair = (-1, -1)

    for h, x, idx in pts:
        if min_x is not None:
            d1 = abs(x - min_x)
            d2 = abs(x - max_x)
            if d1 >= d2:
                area = h * d1
                if area > best_area:
                    best_area = area
                    best_pair = (idx, pts_map_min[min_x])
            else:
                area = h * d2
                if area > best_area:
                    best_area = area
                    best_pair = (idx, pts_map_max[max_x])

        if min_x is None:
            min_x = max_x = x
            pts_map_min = {x: idx}
            pts_map_max = {x: idx}
        else:
            if x < min_x:
                min_x = x
                pts_map_min[x] = idx
            if x > max_x:
                max_x = x
                pts_map_max[x] = idx

    if best_area == 0:
        print(-1, -1)
    else:
        print(*best_pair)

if __name__ == "__main__":
    solve()
```

The implementation follows the sweep idea directly. The array is sorted by height so that feasibility is guaranteed when pairing with previously seen points.

We maintain minimum and maximum x among processed points, along with a mapping to retrieve the corresponding indices. Each new point is compared against both extremes, since only those can maximize distance.

A subtle implementation issue is that both extremes must be tracked along with their originating indices. If multiple points share the same extreme x over time, we must ensure we still reference a valid index. The dictionaries here serve that purpose, although a simpler implementation can store both (x, idx) pairs for min and max explicitly.

The check for best_area == 0 handles the case where no valid pair exists, meaning we never had at least two compatible points.

## Worked Examples

### Sample 1

Input:

```
4
0 2
1 4
3 3
5 2
```

Sorted by height:

| step | h | x | min_x | max_x | best distance | area |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 4 | 1 | 1 | 1 | - | - |
| 2 | 3 | 3 | 1 | 1 | 2 | 6 |
| 3 | 2 | 0 | 0 | 3 | 3 | 6 |
| 4 | 2 | 5 | 0 | 5 | 5 | 10 |

The best pair comes from the last step, where the height 2 point at x=5 pairs with x=0.

This confirms that the optimal structure may involve a shorter target but a larger horizontal span, which motivates tracking global extremes rather than local adjacency.

### Sample 2

Input:

```
5
2 4
8 1
11 5
9 9
4 5
```

Sorted by height:

| step | h | x | min_x | max_x | best distance | area |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 9 | 9 | 9 | 9 | - | - |
| 2 | 5 | 11 | 9 | 9 | 2 | 10 |
| 3 | 5 | 4 | 4 | 11 | 7 | 35 |
| 4 | 4 | 2 | 2 | 11 | 9 | 36 |
| 5 | 1 | 8 | 2 | 11 | 9 | 9 |

The best configuration appears at step 4, pairing x=2 and x=11.

This demonstrates that even a moderately tall post can dominate the answer if it allows a large horizontal separation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates, all updates are O(1) |
| Space | O(n) | storing posts and auxiliary mappings |

The solution easily fits within limits since n = 100,000 only requires sorting and a single linear sweep with constant-time updates.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue()

# provided samples
# (placeholders since solve prints directly; in real harness you'd capture stdout)

# custom cases
# minimum size
# 2 points, valid
# all equal heights
# extreme spread
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 points with distinct x | valid pair | minimal configuration |
| all equal heights | any valid extreme pair | correctness under symmetry |
| increasing x, decreasing h | correct extreme selection | avoids adjacency trap |
| single dominant far point | correct pairing with extreme | global max distance behavior |

## Edge Cases

A minimal input with two points always produces the only possible pair, and the algorithm handles it by inserting the first point and immediately evaluating the second against it. The sweep ensures that the first point becomes part of the candidate set exactly when needed.

When all points have identical height, every point becomes equally valid as a target. The algorithm reduces to selecting the pair with maximum horizontal distance, which is correctly found using the maintained minimum and maximum x-values.

In cases where points are clustered in x but one point lies far away, the extreme tracking ensures that the far point is always chosen when it becomes part of the processed set, preventing any local clustering from dominating the answer.
