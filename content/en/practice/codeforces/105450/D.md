---
title: "CF 105450D - Trick or Treat"
description: "We are given a set of points on a 2D grid, and we start from the origin at coordinate (0, 0). We want to choose a direction and walk in a straight line passing through the origin. While moving along that line, we collect all candies that lie exactly on it."
date: "2026-06-23T17:32:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105450
codeforces_index: "D"
codeforces_contest_name: "UTPC x WiCS Contest 10-25-24 (UT Internal)"
rating: 0
weight: 105450
solve_time_s: 84
verified: false
draft: false
---

[CF 105450D - Trick or Treat](https://codeforces.com/problemset/problem/105450/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of points on a 2D grid, and we start from the origin at coordinate (0, 0). We want to choose a direction and walk in a straight line passing through the origin. While moving along that line, we collect all candies that lie exactly on it. The goal is to choose the line that passes through the origin and contains the largest number of given points.

Each candy is just a fixed point in the plane. The only valid lines are those that go through the origin, so every candidate solution is fully determined by a direction vector from (0, 0) to some candy point (x, y). All points that lie on the same such line share the same slope, or more precisely, the same reduced direction ratio.

The input size goes up to 100,000 points, which immediately rules out comparing every pair of points or checking all pairs of slopes. Any solution that attempts O(n²) behavior will perform up to 10¹⁰ comparisons in the worst case, which is far beyond feasible limits in one second. This pushes us toward an O(n log n) or O(n) approach.

A few subtle cases matter here. First, points in opposite quadrants can lie on the same line through the origin, for example (2, 3) and (-4, -6). A naive slope computation y/x would treat them as different signs unless normalized carefully.

Second, vertical lines must be handled. A point like (0, 5) defines a valid line, but slope representation would involve division by zero if not treated separately.

Third, normalization is critical. Without reducing direction vectors to canonical form, the same line could be counted multiple times under different integer representations like (2, 4) and (1, 2), which must be considered identical.

## Approaches

A brute-force idea is to consider every pair of points and compute the line passing through the origin and that pair’s direction. For each such line, we could count how many points lie on it by checking collinearity via cross products. This works because two points define a direction, and every other point can be tested against that direction.

However, this leads to O(n²) candidate directions, and for each direction we might scan all n points, giving O(n³) in the worst form, or at best O(n²) if we optimize counting. With n = 10⁵, even O(n²) is impossible.

The key observation is that every valid line through the origin can be uniquely represented by the direction vector from the origin to any point on that line. Instead of enumerating pairs of points, we only need to classify each point by its normalized direction. Points sharing the same reduced direction lie on the same line, so the task reduces to counting frequencies of normalized direction vectors.

This transforms the problem into a hashing problem over reduced integer pairs. Each point contributes exactly one direction, and we maintain a frequency map to find the maximum count.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) to O(n³) | O(1) | Too slow |
| Direction Hashing | O(n log n) or O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each point (x, y), compute a normalized representation of its direction from the origin. This ensures that all points on the same line map to the same key. Normalization is necessary because raw ratios like y/x are not stable under integer scaling or sign changes.
2. If x is zero, treat the direction as a special vertical class. All points with x = 0 belong to the same line through the origin, regardless of whether y is positive or negative.
3. If x is nonzero, compute the greatest common divisor of x and y, then divide both by it. This reduces the pair to its smallest integer representation. This step removes duplicates like (2, 4) and (1, 2).
4. Normalize sign so that equivalent directions map identically. A standard rule is to ensure that either x is positive, or if x is zero then y is positive. If x is negative, multiply both components by -1.
5. Store each normalized direction in a hash map and increment its frequency.
6. After processing all points, return the maximum frequency seen among all direction classes.

Why it works: every point belongs to exactly one line through the origin, and every such line corresponds to exactly one reduced direction vector. The normalization guarantees a one-to-one mapping between geometric lines and hash keys, so counting frequencies is equivalent to counting how many points lie on each valid line.

## Python Solution

