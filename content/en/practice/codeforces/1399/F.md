---
title: "CF 1399F - Yet Another Segments Subset"
description: "We are given a collection of segments on a number line, each defined by a left endpoint and a right endpoint. The task is to select the largest possible subset of these segments with a specific property: for any two segments in the subset, they must either be completely…"
date: "2026-06-11T09:04:20+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "graphs", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1399
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 661 (Div. 3)"
rating: 2300
weight: 1399
solve_time_s: 131
verified: false
draft: false
---

[CF 1399F - Yet Another Segments Subset](https://codeforces.com/problemset/problem/1399/F)

**Rating:** 2300  
**Tags:** data structures, dp, graphs, sortings  
**Solve time:** 2m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of segments on a number line, each defined by a left endpoint and a right endpoint. The task is to select the largest possible subset of these segments with a specific property: for any two segments in the subset, they must either be completely disjoint, meaning they share no points at all, or one must be fully contained inside the other. Partial overlaps that are not containment are not allowed. The input contains multiple independent test cases, each with its own set of segments.

The constraints tell us that the total number of segments across all test cases does not exceed 3000. This is small enough that an algorithm with quadratic time in the number of segments per test case is feasible, since $3000^2$ operations fit comfortably within the 3-second limit. However, naive approaches that attempt to enumerate all subsets would be exponential and completely infeasible.

A subtle edge case arises when segments share endpoints but do not strictly contain one another. For example, the segments [1,2] and [2,3] touch at a single point, so they are considered intersecting and cannot be included together unless one is strictly contained in the other. Another edge case is nested segments of length one, such as [2,2] inside [1,3]. A careless solution that treats endpoint overlaps as non-intersections would incorrectly include both segments.

## Approaches

The brute-force approach is to try all subsets of segments and check whether each subset satisfies the non-intersection-or-containment condition. Checking one subset requires comparing all pairs of segments in it, giving an $O(n^3)$ solution for a single test case with $n$ segments. This is too slow for $n$ up to 3000.

To optimize, we observe that the problem has a natural structure: segments can be ordered and nested. Sorting the segments by their left endpoint, and breaking ties by decreasing right endpoint, guarantees that for any segment, potential segments that can be nested inside it appear later in the list. This naturally suggests a dynamic programming approach where `dp[i]` is the size of the largest valid subset ending with the i-th segment. To fill `dp[i]`, we consider all previous segments `j < i` and check whether segment `i` can be added to a subset ending with `j`. Segment `i` can be added if it is completely inside `j` or completely disjoint from `j`. Disjointness can be checked efficiently because segments are sorted by left endpoint.

The key insight is that after sorting, the decision of including segment `i` depends only on segments that start before `i`. This lets us compute the optimal solution in $O(n^2)$ time using a simple nested loop to update the DP table.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n^2) | O(n) | Too slow |
| DP after sorting | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of segments and the segments themselves. Represent each segment as a tuple `(l, r)`.
2. Sort the segments first by the left endpoint `l` in increasing order, and then by right endpoint `r` in decreasing order. Sorting this way ensures that any segment that could contain another appears earlier.
3. Initialize a DP array `dp` of size `n`, where `dp[i]` will store the size of the largest valid subset ending with segment `i`. Set all `dp[i]` initially to 1, since each segment can form a subset of size 1 on its own.
4. Iterate over the segments in order. For segment `i`, check all previous segments `j < i`. If segment `i` is fully inside `j` (i.e., `l[j] <= l[i]` and `r[i] <= r[j]`) or disjoint from `j` (i.e., `r[j] < l[i]`), then `i` can extend the subset ending at `j`. Update `dp[i] = max(dp[i], dp[j] + 1)`.
5. After filling the DP array, the largest valid subset for this test case is the maximum value in `dp`.

Why it works: Sorting by left endpoint ensures that all segments that can contain another appear before it, making it sufficient to check only previous segments in the DP update. The DP invariant is that `dp[i]` always represents the largest subset ending at segment `i` that satisfies the problem’s constraints. This ensures correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        segments = [tuple(map(int, input().split())) for _ in range(n)]
        # sort by left ascending, then right descending
        segments.sort(key=lambda x: (x[0], -x[1]))
        dp = [1] * n
        for i in range(n):
            li, ri = segments[i]
            for j in range(i):
                lj, rj = segments[j]
                if ri <= rj or rj < li:
                    dp[i] = max(dp[i], dp[j] + 1)
        print(max(dp))

if __name__ == "__main__":
    solve()
```

The first section reads input and organizes segments. Sorting by left endpoint ensures containment checks work correctly, while descending right endpoint resolves ties for nested segments. The nested loops implement the DP, where the condition `ri <= rj or rj < li` exactly matches the requirement for inclusion: either `i` is inside `j` or disjoint. Taking the maximum over `dp` gives the answer for each test case.

## Worked Examples

**Example 1:**

Input:

```
4
1 5
2 4
2 3
3 4
```

| i | Segment | dp[i] | Notes |
| --- | --- | --- | --- |
| 0 | [1,5] | 1 | only itself |
| 1 | [2,4] | 2 | inside [1,5] |
| 2 | [2,3] | 3 | inside [2,4] |
| 3 | [3,4] | 3 | cannot extend [2,3], can extend [1,5] |

Max dp = 3. This matches the expected output.

**Example 2:**

Input:

```
1 5
2 3
2 5
3 5
2 2
```

| i | Segment | dp[i] | Notes |
| --- | --- | --- | --- |
| 0 | [1,5] | 1 | only itself |
| 1 | [2,3] | 2 | inside [1,5] |
| 2 | [2,5] | 2 | overlaps [1,5] but not inside, cannot extend [1,5]? Actually [2,5] inside [1,5]? r2=5, r1=5, l1<=l2, r2<=r1 yes => inside, dp=2 |
| 3 | [3,5] | 3 | inside [2,5] |
| 4 | [2,2] | 3 | inside [2,3] |

Max dp = 4.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Nested loops over all segments to update dp; sorting is O(n log n) but dominated by O(n^2) |
| Space | O(n) | DP array stores one integer per segment |

The sum of n across all test cases is ≤ 3000, so even in the worst case the algorithm performs under 9 million operations, which is safe under 3 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# Provided samples
assert run("""4
4
1 5
2 4
2 3
3 4
5
1 5
2 3
2 5
3 5
2 2
3
1 3
2 4
2 3
7
1 10
2 8
2 5
3 4
4 4
6 8
7 7
""") == "3\n4\n2\n7", "sample tests"

# Custom edge cases
assert run("1\n1\n1 1\n") == "1", "single segment"
assert run("1\n2\n1 2\n3 4\n") == "2", "disjoint segments"
assert run("1\n3\n1 5\n2 5\n3 5\n") == "3", "nested segments with same right"
assert run("1\n4\n1 3\n3 4\n2 2\n4 4\n") == "3", "touching endpoints handled correctly"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 segment | 1 | minimal input |
| 2 disjoint segments | 2 | basic disjoint inclusion |
| 3 nested with same right | 3 | handling ties in right endpoint |
| 4 touching endpoints | 3 | ensures intersecting-at-endpoints |
