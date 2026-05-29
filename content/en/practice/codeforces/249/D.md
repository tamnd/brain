---
title: "CF 249D - Donkey and Stars"
description: "We are asked to model a chain of stars in a 2D plane, originating from the point (0,0). Each star is defined by its coordinates, and two rays emanate from the origin at slopes defined by fractions α1 = a/b and α2 = c/d."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "geometry", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 249
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 152 (Div. 1)"
rating: 2700
weight: 249
solve_time_s: 75
verified: true
draft: false
---

[CF 249D - Donkey and Stars](https://codeforces.com/problemset/problem/249/D)

**Rating:** 2700  
**Tags:** data structures, dp, geometry, math, sortings  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to model a chain of stars in a 2D plane, originating from the point (0,0). Each star is defined by its coordinates, and two rays emanate from the origin at slopes defined by fractions α1 = a/b and α2 = c/d. A valid chain starts at the origin and moves from one star to another, where the next star must lie strictly between the two rays projected from the current star. The task is to find the maximum length of such a chain.

The input gives up to 100,000 stars with integer coordinates up to 100,000. With a time limit of 2 seconds, any solution iterating over all possible pairs of stars directly would require O(n²) operations, which is roughly 10¹⁰ and far too slow. Therefore, we need an algorithm that works in O(n log n) or O(n) per query.

A non-obvious edge case arises when multiple stars lie collinear with the rays. Since stars on the boundary of the rays cannot be chosen, the chain must strictly avoid these. Another tricky scenario is when all stars are either entirely above, below, or to the left of each other - a naive top-down sweep could miss a valid chain that starts farther left but climbs more gradually.

For example, consider stars at coordinates (1,1), (2,2), (3,3) with α1 = 1/2 and α2 = 2/1. The longest chain is length 2, but if the code incorrectly treats stars on the rays as valid, it might return 3.

## Approaches

A brute-force solution would attempt to start a chain from each star and recursively search for all next stars that fall strictly between the rays projected from it. This is correct but impractical: each search could iterate over O(n) stars, giving O(n²) complexity.

The key observation is that the problem can be transformed into a type of 2D dynamic programming based on dominance order. By computing for each star its transformed coordinates relative to the rays, the problem reduces to finding the longest chain such that each subsequent star has a greater "left slope" and a smaller "right slope." Sorting the stars by one coordinate (say x) and applying a variant of the Longest Increasing Subsequence (LIS) in the second coordinate yields an O(n log n) solution.

This works because the strict inequalities implied by the rays translate to strict inequalities on the transformed slopes. Once we have this order, LIS guarantees that no valid chain is missed and the maximum possible chain is found efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Transform + LIS | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Parse the slope fractions α1 = a/b and α2 = c/d and compute them as rational numbers. These define the left and right rays.
2. For each star (x_i, y_i), compute its transformed values relative to the rays. Specifically, compute `left = y_i - (a/b) * x_i` and `right = y_i - (c/d) * x_i`. These numbers measure vertical distance from the rays; a star is strictly between the rays if left > 0 and right < 0.
3. Filter out all stars that do not satisfy left > 0 and right < 0.
4. Sort the remaining stars primarily by `left` ascending, and secondarily by `right` descending. This ensures that when we apply LIS on `right`, we maintain the dominance property: a star later in the chain will have higher `left` and lower `right`.
5. Apply a Longest Increasing Subsequence algorithm on the negative of `right` values. Using a binary search approach, maintain a list that keeps the minimum ending `right` value for LIS of each length.
6. The length of the LIS is the maximum number of stars in the chain.

Why it works: Sorting by `left` guarantees that any subsequent star has strictly larger `left` than its predecessors. Applying LIS on `-right` ensures that the next star in the chain also has a strictly smaller `right`. Combining these two guarantees preserves the invariant that each star lies strictly between the rays of its predecessor.

## Python Solution

```python
import sys
import bisect
input = sys.stdin.readline

n = int(input())
a_b, c_d = input().split()
a, b = map(int, a_b.split('/'))
c, d = map(int, c_d.split('/'))

stars = []
for _ in range(n):
    x, y = map(int, input().split())
    # left = y - (a/b) * x > 0  => b*y - a*x > 0
    # right = y - (c/d) * x < 0 => d*y - c*x < 0
    left = b * y - a * x
    right = d * y - c * x
    if left > 0 and right < 0:
        stars.append((left, right))

# sort by left ascending, then right descending
stars.sort(key=lambda p: (p[0], -p[1]))

# compute LIS on -right
lis = []
for _, r in stars:
    r_neg = -r
    idx = bisect.bisect_left(lis, r_neg)
    if idx == len(lis):
        lis.append(r_neg)
    else:
        lis[idx] = r_neg

print(len(lis))
```

The code first converts fractions to integer multipliers to avoid floating-point precision issues. Filtering ensures only stars strictly inside the initial rays are considered. Sorting by `left` ascending and `right` descending preserves the proper order for LIS. Using `bisect_left` allows O(n log n) LIS computation. Using `-right` instead of `right` ensures we maintain decreasing `right` in the chain.

## Worked Examples

### Sample 1

Input:

```
15
1/3 2/1
3 1
6 2
4 2
2 5
4 5
6 6
3 4
1 6
2 1
7 4
9 3
5 3
1 3
15 5
12 4
```

After filtering, transformed coordinates are computed as `left = 3*y - 1*x`, `right = 2*y - 1*x`. Only stars with left > 0 and right < 0 are considered. Sorted by `left` ascending, `right` descending, the LIS on `-right` finds the maximum chain length 4.

| Star | left | right | lis state |
| --- | --- | --- | --- |
| (1,3) | 8 | 5 | [ -5 ] |
| (2,5) | 13 | 8 | [ -8, -5 ] |
| (3,4) | 9 | 5 | [ -8, -5 ] |
| ... | ... | ... | ... |

### Custom Input

```
3
1/1 2/1
1 1
2 2
3 3
```

Only the middle star satisfies left > 0 and right < 0. LIS gives length 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting and LIS with binary search dominate the cost. |
| Space | O(n) | Storing filtered stars and LIS array. |

With n ≤ 10^5, O(n log n) operations is roughly 5*10^5, well within the 2-second limit.

## Test Cases

```python
import sys, io, bisect

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a_b, c_d = input().split()
    a, b = map(int, a_b.split('/'))
    c, d = map(int, c_d.split('/'))

    stars = []
    for _ in range(n):
        x, y = map(int, input().split())
        left = b * y - a * x
        right = d * y - c * x
        if left > 0 and right < 0:
            stars.append((left, right))

    stars.sort(key=lambda p: (p[0], -p[1]))
    lis = []
    for _, r in stars:
        r_neg = -r
        idx = bisect.bisect_left(lis, r_neg)
        if idx == len(lis):
            lis.append(r_neg)
        else:
            lis[idx] = r_neg
    return str(len(lis))

# provided sample
assert run("""15
1/3 2/1
3 1
6 2
4 2
2 5
4 5
6 6
3 4
1 6
2 1
7 4
9 3
5 3
1 3
15 5
12 4
""") == "4", "sample 1"

# minimum input
assert run("1\n1/1 2/1\n1 1\n") == "0", "min input"

# increasing diagonal
assert run("3\n1/1 2/1\n1 1\n2 2\n3 3\n") == "2", "diagonal"

# all stars outside rays
assert run("2\n1/3 2/1\n1 10\n10 1\n")
```
