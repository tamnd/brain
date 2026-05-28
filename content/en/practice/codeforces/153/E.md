---
title: "CF 153E - Euclidean Distance"
description: "We are given up to 50 points on a 2D plane. Each point has integer coordinates, and some points may coincide. The task is to find the largest Euclidean distance between any pair of points."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 153
codeforces_index: "E"
codeforces_contest_name: "Surprise Language Round 5"
rating: 2100
weight: 153
solve_time_s: 93
verified: false
draft: false
---

[CF 153E - Euclidean Distance](https://codeforces.com/problemset/problem/153/E)

**Rating:** 2100  
**Tags:** *special  
**Solve time:** 1m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are given up to 50 points on a 2D plane. Each point has integer coordinates, and some points may coincide. The task is to find the largest Euclidean distance between any pair of points.

For two points $(x_1, y_1)$ and $(x_2, y_2)$, the Euclidean distance is:

$d=\sqrt{(x_1-x_2)^2+(y_1-y_2)^2}$Drag the points to update the distance between two points.-10-8-6-4-2246810-10-5510A(6.0, 6.0)B(-6.0, -6.0)d = 16.97Delta x = 12Delta y = 12

The input format is slightly unusual because each coordinate is given on its own line. After reading `n`, we read `2n` more lines: one `x`, one `y`, repeated for every point.

The constraints are extremely small. With only 50 points, the total number of pairs is at most:

$\frac{50\cdot49}{2}=1225$

That is tiny for a 2 second limit. Even an $O(n^2)$ algorithm performs only a few thousand distance computations, which is trivial.

The main danger is not performance but correctness and precision.

One easy mistake is forgetting that the Euclidean distance uses a square root. A careless implementation might maximize squared distance and print it directly.

Example:

```
2
0
0
3
4
```

The correct answer is:

```
5
```

because:

$\sqrt{3^2+4^2}=5$

Printing `25` instead would be wrong.

Another subtle case is duplicate points.

```
3
1
1
1
1
4
5
```

Two points are identical, so their distance is zero. The correct maximum distance is between `(1,1)` and `(4,5)`.

A buggy implementation that assumes all points are distinct could accidentally skip valid comparisons or mishandle indexing.

Floating-point output formatting is another common source of issues. The judge accepts a small error tolerance, so printing with standard floating-point precision is enough, but integer division or truncation would fail.

## Approaches

The most direct solution is brute force. We check every pair of points, compute the Euclidean distance between them, and keep the maximum value seen so far.

This works because the answer is literally defined as the maximum over all pairs. If we examine every pair exactly once, we cannot miss the optimal one.

The brute-force algorithm performs:

$O(n^2)$

distance computations. With `n = 50`, that means at most 1225 pairs, which is negligible.

For larger constraints, this approach would become problematic. If `n` were $10^5$, pairwise checking would require roughly $10^{10}$ operations, which is impossible within the time limit. In those settings, computational geometry techniques such as convex hulls and rotating calipers become necessary because the farthest pair must lie on the convex hull.

This problem does not require those optimizations. The constraints are intentionally small enough that the simple pairwise solution is already optimal in practice. The key observation is that trying to build a more advanced geometry algorithm would only add complexity without any benefit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Geometry Optimization | O(n log n) | O(n) | Unnecessary |

## Algorithm Walkthrough

1. Read the integer `n`.
2. Read all points into a list of `(x, y)` pairs.
3. Initialize a variable `best = 0.0`.
4. Iterate over every pair of indices `(i, j)` with `i < j`.
5. For each pair, compute the coordinate differences:

$dx=x_i-x_j$

$dy=y_i-y_j$
6. Compute the Euclidean distance:

$d=\sqrt{dx^2+dy^2}$
7. Update `best` if this distance is larger.
8. After all pairs are processed, print `best`.

### Why it works

The algorithm explicitly evaluates the distance for every possible pair of points. Since the definition of the answer is the maximum distance among all pairs, the optimal pair is guaranteed to appear during iteration. Whenever a larger distance is found, `best` is updated. After the loop finishes, `best` equals the maximum distance over the complete set of pairs, which is exactly the required answer.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

# solution
def solve():
    n = int(input())
    
    points = []
    for _ in range(n):
        x = int(input())
        y = int(input())
        points.append((x, y))
    
    best = 0.0
    
    for i in range(n):
        x1, y1 = points[i]
        
        for j in range(i + 1, n):
            x2, y2 = points[j]
            
            dx = x1 - x2
            dy = y1 - y2
            
            dist = math.sqrt(dx * dx + dy * dy)
            best = max(best, dist)
    
    print(best)

if __name__ == "__main__":
    solve()
```

The first section reads all points into a list. Since coordinates are split across separate lines, we read two integers per point and store them together as a tuple.

The nested loops enumerate every unordered pair exactly once. Using `j` from `i + 1` avoids duplicate comparisons like `(A,B)` and `(B,A)`, and also skips comparing a point with itself.

Distance computation uses squared differences before taking the square root. The coordinates are small enough that overflow is impossible in Python, but using squared terms directly still avoids unnecessary floating-point operations until the final step.

The answer variable starts at `0.0` because distances are non-negative. Every computed distance is compared against the current maximum.

The final print statement uses Python's default floating-point formatting, which already provides enough precision for the judge's tolerance requirement.

## Worked Examples

### Example 1

Input:

```
3
0
1
2
3
4
5
```

The points are:

```
(0,1), (2,3), (4,5)
```

| i | j | Point A | Point B | Distance | best |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | (0,1) | (2,3) | 2.828427 | 2.828427 |
| 0 | 2 | (0,1) | (4,5) | 5.656854 | 5.656854 |
| 1 | 2 | (2,3) | (4,5) | 2.828427 | 5.656854 |

The farthest pair is `(0,1)` and `(4,5)`. The trace shows that once the maximum is found, later comparisons cannot overwrite it unless they are larger.

### Example 2

Input:

```
3
1
1
1
1
4
5
```

The points are:

```
(1,1), (1,1), (4,5)
```

| i | j | Point A | Point B | Distance | best |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | (1,1) | (1,1) | 0.000000 | 0.000000 |
| 0 | 2 | (1,1) | (4,5) | 5.000000 | 5.000000 |
| 1 | 2 | (1,1) | (4,5) | 5.000000 | 5.000000 |

This example demonstrates that duplicate points do not cause any issues. Their pairwise distance is simply zero, and the algorithm still correctly identifies the farthest pair.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Every pair of points is checked once |
| Space | O(n) | The list of points is stored |

With `n ≤ 50`, the algorithm performs at most 1225 distance computations. That is tiny compared to the available limits, so the solution comfortably fits within both time and memory constraints.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
import math

def solve():
    input = sys.stdin.readline

    n = int(input())

    points = []
    for _ in range(n):
        x = int(input())
        y = int(input())
        points.append((x, y))

    best = 0.0

    for i in range(n):
        x1, y1 = points[i]

        for j in range(i + 1, n):
            x2, y2 = points[j]

            dx = x1 - x2
            dy = y1 - y2

            dist = math.sqrt(dx * dx + dy * dy)
            best = max(best, dist)

    print(best)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
ans = float(run(
"""3
0
1
2
3
4
5
"""))
assert abs(ans - 5.656854249) < 1e-6, "sample 1"

# minimum size
ans = float(run(
"""2
0
0
3
4
"""))
assert abs(ans - 5.0) < 1e-6, "minimum case"

# all points equal
ans = float(run(
"""4
2
2
2
2
2
2
2
2
"""))
assert abs(ans - 0.0) < 1e-6, "all equal"

# boundary coordinates
ans = float(run(
"""2
-50
-50
50
50
"""))
assert abs(ans - 141.421356237) < 1e-6, "boundary coordinates"

# off-by-one style check
ans = float(run(
"""3
0
0
1
1
10
10
"""))
assert abs(ans - 14.1421356237) < 1e-6, "largest pair at end"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two points `(0,0)` and `(3,4)` | `5` | Minimum valid input size |
| All points `(2,2)` | `0` | Duplicate points and zero distance |
| `(-50,-50)` and `(50,50)` | `141.421356...` | Boundary coordinates |
| Largest pair appears last | `14.142135...` | Correct pair iteration |

## Edge Cases

Consider duplicate points:

```
3
5
5
5
5
8
9
```

The algorithm compares the first two points and computes distance `0`. That does not affect correctness because `best` remains the maximum seen so far. When `(5,5)` and `(8,9)` are checked, the distance becomes:

$\sqrt{3^2+4^2}=5$

The final answer is `5`.

Now consider boundary coordinates:

```
2
-50
-50
50
50
```

The algorithm computes:

$dx=-100$

$dy=-100$

and then:

$\sqrt{100^2+100^2}=141.421356\ldots$

The coordinate limits are small, so squaring values is completely safe.

Finally, consider a case where the optimal pair appears late in iteration order:

```
3
0
0
1
1
10
10
```

The first comparison gives distance about `1.414`. A buggy implementation that stops early or initializes incorrectly could fail here. The algorithm continues through all pairs and eventually checks `(0,0)` with `(10,10)`, producing the correct maximum `14.142135...`.
