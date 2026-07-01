---
title: "CF 104158C - Flush-tastic Throwing Challenge"
description: "We are given a circular target on a 2D plane and a set of points representing where employees throw an object. The task is to count how many of these points land inside or exactly on the boundary of the circle. Each throw is just a coordinate on the plane."
date: "2026-07-02T01:09:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104158
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 01-27-23 Div. 1 (Advanced)"
rating: 0
weight: 104158
solve_time_s: 61
verified: true
draft: false
---

[CF 104158C - Flush-tastic Throwing Challenge](https://codeforces.com/problemset/problem/104158/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a circular target on a 2D plane and a set of points representing where employees throw an object. The task is to count how many of these points land inside or exactly on the boundary of the circle.

Each throw is just a coordinate on the plane. The target is defined by its center $(c_x, c_y)$ and a radius $r$. A throw is successful if its distance to the center of the circle is less than or equal to $r$.

The main quantity we need is the Euclidean distance between each point and the center. However, computing square roots for up to $10^5$ points is unnecessary and can introduce floating point precision issues. The decision can be made using squared distances instead.

The constraints are tight enough that an $O(n)$ solution is expected. Since $n \leq 10^5$, any approach that processes each point in constant time is sufficient. Anything involving sorting or pairwise comparisons would be excessive.

A subtle edge case arises when a point lies exactly on the boundary of the circle. For example, if the center is $(0, 0)$, radius is $5$, and a point is $(3, 4)$, the distance is exactly $5$, so it must be counted as successful. This is easy to mishandle if strict inequality is used instead of inclusive comparison.

Another potential pitfall is integer overflow in languages with fixed-width integers, because coordinates can be as large as $10^9$. Squaring differences can reach up to $10^{18}$, so 64-bit integers are required. In Python this is safe, but the reasoning still matters for translation.

## Approaches

The straightforward approach is to compute the Euclidean distance for every point, take a square root, and check whether it is less than or equal to $r$. This is correct because it directly implements the geometric definition of a circle. However, it performs an expensive square root operation for every employee, leading to $O(n)$ square root calls. While still linear, this is slower than necessary and risks precision issues when comparing floating-point values near the boundary.

The key observation is that the square root is monotonic. Comparing distances is equivalent to comparing squared distances. Instead of checking

$$\sqrt{(x - c_x)^2 + (y - c_y)^2} \le r$$

we can safely square both sides:

$$(x - c_x)^2 + (y - c_y)^2 \le r^2$$

This removes floating-point arithmetic entirely and reduces the operation per point to a few integer subtractions and multiplications. The problem becomes a simple linear scan with constant-time checks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (with sqrt) | O(n) | O(1) | Accepted but slower and riskier |
| Squared distance check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of throws and the circle parameters $c_x, c_y, r$. This defines the fixed reference point and threshold for all computations.
2. Precompute $r^2$. This avoids recomputing it for every point and ensures all comparisons stay in integer arithmetic.
3. Initialize a counter to zero. This will track how many throws land inside or on the boundary of the circle.
4. For each employee’s throw at $(x_i, y_i)$, compute the horizontal and vertical offsets from the center: $dx = x_i - c_x$, $dy = y_i - c_y$. This transforms the problem into measuring distance from the origin in a shifted coordinate system.
5. Compute the squared distance $d = dx^2 + dy^2$. This represents the exact squared Euclidean distance from the center.
6. Compare $d$ with $r^2$. If $d \le r^2$, increment the counter. The equality case is included because points on the boundary are considered successful.
7. After processing all points, output the counter.

### Why it works

The algorithm relies on the fact that squaring is strictly monotonic for non-negative values. Since both the squared distance and $r^2$ are non-negative, comparing squared values preserves the ordering of actual distances. Every point is classified based on an equivalent condition, so no geometric case is misclassified. The transformation from Euclidean distance to squared distance preserves correctness while removing floating-point computation entirely.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, cx, cy, r = map(int, input().split())
    r2 = r * r
    ans = 0

    for _ in range(n):
        x, y = map(int, input().split())
        dx = x - cx
        dy = y - cy
        if dx * dx + dy * dy <= r2:
            ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by reading all inputs in constant time per line. The squared radius is computed once, which avoids repeated multiplication inside the loop. Each point is processed independently, computing its offset from the center before evaluating the squared distance condition.

The comparison uses `<=` rather than `<`, which is essential because boundary points are valid hits. All arithmetic is performed using Python integers, which naturally handle large values without overflow.

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

| Point | dx | dy | dx² + dy² | ≤ 25 |
| --- | --- | --- | --- | --- |
| (0,0) | -1 | -2 | 1 + 4 = 5 | yes |
| (-2,-2) | -3 | -4 | 9 + 16 = 25 | yes |
| (5,6) | 4 | 4 | 16 + 16 = 32 | no |
| (3,3) | 2 | 1 | 4 + 1 = 5 | yes |

Answer is 3.

This trace shows that equality at 25 is accepted, confirming correct boundary handling.

### Example 2

Input:

```
3 0 0 3
3 0
2 2
0 4
```

We compute $r^2 = 9$.

| Point | dx | dy | dx² + dy² | ≤ 9 |
| --- | --- | --- | --- | --- |
| (3,0) | 3 | 0 | 9 | yes |
| (2,2) | 2 | 2 | 8 | yes |
| (0,4) | 0 | 4 | 16 | no |

Answer is 2.

This confirms that points strictly outside the circle are correctly excluded even when one coordinate is large.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each point is processed once with constant-time arithmetic |
| Space | O(1) | Only a few scalar variables are used |

The solution is optimal for $n \leq 10^5$. Each iteration uses only a handful of integer operations, which comfortably fits within the 1-second limit in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue() if False else __import__("builtins").print(solve())

# Re-define properly for isolated runs
def run(inp: str) -> str:
    import sys, io
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = backup_stdin
        sys.stdout = backup_stdout

# provided sample
assert run("""4 1 2 5
0 0
-2 -2
5 6
3 3
""") == "3"

# minimum input
assert run("""1 0 0 1
0 0
""") == "1"

# boundary-only hit
assert run("""2 0 0 5
3 4
-3 -4
""") == "2"

# all outside
assert run("""3 0 0 2
3 3
-3 -3
5 0
""") == "0"

# large coordinate edge
assert run("""2 1000000000 -1000000000 1
1000000000 -999999999
0 0
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point at center | 1 | minimum case correctness |
| (3,4) style boundary hits | 2 | exact circle boundary |
| all outside points | 0 | strict rejection |
| large coordinates near limit | 1 | overflow-safe arithmetic |

## Edge Cases

One edge case is when a point lies exactly at distance $r$. For example, center $(0,0)$, radius $5$, point $(3,4)$. The algorithm computes $dx^2 + dy^2 = 25$, which is equal to $r^2$, so it is correctly counted. This confirms the inclusive boundary condition.

Another edge case is when coordinates are extremely large, such as $(10^9, -10^9)$. The squared distance becomes about $2 \cdot 10^{18}$, which still fits safely in Python integers. The algorithm remains correct because it never relies on floating-point precision.

A final case is when all points coincide with the center. Every $dx$ and $dy$ becomes zero, so all points are counted, matching the geometric definition of a circle containing its center.
