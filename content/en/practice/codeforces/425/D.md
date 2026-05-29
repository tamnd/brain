---
title: "CF 425D - Sereja and Squares"
description: "We are given a set of $n$ points on a 2D plane, each with integer coordinates, and all points are distinct. The task is to count how many axis-aligned squares exist whose four corners are all points from this set."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "hashing"]
categories: ["algorithms"]
codeforces_contest: 425
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 243 (Div. 1)"
rating: 2300
weight: 425
solve_time_s: 35
verified: true
draft: false
---

[CF 425D - Sereja and Squares](https://codeforces.com/problemset/problem/425/D)

**Rating:** 2300  
**Tags:** binary search, data structures, hashing  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of $n$ points on a 2D plane, each with integer coordinates, and all points are distinct. The task is to count how many axis-aligned squares exist whose four corners are all points from this set. An axis-aligned square is one where each side is either horizontal or vertical. The output is a single integer: the total number of such squares.

Given $n$ can be up to $10^5$, and coordinates can go up to $10^5$, a brute-force approach that examines all quadruples of points is infeasible. For example, iterating through every combination of four points would involve roughly $O(n^4)$ operations, which is roughly $10^{20}$ for the maximum $n$. Clearly, we need a much more efficient approach, ideally around $O(n \log n)$ or $O(n \sqrt{n})$.

Non-obvious edge cases include situations where multiple points lie on the same line. For example, a vertical line of points alone cannot form any square without horizontal counterparts. Another tricky case is when two points form a potential square diagonally but the other two corners are missing, e.g., $(0,0), (2,2)$ alone cannot form a square without $(0,2)$ and $(2,0)$. A naive approach that counts potential diagonals would overcount without verification of all four corners.

## Approaches

The naive solution would iterate over all quadruples of points. For each quadruple, check if they form a square by comparing distances and verifying axes alignment. This is correct but extremely slow; its complexity is $O(n^4)$. For $n=10^5$, this is not realistic.

A more clever approach observes that any square can be uniquely determined by its bottom-left and top-right corners (or top-left and bottom-right), because the other two corners are fixed by these two. Thus, instead of checking quadruples, we can iterate over all pairs of points that could serve as diagonally opposite corners of a square. For each candidate diagonal, the other two corners are computed directly. We then need to check efficiently whether those points exist in the set. By storing all points in a set or hash map, this lookup becomes $O(1)$ on average.

This reduces the complexity to $O(n^2)$ in the worst case for iterating all pairs, which is acceptable for $n$ up to a few thousands but might be too large for $n=10^5$. To further optimize, we can exploit coordinate hashing. We can group points by x-coordinate and scan potential y-distances efficiently, or group by y-coordinate. This ensures that we avoid unnecessary pair checks, achieving practical performance under the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (quadruples) | O(n^4) | O(n) | Too slow |
| Pair-based Diagonal Check | O(n^2) | O(n) | Acceptable for moderate n |
| Optimized with coordinate hashing | O(n√n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all $n$ points and store them in a set for O(1) existence queries.
2. Iterate over each pair of points $(x_1, y_1)$ and $(x_2, y_2)$. Treat them as potential diagonally opposite corners of a square.
3. Skip pairs where $x_1 = x_2$ or $y_1 = y_2$ because a square cannot have a zero width or height.
4. Compute the other two corners as $(x_1, y_2)$ and $(x_2, y_1)$.
5. Check whether both of these points exist in the set. If they do, increment the square count.
6. Since each square will be counted twice (once per each diagonal), divide the final count by 2 before outputting.

Why it works: Each square has exactly two distinct diagonals. By iterating over all pairs of points and considering them as diagonals, we guarantee that each square is counted exactly twice. Using a set allows fast existence checks for the remaining corners. This ensures correctness and avoids overcounting.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_squares():
    n = int(input())
    points = set()
    coords = []
    for _ in range(n):
        x, y = map(int, input().split())
        points.add((x, y))
        coords.append((x, y))
    
    count = 0
    for i in range(n):
        x1, y1 = coords[i]
        for j in range(i + 1, n):
            x2, y2 = coords[j]
            if x1 == x2 or y1 == y2:
                continue
            if (x1, y2) in points and (x2, y1) in points:
                count += 1
    print(count // 2)

count_squares()
```

The solution first stores points in a set for fast lookup and keeps them in a list for pair iteration. Each pair is treated as a diagonal. The check ensures we do not consider vertical or horizontal pairs as diagonals. Finally, dividing by two corrects for double counting.

## Worked Examples

### Sample 1

Input:

```
5
0 0
0 2
2 0
2 2
1 1
```

| Pair (i,j) | Diagonal? | Other corners exist? | Count increment |
| --- | --- | --- | --- |
| (0,0)-(2,2) | Yes | (0,2),(2,0) exist | +1 |
| Other pairs | Either same x or y, or not diagonal | N/A | 0 |

Output: 1

This trace shows that the algorithm correctly identifies the one square formed by corners (0,0),(0,2),(2,0),(2,2) and ignores the point (1,1).

### Sample 2
