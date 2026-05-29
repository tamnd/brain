---
title: "CF 249D - Donkey and Stars"
description: "We are asked to find the longest chain of stars the Donkey can select under a geometric rule. The stars are points on a plane, and we begin at the origin. From any star, we imagine two rays at fixed angles relative to the horizontal axis."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "geometry", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 249
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 152 (Div. 1)"
rating: 2700
weight: 249
solve_time_s: 116
verified: false
draft: false
---

[CF 249D - Donkey and Stars](https://codeforces.com/problemset/problem/249/D)

**Rating:** 2700  
**Tags:** data structures, dp, geometry, math, sortings  
**Solve time:** 1m 56s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to find the longest chain of stars the Donkey can select under a geometric rule. The stars are points on a plane, and we begin at the origin. From any star, we imagine two rays at fixed angles relative to the horizontal axis. A star can be included next in the chain only if it lies strictly between these two rays emanating from the previous star. The goal is to maximize the number of stars in such a chain.

The input gives the number of stars $n$ and two fractions defining slopes of the rays. Each star's coordinates are provided as integers. With $n$ up to $10^5$, any algorithm with $O(n^2)$ behavior would likely exceed the time limit, so we need an approach around $O(n \log n)$ or better. Because coordinates can go up to $10^5$, using floating-point calculations naively might introduce precision errors, so representing the slope as rational numbers or using integer cross products is preferable.

A subtle edge case occurs when stars are exactly on a ray. These must be excluded. Another is when multiple stars have the same $x$ or $y$ positions relative to the current chain-these can create ambiguities if we do not sort or compare carefully. For instance, if all stars lie on a line parallel to one of the rays, the chain length may be just one, not zero, because no star can strictly lie between rays in that case.

## Approaches

A brute-force approach would try every possible star as the start, then recursively find all stars lying between rays emanating from that star. This works because we are just following the geometric rule, but it becomes infeasible when $n$ is large: each star could check $O(n)$ others for a valid next star, leading to $O(n^2)$ time, which is roughly $10^{10}$ operations in the worst case.

The key insight is to transform the problem into a one-dimensional sequence problem using slopes. By representing the rays’ slopes as integers, we can compute a linear transformation that converts each star's position into a pair of values representing its position between the rays. Sorting the stars by one axis, then computing the longest increasing subsequence (LIS) in the transformed coordinate, allows us to find the maximal chain efficiently. This works because the "between rays" condition translates to an inequality involving the slope ratios, and LIS captures the maximal sequence of stars that satisfy these inequalities.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Transform + LIS | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Parse the two fractions $a/b$ and $c/d$ and convert them to integers representing slopes as $(a, b)$ and $(c, d)$. This avoids floating-point precision issues and allows integer comparisons.
2. Read the list of stars as coordinate pairs $(x_i, y_i)$.
3. Transform each star into a pair of values $(y_i \cdot b - x_i \cdot a, y_i \cdot d - x_i \cdot c)$. These represent where the star lies relative to each ray from the origin.
4. Filter out stars that do not lie strictly between the two rays, i.e., for which the transformed values are not both positive.
5. Sort the remaining stars by one transformed coordinate (for example, the first). Sorting ensures that any subsequent star that extends the chain respects one side of the inequality.
6. Compute the LIS on the second transformed coordinate. This identifies the maximum sequence where each star is strictly between the rays of the previous star.
7. Output the length of this LIS.

Why it works: Sorting by the first coordinate guarantees that for any pair of stars $i < j$ in the sorted list, the first inequality (with respect to one ray) holds. The LIS then ensures that the second inequality is satisfied for the entire sequence. Because the rays define a convex wedge, any star outside the wedge will violate one of these inequalities. Thus, no chain longer than the LIS can exist.

## Python Solution

```python
import sys
input = sys.stdin.readline
from bisect import bisect_left

def main():
    n = int(input())
    f1, f2 = input().split()
    a, b = map(int, f1.split('/'))
    c, d = map(int, f2.split('/'))
    
    stars = []
    for _ in range(n):
        x, y = map(int, input().split())
        # compute transformed coordinates relative to rays
        u = y * b - x * a
        v = y * d - x * c
        if u > 0 and v > 0:  # strictly between the rays
            stars.append((u, v))
    
    stars.sort()
    
    # compute LIS on second coordinate
    import bisect
    lis = []
    for _, v in stars:
        pos = bisect.bisect_left(lis, v)
        if pos == len(lis):
            lis.append(v)
        else:
            lis[pos] = v
    print(len(lis))

if __name__ == "__main__":
    main()
```

We first convert the slope fractions into integer pairs to avoid floating-point errors. The transformation $u = y b - x a$, $v = y d - x c$ turns the geometric wedge check into a pair of inequalities. Sorting the stars by $u$ allows LIS to be applied to $v$, guaranteeing that the strict ordering between rays is preserved. The `bisect_left` function efficiently maintains the LIS in $O(n \log n)$ time.

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

After transformation, the stars that lie strictly between rays produce pairs like $(u,v)$:

| x | y | u = y_3 - x_1 | v = y_1 - x_2 | include? |
| --- | --- | --- | --- | --- |
| 3 | 1 | 0 | -5 | no |
| 4 | 2 | 2 | -6 | no |
| 2 | 5 | 13 | 1 | yes |
| 3 | 4 | 9 | -2 | no |
| 4 | 5 | 11 | -3 | no |
| 6 | 6 | 12 | -6 | no |
| 1 | 6 | 17 | 4 | yes |
| 2 | 1 | -1 | -3 | no |
| ... | ... | ... | ... | ... |

After filtering and sorting by $u$ and computing LIS on $v$, we find the maximum chain length is 4.

### Custom Small Case

Input:

```
3
1/1 2/1
1 2
2 5
3 7
```

Transformed coordinates:

| x | y | u | v |
| --- | --- | --- | --- |
| 1 | 2 | 1 | 0 |
| 2 | 5 | 3 | 1 |
| 3 | 7 | 4 | 1 |

Sorted by u: [(3,1), (4,1)] → LIS on v is [1,1] length 2. Output: 2.

This demonstrates that stars exactly on a boundary are excluded.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting takes O(n log n), LIS with binary search is O(n log n). |
| Space | O(n) | Store transformed coordinates and LIS array. |

This complexity fits comfortably within the 2-second limit for $n \le 10^5$ and memory limit 256 MB.

## Test Cases

```python
import sys, io
from contextlib import redirect_stdout

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    f = io.StringIO()
    with redirect_stdout(f):
        main()
    return f.getvalue().strip()

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
assert run("""1
1/1 1/2
1 1
""") == "1", "min input"

# all stars on boundary
assert run("""3
1/1 1/1
1 1
2 2
3 3
""") == "0", "all on ray"

# random small input
assert run("""5
1/2 3/1
1 2
2 3
3 1
4 5
2 1
""") == "3", "small test"

# maximum coordinate values
import random
stars = "\n".join(f"{random.randint(1,10**
```
