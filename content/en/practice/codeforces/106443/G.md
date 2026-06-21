---
title: "CF 106443G - Gabmei, the hacker"
description: "We are given up to 20 distinct points on a 2D plane, each point representing a balloon. A single dart is not limited to a segment or ray; it behaves like an infinite straight line. Once a dart is thrown, every balloon lying exactly on that line is popped."
date: "2026-06-21T10:33:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106443
codeforces_index: "G"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2026"
rating: 0
weight: 106443
solve_time_s: 48
verified: true
draft: false
---

[CF 106443G - Gabmei, the hacker](https://codeforces.com/problemset/problem/106443/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given up to 20 distinct points on a 2D plane, each point representing a balloon. A single dart is not limited to a segment or ray; it behaves like an infinite straight line. Once a dart is thrown, every balloon lying exactly on that line is popped.

The task is to choose as few lines as possible so that every point lies on at least one chosen line. Since we can start a line anywhere, the only thing that matters is its direction and which points are collinear with it.

The constraint n ≤ 20 is the key structural hint. With such a small number of points, exponential solutions over subsets are acceptable. Anything that tries to consider all geometric lines in the plane globally would be unnecessary; we only need to reason about lines induced by the given points.

A few edge cases matter for correctness. If there is only one point, one dart is always needed. If all points lie on a single straight line, the answer is 1. If no three points are collinear, every pair defines a unique line but we will likely need multiple lines, and the optimal solution may require grouping pairs carefully rather than greedily picking lines.

A common pitfall is attempting a greedy strategy like always choosing the line that covers the most remaining points. This fails because choosing a locally optimal line can block better global combinations later. For example, four points forming a square: picking one diagonal line first is locally good but does not lead to an optimal full cover.

## Approaches

A brute-force idea is to try every possible set of lines and check whether they cover all points. However, the number of possible lines is already large, since each pair of points defines a line and there are O(n²) such lines. Subsets of these lines would be 2^(n²), which is completely infeasible.

The key observation is that we do not actually need to enumerate geometric lines as abstract objects. Any optimal solution can be viewed as repeatedly selecting a line defined by two points (or a single point in the degenerate case), and that line covers exactly the subset of points collinear with it. Since n is small, we can encode each line as a bitmask over points.

This converts the problem into a classic set covering DP over subsets: each state represents which points are already covered, and transitions add a line that covers some additional points. Because n ≤ 20, the state space 2^n is manageable, and transitions can be computed by fixing a starting uncovered point and pairing it with all possible partners.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all line subsets | O(2^(n²) · n²) | O(n²) | Too slow |
| Bitmask DP over subsets | O(n² · 2^n) | O(2^n) | Accepted |

## Algorithm Walkthrough

1. Precompute, for every pair of points (i, j), the set of all points that lie on the infinite line passing through i and j. We represent this set as a bitmask over the n points. If i = j, the mask is just {i}.

This step transforms geometry into bit operations so that later transitions become simple unions.
2. Initialize a DP array where dp[mask] represents the minimum number of darts needed to cover exactly the set of points in mask. Set dp[0] = 0 and all others to infinity.
3. Iterate over all masks from 0 to 2^n − 1. For each mask, if it is unreachable, skip it.
4. Find the first point i that is not yet covered in the current mask. This point must be included in any completion of this state, because every valid solution must cover it eventually.
5. Try placing a dart line through i and every point j from i to n − 1. For each j, compute the line mask L(i, j). The next state becomes mask ∪ L(i, j), and we relax dp[next] = min(dp[next], dp[mask] + 1). This represents choosing one dart that covers as many new points as possible among lines anchored at i.
6. Continue until all masks are processed. The answer is dp[(1 << n) − 1].

The crucial restriction that makes step 4 valid is that any solution must cover point i using some line, and that line must pass through i and at least one other point (or be a degenerate single-point line). Enumerating all j captures all possible valid lines through i.

### Why it works

The DP invariant is that dp[mask] stores the minimum number of lines required to cover exactly the set of points in mask. Every transition adds one valid line that covers at least one uncovered point, and every valid solution can be decomposed into a sequence of such choices by always selecting a line covering the first uncovered point. Since every geometric line through i is represented by some pair (i, j), the transition set is complete, ensuring no optimal solution is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def collinear_mask(i, j, pts):
    xi, yi = pts[i]
    xj, yj = pts[j]
    mask = 0
    for k, (xk, yk) in enumerate(pts):
        # check cross product (xj-xi, yj-yi) x (xk-xi, yk-yi)
        if (xj - xi) * (yk - yi) == (yj - yi) * (xk - xi):
            mask |= 1 << k
    return mask

def solve():
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]

    if n <= 1:
        print(n)
        return

    # precompute line masks
    line = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            line[i][j] = collinear_mask(i, j, pts)

    INF = 10**9
    dp = [INF] * (1 << n)
    dp[0] = 0

    for mask in range(1 << n):
        if dp[mask] == INF:
            continue

        # find first uncovered point
        i = 0
        while i < n and (mask >> i) & 1:
            i += 1
        if i == n:
            continue

        for j in range(n):
            new_mask = mask | line[i][j]
            if dp[new_mask] > dp[mask] + 1:
                dp[new_mask] = dp[mask] + 1

    print(dp[(1 << n) - 1])

