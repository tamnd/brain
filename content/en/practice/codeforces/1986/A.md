---
title: "CF 1986A - X Axis"
description: "We are given three integer points on a one-dimensional number line, specifically the X axis. The task is to find a single integer coordinate such that the sum of the distances from this chosen point to the three given points is minimized."
date: "2026-06-08T16:10:56+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "geometry", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1986
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 954 (Div. 3)"
rating: 800
weight: 1986
solve_time_s: 96
verified: true
draft: false
---

[CF 1986A - X Axis](https://codeforces.com/problemset/problem/1986/A)

**Rating:** 800  
**Tags:** brute force, geometry, math, sortings  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three integer points on a one-dimensional number line, specifically the X axis. The task is to find a single integer coordinate such that the sum of the distances from this chosen point to the three given points is minimized. The distance metric is the usual absolute difference, so for a point $a$ and a point $x_i$, the distance is $|a - x_i|$.

The input consists of multiple test cases, each specifying three integers in the range from 1 to 10. The output for each test case is a single integer representing the smallest total distance that can be achieved.

Because the points are limited to a very small range, a naive approach could even check all possible integer coordinates from 1 to 10. However, for understanding the general structure of the problem, it is helpful to consider the mathematical properties: for three points on a line, the sum of distances is minimized when the chosen point is the median of the three points. This is because the median balances the distances to the left and right extremes.

Non-obvious edge cases include situations where two or all three points coincide. For instance, if all points are at 1, then the optimal point is also 1, yielding a total distance of 0. If two points are at 1 and one is at 10, the optimal choice is 1 or 10, but calculating it carefully shows the median approach naturally selects the point that balances the distances.

## Approaches

The brute-force approach would consider every integer coordinate between 1 and 10 and compute the sum of distances for each. Since the coordinate range is extremely small, this approach is feasible for this problem, though it is unnecessary from a mathematical perspective. For each candidate $a$, the algorithm sums $|a - x_1| + |a - x_2| + |a - x_3|$. With three points and ten candidate positions, this requires at most 30 distance calculations per test case. Given that $t \leq 1000$, this is only 30,000 calculations, which easily fits within the 2-second time limit.

The optimal approach comes from observing that the sum of absolute differences is minimized at the median of the points. Sorting the three points and taking the middle value directly gives the optimal coordinate $a$. This reduces the problem to simply sorting three numbers, which is constant time. There is no need to iterate through candidate positions or perform repeated summations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(t * 10) = O(t) | O(1) | Accepted due to small input range |
| Median-based Optimal | O(t) | O(1) | Accepted and optimal |

## Algorithm Walkthrough

1. Read the number of test cases $t$. We will process each test case independently.
2. For each test case, read the three integers representing the points on the X axis.
3. Sort the three integers. This ensures that the smallest, median, and largest values are easily identified.
4. Select the middle value of the sorted list as the optimal coordinate $a$. This is the median and guarantees the minimal sum of distances.
5. Compute the sum of distances from $a$ to each of the three points using $|a - x_1| + |a - x_2| + |a - x_3|$.
6. Print the computed sum for the current test case.

Why it works: For a set of three points on a line, moving the chosen point away from the median increases the total distance in at least one direction without sufficient reduction in the other. Therefore, the median is the unique point that minimizes the sum of absolute differences.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    x = list(map(int, input().split()))
    x.sort()
    median = x[1]
    total_distance = abs(median - x[0]) + abs(median - x[1]) + abs(median - x[2])
    print(total_distance)
```

The code first reads the number of test cases. For each test case, it parses the three coordinates, sorts them, and takes the middle element as the median. Using the absolute value function, it calculates the sum of distances to all points and prints it. Sorting three elements is constant time, so this step is trivial in terms of performance. Using the middle element guarantees correctness without checking all candidate coordinates.

## Worked Examples

**Example 1:** `1 5 9`

| Step | Sorted Points | Median | Total Distance |
| --- | --- | --- | --- |
| Initial | 1, 5, 9 | 5 |  |
| Compute |  | 5 |  |

Explanation: Choosing 5 balances the distances to 1 and 9.

**Example 2:** `8 2 8`

| Step | Sorted Points | Median | Total Distance |
| --- | --- | --- | --- |
| Initial | 2, 8, 8 | 8 |  |
| Compute |  | 8 |  |

Explanation: Median 8 is repeated and minimizes distance.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Sorting 3 elements is constant time, done for each of t test cases. |
| Space | O(1) | Only a list of three elements is stored per test case. |

Given $t \leq 1000$ and three points per test case, this algorithm is extremely fast and memory-efficient, well within the problem constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # Solution function
    t = int(input())
    for _ in range(t):
        x = list(map(int, input().split()))
        x.sort()
        median = x[1]
        total_distance = abs(median - x[0]) + abs(median - x[1]) + abs(median - x[2])
        print(total_distance)
    return output.getvalue().strip()

# Provided sample
assert run("8\n1 1 1\n1 5 9\n8 2 8\n10 9 3\n2 1 1\n2 4 1\n7 3 5\n1 9 4\n") == "0\n8\n6\n7\n1\n3\n4\n8"

# Custom cases
assert run("1\n1 1 10\n") == "9", "two equal, one far"
assert run("1\n5 5 5\n") == "0", "all equal"
assert run("1\n1 2 3\n") == "2", "consecutive numbers"
assert run("1\n10 1 5\n") == "8", "extremes and middle"
assert run("1\n3 3 4\n") == "1", "two equal, one adjacent"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 10 | 9 | Two equal points and one distant point |
| 5 5 5 | 0 | All points coincide |
| 1 2 3 | 2 | Consecutive numbers and median selection |
| 10 1 5 | 8 | Extreme values and median correctness |
| 3 3 4 | 1 | Two points equal, one adjacent |

## Edge Cases

When all three points are the same, e.g., `5 5 5`, the algorithm selects the median `5`. The distance sum is `0 + 0 + 0 = 0`, correctly handling this edge case.

When two points coincide and one is far away, e.g., `1 1 10`, sorting yields `[1, 1, 10]` and the median is `1`. The sum of distances is `0 + 0 + 9 = 9`, which is minimal compared to choosing `10` (would be `9 + 9 + 0 = 18`).

When points are consecutive, e.g., `1 2 3`, the sorted list is `[1, 2, 3]` and median `2` produces sum `1 + 0 + 1 = 2`. Choosing `1` or `3` would yield `1 + 1 + 2 = 4`, so the algorithm correctly identifies the median.

This confirms the median-based approach handles all small-range edge cases correctly without special case handling.
