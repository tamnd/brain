---
title: "CF 1998A - Find K Distinct Points with Fixed Center"
description: "We are given a target center point $(xc, yc)$ and an integer $k$. The task is not to optimize anything or search for a special configuration. We simply need to construct exactly $k$ distinct integer-coordinate points whose arithmetic mean is exactly $(xc, yc)$."
date: "2026-06-08T14:27:44+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1998
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 965 (Div. 2)"
rating: 800
weight: 1998
solve_time_s: 142
verified: false
draft: false
---

[CF 1998A - Find K Distinct Points with Fixed Center](https://codeforces.com/problemset/problem/1998/A)

**Rating:** 800  
**Tags:** constructive algorithms, implementation, math  
**Solve time:** 2m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a target center point $(x_c, y_c)$ and an integer $k$. The task is not to optimize anything or search for a special configuration. We simply need to construct exactly $k$ distinct integer-coordinate points whose arithmetic mean is exactly $(x_c, y_c)$.

The center condition means:

$$\frac{\sum x_i}{k} = x_c,
\qquad
\frac{\sum y_i}{k} = y_c$$

Equivalently,

$$\sum x_i = k \cdot x_c,
\qquad
\sum y_i = k \cdot y_c.$$

The coordinates of every generated point must stay within $[-10^9,10^9]$, but the given center coordinates are only between $-100$ and $100$, and $k \le 1000$. This is extremely small compared to the allowed coordinate range, so we have enormous freedom when constructing points.

The total sum of all $k$ values across test cases is at most $1000$. Even an $O(k)$ construction per test case is more than enough.

The main danger is accidentally producing duplicate points or producing points whose average is only approximately correct. Since the answer is constructive, every generated point must satisfy the center equation exactly.

Consider $k=1$. For example:

```
10 10 1
```

The only possible center of a single point is the point itself, so we must output:

```
10 10
```

A construction that always creates symmetric pairs would fail because there is no partner point available.

Another subtle case is odd $k$.

For example:

```
0 0 3
```

If we output only one symmetric pair:

```
1 0
-1 0
```

we have only two points. We need a third distinct point while keeping the total sum unchanged. A careless construction may add $(0,0)$ even when it duplicates an existing point.

Finally, all points must be distinct. For example:

```
0 0 2
```

Outputting

```
0 0
0 0
```

has the correct center but violates the distinctness requirement.

## Approaches

A brute-force mindset would be to search for arbitrary integer points and repeatedly check whether their average equals the desired center. Since infinitely many valid configurations exist, such a search eventually succeeds. The problem is that there is no meaningful upper bound on how long the search may take, and correctness becomes difficult to guarantee.

The structure of the center formula gives a much cleaner approach. If two points are placed symmetrically around the center,

$$(x_c-d, y_c)$$

and

$$(x_c+d, y_c),$$

their contribution to the coordinate sums is

$$2x_c,\quad 2y_c.$$

In other words, the pair's average is already exactly the center. Any number of such symmetric pairs can be combined without changing the final center.

This observation immediately suggests a construction.

If $k$ is even, create $k/2$ symmetric pairs around $(x_c,y_c)$.

If $k$ is odd, first place the center point itself. Its contribution is exactly $(x_c,y_c)$. Then construct $(k-1)/2$ symmetric pairs around it.

Using distances $1,2,3,\ldots$ guarantees that every generated point is distinct.

Since $k \le 1000$, the largest offset we use is at most $500$, so all coordinates remain comfortably inside the allowed range.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Unbounded | Unbounded | Not practical |
| Optimal | O(k) | O(1) excluding output | Accepted |

## Algorithm Walkthrough

1. Read $x_c$, $y_c$, and $k$.
2. Create an empty answer list.
3. If $k$ is odd, add the center point $(x_c,y_c)$ to the answer.

This point contributes exactly one copy of the center to the total sum.
4. For each distance $d = 1,2,\ldots,\lfloor k/2 \rfloor$, add the two points:

$$(x_c-d,\ y_c)$$

and

$$(x_c+d,\ y_c).$$
5. Output all generated points.

### Why it works

Every generated pair is symmetric around the center. The sum of their coordinates is

$$(x_c-d)+(x_c+d)=2x_c,$$

and

$$y_c+y_c=2y_c.$$

Thus each pair has average $(x_c,y_c)$.

If $k$ is even, we have exactly $k/2$ such pairs. The total coordinate sum becomes

$$kx_c,\quad ky_c,$$

so the center is correct.

If $k$ is odd, we additionally include $(x_c,y_c)$. The remaining $k-1$ points form symmetric pairs whose total contribution is

$$(k-1)x_c,\quad (k-1)y_c.$$

Adding the center point gives

$$kx_c,\quad ky_c.$$

All distances are different, so no two generated points coincide. Hence the construction always produces $k$ distinct integer-coordinate points with the required center.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

out = []

for _ in range(t):
    xc, yc, k = map(int, input().split())

    if k % 2 == 1:
        out.append(f"{xc} {yc}")

    for d in range(1, k // 2 + 1):
        out.append(f"{xc - d} {yc}")
        out.append(f"{xc + d} {yc}")

sys.stdout.write("\n".join(out))
```

The implementation follows the construction directly.

For odd $k$, the center point is emitted first. This handles the unmatched point while preserving the required average.

The loop generates symmetric pairs using increasing distances from the center. Using different distances guarantees distinct points automatically. Since the maximum distance is at most $500$, every coordinate remains far from the $\pm 10^9$ limits.

No floating-point arithmetic appears anywhere. The proof relies entirely on exact integer sums, eliminating any precision issues.

## Worked Examples

### Example 1

Input:

```
0 0 3
```

| Step | d | Generated point |
| --- | --- | --- |
| Odd k | - | (0, 0) |
| Pair | 1 | (-1, 0) |
| Pair | 1 | (1, 0) |

Coordinate sums:

| x-sum | y-sum | Number of points |
| --- | --- | --- |
| 0 | 0 | 3 |

Average:

$$(0/3,\;0/3)=(0,0)$$

This example demonstrates the odd-$k$ case. The center point absorbs the extra point while the symmetric pair contributes zero net displacement.

### Example 2

Input:

```
4 -5 4
```

| Step | d | Generated point |
| --- | --- | --- |
| Pair | 1 | (3, -5) |
| Pair | 1 | (5, -5) |
| Pair | 2 | (2, -5) |
| Pair | 2 | (6, -5) |

Coordinate sums:

| x-sum | y-sum | Number of points |
| --- | --- | --- |
| 16 | -20 | 4 |

Average:

$$(16/4,\;-20/4)=(4,-5)$$

This example shows that multiple symmetric pairs can be stacked independently and still preserve the same center.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) | Each point is generated exactly once |
| Space | O(1) excluding output | Only a few variables are maintained |

The total sum of all $k$ values across test cases is at most $1000$. Generating each point once is trivial within the time limit, and memory usage is negligible.

## Test Cases

```
# helper: verify construction rather than exact output

def check(points, xc, yc, k):
    assert len(points) == k
    assert len(set(points)) == k

    sx = sum(x for x, y in points)
    sy = sum(y for x, y in points)

    assert sx == xc * k
    assert sy == yc * k

# sample-style case
pts = [(10, 10)]
check(pts, 10, 10, 1)

# minimum size
pts = [(0, 0)]
check(pts, 0, 0, 1)

# even k
pts = [(-1, 0), (1, 0)]
check(pts, 0, 0, 2)

# odd k
pts = [(5, -3), (4, -3), (6, -3)]
check(pts, 5, -3, 3)

# larger case
xc, yc, k = -100, 100, 1000
pts = []
for d in range(1, k // 2 + 1):
    pts.append((xc - d, yc))
    pts.append((xc + d, yc))
check(pts, xc, yc, k)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| $x_c=0,y_c=0,k=1$ | Single center point | Minimum case |
| $x_c=0,y_c=0,k=2$ | One symmetric pair | Even $k$ |
| $x_c=5,y_c=-3,k=3$ | Center plus pair | Odd $k$ |
| $x_c=-100,y_c=100,k=1000$ | Many pairs | Maximum $k$ |
| Negative coordinates | Valid center maintained | Sign handling |

## Edge Cases

### Edge Case 1: $k=1$

Input:

```
10 10 1
```

The algorithm enters the odd-$k$ branch and outputs:

```
10 10
```

The coordinate sums are $(10,10)$, and dividing by one gives the required center. No symmetric pair is needed.

### Edge Case 2: Small odd $k$

Input:

```
0 0 3
```

The algorithm outputs:

```
0 0
-1 0
1 0
```

The sums are:

$$0 + (-1) + 1 = 0,$$

$$0 + 0 + 0 = 0.$$

The center remains $(0,0)$, and all points are distinct.

### Edge Case 3: Maximum $k$

Input:

```
-100 100 1000
```

The largest distance used is $500$. Generated x-coordinates range from

$$-100-500=-600$$

to

$$-100+500=400.$$

These values are nowhere near the allowed bounds of $\pm 10^9$. Distinctness is preserved because every distance is unique.

### Edge Case 4: Negative center coordinates

Input:

```
-5 -8 8
```

Generated points are:

```
-6 -8
-4 -8
-7 -8
-3 -8
-8 -8
-2 -8
-9 -8
-1 -8
```

Each pair remains symmetric around $(-5,-8)$. The sign of the coordinates has no effect on the correctness argument, since the proof depends only on pairwise cancellation around the center.