```python
import sys
input = sys.stdin.readline

from math import gcd
from collections import defaultdict

def solve():
    n = int(input())
    freq = defaultdict(int)

    for _ in range(n):
        x, y = map(int, input().split())

        if x == 0:
            # vertical line through origin
            key = (0, 1)
        else:
            g = gcd(x, y)
            x //= g
            y //= g

            if x < 0:
                x = -x
                y = -y

            key = (x, y)

        freq[key] += 1

    print(max(freq.values()))

if __name__ == "__main__":
    solve()
```

The solution processes each point independently and converts it into a canonical direction vector. The gcd step ensures that all proportional vectors collapse into the same representation. The sign normalization ensures that opposite directions on the same line are not split into separate groups.

A subtle implementation detail is handling x = 0 before attempting gcd normalization. Without this guard, division logic remains valid but sign conventions become inconsistent, especially for (0, y) and (0, -y). Fixing vertical lines explicitly avoids ambiguity and simplifies the mapping.

## Worked Examples

### Example 1

Input:

```
5
2 2
4 4
-3 -3
1 0
0 5
```

We track normalized directions:

| Point | Normalized (x, y) | Frequency Map State |
| --- | --- | --- |
| (2,2) | (1,1) | {(1,1):1} |
| (4,4) | (1,1) | {(1,1):2} |
| (-3,-3) | (1,1) | {(1,1):3} |
| (1,0) | (1,0) | {(1,1):3, (1,0):1} |
| (0,5) | (0,1) | {(1,1):3, (1,0):1, (0,1):1} |

The maximum frequency is 3, corresponding to the diagonal line y = x. This confirms that proportional points are grouped correctly even across sign changes.

### Example 2

Input:

```
4
0 1
0 -2
3 6
-2 -4
```

| Point | Normalized (x, y) | Frequency Map State |
| --- | --- | --- |
| (0,1) | (0,1) | {(0,1):1} |
| (0,-2) | (0,1) | {(0,1):2} |
| (3,6) | (1,2) | {(0,1):2, (1,2):1} |
| (-2,-4) | (1,2) | {(0,1):2, (1,2):2} |

The best line contains 2 points, and both vertical and sloped lines are handled consistently through normalization.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each point requires a gcd computation, which is logarithmic in coordinate size |
| Space | O(n) | In worst case every point forms a distinct direction |

The constraints allow up to 100,000 points, and this solution performs a constant amount of arithmetic per point plus a gcd computation. This is well within typical limits for a 1-second execution.

## Test Cases

```python
import sys, io
from collections import defaultdict
from math import gcd

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        n = int(input())
        freq = defaultdict(int)

        for _ in range(n):
            x, y = map(int, input().split())

            if x == 0:
                key = (0, 1)
            else:
                g = gcd(x, y)
                x //= g
                y //= g
                if x < 0:
                    x = -x
                    y = -y
                key = (x, y)

            freq[key] += 1

        return str(max(freq.values()))

    return solve()

# provided sample
assert run("""5
2 2
4 4
-3 -3
1 0
0 5
""") == "3"

# all same line
assert run("""3
1 2
2 4
-3 -6
""") == "3"

# vertical only
assert run("""3
0 1
0 -5
0 10
""") == "3"

# mixed directions
assert run("""4
1 0
0 1
-1 0
0 -1
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| collinear multiples | 3 | gcd normalization correctness |
| vertical duplicates | 3 | vertical line grouping |
| mixed axes | 2 | sign normalization and axis separation |

## Edge Cases

A key edge case is when all points lie on the same geometric line but appear in different integer scalings and signs. For example, (1, 2), (2, 4), and (-3, -6). The algorithm converts all of them into (1, 2) by dividing by gcd and fixing sign, so they are counted together. Without this normalization, these would incorrectly be treated as different directions.

Another edge case is vertical alignment. For input like (0, 1), (0, -1), and (0, 5), slope-based grouping would fail due to division by zero or inconsistent representation. The explicit mapping to a single canonical key (0, 1) ensures all such points are merged, and the frequency count correctly reflects that they lie on the same line through the origin.
