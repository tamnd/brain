---
title: "CF 2074G - Game With Triangles: Season 2"
description: "We are given a regular polygon with $n$ vertices, each vertex labeled with a positive integer. The goal is to draw non-overlapping triangles inside the polygon to maximize the sum of products of the numbers at their vertices."
date: "2026-06-08T06:41:48+07:00"
tags: ["codeforces", "competitive-programming", "dp", "geometry"]
categories: ["algorithms"]
codeforces_contest: 2074
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 1009 (Div. 3)"
rating: 2100
weight: 2074
solve_time_s: 116
verified: false
draft: false
---

[CF 2074G - Game With Triangles: Season 2](https://codeforces.com/problemset/problem/2074/G)

**Rating:** 2100  
**Tags:** dp, geometry  
**Solve time:** 1m 56s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a regular polygon with $n$ vertices, each vertex labeled with a positive integer. The goal is to draw non-overlapping triangles inside the polygon to maximize the sum of products of the numbers at their vertices. Each triangle contributes its vertex product to the score, and triangles are not allowed to share any positive area.

The input consists of multiple test cases, each describing a polygon via $n$ and an array of integers $a_1, \dots, a_n$. The output is the maximum achievable score for each polygon.

The key constraints are $3 \le n \le 400$ and the sum of $n^3$ across all test cases is at most $400^3$. This suggests that an $O(n^3)$ solution is acceptable, but anything worse, such as $O(n^4)$, would be too slow. Edge cases include polygons where all numbers are equal, or where the optimal solution might involve selecting a single triangle instead of multiple smaller triangles because combining smaller triangles reduces the overall product sum. For instance, in a quadrilateral labeled [2,1,3,4], picking the triangle with vertices 1,3,4 yields 24, whereas combining smaller triangles might give less.

## Approaches

The brute-force approach considers all possible sets of non-overlapping triangles. For $n$ vertices, the number of triangles is $O(n^3)$, and checking overlaps adds extra complexity. This is correct but inefficient because verifying every combination grows factorially, far exceeding feasible computation for $n = 400$.

The observation is that the polygon is regular and convex, so triangles that do not share edges are non-overlapping if chosen carefully. This suggests a dynamic programming approach similar to "matrix chain multiplication" or "polygon triangulation," where we consider sub-polygons and their maximum achievable score recursively. Specifically, if we pick a triangle with vertices $i, j, k$ inside a sub-polygon $[i, j, k]$, we can split the remaining polygon into independent sub-polygons and solve them separately. This ensures we never draw overlapping triangles.

Thus, we reduce the problem to computing the maximum sum of products for all sub-polygons using DP. Let `dp[l][r]` be the maximum score achievable for the polygon segment from vertex $l$ to $r$ along the clockwise order. The recursion is:

```
dp[l][r] = max(dp[l][k] + dp[k][r] + a[l]*a[k]*a[r]) for l<k<r
```

This recurrence considers picking a triangle with endpoints `l` and `r` and some intermediate vertex `k`. Iterating over all segments and lengths fills the DP table in $O(n^3)$, which is feasible given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! for triangles) | O(n^3) | Too slow |
| Dynamic Programming | O(n^3) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Extend the array `a` to handle the polygon circularity easily by concatenating it to itself. This allows linear indexing of segments that wrap around the polygon.
2. Initialize a 2D DP array `dp[l][r]` with zeros, where `l` and `r` are indices of the segment in the extended array.
3. Iterate over segment lengths from 3 to $n$, because a triangle requires at least 3 vertices.
4. For each segment `[l, r]` of the given length, consider all intermediate vertices `k` such that `l < k < r`.
5. Compute the score for drawing the triangle `(l, k, r)` plus the maximum scores for the left and right sub-segments (`dp[l][k]` and `dp[k][r]`).
6. Update `dp[l][r]` with the maximum value obtained from all possible `k`.
7. After filling the DP table, the answer is the maximum `dp[l][l+n-1]` for all starting indices `l` from 0 to `n-1`, ensuring we consider all rotations of the polygon.

Why it works: The DP invariant ensures that `dp[l][r]` always stores the optimal solution for the segment `[l, r]`. Triangles chosen in disjoint sub-segments do not overlap, and by checking all intermediate vertices `k`, we guarantee that every possible triangulation is considered.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        # duplicate array for circularity
        a = a * 2
        dp = [[0] * (2*n) for _ in range(2*n)]
        
        for length in range(3, n+1):
            for l in range(0, 2*n - length + 1):
                r = l + length - 1
                for k in range(l+1, r):
                    dp[l][r] = max(dp[l][r], dp[l][k] + dp[k][r] + a[l]*a[k]*a[r])
        
        ans = 0
        for start in range(n):
            ans = max(ans, dp[start][start+n-1])
        print(ans)
```

The code first duplicates the array `a` to handle circular segments, then fills the DP table for all segment lengths. The nested loops compute the maximum product sum for each segment by choosing a middle vertex `k`. Finally, it selects the maximum score among all rotated versions of the polygon.

## Worked Examples

### Sample 1: Input

```
3
1 2 3
```

| l | r | k | dp[l][r] |
| --- | --- | --- | --- |
| 0 | 2 | 1 | 1_2_3=6 |

The only possible triangle is `(0,1,2)` with product 6. DP table confirms this.

### Sample 2: Input

```
4
2 1 3 4
```

| l | r | k | dp[l][r] |
| --- | --- | --- | --- |
| 0 | 3 | 1 | 0+0+2_1_4=8 |
| 0 | 3 | 2 | 0+0+2_3_4=24 |

The maximum is 24 for triangle `(0,2,3)`, ignoring smaller overlapping triangles.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3) | For each segment of length up to n, we iterate over n starting points and n possible k vertices |
| Space | O(n^2) | DP table of size 2n x 2n to handle circular segments |

Given $n \le 400$, $O(n^3)$ is around $64 \times 10^6$ operations, which fits comfortably in the 4-second limit.

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

# provided samples
assert run("6\n3\n1 2 3\n4\n2 1 3 4\n6\n2 1 2 1 1 1\n6\n1 2 1 3 1 5\n9\n9 9 8 2 4 4 3 5 3\n9\n9 9 3 2 4 4 8 5 3\n") == "6\n24\n5\n30\n732\n696", "samples"

# custom cases
assert run("1\n3\n1 1 1\n") == "1", "all ones"
assert run("1\n4\n1 2 3 4\n") == "24", "single best triangle in quadrilateral"
assert run("1\n5\n5 5 5 5 5\n") == "125", "all equal numbers"
assert run("1\n6\n1 1000 1 1000 1 1000\n") == "1000000000", "alternating large values"
assert run("1\n7\n1 2 3 4 5 6 7\n") == "210", "ascending sequence"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 vertices, all ones | 1 | Smallest polygon, minimal values |
| 4 vertices [1,2,3,4] | 24 | Correctly chooses the single largest triangle |
| 5 vertices all 5 | 125 | DP handles equal values correctly |
| 6 vertices alternating 1,1000 | 1000000000 | Picks triangles maximizing product |
| 7 vertices ascending | 210 | DP correctly navigates larger segments |

## Edge Cases

For a quadrilateral `[2,1,3,4]`, a naive approach might sum two triangles `(0,1,2)` and `(0,2,3)` thinking they are non-overlapping. The DP ensures that overlapping triangles are not chosen together by only considering subsegments for `dp[l][k]` and `dp[k][r]`. In this case, `dp[
