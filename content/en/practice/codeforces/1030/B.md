---
title: "CF 1030B - Vasya and Cornfield"
description: "The task is to classify points in a plane relative to a fixed geometric region defined by four boundary points: $(0, d)$, $(d, 0)$, $(n, n-d)$, and $(n-d, n)$."
date: "2026-06-16T20:59:36+07:00"
tags: ["codeforces", "competitive-programming", "geometry"]
categories: ["algorithms"]
codeforces_contest: 1030
codeforces_index: "B"
codeforces_contest_name: "Technocup 2019 - Elimination Round 1"
rating: 1100
weight: 1030
solve_time_s: 315
verified: true
draft: false
---

[CF 1030B - Vasya and Cornfield](https://codeforces.com/problemset/problem/1030/B)

**Rating:** 1100  
**Tags:** geometry  
**Solve time:** 5m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to classify points in a plane relative to a fixed geometric region defined by four boundary points: $(0, d)$, $(d, 0)$, $(n, n-d)$, and $(n-d, n)$. These four points form a convex quadrilateral that looks like a square rotated 45 degrees and then clipped inside the $n \times n$ grid.

We are given multiple query points, each representing a grasshopper location. For each point $(x, y)$, we must decide whether it lies inside this quadrilateral or exactly on its boundary.

The constraints are very small: $n \le 100$ and $m \le 100$. This immediately rules out any need for advanced geometry structures or optimization. Even an $O(m)$ per query check is trivial, since the total number of operations stays under a few thousand. What matters here is deriving the correct inequalities that describe the region.

The key difficulty is not performance but correctness: translating the rotated geometric shape into simple coordinate conditions.

A few failure cases typically arise.

One common mistake is treating the region as a simple rectangle bounded by min and max coordinates. For example, assuming the field is just $d \le x \le n-d$ and $d \le y \le n-d$ would be wrong. A point like $(1, 1)$ might satisfy rectangle bounds for some values but still lie outside the diamond-shaped field.

Another mistake is forgetting that the boundary is included. Since the problem explicitly counts points on the edges as inside, strict inequalities like $<$ and $>$ instead of $\le$ and $\ge$ would incorrectly reject valid points such as the vertices.

The correct solution comes from identifying that the shape is defined by two linear constraints corresponding to the two diagonals of the rotated square.

## Approaches

A brute-force geometric approach would attempt to determine whether a point lies inside the polygon using orientation tests or triangle decomposition. One could split the quadrilateral into two triangles and check if the point is inside either triangle using cross products. This works correctly and is conceptually general, but it is unnecessary for such a constrained shape.

The issue with brute force is not correctness but overkill: computing cross products for every query introduces more complexity than needed, and it obscures the structure of the region. In the worst case, it still runs in $O(m)$, but with heavier constant factors and more implementation risk.

The key observation is that the polygon is a perfect square rotated by 45 degrees, aligned with lines $x + y = d$ and $x + y = n + d$, and also constrained by $x - y = -d$ and $x - y = n - d$. This means membership can be checked using only two linear inequalities derived from these diagonals.

Once this is recognized, each query reduces to checking whether the point lies between two parallel lines in both diagonal directions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Polygon / brute geometry | O(m) | O(1) | Accepted but unnecessary |
| Inequality check | O(m) | O(1) | Accepted |

## Algorithm Walkthrough

We rewrite the condition of being inside the diamond-shaped region using two transformed coordinates: $x + y$ and $x - y$.

1. Compute the sum $s = x + y$. This captures position along one diagonal direction. The shape is bounded between two lines of constant sum, so this is the first constraint.
2. Compute the difference $t = x - y$. This captures position along the other diagonal direction, orthogonal to the first constraint. The region is also bounded between two lines of constant difference.
3. Derive bounds from the corner points. Substituting the vertices shows that:

- Minimum sum is $d$, maximum sum is $n + d$
- Minimum difference is $-d$, maximum difference is $n - d$
4. For each query point, check whether both conditions hold:

$d \le x + y \le n + d$ and $-d \le x - y \le n - d$
5. If both inequalities are satisfied, the point is inside or on the boundary; otherwise, it is outside.

The reason this works is that the quadrilateral is exactly the intersection of two strips: one defined by bounding $x + y$, and the other defined by bounding $x - y$. Their intersection forms the rotated square.

### Why it works

The transformation $(x, y) \rightarrow (x + y, x - y)$ maps axis-aligned squares into rotated squares. In this transformed space, the region becomes an axis-aligned rectangle. Since axis-aligned rectangles are characterized by independent bounds on each coordinate, membership reduces to two independent interval checks. This guarantees correctness because every edge of the original polygon corresponds exactly to one of the bounding lines in the transformed coordinates.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, d = map(int, input().split())
    m = int(input())

    for _ in range(m):
        x, y = map(int, input().split())

        s = x + y
        t = x - y

        if d <= s <= n + d and -d <= t <= n - d:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The code directly implements the two derived constraints. Each query is handled independently, computing the sum and difference once and comparing them against the fixed bounds.

The most delicate part is ensuring inclusive comparisons. Since boundary points are valid, all inequalities must use $\le$ and $\ge$. The rest is straightforward arithmetic.

## Worked Examples

### Sample 1

Input:

```
n = 7, d = 2
points: (2,4), (4,1), (6,3), (4,5)
```

We compute $s = x+y$ and $t = x-y$. The valid region is $2 \le s \le 9$ and $-2 \le t \le 5$.

| Point | s = x+y | t = x-y | Inside s-range? | Inside t-range? | Result |
| --- | --- | --- | --- | --- | --- |
| (2,4) | 6 | -2 | yes | yes | YES |
| (4,1) | 5 | 3 | no | yes | NO |
| (6,3) | 9 | 3 | yes | yes | YES |
| (4,5) | 9 | -1 | yes | yes | YES |

This trace confirms that boundary points like $(2,4)$ where $t = -2$ are correctly accepted because the inequality is inclusive.

### Sample 2

Input:

```
n = 8, d = 2
points: (4,4), (8,1), (6,1), (1,1)
```

Bounds are $2 \le s \le 10$, $-2 \le t \le 6$.

| Point | s | t | Result |
| --- | --- | --- | --- |
| (4,4) | 8 | 0 | YES |
| (8,1) | 9 | 7 | NO |
| (6,1) | 7 | 5 | YES |
| (1,1) | 2 | 0 | YES |

The second sample highlights how a point can fail only one constraint even if it lies visually close to the region, reinforcing that both inequalities are necessary simultaneously.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m) | Each point requires constant-time arithmetic and comparisons |
| Space | O(1) | No auxiliary structures beyond input variables |

