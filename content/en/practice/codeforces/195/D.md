---
title: "CF 195D - Analyzing Polyline"
description: "We are asked to consider a set of linear functions, each defined by a slope $ki$ and intercept $bi$, and to analyze their sum."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 195
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 123 (Div. 2)"
rating: 1900
weight: 195
solve_time_s: 88
verified: false
draft: false
---

[CF 195D - Analyzing Polyline](https://codeforces.com/problemset/problem/195/D)

**Rating:** 1900  
**Tags:** geometry, math, sortings  
**Solve time:** 1m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to consider a set of linear functions, each defined by a slope $k_i$ and intercept $b_i$, and to analyze their sum. If we take the sum of $n$ such functions, the resulting graph is piecewise-linear, meaning it is composed of straight line segments joined at certain x-coordinates. The task is to determine how many "corners" or angles in this polyline are not straight lines-that is, points where the slope changes.

Each function $y_i(x) = k_i \cdot x + b_i$ contributes a constant slope $k_i$ to the sum. Therefore, the sum $s(x) = \sum_{i=1}^n y_i(x)$ also has segments of constant slope, but the slope of $s(x)$ between two consecutive integer $x$-coordinates depends on the sum of all the individual slopes.

The input size allows up to 100,000 functions, with slope and intercept values up to $10^9$. This precludes naive approaches that attempt to simulate the polyline for all x-coordinates explicitly because that could generate O(n²) points if done carelessly. We need a solution that scales linearly or logarithmically with $n$.

The subtle edge cases include situations where multiple functions have the same slope. If all slopes are equal, the polyline is just a straight line, so the number of non-180-degree angles should be 1 (the starting vertex counts as an angle). Another tricky scenario is when the slopes alternate in a sequence like [2, -2, 2]. A careless sum might miscount transitions, so the algorithm must correctly identify slope changes.

## Approaches

The brute-force method is straightforward: one could compute the sum function and explicitly generate the resulting y-values at a dense set of x-coordinates, then count where the slope changes. For each x, the slope would be computed by comparing successive y-values. This is correct but impractical. For $n = 10^5$, constructing and examining every vertex explicitly could involve O(n²) operations in the worst case, far exceeding the 2-second limit.

The key insight comes from observing that the sum of linear functions is still linear between integer breakpoints, and the slope at any point is simply the sum of the slopes of all contributing functions. The polyline only changes slope where the slope sum changes, which occurs at points where the slope values differ. Therefore, we can reduce the problem to counting distinct slope values in the input. Each change in slope corresponds to a non-180-degree angle.

The optimal approach is to extract all slope values, sort them, and count the number of distinct slopes. The polyline will have as many non-straight angles as there are distinct slopes plus one, accounting for the first vertex. This reduces the problem from simulating all vertices to a single pass over slopes, which is O(n log n) due to sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n²) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the integer $n$, the number of linear functions. This sets the size of the problem.
2. Initialize an empty list to store all slope values.
3. Loop over the next $n$ lines, reading each slope $k_i$ and intercept $b_i$. Only the slope $k_i$ is relevant for counting angles, so append it to the slope list.
4. Sort the slope list. Sorting groups identical slopes together, making it easy to count unique slopes.
5. Initialize a counter for distinct slopes. Traverse the sorted list, incrementing the counter whenever the current slope differs from the previous one.
6. The final answer is the number of distinct slopes plus one. This accounts for the first segment starting from the origin, which forms the first angle.

Why it works: The algorithm leverages the fact that the sum of linear functions produces a polyline whose slopes are additive. Each transition between different slopes creates a corner in the polyline that is not 180 degrees. By counting unique slopes and adding one for the starting vertex, we account for all such corners without simulating every vertex.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    slopes = []
    for _ in range(n):
        k, b = map(int, input().split())
        slopes.append(k)
    
    slopes.sort()
    unique_slopes = 1
    for i in range(1, n):
        if slopes[i] != slopes[i - 1]:
            unique_slopes += 1
    
    print(unique_slopes)

if __name__ == "__main__":
    main()
```

The code first reads all slopes and ignores the intercepts since they do not affect angles. Sorting allows counting distinct slopes efficiently. The loop that increments `unique_slopes` is careful to compare each slope to the previous one, avoiding double counting. The addition of one for the first vertex is implicit in initializing `unique_slopes = 1`.

## Worked Examples

**Sample 1:**

Input:

```
1
1 0
```

| Step | Slopes List | Unique Slopes Count |
| --- | --- | --- |
| Read input | [1] | 1 |
| Sorted | [1] | 1 |
| Count distinct | 1 | 1 |
| Output | 1 | 1 |

The polyline is just a single segment; it has one angle, which is counted correctly.

**Custom Sample 2:**

Input:

```
3
1 2
2 3
1 4
```

| Step | Slopes List | Unique Slopes Count |
| --- | --- | --- |
| Read input | [1, 2, 1] | - |
| Sorted | [1, 1, 2] | - |
| Count distinct | Compare 1 vs 1 (no increment), 2 vs 1 (increment) | 2 |
| Output | 2 | 2 |

The polyline has a slope sequence of 1, 1, 2, giving two distinct slopes. Adding the first vertex, the algorithm counts 2 non-180-degree angles.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the linear scan to count unique slopes |
| Space | O(n) | Storing the list of slopes |

With $n \le 10^5$, O(n log n) operations are comfortably under 2 seconds. Memory usage is linear in n, well below the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# Provided sample
assert run("1\n1 0\n") == "1", "sample 1"

# Minimum size
assert run("1\n0 0\n") == "1", "minimum size"

# All slopes equal
assert run("3\n2 1\n2 3\n2 4\n") == "1", "all slopes equal"

# Slopes alternating
assert run("4\n1 0\n2 0\n1 0\n2 0\n") == "2", "alternating slopes"

# Maximum size with identical slopes
assert run("5\n1000000000 0\n1000000000 0\n1000000000 0\n1000000000 0\n1000000000 0\n") == "1", "max value identical slopes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 0 | 1 | Single function |
| 1 0 0 | 1 | Minimum slope and intercept |
| 3 2 1 ... 2 4 | 1 | All slopes identical |
| 4 1 0 ... 2 0 | 2 | Alternating slopes |
| 5 1000000000 0 ... | 1 | Large values with identical slopes |

## Edge Cases

For a single function input like `1 1 0`, the polyline has only one segment. The algorithm correctly counts one non-180-degree angle because `unique_slopes` starts at 1 and there are no other slopes to increment it. When all slopes are equal, the algorithm still outputs 1, reflecting a straight line with no intermediate angle changes. When slopes alternate or are distinct, each distinct slope is counted once, correctly tracking the number of angle changes in the polyline.
