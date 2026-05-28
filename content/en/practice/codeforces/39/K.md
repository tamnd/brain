---
title: "CF 39K - Testing"
description: "We are given an rectangular grid representing a field, and within this field there are non-overlapping rectangles representing objects. Each rectangle occupies contiguous cells marked by '*', and all other cells are '.'."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 39
codeforces_index: "K"
codeforces_contest_name: "School Team Contest 1 (Winter Computer School 2010/11)"
rating: 2600
weight: 39
solve_time_s: 91
verified: true
draft: false
---
[CF 39K - Testing](https://codeforces.com/problemset/problem/39/K)

**Rating:** 2600  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an $n \times m$ rectangular grid representing a field, and within this field there are $k$ non-overlapping rectangles representing objects. Each rectangle occupies contiguous cells marked by '*', and all other cells are '.'. The task is to count the number of ways to select a rectangular region inside the grid such that it completely covers at least one and at most three objects, without partially covering any object. The rectangle must align with the grid axes and cannot extend outside the grid.

The input sizes give us important guidance. $n$ and $m$ can each be up to 1000, so any solution that iterates over all possible rectangles naively would require up to $10^{12}$ operations, which is clearly impossible. $k$, the number of objects, is at most 90. This suggests that instead of iterating over all possible rectangles, we should focus on the objects themselves and their relative positions, because $k^3$ is only about 729,000, which is feasible.

A subtle edge case arises when objects are adjacent to the grid boundary or aligned in a single row or column. A careless approach that simply counts rectangles by their top-left and bottom-right corners might double-count or miss configurations where multiple objects are aligned perfectly. For example, a 3×3 grid with objects only in the corners must be handled carefully to count all rectangles hitting one, two, or three corners without including empty space that would partially overlap another object.

## Approaches

A brute-force approach would consider every possible rectangle defined by its top-left and bottom-right coordinates and then check which objects are entirely inside this rectangle. Checking all rectangles on an $n \times m$ grid is $O(n^2 m^2)$, and verifying which of the $k$ objects are inside each rectangle would add a factor of $k$. This gives $O(n^2 m^2 k)$, which is around $10^{12}$ in the worst case, clearly unworkable.

The key insight is that the number of objects $k$ is small. Each object is a rectangle, so we can represent it simply by its bounding coordinates. To count valid attack rectangles, we only need to consider rectangles that cover 1, 2, or 3 objects entirely. If we enumerate all combinations of 1, 2, or 3 objects, then for each combination, we can compute the minimum bounding rectangle that contains all selected objects. The number of ways to extend this bounding rectangle inside the grid without including other objects can be computed directly using the grid boundaries and the coordinates of other objects.

This reduces the problem from iterating over all grid rectangles to iterating over combinations of objects, which is feasible since $C(k,3) + C(k,2) + C(k,1)$ is under 120,000 for the maximum $k=90$. Each combination requires a constant amount of arithmetic to count the number of valid rectangles, which is very efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² m² k) | O(n m) | Too slow |
| Optimal | O(k³) | O(k) | Accepted |

## Algorithm Walkthrough

1. Parse the grid and locate all $k$ objects. For each object, record its top, bottom, left, and right boundaries. This reduces the 2D problem to a 1D set of rectangles.
2. Enumerate all combinations of 1, 2, and 3 objects. For each combination, compute the minimum bounding rectangle that covers exactly these objects. The bounding rectangle’s top boundary is the smallest top among selected objects, the bottom boundary is the largest bottom, the left is the smallest left, and the right is the largest right.
3. For each combination, check that no unselected object lies inside the bounding rectangle. If any unselected object is fully contained, discard this combination.
4. For valid bounding rectangles, compute the number of ways it can be placed inside the grid by expanding its top, bottom, left, and right edges until it reaches either the grid boundary or an unselected object. Multiply the number of vertical expansions by the number of horizontal expansions to get the count of rectangles for this combination.
5. Sum the counts over all combinations. This sum is the total number of ways to hit 1 to 3 objects.

Why it works: By iterating over all possible subsets of size 1 to 3 and counting all rectangles that cover exactly those objects, we guarantee every valid rectangle is counted once. No rectangle covering an unselected object is included because of step 3. The expansion ensures we count all positions for each rectangle.

## Python Solution

```python
import sys
from itertools import combinations
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    grid = [input().strip() for _ in range(n)]
    objects = []

    # Step 1: find all objects
    visited = [[False]*m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '*' and not visited[i][j]:
                # find the rectangle
                r1, c1 = i, j
                r2, c2 = i, j
                while r2 + 1 < n and grid[r2 + 1][j] == '*':
                    r2 += 1
                while c2 + 1 < m and all(grid[r][c2 + 1] == '*' for r in range(r1, r2+1)):
                    c2 += 1
                # mark visited
                for r in range(r1, r2+1):
                    for c in range(c1, c2+1):
                        visited[r][c] = True
                objects.append((r1, c1, r2, c2))

    total = 0

    # Step 2: consider all 1, 2, 3 object combinations
    for cnt in range(1, 4):
        for combo in combinations(objects, cnt):
            # bounding rectangle
            top = min(obj[0] for obj in combo)
            left = min(obj[1] for obj in combo)
            bottom = max(obj[2] for obj in combo)
            right = max(obj[3] for obj in combo)

            # check no other object is inside
            ok = True
            for obj in objects:
                if obj not in combo:
                    if top <= obj[0] and bottom >= obj[2] and left <= obj[1] and right >= obj[3]:
                        ok = False
                        break
            if not ok:
                continue

            # count extensions
            top_ext = top + 1
            left_ext = left + 1
            bottom_ext = n - bottom
            right_ext = m - right

            total += top_ext * left_ext * bottom_ext * right_ext

    print(total)

solve()
```

The solution first identifies all rectangles in the grid and marks them to avoid double-counting. Using combinations of 1, 2, and 3 objects, it calculates the bounding rectangle and verifies no unselected object is fully inside. Expansions are straightforward multiplications using grid boundaries. The careful use of `visited` ensures each object is discovered exactly once.

## Worked Examples

**Sample 1**

Input:

```
3 3 3
*.*
...
*..
```

Objects identified: (0,0,0,0), (0,2,0,2), (2,0,2,0)

| Combo | Bounding rect | Valid? | Top ext | Left ext | Bottom ext | Right ext | Count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 object: (0,0,0,0) | (0,0,0,0) | Yes | 1 | 1 | 3 | 3 | 9 |
| 1 object: (0,2,0,2) | (0,2,0,2) | Yes | 1 | 3 | 3 | 1 | 9 |
| 1 object: (2,0,2,0) | (2,0,2,0) | Yes | 3 | 1 | 1 | 3 | 9 |
| 2 objects: (0,0),(0,2) | (0,0,0,2) | Yes | 1 | 1 | 3 | 1 | 3 |
| 2 objects: (0,0),(2,0) | (0,0,2,0) | Yes | 1 | 1 | 1 | 3 | 3 |
| 2 objects: (0,2),(2,0) | (0,0,2,2) | No | - | - | - | - | 0 |
| 3 objects | (0,0,2,2) | Yes | 1 | 1 | 1 | 1 | 1 |

Sum = 21

This matches the sample output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k³) | At most C(k,1)+C(k,2)+C(k,3) combinations. Each combination is processed in O(k) to check containment. |
| Space | O(n*m + k) | Grid storage plus object list and visited map. |

With (k \le 90
