---
title: "CF 105530C - Too Much Walking"
description: "We are given a collection of points on a 2D grid, where each point can be thought of as a cell with integer coordinates. For every point, we want to determine how far it is from the farthest other point, where distance is measured using Manhattan distance."
date: "2026-06-23T22:58:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105530
codeforces_index: "C"
codeforces_contest_name: "Metropolitan University Inter University Programming Contest - Sylhet Division 2024"
rating: 0
weight: 105530
solve_time_s: 50
verified: true
draft: false
---

[CF 105530C - Too Much Walking](https://codeforces.com/problemset/problem/105530/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of points on a 2D grid, where each point can be thought of as a cell with integer coordinates. For every point, we want to determine how far it is from the farthest other point, where distance is measured using Manhattan distance. The Manhattan distance between two points is the sum of absolute differences of their x and y coordinates.

The task is to compute, for each point, the maximum Manhattan distance to any other point in the set, and output these maximum values.

The constraint structure is what makes this interesting. If there are up to n points, a direct pairwise comparison implies checking all pairs, which leads to n squared behavior. For n around 200,000 or even 2000 depending on version, n squared is already infeasible, since it would involve billions or trillions of operations. That immediately rules out any solution that explicitly compares each point to every other point.

A naive implementation might also stumble on absolute values. For example, trying to directly optimize by sorting points by x or y independently does not directly solve Manhattan distance, because both coordinates interact.

A subtle edge case arises when all points are identical or lie on a line. If all points are the same, the correct answer for every point is zero. If all points lie on a diagonal line like (i, i), the Manhattan distance becomes purely proportional to index differences, and incorrect simplifications that treat x and y independently may still appear to work on such structured inputs while failing on general cases.

For instance, consider points (0, 0), (1, 2), (3, 1). A naive projection onto x or y alone does not capture that the farthest point depends on a combined expression, not independent maxima.

## Approaches

The main difficulty is the absolute value in the Manhattan distance formula. For two points (x, y) and (a, b), the distance is |x − a| + |y − b|. The brute force approach directly computes this value for every pair and keeps track of maxima per point. This is correct because it follows the definition exactly, but it costs O(n²) distance computations, each constant time, which is too slow when n is large.

The key observation is that absolute value expressions can be expanded into a finite set of linear forms depending on sign choices. For a single absolute difference, |x − a| can be rewritten as max(x − a, a − x). Extending this idea, the Manhattan distance becomes the maximum over four linear expressions, each corresponding to a choice of signs for x and y differences. This converts a non-linear metric into a set of linear functions.

Once rewritten in this form, the problem changes fundamentally. Instead of comparing every pair of points directly, we only need to evaluate a small fixed number of linear expressions over all points. For each of these expressions, we can precompute the maximum value across all points. Then, for each point, we evaluate its contribution under each expression and combine it with the precomputed global maxima.

This works because each Manhattan distance instance corresponds to exactly one of these sign configurations, and the maximum over all points must appear in one of these linear forms.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We convert each point into contributions under different sign patterns, then use global extrema to answer queries in constant time per point.

1. For each point (x, y), compute four transformed values corresponding to sign combinations: x + y, x − y, −x + y, and −x − y. Each expression represents one way absolute values can resolve when expanded.
2. For each of these four expressions, scan all points and compute the maximum value. These represent the best possible partner point contribution under each sign configuration. This step isolates global structure so we do not need pairwise comparisons later.
3. For each point (x, y), compute the value of each of the four expressions at that point.
4. For each expression, compute the candidate answer by subtracting the point’s own value from the precomputed maximum of that expression. This simulates pairing the point with the best possible opposite-sign partner.
5. Take the maximum over the four candidates. This gives the farthest Manhattan distance for that point.

The reason subtraction appears is that each linear form effectively encodes the distance as a difference between two transformed point values, so pairing reduces to maximizing that difference.

### Why it works

The Manhattan distance decomposes into a maximum over a fixed set of linear functions derived from independent sign choices on x and y differences. Every pair of points contributes its distance under exactly one of these forms. By precomputing the maximum value of each form globally, we ensure that for any fixed point, the best possible partner under each form is already known. Taking the maximum across forms reconstructs the true maximum distance because every valid pair is covered by exactly one of the forms.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]

    INF = 10**18
    max1 = -INF  # x + y
    max2 = -INF  # x - y
    max3 = -INF  # -x + y
    max4 = -INF  # -x - y

    for x, y in pts:
        max1 = max(max1, x + y)
        max2 = max(max2, x - y)
        max3 = max(max3, -x + y)
        max4 = max(max4, -x - y)

    for x, y in pts:
        ans = 0
        ans = max(ans, max1 - (x + y))
        ans = max(ans, max2 - (x - y))
        ans = max(ans, max3 - (-x + y))
        ans = max(ans, max4 - (-x - y))
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution first aggregates global extrema for the four transformed coordinate systems. Each of these extrema corresponds to the best possible endpoint under a fixed sign configuration.

