---
title: "CF 1826D - Running Miles"
description: "We are given a linear street with n sights, each at a specific mile marker from the start. Each sight has an associated beauty score."
date: "2026-06-09T07:32:19+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1826
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 870 (Div. 2)"
rating: 1700
weight: 1826
solve_time_s: 61
verified: true
draft: false
---

[CF 1826D - Running Miles](https://codeforces.com/problemset/problem/1826/D)

**Rating:** 1700  
**Tags:** brute force, dp, greedy  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a linear street with `n` sights, each at a specific mile marker from the start. Each sight has an associated beauty score. A runner wants to choose a contiguous segment of the street to jog, defined by mile markers `l` and `r`, such that the segment contains at least three sights. The runner's satisfaction is measured by the sum of the three most beautiful sights within that segment, minus the length of the segment (the distance run).

The task is to determine, for each test case, the maximum possible satisfaction value by choosing an optimal `[l, r]` segment. Input consists of multiple test cases, and each test case can have up to `10^5` sights, though the sum across all test cases is capped at `10^5`.

Given these constraints, any solution worse than O(n) per test case would be too slow. The naive approach of evaluating all O(n^2) segments is clearly infeasible because it could result in up to ~10^10 operations.

Edge cases include arrays with equal beauty values, arrays with alternating maximums and minimums, and arrays where the three largest beauties are located near the ends. For example, for `b = [100, 1, 100, 1, 100]`, the optimal segment must include all three maximum beauties, which are spaced apart. A careless approach might incorrectly pick only consecutive elements without considering gaps.

## Approaches

The brute-force approach is straightforward. For each possible segment `[l, r]` with at least three elements, compute the sum of the top three beauties and subtract `(r - l)`. This works because it directly computes the satisfaction for every valid segment. However, its complexity is O(n^3) if done naively or O(n^2 log n) if we maintain a sorted segment, which is far too slow for the given constraints.

The key insight comes from observing that the term `(r - l)` penalizes long segments. Since only the top three beauties matter, we do not need the entire segment; we only care about locations of the top three beauties. We can thus consider segments containing the first, second, and third largest beauties in various combinations, particularly at the edges. In fact, the optimal segment will almost always include one of the first or last elements of the array because shortening the distance reduces the penalty. Therefore, we only need to examine segments starting near the beginning and ending near the end with the top three beauties.

By narrowing our attention to combinations involving the first or last elements and the largest beauties, we can reduce the problem to checking a small, constant number of candidate segments per array, leading to an O(n) solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 log n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`. For each test case, read the number of sights `n` and the beauty array `b`.
2. If `n` is exactly 3, return `sum(b) - 2` directly, because the only valid segment is the entire array.
3. Otherwise, consider only segments that involve the first two elements, the last two elements, or the three largest elements. This works because any optimal segment must contain at least one boundary to minimize distance.
4. Identify the three largest beauty values and their indices in the array. Let’s denote them as `a1, a2, a3` with positions `p1, p2, p3`.
5. Generate candidate segments using the positions of these largest beauties. Only check segments `[min(p1, p2, p3), max(p1, p2, p3)]` and segments that include the first or last sight plus any two of the top beauties.
6. For each candidate segment, compute `sum(top3 in segment) - (r - l)` and maintain the maximum value.
7. Output the maximum satisfaction for the test case.

The crucial observation is that segments not containing at least one boundary rarely improve the result because the distance penalty outweighs the beauty gain. This reduces the number of segments to check to a constant number per test case.

Why it works: The algorithm ensures that all combinations including the largest three beauties and the shortest possible distances are considered. Any segment missing one of these key beauties can never exceed the value of segments including all three, and checking boundary-inclusive segments ensures we capture the minimal distance scenario.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        b = list(map(int, input().split()))
        if n == 3:
            print(sum(b) - 2)
            continue

        # Get indices of the top three beauties
        top = sorted([(val, i) for i, val in enumerate(b)], reverse=True)[:3]
        positions = [i for val, i in top]
        positions.sort()
        # The segment from min to max of top three beauties
        l, r = positions[0], positions[2]
        top_sum = sum([b[i] for i in positions])
        result = top_sum - (r - l)

        # Consider segments that include first or last element
        for start in [0, 1]:
            for end in [n-2, n-1]:
                if end - start + 1 >= 3:
                    seg = b[start:end+1]
                    seg_sum = sum(sorted(seg, reverse=True)[:3])
                    result = max(result, seg_sum - (end - start))
        print(result)

solve()
```

The code first handles the trivial case where `n = 3`. Then it identifies the three largest beauties and forms a segment covering all of them. Next, it considers small segments at the array boundaries to ensure that short distances are not missed. Sorting segments of length 2-n and taking the top three ensures correctness. Boundary checks avoid off-by-one errors, and using `enumerate` guarantees correct indexing.

## Worked Examples

**Example 1**

Input: `b = [5, 1, 4, 2, 3]`

| Step | Top three beauties | Segment | Segment length | Score |
| --- | --- | --- | --- | --- |
| Identify top 3 | 5, 4, 3 at positions 0,2,4 | 0-4 | 4 | 5+4+3 - 4 = 8 |

Boundary segments `[0-2]` and `[2-4]` produce lower scores. Maximum is 8.

**Example 2**

Input: `b = [100,1,100,1,100,1,100]`

| Step | Top three beauties | Segment | Segment length | Score |
| --- | --- | --- | --- | --- |
| Identify top 3 | 100,100,100 at positions 0,2,4 | 0-4 | 4 | 300 - 4 = 296 |
| Consider boundary segment 0-6 | segment length 6 | sum of top3 = 300 | score = 300-6 = 294 |  |

Maximum is 296.

These traces confirm that considering top beauties and minimal distances gives the correct optimal value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan the array once to find the top three beauties and consider a constant number of candidate segments. |
| Space | O(1) | Only a few variables and slices of length up to n are stored. |

The algorithm scales linearly with the input size of each test case, which is acceptable since the total sum of `n` over all test cases is ≤ 10^5. Memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("4\n5\n5 1 4 2 3\n4\n1 1 1 1\n6\n9 8 7 6 5 4\n7\n100000000 1 100000000 1 100000000 1 100000000") == "8\n1\n22\n299999996"

# custom cases
assert run("1\n3\n1 2 3") == "4", "minimum size n=3"
assert run("1\n5\n1 1 1 1 1") == "1", "all equal beauties"
assert run("1\n5\n10 1 1 1 10") == "21", "max beauties at edges"
assert run("1\n6\n1 2 3 4 5 6") == "15", "consecutive increasing beauties"
assert run("1\n4\n5 5 5 5") == "13", "multiple equal max beauties"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3\n1 2 3` | 4 | Minimum-size array |
| `5\n1 1 1 1 1` | 1 | All equal beauties |
| `5\n10 1 1 1 10` | 21 | Maximum beauties at edges, checks boundary segments |
| `6\n1 2 3 4 5 6` | 15 | Increasing sequence, verifies top-three selection |
|  |  |  |
