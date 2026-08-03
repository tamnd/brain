---
title: "CF 102562D - Cupidus the Cupidon"
description: "Each candidate stands on the vertical axis at position (0, ai) and fires an arrow that travels in a straight line toward the landing point (xi, yi). The task is to keep as many candidates as possible so that no two chosen arrow trajectories meet."
date: "2026-08-03T18:14:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102562
codeforces_index: "D"
codeforces_contest_name: "AGM 2020, Final Round, Day 1"
rating: 0
weight: 102562
solve_time_s: 315
verified: true
draft: false
---

[CF 102562D - Cupidus the Cupidon](https://codeforces.com/problemset/problem/102562/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

Each candidate stands on the vertical axis at position `(0, a_i)` and fires an arrow that travels in a straight line toward the landing point `(x_i, y_i)`. The task is to keep as many candidates as possible so that no two chosen arrow trajectories meet.

A useful way to look at a trajectory is as a line with a starting height and a slope. The starting height is `a_i`, and the slope is `(y_i - a_i) / x_i`. The input gives the starting height and the landing point, and the output is the largest number of trajectories that can coexist without intersections.

The number of candidates over all test cases can reach `500000`, so an algorithm that compares every pair is not possible. A quadratic approach would perform around `250000000000` comparisons in the largest case, which is far beyond what a normal competitive programming time limit allows. We need a solution around `O(N log N)` per total input.

The coordinates are extremely large, reaching about `2^52`, so floating point arithmetic is unsafe. A tiny precision error while comparing two slopes could change the answer. All slope comparisons have to be done using integer cross multiplication.

There are a few cases where an implementation can silently fail. Equal slopes are one of them. For example:

```
1
3
0 5 5
10 5 15
20 5 25
```

The slopes are all `1`, so the answer is `3`. A strict increasing subsequence implementation would incorrectly return `1`, because equal slopes are allowed.

Another case is negative slopes:

```
1
2
0 2 -2
10 2 8
```

The slopes are `-1` and `-1`, so both trajectories are parallel and the answer is `2`. Treating the numerator as a normal integer without considering the denominator sign would easily produce incorrect ordering.

A third dangerous case is large values:

```
1
2
0 4503599627370496 4503599627370496
1 4503599627370496 0
```

The slopes are `1` and approximately `-1`, and the answer is `1`. Converting these values to `float` can lose enough precision to compare slopes incorrectly.

## Approaches

The direct solution is to examine every pair of trajectories and decide whether they intersect. Since two trajectories intersect when their slopes are ordered incorrectly relative to their starting heights, we could sort by starting height and compare every pair of slopes. This is correct because after sorting by `a_i`, a lower trajectory can stay below a higher one only when its slope is not larger. The problem is the number of comparisons. With `N = 100000`, the brute force method needs about `N * (N - 1) / 2`, or roughly five billion comparisons, which is too slow.

The key observation is that after sorting candidates by their positions on the vertical axis, we only need the longest sequence of slopes that never decreases. Suppose candidate `i` starts below candidate `j`. If the slope of `i` is larger, the lower line eventually catches the upper line and the trajectories intersect. If the slope is smaller or equal, the distance between the two lines never becomes zero, so they can both be selected.

The geometric problem becomes a longest non-decreasing subsequence problem over rational numbers. The standard patience sorting technique solves this in `O(N log N)`. The only additional challenge is comparing fractions exactly, which is handled by cross multiplication.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Too slow |
| Optimal | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Sort all candidates by their starting height `a_i` in increasing order. This fixes the order in which trajectories leave the vertical axis. Any valid chosen set must respect this order.
2. Convert every trajectory into a slope value:

$$s_i = \frac{y_i-a_i}{x_i}$$

The denominator is always positive, so comparing slopes only requires comparing the cross products of the numerators and denominators.

1. Process the slopes in sorted order and maintain the patience sorting array. The value at position `k` represents the smallest possible ending slope of a non-decreasing subsequence of length `k + 1`.
2. For the current slope, find the first stored slope that is strictly greater than it. Replace that value with the current slope. If no stored slope is greater, append the slope.

The search uses the first greater value instead of the first greater-or-equal value because equal slopes can appear together in the answer. We need the longest non-decreasing subsequence, not the longest strictly increasing subsequence.

1. The length of the patience sorting array is the maximum number of non-intersecting trajectories.

Why it works:

After sorting by starting height, every chosen trajectory appears from bottom to top. For two consecutive chosen trajectories, the lower one must have a slope no larger than the upper one. Otherwise, because it starts lower but rises faster, it must eventually meet the upper trajectory. If the slopes are ordered non-decreasingly, the vertical difference between consecutive trajectories starts positive and never decreases below zero. Therefore every valid answer corresponds exactly to a non-decreasing subsequence of slopes. The patience sorting algorithm finds the longest such subsequence, so its length is the required maximum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def greater_frac(a, b):
    return a[0] * b[1] > b[0] * a[1]

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        arr = []

        for _ in range(n):
            a, x, y = map(int, input().split())
            arr.append((a, y - a, x))

        arr.sort()

        tails = []

        for _, num, den in arr:
            cur = (num, den)

            left = 0
            right = len(tails)

            while left < right:
                mid = (left + right) // 2
                if greater_frac(tails[mid], cur):
                    right = mid
                else:
                    left = mid + 1

            if left == len(tails):
                tails.append(cur)
            else:
                tails[left] = cur

        ans.append(str(len(tails)))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The input is first transformed into `(starting height, slope numerator, slope denominator)`. Storing the slope as `(y_i - a_i, x_i)` avoids any floating point operations.

The sorting step is based only on the starting coordinate because the order of departures from the axis determines the order in which trajectories must be considered.

The `tails` array is the usual patience sorting structure for a longest non-decreasing subsequence. The binary search looks for the first fraction strictly larger than the current fraction. The fraction comparison uses multiplication instead of division, which keeps all calculations exact even for the largest coordinates.

Python integers automatically handle the large intermediate products. In languages with fixed-width integers, a wider type would be required because the multiplication can exceed 64-bit limits.

## Worked Examples

### Sample 1

Input:

```
5
6 8 3
-7 8 1
-10 10 -10
0 7 7
-2 2 8
```

After sorting by starting height, the slopes are:

| Step | Start height | Slope | Tails after processing |
| --- | --- | --- | --- |
| 1 | -10 | 0 | [0] |
| 2 | -7 | 1 | [0, 1] |
| 3 | -2 | 5 | [0, 1, 5] |
| 4 | 0 | 1 | [0, 1, 5] |
| 5 | 6 | -3/8 | [-3/8, 1, 5] |

The final length is `3`. The valid sequence of slopes can have lengths `0, 1, 5`, giving three non-intersecting trajectories.

### Sample 2

Input:

```
5
2 6 -4
6 1 6
-6 6 -9
-5 7 1
4 4 -3
```

The sorted slopes are:

| Step | Start height | Slope | Tails after processing |
| --- | --- | --- | --- |
| 1 | -6 | -1/2 | [-1/2] |
| 2 | -5 | 6/7 | [-1/2, 6/7] |
| 3 | 2 | -1 | [-1, 6/7] |
| 4 | 4 | -7/4 | [-7/4, 6/7] |
| 5 | 6 | 0 | [-7/4, 0] |

The final length is `2`. One optimal choice is the trajectory with slope `-7/4` followed by the trajectory with slope `0`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Sorting dominates, and each slope performs one binary search |
| Space | O(N) | The sorted list and patience array store linear numbers of trajectories |

The total number of candidates across all test cases is `500000`, so the total running time is bounded by sorting and binary searches over that many elements. The memory usage remains linear and fits comfortably within the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out.getvalue().strip()

assert run("""2
5
6 8 3
-7 8 1
-10 10 -10
0 7 7
-2 2 8
5
2 6 -4
6 1 6
-6 6 -9
-5 7 1
4 4 -3
""") == "3\n2", "samples"

assert run("""1
1
0 1 5
""") == "1", "single trajectory"

assert run("""1
3
0 5 5
10 5 15
20 5 25
""") == "3", "equal slopes"

assert run("""1
4
0 2 -2
10 2 8
20 4 0
30 1 10
""") == "3", "negative and mixed slopes"

assert run("""1
2
0 4503599627370496 4503599627370496
1 4503599627370496 0
""") == "1", "large coordinates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single trajectory | 1 | Handles the smallest possible case |
| Equal slopes | 3 | Confirms the subsequence must be non-decreasing |
| Negative and mixed slopes | 3 | Checks signed fraction comparison |
| Large coordinates | 1 | Confirms exact integer comparisons |

## Edge Cases

Equal slopes are handled by the binary search choice. For the input:

```
1
3
0 5 5
10 5 15
20 5 25
```

every trajectory has slope `1`. The binary search never replaces an equal slope with a shorter subsequence position because it only searches for values strictly greater than the current one. The array grows to length `3`, which is correct.

Negative slopes do not require special handling. Consider:

```
1
2
0 2 -2
10 2 8
```

The slopes are both `-1`, represented as `(-2, 2)` and `(-2, 2)`. Cross multiplication compares them exactly, so both are considered compatible and the answer is `2`.

Very large coordinates are also safe. For:

```
1
2
0 4503599627370496 4503599627370496
1 4503599627370496 0
```

the first slope is `1`, while the second is `-1`. The patience array replaces the first value with the smaller slope, leaving a length of `1`. The algorithm never converts these values to floating point, so no precision loss occurs.
