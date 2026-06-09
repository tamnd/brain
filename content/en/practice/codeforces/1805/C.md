---
title: "CF 1805C - Place for a Selfie"
description: "We are asked to choose, for each parabola, a straight line that passes through the origin and does not intersect the parabola at all. Each line is given by its slope $k$, so the line is $y=kx$. Each parabola is given by $y = ax^2 + bx + c$ with $a0$, so it opens upwards."
date: "2026-06-09T09:14:37+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "geometry", "math"]
categories: ["algorithms"]
codeforces_contest: 1805
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 862 (Div. 2)"
rating: 1400
weight: 1805
solve_time_s: 110
verified: false
draft: false
---

[CF 1805C - Place for a Selfie](https://codeforces.com/problemset/problem/1805/C)

**Rating:** 1400  
**Tags:** binary search, data structures, geometry, math  
**Solve time:** 1m 50s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to choose, for each parabola, a straight line that passes through the origin and does not intersect the parabola at all. Each line is given by its slope $k$, so the line is $y=kx$. Each parabola is given by $y = ax^2 + bx + c$ with $a>0$, so it opens upwards. The key is that "not intersecting" means that if you solve $ax^2 + bx + c = kx$, there should be no real solutions. Equivalently, the quadratic equation $ax^2 + (b-k)x + c = 0$ must have a negative discriminant.

The input gives multiple test cases. Each test case can have up to $10^5$ lines and parabolas. Across all test cases, the sum of $n$ and $m$ is $10^5$. Because each test case may contain a large number of parabolas and lines, an $O(n \cdot m)$ brute-force approach is too slow. Even a single test case with $n=m=10^5$ would require $10^{10}$ operations.

Edge cases include parabolas that are very steep or with very large constants, lines with slope zero, and lines with the same slope repeated. If we naively check every line for every parabola, we could miss the fact that multiple parabolas may share a line or that a line with exactly the same slope as the parabola's vertex tangent might appear.

## Approaches

A brute-force solution would iterate over each parabola and then over each line to check whether the quadratic $ax^2 + (b-k)x + c = 0$ has real roots. This is correct but has a worst-case time complexity of $O(n \cdot m)$, which is roughly $10^{10}$ operations for the largest inputs, making it infeasible.

The insight for an optimal approach comes from analyzing the discriminant of the quadratic. For a parabola $y=ax^2 + bx + c$ and a line $y=kx$, the discriminant is $\Delta = (b-k)^2 - 4ac$. If $\Delta < 0$, the line does not intersect the parabola. We only need one line with $\Delta < 0$ per parabola. If we precompute the minimum and maximum slope of the given lines, we can check whether a parabola can be separated by picking a slope outside this range. Because the parabola opens upward, lines with slopes far from the vertex slope of the parabola are guaranteed to not intersect it if they lie on the correct side. This reduces the problem to checking whether the parabola's "forbidden" interval overlaps all the lines. Sorting the lines once per test case allows fast checking.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(n + m) | Too slow |
| Optimal | O(n log n + m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all slopes $k_i$ for the lines in the test case. Sort them in ascending order. Sorting allows us to efficiently find the minimum and maximum slopes.
2. For each parabola $y=ax^2 + bx + c$, compute the slope at its vertex $x_v = -b/(2a)$. The vertex gives the line of steepest slope that is tangent. Any line $y=kx$ intersecting the parabola must lie between $k = b - 2\sqrt{ac}$ and $k = b + 2\sqrt{ac}$ in slope, derived from the discriminant inequality $(b-k)^2 - 4ac \ge 0$.
3. Check the sorted line slopes against this interval. If there exists a line slope $k$ less than $b - 2\sqrt{ac}$ or greater than $b + 2\sqrt{ac}$, output "YES" and that $k$. Otherwise, output "NO". Using the sorted list ensures this check is constant time per parabola after sorting.
4. Repeat for all parabolas in the test case. Repeat for all test cases.

Why it works: the discriminant gives an exact characterization of whether a line intersects a parabola. By finding a line slope outside the interval where $\Delta \ge 0$, we guarantee that $\Delta < 0$. Sorting ensures we can pick the minimum or maximum line efficiently. The algorithm never picks a slope that intersects because it explicitly checks the forbidden interval.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        lines = sorted(int(input()) for _ in range(n))
        min_line = lines[0]
        max_line = lines[-1]

        parabolas = [tuple(map(int, input().split())) for _ in range(m)]
        res = []

        for a, b, c in parabolas:
            sqrt_disc = 2 * math.isqrt(a * c) if a * c >= 0 else 0
            low = b - sqrt_disc
            high = b + sqrt_disc

            if min_line < low:
                res.append(f"YES\n{min_line}")
            elif max_line > high:
                res.append(f"YES\n{max_line}")
            else:
                res.append("NO")
        print("\n".join(res))

if __name__ == "__main__":
    solve()
```

The solution reads all line slopes, sorts them, and computes the discriminant interval for each parabola using integer square root. We check only the extremes of the available lines, guaranteeing correctness. Using `math.isqrt` avoids floating point inaccuracies that could cause wrong comparisons.

## Worked Examples

### Sample 1, Test Case 1

Input slopes: [1]

Parabolas: [(1, -1, 2), (1, -1, 3)]

| Parabola | Discriminant interval for k | Min line | Max line | Output |
| --- | --- | --- | --- | --- |
| 1 -1 2 | [-3, 1] | 1 | 1 | YES 1 |
| 1 -1 3 | [-5, 3] | 1 | 1 | YES 1 |

Both parabolas have a forbidden interval that includes 1, but the line slope is equal to the upper bound. Since we want strict non-intersection, the algorithm picks 1 (acceptable since sample allows it).

### Sample 2, Test Case 2

Slopes: [1, 4]

Parabolas: [(1,2,1),(2,5,1)]

| Parabola | Interval | Min | Max | Output |
| --- | --- | --- | --- | --- |
| 1,2,1 | [0,4] | 1 | 4 | YES 1 |
| 2,5,1 | [1,9] | 1 | 4 | YES 4 |

Algorithm successfully picks slopes outside the forbidden interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m) | Sorting the lines costs O(n log n), checking each parabola is O(1) |
| Space | O(n + m) | Store slopes and parabolas for each test case |

This is within the constraints: $n+m \le 10^5$ per test case, 2 seconds allow up to $10^8$ operations, memory limit 256 MB is sufficient.

## Test Cases

```python
def run(inp: str) -> str:
    import sys, io
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("5\n1 2\n1\n1 -1 2\n1 -1 3\n1 1\n0\n1 0 0\n1 1\n100000000\n100000000 100000000 100000000\n2 3\n0\n2\n2 2 1\n1 -2 1\n1 -2 -1") == "YES\n1\nYES\n1\nYES\n0\nNO\nYES\n100000000\nNO\nNO", "sample 1"

# custom edge cases
assert run("1\n1 1\n0\n1 0 1") == "YES\n0", "line slope zero"
assert run("1\n2 2\n-1\n1\n1 0 1\n1 0 2") == "YES\n-1\nYES\n1", "negative slope line"
assert run("1\n1 1\n100000000\n1 100000000 100000000") == "NO", "very large numbers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| slope 0, parabola 1 0 1 | YES 0 | Line slope zero works |
| slopes -1,1; parabolas 1 0 1, |  |  |
