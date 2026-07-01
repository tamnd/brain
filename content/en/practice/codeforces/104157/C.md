---
title: "CF 104157C - Flush-tastic Throwing Challenge"
description: "We are given a circular target on a 2D plane and a list of points representing where different employees threw an object. The task is to count how many of these thrown points land inside the circle or exactly on its boundary. Each throw is just a coordinate pair."
date: "2026-07-02T01:14:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104157
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 01-27-23 Div. 2 (Beginner)"
rating: 0
weight: 104157
solve_time_s: 74
verified: true
draft: false
---

[CF 104157C - Flush-tastic Throwing Challenge](https://codeforces.com/problemset/problem/104157/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a circular target on a 2D plane and a list of points representing where different employees threw an object. The task is to count how many of these thrown points land inside the circle or exactly on its boundary.

Each throw is just a coordinate pair. The circle is defined by its center and radius. A throw is successful if its Euclidean distance from the center is less than or equal to the radius.

The constraints are large enough that any solution must process each point in constant time. With up to 100,000 throws, an $O(n)$ solution is expected. Anything involving sorting or pairwise comparisons would be unnecessary and too slow.

A subtle issue that often appears in problems like this is numerical safety when computing distances. The naive formula involves a square root, and floating-point comparisons can introduce precision errors. Another common pitfall is using 32-bit integers when squaring coordinates up to $10^9$, which overflows immediately.

A few edge situations matter:

A point exactly on the boundary should be counted as successful. For example, if the center is $(0,0)$ and radius is $5$, the point $(3,4)$ must be counted because $3^2 + 4^2 = 25$.

A second subtle case is large coordinates. If we compute $(x - c_x)^2$ using 32-bit integers, values near $10^9$ produce around $10^{18}$, which requires 64-bit arithmetic. Using the wrong type silently produces incorrect results.

## Approaches

The direct way to solve the problem is to process each throw independently and compute its distance to the circle center. For each point, we calculate the Euclidean distance using the formula $\sqrt{(x_i - c_x)^2 + (y_i - c_y)^2}$, and check whether it is less than or equal to $r$. This is correct because the definition of “inside a circle” is exactly that distance condition.

However, this involves a square root for every point. While $O(n)$ is fine in terms of asymptotic complexity, square root operations are comparatively expensive and unnecessary. More importantly, floating-point comparisons can introduce precision errors near the boundary, where a point should be included but might be excluded due to rounding.

The key observation is that we never need the actual distance. We only need to compare it with the radius. Since both sides are non-negative, we can safely square both sides of the inequality:

$$(x_i - c_x)^2 + (y_i - c_y)^2 \le r^2$$

This removes the square root entirely and converts the problem into simple integer arithmetic. Now each point requires only a few integer operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (sqrt per point) | O(n) | O(1) | Accepted but fragile |
| Squared distance check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of points, the circle center coordinates, and the radius. We immediately compute $r^2$ so we never need to recompute it during processing. This avoids repeated multiplication and keeps comparisons uniform.
2. Initialize a counter to zero. This will track how many points satisfy the circle condition.
3. For each throw $(x_i, y_i)$, compute the horizontal and vertical offsets from the center: $dx = x_i - c_x$, $dy = y_i - c_y$. These offsets represent the displacement vector from the center to the point.
4. Compute the squared distance $dx^2 + dy^2$. This is the exact squared Euclidean distance from the center. We intentionally avoid square roots because they are unnecessary for comparison.
5. Compare the squared distance with $r^2$. If it is less than or equal, increment the counter. This directly corresponds to the definition of being inside or on the boundary of the circle.
6. After processing all points, output the counter.

### Why it works

The correctness rests on the fact that squaring is monotonic over non-negative values. Since both the squared distance and $r^2$ are always non-negative, comparing them preserves the ordering of the original distances. This means the inequality after squaring is equivalent to the original geometric condition. Every point is classified exactly as it would be under true Euclidean distance, but without introducing floating-point computation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, cx, cy, r = map(int, input().split())
    r2 = r * r

    cnt = 0
    for _ in range(n):
        x, y = map(int, input().split())
        dx = x - cx
        dy = y - cy
        if dx * dx + dy * dy <= r2:
            cnt += 1

    print(cnt)

if __name__ == "__main__":
    solve()
```

The implementation follows the algorithm directly. The preprocessing step stores $r^2$, ensuring each query only performs a fixed number of arithmetic operations.

The subtraction step is important because it reduces coordinates into a local frame centered at the circle origin. This avoids any need for absolute positions.

All arithmetic is done using Python integers, which naturally support large values, so there is no overflow risk.

## Worked Examples

### Example 1

Input:

```
4 1 2 5
0 0
-2 -2
5 6
3 3
```

We compute $r^2 = 25$.

| Point | dx | dy | dx² + dy² | ≤ 25 | Count |
| --- | --- | --- | --- | --- | --- |
| (0,0) | -1 | -2 | 1 + 4 = 5 | yes | 1 |
| (-2,-2) | -3 | -4 | 9 + 16 = 25 | yes | 2 |
| (5,6) | 4 | 4 | 16 + 16 = 32 | no | 2 |
| (3,3) | 2 | 1 | 4 + 1 = 5 | yes | 3 |

The trace shows that boundary equality is accepted, as seen in the second point where the squared distance equals 25.

### Example 2

Input:

```
3 0 0 2
2 0
0 2
2 2
```

We compute $r^2 = 4$.

| Point | dx | dy | dx² + dy² | ≤ 4 | Count |
| --- | --- | --- | --- | --- | --- |
| (2,0) | 2 | 0 | 4 | yes | 1 |
| (0,2) | 0 | 2 | 4 | yes | 2 |
| (2,2) | 2 | 2 | 8 | no | 2 |

This example isolates a corner case where points exactly on the circle boundary are included, while points just outside are excluded cleanly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each point requires constant-time arithmetic and comparison |
| Space | O(1) | Only a few variables are used regardless of input size |

The solution scales directly with the number of throws, which is optimal given that every point must be inspected at least once. With $n \le 10^5$, this runs comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import sys as _sys
    backup = _sys.stdout
    _sys.stdout = io.StringIO()
    solve()
    out = _sys.stdout.getvalue().strip()
    _sys.stdout = backup
    return out

# provided sample
assert run("""4 1 2 5
0 0
-2 -2
5 6
3 3
""") == "3"

# minimum case
assert run("""1 0 0 1
0 0
""") == "1"

# all outside
assert run("""3 0 0 1
2 0
0 2
-2 -2
""") == "0"

# all inside large radius
assert run("""3 0 0 100
10 10
-20 -30
40 50
""") == "3"

# boundary stress case
assert run("""2 0 0 5
3 4
-3 -4
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single center hit | 1 | minimum size correctness |
| all outside small radius | 0 | rejection logic |
| large radius | all points | acceptance scaling |
| 3-4-5 boundary points | 2 | exact boundary handling |

## Edge Cases

One important edge case is when a point lies exactly on the circle boundary. Consider input:

```
1 0 0 5
3 4
```

The algorithm computes $dx = 3$, $dy = 4$, and $dx^2 + dy^2 = 25$. Since $r^2 = 25$, the condition is satisfied and the point is counted. This confirms correct inclusion of boundary points without requiring floating-point tolerance.

Another edge case is large coordinate values:

```
1 1000000000 -1000000000 1
1000000000 -999999999
```

Here $dx = 0$, $dy = 1$, so squared distance is 1. Even though intermediate coordinate values are huge, Python’s integer arithmetic handles them safely, and the comparison remains correct.