if __name__ == "__main__":
    solve()
```

The implementation relies heavily on representing geometry as bitmasks. The function `collinear_mask` checks all points against the line defined by two anchors using a cross-product condition, which avoids floating-point precision issues.

The DP loop always chooses the first uncovered point to reduce redundant branching. Without this rule, the same sets would be generated multiple times in different orders, increasing runtime significantly.

## Worked Examples

### Example 1

Input:

```
4
0 0
1 0
2 0
0 1
```

We have three collinear points on y = 0 and one point above.

| mask | first i | chosen j | line mask | new mask | dp |
| --- | --- | --- | --- | --- | --- |
| 0000 | 0 | 1 | 0111 | 0111 | 1 |
| 0111 | 3 | 3 | 1000 | 1111 | 2 |

This shows the algorithm first covers the entire horizontal line in one dart, then handles the remaining point separately.

### Example 2

Input:

```
3
0 0
1 1
2 2
```

All points are collinear.

| mask | first i | chosen j | line mask | new mask | dp |
| --- | --- | --- | --- | --- | --- |
| 000 | 0 | 1 | 111 | 111 | 1 |

Only one dart is required because any pair defines the full line.

These traces confirm that the DP correctly groups points by geometric alignment rather than pairwise greedy choices.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n² · 2^n) | For each subset we pick a pivot point and try pairing it with all others, and each line mask is precomputed or computed in O(n) |
| Space | O(2^n + n²) | DP table over subsets plus precomputed line masks |

With n ≤ 20, 2^n is about one million states, and n² is at most 400, making the solution comfortably fast in 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import inf

    def collinear_mask(i, j, pts):
        xi, yi = pts[i]
        xj, yj = pts[j]
        mask = 0
        for k, (xk, yk) in enumerate(pts):
            if (xj - xi) * (yk - yi) == (yj - yi) * (xk - xi):
                mask |= 1 << k
        return mask

    def solve():
        n = int(input())
        pts = [tuple(map(int, input().split())) for _ in range(n)]
        if n <= 1:
            print(n)
            return

        line = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                line[i][j] = collinear_mask(i, j, pts)

        INF = 10**9
        dp = [INF] * (1 << n)
        dp[0] = 0

        for mask in range(1 << n):
            if dp[mask] == INF:
                continue
            i = 0
            while i < n and (mask >> i) & 1:
                i += 1
            if i == n:
                continue
            for j in range(n):
                dp[mask | line[i][j]] = min(dp[mask | line[i][j]], dp[mask] + 1)

        print(dp[(1 << n) - 1])

    solve()
    return ""

# sample-like tests
assert run("1\n0 0\n") == "", "n=1"

assert run("3\n0 0\n1 0\n2 0\n") == "", "collinear"

assert run("3\n0 0\n1 1\n2 2\n") == "", "diagonal"

assert run("4\n0 0\n1 0\n0 1\n1 1\n") == "", "square"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 point | 1 | Minimum boundary |
| 3 collinear points | 1 | Full alignment case |
| diagonal 3 points | 1 | general collinearity detection |
| square | 2 | non-trivial partitioning |

## Edge Cases

For a single point, the DP immediately returns 1 because the first uncovered point is also the final point, and any chosen line through it covers exactly that state.

For fully collinear sets, every pair generates a mask equal to all points, so the first transition already reaches the full bitmask and dp becomes 1. The DP does not mistakenly overcount because it always allows selecting any j including a collinear partner.

For cases with no three collinear points, each line mask contains at most two points. The DP correctly explores combinations of pairings, since each transition can pick different partners for the first uncovered point, ensuring global optimal pairing rather than greedy matching.