In the second pass, each point computes how far it can stretch in each transformed system by subtracting its own contribution. The subtraction is critical because it converts absolute pair selection into a difference maximization problem.

A common implementation mistake is to recompute maxima while iterating answers, which accidentally allows a point to pair with itself in a way that can distort reasoning in corner cases. Precomputing ensures consistency across all queries.

Another subtle issue is forgetting that the four transformations are sufficient; adding more or fewer expressions breaks completeness of the absolute value decomposition.

## Worked Examples

Consider points (0, 0), (2, 3), (5, 1).

We compute transformed values:

| Point | x+y | x−y | −x+y | −x−y |
| --- | --- | --- | --- | --- |
| (0,0) | 0 | 0 | 0 | 0 |
| (2,3) | 5 | -1 | 1 | -5 |
| (5,1) | 6 | 4 | -4 | -6 |

Global maxima are max1 = 6, max2 = 4, max3 = 1, max4 = 0.

Now compute answers:

| Point | max1-(x+y) | max2-(x−y) | max3-(-x+y) | max4-(-x−y) | Answer |
| --- | --- | --- | --- | --- | --- |
| (0,0) | 6 | 4 | 1 | 0 | 6 |
| (2,3) | 1 | 5 | 0 | 5 | 5 |
| (5,1) | 0 | 0 | 5 | 6 | 6 |

This confirms that each point finds its farthest partner without explicit pair enumeration.

A second example with symmetric structure: (1,1), (1,1), (1,1). All transformed values are identical, so every max minus self is zero. The output correctly becomes all zeros, confirming correctness on degenerate inputs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Two linear passes over points with constant work per point |
| Space | O(1) | Only a few running maxima are stored |

The algorithm fits comfortably within typical constraints for large coordinate sets because it avoids pairwise distance computation entirely. Even for n up to 200,000, the solution performs only a few simple arithmetic operations per point.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out_lines = []

    n = int(sys.stdin.readline())
    pts = [tuple(map(int, sys.stdin.readline().split())) for _ in range(n)]

    INF = 10**18
    max1 = max(x + y for x, y in pts)
    max2 = max(x - y for x, y in pts)
    max3 = max(-x + y for x, y in pts)
    max4 = max(-x - y for x, y in pts)

    res = []
    for x, y in pts:
        ans = max(
            max1 - (x + y),
            max2 - (x - y),
            max3 - (-x + y),
            max4 - (-x - y),
        )
        res.append(str(ans))
    return "\n".join(res)

# sample-like
assert run("3\n0 0\n2 3\n5 1\n") == "6\n5\n6"

# single point
assert run("1\n10 10\n") == "0"

# all equal
assert run("3\n1 1\n1 1\n1 1\n") == "0\n0\n0"

# line structure
assert run("3\n0 0\n1 1\n2 2\n") == "4\n2\n4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point | 0 | trivial base case |
| all equal points | all zeros | duplicate handling |
| diagonal line | symmetric distances | structured geometry correctness |

## Edge Cases

For a single point input like (10, 10), the algorithm computes all transformed maxima as 20, 0, 0, -20 respectively. When subtracting the point’s own contribution, every expression evaluates to zero, producing the correct answer.

For all identical points, every transformed value is identical, so each max equals each point’s value. Subtraction cancels exactly, guaranteeing zero distances and confirming no self-pairing issues arise.

For points arranged on a diagonal such as (0,0), (1,1), (2,2), the transformation reduces to simple linear offsets. The algorithm still correctly captures maximum spread because each sign configuration collapses consistently, and the global maxima correctly represent endpoints of the line.
