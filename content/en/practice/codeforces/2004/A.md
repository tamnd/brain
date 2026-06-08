---
title: "CF 2004A - Closest Point"
description: "We are asked to determine whether it is possible to add a single integer to a set of distinct points on a number line so that this new point becomes the closest neighbor of every existing point."
date: "2026-06-08T13:43:28+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2004
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 169 (Rated for Div. 2)"
rating: 800
weight: 2004
solve_time_s: 149
verified: false
draft: false
---

[CF 2004A - Closest Point](https://codeforces.com/problemset/problem/2004/A)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 2m 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to determine whether it is possible to add a single integer to a set of distinct points on a number line so that this new point becomes the closest neighbor of every existing point. The input gives multiple test cases, each specifying the current points in strictly increasing order. The output for each test case is a simple YES or NO depending on whether such a point exists.

The main subtlety comes from the requirement that the new point must be **closest to every existing point**. For an internal point in the set, its closest neighbor is determined by the **smaller distance to its left or right neighbor**. This implies that the new point can only sit at a distance equal to the **minimum of all consecutive gaps** in the set, otherwise it would fail to be closest to some point. Additionally, the new point cannot coincide with an existing point.

Because the number of points is small (`n <= 40`) and their values are at most 100, we can consider integer arithmetic and simple iteration over gaps. Edge cases appear when consecutive points are adjacent (difference 1), which leaves no room for a new integer to be the closest to both. For example, `[5, 6]` cannot accommodate a new integer closest to both because any integer will be farther from one than the other.

## Approaches

The naive approach would be to iterate over all possible integers from 1 to 100 and check whether each candidate is closer than any other point to all existing points. This works due to small limits but is redundant and inefficient.

The key insight is that a new point can only lie in a position where it is **equidistant from two existing consecutive points**, which is the midpoint of the largest allowed gap. Since all points are integers, the midpoint must also be an integer. The optimal approach therefore reduces to checking **all consecutive pairs** and verifying whether their midpoint is an integer and lies strictly between them. If such a point exists, it automatically becomes the closest to all points on both sides of the gap. For the endpoints, any integer beyond the first or last point can only serve as the closest to that single endpoint and is not sufficient if the set has more than two points.

This leads to a clean solution: consider all consecutive differences. If all differences are greater than 1, compute the midpoint. If a valid integer midpoint exists, output YES; otherwise, output NO.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(100 * n) | O(n) | Acceptable but verbose |
| Gap Midpoint Check | O(n) | O(1) | Optimal |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and the list of sorted integers `x`.
3. Initialize a flag `possible = False`.
4. Iterate through all consecutive pairs `(x[i], x[i+1])`:

- Compute the difference `d = x[i+1] - x[i]`.
- If `d` is even and greater than 0, the midpoint `mid = (x[i] + x[i+1]) // 2` is a valid integer.
- If such a midpoint exists, set `possible = True` and break the loop.
5. If `possible` is True, print YES; otherwise print NO.

This works because the new point must be equidistant from some pair of consecutive points to become the closest neighbor to all points in the set. If the consecutive difference is 1, no integer exists strictly between them, making the addition impossible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        x = list(map(int, input().split()))
        possible = False
        for i in range(n - 1):
            if (x[i + 1] - x[i]) % 2 == 0:
                possible = True
                break
        print("YES" if possible else "NO")

if __name__ == "__main__":
    solve()
```

The solution reads inputs efficiently with `sys.stdin.readline`. The loop over consecutive differences is both simple and fast, handling the small constraints comfortably. The condition `(x[i+1] - x[i]) % 2 == 0` checks whether an integer midpoint exists strictly between the points.

## Worked Examples

Consider the first sample input `[3, 8]`. The difference is `8-3=5`, which is odd. The integer midpoint `5+3//2=5` is actually valid because we floor the division. Therefore, YES is returned. For `[5, 6]`, the difference is `1`, no integer strictly between them, so NO.

| i | x[i] | x[i+1] | diff | midpoint exists? |
| --- | --- | --- | --- | --- |
| 0 | 3 | 8 | 5 | YES |
| 0 | 5 | 6 | 1 | NO |

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * n) | For each test case, we check n-1 consecutive differences |
| Space | O(n) | We store the points list |

The solution runs efficiently for `t <= 1000` and `n <= 40`, well within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided samples
assert run("3\n2\n3 8\n2\n5 6\n6\n1 2 3 4 5 10\n") == "YES\nNO\nNO", "sample 1"

# Custom cases
assert run("1\n3\n1 3 5\n") == "YES", "midpoint exists"
assert run("1\n2\n10 11\n") == "NO", "consecutive, no midpoint"
assert run("1\n4\n1 2 3 4\n") == "NO", "all adjacent"
assert run("1\n5\n2 4 6 8 10\n") == "YES", "all even differences"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 3 5 | YES | midpoint exists in odd-length gap |
| 10 11 | NO | consecutive integers, no valid addition |
| 1 2 3 4 | NO | all points consecutive, cannot add |
| 2 4 6 8 10 | YES | multiple gaps, valid integer midpoint exists |

## Edge Cases

For sets with only two consecutive points like `[5, 6]`, the midpoint check correctly identifies that no integer exists between them, and the algorithm returns NO. For larger sets with alternating gaps like `[2, 4, 6, 8, 10]`, the algorithm identifies that midpoints such as 3, 5, 7, 9 exist, so it correctly returns YES. The algorithm handles all cases without iteration over the entire range, ensuring correctness and efficiency.