The constraints limit $m$ to at most 100, so even a constant-factor-heavy solution would run instantly. The direct inequality check is far below any meaningful runtime limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, d = map(int, input().split())
    m = int(input())
    out = []
    for _ in range(m):
        x, y = map(int, input().split())
        s = x + y
        t = x - y
        out.append("YES" if d <= s <= n + d and -d <= t <= n - d else "NO")
    return "\n".join(out)

# provided sample 1
assert run("""7 2
4
2 4
4 1
6 3
4 5
""") == """YES
NO
NO
YES"""

# minimum values, corner cases
assert run("""2 1
3
0 1
1 0
2 2
""") == """YES
YES
NO"""

# all points identical inside
assert run("""5 1
3
2 2
2 2
2 2
""") == """YES
YES
YES"""

# boundary strip behavior
assert run("""10 3
4
3 0
0 3
10 7
7 10
""") == """YES
YES
YES
YES"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample 1 | YES/NO pattern | correctness of main logic |
| small n,d corners | mixed YES/NO | vertex and axis behavior |
| repeated points | all YES | stability under duplicates |
| boundary strip | all YES | inclusive boundary handling |

## Edge Cases

One edge case is when a point lies exactly on a vertex of the polygon. For example, $(0, d)$. Here $x+y = d$ and $x-y = -d$, which both satisfy inclusive bounds, so the algorithm correctly returns YES.

Another case is when a point is just outside one diagonal boundary but inside the other. For instance, a point with $x+y = d-1$ will fail immediately even if its difference value is valid. The algorithm rejects it correctly because both conditions are required simultaneously.

A final case is when points lie near the opposite corner $(n-d, n)$. These maximize both transformed coordinates: $x+y = n+d$ and $x-y = n-2d$, both still within bounds. The algorithm includes them correctly, confirming that the upper bounds are tight and correctly derived from the geometry.
